# ─── SAP2000 Circular Ring Area Generator — Parametric Script ─────────────────
# Description: Crea un modelo de anillo circular (placa anular) con 3 zonas
#              concéntricas de área (shell), separadas por radios intermedios.
#              La geometría se genera en el plano XY (Z=0).
#
#   Zona 1 (Interior) : r_inner → r_mid1  — espesor t1
#   Zona 2 (Intermedia): r_mid1  → r_mid2  — espesor t2
#   Zona 3 (Exterior) : r_mid2  → r_outer — espesor t1
#
# Entradas:
#   r_inner, r_mid1, r_mid2, r_outer  — radios de separación [m]
#   t1, t2                            — dos espesores de shell [m]
#   n_segs                            — segmentos angulares (calidad de malla)
#
# Units : kN_m_C  (ID 6)
# ──────────────────────────────────────────────────────────────────────────────

# NOTE: `math` es pre-inyectado por el sandbox — no usar `import math`

# ═════════════════════════════════════════════════════════════════════════════
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                       CONFIGURACION DE VARIABLES                          ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# ═════════════════════════════════════════════════════════════════════════════

# ── Radios [m] ────────────────────────────────────────────────────────────────
r_inner = 1.0    # Radio interior (borde del agujero central)
r_mid1  = 2.0    # Límite entre Zona 1 (interior) y Zona 2 (intermedia)
r_mid2  = 3.5    # Límite entre Zona 2 (intermedia) y Zona 3 (exterior)
r_outer = 5.0    # Radio exterior (borde externo del anillo)

# ── Espesores de shell [m] ────────────────────────────────────────────────────
t1 = 0.30        # Espesor de Zona 1 (interior) y Zona 3 (exterior)
t2 = 0.20        # Espesor de Zona 2 (intermedia)

# ── Material ──────────────────────────────────────────────────────────────────
mat_name = "CONC"          # Nombre del material
E_mat    = 2.5e7           # Módulo de elasticidad [kN/m²] (≈ 25 GPa)
nu_mat   = 0.2             # Coeficiente de Poisson
alpha    = 1.0e-5          # Coef. expansión térmica [1/°C]

# ── Discretización ────────────────────────────────────────────────────────────
n_segs = 36                # Segmentos angulares (>=12 recomendado, 36 = malla fina)

# ═════════════════════════════════════════════════════════════════════════════
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                        FUNCIONES AUXILIARES                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# ═════════════════════════════════════════════════════════════════════════════

def ring_pts(radius, n):
    """Devuelve lista de n puntos (x, y) sobre una circunferencia de radio dado."""
    return [
        (radius * math.cos(2.0 * math.pi * i / n),
         radius * math.sin(2.0 * math.pi * i / n))
        for i in range(n)
    ]

# ═════════════════════════════════════════════════════════════════════════════
# ── Task 1: Inicializar modelo ────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

result["task_1_init"] = True

# ═════════════════════════════════════════════════════════════════════════════
# ── Task 2: Definir material ──────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

ret = SapModel.PropMaterial.SetMaterial(mat_name, 2)  # 2 = Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic(mat_name, E_mat, nu_mat, alpha)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

result["task_2_material"] = mat_name

# ═════════════════════════════════════════════════════════════════════════════
# ── Task 3: Definir propiedades de área (shell) ───────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

# SHELL_T1 — usado en Zona 1 (interior) y Zona 3 (exterior)
ret = SapModel.PropArea.SetShell_1("SHELL_T1", 1, True, mat_name, 0, t1, t1)
assert ret == 0, f"SetShell_1(SHELL_T1) failed: {ret}"

# SHELL_T2 — usado en Zona 2 (intermedia)
ret = SapModel.PropArea.SetShell_1("SHELL_T2", 1, True, mat_name, 0, t2, t2)
assert ret == 0, f"SetShell_1(SHELL_T2) failed: {ret}"

result["task_3_sections"] = {"SHELL_T1": t1, "SHELL_T2": t2}

# ═════════════════════════════════════════════════════════════════════════════
# ── Task 4: Generar geometría de anillos concéntricos ─────────────────────────
# ═════════════════════════════════════════════════════════════════════════════
#
#  Cada zona se subdivide en n_segs paneles cuadriláteros (quads).
#  Para el segmento i (de n_segs totales):
#    ángulo1 = 2π * i / n_segs
#    ángulo2 = 2π * (i+1) / n_segs
#  Corners del quad (sentido antihorario visto desde +Z):
#    P0 = (r_in  * cos(a1), r_in  * sin(a1))
#    P1 = (r_out * cos(a1), r_out * sin(a1))
#    P2 = (r_out * cos(a2), r_out * sin(a2))
#    P3 = (r_in  * cos(a2), r_in  * sin(a2))
# ─────────────────────────────────────────────────────────────────────────────

zones = [
    #  r_in,   r_out,  section,   label
    (r_inner, r_mid1, "SHELL_T1", "ZONA1_interior"),
    (r_mid1,  r_mid2, "SHELL_T2", "ZONA2_intermedia"),
    (r_mid2,  r_outer,"SHELL_T1", "ZONA3_exterior"),
]

area_count = {"ZONA1_interior": 0, "ZONA2_intermedia": 0, "ZONA3_exterior": 0}

for (r_in, r_out, prop, label) in zones:
    pts_in  = ring_pts(r_in,  n_segs)
    pts_out = ring_pts(r_out, n_segs)

    for i in range(n_segs):
        j = (i + 1) % n_segs  # índice siguiente (cierra el anillo)

        # Quad corners: inner_i → outer_i → outer_j → inner_j
        x = [pts_in[i][0], pts_out[i][0], pts_out[j][0], pts_in[j][0]]
        y = [pts_in[i][1], pts_out[i][1], pts_out[j][1], pts_in[j][1]]
        z = [0.0, 0.0, 0.0, 0.0]

        raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", prop, "")
        assert raw[-1] == 0, f"AddByCoord({label}[{i}]) failed: {raw[-1]}"
        area_count[label] += 1

result["task_4_geometry"] = area_count
result["total_areas"] = sum(area_count.values())

# ═════════════════════════════════════════════════════════════════════════════
# ── Task 5: Guardar modelo y refrescar vista ──────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

ret = SapModel.File.Save(sap_temp_dir + r"\ring_areas_model.sdb")
assert ret == 0, f"File.Save failed: {ret}"

SapModel.View.RefreshView(0, False)

result["task_5_saved"] = True

# ═════════════════════════════════════════════════════════════════════════════
# ── Resumen final ────────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

result["success"]     = True
result["radii"]       = {"r_inner": r_inner, "r_mid1": r_mid1,
                          "r_mid2": r_mid2,  "r_outer": r_outer}
result["thicknesses"] = {"t1 (Zona1+Zona3)": t1, "t2 (Zona2)": t2}
result["n_segments"]  = n_segs
