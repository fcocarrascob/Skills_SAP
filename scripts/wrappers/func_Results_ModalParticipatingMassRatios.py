# ============================================================
# Wrapper: SapModel.Results.ModalParticipatingMassRatios
# Category: Analysis_Results
# Description: Extract modal participating mass ratios per mode
# Verified: 2026-03-28
# Prerequisites: Model analyzed with modal case
# ============================================================
"""
Usage: Reports the modal participating mass ratios for each mode.
       Critical for seismic design (ASCE 7, NSR-10 require ≥90% mass).

API Signature:
  SapModel.Results.ModalParticipatingMassRatios(NumberResults,
      LoadCase, StepType, StepNum, Period,
      Ux, Uy, Uz, SumUx, SumUy, SumUz,
      Rx, Ry, Rz, SumRx, SumRy, SumRz) -> ret_code

ByRef Output (16 values):
  NumberResults : int     — number of modes
  LoadCase[]    : str[]   — modal case names
  StepType[]    : str[]   — always "Mode"
  StepNum[]     : float[] — mode numbers
  Period[]      : float[] — period per mode [s]
  Ux..Uz[]      : float[] — mass ratio per mode per DOF
  SumUx..SumUz[]: float[] — cumulative mass ratios
  Rx..Rz[]      : float[] — rotational mass ratios
  SumRx..SumRz[]: float[] — cumulative rotational ratios

Parameters: None (all are ByRef outputs)
"""

# --- Use same 2-story frame as ModalPeriod ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_M", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_M", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 1, 24.0)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 2, 2.4)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("COL_40", "CONC_M", 0.4, 0.4)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30", "CONC_M", 0.3, 0.2)
assert ret == 0

for x in [0, 5]:
    raw = SapModel.FrameObj.AddByCoord(x, 0, 0, x, 0, 3, "", "COL_40", "")
    assert raw[-1] == 0
    raw = SapModel.FrameObj.AddByCoord(x, 0, 3, x, 0, 6, "", "COL_40", "")
    assert raw[-1] == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "BEAM_30", "")
assert raw[-1] == 0
raw = SapModel.FrameObj.AddByCoord(0, 0, 6, 5, 0, 6, "", "BEAM_30", "")
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("4", [True, True, True, True, True, True])
assert ret[-1] == 0

ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_modalmass.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.ModalParticipatingMassRatios(
    0, [], [], [], [],
    [], [], [], [], [], [],
    [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"ModalParticipatingMassRatios failed: {ret_code}"

num_modes = raw[0]
step_nums = list(raw[3])    # mode numbers
Ux = list(raw[5])           # Ux participating mass ratio per mode
Uy = list(raw[6])           # Uy per mode
Uz = list(raw[7])           # Uz per mode
SumUx = list(raw[8])        # cumulative Ux
SumUy = list(raw[9])        # cumulative Uy
SumUz = list(raw[10])       # cumulative Uz

assert num_modes > 0, f"No modal results"
# Last SumUx should be close to 1.0 if enough modes captured
last_SumUx = SumUx[-1] if SumUx else 0

# --- Result ---
result["function"] = "SapModel.Results.ModalParticipatingMassRatios"
result["num_modes"] = num_modes
result["Ux_per_mode"] = Ux
result["SumUx"] = SumUx
result["SumUy"] = SumUy
result["final_SumUx"] = last_SumUx
result["status"] = "verified"
