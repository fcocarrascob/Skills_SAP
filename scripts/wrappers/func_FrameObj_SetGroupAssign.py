# ============================================================
# Wrapper: SapModel.FrameObj.SetGroupAssign
# Category: Object_Model
# Description: Add or remove frame objects from a group
# Verified: 2026-03-28
# Prerequisites: Model open, frame and group exist
# ============================================================
"""
Usage: Adds frame objects to (or removes from) a specified group.
       Groups must exist before objects can be assigned to them.

API Signature:
  SapModel.FrameObj.SetGroupAssign(Name, GroupName, Remove,
      ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name      : str  — Frame object name
  GroupName : str  — Target group name (must exist)
  Remove    : bool — False=add, True=remove from group
  ItemType  : int  — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("COL_SEC", "STEEL_TEST", 0.4, 0.4)
assert ret == 0

# Create some frames
raw1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "COL_SEC", "")
f1 = raw1[0]
assert raw1[-1] == 0
raw2 = SapModel.FrameObj.AddByCoord(5, 0, 0, 5, 0, 3, "", "COL_SEC", "")
f2 = raw2[0]
assert raw2[-1] == 0
raw3 = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "COL_SEC", "")
f3 = raw3[0]
assert raw3[-1] == 0

# Create group
ret = SapModel.GroupDef.SetGroup("COLUMNS")
assert ret == 0

# --- Target function ---
ret = SapModel.FrameObj.SetGroupAssign(f1, "COLUMNS")
assert ret == 0, f"SetGroupAssign(f1) failed: {ret}"

ret = SapModel.FrameObj.SetGroupAssign(f2, "COLUMNS")
assert ret == 0, f"SetGroupAssign(f2) failed: {ret}"

# --- Verification via GetAssignments ---
raw = SapModel.GroupDef.GetAssignments("COLUMNS", 0, [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetAssignments failed: {ret_code}"

num_items = raw[0]
obj_types = list(raw[1])
obj_names = list(raw[2])
assert num_items == 2, f"Expected 2 items in group, got {num_items}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetGroupAssign"
result["group_name"] = "COLUMNS"
result["items_in_group"] = num_items
result["object_names"] = obj_names
result["status"] = "verified"
