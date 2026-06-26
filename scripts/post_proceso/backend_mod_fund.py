"""
Backend: Modelo de Fundación (Mod FUND)
=======================================
Automatiza la creación de un modelo de fundación a partir de un modelo
estructural analizado en SAP2000.

Flujo:
  1. check_analysis_done      — verifica modelo bloqueado (análisis completado)
  2. get_restricted_joints    — nodos con al menos un DOF restringido,
                                incluyendo coordenadas y valores de restraint
     get_load_combinations    — Load Combinations (RespCombo) definidos en el modelo
     get_joint_reactions      — reacciones nodales por Load Combination
  3. build_foundation_model   — crea modelo nuevo en blanco, recrea nodos
                                de apoyo en sus coordenadas originales,
                                crea un Load Pattern por cada combo y asigna
                                las reacciones (×-1) como Joint Loads

Dependencias: comtypes, stdlib
Sin imports de mcp_server/ ni módulos internos del framework.

Notas sobre firmas COM (verificadas contra wrappers del registry):
  PointObj.AddCartesian(X, Y, Z, Name_byref, UserName)
    → [Name, ret_code]
  PointObj.SetRestraint(Name, Value[6]) → ret_code
  PointObj.SetLoadForce(Name, LoadPat, Value[6], Replace, CSys)
    → [Value_echoed[], ret_code]
  LoadPatterns.Add(Name, MyType, SelfWtMult, AddCase) → ret_code
  Results.JointReact(Name, ItemTypeElm=0, NRes, Obj, Elm,
      LC, StepType, StepNum, F1, F2, F3, M1, M2, M3) → [14 ByRef outs + ret_code]
  PointObj.GetCoordCartesian(Name, X, Y, Z, CSys) → [X, Y, Z, ret_code]
  PointObj.GetRestraint(Name, Value[]) → [values[6], ret_code]
  RespCombo.GetNameList(Count, Names[]) → [Count, Names[], ret_code]
  Results.Setup.SetComboSelectedForOutput(Name) → ret_code
"""

import os
import comtypes.client
from typing import List


# ══════════════════════════════════════════════════════════════════════════════
# Backend: Mod FUND
# ══════════════════════════════════════════════════════════════════════════════

class ModFundBackend:
    """
    Extrae reacciones del modelo analizado y construye el modelo de fundación.

    Uso típico:
        1. check_analysis_done()
        2. get_restricted_joints()
           get_load_combinations()
        3. get_joint_reactions(joint_names, combo_names)
        4. build_foundation_model(joints_data, reactions_rows)
    """

    def __init__(self, connection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión activa con SAP2000.")
        return self._conn.sap_model

    # ── Step 1: Verificar análisis ────────────────────────────────────────────

    def check_analysis_done(self) -> dict:
        """Retorna {locked: bool, success: bool}.

        SAP2000 bloquea el modelo al completar el análisis.
        GetModelIsLocked() puede retornar bool directamente o en tuple.
        """
        SapModel = self.sap_model
        result = SapModel.GetModelIsLocked()
        locked = bool(result[0]) if isinstance(result, (list, tuple)) else bool(result)
        return {"success": True, "locked": locked}

    # ── Step 2a: Nodos restringidos ───────────────────────────────────────────

    def get_restricted_joints(self) -> dict:
        """Obtiene joints con al menos un DOF restringido.

        Por cada joint devuelve nombre, coordenadas cartesianas globales
        y vector de restraints [6 bools], necesarios para recrearlos en
        el modelo de fundación.

        Returns:
            {
              success: bool,
              joints: list[{name, x, y, z, restraints: [6 bools]}],
              joint_names: list[str],
              count: int
            }
        """
        SapModel = self.sap_model

        raw = SapModel.PointObj.GetNameList(0, [])
        ret = raw[-1]
        assert ret == 0, f"PointObj.GetNameList failed: {ret}"

        n = raw[0]
        all_names = list(raw[1])[:n]

        joints = []
        for name in all_names:
            raw_r = SapModel.PointObj.GetRestraint(name, [])
            if raw_r[-1] != 0:
                continue
            restraints = list(raw_r[0])
            if not any(restraints):
                continue

            raw_c = SapModel.PointObj.GetCoordCartesian(
                name, 0.0, 0.0, 0.0, "Global"
            )
            if raw_c[-1] != 0:
                continue

            joints.append({
                "name":       name,
                "x":          float(raw_c[0]),
                "y":          float(raw_c[1]),
                "z":          float(raw_c[2]),
                "restraints": restraints,
            })

        return {
            "success":     True,
            "joints":      joints,
            "joint_names": [j["name"] for j in joints],
            "count":       len(joints),
        }

    # ── Step 2b: Load Combinations ────────────────────────────────────────────

    def get_load_combinations(self) -> dict:
        """Obtiene los Load Combinations (RespCombo) definidos en el modelo.

        RespCombo.GetNameList(Count, Names[]) → [Count, Names[], ret_code]
        """
        SapModel = self.sap_model

        raw = SapModel.RespCombo.GetNameList(0, [])
        ret = raw[-1]
        assert ret == 0, f"RespCombo.GetNameList failed: {ret}"

        n = raw[0]
        names = list(raw[1])[:n]
        return {"success": True, "combo_names": names, "count": n}

    # ── Step 2c: Reacciones nodales por combo ─────────────────────────────────

    def get_joint_reactions(
        self, joint_names: List[str], combo_names: List[str]
    ) -> dict:
        """Extrae Joint Reactions para los joints y Load Combinations dados.

        Selecciona los combos para output usando SetComboSelectedForOutput.
        Itera por cada joint llamando Results.JointReact con ItemTypeElm=0.

        Returns:
            {rows: list[dict], num_results: int,
             skipped_joints: list[str], success: bool}
        """
        SapModel = self.sap_model

        if not joint_names:
            return {"success": False, "error": "No hay nodos con restricciones."}
        if not combo_names:
            return {"success": False, "error": "No hay Load Combinations en el modelo."}

        ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        assert ret == 0, f"DeselectAllCasesAndCombosForOutput failed: {ret}"

        for combo in combo_names:
            ret = SapModel.Results.Setup.SetComboSelectedForOutput(combo)
            assert ret == 0, f"SetComboSelectedForOutput({combo!r}) failed: {ret}"

        rows = []
        skipped = []

        for joint in joint_names:
            # ByRef layout:
            # [NRes, Obj[], Elm[], LC[], StepType[], StepNum[],
            #  F1[], F2[], F3[], M1[], M2[], M3[], ret_code]
            raw = SapModel.Results.JointReact(
                joint, 0,
                0, [], [],
                [], [], [],
                [], [], [], [], [], []
            )
            if raw[-1] != 0:
                skipped.append(joint)
                continue

            n_rows = raw[0]
            load_cases  = list(raw[3]);  step_types = list(raw[4])
            step_nums   = list(raw[5])
            F1 = list(raw[6]);  F2 = list(raw[7]);  F3 = list(raw[8])
            M1 = list(raw[9]);  M2 = list(raw[10]); M3 = list(raw[11])

            for i in range(n_rows):
                rows.append({
                    "joint":     joint,
                    "load_case": load_cases[i],
                    "step_type": step_types[i],
                    "step_num":  float(step_nums[i]),
                    "F1": float(F1[i]), "F2": float(F2[i]), "F3": float(F3[i]),
                    "M1": float(M1[i]), "M2": float(M2[i]), "M3": float(M3[i]),
                })

        result = {"rows": rows, "num_results": len(rows), "success": True}
        if skipped:
            result["skipped_joints"] = skipped
        return result

    # ── Step 3: Construir modelo de fundación ─────────────────────────────────

    def build_foundation_model(
        self,
        joints_data: List[dict],
        reactions_rows: List[dict],
    ) -> dict:
        """
        Crea un modelo SAP2000 nuevo en blanco con los nodos de apoyo y las
        reacciones del modelo original aplicadas como Joint Loads.

        Secuencia:
          1. Guarda el path del modelo actual (para nombrar el archivo FUND)
          2. Crea modelo nuevo en blanco (File.NewBlank)
          3. Recrea cada nodo restringido en su posición original
             (PointObj.AddCartesian + PointObj.SetRestraint)
          4. Construye lookup (joint, combo) → reacciones
             Para combos multi-step, prioriza la fila "Max"
          5. Crea un Load Pattern por cada combo (type 8=Other, sin self-weight)
          6. Asigna las reacciones × -1 como fuerzas nodales
             (PointObj.SetLoadForce)
          7. Guarda como <nombre_original>_FUND.sdb

        Args:
            joints_data:    lista de dicts {name, x, y, z, restraints}
                            devuelta por get_restricted_joints()
            reactions_rows: lista de dicts devuelta por get_joint_reactions()

        Returns:
            {success, created_joints, created_patterns,
             assigned_forces, saved_path}
        """
        SapModel = self.sap_model

        # 1 ── Guardar path del modelo original antes de crear el nuevo
        try:
            model_path = str(SapModel.GetModelFilename())
        except Exception:
            model_path = ""

        # 2 ── Crear modelo nuevo en blanco
        ret = SapModel.File.NewBlank()
        assert ret == 0, f"File.NewBlank failed: {ret}"

        # 3 ── Recrear nodos de apoyo en sus coordenadas originales
        #       AddCartesian(X, Y, Z, Name_byref, UserName) → [Name, ret_code]
        joint_name_map: dict = {}
        for jdata in joints_data:
            raw_pt = SapModel.PointObj.AddCartesian(
                jdata["x"], jdata["y"], jdata["z"], "", jdata["name"]
            )
            assert raw_pt[-1] == 0, (
                f"PointObj.AddCartesian for joint {jdata['name']!r} failed: {raw_pt[-1]}"
            )
            new_name = raw_pt[0]
            joint_name_map[jdata["name"]] = new_name

            raw_rs = SapModel.PointObj.SetRestraint(new_name, jdata["restraints"])
            rc_rs = raw_rs[-1] if isinstance(raw_rs, (list, tuple)) else raw_rs
            assert rc_rs == 0, (
                f"PointObj.SetRestraint for joint {new_name!r} failed: {rc_rs}"
            )

        # 4 ── Lookup (joint_original, combo) → mejor reacción
        #       Para envolventes con "Max"/"Min", priorizar "Max"
        reactions_lookup: dict = {}
        for row in reactions_rows:
            key = (row["joint"], row["load_case"])
            if key not in reactions_lookup or row["step_type"] == "Max":
                reactions_lookup[key] = {
                    k: row[k] for k in ("F1", "F2", "F3", "M1", "M2", "M3")
                }

        combo_names = sorted({row["load_case"] for row in reactions_rows})

        # 5 ── Crear Load Patterns (uno por combo, type 8=Other, sin self-weight)
        #       Si Add retorna error porque ya existe, se ignora.
        created_patterns = []
        for combo in combo_names:
            ret_add = SapModel.LoadPatterns.Add(combo, 8, 0, True)
            if ret_add == 0:
                created_patterns.append(combo)

        # 6 ── Asignar fuerzas nodales: reacciones × -1
        #       SetLoadForce(Name, LoadPat, Value[6], Replace, CSys)
        #       → [Value_echoed[], ret_code]
        assigned = 0
        for jdata in joints_data:
            orig_name = jdata["name"]
            new_name  = joint_name_map.get(orig_name, orig_name)
            for combo in combo_names:
                key = (orig_name, combo)
                if key not in reactions_lookup:
                    continue
                R = reactions_lookup[key]
                force_vals = [
                    -R["F1"], -R["F2"], -R["F3"],
                    -R["M1"], -R["M2"], -R["M3"],
                ]
                raw_sf = SapModel.PointObj.SetLoadForce(
                    new_name, combo, force_vals, True, "Global"
                )
                if raw_sf[-1] == 0:
                    assigned += 1

        # 7 ── Guardar como <nombre_original>_FUND.sdb
        saved_path = ""
        if model_path:
            base, ext = os.path.splitext(model_path)
            new_path = base + "_FUND" + (ext if ext else ".sdb")
            try:
                ret_save = SapModel.File.Save(new_path)
                if ret_save == 0:
                    saved_path = new_path
            except Exception:
                pass

        return {
            "success":          True,
            "created_joints":   len(joints_data),
            "created_patterns": created_patterns,
            "assigned_forces":  assigned,
            "saved_path":       saved_path,
        }
