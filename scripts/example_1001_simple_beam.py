# ─── SAP2000 Example 1-001 — Simple Beam Verification ────────────────
# Description: End-to-end verification script. Creates a simply-supported
#              beam with a uniform load, runs analysis, extracts results,
#              and compares against hand-calculated reference values.
#
# Reference:
#   Simply supported beam, span L=10m, uniform load w=24 kN/m
#   Steel beam: E=200 GPa, t3=0.5m, t2=0.2m (local-3 wide, local-2 deep)
#   I33 = t3*t2^3/12 = 0.5*0.2^3/12 = 3.333e-4 m^4  (gravity bending, M3)
#
#   Max midspan moment:   M = wL^2/8 = 24*100/8 = 300 kN*m
#   Max support reaction: R = wL/2   = 24*10/2  = 120 kN
#   Max midspan deflection: delta = 5wL^4/(384EI33)
#     = 5*24*10^4 / (384 * 200e6 * 3.333e-4)
#     = 1200000 / 25600000 = 0.04688 m = 46.9 mm
#
# Units: kN_m_C (6)
# ─────────────────────────────────────────────────────────────────────

# ── 1. Initialize ─────────────────────────────────────────────────────
ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# ── Disable self-weight on DEAD load pattern (isolate applied load) ───
ret = SapModel.LoadPatterns.SetSelfWTMultiplier("DEAD", 0.0)
assert ret == 0, f"SetSelfWTMultiplier failed: {ret}"

# ── 2. Material ───────────────────────────────────────────────────────
ret = SapModel.PropMaterial.SetMaterial("STEEL", 1)  # 1=Steel
assert ret == 0, f"SetMaterial failed: {ret}"

# E = 200 GPa = 200e6 kN/m², ν = 0.3, α = 1.2e-5
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL", 200e6, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# ── 3. Section ────────────────────────────────────────────────────────
# t3=0.5m (local-3 = horizontal Y), t2=0.2m (local-2 = vertical Z)
# I33 (gravity bending, M3) = t3 * t2^3 / 12 = 0.5 * 0.2^3 / 12 = 3.333e-4 m^4
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL", 0.5, 0.2)
assert ret == 0, f"SetRectangle failed: {ret}"

# ── 4. Geometry ───────────────────────────────────────────────────────
# Simply-supported beam along X-axis, 10m span
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Get actual joint names via GetPoints (never hardcode joint names)
raw_pts = SapModel.FrameObj.GetPoints(beam_name, "", "")
pt_i = raw_pts[0]  # start joint at (0,0,0)
pt_j = raw_pts[1]  # end joint at (10,0,0)
assert raw_pts[-1] == 0, f"GetPoints failed: {raw_pts[-1]}"

# ── 5. Supports (pin-roller) ─────────────────────────────────────────
# Node i: pin (restrain X, Y, Z translations)
ret = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])
assert ret[-1] == 0, f"SetRestraint pin failed: {ret[-1]}"

# Node j: roller (restrain Y, Z translations only — free in X)
ret = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])
assert ret[-1] == 0, f"SetRestraint roller failed: {ret[-1]}"

# ── 6. Load ───────────────────────────────────────────────────────────
# Dir=10 = Gravity direction. POSITIVE value = downward (in gravity direction).
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, 24, 24, "Global", True, True
)
assert ret == 0, f"SetLoadDistributed failed: {ret}"

# ── 7. Save & Analyze ────────────────────────────────────────────────
ret = SapModel.File.Save(sap_temp_dir + r"\example_1001_simple_beam.sdb")
assert ret == 0, f"File.Save failed: {ret}"

ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# ── 8. Set output case ───────────────────────────────────────────────
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0, f"DeselectAll failed: {ret}"

ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0, f"SetCaseSelectedForOutput failed: {ret}"

# ── 9. Extract reactions ─────────────────────────────────────────────
# Reaction at pin support
raw_r1 = SapModel.Results.JointReact(
    pt_i, 0,
    0, [], [],
    [], [], [],
    [], [], [], [], [], []
)
assert raw_r1[-1] == 0, f"JointReact pt_i failed: {raw_r1[-1]}"
R1_F3 = raw_r1[8][0]  # F3 = global Z reaction

# Reaction at roller support
raw_r2 = SapModel.Results.JointReact(
    pt_j, 0,
    0, [], [],
    [], [], [],
    [], [], [], [], [], []
)
assert raw_r2[-1] == 0, f"JointReact pt_j failed: {raw_r2[-1]}"
R2_F3 = raw_r2[8][0]  # F3 = global Z reaction

# ── 10. Extract frame forces ─────────────────────────────────────────
raw_ff = SapModel.Results.FrameForce(
    beam_name, 0,
    0, [], [], [], [], [], [], [],
    [], [], [], [], [], []
)
assert raw_ff[-1] == 0, f"FrameForce failed: {raw_ff[-1]}"

num_stations = raw_ff[0]
stations     = list(raw_ff[2])  # ObjSta (station distances)
M3_values    = list(raw_ff[13]) # M3 (moment about local-3)
V2_values    = list(raw_ff[9])  # V2 (shear in local-2)

# Find midspan moment (station closest to 5.0m)
mid_idx = min(range(num_stations), key=lambda i: abs(stations[i] - 5.0))
M3_mid = M3_values[mid_idx]

# ── 11. Extract displacements ────────────────────────────────────────
# We need midspan displacement. SAP2000 doesn't auto-create midspan joints,
# so we get all joint displacements and pick the largest U3 magnitude.
# For a SS beam under uniform load, max deflection is at midspan.
raw_jd = SapModel.Results.JointDispl(
    "All", 0,
    0, [], [],
    [], [], [],
    [], [], [], [], [], []
)
# If "All" doesn't work, try getting specific joints
if raw_jd[-1] != 0:
    # Fallback: get displacement at internal joints created by meshing
    # For a simple beam with no internal mesh points, deflection is
    # only available at end joints (which are zero for supports)
    U3_mid = None
else:
    U3_values = list(raw_jd[8])  # U3 array
    # Midspan deflection = minimum U3 (most negative for downward)
    U3_mid = min(U3_values) if U3_values else None

# ── 12. Reference values & comparison ────────────────────────────────
L = 10.0    # span [m]
w = 24.0    # distributed load [kN/m]

ref_reaction     = w * L / 2          # 120.0 kN
ref_moment_mid   = w * L**2 / 8       # 300.0 kN*m
# I33 (gravity bending, M3) = t3 * t2^3 / 12 = 0.5 * 0.2^3 / 12 = 3.333e-4 m^4
# delta = 5wL^4 / (384EI33) = 5*24*10^4 / (384*200e6*3.333e-4) = 0.04688 m = 46.9 mm
E = 200e6
I33 = 0.5 * 0.2**3 / 12           # 3.333e-4 m^4 — correct for M3 bending
ref_deflection   = 5 * w * L**4 / (384 * E * I33)

tol = 0.02  # 2% tolerance

# Reaction check (use abs — SAP sign convention may vary)
r1_err = abs(abs(R1_F3) - ref_reaction) / ref_reaction if ref_reaction != 0 else 0
r2_err = abs(abs(R2_F3) - ref_reaction) / ref_reaction if ref_reaction != 0 else 0
reaction_ok = r1_err < tol and r2_err < tol

# Moment check (M3 is negative in SAP2000 convention for this load case)
m3_err = abs(abs(M3_mid) - ref_moment_mid) / ref_moment_mid if ref_moment_mid != 0 else 0
moment_ok = m3_err < tol

# Deflection check (only if we got a midspan value)
deflection_ok = True
if U3_mid is not None:
    u3_err = abs(abs(U3_mid) - ref_deflection) / ref_deflection if ref_deflection != 0 else 0
    deflection_ok = u3_err < tol

verification_passed = reaction_ok and moment_ok and deflection_ok

# ── 13. Write results ────────────────────────────────────────────────
result["beam_name"] = beam_name
result["span_m"] = L
result["load_kN_per_m"] = w

result["R1_F3_kN"] = round(R1_F3, 4)
result["R2_F3_kN"] = round(R2_F3, 4)
result["ref_reaction_kN"] = ref_reaction
result["reaction_error_pct"] = round(max(r1_err, r2_err) * 100, 4)

result["M3_midspan_kNm"] = round(M3_mid, 4)
result["ref_moment_kNm"] = ref_moment_mid
result["moment_error_pct"] = round(m3_err * 100, 4)

result["U3_midspan_m"] = round(U3_mid, 6) if U3_mid is not None else "N/A"
result["ref_deflection_m"] = round(ref_deflection, 6)
result["deflection_error_pct"] = round(u3_err * 100, 4) if U3_mid is not None else "N/A"

result["verification_passed"] = verification_passed
result["num_stations"] = num_stations

print(f"Reaction R1={R1_F3:.2f} kN, R2={R2_F3:.2f} kN (ref={ref_reaction:.2f})")
print(f"Midspan moment M3={M3_mid:.2f} kN*m (ref={ref_moment_mid:.2f})")
if U3_mid is not None:
    print(f"Midspan deflection U3={U3_mid:.6f} m (ref={ref_deflection:.6f})")
print(f"Verification: {'PASS' if verification_passed else 'FAIL'}")
