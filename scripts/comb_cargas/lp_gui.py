"""Tab widget de Load Patterns — workers y UI."""

from PySide6.QtCore import Qt, QThread, Signal, QEvent
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QCheckBox, QMessageBox,
)

from sap_connection import SapConnection
from lp_backend import LoadPatternsBackend
import table_utils


class ReadPatternsWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: LoadPatternsBackend):
        super().__init__()
        self._backend = backend

    def run(self):
        try:
            patterns = self._backend.get_patterns()
            self.finished.emit({"success": True, "patterns": patterns})
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class WritePatternsWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: LoadPatternsBackend, data: list, to_delete: list, add_lc: bool):
        super().__init__()
        self._backend = backend
        self._data = data
        self._to_delete = to_delete
        self._add_lc = add_lc

    def run(self):
        try:
            result = self._backend.push_patterns(self._data, self._to_delete, self._add_lc)
            self.finished.emit({"success": True, **result})
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class LoadPatternsTab(QWidget):
    dirty_changed = Signal(bool)
    busy_changed = Signal(bool)

    # Tipos más comunes en ingeniería estructural primero
    _LP_TYPE_ORDER = [
        1, 3, 2, 4, 5, 6, 7, 11, 10, 8, 9, 13, 12,
        14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
        26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
    ]

    def __init__(self, connection: SapConnection, log_fn):
        super().__init__()
        self._conn = connection
        self._backend = LoadPatternsBackend(connection)
        self._log = log_fn
        self._worker = None
        self._loaded = False
        self._original_names: set = set()
        self._original_data: dict = {}
        self._dirty = False

        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)

        toolbar = QHBoxLayout()
        self._btn_read = QPushButton("📥 Leer Patrones")
        self._btn_read.setFixedHeight(32)
        self._btn_read.setEnabled(False)
        self._btn_read.clicked.connect(self._on_read)

        self._btn_send = QPushButton("📤 Enviar Patrones")
        self._btn_send.setFixedHeight(32)
        self._btn_send.setEnabled(False)
        self._btn_send.clicked.connect(self._on_write)

        self._btn_add = QPushButton("➕ Agregar")
        self._btn_add.setFixedHeight(32)
        self._btn_add.setEnabled(False)
        self._btn_add.clicked.connect(self._add_row)

        self._btn_del = QPushButton("➖ Eliminar")
        self._btn_del.setFixedHeight(32)
        self._btn_del.setEnabled(False)
        self._btn_del.clicked.connect(self._delete_row)

        toolbar.addWidget(self._btn_read)
        toolbar.addWidget(self._btn_send)
        toolbar.addStretch()
        toolbar.addWidget(self._btn_add)
        toolbar.addWidget(self._btn_del)
        layout.addLayout(toolbar)

        self._chk_add_lc = QCheckBox("Crear Load Case automáticamente al agregar patrón")
        self._chk_add_lc.setChecked(True)
        layout.addWidget(self._chk_add_lc)

        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(["Nombre Patrón", "Tipo", "Mult. PP"])
        hdr = self._table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self._table.itemChanged.connect(self._on_item_changed)
        self._table.installEventFilter(self)
        layout.addWidget(self._table)

    # ── Interfaz pública ───────────────────────────────────────────────

    def is_dirty(self) -> bool:
        return self._dirty

    def is_loaded(self) -> bool:
        return self._loaded

    def set_connected(self, connected: bool):
        self._btn_read.setEnabled(connected)
        if not connected:
            self._btn_send.setEnabled(False)
            self._btn_add.setEnabled(False)
            self._btn_del.setEnabled(False)

    def set_busy(self, is_busy: bool):
        connected = self._conn.is_connected
        self._btn_read.setEnabled(not is_busy and connected)
        self._btn_send.setEnabled(not is_busy and connected and self._loaded)
        self._btn_add.setEnabled(not is_busy and self._loaded)
        self._btn_del.setEnabled(not is_busy and self._loaded)

    # ── Copiar / Pegar ─────────────────────────────────────────────────

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self._table:
            if event.matches(QKeySequence.StandardKey.Copy):
                table_utils.copy_selection(self._table, self._log)
                return True
            elif event.matches(QKeySequence.StandardKey.Paste):
                table_utils.paste_selection(
                    self._table,
                    lambda col: col == 2,
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

    # ── Helpers de tipo ────────────────────────────────────────────────

    def _type_labels(self) -> list:
        return [LoadPatternsBackend.LOAD_TYPES[t] for t in self._LP_TYPE_ORDER]

    def _type_to_combo_idx(self, type_int: int) -> int:
        try:
            return self._LP_TYPE_ORDER.index(type_int)
        except ValueError:
            return 0

    def _combo_idx_to_type(self, idx: int) -> int:
        if 0 <= idx < len(self._LP_TYPE_ORDER):
            return self._LP_TYPE_ORDER[idx]
        return 1

    # ── Tabla helpers ──────────────────────────────────────────────────

    def _add_row_data(self, name: str, type_int: int, sw_mult: float):
        row = self._table.rowCount()
        self._table.insertRow(row)
        self._table.setItem(row, 0, QTableWidgetItem(str(name)))

        combo_type = QComboBox()
        combo_type.addItems(self._type_labels())
        combo_type.setCurrentIndex(self._type_to_combo_idx(type_int))
        self._table.setCellWidget(row, 1, combo_type)
        combo_type.activated.connect(lambda _: self._set_dirty(True))

        mult_item = QTableWidgetItem("" if sw_mult == 0 else str(sw_mult))
        mult_item.setTextAlignment(Qt.AlignCenter)
        self._table.setItem(row, 2, mult_item)
        table_utils.color_cell(mult_item)

    def _add_row(self):
        existing = {
            self._table.item(r, 0).text().strip()
            for r in range(self._table.rowCount())
            if self._table.item(r, 0)
        }
        i = 1
        while f"LP_{i}" in existing:
            i += 1
        self._add_row_data(f"LP_{i}", 1, 0.0)
        self._table.selectRow(self._table.rowCount() - 1)
        self._table.scrollToBottom()
        self._set_dirty(True)

    def _delete_row(self):
        rows = sorted(
            {idx.row() for idx in self._table.selectedIndexes()}, reverse=True
        )
        if not rows:
            return
        for row in rows:
            self._table.removeRow(row)
        self._set_dirty(True)

    def _on_item_changed(self, item):
        if item.column() == 2:
            table_utils.color_cell(item)
        self._set_dirty(True)

    def _collect_data(self) -> list:
        data = []
        for r in range(self._table.rowCount()):
            it = self._table.item(r, 0)
            name = it.text().strip() if it else ""
            if not name:
                continue
            w = self._table.cellWidget(r, 1)
            type_int = self._combo_idx_to_type(w.currentIndex() if w else 0)
            mult_it = self._table.item(r, 2)
            mult_text = mult_it.text().strip() if mult_it else ""
            try:
                sw_mult = float(mult_text) if mult_text else 0.0
            except ValueError:
                sw_mult = 0.0
            data.append({"name": name, "type": type_int, "sw_mult": sw_mult})
        return data

    # ── Leer ───────────────────────────────────────────────────────────

    def _on_read(self):
        self._log("\n─── Leyendo Load Patterns de SAP2000 ─────────────────")
        self._start_op()
        self._worker = ReadPatternsWorker(self._backend)
        self._worker.finished.connect(self._on_read_done)
        self._worker.start()

    def _on_read_done(self, result: dict):
        self._finish_op()
        if not result.get("success"):
            self._log(f"✘ Error: {result.get('error', 'Error desconocido')}")
            return

        patterns = result["patterns"]
        self._original_names = {p["name"] for p in patterns}
        self._original_data = {
            p["name"]: {"type": p["type"], "sw_mult": p["sw_mult"]}
            for p in patterns
        }

        self._table.blockSignals(True)
        self._table.setRowCount(0)
        for p in patterns:
            self._add_row_data(p["name"], p["type"], p["sw_mult"])
        self._table.blockSignals(False)

        self._loaded = True
        self._log(f"✔ Cargados {len(patterns)} Load Patterns")
        self._btn_send.setEnabled(True)
        self._btn_add.setEnabled(True)
        self._btn_del.setEnabled(True)
        self._set_dirty(False)

    # ── Enviar ─────────────────────────────────────────────────────────

    def _on_write(self):
        data = self._collect_data()
        if not data:
            QMessageBox.information(self, "Info", "No hay patrones para enviar.")
            return

        if not table_utils.validate_name_table(self._table):
            QMessageBox.warning(
                self, "Nombres inválidos",
                "Existen patrones con nombre vacío o duplicado.\n"
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
                or d["sw_mult"] != self._original_data[name]["sw_mult"]
            )
        )

        add_lc = self._chk_add_lc.isChecked()
        msg = f"Se enviarán {len(data)} Load Patterns a SAP2000."
        if names_to_add:
            lc_note = " (+ Load Case auto)" if add_lc else ""
            msg += f"\n\n✚ Se agregarán {len(names_to_add)}{lc_note}:\n  " + "\n  ".join(names_to_add)
        if names_to_modify:
            msg += f"\n\n✎ Se modificarán {len(names_to_modify)}:\n  " + "\n  ".join(names_to_modify)
        if names_to_delete:
            msg += f"\n\n✖ Se eliminarán {len(names_to_delete)}:\n  " + "\n  ".join(names_to_delete)
            msg += "\n  (se intentará eliminar el Load Case asociado si es necesario)"
        if not (names_to_add or names_to_modify or names_to_delete):
            msg += "\n\n(Sin cambios detectados)"
        msg += "\n\n¿Continuar?"

        if QMessageBox.question(self, "Enviar Load Patterns", msg,
                                QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return

        self._log("\n─── Enviando Load Patterns a SAP2000 ─────────────────")
        self._start_op()
        self._worker = WritePatternsWorker(self._backend, data, names_to_delete, add_lc)
        self._worker.finished.connect(self._on_write_done)
        self._worker.start()

    def _on_write_done(self, result: dict):
        self._finish_op()
        if result.get("success"):
            sent = result.get("sent", 0)
            deleted = result.get("deleted", 0)
            failed_del = result.get("failed_deletions", [])
            failed_add = result.get("failed_adds", [])
            parts = [f"✔ {sent} patrones enviados"]
            if deleted:
                parts.append(f"{deleted} eliminados")
            if failed_del:
                parts.append(f"⚠ No se pudieron eliminar: {', '.join(failed_del)}")
            if failed_add:
                parts.append(f"⚠ No se pudieron agregar: {', '.join(failed_add)}")
            self._log("  |  ".join(parts))
            sent_data = self._collect_data()
            self._original_names = {d["name"] for d in sent_data}
            self._original_data = {
                d["name"]: {"type": d["type"], "sw_mult": d["sw_mult"]}
                for d in sent_data
            }
            self._set_dirty(False)
        else:
            self._log(f"✘ Error: {result.get('error', 'Error desconocido')}")
