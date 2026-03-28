# ============================================================
# Wrapper: SapModel.PropFrame.GetRectangle
# Category: PropFrame
# Description: Retrieve rectangular section properties
# Verified: 2026-03-28
# Prerequisites: Model open, rectangular section defined
# ============================================================
"""
Usage: Reads back the properties of an existing rectangular frame section.

API Signature:
  SapModel.PropFrame.GetRectangle(Name, FileName, MatProp, T3, T2, Color, Notes, GUID)

ByRef Output:
  [FileName, MatProp, T3, T2, Color, Notes, GUID, ret_code]

Parameters:
  Name     : str   — Existing section name
  FileName : str   — (ByRef out) Section file name
  MatProp  : str   — (ByRef out) Material property name
  T3       : float — (ByRef out) Section depth [L]
  T2       : float — (ByRef out) Section width [L]
  Color    : int   — (ByRef out) Display color
  Notes    : str   — (ByRef out) Notes
  GUID     : str   — (ByRef out) GUID
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create material and rectangular section ---
ret = SapModel.PropMaterial.SetMaterial("CONC_R", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_R", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

T3_set = 0.6
T2_set = 0.3
ret = SapModel.PropFrame.SetRectangle("BEAM_30x60", "CONC_R", T3_set, T2_set)
assert ret == 0, f"SetRectangle failed: {ret}"

# --- Target function ---
raw = SapModel.PropFrame.GetRectangle("BEAM_30x60", "", "", 0, 0, 0, "", "")
ret_code = raw[-1]
assert ret_code == 0, f"GetRectangle failed: {ret_code}"

file_name = raw[0]
mat_prop = raw[1]
T3_got = raw[2]
T2_got = raw[3]

assert mat_prop == "CONC_R", f"Material mismatch: expected CONC_R, got {mat_prop}"
assert abs(T3_got - T3_set) < 0.001, f"T3 mismatch: set={T3_set}, got={T3_got}"
assert abs(T2_got - T2_set) < 0.001, f"T2 mismatch: set={T2_set}, got={T2_got}"

# --- Result ---
result["function"] = "SapModel.PropFrame.GetRectangle"
result["section_name"] = "BEAM_30x60"
result["material"] = mat_prop
result["T3"] = T3_got
result["T2"] = T2_got
result["byref_layout"] = "[FileName, MatProp, T3, T2, Color, Notes, GUID, ret_code]"
result["status"] = "verified"
