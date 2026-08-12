# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        galpon_altiplano_espectral
# Description: Recrear espectros y casos RS, y verificar cómo reporta SAP una combinación que contiene un caso espectral
# Created:     2026-08-12 20:10:13 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"T_estrella": {"X": 0.8526565963543608, "Y": 0.16106089231442797}, "R_estrella": {"R4": {"X": 4.0, "Y": 3.8301633726045714}, "R5": {"X": 5.0, "Y": 4.10978297731712}}, "pruebas_combo": {"LinearAdd": {"add": 0, "set_DEAD": 0, "set_RSX": 0}, "RangeAdd": {"add": 0, "set_DEAD": 0, "set_RSX": 0}}, "cabecera": "[StepType, sta, P, V2, M3]", "caso_RSX_R4": {"n": 3, "ret": 0, "filas": [["Max", 0.0, 5.7213, 8.6401, 0.0], ["Max", 1.0, 5.7213, 8.6401, 8.64], ["Max", 2.0, 5.7213, 8.6401, 17.28]]}, "combo_PR0_linearadd": {"n": 6, "ret": 0, "filas": [["Max", 0.0, -17.6091, 1.656, 0.0], ["Max", 1.0, -16.9095, 1.656, 15.624], ["Max", 2.0, -16.2099, 1.656, 31.248], ["Min", 0.0, -29.0517, -15.6241, -0.0], ["Min", 1.0, -28.3521, -15.6241, -1.656], ["Min", 2.0, -27.6524, -15.6241, -3.312]]}, "combo_PR4_rangeadd": {"n": 6, "ret": 0, "filas": [["Max", 0.0, 5.7213, 8.6401, 0.0], ["Max", 1.0, 5.7213, 8.6401, 15.624], ["Max", 2.0, 5.7213, 8.6401, 31.248], ["Min", 0.0, -29.0517, -15.6241, -0.0], ["Min", 1.0, -28.3521, -15.6241, -8.64], ["Min", 2.0, -27.6524, -15.6241, -17.28]]}}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Galpon altiplano — ESPECTROS Y CASOS ESPECTRALES. NCh2369:2025.
# CORRER SIEMPRE DESPUES DE galpon_altiplano_build: aquel hace InitializeNewModel y borra
# los espectros, los casos RS y las combinaciones que este crea.
#   Ec. (3)  S_aH(T) = A_r S [1 + r (T/T0)^p] / [1 + (T/T0)^q]        pag. impresa 29
#   Ec. (1a) S_a(T)  = I S_aH(T)/R* (0,05/xi)^0,4                     pag. impresa 28
#   Ec. (1b) R* con Cr = 0,16 R                                       pag. impresa 28
#   §5.7.1   F_V = +- C_V P, C_V = 1,2 I A_r S/g para suelos A, B y C  pag. impresa 35
# GOTCHAS: SetModelIsLocked(False) borra los resultados -> leer el modal ANTES de desbloquear.
#          DampRatio de FuncRS.SetUser = xi del caso (la curva ya trae el (0,05/xi)^0,4).
import math
def rc(raw): return raw if isinstance(raw,int) else raw[-1]
AR,S,R_PAR,T0,P_PAR,Q_PAR,T1 = 0.42,1.00,4.50,0.30,1.60,3.00,0.27
I_IMP,XI,G = 1.00,0.02,9.80665
FXI=(0.05/XI)**0.4
def sah(t):
    if t<=0: return AR*S
    x=t/T0
    return AR*S*(1.0+R_PAR*x**P_PAR)/(1.0+x**Q_PAR)
def r_star(t,R):
    if R==1: return 1.0
    lim=0.16*R*T1
    return R if t>=lim else 1.5+(R-1.5)*t/lim

assert SapModel.Analyze.RunAnalysis()==0
assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL"))==0
T=list(SapModel.Results.ModalPeriod(0,[],[],[],[],[],[])[4])
raw=SapModel.Results.ModalParticipatingMassRatios(0,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[])
ux,uy=list(raw[5]),list(raw[6])
assert len(T)>0,"modal vacio"
TSX=T[max(range(len(ux)),key=lambda i:ux[i])]
TSY=T[max(range(len(uy)),key=lambda i:uy[i])]
RUTAS={"R4":4.0,"R5":5.0}
RS={k:{"X":r_star(TSX,R),"Y":r_star(TSY,R)} for k,R in RUTAS.items()}

assert SapModel.SetModelIsLocked(False)==0
per=[round(i*0.01,4) for i in range(501)]
def su(n,v): assert rc(SapModel.Func.FuncRS.SetUser(n,len(per),per,v,XI))==0,"func "+n
su("SREF",[I_IMP*sah(t)*FXI for t in per])
for k in RUTAS:
    su("SAX_"+k,[I_IMP*sah(t)/RS[k]["X"]*FXI for t in per])
    su("SAY_"+k,[I_IMP*sah(t)/RS[k]["Y"]*FXI for t in per])
for n,d,f in [("RSX_R4","U1","SAX_R4"),("RSY_R4","U2","SAY_R4"),("RSX_R5","U1","SAX_R5"),
              ("RSY_R5","U2","SAY_R5"),("RSX_REF","U1","SREF"),("RSY_REF","U2","SREF")]:
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetCase(n))==0
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetModalCase(n,"MODAL"))==0
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetModalComb_1(n,1))==0
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetLoads(n,1,[d],[f],[G],["Global"],[0.0]))==0
    assert rc(SapModel.LoadCases.ResponseSpectrum.SetDampConstant(n,XI))==0
CV=1.2*I_IMP*AR*S
assert rc(SapModel.LoadCases.StaticLinear.SetCase("EV"))==0
assert rc(SapModel.LoadCases.StaticLinear.SetLoads("EV",3,["Load"]*3,["DEAD","DSD","SBAL"],[CV,CV,CV*0.20]))==0

# --- Prueba de semantica del signo en una combinacion con caso espectral ---
for nm in ("TT0","TT1","TT2","TT3","TT4","TST_RS","TST_GP","TST_GN"): SapModel.RespCombo.Delete(nm)
pruebas={}
for t,etq in ((0,"LinearAdd"),(4,"RangeAdd")):
    nm="PR%d"%t
    SapModel.RespCombo.Delete(nm)
    a=SapModel.RespCombo.Add(nm,t)
    s1=rc(SapModel.RespCombo.SetCaseList(nm,0,"DEAD",1.2))
    s2=rc(SapModel.RespCombo.SetCaseList(nm,0,"RSX_R4",1.0))
    pruebas[etq]={"add":a,"set_DEAD":s1,"set_RSX":s2}
assert SapModel.File.Save(sap_temp_dir+"\\galpon_altiplano.sdb")==0
assert SapModel.Analyze.RunAnalysis()==0

def leer(nombre,combo):
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
    if combo: assert rc(SapModel.Results.Setup.SetComboSelectedForOutput(nombre))==0
    else:     assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput(nombre))==0
    r=SapModel.Results.FrameForce("COL3A_1",0,0,[],[],[],[],[],[],[],[],[],[],[],[])
    n=r[0]
    return {"n":n,"ret":r[-1],
            "filas":[[r[6][i],round(r[2][i],3),round(r[8][i],4),round(r[9][i],4),round(r[13][i],3)]
                     for i in range(min(n,6))]}
result["T_estrella"]={"X":TSX,"Y":TSY}
result["R_estrella"]=RS
result["pruebas_combo"]=pruebas
result["cabecera"]="[StepType, sta, P, V2, M3]"
result["caso_RSX_R4"]=leer("RSX_R4",False)
result["combo_PR0_linearadd"]=leer("PR0",True)
result["combo_PR4_rangeadd"]=leer("PR4",True)
