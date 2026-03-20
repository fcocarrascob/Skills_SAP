"""
Simple Beam Example

Creates a simply-supported beam with a uniform distributed load,
runs analysis, and extracts the midpoint displacement.

Run via: run_sap_script (expects SapModel, SapObject, result pre-injected)
"""

# ── Initialize ────────────────────────────────────────────────────────

ret = SapModel.InitializeNewModel()
ret = SapModel.File.NewBlank()

# ── Units: kN, m, C ──────────────────────────────────────────────────

ret = SapModel.SetPresentUnits(6)  # kN_m_C

# ── Material: Steel ───────────────────────────────────────────────────

ret = SapModel.PropMaterial.SetMaterial("STEEL", 1)  # 1 = Steel
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL", 200000000, 0.3, 0.0000117)

# ── Section: W310x60 approximated as rectangle ───────────────────────

ret = SapModel.PropFrame.SetRectangle("BEAM_SECT", "STEEL", 0.302, 0.203)

# ── Create beam: 6m span along X ─────────────────────────────────────

ret = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SECT", "1")
beam_name = ret[0] if isinstance(ret, (list, tuple)) else "1"  # ByRef Name is raw[0]

# ── Supports ──────────────────────────────────────────────────────────

# Get end points
raw = SapModel.FrameObj.GetPoints(beam_name, "", "")
pt_i = raw[0]  # pt_i is raw[0]
pt_j = raw[1]  # pt_j is raw[1]
# raw[-1] is ret_code

# Pin at left end (all translations fixed)
ret = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])

# Roller at right end (Uy and Uz fixed)
ret = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])

# ── Load ──────────────────────────────────────────────────────────────

# Add a live load pattern
ret = SapModel.LoadPatterns.Add("LIVE", 3)  # 3 = Live

# Uniform distributed load: 10 kN/m downward (gravity projected)
ret = SapModel.FrameObj.SetLoadDistributed(beam_name, "LIVE", 1, 10, 0, 1, 10, 10)

# ── Analysis ──────────────────────────────────────────────────────────

ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# ── Results ───────────────────────────────────────────────────────────

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("LIVE")

# Get displacement at both joints to check
# JointDispl: raw[-1]=ret_code, raw[8]=U3[]
for pt_name, label in [(pt_i, "left"), (pt_j, "right")]:
    raw = SapModel.Results.JointDispl(
        pt_name, 0, 0, [], [], [], [], [], [], [], [], [], []
    )
    if raw[-1] == 0 and len(raw[8]) > 0:
        result[f"U3_{label}"] = raw[8][0]

result["beam_name"] = beam_name
result["span_m"] = 6.0
result["load_kN_per_m"] = 10.0
result["num_frames"] = SapModel.FrameObj.Count()
result["num_points"] = SapModel.PointObj.Count()

print(f"Simple beam created: span = 6m, load = 10 kN/m")
print(f"Frames: {result['num_frames']}, Points: {result['num_points']}")
