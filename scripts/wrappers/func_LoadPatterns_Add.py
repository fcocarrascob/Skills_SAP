# ============================================================
# Wrapper: SapModel.LoadPatterns.Add
# Category: Load_Patterns
# Description: Add a new load pattern to the model
# Verified: 2026-03-20
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a new load pattern with a specified name, type,
       and optional self-weight multiplier.

API Signature:
  SapModel.LoadPatterns.Add(Name, MyType, SelfWTMultiplier, AddCase)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name              : str   — Load pattern name
  MyType            : int   — eLoadPatternType enum:
                               1=Dead, 2=SuperDead, 3=Live, 4=ReduceLive,
                               5=Quake, 6=Wind, 7=Snow, 8=Other
  SelfWTMultiplier  : float — Self-weight multiplier (default=0)
  AddCase           : bool  — True=auto-create matching load case (default=True)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: add multiple load patterns ---
# Dead load with self-weight multiplier = 1
ret = SapModel.LoadPatterns.Add("DEAD_CUSTOM", 1, 1)
assert ret == 0, f"Add(DEAD_CUSTOM) failed: {ret}"

# Live load (no self-weight)
ret = SapModel.LoadPatterns.Add("LIVE_CUSTOM", 3)
assert ret == 0, f"Add(LIVE_CUSTOM) failed: {ret}"

# Wind load
ret = SapModel.LoadPatterns.Add("WIND_X", 6)
assert ret == 0, f"Add(WIND_X) failed: {ret}"

# --- Verification ---
# Count load patterns (includes default "DEAD" pattern)
raw = SapModel.LoadPatterns.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
num_patterns = raw[0]
pattern_names = list(raw[1])

assert "DEAD_CUSTOM" in pattern_names, "DEAD_CUSTOM not found in load patterns"
assert "LIVE_CUSTOM" in pattern_names, "LIVE_CUSTOM not found in load patterns"
assert "WIND_X" in pattern_names, "WIND_X not found in load patterns"

# --- Result ---
result["function"] = "SapModel.LoadPatterns.Add"
result["num_patterns"] = num_patterns
result["pattern_names"] = pattern_names
result["status"] = "verified"
