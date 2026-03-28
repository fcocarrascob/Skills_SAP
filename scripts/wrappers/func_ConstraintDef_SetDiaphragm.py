# ============================================================
# Wrapper: SapModel.ConstraintDef.SetDiaphragm
# Category: Constraints
# Description: Define a diaphragm constraint (rigid floor)
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates or modifies a diaphragm constraint. Diaphragms model rigid
       floor slabs where in-plane translations and rotation are coupled.
       Most common constraint for multi-story buildings.

API Signature:
  SapModel.ConstraintDef.SetDiaphragm(Name, Axis, CSys) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Constraint name (creates new if not exists)
  Axis : int — Perpendicular axis: 1=X, 2=Y, 3=Z, 4=AutoAxis (default)
  CSys : str — Coordinate system (default "Global")
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: create diaphragm constraints ---
# Z-axis perpendicular = horizontal floor diaphragm (most common)
ret = SapModel.ConstraintDef.SetDiaphragm("DIAPH_FLOOR1", 3, "Global")
assert ret == 0, f"SetDiaphragm(FLOOR1) failed: {ret}"

# Auto-axis (let SAP2000 determine from joint positions)
ret = SapModel.ConstraintDef.SetDiaphragm("DIAPH_FLOOR2", 4, "Global")
assert ret == 0, f"SetDiaphragm(FLOOR2) failed: {ret}"

# --- Create points and assign diaphragm ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0

raw = SapModel.PointObj.AddCartesian(0, 0, 3, "", "PT1")
assert raw[-1] == 0
raw = SapModel.PointObj.AddCartesian(5, 0, 3, "", "PT2")
assert raw[-1] == 0
raw = SapModel.PointObj.AddCartesian(5, 5, 3, "", "PT3")
assert raw[-1] == 0
raw = SapModel.PointObj.AddCartesian(0, 5, 3, "", "PT4")
assert raw[-1] == 0

for pt in ["PT1", "PT2", "PT3", "PT4"]:
    ret = SapModel.PointObj.SetConstraint(pt, "DIAPH_FLOOR1")
    assert ret[-1] == 0, f"SetConstraint({pt}) failed: {ret[-1]}"

# --- Verification via GetDiaphragm ---
raw = SapModel.ConstraintDef.GetDiaphragm("DIAPH_FLOOR1", 0, "")
ret_code = raw[-1]
assert ret_code == 0, f"GetDiaphragm failed: {ret_code}"
axis = raw[0]
csys = raw[1]

# --- Result ---
result["function"] = "SapModel.ConstraintDef.SetDiaphragm"
result["constraints"] = ["DIAPH_FLOOR1", "DIAPH_FLOOR2"]
result["axis_read"] = axis
result["csys_read"] = csys
result["points_assigned"] = ["PT1", "PT2", "PT3", "PT4"]
result["status"] = "verified"
