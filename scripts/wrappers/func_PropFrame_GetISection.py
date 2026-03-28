# ============================================================
# Wrapper: SapModel.PropFrame.GetISection
# Category: PropFrame
# Description: Retrieve I-section properties
# Verified: 2026-03-28
# Prerequisites: Model open, I-section defined
# ============================================================
"""
Usage: Reads back the properties of an existing I/H frame section.

API Signature:
  SapModel.PropFrame.GetISection(Name, FileName, MatProp, T3, T2, TF, TW, T2B, TFB, Color, Notes, GUID)

ByRef Output:
  [FileName, MatProp, T3, T2, TF, TW, T2B, TFB, Color, Notes, GUID, ret_code]

Parameters:
  Name     : str   — Existing section name
  FileName : str   — (ByRef out) Section file name
  MatProp  : str   — (ByRef out) Material property name
  T3       : float — (ByRef out) Overall depth [L]
  T2       : float — (ByRef out) Top flange width [L]
  TF       : float — (ByRef out) Top flange thickness [L]
  TW       : float — (ByRef out) Web thickness [L]
  T2B      : float — (ByRef out) Bottom flange width [L]
  TFB      : float — (ByRef out) Bottom flange thickness [L]
  Color    : int   — (ByRef out) Display color
  Notes    : str   — (ByRef out) Notes
  GUID     : str   — (ByRef out) GUID
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_I", 1)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_I", 2.0e8, 0.3, 1.2e-5)
assert ret == 0

T3_set = 0.308
T2_set = 0.305
TF_set = 0.0154
TW_set = 0.00991
ret = SapModel.PropFrame.SetISection(
    "W310x97", "STEEL_I", T3_set, T2_set, TF_set, TW_set, T2_set, TF_set
)
assert ret == 0, f"SetISection failed: {ret}"

# --- Target function ---
raw = SapModel.PropFrame.GetISection("W310x97", "", "", 0, 0, 0, 0, 0, 0, 0, "", "")
ret_code = raw[-1]
assert ret_code == 0, f"GetISection failed: {ret_code}"

mat_prop = raw[1]
T3_got = raw[2]
T2_got = raw[3]
TF_got = raw[4]
TW_got = raw[5]

assert mat_prop == "STEEL_I", f"Material mismatch: expected STEEL_I, got {mat_prop}"
assert abs(T3_got - T3_set) < 0.001, f"T3 mismatch: set={T3_set}, got={T3_got}"
assert abs(T2_got - T2_set) < 0.001, f"T2 mismatch: set={T2_set}, got={T2_got}"
assert abs(TF_got - TF_set) < 0.001, f"TF mismatch: set={TF_set}, got={TF_got}"
assert abs(TW_got - TW_set) < 0.001, f"TW mismatch: set={TW_set}, got={TW_got}"

# --- Result ---
result["function"] = "SapModel.PropFrame.GetISection"
result["section_name"] = "W310x97"
result["material"] = mat_prop
result["T3"] = T3_got
result["T2"] = T2_got
result["TF"] = TF_got
result["TW"] = TW_got
result["byref_layout"] = "[FileName, MatProp, T3, T2, TF, TW, T2B, TFB, Color, Notes, GUID, ret_code]"
result["status"] = "verified"
