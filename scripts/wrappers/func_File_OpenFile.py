# ============================================================
# Wrapper: SapModel.File.OpenFile
# Category: File
# Description: Open an existing .sdb model file by path
# Verified: 2026-03-21
# Prerequisites: Connected to SAP2000, valid .sdb file path
# ============================================================
"""
Usage: Opens an existing SAP2000 model file. The file must have an
       .sdb, .$2k, .s2k, .xlsx, .xls, or .mdb extension.

API Signature:
  SapModel.File.OpenFile(FileName)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  FileName : str — Full path to the model file
"""
# --- Minimal setup: create a blank model, save it, then re-open ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Create a simple frame so the model isn't empty
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)  # Steel
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Save to a writable location (os/tempfile blocked in sandbox)
temp_path = r"C:\Users\fcoca\AppData\Local\Temp\test_open_file.sdb"
ret = SapModel.File.Save(temp_path)
assert ret == 0, f"Save failed: {ret}"

# Now re-initialize and open the saved file
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# --- Target function ---
ret = SapModel.File.OpenFile(temp_path)
assert ret == 0, f"OpenFile failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
assert frame_count >= 1, f"Expected at least 1 frame after open, got {frame_count}"

# --- Result ---
result["function"] = "SapModel.File.OpenFile"
result["file_path"] = temp_path
result["frame_count"] = frame_count
result["status"] = "verified"
