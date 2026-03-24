"""
Backend — SAP2000 Placa Base Generator (Standalone)
=====================================================
Genera un modelo parametrizado de placa base con pernos de anclaje,
silla opcional, body constraints, TC limits, y resortes de balasto.

Conexión: COM directo vía comtypes.client (sin MCP).
Basado en: placabase_backend.py (migrado a standalone, sin app_logger/sap_utils_common)
"""

import math
import comtypes.client
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


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

DIA_TO_SPACING = {
    16: (80, 80), 19: (100, 100), 22: (100, 100), 25: (100, 100),
    32: (125, 125), 38: (150, 150), 44: (175, 175), 51: (200, 200),
    57: (225, 225), 64: (250, 250),
}


@dataclass
class PlacaBaseConfig:
    """Parámetros de entrada para el generador de placa base."""

    # Pernos
    bolt_dia: float = 25.0
    bolt_material: str = "A36"
    n_pernos: int = 4
    bolt_centers: List[Tuple[float, float, float]] = field(default_factory=list)

    # Columna
    H_col: float = 300.0
    B_col: float = 250.0

    # Espesores
    plate_thickness: float = 20.0
    flange_thickness: float = 15.0
    web_thickness: float = 10.0

    # Silla de anclaje
    include_anchor_chair: bool = False
    anchor_chair_height: float = 50.0
    anchor_chair_thickness: float = 15.0

    # Balasto
    ks_balasto: float = 0.0  # kgf/cm³ — 0 para omitir

    @staticmethod
    def map_dia_to_spacing(dia: float) -> Tuple[float, float]:
        d = int(round(float(dia)))
        return DIA_TO_SPACING.get(d, (100.0, 100.0))

    def resolve_bolt_centers(self):
        """Auto-genera bolt_centers si está vacío."""
        if not self.bolt_centers:
            A, _ = self.map_dia_to_spacing(self.bolt_dia)
            H = self.H_col
            self.bolt_centers = [
                (A / 2.0, H / 2.0, 0.0), (3 * A / 2.0, H / 2.0, 0.0),
                (-A / 2.0, H / 2.0, 0.0), (-3 * A / 2.0, H / 2.0, 0.0),
                (A / 2.0, -H / 2.0, 0.0), (3 * A / 2.0, -H / 2.0, 0.0),
                (-A / 2.0, -H / 2.0, 0.0), (-3 * A / 2.0, -H / 2.0, 0.0),
            ]
            self.bolt_centers = self.bolt_centers[: self.n_pernos]


# ══════════════════════════════════════════════════════════════════════════════
# Helpers — ret code checking (inline, replaces sap_utils_common)
# ══════════════════════════════════════════════════════════════════════════════

def _check_ret(ret) -> bool:
    """Verifica si un return code/tuple indica éxito (0)."""
    if isinstance(ret, (list, tuple)):
        return len(ret) > 0 and int(ret[-1]) == 0
    return int(ret) == 0


def _get_name(ret, fallback: str) -> str:
    """Extrae el nombre creado de un retorno COM (primer elemento)."""
    if isinstance(ret, (list, tuple)) and len(ret) >= 2 and ret[-1] == 0:
        val = ret[0]
        if isinstance(val, (list, tuple)) and len(val) > 0:
            return str(val[0])
        return str(val)
    return fallback


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class PlacaBaseBackend:
    """Backend standalone para generar placa base en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def _log(self, message: str):
        """Log a stdout (standalone no tiene logger externo)."""
        print(message)

    # ── Funciones de geometría ───────────────────────────────────────────

    def _create_point(self, x: float, y: float, z: float, user_name: str = "") -> Optional[str]:
        ret = self.sap_model.PointObj.AddCartesian(x, y, z, "", user_name)
        if _check_ret(ret):
            return _get_name(ret, user_name)
        return None

    def _create_area_by_points(self, points: List[str], prop: str, user_name: str = "") -> Optional[str]:
        ret = self.sap_model.AreaObj.AddByPoint(len(points), points, "", prop, user_name)
        if _check_ret(ret):
            return _get_name(ret, user_name)
        return None

    def _create_area_by_coord(self, xs, ys, zs, prop: str, user_name: str = "") -> Optional[str]:
        ret = self.sap_model.AreaObj.AddByCoord(len(xs), xs, ys, zs, "", prop, user_name, "Global")
        if _check_ret(ret):
            return _get_name(ret, user_name)
        return None

    def _get_point_coord(self, name: str) -> Optional[Tuple[float, float, float]]:
        try:
            ret = self.sap_model.PointObj.GetCoordCartesian(name, 0.0, 0.0, 0.0, "Global")
            if _check_ret(ret):
                return (ret[0], ret[1], ret[2])
        except Exception:
            pass
        return None

    def _create_shell_prop(self, name: str, thickness: float, mat: str = "A992Fy50"):
        """Crea propiedad shell con fallback SetShell_1 → SetShell."""
        try:
            ret = self.sap_model.PropArea.SetShell_1(name, 1, True, mat, 0.0, thickness, thickness)
            if _check_ret(ret):
                self._log(f"Propiedad '{name}' creada (SetShell_1).")
                return True
        except AttributeError:
            try:
                ret = self.sap_model.PropArea.SetShell(name, 1, mat, 0.0, thickness, thickness)
                if _check_ret(ret):
                    self._log(f"Propiedad '{name}' creada (SetShell).")
                    return True
            except Exception as e:
                self._log(f"Error creando propiedad '{name}': {e}")
        except Exception as e:
            self._log(f"Error creando propiedad '{name}': {e}")
        return False

    def _create_circle_points(self, cx, cy, z, radius, num_points=16, prefix="P_c"):
        names = []
        for j in range(num_points):
            angle = -math.radians(j * (360.0 / num_points))
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            nm = self._create_point(x, y, z, f"{prefix}{j + 1}")
            names.append(nm)
        return names

    def _create_square_points(self, cx, cy, z, side, num_points=16, prefix="P_s"):
        half = side / 2.0
        perimeter = 4.0 * side
        names = []
        if num_points < 4:
            num_points = 4

        for i in range(num_points):
            s = (i * perimeter) / num_points
            if s < half:
                x, y = half, -s
            elif s < half + side:
                rem = s - half
                x, y = half - rem, -half
            elif s < half + 2 * side:
                rem = s - (half + side)
                x, y = -half, -half + rem
            elif s < half + 3 * side:
                rem = s - (half + 2 * side)
                x, y = -half + rem, half
            else:
                rem = s - (half + 3 * side)
                x, y = half, half - rem

            nm = self._create_point(cx + x, cy + y, z, f"{prefix}{i + 1}")
            names.append(nm)
        return names

    def _sort_points_angularly(self, point_names, center):
        valid_pts = []
        for pn in point_names:
            if not pn:
                continue
            coord = self._get_point_coord(pn)
            if coord:
                angle = math.atan2(coord[1] - center[1], coord[0] - center[0])
                valid_pts.append((pn, angle))
        valid_pts.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in valid_pts]

    def _align_rings(self, inner_pts, outer_pts, center):
        inner_sorted = self._sort_points_angularly(inner_pts, center)
        outer_sorted = self._sort_points_angularly(outer_pts, center)
        if not inner_sorted or not outer_sorted:
            return inner_sorted, outer_sorted

        def get_angles(pts):
            angles = []
            for p in pts:
                c = self._get_point_coord(p)
                if c:
                    angles.append(math.atan2(c[1] - center[1], c[0] - center[0]))
                else:
                    angles.append(0)
            return angles

        inner_angs = get_angles(inner_sorted)
        outer_angs = get_angles(outer_sorted)
        n = len(inner_sorted)
        best_shift = 0
        min_diff = float("inf")
        for shift in range(n):
            diff = 0
            for i in range(n):
                a1 = inner_angs[i]
                a2 = outer_angs[(i + shift) % n]
                d = abs(a1 - a2) % (2 * math.pi)
                d = min(d, 2 * math.pi - d)
                diff += d
            if diff < min_diff:
                min_diff = diff
                best_shift = shift
        if best_shift != 0:
            outer_sorted = outer_sorted[best_shift:] + outer_sorted[:best_shift]
        return inner_sorted, outer_sorted

    def _create_ring_mesh(self, inner_pts, outer_pts, center, prefix, prop):
        inner, outer = self._align_rings(inner_pts, outer_pts, center)
        n = min(len(inner), len(outer))
        for i in range(n):
            p1 = inner[i]
            p2 = inner[(i + 1) % n]
            p3 = outer[(i + 1) % n]
            p4 = outer[i]
            self._create_area_by_points([p1, p2, p3, p4], prop, f"{prefix}_{i + 1}")

    def _coordinate_range(self, xmin, xmax, ymin, ymax, zmin, zmax,
                          deselect=False, csys="Global", include_intersections=False,
                          point=True, line=True, area=True, solid=True, link=True):
        try:
            ret = self.sap_model.SelectObj.CoordinateRange(
                float(xmin), float(xmax), float(ymin), float(ymax),
                float(zmin), float(zmax), bool(deselect), str(csys),
                bool(include_intersections),
                bool(point), bool(line), bool(area), bool(solid), bool(link),
            )
        except Exception:
            return False, None
        if isinstance(ret, (list, tuple)):
            return int(ret[-1]) == 0, ret
        return int(ret) == 0, ret

    def _divide_area_by_selection(self, area_name: str) -> list:
        try:
            ret = self.sap_model.EditArea.Divide(
                str(area_name), 3, 0, [], 0, 0, 0.0, 0.0, False, False, True
            )
            if _check_ret(ret) and len(ret) >= 2:
                names = ret[1]
                if isinstance(names, (list, tuple)):
                    return list(names)
        except Exception:
            pass
        return []

    def _subdivide_areas(self, area_names, n1=2, n2=2):
        for name in area_names:
            try:
                self.sap_model.EditArea.Divide(name, 1, 0, [], n1, n2)
            except Exception:
                pass

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: PlacaBaseConfig) -> dict:
        """Ejecuta la generación completa de placa base.

        Args:
            config: Parámetros de entrada (auto-resuelve bolt_centers si vacío).

        Returns:
            dict con resultados del modelo generado.
        """
        config.resolve_bolt_centers()
        self._log("Iniciando generación de placa base...")
        self._log(f"Pernos: {len(config.bolt_centers)} | H={config.H_col} B={config.B_col} | dia={config.bolt_dia}")
        SapModel = self.sap_model
        result = {}

        H = config.H_col
        B = config.B_col
        A, B_bolt = config.map_dia_to_spacing(config.bolt_dia)
        circle_radius = config.bolt_dia / 2.0
        outer_half = B_bolt / 2.0
        inner_half = (circle_radius + outer_half) / 2.0
        inner_side = inner_half * 2.0
        bolt_length = 8.0 * config.bolt_dia
        z_col = 2.0 * H

        # ── Task 1: Propiedades de material y shell ──────────────────────
        plate_prop = "PLACA_BASE"
        if config.plate_thickness:
            self._create_shell_prop(plate_prop, config.plate_thickness)
        if config.flange_thickness:
            self._create_shell_prop("ALA", config.flange_thickness)
        if config.web_thickness:
            self._create_shell_prop("ALMA", config.web_thickness)

        chair_prop = None
        if config.include_anchor_chair and config.anchor_chair_height > 0 and config.anchor_chair_thickness > 0:
            chair_prop = "ChairPlate"
            self._create_shell_prop(chair_prop, config.anchor_chair_thickness)

        self._log("Task 1: Propiedades de material creadas.")
        result["task_1_properties"] = True

        # ── Task 1b: Sección Frame para pernos ──────────────────────────
        bolt_section = f"BOLT_{int(config.bolt_dia)}"
        ret = SapModel.PropFrame.SetCircle(bolt_section, config.bolt_material, config.bolt_dia)
        bolt_section_ok = _check_ret(ret)
        result["bolt_section"] = bolt_section if bolt_section_ok else None
        if bolt_section_ok:
            self._log(f"Sección Frame '{bolt_section}' creada (d={config.bolt_dia}, mat={config.bolt_material}).")
        else:
            self._log(f"⚠ No se pudo crear la sección Frame del perno.")

        # ── Task 2: Geometría de columna ─────────────────────────────────
        self._create_area_by_coord(
            [-B / 2, B / 2, B / 2, -B / 2],
            [H / 2, H / 2, H / 2, H / 2],
            [0, 0, z_col, z_col],
            "ALA", "COL_FLANGE_TOP",
        )
        self._create_area_by_coord(
            [-B / 2, B / 2, B / 2, -B / 2],
            [-H / 2, -H / 2, -H / 2, -H / 2],
            [0, 0, z_col, z_col],
            "ALA", "COL_FLANGE_BOTTOM",
        )
        self._create_area_by_coord(
            [0, 0, 0, 0],
            [H / 2, -H / 2, -H / 2, H / 2],
            [0, 0, z_col, z_col],
            "ALMA", "COL_WEB",
        )
        self._log("Task 2: Geometría de columna creada.")
        result["task_2_column"] = True

        # ── Task 3: Áreas de pernos y mesh ───────────────────────────────
        outer_square_points_list = []
        chair_outer_square_points_list = []
        bolt_frame_names = []

        for idx, (cx, cy, cz) in enumerate(config.bolt_centers, 1):
            self._log(f"Procesando perno {idx} en ({cx}, {cy}, {cz})...")
            self._create_point(cx, cy, cz, f"CENTER_{idx}")

            c_pts = self._create_circle_points(cx, cy, cz, circle_radius, 16, f"P_c{idx}_")
            in_pts = self._create_square_points(cx, cy, cz, inner_side, 16, f"P_s_in{idx}_")
            out_pts = self._create_square_points(cx, cy, cz, B_bolt, 16, f"P_s_out{idx}_")
            outer_square_points_list.append(out_pts)

            if config.plate_thickness:
                self._create_ring_mesh(c_pts, in_pts, (cx, cy), f"A_ring_in{idx}", plate_prop)
                self._create_ring_mesh(in_pts, out_pts, (cx, cy), f"A_ring_out{idx}", plate_prop)

            # Bolt Frames + Body Constraints
            if bolt_section_ok:
                center_name = f"CENTER_{idx}"

                if chair_prop:
                    # CON SILLA: perno de 2 tramos
                    chair_center, chair_c_pts, chair_out_pts = self._create_single_chair(
                        idx, cx, cy, config.anchor_chair_height,
                        circle_radius, inner_side, B_bolt, chair_prop,
                    )
                    chair_outer_square_points_list.append(chair_out_pts)

                    # Tramo superior: silla → placa
                    chair_frame = self._create_chair_bolt_frame(
                        chair_center, center_name, bolt_section, idx
                    )
                    if chair_frame:
                        bolt_frame_names.append(chair_frame)

                    # Tramo inferior: placa → fundación
                    frame_name, bottom_pt = self._create_bolt_frame(
                        center_name, cx, cy, cz, bolt_section, bolt_length, idx
                    )
                    if frame_name:
                        bolt_frame_names.append(frame_name)

                    # Body Constraint en silla (todos DOF)
                    self._create_body_constraint(
                        f"BOLT_BODY_CHAIR_{idx}", chair_center, chair_c_pts,
                        [True, True, True, True, True, True],
                    )
                    # Body Constraint en placa (UZ libre)
                    self._create_body_constraint(
                        f"BOLT_BODY_{idx}", center_name, c_pts,
                        [True, True, False, True, True, True],
                    )
                    if frame_name and bottom_pt:
                        self._set_pin_restraint(bottom_pt)
                else:
                    # SIN SILLA: perno de 1 tramo
                    frame_name, bottom_pt = self._create_bolt_frame(
                        center_name, cx, cy, cz, bolt_section, bolt_length, idx
                    )
                    if frame_name:
                        bolt_frame_names.append(frame_name)
                        self._create_body_constraint(
                            f"BOLT_BODY_{idx}", center_name, c_pts,
                            [True, True, True, True, True, True],
                        )
                        self._set_pin_restraint(bottom_pt)

        self._log(f"Task 3: {len(config.bolt_centers)} pernos procesados, {len(bolt_frame_names)} frames creados.")
        result["task_3_bolts"] = len(config.bolt_centers)
        result["bolt_frames"] = len(bolt_frame_names)

        # ── Task 4: Área de enlace ───────────────────────────────────────
        if len(config.bolt_centers) >= 4 and len(outer_square_points_list) == len(config.bolt_centers):
            try:
                N = len(config.bolt_centers) // 2
                if 2 * N - 1 < len(outer_square_points_list):
                    p1 = outer_square_points_list[N][10]
                    p2 = outer_square_points_list[2 * N - 1][14]
                    p3 = outer_square_points_list[N - 1][2]
                    p4 = outer_square_points_list[0][6]
                    link_area = self._create_area_by_points(
                        [p1, p2, p3, p4], plate_prop, "A_outer_link"
                    )
                    if link_area:
                        self.sap_model.EditArea.Divide(link_area, 1, 0, [], 4 * config.n_pernos, 10)
            except Exception:
                pass

        if chair_prop and len(chair_outer_square_points_list) >= 4:
            try:
                N = len(config.bolt_centers) // 2
                if 2 * N - 1 < len(chair_outer_square_points_list):
                    p1 = chair_outer_square_points_list[N][10]
                    p2 = chair_outer_square_points_list[2 * N - 1][14]
                    p3 = chair_outer_square_points_list[N - 1][2]
                    p4 = chair_outer_square_points_list[0][6]
                    chair_link = self._create_area_by_points(
                        [p1, p2, p3, p4], chair_prop, "A_chair_link"
                    )
                    if chair_link:
                        self.sap_model.EditArea.Divide(chair_link, 1, 0, [], 4 * config.n_pernos, 10)
            except Exception:
                pass

        # Chair-level column points
        if chair_prop and config.anchor_chair_height:
            z_ch = config.anchor_chair_height
            self._create_point(-B / 2, H / 2, z_ch, "COL_FT_CHAIR_L")
            self._create_point(B / 2, H / 2, z_ch, "COL_FT_CHAIR_R")
            self._create_point(-B / 2, -H / 2, z_ch, "COL_FB_CHAIR_L")
            self._create_point(B / 2, -H / 2, z_ch, "COL_FB_CHAIR_R")
            self._create_point(0, H / 2, z_ch, "COL_WEB_CHAIR_T")
            self._create_point(0, -H / 2, z_ch, "COL_WEB_CHAIR_B")

        self._log("Task 4: Áreas de enlace creadas.")
        result["task_4_link_area"] = True

        # ── Task 5: Mesh refinement ──────────────────────────────────────
        try:
            z_target = 0.0

            # Top flange
            SapModel.SelectObj.ClearSelection()
            ok, _ = self._coordinate_range(
                -B / 2, B / 2, H / 2, H / 2, z_target, z_target,
                deselect=False, csys="Global", include_intersections=True,
                point=True, line=False, area=False, solid=False, link=False,
            )
            if chair_prop and config.anchor_chair_height:
                self._coordinate_range(
                    -B / 2, B / 2, H / 2, H / 2,
                    config.anchor_chair_height, config.anchor_chair_height,
                    deselect=False, csys="Global", include_intersections=True,
                    point=True, line=False, area=False, solid=False, link=False,
                )
            if ok:
                new_areas = self._divide_area_by_selection("COL_FLANGE_TOP")
                self._subdivide_areas(new_areas, 1, 2)

            # Bottom flange
            SapModel.SelectObj.ClearSelection()
            ok, _ = self._coordinate_range(
                -B / 2, B / 2, -H / 2, -H / 2, z_target, z_target,
                deselect=False, csys="Global", include_intersections=True,
                point=True, line=False, area=False, solid=False, link=False,
            )
            if chair_prop and config.anchor_chair_height:
                self._coordinate_range(
                    -B / 2, B / 2, -H / 2, -H / 2,
                    config.anchor_chair_height, config.anchor_chair_height,
                    deselect=False, csys="Global", include_intersections=True,
                    point=True, line=False, area=False, solid=False, link=False,
                )
            if ok:
                new_areas = self._divide_area_by_selection("COL_FLANGE_BOTTOM")
                self._subdivide_areas(new_areas, 1, 2)

            # Link area at top flange line
            SapModel.SelectObj.ClearSelection()
            x_limit = A * config.n_pernos / 2.0
            ok, _ = self._coordinate_range(
                -x_limit, x_limit, H / 2, H / 2, z_target, z_target,
                deselect=False, csys="Global", include_intersections=True,
                point=True, line=False, area=False, solid=False, link=False,
            )
            if ok:
                new_areas = self._divide_area_by_selection("A_outer_link")
                self._subdivide_areas(new_areas, 1, 2)

            # Chair link
            if chair_prop and config.anchor_chair_height:
                SapModel.SelectObj.ClearSelection()
                z_ch = config.anchor_chair_height
                ok, _ = self._coordinate_range(
                    -x_limit, x_limit, H / 2, H / 2, z_ch, z_ch,
                    deselect=False, csys="Global", include_intersections=True,
                    point=True, line=False, area=False, solid=False, link=False,
                )
                if ok:
                    new_areas = self._divide_area_by_selection("A_chair_link")
                    self._subdivide_areas(new_areas, 1, 2)

            # Web
            SapModel.SelectObj.ClearSelection()
            ok, _ = self._coordinate_range(
                0.0, 0.0, -H / 2, H / 2, z_target, z_target,
                deselect=False, csys="Global", include_intersections=True,
                point=True, line=False, area=False, solid=False, link=False,
            )
            if chair_prop and config.anchor_chair_height:
                self._coordinate_range(
                    0.0, 0.0, -H / 2, H / 2,
                    config.anchor_chair_height, config.anchor_chair_height,
                    deselect=False, csys="Global", include_intersections=True,
                    point=True, line=False, area=False, solid=False, link=False,
                )
            if ok:
                new_areas = self._divide_area_by_selection("COL_WEB")
                self._subdivide_areas(new_areas, 1, 2)

        except Exception:
            pass

        self._log("Task 5: Mesh refinement completado.")
        result["task_5_mesh"] = True

        # ── Task 6: TC Limits (compresión=0 en pernos) ──────────────────
        tc_ok = 0
        for name in bolt_frame_names:
            try:
                ret = SapModel.FrameObj.SetTCLimits(str(name), True, 0.0, False, 0.0, 0)
                if _check_ret(ret):
                    tc_ok += 1
            except Exception:
                pass
        result["task_6_tc_limits"] = tc_ok

        # ── Task 7: Módulo de balasto ────────────────────────────────────
        if config.ks_balasto and config.ks_balasto > 0:
            current_units = SapModel.GetPresentUnits()
            SapModel.SetPresentUnits(14)  # kgf_cm_C
            try:
                SapModel.SelectObj.ClearSelection()
                ok, _ = self._coordinate_range(
                    -1e10, 1e10, -1e10, 1e10, 0.0, 0.0,
                    deselect=False, csys="Global", include_intersections=False,
                    point=False, line=False, area=True, solid=False, link=False,
                )
                if ok:
                    vec = [0.0, 0.0, 0.0]
                    ret = SapModel.AreaObj.SetSpring(
                        "ALL", 1, float(config.ks_balasto), 2, "", -1, 2, 1,
                        True, vec, 0.0, True, "Local", 2,
                    )
                    result["task_7_balasto"] = _check_ret(ret)
                else:
                    result["task_7_balasto"] = False
            finally:
                SapModel.SetPresentUnits(current_units)
        else:
            result["task_7_balasto"] = "skipped"

        # ── Task 8: Refresh ──────────────────────────────────────────────
        try:
            SapModel.View.RefreshView(0, False)
            SapModel.View.RefreshWindow()
        except Exception:
            pass

        result["success"] = True
        result["n_pernos"] = len(config.bolt_centers)
        result["bolt_frames_total"] = len(bolt_frame_names)
        result["include_anchor_chair"] = config.include_anchor_chair

        self._log("Proceso finalizado correctamente.")
        return result

    # ── Helpers internos de pernos ───────────────────────────────────────

    def _create_bolt_frame(self, center_name, cx, cy, cz, section, bolt_length, idx):
        z_bottom = cz - bolt_length
        bottom_pt = self._create_point(cx, cy, z_bottom, f"BOLT_BASE_{idx}")
        if not bottom_pt:
            return None, None
        try:
            ret = self.sap_model.FrameObj.AddByPoint(
                center_name, bottom_pt, "", section, f"BOLT_FRAME_{idx}"
            )
            if _check_ret(ret):
                return _get_name(ret, f"BOLT_FRAME_{idx}"), bottom_pt
        except Exception:
            pass
        return None, None

    def _create_chair_bolt_frame(self, chair_pt, plate_pt, section, idx):
        try:
            ret = self.sap_model.FrameObj.AddByPoint(
                chair_pt, plate_pt, "", section, f"BOLT_CHAIR_FRAME_{idx}"
            )
            if _check_ret(ret):
                return _get_name(ret, f"BOLT_CHAIR_FRAME_{idx}")
        except Exception:
            pass
        return None

    def _create_body_constraint(self, name, center_pt, circle_pts, dof_values):
        try:
            ret = self.sap_model.ConstraintDef.SetBody(name, dof_values, "Global")
            if not _check_ret(ret):
                return False
        except Exception:
            return False

        try:
            self.sap_model.PointObj.SetConstraint(center_pt, name)
        except Exception:
            return False

        for pt in circle_pts:
            if pt:
                try:
                    self.sap_model.PointObj.SetConstraint(pt, name)
                except Exception:
                    pass
        return True

    def _set_pin_restraint(self, point_name):
        try:
            value = [True, True, True, False, False, False]
            ret = self.sap_model.PointObj.SetRestraint(point_name, value)
            return _check_ret(ret)
        except Exception:
            return False

    def _create_single_chair(self, idx, cx, cy, z_level, circle_radius, inner_side, B_bolt, prop):
        chair_center = self._create_point(cx, cy, z_level, f"CHAIR_CENTER_{idx}")
        c_pts = self._create_circle_points(cx, cy, z_level, circle_radius, 16, f"CHAIR_c{idx}_")
        in_pts = self._create_square_points(cx, cy, z_level, inner_side, 16, f"CHAIR_sin{idx}_")
        out_pts = self._create_square_points(cx, cy, z_level, B_bolt, 16, f"CHAIR_sout{idx}_")
        self._create_ring_mesh(c_pts, in_pts, (cx, cy), f"CHAIR_ring_in{idx}", prop)
        self._create_ring_mesh(in_pts, out_pts, (cx, cy), f"CHAIR_ring_out{idx}", prop)
        return chair_center or f"CHAIR_CENTER_{idx}", c_pts, out_pts


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = PlacaBaseBackend(conn)
        config = PlacaBaseConfig()

        try:
            output = backend.run(config)
            import json
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
