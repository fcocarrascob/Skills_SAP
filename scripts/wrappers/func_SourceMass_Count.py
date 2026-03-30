# ============================================================
# Wrapper: SapModel.SourceMass.Count
# Category: Mass_Source
# Description: Get total number of mass sources
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined mass sources.

API Signature:
  SapModel.SourceMass.Count()

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
count_before = SapModel.SourceMass.Count()
assert count_before >= 1, f"Expected at least 1 default mass source, got {count_before}"

# Add a mass source
ret = SapModel.SourceMass.SetMassSource(
    "MS_COUNT_TEST", True, True, True, False, 1, ["DEAD"], [1.0]
)
assert ret == 0

count_after = SapModel.SourceMass.Count()
assert count_after == count_before + 1, f"Expected {count_before + 1}, got {count_after}"

# --- Result ---
result["function"] = "SapModel.SourceMass.Count"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
