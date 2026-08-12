# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        case9_torre_build
# Description: Torre CBF(X)/MRF(Y) 6x4x12 m NCh2369:2025 — construcción completa. Secciones CON FORMA (SetISection/SetTube, legibles en GUI) + modificadores As2/As3 ×1e6 que anulan la deformación por corte (equivale a As=0, iguala elasticBeamColumn de OpenSees a ~5e-8). DampRatio de cada función RS = ξ del caso (evita la re-corrección Newmark-Hall de SAP). Releases, bases mixtas, masa desde cargas, modal 12 modos, espectros por dirección (R* de Ec. 1b con T* del modal), 5 casos RS con CQC.
# Created:     2026-08-12 03:54:23 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"T_star_X": 0.22018507693700515, "T_star_Y": 0.995671904871543, "R_star_X": 3.84953588194975, "R_star_Y": 5.0, "Q0X": 474.87710235070153, "ok": true}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Torre CBF(X)/MRF(Y) — caso 9 de la serie Rukan. NCh2369:2025, zona 3, suelo D, I=1.
# Convenciones: kN-m; secciones CON FORMA (SetISection/SetTube: la GUI muestra doble T y
# cajones) + modificadores de area de corte x1e6, que anulan la deformacion por corte y
# igualan el elasticBeamColumn (Euler-Bernoulli) de OpenSees a ~5e-8 relativo — mismo
# efecto que la convencion As=0 de los casos 5-8, pero con el modelo legible.
# Masa desde cargas (g interno 9.80665); escala RS 9.80665; espectro de diseno por
# direccion con R* constante (Ec. 1b) calculado del T* del modal.
# GOTCHA 1: DampRatio de Func.FuncRS.SetUser = xi del caso (con 0,05 SAP re-corrige por
# Newmark-Hall y duplica el (0,05/xi)^0,4 ya incluido: +22,8% silencioso).
# GOTCHA 2: una seccion SetGeneral se dibuja como circulo generico en la GUI — por eso
# aqui se usan secciones con forma + modificadores, no SetGeneral.
def rc(raw):
    return raw if isinstance(raw, int) else raw[-1]

assert SapModel.InitializeNewModel(6) == 0   # kN_m_C
assert SapModel.File.NewBlank() == 0
assert SapModel.PropMaterial.SetMaterial("A36", 1) == 0
assert SapModel.PropMaterial.SetMPIsotropic("A36", 2.0e8, 0.3, 1.17e-5) == 0
assert rc(SapModel.PropMaterial.SetWeightAndMass("A36", 1, 0.0)) == 0

# Perfiles soldados chilenos por placas (esquina viva; SAP calcula A/I/J de las placas)
assert rc(SapModel.PropFrame.SetISection("HN30", "A36", 0.300, 0.300, 0.016, 0.008, 0.300, 0.016)) == 0
assert rc(SapModel.PropFrame.SetISection("IN30", "A36", 0.300, 0.150, 0.010, 0.006, 0.150, 0.010)) == 0
assert rc(SapModel.PropFrame.SetTube("CAJ125X6", "A36", 0.125, 0.125, 0.006, 0.006)) == 0
assert rc(SapModel.PropFrame.SetTube("CAJ100X4", "A36", 0.100, 0.100, 0.004, 0.004)) == 0

# Deformacion por corte anulada: modificadores As2/As3 grandes.
# Modifiers: [Area, As2, As3, Torsion, I22, I33, Mass, Weight]
MOD = [1.0, 1.0e6, 1.0e6, 1.0, 1.0, 1.0, 1.0, 1.0]
for nm in ["HN30", "IN30", "CAJ125X6", "CAJ100X4"]:
    assert rc(SapModel.PropFrame.SetModifiers(nm, MOD)) == 0

CORNERS = {1: (0.0, 0.0), 2: (6.0, 0.0), 3: (0.0, 4.0), 4: (6.0, 4.0)}
NLEV, DZ = 3, 4.0

def nname(lev, c):
    return f"N{lev}{c}"

for lev in range(0, NLEV + 1):
    for c, (x, y) in CORNERS.items():
        assert rc(SapModel.PointObj.AddCartesian(x, y, lev * DZ, "", nname(lev, c))) == 0
for story in range(1, NLEV + 1):
    for y, tag in ((0.0, "A"), (4.0, "B")):
        assert rc(SapModel.PointObj.AddCartesian(3.0, y, (story - 0.5) * DZ, "", f"C{story}{tag}")) == 0
for lev in range(1, NLEV + 1):
    assert rc(SapModel.PointObj.AddCartesian(3.0, 2.0, lev * DZ, "", f"P{lev}")) == 0

def add_frame(pi, pj, sec, name):
    assert rc(SapModel.FrameObj.AddByPoint(pi, pj, "", sec, name)) == 0, f"AddByPoint {name}"

# Columnas: eje fuerte orientado al plano MRF (Y) -> ejes locales a 90
for c in CORNERS:
    for story in range(1, NLEV + 1):
        nm = f"COL{story}{c}"
        add_frame(nname(story - 1, c), nname(story, c), "HN30", nm)
        assert rc(SapModel.FrameObj.SetLocalAxes(nm, 90.0)) == 0

for lev in range(1, NLEV + 1):
    add_frame(nname(lev, 1), nname(lev, 3), "IN30", f"VMY{lev}A")
    add_frame(nname(lev, 2), nname(lev, 4), "IN30", f"VMY{lev}B")

REL_PIN = [False, False, False, False, True, True]
NOREL = [False] * 6
Z6 = [0.0] * 6

for lev in range(1, NLEV + 1):
    for (ci, cj, tag) in ((1, 2, "A"), (3, 4, "B")):
        nm = f"VPX{lev}{tag}"
        add_frame(nname(lev, ci), nname(lev, cj), "IN30", nm)
        assert rc(SapModel.FrameObj.SetReleases(nm, REL_PIN, REL_PIN, Z6, Z6)) == 0

def add_half_diag(nm, p_col, p_centro, sec):
    add_frame(p_col, p_centro, sec, nm)
    assert rc(SapModel.FrameObj.SetReleases(nm, REL_PIN, NOREL, Z6, Z6)) == 0

for story in range(1, NLEV + 1):
    lo, hi = story - 1, story
    for (ca, cb, tag) in ((1, 2, "A"), (3, 4, "B")):
        cen = f"C{story}{tag}"
        add_half_diag(f"D{story}{tag}1", nname(lo, ca), cen, "CAJ125X6")
        add_half_diag(f"D{story}{tag}2", nname(hi, cb), cen, "CAJ125X6")
        add_half_diag(f"D{story}{tag}3", nname(lo, cb), cen, "CAJ125X6")
        add_half_diag(f"D{story}{tag}4", nname(hi, ca), cen, "CAJ125X6")

for lev in range(1, NLEV + 1):
    for c in CORNERS:
        add_half_diag(f"PB{lev}{c}", nname(lev, c), f"P{lev}", "CAJ100X4")

BASE = [True, True, True, True, False, True]
for c in CORNERS:
    assert rc(SapModel.PointObj.SetRestraint(nname(0, c), BASE)) == 0

P_NIVEL = {1: 325.0, 2: 612.5, 3: 262.5}
assert SapModel.LoadPatterns.Add("PSIS", 3, 0.0, True) == 0
for lev, P in P_NIVEL.items():
    for c in CORNERS:
        assert rc(SapModel.PointObj.SetLoadForce(nname(lev, c), "PSIS", [0.0, 0.0, -P / 4.0, 0.0, 0.0, 0.0])) == 0
assert rc(SapModel.SourceMass.SetMassSource("MASA_P", False, False, True, True, 1, ["PSIS"], [1.0])) == 0

assert rc(SapModel.LoadCases.ModalEigen.SetCase("MODAL")) == 0
assert rc(SapModel.LoadCases.ModalEigen.SetNumberModes("MODAL", 12, 1)) == 0
assert SapModel.File.Save(sap_temp_dir + "\\torre_cbf_mrf.sdb") == 0
assert SapModel.Analyze.RunAnalysis() == 0

assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()) == 0
assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")) == 0
raw = SapModel.Results.ModalPeriod(0, [], [], [], [], [], [])
assert raw[-1] == 0
periods_modal = list(raw[4])
raw = SapModel.Results.ModalParticipatingMassRatios(0, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [])
assert raw[-1] == 0
ux, uy = list(raw[5]), list(raw[6])
T_STAR_X = periods_modal[max(range(len(ux)), key=lambda i: ux[i])]
T_STAR_Y = periods_modal[max(range(len(uy)), key=lambda i: uy[i])]

AR, S, R_PAR, T0, P_PAR, Q_PAR, T1 = 0.56, 1.00, 3.50, 0.60, 1.00, 2.50, 0.41  # Tablas 3 y 6
I_IMP, R_TAB = 1.0, 5.0   # Tabla 7 filas 5.1 y 5.3 (soldadas: xi=0.02)
CRT1 = 0.16 * R_TAB * T1
DAMP020 = (0.05 / 0.02) ** 0.4
DAMP030 = (0.05 / 0.03) ** 0.4

def sah_ref(t):
    if t <= 0:
        return AR * S
    x = t / T0
    return AR * S * (1.0 + R_PAR * x ** P_PAR) / (1.0 + x ** Q_PAR)

def sav_ref(t):
    if t <= 0:
        return 0.7 * AR * S
    x = 1.7 * t / T0
    return 0.7 * AR * S * (1.0 + R_PAR * x ** P_PAR) / (1.0 + x ** Q_PAR)

def r_star(t_star, R):
    if R <= 1:
        return 1.0          # rama impresa en la Ec. (1b)
    if t_star >= CRT1:
        return R
    return 1.5 + (R - 1.5) * t_star / CRT1

RSX = r_star(T_STAR_X, R_TAB)
RSY = r_star(T_STAR_Y, R_TAB)

periods = [round(i * 0.01, 4) for i in range(501)]
assert SapModel.SetModelIsLocked(False) == 0

def set_user(name, vals, damp):
    # DampRatio = xi del caso: la curva YA trae el (0,05/xi)^0,4.
    assert rc(SapModel.Func.FuncRS.SetUser(name, len(periods), periods, vals, damp)) == 0

set_user("SAX_DIS", [I_IMP * sah_ref(t) / RSX * DAMP020 for t in periods], 0.02)
set_user("SAY_DIS", [I_IMP * sah_ref(t) / RSY * DAMP020 for t in periods], 0.02)
set_user("SREF020", [I_IMP * sah_ref(t) * DAMP020 for t in periods], 0.02)
set_user("SAZ_DIS", [I_IMP * sav_ref(t) / 2.0 * DAMP030 for t in periods], 0.03)

G = 9.80665
for name, direc, func, damp in [
    ("RSX_DIS", "U1", "SAX_DIS", 0.02),
    ("RSY_DIS", "U2", "SAY_DIS", 0.02),
    ("RSX_REF", "U1", "SREF020", 0.02),
    ("RSY_REF", "U2", "SREF020", 0.02),
    ("RSZ_DIS", "U3", "SAZ_DIS", 0.03),
]:
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetCase(name)) == 0
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetModalCase(name, "MODAL")) == 0
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetModalComb_1(name, 1)) == 0  # CQC
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetLoads(name, 1, [direc], [func], [G], ["Global"], [0.0])) == 0
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetDampConstant(name, damp)) == 0

assert SapModel.File.Save(sap_temp_dir + "\\torre_cbf_mrf.sdb") == 0
assert SapModel.Analyze.RunAnalysis() == 0

# Verificacion contra las referencias validadas (case09 rukan en verde)
assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()) == 0
assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput("RSX_DIS")) == 0
raw = SapModel.Results.BaseReact(0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0)
assert raw[-1] == 0
q0x = raw[4][0]
assert abs(q0x - 474.8771023518899) / 474.8771023518899 < 1e-6, f"Q0X={q0x}"

result["T_star_X"] = T_STAR_X
result["T_star_Y"] = T_STAR_Y
result["R_star_X"] = RSX
result["R_star_Y"] = RSY
result["Q0X"] = q0x
result["ok"] = True
