"""
Backend — SAP2000 Placas de Conexión + Links Gap (Conexión Pernada)
====================================================================
Genera dos placas anulares de conexión enfrentadas para cada perno,
separadas una distancia sep = (t1 + t2) / 2, conectadas nodo a nodo
mediante elementos Link con propiedad Gap (solo compresión).

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: backend_mesh_hole.py
"""

import math
import comtypes.client
from dataclasses import dataclass
from typing import List, Optional, Tuple


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
# Helpers de geometría
# (replicados aquí para mantener el módulo autónomo)
# ══════════════════════════════════════════════════════════════════════════════

def _check_ret(ret) -> bool:
    """Retorna True si el código de retorno de la API es 0 (éxito)."""
    if isinstance(ret, (list, tuple)):
        return int(ret[-1]) == 0
    return int(ret) == 0


def _shape_coords_2d(
    shape_type: str,
    center_u: float,
    center_v: float,
    dim: float,
    num_points: int,
) -> List[Tuple[float, float]]:
    """Genera coordenadas 2D (u, v) distribuidas sobre la forma indicada.

    Args:
        shape_type: "circulo" o "cuadrado" (case-insensitive, acepta tildes).
        center_u, center_v: Centro en espacio local 2D.
        dim: Diámetro si es círculo, Lado si es cuadrado.
        num_points: Número de puntos a generar.
    """
    coords: List[Tuple[float, float]] = []
    radius = dim / 2.0
    shape = shape_type.lower().replace("í", "i").replace("ó", "o")

    if "circulo" in shape or "circle" in shape:
        for i in range(num_points):
            angle = -2.0 * math.pi * i / num_points
            coords.append((center_u + radius * math.cos(angle),
                           center_v + radius * math.sin(angle)))
    else:  # cuadrado
        perimeter = 4.0 * dim
        step = perimeter / float(num_points) if num_points > 0 else 0.0
        for i in range(num_points):
            dist = i * step
            if dist < radius:
                u_l, v_l = radius, -dist
            elif dist < radius + dim:
                u_l, v_l = radius - (dist - radius), -radius
            elif dist < radius + 2.0 * dim:
                u_l, v_l = -radius, -radius + (dist - radius - dim)
            elif dist < radius + 3.0 * dim:
                u_l, v_l = -radius + (dist - radius - 2.0 * dim), radius
            else:
                u_l, v_l = radius, radius - (dist - radius - 3.0 * dim)
            coords.append((center_u + u_l, center_v + v_l))

    return coords


def _local_to_global(
    u: float, v: float,
    origin_x: float, origin_y: float, origin_z: float,
    plane: str,
    normal_offset: float = 0.0,
) -> Tuple[float, float, float]:
    """Convierte coordenadas locales 2D + offset normal a Global 3D.

    El offset normal se aplica en la dirección perpendicular al plano:
      XY → normal = Z,  XZ → normal = Y,  YZ → normal = X.
    """
    if plane == "XY":
        return origin_x + u, origin_y + v, origin_z + normal_offset
    if plane == "XZ":
        return origin_x + u, origin_y + normal_offset, origin_z + v
    # YZ
    return origin_x + normal_offset, origin_y + u, origin_z + v


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BoltPlatesConfig:
    """Parámetros de entrada para las placas de conexión con links gap."""

    # Espesores de las placas conectadas (mismas unidades que el modelo)
    plate_thickness_1: float = 16.0
    plate_thickness_2: float = 16.0

    # Geometría de la placa de conexión
    bolt_diameter: float = 22.0        # Diámetro del orificio (= diámetro perno)
    outer_dim: float = 80.0            # Dimensión exterior (lado o diámetro)
    outer_shape: str = "Círculo"       # "Círculo" o "Cuadrado"

    # Discretización
    num_angular: int = 12              # Puntos por anillo (>= 3)
    num_radial: int = 2                # Anillos radiales (>= 1)

    # Nodo de inserción: esquina inferior de la placa delantera (mín U, mín V y normal)
    start_x: float = 0.0
    start_y: float = 0.0
    start_z: float = 0.0

    # Plano de la placa
    plane: str = "XY"                  # "XY", "XZ", "YZ"

    # Propiedades SAP2000
    area_prop: str = "Default"
    gap_prop_name: str = "GAP_BOLT"
    gap_stiffness: float = 1.0e6       # Rigidez del gap (unidades del modelo)
    initial_gap: float = 0.0           # Apertura inicial del gap

    # Barra de perno
    bolt_material: str = "A36"         # Material para la sección Frame circular del perno
    bolt_section_name: str = ""        # Nombre de sección (auto: "BOLT_{dia}" si vacío)


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class BoltPlatesBackend:
    """Backend standalone para generar placas de conexión con links gap en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Helpers de API ───────────────────────────────────────────────────

    def _create_point(self, x: float, y: float, z: float) -> Optional[str]:
        """Crea un punto y retorna su nombre asignado."""
        try:
            ret = self.sap_model.PointObj.AddCartesian(x, y, z, "", "", "Global")
            if _check_ret(ret) and isinstance(ret, (list, tuple)) and len(ret) > 1:
                return str(ret[0])
        except Exception as exc:
            raise RuntimeError(
                f"PointObj.AddCartesian falló en ({x:.3f},{y:.3f},{z:.3f}): {exc}"
            )
        return None

    def _create_area(
        self, point_names: List[str], prop_name: str
    ) -> Optional[str]:
        """Crea un área cuadrilateral conectando cuatro puntos por nombre."""
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

    def _ensure_gap_prop(self, config: BoltPlatesConfig) -> None:
        """Crea la propiedad Link Gap en el modelo.

        Propiedad Gap (solo compresión) activa en DOF U1 (axial al link).
        Si el nombre ya existe, SAP2000 lo sobreescribe con los nuevos parámetros.

        API: SapModel.PropLink.SetGap(Name, DOF, Fixed, Ke, Ce, k, dis,
                                       NonLinear, iEta, jEta, Notes, GUID) → Long
        Nota: retorna un Long directo (no lista ByRef), pero se maneja
              con _check_ret por seguridad.
        """
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
                    f"PropLink.SetGap falló con código {rc}. "
                    "Verifique que el nombre de propiedad sea válido."
                )
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError(f"PropLink.SetGap excepción: {exc}")

    def _create_link(
        self, pt1: str, pt2: str, prop_name: str
    ) -> Optional[str]:
        """Crea un elemento Link de dos juntas entre pt1 y pt2.

        API: SapModel.LinkObj.AddByPoint(Point1, Point2, IsSingleJoint,
                                          Name, PropName, UserName, CSys)
             → [Name_assigned, ret_code]
        """
        try:
            # Firma: AddByPoint(Point1, Point2, Name[ByRef out]="", IsSingleJoint=False,
            #                   PropName, UserName)  →  [Name, ret_code]
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

    def _ensure_bolt_section(self, config: "BoltPlatesConfig") -> Optional[str]:
        """Crea sección Frame circular para la barra del perno."""
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
        """Crea un elemento Frame entre dos puntos."""
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
        """Retorna la cantidad de Body Constraints ya definidos en el modelo."""
        try:
            ret = self.sap_model.ConstraintDef.GetNameList(0, [])
            # ret = [count, [names...], ret_code]
            if isinstance(ret, (list, tuple)) and int(ret[-1]) == 0:
                return int(ret[0])
        except Exception:
            pass
        return 0

    def _create_body_constraint(
        self, name: str, center_pt: str, ring_pts: List[str]
    ) -> bool:
        """Crea Body Constraint con todos los GDL restringidos."""
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

    def run(self, config: BoltPlatesConfig) -> dict:
        """Genera las placas de conexión y los links gap en el modelo activo.

        No inicializa un modelo nuevo; opera sobre el modelo abierto.

        Args:
            config: Parámetros de las placas y del gap.

        Returns:
            dict: success, num_areas, num_points, num_links, separation, plane, gap_prop.
        """
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
        plane = config.plane.upper()
        if plane not in ("XY", "XZ", "YZ"):
            raise ValueError(f"Plano '{config.plane}' no válido. Use XY, XZ o YZ.")

        sep = (config.plate_thickness_1 + config.plate_thickness_2) / 2.0

        # ── Nodo de inserción → centro del perno ────────────────────────
        # La inserción es la esquina inferior (mín U, mín V) de la placa
        # delantera (offset normal = -sep/2). Se deriva el centro real del perno.
        half_outer = config.outer_dim / 2.0
        if plane == "XY":
            bolt_cx = config.start_x + half_outer
            bolt_cy = config.start_y + half_outer
            bolt_cz = config.start_z + sep / 2.0
        elif plane == "XZ":
            bolt_cx = config.start_x + half_outer
            bolt_cy = config.start_y + sep / 2.0
            bolt_cz = config.start_z + half_outer
        else:  # YZ
            bolt_cx = config.start_x + sep / 2.0
            bolt_cy = config.start_y + half_outer
            bolt_cz = config.start_z + half_outer

        # ── Fase 0: Sección Frame del perno ──────────────────────────────
        bolt_section = self._ensure_bolt_section(config)

        # ── Fase 1: Propiedad Link Gap ───────────────────────────────────
        self._ensure_gap_prop(config)

        # ── Fase 2: Coordenadas de los anillos en espacio local ──────────
        # El orificio interno es siempre circular (diámetro del perno).
        # La forma exterior es configurable.
        # Los anillos se generan centrados en (0,0) del espacio local;
        # el offset al centro del perno se aplica en _local_to_global.
        inner_coords = _shape_coords_2d(
            "Círculo", 0.0, 0.0, config.bolt_diameter, config.num_angular
        )
        outer_coords = _shape_coords_2d(
            config.outer_shape, 0.0, 0.0, config.outer_dim, config.num_angular
        )

        # ── Fases 3 y 4: Crear puntos para las dos placas ────────────────
        # Placa 1 → offset normal = -sep/2
        # Placa 2 → offset normal = +sep/2
        # all_rings_pN[r][i] = nombre del punto SAP2000
        # r=0 → anillo interno, r=num_radial → anillo externo

        all_rings_p1: List[List[str]] = []
        all_rings_p2: List[List[str]] = []
        created_points = 0

        for r in range(config.num_radial + 1):
            fraction = r / float(config.num_radial) if config.num_radial > 0 else 1.0
            ring_p1: List[str] = []
            ring_p2: List[str] = []

            for i in range(config.num_angular):
                u_in, v_in = inner_coords[i]
                u_out, v_out = outer_coords[i]
                u = u_in + (u_out - u_in) * fraction
                v = v_in + (v_out - v_in) * fraction

                # Placa 1 (offset negativo)
                gx, gy, gz = _local_to_global(
                    u, v,
                    bolt_cx, bolt_cy, bolt_cz,
                    plane, normal_offset=-sep / 2.0,
                )
                p1_name = self._create_point(gx, gy, gz)
                ring_p1.append(p1_name or "")
                if p1_name:
                    created_points += 1

                # Placa 2 (offset positivo)
                gx, gy, gz = _local_to_global(
                    u, v,
                    bolt_cx, bolt_cy, bolt_cz,
                    plane, normal_offset=+sep / 2.0,
                )
                p2_name = self._create_point(gx, gy, gz)
                ring_p2.append(p2_name or "")
                if p2_name:
                    created_points += 1

            all_rings_p1.append(ring_p1)
            all_rings_p2.append(ring_p2)

        # ── Centro de cada placa (nodo en el centro del orificio) ─────────
        gx_c1, gy_c1, gz_c1 = _local_to_global(
            0.0, 0.0,
            bolt_cx, bolt_cy, bolt_cz,
            plane, normal_offset=-sep / 2.0,
        )
        gx_c2, gy_c2, gz_c2 = _local_to_global(
            0.0, 0.0,
            bolt_cx, bolt_cy, bolt_cz,
            plane, normal_offset=+sep / 2.0,
        )
        center_p1 = self._create_point(gx_c1, gy_c1, gz_c1)
        center_p2 = self._create_point(gx_c2, gy_c2, gz_c2)
        if center_p1:
            created_points += 1
        if center_p2:
            created_points += 1

        # ── Fase 3 (cont.): Crear áreas de malla para cada placa ─────────
        created_areas: List[str] = []

        for r in range(config.num_radial):
            inner_p1 = all_rings_p1[r]
            outer_p1 = all_rings_p1[r + 1]
            inner_p2 = all_rings_p2[r]
            outer_p2 = all_rings_p2[r + 1]

            for i in range(config.num_angular):
                j = (i + 1) % config.num_angular

                # Placa 1
                pts = [inner_p1[i], inner_p1[j], outer_p1[j], outer_p1[i]]
                if all(pts):
                    a = self._create_area(pts, config.area_prop)
                    if a:
                        created_areas.append(a)

                # Placa 2
                pts = [inner_p2[i], inner_p2[j], outer_p2[j], outer_p2[i]]
                if all(pts):
                    a = self._create_area(pts, config.area_prop)
                    if a:
                        created_areas.append(a)

        # ── Fase 5: Crear links Gap nodo a nodo ──────────────────────────
        # Para cada posición (r, i): link entre plate1[r][i] y plate2[r][i].
        # Esto cubre todos los anillos, incluyendo interno y externo.
        created_links: List[str] = []

        for r in range(config.num_radial + 1):
            for i in range(config.num_angular):
                pt_p1 = all_rings_p1[r][i]
                pt_p2 = all_rings_p2[r][i]
                if pt_p1 and pt_p2:
                    lnk = self._create_link(pt_p1, pt_p2, config.gap_prop_name)
                    if lnk:
                        created_links.append(lnk)

        # ── Fase 6: Barra de perno (Frame circular entre centros de placas) ──
        bolt_bar_name = None
        if bolt_section and center_p1 and center_p2:
            bolt_bar_name = self._create_frame_bar(
                center_p1, center_p2, bolt_section, "BOLT_BAR"
            )

        # ── Fase 7: Body constraints (1 por placa) ───────────────────────────
        # Un único body por placa: nodo central + anillo interno (r=0).
        # Los nombres usan el contador de constraints existentes para ser únicos
        # cuando se generan múltiples placas en el mismo modelo.
        body_constraints_created = 0
        inner_p1_nodes = [pt for pt in all_rings_p1[0] if pt]
        inner_p2_nodes = [pt for pt in all_rings_p2[0] if pt]
        base_idx = self._existing_body_count() + 1
        name_p1 = f"BODY_P{base_idx}"
        name_p2 = f"BODY_P{base_idx + 1}"
        if center_p1:
            if self._create_body_constraint(name_p1, center_p1, inner_p1_nodes):
                body_constraints_created += 1
        if center_p2:
            if self._create_body_constraint(name_p2, center_p2, inner_p2_nodes):
                body_constraints_created += 1

        # ── Refresh ──────────────────────────────────────────────────────
        try:
            self.sap_model.View.RefreshView(0, False)
        except Exception:
            pass

        return {
            "success": True,
            "num_areas": len(created_areas),
            "num_points": created_points,
            "num_links": len(created_links),
            "separation": sep,
            "plane": plane,
            "gap_prop": config.gap_prop_name,
            "radial_rings": config.num_radial,
            "angular_divisions": config.num_angular,
            "bolt_section": bolt_section,
            "bolt_bar": bolt_bar_name,
            "body_constraints": body_constraints_created,
            "body_names": [name_p1, name_p2],
        }


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        import json
        backend = BoltPlatesBackend(conn)
        config = BoltPlatesConfig(
            plate_thickness_1=16.0,
            plate_thickness_2=16.0,
            bolt_diameter=22.0,
            outer_dim=80.0,
            outer_shape="Círculo",
            num_angular=12,
            num_radial=2,
            start_x=0.0,
            start_y=0.0,
            start_z=0.0,
            plane="XY",
            area_prop="Default",
            gap_prop_name="GAP_BOLT",
            gap_stiffness=1.0e6,
            initial_gap=0.0,
        )
        try:
            output = backend.run(config)
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
