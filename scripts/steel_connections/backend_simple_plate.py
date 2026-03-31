"""
Backend — SAP2000 Placa Simple con Orientación Arbitraria
==========================================================
Genera una placa rectangular mallada en SAP2000, con soporte de
orientación arbitraria (plano + ángulo de inclinación) para hacer
match con conexiones apernadas inclinadas.

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: backend_mesh_rect.py / backend_multi_bolt.py
"""

from dataclasses import dataclass
from typing import List

from shared import SapConnection, _check_ret, _build_axes, _local_to_global_axes


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class SimplePlateConfig:
    """Parámetros de entrada para la placa simple con orientación arbitraria."""

    # ── Dimensiones ─────────────────────────────────────────────────────
    width: float = 500.0           # Ancho de la placa (dirección u)
    height: float = 500.0          # Alto de la placa (dirección v)

    # ── Discretización ──────────────────────────────────────────────────
    nx: int = 5                    # Divisiones en dirección u (ancho)
    ny: int = 5                    # Divisiones en dirección v (alto)

    # ── Ubicación (nodo inferior izquierdo de la placa) ───────────────
    origin_x: float = 0.0
    origin_y: float = 0.0
    origin_z: float = 0.0

    # ── Orientación ─────────────────────────────────────────────────────
    plane: str = "XZ"              # Plano base: "XY", "XZ", "YZ"
    angle: float = 0.0             # Rotación dentro del plano (grados)

    # ── Propiedades SAP2000 ─────────────────────────────────────────────
    material: str = "A36"          # Material de la placa
    thickness: float = 16.0        # Espesor de la placa (mm)

    # ── Grupo ───────────────────────────────────────────────────────────
    group_name: str = "SIMPLE_PLATE"


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class SimplePlateBackend:
    """Backend standalone para generar placas simples con orientación arbitraria."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: SimplePlateConfig) -> dict:
        """Genera la placa rectangular mallada en el modelo activo.

        La placa se posiciona con el nodo inferior izquierdo en
        (origin_x, origin_y, origin_z) y se orienta según plane + angle
        usando _build_axes().

        Returns:
            dict con: success, num_areas, plane, angle, grid, cell_size.
        """
        SapModel = self.sap_model

        # ── Validaciones ────────────────────────────────────────────────
        if config.width <= 0 or config.height <= 0:
            raise ValueError("width y height deben ser > 0.")
        if config.nx < 1 or config.ny < 1:
            raise ValueError("nx y ny deben ser >= 1.")
        plane = config.plane.upper()
        if plane not in ("XY", "XZ", "YZ"):
            raise ValueError(f"plane '{config.plane}' no válido. Use XY, XZ o YZ.")
        if config.thickness <= 0:
            raise ValueError("thickness debe ser > 0.")

        # ── Orientación ─────────────────────────────────────────────────
        e_u, e_v, e_n = _build_axes(plane, config.angle)
        origin = (config.origin_x, config.origin_y, config.origin_z)

        d_u = config.width / config.nx
        d_v = config.height / config.ny

        # ── Auto-crear propiedad Shell ───────────────────────────────────
        shell_prop = f"PLATE_{config.material}_{config.thickness:.0f}"
        ret = SapModel.PropArea.SetShell_1(
            shell_prop, 1, False, config.material, 0.0,
            config.thickness, config.thickness
        )
        if not _check_ret(ret):
            shell_prop = "Default"

        # ── Grupo ───────────────────────────────────────────────────────
        ret = SapModel.GroupDef.SetGroup(config.group_name)
        if not _check_ret(ret):
            raise RuntimeError(f"GroupDef.SetGroup falló: {ret}")

        # ── Crear áreas celda por celda ─────────────────────────────────
        created_areas: List[str] = []

        for i in range(config.nx):
            for j in range(config.ny):
                # Coordenadas locales de las 4 esquinas (origen = esquina inf-izq)
                u0 = i * d_u
                v0 = j * d_v

                us = [u0,       u0 + d_u, u0 + d_u, u0      ]
                vs = [v0,       v0,       v0 + d_v, v0 + d_v]

                xs, ys, zs = [], [], []
                for k in range(4):
                    gx, gy, gz = _local_to_global_axes(
                        origin, e_u, e_v, e_n, us[k], vs[k], 0.0
                    )
                    xs.append(gx)
                    ys.append(gy)
                    zs.append(gz)

                ret = SapModel.AreaObj.AddByCoord(
                    4, xs, ys, zs, "", shell_prop, "", "Global"
                )
                if not _check_ret(ret):
                    raise RuntimeError(
                        f"AreaObj.AddByCoord falló en celda ({i},{j}): {ret}"
                    )

                if isinstance(ret, (list, tuple)) and len(ret) > 1:
                    area_name = str(ret[0])
                    if area_name:
                        created_areas.append(area_name)
                        SapModel.AreaObj.SetGroupAssign(
                            area_name, config.group_name, False
                        )

        # ── Refresh ──────────────────────────────────────────────────────
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        return {
            "success": True,
            "num_areas": len(created_areas),
            "area_names": created_areas,
            "plane": plane,
            "angle": config.angle,
            "grid": f"{config.nx}x{config.ny}",
            "cell_size": f"{d_u:.4f} x {d_v:.4f}",
            "shell_prop": shell_prop,
            "group": config.group_name,
        }


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json

    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = SimplePlateBackend(conn)
        config = SimplePlateConfig(
            width=500.0, height=500.0,
            nx=5, ny=5,
            origin_x=0.0, origin_y=0.0, origin_z=0.0,
            plane="XZ", angle=30.0,
            material="A36",
            thickness=16.0,
            group_name="PLATE_TEST",
        )
        try:
            output = backend.run(config)
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
