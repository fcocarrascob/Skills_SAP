# ============================================================
# Wrapper: SapModel.GroupDef.SetGroup
# Category: Groups
# Description: Create or modify a group definition with properties
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a new group or modifies an existing group. Groups are used for
       selection, design, output reporting, and batch operations.

API Signature:
  SapModel.GroupDef.SetGroup(Name, Color, SpecifiedForSelection,
      SpecifiedForSectionCutDefinition, SpecifiedForSteelDesign,
      SpecifiedForConcreteDesign, SpecifiedForAluminumDesign,
      SpecifiedForColdFormedDesign, SpecifiedForStaticNLActiveStage,
      SpecifiedForBridgeResponseOutput, SpecifiedForAutoSeismicOutput,
      SpecifiedForAutoWindOutput, SpecifiedForMassAndWeight) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Group name. New group created if doesn't exist; modified if exists.
  Color: int — Display color (-1=auto)
  SpecifiedFor* : bool — 12 optional booleans controlling group usage
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: create groups ---
# Basic group with defaults
ret = SapModel.GroupDef.SetGroup("COLUMNS")
assert ret == 0, f"SetGroup(COLUMNS) failed: {ret}"

# Group with specific properties: for selection and concrete design only
ret = SapModel.GroupDef.SetGroup(
    "BEAMS_LEVEL1", -1, True, False, False, True, False, False, False, False, False, False, True
)
assert ret == 0, f"SetGroup(BEAMS_LEVEL1) failed: {ret}"

# --- Verification via GetNameList ---
raw = SapModel.GroupDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

num_groups = raw[0]
group_names = list(raw[1])
assert "COLUMNS" in group_names, f"COLUMNS not in groups: {group_names}"
assert "BEAMS_LEVEL1" in group_names, f"BEAMS_LEVEL1 not in groups: {group_names}"

# --- Result ---
result["function"] = "SapModel.GroupDef.SetGroup"
result["groups_created"] = ["COLUMNS", "BEAMS_LEVEL1"]
result["total_groups"] = num_groups
result["all_group_names"] = group_names
result["status"] = "verified"
