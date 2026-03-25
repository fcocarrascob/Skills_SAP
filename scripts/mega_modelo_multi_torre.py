# ═══════════════════════════════════════════════════════════════════════════════
# Script: mega_modelo_multi_torre.py
# Description: Mega estructura mixta — Complejo multi-torre con puente peatonal
#              y rampa helicoidal. Combina hormigón armado, acero estructural,
#              elementos frame y de área, análisis sísmico espectral y extracción
#              de resultados para demostrar el alcance completo de la API SAP2000.
#
# Componentes modelados:
#   TORRE A — Pórtico de H.A. 3×3 columnas, 3 pisos (Z=0,4,8,12 m)
#     - 27 columnas rectangulares COL_50x50 (H30)
#     - Vigas VIGA_30x60 en ambas direcciones por nivel
#     - Arriostres tubulares HSS200x10 tension-only (Cruz de San Andrés)
#     - Muro de corte MURO_25 en eje X=6
#     - Losas LOSA_20 malladas 3×2 (FEM)
#
#   TORRE B — Pórtico octagonal de acero, 2 pisos (Z=0,4,8 m)
#     - 8 columnas circulares COL_CIRC350 (A36) en geometría octagonal
#     - Vigas perimetrales + diagonales HEB300
#     - Losas poligonales LOSA_20 (8 vértices)
#     - Rampa helicoidal con perfiles BARANDA (R=6.5m, 16 segmentos)
#
#   PODIO COMERCIAL — Nivel único Z=4m, 3×3 columnas, entre torres
#     - Columnas COL_40x40 (H30), evitando conflicto con Torre A
#     - Vigas VIGA_25x50 en ambas direcciones
#     - Losas LOSA_20
#
#   PUENTE PEATONAL — Z=8m, conecta Torre A con Torre B
#     - Vigas longitudinales + transversales IPE400 (A36)
#     - Deck triangular de conexión DECK_15
#
#   FUNDACIONES
#     - Losa fundación FA bajo Torre A (FUND_80, H50)
#     - Losa fundación FP bajo Podio  (FUND_80, H50)
#     - Losa fundación FB octagonal bajo Torre B (FUND_80, H50)
#     - Resortes Winkler kz=40000 kN/m³ en todas las fundaciones
#
#   ANÁLISIS
#     - Apoyos articulados (pinned) en bases de columnas
#     - Diafragmas rígidos por nivel: DA0,DA1,DA2 (Torre A) + DB0,DB1 (Torre B)
#     - Patrones: PP, CM, CV, CV_T, SX, SY, VIENTO, NIEVE
#     - Espectro NCh2745 Zona 3 Suelo II — 13 puntos
#     - Casos espectrales: RS_SX (U1) y RS_SY (U2)
#     - Combinaciones LRFD: C1_GRAV, C2_SX, C3_SY, C4_WIND, C5_UPLIFT, C6_SNOW
#     - Envolvente: ENV_ULS
#
# Funciones API usadas: 39
# Units: kN, m, °C  (código 6)
# Status:  ✓ Verificado (ejecutado exitosamente)
# Created: 2026-03-24
# ═══════════════════════════════════════════════════════════════════════════════

# NOTE: `math` está pre-inyectado por el sandbox — no usar `import math`

# ─── RUTA DE GUARDADO ─────────────────────────────────────────────────────────
# Ajustar según el equipo donde se ejecute
SAVE_PATH = r"C:\Users\fcoca\Desktop\Ingenieria\Proyectos_Python\Skills_SAP\scripts\MEGA_MODELO_MULTI_TORRE.sdb"

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 1: GENERACIÓN DEL MODELO
# ═══════════════════════════════════════════════════════════════════════════════

# ─── 0. INIT ──────────────────────────────────────────────────────────────────
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0, "SetPresentUnits"

# ─── 1. MATERIALES ────────────────────────────────────────────────────────────
# (nombre, tipo, E [kN/m²], ν, α [1/°C], γ [kN/m³])
for mat, tp, E, nu, al, w in [
    ("H30", 2, 25e6,  0.2,  1e-5,   25.0),   # Hormigón H30
    ("A36", 1, 200e6, 0.3,  1.2e-5, 78.5),   # Acero A36
    ("H50", 2, 35e6,  0.2,  1e-5,   25.0),   # Hormigón H50 (fundaciones)
]:
    ret = SapModel.PropMaterial.SetMaterial(mat, tp)
    assert ret == 0, f"SetMaterial({mat})"
    ret = SapModel.PropMaterial.SetMPIsotropic(mat, E, nu, al)
    assert ret == 0, f"IsotropicErr({mat})"
    ret = SapModel.PropMaterial.SetWeightAndMass(mat, 1, w)
    assert ret == 0, f"W({mat})"
    ret = SapModel.PropMaterial.SetWeightAndMass(mat, 2, w / 9.81)
    assert ret == 0, f"M({mat})"

# ─── 2. SECCIONES FRAME ───────────────────────────────────────────────────────
ret = SapModel.PropFrame.SetRectangle("COL_50x50",  "H30", 0.50, 0.50); assert ret == 0, "COL_50x50"
ret = SapModel.PropFrame.SetRectangle("VIGA_30x60", "H30", 0.60, 0.30); assert ret == 0, "VIGA_30x60"
ret = SapModel.PropFrame.SetCircle(   "COL_CIRC350","A36", 0.35);        assert ret == 0, "COL_CIRC350"
ret = SapModel.PropFrame.SetISection( "HEB300", "A36", 0.30, 0.30, 0.019, 0.011, 0.30, 0.019); assert ret == 0, "HEB300"
ret = SapModel.PropFrame.SetISection( "IPE400", "A36", 0.40, 0.18, 0.0135, 0.0086, 0.18, 0.0135); assert ret == 0, "IPE400"
ret = SapModel.PropFrame.SetTube(     "HSS200x10","A36", 0.20, 0.20, 0.010, 0.010); assert ret == 0, "HSS200x10"
ret = SapModel.PropFrame.SetRectangle("COL_40x40",  "H30", 0.40, 0.40); assert ret == 0, "COL_40x40"
ret = SapModel.PropFrame.SetRectangle("VIGA_25x50", "H30", 0.50, 0.25); assert ret == 0, "VIGA_25x50"
ret = SapModel.PropFrame.SetCircle(   "BARANDA",    "A36", 0.05);        assert ret == 0, "BARANDA"

# ─── 3. SECCIONES ÁREA ────────────────────────────────────────────────────────
# (nombre, tipo_shell, tiene_membrana, material, ángulo, t_membrana, t_flexión)
ret = SapModel.PropArea.SetShell_1("LOSA_20", 1, True, "H30", 0, 0.20, 0.20); assert ret == 0, "LOSA_20"
ret = SapModel.PropArea.SetShell_1("MURO_25", 1, True, "H30", 0, 0.25, 0.25); assert ret == 0, "MURO_25"
ret = SapModel.PropArea.SetShell_1("FUND_80", 2, True, "H50", 0, 0.80, 0.80); assert ret == 0, "FUND_80"
ret = SapModel.PropArea.SetShell_1("DECK_15", 1, True, "H30", 0, 0.15, 0.15); assert ret == 0, "DECK_15"

# ═══════════════════════════════════════════════════════════════════════════════
# ── TORRE A — Pórtico H.A. 3×3, 3 pisos ──────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
#
#   Y=10 |  (0,10) ─── (6,10) ─── (12,10)
#        |     |           |           |
#   Y=5  |  (0, 5) ─── (6, 5) ─── (12, 5)
#        |     |           |           |
#   Y=0  |  (0, 0) ─── (6, 0) ─── (12, 0)
#             0       6       12   → X
#

TA_X = [0.0, 6.0, 12.0]
TA_Y = [0.0, 5.0, 10.0]
TA_Z = [0.0, 4.0, 8.0, 12.0]
TA_COL_SET = {(x, y) for x in TA_X for y in TA_Y}

# ── Columnas Torre A ──────────────────────────────────────────────────────────
tA_cols = {}; tA_base = {}; tA_top = {}
for iz in range(len(TA_Z) - 1):
    for ix, x in enumerate(TA_X):
        for iy, y in enumerate(TA_Y):
            raw = SapModel.FrameObj.AddByCoord(x, y, TA_Z[iz], x, y, TA_Z[iz + 1],
                                               "", "COL_50x50", f"tAc{ix}{iy}{iz}")
            assert raw[-1] == 0, f"tAc{ix}{iy}{iz}"
            tA_cols[(ix, iy, iz)] = raw[0]
            rp = SapModel.FrameObj.GetPoints(raw[0], "", "")
            assert rp[-1] == 0, f"GP tAc{ix}{iy}{iz}"
            tA_top[(ix, iy, iz)] = rp[1]
            if iz == 0:
                tA_base[(ix, iy)] = rp[0]

# ── Vigas Torre A ─────────────────────────────────────────────────────────────
tA_beams = {}
for iz in range(1, len(TA_Z)):
    z = TA_Z[iz]
    # Dirección X
    for iy, y in enumerate(TA_Y):
        for ix in range(len(TA_X) - 1):
            tag = f"tAbx{ix}{iy}{iz}"
            raw = SapModel.FrameObj.AddByCoord(TA_X[ix], y, z, TA_X[ix + 1], y, z,
                                               "", "VIGA_30x60", tag)
            assert raw[-1] == 0, f"beam {tag}"
            tA_beams[tag] = raw[0]
    # Dirección Y
    for ix, x in enumerate(TA_X):
        for iy in range(len(TA_Y) - 1):
            tag = f"tAby{ix}{iy}{iz}"
            raw = SapModel.FrameObj.AddByCoord(x, TA_Y[iy], z, x, TA_Y[iy + 1], z,
                                               "", "VIGA_30x60", tag)
            assert raw[-1] == 0, f"beam {tag}"
            tA_beams[tag] = raw[0]

# ── Arriostres tension-only HSS (Cruz de San Andrés en cara Y=0) ──────────────
tA_braces = []
for iz in range(len(TA_Z) - 1):
    zb, zt = TA_Z[iz], TA_Z[iz + 1]
    for ix in range(len(TA_X) - 1):
        x1, x2 = TA_X[ix], TA_X[ix + 1]
        for xs, xe, zs, ze in [(x1, x2, zb, zt), (x2, x1, zb, zt)]:
            raw = SapModel.FrameObj.AddByCoord(xs, 0, zs, xe, 0, ze, "", "HSS200x10", "")
            assert raw[-1] == 0, f"brace ({xs},{ze})"
            ret = SapModel.FrameObj.SetTCLimits(raw[0], True, 0.0, False, 0.0, 0)
            assert ret == 0, f"TC {raw[0]}"
            tA_braces.append(raw[0])

# ── Muros de corte en X=6 ─────────────────────────────────────────────────────
walls = []
for iz in range(len(TA_Z) - 1):
    zb, zt = TA_Z[iz], TA_Z[iz + 1]
    raw = SapModel.AreaObj.AddByCoord(4, [6, 6, 6, 6], [3, 7, 7, 3], [zb, zb, zt, zt],
                                      "", "MURO_25", f"wX6_{iz}")
    assert raw[-1] == 0, f"wall {iz}"
    walls.append(raw[3])

# ── Losas Torre A ─────────────────────────────────────────────────────────────
tA_slabs = []
for iz in range(1, len(TA_Z)):
    z = TA_Z[iz]
    for ix in range(len(TA_X) - 1):
        for iy in range(len(TA_Y) - 1):
            xs = [TA_X[ix], TA_X[ix + 1], TA_X[ix + 1], TA_X[ix]]
            ys = [TA_Y[iy], TA_Y[iy],     TA_Y[iy + 1], TA_Y[iy + 1]]
            raw = SapModel.AreaObj.AddByCoord(4, xs, ys, [z] * 4,
                                              "", "LOSA_20", f"tAs{ix}{iy}{iz}")
            assert raw[-1] == 0, f"slab tAs{ix}{iy}{iz}"
            tA_slabs.append(raw[3])

# ═══════════════════════════════════════════════════════════════════════════════
# ── TORRE B — Pórtico octagonal de acero, 2 pisos ────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
#
#   Centro: (30, 5),  Radio=5m,  8 nodos octagonales
#   Piso 1: Z=4m  |  Piso 2: Z=8m
#   Rampa helicoidal exterior: R=6.5m, 16 segmentos de Z=0 a Z=4m

TB_CX, TB_CY, TB_R, NS = 30.0, 5.0, 5.0, 8
TB_Z = [0.0, 4.0, 8.0]

# Vértices octagonales (sentido antihorario desde ángulo π/2)
oct_pts = []
for i in range(NS):
    a = math.pi / 2 + 2 * math.pi * i / NS
    oct_pts.append((round(TB_CX + TB_R * math.cos(a), 4),
                    round(TB_CY + TB_R * math.sin(a), 4)))

# ── Columnas Torre B ──────────────────────────────────────────────────────────
tB_cols = {}; tB_base = {}; tB_top = {}
for iz in range(len(TB_Z) - 1):
    for iv, (x, y) in enumerate(oct_pts):
        raw = SapModel.FrameObj.AddByCoord(x, y, TB_Z[iz], x, y, TB_Z[iz + 1],
                                           "", "COL_CIRC350", f"tBc{iv}{iz}")
        assert raw[-1] == 0, f"tBc{iv}{iz}"
        tB_cols[(iv, iz)] = raw[0]
        rp = SapModel.FrameObj.GetPoints(raw[0], "", "")
        assert rp[-1] == 0, f"GP tBc{iv}{iz}"
        tB_top[(iv, iz)] = rp[1]
        if iz == 0:
            tB_base[iv] = rp[0]

# ── Vigas perimetrales + diagonales Torre B ───────────────────────────────────
tB_beams = {}
for iz in range(1, len(TB_Z)):
    z = TB_Z[iz]
    # Vigas perimetrales (anillo)
    for iv in range(NS):
        x1, y1 = oct_pts[iv]
        x2, y2 = oct_pts[(iv + 1) % NS]
        tag = f"tBr{iv}{iz}"
        raw = SapModel.FrameObj.AddByCoord(x1, y1, z, x2, y2, z, "", "HEB300", tag)
        assert raw[-1] == 0, f"tBr{iv}{iz}"
        tB_beams[tag] = raw[0]
    # Vigas diagonales (diámetros del octágono)
    for iv in range(NS // 2):
        x1, y1 = oct_pts[iv]
        x2, y2 = oct_pts[iv + NS // 2]
        tag = f"tBd{iv}{iz}"
        raw = SapModel.FrameObj.AddByCoord(x1, y1, z, x2, y2, z, "", "HEB300", tag)
        assert raw[-1] == 0, f"tBd{iv}{iz}"
        tB_beams[tag] = raw[0]

# ── Losas octagonales Torre B ─────────────────────────────────────────────────
tB_slabs = []
for iz in range(1, len(TB_Z)):
    z = TB_Z[iz]
    xs = [p[0] for p in oct_pts]
    ys = [p[1] for p in oct_pts]
    raw = SapModel.AreaObj.AddByCoord(NS, xs, ys, [z] * NS, "", "LOSA_20", f"tBs{iz}")
    assert raw[-1] == 0, f"tBs{iz}"
    tB_slabs.append(raw[3])

# ── Rampa helicoidal (R=6.5m, 16 segmentos, Z=0→4m) ─────────────────────────
RAMP_R, RAMP_N = 6.5, 16
ramp_frames = []
for i in range(RAMP_N):
    a1 = 2 * math.pi * i / RAMP_N
    a2 = 2 * math.pi * (i + 1) / RAMP_N
    x1 = round(TB_CX + RAMP_R * math.cos(a1), 4)
    y1 = round(TB_CY + RAMP_R * math.sin(a1), 4)
    z1 = round(4.0 * i / RAMP_N, 4)
    x2 = round(TB_CX + RAMP_R * math.cos(a2), 4)
    y2 = round(TB_CY + RAMP_R * math.sin(a2), 4)
    z2 = round(4.0 * (i + 1) / RAMP_N, 4)
    raw = SapModel.FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, "", "BARANDA", f"RM{i}")
    assert raw[-1] == 0, f"RM{i}"
    ramp_frames.append(raw[0])

# ═══════════════════════════════════════════════════════════════════════════════
# ── PODIO COMERCIAL — Nivel único Z=4m ───────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
#
#   Grid 3×3 entre Torre A y Torre B (X=12→20, Y=2→8)
#   Columnas que coinciden con Torre A se omiten (nodo compartido)

POD_X = [12.0, 16.0, 20.0]
POD_Y = [2.0, 5.0, 8.0]

pod_cols = {}; pod_base = {}
for ix, x in enumerate(POD_X):
    for iy, y in enumerate(POD_Y):
        if (x, y) in TA_COL_SET:
            continue  # Nodo compartido con Torre A — no duplicar columna
        raw = SapModel.FrameObj.AddByCoord(x, y, 0, x, y, 4, "", "COL_40x40", f"pc{ix}{iy}")
        assert raw[-1] == 0, f"pc{ix}{iy} at ({x},{y})"
        pod_cols[f"pc{ix}{iy}"] = raw[0]
        rp = SapModel.FrameObj.GetPoints(raw[0], "", "")
        assert rp[-1] == 0, f"GP pc{ix}{iy}"
        pod_base[f"pc{ix}{iy}"] = rp[0]

pod_beams = {}
for iy, y in enumerate(POD_Y):
    for ix in range(len(POD_X) - 1):
        tag = f"pbx{ix}{iy}"
        raw = SapModel.FrameObj.AddByCoord(POD_X[ix], y, 4, POD_X[ix + 1], y, 4,
                                           "", "VIGA_25x50", tag)
        assert raw[-1] == 0, f"pod beam {tag}"
        pod_beams[tag] = raw[0]
for ix, x in enumerate(POD_X):
    for iy in range(len(POD_Y) - 1):
        tag = f"pby{ix}{iy}"
        raw = SapModel.FrameObj.AddByCoord(x, POD_Y[iy], 4, x, POD_Y[iy + 1], 4,
                                           "", "VIGA_25x50", tag)
        assert raw[-1] == 0, f"pod beam {tag}"
        pod_beams[tag] = raw[0]

pod_slabs = []
for ix in range(len(POD_X) - 1):
    for iy in range(len(POD_Y) - 1):
        xs = [POD_X[ix], POD_X[ix + 1], POD_X[ix + 1], POD_X[ix]]
        ys = [POD_Y[iy], POD_Y[iy],     POD_Y[iy + 1], POD_Y[iy + 1]]
        raw = SapModel.AreaObj.AddByCoord(4, xs, ys, [4.0] * 4, "", "LOSA_20", f"ps{ix}{iy}")
        assert raw[-1] == 0, f"pod slab ps{ix}{iy}"
        pod_slabs.append(raw[3])

# ═══════════════════════════════════════════════════════════════════════════════
# ── PUENTE PEATONAL — Z=8m, conecta Torre A con Torre B ──────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
#
#   Tramo recto: X=12→21, Y∈{4,6}  (IPE400 longitudinales + transversales)
#   Tramo V:     (21,4)→(25,5) y (21,6)→(25,5)  (convergencia hacia Torre B)

BR_Z    = 8.0
BR_X_PAR = [12.0, 15.0, 18.0, 21.0]

bridge_beams = {}
# Vigas longitudinales (cuerdas Y=4 e Y=6)
for iy, y in enumerate([4.0, 6.0]):
    for ix in range(len(BR_X_PAR) - 1):
        tag = f"brl{ix}{iy}"
        raw = SapModel.FrameObj.AddByCoord(BR_X_PAR[ix], y, BR_Z,
                                           BR_X_PAR[ix + 1], y, BR_Z, "", "IPE400", tag)
        assert raw[-1] == 0, f"bridge {tag}"
        bridge_beams[tag] = raw[0]

# Vigas V de convergencia hacia Torre B
for tag, ys in [("brv0", 4.0), ("brv1", 6.0)]:
    raw = SapModel.FrameObj.AddByCoord(21, ys, BR_Z, 25, 5, BR_Z, "", "IPE400", tag)
    assert raw[-1] == 0, f"bridge {tag}"
    bridge_beams[tag] = raw[0]

# Vigas transversales (costillas)
for x in BR_X_PAR:
    tag = f"brc{int(x)}"
    raw = SapModel.FrameObj.AddByCoord(x, 4, BR_Z, x, 6, BR_Z, "", "IPE400", tag)
    assert raw[-1] == 0, f"bridge {tag}"
    bridge_beams[tag] = raw[0]

bridge_slabs = []
for ix in range(len(BR_X_PAR) - 1):
    xs = [BR_X_PAR[ix], BR_X_PAR[ix + 1], BR_X_PAR[ix + 1], BR_X_PAR[ix]]
    ys = [4, 4, 6, 6]
    raw = SapModel.AreaObj.AddByCoord(4, xs, ys, [BR_Z] * 4, "", "DECK_15", f"bds{ix}")
    assert raw[-1] == 0, f"bridge deck {ix}"
    bridge_slabs.append(raw[3])

# Deck triangular de convergencia
raw = SapModel.AreaObj.AddByCoord(3, [21, 21, 25], [4, 6, 5], [BR_Z] * 3, "", "DECK_15", "bdv")
assert raw[-1] == 0, "bridge V-deck"
bridge_slabs.append(raw[3])

# ═══════════════════════════════════════════════════════════════════════════════
# ── FUNDACIONES + RESORTES WINKLER ───────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
fund_names = []

raw = SapModel.AreaObj.AddByCoord(4, [0, 12, 12, 0],  [0, 0, 10, 10], [0] * 4, "", "FUND_80", "FA")
assert raw[-1] == 0, "fund A"
fund_names.append(raw[3])

raw = SapModel.AreaObj.AddByCoord(4, [12, 20, 20, 12], [2, 2, 8, 8],   [0] * 4, "", "FUND_80", "FP")
assert raw[-1] == 0, "fund P"
fund_names.append(raw[3])

xs_f = [p[0] for p in oct_pts]
ys_f = [p[1] for p in oct_pts]
raw = SapModel.AreaObj.AddByCoord(NS, xs_f, ys_f, [0] * NS, "", "FUND_80", "FB")
assert raw[-1] == 0, "fund B"
fund_names.append(raw[3])

# Resortes Winkler kz=40000 kN/m³ en todas las losas de fundación
for fn in fund_names:
    raw = SapModel.AreaObj.SetSpring(fn, 1, 40000.0, 1, "", -1, 1, 1, False, [0, 0, 0], 0, True, "Global", 0)
    assert raw[-1] == 0, f"spring {fn}"

# ─── Mesh de losas primer piso Torre A (3×2) ──────────────────────────────────
meshed = 0
for sn in tA_slabs[:4]:
    raw = SapModel.EditArea.Divide(sn, 1, 0, [], 3, 2, 0, 0,
                                   False, False, False, False, 0, 0,
                                   False, False, False, False)
    assert raw[-1] == 0, f"mesh {sn}"
    meshed += raw[0]

# ─── Apoyos articulados (pinned) en bases de columnas ─────────────────────────
pinned = [True, True, True, False, False, False]
for pt in list(tA_base.values()) + list(tB_base.values()) + list(pod_base.values()):
    rr = SapModel.PointObj.SetRestraint(pt, pinned)
    ret = rr[-1] if isinstance(rr, (list, tuple)) else rr
    assert ret == 0, f"restraint {pt}"

# ─── Diafragmas rígidos por nivel ─────────────────────────────────────────────
# DOF activos: UX, UY, RZ (traslación horizontal + rotación vertical)
dof_d = [True, True, False, False, False, True]

for iz in range(len(TA_Z) - 1):
    dn = f"DA{iz}"
    raw = SapModel.ConstraintDef.SetBody(dn, dof_d, "Global")
    assert raw[-1] == 0, f"body {dn}"
    for ix in range(len(TA_X)):
        for iy in range(len(TA_Y)):
            pt = tA_top.get((ix, iy, iz))
            if pt:
                rc = SapModel.PointObj.SetConstraint(pt, dn)
                assert rc[-1] == 0, f"const {dn} {pt}"

for iz in range(len(TB_Z) - 1):
    dn = f"DB{iz}"
    raw = SapModel.ConstraintDef.SetBody(dn, dof_d, "Global")
    assert raw[-1] == 0, f"body {dn}"
    for iv in range(NS):
        pt = tB_top.get((iv, iz))
        if pt:
            rc = SapModel.PointObj.SetConstraint(pt, dn)
            assert rc[-1] == 0, f"const {dn} {pt}"

# ─── Patrones de carga ────────────────────────────────────────────────────────
# (nombre, tipo SAP2000, peso propio multiplicador)
for name, typ, sw in [
    ("PP",     1, 1.0),   # Peso propio
    ("CM",     2, 0),     # Carga muerta adicional
    ("CV",     3, 0),     # Carga viva
    ("CV_T",   4, 0),     # Carga viva de techo
    ("SX",     5, 0),     # Sísmica X (estática)
    ("SY",     5, 0),     # Sísmica Y (estática)
    ("VIENTO", 6, 0),     # Viento
    ("NIEVE",  7, 0),     # Nieve
]:
    ret = SapModel.LoadPatterns.Add(name, typ, sw)
    assert ret == 0, f"LP {name}"

# ─── Asignación de cargas ─────────────────────────────────────────────────────
# CM + CV en vigas horizontales Torre A
for tag, bn in tA_beams.items():
    if "bx" in tag:
        ret = SapModel.FrameObj.SetLoadDistributed(bn, "CM", 1, 10, 0, 1, 1.5, 1.5)
        assert ret == 0, f"CM {tag}"
        ret = SapModel.FrameObj.SetLoadDistributed(bn, "CV", 1, 10, 0, 1, 3.0, 3.0)
        assert ret == 0, f"CV {tag}"

# Viento en columnas frontales (cara Y=0) Torre A
for iz in range(len(TA_Z) - 1):
    for ix in range(len(TA_X)):
        cn = tA_cols.get((ix, 0, iz))
        if cn:
            ret = SapModel.FrameObj.SetLoadDistributed(cn, "VIENTO", 1, 5, 0, 1, 2.0, 2.0)
            assert ret == 0, f"wind {cn}"

# Carga puntual de nieve en nodo central último piso Torre A
center_top = tA_top.get((1, 1, 2))
if center_top:
    FV = [0, 0, -30.0, 0, 0, 0]
    rr = SapModel.PointObj.SetLoadForce(center_top, "NIEVE", FV)
    ret = rr[-1] if isinstance(rr, (list, tuple)) else rr
    assert ret == 0, "snow force"

# CM en vigas Podio
for tag, bn in pod_beams.items():
    if "bx" in tag:
        ret = SapModel.FrameObj.SetLoadDistributed(bn, "CM", 1, 10, 0, 1, 2.0, 2.0)
        assert ret == 0, f"pod CM {tag}"

# CV en vigas longitudinales del Puente
for tag, bn in bridge_beams.items():
    if "brl" in tag:
        ret = SapModel.FrameObj.SetLoadDistributed(bn, "CV", 1, 10, 0, 1, 5.0, 5.0)
        assert ret == 0, f"br CV {tag}"

# ─── Espectro NCh2745 Zona 3, Suelo II ───────────────────────────────────────
periods = [0.0,  0.05, 0.1, 0.15, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0,  4.0,  5.0]
values  = [0.4,  0.6,  0.8, 1.0,  1.0, 1.0, 0.8,  0.6, 0.4, 0.3, 0.2,  0.15, 0.12]

raw = SapModel.Func.FuncRS.SetUser("RS_NCh2745", len(periods), periods, values, 0.05)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, "RS func"

# ─── Casos de respuesta espectral ────────────────────────────────────────────
for case, dof in [("RS_SX", "U1"), ("RS_SY", "U2")]:
    ret = SapModel.LoadCases.ResponseSpectrum.SetCase(case)
    assert ret == 0, f"RS case {case}"
    raw = SapModel.LoadCases.ResponseSpectrum.SetLoads(
        case, 1, [dof], ["RS_NCh2745"], [9.81], ["Global"], [0.0])
    ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
    assert ret == 0, f"RS loads {case}"

# ─── Combinaciones LRFD ───────────────────────────────────────────────────────
combos_def = [
    ("C1_GRAV",   0, [("PP", 1.2), ("CM", 1.2), ("CV", 1.6)]),
    ("C2_SX",     0, [("PP", 1.0), ("CM", 1.0), ("CV", 0.3), ("RS_SX", 1.0)]),
    ("C3_SY",     0, [("PP", 1.0), ("CM", 1.0), ("CV", 0.3), ("RS_SY", 1.0)]),
    ("C4_WIND",   0, [("PP", 1.0), ("CM", 1.0), ("CV", 0.5), ("VIENTO", 1.0)]),
    ("C5_UPLIFT", 0, [("PP", 0.9), ("RS_SX", 1.0)]),
    ("C6_SNOW",   0, [("PP", 1.2), ("CM", 1.2), ("NIEVE", 1.6)]),
]
for cn, ct, cases in combos_def:
    ret = SapModel.RespCombo.Add(cn, ct)
    assert ret == 0, f"combo {cn}"
    for caso, sf in cases:
        raw = SapModel.RespCombo.SetCaseList(cn, 0, caso, sf)
        assert raw[-1] == 0, f"CL {cn}/{caso}"

# Envolvente ULS
ret = SapModel.RespCombo.Add("ENV_ULS", 1)
assert ret == 0, "ENV_ULS"
for cn, _, _ in combos_def:
    raw = SapModel.RespCombo.SetCaseList("ENV_ULS", 1, cn, 1.0)
    assert raw[-1] == 0, f"ENV/{cn}"

# ─── Selección por rango de coordenadas (verificación) ────────────────────────
ret = SapModel.SelectObj.ClearSelection()
ret_sel = SapModel.SelectObj.CoordinateRange(-0.1, 12.1, -0.1, 10.1, -0.1, 0.1, False, "Global")
assert ret_sel == 0, "sel range"
raw_sel = SapModel.SelectObj.GetSelected(0, [], [])
n_sel = raw_sel[0] if raw_sel[-1] == 0 else 0
ret = SapModel.SelectObj.ClearSelection()

# ─── Conteos pre-análisis ─────────────────────────────────────────────────────
n_frames = SapModel.FrameObj.Count()
n_areas  = SapModel.AreaObj.Count()
n_pts    = SapModel.PointObj.Count()

raw_lp = SapModel.LoadPatterns.GetNameList(0, [])
pats = list(raw_lp[1]) if raw_lp[-1] == 0 else []
raw_lc = SapModel.LoadCases.GetNameList(0, [])
lc = list(raw_lc[1]) if raw_lc[-1] == 0 else []
raw_rc = SapModel.RespCombo.GetNameList(0, [])
cbn = list(raw_rc[1]) if raw_rc[-1] == 0 else []
raw_as = SapModel.PropArea.GetNameList(0, [])
asn = list(raw_as[1]) if raw_as[-1] == 0 else []
raw_rs = SapModel.Func.FuncRS.GetUser("RS_NCh2745", 0, [], [], 0)
rs_n = raw_rs[0] if raw_rs[-1] == 0 else 0

SapModel.View.RefreshView(0, False)

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 2: GUARDAR MODELO, EJECUTAR ANÁLISIS, EXTRAER RESULTADOS
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Guardar modelo ───────────────────────────────────────────────────────────
ret = SapModel.File.Save(SAVE_PATH)
assert ret == 0, f"File.Save failed: {ret}"

# ─── Ejecutar análisis ────────────────────────────────────────────────────────
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# ─── Extracción de resultados ─────────────────────────────────────────────────

# PP — Desplazamientos de nodos
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("PP")
raw = SapModel.Results.JointDispl("ALL", 2, 0, [], [], [], [], [], [], [], [], [], [])
if raw[-1] == 0 and raw[0] > 0:
    U3 = list(raw[8]); U1 = list(raw[6]); U2 = list(raw[7])
    min_U3 = min(U3); min_idx = U3.index(min_U3)
    result["PP"] = {
        "n":             raw[0],
        "max_down_U3_mm": round(min_U3 * 1000, 3),
        "worst_joint":   raw[1][min_idx],
        "max_U1_mm":     round(max(abs(v) for v in U1) * 1000, 3),
        "max_U2_mm":     round(max(abs(v) for v in U2) * 1000, 3),
    }

# VIENTO — Derivas laterales
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("VIENTO")
raw = SapModel.Results.JointDispl("ALL", 2, 0, [], [], [], [], [], [], [], [], [], [])
if raw[-1] == 0 and raw[0] > 0:
    U2 = list(raw[7]); mx = max(abs(v) for v in U2)
    mi = [abs(v) for v in U2].index(mx)
    result["VIENTO"] = {"max_drift_U2_mm": round(mx * 1000, 3), "worst_joint": raw[1][mi]}

# RS_SX — Desplazamientos espectrales en X
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("RS_SX")
raw = SapModel.Results.JointDispl("ALL", 2, 0, [], [], [], [], [], [], [], [], [], [])
if raw[-1] == 0 and raw[0] > 0:
    U1 = list(raw[6]); mx = max(abs(v) for v in U1)
    mi = [abs(v) for v in U1].index(mx)
    result["RS_SX"] = {
        "max_U1_mm":    round(mx * 1000, 3),
        "worst_joint":  raw[1][mi],
        "max_U3_mm":    round(max(abs(v) for v in raw[8]) * 1000, 3),
    }

# PP — Fuerzas en viga Torre A
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("PP")
raw_ff = SapModel.Results.FrameForce(
    "tAbx001", 0,
    0, [], [], [], [], [], [], [], [], [], [], [], [], []
)
if raw_ff[-1] == 0 and raw_ff[0] > 0:
    M3 = list(raw_ff[13]); V2 = list(raw_ff[9]); Px = list(raw_ff[8])
    result["beam_PP"] = {
        "beam":        "tAbx001",
        "stations":    raw_ff[0],
        "max_M3_kNm":  round(max(abs(v) for v in M3), 2),
        "max_V2_kN":   round(max(abs(v) for v in V2), 2),
        "max_P_kN":    round(max(abs(v) for v in Px), 2),
    }

# PP — Reacciones en bases
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("PP")
raw_r = SapModel.Results.JointReact("ALL", 2, 0, [], [], [], [], [], [], [], [], [], [])
if raw_r[-1] == 0 and raw_r[0] > 0:
    Fz = list(raw_r[8])
    result["reactions_PP"] = {
        "n":           raw_r[0],
        "total_Fz_kN": round(sum(Fz), 2),
        "max_Fz_kN":   round(max(abs(v) for v in Fz), 2),
    }

# ENV_ULS — Envolvente de desplazamientos
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetComboSelectedForOutput("ENV_ULS")
raw_e = SapModel.Results.JointDispl("ALL", 2, 0, [], [], [], [], [], [], [], [], [], [])
if raw_e[-1] == 0 and raw_e[0] > 0:
    result["ENV_ULS"] = {
        "n":          raw_e[0],
        "max_U1_mm":  round(max(abs(v) for v in raw_e[6]) * 1000, 3),
        "max_U2_mm":  round(max(abs(v) for v in raw_e[7]) * 1000, 3),
        "max_U3_mm":  round(max(abs(v) for v in raw_e[8]) * 1000, 3),
    }

# ─── Resultado final ──────────────────────────────────────────────────────────
result["modelo"]          = "MEGA_ESTRUCTURA_MIXTA_MULTI_TORRE"
result["unidades"]        = "kN_m_C"
result["materiales"]      = ["H30", "A36", "H50"]
result["secc_frame"]      = ["COL_50x50", "VIGA_30x60", "COL_CIRC350", "HEB300",
                             "IPE400", "HSS200x10", "COL_40x40", "VIGA_25x50", "BARANDA"]
result["secc_area"]       = asn
result["torre_A"]         = {"cols": len(tA_cols), "vigas": len(tA_beams),
                             "braces_TC": len(tA_braces), "muros": len(walls),
                             "losas": len(tA_slabs)}
result["torre_B"]         = {"cols": len(tB_cols), "vigas": len(tB_beams),
                             "losas": len(tB_slabs), "rampa_seg": len(ramp_frames)}
result["podio"]           = {"cols": len(pod_cols), "vigas": len(pod_beams),
                             "losas": len(pod_slabs)}
result["puente"]          = {"vigas": len(bridge_beams), "deck": len(bridge_slabs)}
result["fundaciones"]     = fund_names
result["mesh_panels"]     = meshed
result["diafragmas"]      = ["DA0", "DA1", "DA2", "DB0", "DB1"]
result["n_frames"]        = n_frames
result["n_areas"]         = n_areas
result["n_puntos"]        = n_pts
result["seleccion_Z0"]    = n_sel
result["patrones"]        = pats
result["casos_carga"]     = lc
result["combinaciones"]   = cbn
result["espectro_pts"]    = rs_n
result["n_funciones_API"] = 39
result["save_path"]       = SAVE_PATH
result["status"]          = "OK — MEGA MODELO CREADO, ANALIZADO Y RESULTADOS EXTRAÍDOS"
