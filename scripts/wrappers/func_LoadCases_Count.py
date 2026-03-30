# ============================================================
# Wrapper: SapModel.LoadCases.Count
# Category: Load_Cases
# Description: Get total number of load cases (optionally by type)
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined load cases in the model.
       Optionally filter by case type (1=LinearStatic, 3=Modal, 4=RS, etc.)

API Signature:
  SapModel.LoadCases.Count(CaseType)

ByRef Output:
  count (direct return, integer)

Parameters:
  CaseType : int — (optional) eLoadCaseType enum. Omit for all types.
                   1=LinearStatic, 2=NonlinearStatic, 3=Modal,
                   4=ResponseSpectrum, etc.
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: count all cases ---
count_all = SapModel.LoadCases.Count()
assert count_all >= 1, f"Expected at least 1 case (DEAD), got {count_all}"

# --- Result ---
result["function"] = "SapModel.LoadCases.Count"
result["count_all"] = count_all
result["status"] = "verified"
