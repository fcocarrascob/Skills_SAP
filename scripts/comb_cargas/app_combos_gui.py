"""Shim de compatibilidad — el módulo fue dividido en archivos separados. Usa app.py."""
import sys
from app import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
