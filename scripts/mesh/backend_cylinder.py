"""
Backend — SAP2000 Vertical Cylinder Generator (Standalone)
==========================================================
Genera un cilindro vertical discretizado con elementos shell cuadriláteros.

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
class CylinderConfig:
    """Parámetros de entrada para el generador de cilindro vertical."""

    # Geometría [m]
    radius: float = 5.0
    height: float = 10.0

    # Discretización
    n_radial: int = 36   # segmentos angulares (circunferencia)
    n_vert: int = 10     # divisiones verticales

    # Ubicación — base del cilindro
    center_x: float = 0.0
    center_y: float = 0.0
    base_z: float = 0.0

    # Propiedad de área (nombre existente en el modelo)
    prop_name: str = "Default"


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class CylinderBackend:
    """Backend standalone para generar cilindros verticales en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config: CylinderConfig) -> dict:
        """Genera el cilindro vertical en el modelo activo de SAP2000.

        No inicializa modelo nuevo; opera sobre el modelo abierto.

        Args:
            config: Parámetros de entrada.

        Returns:
            dict con resultados del modelo generado.
        """
        # ── Validar parámetros ───────────────────────────────────────────
        if config.radius <= 0 or config.height <= 0:
            raise ValueError("radius y height deben ser > 0.")
        if config.n_radial < 3:
            raise ValueError("n_radial debe ser >= 3.")
        if config.n_vert < 1:
            raise ValueError("n_vert debe ser >= 1.")

        SapModel = self.sap_model
        result: dict = {}

        # ── Task 1: Geometría del cilindro ───────────────────────────────
        n  = config.n_radial
        nv = config.n_vert
        dz = config.height / nv
        area_count = 0

        for j in range(nv):
            z0 = config.base_z + j * dz
            z1 = z0 + dz
            for i in range(n):
                i_next = (i + 1) % n
                a0 = 2.0 * math.pi * i / n
                a1 = 2.0 * math.pi * i_next / n

                xs = [config.center_x + config.radius * math.cos(a0),
                      config.center_x + config.radius * math.cos(a1),
                      config.center_x + config.radius * math.cos(a1),
                      config.center_x + config.radius * math.cos(a0)]
                ys = [config.center_y + config.radius * math.sin(a0),
                      config.center_y + config.radius * math.sin(a1),
                      config.center_y + config.radius * math.sin(a1),
                      config.center_y + config.radius * math.sin(a0)]
                zs = [z0, z0, z1, z1]

                ret = SapModel.AreaObj.AddByCoord(
                    4, xs, ys, zs, "", config.prop_name, "", "Global"
                )
                assert _check_ret(ret), f"AddByCoord[{j},{i}] failed: {ret}"
                area_count += 1

        # ── Task 2: Refrescar vista ──────────────────────────────────────
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        result["success"]   = True
        result["num_areas"] = area_count
        result["radius"]    = config.radius
        result["height"]    = config.height
        result["n_radial"]  = config.n_radial
        result["n_vert"]    = config.n_vert
        result["center"]    = (config.center_x, config.center_y, config.base_z)
        result["prop_name"] = config.prop_name
        return result


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = CylinderBackend(conn)
        config = CylinderConfig(
            radius=5.0, height=10.0,
            n_radial=36, n_vert=10,
            center_x=0.0, center_y=0.0, base_z=0.0,
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
