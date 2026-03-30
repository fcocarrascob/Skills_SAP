# ============================================================
# Wrapper: SapModel.Results.ModalPeriod
# Category: Analysis_Results
# Description: Extract modal periods, frequencies, and eigenvalues
# Verified: 2026-03-28
# Prerequisites: Model analyzed with modal case
# ============================================================
"""
Usage: Reports the modal period, cyclic frequency, circular frequency, and
       eigenvalue for each mode in selected modal load cases.

API Signature:
  SapModel.Results.ModalPeriod(NumberResults, LoadCase, StepType,
      StepNum, Period, Frequency, CircFreq, EigenValue) -> ret_code

ByRef Output (7 values):
  NumberResults : int     — number of modes
  LoadCase[]    : str[]   — modal case names
  StepType[]    : str[]   — always "Mode"
  StepNum[]     : float[] — mode numbers (1, 2, 3, ...)
  Period[]      : float[] — period per mode [s]
  Frequency[]   : float[] — cyclic frequency [1/s]
  CircFreq[]    : float[] — circular frequency [rad/s]
  EigenValue[]  : float[] — eigenvalue [rad²/s²]

Parameters: None (all are ByRef outputs)
"""

# --- Build a simple 3D frame for modal analysis ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material with weight/mass for modal analysis
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

# 2-story portal frame
# Columns
for x in [0, 5]:
    raw = SapModel.FrameObj.AddByCoord(x, 0, 0, x, 0, 3, "", "COL_40", "")
    assert raw[-1] == 0
    raw = SapModel.FrameObj.AddByCoord(x, 0, 3, x, 0, 6, "", "COL_40", "")
    assert raw[-1] == 0

# Beams
raw = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "BEAM_30", "")
assert raw[-1] == 0
raw = SapModel.FrameObj.AddByCoord(0, 0, 6, 5, 0, 6, "", "BEAM_30", "")
assert raw[-1] == 0

# Fixed bases
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("4", [True, True, True, True, True, True])
assert ret[-1] == 0

# MODAL case exists by default in SAP2000 — just run analysis
ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_modalperiod.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

# Select MODAL case for output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.ModalPeriod(
    0, [], [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"ModalPeriod failed: {ret_code}"

num_modes = raw[0]
load_cases = list(raw[1])
step_types = list(raw[2])   # always "Mode"
step_nums = list(raw[3])    # mode numbers: 1, 2, 3, ...
periods = list(raw[4])      # period per mode [s]
frequencies = list(raw[5])  # cyclic frequency [Hz]
circ_freqs = list(raw[6])   # circular frequency [rad/s]
eigenvalues = list(raw[7])  # eigenvalues [rad²/s²]

assert num_modes > 0, f"No modal results"
assert periods[0] > 0, f"First period should be positive, got {periods[0]}"

# --- Result ---
result["function"] = "SapModel.Results.ModalPeriod"
result["num_modes"] = num_modes
result["periods"] = periods
result["frequencies"] = frequencies
result["T1"] = periods[0]
result["status"] = "verified"
