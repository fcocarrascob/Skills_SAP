# ============================================================
# Wrapper: SapModel.DesignSteel.DeleteResults
# Category: Design
# Description: Delete all steel frame design results
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Deletes all steel frame design results from the model.
       Useful before re-running design with updated parameters.

API Signature:
  SapModel.DesignSteel.DeleteResults()

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  (none)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
ret = SapModel.DesignSteel.DeleteResults()
assert ret == 0, f"DeleteResults failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.DeleteResults"
result["status"] = "verified"
