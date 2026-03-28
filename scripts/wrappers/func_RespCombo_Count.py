# ============================================================
# Wrapper: SapModel.RespCombo.Count
# Category: RespCombo
# Description: Get total number of load combinations
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of load combinations defined in the model.

API Signature:
  SapModel.RespCombo.Count()

ByRef Output:
  count (direct return, integer)

Parameters:
  (none)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Count before adding ---
count_before = SapModel.RespCombo.Count()

# --- Add combos ---
ret = SapModel.RespCombo.Add("COUNT_TEST_1", 0)
assert ret == 0
ret = SapModel.RespCombo.Add("COUNT_TEST_2", 1)
assert ret == 0

# --- Target function ---
count_after = SapModel.RespCombo.Count()
assert count_after == count_before + 2, f"Expected {count_before + 2}, got {count_after}"

# --- Result ---
result["function"] = "SapModel.RespCombo.Count"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
