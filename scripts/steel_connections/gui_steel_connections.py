"""
GUI — SAP2000 Steel Connections: Ventana Principal con Tabs
=============================================================
Integra los módulos de conexiones de acero en una ventana única:
  Tab 1: Placas Pernadas (Bolt Plates + Gap Links)
  Tab 2: Perfiles de Acero (como Placas Shell)
  Tab 3: Patrón Multi-Perno (filas × columnas con orientación)
  Tab 4: Placa Simple (malla rectangular con orientación arbitraria)

La conexión SAP2000 es compartida entre todos los tabs.
Botón "Crear Modelo Base" crea un modelo limpio N-mm-C con materiales de acero.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from shared import SapConnection, ConnectWorker, DisconnectWorker, BaseModelWorker
from gui_bolt_plates import BoltPlatesGUI
from gui_multi_bolt import MultiBoltGUI
from gui_steel_profiles import SteelProfilesGUI
from gui_simple_plate import SimplePlateGUI


# ══════════════════════════════════════════════════════════════════════════════
# Ventana principal
# ══════════════════════════════════════════════════════════════════════════════

class SteelConnectionsWindow(QWidget):
    """Ventana principal: tabs para módulos de conexiones de acero."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Conexiones de Acero")
        self.setMinimumSize(780, 700)

        self._conn = SapConnection()
        self._worker = None

        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Estado y conexión (compartida) ───────────────────────────────
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        root.addWidget(self._status_lbl)

        conn_row = QHBoxLayout()
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(34)
        self._btn_connect.clicked.connect(self._on_connect)

        self._btn_disconnect = QPushButton("Desconectar")
        self._btn_disconnect.setFixedHeight(34)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)

        self._btn_base_model = QPushButton("Crear Modelo Base")
        self._btn_base_model.setFixedHeight(34)
        self._btn_base_model.setEnabled(False)
        self._btn_base_model.setToolTip(
            "Crea un modelo nuevo en blanco con unidades N-mm-C\n"
            "y materiales de acero: A36, A500_GrB, A325, A490"
        )
        self._btn_base_model.clicked.connect(self._on_create_base_model)

        conn_row.addWidget(self._btn_connect)
        conn_row.addWidget(self._btn_disconnect)
        conn_row.addWidget(self._btn_base_model)
        root.addLayout(conn_row)

        # ── Tabs ─────────────────────────────────────────────────────────
        self._tabs = QTabWidget()
        self._tabs.setFont(QFont("Segoe UI", 10))

        # Tab 1: Bolt Plates — inyectar conexión compartida
        self._bolt_gui = BoltPlatesGUI(connection=self._conn)
        # Ocultar los controles de conexión propios del tab
        self._bolt_gui._status_lbl.setVisible(False)
        self._bolt_gui._btn_connect.setVisible(False)
        self._bolt_gui._btn_disconnect.setVisible(False)

        # Tab 2: Steel Profiles — inyectar conexión compartida
        self._profiles_gui = SteelProfilesGUI(connection=self._conn)
        self._profiles_gui._status_lbl.setVisible(False)
        self._profiles_gui._btn_connect.setVisible(False)
        self._profiles_gui._btn_disconnect.setVisible(False)

        # Tab 3: Multi-Bolt Pattern — inyectar conexión compartida
        self._multi_bolt_gui = MultiBoltGUI(connection=self._conn)
        self._multi_bolt_gui._status_lbl.setVisible(False)
        self._multi_bolt_gui._btn_connect.setVisible(False)
        self._multi_bolt_gui._btn_disconnect.setVisible(False)

        # Tab 4: Placa Simple — inyectar conexión compartida
        self._plate_gui = SimplePlateGUI(connection=self._conn)
        self._plate_gui._status_lbl.setVisible(False)
        self._plate_gui._btn_connect.setVisible(False)
        self._plate_gui._btn_disconnect.setVisible(False)

        self._tabs.addTab(self._bolt_gui, "Placas Pernadas")
        self._tabs.addTab(self._profiles_gui, "Perfiles de Acero")
        self._tabs.addTab(self._multi_bolt_gui, "Patrón Multi-Perno")
        self._tabs.addTab(self._plate_gui, "Placa Simple")
        root.addWidget(self._tabs)

    # ── Helpers ──────────────────────────────────────────────────────────

    def _busy(self, is_busy: bool):
        connected = self._conn.is_connected
        self._btn_connect.setEnabled(not is_busy and not connected)
        self._btn_disconnect.setEnabled(not is_busy and connected)
        self._btn_base_model.setEnabled(not is_busy and connected)

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_disconnect.setEnabled(connected)
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")

        # Propagar estado a todos los tabs
        self._bolt_gui._set_connected(connected)
        self._profiles_gui._set_connected(connected)
        self._multi_bolt_gui._set_connected(connected)
        self._plate_gui._set_connected(connected)

    # ── Slots ────────────────────────────────────────────────────────────

    def _on_connect(self):
        self._busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy(False)
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            props = result.get("shell_props", [])

            self._set_connected(True)

            # Propagar propiedades Shell a todos los tabs
            self._bolt_gui.populate_area_props(props)
            self._profiles_gui.populate_area_props(props)
            self._multi_bolt_gui.populate_area_props(props)
            self._plate_gui.populate_area_props(props)

            # Log en todos los tabs
            msg = f"✔ Conectado — versión {ver}  |  modelo: {path}"
            self._bolt_gui._log_append(msg)
            self._profiles_gui._log_append(msg)
            self._multi_bolt_gui._log_append(msg)
            self._plate_gui._log_append(msg)
            if props:
                info = f"  Propiedades Shell cargadas: {len(props)}"
                self._bolt_gui._log_append(info)
                self._profiles_gui._log_append(info)
                self._multi_bolt_gui._log_append(info)
                self._plate_gui._log_append(info)
        else:
            err = result.get("error", "Error desconocido")
            self._set_connected(False)
            self._bolt_gui._log_append(f"✘ No se pudo conectar: {err}")
            self._profiles_gui._log_append(f"✘ No se pudo conectar: {err}")
            self._multi_bolt_gui._log_append(f"✘ No se pudo conectar: {err}")
            self._plate_gui._log_append(f"✘ No se pudo conectar: {err}")

    def _on_disconnect(self):
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, result: dict):
        self._busy(False)
        self._set_connected(False)
        self._bolt_gui.populate_area_props([])
        self._profiles_gui.populate_area_props([])
        self._multi_bolt_gui.populate_area_props([])
        self._plate_gui.populate_area_props([])
        self._bolt_gui._log_append("✔ Desconectado de SAP2000")
        self._profiles_gui._log_append("✔ Desconectado de SAP2000")
        self._multi_bolt_gui._log_append("✔ Desconectado de SAP2000")
        self._plate_gui._log_append("✔ Desconectado de SAP2000")

    def _on_create_base_model(self):
        self._busy(True)
        self._worker = BaseModelWorker(self._conn)
        self._worker.finished.connect(self._on_base_model_done)
        self._worker.start()

    def _on_base_model_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            mats = result.get("materials_created", 0)
            msg = f"✔ Modelo base creado — {mats} materiales (N-mm-C)"
            self._bolt_gui._log_append(msg)
            self._profiles_gui._log_append(msg)
            self._multi_bolt_gui._log_append(msg)
            self._plate_gui._log_append(msg)

            # Recargar propiedades Shell del nuevo modelo
            props = []
            try:
                ret = self._conn.sap_model.PropArea.GetNameList(0, [])
                if isinstance(ret, (list, tuple)) and int(ret[-1]) == 0 and int(ret[0]) > 0:
                    props = list(ret[1])
            except Exception:
                pass
            self._bolt_gui.populate_area_props(props)
            self._profiles_gui.populate_area_props(props)
            self._multi_bolt_gui.populate_area_props(props)
            self._plate_gui.populate_area_props(props)

            errors = result.get("errors", [])
            if errors:
                for e in errors:
                    for gui in (self._bolt_gui, self._profiles_gui,
                                self._multi_bolt_gui, self._plate_gui):
                        gui._log_append(f"  ⚠ {e}")
        else:
            err = result.get("error", "Error desconocido")
            for gui in (self._bolt_gui, self._profiles_gui,
                        self._multi_bolt_gui, self._plate_gui):
                gui._log_append(f"✘ Modelo base: {err}")


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteelConnectionsWindow()
    window.show()
    sys.exit(app.exec())
