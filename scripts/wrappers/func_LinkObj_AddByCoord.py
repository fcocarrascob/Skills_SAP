# ============================================================
# Wrapper: SapModel.LinkObj.AddByCoord
# Category: Object_Model
# Description: Create a link element by specifying end-point coordinates
# Verified: 2026-03-28
# Prerequisites: Model open, link property exists
# ============================================================
"""
Usage: Creates a link between two coordinate locations. Points are
       auto-created if they don't exist at those coordinates.

API Signature:
  SapModel.LinkObj.AddByCoord(xi, yi, zi, xj, yj, zj, Name,
      IsSingleJoint, PropName, UserName, CSys) -> [Name, ret_code]

ByRef Output:
  Name     : str — Assigned link name
  ret_code : int — 0=success

Parameters:
  xi,yi,zi      : float — I-End coordinates
  xj,yj,zj      : float — J-End coordinates (ignored if single joint)
  Name           : str   — Output: assigned name
  IsSingleJoint  : bool  — True=1-joint grounded link
  PropName       : str   — Link property name
  UserName       : str   — Optional user name
  CSys           : str   — Coordinate system
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

dof = [True, True, True, True, True, True]
fixed = [False, False, False, False, False, False]
ke = [10000, 10000, 20000, 1000, 1000, 1000]
ce = [0, 0, 0, 0, 0, 0]
ret = SapModel.PropLink.SetLinear("CONN_TEST", dof, fixed, ke, ce, 0, 0)
assert ret == 0

# --- Target function: two-joint link by coordinates ---
raw = SapModel.LinkObj.AddByCoord(
    0, 0, 0,     # I-End
    0, 0, 0.3,   # J-End
    "", False, "CONN_TEST", "LINK_COORD1"
)
link1 = raw[0]
assert raw[-1] == 0, f"AddByCoord(2-joint) failed: {raw[-1]}"

# Single-joint grounded link
raw = SapModel.LinkObj.AddByCoord(
    5, 5, 0,     # I-End
    0, 0, 0,     # J-End (ignored)
    "", True, "CONN_TEST", "LINK_GRND"
)
link2 = raw[0]
assert raw[-1] == 0, f"AddByCoord(1-joint) failed: {raw[-1]}"

# --- Verification ---
count = SapModel.LinkObj.Count()
assert count == 2, f"Expected 2 links, got {count}"

# --- Result ---
result["function"] = "SapModel.LinkObj.AddByCoord"
result["link_2joint"] = link1
result["link_grounded"] = link2
result["link_count"] = count
result["status"] = "verified"
