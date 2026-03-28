# ============================================================
# Wrapper: SapModel.Results.AreaStressShell
# Category: Analysis_Results
# Description: Extract shell element stresses (S11, S22, S12, etc.)
# Verified: 2026-03-28
# Prerequisites: Model analyzed, shell area elements exist
# ============================================================
"""
Usage: Reports area element stresses at top/bottom faces and average
       out-of-plane shear. Only applies to shell-type properties.

API Signature:
  SapModel.Results.AreaStressShell(Name, ItemTypeElm,
      NumberResults, Obj, Elm, PointElm,
      LoadCase, StepType, StepNum,
      S11Top, S22Top, S12Top, SMaxTop, SMinTop, SAngleTop, SVMTop,
      S11Bot, S22Bot, S12Bot, SMaxBot, SMinBot, SAngleBot, SVMBot,
      S13Avg, S23Avg, SMaxAvg, SAngleAvg) -> ret_code

ByRef Output (26 values):
  NumberResults : int   — number of result rows
  Obj..StepNum  : arrays — identification arrays
  S11Top..SVMTop: float[] — top fiber stresses [F/L²]
  S11Bot..SVMBot: float[] — bottom fiber stresses [F/L²]
  S13Avg..SAngleAvg: float[] — average out-of-plane shear [F/L²]

Parameters:
  Name        : str — Area name
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: loaded slab ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, False, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0

# 4x4m supported slab
raw = SapModel.AreaObj.AddByCoord(
    4, [0, 4, 4, 0], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_20"
)
area_name = raw[3]
assert raw[-1] == 0

for i in range(1, 5):
    ret = SapModel.PointObj.SetRestraint(
        str(i), [True, True, True, False, False, False]
    )
    assert ret[-1] == 0

ret = SapModel.AreaObj.SetLoadUniform(area_name, "DEAD", -10, 10, True, "Global")
assert ret == 0

ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_areastressshell.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.AreaStressShell(
    area_name, 0,
    0, [], [], [],
    [], [], [],
    [], [], [], [], [], [], [],
    [], [], [], [], [], [], [],
    [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"AreaStressShell failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No stress results returned"

S11Top = list(raw[6])
S22Top = list(raw[7])

# --- Result ---
result["function"] = "SapModel.Results.AreaStressShell"
result["area_name"] = area_name
result["num_results"] = num_results
result["S11Top_sample"] = S11Top[:4] if len(S11Top) >= 4 else S11Top
result["S22Top_sample"] = S22Top[:4] if len(S22Top) >= 4 else S22Top
result["status"] = "verified"
