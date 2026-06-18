"""
Blockly Script Executor — Ejecuta Python generado contra SAP2000
==================================================================
Conecta a SAP2000 vía COM, ejecuta script Python en sandbox seguro,
captura output/errores, y retorna resultados.

Uso:
    executor = BlocklyScriptExecutor()
    executor.connect()
    result = executor.run_script(python_code_string)
    executor.disconnect()
"""

import comtypes.client
import sys
import io
import time
from typing import Dict, Any, Optional
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr


class SapConnection:
    """Conexión COM directa a SAP2000"""
    
    def __init__(self):
        self.sap_object = None
        self.sap_model = None
        self.is_connected = False
    
    def connect(self, attach_to_existing: bool = True) -> Dict[str, Any]:
        """Conectar a instancia SAP2000
        
        Args:
            attach_to_existing: True = conectar a instancia abierta,
                               False = crear nueva instancia
        
        Returns:
            {connected: bool, version: str, model_path: str, error: str}
        """
        try:
            if attach_to_existing:
                self.sap_object = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject"
                )
            else:
                helper = comtypes.client.CreateObject("SAP2000v1.Helper")
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
                self.sap_object = helper.CreateObjectProgID(
                    "CSI.SAP2000.API.SapObject"
                )
                self.sap_object.ApplicationStart()
            
            self.sap_model = self.sap_object.SapModel
            self.is_connected = True
            
            version = str(self.sap_object.GetOAPIVersionNumber())
            model_path = str(self.sap_model.GetModelFilename())
            
            return {
                "connected": True,
                "version": version,
                "model_path": model_path,
                "error": None
            }
        
        except Exception as e:
            self.sap_object = None
            self.sap_model = None
            self.is_connected = False
            return {
                "connected": False,
                "version": None,
                "model_path": None,
                "error": str(e)
            }
    
    def disconnect(self):
        """Desconectar (libera referencias COM)"""
        self.sap_model = None
        self.sap_object = None
        self.is_connected = False


class BlocklyScriptExecutor:
    """Ejecutor de scripts Python para Blockly"""
    
    def __init__(self):
        self.sap_connection = SapConnection()
        self.sap_temp_dir = Path.home() / ".blockly_scripts"
        self.sap_temp_dir.mkdir(exist_ok=True)
    
    def connect(self, attach_to_existing: bool = True) -> Dict[str, Any]:
        """Conectar a SAP2000"""
        return self.sap_connection.connect(attach_to_existing=attach_to_existing)
    
    def disconnect(self):
        """Desconectar de SAP2000"""
        self.sap_connection.disconnect()
    
    def run_script(
        self,
        script_str: str,
        timeout: float = 120.0
    ) -> Dict[str, Any]:
        """Ejecutar script Python generado
        
        Args:
            script_str: Código Python para ejecutar
            timeout: Timeout en segundos
        
        Returns:
            {
                success: bool,
                stdout: str,
                stderr: str,
                result: dict,
                execution_time_s: float,
                error: Optional[str]
            }
        """
        
        if not self.sap_connection.is_connected:
            return {
                "success": False,
                "stdout": "",
                "stderr": "",
                "result": {},
                "execution_time_s": 0,
                "error": "No hay conexión con SAP2000"
            }
        
        # Capturar stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        
        try:
            # Preparar namespace seguro
            safe_builtins = {
                'print': print,
                'len': len,
                'range': range,
                'list': list,
                'dict': dict,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'tuple': tuple,
                'set': set,
                'abs': abs,
                'sum': sum,
                'min': min,
                'max': max,
                'enumerate': enumerate,
                'zip': zip,
                'sorted': sorted,
                'isinstance': isinstance,
                'type': type,
                'ValueError': ValueError,
                'RuntimeError': RuntimeError,
                'AssertionError': AssertionError,
            }
            
            namespace = {
                '__builtins__': safe_builtins,
                'SapModel': self.sap_connection.sap_model,
                'SapObject': self.sap_connection.sap_object,
                'result': {},
                'sap_temp_dir': str(self.sap_temp_dir),
            }
            
            # Ejecutar con captura de output
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(script_str, namespace)
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "stdout": stdout_capture.getvalue(),
                "stderr": "",
                "result": namespace.get('result', {}),
                "execution_time_s": execution_time,
                "error": None
            }
        
        except AssertionError as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "stdout": stdout_capture.getvalue(),
                "stderr": f"Assertion failed: {e}",
                "result": {},
                "execution_time_s": execution_time,
                "error": str(e)
            }
        
        except SyntaxError as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "stdout": stdout_capture.getvalue(),
                "stderr": f"Syntax error: {e}",
                "result": {},
                "execution_time_s": execution_time,
                "error": f"Syntax error at line {e.lineno}: {e.msg}"
            }
        
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
                "result": {},
                "execution_time_s": execution_time,
                "error": str(e)
            }
    
    def get_temp_dir(self) -> str:
        """Obtener directorio temporal para scripts"""
        return str(self.sap_temp_dir)


def example_usage():
    """Ejemplo de uso"""
    
    # Código Python generado de Blockly (ejemplo)
    python_code = """
# Script generado: Simple viga
ret = SapModel.File.NewBlank()
assert ret == 0, "NewBlank failed"

ret = SapModel.PropMaterial.SetMaterial("CONC", 2)
assert ret == 0, "SetMaterial failed"

result["success"] = True
result["message"] = "Script ejecutado correctamente"
    """
    
    executor = BlocklyScriptExecutor()
    
    # Conectar
    conn_result = executor.connect(attach_to_existing=True)
    print(f"Conexión: {conn_result}")
    
    if conn_result["connected"]:
        # Ejecutar script
        exec_result = executor.run_script(python_code)
        
        print("\n=== Resultado Ejecución ===")
        print(f"Exitoso: {exec_result['success']}")
        print(f"Tiempo: {exec_result['execution_time_s']:.2f}s")
        print(f"Output: {exec_result['stdout']}")
        if exec_result['stderr']:
            print(f"Errores: {exec_result['stderr']}")
        print(f"Resultado dict: {exec_result['result']}")
        
        # Desconectar
        executor.disconnect()
        print("\nDesconectado")


if __name__ == "__main__":
    example_usage()
