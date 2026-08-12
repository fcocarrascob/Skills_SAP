# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        galpon_altiplano_combos
# Description: Galpón altiplano — combinaciones LRFD: NCh3171 §9.1.1 para gravedad y viento, NCh2369 §4.5.1 + §4.5.2 para sismo
# Created:     2026-08-12 20:11:32 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"n_combinaciones": 79, "nombres": ["G1", "G2_B", "G2_I", "G2_D", "G3A_B", "G3A_I", "G3A_D", "G3B_BTXPP", "G4_BTXPP", "G3B_BTXPN", "G4_BTXPN", "G3B_BTXNP", "G4_BTXNP", "G3B_BTXNN", "G4_BTXNN", "G3B_BLYPP", "G4_BLYPP", "G3B_BLYPN", "G4_BLYPN", "G3B_BLYNP", "G4_BLYNP", "G3B_BLYNN", "G4_BLYNN", "G3B_ITXPP", "G4_ITXPP", "G3B_ITXPN", "G4_ITXPN", "G3B_ITXNP", "G4_ITXNP", "G3B_ITXNN", "G4_ITXNN", "G3B_ILYPP", "G4_ILYPP", "G3B_ILYPN", "G4_ILYPN", "G3B_ILYNP", "G4_ILYNP", "G3B_ILYNN", "G4_ILYNN", "G3B_DTXPP", "G4_DTXPP", "G3B_DTXPN", "G4_DTXPN", "G3B_DTXNP", "G4_DTXNP", "G3B_DTXNN", "G4_DTXNN", "G3B_DLYPP", "G4_DLYPP", "G3B_DLYPN", "G4_DLYPN", "G3B_DLYNP", "G4_DLYNP", "G3B_DLYNN", "G4_DLYNN", "G6_TXPP", "G6_TXPN", "G6_TXNP", "G6_TXNN", "G6_LYPP", "G6_LYPN", "G6_LYNP", "G6_LYNN", "E1P_A", "E1P_B", "E1N_A", "E1N_B", "E2P_A", "E2P_B", "E2N_A", "E2N_B", "E3P_A", "E3P_B", "E3N_A", "E3N_B", "R5_1P", "R5_1N", "R5_2P", "R5_2N"], "chequeo_linealidad": {"G1_SAP": [1, [751.269527]], "G1_a_mano": 751.269527, "G3A_B_SAP": [1, [1749.865309]], "G3A_B_a_mano": 1749.865309}, "combo_sismico_muestra": {"E1P_A": [2, [884.23546, 884.213153]], "E1N_A": [2, [680.157466, 680.135159]]}}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Galpon altiplano — COMBINACIONES LRFD. Correr despues de build y de espectral.
#
# Reparto de normas, resuelto por escrito en NCh3171 §9: «Cuando las normas de diseno sismico
# consideren otras combinaciones para casos particulares de cargas, ESTAS PREVALECEN.»
#   - Gravedad y viento: NCh3171 §9.1.1, combinaciones (1) a (7).
#   - Sismo: NCh2369 §4.5.1, que reemplaza la rama sismica. E va con factor 1,0, no 1,4.
#     Con a = 0 (Tabla C-2, techos) y sin SO ni SA quedan `1,2D + E` y `0,9D + E`, mas la
#     nieve concurrente que la (5) de NCh3171 valoriza en 0,2S.
#   - Simultaneidad direccional: NCh2369 §4.5.2, TRES ecuaciones independientes 100/30/30
#     con la vertical adentro (C4.5.2: «no a una eleccion entre las alternativas posibles»).
# L = 0: no hay plataformas. L_r = 0,30 < S = 1,20 siempre, asi que L_r no sobrevive a ninguna
# combinacion donde S este presente; se declara y se omite.
#
# GOTCHA verificado: en una combinacion Linear Additive, SAP aplica el caso ESPECTRAL con
# signo +- automatico y reporta Max/Min. Enumerar sus signos a mano los duplicaria. Solo hay
# que enumerar el signo de los casos ESTATICOS: EV (vertical de §5.7.1) y WPI (presion interna).
def rc(raw): return raw if isinstance(raw,int) else raw[-1]
assert SapModel.SetModelIsLocked(False)==0
viejos=list(SapModel.RespCombo.GetNameList()[1]) if SapModel.RespCombo.GetNameList()[0] else []
for nm in viejos: SapModel.RespCombo.Delete(nm)

D=[("DEAD",1.0),("DSD",1.0)]
NIEVE={"B":"SBAL","I":"SUNBI","D":"SUNBD"}
VIENTOS=["WTXP","WTXN","WLYP","WLYN"]
creadas=[]
def combo(nm, items):
    assert rc(SapModel.RespCombo.Add(nm,0))==0, "add "+nm
    for caso,f in items:
        assert rc(SapModel.RespCombo.SetCaseList(nm,0,caso,f))==0, "set %s %s"%(nm,caso)
    creadas.append(nm)
def esc(base,f): return [(c,f*k) for c,k in base]

# (1) 1,4D
combo("G1", esc(D,1.4))
# (2) 1,2D + 1,6L + 0,5(L_r o S)  con L = 0
for s,pat in NIEVE.items():
    combo("G2_%s"%s, esc(D,1.2)+[(pat,0.5)])
# (3a) 1,2D + 1,6(L_r o S) + L
for s,pat in NIEVE.items():
    combo("G3A_%s"%s, esc(D,1.2)+[(pat,1.6)])
# (3b) 1,2D + 1,6(L_r o S) + 0,8W     y     (4) 1,2D + 1,6W + L + 0,5(L_r o S)
for s,pat in NIEVE.items():
    for w in VIENTOS:
        for sg,et in ((1.0,"P"),(-1.0,"N")):
            combo("G3B_%s%s%s"%(s,w[1:],et), esc(D,1.2)+[(pat,1.6),(w,0.8),("WPI",0.8*sg)])
            combo("G4_%s%s%s"%(s,w[1:],et),  esc(D,1.2)+[(pat,0.5),(w,1.6),("WPI",1.6*sg)])
# (6) 0,9D + 1,6W
for w in VIENTOS:
    for sg,et in ((1.0,"P"),(-1.0,"N")):
        combo("G6_%s%s"%(w[1:],et), esc(D,0.9)+[(w,1.6),("WPI",1.6*sg)])

# Sismo: NCh2369 §4.5.1 con la simultaneidad de §4.5.2. Los RS entran sin signo (SAP los da +-);
# EV, que es estatico, se enumera.
EQ=[("1",1.0,0.3,0.3), ("2",0.3,1.0,0.3), ("3",0.3,0.3,1.0)]
GRAV=[("A", esc(D,1.2)+[("SBAL",0.2)]), ("B", esc(D,0.9))]
for eq,fx,fy,fz in EQ:
    for sg,et in ((1.0,"P"),(-1.0,"N")):
        for g,base in GRAV:
            combo("E%s%s_%s"%(eq,et,g), base+[("RSX_R4",fx),("RSY_R4",fy),("EV",fz*sg)])
# Rama ilustrativa con R = 5 (fila 5.5), solo la ecuacion 1 y 2 para comparar
for eq,fx,fy,fz in EQ[:2]:
    for sg,et in ((1.0,"P"),(-1.0,"N")):
        combo("R5_%s%s"%(eq,et), esc(D,1.2)+[("SBAL",0.2),("RSX_R5",fx),("RSY_R5",fy),("EV",fz*sg)])

assert SapModel.File.Save(sap_temp_dir+"\\galpon_altiplano.sdb")==0
assert SapModel.Analyze.RunAnalysis()==0

# Verificacion de linealidad: G1 debe dar exactamente 1,4 x (DEAD+DSD) en reaccion vertical
def rz_caso(n):
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
    assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput(n))==0
    return SapModel.Results.BaseReact(0,[],[],[],[],[],[],[],[],[],0.0,0.0,0.0)[6][0]
def rz_combo(n):
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
    assert rc(SapModel.Results.Setup.SetComboSelectedForOutput(n))==0
    b=SapModel.Results.BaseReact(0,[],[],[],[],[],[],[],[],[],0.0,0.0,0.0)
    return [b[0], [round(v,6) for v in list(b[6])]]
dead,dsd,sbal=rz_caso("DEAD"),rz_caso("DSD"),rz_caso("SBAL")
result["n_combinaciones"]=len(creadas)
result["nombres"]=creadas
result["chequeo_linealidad"]={
  "G1_SAP":rz_combo("G1"), "G1_a_mano":round(1.4*(dead+dsd),6),
  "G3A_B_SAP":rz_combo("G3A_B"), "G3A_B_a_mano":round(1.2*(dead+dsd)+1.6*sbal,6)}
result["combo_sismico_muestra"]={"E1P_A":rz_combo("E1P_A"), "E1N_A":rz_combo("E1N_A")}
