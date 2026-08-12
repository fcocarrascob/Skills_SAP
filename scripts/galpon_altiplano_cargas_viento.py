# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        galpon_altiplano_cargas_viento
# Description: Galpón altiplano — paso 2.4b simplificado: presión pareja por cara con GC_pf promediado por área, cuatro estados externos más el interno
# Created:     2026-08-12 18:53:32 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"parametros": {"q_h_kPa": 0.6495449439239999, "q_h_Kd_kPa": 0.5521132023353998, "a_m": 2.4000000000000004, "fr_E_muro_techo": 0.20000000000000004, "fr_E_hastial": 0.09065607121981573, "A_hastial": 217.39108522201894}, "GC_promediado": {"caso1": {"1": 0.4893333, "2": -0.766, "3": -0.442, "4": -0.3693333}, "caso2": {"1": -0.456, "2": -0.766, "3": -0.402, "4": -0.456, "5": 0.4190378, "6": -0.3026918}}, "p_kPa": {"caso1": {"1": 0.2701674, "2": -0.4229187, "3": -0.244034, "4": -0.2039138}, "caso2": {"1": -0.2517636, "2": -0.4229187, "3": -0.2219495, "4": -0.2517636, "5": 0.2313563, "6": -0.1671202}, "interna": 0.0993804}, "resultante_analitica_kN": {"WTXP": [81.939439, 0.0, 192.082392], "WTXN": [-81.939439, 0.0, 192.082392], "WLYP": [-10.205652, 86.625229, 185.722047], "WLYN": [10.205652, -86.625229, 185.722047], "WPI": [0.0, 0.0, 57.243097]}, "reaccion_SAP_kN": {"WTXP": [-81.939439, -0.0, -192.082392], "WTXN": [81.939439, 0.0, -192.082392], "WLYP": [10.205652, -86.625229, -185.722047], "WLYN": [-10.205652, 86.625229, -185.722047], "WPI": [0.0, -0.0, -57.243097]}, "residuo_abs_kN": {"WTXP": [0.0, 0.0, 0.0], "WTXN": [0.0, 0.0, 0.0], "WLYP": [0.0, 0.0, 0.0], "WLYN": [0.0, 0.0, 0.0], "WPI": [0.0, 0.0, 0.0]}, "chequeos_a_mano": {"WPI_Fz": -57.243096818134255, "WTXP_Fx_muros": 91.02359098982336, "WTXP_Fz_techo": 192.08239154529497, "WLYP_Fy_hastiales": 86.62522886585951, "minimo_muro_0_25": 0.3695477700964943}}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Galpon altiplano — PASO 2.4b: VIENTO, NCh432:2025 clausula 7 (procedimiento envolvente).
#   p = q_h * K_d * [(GCpf) - (GCpi)]                                    Ec. (7), §7.3.1
#
# SIMPLIFICACION DECLARADA: presion PAREJA por cara. El GCpf de cada cara es el promedio
# PONDERADO POR AREA entre su zona normal y su franja de esquina (E). Con eso la resultante
# sobre cada cara es identica a la de la norma —el corte total de §7.3.3 y el equilibrio
# global siguen exactos— y lo unico que se pierde es la concentracion local de la esquina,
# que es materia de componentes y revestimientos (clausula 9), no del SPRFV.
# La presion INTERNA va en su propio patron (WPI, GC = -GCpi): las combinaciones lo toman +-1.
# Casos de torsion EXENTOS: §7.3.2 excepcion 1 (un piso, h = 8,0 m <= 9 m).
# h = altura del ALERO porque theta <= 10° (notacion de la Figura 12).
# GOTCHAS:
#  - SetLoadDistributed toma FUERZA POR UNIDAD DE LARGO. Los 8 tramos de una columna van EN
#    SERIE: cada uno lleva el w completo, no w/8.
#  - LoadPatterns.Delete no saca un patron que ya tiene resultados. Se reusa el patron y se
#    borran sus asignaciones con PointObj.DeleteLoadForce / FrameObj.DeleteLoadDistributed.
import math
def rc(raw): return raw if isinstance(raw,int) else raw[-1]

LUZ, PEND, H_ALERO, SEP, NMARCOS = 24.0, 10.0, 8.0, 6.0, 5
NCOL, NFAL = 8, 9
TAN10, COS10, SIN10 = math.tan(math.radians(PEND)), math.cos(math.radians(PEND)), math.sin(math.radians(PEND))
DX, DS, NJ = (LUZ/2.0)/NFAL, (LUZ/2.0)/NFAL/COS10, 2*NFAL
LARGO = (NMARCOS-1)*SEP
J_PIL, F_HAS = [3,6,9,12,15], [1,NMARCOS]

QH   = 0.613*1.00*0.95*1.948*0.6362*30.0**2/1000.0     # kPa, sin K_d
KD, GCPI = 0.85, 0.18
QK   = QH*KD
A_ZONA = max(min(0.10*min(LUZ,LARGO), 0.4*H_ALERO), 0.04*min(LUZ,LARGO), 0.9)

def area_franja(xa,xb):
    if xb<=xa: return 0.0
    def prim(x): return H_ALERO*x + TAN10*x*x/2.0
    if xb<=LUZ/2.0: return prim(xb)-prim(xa)
    if xa>=LUZ/2.0: return area_franja(LUZ-xb,LUZ-xa)
    return area_franja(xa,LUZ/2.0)+area_franja(LUZ/2.0,xb)
A_HASTIAL = area_franja(0.0,LUZ)
FR_E_LARGO = 2*A_ZONA/LARGO                       # 4,80 / 24,0
FR_E_HAST  = area_franja(0.0,A_ZONA)/A_HASTIAL    # por AREA, la altura del muro varia

T05 = {"1":0.40,"2":-0.69,"3":-0.37,"4":-0.29,"1E":0.61,"2E":-1.07,"3E":-0.53,"4E":-0.43}
T20 = {"1":0.53,"2":-0.69,"3":-0.48,"4":-0.43,"1E":0.80,"2E":-1.07,"3E":-0.69,"4E":-0.64}
FI  = (PEND-5.0)/(20.0-5.0)
C1  = {k: T05[k]+(T20[k]-T05[k])*FI for k in T05}
C2  = {"1":-0.45,"2":-0.69,"3":-0.37,"4":-0.45,"5":0.40,"6":-0.29,
       "1E":-0.48,"2E":-1.07,"3E":-0.53,"4E":-0.48,"5E":0.61,"6E":-0.43}
def prom(t,z,fr): return t[z+"E"]*fr + t[z]*(1.0-fr)
G1 = {z: prom(C1,z,FR_E_LARGO) for z in ("1","2","3","4")}
G2 = {z: prom(C2,z,FR_E_LARGO) for z in ("1","2","3","4")}
G2.update({z: prom(C2,z,FR_E_HAST) for z in ("5","6")})

# Cada estado: GCpf uniforme por cara. muroA = x=0, muroB = x=24, h0 = y=0, h24 = y=24.
ESTADOS = {
 "WTXP": {"muroA":G1["1"], "muroB":G1["4"], "faldI":G1["2"], "faldD":G1["3"], "h0":None, "h24":None},
 "WTXN": {"muroA":G1["4"], "muroB":G1["1"], "faldI":G1["3"], "faldD":G1["2"], "h0":None, "h24":None},
 "WLYP": {"muroA":G2["1"], "muroB":G2["4"], "faldI":G2["2"], "faldD":G2["3"], "h0":G2["5"], "h24":G2["6"]},
 "WLYN": {"muroA":G2["4"], "muroB":G2["1"], "faldI":G2["3"], "faldD":G2["2"], "h0":G2["6"], "h24":G2["5"]},
 "WPI" : {"muroA":-GCPI, "muroB":-GCPI, "faldI":-GCPI, "faldD":-GCPI, "h0":-GCPI, "h24":-GCPI},
}
PATS = list(ESTADOS.keys())

def z_roof(j): return H_ALERO + (j if j<=NFAL else NJ-j)*DX*TAN10
def y_of(f):   return (f-1)*SEP
def n_roof(f,j): return "R%d_%02d"%(f,j)
def trib_long(f): return SEP/2.0 if f in F_HAS else SEP
def medios(j):
    out=[]
    if j>=1:    out.append((DS/2.0,"faldI" if j<=NFAL   else "faldD"))
    if j<=NJ-1: out.append((DS/2.0,"faldI" if j<=NFAL-1 else "faldD"))
    return out
DIR = {"faldI":(SIN10,0.0,-COS10), "faldD":(-SIN10,0.0,-COS10)}

assert SapModel.SetModelIsLocked(False)==0
raw = SapModel.LoadPatterns.GetNameList()
existentes = set(raw[1])
for nm in PATS:
    if nm in existentes:
        try: SapModel.PointObj.DeleteLoadForce("ALL", nm, 1)
        except Exception: pass
        try: SapModel.FrameObj.DeleteLoadDistributed("ALL", nm, 1)
        except Exception: pass
    else:
        assert SapModel.LoadPatterns.Add(nm, 6, 0.0, True)==0, "pat "+nm

esp = {nm:[0.0,0.0,0.0] for nm in PATS}
def nodal(nodo,pat,F):
    assert rc(SapModel.PointObj.SetLoadForce(nodo,pat,[F[0],F[1],F[2],0.,0.,0.],False,"Global"))==0
    for i in range(3): esp[pat][i]+=F[i]
def distrib(barra,pat,direc,w,l_elem):
    assert rc(SapModel.FrameObj.SetLoadDistributed(barra,pat,1,direc,0.0,1.0,w,w,"Global",True,False))==0
    esp[pat][direc-4] += w*l_elem

for pat in PATS:
    e = ESTADOS[pat]
    for f in range(1,NMARCOS+1):
        tl = trib_long(f)
        for j in range(NJ+1):                                   # techo: nodal, area inclinada
            F=[0.0,0.0,0.0]
            for (ai,cara) in medios(j):
                g = e[cara]
                if g is None: continue
                pA = QK*g*ai*tl; d = DIR[cara]
                for i in range(3): F[i]+=pA*d[i]
            if abs(F[0])+abs(F[1])+abs(F[2])>0: nodal(n_roof(f,j),pat,F)
        for cara,l,signo in (("muroA","A",+1.0),("muroB","B",-1.0)):   # muros largos
            g = e[cara]
            if g is None: continue
            w = signo*QK*g*tl
            for k in range(1,NCOL+1): distrib("COL%d%s_%d"%(f,l,k),pat,4,w,H_ALERO/NCOL)
    for cara,f,signo in (("h0",1,+1.0),("h24",NMARCOS,-1.0)):          # hastiales
        g = e[cara]
        if g is None: continue
        for j in J_PIL:
            A = area_franja(j*DX-2.0, j*DX+2.0); zt = z_roof(j)
            distrib("PIL%d_%02d"%(f,j),pat,5,signo*QK*g*A/zt,zt)
        for l,(xa,xb) in (("A",(0.0,2.0)),("B",(LUZ-2.0,LUZ))):
            A = area_franja(xa,xb); w = signo*QK*g*A/H_ALERO
            for k in range(1,NCOL+1): distrib("COL%d%s_%d"%(f,l,k),pat,5,w,H_ALERO/NCOL)

assert SapModel.File.Save(sap_temp_dir+"\\galpon_altiplano.sdb")==0
assert SapModel.Analyze.RunAnalysis()==0
obt,err={},{}
for nm in PATS:
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
    assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput(nm))==0
    r = SapModel.Results.BaseReact(0,[],[],[],[],[],[],[],[],[],0.0,0.0,0.0)
    obt[nm]=[r[4][0],r[5][0],r[6][0]]
    err[nm]=[abs(obt[nm][i]+esp[nm][i]) for i in range(3)]

A_TECHO = LUZ/COS10*LARGO
result["parametros"]={"q_h_kPa":QH,"q_h_Kd_kPa":QK,"a_m":A_ZONA,
                      "fr_E_muro_techo":FR_E_LARGO,"fr_E_hastial":FR_E_HAST,"A_hastial":A_HASTIAL}
result["GC_promediado"]={"caso1":{k:round(v,7) for k,v in G1.items()},
                         "caso2":{k:round(v,7) for k,v in G2.items()}}
result["p_kPa"]={"caso1":{k:round(QK*v,7) for k,v in G1.items()},
                 "caso2":{k:round(QK*v,7) for k,v in G2.items()},
                 "interna":round(QK*GCPI,7)}
result["resultante_analitica_kN"]={k:[round(v,6) for v in esp[k]] for k in PATS}
result["reaccion_SAP_kN"]={k:[round(v,6) for v in obt[k]] for k in PATS}
result["residuo_abs_kN"]={k:[round(v,10) for v in err[k]] for k in PATS}
result["chequeos_a_mano"]={
  "WPI_Fz": -QK*GCPI*LUZ*LARGO,
  "WTXP_Fx_muros": QK*(G1["1"]-G1["4"])*LARGO*H_ALERO,
  "WTXP_Fz_techo": -QK*(G1["2"]+G1["3"])*A_TECHO/2.0*COS10,
  "WLYP_Fy_hastiales": QK*(G2["5"]-G2["6"])*A_HASTIAL,
  "minimo_muro_0_25": QK*(G1["1"]+GCPI)}
