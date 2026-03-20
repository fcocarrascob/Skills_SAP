# ============================================================
# Wrapper: SapModel.Func.FuncRS.SetUser
# Category: Functions
# Description: Define a user-defined response spectrum function
# Verified: 2026-03-20
# Prerequisites: Model open
# ============================================================
"""
Usage: Defines a user response spectrum curve given period-value pairs.
       The spectrum is then available for assignment to response spectrum
       load cases. Use for site-specific spectra (e.g., NCh 2745).

API Signature:
  SapModel.Func.FuncRS.SetUser(Name, NumberItems, Period, Value, DampRatio)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name        : str     — Function name
  NumberItems : int     — Number of period-value pairs
  Period      : float[] — Array of period values [s]
  Value       : float[] — Array of spectral acceleration values [g or L/T^2]
  DampRatio   : float   — Damping ratio (default=0.05 for 5%)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: define a simple 5-point response spectrum ---
# Simplified NCh 2745 Zone 3, Soil Type II style spectrum
func_name = "RS_NCh2745_Z3_S2"
periods = [0.0, 0.15, 0.50, 1.50, 4.00]
values  = [0.40, 1.00, 1.00, 0.33, 0.125]
num_points = len(periods)

raw = SapModel.Func.FuncRS.SetUser(
    func_name,
    num_points,
    periods,
    values,
    0.05  # 5% damping
)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, f"FuncRS.SetUser failed: {raw}"

# Create a second spectrum for comparison
func_name_2 = "RS_FLAT_05g"
periods_2 = [0.0, 0.10, 3.00]
values_2  = [0.50, 0.50, 0.50]

raw = SapModel.Func.FuncRS.SetUser(
    func_name_2,
    len(periods_2),
    periods_2,
    values_2,
    0.05
)
ret = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret == 0, f"FuncRS.SetUser(flat) failed: {raw}"

# --- Verification ---
# Read back the first spectrum function
raw = SapModel.Func.FuncRS.GetUser(func_name, 0, [], [], 0)
ret_code = raw[-1]
assert ret_code == 0, f"FuncRS.GetUser failed: {ret_code}"
read_count = raw[0]
assert read_count == num_points, f"Expected {num_points} points, got {read_count}"

# --- Result ---
result["function"] = "SapModel.Func.FuncRS.SetUser"
result["spectra_created"] = [func_name, func_name_2]
result["num_points"] = read_count
result["status"] = "verified"
