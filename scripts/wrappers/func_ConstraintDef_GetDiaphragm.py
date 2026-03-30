# ============================================================
# Wrapper: SapModel.ConstraintDef.GetDiaphragm
# Category: Constraints
# Description: Retrieve diaphragm constraint definition
# Verified: 2026-03-28
# Prerequisites: Model open, diaphragm constraint defined
# ============================================================
"""
Usage: Retrieves the axis and coordinate system for a diaphragm constraint.

API Signature:
  SapModel.ConstraintDef.GetDiaphragm(Name, Axis, CSys) ->
      [Axis, CSys, ret_code]

ByRef Output:
  Axis : int — 1=X, 2=Y, 3=Z, 4=AutoAxis
  CSys : str — Coordinate system name

Parameters:
  Name : str — Name of existing diaphragm constraint
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Create diaphragms with known axes
ret = SapModel.ConstraintDef.SetDiaphragm("DIAPH_Z", 3, "Global")
assert ret == 0
ret = SapModel.ConstraintDef.SetDiaphragm("DIAPH_AUTO", 4, "Global")
assert ret == 0

# --- Target function ---
raw = SapModel.ConstraintDef.GetDiaphragm("DIAPH_Z", 0, "")
ret_code = raw[-1]
assert ret_code == 0, f"GetDiaphragm(Z) failed: {ret_code}"
axis_z = raw[0]
csys_z = raw[1]
assert axis_z == 3, f"Expected axis=3(Z), got {axis_z}"

raw = SapModel.ConstraintDef.GetDiaphragm("DIAPH_AUTO", 0, "")
ret_code = raw[-1]
assert ret_code == 0, f"GetDiaphragm(AUTO) failed: {ret_code}"
axis_auto = raw[0]
assert axis_auto == 4, f"Expected axis=4(Auto), got {axis_auto}"

# --- Result ---
result["function"] = "SapModel.ConstraintDef.GetDiaphragm"
result["diaph_z_axis"] = axis_z
result["diaph_z_csys"] = csys_z
result["diaph_auto_axis"] = axis_auto
result["status"] = "verified"
