# Quick Reference: SAP2000 Script Development

## 🚀 Quick Start

```bash
# 1. Verificar conexión
get_model_info

# 2. Buscar función necesaria
query_function_registry("PropFrame.SetCircle")

# 3. Cargar wrapper si existe
load_script("func_PropFrame_SetCircle")

# 4. Escribir código (copiar del wrapper)

# 5. Ejecutar
run_sap_script(script)

# 6. Verificar result[] → ✅ o ❌

# 7. Guardar cuando funcione
run_sap_script(script, save_as="mi_script.py")
```

## ⚠️ Reglas Críticas

### ✅ SIEMPRE Hacer:

1. **Buscar wrapper PRIMERO** con `query_function_registry`
   ```python
   # ✅ Correcto:
   query_function_registry("FrameObj.SetTCLimits")
   load_script("func_FrameObj_SetTCLimits")  # Copiar de aquí
   
   # ❌ Incorrecto:
   search_api_docs("SetTCLimits")  # API docs pueden estar desactualizados
   ```

2. **Validar return codes** con `assert`
   ```python
   # ✅ Correcto:
   ret = SapModel.PropFrame.SetCircle("SEC1", "STEEL", 50.0)
   assert ret == 0, f"SetCircle failed: {ret}"
   
   # ❌ Incorrecto:
   ret = SapModel.PropFrame.SetCircle("SEC1", "STEEL", 50.0)
   # ... continuar sin verificar
   ```

3. **Escribir a result[]** para verificación
   ```python
   # ✅ Correcto:
   result["frame_created"] = frame_name
   result["num_frames"] = len(bolt_frame_names)
   
   # ❌ Incorrecto:
   # ... no escribir nada, confiar en prints
   ```

4. **Usar sap_temp_dir** para guardar
   ```python
   # ✅ Correcto:
   ret = SapModel.File.Save(sap_temp_dir + r"\my_model.sdb")
   
   # ❌ Incorrecto:
   ret = SapModel.File.Save(r"C:\Users\...\my_model.sdb")  # Hardcoded
   ```

5. **Desarrollar por tareas incrementales**
   ```python
   # ✅ Correcto:
   # Task 1 → Ejecutar → ✅
   # Task 2 → Ejecutar → ✅
   # Task 3 → Ejecutar → ✅
   # Integrar todo → Ejecutar → ✅
   
   # ❌ Incorrecto:
   # Escribir 500 líneas → Ejecutar → ❌ Error en línea 237, imposible debuggear
   ```

### ❌ NUNCA Hacer:

1. **NO inventar signatures sin verificar**
   ```python
   # ❌ MAL (inventado):
   ret = SapModel.FrameObj.SetTCLimits(name, True, 0.0, False, 0.0, 0)  # 6 args
   
   # ✅ BIEN (del wrapper):
   ret = SapModel.FrameObj.SetTCLimits(name, True, 0.0, False, 0.0)  # 5 args (ItemType omitido)
   ```

2. **NO ignorar return codes**
   ```python
   # ❌ MAL:
   SapModel.PropFrame.SetCircle("SEC1", "STEEL", 50.0)
   # ¿Funcionó? No lo sabemos
   
   # ✅ BIEN:
   ret = SapModel.PropFrame.SetCircle("SEC1", "STEEL", 50.0)
   assert ret == 0, f"Failed: {ret}"
   ```

3. **NO asumir layout de ByRef sin verificar**
   ```python
   # ❌ MAL (asumido):
   raw = SapModel.FrameObj.AddByCoord(...)
   frame_name = raw[1]  # ¿Índice correcto?
   
   # ✅ BIEN (verificado en wrapper):
   raw = SapModel.FrameObj.AddByCoord(...)
   frame_name = raw[0]   # Name siempre es raw[0]
   ret_code = raw[-1]    # Return code siempre es raw[-1]
   ```

4. **NO mezclar API docs con wrappers**
   ```python
   # ❌ MAL (mezclado):
   # Wrapper dice: SetCircle(Name, MatProp, t3)
   # API doc dice: SetCircle(Name, MatProp, t3, Color, Notes, GUID)
   # Tú usas: SetCircle(Name, MatProp, t3, Color)  # ROMPE!
   
   # ✅ BIEN:
   # Si hay wrapper: usar EXACTAMENTE lo del wrapper
   # Si NO hay wrapper: usar API docs y marcar como no verificado
   ```

## 🔍 Debugging Common Errors

| Error | Causa | Solución |
|-------|-------|----------|
| `return_code != 0` | Parámetros incorrectos | Verificar wrapper o API docs |
| `IndexError` | ByRef layout incorrecto | Revisar wrapper: `ret[0]` vs `ret[-1]` |
| `AttributeError: 'int'` | Asumiste tuple | `isinstance(ret, tuple)` antes de indexar |
| `COMError` | SAP2000 crasheó | `connect_sap2000` |
| `AssertionError` | Validación falló | Leer mensaje, ajustar params |

## 📝 Task Template

```python
# ═════════════════════════════════════════════════════════════════════
# ── Task N: [Nombre] ─────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════

# ── N.1. [Sub-tarea 1] ───────────────────────────────────────────────
ret = SapModel.Algo.Hacer(...)
assert ret == 0, f"Error: {ret}"

# ── N.2. [Sub-tarea 2] ───────────────────────────────────────────────
raw = SapModel.Algo.Crear(...)
nombre = raw[0]
assert raw[-1] == 0, f"Error: {raw[-1]}"

# ── N.3. Verificación ────────────────────────────────────────────────
result[f"task_{N}_success"] = True
result[f"task_{N}_output"] = nombre
```

## 🎯 One-Page Checklist

```
□ Fase 1: Planificación
  □ Objetivo definido
  □ Variables listadas
  □ Tareas descompuestas

□ Fase 2: Investigación
  □ get_model_info → Conexión OK
  □ query_function_registry → Para CADA función
  □ load_script → Wrappers cargados
  □ list_scripts → Ejemplos vistos

□ Fase 3: Desarrollo
  □ Task 1 → Escribir → Ejecutar → ✅
  □ Task 2 → Escribir → Ejecutar → ✅
  □ Task 3 → Escribir → Ejecutar → ✅
  □ ... (todas las tareas)
  □ Funciones auxiliares extraídas

□ Fase 4: Integración
  □ Todas las tareas combinadas
  □ Script completo ejecutado → ✅
  □ result[] completo
  □ Código refinado

□ Fase 5: Documentación
  □ Header agregado
  □ Comentarios claros
  □ save_as → Guardado
  □ register_verified_function → Funciones nuevas
```

## 🛠️ MCP Tools Reference

| Tool | Use Case | Priority |
|------|----------|----------|
| `get_model_info` | Verificar conexión | ⭐⭐⭐ |
| `query_function_registry` | Buscar wrappers | ⭐⭐⭐ |
| `load_script` | Copiar signature | ⭐⭐⭐ |
| `run_sap_script` | Ejecutar/Testing | ⭐⭐⭐ |
| `search_api_docs` | Fallback (sin wrapper) | ⭐⭐ |
| `list_scripts` | Buscar ejemplos | ⭐⭐ |
| `register_verified_function` | Documentar nuevas | ⭐ |

## 💡 Pro Tips

1. **Desarrolla en orden de dependencias**
   - Initialize → Materials → Properties → Geometry → Constraints

2. **Una función auxiliar = Una responsabilidad**
   ```python
   # ✅ BIEN:
   def create_circle_points(cx, cy, z, radius, num_points, prefix):
       # Solo crea puntos en círculo
   
   # ❌ MAL:
   def create_bolt_geometry(bolt_data):
       # Crea puntos + áreas + frames + constraints ← Demasiado complejo
   ```

3. **Print para debug, assert para validación**
   ```python
   # Durante desarrollo:
   print(f"AddByCoord returned: {raw}")  # Ver estructura
   
   # En producción:
   assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"  # Validar
   ```

4. **Usa result[] como "test report"**
   ```python
   result["initialized"] = True
   result["num_bolts"] = len(bolt_centers)
   result["frames_created"] = len(bolt_frame_names)
   result["tc_limits_applied"] = tc_count
   result["success"] = all([...])
   ```

5. **Guarda versiones incrementales**
   ```python
   # Versión 1: Solo geometría básica
   run_sap_script(script, save_as="placabase_v1_geometry.py")
   
   # Versión 2: + Constraints
   run_sap_script(script, save_as="placabase_v2_constraints.py")
   
   # Versión 3: + Balasto
   run_sap_script(script, save_as="placabase_v3_balasto.py")
   
   # Final:
   run_sap_script(script, save_as="example_placabase_parametric.py")
   ```

## 📚 Further Reading

- [Workflow Completo](workflow-script-creation.md) — Guía exhaustiva
- [SAP2000 API SKILL.md](../.github/skills/sap2000-api/SKILL.md) — Referencia del skill
- [Function Registry](../scripts/registry.json) — Funciones verificadas
- [Script Library](../scripts/) — Ejemplos existentes

---

## 🖥️ GUI Standalone — Quick Reference

### Cuándo Generar GUI

Al final de la Fase 5, preguntar al usuario:
> *"¿Quieres generar una GUI standalone (PySide6) para este script?"*

### Checklist Fase 6

```
□ 6.1 Identificar inputs (variables configurables del script)
□ 6.2 Generar backend_{nombre}.py (copiar de template)
□ 6.3 Generar gui_{nombre}.py (copiar de template)
□ 6.4 Crear carpeta scripts/{nombre}/
□ 6.5 Testing: ast.parse + GUI abre + flujo completo
```

### Estructura de Carpeta

```
scripts/{nombre}/
    gui_{nombre}.py         # PySide6 GUI
    backend_{nombre}.py     # COM directo (comtypes)
```

### Template: SapConnection (COM directo)

```python
import comtypes.client

class SapConnection:
    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing=True) -> dict:
        try:
            self.sap_object = comtypes.client.GetActiveObject(
                "CSI.SAP2000.API.SapObject"
            )
            self.sap_model = self.sap_object.SapModel
            return {"connected": True,
                    "version": str(self.sap_object.GetOAPIVersionNumber()),
                    "model_path": str(self.sap_model.GetModelFilename())}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}
```

### Template: Backend.run()

```python
class MyBackend:
    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config) -> dict:
        SapModel = self.sap_model
        result = {}
        # ... lógica del script (tareas numeradas, asserts) ...
        result["success"] = True
        return result
```

### Template: QThread Worker

```python
class RunWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend, config):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            result = self._backend.run(self._config)
            self.finished.emit(result)
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})
```

### Reglas

| ✅ Hacer | ❌ No Hacer |
|----------|-------------|
| `import comtypes.client` | `from sap_bridge import bridge` |
| `SapConnection.connect()` | `bridge.connect()` |
| `backend.run(config)` | `run_script(script_text)` |
| `from backend_X import ...` | `from sap_executor import ...` |
| Solo stdlib + comtypes + PySide6 | Importar `app_logger`, `sap_utils_common` |

### Naming Convention

| Tipo | Ubicación | Ejemplo |
|------|-----------|---------|
| Script MCP verificado | `scripts/example_*.py` | `scripts/example_ring_areas_parametric.py` |
| GUI standalone | `scripts/{nombre}/gui_{nombre}.py` | `scripts/ring_areas/gui_ring_areas.py` |
| Backend standalone | `scripts/{nombre}/backend_{nombre}.py` | `scripts/ring_areas/backend_ring_areas.py` |
| Templates | `scripts/templates/*.py` | `scripts/templates/backend_template.py` |
| Wrappers | `scripts/wrappers/func_*.py` | `scripts/wrappers/func_FrameObj_AddByCoord.py` |
