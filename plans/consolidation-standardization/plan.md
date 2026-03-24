# Consolidación y Estandarización de Documentación SAP2000

**Branch:** `refactor/consolidate-docs-and-agent`
**Description:** Reestructurar la documentación, eliminar duplicaciones, crear un agente formal `.agent.md`, y establecer una arquitectura clara de 3 capas.

## Situación Actual (Diagnóstico)

### Problemas detectados

| # | Problema | Impacto |
|---|---------|---------|
| 1 | **No existe `.agent.md`** — "SAP2000 Scripter" se menciona pero no está definido en el workspace | El agente no se carga automáticamente; depende de setup manual |
| 2 | **Duplicación crítica** — ByRef convention, wrapper priority rule, return codes aparecen en 3-4 lugares | Riesgo de inconsistencia al actualizar |
| 3 | **Dos workflows sin criterio de uso** — `workflow-script-creation.md` (500 líneas, español) vs `quick-reference-workflow.md` (80 líneas, inglés) | Confusión sobre cuál seguir |
| 4 | **SKILL.md es híbrido** — mezcla workflow (pasos 1-10), referencia API, convenciones y enums | Demasiado largo (550+ líneas), difícil de mantener |
| 5 | **copilot-instructions.md es superficial** — repite info de SKILL.md sin añadir valor | No funciona como router ni como referencia |
| 6 | **Enums dispersos** — aparecen en SKILL.md, enum-reference.md, api-patterns.md | No hay fuente única de verdad |
| 7 | **Config MCP oculta** — `.vscode/mcp.json` no documentado en ningún doc de usuario | Nuevos usuarios no saben cómo funciona |
| 8 | **Idioma mixto** — workflow largo en español, quick-reference en inglés | Inconsistencia |

### Estructura actual de archivos de documentación

```
.github/
  copilot-instructions.md          ← Router (75 líneas, superficial)
  skills/sap2000-api/
    SKILL.md                       ← TODO junto (550+ líneas)
    references/
      api-patterns.md              ← Patrones de código (200 líneas)
      enum-reference.md            ← Enums completo (160 líneas)
      common-workflows.md          ← 5 workflows (80 líneas)
      script-templates.md          ← Templates paramétricos (300+ líneas)
  agents/                          ← VACÍO
  prompts/
    structured-autonomy-*.md       ← Prompts genéricos (no SAP2000)
plans/
  workflow-script-creation.md      ← Workflow detallado (500 líneas, ES)
  quick-reference-workflow.md      ← Quick reference (80 líneas, EN)
```

## Goal

Establecer una **arquitectura de 3 capas** clara y sin duplicaciones:

```
CAPA 1: ROUTING     → copilot-instructions.md (¿qué herramienta uso?)
CAPA 2: AGENTES     → .agent.md (comportamiento + workflow embebido)
CAPA 3: REFERENCIA  → SKILL.md + references/ (datos, convenciones, patrones)
```

**Principio rector:** Cada pieza de información vive en UN solo lugar. Todo lo demás enlaza.

## Propuesta de Arquitectura

### Estructura objetivo

```
.github/
  copilot-instructions.md          ← CAPA 1: Router ligero
  agents/
    sap2000-scripter.agent.md      ← CAPA 2: Agente con workflow embebido
  skills/sap2000-api/
    SKILL.md                       ← CAPA 3: Solo referencia técnica
    references/
      api-patterns.md              ← (sin cambios)
      enum-reference.md            ← (consolidado: TODOS los enums aquí)
      common-workflows.md          ← (sin cambios)
      script-templates.md          ← (sin cambios)
      gui-generation.md            ← NUEVO: Phase 6 extraída aquí
plans/
  consolidation-standardization/
    plan.md                        ← Este archivo
  (workflow-script-creation.md)    ← ARCHIVADO o eliminado
  (quick-reference-workflow.md)    ← ARCHIVADO o eliminado
```

### Qué hace cada archivo

| Archivo | Responsabilidad | Tamaño objetivo |
|---------|----------------|-----------------|
| `copilot-instructions.md` | Router: cuándo usar qué, mapa de docs, config MCP | ~60 líneas |
| `sap2000-scripter.agent.md` | Agente formal: personalidad, workflow de 10 pasos, reglas críticas, cuándo cargar referencias | ~150 líneas |
| `SKILL.md` | Referencia pura: convenciones API, patrones de script, registry, templates de código | ~300 líneas |
| `references/gui-generation.md` | Guía completa de Phase 6 (GUI standalone) | ~100 líneas |

### Flujo de información

```
Usuario pide algo de SAP2000
        │
        ▼
copilot-instructions.md
  "Usa el agente SAP2000 Scripter o la skill sap2000-api"
        │
        ▼
sap2000-scripter.agent.md ← CARGADO AUTOMÁTICAMENTE
  ┌──────────────────────────────────┐
  │  WORKFLOW EMBEBIDO (10 pasos)    │
  │  1. connect                      │
  │  2. query registry               │
  │  3. load wrappers                │
  │  4. search scripts               │
  │  5. search API docs (fallback)   │
  │  6. generate script              │
  │  7. execute                      │
  │  8. verify                       │
  │  9. save                         │
  │  10. register + offer GUI        │
  │                                  │
  │  REGLAS CRÍTICAS (inline)        │
  │  • Wrapper priority rule         │
  │  • ByRef convention              │
  │  • Return code checks            │
  │                                  │
  │  REFERENCIAS BAJO DEMANDA        │
  │  → Lee SKILL.md para patrones    │
  │  → Lee enum-reference.md si      │
  │    necesitas enums               │
  │  → Lee gui-generation.md si      │
  │    usuario quiere GUI            │
  └──────────────────────────────────┘
        │
        ▼ (cuando necesita datos)
SKILL.md (referencia)
  • Convenciones COM/ByRef detalladas
  • Templates de scripts
  • Function registry usage
  • Tabla de errores comunes
```

## Valor agregado vs. situación actual

| Aspecto | Antes | Después |
|---------|-------|---------|
| Agente SAP2000 | No existe formalmente | `.agent.md` con personalidad, tools, workflow |
| Workflow | 2 archivos separados, sin criterio | Embebido en el agente (single source of truth) |
| Duplicaciones | ByRef, wrapper rule en 3-4 lugares | Cada concepto en 1 lugar, el resto enlaza |
| Onboarding | Hay que leer 4+ archivos | `copilot-instructions.md` es un mapa claro |
| Enums | Dispersos en SKILL.md + enum-reference | Solo en `enum-reference.md` |
| GUI generation | Mencionada pero no documentada | `gui-generation.md` dedicado |
| Config MCP | Oculta en `.vscode/mcp.json` | Documentada en copilot-instructions |
| Idioma | Español + Inglés mezclados | Estandarizado (propuesta: español, tu preferencia) |

## Decisiones Tomadas

| # | Decisión | Valor |
|---|----------|-------|
| 1 | **Idioma de documentación** | **Español** (unificado) |
| 2 | **Workflows redundantes** | **Archivar** a `plans/_archive/` (no eliminar) |
| 3 | **Modelo del agente** | **Claude Sonnet 4.6** (balance velocidad/capacidad) |
| 4 | **Prompts genéricos SA** | **Mantener como están** (útiles para futuros desarrollos del MCP server) |
| 5 | **Nombre del agente** | **SAP2000 Scripter** (sin cambios) |
| 6 | **Capacidad de research** | **Opción B**: Research integrado en el agente con `runSubagent` (ver [research-capability-analysis.md](research-capability-analysis.md)) |

## Implementation Steps

### Step 1: Crear el agente formal `sap2000-scripter.agent.md`
**Files:** `.github/agents/sap2000-scripter.agent.md`

**What:** Crear el archivo `.agent.md` con:

**A. YAML frontmatter:**
- `name: sap2000-scripter`
- `description:` Experto en API de SAP2000, genera y ejecuta scripts de automatización estructural
- `model: claude-sonnet-4.6`
- `tools:` Restringido a `mcp_sap2000_*` (todos los tools del MCP server)

**B. Personalidad:**
- Experto en ingeniería estructural y API de SAP2000
- Metódico: verifica cada paso antes de continuar
- Enfocado en código verificable y reproducible
- Educativo: explica decisiones técnicas cuando es relevante

**C. Workflow embebido (10 pasos):**
Consolidar contenido de `workflow-script-creation.md` + `quick-reference-workflow.md` + SKILL.md:
1. **Connect** — Verificar conexión con `get_model_info`
2. **Query registry** — Buscar funciones verificadas
3. **Load wrappers** — Cargar scripts de referencia si existen
4. **Search scripts** — Buscar scripts similares en la biblioteca
5. **Search API docs** — Solo como fallback para funciones no verificadas
6. **Generate script** — Escribir código siguiendo patrones establecidos
7. **Execute** — Ejecutar con `run_sap_script`
8. **Verify** — Analizar resultados, corregir errores si es necesario
9. **Save** — Guardar script verificado en la biblioteca
10. **Register + offer GUI** — Registrar funciones nuevas, ofrecer generación de GUI

**D. Reglas críticas inline (5 reglas):**
- ✅ **Wrapper priority rule**: Wrappers verificados son la única fuente de verdad
- ✅ **ByRef convention**: Outputs primero, return code SIEMPRE al final `raw[-1]`
- ✅ **Return code checks**: Always `assert ret == 0`
- ✅ **sap_temp_dir**: Nunca hardcodear paths, usar `sap_temp_dir` para `File.Save()`
- ✅ **result dict**: Escribir valores verificables a `result` para testing

**E. Referencias bajo demanda:**
- Para patrones de código → leer `SKILL.md`
- Para enums → leer `references/enum-reference.md`
- Para GUI generation → leer `references/gui-generation.md`

**Testing:** Invocar `@sap2000-scripter` en VS Code Chat y verificar que se activa con el workflow correcto

---

### Step 2: Agregar capacidad de research exhaustivo al agente
**Files:** `.github/agents/sap2000-scripter.agent.md` (editar)

**What:** Agregar **Paso 0 condicional** al workflow del agente:

**A. Criterios de detección de script complejo:**
Activar research si el request tiene ≥3 de estos indicadores:
- Keywords: "multi", "parametric", "batch", "optimization", "mega", "complex"
- Menciona >8 tipos de elementos diferentes (frames + areas + joints + links + constraints + ...)
- Menciona análisis no lineal / multi-etapa / time-history / pushover
- Menciona >10 parámetros configurables
- Referencias a scripts existentes complejos (MEGA_MODELO, placabase_parametric, etc.)

**B. Instrucciones de research:**
Si se detecta complejidad, ejecutar ANTES del Paso 1:

```markdown
## Paso 0: Research Exhaustivo (Scripts Complejos)

Invocar `runSubagent` con agente "Explore" (thoroughness=thorough):

**Prompt para el subagent:**
"""
Realiza research exhaustivo para el siguiente script SAP2000: [descripción del usuario]

1. **Semantic search:** Busca scripts existentes relacionados con: [keywords extraídos]
2. **Query registry:** Identifica funciones SAP2000 necesarias y su estado de verificación
3. **Analyze dependencies:** Propone tabla de tareas con dependencias
4. **Find patterns:** Busca patrones reutilizables en scripts similares
5. **Identify gaps:** Lista funciones que NO tienen wrapper verificado

Retorna:
- Lista de scripts similares encontrados (con nombres y relevancia)
- Funciones del registry necesarias (✅ verificadas / ⚠️ no verificadas)
- Tabla de tareas propuesta con dependencias
- Patterns/helpers reutilizables de otros scripts
- Riesgos y complejidades detectadas
"""

**Uso de findings:**
- Findings disponibles durante todo el workflow (Pasos 1-10)
- Usar tabla de tareas como guía para implementación incremental
- Priorizar funciones verificadas, marcar no verificadas para extra cuidado
```

**C. Nota sobre extensión futura:**
Incluir comentario en el agente:
```markdown
> 💡 **Nota:** Para scripts mega-complejos (>500 líneas, >15 tareas), considera
> usar `/sap2000-plan` (si está disponible) para generar un plan persistido y
> revisable antes de la implementación.
```

**Testing:** Probar con script medio-complejo (pórtico sísmico) y verificar que el research se activa correctamente

---

### Step 3: Reestructurar SKILL.md como referencia pura
**Files:** `.github/skills/sap2000-api/SKILL.md`

**What:** Transformar SKILL.md de "workflow + referencia" a **solo referencia**:

**A. Remover (ahora vive en el agente):**
- El workflow de 10 pasos (paso a paso)
- Las instrucciones de personalidad/comportamiento
- El paso 0 de research (ahora en el agente)

**B. Mantener y consolidar:**
- **Convenciones API detalladas:**
  - ByRef convention con múltiples ejemplos
  - Return code checks con patterns
  - Unit system (referencia a enum-reference.md, no duplicar tabla)
  - Arrays (0-based, COM marshalling)
- **Script patterns:**
  - Pre-injected variables (`SapModel`, `SapObject`, `result`, `sap_temp_dir`)
  - Template básico (initialize → materials → sections → geometry)
  - Results extraction template (análisis + ByRef outputs)
- **Function registry:**
  - Cómo usar `query_function_registry` con ejemplos
  - Estructura de entries en el registry
  - Wrapper scripts: qué son y por qué son autoridad
- **Tabla de errores comunes** (7 tipos con fixes)
- **Object hierarchy diagram** (SapObject → SapModel)

**C. Reemplazar enums inline:**
- Donde hay tablas de enums (units, material types, load patterns) → reemplazar con:
  ```markdown
  Ver [enum-reference.md](references/enum-reference.md) para listas completas de enumeraciones.
  ```

**D. Idioma:**
- Traducir todas las secciones a **español**
- Mantener nombres de funciones/variables en inglés (API es en inglés)

**Testing:** Verificar que SKILL.md se carga correctamente y que todas las referencias a enums/GUI apuntan a los archivos correctos

---

### Step 4: Crear `gui-generation.md` y consolidar enums
**Files:** 
- `.github/skills/sap2000-api/references/gui-generation.md` (nuevo)
- `.github/skills/sap2000-api/references/enum-reference.md` (actualizar)

**What:**

**A. Crear `gui-generation.md`:**
Extraer de `workflow-script-creation.md` la **Fase 6 completa** y expandir:
- Cuándo ofrecer GUI (después de script verificado)
- Estructura de archivos: `scripts/{nombre}/gui_{nombre}.py` + `backend_{nombre}.py`
- Backend pattern:
  - Clase `SapConnection` (connect/disconnect COM directo)
  - Dataclass `Config` (parámetros de input)
  - Clase `Backend` con método `run(config) → dict`
- GUI pattern:
  - Workers async (QThread) para connect/run/disconnect
  - MainWindow con inputs, log, botones
  - Import del backend: `from backend_xname import ...`
- Templates: enlazar a `scripts/templates/backend_template.py` y `gui_template.py`
- Ejemplos: enlazar a `scripts/placabase/` y `scripts/ring_areas/`
- Idioma: **español**

**B. Consolidar enums en `enum-reference.md`:**
- Verificar que TODOS los enums están presentes:
  - eUnits (12 valores)
  - eMatType (7 valores)
  - eLoadPatternType (13 valores)
  - e2DFrameType (3 valores)
  - e3DFrameType (4 valores)
  - eLoadCaseType (12 valores)
  - eItemTypeElm (4 valores)
  - eConstraintType (7 valores)
  - eCombType (5 valores)
- Mover cualquier enum que esté en SKILL.md pero no en enum-reference.md
- Formato: tablas markdown con valor numérico y nombre
- Idioma: **español** para descripciones, nombres de enums en inglés

**Testing:** 
- `gui-generation.md` tiene workflow completo y enlaza correctamente a templates
- `enum-reference.md` es la única fuente de enums (ningún otro archivo los duplica)

---

### Step 5: Reescribir `copilot-instructions.md` como router
**Files:** `.github/copilot-instructions.md`

**What:** Reescribir completamente como documento ligero (~80 líneas):

**Estructura:**

```markdown
# SAP2000 API Skill - Instrucciones de Copilot

## ¿Qué es este workspace?
Framework para automatizar SAP2000 mediante scripts Python + MCP bridge.

## 📚 Mapa de Documentación

| Documento | Para qué |
|-----------|----------|
| `.github/agents/sap2000-scripter.agent.md` | Workflow del agente (usa `@sap2000-scripter`) |
| `.github/skills/sap2000-api/SKILL.md` | Referencia técnica API |
| `.github/skills/sap2000-api/references/` | Patrones, enums, workflows, templates |
| `scripts/wrappers/` | Funciones verificadas (referencia de firmas) |
| `scripts/templates/` | Templates para backend/GUI |
| `scripts/registry.json` | Registry de funciones verificadas |

## 🔧 Configuración MCP

El servidor MCP se autoconfigura via `.vscode/mcp.json`:
- Python venv: `.venv/Scripts/python.exe`
- Script: `mcp_server/server.py`
- Tools expuestos: 11 (connect, execute, run_script, registry, etc.)

## 🤖 Cuándo usar qué

### Agente SAP2000 Scripter (`@sap2000-scripter`)
**Usar para:**
- Generar scripts de SAP2000 (marcos, áreas, análisis)
- Automatización estructural
- Workflow completo: research → código → ejecución → verificación

**Capacidades:**
- Research automático para scripts complejos
- Consulta inteligente al registry de funciones
- Generación iterativa con testing incremental
- Oferta de GUI standalone al finalizar

### Skill sap2000-api (attachment)
**Usar para:**
- Consultas rápidas sobre convenciones API
- Patrones de código específicos
- Referencia de enumeraciones

## 📋 Requisitos del Sistema

- Windows OS (SAP2000 solo corre en Windows)
- Python 3.10+
- SAP2000 instalado localmente
- Paquetes: `comtypes`, `mcp[cli]` (ver `mcp_server/requirements.txt`)

## 🚀 Quick Start

1. Activar venv: `.venv/Scripts/Activate.ps1`
2. Invocar agente: `@sap2000-scripter genera viga simple con carga muerta`
3. El agente maneja el resto (conexión, registry, generación, ejecución)
```

**Idioma:** **Español** completo

**Testing:** Nuevo usuario debe poder leer este archivo y entender inmediatamente:
- Qué es el workspace
- Dónde buscar información específica
- Cómo empezar a usar el agente

---

### Step 6: Archivar workflows redundantes
**Files:** 
- `plans/workflow-script-creation.md`
- `plans/quick-reference-workflow.md`

**What:**
1. Crear directorio `plans/_archive/`
2. Mover ambos archivos al archive:
   - `plans/_archive/workflow-script-creation.md`
   - `plans/_archive/workflow-script-creation-ORIGINAL.md` (backup)
   - `plans/_archive/quick-reference-workflow.md`
3. Agregar `plans/_archive/README.md` explicando:
   ```markdown
   # Archive - Workflows Originales
   
   Estos workflows fueron consolidados en el agente `sap2000-scripter.agent.md`.
   
   Se mantienen aquí como referencia histórica.
   
   **No usar estos archivos** — el workflow actual vive en el agente.
   ```
4. Buscar y actualizar cualquier enlace roto en otros documentos

**Testing:** 
- Verificar que no hay enlaces rotos en la documentación activa
- `plans/_archive/` contiene los archivos originales con README explicativo

---

## Orden de Implementación Recomendado

```
Step 2 (research) → Step 1 (agente completo) → Step 3 (SKILL.md) → 
Step 4 (gui-gen + enums) → Step 5 (router) → Step 6 (archive)
```

**Razón:** Implementar research primero, luego crear el agente con todo (workflow + research). Después limpiar referencias.
