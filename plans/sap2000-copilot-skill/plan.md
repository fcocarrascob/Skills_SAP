# SAP2000 Copilot Skill — API Execution Bridge

**Branch:** `feat/sap2000-copilot-skill`
**Description:** Skill + MCP server que permite a Copilot crear scripts de la API de SAP2000, ejecutarlos contra una instancia local vía COM, y verificar la correcta ejecución leyendo resultados.

## Alcance

- **Producto:** SAP2000 únicamente (sin ETABS, CSiBridge ni SAFE)
- **Conexión:** Local COM solamente (sin API remota TCP)
- **Sandbox:** Solo operaciones SAP (sin acceso a filesystem, subprocess ni imports peligrosos)
- **Caso de uso principal:** Asistir al usuario en la creación de scripts de la API y verificar su correcta ejecución — el agente genera código, lo ejecuta, lee el resultado, y confirma o corrige.

## Goal

Crear un sistema donde Copilot actúe como **asistente de desarrollo de scripts SAP2000**: el usuario describe lo que necesita en lenguaje natural, Copilot consulta la documentación de la API, genera el script Python correspondiente, lo ejecuta contra SAP2000 vía COM, y verifica que la ejecución fue correcta leyendo los resultados. El ciclo es: **consultar docs → generar script → ejecutar → verificar → iterar si hay errores**.

## Análisis de Enfoques

### Opción A: Una herramienta MCP por cada función de la API
| Aspecto | Evaluación |
|---------|-----------|
| Cobertura | Requiere crear y mantener 200+ herramientas |
| Type safety | Alta — cada tool tiene parámetros tipados |
| Mantenimiento | Muy alto — cualquier cambio en la API requiere actualizar herramientas |
| Context window | Problema — 200+ tool definitions saturan el contexto del modelo |
| Escalabilidad | Pobre — cada nueva versión de SAP2000 requiere rewrite |
| **Veredicto** | **No recomendado** — overhead excesivo, límites prácticos de MCP |

### Opción B: El agente busca en los docs y ejecuta scripts genéricos
| Aspecto | Evaluación |
|---------|-----------|
| Cobertura | Inmediata — cubre TODAS las funciones documentadas |
| Type safety | Baja a nivel de tool, pero el agente puede validar leyendo docs |
| Mantenimiento | Mínimo — solo actualizar markdown de API si cambia |
| Context window | Eficiente — pocas herramientas, docs se cargan on-demand |
| Escalabilidad | Excelente — nuevas funciones = nuevo markdown |
| **Veredicto** | **Bueno pero necesita guardrails** |

### Opción C (RECOMENDADA): Híbrido — Skill + MCP Bridge Inteligente
| Aspecto | Evaluación |
|---------|-----------|
| Cobertura | Total — 5-6 herramientas genéricas cubren toda la API |
| Type safety | Media — el SKILL.md enseña patrones, el agente valida contra docs |
| Mantenimiento | Bajo — herramientas estables, docs de API como referencias |
| Context window | Óptimo — SKILL.md ligero + carga progresiva de referencias |
| Escalabilidad | Excelente — agregar funciones = actualizar markdown |
| **Veredicto** | **Recomendado** — mejor balance entre flexibilidad y control |

**Arquitectura elegida: Opción C**

```
┌──────────────────────────────────────────────────────┐
│  Copilot Agent (VS Code)                             │
│                                                      │
│  1. Usuario pide: "Crea un pórtico 3x3 con cargas"  │
│            │                                         │
│  2. ┌──────▼──────────────────────────────────┐      │
│     │  SKILL.md (carga automática)            │      │
│     │  • Patrones de la API SAP2000           │      │
│     │  • Secuencia: connect → work → verify   │      │
│     │  • Refs a docs de API (on-demand)       │      │
│     └──────┬──────────────────────────────────┘      │
│            │                                         │
│  3. ┌──────▼──────────────────────────────────┐      │
│     │  search_api_docs (MCP Tool)             │      │
│     │  Busca funciones relevantes en API/     │      │
│     └──────┬──────────────────────────────────┘      │
│            │                                         │
│  4. ┌──────▼──────────────────────────────────┐      │
│     │  Agente genera script Python            │      │
│     │  (usando patrones del SKILL + docs)     │      │
│     └──────┬──────────────────────────────────┘      │
│            │                                         │
│  5. ┌──────▼──────────────────────────────────┐      │
│     │  run_sap_script (MCP Tool)              │      │
│     │  Ejecuta script → captura resultado     │      │
│     └──────┬──────────────────────────────────┘      │
│            │                                         │
│  6. ┌──────▼──────────────────────────────────┐      │
│     │  Agente verifica resultado              │      │
│     │  • return_code == 0? ✓                  │      │
│     │  • Valores esperados? ✓                 │      │
│     │  • Error? → corrige y re-ejecuta        │      │
│     └────────────────────────────────────────┘       │
│                                                      │
│  MCP Server (Python) ←── COM ──→ SAP2000 (local)    │
│  Tools: connect | disconnect | get_model_info        │
│         run_sap_script | execute_sap_function        │
│         search_api_docs | list_scripts | load_script │
└──────────────────────────────────────────────────────┘
```

### Flujo del Agente (ciclo principal)
```
buscar scripts existentes ──→ consultar docs API ──→ generar script
         ↑                                                │
         │                                    ejecutar via MCP
         │                                                │
         │                                    verificar resultado
         │                                                │
         └───── si error, corregir ───────────────────────┤
                                                          │
                                              si ok, guardar en scripts/
```

## Implementation Steps

### Step 1: Python MCP Server — Core Connection
**Files:**
- `mcp_server/server.py` — Entry point del MCP server
- `mcp_server/sap_bridge.py` — Wrapper de conexión COM local a SAP2000
- `mcp_server/requirements.txt` — Dependencias (comtypes, mcp-sdk)
- `mcp_server/__init__.py`

**What:**
Crear el servidor MCP con las herramientas `connect_sap2000` y `disconnect_sap2000`. El bridge Python usa `comtypes` para conectarse a SAP2000 vía COM local (ProgID: `CSI.SAP2000.API.SapObject`). Soporta dos modos: iniciar nueva instancia o attach a instancia existente. Incluir `get_model_info` para que el agente pueda verificar estado de conexión y modelo activo antes de ejecutar scripts.

**Herramientas de este step:**
```python
# connect_sap2000(program_path: str | None, attach_to_existing: bool) -> dict
# Conecta a SAP2000 local vía COM, devuelve status + versión + modelo activo

# disconnect_sap2000(save_model: bool) -> dict
# Cierra conexión limpiamente, opcionalmente guarda modelo

# get_model_info() -> dict
# Devuelve: connected, version, model_path, units, num_frames, num_points, etc.
# El agente usa esto para verificar estado antes/después de ejecutar scripts
```

**Testing:** Verificar conexión/desconexión a SAP2000 local, confirmar que `get_model_info` devuelve datos correctos con una instancia abierta.

---

### Step 2: Generic Function Executor
**Files:**
- `mcp_server/sap_executor.py` — Motor de ejecución genérica de funciones
- `mcp_server/server.py` (update) — Registrar nueva herramienta

**What:**
Implementar `execute_sap_function` — la herramienta central. Recibe un path de API (ej: `"SapModel.FrameObj.AddByCoord"`) y parámetros como lista, navega la jerarquía de objetos COM, ejecuta la función, y devuelve el resultado. Implementar manejo de: valores de retorno (0=success), parámetros ByRef (output params que SAP2000 modifica), y arrays dinámicos.

**Herramienta:**
```python
# execute_sap_function(
#     function_path: str,       # "SapModel.FrameObj.AddByCoord"
#     args: list[any],          # [0, 0, 0, 0, 0, 10, "", "R1", "1"]
#     description: str          # "Add frame from (0,0,0) to (0,0,10)"
# ) -> dict
# Devuelve: {success, return_code, result, output_params, description}
```

**Testing:** Ejecutar secuencia básica: `InitializeNewModel` → `File.NewBlank` → `FrameObj.AddByCoord` → verificar con `FrameObj.Count`.

---

### Step 3: Script Runner
**Files:**
- `mcp_server/sap_executor.py` (update) — Agregar ejecución de scripts
- `mcp_server/server.py` (update) — Registrar herramienta

**What:**
Implementar `run_sap_script` — la herramienta principal del flujo. El agente genera scripts Python completos basándose en los docs de la API, y esta herramienta los ejecuta contra SAP2000. El script recibe `SapModel` y `SapObject` como variables pre-inyectadas. Sandbox estricto: solo operaciones SAP permitidas.

**Restricciones del sandbox (solo operaciones SAP):**
- **Permitidos:** `math`, `json`, `datetime`, `decimal`, `fractions`, `collections`, `itertools`, `functools`, `typing`
- **Bloqueados:** `os`, `subprocess`, `sys`, `shutil`, `pathlib`, `socket`, `http`, `urllib`, `importlib`, `ctypes`, `pickle`
- **Sin acceso a filesystem:** No `open()`, no lectura/escritura de archivos
- **Timeout:** máximo 120s (análisis pueden tardar)

**Herramienta:**
```python
# run_sap_script(
#     script: str,              # Código Python completo generado por el agente
#     description: str          # "Create portal frame 3x3 and assign loads"
#     save_as: str | None       # Nombre para guardar en scripts/ (ej: "create_portal_3x3")
# ) -> dict
# Devuelve: {success, stdout, stderr, result: dict, execution_time_s, saved_path}
# Variables pre-inyectadas: SapModel, SapObject, result (dict para output)
#
# Si save_as se proporciona y el script ejecuta exitosamente:
#   → Se guarda en scripts/{save_as}.py con metadata (fecha, descripción, resultado)
#   → El agente puede reutilizarlo después con list_scripts / load_script
#
# Flujo del agente:
# 1. Genera script basándose en docs API
# 2. Ejecuta con run_sap_script
# 3. Lee resultado → si error, corrige script y reintenta
# 4. Si ok, guarda el script funcional para reutilización
# 5. Reporta resultado al usuario
```

**Testing:** Ejecutar el Example 1-001 (verificación) como script Python completo, comparar resultados con valores de referencia.

---

### Step 4: Script Library — Gestión y Reutilización
**Files:**
- `mcp_server/script_library.py` — Motor de almacenamiento y búsqueda de scripts
- `mcp_server/server.py` (update) — Registrar herramientas
- `scripts/` — Carpeta raíz donde se almacenan scripts guardados
- `scripts/README.md` — Índice auto-generado de scripts disponibles

**What:**
Implementar el sistema de persistencia de scripts. Cuando un script se ejecuta exitosamente y el agente proporciona `save_as`, se guarda en `scripts/` con metadata embebida. Implementar dos herramientas de gestión: `list_scripts` para explorar la biblioteca y `load_script` para cargar uno existente.

**Estructura de `scripts/`:**
```
scripts/
├── README.md                          # Índice auto-generado
├── create_portal_frame_3x3.py         # Script guardado
├── assign_seismic_loads_asce716.py
├── extract_joint_displacements.py
└── run_analysis_and_verify.py
```

**Formato de script guardado:**
```python
# ─── SAP2000 Script ───────────────────────────────────────
# Name:        create_portal_frame_3x3
# Description: Create a 3-story 3-bay portal frame with dead and live loads
# Created:     2026-03-19 14:30:00
# Status:      ✓ Verified (executed successfully)
# Result:      {"frames": 12, "joints": 16, "return_code": 0}
# ──────────────────────────────────────────────────────────

# SapModel y SapObject están pre-inyectados
ret = SapModel.InitializeNewModel()
ret = SapModel.File.New2DFrame(...)
# ... resto del script
result["frames"] = SapModel.FrameObj.Count()[1]
```

**Herramientas:**
```python
# list_scripts(
#     query: str | None,        # Búsqueda por nombre/descripción
#     tag: str | None            # Filtrar por tag ("loads", "analysis", "results")
# ) -> list[dict]
# Devuelve: [{name, description, created, status, tags, path}]

# load_script(
#     name: str                  # Nombre del script (sin .py)
# ) -> dict
# Devuelve: {name, description, script_code, metadata}
# El agente puede cargar un script existente, modificarlo, y re-ejecutarlo
```

**Flujo de reutilización del agente:**
1. Usuario pide algo similar a un script existente
2. Agente usa `list_scripts` para buscar scripts relevantes
3. Carga el script con `load_script`
4. Lo modifica según la nueva necesidad
5. Ejecuta con `run_sap_script` y guarda la nueva versión

**Testing:** Ejecutar un script, guardarlo con `save_as`. Verificar que aparece en `list_scripts`. Cargarlo con `load_script`, modificar un parámetro, re-ejecutar.

---

### Step 5: API Documentation Search Tool
**Files:**
- `mcp_server/doc_search.py` — Motor de búsqueda en docs de API
- `mcp_server/server.py` (update) — Registrar herramienta

**What:**
Implementar `search_api_docs` que busca en los archivos markdown de `API/` por keyword, categoría, o descripción de funcionalidad. Devuelve snippets relevantes con la firma de la función, parámetros, y ejemplo de uso. Esto permite al agente encontrar la función correcta antes de ejecutarla.

**Herramienta:**
```python
# search_api_docs(
#     query: str,               # "how to add a frame object by coordinates"
#     category: str | None      # "Object_Model", "Load_Cases", etc.
# ) -> list[dict]
# Devuelve: [{file, function_name, signature, description, example_snippet}]
```

**Testing:** Buscar "add frame by coordinates" → debe retornar `FrameObj.AddByCoord`. Buscar "run analysis" → debe retornar `Analyze.RunAnalysis`.

---

### Step 6: SKILL.md — Conocimiento del Dominio
**Files:**
- `.github/skills/sap2000-api/SKILL.md` — Skill principal
- `.github/skills/sap2000-api/references/api-patterns.md` — Patrones de la API
- `.github/skills/sap2000-api/references/common-workflows.md` — Flujos comunes
- `.github/skills/sap2000-api/references/enum-reference.md` — Enumeraciones

**What:**
Crear el SKILL.md que enseña al agente el flujo de trabajo: **consultar docs → generar script → ejecutar → verificar**. El skill es la pieza clave que transforma a Copilot de un asistente genérico a un experto en la API de SAP2000.

Contenido del SKILL.md:
- **Flujo obligatorio:** Siempre buscar en docs antes de generar código, siempre verificar resultado después de ejecutar
- **Reutilización:** Antes de generar un script nuevo, buscar en `list_scripts` si ya existe uno similar para usarlo como base
- **Guardado:** Siempre guardar scripts exitosos con `save_as` para reutilización futura
- **Patrones de scripts:** Cómo estructurar scripts Python usando las variables pre-inyectadas (`SapModel`, `SapObject`, `result`)
- **Convenciones SAP2000:** Return codes (0=success), ByRef params, unit system, arrays 0-based
- **Manejo de errores:** Cómo interpretar return codes ≠ 0, errores COM comunes, y cómo corregir
- **Referencias progresivas:** Links a api-patterns.md, common-workflows.md, enum-reference.md para carga on-demand
- Los 24 archivos de API/ como documentación de referencia

**Estructura del SKILL.md:**
```yaml
---
name: sap2000-api
description: >-
  Create, execute, and verify SAP2000 API scripts via MCP bridge.
  Use when: writing SAP2000 scripts, creating structural models, assigning loads,
  running analysis, extracting results, debugging API errors, SAP2000 automation.
  Workflow: search API docs → check script library → generate Python script → execute via MCP → verify results → save script.
---
```

**Testing:** Invocar el skill con `/sap2000-api` en Copilot Chat, pedir "crea un pórtico simple con cargas" y verificar que el agente: busca scripts existentes, busca docs, genera script, ejecuta, verifica resultado, y guarda el script.

---

### Step 7: MCP Configuration + Integration
**Files:**
- `.vscode/mcp.json` — Configuración del MCP server para VS Code
- `mcp_server/README.md` — Documentación de instalación y uso
- `.github/copilot-instructions.md` (create/update) — Instrucciones globales

**What:**
Configurar VS Code para reconocer el MCP server local. Crear `mcp.json` apuntando al server Python con stdio transport. Agregar instrucciones globales en `copilot-instructions.md` indicando que el skill `sap2000-api` está disponible y que el agente debe usarlo para cualquier tarea relacionada con SAP2000.

Requisitos documentados:
- Windows (obligatorio — SAP2000 solo corre en Windows)
- Python 3.10+
- SAP2000 instalado localmente
- `comtypes` para interfaz COM
- `mcp` SDK para el servidor

**Testing:** Abrir VS Code, verificar que el MCP server se inicia automáticamente. Pedir a Copilot "Conéctate a SAP2000 y crea una viga simple" — debe usar el skill, buscar docs, generar script, ejecutar, y verificar.

---

### Step 8: End-to-End Workflow Test
**Files:**
- `examples/example_1001_verification.py` — Port del Example 1-001 como test
- `examples/simple_beam.py` — Ejemplo simple de viga
- `mcp_server/tests/test_bridge.py` — Tests unitarios del bridge

**What:**
Crear ejemplos end-to-end que validen el flujo completo: conexión → creación de modelo → asignación de cargas → análisis → extracción de resultados → comparación con valores esperados. Estos ejemplos se guardan automáticamente en `scripts/` como biblioteca inicial y sirven como tests de integración y referencia para el SKILL.md.

**Testing:** Ejecutar los ejemplos, verificar que los resultados coinciden con los valores de referencia del Example 1-001 de SAP2000. Confirmar que los scripts quedan guardados en `scripts/` y son listables/cargables.

## Notas Técnicas

### COM Interface en Python (comtypes)
```python
import comtypes.client

# Iniciar nueva instancia
helper = comtypes.client.CreateObject("SAP2000v1.Helper")
sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
sap_object.ApplicationStart()
sap_model = sap_object.SapModel

# O attach a instancia existente
sap_object = helper.GetObject("CSI.SAP2000.API.SapObject")
```

### Manejo de ByRef Parameters
SAP2000 usa ByRef para devolver arrays y valores. En Python/COM con `comtypes`:
```python
# Los parámetros ByRef se devuelven como parte de una tupla
ret, num_names, names = sap_model.FrameObj.GetNameList(0, [])
# ret = 0 (success), num_names = 3, names = ["1", "2", "3"]
```

### Sandbox del Script Runner
- **Solo operaciones SAP:** No filesystem, no network, no subprocess
- **Imports bloqueados:** `os`, `subprocess`, `sys`, `shutil`, `pathlib`, `socket`, `http`, `urllib`, `importlib`, `ctypes`, `pickle`
- **Imports permitidos:** `math`, `json`, `datetime`, `decimal`, `collections`, `itertools`, `functools`, `typing`
- **Timeout:** 120s máximo (análisis estructurales pueden tardar)
- **Variables pre-inyectadas:** `SapModel`, `SapObject`, `result` (dict para output)
- **Log:** Todas las operaciones ejecutadas se registran para depuración
