"""
Backend — SAP2000 Perfiles de Acero como Placas Shell
=====================================================
Modela perfiles de acero estándar (W, HSS, L, C) como conjuntos de elementos
Area (Shell) que representan alas, almas y paredes del perfil.

Soporta orientación arbitraria: plano de extensión + ángulo de inclinación.

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: backend_bolt_plates.py
"""

import math
import comtypes.client
from dataclasses import dataclass
from typing import List, Tuple

from backend_bolt_plates import SapConnection


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _check_ret(ret) -> bool:
    if isinstance(ret, (list, tuple)):
        return int(ret[-1]) == 0
    return int(ret) == 0


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class SteelProfileConfig:
    """Parámetros de entrada para modelar un perfil como placas Shell."""

    # Tipo de perfil
    profile_type: str = "W"           # "W", "HSS", "L", "C"

    # Dimensiones de sección — W / C  (todas en mm)
    d: float = 300.0                  # Peralte total (mm)
    bf: float = 150.0                 # Ancho de ala (mm)
    tf: float = 10.0                  # Espesor de ala (mm)
    tw: float = 7.0                   # Espesor de alma (mm)

    # Dimensiones de sección — HSS  (mm)
    B: float = 200.0                  # Ancho HSS (mm)
    H: float = 200.0                  # Alto HSS (mm)
    t_hss: float = 8.0               # Espesor HSS (mm)

    # Dimensiones de sección — L  (mm)
    b1: float = 100.0                 # Ala vertical (mm)
    b2: float = 100.0                 # Ala horizontal (mm)
    t_angle: float = 10.0            # Espesor ángulo (mm)

    # Longitud del perfil
    length: float = 3000.0            # Largo del perfil (mm)

    # Ubicación punto base (inicio del perfil, en mm)
    origin_x: float = 0.0
    origin_y: float = 0.0
    origin_z: float = 0.0

    # Orientación
    plane: str = "XZ"                 # Plano donde se extiende el largo: "XZ", "YZ", "XY"
    angle: float = 0.0                # Inclinación en grados dentro del plano (0=horizontal)

    # Discretización
    n_length: int = 6                 # Divisiones a lo largo del perfil
    n_width: int = 2                  # Divisiones a lo ancho de cada placa

    # Propiedad SAP2000
    area_prop: str = "Default"        # Nombre de propiedad Shell existente

    # Grupo
    group_name: str = "STEEL_PROFILE" # Grupo para identificar las áreas creadas


# ══════════════════════════════════════════════════════════════════════════════
# Definición de placas para cada tipo de perfil
# ══════════════════════════════════════════════════════════════════════════════
# Cada placa se define como:
#   (nombre, offset_d, offset_w, placa_alto_d, placa_ancho_w)
#
# Sistema local de sección transversal:
#   d_axis: eje de peralte (vertical en sección)
#   w_axis: eje de ancho (horizontal en sección, fuera del plano del perfil)
#
# Origen de sección: centroide geométrico (para W, HSS, C)
#                    esquina interior (para L)

PlateSpec = Tuple[str, float, float, float, float]


def _plates_W(cfg: SteelProfileConfig) -> List[PlateSpec]:
    """W (Wide Flange): Ala superior + Alma + Ala inferior."""
    d, bf, tf = cfg.d, cfg.bf, cfg.tf
    # hw centroide-a-centroide: el alma llega hasta el plano medio de cada ala,
    # garantizando nodos coincidentes entre alma y alas para n_width par.
    hw = d - tf
    return [
        # (nombre, centro_d, centro_w, alto_d, ancho_w)
        ("TOP_FLANGE",    d / 2 - tf / 2,   0.0,  tf,  bf),
        ("WEB",           0.0,               0.0,  hw,  cfg.tw),
        ("BOT_FLANGE",   -d / 2 + tf / 2,   0.0,  tf,  bf),
    ]


def _plates_HSS(cfg: SteelProfileConfig) -> List[PlateSpec]:
    """HSS (Rectangular Tube): 4 paredes."""
    B, H, t = cfg.B, cfg.H, cfg.t_hss
    # Dimensiones centroide-a-centroide: paredes horizontales se acortan para
    # terminar justo en el plano medio de las paredes verticales y viceversa.
    # Esquinas: (v=±(H/2-t/2), w=±(B/2-t/2)) son compartidas por ambas paredes.
    hw = H - t   # altura pared vertical (de centroide inf a centroide sup)
    bw = B - t   # ancho pared horizontal (de centroide izq a centroide der)
    return [
        ("TOP_WALL",     H / 2 - t / 2,   0.0,           t,   bw),
        ("BOT_WALL",    -H / 2 + t / 2,   0.0,           t,   bw),
        ("LEFT_WALL",    0.0,             -B / 2 + t / 2, hw,  t),
        ("RIGHT_WALL",   0.0,              B / 2 - t / 2, hw,  t),
    ]


def _plates_L(cfg: SteelProfileConfig) -> List[PlateSpec]:
    """L (Ángulo): Ala vertical + Ala horizontal."""
    b1, b2, t = cfg.b1, cfg.b2, cfg.t_angle
    # Método centroide-a-centroide: cada ala empieza en el plano medio de la otra.
    # Nodo compartido en esquina interior: (v=t/2, w=t/2).
    vert_h  = b1 - t / 2             # ala vertical:   v ∈ [t/2, b1]
    vert_cd = t / 2 + vert_h / 2     # centroide en d
    horiz_w  = b2 - t / 2            # ala horizontal: w ∈ [t/2, b2]
    horiz_cw = t / 2 + horiz_w / 2   # centroide en w
    return [
        ("VERT_LEG",   vert_cd,   t / 2,     vert_h,  t),
        ("HORIZ_LEG",  t / 2,     horiz_cw,  t,       horiz_w),
    ]


def _plates_C(cfg: SteelProfileConfig) -> List[PlateSpec]:
    """C (Canal): Alma + Ala superior + Ala inferior."""
    d, bf, tf, tw = cfg.d, cfg.bf, cfg.tf, cfg.tw
    # hw centroide-a-centroide: alma entre planos medios de alas.
    hw = d - tf
    # Alas: se extienden desde el plano medio del alma hasta el extremo del ala.
    # Garantiza nodo compartido en (v=±(d/2-tf/2), w=-bf/2+tw/2).
    w_web      = -bf / 2 + tw / 2          # centroide del alma en w
    flange_w   = bf - tw / 2               # ancho de ala (de centroide alma a extremo)
    flange_cw  = w_web + flange_w / 2      # centroide de ala en w
    return [
        ("WEB",          0.0,              w_web,      hw,  tw),
        ("TOP_FLANGE",   d / 2 - tf / 2,  flange_cw,  tf,  flange_w),
        ("BOT_FLANGE",  -d / 2 + tf / 2,  flange_cw,  tf,  flange_w),
    ]


PROFILE_GENERATORS = {
    "W": _plates_W,
    "HSS": _plates_HSS,
    "L": _plates_L,
    "C": _plates_C,
}


# ══════════════════════════════════════════════════════════════════════════════
# Sistema de coordenadas con orientación arbitraria
# ══════════════════════════════════════════════════════════════════════════════

def _build_axes(plane: str, angle_deg: float):
    """Construye los 3 ejes unitarios del perfil.

    Returns:
        (e_L, e_d, e_w) — vectores unitarios (tuple de 3 floats cada uno)
        e_L: dirección longitudinal (largo del perfil)
        e_d: dirección peralte (vertical de sección)
        e_w: dirección ancho (fuera del plano del perfil)
    """
    theta = math.radians(angle_deg)
    c, s = math.cos(theta), math.sin(theta)

    if plane == "XZ":
        # Largo en plano XZ, ancho sale por Y
        e_L = (c, 0.0, s)
        e_d = (-s, 0.0, c)
        e_w = (0.0, 1.0, 0.0)
    elif plane == "YZ":
        # Largo en plano YZ, ancho sale por X
        e_L = (0.0, c, s)
        e_d = (0.0, -s, c)
        e_w = (1.0, 0.0, 0.0)
    else:  # XY
        # Largo en plano XY, ancho sale por Z
        e_L = (c, s, 0.0)
        e_d = (-s, c, 0.0)
        e_w = (0.0, 0.0, 1.0)

    return e_L, e_d, e_w


def _local_to_global(
    origin: Tuple[float, float, float],
    e_L: Tuple[float, float, float],
    e_d: Tuple[float, float, float],
    e_w: Tuple[float, float, float],
    u: float,   # coordenada a lo largo del largo
    v: float,   # coordenada en dirección del peralte
    w: float,   # coordenada en dirección del ancho
) -> Tuple[float, float, float]:
    """P_global = origin + u·e_L + v·e_d + w·e_w"""
    return (
        origin[0] + u * e_L[0] + v * e_d[0] + w * e_w[0],
        origin[1] + u * e_L[1] + v * e_d[1] + w * e_w[1],
        origin[2] + u * e_L[2] + v * e_d[2] + w * e_w[2],
    )


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class SteelProfileBackend:
    """Backend standalone para modelar perfiles de acero como placas Shell."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config: SteelProfileConfig) -> dict:
        SapModel = self.sap_model
        result = {
            "success": False,
            "profile_type": config.profile_type,
            "num_areas": 0,
            "num_plates": 0,
            "plate_names": [],
        }

        # ── Task 0: Establecer unidades kN-mm ─────────────────────────────
        ret = SapModel.SetPresentUnits(5)  # 5 = kN_mm_C
        assert _check_ret(ret), f"SetPresentUnits failed: {ret}"

        # ── Task 1: Validar tipo de perfil ──────────────────────────────
        ptype = config.profile_type.upper()
        gen_func = PROFILE_GENERATORS.get(ptype)
        if gen_func is None:
            raise ValueError(f"Tipo de perfil no soportado: {ptype}")

        plates = gen_func(config)
        result["num_plates"] = len(plates)

        # ── Task 2: Construir ejes locales ──────────────────────────────
        e_L, e_d, e_w = _build_axes(config.plane, config.angle)
        origin = (config.origin_x, config.origin_y, config.origin_z)

        # ── Task 3: Crear grupo ─────────────────────────────────────────
        ret = SapModel.GroupDef.SetGroup(config.group_name)
        assert _check_ret(ret), f"GroupDef.SetGroup failed: {ret}"

        # ── Task 4: Generar placas ──────────────────────────────────────
        dl = config.length / config.n_length  # paso longitudinal
        total_areas = 0
        area_names = []

        for plate_name, cd, cw, plate_h, plate_w in plates:
            # Divisiones en ancho de esta placa
            dw = plate_w / config.n_width

            # Si el alto de la placa es significativo y ancho es muy pequeño
            # (alma), las subdivisiones van en dirección del peralte (v).
            # Si es ala (ancho >> alto), las subdivisiones van en dirección w.
            # En cualquier caso, representamos la placa como un rectángulo en
            # el espacio (L × W_or_H):
            #   - Se extiende a lo largo: u ∈ [0, length]
            #   - Se extiende en su "ancho": la dimensión perpendicular al largo

            # Determinar la orientación de la placa en la sección transversal
            # La placa es un rectángulo plate_h × plate_w en el plano (d, w)
            # centrado en (cd, cw).
            # Discretizar en n_width divisiones de la dimensión mayor.
            # Para simplificar: siempre n_width divisiones en la dirección w,
            # y la placa tiene plate_h en dirección d (se toma como 1 celda
            # en d, a menos que sea alma donde conviene subdividir en d).

            # Estrategia: cada placa se modela como n_length × n_width celdas.
            # La placa se orienta según su geometría:
            #   - Si plate_w >= plate_h: placa "horizontal" → subdivisiones en w
            #   - Si plate_h > plate_w: placa "vertical" → subdivisiones en d(v)

            if plate_h > plate_w:
                # Placa vertical (alma): subdivisiones en dirección d
                dd_plate = plate_h / config.n_width
                for i in range(config.n_length):
                    u0 = i * dl
                    u1 = u0 + dl
                    for j in range(config.n_width):
                        v0 = cd - plate_h / 2 + j * dd_plate
                        v1 = v0 + dd_plate
                        w_val = cw

                        p00 = _local_to_global(origin, e_L, e_d, e_w, u0, v0, w_val)
                        p10 = _local_to_global(origin, e_L, e_d, e_w, u1, v0, w_val)
                        p11 = _local_to_global(origin, e_L, e_d, e_w, u1, v1, w_val)
                        p01 = _local_to_global(origin, e_L, e_d, e_w, u0, v1, w_val)

                        xs = [p00[0], p10[0], p11[0], p01[0]]
                        ys = [p00[1], p10[1], p11[1], p01[1]]
                        zs = [p00[2], p10[2], p11[2], p01[2]]

                        raw = SapModel.AreaObj.AddByCoord(
                            4, xs, ys, zs, "", config.area_prop, ""
                        )
                        if not _check_ret(raw):
                            raise RuntimeError(
                                f"AreaObj.AddByCoord failed (plate={plate_name}, "
                                f"i={i}, j={j}): {raw}"
                            )
                        a_name = str(raw[3])
                        area_names.append(a_name)
                        total_areas += 1

                        # Asignar al grupo
                        SapModel.AreaObj.SetGroupAssign(
                            a_name, config.group_name, False
                        )
            else:
                # Placa horizontal (ala): subdivisiones en dirección w
                dw_plate = plate_w / config.n_width
                for i in range(config.n_length):
                    u0 = i * dl
                    u1 = u0 + dl
                    for j in range(config.n_width):
                        w0 = cw - plate_w / 2 + j * dw_plate
                        w1 = w0 + dw_plate
                        v_val = cd

                        p00 = _local_to_global(origin, e_L, e_d, e_w, u0, v_val, w0)
                        p10 = _local_to_global(origin, e_L, e_d, e_w, u1, v_val, w0)
                        p11 = _local_to_global(origin, e_L, e_d, e_w, u1, v_val, w1)
                        p01 = _local_to_global(origin, e_L, e_d, e_w, u0, v_val, w1)

                        xs = [p00[0], p10[0], p11[0], p01[0]]
                        ys = [p00[1], p10[1], p11[1], p01[1]]
                        zs = [p00[2], p10[2], p11[2], p01[2]]

                        raw = SapModel.AreaObj.AddByCoord(
                            4, xs, ys, zs, "", config.area_prop, ""
                        )
                        if not _check_ret(raw):
                            raise RuntimeError(
                                f"AreaObj.AddByCoord failed (plate={plate_name}, "
                                f"i={i}, j={j}): {raw}"
                            )
                        a_name = str(raw[3])
                        area_names.append(a_name)
                        total_areas += 1

                        SapModel.AreaObj.SetGroupAssign(
                            a_name, config.group_name, False
                        )

            result["plate_names"].append(plate_name)

        # ── Task 5: Verificar creación ────────────────────────────────
        verified_count = SapModel.AreaObj.Count()
        if verified_count < total_areas:
            raise RuntimeError(
                f"Se esperaban al menos {total_areas} áreas, "
                f"SAP2000 reporta {verified_count}"
            )

        # ── Task 6: Refrescar vista ─────────────────────────────────────
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        result["success"] = True
        result["num_areas"] = total_areas
        result["verified_count"] = verified_count
        result["areas_per_plate"] = config.n_length * config.n_width
        result["angle"] = config.angle
        result["plane"] = config.plane
        result["length"] = config.length
        result["group"] = config.group_name
        return result


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")
    if not res.get("connected"):
        raise SystemExit("No se pudo conectar a SAP2000.")

    backend = SteelProfileBackend(conn)

    cfg = SteelProfileConfig(
        profile_type="W",
        d=300.0, bf=150.0, tf=10.0, tw=7.0,
        length=3000.0,
        origin_x=0.0, origin_y=0.0, origin_z=0.0,
        plane="XZ", angle=0.0,
        n_length=6, n_width=2,
        area_prop="Default",
        group_name="PROFILE_W_TEST",
    )

    result = backend.run(cfg)
    print(f"\nResultado: {result}")
    conn.disconnect()
