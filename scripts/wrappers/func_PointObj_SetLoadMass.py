# ============================================================
# Wrapper: SapModel.PointObj.SetMass
# Category: Object_Model
# Description: Assign concentrated mass to a joint
# Verified: 2026-03-21
# Prerequisites: Model open, point object exists
# ============================================================
"""
Usage: Assigns a concentrated (lumped) mass to a point object.
       Used for equipment loads, non-structural mass, and dynamic
       analysis mass idealization. The mass is 6-DOF.

NOTE: COM bridge exposes this as SetMass (not SetLoadMass).
      The function does NOT take LoadPat, Replace, CSys, or ItemType
      arguments — it directly sets structural mass on the joint.

API Signature:
  SapModel.PointObj.SetMass(Name, Value) -> [Value_byref, ret_code]

ByRef Output:
  raw[0]  = Value (tuple of 6 floats — verified values set)
  raw[-1] = ret_code (0=success)

Parameters:
  Name  : str      — Point object name
  Value : float[6] — Mass values [M_UX, M_UY, M_UZ, M_RX, M_RY, M_RZ]
                     in mass units (e.g., kg for kN_m_C)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Create a column with a joint at the top
col = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 5, "", "SEC_TEST", "")
assert col[-1] == 0

# Support at base
ret_r = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret_r[-1] == 0

# --- Target function: assign 5000 kg translational mass at top node ---
# SetMass(Name, Value[6]) -> [Value_byref, ret_code]
raw = SapModel.PointObj.SetMass(
    "2",
    [5000, 5000, 5000, 0, 0, 0]   # 5 tonnes translational mass
)
assert raw[-1] == 0, f"SetMass failed: {raw[-1]}"

# Verify mass was stored
raw_get = SapModel.PointObj.GetMass("2", [0]*6)
assert raw_get[-1] == 0, f"GetMass failed: {raw_get[-1]}"
values = list(raw_get[0])
assert values[0] == 5000.0, f"Expected M_UX=5000, got: {values[0]}"

# Overwrite with different values
raw2 = SapModel.PointObj.SetMass("2", [2000, 2000, 2000, 0, 0, 0])
assert raw2[-1] == 0, f"SetMass (overwrite) failed: {raw2[-1]}"

# --- Result ---
result["function"] = "SapModel.PointObj.SetMass"
result["joint"] = "2"
result["mass_set"] = [5000, 5000, 5000, 0, 0, 0]
result["mass_verified"] = values
result["mass_overwrite"] = [2000, 2000, 2000, 0, 0, 0]
result["status"] = "verified"
