# Manual de Scripts SAP2000 — Guía Teórica Completa

> **Alcance:** este manual explica en profundidad la arquitectura, los patrones
> de diseño y el flujo de información de todos los scripts que viven en la
> carpeta `scripts/`.  Está orientado a quién quiera entender **cómo funcionan**
> los módulos existentes o **crear uno nuevo** siguiendo las mismas convenciones.

---

## Índice

1. [Visión general de la arquitectura](#1-visión-general-de-la-arquitectura)
2. [Dos modos de ejecución](#2-dos-modos-de-ejecución)
3. [Bloque de conexión COM — `SapConnection`](#3-bloque-de-conexión-com--sapconnection)
4. [Capa de configuración — Dataclasses](#4-capa-de-configuración--dataclasses)
5. [Capa de lógica — Backend](#5-capa-de-lógica--backend)
6. [Helper `_check_ret`](#6-helper-_check_ret)
7. [Capa de interfaz — GUI PySide6](#7-capa-de-interfaz--gui-pyside6)
8. [Workers asíncronos — QThread + Signal](#8-workers-asíncronos--qthread--signal)
9. [Flujo de información GUI ↔ Backend](#9-flujo-de-información-gui--backend)
10. [Infraestructura compartida — `shared.py`](#10-infraestructura-compartida--sharedpy)
11. [Configuración externa — `config.py`](#11-configuración-externa--configpy)
12. [Módulo multi-tab](#12-módulo-multi-tab)
13. [Catálogo de módulos](#13-catálogo-de-módulos)
14. [Scripts MCP sin GUI](#14-scripts-mcp-sin-gui)
15. [Wrappers de funciones individuales](#15-wrappers-de-funciones-individuales)
16. [Registry de funciones verificadas](#16-registry-de-funciones-verificadas)
17. [Guía para crear un nuevo módulo](#17-guía-para-crear-un-nuevo-módulo)
18. [Preguntas frecuentes y errores comunes](#18-preguntas-frecuentes-y-errores-comunes)

---

## 1. Visión general de la arquitectura

```
scripts/
├── templates/              ← Punto de partida: backend_template.py + gui_template.py
├── <módulo>/               ← Un subdirectorio por funcionalidad
│   ├── backend_<nombre>.py ← Lógica pura SAP2000 (COM)
│   ├── gui_<nombre>.py     ← Interfaz PySide6 que consume el backend
│   └── (config.py / shared.py  opcionales)
├── wrappers/               ← Scripts mínimos que demuestran 1 función API
├── registry.json           ← Índice de funciones verificadas
└── example_*.py            ← Scripts de ejemplo/verificación vía MCP
```

La arquitectura sigue un patrón **MVC simplificado** de tres capas:

```
┌──────────────────────────────────────────────────────────┐
│   GUI  (gui_*.py)  — PySide6                             │
│   Responsabilidad: presentar inputs, lanzar workers,     │
│   mostrar resultados. No toca la API de SAP2000.         │
├──────────────────────────────────────────────────────────┤
│   Workers (QThread)                                      │
│   Puente asíncrono: ejecutan operaciones COM en un hilo  │
│   separado para no bloquear la interfaz gráfica.         │
├──────────────────────────────────────────────────────────┤
│   Backend (backend_*.py)  — Python puro + comtypes       │
│   Responsabilidad: toda la lógica SAP2000.               │
│   Recibe un Config (dataclass), retorna un dict.         │
├──────────────────────────────────────────────────────────┤
│   SapConnection                                          │
│   Gestiona la conexión/desconexión COM al proceso        │
│   SAP2000 en ejecución.                                  │
└──────────────────────────────────────────────────────────┘
```

**Principio clave:** la GUI nunca llama a `comtypes` directamente.
El backend nunca importa nada de PySide6.
Cada capa tiene una responsabilidad única y bien delimitada.

---

## 2. Dos modos de ejecución

### Modo A — Script MCP (sin GUI)

Los archivos `example_*.py` y los scripts guardados en la raíz de `scripts/`
están pensados para ejecutarse a través del servidor MCP (`run_sap_script`).

En este modo:
- SAP2000 ya está en ejecución y conectado.
- Las variables `SapModel`, `SapObject` y `result` son **pre-inyectadas** por el
  sandbox del servidor MCP antes de correr el script.
- No hay UI, no hay `comtypes.client` directo: el sandbox provee la conexión.
- Los scripts terminan poniendo resultados en el dict `result`.

```python
# Ejemplo: example_1001_simple_beam.py (extracto)
ret = SapModel.InitializeNewModel()          # SapModel ya existe
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

result["beam_name"] = beam_name              # result ya existe
result["success"] = True
```

### Modo B — GUI Standalone (COM directo)

Los módulos con GUI conectan a SAP2000 directamente vía `comtypes.client`,
**sin pasar por el MCP server**.  Esto permite distribuir la herramienta como
una aplicación independiente que el ingeniero abre mientras SAP2000 está corriendo.

```
Ingeniero
   │  abre gui_placabase.py
   ▼
GUI (PySide6)  ──[click Conectar]──►  SapConnection.connect()
                                            │
                                            ▼
                               comtypes.client.GetActiveObject(
                                   "CSI.SAP2000.API.SapObject")
                                            │
                                            ▼
                                       SapModel  ◄──── SAP2000 en ejecución
```

Los imports en este modo:
```python
import comtypes.client          # COM Windows
from dataclasses import dataclass
from PySide6.QtCore import QThread, Signal
```

> **Importante:** los módulos Modo B **no deben importar** nada de
> `mcp_server/`, `sap_bridge`, ni `sap_executor`.  Son completamente autónomos.

---

## 3. Bloque de conexión COM — `SapConnection`

`SapConnection` aparece **copiada literalmente** en casi todos los backends.
Es una clase pequeña y estable que maneja el ciclo de vida de la conexión COM.

```python
class SapConnection:
    def __init__(self):
        self.sap_object = None   # CSI.SAP2000.API.SapObject
        self.sap_model  = None   # SapModel (raíz de la API)

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing: bool = True) -> dict:
        ...

    def disconnect(self) -> dict:
        ...
```

### Método `connect()`

Tiene dos modos internos controlados por `attach_to_existing`:

| `attach_to_existing` | Comportamiento |
|---|---|
| `True` (default) | Usa `GetActiveObject` — se conecta a la instancia SAP2000 **ya abierta**. Es el uso normal en GUI. |
| `False` | Crea una nueva instancia de SAP2000 vía `cHelper.CreateObjectProgID`. Útil para scripts automáticos. |

**Retorno siempre es un `dict`** (nunca lanza excepción a la GUI):

```python
# Éxito:
{"connected": True, "version": "22.0.0", "model_path": "C:\\...\\modelo.sdb"}

# Fallo:
{"connected": False, "error": "No se puede conectar al servidor COM"}
```

La cadena COM es:
```
comtypes.client.GetActiveObject("CSI.SAP2000.API.SapObject")
    → sap_object                           (nivel aplicación)
    → sap_object.SapModel  = sap_model     (nivel modelo)
```

`sap_model` es el punto de entrada a toda la API de SAP2000:
`sap_model.PropMaterial`, `sap_model.FrameObj`, `sap_model.Analyze`, etc.

### Método `disconnect()`

Simplemente pone a `None` las referencias COM.  **No cierra SAP2000.**  Solo
libera el puntero Python al objeto COM para permitir que el garbage collector
limpie la referencia.

---

## 4. Capa de configuración — Dataclasses

Cada módulo define un **dataclass de configuración** que encapsula todos los
parámetros de entrada.  Esto desacopla la GUI del backend: la GUI sólo necesita
saber cómo construir el Config, y el backend sólo necesita saber cómo consumirlo.

### Patrón básico

```python
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class RingAreasConfig:
    r_inner: float = 1.0    # Radio interior [m]
    r_mid1:  float = 2.0    # Radio intermedio 1 [m]
    r_mid2:  float = 3.5    # Radio intermedio 2 [m]
    r_outer: float = 5.0    # Radio exterior [m]
    t1:      float = 0.30   # Espesor zona interior/exterior [m]
    t2:      float = 0.20   # Espesor zona intermedia [m]
    mat_name: str  = "CONC" # Nombre del material en SAP2000
    n_segs:  int   = 16     # Segmentos por cuarto de arco
```

### Patrón con listas (usando `field`)

Cuando un parámetro es una lista mutable, se usa `field(default_factory=list)`
para evitar el problema clásico de los valores por defecto mutables en Python:

```python
@dataclass
class PlacaBaseConfig:
    bolt_centers: List[Tuple[float, float, float]] = field(default_factory=list)
    # NO: bolt_centers: list = []   ← peligroso, todas las instancias comparten la misma lista
```

### Patrón con método de resolución

Algunos configs tienen lógica interna para auto-completar valores:

```python
@dataclass
class PlacaBaseConfig:
    n_pernos: int = 4
    bolt_dia: float = 25.0
    bolt_centers: List[...] = field(default_factory=list)

    def resolve_bolt_centers(self):
        """Auto-genera bolt_centers si está vacío según diámetro y número de pernos."""
        if not self.bolt_centers:
            A, _ = self.map_dia_to_spacing(self.bolt_dia)
            # ... lógica de posicionamiento automático ...
            self.bolt_centers = self.bolt_centers[: self.n_pernos]
```

El backend llama `config.resolve_bolt_centers()` al inicio de `run()`.

### Dataclasses frozen (inmutables)

Para tablas de constantes que **no deben modificarse**, se usa `frozen=True`:

```python
@dataclass(frozen=True)
class SoilParameters:
    S: float    # Factor de suelo
    r: float    # Exponente
    T0: float   # Período característico 1
    p: float    # Exponente espectro
    q: float    # Exponente espectro 2
    T1: float   # Período de plataforma
```

Estas dataclasses viven en `config.py` y se importan como constantes.

### Dónde vive la config

| Módulo | Archivo config | Clase |
|---|---|---|
| `ring_areas` | `backend_ring_areas.py` | `RingAreasConfig` |
| `placabase` | `backend_placabase.py` | `PlacaBaseConfig` |
| `mesh` | `backend_mesh_rect.py`, etc. | `RectMeshConfig`, `MeshHoleConfig` |
| `modelo_base` | `backend_modelo_base.py` | `BaseModelConfig` |
| `comb_cargas` | No usa dataclass — los combos son listas de dicts dinámicos |
| `database_tables` | `backend_database_tables.py` | (varias clases internas) |

---

## 5. Capa de lógica — Backend

El backend es el núcleo del sistema.  Su responsabilidad es traducir un
`Config` a llamadas API de SAP2000 y devolver un `dict` de resultados.

### Estructura canónica

```python
class RingAreasBackend:

    def __init__(self, connection: SapConnection):
        self._conn = connection          # Guarda referencia, no copia

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model      # Acceso centralizado y protegido

    def run(self, config: RingAreasConfig) -> dict:
        SapModel = self.sap_model        # Alias local por comodidad
        result = {}

        # ── Task 1: Inicializar ──────────────────────────────────────────
        ret = SapModel.InitializeNewModel()
        assert ret == 0, f"InitializeNewModel failed: {ret}"

        ret = SapModel.File.NewBlank()
        assert ret == 0, f"NewBlank failed: {ret}"

        result["task_1_init"] = True

        # ── Task 2: Material ─────────────────────────────────────────────
        ret = SapModel.PropMaterial.SetMaterial(config.mat_name, 2)
        assert ret == 0, f"SetMaterial failed: {ret}"

        result["task_2_material"] = config.mat_name

        # ── ... más tasks ─────────────────────────────────────────────────

        result["success"] = True
        return result
```

### Convenciones del método `run()`

1. **Variable local `SapModel`**: siempre se asigna `SapModel = self.sap_model`
   al inicio para tener un alias corto y legible.

2. **Tareas numeradas**: el código se divide en bloques `# ── Task N: ... ──`
   para facilitar depuración y lectura.

3. **Assert en cada `ret`**: `assert ret == 0, f"API_call failed: {ret}"` es
   la forma estándar de detener la ejecución si algo falla en la API.

4. **Dict de resultados**: cada tarea exitosa escribe su resultado en `result`.
   El dict final siempre incluye `result["success"] = True` al terminar bien.

5. **Sin prints ni logging externo**: el backend usa `print()` como mucho, o
   un método `_log()` interno.  No depende de loggers externos.

### Backends con múltiples métodos (no solo `run`)

Algunos backends, en lugar de un único `run()`, exponen métodos individuales:

```python
class CombosBackend:
    def get_load_cases(self) -> list: ...        # Lee casos de SAP2000
    def get_combinations(self) -> list: ...      # Lee combos existentes
    def push_combinations(self, data: list) -> int: ...  # Escribe combos
    def delete_combination(self, name: str) -> bool: ... # Borra combo
```

Esta variante es típica de backends que implementan operaciones **CRUD**
(leer, crear, actualizar, borrar) en lugar de un único proceso de generación.

### Backends de post-proceso (solo lectura)

```python
class EstabilidadBackend:
    def get_selected_joints(self) -> List[str]: ...
    def get_combo_names(self) -> List[str]: ...
    def get_joint_displacements(self, joints, combos) -> List[dict]: ...
```

Aquí el backend no crea geometría, solo **extrae resultados** de un modelo
ya analizado.

---

## 6. Helper `_check_ret`

La API de SAP2000 retorna valores de dos formas:

| Tipo de retorno | Ejemplo | Significado |
|---|---|---|
| `int` directo | `ret = SapModel.File.NewBlank()` → `0` | 0 = éxito |
| `tuple/list` | `ret = SapModel.FrameObj.AddByCoord(...)` → `("1", 0)` | último elemento = código de retorno |

`_check_ret` abstrae esta dualidad:

```python
def _check_ret(ret) -> bool:
    if isinstance(ret, (list, tuple)):
        return int(ret[-1]) == 0   # último elemento de la tupla
    return int(ret) == 0           # valor directo
```

Uso típico:

```python
ret = SapModel.PropArea.SetShell_1(name, 1, True, mat, 0.0, t, t)
if not _check_ret(ret):
    raise RuntimeError(f"SetShell_1 '{name}' falló: código {ret}")
```

### Helper `_get_name`

Cuando la API retorna el nombre del objeto creado (generalmente en `ret[0]`):

```python
def _get_name(ret, fallback: str) -> str:
    if isinstance(ret, (list, tuple)) and len(ret) >= 2 and ret[-1] == 0:
        val = ret[0]
        if isinstance(val, (list, tuple)) and len(val) > 0:
            return str(val[0])
        return str(val)
    return fallback   # usa el nombre que nosotros intentamos asignar
```

Ejemplo de uso:

```python
ret = SapModel.FrameObj.AddByCoord(0,0,0, 10,0,0, "", "BEAM_SEC", "BEAM_1")
beam_name = _get_name(ret, "BEAM_1")   # SAP puede renombrar internamente
```

---

## 7. Capa de interfaz — GUI PySide6

La GUI es responsable de:

- Mostrar un **formulario de parámetros** (campos `QLineEdit`, `QComboBox`,
  `QCheckBox`, `QTableWidget`, etc.)
- Gestionar el estado de conexión (botones habilitados/deshabilitados)
- Lanzar **Workers** para operaciones SAP2000 (asíncronos)
- Mostrar resultados en un **log** (`QTextEdit` read-only, fuente Consolas)
- Opcionalmente, mostrar una **vista previa** del modelo a generar

### Estructura de la ventana principal

```
QWidget (MainWindow)
├── Status label (rojo/verde)
├── QPushButton "Conectar a SAP2000"
├── QGroupBox "Parámetros de entrada"
│   └── QGridLayout con QLabel + QLineEdit / QComboBox / QCheckBox
├── QPushButton "Ejecutar"
├── QGroupBox "Salida"
│   └── QTextEdit (read-only, Consolas 9pt)
└── QPushButton "Desconectar de SAP2000"
```

### Estado interno de la ventana

```python
class MainWindow(QWidget):
    def __init__(self):
        self._conn    = SapConnection()        # única instancia de conexión
        self._backend = MyBackend(self._conn)  # backend comparte la conexión
        self._worker  = None                   # referencia al QThread activo
```

`self._worker` mantiene una referencia fuerte al QThread para evitar que el
garbage collector lo destruya mientras está ejecutándose.

### Gestión de botones — método `_busy()`

```python
def _busy(self, is_busy: bool):
    self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
    self._btn_run.setEnabled(not is_busy and self._conn.is_connected)
    self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)
```

Reglas:
- Mientras hay un Worker ejecutándose → todos los botones deshabilitados
- Sin Worker y desconectado → solo "Conectar" habilitado
- Sin Worker y conectado → "Ejecutar" y "Desconectar" habilitados

### Método `_build_config()`

Convierte los valores de los widgets en un objeto Config:

```python
def _build_config(self) -> MyConfig:
    return MyConfig(
        r_inner = float(self._input_r_inner.text()),
        r_outer = float(self._input_r_outer.text()),
        mat_name = self._combo_material.currentText(),
    )
```

Si los inputs tienen errores de conversión (`ValueError`), el método los
propaga para que `_on_run()` los capture y los muestre en el log.

### Método `_format_result()`

Convierte el dict de resultados a texto legible para el log.  La
implementación mínima usa `json.dumps`, pero se puede personalizar:

```python
def _format_result(self, data: dict) -> str:
    lines = []
    lines.append(f"Áreas creadas: {data.get('num_areas', 0)}")
    lines.append(f"Material:      {data.get('material', '-')}")
    return "\n".join(lines)
```

---

## 8. Workers asíncronos — QThread + Signal

Las operaciones COM a SAP2000 pueden tardar varios segundos.  Si se ejecutan
en el hilo principal de Qt, la GUI se congela.  La solución son los **Workers**.

### Patrón Worker

```python
class RunWorker(QThread):
    finished = Signal(dict)   # señal emitida al terminar

    def __init__(self, backend: MyBackend, config: MyConfig):
        super().__init__()
        self._backend = backend
        self._config  = config

    def run(self):                    # se ejecuta en hilo separado
        try:
            result = self._backend.run(self._config)
            self.finished.emit(result)
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})
```

**Reglas de QThread:**
- Solo se define el método `run()`.  Todo lo que esté en `run()` corre en el
  hilo secundario.
- **Nunca** se llama a widgets de Qt desde `run()` (no es thread-safe).
- La comunicación de vuelta al hilo GUI es únicamente a través de `Signal`.

### Los tres Workers estándar

| Worker | Operación |
|---|---|
| `ConnectWorker` | Llama `connection.connect()` |
| `RunWorker` | Llama `backend.run(config)` |
| `DisconnectWorker` | Llama `connection.disconnect()` |

### Workers especializados

Algunos módulos añaden workers adicionales:

| Worker | Módulo | Operación |
|---|---|---|
| `ReadWorker` | `comb_cargas` | Lee Load Cases + Combos existentes |
| `WriteWorker` | `comb_cargas` | Escribe combos + borra los eliminados |
| `GetCoordsWorker` | `steel_connections` | Lee coords del nodo seleccionado |
| `BaseModelWorker` | `steel_connections` | Crea modelo base N-mm-C |
| `GetJointsWorker` | `post_proceso` | Lee joints seleccionados |
| `GetResultsWorker` | `post_proceso` | Extrae desplazamientos/resultados |

### Ciclo de vida completo de un Worker

```
GUI: _on_run()
  │
  ├─ Llama _build_config()         → puede lanzar ValueError
  ├─ Llama _busy(True)             → deshabilita botones
  ├─ Crea RunWorker(backend, config)
  ├─ Conecta worker.finished → _on_run_done
  ├─ worker.start()                → lanza el hilo
  │
  │  [Hilo secundario]
  │  worker.run()
  │    └─ backend.run(config)
  │         └─ llamadas COM a SAP2000
  │    └─ emit finished(result_dict)
  │
  └─ [Hilo GUI — callback]
     _on_run_done(result)
       ├─ _busy(False)             → re-habilita botones
       ├─ si result["success"]:    → muestra resultado
       └─ si not success:          → muestra error
```

---

## 9. Flujo de información GUI ↔ Backend

Este es el diagrama completo del flujo de datos para la operación más común
(generar modelo):

```
┌──────────────────────────────────────────────────────────────────┐
│  USUARIO                                                         │
│  Rellena campos: r_inner=1.0, r_outer=5.0, material="CONC"      │
│  Hace click en [Ejecutar]                                        │
└────────────────────────────┬─────────────────────────────────────┘
                             │  click event
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  GUI — _on_run()                                                 │
│                                                                  │
│  1. config = _build_config()                                     │
│     ┌──────────────────────────────────────────────────────┐     │
│     │ RingAreasConfig(                                     │     │
│     │   r_inner  = float(self._input_r_inner.text()),      │     │
│     │   r_outer  = float(self._input_r_outer.text()),      │     │
│     │   mat_name = self._combo_material.currentText(),     │     │
│     │ )                                                    │     │
│     └──────────────────────────────────────────────────────┘     │
│                                                                  │
│  2. _busy(True)    → deshabilita todos los botones               │
│                                                                  │
│  3. worker = RunWorker(self._backend, config)                    │
│  4. worker.finished.connect(self._on_run_done)                   │
│  5. worker.start()                                               │
└────────────────────────────┬─────────────────────────────────────┘
                             │  QThread lanza hilo secundario
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  RunWorker.run()   [Hilo secundario]                             │
│                                                                  │
│  result = self._backend.run(self._config)                        │
└────────────────────────────┬─────────────────────────────────────┘
                             │  delega a backend
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  BACKEND — RingAreasBackend.run(config)                          │
│                                                                  │
│  SapModel = self.sap_model     ← valida conexión                │
│                                                                  │
│  Task 1: SapModel.InitializeNewModel()  → assert ret==0         │
│  Task 2: SapModel.File.NewBlank()       → assert ret==0         │
│  Task 3: SapModel.SetPresentUnits(6)    → assert ret==0         │
│  Task 4: SapModel.PropMaterial.SetMaterial(config.mat_name, 2)  │
│  Task 5: SapModel.PropArea.SetShell_1(...)  × 3 propiedades     │
│  Task 6: SapModel.AreaObj.AddByCoord(...)   × N áreas           │
│  Task 7: SapModel.View.RefreshView(0, False)                    │
│                                                                  │
│  return {                                                        │
│    "success": True,                                              │
│    "num_areas": N,                                               │
│    "material": config.mat_name,                                  │
│    "ring_zones": [{"zone": 1, "areas": [...]}, ...]              │
│  }                                                               │
└────────────────────────────┬─────────────────────────────────────┘
                             │  COM → SAP2000
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  SAP2000 (proceso separado, Windows)                             │
│  Modelo se actualiza en tiempo real                              │
└────────────────────────────┬─────────────────────────────────────┘
                             │  resultado dict
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  RunWorker.run()   [Hilo secundario]                             │
│                                                                  │
│  self.finished.emit(result)   → señal Qt cruzando hilos          │
└────────────────────────────┬─────────────────────────────────────┘
                             │  Signal → hilo GUI
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  GUI — _on_run_done(result)                                      │
│                                                                  │
│  _busy(False)           → re-habilita botones                    │
│  if result["success"]:                                           │
│      _log_append("✔ Ejecución exitosa")                          │
│      _log_append(_format_result(result))                         │
│  else:                                                           │
│      _log_append(f"✘ Error: {result['error']}")                  │
└──────────────────────────────────────────────────────────────────┘
```

### Flujo para módulo CRUD (comb_cargas)

El módulo de combinaciones tiene un flujo bidireccional más complejo:

```
[Leer de SAP2000]
GUI._on_read()
  │
  ▼ ReadWorker.run()
      │── backend.get_load_cases()  → ["DEAD", "LIVE", "QUAKE", ...]
      │── backend.get_combinations() → [{"name":"COMB1","items":{...}}, ...]
      └── emit finished({"cases": [...], "combos": [...]})
  │
  ▼ GUI._on_read_done(result)
      │── Reconstruye columnas de la tabla con los Load Cases
      └── Rellena filas con los combos existentes

[Edición manual en la tabla por el usuario]

[Enviar a SAP2000]
GUI._on_write()
  │
  ▼ WriteWorker.run()
      │── backend.delete_combination(name)  × combos eliminados
      └── backend.push_combinations(data)   × combos actuales
  │
  ▼ GUI._on_write_done(result)
      └── Log: "N combinaciones procesadas"
```

---

## 10. Infraestructura compartida — `shared.py`

Cuando varios módulos dentro de un mismo directorio comparten código, se extrae
a un archivo `shared.py`.  El ejemplo más completo es `steel_connections/shared.py`.

### Contenido de `steel_connections/shared.py`

```
shared.py
├── SapConnection          ← Igual a todos los backends
├── _check_ret()           ← Helper de API
├── _shape_coords_2d()     ← Genera coordenadas círculo/cuadrado en 2D
├── _build_axes()          ← Construye ejes locales con rotación
├── _local_to_global_axes() ← Transforma coord local → global 3D
├── ConnectWorker          ← Worker de conexión (con carga extra de propiedades)
├── DisconnectWorker       ← Worker de desconexión
├── RunWorker              ← Worker de ejecución genérico
├── GetCoordsWorker        ← Worker que lee coords del nodo seleccionado en SAP2000
├── BaseModelWorker        ← Worker que crea modelo base N-mm-C con materiales
├── BASE_MATERIALS         ← Lista de materiales de acero (A36, A500_GrB, A325, A490)
└── create_base_model()    ← Función que inicializa modelo con materiales de acero
```

Los backends (`backend_simple_plate.py`, `backend_multi_bolt.py`, etc.) importan
solo lo que necesitan:

```python
from shared import SapConnection, _check_ret, _shape_coords_2d, _build_axes
```

Las GUIs importan Workers y SapConnection:

```python
from shared import SapConnection, ConnectWorker, DisconnectWorker, RunWorker
```

### Helper `_shape_coords_2d`

Genera puntos distribuidos uniformemente sobre una forma (círculo o cuadrado)
en el plano local 2D:

```
Círculo: N puntos equiangulares sobre radio = dim/2
Cuadrado: N puntos distribuidos sobre el perímetro del cuadrado de lado dim
```

### Helper `_build_axes` + `_local_to_global_axes`

Permiten definir patrones de geometría en un plano arbitrario (XY, XZ, YZ)
con rotación adicional, y luego transformar las coordenadas al sistema global:

```python
e_u, e_v, e_n = _build_axes(plane="XZ", angle_deg=30.0)

for u, v in coords_2d:
    x, y, z = _local_to_global_axes(origin, e_u, e_v, e_n, u, v, 0.0)
    # crear punto en SAP2000 con (x, y, z)
```

---

## 11. Configuración externa — `config.py`

El módulo `modelo_base` externaliza todas las constantes a un `config.py`
separado.  Esto facilita editar tablas de materiales, secciones y combinaciones
**sin tocar la lógica del backend**.

### Estructura de `modelo_base/config.py`

```python
# Constantes físicas
TON_M_UNITS: int = 12
GRAVITY: float = 9.81

# Parámetros sísmicos NCh2369
AR_BY_ZONE: Dict[SeismicZone, float] = {1: 0.28, 2: 0.42, 3: 0.56}
SOIL_PARAMS: Dict[SoilType, SoilParameters] = {
    "A": SoilParameters(S=0.90, r=4.50, T0=0.15, ...),
    "C": SoilParameters(S=1.05, r=4.50, T0=0.40, ...),
    ...
}

# Patrones de carga
LOAD_PATTERNS = [
    {"name": "DEAD", "type": 1, "self_wt": 1.2},
    {"name": "LIVE", "type": 3, "self_wt": 0.0},
    ...
]

# Materiales por defecto
DEFAULT_MATERIALS = [...]
DEFAULT_I_SECTIONS = [...]

# Combinaciones LRFD / ASD / NCh
LRFD_COMBOS = [...]
ASD_COMBOS  = [...]
NCH_COMBOS  = [...]
```

El backend lo importa al inicio:

```python
from config import (
    TON_M_UNITS, GRAVITY, AR_BY_ZONE, SOIL_PARAMS,
    LOAD_PATTERNS, DEFAULT_MATERIALS,
    NCH_COMBOS, LRFD_COMBOS, ASD_COMBOS,
)
```

---

## 12. Módulo multi-tab

Algunos módulos agrupan varias funcionalidades relacionadas en una **ventana
con pestañas** (`QTabWidget`).  Los ejemplos son:

- `steel_connections/gui_steel_connections.py` — 4 tabs: Placas Pernadas,
  Perfiles, Multi-Perno, Placa Simple
- `post_proceso/gui_post_proceso.py` — tabs: Estabilidad, Shells, Modo Fundamental

### Patrón de ventana multi-tab

```python
class SteelConnectionsWindow(QWidget):
    def __init__(self):
        self._conn = SapConnection()    # conexión COMPARTIDA entre todos los tabs

        root = QVBoxLayout(self)

        # Header: estado + Conectar / Desconectar (COMPARTIDO)
        self._status_lbl = QLabel("Estado: desconectado")
        self._btn_connect = QPushButton("Conectar")
        self._btn_disconnect = QPushButton("Desconectar")

        # Tabs: cada uno recibe la conexión compartida
        self._tabs = QTabWidget()
        self._tabs.addTab(BoltPlatesGUI(self._conn), "Placas Pernadas")
        self._tabs.addTab(MultiBoltGUI(self._conn), "Multi-Perno")
        self._tabs.addTab(SteelProfilesGUI(self._conn), "Perfiles")
        self._tabs.addTab(SimplePlateGUI(self._conn), "Placa Simple")

        root.addWidget(self._tabs)
```

### Cómo los tabs reciben la conexión

Cada tab (subclase de `QWidget`) acepta `conn: SapConnection` en su
constructor y lo guarda para pasarlo a su backend:

```python
class BoltPlatesGUI(QWidget):
    def __init__(self, conn: SapConnection):
        super().__init__()
        self._conn    = conn
        self._backend = BoltPlatesBackend(conn)   # comparte la misma conexión
```

Así, con un solo click en "Conectar" en el header, todos los tabs quedan
conectados automáticamente porque todos apuntan al mismo `SapConnection`.

---

## 13. Catálogo de módulos

### `ring_areas/` — Generador de anillos circulares

| Archivo | Descripción |
|---|---|
| `backend_ring_areas.py` | Genera placa anular con 3 zonas de shell concéntricas |
| `gui_ring_areas.py` | Formulario de radios, espesores, material y segmentación |
| `backend_cylinder.py` | Generador de cilindro vertical (variante 3D) |

**Config clave:** `RingAreasConfig` — radios `r_inner`, `r_mid1`, `r_mid2`,
`r_outer`; espesores `t1`, `t2`; `mat_name`; `n_segs`.

### `placabase/` — Generador de placa base

| Archivo | Descripción |
|---|---|
| `backend_placabase.py` | Genera placa base con pernos, silla y resortes de balasto |
| `gui_placabase.py` | Formulario completo + vista previa 2D del perfil y pernos |

**Config clave:** `PlacaBaseConfig` — dimensiones de columna (`H_col`, `B_col`),
espesores de placa y alas, diámetro de pernos (`bolt_dia`), número de pernos
(`n_pernos`), posiciones (`bolt_centers`), silla de anclaje opcional,
balasto (`ks_balasto`).

**Característica especial:** incluye un `PreviewWidget` (subclase de `QWidget`)
que dibuja con `QPainter` una vista previa esquemática del perfil I y los
pernos de anclaje antes de ejecutar.

### `comb_cargas/` — Gestor de combinaciones de carga

| Archivo | Descripción |
|---|---|
| `combos_backend.py` | CRUD de combinaciones: leer, crear, modificar, borrar |
| `app_combos_gui.py` | Tabla editable con filas = combos, columnas = load cases |

**Sin dataclass fija:** los datos fluyen como `List[dict]` con estructura:
```python
[
  {
    "name": "COMB1_LRFD",
    "type": 0,               # 0=LRFD, 1=ASD, etc.
    "items": {
      "DEAD": 1.2,
      "LIVE": 1.6,
      "QUAKE": 1.0,
    }
  },
  ...
]
```

### `mesh/` — Generador de mallas de áreas

| Archivo | Descripción |
|---|---|
| `backend_mesh_rect.py` | Malla rectangular parametrizada (nx × ny celdas) |
| `backend_mesh_hole.py` | Malla rectangular con hueco interior |
| `backend_ring_areas.py` | Malla tipo anillo (copia del módulo ring_areas) |
| `backend_cylinder.py` | Malla cilíndrica 3D |
| `gui_mesh.py` | GUI unificada con QTabWidget para todos los tipos de malla |

**Config `RectMeshConfig`:** `width`, `length`, `nx`, `ny`, `start_x/y/z`,
`plane` ("XY"/"XZ"/"YZ"), `prop_name`.

### `modelo_base/` — Modelo base sísmico NCh2369

| Archivo | Descripción |
|---|---|
| `backend_modelo_base.py` | Crea modelo con materiales, secciones, espectros y combos |
| `gui_modelo_base.py` | Formulario de zona sísmica, suelo, factores R y amortiguamiento |
| `config.py` | Tablas de materiales, secciones, load patterns y combinaciones |

**Config `BaseModelConfig`:** `zone` (1-3), `soil` (A-E), `importance`,
`r_x`, `r_y`, `r_v`, `damping_x`, `damping_y`, `xi_v`.

### `steel_connections/` — Conexiones de acero

| Archivo | Descripción |
|---|---|
| `shared.py` | Infraestructura compartida (ver §10) |
| `backend_simple_plate.py` | Placa simple con malla rectangular en cualquier plano |
| `backend_multi_bolt.py` | Patrón de pernos filas × columnas con orientación 3D |
| `backend_steel_profiles.py` | Perfiles de acero modelados como placas shell |
| `gui_steel_connections.py` | Ventana principal con 4 tabs |
| `gui_bolt_plates.py` | Tab: Placas Pernadas (frame + gap links + shell) |
| `gui_multi_bolt.py` | Tab: Patrón Multi-Perno |
| `gui_steel_profiles.py` | Tab: Perfiles de Acero |
| `gui_simple_plate.py` | Tab: Placa Simple |

### `post_proceso/` — Post-proceso de resultados

| Archivo | Descripción |
|---|---|
| `backend_estabilidad.py` | Extrae desplazamientos de nodos por combinación |
| `backend_shells.py` | Extrae fuerzas/tensiones de elementos shell |
| `backend_mod_fund.py` | Extrae períodos y participación modal |
| `gui_post_proceso.py` | GUI multi-tab con exportación a CSV |

### `database_tables/` — Explorador de tablas

| Archivo | Descripción |
|---|---|
| `backend_database_tables.py` | Lista, lee, edita y exporta Database Tables de SAP2000 |
| `gui_database_tables.py` | Interfaz de exploración con búsqueda y edición inline |

---

## 14. Scripts MCP sin GUI

Los scripts en la raíz de `scripts/` y los de `example_*.py` se ejecutan
directamente a través de la herramienta MCP `run_sap_script`.

### Variables pre-inyectadas

Cuando el MCP server ejecuta un script, inyecta automáticamente:

| Variable | Tipo | Descripción |
|---|---|---|
| `SapModel` | `comtypes.POINTER(...)` | Objeto SapModel activo |
| `SapObject` | `comtypes.POINTER(...)` | Objeto SapObject de nivel aplicación |
| `result` | `dict` | Dict vacío para que el script escriba sus resultados |
| `sap_temp_dir` | `str` | Directorio temporal donde guardar archivos `.sdb` |

### Convenciones de estos scripts

1. Usar `SapModel` directamente (sin `self` ni class).
2. `assert ret == 0` para validar cada llamada crítica.
3. Escribir en `result` al final para retornar datos al MCP.
4. Son scripts planos, sin estructura de clase.

```python
# example_ring_areas_parametric.py (fragmento)
ret = SapModel.InitializeNewModel()
assert ret == 0

# ... toda la lógica ...

result["num_areas"] = total_areas
result["success"]   = True
```

---

## 15. Wrappers de funciones individuales

El directorio `wrappers/` contiene scripts **mínimos** (generalmente 20-50 líneas)
que demuestran el uso correcto de **una sola función** de la API de SAP2000.

### Propósito

- Documentación ejecutable de cada función API
- Fuente de referencia para firmas, tipos de parámetros y formatos de retorno
- Punto de verificación al incorporar nuevas funciones al registry

### Naming convention

```
func_{Namespace}_{FunctionName}.py
```

Ejemplos:
- `func_PropMaterial_SetMaterial.py`
- `func_FrameObj_AddByCoord.py`
- `func_Results_JointDispl.py`
- `func_DatabaseTables_GetAllTables.py`

### Estructura de un wrapper

```python
# func_FrameObj_AddByCoord.py
"""Wrapper: SapModel.FrameObj.AddByCoord
Agrega un elemento frame por coordenadas de inicio y fin.
Retorna (nombre_asignado, ret_code).
"""

# Requiere: SapModel inyectado por MCP
ret = SapModel.FrameObj.AddByCoord(
    xi=0.0, yi=0.0, zi=0.0,      # coord inicio
    xj=5.0, yj=0.0, zj=0.0,      # coord fin
    PropName="SEC_A",              # sección
    UserName="FRAME_1"             # nombre user (puede ser vacío "")
)

assert ret[-1] == 0, f"AddByCoord falló: {ret}"
name = ret[0]

result["frame_name"] = name
result["success"] = True
```

---

## 16. Registry de funciones verificadas

El archivo `registry.json` es el **catálogo de verdad** de todas las funciones
API que han sido verificadas con éxito en SAP2000 real.

### Estructura de una entrada

```json
{
  "SapModel.FrameObj.AddByCoord": {
    "category": "FrameObj",
    "description": "Add a new frame object by coordinates",
    "signature": "(xi, yi, zi, xj, yj, zj, PropName, UserName, CSys) -> (name, ret_code)",
    "verified": true,
    "first_verified": "2026-03-20T00:00:00+00:00",
    "last_verified": "2026-03-31T17:37:44.434636+00:00",
    "verification_count": 42,
    "wrapper_script": "func_FrameObj_AddByCoord",
    "used_in_scripts": ["example_1001_simple_beam.py"],
    "parameter_notes": "xi,yi,zi: start; xj,yj,zj: end; PropName: section name; UserName: '' for auto-name; CSys: 'Global'",
    "known_errors": [],
    "notes": "Returns (name_str, ret_code). Last element is always ret_code.",
    "verification_type": "auto"
  }
}
```

### Campos clave

| Campo | Significado |
|---|---|
| `signature` | Firma de la función con tipos de retorno |
| `parameter_notes` | Descripción detallada de cada parámetro |
| `known_errors` | Lista de errores comunes y cómo evitarlos |
| `verification_count` | Número de veces que fue verificada exitosamente |
| `wrapper_script` | Nombre del wrapper asociado en `wrappers/` |

### Importante

> ⚠️ Nunca editar `registry.json` directamente.
> Usar la herramienta MCP `register_verified_function` para agregar o actualizar entradas.

---

## 17. Guía para crear un nuevo módulo

Pasos para crear un módulo completo `mi_modulo/`:

### Paso 1: Crear el directorio

```
scripts/mi_modulo/
```

### Paso 2: Crear el backend

Copiar `templates/backend_template.py` como `backend_mi_modulo.py`.

1. Renombrar `MyConfig` → `MiModuloConfig`
2. Reemplazar los parámetros del dataclass con los de tu módulo
3. Renombrar `MyBackend` → `MiModuloBackend`
4. Reemplazar el cuerpo de `run()` con la lógica real

```python
@dataclass
class MiModuloConfig:
    ancho:    float = 10.0    # [m]
    alto:     float = 5.0     # [m]
    material: str   = "CONC"

class MiModuloBackend:
    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config: MiModuloConfig) -> dict:
        SapModel = self.sap_model
        result = {}

        # Task 1: Inicializar
        ret = SapModel.InitializeNewModel()
        assert ret == 0
        ret = SapModel.File.NewBlank()
        assert ret == 0
        result["task_1_init"] = True

        # Task 2: ... tu lógica ...

        result["success"] = True
        return result
```

### Paso 3: Crear la GUI

Copiar `templates/gui_template.py` como `gui_mi_modulo.py`.

1. Cambiar el import: `from backend_mi_modulo import SapConnection, MiModuloBackend, MiModuloConfig`
2. Renombrar `MainWindow` → `MiModuloGUI`
3. Reemplazar los campos de input en el `QGroupBox`
4. Actualizar `_build_config()` para leer los nuevos campos
5. Actualizar `_format_result()` para mostrar los resultados relevantes

### Paso 4: Agregar `if __name__ == "__main__":`

Tanto en backend (para prueba standalone sin GUI):

```python
if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect()
    if res.get("connected"):
        backend = MiModuloBackend(conn)
        config = MiModuloConfig(ancho=8.0, alto=4.0)
        output = backend.run(config)
        import json; print(json.dumps(output, indent=2))
        conn.disconnect()
```

Como en la GUI (para ejecutar directamente):

```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MiModuloGUI()
    win.show()
    sys.exit(app.exec())
```

### Paso 5: Verificar con wrappers

Si usas funciones API que no están en el registry, crear el wrapper
correspondiente en `wrappers/` y verificarlo antes de integrar.

---

## 18. Preguntas frecuentes y errores comunes

### ¿Por qué el assert falla con "InitializeNewModel failed: 0"?

No falla — `ret == 0` es éxito.  El assert es `assert ret == 0`, que pasa cuando
es 0.  Si el assert falla, el código de retorno es **distinto de 0** (ej: 1, -1).

### ¿Por qué `ret[-1]` y no `ret[0]` para el código de retorno?

La API de SAP2000 puede retornar:
- Solo el código: `ret = 0`  → `_check_ret(ret)` → `int(ret) == 0`
- Una tupla con datos primero y código al final: `ret = ("FRAME1", 0)`
  → `ret[-1]` es el código de retorno

El patrón `ret[-1]` funciona para ambos casos.

### ¿Por qué los Workers usan `Signal(dict)` y no devuelven valor?

Qt no permite acceder a widgets desde hilos secundarios.  La única forma
segura de comunicar el resultado de vuelta al hilo GUI es a través de una
`Signal`, que Qt enruta automáticamente al hilo correcto.

### ¿Por qué `self._worker = worker` en la GUI?

Para evitar que Python destruya el QThread por garbage collection mientras
está ejecutándose.  Si no se guarda la referencia, el GC puede liberar el
objeto antes de que termine.

### ¿Qué pasa si SAP2000 no está abierto al hacer "Conectar"?

`comtypes.client.GetActiveObject` lanza una excepción COM que `SapConnection.connect()`
captura y retorna como `{"connected": False, "error": "..."}`.
La GUI muestra el error en el log sin crashear.

### ¿Por qué `field(default_factory=list)` en los dataclasses?

En Python, si se usa un valor mutable como default en un dataclass sin
`field()`, **todas las instancias comparten el mismo objeto**:

```python
# ⚠️ INCORRECTO — todas las instancias comparten la lista
@dataclass
class Config:
    items: list = []

# ✔ CORRECTO — cada instancia obtiene una lista nueva
@dataclass
class Config:
    items: list = field(default_factory=list)
```

### ¿Puedo ejecutar el backend sin GUI?

Sí.  El backend es 100% independiente de PySide6.  El bloque
`if __name__ == "__main__":` en cada `backend_*.py` permite probar la lógica
directamente desde la terminal (con SAP2000 abierto en segundo plano).

### ¿Cómo agrego una nueva pestaña a un módulo multi-tab existente?

1. Crear `backend_nueva_tab.py` con la lógica correspondiente
2. Crear la clase `NuevaTabWidget(QWidget)` en `gui_post_proceso.py`
3. Agregar `self._tabs.addTab(NuevaTabWidget(self._conn), "Nueva Tab")`

La conexión se comparte automáticamente al pasarla al constructor del nuevo tab.

---

## Resumen visual del ecosistema

```
SAP2000 (proceso Windows)
        │  COM (comtypes)
        │
┌───────┴──────────────────────────────────────────────────────────┐
│  SapConnection                                                   │
│  ├── GetActiveObject("CSI.SAP2000.API.SapObject")                │
│  └── sap_model = sap_object.SapModel                             │
└───────┬──────────────────────────────────────────────────────────┘
        │
┌───────┴──────────────────────────────────────────────────────────┐
│  Backend (backend_*.py)                                          │
│  ├── Config Dataclass  ← parámetros tipados con defaults         │
│  ├── _check_ret()      ← manejo uniforme de retornos COM         │
│  ├── _get_name()       ← extrae nombre de objetos creados        │
│  └── run(config) → dict  ← lógica pura, retorna resultados       │
└───────┬──────────────────────────────────────────────────────────┘
        │
┌───────┴──────────────────────────────────────────────────────────┐
│  Workers (QThread)                                               │
│  ├── ConnectWorker    → connection.connect()                      │
│  ├── RunWorker        → backend.run(config)                       │
│  ├── DisconnectWorker → connection.disconnect()                   │
│  └── [Especializados] → según el módulo                          │
└───────┬──────────────────────────────────────────────────────────┘
        │  Signal(dict) — thread-safe
┌───────┴──────────────────────────────────────────────────────────┐
│  GUI (gui_*.py — PySide6)                                        │
│  ├── _build_config()    ← QLineEdit → Config                     │
│  ├── _busy(True/False)  ← gestión de estado de botones           │
│  ├── _log_append()      ← muestra resultados                     │
│  └── _format_result()   ← formatea dict para el usuario          │
└──────────────────────────────────────────────────────────────────┘
```

---

*Generado automáticamente a partir del análisis de los módulos en `scripts/`.*
*Última actualización: 2026-04-02*
