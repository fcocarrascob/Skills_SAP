"""
Backend — SAP2000 Database Tables Explorer (Standalone)
========================================================
Provides high-level methods to list, read, write, and export SAP2000
database tables via direct COM connection (no MCP dependency).

Connection: COM directo vía comtypes.client
"""

import math
import tempfile
import comtypes.client
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo)
# ══════════════════════════════════════════════════════════════════════════════

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""

    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing: bool = True) -> dict:
        try:
            if attach_to_existing:
                self.sap_object = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject"
                )
            else:
                helper = comtypes.client.CreateObject("SAP2000v1.Helper")
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
                self.sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                self.sap_object.ApplicationStart()

            self.sap_model = self.sap_object.SapModel
            version = str(self.sap_object.GetOAPIVersionNumber())
            model_path = str(self.sap_model.GetModelFilename())
            return {"connected": True, "version": version, "model_path": model_path}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseTablesBackend:
    """Backend standalone para explorar y editar Database Tables de SAP2000."""

    IMPORT_TYPE_LABELS = {
        0: "Not importable",
        1: "Importable (non-interactive)",
        2: "Interactive (unlocked only)",
        3: "Interactive (unlocked + locked)",
    }

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Metadata ──────────────────────────────────────────────────────────

    def list_tables(self, include_empty: bool = True) -> List[Dict[str, Any]]:
        """Returns all tables with metadata.

        Args:
            include_empty: If False, filters out tables with no data.

        Returns:
            List of dicts with keys: table_key, table_name, import_type,
            import_label, is_empty.
        """
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetAllTables failed: {ret_code}")

        num = raw[0]
        keys = list(raw[1])
        names = list(raw[2])
        imports = list(raw[3])
        empties = list(raw[4])

        tables = []
        for i in range(num):
            if not include_empty and empties[i]:
                continue
            tables.append({
                "table_key": keys[i],
                "table_name": names[i],
                "import_type": imports[i],
                "import_label": self.IMPORT_TYPE_LABELS.get(imports[i], "Unknown"),
                "is_empty": empties[i],
            })
        return tables

    def get_table_fields(self, table_key: str) -> List[Dict[str, Any]]:
        """Returns field metadata for a specific table.

        Returns:
            List of dicts with keys: field_key, field_name, description,
            units, is_importable.
        """
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetAllFieldsInTable(
            table_key, 0, 0, [], [], [], [], []
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetAllFieldsInTable failed: {ret_code}")

        num = raw[1]
        fields = []
        for i in range(num):
            fields.append({
                "field_key": raw[2][i],
                "field_name": raw[3][i],
                "description": raw[4][i],
                "units": raw[5][i],
                "is_importable": raw[6][i],
            })
        return fields

    # ── Read ──────────────────────────────────────────────────────────────

    def read_table(
        self, table_key: str, group: str = "All", for_editing: bool = False
    ) -> Dict[str, Any]:
        """Reads a table and returns structured data.

        Args:
            table_key: The table key to read.
            group: Group filter ("All" for everything).
            for_editing: If True, uses GetTableForEditingArray (editable).
                         If False, uses GetTableForDisplayArray (read-only).

        Returns:
            Dict with keys: table_version, field_keys, num_records, rows
            where rows is a list of dicts (one per record).
        """
        SapModel = self.sap_model

        if for_editing:
            raw = SapModel.DatabaseTables.GetTableForEditingArray(
                table_key, group, 0, [], 0, []
            )
        else:
            raw = SapModel.DatabaseTables.GetTableForDisplayArray(
                table_key, [""], group, 0, [], 0, []
            )

        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(
                f"{'GetTableForEditingArray' if for_editing else 'GetTableForDisplayArray'} "
                f"failed: {ret_code}"
            )

        if for_editing:
            # GetTableForEditingArray: raw[0]=TableVersion, raw[1]=FieldKeys, raw[2]=NumRecords, raw[3]=TableData
            table_version = raw[0]
            field_keys = list(raw[1])
            num_records = raw[2]
            table_data = list(raw[3]) if raw[3] else []
        else:
            # GetTableForDisplayArray: raw[0]=FieldKeyList(echoed), raw[1]=TableVersion,
            #                          raw[2]=FieldKeysIncluded, raw[3]=NumRecords, raw[4]=TableData
            table_version = raw[1]
            field_keys = list(raw[2])
            num_records = raw[3]
            table_data = list(raw[4]) if raw[4] else []

        # Convert flat array to list of dicts
        num_fields = len(field_keys)
        rows = []
        for r in range(num_records):
            row = {}
            for c in range(num_fields):
                row[field_keys[c]] = table_data[r * num_fields + c]
            rows.append(row)

        return {
            "table_version": table_version,
            "field_keys": field_keys,
            "num_records": num_records,
            "rows": rows,
        }

    # ── Write ─────────────────────────────────────────────────────────────

    def write_table(
        self,
        table_key: str,
        field_keys: List[str],
        rows: List[Dict[str, str]],
        table_version: int = 0,
    ) -> Dict[str, Any]:
        """Writes table data and applies changes.

        Args:
            table_key: The table key to write.
            field_keys: Column headers (field key names).
            rows: List of dicts (one per record, keys matching field_keys).
            table_version: Table version (from previous read, or 0).

        Returns:
            Dict with import results (fatal_errors, errors, warnings, info, log).
        """
        SapModel = self.sap_model

        # Flatten rows to flat array
        num_records = len(rows)
        table_data = []
        for row in rows:
            for fk in field_keys:
                table_data.append(str(row.get(fk, "")))

        raw = SapModel.DatabaseTables.SetTableForEditingArray(
            table_key, table_version, field_keys, num_records, table_data
        )
        set_ret = raw[-1] if isinstance(raw, tuple) else raw
        if set_ret != 0:
            raise RuntimeError(f"SetTableForEditingArray failed: {set_ret}")

        # Apply
        raw = SapModel.DatabaseTables.ApplyEditedTables(True, 0, 0, 0, 0, "")
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"ApplyEditedTables failed: {ret_code}")

        return {
            "fatal_errors": raw[0],
            "errors": raw[1],
            "warnings": raw[2],
            "info_msgs": raw[3],
            "import_log": raw[4],
        }

    def cancel_editing(self) -> int:
        """Cancels any pending table edits."""
        return self.sap_model.DatabaseTables.CancelTableEditing()

    # ── Export ────────────────────────────────────────────────────────────

    def export_csv(
        self,
        table_key: str,
        filepath: str,
        group: str = "All",
        separator: str = ",",
    ) -> Dict[str, Any]:
        """Exports a table to a CSV file.

        Args:
            table_key: Table key to export.
            filepath: Full output file path.
            group: Group filter.
            separator: CSV delimiter.

        Returns:
            Dict with table_version and filepath.
        """
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetTableForDisplayCSVFile(
            table_key, [""], group, 0, filepath, separator
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetTableForDisplayCSVFile failed: {ret_code}")

        return {"table_version": raw[0], "filepath": filepath}

    def export_csv_string(
        self, table_key: str, group: str = "All", separator: str = ","
    ) -> str:
        """Exports a table as a CSV string."""
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetTableForDisplayCSVString(
            table_key, [""], group, 0, "", separator
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetTableForDisplayCSVString failed: {ret_code}")
        # raw[0]=FieldKeys, raw[1]=NumRecords, raw[2]=csvString, raw[-1]=ret_code
        return raw[2]

    def export_xml_string(
        self,
        table_key: str,
        group: str = "All",
        include_schema: bool = True,
    ) -> str:
        """Exports a table as an XML string."""
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetTableForDisplayXMLString(
            table_key, [""], group, include_schema, 0, ""
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetTableForDisplayXMLString failed: {ret_code}")
        # raw[0]=FieldKeys, raw[1]=NumRecords, raw[2]=XMLString, raw[-1]=ret_code
        return raw[2]

    def import_csv(
        self,
        table_key: str,
        filepath: str,
        separator: str = ",",
        apply_immediately: bool = True,
    ) -> Dict[str, Any]:
        """Imports table data from a CSV file.

        Args:
            table_key: Table key to import into.
            filepath: Path to CSV file.
            separator: CSV delimiter.
            apply_immediately: If True, calls ApplyEditedTables after import.

        Returns:
            Dict with import results (if applied) or staging confirmation.
        """
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.SetTableForEditingCSVFile(
            table_key, 0, filepath, separator
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"SetTableForEditingCSVFile failed: {ret_code}")

        if apply_immediately:
            raw = SapModel.DatabaseTables.ApplyEditedTables(True, 0, 0, 0, 0, "")
            if raw[-1] != 0:
                raise RuntimeError(f"ApplyEditedTables failed: {raw[-1]}")
            return {
                "fatal_errors": raw[0],
                "errors": raw[1],
                "warnings": raw[2],
                "info_msgs": raw[3],
                "import_log": raw[4],
            }

        return {"staged": True, "table_version": raw[0]}

    # ── Model State ───────────────────────────────────────────────────────

    def is_model_locked(self) -> bool:
        """Returns True if the model is locked (analysis has been run)."""
        return bool(self.sap_model.GetModelIsLocked())


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json

    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = DatabaseTablesBackend(conn)

        try:
            # List tables
            tables = backend.list_tables(include_empty=False)
            print(f"\n═══ Tablas con datos: {len(tables)} ═══")
            for t in tables[:15]:
                print(f"  [{t['import_type']}] {t['table_key']}: {t['table_name']}")

            # Read first non-empty table
            if tables:
                key = tables[0]["table_key"]
                print(f"\n═══ Leyendo tabla: {key} ═══")
                data = backend.read_table(key)
                print(f"  Fields: {data['field_keys']}")
                print(f"  Records: {data['num_records']}")
                for row in data["rows"][:3]:
                    print(f"  → {row}")

                # Get fields
                fields = backend.get_table_fields(key)
                print(f"\n═══ Campos de {key} ═══")
                for f in fields[:5]:
                    print(f"  {f['field_key']}: {f['field_name']} [{f['units']}]")

                # Export CSV string
                csv_str = backend.export_csv_string(key)
                print(f"\n═══ CSV preview ═══")
                print(csv_str[:500])

            # Lock state
            print(f"\nModelo bloqueado: {backend.is_model_locked()}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
