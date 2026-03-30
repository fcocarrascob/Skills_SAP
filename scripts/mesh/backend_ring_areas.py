"""
Backend — SAP2000 Circular Ring Area Generator (Standalone)
============================================================
Genera un anillo circular (placa anular) discretizado con elementos shell,
dividido en dos sub-anillos concéntricos (interior y exterior) con la misma
propiedad de área. El radio medio se calcula automáticamente como el promedio
de radio interior y radio exterior.

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: backend_mesh_rect.py / backend_mesh_hole.py
"""

import math
import comtypes.client
from dataclasses import dataclass
from typing import List


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
        """Conecta a una instancia de SAP2000 en ejecución.

        Args:
            attach_to_existing: Si True, se conecta a la instancia ya abierta.

        Returns:
            dict con claves: connected, version, model_path, error (si falla).
        """
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
        """Libera la referencia COM (no cierra SAP2000)."""
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Helpers internos
# ══════════════════════════════════════════════════════════════════════════════

def _check_ret(ret) -> bool:
    """Retorna True si el código de retorno de la API es 0 (éxito)."""
    if isinstance(ret, (list, tuple)):
        return int(ret[-1]) == 0
    return int(ret) == 0


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class RingAreasConfig:
    """Parámetros de entrada para el generador de anillo."""

    # Radios [m]
    r_inner: float = 1.0
    r_outer: float = 5.0

    # Discretización
    n_segs: int = 36

    # Ubicación — centro del anillo
    center_x: float = 0.0
    center_y: float = 0.0
    center_z: float = 0.0

    # Plano de dibujo
    plane: str = "XY"          # "XY", "XZ", "YZ"

    # Propiedad de área (nombre existente en el modelo)
    prop_name: str = "Default"


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

    # ── Helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def _ring_pts_2d(radius: float, n: int) -> List[tuple]:
        """Devuelve n puntos (u, v) sobre una circunferencia."""
        return [
            (radius * math.cos(2.0 * math.pi * i / n),
             radius * math.sin(2.0 * math.pi * i / n))
            for i in range(n)
        ]

    @staticmethod
    def _to_global(
        u: float, v: float,
        cx: float, cy: float, cz: float,
        plane: str,
    ):
        """Convierte coordenadas locales 2D al espacio global 3D."""
        if plane == "XY":
            return cx + u, cy + v, cz
        if plane == "XZ":
            return cx + u, cy, cz + v
        # YZ
        return cx, cy + u, cz + v

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: RingAreasConfig) -> dict:
        """Genera el anillo de shells en el modelo activo de SAP2000.

        No inicializa modelo nuevo; opera sobre el modelo abierto.
        El radio medio se calcula automáticamente (promedio de r_inner y r_outer)
        y divide el anillo en dos sub-anillos con la misma propiedad.

        Args:
            config: Parámetros de entrada.

        Returns:
            dict con resultados del modelo generado.
        """
        # ── Validar parámetros ───────────────────────────────────────────
        if config.r_inner <= 0 or config.r_outer <= 0:
            raise ValueError("r_inner y r_outer deben ser > 0.")
        if config.r_inner >= config.r_outer:
            raise ValueError("r_inner debe ser menor que r_outer.")
        if config.n_segs < 3:
            raise ValueError("n_segs debe ser >= 3.")
        if config.plane.upper() not in ("XY", "XZ", "YZ"):
            raise ValueError(f"plane '{config.plane}' no válido. Use XY, XZ o YZ.")

        plane = config.plane.upper()
        r_mid = (config.r_inner + config.r_outer) / 2.0
        n = config.n_segs

        SapModel = self.sap_model
        result: dict = {}

        # ── Task 1: Generar geometría de anillos ─────────────────────────
        zones = [
            (config.r_inner, r_mid,          "anillo_interior"),
            (r_mid,          config.r_outer, "anillo_exterior"),
        ]
        area_count = {"anillo_interior": 0, "anillo_exterior": 0}

        for (r_in, r_out, label) in zones:
            pts_in  = self._ring_pts_2d(r_in,  n)
            pts_out = self._ring_pts_2d(r_out, n)

            for i in range(n):
                j = (i + 1) % n

                u = [pts_in[i][0], pts_out[i][0], pts_out[j][0], pts_in[j][0]]
                v = [pts_in[i][1], pts_out[i][1], pts_out[j][1], pts_in[j][1]]

                xs, ys, zs = [], [], []
                for k in range(4):
                    gx, gy, gz = self._to_global(
                        u[k], v[k],
                        config.center_x, config.center_y, config.center_z,
                        plane,
                    )
                    xs.append(gx)
                    ys.append(gy)
                    zs.append(gz)

                ret = SapModel.AreaObj.AddByCoord(
                    4, xs, ys, zs, "", config.prop_name, "", "Global"
                )
                assert _check_ret(ret), f"AddByCoord({label}[{i}]) failed: {ret}"
                area_count[label] += 1

        # ── Task 2: Refrescar vista ──────────────────────────────────────
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        result["success"]    = True
        result["num_areas"]  = sum(area_count.values())
        result["area_count"] = area_count
        result["r_inner"]    = config.r_inner
        result["r_mid"]      = r_mid
        result["r_outer"]    = config.r_outer
        result["n_segs"]     = config.n_segs
        result["plane"]      = plane
        result["center"]     = (config.center_x, config.center_y, config.center_z)
        result["prop_name"]  = config.prop_name
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
        config = RingAreasConfig(
            r_inner=1.0, r_outer=5.0,
            n_segs=36,
            center_x=0.0, center_y=0.0, center_z=0.0,
            plane="XY",
            prop_name="Default",
        )
        try:
            import json
            output = backend.run(config)
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
