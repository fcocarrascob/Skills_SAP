# ============================================================
# Wrapper: SapModel.DatabaseTables — Display Selection (Consolidated)
# Category: Database_Tables
# Description: Tests all 10 Get/Set pairs for display selection config
# Verified: pending
# Prerequisites: Connected to SAP2000, model with load patterns and cases
# ============================================================
"""
Usage: Consolidated wrapper that exercises all 20 display selection
       functions (10 Get/Set pairs). Each pair controls which items
       are included when displaying analysis results.

Functions tested:
  1. Get/SetLoadCasesSelectedForDisplay
  2. Get/SetLoadCombinationsSelectedForDisplay
  3. Get/SetLoadPatternsSelectedForDisplay
  4. Get/SetElementVirtualWorkNamedSetsSelectedForDisplay
  5. Get/SetGeneralizedDisplacementsSelectedForDisplay
  6. Get/SetJointResponseSpectraNamedSetsSelectedForDisplay
  7. Get/SetPlotFunctionTracesNamedSetsSelectedForDisplay
  8. Get/SetPushoverNamedSetsSelectedForDisplay
  9. Get/SetSectionCutsSelectedForDisplay
 10. Get/SetTableOutputOptionsForDisplay

For pairs 1-9, the pattern is:
  Get: (NumberSelected, NameList[]) → ret_code
  Set: (NameList[]) → ret_code

Pair 10 (TableOutputOptions) has 18 ByRef parameters — special handling.
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Create minimal model with a load pattern and frame
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Add extra load patterns for testing display selection
ret = SapModel.LoadPatterns.Add("LIVE_TEST", 3)
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

tested_functions = []

# ═══════════════════════════════════════════════════════════════
# Pair 1: LoadCasesSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetLoadCasesSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadCasesSelectedForDisplay failed: {ret_code}"
num_selected_lc = raw[0]
lc_list = list(raw[1]) if raw[1] else []
tested_functions.append("GetLoadCasesSelectedForDisplay")

# Set: select all available load cases
ret = SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(lc_list if lc_list else [""])
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetLoadCasesSelectedForDisplay failed: {ret_val}"
tested_functions.append("SetLoadCasesSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 2: LoadCombinationsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetLoadCombinationsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadCombinationsSelectedForDisplay failed: {ret_code}"
tested_functions.append("GetLoadCombinationsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetLoadCombinationsSelectedForDisplay failed: {ret_val}"
tested_functions.append("SetLoadCombinationsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 3: LoadPatternsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetLoadPatternsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadPatternsSelectedForDisplay failed: {ret_code}"
num_patterns = raw[0]
pattern_list = list(raw[1]) if raw[1] else []
tested_functions.append("GetLoadPatternsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay(
    pattern_list if pattern_list else [""]
)
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetLoadPatternsSelectedForDisplay failed: {ret_val}"
tested_functions.append("SetLoadPatternsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 4: ElementVirtualWorkNamedSetsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetElementVirtualWorkNamedSets failed: {ret_code}"
tested_functions.append("GetElementVirtualWorkNamedSetsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetElementVirtualWorkNamedSets failed: {ret_val}"
tested_functions.append("SetElementVirtualWorkNamedSetsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 5: GeneralizedDisplacementsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetGeneralizedDisplacements failed: {ret_code}"
tested_functions.append("GetGeneralizedDisplacementsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetGeneralizedDisplacements failed: {ret_val}"
tested_functions.append("SetGeneralizedDisplacementsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 6: JointResponseSpectraNamedSetsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetJointResponseSpectraNamed failed: {ret_code}"
tested_functions.append("GetJointResponseSpectraNamedSetsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetJointResponseSpectraNamed failed: {ret_val}"
tested_functions.append("SetJointResponseSpectraNamedSetsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 7: PlotFunctionTracesNamedSetsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetPlotFunctionTracesNamed failed: {ret_code}"
tested_functions.append("GetPlotFunctionTracesNamedSetsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetPlotFunctionTracesNamed failed: {ret_val}"
tested_functions.append("SetPlotFunctionTracesNamedSetsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 8: PushoverNamedSetsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetPushoverNamedSetsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetPushoverNamedSets failed: {ret_code}"
tested_functions.append("GetPushoverNamedSetsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetPushoverNamedSetsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetPushoverNamedSets failed: {ret_val}"
tested_functions.append("SetPushoverNamedSetsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 9: SectionCutsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetSectionCutsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetSectionCuts failed: {ret_code}"
tested_functions.append("GetSectionCutsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetSectionCutsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetSectionCuts failed: {ret_val}"
tested_functions.append("SetSectionCutsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 10: TableOutputOptionsForDisplay (18 ByRef params)
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetTableOutputOptionsForDisplay(
    0.0, 0.0, 0.0,      # BaseReactionGX/GY/GZ
    True, 1, 12,         # IsAllModes, StartMode, EndMode
    True, 1, 6,          # IsAllBucklingModes, Start, End
    1, 1, 1, 1,          # ModalHistory, DirectHistory, NonlinearStatic, MultistepStatic
    1, 1, 1, 1, 1        # SteadyState, SteadyStateOption, PSD, Combo, BridgeDesign
)
ret_code = raw[-1]
assert ret_code == 0, f"GetTableOutputOptionsForDisplay failed: {ret_code}"
tested_functions.append("GetTableOutputOptionsForDisplay")

# Set with known good values
ret = SapModel.DatabaseTables.SetTableOutputOptionsForDisplay(
    0.0, 0.0, 0.0,      # BaseReactionGX/GY/GZ
    True, 1, 12,         # IsAllModes, StartMode, EndMode
    True, 1, 6,          # IsAllBucklingModes, Start, End
    1, 1, 2, 2,          # ModalHistory, DirectHistory, NonlinearStatic, MultistepStatic
    1, 1, 2, 2, 1        # SteadyState, SteadyStateOption, PSD, Combo, BridgeDesign
)
ret_val = ret if isinstance(ret, int) else ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_val == 0, f"SetTableOutputOptionsForDisplay failed: {ret_val}"
tested_functions.append("SetTableOutputOptionsForDisplay")

# --- Summary ---
assert len(tested_functions) == 20, f"Expected 20 functions, got {len(tested_functions)}"

result["function"] = "SapModel.DatabaseTables — Display Selection (Consolidated)"
result["functions_tested"] = tested_functions
result["total_tested"] = len(tested_functions)
result["status"] = "verified"
