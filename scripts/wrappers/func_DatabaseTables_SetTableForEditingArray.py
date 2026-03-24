# ============================================================
# Wrapper: SapModel.DatabaseTables.SetTableForEditingArray
# Category: Database_Tables
# Description: Write edited table data back for import
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Stores modified table data for later import via ApplyEditedTables.
       The data format matches GetTableForEditingArray output (flat array).

API Signature (VBA):
  SapModel.DatabaseTables.SetTableForEditingArray(TableKey, TableVersion,
      FieldKeysIncluded(), NumberRecords, TableData())

ByRef Output (COM Python):
  raw[0] = TableVersion       (int — echoed back)
  raw[1] = FieldKeysIncluded[] (tuple of str — echoed back)
  raw[2] = TableData[]         (tuple of str — echoed back)
  raw[-1] = ret_code           (0=success)

Parameters:
  TableKey           : str     — Table key to write
  TableVersion       : int     — Version from GetTableForEditingArray
  FieldKeysIncluded  : str[]   — Column headers (field keys)
  NumberRecords      : int     — Number of data rows
  TableData          : str[]   — Flat row-by-row data
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

# --- Read an editable table first ---
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
assert raw[-1] == 0, f"GetTableForEditingArray failed: {raw[-1]}"
assert num_records > 0, "Need at least one record to test SetTableForEditingArray"

# Cancel the get — clean state before set
SapModel.DatabaseTables.CancelTableEditing()

# --- Target function: write the same data back (round-trip) ---
raw = SapModel.DatabaseTables.SetTableForEditingArray(
    test_key, table_version, field_keys, num_records, table_data
)
ret_code = raw[-1] if isinstance(raw, (tuple, list)) else raw
assert ret_code == 0, f"SetTableForEditingArray failed: {ret_code}"

# Cancel to clean up (don't apply changes for this test)
SapModel.DatabaseTables.CancelTableEditing()

# --- Result ---
result["function"] = "SapModel.DatabaseTables.SetTableForEditingArray"
result["table_key"] = test_key
result["table_version"] = table_version
result["field_keys"] = field_keys
result["num_records"] = num_records
result["status"] = "verified"
