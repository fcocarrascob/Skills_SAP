# SAP2000 Script Generator Agent

**Branch:** `feat/sap2000-script-agent`
**Description:** Agente especializado que guía al usuario paso a paso para generar, ejecutar y verificar scripts de SAP2000 a través del MCP bridge.

## Goal

Crear un custom agent de VS Code (`.agent.md`) cuya función exclusiva sea ayudar al usuario a generar scripts de SAP2000 de forma interactiva. El usuario describe en lenguaje natural lo que quiere modelar (p.ej. "parametriza una placa rectangular con orificios" o "dibuja una circunferencia y conecta puntos con placas") y el agente:

1. Le hace preguntas de clarificación (unidades, dimensiones, materiales, condiciones de borde)
2. Busca funciones verificadas en el registry y wrappers existentes
3. Genera un script Python limpio y simple (estilo `example_1001_simple_beam.py`)
4. Lo ejecuta contra SAP2000 vía `run_sap_script`
5. Verifica el resultado y lo muestra al usuario
6. Guarda el script en la librería si el usuario lo aprueba

## Implementation Steps

### Step 1: Crear el Agent File principal
**Files:** `.github/agents/sap2000-scripter.agent.md`
**What:** Crear el archivo `.agent.md` con:
- **Frontmatter YAML:** nombre, descripción, tools restringidos al MCP de SAP2000 (`sap2000/*`) más herramientas de lectura (`search/codebase`), y el modelo preferido.
- **Body (instrucciones):** Workflow interactivo completo que el agente debe seguir:
  1. **Fase de Clarificación** — Antes de escribir código, el agente SIEMPRE pregunta al usuario los datos que faltan: sistema de unidades, dimensiones clave, materiales, tipo de sección, condiciones de apoyo, cargas. Presenta las preguntas como checklist conciso.
  2. **Fase de Búsqueda** — Consulta el function registry (`query_function_registry`) y wrappers (`load_script`) para todas las funciones API que necesitará. Si hay scripts similares en la librería (`list_scripts`), los carga como referencia.
  3. **Fase de Generación** — Produce un script Python completo siguiendo las convenciones del SKILL.md: variables pre-inyectadas (`SapModel`, `result`, `sap_temp_dir`), asserts en cada llamada, output a `result` dict, comentarios seccionales claros. El script debe ser autocontenido y legible.
  4. **Fase de Ejecución** — Ejecuta el script con `run_sap_script`. Si falla, analiza el error, corrige y reintenta (máximo 3 intentos).
  5. **Fase de Verificación** — Presenta al usuario un resumen de resultados: conteo de objetos creados, coordenadas clave, propiedades asignadas. Si aplica, compara contra valores de referencia.
  6. **Fase de Guardado** — Pregunta al usuario si quiere guardar el script. Si sí, lo guarda con `save_as` y nombre descriptivo.
- **Referencia al SKILL.md** — Link markdown a la skill existente para heredar convenciones técnicas (ByRef patterns, wrapper priority rule, enums) sin duplicarlas.
- **Handoff** — Handoff opcional al agente por defecto para tareas que no son de scripting SAP2000.

**Testing:** 
- Verificar que el agente aparece en el dropdown de agentes de VS Code.
- Seleccionar el agente y enviarle un prompt simple como "Crea una viga simplemente apoyada de 6m con carga puntual". Confirmar que el agente sigue el workflow: pregunta → busca → genera → ejecuta → verifica.

### Step 2: Crear templates de referencia para el agente
**Files:** `.github/skills/sap2000-api/references/script-templates.md`
**What:** Crear un archivo de templates que el agente puede referenciar internamente. Incluye plantillas parametrizadas para los escenarios más comunes:
- **Template: Geometría por coordenadas** — Creación de puntos, frames y áreas usando loops con parámetros (ej. placa rectangular parametrizada por filas/columnas de puntos).
- **Template: Geometría circular** — Generación de puntos en circunferencia usando `math.cos`/`math.sin`, conexión con frames o áreas.
- **Template: Placa con orificios** — Patrón de área con substracción de regiones (dividir área y eliminar sub-áreas, o generar mesh con huecos).
- **Template: Modelo completo mínimo** — Secuencia canónica: init → units → material → section → geometry → supports → loads → save → result.

Cada template incluye:
- Parámetros que el agente debe pedir al usuario (con defaults sugeridos)
- Código Python con placeholders `{param}` documentados
- Ejemplo de `result` dict esperado

**Testing:**
- Leer el archivo desde el agente y verificar que los templates son sintácticamente válidos.
- Usar un template para generar un script concreto y ejecutarlo con `run_sap_script`.

### Step 3: Agregar el agente al index de AGENTS.md y actualizar copilot-instructions
**Files:** `.github/copilot-instructions.md`
**What:** 
- Actualizar `copilot-instructions.md` para mencionar la existencia del agente `sap2000-scripter` y cuándo usarlo: "Para generar scripts de SAP2000 de forma interactiva, usa el agente SAP2000 Scripter".
- Asegurar que el agente hereda las instrucciones globales del workspace.

**Testing:**
- Verificar que Copilot en modo normal sugiere usar el agente `sap2000-scripter` cuando el usuario pide generar un script de SAP2000.
- Confirmar que el agente carga correctamente las instrucciones del SKILL.md referenciado.

### Step 4: Test end-to-end con 3 escenarios representativos
**Files:** `scripts/example_2001_parametric_plate.py`, `scripts/example_2002_circular_ring.py`, `scripts/example_2003_plate_with_holes.py`
**What:** Ejecutar manualmente el agente con tres prompts representativos y guardar los scripts resultantes como ejemplos verificados:
1. **"Genera un script que cree una placa rectangular de 4x6m dividida en una malla de 4x6 elementos"** — Valida: AreaObj.AddByCoord, EditArea.Divide, PropArea.SetShell_1
2. **"Genera un script que dibuje dos circunferencias (R=5m y R=3m) y conecte sus puntos con placas triangulares"** — Valida: math.cos/sin, PointObj.AddCartesian, AreaObj.AddByPoint (3 puntos)
3. **"Genera un script para una placa con un orificio circular centrado"** — Valida: combinación de geometría rectangular + circular, meshing strategy

Cada script resultante debe:
- Seguir el estilo de `example_1001_simple_beam.py`
- Escribir a `result` dict con conteos y verificaciones
- Ejecutar exitosamente vía `run_sap_script`

**Testing:**
- Los 3 scripts ejecutan exitosamente en SAP2000
- Los `result` dicts contienen los campos esperados (conteos de objetos, coordenadas)
- Los scripts son legibles y están bien comentados
