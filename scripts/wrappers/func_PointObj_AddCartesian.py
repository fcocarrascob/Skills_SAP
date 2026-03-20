# ============================================================
# Wrapper: SapModel.PointObj.AddCartesian
# Category: Object_Model
# Description: Create a point object at Cartesian coordinates
# Verified: 2026-03-20
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a point (joint) at specified X, Y, Z coordinates.
       Points are the basis for frame endpoints, area corners,
       boundary conditions, and applied loads.

API Signature:
  SapModel.PointObj.AddCartesian(X, Y, Z, Name, UserName, CSys, MergeOff, MergeNumber)

ByRef Output:
  raw[0]  = Name (name assigned by SAP2000)
  raw[-1] = ret_code (0=success)

Parameters:
  X          : float — X coordinate [L]
  Y          : float — Y coordinate [L]
  Z          : float — Z coordinate [L]
  Name       : str   — Output: assigned point name (""=auto-assign)
  UserName   : str   — User-defined name (optional)
  CSys       : str   — Coordinate system (default="Global")
  MergeOff   : bool  — True=skip merge with nearby points (default=False)
  MergeNumber: int   — Merge tolerance (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: create multiple points ---
# Origin point
raw = SapModel.PointObj.AddCartesian(0, 0, 0, "", "PT_ORIGIN")
pt1_name = raw[0]
assert raw[-1] == 0, f"AddCartesian(PT_ORIGIN) failed: {raw[-1]}"

# X-axis point at 5m
raw = SapModel.PointObj.AddCartesian(5.0, 0, 0, "", "PT_X5")
pt2_name = raw[0]
assert raw[-1] == 0, f"AddCartesian(PT_X5) failed: {raw[-1]}"

# Elevated point (column top)
raw = SapModel.PointObj.AddCartesian(0, 0, 3.5, "", "PT_TOP")
pt3_name = raw[0]
assert raw[-1] == 0, f"AddCartesian(PT_TOP) failed: {raw[-1]}"

# 3D point
raw = SapModel.PointObj.AddCartesian(5.0, 4.0, 3.5, "", "PT_3D")
pt4_name = raw[0]
assert raw[-1] == 0, f"AddCartesian(PT_3D) failed: {raw[-1]}"

# --- Verification ---
count = SapModel.PointObj.Count()
assert count == 4, f"Expected 4 points, got {count}"

# Verify coordinates of first point
raw = SapModel.PointObj.GetCoordCartesian(pt1_name, 0, 0, 0)
assert raw[-1] == 0, f"GetCoordCartesian failed: {raw[-1]}"
x, y, z = raw[0], raw[1], raw[2]
assert abs(x) < 1e-6 and abs(y) < 1e-6 and abs(z) < 1e-6, f"Origin coords wrong: ({x},{y},{z})"

# --- Result ---
result["function"] = "SapModel.PointObj.AddCartesian"
result["points_created"] = [pt1_name, pt2_name, pt3_name, pt4_name]
result["point_count"] = count
result["status"] = "verified"
