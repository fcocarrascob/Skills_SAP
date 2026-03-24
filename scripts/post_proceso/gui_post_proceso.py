"""
GUI Post Proceso — SAP2000
==========================
Interfaz principal multi-pestaña para extracción de resultados de SAP2000.

Estructura:
    MainWindow
    ├── Header: status + Conectar / Desconectar  (compartido)
    ├── QTabWidget
    │   └── Tab "Estabilidad"  → EstabilidadTab
    └── Log (compartido)

Para agregar nuevas pestañas:
    1. Crear backend_<nombre>.py en esta misma carpeta
    2. Crear la clase <Nombre>Tab(QWidget) en este archivo
    3. Agregar self._tabs.addTab(<Nombre>Tab(self._conn), "<Nombre>")
"""

import sys
import csv
from datetime import datetime

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QTextEdit,
    QTabWidget,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSplitter,
    QFileDialog,
    QAbstractItemView,
)

from backend_estabilidad import SapConnection, EstabilidadBackend


# ══════════════════════════════════════════════════════════════════════════════
# Workers — operaciones SAP2000 fuera del hilo GUI
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, conn: SapConnection):
        super().__init__()
        self._c = conn

    def run(self):
        self.finished.emit(self._c.connect(attach_to_existing=True))


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, conn: SapConnection):
        super().__init__()
        self._c = conn

    def run(self):
        self.finished.emit(self._c.disconnect())


class ReadSelectionWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: EstabilidadBackend):
        super().__init__()
        self._b = backend

    def run(self):
        try:
            self.finished.emit(self._b.get_selected_joints())
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class GetCombosWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: EstabilidadBackend):
        super().__init__()
        self._b = backend

    def run(self):
        try:
            self.finished.emit(self._b.get_combo_names())
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class GetDisplacementsWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: EstabilidadBackend, joint_names: list, combo_names: list):
        super().__init__()
        self._b = backend
        self._joints = joint_names
        self._combos = combo_names

    def run(self):
        try:
            self.finished.emit(self._b.get_joint_displacements(self._joints, self._combos))
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


# ══════════════════════════════════════════════════════════════════════════════
# Tab: Estabilidad
# ══════════════════════════════════════════════════════════════════════════════

class EstabilidadTab(QWidget):
    """
    Pestaña de Estabilidad: recupera Joint Displacements para nodos
    seleccionados manualmente en el modelo y todas las combinaciones.

    Flujo:
        1. Usuario selecciona nodos en SAP2000
        2. Clic "Leer nodos seleccionados" → muestra lista de nodos + carga combos
        3. Clic "Obtener desplazamientos" → construye tabla de resultados
        4. Clic "Exportar CSV" → guarda archivo
    """

    # Señal para enviar mensajes al log de la ventana principal
    log_message = Signal(str)

    def __init__(self, conn: SapConnection, parent=None):
        super().__init__(parent)
        self._conn = conn
        self._backend = EstabilidadBackend(conn)
        self._worker = None

        # Estado interno
        self._joint_names: list = []
        self._combo_names: list = []
        self._rows: list = []

        self._build_ui()

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        # ── Fila de botones ───────────────────────────────────────────────────
        btn_row = QHBoxLayout()

        self._btn_read = QPushButton("Leer nodos seleccionados")
        self._btn_read.setFixedHeight(32)
        self._btn_read.setEnabled(False)
        self._btn_read.setToolTip(
            "Lee los nodos actualmente seleccionados en SAP2000\n"
            "y carga la lista de combinaciones del modelo."
        )
        self._btn_read.clicked.connect(self._on_read_selection)
        btn_row.addWidget(self._btn_read)

        self._btn_run = QPushButton("Obtener desplazamientos")
        self._btn_run.setFixedHeight(32)
        self._btn_run.setEnabled(False)
        self._btn_run.setToolTip(
            "Extrae Joint Displacements para los nodos y\n"
            "combinaciones cargados."
        )
        self._btn_run.clicked.connect(self._on_get_displacements)
        btn_row.addWidget(self._btn_run)

        self._btn_calc = QPushButton("Calcular Estabilidad")
        self._btn_calc.setFixedHeight(32)
        self._btn_calc.setEnabled(False)
        self._btn_calc.setToolTip(
            "Para cada combinación calcula el % de nodos con U3 > 0 (levantamiento).\n"
            "Requiere haber obtenido los desplazamientos primero."
        )
        self._btn_calc.clicked.connect(self._on_calc_stability)
        btn_row.addWidget(self._btn_calc)

        btn_row.addStretch()

        self._btn_export = QPushButton("Exportar CSV")
        self._btn_export.setFixedHeight(32)
        self._btn_export.setEnabled(False)
        self._btn_export.clicked.connect(self._on_export_csv)
        btn_row.addWidget(self._btn_export)

        self._btn_clear = QPushButton("Limpiar")
        self._btn_clear.setFixedHeight(32)
        self._btn_clear.setEnabled(False)
        self._btn_clear.setToolTip("Borra todos los datos cargados para reiniciar el flujo.")
        self._btn_clear.clicked.connect(self._on_clear)
        btn_row.addWidget(self._btn_clear)

        layout.addLayout(btn_row)

        # ── Splitter: lista de nodos | tabla de resultados ────────────────────
        splitter = QSplitter(Qt.Horizontal)

        # Panel izquierdo — nodos seleccionados
        self._joints_box = QGroupBox("Nodos seleccionados (0)")
        joints_layout = QVBoxLayout(self._joints_box)
        self._joints_list = QListWidget()
        self._joints_list.setToolTip("Nodos leídos desde la selección activa en SAP2000")
        joints_layout.addWidget(self._joints_list)
        splitter.addWidget(self._joints_box)

        # Panel izquierdo — combinaciones encontradas
        self._combos_box = QGroupBox("Combinaciones (0)")
        combos_layout = QVBoxLayout(self._combos_box)
        self._combos_list = QListWidget()
        self._combos_list.setToolTip("Combinaciones de respuesta del modelo")
        combos_layout.addWidget(self._combos_list)
        splitter.addWidget(self._combos_box)

        # Panel derecho — tabla de resultados
        results_box = QGroupBox("Desplazamientos")
        results_layout = QVBoxLayout(results_box)

        self._table = QTableWidget()
        self._table.setColumnCount(9)
        self._table.setHorizontalHeaderLabels([
            "Nodo", "Combinación", "Tipo Paso",
            "U1 [m]", "U2 [m]", "U3 [m]",
            "R1 [rad]", "R2 [rad]", "R3 [rad]",
        ])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        results_layout.addWidget(self._table)
        splitter.addWidget(results_box)

        splitter.setSizes([150, 150, 600])
        layout.addWidget(splitter, 1)

        # ── Tabla de resumen de estabilidad ───────────────────────────────────
        stab_box = QGroupBox("Resumen de Estabilidad — Levantamiento por Combinación")
        stab_layout = QVBoxLayout(stab_box)
        stab_layout.setContentsMargins(6, 4, 6, 4)

        self._stab_table = QTableWidget()
        self._stab_table.setColumnCount(4)
        self._stab_table.setHorizontalHeaderLabels([
            "Combinación", "Nodos Totales", "Nodos U3 > 0", "% Levantamiento",
        ])
        self._stab_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._stab_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._stab_table.setAlternatingRowColors(True)
        self._stab_table.setSortingEnabled(True)
        self._stab_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._stab_table.setMaximumHeight(180)
        stab_layout.addWidget(self._stab_table)
        layout.addWidget(stab_box)

    # ── API pública (llamada desde MainWindow) ────────────────────────────────

    def set_connected(self, connected: bool):
        """Habilita/deshabilita controles según estado de conexión."""
        self._btn_read.setEnabled(connected)
        if not connected:
            self._btn_run.setEnabled(False)
            self._btn_calc.setEnabled(False)

    # ── Helpers internos ──────────────────────────────────────────────────────

    def _busy(self, is_busy: bool):
        connected = self._conn.is_connected
        self._btn_read.setEnabled(not is_busy and connected)
        self._btn_run.setEnabled(not is_busy and connected and bool(self._joint_names))
        self._btn_calc.setEnabled(not is_busy and bool(self._rows))
        self._btn_export.setEnabled(not is_busy and bool(self._rows))
        has_data = bool(self._joint_names or self._combo_names or self._rows)
        self._btn_clear.setEnabled(not is_busy and has_data)

    def _log(self, msg: str):
        self.log_message.emit(msg)

    # ── Acción: Leer selección ────────────────────────────────────────────────

    def _on_read_selection(self):
        self._log("Leyendo nodos seleccionados en SAP2000...")
        self._busy(True)
        self._worker = ReadSelectionWorker(self._backend)
        self._worker.finished.connect(self._on_read_done)
        self._worker.start()

    def _on_read_done(self, result: dict):
        if not result.get("success"):
            self._log(f"✘ Error al leer selección: {result.get('error', 'desconocido')}")
            self._busy(False)
            return

        # Actualizar estado ANTES de llamar _busy para que vea la lista correcta
        self._joint_names = result["joint_names"]
        self._busy(False)

        count = result["count"]
        self._joints_box.setTitle(f"Nodos seleccionados ({count})")
        self._joints_list.clear()
        for name in self._joint_names:
            self._joints_list.addItem(name)

        if count == 0:
            self._log("⚠ No hay nodos seleccionados en el modelo.")
            return

        preview = ", ".join(self._joint_names[:8])
        suffix = "..." if count > 8 else ""
        self._log(f"✔ {count} nodo(s): {preview}{suffix}")

        # Cargar combinaciones automáticamente
        self._load_combos()

    # ── Carga silenciosa de combinaciones ─────────────────────────────────────

    def _load_combos(self):
        self._worker = GetCombosWorker(self._backend)
        self._worker.finished.connect(self._on_combos_done)
        self._worker.start()

    def _on_combos_done(self, result: dict):
        if not result.get("success"):
            self._log(f"⚠ No se pudieron leer combinaciones: {result.get('error', '')}")
            self._combo_names = []
            return

        self._combo_names = result["combo_names"]
        count = result["count"]

        self._combos_box.setTitle(f"Combinaciones ({count})")
        self._combos_list.clear()
        for name in self._combo_names:
            self._combos_list.addItem(name)

        preview = ", ".join(self._combo_names[:5])
        suffix = "..." if count > 5 else ""
        self._log(f"✔ {count} combinación(es): {preview}{suffix}")

    # ── Acción: Obtener desplazamientos ───────────────────────────────────────

    def _on_get_displacements(self):
        if not self._joint_names:
            self._log("⚠ Primero lee los nodos seleccionados.")
            return
        if not self._combo_names:
            self._log("⚠ No hay combinaciones cargadas. Presiona 'Leer nodos seleccionados' nuevamente.")
            return

        self._log(
            f"\n─── Obteniendo desplazamientos — "
            f"{len(self._joint_names)} nodo(s), {len(self._combo_names)} combo(s) ───"
        )
        self._busy(True)
        self._worker = GetDisplacementsWorker(
            self._backend, self._joint_names, self._combo_names
        )
        self._worker.finished.connect(self._on_displacements_done)
        self._worker.start()

    def _on_displacements_done(self, result: dict):
        self._rows = result.get("rows", [])
        self._busy(False)

        if not result.get("success"):
            self._log(f"✘ Error: {result.get('error', 'desconocido')}")
            return

        skipped = result.get("skipped_joints", [])
        if skipped:
            self._log(f"⚠ Nodos sin resultados (sin análisis): {', '.join(skipped)}")

        n = result["num_results"]
        self._log(f"✔ {n} fila(s) de resultados obtenidas")
        self._populate_table(self._rows)

    def _populate_table(self, rows: list):
        self._table.setSortingEnabled(False)
        self._table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            def _str_item(val: str) -> QTableWidgetItem:
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                return item

            def _num_item(val: float, decimals: int = 6) -> QTableWidgetItem:
                item = QTableWidgetItem(f"{val:.{decimals}e}")
                item.setData(Qt.UserRole, val)   # valor numérico para ordenar
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                return item

            self._table.setItem(r, 0, _str_item(row["joint"]))
            self._table.setItem(r, 1, _str_item(row["load_case"]))
            self._table.setItem(r, 2, _str_item(row["step_type"]))
            self._table.setItem(r, 3, _num_item(row["U1"]))
            self._table.setItem(r, 4, _num_item(row["U2"]))
            self._table.setItem(r, 5, _num_item(row["U3"]))
            self._table.setItem(r, 6, _num_item(row["R1"]))
            self._table.setItem(r, 7, _num_item(row["R2"]))
            self._table.setItem(r, 8, _num_item(row["R3"]))

        self._table.setSortingEnabled(True)
        self._table.resizeColumnsToContents()

    # ── Acción: Exportar CSV ──────────────────────────────────────────────────

    # ── Acción: Limpiar ───────────────────────────────────────────────────────

    def _on_clear(self):
        """Resetea todos los datos y controles para reiniciar el flujo."""
        self._joint_names = []
        self._combo_names = []
        self._rows = []

        self._joints_list.clear()
        self._joints_box.setTitle("Nodos seleccionados (0)")

        self._combos_list.clear()
        self._combos_box.setTitle("Combinaciones (0)")

        self._table.setRowCount(0)
        self._stab_table.setRowCount(0)

        self._busy(False)
        self._log("↺ Datos limpiados — listo para nuevo flujo.")

    # ── Acción: Calcular Estabilidad ─────────────────────────────────────────

    def _on_calc_stability(self):
        """Calcula % de levantamiento (U3 > 0) por combinación de carga.

        Para combos de tipo envolvente (múltiples pasos por nodo), usa el
        valor máximo de U3 de cada nodo dentro de la combinación. Si el
        máximo es > 0, el nodo se considera en levantamiento.
        """
        if not self._rows:
            self._log("⚠ Primero obtén los desplazamientos.")
            return

        total_nodes = len(self._joint_names)
        if total_nodes == 0:
            self._log("⚠ No hay nodos de referencia.")
            return

        # Agrupar: max_U3[combo][joint] = max(U3 sobre todos los pasos)
        from collections import defaultdict
        max_u3: dict = defaultdict(lambda: defaultdict(lambda: -float("inf")))

        for row in self._rows:
            combo = row["load_case"]
            joint = row["joint"]
            if row["U3"] > max_u3[combo][joint]:
                max_u3[combo][joint] = row["U3"]

        # Calcular resumen por combinación
        summary = []
        for combo in sorted(max_u3.keys()):
            joints_in_combo = max_u3[combo]
            uplift_count = sum(1 for u3 in joints_in_combo.values() if u3 > 0)
            pct = uplift_count / total_nodes * 100.0
            summary.append({
                "combo": combo,
                "total": total_nodes,
                "uplift": uplift_count,
                "pct": pct,
            })

        # Poblar tabla de resumen
        self._stab_table.setSortingEnabled(False)
        self._stab_table.setRowCount(len(summary))

        for r, s in enumerate(summary):
            def _center(val: str) -> QTableWidgetItem:
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                return item

            pct_item = QTableWidgetItem(f"{s['pct']:.1f}%")
            pct_item.setData(Qt.UserRole, s["pct"])
            pct_item.setTextAlignment(Qt.AlignCenter)
            # Resaltar en rojo si hay levantamiento
            if s["uplift"] > 0:
                from PySide6.QtGui import QColor
                for col_item in [_center(s["combo"]), _center(str(s["total"])),
                                  _center(str(s["uplift"])), pct_item]:
                    col_item.setBackground(QColor("#fdecea"))
                self._stab_table.setItem(r, 0, _center(s["combo"]))
                self._stab_table.setItem(r, 1, _center(str(s["total"])))
                self._stab_table.setItem(r, 2, _center(str(s["uplift"])))
                self._stab_table.setItem(r, 3, pct_item)
            else:
                self._stab_table.setItem(r, 0, _center(s["combo"]))
                self._stab_table.setItem(r, 1, _center(str(s["total"])))
                self._stab_table.setItem(r, 2, _center(str(s["uplift"])))
                self._stab_table.setItem(r, 3, pct_item)

        self._stab_table.setSortingEnabled(True)

        # Log resumen
        combos_con_levantamiento = sum(1 for s in summary if s["uplift"] > 0)
        self._log(
            f"✔ Estabilidad calculada — {len(summary)} combinación(es), "
            f"{combos_con_levantamiento} con levantamiento"
        )

    # ── Acción: Exportar CSV ──────────────────────────────────────────────────

    def _on_export_csv(self):
        if not self._rows:
            return

        default_name = f"desplazamientos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar resultados como CSV", default_name, "CSV Files (*.csv)"
        )
        if not path:
            return

        fieldnames = ["joint", "load_case", "step_type", "step_num",
                      "U1", "U2", "U3", "R1", "R2", "R3"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self._rows)

        self._log(f"✔ CSV exportado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    """
    Ventana principal con QTabWidget compartido.
    La SapConnection es única e instanciada aquí; cada pestaña la recibe.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Post Proceso")
        self.setMinimumSize(960, 650)

        self._conn = SapConnection()
        self._worker = None          # referencia al worker activo (evita GC)

        # ── Widget central ────────────────────────────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(6)
        root.setContentsMargins(10, 10, 10, 10)

        # ── Header: status + botones de conexión ──────────────────────────────
        header = QHBoxLayout()

        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold; font-size: 13px;")
        header.addWidget(self._status_lbl)
        header.addStretch()

        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(32)
        self._btn_connect.setFixedWidth(150)
        self._btn_connect.clicked.connect(self._on_connect)
        header.addWidget(self._btn_connect)

        self._btn_disconnect = QPushButton("Desconectar")
        self._btn_disconnect.setFixedHeight(32)
        self._btn_disconnect.setFixedWidth(110)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        header.addWidget(self._btn_disconnect)

        root.addLayout(header)

        # ── Tab widget ────────────────────────────────────────────────────────
        self._tabs = QTabWidget()

        self._tab_estabilidad = EstabilidadTab(self._conn)
        self._tab_estabilidad.log_message.connect(self._log_append)
        self._tabs.addTab(self._tab_estabilidad, "Estabilidad")

        # Aquí se agregarán otras pestañas en el futuro:
        # self._tab_otra = OtraTab(self._conn)
        # self._tab_otra.log_message.connect(self._log_append)
        # self._tabs.addTab(self._tab_otra, "Otra Pestaña")

        root.addWidget(self._tabs, 1)

        # ── Log compartido ────────────────────────────────────────────────────
        log_box = QGroupBox("Log")
        log_layout = QVBoxLayout(log_box)
        log_layout.setContentsMargins(6, 4, 6, 4)
        self._log_widget = QTextEdit()
        self._log_widget.setReadOnly(True)
        self._log_widget.setFont(QFont("Consolas", 9))
        self._log_widget.setMaximumHeight(110)
        log_layout.addWidget(self._log_widget)
        root.addWidget(log_box)

    # ── Helpers internos ──────────────────────────────────────────────────────

    def _log_append(self, msg: str):
        self._log_widget.append(msg)

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_disconnect.setEnabled(connected)
        self._tab_estabilidad.set_connected(connected)
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold; font-size: 13px;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold; font-size: 13px;")

    def _busy_all(self, is_busy: bool):
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)

    # ── Conectar ──────────────────────────────────────────────────────────────

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._busy_all(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy_all(False)
        if result.get("connected"):
            ver  = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo cargado)"
            self._log_append(f"✔ Conectado — SAP2000 v{ver}  |  {path}")
            self._set_connected(True)
        else:
            self._log_append(f"✘ No se pudo conectar: {result.get('error', 'error desconocido')}")
            self._set_connected(False)

    # ── Desconectar ───────────────────────────────────────────────────────────

    def _on_disconnect(self):
        self._log_append("Desconectando...")
        self._busy_all(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, _result: dict):
        self._busy_all(False)
        self._log_append("✔ Desconectado de SAP2000")
        self._set_connected(False)


# ══════════════════════════════════════════════════════════════════════════════
# Entry Point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
