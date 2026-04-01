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
    QMessageBox,
    QDoubleSpinBox,
    QComboBox,
)

from backend_estabilidad import SapConnection, EstabilidadBackend
from backend_shells import ShellsBackend
from backend_mod_fund import ModFundBackend


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


# ── Workers: Shells ───────────────────────────────────────────────────────────

class ReadAreasWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: ShellsBackend):
        super().__init__()
        self._b = backend

    def run(self):
        try:
            self.finished.emit(self._b.get_selected_areas())
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class GetShellCombosWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: ShellsBackend):
        super().__init__()
        self._b = backend

    def run(self):
        try:
            self.finished.emit(self._b.get_combo_names())
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class GetShellForcesWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: ShellsBackend, area_names: list, combo_names: list):
        super().__init__()
        self._b = backend
        self._areas = area_names
        self._combos = combo_names

    def run(self):
        try:
            self.finished.emit(self._b.get_shell_forces(self._areas, self._combos))
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


# ── Workers: Mod FUND ─────────────────────────────────────────────────────────

class CheckAnalysisWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: ModFundBackend):
        super().__init__()
        self._b = backend

    def run(self):
        try:
            self.finished.emit(self._b.check_analysis_done())
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class GetReactionsWorker(QThread):
    """Obtiene nodos restringidos, load cases, secciones y reacciones en un solo paso."""
    finished = Signal(dict)

    def __init__(self, backend: ModFundBackend):
        super().__init__()
        self._b = backend

    def run(self):
        try:
            joints_r = self._b.get_restricted_joints()
            if not joints_r["success"]:
                self.finished.emit(joints_r)
                return

            cases_r = self._b.get_load_cases_no_modal()
            if not cases_r["success"]:
                self.finished.emit(cases_r)
                return

            secs_r = self._b.get_frame_sections()

            react_r = self._b.get_joint_reactions(
                joints_r["joint_names"], cases_r["case_names"]
            )
            if not react_r["success"]:
                self.finished.emit(react_r)
                return

            self.finished.emit({
                "success": True,
                "joint_names":    joints_r["joint_names"],
                "joint_count":    joints_r["count"],
                "case_names":     cases_r["case_names"],
                "case_count":     cases_r["count"],
                "section_names":  secs_r.get("section_names", []),
                "rows":           react_r["rows"],
                "num_results":    react_r["num_results"],
                "skipped_joints": react_r.get("skipped_joints", []),
            })
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class BuildFoundationWorker(QThread):
    finished = Signal(dict)

    def __init__(
        self,
        backend: ModFundBackend,
        joint_names: list,
        reactions_rows: list,
        section_name: str,
        pile_depth: float,
    ):
        super().__init__()
        self._b = backend
        self._joints = joint_names
        self._rows = reactions_rows
        self._section = section_name
        self._depth = pile_depth

    def run(self):
        try:
            self.finished.emit(
                self._b.build_foundation_model(
                    self._joints, self._rows, self._section, self._depth
                )
            )
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
# Tab: Shells
# ══════════════════════════════════════════════════════════════════════════════

class ShellsTab(QWidget):
    """
    Pestaña de Shells: recupera AreaForceShell para áreas seleccionadas
    manualmente en el modelo y todas las combinaciones.

    Flujo:
        1. Usuario selecciona shells en SAP2000
        2. Clic "Leer Áreas" → lista de áreas + carga combos automáticamente
        3. Clic "Obtener Shell Forces" → tabla detallada de resultados
        4. Clic "Calcular Máx/Mín" → resumen por combinación
        5. Clic "Exportar CSV" → guarda tabla detallada
    """

    log_message = Signal(str)

    def __init__(self, conn: SapConnection, parent=None):
        super().__init__(parent)
        self._conn = conn
        self._backend = ShellsBackend(conn)
        self._worker = None

        self._area_names: list = []
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

        self._btn_read = QPushButton("Leer Áreas")
        self._btn_read.setFixedHeight(32)
        self._btn_read.setEnabled(False)
        self._btn_read.setToolTip(
            "Lee los shells (AreaObj) actualmente seleccionados en SAP2000\n"
            "y carga la lista de combinaciones del modelo."
        )
        self._btn_read.clicked.connect(self._on_read_areas)
        btn_row.addWidget(self._btn_read)

        self._btn_run = QPushButton("Obtener Shell Forces")
        self._btn_run.setFixedHeight(32)
        self._btn_run.setEnabled(False)
        self._btn_run.setToolTip(
            "Extrae AreaForceShell para las áreas y combinaciones cargadas."
        )
        self._btn_run.clicked.connect(self._on_get_shell_forces)
        btn_row.addWidget(self._btn_run)

        self._btn_calc = QPushButton("Calcular Máx/Mín")
        self._btn_calc.setFixedHeight(32)
        self._btn_calc.setEnabled(False)
        self._btn_calc.setToolTip(
            "Calcula máximo y mínimo de M11, M22, V13, V23 por combinación.\n"
            "Requiere haber obtenido las fuerzas primero."
        )
        self._btn_calc.clicked.connect(self._on_calc_extremes)
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

        # ── Splitter: listas | tabla de resultados ────────────────────────────
        splitter = QSplitter(Qt.Horizontal)

        self._areas_box = QGroupBox("Áreas seleccionadas (0)")
        areas_layout = QVBoxLayout(self._areas_box)
        self._areas_list = QListWidget()
        self._areas_list.setToolTip("AreaObj leídos desde la selección activa en SAP2000")
        areas_layout.addWidget(self._areas_list)
        splitter.addWidget(self._areas_box)

        self._combos_box = QGroupBox("Combinaciones (0)")
        combos_layout = QVBoxLayout(self._combos_box)
        self._combos_list = QListWidget()
        self._combos_list.setToolTip("Combinaciones de respuesta del modelo")
        combos_layout.addWidget(self._combos_list)
        splitter.addWidget(self._combos_box)

        results_box = QGroupBox("Shell Forces")
        results_layout = QVBoxLayout(results_box)
        self._table = QTableWidget()
        self._table.setColumnCount(10)
        self._table.setHorizontalHeaderLabels([
            "Área", "Punto", "Combinación", "Tipo Paso",
            "F11 [kN/m]", "F22 [kN/m]", "F12 [kN/m]",
            "M11 [kN·m/m]", "M22 [kN·m/m]", "M12 [kN·m/m]",
        ])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        results_layout.addWidget(self._table)
        splitter.addWidget(results_box)

        splitter.setSizes([140, 140, 620])
        layout.addWidget(splitter, 1)

        # ── Tabla de resumen Máx/Mín ──────────────────────────────────────────
        summary_box = QGroupBox("Resumen Máx/Mín por Combinación")
        summary_layout = QVBoxLayout(summary_box)
        summary_layout.setContentsMargins(6, 4, 6, 4)

        self._summary_table = QTableWidget()
        self._summary_table.setColumnCount(9)
        self._summary_table.setHorizontalHeaderLabels([
            "Combinación",
            "M11 máx", "M11 mín",
            "M22 máx", "M22 mín",
            "V13 máx", "V13 mín",
            "V23 máx", "V23 mín",
        ])
        self._summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._summary_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._summary_table.setAlternatingRowColors(True)
        self._summary_table.setSortingEnabled(True)
        self._summary_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._summary_table.setMaximumHeight(180)
        summary_layout.addWidget(self._summary_table)
        layout.addWidget(summary_box)

    # ── API pública ───────────────────────────────────────────────────────────

    def set_connected(self, connected: bool):
        self._btn_read.setEnabled(connected)
        if not connected:
            self._btn_run.setEnabled(False)
            self._btn_calc.setEnabled(False)

    # ── Helpers internos ──────────────────────────────────────────────────────

    def _busy(self, is_busy: bool):
        connected = self._conn.is_connected
        self._btn_read.setEnabled(not is_busy and connected)
        self._btn_run.setEnabled(not is_busy and connected and bool(self._area_names))
        self._btn_calc.setEnabled(not is_busy and bool(self._rows))
        self._btn_export.setEnabled(not is_busy and bool(self._rows))
        has_data = bool(self._area_names or self._combo_names or self._rows)
        self._btn_clear.setEnabled(not is_busy and has_data)

    def _log(self, msg: str):
        self.log_message.emit(msg)

    # ── Acción: Leer áreas ────────────────────────────────────────────────────

    def _on_read_areas(self):
        self._log("Leyendo áreas seleccionadas en SAP2000...")
        self._busy(True)
        self._worker = ReadAreasWorker(self._backend)
        self._worker.finished.connect(self._on_read_done)
        self._worker.start()

    def _on_read_done(self, result: dict):
        if not result.get("success"):
            self._log(f"✘ Error al leer selección: {result.get('error', 'desconocido')}")
            self._busy(False)
            return

        self._area_names = result["area_names"]
        self._busy(False)

        count = result["count"]
        self._areas_box.setTitle(f"Áreas seleccionadas ({count})")
        self._areas_list.clear()
        for name in self._area_names:
            self._areas_list.addItem(name)

        if count == 0:
            self._log("⚠ No hay áreas (shells) seleccionadas en el modelo.")
            return

        preview = ", ".join(self._area_names[:8])
        suffix = "..." if count > 8 else ""
        self._log(f"✔ {count} área(s): {preview}{suffix}")
        self._load_combos()

    # ── Carga silenciosa de combinaciones ─────────────────────────────────────

    def _load_combos(self):
        self._worker = GetShellCombosWorker(self._backend)
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

    # ── Acción: Obtener shell forces ──────────────────────────────────────────

    def _on_get_shell_forces(self):
        if not self._area_names:
            self._log("⚠ Primero lee las áreas seleccionadas.")
            return
        if not self._combo_names:
            self._log("⚠ No hay combinaciones cargadas. Presiona 'Leer Áreas' nuevamente.")
            return

        self._log(
            f"\n─── Obteniendo shell forces — "
            f"{len(self._area_names)} área(s), {len(self._combo_names)} combo(s) ───"
        )
        self._busy(True)
        self._worker = GetShellForcesWorker(
            self._backend, self._area_names, self._combo_names
        )
        self._worker.finished.connect(self._on_forces_done)
        self._worker.start()

    def _on_forces_done(self, result: dict):
        self._rows = result.get("rows", [])
        self._busy(False)

        if not result.get("success"):
            self._log(f"✘ Error: {result.get('error', 'desconocido')}")
            return

        skipped = result.get("skipped_areas", [])
        if skipped:
            self._log(f"⚠ Áreas sin resultados: {', '.join(skipped)}")

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

            def _num_item(val: float) -> QTableWidgetItem:
                item = QTableWidgetItem(f"{val:.4f}")
                item.setData(Qt.UserRole, val)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                return item

            self._table.setItem(r, 0, _str_item(row["area"]))
            self._table.setItem(r, 1, _str_item(row["point_elm"]))
            self._table.setItem(r, 2, _str_item(row["load_case"]))
            self._table.setItem(r, 3, _str_item(row["step_type"]))
            self._table.setItem(r, 4, _num_item(row["F11"]))
            self._table.setItem(r, 5, _num_item(row["F22"]))
            self._table.setItem(r, 6, _num_item(row["F12"]))
            self._table.setItem(r, 7, _num_item(row["M11"]))
            self._table.setItem(r, 8, _num_item(row["M22"]))
            self._table.setItem(r, 9, _num_item(row["M12"]))

        self._table.setSortingEnabled(True)
        self._table.resizeColumnsToContents()

    # ── Acción: Calcular Máx/Mín ──────────────────────────────────────────────

    def _on_calc_extremes(self):
        """Calcula máx y mín de M11, M22, V13, V23 por combinación de carga.

        Para combos con múltiples pasos (envolventes), los extremos ya están
        implícitos en las filas — se busca el global por combo.
        """
        if not self._rows:
            self._log("⚠ Primero obtén las shell forces.")
            return

        # Acumular por combo
        from collections import defaultdict
        stats: dict = defaultdict(lambda: {
            "M11_max": -float("inf"), "M11_min":  float("inf"),
            "M22_max": -float("inf"), "M22_min":  float("inf"),
            "V13_max": -float("inf"), "V13_min":  float("inf"),
            "V23_max": -float("inf"), "V23_min":  float("inf"),
        })

        for row in self._rows:
            s = stats[row["load_case"]]
            if row["M11"] > s["M11_max"]: s["M11_max"] = row["M11"]
            if row["M11"] < s["M11_min"]: s["M11_min"] = row["M11"]
            if row["M22"] > s["M22_max"]: s["M22_max"] = row["M22"]
            if row["M22"] < s["M22_min"]: s["M22_min"] = row["M22"]
            if row["V13"] > s["V13_max"]: s["V13_max"] = row["V13"]
            if row["V13"] < s["V13_min"]: s["V13_min"] = row["V13"]
            if row["V23"] > s["V23_max"]: s["V23_max"] = row["V23"]
            if row["V23"] < s["V23_min"]: s["V23_min"] = row["V23"]

        combos = sorted(stats.keys())
        self._summary_table.setSortingEnabled(False)
        self._summary_table.setRowCount(len(combos))

        for r, combo in enumerate(combos):
            s = stats[combo]

            def _center(val: str) -> QTableWidgetItem:
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                return item

            def _num(val: float) -> QTableWidgetItem:
                item = QTableWidgetItem(f"{val:.4f}")
                item.setData(Qt.UserRole, val)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                return item

            self._summary_table.setItem(r, 0, _center(combo))
            self._summary_table.setItem(r, 1, _num(s["M11_max"]))
            self._summary_table.setItem(r, 2, _num(s["M11_min"]))
            self._summary_table.setItem(r, 3, _num(s["M22_max"]))
            self._summary_table.setItem(r, 4, _num(s["M22_min"]))
            self._summary_table.setItem(r, 5, _num(s["V13_max"]))
            self._summary_table.setItem(r, 6, _num(s["V13_min"]))
            self._summary_table.setItem(r, 7, _num(s["V23_max"]))
            self._summary_table.setItem(r, 8, _num(s["V23_min"]))

        self._summary_table.setSortingEnabled(True)
        self._log(f"✔ Máx/Mín calculados — {len(combos)} combinación(es)")

    # ── Acción: Limpiar ───────────────────────────────────────────────────────

    def _on_clear(self):
        self._area_names = []
        self._combo_names = []
        self._rows = []

        self._areas_list.clear()
        self._areas_box.setTitle("Áreas seleccionadas (0)")
        self._combos_list.clear()
        self._combos_box.setTitle("Combinaciones (0)")
        self._table.setRowCount(0)
        self._summary_table.setRowCount(0)

        self._busy(False)
        self._log("↺ Datos limpiados — listo para nuevo flujo.")

    # ── Acción: Exportar CSV ──────────────────────────────────────────────────

    def _on_export_csv(self):
        if not self._rows:
            return

        default_name = f"shell_forces_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar resultados como CSV", default_name, "CSV Files (*.csv)"
        )
        if not path:
            return

        fieldnames = ["area", "point_elm", "load_case", "step_type", "step_num",
                      "F11", "F22", "F12", "M11", "M22", "M12", "V13", "V23"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(self._rows)

        self._log(f"✔ CSV exportado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Tab: Mod FUND
# ══════════════════════════════════════════════════════════════════════════════

class ModFundTab(QWidget):
    """
    Pestaña Mod FUND: genera un modelo de fundación a partir de un modelo
    estructural ya analizado.

    Flujo:
        1. Clic "1. Verificar Análisis" → confirma que el modelo está bloqueado
        2. Clic "2. Obtener Reacciones" → lee nodos restringidos, load cases
           (sin MODAL), secciones disponibles y reacciones nodales
        3. Seleccionar sección y profundidad de pila
        4. Clic "3. Construir Modelo Fundación" → confirmación → ejecuta:
           - Desbloquea modelo
           - Crea frames hacia Z- desde cada nodo restringido
           - Elimina estructura superior (frames + áreas)
           - Crea load patterns RF_<case> y asigna reacciones como fuerzas
    """

    log_message = Signal(str)

    def __init__(self, conn: SapConnection, parent=None):
        super().__init__(parent)
        self._conn = conn
        self._backend = ModFundBackend(conn)
        self._worker = None

        # Estado interno
        self._analysis_ok: bool = False
        self._joint_names: list = []
        self._case_names: list = []
        self._reaction_rows: list = []

        self._build_ui()

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        # ── Paso 1: Verificar análisis ────────────────────────────────────────
        row1 = QHBoxLayout()

        self._btn_check = QPushButton("1. Verificar Análisis")
        self._btn_check.setFixedHeight(32)
        self._btn_check.setFixedWidth(170)
        self._btn_check.setEnabled(False)
        self._btn_check.setToolTip(
            "Verifica que el análisis fue ejecutado.\n"
            "SAP2000 bloquea el modelo al completar el análisis."
        )
        self._btn_check.clicked.connect(self._on_check_analysis)
        row1.addWidget(self._btn_check)

        self._analysis_lbl = QLabel("Estado: sin verificar")
        self._analysis_lbl.setStyleSheet("color: #7f8c8d; font-weight: bold;")
        row1.addWidget(self._analysis_lbl)
        row1.addStretch()
        layout.addLayout(row1)

        # ── Paso 2: Obtener reacciones ────────────────────────────────────────
        row2 = QHBoxLayout()

        self._btn_get = QPushButton("2. Obtener Reacciones")
        self._btn_get.setFixedHeight(32)
        self._btn_get.setFixedWidth(190)
        self._btn_get.setEnabled(False)
        self._btn_get.setToolTip(
            "Lee nodos con restricciones, load cases (sin MODAL),\n"
            "secciones disponibles y extrae las reacciones nodales."
        )
        self._btn_get.clicked.connect(self._on_get_reactions)
        row2.addWidget(self._btn_get)
        row2.addStretch()
        layout.addLayout(row2)

        # ── Splitter: nodos | load cases | tabla reacciones ───────────────────
        splitter = QSplitter(Qt.Horizontal)

        self._joints_box = QGroupBox("Nodos Restringidos (0)")
        joints_lyt = QVBoxLayout(self._joints_box)
        self._joints_list = QListWidget()
        self._joints_list.setToolTip("Nodos con al menos un DOF restringido")
        joints_lyt.addWidget(self._joints_list)
        splitter.addWidget(self._joints_box)

        self._cases_box = QGroupBox("Load Cases (0)")
        cases_lyt = QVBoxLayout(self._cases_box)
        self._cases_list = QListWidget()
        self._cases_list.setToolTip("Load cases del modelo (tipo MODAL excluido)")
        cases_lyt.addWidget(self._cases_list)
        splitter.addWidget(self._cases_box)

        react_box = QGroupBox("Reacciones (0 filas)")
        react_lyt = QVBoxLayout(react_box)
        self._react_table = QTableWidget()
        self._react_table.setColumnCount(9)
        self._react_table.setHorizontalHeaderLabels([
            "Nodo", "Load Case", "Paso",
            "F1", "F2", "F3",
            "M1", "M2", "M3",
        ])
        self._react_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self._react_table.horizontalHeader().setStretchLastSection(True)
        self._react_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._react_table.setAlternatingRowColors(True)
        self._react_table.setSortingEnabled(True)
        self._react_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        react_lyt.addWidget(self._react_table)
        splitter.addWidget(react_box)

        splitter.setSizes([140, 140, 620])
        layout.addWidget(splitter, 1)

        # ── Configuración: sección y profundidad ──────────────────────────────
        cfg_box = QGroupBox("Configuración")
        cfg_lyt = QVBoxLayout(cfg_box)
        cfg_lyt.setContentsMargins(8, 6, 8, 6)
        cfg_lyt.setSpacing(6)

        sec_row = QHBoxLayout()
        sec_row.addWidget(QLabel("Sección Frame:"))
        self._section_combo = QComboBox()
        self._section_combo.setMinimumWidth(200)
        self._section_combo.setToolTip(
            "Sección a asignar a los frames tipo pila.\n"
            "Se pobla al completar el Paso 2."
        )
        sec_row.addWidget(self._section_combo)
        sec_row.addStretch()
        cfg_lyt.addLayout(sec_row)

        depth_row = QHBoxLayout()
        depth_row.addWidget(QLabel("Profundidad pila (hacia Z-):"))
        self._depth_spin = QDoubleSpinBox()
        self._depth_spin.setRange(0.01, 9999.0)
        self._depth_spin.setValue(5.0)
        self._depth_spin.setDecimals(2)
        self._depth_spin.setSingleStep(0.5)
        self._depth_spin.setFixedWidth(100)
        self._depth_spin.setToolTip(
            "Longitud del elemento pila en dirección Z-.\n"
            "El frame se crea desde el nodo restringido hacia abajo."
        )
        depth_row.addWidget(self._depth_spin)
        depth_row.addWidget(QLabel("[unidades del modelo]"))
        depth_row.addStretch()
        cfg_lyt.addLayout(depth_row)

        layout.addWidget(cfg_box)

        # ── Advertencia y botón de construcción ───────────────────────────────
        warn_lbl = QLabel(
            "\u26a0  IRREVERSIBLE: Esta operación modifica el modelo SAP2000 abierto. "
            "Se eliminarán todos los frames y áreas de la estructura superior. "
            "Guarde una copia del modelo antes de continuar."
        )
        warn_lbl.setWordWrap(True)
        warn_lbl.setStyleSheet(
            "background: #fff3cd; color: #856404; "
            "border: 1px solid #ffc107; border-radius: 4px; padding: 6px;"
        )
        layout.addWidget(warn_lbl)

        self._btn_build = QPushButton("3. Construir Modelo Fundación")
        self._btn_build.setFixedHeight(38)
        self._btn_build.setEnabled(False)
        self._btn_build.setStyleSheet(
            "QPushButton { background-color: #e74c3c; color: white; "
            "font-weight: bold; border-radius: 4px; } "
            "QPushButton:hover { background-color: #c0392b; } "
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }"
        )
        self._btn_build.setToolTip(
            "Desbloquea el modelo, crea frames pila hacia Z-, "
            "elimina la estructura superior y asigna las reacciones como fuerzas."
        )
        self._btn_build.clicked.connect(self._on_build_foundation)
        layout.addWidget(self._btn_build)

    # ── API pública ───────────────────────────────────────────────────────────

    def set_connected(self, connected: bool):
        """Habilita/deshabilita controles según estado de conexión."""
        self._btn_check.setEnabled(connected)
        if not connected:
            self._analysis_ok = False
            self._btn_get.setEnabled(False)
            self._btn_build.setEnabled(False)
            self._analysis_lbl.setText("Estado: sin verificar")
            self._analysis_lbl.setStyleSheet("color: #7f8c8d; font-weight: bold;")

    # ── Helpers internos ──────────────────────────────────────────────────────

    def _busy(self, is_busy: bool):
        connected = self._conn.is_connected
        self._btn_check.setEnabled(not is_busy and connected)
        self._btn_get.setEnabled(not is_busy and connected and self._analysis_ok)
        can_build = (
            not is_busy
            and connected
            and bool(self._reaction_rows)
            and bool(self._section_combo.currentText())
        )
        self._btn_build.setEnabled(can_build)

    def _log(self, msg: str):
        self.log_message.emit(msg)

    # ── Paso 1: Verificar análisis ────────────────────────────────────────────

    def _on_check_analysis(self):
        self._log("Verificando estado del análisis...")
        self._busy(True)
        self._worker = CheckAnalysisWorker(self._backend)
        self._worker.finished.connect(self._on_check_done)
        self._worker.start()

    def _on_check_done(self, result: dict):
        self._busy(False)
        if not result.get("success"):
            err = result.get("error", "desconocido")
            self._analysis_lbl.setText(f"✘ Error: {err}")
            self._analysis_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
            self._log(f"✘ Error al verificar análisis: {err}")
            return

        if result["locked"]:
            self._analysis_ok = True
            self._analysis_lbl.setText("✔ Análisis completado (modelo bloqueado)")
            self._analysis_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
            self._log("✔ Análisis verificado — el modelo está bloqueado.")
            self._btn_get.setEnabled(self._conn.is_connected)
        else:
            self._analysis_ok = False
            self._analysis_lbl.setText("⚠ Sin análisis — ejecute el análisis en SAP2000")
            self._analysis_lbl.setStyleSheet("color: #e67e22; font-weight: bold;")
            self._log(
                "⚠ El modelo NO está bloqueado. "
                "Ejecute el análisis en SAP2000 (Analyze → Run All) y vuelva a verificar."
            )

    # ── Paso 2: Obtener reacciones ────────────────────────────────────────────

    def _on_get_reactions(self):
        self._log("\n─── Obteniendo nodos, load cases y reacciones... ───")
        self._busy(True)
        self._worker = GetReactionsWorker(self._backend)
        self._worker.finished.connect(self._on_reactions_done)
        self._worker.start()

    def _on_reactions_done(self, result: dict):
        self._busy(False)
        if not result.get("success"):
            self._log(f"✘ Error: {result.get('error', 'desconocido')}")
            return

        self._joint_names  = result["joint_names"]
        self._case_names   = result["case_names"]
        self._reaction_rows = result["rows"]

        # Poblar lista de nodos
        jc = result["joint_count"]
        self._joints_box.setTitle(f"Nodos Restringidos ({jc})")
        self._joints_list.clear()
        for name in self._joint_names:
            self._joints_list.addItem(name)

        # Poblar lista de load cases
        cc = result["case_count"]
        self._cases_box.setTitle(f"Load Cases ({cc})")
        self._cases_list.clear()
        for name in self._case_names:
            self._cases_list.addItem(name)

        # Poblar secciones en el combo
        sections = result.get("section_names", [])
        prev = self._section_combo.currentText()
        self._section_combo.clear()
        self._section_combo.addItems(sections)
        if prev in sections:
            self._section_combo.setCurrentText(prev)

        # Poblar tabla de reacciones
        n = result["num_results"]
        self._react_table.setObjectName("react_table")
        self._react_table.parentWidget().setTitle(f"Reacciones ({n} filas)") \
            if self._react_table.parentWidget() else None
        # Actualizar título del groupbox directamente
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            w = item.widget() if item else None
            if isinstance(w, QSplitter):
                gb = w.widget(2)
                if isinstance(gb, QGroupBox):
                    gb.setTitle(f"Reacciones ({n} filas)")
                break
        self._populate_react_table(self._reaction_rows)

        skipped = result.get("skipped_joints", [])
        if skipped:
            self._log(f"⚠ Nodos sin resultados: {', '.join(skipped)}")

        self._log(
            f"✔ {jc} nodo(s), {cc} load case(s), {n} fila(s) de reacciones"
        )
        # Habilitar botón de construcción si hay secciones
        self._busy(False)

    def _populate_react_table(self, rows: list):
        self._react_table.setSortingEnabled(False)
        self._react_table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            def _str_item(val: str) -> QTableWidgetItem:
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                return item

            def _num_item(val: float) -> QTableWidgetItem:
                item = QTableWidgetItem(f"{val:.4f}")
                item.setData(Qt.UserRole, val)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                return item

            self._react_table.setItem(r, 0, _str_item(row["joint"]))
            self._react_table.setItem(r, 1, _str_item(row["load_case"]))
            self._react_table.setItem(r, 2, _str_item(row["step_type"]))
            self._react_table.setItem(r, 3, _num_item(row["F1"]))
            self._react_table.setItem(r, 4, _num_item(row["F2"]))
            self._react_table.setItem(r, 5, _num_item(row["F3"]))
            self._react_table.setItem(r, 6, _num_item(row["M1"]))
            self._react_table.setItem(r, 7, _num_item(row["M2"]))
            self._react_table.setItem(r, 8, _num_item(row["M3"]))

        self._react_table.setSortingEnabled(True)
        self._react_table.resizeColumnsToContents()

    # ── Paso 3: Construir modelo de fundación ─────────────────────────────────

    def _on_build_foundation(self):
        section = self._section_combo.currentText()
        if not section:
            self._log("⚠ Selecciona una sección de Frame antes de construir.")
            return
        if not self._reaction_rows:
            self._log("⚠ Primero obtén las reacciones (Paso 2).")
            return

        depth = self._depth_spin.value()

        msg = QMessageBox(self)
        msg.setWindowTitle("Confirmar construcción")
        msg.setIcon(QMessageBox.Warning)
        msg.setText(
            "Esta operación modificará permanentemente el modelo SAP2000.\n\n"
            f"  • Sección pila: {section}\n"
            f"  • Profundidad: {depth} [unidades del modelo]\n"
            f"  • Nodos a procesar: {len(self._joint_names)}\n"
            f"  • Load cases: {len(self._case_names)}\n\n"
            "Se eliminarán TODOS los frames y áreas de la estructura superior.\n"
            "¿Desea continuar?"
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec() != QMessageBox.Yes:
            return

        self._log(
            f"\n─── Construyendo modelo fundación — sección={section}, "
            f"profundidad={depth} ───"
        )
        self._busy(True)
        self._worker = BuildFoundationWorker(
            self._backend,
            self._joint_names,
            self._reaction_rows,
            section,
            depth,
        )
        self._worker.finished.connect(self._on_build_done)
        self._worker.start()

    def _on_build_done(self, result: dict):
        self._busy(False)
        if not result.get("success"):
            self._log(f"✘ Error al construir: {result.get('error', 'desconocido')}")
            return

        cf  = result["created_frames"]
        df  = result["deleted_frames"]
        da  = result["deleted_areas"]
        cp  = len(result["created_patterns"])
        af  = result["assigned_forces"]
        pats = ", ".join(result["created_patterns"][:5])
        if len(result["created_patterns"]) > 5:
            pats += "..."
        saved = result.get("saved_path", "")
        saved_line = f"\n   Guardado como: {saved}" if saved else ""
        self._log(
            f"✔ Modelo de fundación construido:\n"
            f"   Frames pila creados: {cf}\n"
            f"   Frames superiores eliminados: {df}\n"
            f"   Áreas eliminadas: {da}\n"
            f"   Load patterns creados: {cp} ({pats})\n"
            f"   Fuerzas asignadas: {af}{saved_line}"
        )


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

        self._tab_shells = ShellsTab(self._conn)
        self._tab_shells.log_message.connect(self._log_append)
        self._tabs.addTab(self._tab_shells, "Shells")

        self._tab_mod_fund = ModFundTab(self._conn)
        self._tab_mod_fund.log_message.connect(self._log_append)
        self._tabs.addTab(self._tab_mod_fund, "Mod FUND")

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
        self._tab_shells.set_connected(connected)
        self._tab_mod_fund.set_connected(connected)
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
