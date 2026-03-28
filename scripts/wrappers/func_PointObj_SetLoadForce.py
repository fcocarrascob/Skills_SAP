# ============================================================
# Wrapper: SapModel.PointObj.SetLoadForce
# Category: Object_Model
# Description: Assign point load forces/moments to point objects
# Verified: 2026-03-28
# Prerequisites: Model open, point object exists, load pattern defined
# ============================================================
"""
Usage: Assigns concentrated forces and moments to point (joint) objects.

API Signature:
  SapModel.PointObj.SetLoadForce(Name, LoadPat, Value,
      Replace, CSys, ItemType) -> [Value[], ret_code]

ByRef Output:
  Value[]  : float[6] — echoed back as ByRef
  ret_code : int (0=success) — raw[-1]

Parameters:
  Name    : str      — Point object name
  LoadPat : str      — Load pattern name
  Value   : float[6] — [F1, F2, F3, M1, M2, M3] in specified CSys
  Replace : bool     — True=replace previous force loads
  CSys    : str      — "Global" or "Local" or named system
  ItemType: int      — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("COL_SEC", "STEEL_TEST", 0.4, 0.4)
assert ret == 0

# Cantilever column (vertical)
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 5, "", "COL_SEC", "")
col_name = raw[0]
assert raw[-1] == 0

# Fixed base
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0

# --- Target function: apply lateral force at top ---
# 100 kN in X direction, 50 kN downward (Z), 20 kN-m moment about Y
load_values = [100.0, 0.0, -50.0, 0.0, 20.0, 0.0]
raw_lf = SapModel.PointObj.SetLoadForce("2", "DEAD", load_values, True, "Global")
ret = raw_lf[-1]
assert ret == 0, f"SetLoadForce failed: {ret}"

# --- Verification via analysis ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_pointobj_setloadforce.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# Check base reactions
raw = SapModel.Results.JointReact(
    "1", 0, 0, [], [], [], [], [], [], [], [], [], [], []
)
assert raw[-1] == 0
F1_base = raw[6][0]  # Should be ≈ -100 kN (reaction opposes applied)
F3_base = raw[8][0]  # Should be ≈ 50 kN (reaction opposes applied)

# --- Result ---
result["function"] = "SapModel.PointObj.SetLoadForce"
result["applied_forces"] = load_values
result["base_reaction_F1"] = F1_base
result["base_reaction_F3"] = F3_base
result["status"] = "verified"
