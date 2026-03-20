# ============================================================
# Wrapper: SapModel.PointObj.SetRestraint
# Category: Object_Model
# Description: Assign translational and rotational restraints to a joint
# Verified: 2026-03-20
# Prerequisites: Model open, at least one point object exists
# ============================================================
"""
Usage: Sets support restraints (boundary conditions) on a joint point.
       The restraint is a 6-element boolean array [Ux, Uy, Uz, Rx, Ry, Rz].

API Signature:
  SapModel.PointObj.SetRestraint(Name, Value, ItemType)

ByRef Output:
  raw[0]  = Value (bool[6] — echoed back)
  raw[-1] = ret_code (0=success)

Parameters:
  Name     : str        — Name of the point object
  Value    : bool[6]    — [Ux, Uy, Uz, Rx, Ry, Rz] True=fixed, False=free
  ItemType : int        — 0=Object (default), 1=Group, 2=SelectedObjects
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, section, and a frame to get points ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)  # 1=Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "SEC_TEST", "")
frame_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Get endpoint names
raw = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i = raw[0]
pt_j = raw[1]
assert raw[-1] == 0, f"GetPoints failed: {raw[-1]}"

# --- Target function: pin at left, roller at right ---
# Pin: all translations fixed, all rotations free
raw = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])
assert raw[-1] == 0, f"SetRestraint(pin) failed: {raw[-1]}"

# Roller: only Uy and Uz fixed
raw = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])
assert raw[-1] == 0, f"SetRestraint(roller) failed: {raw[-1]}"

# --- Verification ---
point_count = SapModel.PointObj.Count()
assert point_count >= 2, f"Expected at least 2 points, got {point_count}"

# --- Result ---
result["function"] = "SapModel.PointObj.SetRestraint"
result["point_i"] = pt_i
result["point_j"] = pt_j
result["point_count"] = point_count
result["status"] = "verified"
