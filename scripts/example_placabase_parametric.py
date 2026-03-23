# ─── SAP2000 Base Plate Generator — Parametric Script ────────────────
# Description: Generates a parametric base plate with anchor bolts,
#              anchor chair (optional), body constraints, and balasto spring.
#              Includes column flanges/web and automatic meshing.
#
# Features:
#   - Configurable bolt diameter, spacing, and count
#   - Optional anchor chair (silleta de anclaje)
#   - Body constraints connecting bolt centers to circular regions
#   - TC Limits on bolts (compression=0, tension-only)
#   - Balasto spring on base plate areas (z=0)
#   - Automatic mesh refinement at bolt/chair/column intersections
#
# Units: kgf_cm_C (14) for balasto, otherwise consistent with model units
# ─────────────────────────────────────────────────────────────────────

import math

# ═════════════════════════════════════════════════════════════════════
# ╔═══════════════════════════════════════════════════════════════════╗
# ║                    CONFIGURACION DE VARIABLES                      ║
# ╚═══════════════════════════════════════════════════════════════════╝
# ═════════════════════════════════════════════════════════════════════

# ── Dimensiones de Pernos ────────────────────────────────────────────
bolt_dia = 25.0           # Diámetro del perno [mm o unidades actuales]
bolt_material = "A36"     # Material de los pernos
n_pernos = 4              # Número de pernos (debe ser par, idealmente 4, 6, 8)

# ── Dimensiones de Columna ───────────────────────────────────────────
H_col = 300.0             # Altura de la sección de columna [mm]
B_col = 250.0             # Ancho de la sección de columna [mm]
z_col = 2.0 * H_col       # Longitud de columna a modelar (2×altura)

# ── Espesores de Placas ──────────────────────────────────────────────
plate_thickness = 20.0             # Espesor de placa base [mm]
flange_thickness = 15.0            # Espesor de alas de columna [mm]
web_thickness = 10.0               # Espesor de alma de columna [mm]

# ── Silla de Anclaje (Anchor Chair) ──────────────────────────────────
include_anchor_chair = False       # True para incluir silla de anclaje
anchor_chair_height = 50.0         # Altura de la silla [mm] (si está activada)
anchor_chair_thickness = 15.0      # Espesor de la silla [mm]

# ── Módulo de Balasto ─────────────────────────────────────────────────
ks_balasto = 5.0          # Módulo de balasto [kgf/cm³] (0 para omitir)

# ── Centros de Pernos (Auto-generados o Personalizados) ──────────────
# Si bolt_centers está vacío, se genera automáticamente según n_pernos
# Formato: lista de tuplas (x, y, z)
bolt_centers = []

# ── Mapeo Diámetro → Espaciamiento ───────────────────────────────────
# Fuente: Tabla de espaciamiento recomendado según diámetro
DIA_TO_SPACING = {
    16: (80, 80),    19: (100, 100),  22: (100, 100),  25: (100, 100),
    32: (125, 125),  38: (150, 150),  44: (175, 175),  51: (200, 200),
    57: (225, 225),  64: (250, 250),
}

def get_bolt_spacing(dia):
    """Retorna (A, B) según el diámetro del perno."""
    d = int(round(float(dia)))
    return DIA_TO_SPACING.get(d, (100.0, 100.0))

# ── Auto-generar centros de pernos si bolt_centers está vacío ────────
if not bolt_centers:
    A, _ = get_bolt_spacing(bolt_dia)
    bolt_centers = [
        (A/2.0,   H_col/2.0, 0.0),  (3*A/2.0,  H_col/2.0, 0.0),
        (-A/2.0,  H_col/2.0, 0.0),  (-3*A/2.0, H_col/2.0, 0.0),
        (A/2.0,  -H_col/2.0, 0.0),  (3*A/2.0, -H_col/2.0, 0.0),
        (-A/2.0, -H_col/2.0, 0.0),  (-3*A/2.0, -H_col/2.0, 0.0),
    ]
    # Limitar a n_pernos
    bolt_centers = bolt_centers[:n_pernos]

# ── Geometría de Pernos (Calculada) ──────────────────────────────────
A, B_bolt = get_bolt_spacing(bolt_dia)
circle_radius = bolt_dia / 2.0
outer_half = B_bolt / 2.0
inner_half = (circle_radius + outer_half) / 2.0
inner_side = inner_half * 2.0
bolt_length = 8.0 * bolt_dia  # Longitud del tramo inferior del perno (8×diámetro)

# ═════════════════════════════════════════════════════════════════════
# ╔═══════════════════════════════════════════════════════════════════╗
# ║                      FUNCIONES AUXILIARES                          ║
# ╚═══════════════════════════════════════════════════════════════════╝
# ═════════════════════════════════════════════════════════════════════

# ── Funciones de Puntos Geométricos ──────────────────────────────────

def create_circle_points(cx, cy, z, radius, num_points=16, prefix="P_c"):
    """Genera puntos en círculo en sentido horario (visto desde +Z).
    
    Args:
        cx, cy: Coordenadas del centro.
        z: Cota Z.
        radius: Radio del círculo.
        num_points: Número de puntos a generar.
        prefix: Prefijo para nombrar puntos.
        
    Returns:
        Lista de nombres de puntos creados.
    """
    names = []
    for j in range(num_points):
        angle = -math.radians(j * (360.0 / num_points))
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        ret = SapModel.PointObj.AddCartesian(x, y, z, "", f"{prefix}{j+1}")
        point_name = ret[0] if isinstance(ret, tuple) else f"{prefix}{j+1}"
        names.append(point_name)
    return names

def create_square_points(cx, cy, z, side, num_points=16, prefix="P_s"):
    """Genera puntos equiespaciados en un cuadrado, sentido horario desde punto medio derecho.
    
    Args:
        cx, cy: Coordenadas del centro.
        z: Cota Z.
        side: Lado del cuadrado.
        num_points: Número de puntos a generar.
        prefix: Prefijo para nombrar puntos.
        
    Returns:
        Lista de nombres de puntos creados.
    """
    half = side / 2.0
    perimeter = 4.0 * side
    names = []
    if num_points < 4:
        num_points = 4
    
    for i in range(num_points):
        s = (i * perimeter) / num_points
        if s < half:
            # Fase 1: Borde derecho, bajando desde punto medio
            x, y = half, -s
        elif s < half + side:
            # Fase 2: Borde inferior, hacia la izquierda
            rem = s - half
            x, y = half - rem, -half
        elif s < half + 2 * side:
            # Fase 3: Borde izquierdo, subiendo
            rem = s - (half + side)
            x, y = -half, -half + rem
        elif s < half + 3 * side:
            # Fase 4: Borde superior, hacia la derecha
            rem = s - (half + 2 * side)
            x, y = -half + rem, half
        else:
            # Fase 5: Borde derecho, bajando desde esquina superior
            rem = s - (half + 3 * side)
            x, y = half, half - rem
        
        ret = SapModel.PointObj.AddCartesian(cx + x, cy + y, z, "", f"{prefix}{i+1}")
        point_name = ret[0] if isinstance(ret, tuple) else f"{prefix}{i+1}"
        names.append(point_name)
    return names

def get_point_coord(point_name):
    """Obtiene las coordenadas (x, y, z) de un punto.
    
    Returns:
        Tupla (x, y, z) o None si falla.
    """
    try:
        ret = SapModel.PointObj.GetCoordCartesian(point_name, 0.0, 0.0, 0.0, "Global")
        if ret[-1] == 0:
            return (ret[0], ret[1], ret[2])
    except Exception:
        pass
    return None

def sort_points_angularly(point_names, center):
    """Ordena puntos por ángulo alrededor de un centro (sentido horario desde +X).
    
    Args:
        point_names: Lista de nombres de puntos.
        center: Tupla (cx, cy) del centro.
        
    Returns:
        Lista de nombres ordenados.
    """
    valid_pts = []
    for pn in point_names:
        if not pn:
            continue
        coord = get_point_coord(pn)
        if coord:
            angle = math.atan2(coord[1] - center[1], coord[0] - center[0])
            valid_pts.append((pn, angle))
    
    valid_pts.sort(key=lambda x: x[1], reverse=True)  # Descendente → sentido horario
    return [p[0] for p in valid_pts]

def align_rings(inner_pts, outer_pts, center):
    """Alinea dos anillos de puntos para minimizar la longitud de conexión (diferencia angular).
    
    Args:
        inner_pts: Lista de puntos del anillo interior.
        outer_pts: Lista de puntos del anillo exterior.
        center: Tupla (cx, cy) del centro.
        
    Returns:
        (inner_sorted, outer_sorted) — Listas alineadas y ordenadas.
    """
    inner_sorted = sort_points_angularly(inner_pts, center)
    outer_sorted = sort_points_angularly(outer_pts, center)
    
    if not inner_sorted or not outer_sorted:
        return inner_sorted, outer_sorted

    # Helper to get angles
    def get_angles(pts):
        angles = []
        for p in pts:
            c = get_point_coord(p)
            if c:
                angles.append(math.atan2(c[1] - center[1], c[0] - center[0]))
            else:
                angles.append(0)
        return angles

    inner_angs = get_angles(inner_sorted)
    outer_angs = get_angles(outer_sorted)
    
    n = len(inner_sorted)
    best_shift = 0
    min_diff = float('inf')
    
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

# ── Funciones de Creación de Geometría ───────────────────────────────

def create_ring_mesh(inner_pts, outer_pts, center, prop_name, prefix):
    """Crea áreas conectando dos anillos de puntos (inner → outer).
    
    Args:
        inner_pts: Lista de puntos del anillo interior.
        outer_pts: Lista de puntos del anillo exterior.
        center: Tupla (cx, cy) del centro.
        prop_name: Nombre de la propiedad shell.
        prefix: Prefijo para nombrar áreas.
    """
    inner, outer = align_rings(inner_pts, outer_pts, center)
    n = min(len(inner), len(outer))
    
    for i in range(n):
        p1 = inner[i]
        p2 = inner[(i+1) % n]
        p3 = outer[(i+1) % n]
        p4 = outer[i]
        ret = SapModel.AreaObj.AddByPoint(4, [p1, p2, p3, p4], "", prop_name, f"{prefix}_{i+1}")
        assert ret[-1] == 0, f"AddByPoint failed for {prefix}_{i+1}: {ret[-1]}"

def create_area_by_coord(xs, ys, zs, prop_name, user_name):
    """Crea un área por coordenadas.
    
    Args:
        xs, ys, zs: Listas de coordenadas X, Y, Z.
        prop_name: Nombre de la propiedad shell.
        user_name: Nombre de usuario para el área.
        
    Returns:
        Nombre del área creada.
    """
    ret = SapModel.AreaObj.AddByCoord(len(xs), xs, ys, zs, "", prop_name, user_name, "Global")
    assert ret[-1] == 0, f"AddByCoord failed for {user_name}: {ret[-1]}"
    return ret[0] if isinstance(ret, tuple) else user_name

# ── Funciones de Body Constraints y Frames ───────────────────────────

def create_body_constraint(constraint_name, center_point_name, circle_point_names, dof_values):
    """Crea un Body Constraint conectando un punto central con un anillo de puntos.
    
    Args:
        constraint_name: Nombre del constraint.
        center_point_name: Nombre del punto central.
        circle_point_names: Lista de nombres de puntos del anillo.
        dof_values: Lista de 6 booleans [UX, UY, UZ, RX, RY, RZ].
    """
    # 1. Definir el Body Constraint
    ret = SapModel.ConstraintDef.SetBody(constraint_name, dof_values, "Global")
    assert ret == 0, f"SetBody failed for {constraint_name}: {ret}"
    
    # 2. Asignar al punto central
    ret = SapModel.PointObj.SetConstraint(center_point_name, constraint_name)
    assert ret[-1] == 0, f"SetConstraint failed for center {center_point_name}: {ret[-1]}"
    
    # 3. Asignar a cada punto del círculo
    for pt_name in circle_point_names:
        if not pt_name:
            continue
        ret = SapModel.PointObj.SetConstraint(pt_name, constraint_name)
        assert ret[-1] == 0, f"SetConstraint failed for {pt_name}: {ret[-1]}"

def create_bolt_frame(i_point, j_point, section_name, user_name):
    """Crea un Frame (perno) entre dos puntos.
    
    Args:
        i_point: Nombre del punto I-End.
        j_point: Nombre del punto J-End.
        section_name: Nombre de la sección Frame.
        user_name: Nombre de usuario para el Frame.
        
    Returns:
        Nombre del Frame creado.
    """
    ret = SapModel.FrameObj.AddByPoint(i_point, j_point, "", section_name, user_name)
    assert ret[-1] == 0, f"AddByPoint failed for {user_name}: {ret[-1]}"
    return ret[0] if isinstance(ret, tuple) else user_name

def set_tc_limits(frame_name):
    """Asigna TC Limits a un Frame: compresión=0 (solo trabaja a tracción).
    
    Args:
        frame_name: Nombre del Frame.
    """
    ret = SapModel.FrameObj.SetTCLimits(
        frame_name,   # Name
        True,         # LimitCompressionExists
        0.0,          # LimitCompression [F]
        False,        # LimitTensionExists
        0.0,          # LimitTension [F]
        0             # ItemType: Object
    )
    assert ret == 0, f"SetTCLimits failed for {frame_name}: {ret}"

def set_pin_restraint(point_name):
    """Asigna apoyo articulado (Pin) a un punto: fijo en traslaciones, libre en rotaciones.
    
    Args:
        point_name: Nombre del punto.
    """
    # Value = [UX, UY, UZ, RX, RY, RZ]
    value = [True, True, True, False, False, False]
    ret = SapModel.PointObj.SetRestraint(point_name, value)
    assert ret[-1] == 0, f"SetRestraint failed for {point_name}: {ret[-1]}"

# ── Funciones de Mesh Refinement ─────────────────────────────────────

def coordinate_range_select(xmin, xmax, ymin, ymax, zmin, zmax,
                             point=True, line=False, area=False):
    """Selecciona objetos dentro de un rango de coordenadas.
    
    Args:
        xmin, xmax, ymin, ymax, zmin, zmax: Límites de la caja de selección.
        point, line, area: Tipos de objetos a seleccionar.
        
    Returns:
        True si la selección fue exitosa.
    """
    try:
        ret = SapModel.SelectObj.CoordinateRange(
            float(xmin), float(xmax),
            float(ymin), float(ymax),
            float(zmin), float(zmax),
            False,      # deselect
            "Global",   # csys
            True,       # include_intersections
            point, line, area, False, False  # point, line, area, solid, link
        )
        if isinstance(ret, (list, tuple)):
            return ret[-1] == 0
        else:
            return int(ret) == 0
    except Exception:
        return False

def divide_area_by_selection(area_name):
    """Divide un área usando puntos seleccionados en los bordes (MeshType=3).
    
    Args:
        area_name: Nombre del área a dividir.
        
    Returns:
        Lista de nombres de las nuevas áreas creadas.
    """
    try:
        # MeshType=3 → Divide by points on edges
        ret = SapModel.EditArea.Divide(
            str(area_name), 3, 0, [], 0, 0, 0.0, 0.0,
            False, False, True
        )
        if ret[-1] == 0 and len(ret) >= 2:
            names = ret[1]
            if isinstance(names, (list, tuple)):
                return list(names)
    except Exception as e:
        print(f"Error dividiendo área '{area_name}': {e}")
    return []

def subdivide_area(area_name, n1, n2):
    """Subdivide un área en grilla n1×n2 (MeshType=1).
    
    Args:
        area_name: Nombre del área.
        n1, n2: Número de divisiones en cada dirección.
    """
    try:
        ret = SapModel.EditArea.Divide(area_name, 1, 0, [], n1, n2)
        assert ret[-1] == 0, f"Divide failed for {area_name}: {ret[-1]}"
    except Exception as e:
        print(f"Error subdividiendo área '{area_name}': {e}")

# ── Función de Asignación de Balasto ─────────────────────────────────

def assign_balasto_spring(ks):
    """Asigna módulo de balasto (resorte) a todas las áreas en z=0.
    
    Args:
        ks: Módulo de balasto [kgf/cm³].
    """
    if not ks or ks <= 0:
        return
    
    current_units = SapModel.GetPresentUnits()
    SapModel.SetPresentUnits(14)  # kgf_cm_C
    
    try:
        # Seleccionar todas las áreas en z=0
        SapModel.SelectObj.ClearSelection()
        coordinate_range_select(-1e10, 1e10, -1e10, 1e10, 0.0, 0.0, point=False, area=True)
        
        # Asignar spring
        vec = [0.0, 0.0, 0.0]
        ret = SapModel.AreaObj.SetSpring(
            "ALL",      # Name (ignored when ItemType=2)
            1,          # MyType: simple spring
            float(ks),  # s: stiffness per unit area [kgf/cm³]
            2,          # SimpleSpringType: compression only
            "",         # LinkProp
            -1,         # Face: bottom face
            2,          # SpringLocalOneType: normal to face
            1,          # Dir (not used when SpringLocalOneType=2)
            True,       # Outward
            vec,        # Vec (not used when SpringLocalOneType=2)
            0.0,        # Ang
            True,       # Replace
            "Local",    # CSys
            2           # ItemType: SelectedObjects
        )
        assert ret == 0, f"SetSpring failed: {ret}"
        print(f"✅ Módulo de balasto ks={ks} kgf/cm³ asignado a áreas en z=0.")
    except Exception as e:
        print(f"Error asignando balasto: {e}")
    finally:
        SapModel.SetPresentUnits(current_units)

# ═════════════════════════════════════════════════════════════════════
# ╔═══════════════════════════════════════════════════════════════════╗
# ║                    EJECUCION PRINCIPAL                             ║
# ╚═══════════════════════════════════════════════════════════════════╝
# ═════════════════════════════════════════════════════════════════════

# ── 1. Initialize ─────────────────────────────────────────────────────
ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

# ── 2. Materiales y Propiedades ──────────────────────────────────────

# ── 2.1. Propiedad de Placa Base ─────────────────────────────────────
ret = SapModel.PropArea.SetShell_1(
    "PLACA_BASE", 1, True, "A992Fy50", 0.0, plate_thickness, plate_thickness
)
assert ret == 0, f"SetShell_1 failed for PLACA_BASE: {ret}"
print(f"Propiedad 'PLACA_BASE' creada (t={plate_thickness}).")

# ── 2.2. Propiedad de Alas de Columna ────────────────────────────────
ret = SapModel.PropArea.SetShell_1(
    "ALA", 1, True, "A992Fy50", 0.0, flange_thickness, flange_thickness
)
assert ret == 0, f"SetShell_1 failed for ALA: {ret}"
print(f"Propiedad 'ALA' creada (t={flange_thickness}).")

# ── 2.3. Propiedad de Alma de Columna ────────────────────────────────
ret = SapModel.PropArea.SetShell_1(
    "ALMA", 1, True, "A992Fy50", 0.0, web_thickness, web_thickness
)
assert ret == 0, f"SetShell_1 failed for ALMA: {ret}"
print(f"Propiedad 'ALMA' creada (t={web_thickness}).")

# ── 2.4. Propiedad de Silla de Anclaje (si está activada) ────────────
if include_anchor_chair and anchor_chair_height > 0 and anchor_chair_thickness > 0:
    ret = SapModel.PropArea.SetShell_1(
        "ChairPlate", 1, True, "A992Fy50", 0.0, anchor_chair_thickness, anchor_chair_thickness
    )
    assert ret == 0, f"SetShell_1 failed for ChairPlate: {ret}"
    print(f"Propiedad 'ChairPlate' creada (t={anchor_chair_thickness}).")
else:
    include_anchor_chair = False  # Force disable if invalid params

# ── 2.5. Sección Frame de Pernos (Circular Sólida) ───────────────────
bolt_section_name = f"BOLT_{int(bolt_dia)}"
ret = SapModel.PropFrame.SetCircle(bolt_section_name, bolt_material, bolt_dia)
assert ret == 0, f"SetCircle failed for {bolt_section_name}: {ret}"
print(f"Sección Frame '{bolt_section_name}' creada (d={bolt_dia}, mat={bolt_material}).")

# ── 3. Geometría de Columna ───────────────────────────────────────────

# ── 3.1. Ala Superior ─────────────────────────────────────────────────
create_area_by_coord(
    [-B_col/2, B_col/2, B_col/2, -B_col/2],
    [H_col/2, H_col/2, H_col/2, H_col/2],
    [0, 0, z_col, z_col],
    "ALA", "COL_FLANGE_TOP"
)
print("Ala superior de columna creada (COL_FLANGE_TOP).")

# ── 3.2. Ala Inferior ─────────────────────────────────────────────────
create_area_by_coord(
    [-B_col/2, B_col/2, B_col/2, -B_col/2],
    [-H_col/2, -H_col/2, -H_col/2, -H_col/2],
    [0, 0, z_col, z_col],
    "ALA", "COL_FLANGE_BOTTOM"
)
print("Ala inferior de columna creada (COL_FLANGE_BOTTOM).")

# ── 3.3. Alma de Columna ──────────────────────────────────────────────
create_area_by_coord(
    [0, 0, 0, 0],
    [H_col/2, -H_col/2, -H_col/2, H_col/2],
    [0, 0, z_col, z_col],
    "ALMA", "COL_WEB"
)
print("Alma de columna creada (COL_WEB).")

# ── 4. Pernos y Body Constraints ──────────────────────────────────────

bolt_frame_names = []           # Lista de Frames de pernos (para TC Limits)
outer_square_points_list = []   # Puntos exteriores de cada perno (para A_outer_link)

for idx, (cx, cy, cz) in enumerate(bolt_centers, 1):
    print(f"\n── Procesando perno {idx} en ({cx}, {cy}, {cz}) ───")
    
    # ── 4.1. Punto Central del Perno ─────────────────────────────────
    ret = SapModel.PointObj.AddCartesian(cx, cy, cz, "", f"CENTER_{idx}")
    center_point_name = ret[0] if isinstance(ret, tuple) else f"CENTER_{idx}"
    
    # ── 4.2. Puntos Geométricos (Círculo, Cuadrado Interior, Cuadrado Exterior) ─
    c_pts = create_circle_points(cx, cy, cz, circle_radius, 16, f"P_c{idx}_")
    in_pts = create_square_points(cx, cy, cz, inner_side, 16, f"P_s_in{idx}_")
    out_pts = create_square_points(cx, cy, cz, B_bolt, 16, f"P_s_out{idx}_")
    outer_square_points_list.append(out_pts)
    
    # ── 4.3. Mesh de Anillos (Círculo → Interior → Exterior) ─────────
    create_ring_mesh(c_pts, in_pts, (cx, cy), "PLACA_BASE", f"A_ring_in{idx}")
    create_ring_mesh(in_pts, out_pts, (cx, cy), "PLACA_BASE", f"A_ring_out{idx}")
    print(f"Mesh de perno {idx} creado (círculo → interior → exterior).")
    
    # ── 4.4. Frame del Perno (Centro → Fundación) ────────────────────
    # Crear punto inferior (fundación)
    ret = SapModel.PointObj.AddCartesian(cx, cy, cz - bolt_length, "", f"BOLT_BASE_{idx}")
    bottom_point = ret[0] if isinstance(ret, tuple) else f"BOLT_BASE_{idx}"
    
    # Crear Frame
    frame_name = create_bolt_frame(center_point_name, bottom_point, bolt_section_name, f"BOLT_FRAME_{idx}")
    bolt_frame_names.append(frame_name)
    print(f"Frame de perno '{frame_name}' creado (L={bolt_length}).")
    
    # ── 4.5. Body Constraint (Centro ↔ Círculo) ──────────────────────
    # Para pernos SIN silla: todos los DOF restringidos
    # Para pernos CON silla (más adelante): UZ libre en placa, todos restringidos en silla
    if not include_anchor_chair:
        dof_values = [True, True, True, True, True, True]  # Todos restringidos
        create_body_constraint(f"BOLT_BODY_{idx}", center_point_name, c_pts, dof_values)
        print(f"Body Constraint 'BOLT_BODY_{idx}' creado (DOF=111111).")
    else:
        # UZ libre → perno puede deslizar verticalmente en la placa
        dof_values = [True, True, False, True, True, True]  # UZ=False
        create_body_constraint(f"BOLT_BODY_{idx}", center_point_name, c_pts, dof_values)
        print(f"Body Constraint 'BOLT_BODY_{idx}' creado (DOF=110111, UZ libre).")
    
    # ── 4.6. TC Limits (Compresión=0) ────────────────────────────────
    set_tc_limits(frame_name)
    print(f"TC Limits asignados a '{frame_name}' (compresión=0).")
    
    # ── 4.7. Pin Restraint (Fundación) ───────────────────────────────
    set_pin_restraint(bottom_point)
    print(f"Pin restraint asignado a '{bottom_point}'.")

# ── 5. Sillas de Anclaje (Anchor Chairs) ─────────────────────────────

if include_anchor_chair:
    print(f"\n═══ Generando Sillas de Anclaje a z={anchor_chair_height} ═══")
    
    chair_outer_square_points_list = []  # Puntos exteriores de sillas (para A_chair_link)
    
    for idx, (cx, cy, cz) in enumerate(bolt_centers, 1):
        print(f"\n── Procesando silla para perno {idx} ───")
        
        # ── 5.1. Punto Central de la Silla ───────────────────────────
        ret = SapModel.PointObj.AddCartesian(cx, cy, anchor_chair_height, "", f"CHAIR_CENTER_{idx}")
        chair_center = ret[0] if isinstance(ret, tuple) else f"CHAIR_CENTER_{idx}"
        
        # ── 5.2. Puntos Geométricos de la Silla ──────────────────────
        chair_c_pts = create_circle_points(cx, cy, anchor_chair_height, circle_radius, 16, f"CHAIR_c{idx}_")
        chair_in_pts = create_square_points(cx, cy, anchor_chair_height, inner_side, 16, f"CHAIR_sin{idx}_")
        chair_out_pts = create_square_points(cx, cy, anchor_chair_height, B_bolt, 16, f"CHAIR_sout{idx}_")
        chair_outer_square_points_list.append(chair_out_pts)
        
        # ── 5.3. Mesh de Silla ────────────────────────────────────────
        create_ring_mesh(chair_c_pts, chair_in_pts, (cx, cy), "ChairPlate", f"CHAIR_ring_in{idx}")
        create_ring_mesh(chair_in_pts, chair_out_pts, (cx, cy), "ChairPlate", f"CHAIR_ring_out{idx}")
        print(f"Mesh de silla {idx} creado.")
        
        # ── 5.4. Frame Superior del Perno (Silla → Placa) ────────────
        center_point_name = f"CENTER_{idx}"  # Punto en la placa base
        chair_frame = create_bolt_frame(chair_center, center_point_name, bolt_section_name, f"BOLT_CHAIR_FRAME_{idx}")
        bolt_frame_names.append(chair_frame)
        print(f"Frame superior '{chair_frame}' creado (silla → placa).")
        
        # ── 5.5. Body Constraint en Silla (Todos DOF Restringidos) ───
        dof_values = [True, True, True, True, True, True]
        create_body_constraint(f"BOLT_BODY_CHAIR_{idx}", chair_center, chair_c_pts, dof_values)
        print(f"Body Constraint 'BOLT_BODY_CHAIR_{idx}' creado (DOF=111111).")
        
        # ── 5.6. TC Limits en Frame Superior ─────────────────────────
        set_tc_limits(chair_frame)
        print(f"TC Limits asignados a '{chair_frame}'.")
    
    # ── 5.7. Crear Puntos de Columna a Altura de Silla ───────────────
    # Estos puntos permiten mesh compatibility entre columna y sillas
    z_chair = anchor_chair_height
    SapModel.PointObj.AddCartesian(-B_col/2, H_col/2, z_chair, "", "COL_FT_CHAIR_L")
    SapModel.PointObj.AddCartesian( B_col/2, H_col/2, z_chair, "", "COL_FT_CHAIR_R")
    SapModel.PointObj.AddCartesian(-B_col/2, -H_col/2, z_chair, "", "COL_FB_CHAIR_L")
    SapModel.PointObj.AddCartesian( B_col/2, -H_col/2, z_chair, "", "COL_FB_CHAIR_R")
    SapModel.PointObj.AddCartesian(0, H_col/2, z_chair, "", "COL_WEB_CHAIR_T")
    SapModel.PointObj.AddCartesian(0, -H_col/2, z_chair, "", "COL_WEB_CHAIR_B")
    print(f"Puntos de columna creados a z={z_chair} para compatibilidad de mesh.")

# ── 6. Área de Enlace (A_outer_link) ─────────────────────────────────

if len(bolt_centers) >= 4:
    print("\n═══ Generando Área de Enlace (A_outer_link) ═══")
    try:
        N = len(bolt_centers) // 2
        # Índices: 0 → 1er perno, N-1 → Nth perno, N → (N+1)th perno, 2N-1 → 2Nth perno
        # Puntos en cuadrados (16 pts, CW desde medio derecho):
        #   2=BR, 6=BL, 10=TL, 14=TR
        # Orden CCW (visto desde +Z) para eje 3 → +Z:
        #   BL_link → BR_link → TR_link → TL_link
        p1 = outer_square_points_list[N][10]      # (N+1)th center, TL = BL del link
        p2 = outer_square_points_list[2*N-1][14]  # 2Nth center, TR = BR del link
        p3 = outer_square_points_list[N-1][2]     # Nth center, BR = TR del link
        p4 = outer_square_points_list[0][6]       # 1st center, BL = TL del link
        
        ret = SapModel.AreaObj.AddByPoint(4, [p1, p2, p3, p4], "", "PLACA_BASE", "A_outer_link")
        assert ret[-1] == 0, f"AddByPoint failed for A_outer_link: {ret[-1]}"
        print("Área de enlace 'A_outer_link' creada.")
        
        # Dividir el área de enlace
        ret = SapModel.EditArea.Divide("A_outer_link", 1, 0, [], 4*n_pernos, 10)
        assert ret[-1] == 0, f"Divide failed for A_outer_link: {ret[-1]}"
        print(f"Área 'A_outer_link' dividida ({4*n_pernos}×10).")
    except Exception as e:
        print(f"No se pudo crear área de enlace: {e}")

# ── 7. Área de Enlace de Silla (A_chair_link) ────────────────────────

if include_anchor_chair and len(bolt_centers) >= 4:
    print("\n═══ Generando Área de Enlace de Silla (A_chair_link) ═══")
    try:
        N = len(bolt_centers) // 2
        p1 = chair_outer_square_points_list[N][10]      # (N+1)th center, TL
        p2 = chair_outer_square_points_list[2*N-1][14]  # 2Nth center, TR
        p3 = chair_outer_square_points_list[N-1][2]     # Nth center, BR
        p4 = chair_outer_square_points_list[0][6]       # 1st center, BL
        
        ret = SapModel.AreaObj.AddByPoint(4, [p1, p2, p3, p4], "", "ChairPlate", "A_chair_link")
        assert ret[-1] == 0, f"AddByPoint failed for A_chair_link: {ret[-1]}"
        print("Área de enlace de silla 'A_chair_link' creada.")
        
        # Dividir
        ret = SapModel.EditArea.Divide("A_chair_link", 1, 0, [], 4*n_pernos, 10)
        assert ret[-1] == 0, f"Divide failed for A_chair_link: {ret[-1]}"
        print(f"Área 'A_chair_link' dividida ({4*n_pernos}×10).")
    except Exception as e:
        print(f"No se pudo crear área de enlace de silla: {e}")

# ── 8. Mesh Refinement (División de Alas y Alma por Puntos Seleccionados) ─

print("\n═══ Refinando Mesh en Intersecciones ═══")

# ── 8.1. Ala Superior (COL_FLANGE_TOP) ───────────────────────────────
SapModel.SelectObj.ClearSelection()
# Seleccionar puntos en y = H_col/2, z = 0 (base)
ok = coordinate_range_select(-B_col/2, B_col/2, H_col/2, H_col/2, 0.0, 0.0, point=True)
# Si hay silla, también seleccionar puntos a z = anchor_chair_height
if include_anchor_chair:
    coordinate_range_select(-B_col/2, B_col/2, H_col/2, H_col/2, anchor_chair_height, anchor_chair_height, point=True)
if ok:
    new_areas = divide_area_by_selection("COL_FLANGE_TOP")
    print(f"Ala superior dividida en {len(new_areas)} áreas.")
    for area in new_areas:
        subdivide_area(area, 1, 2)
    print("Subdivisión de ala superior completada (1×2).")

# ── 8.2. Ala Inferior (COL_FLANGE_BOTTOM) ────────────────────────────
SapModel.SelectObj.ClearSelection()
ok = coordinate_range_select(-B_col/2, B_col/2, -H_col/2, -H_col/2, 0.0, 0.0, point=True)
if include_anchor_chair:
    coordinate_range_select(-B_col/2, B_col/2, -H_col/2, -H_col/2, anchor_chair_height, anchor_chair_height, point=True)
if ok:
    new_areas = divide_area_by_selection("COL_FLANGE_BOTTOM")
    print(f"Ala inferior dividida en {len(new_areas)} áreas.")
    for area in new_areas:
        subdivide_area(area, 1, 2)
    print("Subdivisión de ala inferior completada (1×2).")

# ── 8.3. A_outer_link (División por Puntos en y=H_col/2, z=0) ────────
SapModel.SelectObj.ClearSelection()
x_limit = A * n_pernos / 2.0
ok = coordinate_range_select(-x_limit, x_limit, H_col/2, H_col/2, 0.0, 0.0, point=True)
if ok:
    new_areas = divide_area_by_selection("A_outer_link")
    print(f"A_outer_link dividida en {len(new_areas)} áreas.")
    for area in new_areas:
        subdivide_area(area, 1, 2)
    print("Subdivisión de A_outer_link completada (1×2).")

# ── 8.4. A_chair_link (División por Puntos en y=H_col/2, z=chair) ────
if include_anchor_chair:
    SapModel.SelectObj.ClearSelection()
    ok = coordinate_range_select(-x_limit, x_limit, H_col/2, H_col/2, anchor_chair_height, anchor_chair_height, point=True)
    if ok:
        new_areas = divide_area_by_selection("A_chair_link")
        print(f"A_chair_link dividida en {len(new_areas)} áreas.")
        for area in new_areas:
            subdivide_area(area, 1, 2)
        print("Subdivisión de A_chair_link completada (1×2).")

# ── 8.5. Alma (COL_WEB) ───────────────────────────────────────────────
SapModel.SelectObj.ClearSelection()
ok = coordinate_range_select(0.0, 0.0, -H_col/2, H_col/2, 0.0, 0.0, point=True)
if include_anchor_chair:
    coordinate_range_select(0.0, 0.0, -H_col/2, H_col/2, anchor_chair_height, anchor_chair_height, point=True)
if ok:
    new_areas = divide_area_by_selection("COL_WEB")
    print(f"Alma dividida en {len(new_areas)} áreas.")
    for area in new_areas:
        subdivide_area(area, 1, 2)
    print("Subdivisión de alma completada (1×2).")

# ── 9. Asignación de Módulo de Balasto ───────────────────────────────

if ks_balasto > 0:
    print(f"\n═══ Asignando Módulo de Balasto (ks={ks_balasto} kgf/cm³) ═══")
    assign_balasto_spring(ks_balasto)
else:
    print("\n═══ Módulo de balasto no especificado (omitido). ═══")

# ── 10. Guardar Modelo ────────────────────────────────────────────────

ret = SapModel.File.Save(sap_temp_dir + r"\example_placabase_parametric.sdb")
assert ret == 0, f"File.Save failed: {ret}"
print("\n✅ Modelo guardado como 'example_placabase_parametric.sdb'.")

# ── 11. Refresh View ──────────────────────────────────────────────────

try:
    SapModel.View.RefreshView(0, False)
    SapModel.View.RefreshWindow()
    print("✅ Vista refrescada.")
except Exception:
    pass

# ── 12. Resultados Finales ───────────────────────────────────────────

result["bolt_count"] = len(bolt_centers)
result["bolt_dia"] = bolt_dia
result["H_col"] = H_col
result["B_col"] = B_col
result["plate_thickness"] = plate_thickness
result["include_anchor_chair"] = include_anchor_chair
result["anchor_chair_height"] = anchor_chair_height if include_anchor_chair else None
result["ks_balasto"] = ks_balasto if ks_balasto > 0 else None
result["bolt_frame_count"] = len(bolt_frame_names)
result["success"] = True

print("\n" + "═"*70)
print("🎉 GENERACION DE PLACA BASE COMPLETADA EXITOSAMENTE 🎉")
print("═"*70)
print(f"  • Pernos creados: {len(bolt_centers)}")
print(f"  • Frames de pernos: {len(bolt_frame_names)}")
print(f"  • Silla de anclaje: {'SÍ' if include_anchor_chair else 'NO'}")
print(f"  • Módulo de balasto: {'SÍ' if ks_balasto > 0 else 'NO'}")
print("═"*70)
