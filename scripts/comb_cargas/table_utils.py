"""Utilidades de tabla compartidas entre los tabs de Load Patterns y Combinaciones."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem


def color_cell(item) -> None:
    """Fondo verde si valor ≠ 0, rojo si inválido, blanco si vacía o cero."""
    text = item.text().strip()
    if not text:
        item.setBackground(QColor("#ffffff"))
        return
    try:
        val = float(text)
        item.setBackground(QColor("#d4edda") if val != 0 else QColor("#ffffff"))
    except ValueError:
        item.setBackground(QColor("#f8d7da"))


def validate_name_table(table: QTableWidget, name_col: int = 0) -> bool:
    """Valida nombres en name_col: no vacíos ni duplicados. Resalta inválidos en rojo."""
    seen: dict = {}
    valid = True
    for r in range(table.rowCount()):
        it = table.item(r, name_col)
        name = it.text().strip() if it else ""
        if not name:
            if it:
                it.setBackground(QColor("#f8d7da"))
            valid = False
        elif name in seen:
            it.setBackground(QColor("#f8d7da"))
            prev = table.item(seen[name], name_col)
            if prev:
                prev.setBackground(QColor("#f8d7da"))
            valid = False
        else:
            seen[name] = r
            if it:
                it.setBackground(QColor("#ffffff"))
    return valid


def copy_selection(table: QTableWidget, log_fn=None) -> None:
    """Copia las celdas seleccionadas al portapapeles como texto separado por tabs."""
    indexes = table.selectedIndexes()
    if not indexes:
        return
    cells: dict = {}
    for idx in indexes:
        cells.setdefault(idx.row(), {})[idx.column()] = idx
    all_rows = sorted(cells.keys())
    all_cols = sorted({c for rd in cells.values() for c in rd})
    lines = []
    for r in all_rows:
        parts = []
        for c in all_cols:
            if c in cells.get(r, {}):
                item = table.item(r, c)
                if item is not None:
                    parts.append(item.text())
                else:
                    w = table.cellWidget(r, c)
                    parts.append(w.currentText() if w else "")
            else:
                parts.append("")
        lines.append("\t".join(parts))
    QApplication.clipboard().setText("\n".join(lines))
    if log_fn:
        log_fn(f"  ✔ Copiadas {len(indexes)} celdas al portapapeles")


def paste_selection(table: QTableWidget, is_numeric_col_fn, set_dirty_fn, log_fn=None) -> None:
    """
    Pega texto del portapapeles en la tabla desde la celda seleccionada.
    is_numeric_col_fn(col) → bool: indica qué columnas deben colorearse numéricamente.
    set_dirty_fn(): se llama si se pegó algo.
    La columna 1 (tipo) se salta automáticamente.
    """
    text = QApplication.clipboard().text()
    if not text.strip():
        return
    indexes = table.selectedIndexes()
    if not indexes:
        return
    start_row = min(idx.row() for idx in indexes)
    start_col = min(idx.column() for idx in indexes)
    if start_col == 1:
        start_col = 2

    lines = text.splitlines()
    pasted = 0
    table.blockSignals(True)
    for ri, line in enumerate(lines):
        target_row = start_row + ri
        if target_row >= table.rowCount():
            break
        values = line.split("\t")
        col_offset = 0
        for ci, val in enumerate(values):
            target_col = start_col + ci + col_offset
            while target_col == 1:
                col_offset += 1
                target_col += 1
            if target_col >= table.columnCount():
                break
            val = val.strip()
            item = table.item(target_row, target_col)
            if item is None:
                item = QTableWidgetItem()
                if target_col != 0:
                    item.setTextAlignment(Qt.AlignCenter)
                table.setItem(target_row, target_col, item)
            item.setText(val)
            if is_numeric_col_fn(target_col):
                color_cell(item)
            pasted += 1
    table.blockSignals(False)
    if pasted > 0:
        set_dirty_fn()
        if log_fn:
            log_fn(f"  ✔ Pegados {pasted} valores desde el portapapeles")
