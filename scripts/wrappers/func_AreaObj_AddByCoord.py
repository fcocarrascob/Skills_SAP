# ============================================================
# Wrapper: SapModel.AreaObj.AddByCoord
# Category: Object_Model
# Description: Create an area element from corner coordinates
# Verified: 2026-03-20
# Prerequisites: Model open, material and shell section defined
# ============================================================
"""
Usage: Creates an area (shell/plate/membrane) element defined by corner
       coordinates. Common for slabs, walls, and footings.

API Signature:
  SapModel.AreaObj.AddByCoord(NumberPoints, X, Y, Z, Name, PropName,
      UserName, CSys)

ByRef Output:
  raw[3]  = Name (name assigned by SAP2000)
  raw[-1] = ret_code (0=success)

Note: Full return is [X[], Y[], Z[], Name, ret_code]

Parameters:
  NumberPoints : int      — Number of corner points (3 for triangle, 4 for quad)
  X            : float[]  — X coordinates [x1, x2, x3, x4]
  Y            : float[]  — Y coordinates [y1, y2, y3, y4]
  Z            : float[]  — Z coordinates [z1, z2, z3, z4]
  Name         : str      — Output: assigned area name (""=auto-assign)
  PropName     : str      — Area section property name
  UserName     : str      — User-defined name (optional)
  CSys         : str      — Coordinate system (default="Global")
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material and shell property ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, True, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0, f"SetShell_1 failed: {ret}"

# --- Target function: create rectangular area (4 corners) ---
# 4m x 3m slab at Z=0 (XY plane)
x = [0.0, 4.0, 4.0, 0.0]
y = [0.0, 0.0, 3.0, 3.0]
z = [0.0, 0.0, 0.0, 0.0]

raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "SLAB_20", "")
area_name = raw[3]
ret_code = raw[-1]
assert ret_code == 0, f"AddByCoord(quad) failed: {ret_code}"

# Create a triangular area (3 corners)
x_tri = [0.0, 3.0, 1.5]
y_tri = [0.0, 0.0, 2.5]
z_tri = [3.5, 3.5, 3.5]

raw = SapModel.AreaObj.AddByCoord(3, x_tri, y_tri, z_tri, "", "SLAB_20", "")
tri_name = raw[3]
ret_code = raw[-1]
assert ret_code == 0, f"AddByCoord(triangle) failed: {ret_code}"

# --- Verification ---
count = SapModel.AreaObj.Count()
assert count == 2, f"Expected 2 areas, got {count}"

# --- Result ---
result["function"] = "SapModel.AreaObj.AddByCoord"
result["areas_created"] = [area_name, tri_name]
result["area_count"] = count
result["status"] = "verified"
