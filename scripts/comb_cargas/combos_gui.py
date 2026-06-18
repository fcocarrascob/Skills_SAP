"""Tab widget de Combinaciones de Carga — workers y UI."""

from PySide6.QtCore import Qt, QThread, Signal, QEvent
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QMessageBox,
)

from sap_connection import SapConnection
from combos_backend import CombosBackend
import table_utils


class ReadCombosWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: CombosBackend):
        super().__init__()
        self._backend = backend

    def run(self):
        try:
            cases = self._backend.get_load_cases()
            combos = self._backend.get_combinations()
            self.finished.emit({"success": True, "cases": cases, "combos": combos})
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class WriteCombosWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: CombosBackend, combos_data: list, names_to_delete: list):
        super().__init__()
        self._backend = backend
        self._data = combos_data
        self._names_to_delete = names_to_delete

    def run(self):
        try:
            deleted = 0
            failed_deletions = []
            for name in self._names_to_delete:
                if self._backend.delete_combination(name):
                    deleted += 1
                else:
                    failed_deletions.append(name)
            count = self._backend.push_combinations(self._data)
            self.finished.emit({
                "success": True,
                "count": count,
                "deleted": deleted,
                "failed_deletions": failed_deletions,
            })
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class CombosTab(QWidget):
    dirty_changed = Signal(bool)
    busy_changed = Signal(bool)

    _COMBO_TYPES = ["Linear Additive", "Envelope", "Absolute Additive", "SRSS", "Range Additive"]

    def __init__(self, connection: SapConnection, log_fn):
        super().__init__()
        self._conn = connection
        self._backend = CombosBackend(connection)
        self._log = log_fn
        self._worker = None
        self._load_cases: list = []
        self._original_names: set = set()
        self._original_data: dict = {}
        self._dirty = False

        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)

        toolbar = QHBoxLayout()
        self._btn_read = QPushButton("📥 Leer Combinaciones")
        self._btn_read.setFixedHeight(32)
        self._btn_read.setEnabled(False)
        self._btn_read.clicked.connect(self._on_read)

        self._btn_send = QPushButton("📤 Enviar Combinaciones")
        self._btn_send.setFixedHeight(32)
        self._btn_send.setEnabled(False)
        self._btn_send.clicked.connect(self._on_write)

        self._btn_add = QPushButton("➕ Agregar Fila")
        self._btn_add.setFixedHeight(32)
        self._btn_add.setEnabled(False)
        self._btn_add.clicked.connect(self._add_row)

        self._btn_dup = QPushButton("⧉ Duplicar Fila")
        self._btn_dup.setFixedHeight(32)
        self._btn_dup.setEnabled(False)
        self._btn_dup.clicked.connect(self._duplicate_row)

        self._btn_del = QPushButton("➖ Eliminar Fila")
        self._btn_del.setFixedHeight(32)
        self._btn_del.setEnabled(False)
        self._btn_del.clicked.connect(self._delete_row)

        toolbar.addWidget(self._btn_read)
        toolbar.addWidget(self._btn_send)
        toolbar.addStretch()
        toolbar.addWidget(self._btn_add)
        toolbar.addWidget(self._btn_dup)
        toolbar.addWidget(self._btn_del)
        layout.addLayout(toolbar)

        self._table = QTableWidget()
        self._table.setColumnCount(2)
        self._table.setHorizontalHeaderLabels(["Nombre Combinación", "Tipo"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._table.itemChanged.connect(self._on_item_changed)
        self._table.installEventFilter(self)
        layout.addWidget(self._table)

    # ── Interfaz pública ───────────────────────────────────────────────

    def is_dirty(self) -> bool:
        return self._dirty

    def has_load_cases(self) -> bool:
        return bool(self._load_cases)

    def set_connected(self, connected: bool):
        self._btn_read.setEnabled(connected)
        if not connected:
            self._btn_send.setEnabled(False)
            self._btn_add.setEnabled(False)
            self._btn_dup.setEnabled(False)
            self._btn_del.setEnabled(False)

    def set_busy(self, is_busy: bool):
        connected = self._conn.is_connected
        has_cases = bool(self._load_cases)
        self._btn_read.setEnabled(not is_busy and connected)
        self._btn_send.setEnabled(not is_busy and connected and has_cases)
        self._btn_add.setEnabled(not is_busy and has_cases)
        self._btn_dup.setEnabled(not is_busy and has_cases)
        self._btn_del.setEnabled(not is_busy and has_cases)

    # ── Copiar / Pegar ─────────────────────────────────────────────────

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self._table:
            if event.matches(QKeySequence.StandardKey.Copy):
                table_utils.copy_selection(self._table, self._log)
                return True
            elif event.matches(QKeySequence.StandardKey.Paste):
                table_utils.paste_selection(
                    self._table,
                    lambda col: col >= 2,
                    lambda: self._set_dirty(True),
                    self._log,
                )
                return True
        return super().eventFilter(obj, event)

    # ── Estado ─────────────────────────────────────────────────────────

    def _set_dirty(self, dirty: bool):
        self._dirty = dirty
        self.dirty_changed.emit(dirty)

    def _start_op(self):
        self.set_busy(True)
        self.busy_changed.emit(True)

    def _finish_op(self):
        self.set_busy(False)
        self.busy_changed.emit(False)

    # ── Tabla helpers ──────────────────────────────────────────────────

    def _on_item_changed(self, item):
        if item.column() >= 2:
            table_utils.color_cell(item)
        self._set_dirty(True)

    def _add_row_data(self, name: str, c_type: int, items: dict):
        row = self._table.rowCount()
        self._table.insertRow(row)
        self._table.setItem(row, 0, QTableWidgetItem(str(name)))

        combo_type = QComboBox()
        combo_type.addItems(self._COMBO_TYPES)
        if 0 <= c_type < len(self._COMBO_TYPES):
            combo_type.setCurrentIndex(c_type)
        self._table.setCellWidget(row, 1, combo_type)
        combo_type.activated.connect(lambda _: self._set_dirty(True))

        for i, case_name in enumerate(self._load_cases):
            factor = items.get(case_name, "")
            item = QTableWidgetItem("" if factor == "" else str(factor))
            item.setTextAlignment(Qt.AlignCenter)
            self._table.setItem(row, 2 + i, item)
            table_utils.color_cell(item)

    def _add_row(self):
        existing = {
            self._table.item(r, 0).text().strip()
            for r in range(self._table.rowCount())
            if self._table.item(r, 0)
        }
        i = 1
        while f"COMB_{i}" in existing:
            i += 1
        self._add_row_data(f"COMB_{i}", 0, {})
        self._table.selectRow(self._table.rowCount() - 1)
        self._table.scrollToBottom()

    def _delete_row(self):
        rows = sorted(
            {idx.row() for idx in self._table.selectedIndexes()}, reverse=True
        )
        if not rows:
            return
        for row in rows:
            self._table.removeRow(row)
        self._set_dirty(True)

    def _duplicate_row(self):
        rows = sorted({idx.row() for idx in self._table.selectedIndexes()})
        if not rows:
            return
        row = rows[0]
        name_item = self._table.item(row, 0)
        base_name = name_item.text().strip() if name_item else "COMB"
        existing = {
            self._table.item(r, 0).text().strip()
            for r in range(self._table.rowCount())
            if self._table.item(r, 0)
        }
        i = 1
        while f"{base_name}_COPY_{i}" in existing:
            i += 1
        w_type = self._table.cellWidget(row, 1)
        c_type = w_type.currentIndex() if w_type else 0
        items = {}
        for j, case_name in enumerate(self._load_cases):
            cell = self._table.item(row, 2 + j)
            text = cell.text().strip() if cell else ""
            if text:
                try:
                    val = float(text)
                    if val != 0:
                        items[case_name] = val
                except ValueError:
                    pass
        self._add_row_data(f"{base_name}_COPY_{i}", c_type, items)
        self._set_dirty(True)

    def _collect_data(self) -> list:
        data = []
        for r in range(self._table.rowCount()):
            it = self._table.item(r, 0)
            name = it.text().strip() if it else ""
            if not name:
                continue
            w_type = self._table.cellWidget(r, 1)
            c_type = w_type.currentIndex() if w_type else 0
            items = {}
            for i, case_name in enumerate(self._load_cases):
                cell = self._table.item(r, 2 + i)
                text = cell.text().strip() if cell else ""
                if text:
                    try:
                        val = float(text)
                        if val != 0:
                            items[case_name] = val
                    except ValueError:
                        pass
            data.append({"name": name, "type": c_type, "items": items})
        return data

    # ── Leer ───────────────────────────────────────────────────────────

    def _on_read(self):
        self._log("\n─── Leyendo Combinaciones de SAP2000 ─────────────────")
        self._start_op()
        self._worker = ReadCombosWorker(self._backend)
        self._worker.finished.connect(self._on_read_done)
        self._worker.start()

    def _on_read_done(self, result: dict):
        self._finish_op()
        if not result.get("success"):
            self._log(f"✘ Error: {result.get('error', 'Error desconocido')}")
            return

        self._load_cases = result["cases"]
        combos = result["combos"]

        self._original_names = {c["name"] for c in combos}
        self._original_data = {
            c["name"]: {"type": c["type"], "items": dict(c["items"])}
            for c in combos
        }

        headers = ["Nombre Combinación", "Tipo"] + self._load_cases
        self._table.blockSignals(True)
        self._table.setColumnCount(len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.setRowCount(0)
        for c in combos:
            self._add_row_data(c["name"], c["type"], c["items"])
        self._table.blockSignals(False)

        hdr = self._table.horizontalHeader()
        for col in range(2):
            hdr.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        for col in range(2, self._table.columnCount()):
            hdr.setSectionResizeMode(col, QHeaderView.Fixed)
            self._table.setColumnWidth(col, 65)

        self._log(f"✔ Cargado: {len(self._load_cases)} Load Cases, {len(combos)} Combinaciones")
        self._btn_send.setEnabled(True)
        self._btn_add.setEnabled(True)
        self._btn_dup.setEnabled(True)
        self._btn_del.setEnabled(True)
        self._set_dirty(False)

    # ── Enviar ─────────────────────────────────────────────────────────

    def _on_write(self):
        if not self._load_cases:
            QMessageBox.warning(self, "Error", "Primero debes leer las Combinaciones de SAP2000.")
            return

        data = self._collect_data()
        if not data:
            QMessageBox.information(self, "Info", "No hay datos válidos para enviar.")
            return

        if not table_utils.validate_name_table(self._table):
            QMessageBox.warning(
                self, "Nombres inválidos",
                "Existen combinaciones con nombre vacío o duplicado.\n"
                "Revisa las filas resaltadas en rojo antes de enviar.",
            )
            return

        current_names = {d["name"] for d in data}
        names_to_delete = sorted(self._original_names - current_names)
        names_to_add = sorted(current_names - self._original_names)
        names_to_modify = sorted(
            name for d in data
            if (name := d["name"]) in self._original_data
            and (
                d["type"] != self._original_data[name]["type"]
                or d["items"] != self._original_data[name]["items"]
            )
        )

        msg = f"Se enviarán {len(data)} combinaciones a SAP2000."
        if names_to_add:
            msg += f"\n\n✚ Se agregarán {len(names_to_add)}:\n  " + "\n  ".join(names_to_add)
        if names_to_modify:
            msg += f"\n\n✎ Se modificarán {len(names_to_modify)}:\n  " + "\n  ".join(names_to_modify)
        if names_to_delete:
            msg += f"\n\n✖ Se eliminarán {len(names_to_delete)}:\n  " + "\n  ".join(names_to_delete)
        if not (names_to_add or names_to_modify or names_to_delete):
            msg += "\n\n(Sin cambios detectados)"
        msg += "\n\n¿Continuar?"

        if QMessageBox.question(self, "Enviar Combinaciones", msg,
                                QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return

        self._log("\n─── Enviando Combinaciones a SAP2000 ─────────────────")
        if names_to_delete:
            self._log(f"  Eliminando: {', '.join(names_to_delete)}")
        self._start_op()
        self._worker = WriteCombosWorker(self._backend, data, names_to_delete)
        self._worker.finished.connect(self._on_write_done)
        self._worker.start()

    def _on_write_done(self, result: dict):
        self._finish_op()
        if result.get("success"):
            count = result.get("count", 0)
            deleted = result.get("deleted", 0)
            failed = result.get("failed_deletions", [])
            parts = [f"✔ {count} combinaciones enviadas"]
            if deleted:
                parts.append(f"{deleted} eliminadas")
            if failed:
                parts.append(f"⚠ No se pudieron eliminar: {', '.join(failed)}")
            self._log("  |  ".join(parts))
            sent_data = self._collect_data()
            self._original_names = {d["name"] for d in sent_data}
            self._original_data = {
                d["name"]: {"type": d["type"], "items": dict(d["items"])}
                for d in sent_data
            }
            self._set_dirty(False)
        else:
            self._log(f"✘ Error: {result.get('error', 'Error desconocido')}")
