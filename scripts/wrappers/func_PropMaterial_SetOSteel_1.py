# ============================================================
# Wrapper: SapModel.PropMaterial.SetOSteel_1
# Category: PropMaterial
# Description: Set steel design properties (ASTM/EN overstrength)
# Verified: 2026-03-28
# Prerequisites: Model open, steel material defined via SetMaterial
# ============================================================
"""
Usage: Assigns steel design properties to an existing steel material.
       Defines yield/ultimate strengths all needed for steel design checks.

API Signature:
  SapModel.PropMaterial.SetOSteel_1(Name, Fy, Fu, EFy, EFu,
    SSType, SSHysType, StrainAtHardening, StrainAtMaxStress,
    StrainAtRupture, FinalSlope)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name              : str   — Existing steel material name
  Fy                : float — Minimum yield stress [F/L^2]
  Fu                : float — Minimum tensile stress [F/L^2]
  EFy               : float — Expected yield stress [F/L^2]
  EFu               : float — Expected tensile stress [F/L^2]
  SSType            : int   — Stress-strain curve type (0=User, 1=Parametric-Simple)
  SSHysType         : int   — Stress-strain hysteresis type (0=Elastic, 1=Kinematic, 2=Takeda, 3=Pivot)
  StrainAtHardening : float — Strain at onset of strain hardening
  StrainAtMaxStress : float — Strain at maximum stress
  StrainAtRupture   : float — Strain at rupture
  FinalSlope        : float — Final slope of stress-strain curve (negative for softening)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create steel material ---
ret = SapModel.PropMaterial.SetMaterial("A992_TEST", 1)  # 1=Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("A992_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function: set steel design properties ---
# A992 Fy=345 MPa = 345000 kN/m2, Fu=450 MPa = 450000 kN/m2
ret = SapModel.PropMaterial.SetOSteel_1(
    "A992_TEST",
    345000,    # Fy  [kN/m^2]
    450000,    # Fu  [kN/m^2]
    379500,    # EFy (1.1 × Fy)
    495000,    # EFu (1.1 × Fu)
    1,         # SSType — Parametric-Simple
    1,         # SSHysType — Kinematic
    0.02,      # StrainAtHardening
    0.10,      # StrainAtMaxStress
    0.20,      # StrainAtRupture
    -0.10      # FinalSlope
)
assert ret == 0, f"SetOSteel_1 failed: {ret}"

# Second steel: A36
ret = SapModel.PropMaterial.SetMaterial("A36_TEST", 1)
assert ret == 0, f"SetMaterial(A36) failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("A36_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetOSteel_1(
    "A36_TEST",
    250000,    # Fy  [kN/m^2]
    400000,    # Fu  [kN/m^2]
    275000,    # EFy
    440000,    # EFu
    1, 1, 0.02, 0.10, 0.20, -0.10
)
assert ret == 0, f"SetOSteel_1(A36) failed: {ret}"

# --- Verification: material exists ---
raw = SapModel.PropMaterial.GetNameList(0, [])
assert raw[-1] == 0, f"GetNameList failed: {raw[-1]}"
mat_names = list(raw[1])
assert "A992_TEST" in mat_names, f"A992_TEST not found in: {mat_names}"
assert "A36_TEST" in mat_names, f"A36_TEST not found in: {mat_names}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.SetOSteel_1"
result["materials_configured"] = ["A992_TEST", "A36_TEST"]
result["material_count"] = raw[0]
result["status"] = "verified"
