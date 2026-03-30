# ============================================================
# Wrapper: SapModel.LoadPatterns.Delete
# Category: Load_Patterns
# Description: Delete a load pattern
# Verified: 2026-03-28
# Prerequisites: Model open, load pattern exists, at least 2 patterns
# ============================================================
"""
Usage: Deletes a specified load pattern from the model.
       Cannot delete the last remaining load pattern.

API Signature:
  SapModel.LoadPatterns.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of existing load pattern
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: must have >1 pattern ---
ret = SapModel.LoadPatterns.Add("TEMP_LP", 3)
assert ret == 0

# NOTE: Must delete the auto-created load case before deleting the pattern
ret_lc = SapModel.LoadCases.Delete("TEMP_LP")
assert ret_lc == 0, f"LoadCases.Delete prerequisite failed: {ret_lc}"

count_before = SapModel.LoadPatterns.Count()

# --- Target function ---
ret = SapModel.LoadPatterns.Delete("TEMP_LP")
assert ret == 0, f"Delete failed: {ret}"

count_after = SapModel.LoadPatterns.Count()
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.LoadPatterns.Delete"
result["deleted"] = "TEMP_LP"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
