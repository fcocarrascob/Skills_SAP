"""
Backend: Modelo de Fundación (Mod FUND)
=======================================
Automatiza la creación de un modelo de fundación a partir de un modelo
estructural analizado en SAP2000.

Flujo:
  1. check_analysis_done      — verifica modelo bloqueado (análisis completado)
  2. get_restricted_joints    — nodos con al menos un DOF restringido
     get_load_cases_no_modal  — load cases del modelo, excluye tipo MODAL (3)
     get_frame_sections       — secciones de Frame disponibles
     get_joint_reactions      — reacciones nodales por load case
  3. build_foundation_model   — desbloquea, crea pilas hacia Z-,
                                borra estructura superior, asigna reacciones

Dependencias: comtypes, stdlib
Sin imports de mcp_server/ ni módulos internos del framework.

Notas sobre firmas COM (verificadas contra wrappers del registry):
  FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, Name_byref, PropName, UserName)
    → [FrameName, ret_code]
  PointObj.SetLoadForce(Name, LoadPat, Value[6], Replace, CSys)
    → [Value_echoed[], ret_code]
  LoadPatterns.Add(Name, MyType, SelfWtMult, AddCase) → ret_code
  Results.JointReact(Name, ItemTypeElm=0, NRes, Obj, Elm,
      LC, StepType, StepNum, F1, F2, F3, M1, M2, M3) → [14 ByRef outs + ret_code]
  PointObj.GetCoordCartesian(Name, X, Y, Z, CSys) → [X, Y, Z, ret_code]
  PointObj.GetRestraint(Name, Value[]) → [values[6], ret_code]
  LoadCases.GetTypeOAPI(Name, CaseType, SubType) → [CaseType, SubType, ret_code]
    CaseType == 3 → Modal
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
        2. get_restricted_joints()  +  get_load_cases_no_modal()
           +  get_frame_sections()
        3. get_joint_reactions(joint_names, case_names)
        4. build_foundation_model(joint_names, reactions_rows,
                                  section_name, pile_depth)
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
        """Obtiene todos los PointObj con al menos un DOF restringido.

        GetRestraint(Name, []) → [values[6_bools], ret_code]
        """
        SapModel = self.sap_model

        raw = SapModel.PointObj.GetNameList(0, [])
        ret = raw[-1]
        assert ret == 0, f"PointObj.GetNameList failed: {ret}"

        n = raw[0]
        all_names = list(raw[1])[:n]

        restrained = []
        for name in all_names:
            raw_r = SapModel.PointObj.GetRestraint(name, [])
            if raw_r[-1] != 0:
                continue
            values = list(raw_r[0])
            if any(values):
                restrained.append(name)

        return {"success": True, "joint_names": restrained, "count": len(restrained)}

    # ── Step 2b: Load cases sin MODAL ─────────────────────────────────────────

    def get_load_cases_no_modal(self) -> dict:
        """Obtiene load cases del modelo excluyendo tipo Modal (CaseType == 3).

        LoadCases.GetTypeOAPI(Name, CaseType, SubType)
            → [CaseType, SubType, ret_code]
        """
        SapModel = self.sap_model

        raw = SapModel.LoadCases.GetNameList(0, [])
        ret = raw[-1]
        assert ret == 0, f"LoadCases.GetNameList failed: {ret}"

        n = raw[0]
        all_names = list(raw[1])[:n]

        non_modal = []
        for name in all_names:
            try:
                raw_t = SapModel.LoadCases.GetTypeOAPI(name, 0, 0)
                if raw_t[-1] == 0 and raw_t[0] == 3:
                    continue  # Modal → excluir
            except Exception:
                pass  # Si la consulta falla, incluir el caso por defecto
            non_modal.append(name)

        return {"success": True, "case_names": non_modal, "count": len(non_modal)}

    # ── Step 2c: Secciones de frame disponibles ───────────────────────────────

    def get_frame_sections(self) -> dict:
        """Obtiene las secciones de Frame (PropFrame) definidas en el modelo."""
        SapModel = self.sap_model

        raw = SapModel.PropFrame.GetNameList(0, [])
        ret = raw[-1]
        assert ret == 0, f"PropFrame.GetNameList failed: {ret}"

        n = raw[0]
        names = list(raw[1])[:n]
        return {"success": True, "section_names": names, "count": n}

    # ── Step 2d: Reacciones nodales ───────────────────────────────────────────

    def get_joint_reactions(
        self, joint_names: List[str], case_names: List[str]
    ) -> dict:
        """Extrae Joint Reactions para los joints y load cases dados.

        Itera por cada joint llamando Results.JointReact con ItemTypeElm=0.

        Returns:
            {rows: list[dict], num_results: int,
             skipped_joints: list[str], success: bool}
        """
        SapModel = self.sap_model

        if not joint_names:
            return {"success": False, "error": "No hay nodos con restricciones."}
        if not case_names:
            return {"success": False, "error": "No hay load cases en el modelo."}

        ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        assert ret == 0, f"DeselectAllCasesAndCombosForOutput failed: {ret}"

        for case in case_names:
            ret = SapModel.Results.Setup.SetCaseSelectedForOutput(case)
            assert ret == 0, f"SetCaseSelectedForOutput({case!r}) failed: {ret}"

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
            load_cases = list(raw[3]);  step_types = list(raw[4])
            step_nums  = list(raw[5])
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
        joint_names: List[str],
        reactions_rows: List[dict],
        section_name: str,
        pile_depth: float,
    ) -> dict:
        """
        Construye el modelo de fundación en el modelo SAP2000 abierto.

        Secuencia:
          1. Desbloquea el modelo  (SetModelIsLocked False)
          2. Registra FrameObj y AreaObj actualmente existentes
          3. Crea FrameObj tipo pila por cada joint restringido hacia Z-
             usando FrameObj.AddByCoord
          4. Elimina los frames y áreas originales
             (FrameObj.Delete / AreaObj.Delete)
          5. Crea load patterns "RF_<case>" (LoadPatterns.Add, type 8=Other)
          6. Asigna reacciones como fuerzas nodales (PointObj.SetLoadForce)
             con la misma magnitud y signo que reporta JointReact.
             Para casos multiestep se usa la fila "Max" si existe.

        Returns:
            {success, created_frames, deleted_frames, deleted_areas,
             created_patterns, assigned_forces}
        """
        SapModel = self.sap_model

        # 1 ── Desbloquear
        ret = SapModel.SetModelIsLocked(False)
        assert ret == 0, f"SetModelIsLocked(False) failed: {ret}"

        # 2 ── Registrar elementos existentes antes de crear nuevos
        raw_fr = SapModel.FrameObj.GetNameList(0, [])
        existing_frames = list(raw_fr[1])[:raw_fr[0]] if raw_fr[-1] == 0 else []

        raw_ar = SapModel.AreaObj.GetNameList(0, [])
        existing_areas = list(raw_ar[1])[:raw_ar[0]] if raw_ar[-1] == 0 else []

        # 3 ── Crear frames tipo pila hacia Z-
        created_frames = []
        for joint in joint_names:
            # GetCoordCartesian(Name, X, Y, Z, CSys) → [X, Y, Z, ret_code]
            raw_c = SapModel.PointObj.GetCoordCartesian(
                joint, 0.0, 0.0, 0.0, "Global"
            )
            assert raw_c[-1] == 0, (
                f"GetCoordCartesian({joint!r}) failed: {raw_c[-1]}"
            )
            x, y, z = float(raw_c[0]), float(raw_c[1]), float(raw_c[2])

            # Punto inferior: misma posición XY, z - profundidad
            zj = z - abs(pile_depth)

            # AddByCoord(x1,y1,z1, x2,y2,z2, Name_byref="", PropName, UserName="")
            # → [FrameName, ret_code]
            raw_f = SapModel.FrameObj.AddByCoord(
                x, y, z, x, y, zj, "", section_name, ""
            )
            assert raw_f[-1] == 0, (
                f"FrameObj.AddByCoord at joint {joint!r} ({x},{y},{z}) "
                f"failed: {raw_f[-1]}"
            )
            created_frames.append(raw_f[0])

        # 4 ── Eliminar estructura superior
        deleted_frames = 0
        for fr_name in existing_frames:
            ret_d = SapModel.FrameObj.Delete(fr_name, 0)
            if ret_d == 0:
                deleted_frames += 1

        deleted_areas = 0
        for ar_name in existing_areas:
            ret_d = SapModel.AreaObj.Delete(ar_name, 0)
            if ret_d == 0:
                deleted_areas += 1

        # 5a ── Lookup (joint, load_case) → mejor reacción
        #        Para envolventes con "Max"/"Min", tomar "Max" si existe.
        reactions_lookup: dict = {}
        for row in reactions_rows:
            key = (row["joint"], row["load_case"])
            if key not in reactions_lookup or row["step_type"] == "Max":
                reactions_lookup[key] = {
                    k: row[k] for k in ("F1", "F2", "F3", "M1", "M2", "M3")
                }

        case_names = sorted({row["load_case"] for row in reactions_rows})

        # 5b ── Crear load patterns con el mismo nombre que el load case
        #        (8=Other, sin self-weight). Si ya existe, Add retorna error
        #        ignorable; se usa el nombre original de todas formas.
        created_patterns = []
        for case in case_names:
            ret_add = SapModel.LoadPatterns.Add(case, 8, 0, True)
            if ret_add == 0:
                created_patterns.append(case)

        # 5c ── Asignar fuerzas nodales
        #        SetLoadForce(Name, LoadPat, Value[6], Replace, CSys)
        #        → [Value_echoed[], ret_code]
        assigned = 0
        for joint in joint_names:
            for case in case_names:
                key = (joint, case)
                if key not in reactions_lookup:
                    continue
                R = reactions_lookup[key]
                force_vals = [
                    R["F1"], R["F2"], R["F3"],
                    R["M1"], R["M2"], R["M3"],
                ]
                raw_sf = SapModel.PointObj.SetLoadForce(
                    joint, case, force_vals, True, "Global"
                )
                if raw_sf[-1] == 0:
                    assigned += 1

        # 6 ── Guardar como <nombre_original>_FUND.sdb
        saved_path = ""
        try:
            model_path = str(SapModel.GetModelFilename())
            if model_path:
                base, ext = os.path.splitext(model_path)
                new_path = base + "_FUND" + (ext if ext else ".sdb")
                ret_save = SapModel.File.Save(new_path)
                if ret_save == 0:
                    saved_path = new_path
        except Exception:
            pass  # no bloquear si el guardado falla

        return {
            "success": True,
            "created_frames": len(created_frames),
            "deleted_frames": deleted_frames,
            "deleted_areas": deleted_areas,
            "created_patterns": created_patterns,
            "assigned_forces": assigned,
            "saved_path": saved_path,
        }
