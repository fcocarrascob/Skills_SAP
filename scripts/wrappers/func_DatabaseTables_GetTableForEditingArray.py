# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForEditingArray
# Category: Database_Tables
# Description: Read a table as flat array for interactive editing
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Retrieves table data in a flat string array, suitable for
       editing and re-importing via SetTableForEditingArray.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForEditingArray(TableKey, GroupName,
      TableVersion, FieldKeysIncluded(), NumberRecords, TableData())

ByRef Output (COM Python):
  raw[0] = TableVersion       (int)
  raw[1] = FieldKeysIncluded[] (tuple of str — column headers)
  raw[2] = NumberRecords       (int — row count)
  raw[3] = TableData[]         (tuple of str — flat row-by-row data)
  raw[-1] = ret_code           (0=success)

Parameters:
  TableKey  : str — Table key to read
  GroupName : str — Group filter ("All" or "" for all objects)
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

# --- Discover an editable table ---
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0, f"GetAllTables failed"
all_keys = list(raw_tables[1])
all_import = list(raw_tables[3])
all_empty = list(raw_tables[4])

# Find a non-empty, editable table
test_key = None
for i, k in enumerate(all_keys):
    if all_import[i] >= 2 and not all_empty[i]:
        test_key = k
        break
if test_key is None:
    for i, k in enumerate(all_keys):
        if not all_empty[i]:
            test_key = k
            break
assert test_key is not None, "No non-empty table found"

# --- Target function ---
raw = SapModel.DatabaseTables.GetTableForEditingArray(test_key, "All", 0, [], 0, [])
table_version = raw[0]
field_keys = list(raw[1])
num_records = raw[2]
table_data = list(raw[3]) if raw[3] else []
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForEditingArray failed: {ret_code}"

# --- Verification ---
assert len(field_keys) > 0, "Expected at least one field"
assert num_records >= 0, f"Unexpected negative records: {num_records}"
if num_records > 0:
    expected_len = len(field_keys) * num_records
    assert len(table_data) == expected_len, (
        f"TableData length {len(table_data)} != fields({len(field_keys)}) * records({num_records})"
    )

# Cancel editing to clean state
SapModel.DatabaseTables.CancelTableEditing()

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForEditingArray"
result["table_key"] = test_key
result["table_version"] = table_version
result["field_keys"] = field_keys
result["num_records"] = num_records
result["sample_data"] = table_data[:20]
result["status"] = "verified"
