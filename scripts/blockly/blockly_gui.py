"""
SAP2000 Visual Scripter — Blockly GUI Application
===================================================
App principal PySide6 embebido con Blockly.

Características:
  - Editor visual tipo Blockly
  - Preview de Python generado
  - Ejecución contra SAP2000
  - Console con output
  - Export/Import de scripts

Uso:
    python blockly_gui.py
"""

import sys
import json
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QPushButton, QLabel, QMessageBox, QFileDialog,
    QSplitter, QDockWidget, QComboBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QObject, Signal, Slot, QTimer, QUrl
from PySide6.QtGui import QFont, QIcon

try:
    from blockly_transpiler import BlocklyTranspiler
    from blockly_executor import BlocklyScriptExecutor
except ImportError:
    from .blockly_transpiler import BlocklyTranspiler
    from .blockly_executor import BlocklyScriptExecutor


class WebChannelBridge(QObject):
    """Bridge entre JavaScript (Blockly) y Python (PySide6)"""
    
    workspace_changed = Signal(str)  # Emitido cuando workspace cambia
    
    @Slot(str)
    def on_workspace_update(self, xml_str: str):
        """JavaScript llama esto cuando workspace cambia"""
        self.workspace_changed.emit(xml_str)


class BlocklyEditor(QWebEngineView):
    """QWebEngineView embebido con Blockly"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bridge = WebChannelBridge()
        self.load_blockly_html()
    
    def load_blockly_html(self):
        """Cargar HTML + Blockly CDN"""
        # Usar HTML inline directamente (más confiable que desde archivo)
        self.setHtml(self._get_minimal_html())
    
    def _get_minimal_html(self) -> str:
        """HTML completo para Blockly + CDN con carga dinámica"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>SAP2000 Blockly</title>
            <link rel="stylesheet" href="https://unpkg.com/blockly/blockly_compressed.css">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: Arial, sans-serif; height: 100vh; background: #fff; }
                #blockly-workspace { width: 100%; height: 100%; display: none; }
                #loading { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                          text-align: center; }
                #loading.hidden { display: none; }
            </style>
        </head>
        <body>
            <div id="loading">
                <p>Cargando Blockly desde CDN...</p>
            </div>
            <div id="blockly-workspace"></div>
            
            <script src="https://unpkg.com/blockly/blockly_compressed.js"></script>
            <script src="https://unpkg.com/blockly/blocks_compressed.js"></script>
            <script src="https://unpkg.com/blockly/en.js"></script>
            <script src="https://unpkg.com/blockly/python_compressed.js"></script>
            
            <script>
                let workspace = null;
                let blocklyReady = false;
                
                // Esperar a que DOM esté listo Y Blockly cargue
                function initBlockly() {
                    console.log('Verificando si Blockly está listo...');
                    
                    if (typeof Blockly === 'undefined') {
                        console.log('Blockly aún no cargó, reintentando en 100ms...');
                        setTimeout(initBlockly, 100);
                        return;
                    }
                    
                    console.log('✅ Blockly cargado correctamente');
                    
                    // Crear bloques básicos
                    createBasicBlocks();
                    
                    // Toolbox XML
                    const toolboxXml = `
                        <xml id="toolbox" style="display: none">
                            <category name="Inicializar (1)" colour="0">
                                <block type="sap_File_NewBlank"></block>
                            </category>
                            <category name="Materiales (2)" colour="45">
                                <block type="sap_PropMaterial_SetMaterial"></block>
                            </category>
                            <category name="Secciones (3)" colour="90">
                                <block type="sap_PropFrame_SetRectangle"></block>
                            </category>
                        </xml>
                    `;
                    
                    // Inyectar Blockly
                    workspace = Blockly.inject('blockly-workspace', {
                        toolbox: toolboxXml,
                        grid: {
                            spacing: 20,
                            length: 3,
                            colour: '#ccc',
                            snap: true
                        },
                        trashcan: true,
                        maxTrashcanContents: 64,
                        move: {
                            scrollbars: { horizontal: true, vertical: true },
                            drag: true,
                            wheel: true
                        },
                        zoom: {
                            controls: true,
                            wheel: true,
                            startScale: 1.0,
                            maxScale: 3,
                            minScale: 0.3
                        }
                    });
                    
                    // Listeners
                    workspace.addChangeListener(onWorkspaceChange);
                    
                    // Ocultar loading
                    document.getElementById('loading').classList.add('hidden');
                    document.getElementById('blockly-workspace').style.display = 'block';
                    
                    console.log('✅ Editor listo para usar');
                    blocklyReady = true;
                }
                
                function createBasicBlocks() {
                    // File.NewBlank
                    Blockly.Blocks['sap_File_NewBlank'] = {
                        init: function() {
                            this.setColour(0);
                            this.appendDummyInput()
                                .appendField('📁 File.NewBlank()');
                            this.setPreviousStatement(true);
                            this.setNextStatement(true);
                            this.setTooltip('Inicializar nuevo modelo');
                        }
                    };
                    Blockly.Python['sap_File_NewBlank'] = function(block) {
                        return 'ret = SapModel.File.NewBlank()\\nassert ret == 0\\n';
                    };
                    
                    // PropMaterial.SetMaterial
                    Blockly.Blocks['sap_PropMaterial_SetMaterial'] = {
                        init: function() {
                            this.setColour(45);
                            this.appendValueInput('NAME')
                                .setCheck('String')
                                .appendField('Material Name:');
                            this.appendValueInput('TYPE')
                                .setCheck('Number')
                                .appendField('Type:');
                            this.setPreviousStatement(true);
                            this.setNextStatement(true);
                            this.setTooltip('Definir material');
                        }
                    };
                    Blockly.Python['sap_PropMaterial_SetMaterial'] = function(block) {
                        var name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_MEMBER) || '""';
                        var type = Blockly.Python.valueToCode(block, 'TYPE', Blockly.Python.ORDER_MEMBER) || '2';
                        return 'ret = SapModel.PropMaterial.SetMaterial(' + name + ', ' + type + ')\\nassert ret == 0\\n';
                    };
                    
                    // PropFrame.SetRectangle
                    Blockly.Blocks['sap_PropFrame_SetRectangle'] = {
                        init: function() {
                            this.setColour(90);
                            this.appendValueInput('NAME')
                                .setCheck('String')
                                .appendField('Sección:');
                            this.appendValueInput('T3')
                                .setCheck('Number')
                                .appendField('Alto (m):');
                            this.appendValueInput('T2')
                                .setCheck('Number')
                                .appendField('Ancho (m):');
                            this.setPreviousStatement(true);
                            this.setNextStatement(true);
                            this.setTooltip('Sección rectangular');
                        }
                    };
                    Blockly.Python['sap_PropFrame_SetRectangle'] = function(block) {
                        var name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_MEMBER) || '""';
                        var t3 = Blockly.Python.valueToCode(block, 'T3', Blockly.Python.ORDER_MEMBER) || '0.3';
                        var t2 = Blockly.Python.valueToCode(block, 'T2', Blockly.Python.ORDER_MEMBER) || '0.3';
                        return 'ret = SapModel.PropFrame.SetRectangle(' + name + ', "CONC", ' + t3 + ', ' + t2 + ')\\nassert ret == 0\\n';
                    };
                }
                
                function onWorkspaceChange(event) {
                    if (!workspace || !blocklyReady) return;
                    const xml = Blockly.Xml.workspaceToDom(workspace);
                    const xmlStr = new XMLSerializer().serializeToString(xml);
                    window.blocklyXml = xmlStr;
                }
                
                // API pública para Python
                window.pyQtGetWorkspaceXml = function() {
                    return window.blocklyXml || '<xml></xml>';
                };
                
                window.pyQtGeneratePython = function() {
                    if (!workspace || !blocklyReady) return '';
                    try {
                        return Blockly.Python.workspaceToCode(workspace) || '';
                    } catch(e) {
                        console.error('Error generando Python:', e);
                        return '';
                    }
                };
                
                window.pyQtClearWorkspace = function() {
                    if (workspace && blocklyReady) workspace.clear();
                };
                
                // Iniciar cuando DOM esté listo
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', initBlockly);
                } else {
                    initBlockly();
                }
            </script>
        </body>
        </html>
        """
    
    def get_workspace_xml(self) -> Optional[str]:
        """Obtener XML del workspace via JavaScript"""
        result = [None]
        
        def on_result(xml):
            result[0] = xml
        
        try:
            self.page().runJavaScript(
                """
                (function() {
                    if (typeof window.pyQtGetWorkspaceXml === 'function') {
                        return window.pyQtGetWorkspaceXml();
                    }
                    return '<xml></xml>';
                })()
                """,
                on_result
            )
        except Exception:
            pass
        
        return result[0] or '<xml></xml>'
    
    def generate_python(self) -> str:
        """Generar Python del workspace"""
        result = [""]
        
        def on_result(code):
            result[0] = code or ""
        
        try:
            self.page().runJavaScript(
                """
                (function() {
                    if (typeof window.pyQtGeneratePython === 'function') {
                        return window.pyQtGeneratePython();
                    }
                    return '';
                })()
                """,
                on_result
            )
        except Exception:
            pass
        
        return result[0]
    
    def clear_workspace(self):
        """Limpiar canvas"""
        try:
            self.page().runJavaScript(
                """
                if (typeof window.pyQtClearWorkspace === 'function') {
                    window.pyQtClearWorkspace();
                }
                """
            )
        except Exception:
            pass


class BlocklyScripterApp(QMainWindow):
    """Aplicación principal"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 Visual Scripter — Blockly")
        self.setGeometry(100, 100, 1920, 1080)
        
        self.transpiler = BlocklyTranspiler()
        self.executor = BlocklyScriptExecutor()
        self.current_xml = None
        
        # Timer para actualizar preview (ya que WebChannel es async)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_python_preview)
        # Iniciar después de 1 segundo (dar tiempo a que JavaScript cargue)
        QTimer.singleShot(1000, lambda: self.update_timer.start(300))
        
        self._setup_ui()
        self._connect_sap2000()
    
    def _setup_ui(self):
        """Construir interfaz"""
        central = QWidget()
        layout = QHBoxLayout(central)
        
        # ─────────────────────────────────────────────────────────────
        # EDITOR (izquierda, 70%)
        # ─────────────────────────────────────────────────────────────
        self.editor = BlocklyEditor()
        # No conectar bridge — usamos timer para actualizar preview
        layout.addWidget(self.editor, 70)
        
        # ─────────────────────────────────────────────────────────────
        # PANEL DERECHA (30%)
        # ─────────────────────────────────────────────────────────────
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # --- Python Code Preview ---
        right_layout.addWidget(QLabel("📝 Python Preview"))
        self.code_preview = QPlainTextEdit()
        self.code_preview.setReadOnly(True)
        self.code_preview.setFont(QFont("Courier", 9))
        self.code_preview.setMaximumHeight(300)
        # Placeholder inicial
        self.code_preview.setPlainText("# 👈 Arrastra bloques para generar código Python")
        right_layout.addWidget(self.code_preview, 25)
        
        # --- Console Output ---
        right_layout.addWidget(QLabel("🖥️ Console"))
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Courier", 9))
        right_layout.addWidget(self.console, 40)
        
        # --- Status ---
        self.status_label = QLabel("⚫ Desconectado")
        self.status_label.setMaximumHeight(30)
        right_layout.addWidget(self.status_label)
        
        # --- Buttons ---
        buttons_layout = QVBoxLayout()
        
        self.btn_run = QPushButton("▶️ Ejecutar")
        self.btn_run.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 8px; font-weight: bold;"
        )
        self.btn_run.clicked.connect(self._on_run_script)
        buttons_layout.addWidget(self.btn_run)
        
        self.btn_export = QPushButton("💾 Exportar Python")
        self.btn_export.clicked.connect(self._on_export_python)
        buttons_layout.addWidget(self.btn_export)
        
        self.btn_save = QPushButton("💾 Guardar Proyecto")
        self.btn_save.clicked.connect(self._on_save_project)
        buttons_layout.addWidget(self.btn_save)
        
        self.btn_clear = QPushButton("🗑️ Limpiar")
        self.btn_clear.clicked.connect(self._on_clear_workspace)
        buttons_layout.addWidget(self.btn_clear)
        
        right_layout.addLayout(buttons_layout)
        layout.addWidget(right_widget, 30)
        
        self.setCentralWidget(central)
        self._setup_menu_bar()
    
    def _setup_menu_bar(self):
        """Setup menu bar"""
        menu = self.menuBar()
        
        file_menu = menu.addMenu("File")
        file_menu.addAction("New", self._on_new_project)
        file_menu.addAction("Open...", self._on_open_project)
        file_menu.addAction("Save", self._on_save_project)
        file_menu.addSeparator()
        file_menu.addAction("Export Python...", self._on_export_python)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        edit_menu = menu.addMenu("Edit")
        edit_menu.addAction("Clear All", self._on_clear_workspace)
        
        help_menu = menu.addMenu("Help")
        help_menu.addAction("About", self._on_about)
    
    def _connect_sap2000(self):
        """Conectar a SAP2000"""
        result = self.executor.connect(attach_to_existing=True)
        
        if result["connected"]:
            self.status_label.setText(
                f"🟢 Conectado a SAP2000 v{result['version']}"
            )
            self.status_label.setStyleSheet("color: green;")
            self.console.appendPlainText("✅ Conectado a SAP2000")
            self.console.appendPlainText("Listo para ejecutar scripts\n")
        else:
            self.status_label.setText(f"🔴 Abre SAP2000 para ejecutar scripts")
            self.status_label.setStyleSheet("color: #ff9800;")
            self.console.appendPlainText("⚠️ SAP2000 no está abierto")
            self.console.appendPlainText("Puedes crear scripts sin SAP2000, pero no ejecutarlos\n")
        
        # Mensaje de bienvenida
        self.console.appendPlainText("👈 Arrastra bloques del toolbox izquierdo")
        self.console.appendPlainText("📝 El Python preview se actualiza automáticamente")
        self.console.appendPlainText("▶️ Presiona 'Ejecutar' para correr el script\n")
    
    @Slot(str)
    def _on_workspace_changed(self, xml_str: str):
        """Workspace cambió → actualizar preview"""
        self.current_xml = xml_str
        
        try:
            python_code = self.transpiler.xml_to_python(xml_str)
            self.code_preview.setPlainText(python_code)
        except ValueError as e:
            self.code_preview.setPlainText(f"Error: {e}")
        except Exception as e:
            self.code_preview.setPlainText(f"Error inesperado: {e}")
    
    def _update_python_preview(self):
        """Timer callback: actualizar preview cada 500ms"""
        # Obtener XML actual del editor
        try:
            xml = self.editor.get_workspace_xml()
            
            if xml:
                # Siempre actualizar si hay XML (incluso si es igual para debug)
                self.current_xml = xml
                
                # Mostrar XML en console para debug
                if '<block' in xml:
                    self.console.appendPlainText(f"📊 XML actualizado: {len(xml)} bytes")
                
                # Transpilar
                python_code = self.transpiler.xml_to_python(xml)
                self.code_preview.setPlainText(python_code)
                
                # Si no hay bloques, mostrar mensaje
                if '<block' not in xml:
                    self.code_preview.setPlainText("# Arrastra bloques del toolbox izquierdo para comenzar")
        except Exception as e:
            # No actualizar preview si hay error (permite que otros intentos funcionen)
            pass
    
    @Slot()
    def _on_run_script(self):
        """Ejecutar script"""
        if not self.current_xml:
            QMessageBox.warning(self, "Vacío", "No hay bloques en el workspace")
            return
        
        try:
            # Transpilar
            python_code = self.transpiler.xml_to_python(self.current_xml)
            
            # Ejecutar
            self.console.appendPlainText("\n▶️ Ejecutando...")
            result = self.executor.run_script(python_code)
            
            # Mostrar resultado
            if result["success"]:
                self.console.appendPlainText("✅ Éxito!")
                self.console.appendPlainText(f"Tiempo: {result['execution_time_s']:.3f}s")
                if result["stdout"]:
                    self.console.appendPlainText(f"Output:\n{result['stdout']}")
                if result["result"]:
                    self.console.appendPlainText(f"Result dict:\n{json.dumps(result['result'], indent=2)}")
            else:
                self.console.appendPlainText(f"❌ Error: {result['error']}")
                if result["stderr"]:
                    self.console.appendPlainText(f"StdErr:\n{result['stderr']}")
        
        except Exception as e:
            self.console.appendPlainText(f"❌ Error: {e}")
            import traceback
            self.console.appendPlainText(traceback.format_exc())
    
    @Slot()
    def _on_export_python(self):
        """Exportar a .py"""
        if not self.current_xml:
            QMessageBox.warning(self, "Vacío", "No hay bloques")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Python", "", "Python Files (*.py)"
        )
        
        if file_path:
            try:
                python_code = self.transpiler.xml_to_python(self.current_xml)
                with open(file_path, 'w') as f:
                    f.write(python_code)
                QMessageBox.information(self, "OK", f"Guardado: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    @Slot()
    def _on_save_project(self):
        """Guardar proyecto (XML + metadatos)"""
        if not self.current_xml:
            QMessageBox.warning(self, "Vacío", "No hay bloques")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Proyecto", "", "Blockly Projects (*.blockly)"
        )
        
        if file_path:
            try:
                project = {
                    "version": "1.0",
                    "workspace_xml": self.current_xml,
                    "timestamp": str(Path(file_path).stat().st_mtime if Path(file_path).exists() else 0)
                }
                with open(file_path, 'w') as f:
                    json.dump(project, f, indent=2)
                QMessageBox.information(self, "OK", f"Guardado: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    @Slot()
    def _on_clear_workspace(self):
        """Limpiar workspace"""
        if QMessageBox.question(self, "Confirmar", "¿Limpiar todos los bloques?") == QMessageBox.Yes:
            self.editor.clear_workspace()
            self.current_xml = None
            self.code_preview.clear()
    
    @Slot()
    def _on_new_project(self):
        """Nuevo proyecto"""
        self._on_clear_workspace()
    
    @Slot()
    def _on_open_project(self):
        """Abrir proyecto"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir Proyecto", "", "Blockly Projects (*.blockly)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    project = json.load(f)
                xml_str = project.get("workspace_xml", "")
                # TODO: Cargar XML en Blockly
                self.current_xml = xml_str
                self.code_preview.setPlainText(
                    self.transpiler.xml_to_python(xml_str)
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    @Slot()
    def _on_about(self):
        """About dialog"""
        QMessageBox.about(
            self,
            "SAP2000 Visual Scripter",
            "Editor visual Blockly para automatizar SAP2000\n\n"
            "v1.0 — 2026\n\n"
            "Arrastra bloques → Configura parámetros → Ejecuta"
        )
    
    def closeEvent(self, event):
        """Al cerrar la app"""
        self.update_timer.stop()
        self.executor.disconnect()
        super().closeEvent(event)


def main():
    """Entry point"""
    app = QApplication(sys.argv)
    window = BlocklyScripterApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
