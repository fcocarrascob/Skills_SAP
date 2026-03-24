# ============================================================
# Wrapper: SapModel.DatabaseTables.GetAllFieldsInTable
# Category: Database_Tables
# Description: Returns all fields (columns) for a specific table
# Verified: true
# Prerequisites: Connected to SAP2000, model with at least one frame
# ============================================================
"""
Usage: Retrieves metadata about every field (column) in a specific table.
       Returns field keys, names, descriptions, units, and importability.

API Signature (VBA):
  SapModel.DatabaseTables.GetAllFieldsInTable(TableKey, TableVersion,
      NumberFields, FieldKey(), FieldName(), Description(), UnitsString(),
      IsImportable())

ByRef Output (COM Python):
  raw[0] = TableVersion  (int)
  raw[1] = NumberFields   (int)
  raw[2] = FieldKey[]     (tuple of str)
  raw[3] = FieldName[]    (tuple of str)
  raw[4] = Description[]  (tuple of str)
  raw[5] = UnitsString[]  (tuple of str)
  raw[6] = IsImportable[] (tuple of bool)
  raw[-1] = ret_code      (0=success)

Parameters:
  TableKey : str — The table key to query (e.g. "Material Properties 01 - General")
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

# --- Discover a valid table key ---
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0, f"GetAllTables failed: {raw_tables[-1]}"
all_keys = list(raw_tables[1])
# Pick a table that should exist in any model with materials
test_key = None
for k in all_keys:
    if "Material Properties" in k:
        test_key = k
        break
assert test_key is not None, "Could not find a Material Properties table"

# --- Target function ---
raw = SapModel.DatabaseTables.GetAllFieldsInTable(
    test_key, 0, 0, [], [], [], [], []
)
table_version = raw[0]
num_fields = raw[1]
field_keys = list(raw[2])
field_names = list(raw[3])
descriptions = list(raw[4])
units_strings = list(raw[5])
is_importable = list(raw[6])
ret_code = raw[-1]
assert ret_code == 0, f"GetAllFieldsInTable failed: {ret_code}"

# --- Verification ---
assert num_fields > 0, f"Expected fields > 0, got {num_fields}"
assert len(field_keys) == num_fields, "FieldKey count mismatch"
assert len(field_names) == num_fields, "FieldName count mismatch"
assert len(descriptions) == num_fields, "Description count mismatch"
assert len(units_strings) == num_fields, "UnitsString count mismatch"
assert len(is_importable) == num_fields, "IsImportable count mismatch"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetAllFieldsInTable"
result["table_key"] = test_key
result["table_version"] = table_version
result["num_fields"] = num_fields
result["field_keys"] = field_keys
result["field_names"] = field_names
result["sample_units"] = units_strings[:5]
result["importable_count"] = sum(1 for v in is_importable if v)
result["status"] = "verified"
