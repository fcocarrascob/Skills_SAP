# Database Tables — SAP2000 Module

Module for exploring and editing SAP2000 database tables via direct COM connection.

## Components

| File | Description |
|------|-------------|
| `backend_database_tables.py` | Backend class with high-level table operations |
| `gui_database_tables.py` | PySide6 GUI with table browser and conditional editing |

## Backend API

```python
from backend_database_tables import SapConnection, DatabaseTablesBackend

conn = SapConnection()
conn.connect()
backend = DatabaseTablesBackend(conn)

# List all tables with data
tables = backend.list_tables(include_empty=False)

# Read table as structured rows
data = backend.read_table("Material Properties 01 - General")

# Get field metadata
fields = backend.get_table_fields("Material Properties 01 - General")

# Export to CSV file
backend.export_csv("Material Properties 01 - General", "C:\\temp\\materials.csv")

# Export as CSV/XML strings
csv_str = backend.export_csv_string("Material Properties 01 - General")
xml_str = backend.export_xml_string("Material Properties 01 - General")

# Write table (edit model)
result = backend.write_table(table_key, field_keys, rows)

# Import from CSV file
result = backend.import_csv(table_key, "C:\\temp\\materials.csv")

# Check model lock state
locked = backend.is_model_locked()

conn.disconnect()
```

## GUI Features

- **Table browser**: TreeView with all available tables (filterable)
- **Data viewer**: QTableWidget showing table data with field headers and units
- **Export**: CSV file, XML string export
- **Import**: CSV file import with Apply/Cancel
- **Conditional editing**: Inline editing when model is unlocked; read-only when locked
- **Lock indicator**: Real-time 🔒/🔓 status with 2-second polling

## Wrapper Coverage

18 wrapper scripts in `scripts/wrappers/func_DatabaseTables_*.py` covering all 37 API functions.
See `scripts/registry.json` for the complete registry (category: `Database_Tables`).

## Table Data Format

TableData is a **flat array** stored row-by-row:
```
[field1_row1, field2_row1, ..., fieldN_row1, field1_row2, ...]
```

The backend's `read_table()` converts this to a list of dicts for easy manipulation.

## Import Types

| Code | Meaning |
|------|---------|
| 0 | Not importable |
| 1 | Importable (non-interactive) |
| 2 | Interactive import when model is unlocked |
| 3 | Interactive import when model is unlocked or locked |
