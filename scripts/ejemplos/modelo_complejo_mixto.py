# ============================================================
# Script: modelo_complejo_mixto.py
# Description: Modelo estructural complejo que combina elementos
#              frame y área para ejercitar todas las funciones
#              verificadas de la API de SAP2000.
#
# Estructura modelada: Nave industrial de 1 planta, 2 vanos
#   - 6 columnas de H.A. (5 rectangulares + 1 circular)
#   - 7 vigas de H.A. (6 rectangulares + 1 perfil I acero)
#   - 2 arriostres diagonales tension-only (cruce de San Andrés)
#   - 2 losas de piso mallas FEM 3×2 (LOSA_20)
#   - Losa de fundación corrida con resortes Winkler
#   - Apoyos articulados (pinned) en bases de columnas
#   - Diafragma rígido en nivel de piso (Z=4m)
#   - Selección por rango de coordenadas
#   - Patrones: PP, CM, CV, SX, SY, VIENTO
#   - Espectro RS simplificado NCh2745 Zona 3 Suelo II
#   - Casos espectrales: RS_SX (U1) y RS_SY (U2)
#   - Combinaciones ULS: COMB1, COMB2_SX, COMB3_SY, ENV_ULS
#
# Planta (Z=0 y Z=4):
#
#   Y=5 |  T4(0,5,z) ----B3---- T5(6,5,z) ----B4---- T6(12,5,z) [circular]
#       |     |                    |                    |
#      B5   (B5)                 (B6)                 V_T3_T6=B7
#       |     |                    |                    |
#   Y=0 |  T1(0,0,z) ----B1---- T2(6,0,z) ----B2---- T3(12,0,z)
#            0              6              12   --> X
#
#   Arriostres (cara Y=0, sin losa): ARR_1 de (0,0,0)→(6,0,4)
#                                    ARR_2 de (6,0,4)→(12,0,0)
#
# Units: kN, m, C (código unidades SAP2000 = 6)
# ============================================================

# ─── 0. INICIALIZAR MODELO ────────────────────────────────────────────────────
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

ret = SapModel.SetPresentUnits(6)  # 6 = kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# ─── 1. MATERIALES ────────────────────────────────────────────────────────────

# --- Hormigón H30 ---
# E=2.87e7 kN/m², ν=0.2, α=1e-5 /°C, γ=24 kN/m³
ret = SapModel.PropMaterial.SetMaterial("H30", 2)          # 2=Concrete
assert ret == 0, f"SetMaterial(H30) failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("H30", 2.87e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic(H30) failed: {ret}"

ret = SapModel.PropMaterial.SetWeightAndMass("H30", 1, 24.0)       # peso unitario [kN/m³]
assert ret == 0, f"SetWeightAndMass(H30, weight) failed: {ret}"

ret = SapModel.PropMaterial.SetWeightAndMass("H30", 2, 24.0 / 9.81)  # masa unitaria [kN·s²/m⁴]
assert ret == 0, f"SetWeightAndMass(H30, mass) failed: {ret}"

# --- Acero A42 ---
# E=2.0e8 kN/m², ν=0.3, α=1.2e-5 /°C, γ=78.5 kN/m³
ret = SapModel.PropMaterial.SetMaterial("A42", 1)          # 1=Steel
assert ret == 0, f"SetMaterial(A42) failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("A42", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic(A42) failed: {ret}"

ret = SapModel.PropMaterial.SetWeightAndMass("A42", 1, 78.5)
assert ret == 0, f"SetWeightAndMass(A42, weight) failed: {ret}"

ret = SapModel.PropMaterial.SetWeightAndMass("A42", 2, 78.5 / 9.81)
assert ret == 0, f"SetWeightAndMass(A42, mass) failed: {ret}"

# ─── 2. SECCIONES FRAME ───────────────────────────────────────────────────────

# (a) Columna rectangular H30 – 40×40 cm
ret = SapModel.PropFrame.SetRectangle("COL_40x40", "H30", 0.40, 0.40)
assert ret == 0, f"SetRectangle(COL_40x40) failed: {ret}"

# (b) Viga rectangular H30 – depth=50 cm, width=30 cm
ret = SapModel.PropFrame.SetRectangle("VIGA_30x50", "H30", 0.50, 0.30)
assert ret == 0, f"SetRectangle(VIGA_30x50) failed: {ret}"

# (c) Columna circular H30 – Ø30 cm (esquina T6, para variedad)
ret = SapModel.PropFrame.SetCircle("COL_CIRC30", "H30", 0.30)
assert ret == 0, f"SetCircle(COL_CIRC30) failed: {ret}"

# (d) Arriostre tubo cuadrado acero – HSS 150×150×8 mm
ret = SapModel.PropFrame.SetTube("ARRIOSTRE_HSS", "A42", 0.15, 0.15, 0.008, 0.008)
assert ret == 0, f"SetTube(ARRIOSTRE_HSS) failed: {ret}"

# (e) Viga perfil I acero – tipo IPN300 simplificado
#     T3=overall_depth, T2=top_flange_w, TF=top_flange_t, TW=web_t,
#     T2B=bot_flange_w, TFB=bot_flange_t
ret = SapModel.PropFrame.SetISection("VIGA_I_300", "A42", 0.30, 0.15, 0.012, 0.008, 0.15, 0.012)
assert ret == 0, f"SetISection(VIGA_I_300) failed: {ret}"

# ─── 3. SECCIONES ÁREA ────────────────────────────────────────────────────────

# (a) Losa de piso – ShellThin H30 e=0.20 m  (ShellType=1)
ret = SapModel.PropArea.SetShell_1("LOSA_20", 1, True, "H30", 0, 0.20, 0.20)
assert ret == 0, f"SetShell_1(LOSA_20) failed: {ret}"

# (b) Losa de fundación – Plate H30 e=0.60 m  (ShellType=2=Plate)
ret = SapModel.PropArea.SetShell_1("FUND_60", 2, True, "H30", 0, 0.60, 0.60)
assert ret == 0, f"SetShell_1(FUND_60) failed: {ret}"

# ─── 4. GEOMETRÍA — COLUMNAS ──────────────────────────────────────────────────
#
#  Grid: X={0,6,12}m,  Y={0,5}m,  altur H=4m
#
#   T4(0,5)  T5(6,5)  T6(12,5) ← circular
#   T1(0,0)  T2(6,0)  T3(12,0)

col_data = [
    (0.0,  0.0, "COL_40x40",  "T1"),
    (6.0,  0.0, "COL_40x40",  "T2"),
    (12.0, 0.0, "COL_40x40",  "T3"),
    (0.0,  5.0, "COL_40x40",  "T4"),
    (6.0,  5.0, "COL_40x40",  "T5"),
    (12.0, 5.0, "COL_CIRC30", "T6"),  # columna circular
]

col_frame_names = {}  # tag → internal frame name
for (x, y, sec, tag) in col_data:
    raw = SapModel.FrameObj.AddByCoord(x, y, 0.0, x, y, 4.0, "", sec, tag)
    assert raw[-1] == 0, f"AddByCoord(columna {tag}) failed: {raw[-1]}"
    col_frame_names[tag] = raw[0]

# ─── 5. GEOMETRÍA — VIGAS EN NIVEL Z=4 ───────────────────────────────────────

# Vigas H.A. rectangulares (longitudinales y transversales)
beam_rect = [
    (0.0,  0.0, 6.0,  0.0, "VIGA_30x50", "B1"),    # eje Y=0 tramo 1
    (6.0,  0.0, 12.0, 0.0, "VIGA_30x50", "B2"),    # eje Y=0 tramo 2
    (0.0,  5.0, 6.0,  5.0, "VIGA_30x50", "B3"),    # eje Y=5 tramo 1
    (6.0,  5.0, 12.0, 5.0, "VIGA_30x50", "B4"),    # eje Y=5 tramo 2
    (0.0,  0.0, 0.0,  5.0, "VIGA_30x50", "B5"),    # eje X=0 transversal
    (6.0,  0.0, 6.0,  5.0, "VIGA_30x50", "B6"),    # eje X=6 transversal
]

# Viga perfil I acero en eje X=12 (transversal derecho)
beam_I = [
    (12.0, 0.0, 12.0, 5.0, "VIGA_I_300", "B7"),
]

beam_frame_names = {}  # tag → internal frame name
for (x1, y1, x2, y2, sec, tag) in beam_rect + beam_I:
    raw = SapModel.FrameObj.AddByCoord(x1, y1, 4.0, x2, y2, 4.0, "", sec, tag)
    assert raw[-1] == 0, f"AddByCoord(viga {tag}) failed: {raw[-1]}"
    beam_frame_names[tag] = raw[0]

# ─── 6. ARRIOSTRES DIAGONALES — CRUCE DE SAN ANDRÉS (cara Y=0) ───────────────
#
#  Tension-only: LimitCompression=0 (no admite compresión)
#
#   (0,0,0) ─── ARR_1 ──→ (6,0,4)
#               (6,0,4) ─── ARR_2 ──→ (12,0,0)

raw = SapModel.FrameObj.AddByCoord(0.0, 0.0, 0.0, 6.0, 0.0, 4.0,
                                   "", "ARRIOSTRE_HSS", "ARR_1")
assert raw[-1] == 0, f"AddByCoord(ARR_1) failed: {raw[-1]}"
arr1_name = raw[0]

raw = SapModel.FrameObj.AddByCoord(6.0, 0.0, 4.0, 12.0, 0.0, 0.0,
                                   "", "ARRIOSTRE_HSS", "ARR_2")
assert raw[-1] == 0, f"AddByCoord(ARR_2) failed: {raw[-1]}"
arr2_name = raw[0]

# Asignar límite TC: compresión = 0  →  elemento solo-tensión
ret = SapModel.FrameObj.SetTCLimits(
    arr1_name, True, 0.0,   # LimitCompressionExists, LimitCompression=0
    False, 0.0, 0            # LimitTensionExists=False, ItemType=Object
)
assert ret == 0, f"SetTCLimits(ARR_1) failed: {ret}"

ret = SapModel.FrameObj.SetTCLimits(
    arr2_name, True, 0.0, False, 0.0, 0
)
assert ret == 0, f"SetTCLimits(ARR_2) failed: {ret}"

# Verificar asignación (lectura de vuelta) — sin ItemType, 5 args
raw_tc = SapModel.FrameObj.GetTCLimits(arr1_name, False, 0, False, 0)
assert raw_tc[-1] == 0, f"GetTCLimits(ARR_1) failed: {raw_tc[-1]}"

# ─── 7. LOSAS DE PISO (áreas en Z=4) — malla FEM ─────────────────────────────

# SLAB_1: bahía izquierda 6×5 m  →  nodos (0,0,4)-(6,0,4)-(6,5,4)-(0,5,4)
x1 = [0.0, 6.0, 6.0, 0.0]
y1 = [0.0, 0.0, 5.0, 5.0]
z1 = [4.0, 4.0, 4.0, 4.0]
raw = SapModel.AreaObj.AddByCoord(4, x1, y1, z1, "", "LOSA_20", "SLAB_1")
assert raw[-1] == 0, f"AddByCoord(SLAB_1) failed: {raw[-1]}"
slab1_raw_name = raw[3]

# SLAB_2: bahía derecha 6×5 m  →  nodos (6,0,4)-(12,0,4)-(12,5,4)-(6,5,4)
x2 = [6.0,  12.0, 12.0, 6.0]
y2 = [0.0,   0.0,  5.0, 5.0]
z2 = [4.0,   4.0,  4.0, 4.0]
raw = SapModel.AreaObj.AddByCoord(4, x2, y2, z2, "", "LOSA_20", "SLAB_2")
assert raw[-1] == 0, f"AddByCoord(SLAB_2) failed: {raw[-1]}"
slab2_raw_name = raw[3]

# Dividir SLAB_1 en malla 3×2 (18 m² → 6 paneles de 2×2.5 m aprox.)
# 18 args — firma verificada: Name,MeshType,Nout,[],n1,n2,sz1,sz2, 4×bool, Rot,MaxSz, 4×bool
raw = SapModel.EditArea.Divide(
    slab1_raw_name, 1, 0, [], 3, 2,
    0, 0,
    False, False, False, False,
    0, 0,
    False, False, False, False,
)
assert raw[-1] == 0, f"EditArea.Divide(SLAB_1) failed: {raw[-1]}"
slab1_mesh_n   = raw[0]
slab1_mesh_ids = list(raw[1])

# Dividir SLAB_2 en malla 3×2
raw = SapModel.EditArea.Divide(
    slab2_raw_name, 1, 0, [], 3, 2,
    0, 0,
    False, False, False, False,
    0, 0,
    False, False, False, False,
)
assert raw[-1] == 0, f"EditArea.Divide(SLAB_2) failed: {raw[-1]}"
slab2_mesh_n   = raw[0]
slab2_mesh_ids = list(raw[1])

# ─── 8. LOSA DE FUNDACIÓN CON RESORTES WINKLER (Z=0) ─────────────────────────
#
# Placa corrida bajo toda la estructura (12×5 m a Z=0).
# Nota: en un modelo real se elegiría entre apoyos de columna Y resortes;
#       aquí ambos se incluyen para ejercitar todas las funciones API.

xf = [0.0, 12.0, 12.0,  0.0]
yf = [0.0,  0.0,  5.0,  5.0]
zf = [0.0,  0.0,  0.0,  0.0]
raw = SapModel.AreaObj.AddByCoord(4, xf, yf, zf, "", "FUND_60", "FUND_BASE")
assert raw[-1] == 0, f"AddByCoord(FUND_BASE) failed: {raw[-1]}"
fund_name = raw[3]

# Resorte Winkler – cara inferior, solo compresión, ks=30 000 kN/m³
raw_spring = SapModel.AreaObj.SetSpring(
    fund_name,    # Name
    1,            # MyType=1 (Simple)
    30000.0,      # S=30 000 kN/m³ (módulo subrasante típico arena densa)
    1,            # SimpleSpringType=1 (Compression-only)
    "",           # LinkProp (N/A para tipo simple)
    -1,           # Face=-1 (Bottom)
    1,            # SpringLocalOneType=1 (Normal to face)
    1,            # Dir=1 (Local-1)
    False,        # Outward=False
    [0.0, 0.0, 0.0],  # Vec (no usado)
    0.0,          # Ang=0
    True,         # Replace=True
    "Global",     # CSys
    0             # ItemType=Object
)
assert raw_spring[-1] == 0, f"SetSpring(FUND_BASE) failed: {raw_spring[-1]}"

# ─── 9. APOYOS EN BASES DE COLUMNAS (pinned) ──────────────────────────────────

pinned = [True, True, True, False, False, False]   # Ux Uy Uz Rx Ry Rz

base_point_names = []
for tag, col_frm in col_frame_names.items():
    raw_pts = SapModel.FrameObj.GetPoints(col_frm, "", "")
    assert raw_pts[-1] == 0, f"GetPoints({tag}) failed: {raw_pts[-1]}"
    pt_base = raw_pts[0]   # extremo I = base (Z=0)
    base_point_names.append(pt_base)

    raw_rest = SapModel.PointObj.SetRestraint(pt_base, pinned)
    assert raw_rest[-1] == 0, f"SetRestraint({tag} base) failed: {raw_rest[-1]}"

# ─── 10. SELECCIÓN POR RANGO DE COORDENADAS (verificación API) ───────────────
#
# Seleccionar todos los objetos en la banda Z∈[-0.1, 0.1] (nivel ±0 = base)

ret = SapModel.SelectObj.ClearSelection()

# Orden verificado: XMin,XMax,YMin,YMax,ZMin,ZMax, Deselect, CSys
ret_sel = SapModel.SelectObj.CoordinateRange(
    -0.1, 12.1,   # XMin, XMax
    -0.1,  5.1,   # YMin, YMax
    -0.1,  0.1,   # ZMin, ZMax  → slice a nivel Z=0
    False,         # Deselect=False (seleccionar)
    "Global"       # CSys
)
assert ret_sel == 0, f"CoordinateRange(Z=0) failed: {ret_sel}"

raw_sel = SapModel.SelectObj.GetSelected(0, [], [])
assert raw_sel[-1] == 0, f"GetSelected failed: {raw_sel[-1]}"
n_selected_z0 = raw_sel[0]

# ─── 11. DIAFRAGMA RÍGIDO EN NIVEL Z=4 ───────────────────────────────────────
#
# Acopla UX, UY, RZ (DOFs en el plano) → diafragma infinitamente rígido.

dof_diaph = [True, True, False, False, False, True]   # [Ux, Uy, Uz, Rx, Ry, Rz]

raw = SapModel.ConstraintDef.SetBody("DIAPH_Z4", dof_diaph, "Global")
assert raw[-1] == 0, f"ConstraintDef.SetBody(DIAPH_Z4) failed: {raw[-1]}"

# Verificar definición
raw_gb = SapModel.ConstraintDef.GetBody("DIAPH_Z4", [], "")
assert raw_gb[-1] == 0, f"ConstraintDef.GetBody failed: {raw_gb[-1]}"

# Asignar a los nodos en el extremo superior (Z=4) de cada columna
top_point_names = []
for tag, col_frm in col_frame_names.items():
    raw_pts = SapModel.FrameObj.GetPoints(col_frm, "", "")
    pt_top = raw_pts[1]   # extremo J = tope (Z=4)
    top_point_names.append(pt_top)

    raw_sc = SapModel.PointObj.SetConstraint(pt_top, "DIAPH_Z4")
    assert raw_sc[-1] == 0, f"SetConstraint({tag} top) failed: {raw_sc[-1]}"

# ─── 12. PATRONES DE CARGA ────────────────────────────────────────────────────

# PP – Peso Propio (Dead, multiplicador PP=1 → genera caso LinStatic automático)
ret = SapModel.LoadPatterns.Add("PP", 1, 1.0)
assert ret == 0, f"LoadPatterns.Add(PP) failed: {ret}"

# CM – Carga Muerta adicional (SuperDead)
ret = SapModel.LoadPatterns.Add("CM", 2, 0.0)
assert ret == 0, f"LoadPatterns.Add(CM) failed: {ret}"

# CV – Carga Viva (Live)
ret = SapModel.LoadPatterns.Add("CV", 3, 0.0)
assert ret == 0, f"LoadPatterns.Add(CV) failed: {ret}"

# SX – Sismo X (Quake, solo para generación de patrón; caso real = RS_SX)
ret = SapModel.LoadPatterns.Add("SX", 5, 0.0)
assert ret == 0, f"LoadPatterns.Add(SX) failed: {ret}"

# SY – Sismo Y
ret = SapModel.LoadPatterns.Add("SY", 5, 0.0)
assert ret == 0, f"LoadPatterns.Add(SY) failed: {ret}"

# VIENTO – Viento longitudinal (Wind)
ret = SapModel.LoadPatterns.Add("VIENTO", 6, 0.0)
assert ret == 0, f"LoadPatterns.Add(VIENTO) failed: {ret}"

# Verificar lista de patrones
raw_lp = SapModel.LoadPatterns.GetNameList(0, [])
assert raw_lp[-1] == 0, f"LoadPatterns.GetNameList failed: {raw_lp[-1]}"
pattern_names = list(raw_lp[1])

# ─── 13. ESPECTRO DE RESPUESTA NCh2745 ───────────────────────────────────────
#
# Espectro simplificado: Zona Sísmica 3, Tipo de Suelo II
# Sa(T) en unidades de g  (se multiplica por 9.81 en el caso RS)

periods = [0.00, 0.10, 0.15, 0.50, 1.00, 2.00, 4.00]
values  = [0.40, 0.80, 1.00, 1.00, 0.70, 0.35, 0.175]

raw = SapModel.Func.FuncRS.SetUser(
    "RS_NCh2745", len(periods), periods, values, 0.05  # 5% amortiguamiento
)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, f"Func.FuncRS.SetUser failed: {raw}"

# Verificar lectura del espectro
raw_rs = SapModel.Func.FuncRS.GetUser("RS_NCh2745", 0, [], [], 0)
assert raw_rs[-1] == 0, f"Func.FuncRS.GetUser failed: {raw_rs[-1]}"
rs_n_pts = raw_rs[0]

# ─── 14. CASOS DE CARGA ESPECTRAL ────────────────────────────────────────────

# RS_SX – Espectro dirección X (U1), SF=9.81 para convertir g→m/s²
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("RS_SX")
assert ret == 0, f"SetCase(RS_SX) failed: {ret}"

raw = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "RS_SX", 1, ["U1"], ["RS_NCh2745"], [9.81], ["Global"], [0.0]
)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, f"SetLoads(RS_SX) failed: {raw}"

# RS_SY – Espectro dirección Y (U2)
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("RS_SY")
assert ret == 0, f"SetCase(RS_SY) failed: {ret}"

raw = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "RS_SY", 1, ["U2"], ["RS_NCh2745"], [9.81], ["Global"], [0.0]
)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, f"SetLoads(RS_SY) failed: {raw}"

# ─── 15. COMBINACIONES DE CARGA (LRFD / NCh 3171) ────────────────────────────

# COMB1_ULS – Carga gravitacional pura: 1.2·PP + 1.2·CM + 1.6·CV
ret = SapModel.RespCombo.Add("COMB1_ULS", 0)   # 0=LinearAdd
assert ret == 0, f"RespCombo.Add(COMB1_ULS) failed: {ret}"

for caso, sf in [("PP", 1.2), ("CM", 1.2), ("CV", 1.6)]:
    raw = SapModel.RespCombo.SetCaseList("COMB1_ULS", 0, caso, sf)
    assert raw[-1] == 0, f"SetCaseList(COMB1_ULS, {caso}) failed: {raw}"

# COMB2_SX – Gravitacional + Sismo X: 1.0·PP + 1.0·CM + 0.3·CV + 1.0·RS_SX
ret = SapModel.RespCombo.Add("COMB2_SX", 0)
assert ret == 0, f"RespCombo.Add(COMB2_SX) failed: {ret}"

for caso, sf in [("PP", 1.0), ("CM", 1.0), ("CV", 0.3), ("RS_SX", 1.0)]:
    raw = SapModel.RespCombo.SetCaseList("COMB2_SX", 0, caso, sf)
    assert raw[-1] == 0, f"SetCaseList(COMB2_SX, {caso}) failed: {raw}"

# COMB3_SY – Gravitacional + Sismo Y: 1.0·PP + 1.0·CM + 0.3·CV + 1.0·RS_SY
ret = SapModel.RespCombo.Add("COMB3_SY", 0)
assert ret == 0, f"RespCombo.Add(COMB3_SY) failed: {ret}"

for caso, sf in [("PP", 1.0), ("CM", 1.0), ("CV", 0.3), ("RS_SY", 1.0)]:
    raw = SapModel.RespCombo.SetCaseList("COMB3_SY", 0, caso, sf)
    assert raw[-1] == 0, f"SetCaseList(COMB3_SY, {caso}) failed: {raw}"

# ENV_ULS – Envolvente de las tres combinaciones anteriores
ret = SapModel.RespCombo.Add("ENV_ULS", 1)     # 1=Envelope
assert ret == 0, f"RespCombo.Add(ENV_ULS) failed: {ret}"

for combo in ["COMB1_ULS", "COMB2_SX", "COMB3_SY"]:
    raw = SapModel.RespCombo.SetCaseList("ENV_ULS", 1, combo, 1.0)  # CaseType=1=LoadCombo
    assert raw[-1] == 0, f"SetCaseList(ENV_ULS, {combo}) failed: {raw}"

# ─── 16. VERIFICACIÓN FINAL ───────────────────────────────────────────────────

n_frames = SapModel.FrameObj.Count()
n_areas  = SapModel.AreaObj.Count()
n_pts    = SapModel.PointObj.Count()

# Leer combinaciones
raw_cn = SapModel.RespCombo.GetNameList(0, [])
combo_names = list(raw_cn[1]) if raw_cn[-1] == 0 else []

# Leer casos de carga
raw_lc = SapModel.LoadCases.GetNameList(0, [])
case_names = list(raw_lc[1]) if raw_lc[-1] == 0 else []

# Leer secciones de área
raw_asecs = SapModel.PropArea.GetNameList(0, [])
area_sec_names = list(raw_asecs[1]) if raw_asecs[-1] == 0 else []

# ─── RESULTADO ────────────────────────────────────────────────────────────────
result["modelo"]              = "modelo_complejo_mixto"
result["unidades"]            = "kN_m_C"

# Materiales y secciones
result["materiales"]          = ["H30", "A42"]
result["secciones_frame"]     = ["COL_40x40", "VIGA_30x50", "COL_CIRC30",
                                  "ARRIOSTRE_HSS", "VIGA_I_300"]
result["secciones_area"]      = area_sec_names

# Geometría frame
result["columnas"]            = list(col_frame_names.keys())
result["vigas"]               = list(beam_frame_names.keys())
result["arriostres_TC"]       = [arr1_name, arr2_name]
result["n_frames_total"]      = n_frames

# Geometría área
result["losa1_mesh_elementos"]  = slab1_mesh_n
result["losa2_mesh_elementos"]  = slab2_mesh_n
result["losa_fund"]             = fund_name
result["n_areas_total"]         = n_areas

# Nodos y apoyos
result["n_puntos"]              = n_pts
result["apoyos_base_rotula"]    = base_point_names
result["nodos_diafragma_Z4"]    = top_point_names
result["objetos_selec_Z0"]      = n_selected_z0

# Cargas
result["patrones_carga"]        = pattern_names
result["espectro_puntos"]       = rs_n_pts
result["casos_carga"]           = case_names
result["combinaciones"]         = combo_names

result["status"]                = "OK - modelo complejo creado exitosamente"
