"""
Backend — Fundaciones SAP2000 (COM Directo)
============================================
Crea y lee secciones de pedestal (Section Designer) y losa (Shell-Thick),
y modela una fundación individual completa en el modelo activo.

Adaptado de SAPy2000/Fundaciones para el esquema standalone de Skills_SAP.
"""

import comtypes.client
from dataclasses import dataclass, field
from typing import Optional


# ══════════════════════════════════════════════════════════════════════════════
# Conexión COM directa
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
                sap2000v1 = __import__("comtypes.gen.SAP2000v1", fromlist=["cHelper"])
                helper = helper.QueryInterface(sap2000v1.cHelper)
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
# Configuraciones (Dataclasses)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PedestalSectionConfig:
    """Parámetros para crear una sección de pedestal con Section Designer."""
    section_name: str = "PED_500x500"
    concrete_mat: str = ""
    rebar_mat: str = ""
    width: float = 500.0       # mm — dimensión Y global
    height: float = 500.0      # mm — dimensión X global
    corner_bar_size: str = "16mm"
    edge_bar_size: str = "12mm"
    edge_spacing: float = 150.0  # mm
    cover: float = 50.0          # mm


@dataclass
class LosaSectionConfig:
    """Parámetros para crear secciones Shell-Thick de losa de fundación."""
    base_name: str = "LOSA_300"
    concrete_mat: str = ""
    thickness: float = 300.0   # mm


@dataclass
class FundacionConfig:
    """Parámetros para modelar una fundación completa (pedestal + losa)."""
    # Secciones ya existentes en el modelo
    frame_section: str = ""       # Sección del pedestal (Frame)
    shell_zapata: str = ""        # Sección losa zapata (Shell)
    shell_pedestal: str = ""      # Sección losa bajo pedestal (Shell)
    # Geometría
    origen_x: float = 0.0        # mm
    origen_y: float = 0.0        # mm
    origen_z: float = 0.0        # mm
    altura_pedestal: float = 1000.0  # mm
    ancho_pedestal: float = 500.0    # mm — dimensión X global
    alto_pedestal: float = 500.0     # mm — dimensión Y global
    espesor_zapata: float = 300.0    # mm
    vuelo: float = 500.0             # mm sobresal del pedestal
    mesh_nx: int = 4
    mesh_ny: int = 4
    balasto: float = 5.0             # kgf/cm³


# ══════════════════════════════════════════════════════════════════════════════
# Helpers internos
# ══════════════════════════════════════════════════════════════════════════════

_CONCRETE = 2
_REBAR = 6
_UNITS_MM = 7   # eUnits.tonf_mm_C
_UNITS_MM2 = 11  # tonf_mm_C variante


def _check(ret) -> bool:
    """Devuelve True si el último elemento de ret (RetCode) es 0."""
    try:
        return ret[-1] == 0
    except (TypeError, IndexError):
        return ret == 0


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class FundacionesBackend:
    """Backend standalone de fundaciones para Skills_SAP."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Lectura del modelo ─────────────────────────────────────────────────

    def get_concrete_materials(self) -> list:
        """Retorna nombres de materiales de tipo Concrete del modelo."""
        try:
            ret = self.sap.PropMaterial.GetNameList()
            if not _check(ret):
                return []
            names = ret[1] if ret[0] > 0 else []
            result = []
            for name in names:
                ret_type = self.sap.PropMaterial.GetMaterial(name)
                if _check(ret_type) and ret_type[0] == _CONCRETE:
                    result.append(name)
            return result
        except Exception as e:
            print(f"get_concrete_materials error: {e}")
            return []

    def get_rebar_materials(self) -> list:
        """Retorna nombres de materiales de tipo Rebar del modelo."""
        try:
            ret = self.sap.PropMaterial.GetNameList()
            if not _check(ret):
                return []
            names = ret[1] if ret[0] > 0 else []
            result = []
            for name in names:
                ret_type = self.sap.PropMaterial.GetMaterial(name)
                if _check(ret_type) and ret_type[0] == _REBAR:
                    result.append(name)
            return result
        except Exception as e:
            print(f"get_rebar_materials error: {e}")
            return []

    def get_rebar_sizes(self) -> list:
        """Retorna los rebars definidos en el modelo (PropRebar)."""
        try:
            ret = self.sap.PropRebar.GetNameList()
            if not _check(ret):
                return []
            return list(ret[1]) if ret[0] > 0 else []
        except Exception as e:
            print(f"get_rebar_sizes error: {e}")
            return []

    def get_frame_sections(self) -> list:
        """Retorna todas las secciones Frame del modelo."""
        try:
            ret = self.sap.PropFrame.GetNameList()
            if not _check(ret):
                return []
            return list(ret[1]) if ret[0] > 0 else []
        except Exception as e:
            print(f"get_frame_sections error: {e}")
            return []

    def get_shell_sections(self) -> list:
        """Retorna todas las secciones Area/Shell del modelo."""
        try:
            ret = self.sap.PropArea.GetNameList()
            if not _check(ret):
                return []
            return list(ret[1]) if ret[0] > 0 else []
        except Exception as e:
            print(f"get_shell_sections error: {e}")
            return []

    def get_selected_point_coords(self) -> Optional[dict]:
        """
        Retorna coords (x, y, z) del primer punto seleccionado en SAP2000.
        Retorna None si no hay selección.
        """
        try:
            ret_sel = self.sap.SelectObj.GetSelected(0, [], [])
            if not _check(ret_sel) or ret_sel[0] == 0:
                return None
            obj_types = ret_sel[1]
            obj_names = ret_sel[2]
            point_name = None
            for i in range(ret_sel[0]):
                if int(obj_types[i]) == 1:
                    point_name = obj_names[i]
                    break
            if not point_name:
                return None
            ret_c = self.sap.PointObj.GetCoordCartesian(point_name, 0.0, 0.0, 0.0, "Global")
            if _check(ret_c):
                return {"name": point_name, "x": ret_c[0], "y": ret_c[1], "z": ret_c[2]}
        except Exception as e:
            print(f"get_selected_point_coords error: {e}")
        return None

    # ── Crear sección pedestal ─────────────────────────────────────────────

    def create_pedestal_section(self, cfg: PedestalSectionConfig) -> dict:
        """
        Crea una sección rectangular con refuerzo en Section Designer.

        Returns:
            dict: {"success": bool, "section_name": str, "error": str}
        """
        try:
            prev_units = self.sap.GetPresentUnits()
            self.sap.SetPresentUnits(_UNITS_MM2)

            # 1. Inicializar sección SD
            ret = self.sap.PropFrame.SetSDSection(cfg.section_name, cfg.concrete_mat)
            assert ret == 0, f"SetSDSection: {ret}"

            # 2. Rectángulo sólido con refuerzo
            shape_name = "ConcreteCore"
            ret = self.sap.PropFrame.SDShape.SetSolidRect(
                cfg.section_name, shape_name, cfg.concrete_mat, "Default",
                0, 0, cfg.height, cfg.width, 0, -1, True, cfg.rebar_mat
            )
            assert ret[-1] == 0, f"SetSolidRect: {ret[-1]}"

            # 3. Barras esquinas
            ret = self.sap.PropFrame.SDShape.SetReinfCorner(
                cfg.section_name, shape_name, 1, cfg.corner_bar_size, True
            )
            assert ret[-1] == 0, f"SetReinfCorner: {ret[-1]}"

            # 4. Barras bordes distribuidas
            ret = self.sap.PropFrame.SDShape.SetReinfEdge(
                cfg.section_name, shape_name, 1,
                cfg.edge_bar_size, cfg.edge_spacing, cfg.cover, True
            )
            assert ret[-1] == 0, f"SetReinfEdge: {ret[-1]}"

            self.sap.SetPresentUnits(prev_units)
            return {"success": True, "section_name": cfg.section_name}
        except Exception as e:
            try:
                self.sap.SetPresentUnits(prev_units)
            except Exception:
                pass
            return {"success": False, "section_name": cfg.section_name, "error": str(e)}

    # ── Crear sección losa ─────────────────────────────────────────────────

    def create_losa_sections(self, cfg: LosaSectionConfig) -> dict:
        """
        Crea dos secciones Shell-Thick: <base_name> y <base_name>PED.

        Returns:
            dict: {"success": bool, "sections": [str], "error": str}
        """
        # Colores BGR (igual que el original): gris claro / gris oscuro
        _COLOR_LIGHT = 200 + (200 << 8) + (200 << 16)   # RGB(200,200,200)
        _COLOR_DARK  = 128 + (128 << 8) + (128 << 16)   # RGB(128,128,128)

        sections_created = []
        try:
            prev_units = self.sap.GetPresentUnits()
            self.sap.SetPresentUnits(_UNITS_MM2)

            for suffix, color in [("", _COLOR_LIGHT), ("PED", _COLOR_DARK)]:
                name = cfg.base_name + suffix
                ret = self.sap.PropArea.SetShell_1(
                    name,             # Name
                    2,                # ShellType (Shell-Thick)
                    True,             # IncludeDrillingDOF
                    cfg.concrete_mat, # MatProp
                    0.0,              # MatAng
                    cfg.thickness,    # Thickness membrane
                    cfg.thickness,    # Thickness bending
                    color,            # Color
                    "",               # Notes
                    "",               # GUID
                )
                assert ret == 0, f"SetShell_1({name}): {ret}"
                sections_created.append(name)
                print(f"✓ Sección creada: {name}")

            self.sap.SetPresentUnits(prev_units)
            return {"success": True, "sections": sections_created}
        except Exception as e:
            try:
                self.sap.SetPresentUnits(prev_units)
            except Exception:
                pass
            return {"success": False, "sections": sections_created, "error": str(e)}

    # ── Modelar fundación completa ─────────────────────────────────────────

    def model_foundation(self, cfg: FundacionConfig) -> dict:
        """
        Modela una fundación completa replicando el comportamiento del original:
          1. Frame pedestal  — va desde oz (parte superior) hacia ABAJO hasta oz−h
          2. Link rígido     — conecta la base del frame con el centroide de la losa
          3. Malla interior  — nx×ny áreas bajo el pedestal  (shell_pedestal)
          4. Anillo perimetral — zapata con vuelo             (shell_zapata)
          5. Balasto          — resortes en cara inferior de todas las áreas

        El origen (origen_x, origen_y, origen_z) corresponde al nodo SUPERIOR
        del pedestal (mismo criterio que la GUI de SAPy2000).

        Returns:
            dict: {"success": bool, "frame": str, "link": str, "areas": [...],
                   "num_areas": int, "balasto_ok": int, "error": str}
        """
        try:
            prev_units = self.sap.GetPresentUnits()
            self.sap.SetPresentUnits(_UNITS_MM)

            ox, oy, oz = cfg.origen_x, cfg.origen_y, cfg.origen_z
            h   = cfg.altura_pedestal
            wx  = cfg.ancho_pedestal
            wy  = cfg.alto_pedestal
            esp = cfg.espesor_zapata
            v   = cfg.vuelo
            nx, ny = cfg.mesh_nx, cfg.mesh_ny

            # Coordenadas derivadas
            z_frame_base = oz - h              # nodo inferior del pedestal
            z_losa       = z_frame_base - esp / 2.0  # centroide de la losa = extremo del link

            # ── 1. Frame pedestal (top → base, hacia abajo) ──────────────────
            ret = self.sap.PointObj.AddCartesian(ox, oy, oz)
            assert ret[-1] == 0, f"AddCartesian top: {ret[-1]}"
            pt_top = ret[0]

            ret = self.sap.PointObj.AddCartesian(ox, oy, z_frame_base)
            assert ret[-1] == 0, f"AddCartesian base: {ret[-1]}"
            pt_base = ret[0]

            ret = self.sap.FrameObj.AddByPoint(pt_top, pt_base)
            assert ret[-1] == 0, f"AddByPoint: {ret[-1]}"
            frame_name = ret[0]

            ret = self.sap.FrameObj.SetSection(frame_name, cfg.frame_section)
            assert ret == 0, f"SetSection: {ret}"
            print(f"✓ Pedestal: {frame_name}  ({oz:.0f} → {z_frame_base:.0f} mm)")

            # ── 2. Propiedad de link rígido ──────────────────────────────────
            link_prop = "LIN_RIGIDO"
            self._create_rigid_link_property(link_prop)

            # ── 3. Link rígido (base del frame → centroide de la losa) ───────
            link_name = self._create_link_element(
                ox, oy, z_frame_base,
                ox, oy, z_losa,
                link_prop,
            )
            assert link_name, "Error al crear link rígido"
            print(f"✓ Link rígido: {link_name}  ({z_frame_base:.0f} → {z_losa:.0f} mm)")

            # ── 4. Malla interior (bajo pedestal) — shell_pedestal ───────────
            inner_areas = self._create_slab_mesh(
                ox, oy, z_losa, wx, wy, cfg.shell_pedestal, nx, ny
            )
            print(f"✓ Malla interior: {len(inner_areas)} elementos ({nx}×{ny})")

            # ── 5. Anillo perimetral (zapata) — shell_zapata ─────────────────
            outer_areas = self._create_perimeter_ring(
                ox, oy, z_losa, wx, wy, v, cfg.shell_zapata, nx, ny
            )
            print(f"✓ Anillo perimetral: {len(outer_areas)} elementos")

            # ── 6. Balasto en cara inferior ───────────────────────────────────
            all_areas = inner_areas + outer_areas
            ok_count = self._assign_balasto(all_areas, cfg.balasto)
            print(f"✓ Balasto: {ok_count}/{len(all_areas)} áreas")

            try:
                self.sap.View.RefreshView(0, False)
            except Exception:
                pass

            self.sap.SetPresentUnits(prev_units)
            return {
                "success": True,
                "frame": frame_name,
                "link": link_name,
                "areas": all_areas,
                "num_areas": len(all_areas),
                "balasto_ok": ok_count,
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            try:
                self.sap.SetPresentUnits(prev_units)
            except Exception:
                pass
            return {"success": False, "error": str(e)}

    # ── Helpers privados de modelado ───────────────────────────────────────

    def _create_rigid_link_property(self, prop_name: str = "LIN_RIGIDO") -> bool:
        """
        Crea (o sobreescribe) una propiedad de link tipo Linear con todos los
        DOF activos y fijos (rígido en todas las direcciones).
        Ignora el error si la propiedad ya existe.
        """
        dof   = [True]  * 6
        fixed = [True]  * 6
        ke    = [0.0]   * 6
        ce    = [0.0]   * 6
        try:
            ret = self.sap.PropLink.SetLinear(prop_name, dof, fixed, ke, ce, 0.0, 0)
            ok = ret == 0 if isinstance(ret, int) else ret[-1] == 0
            if ok:
                print(f"✓ Propiedad link rígido: {prop_name}")
            else:
                print(f"  ⚠️ SetLinear({prop_name}) retornó {ret} (puede que ya exista)")
            return ok
        except Exception as e:
            print(f"  ⚠️ _create_rigid_link_property: {e}")
            return False

    def _create_link_element(self, x1, y1, z1, x2, y2, z2, prop_name: str) -> Optional[str]:
        """
        Crea un elemento Link entre (x1,y1,z1) y (x2,y2,z2) y asigna prop_name.
        Retorna el nombre del link creado, o None si falla.
        """
        try:
            ret = self.sap.PointObj.AddCartesian(x1, y1, z1)
            assert ret[-1] == 0, f"AddCartesian pt1: {ret[-1]}"
            pt1 = ret[0]

            ret = self.sap.PointObj.AddCartesian(x2, y2, z2)
            assert ret[-1] == 0, f"AddCartesian pt2: {ret[-1]}"
            pt2 = ret[0]

            ret = self.sap.LinkObj.AddByPoint(pt1, pt2)
            assert ret[-1] == 0, f"AddByPoint link: {ret[-1]}"
            link_name = ret[0]

            ret = self.sap.LinkObj.SetProperty(link_name, prop_name)
            assert ret == 0, f"SetProperty link: {ret}"

            return link_name
        except Exception as e:
            print(f"  ⚠️ _create_link_element: {e}")
            return None

    def _create_slab_mesh(self, cx, cy, z, width, height, section, nx, ny) -> list:
        """Crea malla nx×ny de áreas rectangulares centrada en (cx, cy, z)."""
        start_x = cx - width / 2.0
        start_y = cy - height / 2.0
        dx = width / nx
        dy = height / ny
        zs4 = [z, z, z, z]
        areas = []
        for i in range(nx):
            for j in range(ny):
                x0 = start_x + i * dx
                y0 = start_y + j * dy
                ret = self.sap.AreaObj.AddByCoord(
                    4,
                    [x0, x0 + dx, x0 + dx, x0],
                    [y0, y0,      y0 + dy,  y0 + dy],
                    zs4, "", section, "", "Global",
                )
                if isinstance(ret, (list, tuple)) and ret[-1] == 0 and len(ret) >= 5:
                    areas.append(str(ret[3]))
                else:
                    code = ret[-1] if isinstance(ret, (list, tuple)) else ret
                    print(f"  ⚠️ Error área malla ({i},{j}): {code}")
        return areas

    def _create_perimeter_ring(self, cx, cy, z, inner_w, inner_h,
                                vuelo, section, nx, ny) -> list:
        """
        Crea el anillo perimetral de la zapata alrededor de la malla interior.

        Genera cada sub-celda directamente con AddByCoord (sin EditArea.Divide)
        para que todos los nombres queden registrados y el balasto se pueda
        asignar a cada área individualmente:
          - Franja Sur  : nx celdas (xl→xr dividido en nx, 1 fila de vuelo)
          - Franja Norte: nx celdas
          - Franja Oeste: ny celdas (1 columna de vuelo, yb→yt dividido en ny)
          - Franja Este : ny celdas
          - 4 Esquinas  : 1 celda cada una (vuelo×vuelo)
        """
        xl  = cx - inner_w / 2.0;  xr  = cx + inner_w / 2.0
        yb  = cy - inner_h / 2.0;  yt  = cy + inner_h / 2.0
        xl_o = xl - vuelo;          xr_o = xr + vuelo
        yb_o = yb - vuelo;          yt_o = yt + vuelo
        zs4 = [z, z, z, z]
        areas = []

        def _add(xs, ys, label):
            ret = self.sap.AreaObj.AddByCoord(
                4, xs, ys, zs4, "", section, "", "Global"
            )
            if isinstance(ret, (list, tuple)) and ret[-1] == 0 and len(ret) >= 5:
                name = str(ret[3])
                areas.append(name)
                return name
            code = ret[-1] if isinstance(ret, (list, tuple)) else ret
            print(f"  ⚠️ Error área {label}: {code}")
            return None

        dx_inner = inner_w / nx
        dy_inner = inner_h / ny

        # Franja Sur (nx celdas)
        for i in range(nx):
            x0 = xl + i * dx_inner;  x1 = x0 + dx_inner
            _add([x0, x1, x1, x0], [yb_o, yb_o, yb,  yb ], f"Sur_{i}")

        # Franja Norte (nx celdas)
        for i in range(nx):
            x0 = xl + i * dx_inner;  x1 = x0 + dx_inner
            _add([x0, x1, x1, x0], [yt,   yt,  yt_o, yt_o], f"Norte_{i}")

        # Franja Oeste (ny celdas)
        for j in range(ny):
            y0 = yb + j * dy_inner;  y1 = y0 + dy_inner
            _add([xl_o, xl,  xl,  xl_o], [y0, y0, y1, y1], f"Oeste_{j}")

        # Franja Este (ny celdas)
        for j in range(ny):
            y0 = yb + j * dy_inner;  y1 = y0 + dy_inner
            _add([xr,  xr_o, xr_o, xr ], [y0, y0, y1, y1], f"Este_{j}")

        # Esquinas (sin subdividir)
        _add([xl_o, xl,  xl,  xl_o], [yb_o, yb_o, yb,  yb ], "SW")
        _add([xr,  xr_o, xr_o, xr ], [yb_o, yb_o, yb,  yb ], "SE")
        _add([xl_o, xl,  xl,  xl_o], [yt,   yt,  yt_o, yt_o], "NW")
        _add([xr,  xr_o, xr_o, xr ], [yt,   yt,  yt_o, yt_o], "NE")

        return areas

    def _assign_balasto(self, area_names: list, ks: float) -> int:
        """
        Asigna módulo de balasto ks [kgf/cm³] como resorte de área
        en cara inferior (compresión) de cada shell.
        Cambia temporalmente las unidades a kgf_cm_C para la asignación.
        """
        prev_units = self.sap.GetPresentUnits()
        self.sap.SetPresentUnits(14)  # kgf_cm_C
        vec = [0.0, 0.0, 0.0]
        ok = 0
        for name in area_names:
            try:
                ret = self.sap.AreaObj.SetSpring(
                    str(name),   # Name
                    1,           # MyType: simple spring
                    float(ks),   # s: stiffness per unit area [kgf/cm³]
                    2,           # SimpleSpringType: compression only
                    "",          # LinkProp
                    -1,          # Face: bottom face
                    2,           # SpringLocalOneType: normal to face
                    1,           # Dir
                    True,        # Outward
                    vec,         # Vec
                    0.0,         # Ang
                    True,        # Replace
                    "Local",     # CSys
                    0,           # ItemType: Object
                )
                if (isinstance(ret, (list, tuple)) and ret[-1] == 0) or ret == 0:
                    ok += 1
            except Exception as exc:
                print(f"  [balasto] excepción en '{name}': {exc}")
        self.sap.SetPresentUnits(prev_units)
        return ok


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json

    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = FundacionesBackend(conn)
        print("Materiales hormigón:", backend.get_concrete_materials())
        print("Materiales acero:", backend.get_rebar_materials())
        print("Secciones Frame:", backend.get_frame_sections())
        print("Secciones Shell:", backend.get_shell_sections())
        conn.disconnect()
    else:
        print(f"No se pudo conectar: {res.get('error')}")
