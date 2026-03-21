# ============================================================
# Wrapper: SapModel.DesignConcrete.StartDesign
# Category: Design
# Description: Run concrete frame design check
# Verified: 2026-03-21
# Prerequisites: Model analyzed, concrete design code set
# ============================================================
"""
Usage: Starts the concrete frame design procedure. The model must
       be analyzed first. The concrete design code should be set
       before calling this function.

API Signature:
  SapModel.DesignConcrete.StartDesign() -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  (none)
"""

# --- Minimal setup (portal frame for design) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites: concrete material & section ---
ret = SapModel.PropMaterial.SetMaterial("CONC28", 2)  # 2=Concrete
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC28", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("COL_40x40", "CONC28", 0.4, 0.4)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30x50", "CONC28", 0.5, 0.3)
assert ret == 0

# Simple portal: 2 columns + 1 beam
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "COL_40x40", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(5, 0, 0, 5, 0, 3, "", "COL_40x40", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "BEAM_30x50", "")
assert beam[-1] == 0

# Supports: fixed bases (joint "1"=base of col1, joint "3"=base of col2)
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("3", [True, True, True, True, True, True])
assert ret[-1] == 0

# Gravity load on beam
ret = SapModel.FrameObj.SetLoadDistributed(
    beam[0], "DEAD", 1, 10, 0, 1, -15, -15, "Global", True, True
)
assert ret == 0

# Set concrete design code
ret = SapModel.DesignConcrete.SetCode("ACI 318-19")
assert ret == 0

# Save model before analysis (required by SAP2000)
ret = SapModel.File.Save(r"C:\Temp\sap_design_concrete.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# Analyze model
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# --- Target function ---
ret = SapModel.DesignConcrete.StartDesign()
assert ret == 0, f"DesignConcrete.StartDesign failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignConcrete.StartDesign"
result["design_code"] = "ACI 318-19"
result["status"] = "verified"
