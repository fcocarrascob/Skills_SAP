"""
GUI — SAP2000 Database Tables Explorer (PySide6 Standalone)
============================================================
Browse, view, export and edit SAP2000 database tables.

Features:
    - Left panel: filterable table list with import type indicators
    - Central panel: QTableWidget showing table data
    - Toolbar: Export CSV, Export XML, Import CSV, Refresh, Apply Changes
    - Lock state indicator with 2s polling
    - Conditional editing: enabled only when model is unlocked

Requires: PySide6, comtypes
"""

import sys
import json
import os

from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QMessageBox,
    QToolBar,
    QStatusBar,
    QMainWindow,
)

from backend_database_tables import SapConnection, DatabaseTablesBackend


# ══════════════════════════════════════════════════════════════════════════════
# Workers
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.connect(attach_to_existing=True)
        self.finished.emit(result)


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.disconnect()
        self.finished.emit(result)


class ListTablesWorker(QThread):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, backend: DatabaseTablesBackend):
        super().__init__()
        self._backend = backend

    def run(self):
        try:
            tables = self._backend.list_tables(include_empty=True)
            self.finished.emit(tables)
        except Exception as e:
            self.error.emit(str(e))


class ReadTableWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, backend: DatabaseTablesBackend, table_key: str):
        super().__init__()
        self._backend = backend
        self._table_key = table_key

    def run(self):
        try:
            data = self._backend.read_table(self._table_key)
            data["table_key"] = self._table_key
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class WriteTableWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, backend, table_key, field_keys, rows, table_version):
        super().__init__()
        self._backend = backend
        self._table_key = table_key
        self._field_keys = field_keys
        self._rows = rows
        self._table_version = table_version

    def run(self):
        try:
            result = self._backend.write_table(
                self._table_key,
                self._field_keys,
                self._rows,
                self._table_version,
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ExportCsvWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, backend, table_key, filepath):
        super().__init__()
        self._backend = backend
        self._table_key = table_key
        self._filepath = filepath

    def run(self):
        try:
            self._backend.export_csv(self._table_key, self._filepath)
            self.finished.emit(self._filepath)
        except Exception as e:
            self.error.emit(str(e))


class ImportCsvWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, backend, table_key, filepath):
        super().__init__()
        self._backend = backend
        self._table_key = table_key
        self._filepath = filepath

    def run(self):
        try:
            result = self._backend.import_csv(self._table_key, self._filepath)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


# ══════════════════════════════════════════════════════════════════════════════
# Main Window
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseTablesGUI(QMainWindow):
    """GUI standalone para explorar Database Tables de SAP2000."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Database Tables Explorer")
        self.setMinimumSize(1100, 700)

        # State
        self._conn = SapConnection()
        self._backend = DatabaseTablesBackend(self._conn)
        self._worker = None
        self._current_table_key = None
        self._current_table_version = 0
        self._current_field_keys = []
        self._model_locked = True
        self._tables_cache = []

        # Lock state polling timer
        self._lock_timer = QTimer()
        self._lock_timer.setInterval(2000)
        self._lock_timer.timeout.connect(self._poll_lock_state)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(6)

        # ── Top bar: connection ──────────────────────────────────────────
        top_row = QHBoxLayout()
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(30)
        self._btn_connect.clicked.connect(self._on_connect)
        top_row.addWidget(self._btn_connect)

        self._status_lbl = QLabel("Desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        top_row.addWidget(self._status_lbl)

        self._lock_lbl = QLabel("")
        self._lock_lbl.setStyleSheet("font-size: 14px;")
        top_row.addWidget(self._lock_lbl)

        top_row.addStretch()

        self._btn_disconnect = QPushButton("Desconectar")
        self._btn_disconnect.setFixedHeight(30)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        top_row.addWidget(self._btn_disconnect)
        root.addLayout(top_row)

        # ── Main splitter ────────────────────────────────────────────────
        splitter = QSplitter(Qt.Horizontal)

        # Left panel: table list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self._filter_input = QLineEdit()
        self._filter_input.setPlaceholderText("Filtrar tablas...")
        self._filter_input.textChanged.connect(self._on_filter_changed)
        left_layout.addWidget(self._filter_input)

        self._table_tree = QTreeWidget()
        self._table_tree.setHeaderLabels(["Tabla", "Import"])
        self._table_tree.setColumnWidth(0, 280)
        self._table_tree.setColumnWidth(1, 40)
        self._table_tree.itemClicked.connect(self._on_table_selected)
        left_layout.addWidget(self._table_tree)

        splitter.addWidget(left_panel)

        # Right panel: data view + actions
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Action buttons
        btn_row = QHBoxLayout()
        self._btn_refresh = QPushButton("Refrescar")
        self._btn_refresh.setEnabled(False)
        self._btn_refresh.clicked.connect(self._on_refresh_table)
        btn_row.addWidget(self._btn_refresh)

        self._btn_export_csv = QPushButton("Exportar CSV")
        self._btn_export_csv.setEnabled(False)
        self._btn_export_csv.clicked.connect(self._on_export_csv)
        btn_row.addWidget(self._btn_export_csv)

        self._btn_import_csv = QPushButton("Importar CSV")
        self._btn_import_csv.setEnabled(False)
        self._btn_import_csv.clicked.connect(self._on_import_csv)
        btn_row.addWidget(self._btn_import_csv)

        self._btn_apply = QPushButton("Aplicar Cambios")
        self._btn_apply.setEnabled(False)
        self._btn_apply.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; font-weight: bold; }"
            "QPushButton:disabled { background-color: #95a5a6; color: #ecf0f1; }"
        )
        self._btn_apply.clicked.connect(self._on_apply_changes)
        btn_row.addWidget(self._btn_apply)

        btn_row.addStretch()
        right_layout.addLayout(btn_row)

        # Table info label
        self._info_lbl = QLabel("Seleccione una tabla del panel izquierdo")
        self._info_lbl.setStyleSheet("color: #7f8c8d; font-style: italic;")
        right_layout.addWidget(self._info_lbl)

        # Data table
        self._data_table = QTableWidget()
        self._data_table.setFont(QFont("Consolas", 9))
        self._data_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self._data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        right_layout.addWidget(self._data_table)

        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        root.addWidget(splitter)

        # ── Log output ───────────────────────────────────────────────────
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 8))
        self._log.setMaximumHeight(120)
        root.addWidget(self._log)

    # ══════════════════════════════════════════════════════════════════════
    # Helpers
    # ══════════════════════════════════════════════════════════════════════

    def _log_append(self, text: str):
        self._log.append(text)

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_disconnect.setEnabled(connected)
        if connected:
            self._status_lbl.setText("Conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
            self._lock_timer.start()
        else:
            self._status_lbl.setText("Desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
            self._lock_lbl.setText("")
            self._lock_timer.stop()
            self._table_tree.clear()
            self._data_table.setRowCount(0)
            self._data_table.setColumnCount(0)
            self._btn_refresh.setEnabled(False)
            self._btn_export_csv.setEnabled(False)
            self._btn_import_csv.setEnabled(False)
            self._btn_apply.setEnabled(False)

    def _busy(self, is_busy: bool):
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_refresh.setEnabled(not is_busy and self._current_table_key is not None)
        self._btn_export_csv.setEnabled(not is_busy and self._current_table_key is not None)
        self._btn_import_csv.setEnabled(
            not is_busy and self._current_table_key is not None and not self._model_locked
        )
        self._btn_apply.setEnabled(
            not is_busy and self._current_table_key is not None and not self._model_locked
        )

    def _update_lock_ui(self):
        if self._model_locked:
            self._lock_lbl.setText("🔒 Modelo bloqueado")
            self._lock_lbl.setToolTip("El modelo está bloqueado — edición deshabilitada")
            self._data_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._btn_apply.setEnabled(False)
            self._btn_apply.setToolTip("Modelo bloqueado — desbloquee para editar")
            self._btn_import_csv.setEnabled(False)
        else:
            self._lock_lbl.setText("🔓 Modelo desbloqueado")
            self._lock_lbl.setToolTip("El modelo está desbloqueado — edición habilitada")
            self._data_table.setEditTriggers(
                QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed
            )
            if self._current_table_key:
                self._btn_apply.setEnabled(True)
                self._btn_import_csv.setEnabled(True)
            self._btn_apply.setToolTip("")

    def _poll_lock_state(self):
        if not self._conn.is_connected:
            return
        try:
            locked = self._backend.is_model_locked()
            if locked != self._model_locked:
                self._model_locked = locked
                self._update_lock_ui()
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════════════
    # Connect / Disconnect
    # ══════════════════════════════════════════════════════════════════════

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy(False)
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            self._log_append(f"✔ Conectado — v{ver}  |  {path}")
            self._set_connected(True)
            self._poll_lock_state()
            self._update_lock_ui()
            self._load_table_list()
        else:
            self._log_append(f"✘ Error: {result.get('error', '?')}")
            self._set_connected(False)

    def _on_disconnect(self):
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, _):
        self._busy(False)
        self._log_append("✔ Desconectado")
        self._set_connected(False)
        self._current_table_key = None

    # ══════════════════════════════════════════════════════════════════════
    # Table List
    # ══════════════════════════════════════════════════════════════════════

    def _load_table_list(self):
        self._log_append("Cargando lista de tablas...")
        self._worker = ListTablesWorker(self._backend)
        self._worker.finished.connect(self._on_tables_loaded)
        self._worker.error.connect(lambda e: self._log_append(f"✘ Error: {e}"))
        self._worker.start()

    def _on_tables_loaded(self, tables: list):
        self._tables_cache = tables
        self._populate_tree(tables)
        self._log_append(f"✔ {len(tables)} tablas cargadas")

    def _populate_tree(self, tables: list):
        self._table_tree.clear()
        import_icons = {0: "○", 1: "◐", 2: "●", 3: "◉"}

        filter_text = self._filter_input.text().lower()

        for t in tables:
            key = t["table_key"]
            name = t["table_name"]
            imp = t["import_type"]
            empty = t["is_empty"]

            if filter_text and filter_text not in key.lower() and filter_text not in name.lower():
                continue

            item = QTreeWidgetItem([name, import_icons.get(imp, "?")])
            item.setData(0, Qt.UserRole, key)
            item.setToolTip(0, f"Key: {key}\nImport: {t['import_label']}")
            if empty:
                item.setForeground(0, QColor("#95a5a6"))
            self._table_tree.addTopLevelItem(item)

    def _on_filter_changed(self, text: str):
        self._populate_tree(self._tables_cache)

    # ══════════════════════════════════════════════════════════════════════
    # Table Selection & Display
    # ══════════════════════════════════════════════════════════════════════

    def _on_table_selected(self, item: QTreeWidgetItem, column: int):
        table_key = item.data(0, Qt.UserRole)
        if not table_key:
            return
        self._current_table_key = table_key
        self._load_table_data(table_key)

    def _load_table_data(self, table_key: str):
        self._log_append(f"Leyendo: {table_key}...")
        self._busy(True)
        self._worker = ReadTableWorker(self._backend, table_key)
        self._worker.finished.connect(self._on_table_data_loaded)
        self._worker.error.connect(self._on_table_data_error)
        self._worker.start()

    def _on_table_data_loaded(self, data: dict):
        self._busy(False)
        self._current_table_version = data.get("table_version", 0)
        self._current_field_keys = data.get("field_keys", [])
        rows = data.get("rows", [])
        num_records = data.get("num_records", 0)

        self._info_lbl.setText(
            f"Tabla: {data.get('table_key', '?')}  |  "
            f"Registros: {num_records}  |  Campos: {len(self._current_field_keys)}"
        )

        # Populate QTableWidget
        self._data_table.setRowCount(num_records)
        self._data_table.setColumnCount(len(self._current_field_keys))
        self._data_table.setHorizontalHeaderLabels(self._current_field_keys)

        for r, row in enumerate(rows):
            for c, fk in enumerate(self._current_field_keys):
                val = str(row.get(fk, ""))
                cell = QTableWidgetItem(val)
                self._data_table.setItem(r, c, cell)

        self._log_append(
            f"✔ {data.get('table_key')}: {num_records} registros, "
            f"{len(self._current_field_keys)} campos"
        )
        self._update_lock_ui()

    def _on_table_data_error(self, error: str):
        self._busy(False)
        self._log_append(f"✘ Error leyendo tabla: {error}")

    def _on_refresh_table(self):
        if self._current_table_key:
            self._load_table_data(self._current_table_key)

    # ══════════════════════════════════════════════════════════════════════
    # Export CSV
    # ══════════════════════════════════════════════════════════════════════

    def _on_export_csv(self):
        if not self._current_table_key:
            return
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Exportar CSV", "", "CSV Files (*.csv)"
        )
        if not filepath:
            return

        self._log_append(f"Exportando CSV: {self._current_table_key}...")
        self._busy(True)
        self._worker = ExportCsvWorker(
            self._backend, self._current_table_key, filepath
        )
        self._worker.finished.connect(self._on_export_done)
        self._worker.error.connect(self._on_export_error)
        self._worker.start()

    def _on_export_done(self, filepath: str):
        self._busy(False)
        self._log_append(f"✔ CSV exportado: {filepath}")

    def _on_export_error(self, error: str):
        self._busy(False)
        self._log_append(f"✘ Error exportando: {error}")

    # ══════════════════════════════════════════════════════════════════════
    # Import CSV
    # ══════════════════════════════════════════════════════════════════════

    def _on_import_csv(self):
        if not self._current_table_key or self._model_locked:
            return
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Importar CSV", "", "CSV Files (*.csv)"
        )
        if not filepath:
            return

        reply = QMessageBox.question(
            self,
            "Confirmar importación",
            f"¿Importar datos desde:\n{filepath}\n\n"
            f"a la tabla: {self._current_table_key}?\n\n"
            "Los cambios se aplicarán inmediatamente al modelo.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self._log_append(f"Importando CSV: {filepath}...")
        self._busy(True)
        self._worker = ImportCsvWorker(
            self._backend, self._current_table_key, filepath
        )
        self._worker.finished.connect(self._on_import_done)
        self._worker.error.connect(self._on_import_error)
        self._worker.start()

    def _on_import_done(self, result: dict):
        self._busy(False)
        fatal = result.get("fatal_errors", 0)
        errors = result.get("errors", 0)
        warnings = result.get("warnings", 0)
        self._log_append(
            f"✔ Importación completada — Fatal: {fatal}, Errors: {errors}, Warnings: {warnings}"
        )
        if fatal > 0 or errors > 0:
            QMessageBox.warning(
                self,
                "Errores en importación",
                f"Fatal: {fatal}\nErrors: {errors}\nWarnings: {warnings}\n\n"
                f"Revise el log para detalles.",
            )
        # Refresh table
        self._on_refresh_table()

    def _on_import_error(self, error: str):
        self._busy(False)
        self._log_append(f"✘ Error importando: {error}")

    # ══════════════════════════════════════════════════════════════════════
    # Apply Changes (from in-place editing)
    # ══════════════════════════════════════════════════════════════════════

    def _on_apply_changes(self):
        if not self._current_table_key or self._model_locked:
            return
        if not self._current_field_keys:
            return

        reply = QMessageBox.question(
            self,
            "Confirmar cambios",
            f"¿Aplicar cambios editados a la tabla:\n{self._current_table_key}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        # Collect data from QTableWidget
        rows = []
        for r in range(self._data_table.rowCount()):
            row = {}
            for c, fk in enumerate(self._current_field_keys):
                item = self._data_table.item(r, c)
                row[fk] = item.text() if item else ""
            rows.append(row)

        self._log_append(f"Aplicando {len(rows)} registros a {self._current_table_key}...")
        self._busy(True)
        self._worker = WriteTableWorker(
            self._backend,
            self._current_table_key,
            self._current_field_keys,
            rows,
            self._current_table_version,
        )
        self._worker.finished.connect(self._on_apply_done)
        self._worker.error.connect(self._on_apply_error)
        self._worker.start()

    def _on_apply_done(self, result: dict):
        self._busy(False)
        fatal = result.get("fatal_errors", 0)
        errors = result.get("errors", 0)
        warnings = result.get("warnings", 0)
        self._log_append(
            f"✔ Cambios aplicados — Fatal: {fatal}, Errors: {errors}, Warnings: {warnings}"
        )
        if fatal > 0 or errors > 0:
            QMessageBox.warning(
                self, "Errores al aplicar",
                f"Fatal: {fatal}\nErrors: {errors}\nWarnings: {warnings}",
            )
        self._on_refresh_table()

    def _on_apply_error(self, error: str):
        self._busy(False)
        self._log_append(f"✘ Error aplicando cambios: {error}")


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = DatabaseTablesGUI()
    win.show()
    sys.exit(app.exec())
