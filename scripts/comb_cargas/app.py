"""
SAP2000 — Load Patterns & Combinaciones de Carga
=================================================
Entry point. Combina LoadPatternsTab y CombosTab en una ventana con log compartido.
"""

import sys

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel, QPushButton, QTextEdit, QTabWidget, QMessageBox,
)

from sap_connection import SapConnection
from lp_gui import LoadPatternsTab
from combos_gui import CombosTab


class ConnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        self.finished.emit(self._conn.connect(attach_to_existing=True))


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        self.finished.emit(self._conn.disconnect())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Load Patterns & Combinaciones de Carga")
        self.setMinimumWidth(960)

        self._conn = SapConnection()
        self._worker = None

        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Status ────────────────────────────────────────────────────
        status_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        status_row.addWidget(self._status_lbl)
        status_row.addStretch()
        root.addLayout(status_row)

        # ── Conectar / Desconectar ─────────────────────────────────────
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

        # ── Tabs ───────────────────────────────────────────────────────
        self._lp_tab = LoadPatternsTab(self._conn, self._log_append)
        self._combos_tab = CombosTab(self._conn, self._log_append)

        self._lp_tab.dirty_changed.connect(lambda _: self._update_title())
        self._combos_tab.dirty_changed.connect(lambda _: self._update_title())
        self._lp_tab.busy_changed.connect(self._on_tab_busy)
        self._combos_tab.busy_changed.connect(self._on_tab_busy)

        self._tabs = QTabWidget()
        self._tabs.addTab(self._lp_tab, "Load Patterns")
        self._tabs.addTab(self._combos_tab, "Combinaciones de Carga")
        root.addWidget(self._tabs)

        # ── Output log ────────────────────────────────────────────────
        log_box = QGroupBox("Salida")
        log_layout = QVBoxLayout(log_box)
        self._log_widget = QTextEdit()
        self._log_widget.setReadOnly(True)
        self._log_widget.setFont(QFont("Consolas", 9))
        self._log_widget.setMinimumHeight(100)
        log_layout.addWidget(self._log_widget)
        root.addWidget(log_box)

    def _log_append(self, text: str):
        self._log_widget.append(text)

    def _update_title(self):
        base = "SAP2000 — Load Patterns & Combinaciones de Carga"
        dirty = self._lp_tab.is_dirty() or self._combos_tab.is_dirty()
        self.setWindowTitle(f"● {base}" if dirty else base)

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_disconnect.setEnabled(connected)
        self._lp_tab.set_connected(connected)
        self._combos_tab.set_connected(connected)
        self._status_lbl.setText(
            "Estado: conectado ✔" if connected else "Estado: desconectado"
        )
        self._status_lbl.setStyleSheet(
            "color: #27ae60; font-weight: bold;" if connected
            else "color: #c0392b; font-weight: bold;"
        )

    def _on_tab_busy(self, is_busy: bool):
        """Deshabilita connect/disconnect mientras un tab opera en SAP2000."""
        connected = self._conn.is_connected
        self._btn_connect.setEnabled(not is_busy and not connected)
        self._btn_disconnect.setEnabled(not is_busy and connected)

    def closeEvent(self, event):
        dirty_tabs = []
        if self._lp_tab.is_dirty():
            dirty_tabs.append("Load Patterns")
        if self._combos_tab.is_dirty():
            dirty_tabs.append("Combinaciones")
        if dirty_tabs:
            reply = QMessageBox.question(
                self,
                "Cambios sin guardar",
                f"Hay cambios pendientes en: {', '.join(dirty_tabs)}.\n¿Salir de todas formas?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return
        event.accept()

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._btn_connect.setEnabled(False)
        self._btn_disconnect.setEnabled(False)
        self._lp_tab.set_busy(True)
        self._combos_tab.set_busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            self._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self._set_connected(True)
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    def _on_disconnect(self):
        self._log_append("Desconectando...")
        self._btn_connect.setEnabled(False)
        self._btn_disconnect.setEnabled(False)
        self._lp_tab.set_busy(True)
        self._combos_tab.set_busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, result: dict):
        self._log_append("✔ Desconectado de SAP2000")
        self._set_connected(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
