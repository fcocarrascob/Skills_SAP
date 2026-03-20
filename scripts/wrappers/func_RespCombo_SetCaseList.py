# ============================================================
# Wrapper: SapModel.RespCombo.SetCaseList
# Category: RespCombo
# Description: Add a load case to a response combination with scale factor
# Verified: 2026-03-20
# Prerequisites: Model open, combo and load cases exist
# ============================================================
"""
Usage: Adds a load case or another combo to a response combination.
       Each call adds one case with its scale factor. Call multiple
       times to build up a full combination (e.g., 1.2D + 1.6L).

API Signature:
  SapModel.RespCombo.SetCaseList(ComboName, CaseType, CaseName, ScaleFactor)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  ComboName   : str   — Name of the response combination
  CaseType    : int   — 0=LoadCase, 1=LoadCombo
  CaseName    : str   — Name of the load case or combo to add
  ScaleFactor : float — Multiplier for this case (e.g., 1.4, 1.6, -1.0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: load patterns and combo ---
# Create load patterns
ret = SapModel.LoadPatterns.Add("PP", 1, 1)   # Dead (self-weight=1)
assert ret == 0, f"LoadPatterns.Add(PP) failed: {ret}"

ret = SapModel.LoadPatterns.Add("SC", 3)       # Live
assert ret == 0, f"LoadPatterns.Add(SC) failed: {ret}"

ret = SapModel.LoadPatterns.Add("VIENTO_X", 6) # Wind
assert ret == 0, f"LoadPatterns.Add(VIENTO_X) failed: {ret}"

# Create combinations
ret = SapModel.RespCombo.Add("COMB1_LRFD", 0)  # Linear add
assert ret == 0, f"RespCombo.Add(COMB1) failed: {ret}"

ret = SapModel.RespCombo.Add("ENV_ULS", 1)  # Envelope
assert ret == 0, f"RespCombo.Add(ENV_ULS) failed: {ret}"

# --- Target function: add cases to combo ---
# LRFD combo: 1.2D + 1.6L
raw = SapModel.RespCombo.SetCaseList("COMB1_LRFD", 0, "PP", 1.2)
assert raw[-1] == 0, f"SetCaseList(PP) failed: {raw}"

raw = SapModel.RespCombo.SetCaseList("COMB1_LRFD", 0, "SC", 1.6)
assert raw[-1] == 0, f"SetCaseList(SC) failed: {raw}"

# Envelope: add LRFD combo + Wind
raw = SapModel.RespCombo.SetCaseList("ENV_ULS", 1, "COMB1_LRFD", 1.0)  # CaseType=1 for combo
assert raw[-1] == 0, f"SetCaseList(COMB1_LRFD→ENV) failed: {raw}"

raw = SapModel.RespCombo.SetCaseList("ENV_ULS", 0, "VIENTO_X", 1.0)
assert raw[-1] == 0, f"SetCaseList(VIENTO_X→ENV) failed: {raw}"

# --- Verification ---
# Verify COMB1_LRFD has 2 cases
raw = SapModel.RespCombo.GetCaseList("COMB1_LRFD", 0, [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetCaseList(COMB1) failed: {ret_code}"
num_cases = raw[0]
assert num_cases == 2, f"Expected 2 cases in COMB1, got {num_cases}"

# --- Result ---
result["function"] = "SapModel.RespCombo.SetCaseList"
result["combo_name"] = "COMB1_LRFD"
result["num_cases"] = num_cases
result["case_names"] = list(raw[2])
result["scale_factors"] = list(raw[3])
result["status"] = "verified"
