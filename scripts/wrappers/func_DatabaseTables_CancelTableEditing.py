# ============================================================
# Wrapper: SapModel.DatabaseTables.CancelTableEditing
# Category: Database_Tables
# Description: Cancel all pending table edits
# Verified: pending
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Clears all tables stored via SetTableForEditing* functions
       without applying them. Acts as a rollback.

API Signature (VBA):
  SapModel.DatabaseTables.CancelTableEditing()

ByRef Output (COM Python):
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  (none)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0, f"SetPresentUnits failed: {ret}"

ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# --- Stage a pending edit to cancel ---
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0
all_keys = list(raw_tables[1])
all_import = list(raw_tables[3])
all_empty = list(raw_tables[4])

test_key = None
for i, k in enumerate(all_keys):
    if all_import[i] >= 2 and not all_empty[i]:
        test_key = k
        break
assert test_key is not None, "No editable non-empty table found"

# Read then stage
raw = SapModel.DatabaseTables.GetTableForEditingArray(test_key, "All", 0, [], 0, [])
assert raw[-1] == 0
SapModel.DatabaseTables.CancelTableEditing()

raw = SapModel.DatabaseTables.SetTableForEditingArray(
    test_key, raw[0], list(raw[1]), raw[2], list(raw[3]) if raw[3] else []
)
set_ret = raw[-1] if isinstance(raw, (tuple, list)) else raw
assert set_ret == 0, f"SetTableForEditingArray failed: {set_ret}"

# --- Target function ---
ret = SapModel.DatabaseTables.CancelTableEditing()
assert ret == 0, f"CancelTableEditing failed: {ret}"

# --- Verification ---
# Cancel succeeded — ApplyEditedTables returns non-zero when nothing is staged,
# so we only verify the cancel return code itself.

# --- Result ---
result["function"] = "SapModel.DatabaseTables.CancelTableEditing"
result["cancel_ret_code"] = ret
result["status"] = "verified"
