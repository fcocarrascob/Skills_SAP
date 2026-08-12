# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        galpon_altiplano_deriva
# Description: Verificación de la deriva de §6.3: desplazamientos con el espectro de referencia y la simultaneidad de §4.5.2
# Created:     2026-08-12 20:31:07 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"limites": {"alero_0015h": 0.12, "alero_excepcion": 0.24, "cumbrera_0015h": 0.1517388565275237, "cumbrera_excepcion": 0.3034777130550474}, "DES_X_referencia": {"R1_00": {"etq": "alero A marco 1", "h": 8.0, "U1": 0.113469, "U2": 0.001832, "lim_0015h": 0.12, "ratio_U1": 0.9456, "ratio_U2": 0.0153}, "R2_00": {"etq": "alero A marco 2", "h": 8.0, "U1": 0.11348, "U2": 0.001955, "lim_0015h": 0.12, "ratio_U1": 0.9457, "ratio_U2": 0.0163}, "R3_00": {"etq": "alero A marco 3", "h": 8.0, "U1": 0.112442, "U2": 0.002088, "lim_0015h": 0.12, "ratio_U1": 0.937, "ratio_U2": 0.0174}, "R4_00": {"etq": "alero A marco 4", "h": 8.0, "U1": 0.113504, "U2": 0.001946, "lim_0015h": 0.12, "ratio_U1": 0.9459, "ratio_U2": 0.0162}, "R5_00": {"etq": "alero A marco 5", "h": 8.0, "U1": 0.113457, "U2": 0.001825, "lim_0015h": 0.12, "ratio_U1": 0.9455, "ratio_U2": 0.0152}, "R1_18": {"etq": "alero B marco 1", "h": 8.0, "U1": 0.113445, "U2": 0.001831, "lim_0015h": 0.12, "ratio_U1": 0.9454, "ratio_U2": 0.0153}, "R3_18": {"etq": "alero B marco 3", "h": 8.0, "U1": 0.112443, "U2": 0.002088, "lim_0015h": 0.12, "ratio_U1": 0.937, "ratio_U2": 0.0174}, "R5_18": {"etq": "alero B marco 5", "h": 8.0, "U1": 0.113482, "U2": 0.001826, "lim_0015h": 0.12, "ratio_U1": 0.9457, "ratio_U2": 0.0152}, "R1_09": {"etq": "cumbrera marco 1", "h": 10.11592376850158, "U1": 0.112195, "U2": 0.005505, "lim_0015h": 0.151739, "ratio_U1": 0.7394, "ratio_U2": 0.0363}, "R2_09": {"etq": "cumbrera marco 2", "h": 10.11592376850158, "U1": 0.112393, "U2": 0.005533, "lim_0015h": 0.151739, "ratio_U1": 0.7407, "ratio_U2": 0.0365}, "R3_09": {"etq": "cumbrera marco 3", "h": 10.11592376850158, "U1": 0.112605, "U2": 0.005566, "lim_0015h": 0.151739, "ratio_U1": 0.7421, "ratio_U2": 0.0367}, "R4_09": {"etq": "cumbrera marco 4", "h": 10.11592376850158, "U1": 0.112397, "U2": 0.005532, "lim_0015h": 0.151739, "ratio_U1": 0.7407, "ratio_U2": 0.0365}, "R5_09": {"etq": "cumbrera marco 5", "h": 10.11592376850158, "U1": 0.112207, "U2": 0.005505, "lim_0015h": 0.151739, "ratio_U1": 0.7395, "ratio_U2": 0.0363}}, "DES_Y_referencia": {"R1_00": {"etq": "alero A marco 1", "h": 8.0, "U1": 0.038418, "U2": 0.005833, "lim_0015h": 0.12, "ratio_U1": 0.3201, "ratio_U2": 0.0486}, "R2_00": {"etq": "alero A marco 2", "h": 8.0, "U1": 0.037814, "U2": 0.006334, "lim_0015h": 0.12, "ratio_U1": 0.3151, "ratio_U2": 0.0528}, "R3_00": {"etq": "alero A marco 3", "h": 8.0, "U1": 0.033799, "U2": 0.006912, "lim_0015h": 0.12, "ratio_U1": 0.2817, "ratio_U2": 0.0576}, "R4_00": {"etq": "alero A marco 4", "h": 8.0, "U1": 0.037881, "U2": 0.006331, "lim_0015h": 0.12, "ratio_U1": 0.3157, "ratio_U2": 0.0528}, "R5_00": {"etq": "alero A marco 5", "h": 8.0, "U1": 0.0384, "U2": 0.00583, "lim_0015h": 0.12, "ratio_U1": 0.32, "ratio_U2": 0.0486}, "R1_18": {"etq": "alero B marco 1", "h": 8.0, "U1": 0.038398, "U2": 0.005832, "lim_0015h": 0.12, "ratio_U1": 0.32, "ratio_U2": 0.0486}, "R3_18": {"etq": "alero B marco 3", "h": 8.0, "U1": 0.033801, "U2": 0.006912, "lim_0015h": 0.12, "ratio_U1": 0.2817, "ratio_U2": 0.0576}, "R5_18": {"etq": "alero B marco 5", "h": 8.0, "U1": 0.038421, "U2": 0.005831, "lim_0015h": 0.12, "ratio_U1": 0.3202, "ratio_U2": 0.0486}, "R1_09": {"etq": "cumbrera marco 1", "h": 10.11592376850158, "U1": 0.033722, "U2": 0.018094, "lim_0015h": 0.151739, "ratio_U1": 0.2222, "ratio_U2": 0.1192}, "R2_09": {"etq": "cumbrera marco 2", "h": 10.11592376850158, "U1": 0.033782, "U2": 0.018183, "lim_0015h": 0.151739, "ratio_U1": 0.2226, "ratio_U2": 0.1198}, "R3_09": {"etq": "cumbrera marco 3", "h": 10.11592376850158, "U1": 0.033849, "U2": 0.018293, "lim_0015h": 0.151739, "ratio_U1": 0.2231, "ratio_U2": 0.1206}, "R4_09": {"etq": "cumbrera marco 4", "h": 10.11592376850158, "U1": 0.033783, "U2": 0.018183, "lim_0015h": 0.151739, "ratio_U1": 0.2226, "ratio_U2": 0.1198}, "R5_09": {"etq": "cumbrera marco 5", "h": 10.11592376850158, "U1": 0.033726, "U2": 0.018093, "lim_0015h": 0.151739, "ratio_U1": 0.2223, "ratio_U2": 0.1192}}, "contraste_diseno": {"RSX_R4": {"etq": "alero A marco 3", "h": 8.0, "U1": 0.028105, "U2": 4e-06, "lim_0015h": 0.12, "ratio_U1": 0.2342, "ratio_U2": 0.0}, "RSY_R4": {"etq": "alero A marco 3", "h": 8.0, "U1": 1.9e-05, "U2": 0.001804, "lim_0015h": 0.12, "ratio_U1": 0.0002, "ratio_U2": 0.015}}}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Galpon altiplano — DERIVA, NCh2369:2025 §6.
#   §6.1  Los desplazamientos se estiman con el ESPECTRO ELASTICO DE REFERENCIA (sin R*),
#         corregido por la razon de amortiguamiento y ponderado por I, y considerando la
#         simultaneidad direccional de §4.5.2.                       pag. impresa 68
#   §6.3  Estructuras en general: d_max = 0,015 h, con h = altura del nivel o entre dos puntos
#         sobre una misma linea vertical. EXCEPCION: el limite se puede AUMENTAR AL DOBLE si
#         se demuestra que el desplazamiento no compromete la operacion. pag. impresa 69-70
#   §6.4  El efecto P-Delta se debe considerar cuando d excede 0,015 h. pag. impresa 70
import math
def rc(raw): return raw if isinstance(raw,int) else raw[-1]
H_ALERO, FLECHA = 8.0, 2.1159237685015797
Z_CUMBRE = H_ALERO + FLECHA

assert SapModel.SetModelIsLocked(False)==0
for nm in ("DES_X","DES_Y"): SapModel.RespCombo.Delete(nm)
assert rc(SapModel.RespCombo.Add("DES_X",0))==0
assert rc(SapModel.RespCombo.SetCaseList("DES_X",0,"RSX_REF",1.0))==0
assert rc(SapModel.RespCombo.SetCaseList("DES_X",0,"RSY_REF",0.3))==0
assert rc(SapModel.RespCombo.Add("DES_Y",0))==0
assert rc(SapModel.RespCombo.SetCaseList("DES_Y",0,"RSX_REF",0.3))==0
assert rc(SapModel.RespCombo.SetCaseList("DES_Y",0,"RSY_REF",1.0))==0
assert SapModel.File.Save(sap_temp_dir+"\\galpon_altiplano.sdb")==0
assert SapModel.Analyze.RunAnalysis()==0

NODOS=[("R%d_00"%f,"alero A marco %d"%f,H_ALERO) for f in range(1,6)] + \
      [("R%d_18"%f,"alero B marco %d"%f,H_ALERO) for f in (1,3,5)] + \
      [("R%d_09"%f,"cumbrera marco %d"%f,Z_CUMBRE) for f in range(1,6)]

def desplaz(fuente, combo):
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
    if combo: assert rc(SapModel.Results.Setup.SetComboSelectedForOutput(fuente))==0
    else:     assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput(fuente))==0
    o={}
    for nodo,etq,h in NODOS:
        r=SapModel.Results.JointDispl(nodo,0,0,[],[],[],[],[],[],[],[],[])
        if r[-1]!=0 or r[0]==0: continue
        u1=max(abs(v) for v in list(r[6])); u2=max(abs(v) for v in list(r[7]))
        o[nodo]={"etq":etq,"h":h,"U1":round(u1,6),"U2":round(u2,6),
                 "lim_0015h":round(0.015*h,6),
                 "ratio_U1":round(u1/(0.015*h),4),"ratio_U2":round(u2/(0.015*h),4)}
    return o

result["limites"]={"alero_0015h":0.015*H_ALERO,"alero_excepcion":0.030*H_ALERO,
                   "cumbrera_0015h":0.015*Z_CUMBRE,"cumbrera_excepcion":0.030*Z_CUMBRE}
result["DES_X_referencia"]=desplaz("DES_X",True)
result["DES_Y_referencia"]=desplaz("DES_Y",True)
result["contraste_diseno"]={"RSX_R4":desplaz("RSX_R4",False)["R3_00"],
                            "RSY_R4":desplaz("RSY_R4",False)["R3_00"]}
