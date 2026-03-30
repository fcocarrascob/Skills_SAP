"""
GUI de Combinaciones de Carga — SAP2000 Standalone PySide6
===========================================================
Interfaz para gestionar combinaciones de carga en SAP2000.
Conexión directa vía comtypes (sin MCP).

Layout
------
  [Conectar]  [Desconectar de SAP2000]
  [📥 Leer de SAP2000]  [📤 Enviar a SAP2000]  [➕ Agregar Fila]  [➖ Eliminar Fila]
  ── Combinaciones de Carga ────────────────────────────────────
     Tabla: Nombre | Tipo | ASD/LRFD | <Load Cases dinámicos>
  ── Salida ────────────────────────────────────────────
     QTextEdit (Consolas 9pt, read-only)
"""

import sys

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QMessageBox,
)

from combos_backend import SapConnection, CombosBackend


# ══════════════════════════════════════════════════════════════════════════════
# Workers — operaciones SAP2000 fuera del hilo GUI
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    """Conecta a SAP2000 en un hilo separado."""
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        self.finished.emit(self._conn.connect(attach_to_existing=True))


class ReadWorker(QThread):
    """Lee Load Cases y Combinaciones de SAP2000."""
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


class WriteWorker(QThread):
    """Envía combinaciones a SAP2000 y elimina las que fueron borradas de la tabla."""
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


class DisconnectWorker(QThread):
    """Desconecta de SAP2000 en un hilo separado."""
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        self.finished.emit(self._conn.disconnect())


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QWidget):
    """GUI standalone para gestión de combinaciones de carga en SAP2000."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Combinaciones de Carga")
        self.setMinimumWidth(900)

        # ── Estado interno ─────────────────────────────────────────────────────
        self._conn = SapConnection()
        self._backend = CombosBackend(self._conn)
        self._worker = None
        self._load_cases: list = []
        self._original_combo_names: set = set()   # nombres presentes en SAP2000 al último leer
        self._original_combo_data: dict = {}      # {name: {"type": int, "items": dict}}
        self._dirty: bool = False                  # hay cambios sin enviar a SAP2000

        # ── Layout raíz ─────────────────────────────────────────────────────
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Status ───────────────────────────────────────────────────────────
        status_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        status_row.addWidget(self._status_lbl)
        status_row.addStretch()
        root.addLayout(status_row)

        # ── Botón Conectar / Desconectar ─────────────────────────────────────
        conn_row = QHBoxLayout()
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(34)
        self._btn_connect.clicked.connect(self._on_connect)

        self._btn_disconnect = QPushButton("Desconectar de SAP2000")
        self._btn_disconnect.setFixedHeight(34)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)

        conn_row.addWidget(self._btn_connect)
        conn_row.addWidget(self._btn_disconnect)
        conn_row.addStretch()
        root.addLayout(conn_row)

        # ── Toolbar combinaciones ──────────────────────────────────────────
        combo_row = QHBoxLayout()
        self._btn_read = QPushButton("📥 Leer de SAP2000")
        self._btn_read.setFixedHeight(32)
        self._btn_read.setEnabled(False)
        self._btn_read.clicked.connect(self._on_read)

        self._btn_send = QPushButton("📤 Enviar a SAP2000")
        self._btn_send.setFixedHeight(32)
        self._btn_send.setEnabled(False)
        self._btn_send.clicked.connect(self._on_write)

        self._btn_add_row = QPushButton("➕ Agregar Fila")
        self._btn_add_row.setFixedHeight(32)
        self._btn_add_row.clicked.connect(self._add_row)

        self._btn_del_row = QPushButton("➖ Eliminar Fila")
        self._btn_del_row.setFixedHeight(32)
        self._btn_del_row.clicked.connect(self._delete_row)

        combo_row.addWidget(self._btn_read)
        combo_row.addWidget(self._btn_send)
        combo_row.addStretch()
        combo_row.addWidget(self._btn_add_row)
        combo_row.addWidget(self._btn_del_row)
        root.addLayout(combo_row)

        # ── Tabla ──────────────────────────────────────────────────────────────
        table_box = QGroupBox("Combinaciones de Carga")
        table_layout = QVBoxLayout(table_box)
        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(["Nombre Combinación", "Tipo", "ASD/LRFD"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table_layout.addWidget(self._table)
        self._table.itemChanged.connect(self._on_item_changed)
        root.addWidget(table_box)

        # ── Output log ──────────────────────────────────────────────────────
        log_box = QGroupBox("Salida")
        log_layout = QVBoxLayout(log_box)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(120)
        log_layout.addWidget(self._log)
        root.addWidget(log_box)

    # ══════════════════════════════════════════════════════════════════
    # Helpers internos
    # ══════════════════════════════════════════════════════════════════

    def _log_append(self, text: str):
        self._log.append(text)

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_disconnect.setEnabled(connected)
        self._btn_read.setEnabled(connected)
        self._btn_send.setEnabled(connected and bool(self._load_cases))
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")

    def _busy(self, is_busy: bool):
        """Deshabilita todos los botones mientras un worker está activo."""
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_read.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_send.setEnabled(
            not is_busy and self._conn.is_connected and bool(self._load_cases)
        )

    def closeEvent(self, event):
        if self._dirty:
            reply = QMessageBox.question(
                self,
                "Cambios sin guardar",
                "Hay cambios pendientes que no se han enviado a SAP2000.\n¿Salir de todas formas?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return
        event.accept()

    def _set_dirty(self, dirty: bool):
        self._dirty = dirty
        base = "SAP2000 — Combinaciones de Carga"
        self.setWindowTitle(f"● {base}" if dirty else base)

    def _color_cell(self, item):
        """Fondo verde si hay factor ≠ 0, blanco si vacía o cero."""
        text = item.text().strip()
        has_value = False
        try:
            if text and float(text) != 0:
                has_value = True
        except ValueError:
            pass
        item.setBackground(QColor("#d4edda") if has_value else QColor("#ffffff"))

    def _on_item_changed(self, item):
        """Colorea celdas de factor y marca la tabla como modificada."""
        if item.column() >= 3:
            self._color_cell(item)
        self._set_dirty(True)

    def _validate_table(self) -> bool:
        """Resalta en rojo nombres vacíos o duplicados. Retorna True si todo es válido."""
        seen: dict = {}
        valid = True
        for r in range(self._table.rowCount()):
            it = self._table.item(r, 0)
            name = it.text().strip() if it else ""
            if not name:
                if it:
                    it.setBackground(QColor("#f8d7da"))
                valid = False
            elif name in seen:
                it.setBackground(QColor("#f8d7da"))
                prev = self._table.item(seen[name], 0)
                if prev:
                    prev.setBackground(QColor("#f8d7da"))
                valid = False
            else:
                seen[name] = r
                if it:
                    it.setBackground(QColor("#ffffff"))
        return valid

    # ══════════════════════════════════════════════════════════════════
    # Tabla helpers
    # ══════════════════════════════════════════════════════════════════

    def _add_row_data(self, name: str, c_type: int, items: dict):
        row = self._table.rowCount()
        self._table.insertRow(row)

        self._table.setItem(row, 0, QTableWidgetItem(str(name)))

        combo_type = QComboBox()
        types = ["Linear Additive", "Envelope", "Absolute Additive", "SRSS", "Range Additive"]
        combo_type.addItems(types)
        if 0 <= c_type < len(types):
            combo_type.setCurrentIndex(c_type)
        self._table.setCellWidget(row, 1, combo_type)
        combo_type.activated.connect(lambda _: self._set_dirty(True))

        combo_design = QComboBox()
        combo_design.addItems(["ASD", "LRFD", ""])
        combo_design.setCurrentIndex(2)
        self._table.setCellWidget(row, 2, combo_design)
        combo_design.activated.connect(lambda _: self._set_dirty(True))

        for i, case_name in enumerate(self._load_cases):
            factor = items.get(case_name, "")
            item = QTableWidgetItem("" if factor == "" else str(factor))
            item.setTextAlignment(Qt.AlignCenter)
            self._table.setItem(row, 3 + i, item)
            self._color_cell(item)

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
        last = self._table.rowCount() - 1
        self._table.selectRow(last)
        self._table.scrollToBottom()

    def _delete_row(self):
        rows = sorted(
            {idx.row() for idx in self._table.selectedIndexes()}, reverse=True
        )
        for row in rows:
            self._table.removeRow(row)

    def _collect_table_data(self) -> list:
        data = []
        for r in range(self._table.rowCount()):
            item_name = self._table.item(r, 0)
            name = item_name.text().strip() if item_name else ""
            if not name:
                continue
            w_type = self._table.cellWidget(r, 1)
            c_type = w_type.currentIndex() if w_type else 0
            items = {}
            for i, case_name in enumerate(self._load_cases):
                cell = self._table.item(r, 3 + i)
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

    # ══════════════════════════════════════════════════════════════════
    # Conectar
    # ══════════════════════════════════════════════════════════════════

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
            self._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self._set_connected(True)
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    # ══════════════════════════════════════════════════════════════════
    # Leer de SAP2000
    # ══════════════════════════════════════════════════════════════════

    def _on_read(self):
        self._log_append("\n─── Leyendo de SAP2000 ────────────────────────────")
        self._busy(True)
        self._worker = ReadWorker(self._backend)
        self._worker.finished.connect(self._on_read_done)
        self._worker.start()

    def _on_read_done(self, result: dict):
        self._busy(False)
        if not result.get("success"):
            self._log_append(f"✘ Error: {result.get('error', 'Error desconocido')}")
            return

        self._load_cases = result["cases"]
        combos = result["combos"]

        # guardar snapshot de SAP2000 para detectar altas, bajas y modificaciones
        self._original_combo_names = {c["name"] for c in combos}
        self._original_combo_data = {
            c["name"]: {"type": c["type"], "items": dict(c["items"])}
            for c in combos
        }

        headers = ["Nombre Combinación", "Tipo", "ASD/LRFD"] + self._load_cases
        self._table.blockSignals(True)
        self._table.setColumnCount(len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.setRowCount(0)

        for c in combos:
            self._add_row_data(c["name"], c["type"], c["items"])
        self._table.blockSignals(False)

        self._log_append(
            f"✔ Cargado: {len(self._load_cases)} Load Cases, {len(combos)} Combinaciones"
        )
        self._btn_send.setEnabled(True)
        self._set_dirty(False)

    # ══════════════════════════════════════════════════════════════════
    # Enviar a SAP2000
    # ══════════════════════════════════════════════════════════════════

    def _on_write(self):
        if not self._load_cases:
            QMessageBox.warning(self, "Error", "Primero debes leer los Load Cases de SAP2000.")
            return

        data = self._collect_table_data()
        if not data:
            QMessageBox.information(self, "Info", "No hay datos válidos para enviar.")
            return

        if not self._validate_table():
            QMessageBox.warning(
                self,
                "Nombres inválidos",
                "Existen combinaciones con nombre vacío o duplicado.\n"
                "Revisa las filas resaltadas en rojo antes de enviar.",
            )
            return

        current_names = {d["name"] for d in data}
        names_to_delete = sorted(self._original_combo_names - current_names)
        names_to_add = sorted(current_names - self._original_combo_names)

        names_to_modify = sorted(
            name for d in data
            if (name := d["name"]) in self._original_combo_data
            and (
                d["type"] != self._original_combo_data[name]["type"]
                or d["items"] != self._original_combo_data[name]["items"]
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

        reply = QMessageBox.question(
            self,
            "Enviar Combinaciones",
            msg,
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self._log_append("\n─── Enviando a SAP2000 ────────────────────────────")
        if names_to_delete:
            self._log_append(f"  Eliminando: {', '.join(names_to_delete)}")
        self._busy(True)
        self._worker = WriteWorker(self._backend, data, names_to_delete)
        self._worker.finished.connect(self._on_write_done)
        self._worker.start()

    def _on_write_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            count = result.get("count", 0)
            deleted = result.get("deleted", 0)
            failed = result.get("failed_deletions", [])

            parts = [f"✔ {count} combinaciones enviadas a SAP2000"]
            if deleted:
                parts.append(f"{deleted} eliminadas")
            if failed:
                parts.append(f"⚠ No se pudieron eliminar: {', '.join(failed)}")
            self._log_append("  |  ".join(parts))

            # sincronizar snapshot con el estado actual de la tabla
            sent_data = self._collect_table_data()
            self._original_combo_names = {d["name"] for d in sent_data}
            self._original_combo_data = {
                d["name"]: {"type": d["type"], "items": dict(d["items"])}
                for d in sent_data
            }
            self._set_dirty(False)
        else:
            self._log_append(f"✘ Error: {result.get('error', 'Error desconocido')}")

    # ══════════════════════════════════════════════════════════════════
    # Desconectar
    # ══════════════════════════════════════════════════════════════════

    def _on_disconnect(self):
        self._log_append("Desconectando...")
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, result: dict):
        self._busy(False)
        self._log_append("✔ Desconectado de SAP2000")
        self._set_connected(False)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())