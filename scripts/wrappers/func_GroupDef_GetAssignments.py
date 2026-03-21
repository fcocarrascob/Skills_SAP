# ============================================================
# Wrapper: SapModel.GroupDef.GetAssignments
# Category: Groups
# Description: Get objects assigned to a group
# Verified: 2026-03-21
# Prerequisites: Model open, group with assigned objects
# ============================================================
"""
Usage: Retrieves the objects assigned to a specified group.
       Returns object types and names for each member.

API Signature:
  SapModel.GroupDef.GetAssignments(Name,
      NumberItems, ObjectType, ObjectName) -> ret_code

ByRef Output (3 values):
  NumberItems  : int   — number of objects in group
  ObjectType[] : int[] — object type codes:
                         1=Point, 2=Frame, 3=Cable, 4=Tendon,
                         5=Area, 6=Solid, 7=Link
  ObjectName[] : str[] — object names

Parameters:
  Name         : str  — Group name
  NumberItems  : int  — placeholder (pass 0)
  ObjectType   : list — placeholder (pass [])
  ObjectName   : list — placeholder (pass [])
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Create structural elements
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "SEC_TEST", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(5, 0, 0, 5, 0, 3, "", "SEC_TEST", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "SEC_TEST", "")
assert beam[-1] == 0

# Create groups and assign objects
SapModel.GroupDef.SetGroup("MY_COLUMNS")
ret = SapModel.FrameObj.SetGroupAssign(col1[0], "MY_COLUMNS")
assert ret == 0
ret = SapModel.FrameObj.SetGroupAssign(col2[0], "MY_COLUMNS")
assert ret == 0

# --- Target function ---
raw = SapModel.GroupDef.GetAssignments("MY_COLUMNS", 0, [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetAssignments failed: {ret_code}"

num_items = raw[0]
obj_types = list(raw[1])
obj_names = list(raw[2])

assert num_items == 2, f"Expected 2 items, got {num_items}"
assert all(t == 2 for t in obj_types), f"Expected all Frame (2), got: {obj_types}"

# --- Result ---
result["function"] = "SapModel.GroupDef.GetAssignments"
result["group_name"] = "MY_COLUMNS"
result["num_items"] = num_items
result["object_types"] = obj_types
result["object_names"] = obj_names
result["status"] = "verified"
