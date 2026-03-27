"""
Backend — SAP2000 Malla Rectangular (Standalone)
=================================================
Genera una malla rectangular de áreas en SAP2000 usando AddByCoord, en el
plano y con los parámetros especificados por el usuario.

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: backend_ring_areas.py / backend_template.py
"""

import math
import comtypes.client
from dataclasses import dataclass, field
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
class RectMeshConfig:
    """Parámetros de entrada para la malla rectangular."""

    # Dimensiones de la malla
    width: float = 500.0       # Dimensión 1 (X en XY/XZ, Y en YZ)
    length: float = 500.0      # Dimensión 2 (Y en XY, Z en XZ/YZ)

    # Divisiones
    nx: int = 5                # Número de divisiones en Dimensión 1
    ny: int = 5                # Número de divisiones en Dimensión 2

    # Origen
    start_x: float = 0.0
    start_y: float = 0.0
    start_z: float = 0.0

    # Plano y propiedad de área
    plane: str = "XY"          # "XY", "XZ", "YZ"
    prop_name: str = "Default"


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class RectMeshBackend:
    """Backend standalone para generar mallas rectangulares en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: RectMeshConfig) -> dict:
        """Genera la malla rectangular de áreas en el modelo activo de SAP2000.

        No inicializa un modelo nuevo; opera sobre el modelo abierto.

        Args:
            config: Parámetros de la malla.

        Returns:
            dict con resultados: success, num_areas, area_names, error.
        """
        SapModel = self.sap_model
        result: dict = {}

        # ── Validar parámetros ───────────────────────────────────────────
        if config.width <= 0 or config.length <= 0:
            raise ValueError("width y length deben ser > 0.")
        if config.nx < 1 or config.ny < 1:
            raise ValueError("nx y ny deben ser >= 1.")
        if config.plane.upper() not in ("XY", "XZ", "YZ"):
            raise ValueError(f"plane '{config.plane}' no válido. Use XY, XZ o YZ.")

        plane = config.plane.upper()
        d1 = config.width / config.nx
        d2 = config.length / config.ny

        # ── Task 1: Crear áreas celda por celda ─────────────────────────
        created_areas: List[str] = []

        for i in range(config.nx):
            for j in range(config.ny):
                u0 = i * d1
                v0 = j * d2

                us = [u0,       u0 + d1, u0 + d1, u0      ]
                vs = [v0,       v0,      v0 + d2, v0 + d2 ]

                xs, ys, zs = [], [], []
                for k in range(4):
                    u, v = us[k], vs[k]
                    if plane == "XY":
                        xs.append(config.start_x + u)
                        ys.append(config.start_y + v)
                        zs.append(config.start_z)
                    elif plane == "XZ":
                        xs.append(config.start_x + u)
                        ys.append(config.start_y)
                        zs.append(config.start_z + v)
                    else:  # YZ
                        xs.append(config.start_x)
                        ys.append(config.start_y + u)
                        zs.append(config.start_z + v)

                # AddByCoord(NumberPoints, x[], y[], z[], Name, PropName, UserName, CSys)
                ret = SapModel.AreaObj.AddByCoord(
                    4, xs, ys, zs, "", config.prop_name, "", "Global"
                )
                assert _check_ret(ret), f"AreaObj.AddByCoord failed en celda ({i},{j}): {ret}"

                if isinstance(ret, (list, tuple)) and len(ret) > 1:
                    area_name = str(ret[0])
                    if area_name:
                        created_areas.append(area_name)

        # ── Task 2: Refrescar vista ──────────────────────────────────────
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        result["success"] = True
        result["num_areas"] = len(created_areas)
        result["area_names"] = created_areas
        result["plane"] = plane
        result["grid"] = f"{config.nx}x{config.ny}"
        result["cell_size"] = f"{d1:.4f} x {d2:.4f}"
        return result


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = RectMeshBackend(conn)
        config = RectMeshConfig(
            width=500.0, length=500.0,
            nx=5, ny=5,
            start_x=0.0, start_y=0.0, start_z=0.0,
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
