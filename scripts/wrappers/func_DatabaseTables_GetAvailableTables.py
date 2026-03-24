# ============================================================
# Wrapper: SapModel.DatabaseTables.GetAvailableTables
# Category: Database_Tables
# Description: Returns available tables with their import type
# Verified: true
# Prerequisites: Connected to SAP2000, model with at least one frame
# ============================================================
"""
Usage: Returns tables available for display (similar to GetAllTables but
       without the IsEmpty array — lighter query).

API Signature (VBA):
  SapModel.DatabaseTables.GetAvailableTables(NumberTables, TableKey(), TableName(), ImportType())

ByRef Output (COM Python):
  raw[0] = NumberTables (int)
  raw[1] = TableKey[]   (tuple of str)
  raw[2] = TableName[]  (tuple of str)
  raw[3] = ImportType[] (tuple of int)
  raw[-1] = ret_code    (0=success)

Parameters:
  (none — all outputs are ByRef)
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

# --- Target function ---
raw = SapModel.DatabaseTables.GetAvailableTables(0, [], [], [])
num_tables = raw[0]
table_keys = list(raw[1])
table_names = list(raw[2])
import_types = list(raw[3])
ret_code = raw[-1]
assert ret_code == 0, f"GetAvailableTables failed: {ret_code}"

# --- Verification ---
assert num_tables > 0, f"Expected tables > 0, got {num_tables}"
assert len(table_keys) == num_tables, "TableKey count mismatch"
assert len(table_names) == num_tables, "TableName count mismatch"
assert len(import_types) == num_tables, "ImportType count mismatch"

# All import types should be 0, 1, 2, or 3
for it in import_types:
    assert it in (0, 1, 2, 3), f"Invalid ImportType: {it}"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetAvailableTables"
result["num_tables"] = num_tables
result["sample_keys"] = table_keys[:10]
result["sample_names"] = table_names[:10]
result["importable_count"] = sum(1 for it in import_types if it > 0)
result["status"] = "verified"
