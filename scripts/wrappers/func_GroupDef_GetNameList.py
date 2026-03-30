# ============================================================
# Wrapper: SapModel.GroupDef.GetNameList
# Category: Groups
# Description: Retrieve names of all defined groups
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns a list of all group names defined in the model.
       Every model has at minimum the "ALL" group.

API Signature:
  SapModel.GroupDef.GetNameList(NumberNames, MyName) ->
      [NumberNames, MyName[], ret_code]

ByRef Output:
  NumberNames : int   — number of groups
  MyName[]    : str[] — group names

Parameters: None (all are ByRef outputs)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Create some groups
ret = SapModel.GroupDef.SetGroup("GROUP_A")
assert ret == 0
ret = SapModel.GroupDef.SetGroup("GROUP_B")
assert ret == 0

# --- Target function ---
raw = SapModel.GroupDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

num_groups = raw[0]
group_names = list(raw[1])

assert num_groups >= 3, f"Expected >=3 groups (ALL + 2), got {num_groups}"
assert "ALL" in group_names, "ALL group missing"
assert "GROUP_A" in group_names, "GROUP_A missing"
assert "GROUP_B" in group_names, "GROUP_B missing"

# --- Result ---
result["function"] = "SapModel.GroupDef.GetNameList"
result["num_groups"] = num_groups
result["group_names"] = group_names
result["status"] = "verified"
