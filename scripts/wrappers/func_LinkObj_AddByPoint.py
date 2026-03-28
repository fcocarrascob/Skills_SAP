# ============================================================
# Wrapper: SapModel.LinkObj.AddByPoint
# Category: Object_Model
# Description: Create a link element between two existing points
# Verified: 2026-03-28
# Prerequisites: Model open, points and link property exist
# ============================================================
"""
Usage: Creates a 2-joint link element connecting two existing point objects,
       or a 1-joint grounded link. Used for spring connections, dampers,
       and simple connectors.

API Signature:
  SapModel.LinkObj.AddByPoint(Point1, Point2, Name,
      IsSingleJoint, PropName, UserName) -> [Name, ret_code]

ByRef Output:
  Name     : str — Assigned link name
  ret_code : int — 0=success

Parameters:
  Point1        : str  — I-End point name
  Point2        : str  — J-End point name (ignored if IsSingleJoint=True)
  Name          : str  — Output: assigned name
  IsSingleJoint : bool — True=1-joint grounded link
  PropName      : str  — Link property name ("Default" or defined)
  UserName      : str  — Optional user name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Create link property
dof = [True, True, True, False, False, False]
fixed = [False, False, False, False, False, False]
ke = [5000, 5000, 5000, 0, 0, 0]
ce = [0, 0, 0, 0, 0, 0]
ret = SapModel.PropLink.SetLinear("SPRING_TEST", dof, fixed, ke, ce, 0, 0)
assert ret == 0

# Create two points
raw = SapModel.PointObj.AddCartesian(0, 0, 0, "", "PT_I")
pt_i = raw[0]
assert raw[-1] == 0
raw = SapModel.PointObj.AddCartesian(0, 0, 0.5, "", "PT_J")
pt_j = raw[0]
assert raw[-1] == 0

# --- Target function: two-joint link ---
raw = SapModel.LinkObj.AddByPoint(pt_i, pt_j, "", False, "SPRING_TEST", "LINK_1")
link_name = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"AddByPoint(2-joint) failed: {ret_code}"

# --- Target function: single-joint (grounded) link ---
raw2 = SapModel.PointObj.AddCartesian(5, 0, 0, "", "PT_GROUND")
pt_g = raw2[0]
assert raw2[-1] == 0

raw = SapModel.LinkObj.AddByPoint(pt_g, "", "", True, "SPRING_TEST", "LINK_GND")
link_gnd = raw[0]
assert raw[-1] == 0, f"AddByPoint(1-joint) failed: {raw[-1]}"

# --- Verification ---
count = SapModel.LinkObj.Count()
assert count == 2, f"Expected 2 links, got {count}"

# --- Result ---
result["function"] = "SapModel.LinkObj.AddByPoint"
result["two_joint_link"] = link_name
result["single_joint_link"] = link_gnd
result["link_count"] = count
result["status"] = "verified"
