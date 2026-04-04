"""Audit registry.json and print functions missing signature."""
import json, sys
from pathlib import Path

reg_path = Path(__file__).parent.parent / "registry.json"
with open(reg_path, encoding="utf-8") as f:
    reg = json.load(f)

funcs = reg["functions"]

skipped   = [(k,v) for k,v in funcs.items() if not v.get("signature","") and not v.get("description","") and not v.get("parameter_notes","")]
no_sig_only = [(k,v) for k,v in funcs.items() if not v.get("signature","") and (v.get("description","") or v.get("parameter_notes",""))]

print(f"Total: {len(funcs)}")
print(f"Omitidos por Blockly (sin sig+desc+pn): {len(skipped)}")
print(f"Sin signature pero con desc/pn:          {len(no_sig_only)}")
print()

print("=== OMITIDOS (sin ninguna metadata) ===")
for k, v in skipped:
    print(f"  {k}  cat={v.get('category','')}  ws={v.get('wrapper_script','')}")

print()
print("=== SIN SIGNATURE pero con descripcion/parameter_notes ===")
for k, v in no_sig_only:
    pn = v.get("parameter_notes","")[:80]
    print(f"  {k}")
    if pn:
        print(f"    pn: {pn}")
