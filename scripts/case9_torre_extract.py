# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        case9_torre_extract
# Description: Torre CBF/MRF caso 9 — extracción de referencias: períodos y masas participantes, cortes basales CQC de los 5 casos RS (diseño X/Y, referencia X/Y, vertical), desplazamientos por nivel del nodo esquina, axiales de medias diagonales del piso 1 y P/M3 de base de columna del MRF. Requiere el modelo de case9_torre_build ya corrido.
# Created:     2026-08-12 01:56:13 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"periods": [0.9956718610259325, 0.3773198547254338, 0.2693380143954706, 0.22018507693652134, 0.1406833613427464, 0.13913695750363383, 0.10267683083068724, 0.07432103783404385, 0.06815490625974083, 0.05786183341839765, 0.05690707068346983, 0.05436326258464669], "Ux": [0.0, 0.0, 0.0, 0.891008, 0.0, 0.0, 0.0, 0.081315, 0.0, 0.0, 0.0, 0.0], "Uy": [0.871135, 0.0, 0.080152, 0.0, 0.048709, 0.0, 0.0, 0.0, 0.0, 0.0, 4e-06, 0.0], "Uz": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.934752, 0.0, 0.0], "SumUx": 0.9723226715049605, "SumUy": 0.9999995435124162, "base": {"RSX_DIS": {"Fx": 582.9906453170968, "Fy": 1.3703426954718387e-07, "Fz": 2.393121230279933e-05}, "RSY_DIS": {"Fx": 2.4094690216424454e-07, "Fy": 314.17190827196936, "Fz": 2.233620602531146e-06}, "RSX_REF": {"Fx": 2244.2434079861932, "Fy": 5.275183376779505e-07, "Fz": 9.21240604580598e-05}, "RSY_REF": {"Fx": 1.2047345108212231e-06, "Fy": 1570.8595413598466, "Fz": 1.1168103012655728e-05}, "RSZ_DIS": {"Fx": 3.23644059760886e-05, "Fy": 1.1749545552165408e-06, "Fz": 473.1010488644882}}, "despl_m": {"RSX_DIS": {"n1": 0.0030490242136742823, "n2": 0.00627351328113446, "n3": 0.008288570901537364}, "RSX_REF": {"n1": 0.01173732811545703, "n2": 0.02415011448158302, "n3": 0.03190715109550987}, "RSY_DIS": {"n1": 0.027553875263344598, "n2": 0.06908056482228885, "n3": 0.09617566064392422}, "RSY_REF": {"n1": 0.13776937631672295, "n2": 0.3454028241114442, "n3": 0.48087830321962094}}, "diag_P_kN_RSX": {"D1A1": 175.39092479598338, "D1A2": 175.35061298402755, "D1A3": 175.39092444182205, "D1A4": 175.35061263440508}, "col11_P_kN": 214.49310263316838, "col11_M3_base_kNm": 246.7023994776849, "ok": true}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Extraccion de referencias del caso 9 (modelo de case9_torre_build ya analizado).
def rc(raw):
    return raw if isinstance(raw, int) else raw[-1]

def solo_caso(name):
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()) == 0
    assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput(name)) == 0

solo_caso("MODAL")
raw = SapModel.Results.ModalPeriod(0, [], [], [], [], [], [])
assert raw[-1] == 0
result["periods"] = list(raw[4])
raw = SapModel.Results.ModalParticipatingMassRatios(0, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [])
assert raw[-1] == 0
result["Ux"] = [round(v, 6) for v in raw[5]]
result["Uy"] = [round(v, 6) for v in raw[6]]
result["Uz"] = [round(v, 6) for v in raw[7]]
result["SumUx"] = list(raw[8])[-1]
result["SumUy"] = list(raw[9])[-1]

bases = {}
for caso in ["RSX_DIS", "RSY_DIS", "RSX_REF", "RSY_REF", "RSZ_DIS"]:
    solo_caso(caso)
    raw = SapModel.Results.BaseReact(0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0)
    assert raw[-1] == 0
    bases[caso] = {"Fx": raw[4][0], "Fy": raw[5][0], "Fz": raw[6][0]}
result["base"] = bases

despl = {}
for caso, idx in [("RSX_DIS", 6), ("RSX_REF", 6), ("RSY_DIS", 7), ("RSY_REF", 7)]:
    solo_caso(caso)
    u = {}
    for lev in (1, 2, 3):
        raw = SapModel.Results.JointDispl(f"N{lev}1", 0, 0, [], [], [], [], [], [], [], [], [], [])
        assert raw[-1] == 0
        u[f"n{lev}"] = raw[idx][0]
    despl[caso] = u
result["despl_m"] = despl

solo_caso("RSX_DIS")
diag = {}
for nm in ["D1A1", "D1A2", "D1A3", "D1A4"]:
    raw = SapModel.Results.FrameForce(nm, 0, 0, [], [], [], [], [], [], [], [], [], [], [], [])
    assert raw[-1] == 0
    diag[nm] = raw[8][0]
result["diag_P_kN_RSX"] = diag

solo_caso("RSY_DIS")
raw = SapModel.Results.FrameForce("COL11", 0, 0, [], [], [], [], [], [], [], [], [], [], [], [])
assert raw[-1] == 0
result["col11_P_kN"] = raw[8][0]
result["col11_M3_base_kNm"] = raw[13][0]
result["ok"] = True
