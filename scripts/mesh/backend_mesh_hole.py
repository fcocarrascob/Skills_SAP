"""
Backend — SAP2000 Malla con Orificio (Standalone)
==================================================
Genera una malla de áreas con orificio central (o transición de formas)
interpolando puntos entre un anillo interno y uno externo. Soporta formas
"Círculo" y "Cuadrado" para cada anillo, en cualquier plano cartesiano.

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: backend_ring_areas.py / backend_template.py
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


def _shape_coords_2d(
    shape_type: str,
    center_u: float,
    center_v: float,
    dim: float,
    num_points: int,
) -> List[Tuple[float, float]]:
    """Genera coordenadas 2D (u, v) distribuidas sobre la forma indicada.

    Args:
        shape_type: "circulo" o "cuadrado" (case-insensitive).
        center_u, center_v: Centro en espacio local 2D.
        dim: Diámetro si es círculo, Lado si es cuadrado.
        num_points: Número de puntos a generar.

    Returns:
        Lista de tuplas (u, v).
    """
    coords: List[Tuple[float, float]] = []
    radius = dim / 2.0
    shape = shape_type.lower().replace("í", "i").replace("ó", "o")  # normalizar

    if "circulo" in shape or "circle" in shape:
        for i in range(num_points):
            angle = -2.0 * math.pi * i / num_points
            u = center_u + radius * math.cos(angle)
            v = center_v + radius * math.sin(angle)
            coords.append((u, v))

    else:  # cuadrado
        perimeter = 4.0 * dim
        step = perimeter / float(num_points) if num_points > 0 else 0.0

        for i in range(num_points):
            dist = i * step

            if dist < radius:                          # Fase 1: borde derecho, bajando
                u_local = radius
                v_local = -dist
            elif dist < radius + dim:                  # Fase 2: borde inferior, izq.
                u_local = radius - (dist - radius)
                v_local = -radius
            elif dist < radius + 2.0 * dim:            # Fase 3: borde izquierdo, subiendo
                u_local = -radius
                v_local = -radius + (dist - radius - dim)
            elif dist < radius + 3.0 * dim:            # Fase 4: borde superior, der.
                u_local = -radius + (dist - radius - 2.0 * dim)
                v_local = radius
            else:                                      # Fase 5: borde derecho, bajando
                u_local = radius
                v_local = radius - (dist - radius - 3.0 * dim)

            coords.append((center_u + u_local, center_v + v_local))

    return coords


def _local_to_global(
    u: float, v: float,
    origin_x: float, origin_y: float, origin_z: float,
    plane: str,
) -> Tuple[float, float, float]:
    """Convierte coordenadas locales 2D a Global 3D según el plano."""
    if plane == "XY":
        return origin_x + u, origin_y + v, origin_z
    if plane == "XZ":
        return origin_x + u, origin_y, origin_z + v
    # YZ
    return origin_x, origin_y + u, origin_z + v


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class HoleMeshConfig:
    """Parámetros de entrada para la malla con orificio."""

    # Forma y dimensión externa ("Círculo" o "Cuadrado")
    outer_shape: str = "Cuadrado"
    outer_dim: float = 500.0   # Lado o diámetro externo

    # Forma y dimensión interna (orificio)
    inner_shape: str = "Círculo"
    inner_dim: float = 200.0   # Lado o diámetro del orificio

    # Discretización
    num_angular: int = 16      # Puntos por anillo (divisiones angulares)
    num_radial: int = 3        # Anillos de áreas (divisiones radiales)

    # Origen (esquina inferior-izquierda del bounding box externo)
    origin_x: float = 0.0
    origin_y: float = 0.0
    origin_z: float = 0.0

    # Plano y propiedad de área
    plane: str = "XY"          # "XY", "XZ", "YZ"
    prop_name: str = "Default"


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class HoleMeshBackend:
    """Backend standalone para generar mallas con orificio en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Helpers de API ───────────────────────────────────────────────────

    def _create_point(self, x: float, y: float, z: float) -> Optional[str]:
        """Crea un punto en SAP2000 y retorna su nombre asignado."""
        try:
            # PointObj.AddCartesian(x, y, z, Name, UserName, CSys)
            ret = self.sap_model.PointObj.AddCartesian(x, y, z, "", "", "Global")
            if _check_ret(ret) and isinstance(ret, (list, tuple)) and len(ret) > 1:
                return str(ret[0])
        except Exception as exc:
            raise RuntimeError(f"PointObj.AddCartesian falló en ({x:.3f},{y:.3f},{z:.3f}): {exc}")
        return None

    def _create_area_by_points(
        self, point_names: List[str], prop_name: str
    ) -> Optional[str]:
        """Crea un área conectando cuatro puntos por nombre."""
        try:
            # AreaObj.AddByPoint(NumberPoints, PointNames, Name, PropName, UserName)
            ret = self.sap_model.AreaObj.AddByPoint(
                len(point_names), point_names, "", prop_name, ""
            )
            if _check_ret(ret) and isinstance(ret, (list, tuple)) and len(ret) > 1:
                return str(ret[0])
        except Exception as exc:
            raise RuntimeError(f"AreaObj.AddByPoint falló con puntos {point_names}: {exc}")
        return None

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: HoleMeshConfig) -> dict:
        """Genera la malla con orificio en el modelo activo de SAP2000.

        No inicializa un modelo nuevo; opera sobre el modelo abierto.

        Args:
            config: Parámetros de la malla.

        Returns:
            dict con resultados: success, num_areas, num_points, error.
        """
        # ── Validar parámetros ───────────────────────────────────────────
        if config.outer_dim <= 0 or config.inner_dim <= 0:
            raise ValueError("outer_dim e inner_dim deben ser > 0.")
        if config.inner_dim >= config.outer_dim:
            raise ValueError("inner_dim debe ser menor que outer_dim.")
        if config.num_angular < 3:
            raise ValueError("num_angular debe ser >= 3.")
        if config.num_radial < 1:
            raise ValueError("num_radial debe ser >= 1.")
        if config.plane.upper() not in ("XY", "XZ", "YZ"):
            raise ValueError(f"plane '{config.plane}' no válido. Use XY, XZ o YZ.")

        plane = config.plane.upper()

        # ── Task 1: Calcular centro local ────────────────────────────────
        center_u = config.outer_dim / 2.0
        center_v = config.outer_dim / 2.0

        # Crear punto en el centro (opcional, asegura nodo de referencia)
        cx, cy, cz = _local_to_global(
            center_u, center_v,
            config.origin_x, config.origin_y, config.origin_z,
            plane,
        )
        self._create_point(cx, cy, cz)

        # ── Task 2: Generar coordenadas 2D de los anillos interno y externo
        inner_coords = _shape_coords_2d(
            config.inner_shape, center_u, center_v,
            config.inner_dim, config.num_angular,
        )
        outer_coords = _shape_coords_2d(
            config.outer_shape, center_u, center_v,
            config.outer_dim, config.num_angular,
        )

        # ── Task 3: Crear puntos en SAP2000 para todos los anillos ───────
        # all_rings[r][i] = nombre del punto SAP2000
        # r=0 → anillo interno, r=num_radial → anillo externo
        all_rings: List[List[str]] = []
        created_points = 0

        for r in range(config.num_radial + 1):
            fraction = r / float(config.num_radial) if config.num_radial > 0 else 1.0
            ring: List[str] = []

            for i in range(config.num_angular):
                u_in, v_in = inner_coords[i]
                u_out, v_out = outer_coords[i]

                u = u_in + (u_out - u_in) * fraction
                v = v_in + (v_out - v_in) * fraction

                gx, gy, gz = _local_to_global(
                    u, v,
                    config.origin_x, config.origin_y, config.origin_z,
                    plane,
                )
                p_name = self._create_point(gx, gy, gz)
                ring.append(p_name or "")
                if p_name:
                    created_points += 1

            all_rings.append(ring)

        # ── Task 4: Crear áreas conectando anillos adyacentes ────────────
        created_areas: List[str] = []

        for r in range(config.num_radial):
            inner_ring = all_rings[r]
            outer_ring = all_rings[r + 1]

            for i in range(config.num_angular):
                p1 = inner_ring[i]
                p2 = inner_ring[(i + 1) % config.num_angular]
                p3 = outer_ring[(i + 1) % config.num_angular]
                p4 = outer_ring[i]

                if not all([p1, p2, p3, p4]):
                    continue

                a_name = self._create_area_by_points([p1, p2, p3, p4], config.prop_name)
                if a_name:
                    created_areas.append(a_name)

        # ── Task 5: Refrescar vista ──────────────────────────────────────
        try:
            self.sap_model.View.RefreshView(0, False)
        except Exception:
            pass

        return {
            "success": True,
            "num_areas": len(created_areas),
            "num_points": created_points,
            "area_names": created_areas,
            "plane": plane,
            "radial_rings": config.num_radial,
            "angular_divisions": config.num_angular,
        }


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = HoleMeshBackend(conn)
        config = HoleMeshConfig(
            outer_shape="Cuadrado", outer_dim=500.0,
            inner_shape="Círculo",  inner_dim=200.0,
            num_angular=16, num_radial=3,
            origin_x=0.0, origin_y=0.0, origin_z=0.0,
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
