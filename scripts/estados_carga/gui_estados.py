"""
GUI — Estados de Carga + Cargas (Standalone)
=============================================
App independiente de SAP2000 con dos pestañas:

  1. Estados de Carga — asocia a cada estado normativo (D, L, Lr, ...) uno o más
     nombres de casos de carga reales del modelo.
  2. Cargas — grilla tipo Excel (copiar/pegar) con las cargas de UN nodo:
     Load Pat + Fx Fy Fz Mx My Mz. El Load Pat se valida contra los nombres de
     la pestaña 1 (se resalta en rojo si no coincide).

El proyecto (estados + cargas) se persiste en un único JSON.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QKeySequence, QBrush, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QFileDialog,
    QSizePolicy,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QDialog,
    QTextEdit,
)

from config_estados import STATE_DEFINITIONS, DEFAULT_SAVE_FILE
from backend_estados import (
    EstadosCargaModel, LoadsModel, FORCE_KEYS,
    save_project, load_project, parse_force,
    loads_by_name, state_resultants, combo_resultants,
    combo_breakdown, state_breakdown,
)
from combos_norma import COMBOS_BY_METHOD


CHIP_STYLE = (
    "QPushButton {"
    "  background:#eaf2fb; border:1px solid #b8d2ef; border-radius:9px;"
    "  padding:1px 8px; color:#1f4e79; font-size:11px;"
    "}"
    "QPushButton:hover { background:#fbe9e9; border-color:#e0a0a0; color:#a33; }"
)

INVALID_BRUSH = QBrush(QColor(255, 215, 215))
VALID_BRUSH = QBrush(QColor(255, 255, 255))


def _fmt_num(value: float) -> str:
    """Formatea un número quitando ceros decimales innecesarios."""
    f = float(value)
    if f == int(f):
        return str(int(f))
    return "%g" % f


def _fmt_res(value: float) -> str:
    """Formatea una resultante (redondea a 3 decimales, sin ceros sobrantes)."""
    return _fmt_num(round(float(value), 3))


# Descripción por símbolo (para la tabla de resumen).
_STATE_DESC = {s["key"]: s["description"] for s in STATE_DEFINITIONS}
_FORCE_HEADERS = ["Fx (tonf)", "Fy (tonf)", "Fz (tonf)",
                  "Mx (tonf·m)", "My (tonf·m)", "Mz (tonf·m)"]


# ══════════════════════════════════════════════════════════════════════════════
# Pestaña 1 — Estados de Carga
# ══════════════════════════════════════════════════════════════════════════════

class EstadosTab(QWidget):
    """Filas fijas por estado normativo; cada una acumula nombres (chips)."""

    def __init__(self, backend: EstadosCargaModel):
        super().__init__()
        self._backend = backend
        self._chip_layouts = {}   # key -> QHBoxLayout de chips
        self._inputs = {}         # key -> QLineEdit
        self._on_status = None     # callback(text, error)

        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)

        box = QGroupBox("Estados de Carga")
        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(6)
        for state in STATE_DEFINITIONS:
            box_layout.addLayout(self._build_row(state))
        box_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(box)
        root.addWidget(scroll)

    # ── Construcción de filas ────────────────────────────────────────────

    def _build_row(self, state: dict) -> QHBoxLayout:
        key = state["key"]
        row = QHBoxLayout()
        row.setSpacing(8)

        lbl = QLabel(state["label"])
        lbl.setFixedWidth(80)
        lbl.setToolTip(state["description"])
        row.addWidget(lbl)

        edit = QLineEdit()
        edit.setPlaceholderText("Nombre")
        edit.setFixedWidth(130)
        edit.setToolTip(state["description"])
        edit.returnPressed.connect(lambda k=key: self._on_add(k))
        self._inputs[key] = edit
        row.addWidget(edit)

        btn = QPushButton("Agregar")
        btn.setFixedWidth(80)
        btn.clicked.connect(lambda _=False, k=key: self._on_add(k))
        row.addWidget(btn)

        chips_host = QWidget()
        chips_layout = QHBoxLayout(chips_host)
        chips_layout.setContentsMargins(0, 0, 0, 0)
        chips_layout.setSpacing(4)
        chips_layout.addStretch()
        chips_host.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._chip_layouts[key] = chips_layout
        row.addWidget(chips_host, stretch=1)

        return row

    def _make_chip(self, key: str, name: str) -> QPushButton:
        chip = QPushButton(f"{name}  ✕")
        chip.setStyleSheet(CHIP_STYLE)
        chip.setCursor(Qt.PointingHandCursor)
        chip.setToolTip("Quitar")
        chip.clicked.connect(lambda _=False, k=key, n=name: self._on_remove(k, n))
        return chip

    def _refresh_row(self, key: str) -> None:
        layout = self._chip_layouts[key]
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        for name in self._backend.names(key):
            layout.addWidget(self._make_chip(key, name))
        layout.addStretch()

    def refresh_all(self) -> None:
        for key in self._backend.keys():
            self._refresh_row(key)

    # ── Acciones ─────────────────────────────────────────────────────────

    def _on_add(self, key: str) -> None:
        edit = self._inputs[key]
        name = edit.text().strip()
        if not name:
            self._status(f"'{key}': ingrese un nombre.", error=True)
            return
        if self._backend.add_name(key, name):
            edit.clear()
            self._refresh_row(key)
            self._status(f"Agregado '{name}' a {key}.")
        else:
            self._status(f"'{name}' ya existe en {key}.", error=True)

    def _on_remove(self, key: str, name: str) -> None:
        if self._backend.remove_name(key, name):
            self._refresh_row(key)
            self._status(f"Quitado '{name}' de {key}.")

    def _status(self, text: str, error: bool = False) -> None:
        if self._on_status:
            self._on_status(text, error)


# ══════════════════════════════════════════════════════════════════════════════
# Grilla tipo Excel (copiar / pegar / borrar)
# ══════════════════════════════════════════════════════════════════════════════

class ExcelTable(QTableWidget):
    """QTableWidget con copiar (Ctrl+C), pegar (Ctrl+V) y borrar (Supr)."""

    def __init__(self, columns: list):
        super().__init__(0, len(columns))
        self.setHorizontalHeaderLabels(columns)
        self.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self._on_changed = None  # callback tras pegar/limpiar

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self._copy()
        elif event.matches(QKeySequence.Paste):
            self._paste()
        elif event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self._clear_selection()
        else:
            super().keyPressEvent(event)

    def _copy(self) -> None:
        ranges = self.selectedRanges()
        if not ranges:
            return
        r = ranges[0]
        lines = []
        for row in range(r.topRow(), r.bottomRow() + 1):
            cells = []
            for col in range(r.leftColumn(), r.rightColumn() + 1):
                it = self.item(row, col)
                cells.append(it.text() if it else "")
            lines.append("\t".join(cells))
        QApplication.clipboard().setText("\n".join(lines))

    def _paste(self) -> None:
        text = QApplication.clipboard().text()
        if not text:
            return
        start_row = max(self.currentRow(), 0)
        start_col = max(self.currentColumn(), 0)
        lines = text.split("\n")
        if lines and lines[-1] == "":
            lines = lines[:-1]
        for i, line in enumerate(lines):
            line = line.rstrip("\r")
            cells = line.split("\t")
            target_row = start_row + i
            while target_row >= self.rowCount():
                self.add_empty_row()
            for j, val in enumerate(cells):
                target_col = start_col + j
                if target_col >= self.columnCount():
                    break
                self._set_cell(target_row, target_col, val.strip())
        if self._on_changed:
            self._on_changed()

    def _clear_selection(self) -> None:
        for it in self.selectedItems():
            it.setText("")
        if self._on_changed:
            self._on_changed()

    def _set_cell(self, row: int, col: int, text: str) -> None:
        it = self.item(row, col)
        if it is None:
            it = QTableWidgetItem()
            self.setItem(row, col, it)
        it.setText(text)

    def add_empty_row(self) -> int:
        row = self.rowCount()
        self.insertRow(row)
        for col in range(self.columnCount()):
            self.setItem(row, col, QTableWidgetItem(""))
        return row


# ══════════════════════════════════════════════════════════════════════════════
# Pestaña 2 — Cargas
# ══════════════════════════════════════════════════════════════════════════════

COLUMNS = ["Load Pat", "Fx (tonf)", "Fy (tonf)", "Fz (tonf)",
           "Mx (tonf·m)", "My (tonf·m)", "Mz (tonf·m)"]
INITIAL_ROWS = 8


class CargasTab(QWidget):
    """Grilla de cargas de un nodo, con validación de Load Pat contra estados."""

    def __init__(self, estados: EstadosCargaModel):
        super().__init__()
        self._estados = estados
        self._on_status = None

        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(8)

        info = QLabel(
            "Cargas de un nodo. Copie/pegue desde Excel (Ctrl+C / Ctrl+V). "
            "El Load Pat debe coincidir con un nombre de la pestaña «Estados de "
            "Carga» (se resalta en rojo si no)."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color:#555;")
        root.addWidget(info)

        self._table = ExcelTable(COLUMNS)
        self._table._on_changed = self.validate
        self._table.cellChanged.connect(self._on_cell_changed)
        hdr = self._table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.Interactive)
        self._table.setColumnWidth(0, 150)
        for c in range(1, len(COLUMNS)):
            hdr.setSectionResizeMode(c, QHeaderView.Stretch)
        for _ in range(INITIAL_ROWS):
            self._table.add_empty_row()
        root.addWidget(self._table, stretch=1)

        # ── Botonera ──────────────────────────────────────────────────────
        btns = QHBoxLayout()
        b_add = QPushButton("Agregar fila")
        b_add.clicked.connect(lambda: (self._table.add_empty_row(), None))
        btns.addWidget(b_add)

        b_del = QPushButton("Eliminar fila(s)")
        b_del.clicked.connect(self._delete_selected_rows)
        btns.addWidget(b_del)

        b_fill = QPushButton("Cargar desde Estados")
        b_fill.setToolTip("Genera una fila por cada nombre definido en «Estados de Carga».")
        b_fill.clicked.connect(self._fill_from_estados)
        btns.addWidget(b_fill)

        btns.addStretch()
        root.addLayout(btns)

    # ── Validación de Load Pat ───────────────────────────────────────────

    def _valid_names(self) -> set:
        names = set()
        for key in self._estados.keys():
            names.update(self._estados.names(key))
        return names

    def _on_cell_changed(self, row: int, col: int) -> None:
        if col == 0:
            self._validate_cell(row)

    def _validate_cell(self, row: int) -> None:
        it = self._table.item(row, 0)
        if it is None:
            return
        valid = self._valid_names()
        name = it.text().strip()
        # Sin estados definidos aún → no marcar nada.
        if name and valid and name not in valid:
            it.setBackground(INVALID_BRUSH)
            it.setToolTip("Load Pat no coincide con la pestaña «Estados de Carga».")
        else:
            it.setBackground(VALID_BRUSH)
            it.setToolTip("")

    def validate(self) -> None:
        """Revalida toda la columna Load Pat (llamar al cambiar de pestaña)."""
        for row in range(self._table.rowCount()):
            self._validate_cell(row)

    # ── Acciones ─────────────────────────────────────────────────────────

    def _delete_selected_rows(self) -> None:
        rows = sorted({idx.row() for idx in self._table.selectedIndexes()}, reverse=True)
        for r in rows:
            self._table.removeRow(r)
        if not rows:
            self._status("Seleccione al menos una fila para eliminar.", error=True)

    def _fill_from_estados(self) -> None:
        # Nombres en orden de definición, sin duplicados.
        names = []
        seen = set()
        for key in self._estados.keys():
            for n in self._estados.names(key):
                if n not in seen:
                    seen.add(n)
                    names.append(n)
        if not names:
            self._status("No hay nombres definidos en «Estados de Carga».", error=True)
            return
        if self._has_data():
            reply = QMessageBox.question(
                self, "Cargar desde Estados",
                "Esto reemplazará las filas actuales. ¿Continuar?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return
        rows = [{"load_pat": n} for n in names]
        self.set_rows(rows)
        self._status(f"Cargadas {len(names)} filas desde Estados de Carga.")

    # ── Interfaz con el modelo de datos ──────────────────────────────────

    def _has_data(self) -> bool:
        for r in range(self._table.rowCount()):
            it = self._table.item(r, 0)
            if it and it.text().strip():
                return True
        return False

    def get_rows(self) -> list:
        """Lee la grilla → lista de dicts (omite filas totalmente vacías)."""
        rows = []
        for r in range(self._table.rowCount()):
            it0 = self._table.item(r, 0)
            load_pat = it0.text().strip() if it0 else ""
            forces = {}
            any_force = False
            for j, key in enumerate(FORCE_KEYS, start=1):
                it = self._table.item(r, j)
                txt = it.text().strip() if it else ""
                forces[key] = parse_force(txt)
                if txt not in ("", "0"):
                    any_force = True
            if not load_pat and not any_force:
                continue
            rows.append({"load_pat": load_pat, **forces})
        return rows

    def set_rows(self, rows: list) -> None:
        """Reemplaza la grilla con las filas dadas (más filas vacías de margen)."""
        self._table.blockSignals(True)
        self._table.setRowCount(0)
        for r in rows:
            row = self._table.add_empty_row()
            self._table.item(row, 0).setText(str(r.get("load_pat", "")))
            for j, key in enumerate(FORCE_KEYS, start=1):
                self._table.item(row, j).setText(_fmt_num(r.get(key, 0.0)))
        for _ in range(max(0, INITIAL_ROWS - self._table.rowCount())):
            self._table.add_empty_row()
        self._table.blockSignals(False)
        self.validate()

    def _status(self, text: str, error: bool = False) -> None:
        if self._on_status:
            self._on_status(text, error)


# ══════════════════════════════════════════════════════════════════════════════
# Pestaña 3 — Resultados (resumen por estado + combinaciones)
# ══════════════════════════════════════════════════════════════════════════════

class NumericItem(QTableWidgetItem):
    """Celda que se ordena por su valor numérico (no por texto)."""

    def __init__(self, value: float, text: str):
        super().__init__(text)
        self._value = float(value)
        self.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def __lt__(self, other):
        if isinstance(other, NumericItem):
            return self._value < other._value
        return super().__lt__(other)


def _make_readonly_table(headers: list) -> QTableWidget:
    t = QTableWidget(0, len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.setSelectionBehavior(QAbstractItemView.SelectRows)
    t.setAlternatingRowColors(True)
    t.verticalHeader().setVisible(False)
    # Ordenamiento por click en encabezado (alterna mayor↔menor).
    t.setSortingEnabled(True)
    t.horizontalHeader().setSortIndicatorShown(True)
    t.horizontalHeader().setToolTip(
        "Click en un encabezado para ordenar (alterna mayor↔menor).")
    return t


def _cell(text: str) -> QTableWidgetItem:
    return QTableWidgetItem(text)


def _num_cell(value: float) -> NumericItem:
    """Celda numérica: muestra el valor formateado y ordena por su magnitud."""
    return NumericItem(value, _fmt_res(value))


class ResultadosTab(QWidget):
    """Resumen de cargas por estado y resultantes de las combinaciones fijas."""

    STATE_COLS = ["Estado", "Descripción", "#Nombres"] + _FORCE_HEADERS
    COMBO_COLS = ["Método", "Combinación"] + _FORCE_HEADERS

    def __init__(self, estados: EstadosCargaModel, get_rows):
        super().__init__()
        self._estados = estados
        self._get_rows = get_rows   # callable -> lista de filas de carga

        # Mapa nombre→items y estado del último cálculo (para los diálogos).
        self._combo_items = {name: items for _, name, items in COMBOS_BY_METHOD}
        self._sr = {}
        self._by_name = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(8)

        top = QHBoxLayout()
        btn = QPushButton("Recalcular")
        btn.setFixedWidth(110)
        btn.clicked.connect(self.recompute)
        top.addWidget(btn)
        self._info = QLabel("")
        self._info.setStyleSheet("color:#555;")
        top.addWidget(self._info)
        top.addStretch()
        root.addLayout(top)

        _DBL = "Doble-click en una fila para ver el desglose del cálculo."

        # ── Resumen por estado ────────────────────────────────────────────
        grp_states = QGroupBox("Resumen por Estado (resultante sumada)")
        gl = QVBoxLayout(grp_states)
        self._t_states = _make_readonly_table(self.STATE_COLS)
        self._t_states.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._t_states.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._t_states.setToolTip(_DBL)
        self._t_states.cellDoubleClicked.connect(self._on_state_dblclick)
        gl.addWidget(self._t_states)
        root.addWidget(grp_states, stretch=1)

        # ── Combinaciones ─────────────────────────────────────────────────
        grp_combos = QGroupBox("Combinaciones (fijas) — resultante en el nodo")
        cl = QVBoxLayout(grp_combos)
        self._t_combos = _make_readonly_table(self.COMBO_COLS)
        hdr = self._t_combos.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.Interactive)
        self._t_combos.setColumnWidth(1, 320)
        self._t_combos.setToolTip(_DBL)
        self._t_combos.cellDoubleClicked.connect(self._on_combo_dblclick)
        cl.addWidget(self._t_combos)
        root.addWidget(grp_combos, stretch=2)

    # ── Cálculo y pintado ────────────────────────────────────────────────

    def recompute(self) -> None:
        rows = self._get_rows()
        by_name = loads_by_name(rows)
        sr = state_resultants(self._estados, by_name)
        # Guardar para los diálogos de auditoría (doble-click).
        self._sr = sr
        self._by_name = by_name

        # Nombres huérfanos (con carga pero sin estado asignado).
        assigned = set()
        for key in self._estados.keys():
            assigned.update(self._estados.names(key))
        orphans = sorted(n for n in by_name if n not in assigned)

        # Nombres asignados sin carga.
        missing = []
        for key in self._estados.keys():
            missing.extend(sr[key]["missing"])

        self._fill_states(sr)
        crs = combo_resultants(COMBOS_BY_METHOD, sr)
        self._fill_combos(crs)

        parts = [f"{len(crs)} combinaciones"]
        if orphans:
            parts.append(f"⚠ {len(orphans)} carga(s) sin estado: {', '.join(orphans)}")
        if missing:
            parts.append(f"⚠ {len(missing)} nombre(s) sin carga: {', '.join(missing)}")
        self._info.setText("   |   ".join(parts))
        self._info.setStyleSheet(
            "color:#c0392b;" if (orphans or missing) else "color:#27ae60;")

    def _fill_states(self, sr: dict) -> None:
        # Solo estados con al menos un nombre asignado.
        keys = [k for k in self._estados.keys() if sr[k]["n_names"] > 0]
        t = self._t_states
        t.setSortingEnabled(False)
        t.setRowCount(len(keys))
        for i, key in enumerate(keys):
            vec = sr[key]["vector"]
            t.setItem(i, 0, _cell(key))
            t.setItem(i, 1, _cell(_STATE_DESC.get(key, "")))
            t.setItem(i, 2, _num_cell(sr[key]["n_names"]))
            for j, fk in enumerate(FORCE_KEYS, start=3):
                t.setItem(i, j, _num_cell(vec[fk]))
        t.setSortingEnabled(True)

    def _fill_combos(self, crs: list) -> None:
        t = self._t_combos
        t.setSortingEnabled(False)
        t.setRowCount(len(crs))
        for i, c in enumerate(crs):
            vec = c["vector"]
            t.setItem(i, 0, _cell(c.get("method", "")))
            t.setItem(i, 1, _cell(c["name"]))
            for j, fk in enumerate(FORCE_KEYS, start=2):
                t.setItem(i, j, _num_cell(vec[fk]))
        t.setSortingEnabled(True)

    # ── Auditoría (doble-click) ──────────────────────────────────────────

    def _on_combo_dblclick(self, row: int, _col: int) -> None:
        item = self._t_combos.item(row, 1)
        if item is None:
            return
        name = item.text()
        items = self._combo_items.get(name)
        if items is None:
            return
        method_item = self._t_combos.item(row, 0)
        method = method_item.text() if method_item else ""
        dlg = AuditDialog.for_combo(
            self, name, method, items, self._sr, self._estados, self._by_name)
        dlg.exec()

    def _on_state_dblclick(self, row: int, _col: int) -> None:
        item = self._t_states.item(row, 0)
        if item is None:
            return
        key = item.text()
        dlg = AuditDialog.for_state(self, key, self._estados, self._by_name)
        dlg.exec()


# ══════════════════════════════════════════════════════════════════════════════
# Diálogo de auditoría (doble-click en un resultado)
# ══════════════════════════════════════════════════════════════════════════════

def _signed_term(factor: float, sym: str) -> str:
    sign = "+" if factor >= 0 else "−"
    return f"{sign} {_fmt_num(abs(factor))}·{sym}"


def _formula(items) -> str:
    s = " ".join(_signed_term(f, sym) for sym, f in items)
    return s[2:] if s.startswith("+ ") else s   # quitar "+ " inicial


def _nonzero_str(vec: dict) -> str:
    """Resume un vector mostrando solo componentes no nulas: 'Fz=-15, Mz=1'."""
    parts = [f"{k.capitalize()}={_fmt_res(vec[k])}"
             for k in FORCE_KEYS if abs(vec[k]) > 1e-12]
    return ", ".join(parts) if parts else "0"


def _detail_table(headers: list) -> QTableWidget:
    t = QTableWidget(0, len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.setSelectionMode(QAbstractItemView.NoSelection)
    t.verticalHeader().setVisible(False)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
    t.setColumnWidth(0, 170)
    return t


def _bold(item: QTableWidgetItem) -> QTableWidgetItem:
    f = item.font()
    f.setBold(True)
    item.setFont(f)
    return item


class AuditDialog(QDialog):
    """Muestra el desglose paso a paso de un resultado (combo o estado)."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Auditoría de cálculo")
        self.setModal(True)
        self.resize(720, 560)
        self._root = QVBoxLayout(self)
        self._root.setSpacing(8)

    # ── Construcción común ───────────────────────────────────────────────

    def _header(self, text: str, bold: bool = False) -> None:
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        if bold:
            lbl.setStyleSheet("font-weight:bold; font-size:13px;")
        self._root.addWidget(lbl)

    def _close_button(self) -> None:
        row = QHBoxLayout()
        row.addStretch()
        b = QPushButton("Cerrar")
        b.clicked.connect(self.accept)
        row.addWidget(b)
        self._root.addLayout(row)

    # ── Fábricas ─────────────────────────────────────────────────────────

    @classmethod
    def for_combo(cls, parent, name, method, items, sr, estados, by_name):
        dlg = cls(parent)
        dlg._build_combo(name, method, items, sr, estados, by_name)
        return dlg

    @classmethod
    def for_state(cls, parent, key, estados, by_name):
        dlg = cls(parent)
        dlg._build_state(key, estados, by_name)
        return dlg

    # ── Combo ────────────────────────────────────────────────────────────

    def _build_combo(self, name, method, items, sr, estados, by_name):
        self._header(f"Combinación:  {name}", bold=True)
        self._header(f"Método:  {method}")
        self._header(f"Fórmula:  {_formula(items)}")

        terms, total = combo_breakdown(items, sr)

        grp = QGroupBox("Aporte por estado  (factor × resultante del estado)")
        gl = QVBoxLayout(grp)
        t = _detail_table(["Término"] + _FORCE_HEADERS)
        t.setRowCount(len(terms) + 1)
        for i, term in enumerate(terms):
            t.setItem(i, 0, _cell(f"{_fmt_num(term['factor'])} · {term['symbol']}"))
            for j, fk in enumerate(FORCE_KEYS, start=1):
                t.setItem(i, j, _num_cell(term["contrib"][fk]))
        last = len(terms)
        t.setItem(last, 0, _bold(_cell("TOTAL")))
        for j, fk in enumerate(FORCE_KEYS, start=1):
            t.setItem(last, j, _bold(_num_cell(total[fk])))
        gl.addWidget(t)
        self._root.addWidget(grp, stretch=1)

        # Composición de los estados involucrados (símbolos del combo, sin duplicar).
        grp2 = QGroupBox("Composición de estados  (cargas del nodo)")
        g2 = QVBoxLayout(grp2)
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setFont(QFont("Consolas", 10))
        seen = set()
        lines = []
        for sym, _factor in items:
            if sym in seen:
                continue
            seen.add(sym)
            lines.append(self._state_line(sym, estados, by_name))
        txt.setPlainText("\n".join(lines))
        g2.addWidget(txt)
        self._root.addWidget(grp2, stretch=1)

        self._close_button()

    @staticmethod
    def _state_line(sym, estados, by_name) -> str:
        rows, total = state_breakdown(estados, by_name, sym)
        if not rows:
            return f"{sym} = (sin cargas asignadas)  →  0"
        parts = []
        for r in rows:
            if r["missing"]:
                parts.append(f"{r['name']}(sin carga)")
            else:
                parts.append(f"{r['name']}({_nonzero_str(r['vector'])})")
        return f"{sym} = " + "  +  ".join(parts) + f"   →   {_nonzero_str(total)}"

    # ── Estado ───────────────────────────────────────────────────────────

    def _build_state(self, key, estados, by_name):
        rows, total = state_breakdown(estados, by_name, key)
        self._header(f"Estado:  {key} — {_STATE_DESC.get(key, '')}", bold=True)
        self._header(f"Resultante:  {_nonzero_str(total)}")

        grp = QGroupBox("Composición  (cargas nombradas que suman el estado)")
        gl = QVBoxLayout(grp)
        if not rows:
            gl.addWidget(QLabel("(sin nombres asignados)"))
        else:
            t = _detail_table(["Carga (nombre)"] + _FORCE_HEADERS)
            t.setRowCount(len(rows) + 1)
            for i, r in enumerate(rows):
                if r["missing"]:
                    item = _cell(f"{r['name']}  (sin carga)")
                    item.setForeground(QBrush(QColor(150, 150, 150)))
                    t.setItem(i, 0, item)
                    for j in range(1, len(_FORCE_HEADERS) + 1):
                        t.setItem(i, j, _num_cell(0.0))
                else:
                    t.setItem(i, 0, _cell(r["name"]))
                    for j, fk in enumerate(FORCE_KEYS, start=1):
                        t.setItem(i, j, _num_cell(r["vector"][fk]))
            last = len(rows)
            t.setItem(last, 0, _bold(_cell("TOTAL")))
            for j, fk in enumerate(FORCE_KEYS, start=1):
                t.setItem(last, j, _bold(_num_cell(total[fk])))
            gl.addWidget(t)
        self._root.addWidget(grp, stretch=1)

        self._close_button()


# ══════════════════════════════════════════════════════════════════════════════
# Ventana principal — pestañas + barra inferior compartida
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Estados de Carga")
        self.setMinimumWidth(720)
        self.setMinimumHeight(600)

        self._estados = EstadosCargaModel()
        self._loads = LoadsModel()

        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        self._tabs = QTabWidget()
        self._estados_tab = EstadosTab(self._estados)
        self._cargas_tab = CargasTab(self._estados)
        self._resultados_tab = ResultadosTab(self._estados, self._cargas_tab.get_rows)
        self._estados_tab._on_status = self._set_status
        self._cargas_tab._on_status = self._set_status
        self._tabs.addTab(self._estados_tab, "Estados de Carga")
        self._tabs.addTab(self._cargas_tab, "Cargas")
        self._tabs.addTab(self._resultados_tab, "Resultados")
        self._tabs.currentChanged.connect(self._on_tab_changed)
        root.addWidget(self._tabs, stretch=1)

        # ── Barra inferior compartida ─────────────────────────────────────
        bottom = QHBoxLayout()
        btn_save = QPushButton("Guardar")
        btn_save.setFixedHeight(32)
        btn_save.clicked.connect(self._on_save)
        bottom.addWidget(btn_save)

        btn_load = QPushButton("Cargar")
        btn_load.setFixedHeight(32)
        btn_load.clicked.connect(self._on_load)
        bottom.addWidget(btn_load)

        bottom.addStretch()
        self._status = QLabel("")
        self._status.setStyleSheet("color:#555;")
        bottom.addWidget(self._status)
        root.addLayout(bottom)

    # ── Eventos ──────────────────────────────────────────────────────────

    def _on_tab_changed(self, index: int) -> None:
        widget = self._tabs.widget(index)
        # Revalidar Load Pat al entrar a la pestaña Cargas (estados pudo cambiar).
        if widget is self._cargas_tab:
            self._cargas_tab.validate()
        # Recalcular resultados al entrar (estados o cargas pudieron cambiar).
        elif widget is self._resultados_tab:
            self._resultados_tab.recompute()

    def _on_save(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar proyecto", DEFAULT_SAVE_FILE, "JSON (*.json)"
        )
        if not path:
            return
        try:
            self._loads.set_rows(self._cargas_tab.get_rows())
            save_project(path, self._estados, self._loads)
            self._set_status(f"Guardado en {path}")
        except Exception as exc:
            self._set_status(f"Error al guardar: {exc}", error=True)

    def _on_load(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Cargar proyecto", "", "JSON (*.json)"
        )
        if not path:
            return
        try:
            load_project(path, self._estados, self._loads)
            self._estados_tab.refresh_all()
            self._cargas_tab.set_rows(self._loads.to_list())
            self._set_status(f"Cargado desde {path}")
        except Exception as exc:
            self._set_status(f"Error al cargar: {exc}", error=True)

    def _set_status(self, text: str, error: bool = False) -> None:
        color = "#c0392b" if error else "#27ae60"
        self._status.setStyleSheet(f"color:{color};")
        self._status.setText(text)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
