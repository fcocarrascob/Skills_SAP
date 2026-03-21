# ============================================================
# Wrapper: SapModel.DesignSteel.StartDesign
# Category: Design
# Description: Run steel frame design check
# Verified: 2026-03-21
# Prerequisites: Model analyzed, steel design code set
# ============================================================
"""
Usage: Starts the steel frame design procedure. The model must
       be analyzed first. The steel design code should be set
       before calling this function.

API Signature:
  SapModel.DesignSteel.StartDesign() -> ret_code

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

# --- Prerequisites: steel material & section ---
ret = SapModel.PropMaterial.SetMaterial("A992Fy50", 1)  # Steel
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("A992Fy50", 2.0e8, 0.3, 1.2e-5)
assert ret == 0
ret = SapModel.PropFrame.SetISection(
    "W310x97", "A992Fy50",
    0.308, 0.305, 0.0154, 0.00991, 0.305, 0.0154  # d, bf, tf, tw, bfb, tfb
)
assert ret == 0

# Simple portal: 2 columns + 1 beam
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 4, "", "W310x97", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(8, 0, 0, 8, 0, 4, "", "W310x97", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 4, 8, 0, 4, "", "W310x97", "")
assert beam[-1] == 0

# Supports: pin bases (joint "1"=base of col1, joint "3"=base of col2)
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("3", [True, True, True, True, True, True])
assert ret[-1] == 0

# Load pattern (dead already exists, add live)
ret = SapModel.LoadPatterns.Add("LIVE", 3)  # 3=Live
assert ret == 0

# Distributed load on beam
ret = SapModel.FrameObj.SetLoadDistributed(
    beam[0], "DEAD", 1, 10, 0, 1, -10, -10, "Global", True, True
)
assert ret == 0

# Set steel design code
ret = SapModel.DesignSteel.SetCode("AISC 360-16")
assert ret == 0

# Save model before analysis (required by SAP2000)
ret = SapModel.File.Save(r"C:\Temp\sap_design_steel.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# Analyze model
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# --- Target function ---
ret = SapModel.DesignSteel.StartDesign()
assert ret == 0, f"DesignSteel.StartDesign failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.StartDesign"
result["design_code"] = "AISC 360-16"
result["status"] = "verified"
