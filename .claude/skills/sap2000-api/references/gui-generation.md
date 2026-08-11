# Generación de GUI Standalone (PySide6 + COM Directo)

## Cuándo Ofrecer GUI

Ofrecer generación de GUI **después** de que un script ha sido:
- ✅ Ejecutado exitosamente via `run_sap_script`
- ✅ Guardado en la biblioteca de scripts
- ✅ Funciones registradas en el registry

**Pregunta de transición:**
> *"El script está verificado y guardado. ¿Quieres generar una GUI standalone
> (PySide6) para que puedas ejecutar este modelo sin necesidad del agente/MCP?"*

## Objetivo

Convertir un script MCP verificado en un mini-software standalone compuesto por:
- `backend_{nombre}.py` — Lógica SAP2000 con COM directo (`comtypes.client`)
- `gui_{nombre}.py` — Interfaz PySide6 con botones Conectar/Ejecutar/Desconectar

**Resultado:** Un software que el usuario puede distribuir e integrar en sus
herramientas, **independiente del framework de IA**.

## Estructura de Archivos

```
scripts/{nombre}/
    gui_{nombre}.py         # GUI PySide6
    backend_{nombre}.py     # Lógica SAP2000 COM directo
```

**Regla:** La carpeta GUI solo contiene `gui_*.py` + `backend_*.py`.
Los scripts MCP originales van en `scripts/` root (ej: `scripts/example_*.py`).

## Paso 1: Identificar Inputs del Script

Revisar las variables configurables al inicio del script verificado.
Cada variable configurable se convierte en un campo de la GUI.

**Ejemplo — ring_areas:**
```python
# Estas variables del script...
r_inner = 1.0
r_mid1  = 2.0
r_mid2  = 3.5
r_outer = 5.0
t1 = 0.30
t2 = 0.20
n_segs = 36

# ...se convierten en inputs de GUI:
#   QLineEdit("r_inner", default="1.0")
#   QLineEdit("r_mid1",  default="2.0")
#   ...etc.
```

## Paso 2: Generar Backend Standalone

Usar como base la plantilla `scripts/templates/backend_template.py`:

1. **Copiar** `backend_template.py` → `backend_{nombre}.py`
2. **Renombrar** `MyConfig` → `{Nombre}Config` con los parámetros del script
3. **Renombrar** `MyBackend` → `{Nombre}Backend`
4. **Copiar la lógica** del script verificado al método `run()`:
   - Variables globales → `config.param_x`
   - `SapModel` (pre-inyectado en sandbox) → `self.sap_model`
   - `result` global → `result` local (dict)
   - `sap_temp_dir` → Ruta configurable o `tempfile.gettempdir()`
   - Funciones auxiliares → métodos de la clase Backend
5. **Mantener asserts** y estructura de tareas numeradas

### Reglas Inquebrantables del Backend

- ❌ NO importar `sap_bridge`, `sap_executor`, ni nada de `mcp_server/`
- ❌ NO importar `app_logger`, `sap_utils_common`, ni módulos externos no estándar
- ✅ Solo `comtypes.client`, `math`, `dataclasses`, stdlib
- ✅ `SapConnection` con `connect()`, `disconnect()`, `is_connected`

### Patrón del Backend

```python
import comtypes.client
from dataclasses import dataclass

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""
    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing=True) -> dict:
        # ... ver backend_template.py para implementación completa
        pass

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}

@dataclass
class NombreConfig:
    param_1: float = 1.0
    param_2: str = "DEFAULT"

class NombreBackend:
    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config: NombreConfig) -> dict:
        SapModel = self.sap_model
        result = {}
        # ... lógica del script verificado ...
        result["success"] = True
        return result
```

## Paso 3: Generar GUI Standalone

Usar como base la plantilla `scripts/templates/gui_template.py`:

1. **Copiar** `gui_template.py` → `gui_{nombre}.py`
2. **Ajustar import:** `from backend_{nombre} import SapConnection, {Nombre}Backend, {Nombre}Config`
3. **Reemplazar inputs:** Un `QLineEdit` por cada variable configurable (de Paso 1)
4. **Ajustar `_build_config()`:** Leer los inputs y crear el Config
5. **Ajustar `_format_result()`:** Mostrar métricas relevantes del resultado
6. **Renombrar** `MainWindow` → `{Nombre}GUI`
7. **Ajustar título** del `setWindowTitle()`

### Patrón de la GUI

La GUI usa 3 Workers (QThread) para operaciones async:
- `ConnectWorker` — Conexión a SAP2000
- `RunWorker` — Ejecución del backend
- `DisconnectWorker` — Desconexión

Elementos de la interfaz:
- Status indicator (rojo/verde)
- Input section (QGroupBox + QLineEdit fields)
- Output log (QTextEdit, read-only, Consolas 9pt)
- 3 botones: Conectar / Ejecutar / Desconectar
- `_busy(True/False)` para deshabilitar botones durante ejecución

## Paso 4: Testing

1. **Sintaxis:** `python -c "import ast; ast.parse(open('backend_*.py').read())"`
2. **GUI abre:** `python gui_{nombre}.py` → debe abrir ventana (sin SAP2000)
3. **Flujo completo** (si SAP2000 disponible):
   - Conectar → status verde
   - Ingresar parámetros → Ejecutar → log muestra resultado
   - Desconectar → status rojo

## Templates de Referencia

- **Backend base:** `scripts/templates/backend_template.py`
- **GUI base:** `scripts/templates/gui_template.py`

## Ejemplos Existentes

- **Placa Base:** `scripts/placabase/backend_placabase.py` + `gui_placabase.py`
- **Ring Areas:** `scripts/ring_areas/backend_ring_areas.py` + `gui_ring_areas.py`

## Estilo de Código

Todo el código generado debe seguir el estilo de `scripts/example_1001_simple_beam.py`:
- Headers claros: `# ── Task N: Nombre ──────────────────────────────`
- Cada llamada API: `assert ret == 0, f"NombreFuncion failed: {ret}"`
- Variables configurables al inicio, separadas visualmente
- Resultado en dict (`result["key"] = value`)
- Fórmulas de referencia en comentarios (si aplica)
