"""
Backend — SAP2000 Vertical Cylinder Generator (Standalone)
==========================================================
Genera un cilindro vertical discretizado con elementos shell cuadriláteros.

Conexión: COM directo vía comtypes.client (sin MCP).
"""

import math
from dataclasses import dataclass

from backend_ring_areas import SapConnection


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class CylinderConfig:
    """Parámetros de entrada para el generador de cilindro vertical."""

    # Geometría [m]
    radius: float = 5.0
    height: float = 10.0

    # Espesor de shell [m]
    thickness: float = 0.25

    # Material (nombre existente en el modelo)
    mat_name: str = "CONC"

    # Discretización
    n_radial: int = 36   # segmentos angulares (circunferencia)
    n_vert: int = 10     # divisiones verticales


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class CylinderBackend:
    """Backend standalone para generar cilindros verticales en SAP2000."""

    PROP_NAME = "SHELL_CYL"

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def get_materials(self) -> list:
        """Devuelve la lista de materiales definidos en el modelo activo."""
        raw = self.sap_model.PropMaterial.GetNameList()
        assert raw[-1] == 0, f"GetNameList failed: {raw[-1]}"
        return list(raw[1]) if raw[0] > 0 else []

    def run(self, config: CylinderConfig) -> dict:
        """Genera el cilindro vertical en SAP2000.

        Args:
            config: Parámetros de entrada.

        Returns:
            dict con resultados del modelo generado.
        """
        SapModel = self.sap_model
        result = {}

        # ── Task 1: Propiedad de sección shell ───────────────────────────
        ret = SapModel.PropArea.SetShell_1(
            self.PROP_NAME, 1, True, config.mat_name, 0,
            config.thickness, config.thickness
        )
        assert ret == 0, f"SetShell_1 failed: {ret}"
        result["task_1_section"] = {self.PROP_NAME: config.thickness}

        # ── Task 2: Geometría del cilindro ───────────────────────────────
        n  = config.n_radial
        nv = config.n_vert
        dz = config.height / nv
        area_count = 0

        for j in range(nv):
            z0 = j * dz
            z1 = z0 + dz
            for i in range(n):
                i_next = (i + 1) % n
                a0 = 2.0 * math.pi * i / n
                a1 = 2.0 * math.pi * i_next / n

                x = [config.radius * math.cos(a0),
                     config.radius * math.cos(a1),
                     config.radius * math.cos(a1),
                     config.radius * math.cos(a0)]
                y = [config.radius * math.sin(a0),
                     config.radius * math.sin(a1),
                     config.radius * math.sin(a1),
                     config.radius * math.sin(a0)]
                z = [z0, z0, z1, z1]

                raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", self.PROP_NAME, "")
                assert raw[-1] == 0, f"AddByCoord[{j},{i}] failed: {raw[-1]}"
                area_count += 1

        result["task_2_geometry"] = {"total_areas": area_count}
        result["total_areas"] = area_count

        # ── Task 3: Refrescar vista ──────────────────────────────────────
        SapModel.View.RefreshView(0, False)

        # ── Resumen final ────────────────────────────────────────────────
        result["success"]   = True
        result["radius"]    = config.radius
        result["height"]    = config.height
        result["thickness"] = config.thickness
        result["n_radial"]  = config.n_radial
        result["n_vert"]    = config.n_vert

        return result
