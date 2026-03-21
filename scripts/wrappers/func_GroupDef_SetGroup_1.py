# ============================================================
# Wrapper: SapModel.GroupDef.SetGroup
# Category: Groups
# Description: Create or modify a group definition
# Verified: 2026-03-21
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a new group or modifies an existing group definition.
       Groups are used to organize objects for selection, design,
       output, and load assignment.

NOTE: COM bridge exposes this as SetGroup (not SetGroup_1).

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
  Name                               : str  — Group name
  Color                              : int  — Display color (-1=default)
  SpecifiedForSelection              : bool — Available for selection (True)
  SpecifiedForSectionCutDefinition   : bool — Section cut group (True)
  SpecifiedForSteelDesign            : bool — Steel design group (True)
  SpecifiedForConcreteDesign         : bool — Concrete design group (True)
  SpecifiedForAluminumDesign         : bool — Aluminum design group (True)
  SpecifiedForColdFormedDesign       : bool — Cold-formed design group (True)
  SpecifiedForStaticNLActiveStage    : bool — NL staged construction (True)
  SpecifiedForBridgeResponseOutput   : bool — Bridge response output (True)
  SpecifiedForAutoSeismicOutput      : bool — Seismic output group (False)
  SpecifiedForAutoWindOutput         : bool — Wind output group (False)
  SpecifiedForMassAndWeight          : bool — Mass & weight group (True)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# --- Target function: create multiple groups ---
# Structural groups
# Args: Name, Color, ForSelection, ForSectionCut, ForSteelDesign, ForConcreteDesign,
#       ForAluminumDesign, ForColdFormedDesign, ForStaticNLActiveStage,
#       ForBridgeResponseOutput, ForAutoSeismicOutput, ForAutoWindOutput, ForMassAndWeight
ret = SapModel.GroupDef.SetGroup(
    "COLUMNS", -1,
    True, True, False, True, False, False, False, False, True, False, True
)
assert ret == 0, f"SetGroup(COLUMNS) failed: {ret}"

ret = SapModel.GroupDef.SetGroup(
    "BEAMS", -1,
    True, True, True, False, False, False, False, False, False, False, True
)
assert ret == 0, f"SetGroup(BEAMS) failed: {ret}"

ret = SapModel.GroupDef.SetGroup(
    "FOUNDATION", -1,
    True, False, False, True, False, False, False, False, True, True, True
)
assert ret == 0, f"SetGroup(FOUNDATION) failed: {ret}"

# --- Verification ---
raw = SapModel.GroupDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

group_count = raw[0]
group_names = list(raw[1])
assert "COLUMNS" in group_names, f"COLUMNS not in groups: {group_names}"
assert "BEAMS" in group_names, f"BEAMS not in groups: {group_names}"
assert "FOUNDATION" in group_names

# --- Result ---
result["function"] = "SapModel.GroupDef.SetGroup"
result["groups_created"] = ["COLUMNS", "BEAMS", "FOUNDATION"]
result["total_groups"] = group_count
result["all_groups"] = group_names
result["status"] = "verified"
