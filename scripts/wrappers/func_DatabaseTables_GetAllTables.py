# ============================================================
# Wrapper: SapModel.DatabaseTables.GetAllTables
# Category: Database_Tables
# Description: Returns all tables with import type and empty status
# Verified: true
# Prerequisites: Connected to SAP2000, model with at least one frame
# ============================================================
"""
Usage: Enumerates every table available in the current model, including
       whether each table is importable and whether it contains data.

API Signature (VBA):
  SapModel.DatabaseTables.GetAllTables(NumberTables, TableKey(), TableName(), ImportType(), IsEmpty())

ByRef Output (COM Python):
  raw[0] = NumberTables (int)
  raw[1] = TableKey[]   (tuple of str)
  raw[2] = TableName[]  (tuple of str)
  raw[3] = ImportType[] (tuple of int: 0=not importable, 1=importable non-interactive,
                         2=interactive unlocked, 3=interactive any)
  raw[4] = IsEmpty[]    (tuple of bool)
  raw[-1] = ret_code    (0=success)

Parameters:
  (none — all outputs are ByRef)
"""

# --- Minimal setup: model with at least one element ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Add a material + section + frame so tables have data
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# --- Target function ---
raw = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
num_tables = raw[0]
table_keys = list(raw[1])
table_names = list(raw[2])
import_types = list(raw[3])
is_empty = list(raw[4])
ret_code = raw[-1]
assert ret_code == 0, f"GetAllTables failed: {ret_code}"

# --- Verification ---
assert num_tables > 0, f"Expected tables > 0, got {num_tables}"
assert len(table_keys) == num_tables, "TableKey count mismatch"
assert len(table_names) == num_tables, "TableName count mismatch"
assert len(import_types) == num_tables, "ImportType count mismatch"
assert len(is_empty) == num_tables, "IsEmpty count mismatch"

# Check known tables exist
known_tables = [k for k in table_keys if "Material" in k or "Frame" in k]
assert len(known_tables) > 0, "Expected material/frame tables in model with elements"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetAllTables"
result["num_tables"] = num_tables
result["sample_keys"] = table_keys[:10]
result["sample_names"] = table_names[:10]
result["sample_import_types"] = import_types[:10]
result["non_empty_count"] = sum(1 for e in is_empty if not e)
result["status"] = "verified"
