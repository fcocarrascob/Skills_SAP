# ============================================================
# Wrapper: SapModel.LoadCases.ResponseSpectrum.SetLoads
# Category: Load_Cases
# Description: Assign response spectrum loads to a spectrum load case
# Verified: 2026-03-20
# Prerequisites: Model open, spectrum function and load case exist
# ============================================================
"""
Usage: Assigns directional spectrum loads to a response spectrum load case.
       Each direction (U1, U2, U3) can reference a different spectrum
       function with a scale factor.

API Signature:
  SapModel.LoadCases.ResponseSpectrum.SetLoads(Name, NumberLoads,
      LoadName, Func, SF, CSys, Ang)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name        : str     — Response spectrum load case name
  NumberLoads : int     — Number of directional loads (typically 1-3)
  LoadName    : str[]   — Load directions: "U1"=X, "U2"=Y, "U3"=Z
  Func        : str[]   — Spectrum function names for each direction
  SF          : float[] — Scale factors (typically 9.81 to convert g→m/s²)
  CSys        : str[]   — Coordinate system for each load
  Ang         : float[] — Angle of application [degrees]
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
# 1) Define a response spectrum function
func_name = "RS_TEST"
periods = [0.0, 0.15, 0.50, 2.00]
values  = [0.40, 1.00, 1.00, 0.25]
raw = SapModel.Func.FuncRS.SetUser(func_name, len(periods), periods, values, 0.05)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, f"FuncRS.SetUser failed: {raw}"

# 2) Create a seismic load pattern (needed for modal mass source)
ret = SapModel.LoadPatterns.Add("QUAKE_X", 5)  # 5=Quake
assert ret == 0, f"LoadPatterns.Add(QUAKE_X) failed: {ret}"

ret = SapModel.LoadPatterns.Add("QUAKE_Y", 5)
assert ret == 0, f"LoadPatterns.Add(QUAKE_Y) failed: {ret}"

# 3) The load case "QUAKE_X" is auto-created as LinStatic;
#    we need a ResponseSpectrum load case instead.
#    Create a new RS load case.
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("RS_X")
assert ret == 0, f"ResponseSpectrum.SetCase(RS_X) failed: {ret}"

ret = SapModel.LoadCases.ResponseSpectrum.SetCase("RS_XY")
assert ret == 0, f"ResponseSpectrum.SetCase(RS_XY) failed: {ret}"

# --- Target function: assign spectrum loads ---
# Single direction: X only
raw = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "RS_X",              # Load case name
    1,                   # NumberLoads
    ["U1"],              # LoadName — X direction
    [func_name],         # Func — spectrum function
    [9.81],              # SF — g to m/s²
    ["Global"],          # CSys
    [0.0]                # Ang
)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, f"SetLoads(RS_X) failed: {raw}"

# Two directions: X + Y
raw = SapModel.LoadCases.ResponseSpectrum.SetLoads(
    "RS_XY",             # Load case name
    2,                   # NumberLoads
    ["U1", "U2"],        # LoadName — X and Y
    [func_name, func_name],  # Same spectrum both directions
    [9.81, 9.81],        # SF
    ["Global", "Global"],# CSys
    [0.0, 0.0]           # Ang
)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, f"SetLoads(RS_XY) failed: {raw}"

# --- Verification ---
# Read back loads for RS_XY
raw = SapModel.LoadCases.ResponseSpectrum.GetLoads("RS_XY", 0, [], [], [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoads failed: {ret_code}"
num_loads = raw[0]
assert num_loads == 2, f"Expected 2 loads, got {num_loads}"

# Verify load case exists in case list
raw = SapModel.LoadCases.GetNameList(0, [])
assert raw[-1] == 0, f"GetNameList failed: {raw[-1]}"
case_names = list(raw[1])
assert "RS_X" in case_names, f"RS_X not found in: {case_names}"
assert "RS_XY" in case_names, f"RS_XY not found in: {case_names}"

# --- Result ---
result["function"] = "SapModel.LoadCases.ResponseSpectrum.SetLoads"
result["cases_configured"] = ["RS_X", "RS_XY"]
result["rs_xy_num_loads"] = num_loads
result["status"] = "verified"
