# ============================================================
# Wrapper: SapModel.LoadCases.Delete
# Category: Load_Cases
# Description: Delete a load case
# Verified: 2026-03-28
# Prerequisites: Model open, load case exists
# ============================================================
"""
Usage: Deletes a specified load case from the model.

API Signature:
  SapModel.LoadCases.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of existing load case
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: add a load pattern → creates auto load case ---
ret = SapModel.LoadPatterns.Add("WIND_DEL", 7)  # 7=LTYPE_WIND
assert ret == 0

count_before = SapModel.LoadCases.Count()

# --- Target function ---
ret = SapModel.LoadCases.Delete("WIND_DEL")
assert ret == 0, f"Delete failed: {ret}"

count_after = SapModel.LoadCases.Count()
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.LoadCases.Delete"
result["deleted"] = "WIND_DEL"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
