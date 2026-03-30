# ============================================================
# Wrapper: SapModel.LoadCases.ResponseSpectrum.SetDampConstant
# Category: Load_Cases
# Description: Set constant damping for a response spectrum case
# Verified: 2026-03-28
# Prerequisites: Model open, RS load case defined
# ============================================================
"""
Usage: Sets a constant modal damping ratio for a response spectrum
       load case. Common value: 0.05 (5% for steel/concrete).

API Signature:
  SapModel.LoadCases.ResponseSpectrum.SetDampConstant(Name, Damp)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str   — Response spectrum load case name
  Damp : float — Modal damping ratio (e.g. 0.05 = 5%)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create a response spectrum case ---
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("RS_X")
assert ret == 0, f"SetCase(RS_X) failed: {ret}"

# --- Target function ---
ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant("RS_X", 0.05)
assert ret == 0, f"SetDampConstant failed: {ret}"

# --- Result ---
result["function"] = "SapModel.LoadCases.ResponseSpectrum.SetDampConstant"
result["case_name"] = "RS_X"
result["damping"] = 0.05
result["status"] = "verified"
