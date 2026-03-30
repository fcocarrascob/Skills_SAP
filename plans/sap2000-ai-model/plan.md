# SAP2000 AI Code Generation Model

**Branch:** `feat/sap2000-ai-model`
**Description:** Pipeline de fine-tuning de un LLM de código para generar scripts SAP2000 a partir de instrucciones en lenguaje natural

## Goal

Crear un mini-modelo IA especializado que, dado un prompt en español/inglés describiendo una estructura (ej: "viga simplemente apoyada con carga muerta de 24 kN/m"), genere un script Python correcto para SAP2000. El modelo aprovecha los ~1,000+ ejemplos verificados ya existentes en el repositorio (97 funciones, 49 wrappers, 79 scripts).

## Análisis de Situación

### Lo que tienes
| Asset | Cantidad | Calidad |
|-------|----------|---------|
| Funciones verificadas (registry) | 97 | Ground truth, estructura JSON uniforme |
| Wrappers (ejemplo por función) | 49 | Formato estandarizado, parseable |
| Scripts completos | 79 (8 root + 71 subdirs) | Working, 50-550 LOC |
| Docs API | 25 archivos | VBA (necesitan traducción) |
| LOC Python total | ~11,500 | Estilo consistente |
| Training pairs estimados | ~1,000+ (augmentables a 3,000+) | Cobertura buena |

### Recomendación Estratégica

**NO entrenes desde cero.** Con ~1,000 ejemplos no tiene sentido. Lo óptimo es:

> **QLoRA fine-tuning de Qwen2.5-Coder-7B** con dataset de instrucciones SAP2000

**¿Por qué esta ruta?**

| Alternativa | Veredicto | Motivo |
|------------|-----------|--------|
| Entrenar desde cero (GPT-style) | ❌ Descartado | Necesitas millones de ejemplos y semanas de GPU |
| RAG puro (sin fine-tuning) | ⚠️ Ya lo tienes | Tu skill + agent + MCP ya es básicamente RAG |
| Full fine-tuning | ❌ Impracticable | 7B params = 28 GB VRAM mínimo, muy lento |
| **QLoRA fine-tuning** | ✅ Ideal | 4-bit cuantización, cabe en 8-12 GB VRAM, entrena en horas |
| LoRA + API (cloud) | ✅ Alternativa | Si no tienes GPU local, usa HuggingFace AutoTrain o RunPod |

**Modelo base recomendado:** `Qwen/Qwen2.5-Coder-7B-Instruct`
- Mejor benchmark en código que CodeLlama 7B y DeepSeek-Coder 6.7B (2026)
- Soporta contexto de 32K tokens (suficiente para scripts largos)
- Licencia Apache 2.0 (uso comercial libre)
- Alternativas: `deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct` (16B, MoE), `codellama/CodeLlama-7b-Instruct-hf`

## Implementation Steps

### Step 1: Dataset Pipeline — Generación del training set
**Files:** `training/prepare_dataset.py`, `training/dataset/`, `training/README.md`
**What:** Script Python que parsea automáticamente los assets existentes y genera un dataset en formato ChatML/Alpaca con pares `{instruction, input, output}`:

1. **Función → Código** (97 pares): Registry entry → wrapper code
   ```json
   {
     "instruction": "Genera código Python para crear un elemento frame entre dos coordenadas en SAP2000",
     "input": "Punto inicial (0,0,0), punto final (5,0,0), sección 'W14x22'",
     "output": "raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, '', 'W14x22', '')\nframe_name = raw[0]\nret = raw[-1]\nassert ret == 0"
   }
   ```

2. **Script completo → Instrucción inversa** (79 pares): Dado un script, generar la instrucción que lo produciría
   ```json
   {
     "instruction": "Genera un script SAP2000 para una viga simplemente apoyada de 10m con carga muerta uniforme de 24 kN/m. Material: hormigón f'c=25 MPa. Sección rectangular 30x50cm.",
     "output": "<script completo del example_1001>"
   }
   ```

3. **Augmentación paramétrica** (~500 pares): Variaciones de parámetros (diferentes luces, cargas, secciones, materiales)

4. **Workflow parciales** (~200 pares): Sub-tareas extraídas de scripts largos (solo materiales, solo geometría, solo cargas)

5. **Convenciones API** (~100 pares): Preguntas sobre ByRef, unidades, secuencia de inicialización

**Target: 800-1,500 pares de entrenamiento** (suficiente para QLoRA de un modelo 7B)

**Testing:** Validar que cada par tenga instrucción coherente y código que pase lint. Script de validación incluido.

---

### Step 2: Entorno de Training — Setup de herramientas
**Files:** `training/requirements.txt`, `training/config.yaml`
**What:** Configurar el entorno de fine-tuning:

```
# training/requirements.txt
torch>=2.1.0
transformers>=4.40.0
peft>=0.10.0          # LoRA/QLoRA
bitsandbytes>=0.43.0  # Cuantización 4-bit
datasets>=2.19.0      # HuggingFace datasets
trl>=0.8.0            # SFTTrainer (Supervised Fine-Tuning)
accelerate>=0.30.0    # Multi-GPU / mixed precision
wandb                 # Tracking de métricas (opcional)
```

**Opciones de hardware:**
| Opción | VRAM | Costo | Velocidad |
|--------|------|-------|-----------|
| **Tu GPU local** (si tienes RTX 3060+) | 8-12 GB | $0 | 2-6 horas |
| **Google Colab Pro** | 15 GB (T4/A100) | ~$10/mes | 1-3 horas |
| **RunPod** (A100 40GB) | 40 GB | ~$1.50/hora | 30-60 min |
| **HuggingFace AutoTrain** | Managed | ~$5-15 por run | 1-2 horas |
| **Lambda Labs** | 24-80 GB | ~$1-2/hora | 30-60 min |

**Configuración QLoRA recomendada:**
```yaml
# training/config.yaml
model:
  base: "Qwen/Qwen2.5-Coder-7B-Instruct"
  quantization: "4bit"       # NF4
  bnb_4bit_compute_dtype: "bfloat16"

lora:
  r: 64                      # Rank (64 es buen balance)
  lora_alpha: 16
  target_modules: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
  lora_dropout: 0.05

training:
  epochs: 3
  batch_size: 2               # Ajustar según VRAM
  gradient_accumulation: 8    # Effective batch = 16
  learning_rate: 2e-4
  warmup_ratio: 0.03
  max_seq_length: 4096        # Suficiente para 90% de scripts
  optimizer: "paged_adamw_8bit"

dataset:
  train_split: 0.9
  eval_split: 0.1
  format: "chatml"            # Compatible con Qwen2.5
```

**Testing:** `python -c "import torch; print(torch.cuda.is_available())"` + verificar que el modelo base se descarga correctamente.

---

### Step 3: Script de Fine-Tuning
**Files:** `training/train.py`
**What:** Script principal de entrenamiento usando `trl.SFTTrainer`:

```python
# Pseudocódigo del flujo
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# 1. Cargar modelo cuantizado
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", ...)
model = AutoModelForCausalLM.from_pretrained(base_model, quantization_config=bnb_config)
model = prepare_model_for_kbit_training(model)

# 2. Aplicar LoRA
lora_config = LoraConfig(r=64, lora_alpha=16, target_modules=[...], ...)
model = get_peft_model(model, lora_config)

# 3. Cargar dataset
dataset = load_dataset("json", data_files="dataset/train.jsonl")

# 4. Formatear en ChatML
def format_chatml(example):
    return f"<|im_start|>system\nEres un experto en SAP2000 API...<|im_end|>\n<|im_start|>user\n{example['instruction']}\n{example.get('input','')}<|im_end|>\n<|im_start|>assistant\n{example['output']}<|im_end|>"

# 5. Entrenar
trainer = SFTTrainer(model=model, train_dataset=dataset, ...)
trainer.train()

# 6. Guardar adaptador LoRA
model.save_pretrained("output/sap2000-coder-lora")
tokenizer.save_pretrained("output/sap2000-coder-lora")
```

**Testing:** Ejecutar entrenamiento con `max_steps=10` para validar que el pipeline funciona antes del entrenamiento completo. Verificar que loss disminuye.

---

### Step 4: Evaluación y Benchmark
**Files:** `training/evaluate.py`, `training/benchmarks/`
**What:** Suite de evaluación para medir la calidad del modelo fine-tuned:

1. **Test set held-out** (10% del dataset): Calcular loss y perplexity
2. **Benchmark funcional** (20 prompts nuevos, no vistos):
   - ¿El código generado es sintácticamente válido?
   - ¿Usa la secuencia correcta de inicialización?
   - ¿Los ByRef se manejan correctamente (raw[-1] = ret_code)?
   - ¿Las unidades se setean antes de geometría?
   - ¿Los nombres de funciones API son correctos?
3. **Comparación base vs fine-tuned**: Mismos 20 prompts con modelo base sin fine-tune
4. **Scoring automático**: Regex-based checks para patrones obligatorios

**Métricas target:**
| Métrica | Base (sin FT) | Target (con FT) |
|---------|---------------|-----------------|
| Sintaxis válida | ~60% | >95% |
| ByRef correcto | ~20% | >85% |
| Secuencia init correcta | ~30% | >90% |
| Funciones API existentes | ~50% | >90% |
| Script ejecutable end-to-end | ~10% | >60% |

**Testing:** Ejecutar benchmark completo, comparar antes/después, documentar resultados.

---

### Step 5: Exportación e Integración
**Files:** `training/export.py`, `training/inference.py`, (opcionalmente `mcp_server/ai_generator.py`)
**What:** Hacer el modelo utilizable:

1. **Merge LoRA → modelo completo** (para GGUF/Ollama):
   ```python
   merged = model.merge_and_unload()
   merged.save_pretrained("output/sap2000-coder-merged")
   ```

2. **Convertir a GGUF** (para inference local con llama.cpp/Ollama):
   ```bash
   python llama.cpp/convert_hf_to_gguf.py output/sap2000-coder-merged --outtype q4_k_m
   # Resultado: ~4.5 GB, ejecutable en CPU o GPU consumer
   ```

3. **Publicar en HuggingFace Hub** (opcional):
   ```python
   model.push_to_hub("tu-usuario/sap2000-coder-7b-qlora")
   ```

4. **Inference local** (script standalone):
   ```python
   # inference.py — generar scripts con el modelo fine-tuned
   from transformers import pipeline
   pipe = pipeline("text-generation", model="output/sap2000-coder-merged", ...)
   result = pipe("Genera una estructura de pórtico 3x3 con vigas HEB300...")
   ```

5. **Integración Ollama** (más práctico para uso diario):
   ```bash
   ollama create sap2000-coder -f Modelfile
   ollama run sap2000-coder "genera una viga simple con carga muerta"
   ```

**Testing:** Generar 5 scripts con el modelo exportado, validar que ejecutan correctamente en SAP2000 vía MCP.

---

### Step 6: [OPCIONAL] Integración con MCP Server
**Files:** `mcp_server/ai_generator.py`, modificación de `mcp_server/server.py`
**What:** Agregar un tool `generate_script_ai` al MCP server que use el modelo local para generar scripts:

```python
@mcp.tool()
async def generate_script_ai(prompt: str, complexity: str = "medium") -> str:
    """Genera un script SAP2000 usando el modelo fine-tuned local."""
    # Llama al modelo via Ollama API o transformers
    # Post-procesa: valida sintaxis, verifica funciones contra registry
    # Retorna código listo para ejecutar con run_sap_script
```

Esto cerraría el loop: **instrucción natural → modelo IA → script generado → ejecución MCP → verificación**

**Testing:** Invocar `generate_script_ai` desde Copilot, ejecutar el script resultante, verificar modelo en SAP2000.

---

## Roadmap Visual

```
Step 1 (Dataset)     Step 2 (Setup)     Step 3 (Train)     Step 4 (Eval)     Step 5 (Export)     Step 6 (Integrate)
┌──────────────┐   ┌─────────────┐   ┌─────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Parse assets │──▸│ pip install  │──▸│ QLoRA train  │──▸│ Benchmark    │──▸│ Merge + GGUF │──▸│ MCP tool     │
│ Generate     │   │ Config YAML │   │ ~1-3 horas   │   │ 20 prompts   │   │ Ollama setup │   │ generate_ai  │
│ ~1000 pairs  │   │ GPU check   │   │ Save adapter │   │ Score >85%   │   │ HF Hub push  │   │ Full loop    │
└──────────────┘   └─────────────┘   └─────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
     ~1 día            ~2 horas          ~3 horas           ~2 horas          ~2 horas           ~4 horas
```

## Notas Importantes

### Hardware mínimo
- **GPU local:** RTX 3060 12GB o superior (QLoRA 4-bit de 7B cabe en ~10 GB VRAM)
- **Sin GPU:** Usa Google Colab Pro ($10/mes) o RunPod ($1.50/hora con A100)
- **Solo CPU:** Puedes hacer inference con GGUF (lento pero funcional). Training NO es viable en CPU.

### Riesgos y mitigaciones
| Riesgo | Mitigación |
|--------|-----------|
| Dataset muy pequeño | Augmentación paramétrica (cambiar valores, secciones, materiales) |
| Overfitting | Early stopping, eval split, regularización dropout 0.05 |
| Modelo genera funciones inventadas | Post-validación contra registry.json |
| Scripts no ejecutan | Pipeline de test automático contra SAP2000 |
| VRAM insuficiente | Reducir batch_size, usar gradient checkpointing, o cloud GPU |

### Expansión futura
- **Fase 2:** Fine-tune con DPO (Direct Preference Optimization) usando feedback de ejecución real
- **Fase 3:** Agente autónomo que genera, ejecuta, evalúa y itera scripts sin intervención
- **Fase 4:** Multi-modal — aceptar screenshots de estructuras y generar el modelo SAP2000
