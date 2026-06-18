# SAP2000 Visual Scripter — Blockly

**Editor visual drag-and-drop para usuarios no-programadores**

Permite crear scripts de SAP2000 arrastrando bloques sin escribir código, exactamente como Scratch/Blockly educativo.

---

## 🚀 Quick Start

### 1. Instalación de dependencias

```bash
cd c:\Users\fcoca\Desktop\Ingenieria\Proyectos_Python\Skills_SAP
.venv\Scripts\Activate.ps1

# Instalar PySide6 (GUI)
pip install PySide6

# Verificar que comtypes ya está instalado
pip list | grep comtypes
```

### 2. Generar definiciones de bloques (desde registry.json)

```bash
python scripts/blockly/blockly_generator.py
```

Esto genera:
- `scripts/blockly/block_definitions.js` — Definiciones JSON de bloques
- `scripts/blockly/toolbox_structure.xml` — Toolbox con 9 fases
- `scripts/blockly/generators.js` — Generadores de código Python

### 3. Ejecutar modo demo (sin SAP2000)

```bash
python scripts/blockly/blockly_gui.py
```

> **Nota:** Requiere SAP2000 abierto para ejecutar scripts reales. 
> Si no está abierto, verás mensaje "🔴 Desconectado".

---

## 📝 Usando el Editor

### Workflow Típico

1. **Arrastrar bloques** desde toolbox izquierdo
   - Las 9 categorías representan las fases SAP2000
   - Colores: Rojo (Init) → Naranja (Mat) → ... → Púrpura (Design)

2. **Configurar parámetros**
   - Click en bloque → editar campos
   - Ejemplo: "Crear viga" → ingresar coordenadas

3. **Ver preview Python**
   - Panel derecha mostrará Python generado automáticamente
   - Válida sintaxis automáticamente

4. **"▶️ Ejecutar"**
   - Transpila XML → Python
   - Valida fases (1→2→3...→9)
   - Ejecuta contra SAP2000
   - Muestra output en console

5. **Exportar/Guardar**
   - "💾 Exportar Python" → archivo .py reutilizable
   - "💾 Guardar Proyecto" → archivo .blockly para editar después

---

## 🛠️ Estructura de Carpetas

```
scripts/blockly/                    # Todo Blockly en un solo lugar
├── __init__.py                    # Package init
├── blockly_gui.py                 # 🚀 APP PRINCIPAL
├── blockly_executor.py            # Executor SAP2000 (COM bridge)
├── blockly_transpiler.py          # XML → Python translator
├── blockly_generator.py           # Genera bloques desde registry
├── index.html                     # HTML + Blockly CDN (standalone)
├── block_definitions.js           # AUTO-GENERADO
├── toolbox_structure.xml          # AUTO-GENERADO
├── generators.js                  # AUTO-GENERADO
└── README.md                      # Esta documentación
```

---

## 📋 Blockly Phases (9 Fases)

| Fase | Categoría | Bloques Ejemplo | Color |
|------|-----------|------------------|-------|
| 1 | Inicializar | NewBlank, OpenFile, Save | 🔴 Rojo |
| 2 | Materiales | SetMaterial, SetMPIsotropic | 🟠 Naranja |
| 3 | Secciones | SetRectangle, SetISection, SetCircle | 🟡 Amarillo |
| 4 | Geometría | AddByCoord, AddCartesian, Divide | 🟢 Verde |
| 5 | Restricciones | SetRestraint, SetDiaphragm, SetBody | 🔵 Cian |
| 6 | Cargas | Add (patterns/cases), SetLoadUniform | 🔷 Azul claro |
| 7 | Análisis | RunAnalysis, SetActiveDOF | 🔵 Azul |
| 8 | Resultados | JointDispl, FrameForce, DatabaseTables | 🟣 Púrpura |
| 9 | Diseño | DesignSteel, DesignConcrete | 🟪 Púrpura oscuro |

**Restricción:** Bloques deben estar en orden creciente de fases
- ✅ Permitido: Fase 1 → Fase 2 → Fase 4
- ❌ No permitido: Fase 2 → Fase 1 (error de validación)

---

## 💻 Ejemplo: Script Simple (Viga)

### Flujo Visual (Blockly)

```
┌──────────────────┐
│  File.NewBlank   │
└─────────┬────────┘
          ↓
┌──────────────────────────────┐
│ Material "CONC" (Type=2)     │
└─────────┬────────────────────┘
          ↓
┌──────────────────────────────────────┐
│ Sección "SEC1" (Rect: 0.3 x 0.3m)   │
└─────────┬──────────────────────────┬─┘
          ↓                          ↓
┌──────────────────────────┐  (referencia al material)
│ Crear viga (0,0,0)→(0,0,10) │
│ Sección: SEC1            │
└──────────────────────────┘
```

### Python Generado

```python
# Auto-generado por Blockly Visual Scripter

ret = SapModel.File.NewBlank()
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC", 2)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("SEC1", "CONC", 0.3, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, "", "SEC1", "1")
frame_name = raw[0]
assert raw[-1] == 0
result["frame_name"] = frame_name
```

### Output

```
✅ Éxito!
Tiempo: 0.245s
Result dict:
{
  "frame_name": "1"
}
```

---

## 🔧 Modo Testing (sin SAP2000)

### Test Transpiler

```bash
python -c "
from blockly_transpiler import BlocklyTranspiler
transpiler = BlocklyTranspiler()
print(transpiler.example_usage())
"
```

### Test Executor (sin SAP2000)

```python
from blockly_executor import BlocklyScriptExecutor

# Código Python simple (sin SAP2000)
code = '''
result['test'] = 42
print('Hola')
'''

executor = BlocklyScriptExecutor()
result = executor.run_script(code)
print(result)
```

---

## 🛑 Troubleshooting

### Error: "No hay conexión con SAP2000"
- Abre SAP2000 primero
- Verifica que no haya conflictos de COM
- Reinicia la app

### Error: "Fase fuera de orden"
- Los bloques deben estar en orden: 1 (Init) → 2 (Materials) → ...
- Mueve los bloques al orden correcto
- O del error mostrará qué fase está fuera

### Error: "ByRef mismatch"
- El transpiler no reconoce los parámetros del bloque
- Verifica que registry.json esté actualizado
- Regenera bloques: `python blockly_generator.py`

### Error: "XML inválido"
- Workspace se corrompió
- "🗑️ Limpiar" y empezar de nuevo
- O cargar proyecto guardado previamente

---

## 🔄 Flujo de Extensión

### Añadir una nueva función SAP2000

1. **Verificar en `scripts/registry.json`**
   - Confirmar que la función está listada

2. **Generar bloques nuevos**
   ```bash
   python scripts/blockly_generator.py
   ```
   El nuevo bloque aparecerá automáticamente en el toolbox

3. **Actualizar `blockly_transpiler.py`**
   - Añadir case en `_generate_block_code()`
   - El transpiler sabrá cómo convertir ese bloque a Python

---

## 📚 Referencias

- [Plan Detallado](../../plans/visual-scripting/IMPLEMENTATION_BLOCKLY.md)
- [SAP2000 API Skill](.../../../.github/skills/sap2000-api/SKILL.md)
- [Registry JSON](registry.json)
- [Templates Backend/GUI](templates/)

---

## 🤝 Créditos

- **Blockly:** [Google Blockly](https://developers.google.com/blockly)
- **PySide6:** [Qt for Python](https://wiki.qt.io/Qt_for_Python)
- **SAP2000 API:** COM bridge nativo

---

## 📄 Licencia

[Tu licencia aquí]

---

**Última actualización:** 2026-04-04
