# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForDisplayArray
# Category: Database_Tables
# Description: Read table data for display (read-only) as flat array
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Retrieves table data for display purposes. Unlike GetTableForEditingArray,
       allows specifying which fields to include and works for read-only tables.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList(),
      GroupName, TableVersion, FieldKeysIncluded(), NumberRecords, TableData())

ByRef Output (COM Python):
  raw[0] = FieldKeyList[]      (tuple of str — echoed input)
  raw[1] = TableVersion        (int)
  raw[2] = FieldKeysIncluded[] (tuple of str)
  raw[3] = NumberRecords       (int)
  raw[4] = TableData[]         (tuple of str — flat row-by-row data)
  raw[-1] = ret_code           (0=success)

Parameters:
  TableKey     : str   — Table key to read
  FieldKeyList : str[] — Fields to include ([""] for all)
  GroupName    : str   — Group filter ("All" or "" for all)
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

# --- Discover a non-empty table ---
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0
all_keys = list(raw_tables[1])
all_empty = list(raw_tables[4])

test_key = None
for i, k in enumerate(all_keys):
    if not all_empty[i]:
        test_key = k
        break
assert test_key is not None, "No non-empty table found"

# --- Target function: get ALL fields ---
raw = SapModel.DatabaseTables.GetTableForDisplayArray(
    test_key, [""], "All", 0, [], 0, []
)
# raw[0] = FieldKeyList (echoed), raw[1] = TableVersion, raw[2] = FieldKeysIncluded[],
# raw[3] = NumberRecords, raw[4] = TableData[], raw[-1] = ret_code
table_version = raw[1]
field_keys = list(raw[2])
num_records = raw[3]
table_data = list(raw[4]) if raw[4] else []
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForDisplayArray failed: {ret_code}"

# --- Verification ---
assert len(field_keys) > 0, "Expected at least one field"
if num_records > 0:
    expected_len = len(field_keys) * num_records
    assert len(table_data) == expected_len, (
        f"TableData length {len(table_data)} != fields({len(field_keys)}) * records({num_records})"
    )

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForDisplayArray"
result["table_key"] = test_key
result["table_version"] = table_version
result["field_keys"] = field_keys
result["num_records"] = num_records
result["sample_data"] = table_data[:20]
result["status"] = "verified"
