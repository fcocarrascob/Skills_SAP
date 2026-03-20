# ============================================================
# Wrapper: SapModel.RespCombo.GetCaseList
# Category: RespCombo
# Description: Query the load cases and scale factors in a combination
# Verified: 2026-03-20
# Prerequisites: Model open, combo with cases exists
# ============================================================
"""
Usage: Retrieves the list of load cases/combos in a response combination,
       including their types and scale factors. Use to verify combo contents.

API Signature:
  SapModel.RespCombo.GetCaseList(ComboName, NumberItems, CaseType,
      CaseName, ScaleFactor)

ByRef Output:
  raw[0]  = NumberItems (int — count of entries)
  raw[1]  = CaseType[] (int[] — 0=LoadCase, 1=LoadCombo per entry)
  raw[2]  = CaseName[] (str[] — names of load cases/combos)
  raw[3]  = ScaleFactor[] (float[] — scale factor per entry)
  raw[-1] = ret_code (0=success)

Parameters:
  ComboName   : str     — Name of the response combination
  NumberItems : int     — Output: number of cases (pass 0)
  CaseType    : int[]   — Output: type array (pass [])
  CaseName    : str[]   — Output: name array (pass [])
  ScaleFactor : float[] — Output: scale factor array (pass [])
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: load patterns, combo, and assigned cases ---
ret = SapModel.LoadPatterns.Add("D", 1, 1)
assert ret == 0, f"LoadPatterns.Add(D) failed: {ret}"

ret = SapModel.LoadPatterns.Add("L", 3)
assert ret == 0, f"LoadPatterns.Add(L) failed: {ret}"

ret = SapModel.LoadPatterns.Add("W", 6)
assert ret == 0, f"LoadPatterns.Add(W) failed: {ret}"

# Create combo with 3 cases: 1.2D + 1.6L + 0.5W
ret = SapModel.RespCombo.Add("TEST_COMBO", 0)
assert ret == 0, f"RespCombo.Add failed: {ret}"

ret = SapModel.RespCombo.SetCaseList("TEST_COMBO", 0, "D", 1.2)
assert ret == 0, f"SetCaseList(D) failed: {ret}"

ret = SapModel.RespCombo.SetCaseList("TEST_COMBO", 0, "L", 1.6)
assert ret == 0, f"SetCaseList(L) failed: {ret}"

ret = SapModel.RespCombo.SetCaseList("TEST_COMBO", 0, "W", 0.5)
assert ret == 0, f"SetCaseList(W) failed: {ret}"

# --- Target function: query combo contents ---
raw = SapModel.RespCombo.GetCaseList("TEST_COMBO", 0, [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetCaseList failed: {ret_code}"

num_items = raw[0]
case_types = list(raw[1])
case_names = list(raw[2])
scale_factors = list(raw[3])

# --- Verification ---
assert num_items == 3, f"Expected 3 cases, got {num_items}"
assert "D" in case_names, f"D not found in combo"
assert "L" in case_names, f"L not found in combo"
assert "W" in case_names, f"W not found in combo"

# Find D and verify its scale factor
d_index = case_names.index("D")
assert abs(scale_factors[d_index] - 1.2) < 0.001, f"D scale factor wrong: {scale_factors[d_index]}"

l_index = case_names.index("L")
assert abs(scale_factors[l_index] - 1.6) < 0.001, f"L scale factor wrong: {scale_factors[l_index]}"

# --- Result ---
result["function"] = "SapModel.RespCombo.GetCaseList"
result["combo_name"] = "TEST_COMBO"
result["num_items"] = num_items
result["case_types"] = case_types
result["case_names"] = case_names
result["scale_factors"] = scale_factors
result["status"] = "verified"
