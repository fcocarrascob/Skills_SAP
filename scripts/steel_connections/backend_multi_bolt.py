"""
Backend — SAP2000 Multi-Bolt Pattern (Patrón Multi-Perno)
==========================================================
Genera un patrón de múltiples pernos (filas × columnas) con soporte
para orientación arbitraria (plano + ángulo de inclinación).

Cada perno se modela como dos placas anulares (arandelas) enfrentadas,
conectadas por links Gap y una barra Frame central.

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: backend_bolt_plates.py
"""

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

from backend_bolt_plates import SapConnection, _check_ret, _shape_coords_2d


# ══════════════════════════════════════════════════════════════════════════════
# Sistema de coordenadas con orientación arbitraria
# ══════════════════════════════════════════════════════════════════════════════

def _build_axes(plane: str, angle_deg: float):
    """Construye los 3 ejes unitarios del plano de la conexión.

    Returns:
        (e_u, e_v, e_n) — vectores unitarios (tuple de 3 floats cada uno)
        e_u: dirección horizontal del patrón (columnas)
        e_v: dirección vertical del patrón (filas)
        e_n: normal al plano (dirección de separación entre placas)
    """
    theta = math.radians(angle_deg)
    c, s = math.cos(theta), math.sin(theta)

    if plane == "XZ":
        e_u = (c, 0.0, s)
        e_v = (-s, 0.0, c)
        e_n = (0.0, 1.0, 0.0)
    elif plane == "YZ":
        e_u = (0.0, c, s)
        e_v = (0.0, -s, c)
        e_n = (1.0, 0.0, 0.0)
    else:  # XY
        e_u = (c, s, 0.0)
        e_v = (-s, c, 0.0)
        e_n = (0.0, 0.0, 1.0)

    return e_u, e_v, e_n


def _local_to_global(
    origin: Tuple[float, float, float],
    e_u: Tuple[float, float, float],
    e_v: Tuple[float, float, float],
    e_n: Tuple[float, float, float],
    u: float, v: float, n: float,
) -> Tuple[float, float, float]:
    """P_global = origin + u·ê_u + v·ê_v + n·ê_n"""
    return (
        origin[0] + u * e_u[0] + v * e_v[0] + n * e_n[0],
        origin[1] + u * e_u[1] + v * e_v[1] + n * e_n[1],
        origin[2] + u * e_u[2] + v * e_v[2] + n * e_n[2],
    )


# ══════════════════════════════════════════════════════════════════════════════
# Generación de patrón
# ══════════════════════════════════════════════════════════════════════════════

def _generate_grid_centers(
    n_rows: int, n_cols: int, spacing_h: float, spacing_v: float,
) -> List[Tuple[float, float]]:
    """Genera centros de pernos en coordenadas locales 2D (u, v).

    El patrón se centra en (0, 0):
      u = dirección horizontal (columnas)
      v = dirección vertical (filas)
    """
    centers: List[Tuple[float, float]] = []
    total_w = (n_cols - 1) * spacing_h
    total_h = (n_rows - 1) * spacing_v

    for row in range(n_rows):
        for col in range(n_cols):
            u = col * spacing_h - total_w / 2.0
            v = row * spacing_v - total_h / 2.0
            centers.append((u, v))

    return centers


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class MultiBoltConfig:
    """Parámetros para patrón multi-perno con orientación arbitraria."""

    # ── Patrón de pernos ────────────────────────────────────────────────
    n_rows: int = 2
    n_cols: int = 3
    spacing_h: float = 75.0            # Separación horizontal (mm)
    spacing_v: float = 75.0            # Separación vertical (mm)

    # ── Espesores de placas ─────────────────────────────────────────────
    plate_thickness_1: float = 16.0
    plate_thickness_2: float = 16.0

    # ── Geometría por perno ─────────────────────────────────────────────
    bolt_diameter: float = 22.0        # Diámetro del perno / orificio (mm)
    outer_dim: float = 50.0            # Dimensión exterior arandela (mm)
    outer_shape: str = "Círculo"       # "Círculo" o "Cuadrado"

    # ── Discretización ──────────────────────────────────────────────────
    num_angular: int = 12              # Puntos por anillo (>= 3)
    num_radial: int = 2                # Anillos radiales (>= 1)

    # ── Ubicación (centro del patrón) ───────────────────────────────────
    origin_x: float = 0.0
    origin_y: float = 0.0
    origin_z: float = 0.0

    # ── Orientación ─────────────────────────────────────────────────────
    plane: str = "XZ"                  # Plano de la placa: "XZ", "YZ", "XY"
    angle: float = 0.0                 # Inclinación en grados dentro del plano

    # ── Propiedades SAP2000 ─────────────────────────────────────────────
    area_prop: str = "Default"
    gap_prop_name: str = "GAP_BOLT"
    gap_stiffness: float = 1.0e6
    initial_gap: float = 0.0
    bolt_material: str = "A36"
    bolt_section_name: str = ""

    # ── Grupo ────────────────────────────────────────────────────────────
    group_name: str = "MULTI_BOLT"


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class MultiBoltBackend:
    """Genera un patrón multi-perno con orientación arbitraria en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Helpers de API ───────────────────────────────────────────────────

    def _create_point(self, x: float, y: float, z: float) -> Optional[str]:
        try:
            ret = self.sap_model.PointObj.AddCartesian(x, y, z, "", "", "Global")
            if _check_ret(ret) and isinstance(ret, (list, tuple)) and len(ret) > 1:
                return str(ret[0])
        except Exception as exc:
            raise RuntimeError(
                f"PointObj.AddCartesian falló en ({x:.3f},{y:.3f},{z:.3f}): {exc}"
            )
        return None

    def _create_area(self, point_names: List[str], prop_name: str) -> Optional[str]:
        try:
            ret = self.sap_model.AreaObj.AddByPoint(
                len(point_names), point_names, "", prop_name, ""
            )
            if _check_ret(ret) and isinstance(ret, (list, tuple)) and len(ret) > 1:
                return str(ret[0])
        except Exception as exc:
            raise RuntimeError(
                f"AreaObj.AddByPoint falló con puntos {point_names}: {exc}"
            )
        return None

    def _ensure_gap_prop(self, config: MultiBoltConfig) -> None:
        k = config.gap_stiffness
        dis = config.initial_gap

        dof     = [True,  False, False, False, False, False]
        fixed   = [False, False, False, False, False, False]
        nonlin  = [True,  False, False, False, False, False]
        ke      = [k,     0.0,   0.0,   0.0,   0.0,   0.0]
        ce      = [0.0,   0.0,   0.0,   0.0,   0.0,   0.0]
        k_nl    = [k,     0.0,   0.0,   0.0,   0.0,   0.0]
        dis_nl  = [dis,   0.0,   0.0,   0.0,   0.0,   0.0]

        try:
            ret = self.sap_model.PropLink.SetGap(
                config.gap_prop_name,
                dof, fixed, nonlin, ke, ce, k_nl, dis_nl,
                0.0, 0.0,
            )
            rc = int(ret[-1]) if isinstance(ret, (list, tuple)) else int(ret)
            if rc != 0:
                raise RuntimeError(
                    f"PropLink.SetGap falló con código {rc}."
                )
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError(f"PropLink.SetGap excepción: {exc}")

    def _create_link(self, pt1: str, pt2: str, prop_name: str) -> Optional[str]:
        try:
            ret = self.sap_model.LinkObj.AddByPoint(
                pt1, pt2, "", False, prop_name, ""
            )
            if _check_ret(ret) and isinstance(ret, (list, tuple)) and len(ret) > 1:
                return str(ret[0])
        except Exception as exc:
            raise RuntimeError(
                f"LinkObj.AddByPoint falló entre {pt1} y {pt2}: {exc}"
            )
        return None

    def _ensure_bolt_section(self, config: MultiBoltConfig) -> Optional[str]:
        name = config.bolt_section_name.strip() if config.bolt_section_name else ""
        if not name:
            name = f"BOLT_{int(config.bolt_diameter)}"
        try:
            ret = self.sap_model.PropFrame.SetCircle(
                name, config.bolt_material, config.bolt_diameter
            )
            if _check_ret(ret):
                return name
        except Exception as exc:
            raise RuntimeError(f"PropFrame.SetCircle falló para '{name}': {exc}")
        return None

    def _create_frame_bar(
        self, pt1: str, pt2: str, section: str, tag: str
    ) -> Optional[str]:
        try:
            ret = self.sap_model.FrameObj.AddByPoint(pt1, pt2, "", section, tag)
            if _check_ret(ret) and isinstance(ret, (list, tuple)) and len(ret) > 1:
                return str(ret[0])
        except Exception as exc:
            raise RuntimeError(
                f"FrameObj.AddByPoint falló entre {pt1} y {pt2}: {exc}"
            )
        return None

    def _existing_body_count(self) -> int:
        try:
            ret = self.sap_model.ConstraintDef.GetNameList(0, [])
            if isinstance(ret, (list, tuple)) and int(ret[-1]) == 0:
                return int(ret[0])
        except Exception:
            pass
        return 0

    def _create_body_constraint(
        self, name: str, center_pt: str, ring_pts: List[str]
    ) -> bool:
        dof = [True, True, True, True, True, True]
        try:
            ret = self.sap_model.ConstraintDef.SetBody(name, dof, "Global")
            if not _check_ret(ret):
                return False
        except Exception:
            return False
        try:
            self.sap_model.PointObj.SetConstraint(center_pt, name)
        except Exception:
            return False
        for pt in ring_pts:
            if pt:
                try:
                    self.sap_model.PointObj.SetConstraint(pt, name)
                except Exception:
                    pass
        return True

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: MultiBoltConfig) -> dict:
        """Genera el patrón multi-perno completo en el modelo activo."""

        # ── Validaciones ────────────────────────────────────────────────
        if config.plate_thickness_1 <= 0 or config.plate_thickness_2 <= 0:
            raise ValueError("Los espesores de placa deben ser > 0.")
        if config.bolt_diameter <= 0:
            raise ValueError("El diámetro del perno debe ser > 0.")
        if config.outer_dim <= config.bolt_diameter:
            raise ValueError("outer_dim debe ser mayor que bolt_diameter.")
        if config.num_angular < 3:
            raise ValueError("num_angular debe ser >= 3.")
        if config.num_radial < 1:
            raise ValueError("num_radial debe ser >= 1.")
        if config.n_rows < 1 or config.n_cols < 1:
            raise ValueError("Filas y columnas deben ser >= 1.")
        plane = config.plane.upper()
        if plane not in ("XY", "XZ", "YZ"):
            raise ValueError(f"Plano '{config.plane}' no válido.")
        if config.n_cols > 1 and config.outer_dim > config.spacing_h:
            raise ValueError(
                f"outer_dim ({config.outer_dim}) debe ser menor que spacing_h "
                f"({config.spacing_h}) para evitar traslape."
            )
        if config.n_rows > 1 and config.outer_dim > config.spacing_v:
            raise ValueError(
                f"outer_dim ({config.outer_dim}) debe ser menor que spacing_v "
                f"({config.spacing_v}) para evitar traslape."
            )

        sep = (config.plate_thickness_1 + config.plate_thickness_2) / 2.0

        # ── Ejes de orientación ─────────────────────────────────────────
        e_u, e_v, e_n = _build_axes(plane, config.angle)
        origin = (config.origin_x, config.origin_y, config.origin_z)

        # ── Setup global (una sola vez) ─────────────────────────────────
        bolt_section = self._ensure_bolt_section(config)
        self._ensure_gap_prop(config)

        ret = self.sap_model.GroupDef.SetGroup(config.group_name)
        if not _check_ret(ret):
            raise RuntimeError(f"GroupDef.SetGroup falló: {ret}")

        # ── Centros de pernos en coordenadas locales 2D ─────────────────
        centers = _generate_grid_centers(
            config.n_rows, config.n_cols, config.spacing_h, config.spacing_v
        )

        # Coordenadas de anillos base (relativas al centro del perno)
        inner_coords = _shape_coords_2d(
            "Círculo", 0.0, 0.0, config.bolt_diameter, config.num_angular
        )
        outer_coords = _shape_coords_2d(
            config.outer_shape, 0.0, 0.0, config.outer_dim, config.num_angular
        )

        # ── Contadores globales ─────────────────────────────────────────
        total_areas = 0
        total_points = 0
        total_links = 0
        total_bolts = 0
        body_constraints_created = 0
        base_body_idx = self._existing_body_count() + 1

        # ── Loop principal: un perno por iteración ──────────────────────
        for bolt_idx, (u_bolt, v_bolt) in enumerate(centers):

            # ── Fase 1: Puntos de los anillos para ambas placas ─────────
            all_rings_p1: List[List[str]] = []
            all_rings_p2: List[List[str]] = []

            for r in range(config.num_radial + 1):
                fraction = (
                    r / float(config.num_radial) if config.num_radial > 0 else 1.0
                )
                ring_p1: List[str] = []
                ring_p2: List[str] = []

                for i in range(config.num_angular):
                    u_in, v_in = inner_coords[i]
                    u_out, v_out = outer_coords[i]
                    u_local = u_in + (u_out - u_in) * fraction
                    v_local = v_in + (v_out - v_in) * fraction

                    # Placa 1 (offset normal negativo)
                    gx, gy, gz = _local_to_global(
                        origin, e_u, e_v, e_n,
                        u_bolt + u_local, v_bolt + v_local, -sep / 2.0,
                    )
                    p1 = self._create_point(gx, gy, gz)
                    ring_p1.append(p1 or "")
                    if p1:
                        total_points += 1

                    # Placa 2 (offset normal positivo)
                    gx, gy, gz = _local_to_global(
                        origin, e_u, e_v, e_n,
                        u_bolt + u_local, v_bolt + v_local, +sep / 2.0,
                    )
                    p2 = self._create_point(gx, gy, gz)
                    ring_p2.append(p2 or "")
                    if p2:
                        total_points += 1

                all_rings_p1.append(ring_p1)
                all_rings_p2.append(ring_p2)

            # ── Centro de cada placa ────────────────────────────────────
            cx1, cy1, cz1 = _local_to_global(
                origin, e_u, e_v, e_n, u_bolt, v_bolt, -sep / 2.0,
            )
            cx2, cy2, cz2 = _local_to_global(
                origin, e_u, e_v, e_n, u_bolt, v_bolt, +sep / 2.0,
            )
            center_p1 = self._create_point(cx1, cy1, cz1)
            center_p2 = self._create_point(cx2, cy2, cz2)
            if center_p1:
                total_points += 1
            if center_p2:
                total_points += 1

            # ── Fase 2: Áreas (malla anular por placa) ──────────────────
            for r in range(config.num_radial):
                inner_r_p1 = all_rings_p1[r]
                outer_r_p1 = all_rings_p1[r + 1]
                inner_r_p2 = all_rings_p2[r]
                outer_r_p2 = all_rings_p2[r + 1]

                for i in range(config.num_angular):
                    j = (i + 1) % config.num_angular

                    # Placa 1
                    pts1 = [inner_r_p1[i], inner_r_p1[j],
                            outer_r_p1[j], outer_r_p1[i]]
                    if all(pts1):
                        a = self._create_area(pts1, config.area_prop)
                        if a:
                            total_areas += 1
                            self.sap_model.AreaObj.SetGroupAssign(
                                a, config.group_name, False
                            )

                    # Placa 2
                    pts2 = [inner_r_p2[i], inner_r_p2[j],
                            outer_r_p2[j], outer_r_p2[i]]
                    if all(pts2):
                        a = self._create_area(pts2, config.area_prop)
                        if a:
                            total_areas += 1
                            self.sap_model.AreaObj.SetGroupAssign(
                                a, config.group_name, False
                            )

            # ── Fase 3: Links Gap nodo a nodo ───────────────────────────
            for r in range(config.num_radial + 1):
                for i in range(config.num_angular):
                    pt1 = all_rings_p1[r][i]
                    pt2 = all_rings_p2[r][i]
                    if pt1 and pt2:
                        lnk = self._create_link(pt1, pt2, config.gap_prop_name)
                        if lnk:
                            total_links += 1

            # ── Fase 4: Barra de perno (Frame) ──────────────────────────
            if bolt_section and center_p1 and center_p2:
                self._create_frame_bar(
                    center_p1, center_p2, bolt_section, "BOLT_BAR"
                )

            # ── Fase 5: Body constraints (1 por placa, 2 por perno) ─────
            inner_p1_nodes = [pt for pt in all_rings_p1[0] if pt]
            inner_p2_nodes = [pt for pt in all_rings_p2[0] if pt]
            idx1 = base_body_idx + 2 * bolt_idx
            idx2 = idx1 + 1

            if center_p1:
                if self._create_body_constraint(
                    f"BODY_P{idx1}", center_p1, inner_p1_nodes
                ):
                    body_constraints_created += 1
            if center_p2:
                if self._create_body_constraint(
                    f"BODY_P{idx2}", center_p2, inner_p2_nodes
                ):
                    body_constraints_created += 1

            total_bolts += 1

        # ── Refresh ─────────────────────────────────────────────────────
        try:
            self.sap_model.View.RefreshView(0, False)
        except Exception:
            pass

        return {
            "success": True,
            "num_bolts": total_bolts,
            "num_areas": total_areas,
            "num_points": total_points,
            "num_links": total_links,
            "separation": sep,
            "plane": plane,
            "angle": config.angle,
            "gap_prop": config.gap_prop_name,
            "bolt_section": bolt_section,
            "body_constraints": body_constraints_created,
            "pattern": f"{config.n_rows}×{config.n_cols}",
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
        backend = MultiBoltBackend(conn)
        cfg = MultiBoltConfig(
            n_rows=2, n_cols=3,
            spacing_h=75.0, spacing_v=75.0,
            plate_thickness_1=16.0, plate_thickness_2=16.0,
            bolt_diameter=22.0, outer_dim=50.0,
            outer_shape="Círculo",
            num_angular=12, num_radial=2,
            origin_x=0.0, origin_y=0.0, origin_z=0.0,
            plane="XZ", angle=0.0,
            area_prop="Default",
            gap_prop_name="GAP_MULTI",
            gap_stiffness=1.0e6,
            initial_gap=0.0,
            bolt_material="A36",
            group_name="MULTI_BOLT_TEST",
        )
        try:
            output = backend.run(cfg)
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
