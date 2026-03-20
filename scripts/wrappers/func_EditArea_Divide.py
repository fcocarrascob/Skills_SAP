# ============================================================
# Wrapper: SapModel.EditArea.Divide
# Category: Edit
# Description: Divide an area object into a mesh of smaller areas
# Verified: 2026-03-20
# Prerequisites: Model open, area object exists
# ============================================================
"""
Usage: Divides a single area element into a mesh of smaller area elements.
       Essential for finite element analysis to control mesh density.
       The original area is replaced by the new mesh.

API Signature:
  SapModel.EditArea.Divide(Name, MeshType, NumAreas, AreaName,
      N1, N2, MaxSize1, MaxSize2, PointOnEdgeFromLine,
      PointOnEdgeFromPoint, ExtendCookieCutLines, Rotation,
      MaxSizeGeneral, LocalAxesOnEdge, LocalAxesOnFace,
      RestraintsOnEdge, RestraintsOnFace, Group, SubMesh,
      SubMeshSize)

ByRef Output:
  raw[0]  = NumAreas (int — number of areas created)
  raw[1]  = AreaName[] (str[] — names of created areas)
  raw[-1] = ret_code (0=success)

Parameters:
  Name      : str — Area object name to divide
  MeshType  : int — 1=Cookie-cut by lines, 2=Cookie-cut by points,
                     3=Quad N1xN2, 4=Quad max size, 5=General
  N1        : int — Number of divisions along local axis 1 (for MeshType=3)
  N2        : int — Number of divisions along local axis 2 (for MeshType=3)
  MaxSize1  : float — Max element size along axis 1 (for MeshType=4)
  MaxSize2  : float — Max element size along axis 2 (for MeshType=4)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, shell, and area ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, True, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0, f"SetShell_1 failed: {ret}"

# Create a 4m x 3m area
x = [0.0, 4.0, 4.0, 0.0]
y = [0.0, 0.0, 3.0, 3.0]
z = [0.0, 0.0, 0.0, 0.0]
raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "SLAB_20", "")
area_name = raw[3]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Confirm 1 area before divide
count_before = SapModel.AreaObj.Count()
assert count_before == 1, f"Expected 1 area before divide, got {count_before}"

# --- Target function: divide into 2x2 grid ---
raw = SapModel.EditArea.Divide(
    area_name,    # Name of area to divide
    1,            # MeshType = 1 (Mesh into specified number of objects, n1xn2)
    0,            # NumberAreas (output)
    [],           # AreaName[] (output)
    2,            # n1 — 2 divisions along edge from pt1 to pt2
    2,            # n2 — 2 divisions along edge from pt2 to pt3
    0, 0,         # MaxSize1, MaxSize2 (not used for MeshType=1)
    False,        # PointOnEdgeFromGrid
    False,        # PointOnEdgeFromLine
    False,        # PointOnEdgeFromPoint
    False,        # ExtendCookieCutLines
    0,            # Rotation
    0,            # MaxSizeGeneral
    False,        # LocalAxesOnEdge
    False,        # LocalAxesOnFace
    False,        # RestraintsOnEdge
    False,        # RestraintsOnFace
)
ret_code = raw[-1]
assert ret_code == 0, f"EditArea.Divide failed: {ret_code}"

num_created = raw[0]
created_names = list(raw[1]) if raw[1] else []

# --- Verification ---
count_after = SapModel.AreaObj.Count()
assert count_after == 4, f"Expected 4 areas after 2x2 divide, got {count_after}"

# --- Result ---
result["function"] = "SapModel.EditArea.Divide"
result["original_area"] = area_name
result["areas_before"] = count_before
result["areas_after"] = count_after
result["num_created"] = num_created
result["created_names"] = created_names
result["status"] = "verified"
