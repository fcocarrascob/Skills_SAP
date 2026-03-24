# ============================================================
# Wrapper: SapModel.DatabaseTables.ApplyEditedTables
# Category: Database_Tables
# Description: Apply all pending table edits to the model
# Verified: pending
# Prerequisites: Connected to SAP2000, pending table edits via SetTableForEditing*
# ============================================================
"""
Usage: Imports all tables stored via SetTableForEditing* functions.
       Returns error/warning/info message counts and optional log.

API Signature (VBA):
  SapModel.DatabaseTables.ApplyEditedTables(FillImportLog,
      NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

ByRef Output (COM Python):
  raw[0] = NumFatalErrors (int)
  raw[1] = NumErrorMsgs   (int)
  raw[2] = NumWarnMsgs    (int)
  raw[3] = NumInfoMsgs    (int)
  raw[4] = ImportLog      (str)
  raw[-1] = ret_code      (0=success)

Parameters:
  FillImportLog : bool — True to populate the ImportLog string
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

# --- Read→Set round trip to stage a pending edit ---
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

raw = SapModel.DatabaseTables.GetTableForEditingArray(test_key, "All", 0, [], 0, [])
table_version = raw[0]
field_keys = list(raw[1])
num_records = raw[2]
table_data = list(raw[3]) if raw[3] else []
assert raw[-1] == 0
SapModel.DatabaseTables.CancelTableEditing()

# Stage the same data back
raw = SapModel.DatabaseTables.SetTableForEditingArray(
    test_key, table_version, field_keys, num_records, table_data
)
set_ret = raw[-1] if isinstance(raw, (tuple, list)) else raw
assert set_ret == 0, f"SetTableForEditingArray failed: {set_ret}"

# --- Target function ---
raw = SapModel.DatabaseTables.ApplyEditedTables(True, 0, 0, 0, 0, "")
num_fatal = raw[0]
num_errors = raw[1]
num_warnings = raw[2]
num_info = raw[3]
import_log = raw[4]
ret_code = raw[-1]
assert ret_code == 0, f"ApplyEditedTables failed: {ret_code}"

# --- Verification ---
assert num_fatal == 0, f"Fatal errors during import: {num_fatal}"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.ApplyEditedTables"
result["num_fatal_errors"] = num_fatal
result["num_error_msgs"] = num_errors
result["num_warn_msgs"] = num_warnings
result["num_info_msgs"] = num_info
result["import_log_length"] = len(import_log) if import_log else 0
result["status"] = "verified"
