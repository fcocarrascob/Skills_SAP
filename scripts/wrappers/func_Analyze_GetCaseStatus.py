# ============================================================
# Wrapper: SapModel.Analyze.GetCaseStatus
# Category: Analyze
# Description: Retrieve run status for all load cases
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Reports whether each load case has been run, is pending, or failed.
       Status: 1=Not run, 2=Could not start, 3=Not finished, 4=Finished.

API Signature:
  SapModel.Analyze.GetCaseStatus(NumberItems, CaseName, Status) ->
      [NumberItems, CaseName[], Status[], ret_code]

ByRef Output:
  NumberItems : int   — number of load cases
  CaseName[]  : str[] — load case names
  Status[]    : int[] — 1=Not run, 2=Could not start, 3=Not finished, 4=Finished

Parameters: None (all are ByRef outputs)
"""

# --- Setup with a model that can be analyzed ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "SEC", "")
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, True, True, True])
assert ret[-1] == 0

# --- Check status BEFORE analysis (should be "Not run") ---
raw = SapModel.Analyze.GetCaseStatus(0, [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetCaseStatus(before) failed: {ret_code}"

num_before = raw[0]
names_before = list(raw[1])
status_before = list(raw[2])

# All should be 1 (Not run)
assert all(s == 1 for s in status_before), f"Expected all status=1, got {status_before}"

# --- Run analysis ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_analyze_casestatus.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

# --- Check status AFTER analysis ---
raw = SapModel.Analyze.GetCaseStatus(0, [], [])
assert raw[-1] == 0

num_after = raw[0]
names_after = list(raw[1])
status_after = list(raw[2])

# Cases that ran should be 4 (Finished)
finished_cases = [n for n, s in zip(names_after, status_after) if s == 4]

# --- Result ---
result["function"] = "SapModel.Analyze.GetCaseStatus"
result["cases_before"] = names_before
result["status_before"] = status_before
result["cases_after"] = names_after
result["status_after"] = status_after
result["finished_cases"] = finished_cases
result["status"] = "verified"
