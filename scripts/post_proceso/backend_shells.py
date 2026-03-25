"""
Backend: Shells — Fuerzas en Elementos de Área (Shell)
=======================================================
Extrae AreaForceShell de SAP2000 para áreas seleccionadas manualmente
en el modelo y para todas las combinaciones de carga existentes.

Dependencias: comtypes, stdlib
Sin imports de mcp_server/ ni módulos internos del framework.

Índices ByRef de SapModel.Results.AreaForceShell:
  [0]  NumberResults
  [1]  Obj[]        [2]  Elm[]        [3]  PointElm[]
  [4]  LoadCase[]   [5]  StepType[]   [6]  StepNum[]
  [7]  F11[]  [8]  F22[]  [9]  F12[]  [10] FMax[]  [11] FMin[]  [12] FAngle[]  [13] FVM[]
  [14] M11[]  [15] M22[]  [16] M12[]  [17] MMax[]  [18] MMin[]  [19] MAngle[]
  [20] V13[]  [21] V23[]  [22] VMax[] [23] VAngle[]
  [-1] ret_code
"""

import comtypes.client
from typing import List


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo) — reutiliza la misma clase del módulo
# de estabilidad para mantener coherencia, pero importable de forma
# independiente si se usa este backend solo.
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
# Backend: Shells
# ══════════════════════════════════════════════════════════════════════════════

class ShellsBackend:
    """
    Extrae Shell Forces de áreas seleccionadas para las combinaciones de carga.

    Flujo típico:
        1. get_selected_areas()                          → AreaObj seleccionados
        2. get_combo_names()                             → combinaciones del modelo
        3. get_shell_forces(areas, combos) → tabla de resultados
    """

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión activa con SAP2000.")
        return self._conn.sap_model

    # ── Task 1: Leer áreas seleccionadas ─────────────────────────────────────

    def get_selected_areas(self) -> dict:
        """Lee los AreaObj actualmente seleccionados en SAP2000.

        Filtra ObjectType == 5 (Area object).

        Returns:
            {area_names: list[str], count: int, success: bool}
        """
        SapModel = self.sap_model

        # ByRef layout: [NumberItems, ObjectType[], ObjectName[], ret_code]
        raw = SapModel.SelectObj.GetSelected(0, [], [])
        ret = raw[-1]
        assert ret == 0, f"SelectObj.GetSelected failed: {ret}"

        n_total = raw[0]
        obj_types = list(raw[1])   # 5 = Area object
        obj_names = list(raw[2])

        area_names = [obj_names[i] for i in range(n_total) if obj_types[i] == 5]

        return {
            "area_names": area_names,
            "count": len(area_names),
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

    # ── Task 3: Obtener fuerzas en shells ─────────────────────────────────────

    def get_shell_forces(
        self, area_names: List[str], combo_names: List[str]
    ) -> dict:
        """Extrae Shell Forces de las áreas dadas para las combinaciones dadas.

        Configura el output selector para las combos y llama
        Results.AreaForceShell por cada área.

        ByRef index reference:
          [0]NRes [1]Obj [2]Elm [3]PtElm [4]LC [5]StType [6]StNum
          [7]F11  [8]F22  [9]F12  [10]FMax [11]FMin [12]FAngle [13]FVM
          [14]M11 [15]M22 [16]M12 [17]MMax [18]MMin [19]MAngle
          [20]V13 [21]V23 [22]VMax [23]VAngle  [-1]ret_code

        Returns:
            {rows: list[dict], num_results: int, success: bool}
        """
        SapModel = self.sap_model

        if not area_names:
            return {"success": False, "error": "No hay áreas seleccionadas."}
        if not combo_names:
            return {"success": False, "error": "No hay combinaciones en el modelo."}

        # ── Seleccionar combos para output ────────────────────────────────────
        ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        assert ret == 0, f"DeselectAllCasesAndCombosForOutput failed: {ret}"

        for combo in combo_names:
            ret = SapModel.Results.Setup.SetComboSelectedForOutput(combo)
            assert ret == 0, f"SetComboSelectedForOutput({combo!r}) failed: {ret}"

        # ── Extraer fuerzas por área ──────────────────────────────────────────
        rows = []
        skipped = []

        for area in area_names:
            raw = SapModel.Results.AreaForceShell(
                area, 0,
                0, [], [], [],         # NumberResults, Obj, Elm, PointElm
                [], [], [],            # LoadCase, StepType, StepNum
                [], [], [], [], [], [], [],  # F11..FVM
                [], [], [], [], [], [],      # M11..MAngle
                [], [], [], []              # V13, V23, VMax, VAngle
            )
            ret_code = raw[-1]
            if ret_code != 0:
                skipped.append(area)
                continue

            n = raw[0]
            obj_names  = list(raw[1])
            point_elms = list(raw[3])
            load_cases = list(raw[4])
            step_types = list(raw[5])
            step_nums  = list(raw[6])
            F11 = list(raw[7]);   F22 = list(raw[8]);   F12 = list(raw[9])
            M11 = list(raw[14]);  M22 = list(raw[15]);  M12 = list(raw[16])
            V13 = list(raw[20]);  V23 = list(raw[21])

            for i in range(n):
                rows.append({
                    "area":      obj_names[i],
                    "point_elm": point_elms[i],
                    "load_case": load_cases[i],
                    "step_type": step_types[i],
                    "step_num":  float(step_nums[i]),
                    "F11": float(F11[i]),
                    "F22": float(F22[i]),
                    "F12": float(F12[i]),
                    "M11": float(M11[i]),
                    "M22": float(M22[i]),
                    "M12": float(M12[i]),
                    "V13": float(V13[i]),
                    "V23": float(V23[i]),
                })

        result = {
            "rows": rows,
            "num_results": len(rows),
            "success": True,
        }
        if skipped:
            result["skipped_areas"] = skipped

        return result
