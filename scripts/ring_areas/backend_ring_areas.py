"""
Backend — SAP2000 Circular Ring Area Generator (Standalone)
============================================================
Genera un modelo de anillo circular (placa anular) con 3 zonas concéntricas
de área (shell), separadas por radios intermedios.

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: example_1001_simple_beam.py
"""

import math
import tempfile
import comtypes.client
from dataclasses import dataclass


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
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class RingAreasConfig:
    """Parámetros de entrada para el generador de anillos."""

    # Radios [m]
    r_inner: float = 1.0
    r_mid1: float = 2.0
    r_mid2: float = 3.5
    r_outer: float = 5.0

    # Espesores de shell [m]
    t1: float = 0.30   # Zona 1 (interior) y Zona 3 (exterior)
    t2: float = 0.20   # Zona 2 (intermedia)

    # Material
    mat_name: str = "CONC"
    E_mat: float = 2.5e7       # [kN/m²]
    nu_mat: float = 0.2
    alpha: float = 1.0e-5      # [1/°C]

    # Discretización
    n_segs: int = 36


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class RingAreasBackend:
    """Backend standalone para generar anillos concéntricos en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Funciones auxiliares ──────────────────────────────────────────────

    @staticmethod
    def ring_pts(radius: float, n: int):
        """Devuelve lista de n puntos (x, y) sobre una circunferencia."""
        return [
            (radius * math.cos(2.0 * math.pi * i / n),
             radius * math.sin(2.0 * math.pi * i / n))
            for i in range(n)
        ]

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: RingAreasConfig) -> dict:
        """Ejecuta la generación de anillos concéntricos.

        Args:
            config: Parámetros de entrada.

        Returns:
            dict con resultados del modelo generado.
        """
        SapModel = self.sap_model
        result = {}

        # ── Task 1: Inicializar modelo ───────────────────────────────────
        ret = SapModel.InitializeNewModel()
        assert ret == 0, f"InitializeNewModel failed: {ret}"

        ret = SapModel.File.NewBlank()
        assert ret == 0, f"NewBlank failed: {ret}"

        ret = SapModel.SetPresentUnits(6)  # kN_m_C
        assert ret == 0, f"SetPresentUnits failed: {ret}"

        result["task_1_init"] = True

        # ── Task 2: Definir material ─────────────────────────────────────
        ret = SapModel.PropMaterial.SetMaterial(config.mat_name, 2)  # 2 = Concrete
        assert ret == 0, f"SetMaterial failed: {ret}"

        ret = SapModel.PropMaterial.SetMPIsotropic(
            config.mat_name, config.E_mat, config.nu_mat, config.alpha
        )
        assert ret == 0, f"SetMPIsotropic failed: {ret}"

        result["task_2_material"] = config.mat_name

        # ── Task 3: Definir propiedades de área (shell) ──────────────────
        ret = SapModel.PropArea.SetShell_1(
            "SHELL_T1", 1, True, config.mat_name, 0, config.t1, config.t1
        )
        assert ret == 0, f"SetShell_1(SHELL_T1) failed: {ret}"

        ret = SapModel.PropArea.SetShell_1(
            "SHELL_T2", 1, True, config.mat_name, 0, config.t2, config.t2
        )
        assert ret == 0, f"SetShell_1(SHELL_T2) failed: {ret}"

        result["task_3_sections"] = {"SHELL_T1": config.t1, "SHELL_T2": config.t2}

        # ── Task 4: Generar geometría de anillos concéntricos ────────────
        zones = [
            (config.r_inner, config.r_mid1,  "SHELL_T1", "ZONA1_interior"),
            (config.r_mid1,  config.r_mid2,  "SHELL_T2", "ZONA2_intermedia"),
            (config.r_mid2,  config.r_outer, "SHELL_T1", "ZONA3_exterior"),
        ]
        area_count = {
            "ZONA1_interior": 0,
            "ZONA2_intermedia": 0,
            "ZONA3_exterior": 0,
        }

        n = config.n_segs
        for (r_in, r_out, prop, label) in zones:
            pts_in = self.ring_pts(r_in, n)
            pts_out = self.ring_pts(r_out, n)

            for i in range(n):
                j = (i + 1) % n

                x = [pts_in[i][0], pts_out[i][0], pts_out[j][0], pts_in[j][0]]
                y = [pts_in[i][1], pts_out[i][1], pts_out[j][1], pts_in[j][1]]
                z = [0.0, 0.0, 0.0, 0.0]

                raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", prop, "")
                assert raw[-1] == 0, f"AddByCoord({label}[{i}]) failed: {raw[-1]}"
                area_count[label] += 1

        result["task_4_geometry"] = area_count
        result["total_areas"] = sum(area_count.values())

        # ── Task 5: Guardar modelo y refrescar vista ─────────────────────
        save_path = tempfile.gettempdir() + r"\ring_areas_model.sdb"
        ret = SapModel.File.Save(save_path)
        assert ret == 0, f"File.Save failed: {ret}"

        SapModel.View.RefreshView(0, False)
        result["task_5_saved"] = True
        result["save_path"] = save_path

        # ── Resumen final ────────────────────────────────────────────────
        result["success"] = True
        result["radii"] = {
            "r_inner": config.r_inner,
            "r_mid1": config.r_mid1,
            "r_mid2": config.r_mid2,
            "r_outer": config.r_outer,
        }
        result["thicknesses"] = {
            "t1 (Zona1+Zona3)": config.t1,
            "t2 (Zona2)": config.t2,
        }
        result["n_segments"] = config.n_segs

        return result


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = RingAreasBackend(conn)
        config = RingAreasConfig()

        try:
            output = backend.run(config)
            import json
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
