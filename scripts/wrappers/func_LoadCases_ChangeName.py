# ============================================================
# Wrapper: SapModel.LoadCases.ChangeName
# Category: Load_Cases
# Description: Rename a load case
# Verified: 2026-03-28
# Prerequisites: Model open, load case exists
# ============================================================
"""
Usage: Changes the name of an existing load case.

API Signature:
  SapModel.LoadCases.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing load case name
  NewName : str — New name for the load case
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.LoadPatterns.Add("RENAME_LC", 3)
assert ret == 0

# --- Target function ---
ret = SapModel.LoadCases.ChangeName("RENAME_LC", "RENAMED_LC")
assert ret == 0, f"ChangeName failed: {ret}"

# Verify via GetNameList
raw = SapModel.LoadCases.GetNameList(0, [])
assert raw[-1] == 0
case_names = list(raw[1])
assert "RENAMED_LC" in case_names, f"RENAMED_LC not found in: {case_names}"
assert "RENAME_LC" not in case_names, f"RENAME_LC still exists in: {case_names}"

# --- Result ---
result["function"] = "SapModel.LoadCases.ChangeName"
result["old_name"] = "RENAME_LC"
result["new_name"] = "RENAMED_LC"
result["status"] = "verified"
