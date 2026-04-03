# Ideas: Aplicar `karpathy/autoresearch` a SAP Skills

> **Referencia:** [github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch)

---

## ¿Qué es `autoresearch`?

`autoresearch` es un framework minimalista de Andrej Karpathy donde un agente de IA recibe un único archivo de entrenamiento (`train.py`), un presupuesto fijo de tiempo (5 minutos) y un archivo de instrucciones (`program.md`). El agente modifica el código de manera autónoma, entrena el modelo, mide una métrica de validación (`val_bpb`), conserva los cambios si mejoran el resultado y repite el ciclo —todo esto mientras el investigador duerme.

La filosofía central es:

- **Un archivo que modificar** (el agente no toca nada más)
- **Un presupuesto de tiempo fijo** (comparaciones justas entre experimentos)
- **Una métrica única** (señal de mejora/descenso sin ambigüedad)
- **`program.md` como "código de la organización de investigación"** (instrucciones que el humano itera, no el agente)

---

## Paralelismo con SAP Skills

| `autoresearch`               | SAP Skills (este repo)                             |
|------------------------------|----------------------------------------------------|
| `train.py`                   | Script de modelo SAP (`scripts/*.py`)              |
| `val_bpb` (métrica)          | Índice de utilización, peso, deriva, costo         |
| `program.md`                 | `.github/skills/sap2000-api/` + `program.md` nuevo |
| GPU / iteración de 5 min     | Análisis SAP2000 / presupuesto de runs             |
| Agente Claude/Codex           | Agente `@sap2000-scripter`                         |
| Dataset de entrenamiento     | Parámetros del proyecto (cargas, geometría, norma) |

---

## Ideas Concretas de Implementación

### 1. 🔁 Auto-Optimización Estructural Autónoma

**Concepto:** Un agente modifica iterativamente un script de SAP2000 (p. ej. secciones de vigas, alturas de piso, rigidez de conexiones), corre el análisis y compara la métrica de diseño objetivo.

**Cómo funciona:**
```
loop:
  agente modifica scripts/train_structure.py
  ejecuta análisis via MCP (run_sap_script)
  lee resultados (deriva, peso, índice de utilización)
  si métrica_nueva < métrica_anterior → conserva cambios
  si no → descarta y prueba otra variación
  repite N veces o hasta presupuesto agotado
```

**Métrica única sugerida:** `max_demand_capacity_ratio` (máximo índice D/C de todos los elementos) — análogo a `val_bpb`. Cuanto menor, mejor el diseño dentro del presupuesto de peso.

**Archivo que el agente modifica:** Un único `scripts/train_structure.py` que define: sección de columnas/vigas, altura entrepiso, rigidez de losa.

**Archivo que el humano itera:** `program_structure.md` con instrucciones de norma, combinaciones de carga, restricciones arquitectónicas.

---

### 2. 📄 `program_structure.md` — El "Código de la Org de Diseño"

**Concepto:** Crear un `program_structure.md` en la raíz del repo (análogo al `program.md` de autoresearch) que el ingeniero estructural itera —no el agente— para configurar la "organización de investigación estructural autónoma".

**Contenido típico:**
```markdown
# program_structure.md

## Objetivo
Minimizar el peso total de acero manteniendo deriva < L/400
y todos los índices D/C < 0.90 bajo ASCE 7-22.

## Parámetros a explorar
- Secciones W para vigas: W14, W16, W18, W21, W24
- Secciones HSS para columnas: HSS 6x6, HSS 8x8, HSS 10x10
- Configuración de arriostramiento: X, V, chevron

## Restricciones
- No modificar geometría de planta
- No modificar cargas de diseño
- Norma sísmica: ASCE 7-22 zona Dmax

## Presupuesto
- Máximo 20 análisis por sesión overnight
- Tiempo máximo por análisis: 10 minutos

## Métrica de éxito
max(D/C) < 0.90 AND peso_acero < baseline_weight * 0.85
```

---

### 3. ⏱️ Presupuesto Fijo de Análisis (en lugar de tiempo)

**Concepto:** En lugar de fijar tiempo de entrenamiento como autoresearch, fijar el número de corridas de SAP2000 por sesión del agente. Esto hace los experimentos **comparables entre máquinas con diferente velocidad**.

**Implementación:**
- Constante `MAX_ANALYSIS_RUNS = 20` en un archivo `experiment_config.py` (análogo al `prepare.py` de autoresearch, que el agente no toca)
- El agente cuenta sus corridas y para al llegar al límite
- Genera un `experiment_log.md` con resultados de cada iteración

**Ventaja:** Al despertar tienes un log de 20 experimentos con métricas comparables, sin que el agente haya "gastado" tiempo en análisis demasiado lentos.

---

### 4. 📊 `experiment_log.md` Generado Automáticamente

**Concepto:** Después de cada sesión autónoma, el agente genera (o actualiza) un `experiment_log.md` en la raíz —similar al log de experimentos que autoresearch produce— con una tabla de resultados.

**Formato ejemplo:**
```markdown
# Experiment Log — Estructura Torre Norte

| Run | Cambio Realizado                   | max(D/C) | Peso Acero (ton) | ¿Conservado? |
|-----|------------------------------------|----------|------------------|--------------|
| 001 | baseline (W16 vigas, HSS8 col.)    | 0.97     | 245.3            | —            |
| 002 | vigas → W18                        | 0.88     | 252.1            | ✅           |
| 003 | columnas → HSS10x10                | 0.81     | 261.4            | ✅           |
| 004 | vigas → W14 (regresión)            | 1.03     | 238.0            | ❌           |
| 005 | arriostramiento X → chevron        | 0.79     | 259.8            | ✅           |
```

---

### 5. 🔬 Multi-Agente: Exploración en Paralelo

**Concepto:** Extender autoresearch hacia múltiples agentes simultáneos. Cada agente explora una rama de diseño diferente:

```
Agente 1: optimiza secciones de acero
Agente 2: optimiza configuración de arriostramiento  
Agente 3: optimiza espesores de losa
          ↓
     Merge las mejores ideas
          ↓
     Análisis combinado
```

**Implementación:**
- Cada agente trabaja en su propio `branch_agentN.py`
- Un agente "coordinador" lee los logs de todos y genera una propuesta de modelo consolidado
- Análogo a cómo autoresearch propone escalar a "swarms of AI agents"

---

### 6. 🧬 Evolución del `program_structure.md` Como Código Genético

**Concepto:** El ingeniero itera el `program_structure.md` según lo aprendido en cada sesión —exactamente como Karpathy describe iterar el `program.md` para encontrar "el código de la org que logra mayor velocidad de investigación".

**Flujo de trabajo humano:**
```
Sesión 1: program_structure.md v1 → 20 experimentos → log revela que arriostramiento es el mayor lever
Sesión 2: program_structure.md v2 → foco en variantes de arriostramiento → 20 experimentos
Sesión 3: program_structure.md v3 → refinamiento con norma actualizada
...
Sesión N: diseño óptimo encontrado
```

**El ingeniero NO toca el script de modelo directamente. Solo itera las instrucciones al agente.**

---

### 7. 🤖 Auto-Generación de Scripts con Validación Autónoma

**Concepto:** Adaptar el ciclo de autoresearch para generar y validar scripts MCP automáticamente. El agente:

1. Lee `program_structure.md`
2. Genera un script candidato usando `@sap2000-scripter`
3. Lo ejecuta vía MCP (`run_sap_script`)
4. Lee resultados de análisis
5. Registra en `scripts/registry.json` si supera el umbral de calidad
6. Propone la siguiente variación

**Esto convierte el registry de funciones en un "modelo mejorado" acumulativo**, igual que `train.py` acumula mejoras en autoresearch.

---

### 8. 📐 Benchmark Estructural Estándar (análogo al dataset de FineWeb)

**Concepto:** Autoresearch usa siempre el mismo dataset (FineWeb-Edu) para que los experimentos sean comparables. Para SAP Skills, crear un **conjunto de modelos benchmark** estándar:

- `benchmark_simple_beam.sdb` — viga simple estándar
- `benchmark_portal_frame.sdb` — pórtico 2D estándar
- `benchmark_3d_building.sdb` — edificio 3D de 5 pisos estándar

El agente siempre prueba sus cambios sobre estos benchmarks. La métrica: cuánto mejora el índice D/C o deriva vs. el baseline del benchmark.

---

## Arquitectura Propuesta del "SAP AutoResearch"

```
SAP Skills AutoResearch
│
├── program_structure.md          ← Itera el HUMANO (norma, objetivo, restricciones)
├── experiment_config.py          ← Constantes fijas, NO modifica el agente
├── train_structure.py            ← Itera el AGENTE (parámetros estructurales)
├── experiment_log.md             ← Genera el AGENTE automáticamente
│
├── benchmarks/                   ← Modelos SAP estándar de referencia
│   ├── benchmark_simple_beam.sdb
│   ├── benchmark_portal_frame.sdb
│   └── benchmark_3d_building.sdb
│
└── scripts/
    ├── registry.json             ← Crece con cada función validada
    └── ...
```

---

## Comparación de Filosofías

| Principio autoresearch         | Aplicación SAP Skills                                          |
|--------------------------------|----------------------------------------------------------------|
| "No toques los archivos Python" | "No toques la geometría del proyecto ni las cargas de diseño" |
| "5 minutos de entrenamiento"   | "N análisis por sesión overnight"                              |
| "val_bpb única métrica"        | "max(D/C) única métrica de diseño"                             |
| "El agente edita train.py"     | "El agente edita train_structure.py"                           |
| "El humano edita program.md"   | "El ingeniero edita program_structure.md"                      |
| "Log de experimentos al despertar" | "experiment_log.md al llegar a la oficina"                 |

---

## Próximos Pasos Sugeridos

1. **Crear `program_structure.md`** con un proyecto estructural real como primer experimento
2. **Crear `experiment_config.py`** con `MAX_ANALYSIS_RUNS`, `BENCHMARK_METRIC`, y parámetros fijos del proyecto
3. **Crear `train_structure.py`** con los parámetros del modelo que el agente puede variar (secciones, alturas, rigideces)
4. **Adaptar `@sap2000-scripter`** para leer `program_structure.md` al inicio de cada sesión y mantener el contador de runs
5. **Implementar `experiment_log.md`** auto-generado con tabla de resultados por iteración
6. **Definir benchmark estructural** (modelo SAP2000 de referencia reproducible)

---

## Reflexión Final

La idea más poderosa de autoresearch no es técnica: es la **inversión del rol humano**. El ingeniero deja de modificar scripts y empieza a **programar las instrucciones del agente**. La clave está en encontrar el `program_structure.md` que maximiza la velocidad de convergencia hacia el diseño óptimo —exactamente como Karpathy busca el `program.md` que maximiza la velocidad de investigación en LLMs.

> _"You are not touching any of the Python files like you normally would. Instead, you are programming the `program.md` Markdown files."_ — Andrej Karpathy

En SAP Skills, esto se traduce en: **El ingeniero no toca los scripts de SAP2000. Programa las instrucciones al agente.**
