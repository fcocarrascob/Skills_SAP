# ============================================================
# Wrapper: SapModel.DesignSteel.GetComboStrength
# Category: Design
# Description: Retrieve combos selected for steel strength design
# Verified: 2026-03-28
# Prerequisites: Model open, combos selected via SetComboStrength
# ============================================================
"""
Usage: Returns the list of load combinations currently selected
       for steel strength design.

API Signature:
  SapModel.DesignSteel.GetComboStrength(NumberItems, MyName[])

ByRef Output:
  [NumberItems, MyName[], ret_code]

Parameters:
  NumberItems : int    — (ByRef out) Number of selected combos
  MyName      : str[]  — (ByRef out) Names of selected combos
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("STR_1", 0)
assert ret == 0
ret = SapModel.RespCombo.Add("STR_2", 0)
assert ret == 0

ret = SapModel.DesignSteel.SetComboStrength("STR_1", True)
assert ret == 0
ret = SapModel.DesignSteel.SetComboStrength("STR_2", True)
assert ret == 0

# --- Target function ---
raw = SapModel.DesignSteel.GetComboStrength(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetComboStrength failed: {ret_code}"

num_items = raw[0]
combo_names = list(raw[1]) if isinstance(raw[1], (list, tuple)) else [raw[1]]

assert num_items >= 2, f"Expected at least 2 combos, got {num_items}"
assert "STR_1" in combo_names, f"STR_1 not in strength combos: {combo_names}"
assert "STR_2" in combo_names, f"STR_2 not in strength combos: {combo_names}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.GetComboStrength"
result["num_items"] = num_items
result["combo_names"] = combo_names
result["byref_layout"] = "[NumberItems, MyName[], ret_code]"
result["status"] = "verified"
