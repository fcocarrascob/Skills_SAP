# Database Tables — Colección completa de scripts verificados

**Branch:** `feature/database-tables-wrappers`
**Description:** Crear carpeta `scripts/database_tables/` con wrappers verificados, backend y GUI para las 37 funciones de la API DatabaseTables de SAP2000.

## Goal

Cubrir el 100% de la superficie API de `SapModel.DatabaseTables` (37 funciones) con wrapper scripts verificados (18 archivos — uno consolidado para Display Selection), un backend reutilizable y GUI standalone. Actualmente no existe ningún wrapper ni registro para DatabaseTables — es territorio virgen.

## Inventario API completo (37 funciones)

| # | Función | Grupo | Prioridad |
|---|---------|-------|-----------|
| 1 | `GetAllTables` | Metadata | Alta |
| 2 | `GetAvailableTables` | Metadata | Alta |
| 3 | `GetAllFieldsInTable` | Metadata | Alta |
| 4 | `GetObsoleteTableKeyList` | Metadata | Baja |
| 5 | `GetTableForEditingArray` | Core Array R/W | Alta |
| 6 | `SetTableForEditingArray` | Core Array R/W | Alta |
| 7 | `ApplyEditedTables` | Core Array R/W | Alta |
| 8 | `CancelTableEditing` | Core Array R/W | Media |
| 9 | `GetTableForDisplayArray` | Core Array R/W | Alta |
| 10 | `GetTableForDisplayCSVFile` | CSV/String/XML | Media |
| 11 | `GetTableForDisplayCSVString` | CSV/String/XML | Media |
| 12 | `GetTableForDisplayXMLString` | CSV/String/XML | Media |
| 13 | `GetTableForEditingCSVFile` | CSV/String/XML | Media |
| 14 | `GetTableForEditingCSVString` | CSV/String/XML | Media |
| 15 | `SetTableForEditingCSVFile` | CSV/String/XML | Media |
| 16 | `SetTableForEditingCSVString` | CSV/String/XML | Media |
| 17 | `GetLoadCasesSelectedForDisplay` | Display Selection | Baja |
| 18 | `SetLoadCasesSelectedForDisplay` | Display Selection | Baja |
| 19 | `GetLoadCombinationsSelectedForDisplay` | Display Selection | Baja |
| 20 | `SetLoadCombinationsSelectedForDisplay` | Display Selection | Baja |
| 21 | `GetLoadPatternsSelectedForDisplay` | Display Selection | Baja |
| 22 | `SetLoadPatternsSelectedForDisplay` | Display Selection | Baja |
| 23 | `GetElementVirtualWorkNamedSetsSelectedForDisplay` | Display Selection | Baja |
| 24 | `SetElementVirtualWorkNamedSetsSelectedForDisplay` | Display Selection | Baja |
| 25 | `GetGeneralizedDisplacementsSelectedForDisplay` | Display Selection | Baja |
| 26 | `SetGeneralizedDisplacementsSelectedForDisplay` | Display Selection | Baja |
| 27 | `GetJointResponseSpectraNamedSetsSelectedForDisplay` | Display Selection | Baja |
| 28 | `SetJointResponseSpectraNamedSetsSelectedForDisplay` | Display Selection | Baja |
| 29 | `GetPlotFunctionTracesNamedSetsSelectedForDisplay` | Display Selection | Baja |
| 30 | `SetPlotFunctionTracesNamedSetsSelectedForDisplay` | Display Selection | Baja |
| 31 | `GetPushoverNamedSetsSelectedForDisplay` | Display Selection | Baja |
| 32 | `SetPushoverNamedSetsSelectedForDisplay` | Display Selection | Baja |
| 33 | `GetSectionCutsSelectedForDisplay` | Display Selection | Baja |
| 34 | `SetSectionCutsSelectedForDisplay` | Display Selection | Baja |
| 35 | `GetTableOutputOptionsForDisplay` | Display Selection | Baja |
| 36 | `SetTableOutputOptionsForDisplay` | Display Selection | Baja |
| 37 | `ShowTablesInExcel` | Utility | Baja |

## Estructura de carpeta propuesta

```
scripts/database_tables/
├── README.md                        # Documentación del módulo
├── backend_database_tables.py       # Backend reutilizable (clase DatabaseTablesBackend)
└── gui_database_tables.py           # GUI standalone PySide6

scripts/wrappers/                    # 18 wrappers nuevos (naming: func_DatabaseTables_*.py)
├── func_DatabaseTables_GetAllTables.py
├── func_DatabaseTables_GetAvailableTables.py
├── func_DatabaseTables_GetAllFieldsInTable.py
├── func_DatabaseTables_GetTableForEditingArray.py
├── func_DatabaseTables_SetTableForEditingArray.py
├── func_DatabaseTables_ApplyEditedTables.py
├── func_DatabaseTables_CancelTableEditing.py
├── func_DatabaseTables_GetTableForDisplayArray.py
├── func_DatabaseTables_GetTableForDisplayCSVFile.py
├── func_DatabaseTables_GetTableForDisplayCSVString.py
├── func_DatabaseTables_GetTableForDisplayXMLString.py
├── func_DatabaseTables_GetTableForEditingCSVFile.py
├── func_DatabaseTables_GetTableForEditingCSVString.py
├── func_DatabaseTables_SetTableForEditingCSVFile.py
├── func_DatabaseTables_SetTableForEditingCSVString.py
├── func_DatabaseTables_DisplaySelection_Consolidated.py     # Wrapper consolidado (testea 20 funciones)
├── func_DatabaseTables_GetObsoleteTableKeyList.py
└── func_DatabaseTables_ShowTablesInExcel.py

scripts/registry.json                # +37 entradas nuevas
```

## Implementation Steps

### Step 1: Wrappers de Metadata (fundacionales) — COMMIT CHECKPOINT
**Files:** `scripts/wrappers/func_DatabaseTables_GetAllTables.py`, `func_DatabaseTables_GetAvailableTables.py`, `func_DatabaseTables_GetAllFieldsInTable.py`, `func_DatabaseTables_GetObsoleteTableKeyList.py`, `scripts/registry.json`
**What:** Crear 4 wrappers para las funciones de enumeración y metadatos de tablas. Son prerequisito para todo lo demás — permiten descubrir qué tablas existen, sus campos y tipos de importación. Cada wrapper sigue la convención estándar: setup mínimo → llamada COM → extracción ByRef → assert → result dict. Registrar las 4 funciones en `registry.json`.
**Firmas clave:**
- `GetAllTables()` → `[NumberTables, TableKey[], TableName[], ImportType[], IsEmpty[], ret_code]`
- `GetAvailableTables()` → `[NumberTables, TableKey[], TableName[], ImportType[], ret_code]`
- `GetAllFieldsInTable(TableKey)` → `[TableVersion, NumberFields, FieldKey[], FieldName[], Description[], UnitsString[], IsImportable[], ret_code]`
- `GetObsoleteTableKeyList()` → `[NumberTableKeys, TableKeyList[], NotesList[], ret_code]`
**Testing:** Ejecutar cada wrapper via `run_sap_script`. Verificar que `ret_code == 0` y que los arrays retornados contienen datos válidos (nombres de tablas conocidas como "Material Properties", etc.).
**Commit:** `feat(db-tables): add metadata wrappers (GetAllTables, GetAvailableTables, GetAllFieldsInTable, GetObsoleteTableKeyList)`

### Step 2: Wrappers Core Array R/W (flujo principal de lectura/escritura) — COMMIT CHECKPOINT
**Files:** `scripts/wrappers/func_DatabaseTables_GetTableForEditingArray.py`, `func_DatabaseTables_SetTableForEditingArray.py`, `func_DatabaseTables_GetTableForDisplayArray.py`, `func_DatabaseTables_ApplyEditedTables.py`, `func_DatabaseTables_CancelTableEditing.py`, `scripts/registry.json`
**What:** Crear 5 wrappers para el flujo central: leer tabla (GetTableForEditingArray/GetTableForDisplayArray) → modificar datos → escribir tabla (SetTableForEditingArray) → aplicar cambios (ApplyEditedTables). CancelTableEditing como rollback. Registrar las 5 funciones en `registry.json`.
**Firmas clave:**
- `GetTableForEditingArray(TableKey, GroupName, ...)` → `[TableVersion, FieldKeysIncluded[], NumberRecords, TableData[], ret_code]`
- `SetTableForEditingArray(TableKey, TableVersion, FieldKeysIncluded[], NumberRecords, TableData[])` → `[ret_code]` (ByRef en TableVersion, FieldKeysIncluded, TableData)
- `GetTableForDisplayArray(TableKey, FieldKeyList[], GroupName, ...)` → `[TableVersion, FieldKeysIncluded[], NumberRecords, TableData[], ret_code]`
- `ApplyEditedTables(FillImportLog, ...)` → `[NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog, ret_code]`
- `CancelTableEditing()` → `ret_code`
**Testing:** Workflow completo: (1) GetTableForEditingArray en tabla conocida → verificar datos, (2) SetTableForEditingArray modificando un valor → ApplyEditedTables → verificar que el cambio se aplicó. CancelTableEditing para limpiar.
**Commit:** `feat(db-tables): add core array R/W wrappers (Get/Set/Apply/Cancel)`
 — COMMIT CHECKPOINT
**Files:** 7 wrappers en `scripts/wrappers/func_DatabaseTables_*CSV*.py`, `*XMLString*.py`, `scripts/registry.json`
**What:** Crear wrappers para las variantes de exportación/importación en CSV file, CSV string y XML string. Siguen el mismo patrón que Array pero con formatos de serialización diferentes. Registrar las 7 funciones en `registry.json`.
**Funciones:**
- `GetTableForDisplayCSVFile(TableKey, FieldKeyList[], GroupName, FileName, ...)` → exporta a archivo CSV
- `GetTableForDisplayCSVString(TableKey, FieldKeyList[], GroupName, ...)` → retorna CSV como string
- `GetTableForDisplayXMLString(TableKey, FieldKeyList[], GroupName, ...)` → retorna XML como string
- `GetTableForEditingCSVFile(TableKey, GroupName, FileName, ...)` → exporta editable a CSV
- `GetTableForEditingCSVString(TableKey, GroupName, ...)` → retorna editable como CSV string
- `SetTableForEditingCSVFile(TableKey, FileName, ...)` → importa desde CSV file
- `SetTableForEditingCSVString(TableKey, CSVString, ...)` → importa desde CSV string
**Testing:** Exportar tabla conocida a CSV string/file → verificar contenido no vacío. Round-trip: exportar → re-importar → ApplyEditedTables → verificar integridad.
**Commit:** `feat(db-tables): add CSV/XML I/O wrappers (7 functions)`
**Testing:** Exportar tabla conocida a CSV string/file → verificar contenido no vacío. Round-trip: exportar → re-importar → ApplyEditedTables → verificar integridad.

### Step 4: Wrapper consolidado Display Selection (configuración de visualización)
**Files:** `scripts/wrappers/func_DatabaseTables_DisplaySelection_Consolidated.py`
**What:** Crear UN SOLO wrapper consolidado que pruebe los 10 pares Get/Set de configuración de visualización. Son funciones simples con firma repetitiva: Get retorna array de nombres seleccionados, Set recibe array de nombres. El wrapper ejecutará el ciclo Get→Set→Get para cada par y verificará cambios. `GetTableOutputOptionsForDisplay`/`SetTableOutputOptionsForDisplay` requieren manejo especial (18 parámetros ByRef).
**Funciones (10 pares Get/Set testeados):**
1. LoadCases
2. LoadCombinations
3. LoadPatterns
4. ElementVirtualWorkNamedSets
5. GeneralizedDisplacements
6. JointResponseSpectraNamedSets
7. PlotFunctionTracesNamedSets
8. PushoverNamedSets
9. SectionCuts
10. TableOutputOptions
**Testing:** Script ejecuta ciclo para cada par: Get → capturar selección actual → Set con valor modificado → Get de nuevo → verificar cambio → restaurar estado original. Registrar las 20 funciones individuales en registry.json pero con referencia al mismo wrapper consolidado.

### Step 5: Wrapper ShowTablesInExcel + Registro completo en registry.json
**Files:** `scripts/wrappers/func_DatabaseTables_ShowTablesInExcel.py`, `scripts/registry.json`
**What:** Crear el último wrapper (ShowTablesInExcel) y registrar las 37 funciones en `registry.json` con la estructura estándar: category "Database_Tables", description, signature, verified=true, wrapper_script. Para las 20 funciones de Display Selection, registrarlas individualmente pero apuntando todas al wrapper consolidado `func_DatabaseTables_DisplaySelection_Consolidated`.
**Testing:** Verificar que `query_function_registry(category="Database_Tables")` retorna las 37 funciones. ShowTablesInExcel: ejecutar con una tabla → verificar que Excel se abre (visual). Commit checkpoint antes de continuar con backend.
 — COMMIT CHECKPOINT
**Files:** `scripts/database_tables/backend_database_tables.py`, `scripts/database_tables/README.md`
**What:** Crear clase `DatabaseTablesBackend` siguiendo el patrón de `backend_template.py`. Expondrá métodos de alto nivel:
- `list_tables()` → lista todas las tablas con metadata
- `read_table(table_key, group="All")` → lee tabla como lista de dicts
- `write_table(table_key, data)` → escribe tabla modificada y aplica cambios
- `export_csv(table_key, filepath)` → exporta a CSV
- `import_csv(table_key, filepath)` → importa desde CSV
- `get_table_fields(table_key)` → retorna campos disponibles con tipos y unidades
- `is_model_locked()` → verifica estado de bloqueo del modelo
- `configure_display(load_cases=[], combos=[], patterns=[])` → configura visualización
**Testing:** Standalone test (`if __name__ == "__main__"`) que conecta a SAP2000 existente → lista tablas → lee una tabla → muestra datos formateados → exporta CSV → verifica archivo.
**Commit:** `feat(db-tables): add DatabaseTablesBackend class with high-level API` — COMMIT CHECKPOINT
**Files:** `scripts/database_tables/gui_database_tables.py`
**What:** GUI con:
- Panel izquierdo: TreeView de tablas disponibles (agrupadas por categoría: Model Definition, Assignments, Loads, Analysis Results, etc.)
- Panel central: QTableWidget mostrando datos de la tabla seleccionada (headers con nombres de campos y unidades)
- Toolbar: Exportar CSV, Exportar Excel, Importar CSV, Refrescar, Apply Changes, Conectar/Desconectar
- Barra de estado: indicador de conexión SAP2000, **indicador visual de estado lock del modelo** (🔒/🔓), tabla activa, número de registros
- **Edición condicional:** 
  - Al cargar tabla, verificar `backend.is_model_locked()`
  - Si bloqueado: QTableWidget en modo read-only, botón Apply Changes deshabilitado, tooltip warning "Modelo bloqueado - edición deshabilitada"
  - Si desbloqueado: permitir edición doble-click en celdas, botón Apply Changes habilitado
  - Polling cada 2 segundos para actualizar indicador de lock state
- Apply Changes: diálogo de confirmación → ejecuta `backend.write_table()` → muestra resultado (errores/warnings/success) → refrescar tabla
**Testing:** Ejecutar GUI → verificar que lista tablas → seleccionar tabla → verificar que muestra datos → exportar CSV → verificar archivo generado. Para edición: desbloquear modelo → editar celda → Apply Changes → refrescar → verificar cambio persistió. Bloquear modelo (correr análisis) → verificar que edición está deshabilitada y indicador 🔒 activo.
**Commit:** `feat(db-tables): add PySide6 GUI with conditional editing and lock state monitoring`

## Decisiones de implementación (confirmadas)

1. **Step 4 — Display Selection**: ✅ Wrapper consolidado único que testea los 10 pares, registrado en registry como 20 entradas individuales apuntando al mismo wrapper.

2. **Step 7 — GUI**: ✅ Edición in-place habilitada SOLO si `SapModel.GetModelIsLocked() == False`. Si bloqueado, deshabilitar edición y mostrar warning visual (indicador 🔒).

3. **Priorización**: ✅ Implementación por etapas con commit checkpoints:
   - **Commit 1:** Steps 1-2 (wrappers metadata + core)
   - **Commit 2:** Step 3 (CSV/XML wrappers)
   - **Commit 3:** Steps 4-5 (Display Selection consolidado + registry completo)
   - **Commit 4:** Step 6 (Backend class)
   - **Commit 5:** Step 7 (GUI standalone)

## Notas técnicas

### ByRef en COM Python
Todas las funciones DatabaseTables retornan `ret_code` como **último elemento** de la tupla COM. Los arrays ByRef (FieldKey[], TableData[], etc.) se retornan como tuplas de Python que requieren `list()` para manipularse.

### TableData[] — Formato flat array
`TableData` es un **array plano** donde los datos se almacenan fila por fila:
```
[field1_row1, field2_row1, ..., fieldN_row1, field1_row2, field2_row2, ..., fieldN_row2, ...]
```
El número de columnas se determina por `len(FieldKeysIncluded)` y el número de filas por `NumberRecords`.

### Prerequisitos para wrappers
La mayoría de funciones DatabaseTables requieren un modelo con datos. Los wrappers deberían:
1. Crear modelo blank → agregar al menos un frame/area y un load pattern
2. Ejecutar la función sobre tablas que se sabe tienen datos (ej: "Frame Assignments - Summary")

### Orden de dependencia
```
Step 1 (Metadata) → Step 2 (Core) → Step 3 (CSV/XML) → Step 4 (Display) → Step 5 (Registry)
                                                                                    ↓
                                                         Step 6 (Backend) → Step 7 (GUI)
```
