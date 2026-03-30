# ============================================================
# Wrapper: SapModel.LoadPatterns.Count
# Category: Load_Patterns
# Description: Get total number of load patterns
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined load patterns in the model.

API Signature:
  SapModel.LoadPatterns.Count()

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

# --- Target function ---
count_before = SapModel.LoadPatterns.Count()
assert count_before >= 1, f"Expected at least 1 (DEAD), got {count_before}"

# Add patterns and recount
ret = SapModel.LoadPatterns.Add("LIVE_C", 3)
assert ret == 0
ret = SapModel.LoadPatterns.Add("WIND_C", 7)
assert ret == 0

count_after = SapModel.LoadPatterns.Count()
assert count_after == count_before + 2, f"Expected {count_before + 2}, got {count_after}"

# --- Result ---
result["function"] = "SapModel.LoadPatterns.Count"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
