"""
SAP2000 Verification Example 1-001

Port of the official SAP2000 Example 1-001 verification problem.
Creates a model from scratch, runs analysis, extracts results, and
compares with hand-calculated values.

Run via: run_sap_script (this script expects SapModel, SapObject, result pre-injected)
"""

# ── Step 1: Initialize model ──────────────────────────────────────────

ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

# ── Step 2: Define material ───────────────────────────────────────────

ret = SapModel.PropMaterial.SetMaterial("CONC", 2)  # 2 = Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2, 0.0000055)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# ── Step 3: Define frame section ──────────────────────────────────────

ret = SapModel.PropFrame.SetRectangle("R1", "CONC", 12, 12)
assert ret == 0, f"SetRectangle failed: {ret}"

# Set section modifiers: Area=1000, AS2=0, AS3=0, rest=1
ModValue = [1000, 0, 0, 1, 1, 1, 1, 1]
ret = SapModel.PropFrame.SetModifiers("R1", ModValue)
assert ret == 0, f"SetModifiers failed: {ret}"

# ── Step 4: Switch to kip-ft units ────────────────────────────────────

ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# ── Step 5: Create geometry ───────────────────────────────────────────

# Frame 1: Column (0,0,0) → (0,0,10)
ret1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, "", "R1", "1")
FrameName0 = ret1[1] if isinstance(ret1, tuple) else ""

# Frame 2: Inclined beam (0,0,10) → (8,0,16)
ret2 = SapModel.FrameObj.AddByCoord(0, 0, 10, 8, 0, 16, "", "R1", "2")
FrameName1 = ret2[1] if isinstance(ret2, tuple) else ""

# Frame 3: Cantilever (-4,0,10) → (0,0,10)
ret3 = SapModel.FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10, "", "R1", "3")
FrameName2 = ret3[1] if isinstance(ret3, tuple) else ""

# ── Step 6: Set restraints ────────────────────────────────────────────

# Base of column: fixed (Ux, Uy, Uz, Rx free Ry, Rz)
ret = SapModel.FrameObj.GetPoints(FrameName0, "", "")
BasePt = ret[1]
Restraint_base = [True, True, True, True, False, False]
ret = SapModel.PointObj.SetRestraint(BasePt, Restraint_base)
assert ret == 0, f"SetRestraint(base) failed: {ret}"

# Top of inclined beam: roller (Ux, Uy)
ret = SapModel.FrameObj.GetPoints(FrameName1, "", "")
TopPt = ret[2]
Restraint_top = [True, True, False, False, False, False]
ret = SapModel.PointObj.SetRestraint(TopPt, Restraint_top)
assert ret == 0, f"SetRestraint(top) failed: {ret}"

# ── Step 7: Refresh view ──────────────────────────────────────────────

ret = SapModel.View.RefreshView(0, False)

# ── Step 8: Add load patterns ─────────────────────────────────────────

ret = SapModel.LoadPatterns.Add("1", 8, 1)   # type=8 (Other), selfweight=1
ret = SapModel.LoadPatterns.Add("2", 8)
ret = SapModel.LoadPatterns.Add("3", 8)
ret = SapModel.LoadPatterns.Add("4", 8)
ret = SapModel.LoadPatterns.Add("5", 8)
ret = SapModel.LoadPatterns.Add("6", 8)
ret = SapModel.LoadPatterns.Add("7", 8)

# ── Step 9: Assign loads ──────────────────────────────────────────────

# Load pattern 2: point load + distributed load on cantilever
ret = SapModel.FrameObj.GetPoints(FrameName2, "", "")
CantPt_i = ret[1]
PointLoadValue_2 = [0, 0, -10, 0, 0, 0]
ret = SapModel.PointObj.SetLoadForce(CantPt_i, "2", PointLoadValue_2)
ret = SapModel.FrameObj.SetLoadDistributed(FrameName2, "2", 1, 10, 0, 1, 1.8, 1.8)

# Load pattern 3: point load at end of inclined beam
ret = SapModel.FrameObj.GetPoints(FrameName2, "", "")
CantPt_j = ret[2]  # This is the junction point
PointLoadValue_3 = [0, 0, -17.2, 0, -54.4, 0]
ret = SapModel.PointObj.SetLoadForce(CantPt_j, "3", PointLoadValue_3)

# Load pattern 4: distributed load on inclined beam
ret = SapModel.FrameObj.SetLoadDistributed(FrameName1, "4", 1, 11, 0, 1, 2, 2)

# Load pattern 5: local distributed loads
ret = SapModel.FrameObj.SetLoadDistributed(FrameName0, "5", 1, 2, 0, 1, 2, 2, "Local")
ret = SapModel.FrameObj.SetLoadDistributed(FrameName1, "5", 1, 2, 0, 1, -2, -2, "Local")

# Load pattern 6: trapezoidal local loads
ret = SapModel.FrameObj.SetLoadDistributed(
    FrameName0, "6", 1, 2, 0, 1, 0.9984, 0.3744, "Local"
)
ret = SapModel.FrameObj.SetLoadDistributed(
    FrameName1, "6", 1, 2, 0, 1, -0.3744, 0, "Local"
)

# Load pattern 7: point load at midspan of inclined beam
ret = SapModel.FrameObj.SetLoadPoint(FrameName1, "7", 1, 2, 0.5, -15, "Local")

# ── Step 10: Switch to kip-in and save ────────────────────────────────

ret = SapModel.SetPresentUnits(3)  # kip_in_F

# ── Step 11: Run analysis ─────────────────────────────────────────────

ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# ── Step 12: Extract results ──────────────────────────────────────────

# Get endpoint of inclined beam for vertical displacement results
ret = SapModel.FrameObj.GetPoints(FrameName1, "", "")
ResultPt_beam = ret[2]

# Get I-end of column for horizontal displacement results
ret = SapModel.FrameObj.GetPoints(FrameName0, "", "")
ResultPt_col = ret[1]

SapResult = []
for i in range(7):
    ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    ret = SapModel.Results.Setup.SetCaseSelectedForOutput(str(i + 1))

    if i <= 3:
        # Vertical displacement at beam end
        ret = SapModel.Results.JointDispl(
            ResultPt_beam, 0,
            0, [], [], [], [], [], [], [], [], [], []
        )
        if ret[0] == 0 and len(ret[9]) > 0:
            SapResult.append(ret[9][0])  # U3
        else:
            SapResult.append(None)
    else:
        # Horizontal displacement at column base
        ret = SapModel.Results.JointDispl(
            ResultPt_col, 0,
            0, [], [], [], [], [], [], [], [], [], []
        )
        if ret[0] == 0 and len(ret[7]) > 0:
            SapResult.append(ret[7][0])  # U1
        else:
            SapResult.append(None)

# ── Step 13: Compare with reference values ────────────────────────────

IndResult = [
    -0.02639,   # LC1: vertical displacement
     0.06296,   # LC2
     0.06296,   # LC3
    -0.02639,   # LC4
     0.06296,   # LC5
     0.06296,   # LC6
     0.06296,   # LC7
]

result["sap_values"] = SapResult
result["reference_values"] = IndResult
result["load_cases"] = list(range(1, 8))

# Calculate percent difference
percent_diff = []
for sap_val, ref_val in zip(SapResult, IndResult):
    if sap_val is not None and ref_val != 0:
        diff = (sap_val / ref_val) - 1
        percent_diff.append(round(diff * 100, 2))
    else:
        percent_diff.append(None)

result["percent_diff"] = percent_diff
result["all_pass"] = all(
    d is not None and abs(d) < 1.0  # within 1%
    for d in percent_diff
)

print("Example 1-001 Verification Results:")
print(f"{'LC':<4} {'SAP2000':<12} {'Reference':<12} {'%Diff':<8}")
for i in range(7):
    sap_str = f"{SapResult[i]:.5f}" if SapResult[i] is not None else "N/A"
    ref_str = f"{IndResult[i]:.5f}"
    diff_str = f"{percent_diff[i]:.2f}%" if percent_diff[i] is not None else "N/A"
    print(f"{i+1:<4} {sap_str:<12} {ref_str:<12} {diff_str:<8}")

print(f"\nAll within 1%: {result['all_pass']}")
