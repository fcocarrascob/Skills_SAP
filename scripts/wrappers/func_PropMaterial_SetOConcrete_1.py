# ============================================================
# Wrapper: SapModel.PropMaterial.SetOConcrete_1
# Category: PropMaterial
# Description: Set concrete design properties (fc, strain model)
# Verified: 2026-03-28
# Prerequisites: Model open, concrete material defined via SetMaterial
# ============================================================
"""
Usage: Assigns concrete design properties to an existing concrete material.
       Defines compressive strength and stress-strain model for design checks.

API Signature:
  SapModel.PropMaterial.SetOConcrete_1(Name, fc, IsLightweight,
    FcsFactor, SSType, SSHysType, StrainAtfc,
    StrainUltimate, FinalSlope, FrictionAngle, DilatationalAngle)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name              : str   — Existing concrete material name
  fc                : float — Concrete compressive strength [F/L^2]
  IsLightweight     : bool  — True if lightweight concrete
  FcsFactor         : float — Concrete stress-strain factor (typically 0 for confined)
  SSType            : int   — Stress-strain type (0=User, 1=Parametric-Simple)
  SSHysType         : int   — Hysteresis type (0=Elastic, 1=Kinematic, 2=Takeda, 3=Pivot)
  StrainAtfc        : float — Strain at fc
  StrainUltimate    : float — Ultimate strain capacity
  FinalSlope        : float — Final slope (negative for softening)
  FrictionAngle     : float — Friction angle [deg] (default 0)
  DilatationalAngle : float — Dilatational angle [deg] (default 0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create concrete material ---
ret = SapModel.PropMaterial.SetMaterial("CONC_28", 2)  # 2=Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_28", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function: set concrete design properties ---
# fc=28 MPa = 28000 kN/m2
ret = SapModel.PropMaterial.SetOConcrete_1(
    "CONC_28",
    28000,     # fc [kN/m^2]
    False,     # IsLightweight
    0,         # FcsFactor
    1,         # SSType — Parametric-Simple
    1,         # SSHysType — Kinematic
    0.002,     # StrainAtfc
    0.005,     # StrainUltimate
    -0.10,     # FinalSlope
    0,         # FrictionAngle
    0          # DilatationalAngle
)
assert ret == 0, f"SetOConcrete_1 failed: {ret}"

# Second concrete: H30
ret = SapModel.PropMaterial.SetMaterial("CONC_H30", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_H30", 2.65e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetOConcrete_1(
    "CONC_H30",
    25000, False, 0, 1, 1, 0.002, 0.005, -0.10, 0, 0
)
assert ret == 0, f"SetOConcrete_1(H30) failed: {ret}"

# --- Verification ---
raw = SapModel.PropMaterial.GetNameList(0, [])
assert raw[-1] == 0, f"GetNameList failed: {raw[-1]}"
mat_names = list(raw[1])
assert "CONC_28" in mat_names, f"CONC_28 not found in: {mat_names}"
assert "CONC_H30" in mat_names, f"CONC_H30 not found in: {mat_names}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.SetOConcrete_1"
result["materials_configured"] = ["CONC_28", "CONC_H30"]
result["material_count"] = raw[0]
result["status"] = "verified"
