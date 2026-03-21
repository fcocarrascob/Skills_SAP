# ============================================================
# Wrapper: SapModel.GroupDef.GetNameList
# Category: Groups
# Description: Get list of all defined group names
# Verified: 2026-03-21
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the names and count of all groups defined in the model.
       The "All" group always exists by default.

API Signature:
  SapModel.GroupDef.GetNameList(NumberNames, MyName) -> ret_code

ByRef Output (2 values):
  NumberNames : int   — total number of groups
  MyName[]    : str[] — array of group names

Parameters:
  NumberNames : int   — placeholder (pass 0)
  MyName      : list  — placeholder (pass [])
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# Create some groups first
SapModel.GroupDef.SetGroup("LEVEL_1")
SapModel.GroupDef.SetGroup("LEVEL_2")

# --- Target function ---
raw = SapModel.GroupDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

num_groups = raw[0]
group_names = list(raw[1])

assert num_groups >= 3, f"Expected >=3 groups (All + 2 custom), got {num_groups}"
assert "All" in group_names, f"Default 'All' group missing: {group_names}"
assert "LEVEL_1" in group_names
assert "LEVEL_2" in group_names

# --- Result ---
result["function"] = "SapModel.GroupDef.GetNameList"
result["num_groups"] = num_groups
result["group_names"] = group_names
result["status"] = "verified"
