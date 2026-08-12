# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        galpon_altiplano_envolvente
# Description: Envolventes (total, gravedad+viento, sísmica) y extracción del combo gobernante por miembro
# Created:     2026-08-12 20:15:52 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"n_combos_en_ENV": {"ENV": 79, "ENVG": 63, "ENVE": 12, "ENVR5": 4}, "gobernantes": {"COL3A_1": {"etiqueta": "columna base", "n_resultados": 285, "M3_max": 158.321, "combo_M3": "G3A_B", "P_comp": -190.14, "combo_P_comp": "G3A_B", "P_trac": 13.964, "combo_P_trac": "G6_TXPP"}, "COL3A_4": {"etiqueta": "columna alero", "n_resultados": 285, "M3_max": 633.284, "combo_M3": "G3A_B", "P_comp": -180.384, "combo_P_comp": "G3A_B", "P_trac": 21.562, "combo_P_trac": "G6_TXPP"}, "DIN3_1": {"etiqueta": "dintel alero", "n_resultados": 285, "M3_max": -633.206, "combo_M3": "G3A_B", "P_comp": -136.003, "combo_P_comp": "G3A_B", "P_trac": 24.78, "combo_P_trac": "G6_LYNP"}, "DIN3_2": {"etiqueta": "dintel medio", "n_resultados": 285, "M3_max": 176.334, "combo_M3": "G3A_I", "P_comp": -148.067, "combo_P_comp": "G3A_B", "P_trac": 30.587, "combo_P_trac": "G6_LYNP"}, "DIN3_3": {"etiqueta": "dintel cumbrera", "n_resultados": 285, "M3_max": 207.932, "combo_M3": "G3A_B", "P_comp": -137.454, "combo_P_comp": "G3A_B", "P_trac": 32.502, "combo_P_trac": "G6_LYNP"}, "PUN00_1": {"etiqueta": "puntal alero", "n_resultados": 1235, "M3_max": 1.686, "combo_M3": "E3P_A", "P_comp": -16.113, "combo_P_comp": "E2N_B", "P_trac": 28.248, "combo_P_trac": "E2P_A"}, "PUN09_2": {"etiqueta": "puntal cumbrera", "n_resultados": 1235, "M3_max": 1.686, "combo_M3": "E3P_A", "P_comp": -96.087, "combo_P_comp": "G3A_B", "P_trac": 14.959, "combo_P_trac": "G6_TXNP"}, "ARWA1_1": {"etiqueta": "media diag. muro", "n_resultados": 285, "M3_max": -0.384, "combo_M3": "E3P_A", "P_comp": -39.895, "combo_P_comp": "E2P_A", "P_trac": 23.651, "combo_P_trac": "E2N_B"}, "ART1_00_1": {"etiqueta": "media diag. techo", "n_resultados": 285, "M3_max": 2.014, "combo_M3": "E3P_A", "P_comp": -28.234, "combo_P_comp": "G3A_B", "P_trac": 15.007, "combo_P_trac": "E2N_B"}, "PIL1_06": {"etiqueta": "pilar hastial", "n_resultados": 285, "M3_max": -23.432, "combo_M3": "G4_BLYPN", "P_comp": -13.504, "combo_P_comp": "E3P_A", "P_trac": 0.0, "combo_P_trac": "E3N_A"}}, "ENV": {"COL3A_1": {"P_min": -190.14, "P_max": 13.964, "M3_abs": 158.321}, "COL3A_4": {"P_min": -180.384, "P_max": 21.562, "M3_abs": 633.284}, "DIN3_1": {"P_min": -136.003, "P_max": 24.78, "M3_abs": 633.206}, "DIN3_2": {"P_min": -148.067, "P_max": 30.587, "M3_abs": 176.334}, "DIN3_3": {"P_min": -137.454, "P_max": 32.502, "M3_abs": 207.932}, "PUN00_1": {"P_min": -16.113, "P_max": 28.248, "M3_abs": 1.686}, "PUN09_2": {"P_min": -96.087, "P_max": 14.959, "M3_abs": 1.686}, "ARWA1_1": {"P_min": -39.895, "P_max": 23.651, "M3_abs": 0.384}, "ART1_00_1": {"P_min": -28.234, "P_max": 15.007, "M3_abs": 2.014}, "PIL1_06": {"P_min": -13.504, "P_max": 0.0, "M3_abs": 23.432}}, "ENVG_gravedad_viento": {"COL3A_1": {"P_min": -190.14, "P_max": 13.964, "M3_abs": 158.321}, "COL3A_4": {"P_min": -180.384, "P_max": 21.562, "M3_abs": 633.284}, "DIN3_1": {"P_min": -136.003, "P_max": 24.78, "M3_abs": 633.206}, "DIN3_2": {"P_min": -148.067, "P_max": 30.587, "M3_abs": 176.334}, "DIN3_3": {"P_min": -137.454, "P_max": 32.502, "M3_abs": 207.932}, "PUN00_1": {"P_min": -5.756, "P_max": 23.96, "M3_abs": 1.385}, "PUN09_2": {"P_min": -96.087, "P_max": 14.959, "M3_abs": 1.385}, "ARWA1_1": {"P_min": -34.233, "P_max": 16.385, "M3_abs": 0.312}, "ART1_00_1": {"P_min": -28.234, "P_max": 3.675, "M3_abs": 1.57}, "PIL1_06": {"P_min": -11.095, "P_max": 0.0, "M3_abs": 23.432}}, "ENVE_sismo": {"COL3A_1": {"P_min": -110.549, "P_max": -8.555, "M3_abs": 84.486}, "COL3A_4": {"P_min": -96.694, "P_max": -5.213, "M3_abs": 337.165}, "DIN3_1": {"P_min": -66.818, "P_max": -1.34, "M3_abs": 337.098}, "DIN3_2": {"P_min": -69.576, "P_max": -1.585, "M3_abs": 92.165}, "DIN3_3": {"P_min": -63.525, "P_max": -2.084, "M3_abs": 108.078}, "PUN00_1": {"P_min": -16.113, "P_max": 28.248, "M3_abs": 1.686}, "PUN09_2": {"P_min": -42.734, "P_max": -0.645, "M3_abs": 1.686}, "ARWA1_1": {"P_min": -39.895, "P_max": 23.651, "M3_abs": 0.384}, "ART1_00_1": {"P_min": -28.215, "P_max": 15.007, "M3_abs": 2.014}, "PIL1_06": {"P_min": -13.504, "P_max": 0.0, "M3_abs": 0.0}}}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Galpon altiplano — ENVOLVENTES Y GOBERNANTES. Correr despues de build, espectral y combos.
# Una combinacion de tipo Envelope (RespCombo.Add(nm,1)) puede contener OTRAS combinaciones:
# se agregan con SetCaseList(..., CType=1, ...). Y si se seleccionan todas las combos para
# salida a la vez, FrameForce devuelve en su arreglo LoadCase EL NOMBRE de la que produjo cada
# valor — que es lo que permite armar la matriz de gobernantes sin iterar combo por combo.
def rc(raw): return raw if isinstance(raw,int) else raw[-1]
assert SapModel.SetModelIsLocked(False)==0
todos=[c for c in list(SapModel.RespCombo.GetNameList()[1]) if not c.startswith("ENV")]
for nm in ("ENV","ENVG","ENVE","ENVR5"): SapModel.RespCombo.Delete(nm)
grupos={"ENV":  [c for c in todos],
        "ENVG": [c for c in todos if c.startswith("G")],
        "ENVE": [c for c in todos if c.startswith("E")],
        "ENVR5":[c for c in todos if c.startswith("R5")]}
for nm,lista in grupos.items():
    assert rc(SapModel.RespCombo.Add(nm,1))==0, "add "+nm          # 1 = Envelope
    for c in lista:
        assert rc(SapModel.RespCombo.SetCaseList(nm,1,c,1.0))==0, "set %s <- %s"%(nm,c)
assert SapModel.File.Save(sap_temp_dir+"\\galpon_altiplano.sdb")==0
assert SapModel.Analyze.RunAnalysis()==0

MIEMBROS=[("COL3A_1","columna base"),("COL3A_4","columna alero"),
          ("DIN3_1","dintel alero"),("DIN3_2","dintel medio"),("DIN3_3","dintel cumbrera"),
          ("PUN00_1","puntal alero"),("PUN09_2","puntal cumbrera"),
          ("ARWA1_1","media diag. muro"),("ART1_00_1","media diag. techo"),
          ("PIL1_06","pilar hastial")]

def envolvente(nombre_combo):
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
    assert rc(SapModel.Results.Setup.SetComboSelectedForOutput(nombre_combo))==0
    out={}
    for nm,etq in MIEMBROS:
        r=SapModel.Results.FrameForce(nm,0,0,[],[],[],[],[],[],[],[],[],[],[],[])
        if r[-1]!=0 or r[0]==0: continue
        P,M3=list(r[8]),list(r[13])
        out[nm]={"P_min":round(min(P),3),"P_max":round(max(P),3),
                 "M3_abs":round(max(abs(v) for v in M3),3)}
    return out

# Gobernantes: todas las combos seleccionadas a la vez; el arreglo LoadCase dice cual manda.
assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
for c in todos: assert rc(SapModel.Results.Setup.SetComboSelectedForOutput(c))==0
gob={}
for nm,etq in MIEMBROS:
    r=SapModel.Results.FrameForce(nm,0,0,[],[],[],[],[],[],[],[],[],[],[],[])
    if r[-1]!=0 or r[0]==0: continue
    caso,P,M3=list(r[5]),list(r[8]),list(r[13])
    iM=max(range(len(M3)),key=lambda i:abs(M3[i]))
    iC=min(range(len(P)),key=lambda i:P[i])          # mas comprimido
    iT=max(range(len(P)),key=lambda i:P[i])          # mas traccionado
    gob[nm]={"etiqueta":etq,"n_resultados":r[0],
             "M3_max":round(M3[iM],3),"combo_M3":caso[iM],
             "P_comp":round(P[iC],3),"combo_P_comp":caso[iC],
             "P_trac":round(P[iT],3),"combo_P_trac":caso[iT]}
result["n_combos_en_ENV"]={k:len(v) for k,v in grupos.items()}
result["gobernantes"]=gob
result["ENV"]=envolvente("ENV")
result["ENVG_gravedad_viento"]=envolvente("ENVG")
result["ENVE_sismo"]=envolvente("ENVE")
