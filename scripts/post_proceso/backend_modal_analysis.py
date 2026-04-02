"""
Backend: Análisis Modal — Contribuciones por Modo
==================================================
Extrae desde SAP2000 las contribuciones modales a las reacciones de base
para los casos de espectro de respuesta (Response Spectrum).

Flujo:
    1. get_rs_cases()                  → lista de casos LinRespSpec del modelo
    2. compute_contributions(rs_case, component)
                                       → tabla de contribuciones por modo

Cálculo:
    Para cada modo n:
      contrib_n = Amp_n × F_modal_n

    donde:
      Amp_n    = U1Amp / U2Amp / U3Amp según dirección dominante del caso RS
                 (detectada comparando la suma de U1Acc, U2Acc, U3Acc)
      F_modal_n = componente de reacción de base del modo n (caso MODAL)

    SRSS = sqrt(sum(contrib_n²))
    % Contrib se calcula relativo a la reacción CQC de SAP2000 (Base Reactions).

Dependencias: comtypes, stdlib (math)
Sin imports de mcp_server/ ni módulos del framework.
"""

import math
from typing import List, Dict, Any


class ModalAnalysisBackend:
    """Calcula contribuciones modales a las reacciones de base para casos RS."""

    COMPONENTS = ["FX", "FY", "FZ", "MX", "MY", "MZ"]
    _COMP_IDX  = {c: i for i, c in enumerate(COMPONENTS)}

    def __init__(self, connection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión activa con SAP2000.")
        return self._conn.sap_model

    # ── 1. Detectar casos Response Spectrum ──────────────────────────────────

    def get_rs_cases(self) -> dict:
        """Retorna los nombres de los casos de Response Spectrum del modelo.

        Usa LoadCases.GetTypeOAPI para filtrar CaseType == 4 (LinRespSpec).

        Returns:
            {success: bool, rs_cases: list[str], count: int}
        """
        try:
            SapModel = self.sap_model

            raw = SapModel.LoadCases.GetNameList(0, [])
            # raw: [n_cases, names_tuple, ret_code]
            assert raw[-1] == 0, f"LoadCases.GetNameList failed: {raw[-1]}"
            n     = raw[0]
            names = list(raw[1])[:n]

            rs_cases = []
            for name in names:
                try:
                    raw_t = SapModel.LoadCases.GetTypeOAPI(name, 0, 0)
                    # raw_t: [CaseType, SubType, ret_code]
                    # CaseType 4 = LinRespSpec (Response Spectrum)
                    if raw_t[-1] == 0 and raw_t[0] == 4:
                        rs_cases.append(name)
                except Exception:
                    pass

            return {"success": True, "rs_cases": rs_cases, "count": len(rs_cases)}
        except Exception as exc:
            return {"success": False, "error": str(exc), "rs_cases": []}

    # ── 2. Calcular contribuciones modales ────────────────────────────────────

    def compute_contributions(self, rs_case: str, component: str) -> dict:
        """Calcula la contribución de cada modo a la reacción de base indicada.

        Args:
            rs_case:   Nombre del caso RS (e.g. "EQX")
            component: Componente de reacción ("FX","FY","FZ","MX","MY","MZ")

        Returns:
            {
              success:       bool,
              rows:          list[dict] ordenada por |contrib| desc, con claves:
                               mode, T, amplitude, F_modal,
                               contrib, pct_contrib, pct_acum,
              srss_total:    float      ← combinación SRSS calculada aquí
              rs_total:      float      ← resultado CQC de SAP2000 (Max)
              amp_direction: str        ← "U1", "U2" o "U3"
              amp_column:    str        ← "U1Amp", "U2Amp" o "U3Amp"
              num_modes:     int
              component:     str
              rs_case:       str
            }
        """
        comp_idx = self._COMP_IDX.get(component, 0)

        try:
            SapModel = self.sap_model

            # ── Paso 1: Reacciones de base del caso MODAL (por modo) ──────────
            SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
            ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL", True)
            if ret != 0:
                raise RuntimeError(f"No se pudo seleccionar caso MODAL (ret={ret})")

            raw_m = SapModel.Results.BaseReact(
                0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0
            )
            # raw_m: [num, LoadCase[], StepType[], StepNum[],
            #         FX[], FY[], FZ[], MX[], MY[], MZ[],
            #         GlobalX, GlobalY, GlobalZ, ret_code]
            if raw_m[13] != 0:
                raise RuntimeError(f"BaseReact MODAL falló: ret={raw_m[13]}")

            num_modes  = raw_m[0]
            step_nums  = list(raw_m[3])
            comp_vals  = list(raw_m[4 + comp_idx])
            modal_react = {int(step_nums[i]): comp_vals[i] for i in range(num_modes)}

            # ── Paso 2: RS Modal Information (amplitudes por modo) ────────────
            SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
            SapModel.Results.Setup.SetCaseSelectedForOutput(rs_case, True)

            raw_rs = SapModel.DatabaseTables.GetTableForDisplayArray(
                "Response Spectrum Modal Information", [""], "All", 0, [], 0, []
            )
            # raw_rs: [FieldKeyList, TableVersion, FieldKeysIncluded,
            #          NumberRecords, TableData, ret_code]
            if raw_rs[5] != 0:
                raise RuntimeError(
                    f"Response Spectrum Modal Information falló: ret={raw_rs[5]}"
                )

            fk = list(raw_rs[2])
            nr = raw_rs[3]
            td = list(raw_rs[4])
            nc = len(fk)

            rs_data: Dict[int, dict] = {}
            for i in range(nr):
                row = {fk[j]: td[i * nc + j] for j in range(nc)}
                if row.get("OutputCase") != rs_case:
                    continue
                rs_data[int(row["StepNum"])] = row

            # ── Paso 3: Detectar dirección dominante del espectro ─────────────
            def _sf(v) -> float:
                if v is None:
                    return 0.0
                return float(str(v).replace(",", "."))

            sum_acc = {"U1": 0.0, "U2": 0.0, "U3": 0.0}
            for row in rs_data.values():
                sum_acc["U1"] += abs(_sf(row.get("U1Acc", "0")))
                sum_acc["U2"] += abs(_sf(row.get("U2Acc", "0")))
                sum_acc["U3"] += abs(_sf(row.get("U3Acc", "0")))

            amp_dir = max(sum_acc, key=lambda k: sum_acc[k])
            amp_col = f"{amp_dir}Amp"  # "U1Amp", "U2Amp" o "U3Amp"

            # ── Paso 4: Contribución por modo ─────────────────────────────────
            contribs = []
            for mode_n in range(1, num_modes + 1):
                row = rs_data.get(mode_n)
                if row is None:
                    continue
                amp     = _sf(row.get(amp_col, "0"))
                f_modal = modal_react.get(mode_n, 0.0)
                contribs.append({
                    "mode":      mode_n,
                    "T":         _sf(row.get("Period", "0")),
                    "amplitude": amp,
                    "F_modal":   f_modal,
                    "contrib":   amp * f_modal,
                })

            # ── Paso 5: SRSS ─────────────────────────────────────────────────
            srss_total = math.sqrt(sum(c["contrib"] ** 2 for c in contribs))

            # ── Paso 6: Resultado CQC de SAP2000 (caso RS ya seleccionado) ────
            raw_rsb = SapModel.Results.BaseReact(
                0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0
            )
            rs_total = 0.0
            if raw_rsb[13] == 0 and raw_rsb[0] > 0:
                rs_total = abs(list(raw_rsb[4 + comp_idx])[0])

            # ── Paso 7: Ordenar por |contrib| y calcular porcentajes ──────────
            contribs.sort(key=lambda x: abs(x["contrib"]), reverse=True)
            denom = rs_total if rs_total > 0 else (srss_total if srss_total > 0 else 1.0)

            running_pct = 0.0
            rows_out = []
            for c in contribs:
                pct = abs(c["contrib"]) / denom * 100.0
                running_pct += pct
                rows_out.append({
                    "mode":        c["mode"],
                    "T":           c["T"],
                    "amplitude":   c["amplitude"],
                    "F_modal":     c["F_modal"],
                    "contrib":     c["contrib"],
                    "pct_contrib": pct,
                    "pct_acum":    running_pct,
                })

            return {
                "success":       True,
                "rows":          rows_out,
                "srss_total":    srss_total,
                "rs_total":      rs_total,
                "amp_direction": amp_dir,
                "amp_column":    amp_col,
                "num_modes":     num_modes,
                "component":     component,
                "rs_case":       rs_case,
            }

        except Exception as exc:
            return {"success": False, "error": str(exc)}
