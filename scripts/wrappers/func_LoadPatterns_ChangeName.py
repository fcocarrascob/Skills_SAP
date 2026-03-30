# ============================================================
# Wrapper: SapModel.LoadPatterns.ChangeName
# Category: Load_Patterns
# Description: Rename a load pattern
# Verified: 2026-03-28
# Prerequisites: Model open, load pattern exists
# ============================================================
"""
Usage: Changes the name of an existing load pattern.

API Signature:
  SapModel.LoadPatterns.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing load pattern name
  NewName : str — New name for the load pattern
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# DEAD pattern exists by default
# --- Target function ---
ret = SapModel.LoadPatterns.ChangeName("DEAD", "PP")
assert ret == 0, f"ChangeName failed: {ret}"

# Verify
raw = SapModel.LoadPatterns.GetNameList(0, [])
assert raw[-1] == 0
pat_names = list(raw[1])
assert "PP" in pat_names, f"PP not found in: {pat_names}"
assert "DEAD" not in pat_names, f"DEAD still exists in: {pat_names}"

# --- Result ---
result["function"] = "SapModel.LoadPatterns.ChangeName"
result["old_name"] = "DEAD"
result["new_name"] = "PP"
result["status"] = "verified"
