"""
Backend: Estabilidad — Desplazamientos de Nodos
================================================
Extrae Joint Displacements de SAP2000 para nodos seleccionados manualmente
en el modelo y para todas las combinaciones de carga existentes.

Dependencias: comtypes, stdlib
Sin imports de mcp_server/ ni módulos internos del framework.
"""

import comtypes.client
from typing import List, Dict, Any


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo)
# ══════════════════════════════════════════════════════════════════════════════

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""

    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing: bool = True) -> dict:
        try:
            if attach_to_existing:
                self.sap_object = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject"
                )
            else:
                helper = comtypes.client.CreateObject("SAP2000v1.Helper")
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
                self.sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                self.sap_object.ApplicationStart()

            self.sap_model = self.sap_object.SapModel
            version = str(self.sap_object.GetOAPIVersionNumber())
            model_path = str(self.sap_model.GetModelFilename())
            return {"connected": True, "version": version, "model_path": model_path}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Backend: Estabilidad
# ══════════════════════════════════════════════════════════════════════════════

class EstabilidadBackend:
    """
    Extrae desplazamientos de nodos seleccionados para combinaciones de carga.

    Flujo típico:
        1. get_selected_joints()   → lista los PointObj seleccionados en SAP2000
        2. get_combo_names()       → lista todas las RespCombo del modelo
        3. get_joint_displacements(joints, combos) → tabla de resultados
    """

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión activa con SAP2000.")
        return self._conn.sap_model

    # ── Task 1: Leer nodos seleccionados ─────────────────────────────────────

    def get_selected_joints(self) -> dict:
        """Lee los nodos (PointObj) actualmente seleccionados en SAP2000.

        Usa SelectObj.GetSelected y filtra ObjectType == 1 (Point).

        Returns:
            {joint_names: list[str], count: int, success: bool}
        """
        SapModel = self.sap_model

        # ByRef layout: [NumberItems, ObjectType[], ObjectName[], ret_code]
        raw = SapModel.SelectObj.GetSelected(0, [], [])
        ret = raw[-1]
        assert ret == 0, f"SelectObj.GetSelected failed: {ret}"

        n_total = raw[0]
        obj_types = list(raw[1])   # 1=Point, 2=Frame, 3=Area, 4=Solid, 5=Link
        obj_names = list(raw[2])

        joint_names = [obj_names[i] for i in range(n_total) if obj_types[i] == 1]

        return {
            "joint_names": joint_names,
            "count": len(joint_names),
            "success": True,
        }

    # ── Task 2: Leer combinaciones de carga ──────────────────────────────────

    def get_combo_names(self) -> dict:
        """Obtiene todos los nombres de combinaciones de respuesta del modelo.

        Returns:
            {combo_names: list[str], count: int, success: bool}
        """
        SapModel = self.sap_model

        # ByRef layout: [NumberNames, MyName[], ret_code]
        raw = SapModel.RespCombo.GetNameList(0, [])
        ret = raw[-1]
        assert ret == 0, f"RespCombo.GetNameList failed: {ret}"

        n = raw[0]
        names = list(raw[1])[:n]

        return {"combo_names": names, "count": n, "success": True}

    # ── Task 3: Obtener desplazamientos ──────────────────────────────────────

    def get_joint_displacements(
        self, joint_names: List[str], combo_names: List[str]
    ) -> dict:
        """Extrae desplazamientos de los joints dados para las combinaciones dadas.

        Configura el output selector para las combos, luego itera por cada
        nodo llamando a Results.JointDispl con ItemTypeElm=0 (Object).

        Returns:
            {
                rows: list[dict],   # una fila por (joint, combo, step)
                num_results: int,
                success: bool,
            }
        """
        SapModel = self.sap_model
        result: Dict[str, Any] = {"rows": [], "success": True}

        if not joint_names:
            return {"success": False, "error": "No hay nodos seleccionados."}

        if not combo_names:
            return {"success": False, "error": "No hay combinaciones en el modelo."}

        # ── Seleccionar combos para output ────────────────────────────────────
        ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        assert ret == 0, f"DeselectAllCasesAndCombosForOutput failed: {ret}"

        for combo in combo_names:
            ret = SapModel.Results.Setup.SetComboSelectedForOutput(combo)
            assert ret == 0, f"SetComboSelectedForOutput({combo!r}) failed: {ret}"

        # ── Extraer desplazamientos por nodo ──────────────────────────────────
        rows = []
        skipped = []

        for joint in joint_names:
            # ByRef layout:
            #   [NRes, Obj[], Elm[], LC[], StepType[], StepNum[],
            #    U1[], U2[], U3[], R1[], R2[], R3[], ret_code]
            raw = SapModel.Results.JointDispl(
                joint, 0,          # Name, ItemTypeElm=Object
                0, [], [],         # ByRef: NumberResults, Obj, Elm
                [], [], [],        # ByRef: LoadCase, StepType, StepNum
                [], [], [], [], [], []  # ByRef: U1, U2, U3, R1, R2, R3
            )
            ret_code = raw[-1]
            if ret_code != 0:
                skipped.append(joint)
                continue

            n = raw[0]
            load_cases = list(raw[3])
            step_types = list(raw[4])
            step_nums  = list(raw[5])
            U1 = list(raw[6])
            U2 = list(raw[7])
            U3 = list(raw[8])
            R1 = list(raw[9])
            R2 = list(raw[10])
            R3 = list(raw[11])

            for i in range(n):
                rows.append({
                    "joint":     joint,
                    "load_case": load_cases[i],
                    "step_type": step_types[i],
                    "step_num":  float(step_nums[i]),
                    "U1": float(U1[i]),
                    "U2": float(U2[i]),
                    "U3": float(U3[i]),
                    "R1": float(R1[i]),
                    "R2": float(R2[i]),
                    "R3": float(R3[i]),
                })

        result["rows"] = rows
        result["num_results"] = len(rows)
        if skipped:
            result["skipped_joints"] = skipped

        return result
