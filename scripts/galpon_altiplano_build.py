# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        galpon_altiplano_build
# Description: Galpón altiplano — build rev.G autoritativo: incluye el detalle §8.6.4 y la carga muerta de hastial completa
# Created:     2026-08-12 19:39:04 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"conteo": {"nodos": 105, "barras": 188, "bases": 20, "tapered_no_design": 70}, "residuo_max_kN": {"DEAD": 0.0, "DSD": 0.0, "LR": 0.0, "SBAL": 0.0, "SUNBI": 0.0, "SUNBD": 0.0, "WTXP": 0.0, "WTXN": 0.0, "WLYP": 0.0, "WLYN": 0.0, "WPI": 0.0}, "DSD_kN": 302.9638654094505, "masa_sismica_kN": 674.8610909934324, "modal": {"T_estrella_X": 0.8526565963541679, "T_estrella_Y": 0.1610608923144279, "modo_X": 1, "modo_Y": 41, "Ux": 0.9462672299974055, "Uy": 0.47422108045972844, "acum": {"X": 0.9763473474991504, "Y": 0.9782785603899916, "Z": 0.6513158495167387}}, "acero_kg": 23826.406894506235}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Galpon a dos aguas — altiplano (Pica, Tarapaca). NCh2369:2025 + NCh3171:2017 + NCh432:2025.
# BUILD CONSOLIDADO E IDEMPOTENTE — rev.G. Correr despues: galpon_altiplano_espectral.
#
# Criterios de modelado, con su procedencia:
#  - Costaneras FUERA del modelo (viga simple de 6,0 m, calculada aparte). Su carga entra
#    DISTRIBUIDA sobre el dintel, nunca nodal: SAP convierte carga en masa donde la carga esta,
#    y la version nodal concentraba masa en nodos sin atadura -> enjambre de modos locales.
#  - MALLA cortada en las uniones con el arriostramiento de techo (j = 0,3,6,9,12,15,18).
#    Dintel en 6 tramos -> 3 secciones por simetria; columna en 4 -> 4 secciones. SIETE en total.
#  - Se MANTIENE el peralte variable: ningun prismatico equivalente lo reemplaza (subestima el
#    momento de alero 23 % y sobreestima la cumbrera 75 %). La simplificacion del calculo va en
#    la verificacion (2 estaciones por miembro), no en el analisis.
#  - Arriostramiento de techo por §12.1.2 (NORMATIVO), ilustrado por la Fig. A.2 (Anexo A,
#    INFORMATIVO): puntales en las 7 lineas y los 4 vanos; diagonales solo en el anillo.
#  - §8.6.4: las diagonales se conectan en el cruce y SOLO UNA es continua ahi. Las mitades
#    _1 y _4 forman la continua (momento continuo en el cruce); _2 y _3 llegan apernadas.
#    El "punto fijo perpendicular al plano" de la clausula es hipotesis de PANDEO, no un apoyo.
#  - Pilares de hastial de UN elemento, con P liberada arriba (no apuntalan el dintel).
#  - PROHIBIDA la seccion no prismatica de SAP (no reproducible desde rukan).
#  - Tapered con SetDesignProcedure(...,2) = NO DESIGN (AISC 360-22 no tiene capitulo de
#    peralte variable, y SAP tomaria el largo del objeto como largo de pandeo).
# GOTCHA: SetLoadDistributed es fuerza por unidad de largo y los tramos van EN SERIE.
#   Dir 10 = gravedad por largo de barra · Dir 11 = por PROYECCION horizontal · Dir 2 + CSys
#   "Local" = normal al faldon (el eje local 2 del dintel ya es esa normal).
import math
def rc(raw): return raw if isinstance(raw,int) else raw[-1]

LUZ, PEND, H_ALERO, SEP, NMARCOS = 24.0, 10.0, 8.0, 6.0, 5
NCOL, NSEG = 4, 6
TAN10, COS10, SIN10 = math.tan(math.radians(PEND)), math.cos(math.radians(PEND)), math.sin(math.radians(PEND))
NJ, LARGO = 18, (NMARCOS-1)*SEP
DXJ = (LUZ/2.0)/9.0
JS  = [0,3,6,9,12,15,18]
BAYS, BAYS_ARR = [1,2,3,4], [1,4]
J_PIL, F_HAS = [3,6,9,12,15], [1,NMARCOS]
BF, TF, TW = 0.220, 0.012, 0.006
D_BASE, D_ALERO, D_CUMBRE = 0.350, 0.800, 0.350
D_TECHO, D_MURO, LR, S_BAL, F_UNB = 0.35, 0.12, 0.30, 1.20, 0.50
QH = 0.613*1.00*0.95*1.948*0.6362*30.0**2/1000.0
KD, GCPI = 0.85, 0.18
QK = QH*KD
A_ZONA = max(min(0.10*min(LUZ,LARGO), 0.4*H_ALERO), 0.04*min(LUZ,LARGO), 0.9)
PANELES  = [(b,0,3) for b in BAYS] + [(b,15,18) for b in BAYS]
PANELES += [(b,j1,j2) for b in BAYS_ARR for (j1,j2) in ((3,6),(6,9),(9,12),(12,15))]
PUNTALES = [(b,j) for b in BAYS for j in JS]
SEGS = [(JS[i],JS[i+1]) for i in range(NSEG)]

def x_roof(j): return j*DXJ
def z_roof(j): return H_ALERO + (j if j<=9 else NJ-j)*DXJ*TAN10
def y_of(f):   return (f-1)*SEP
def n_roof(f,j): return "R%d_%02d"%(f,j)
def n_col(f,l,k): return n_roof(f, 0 if l=="A" else NJ) if k==NCOL else "K%d%s_%d"%(f,l,k)
def d_col(k): return D_BASE + (D_ALERO-D_BASE)*(k-0.5)/NCOL
def d_din(m): return D_ALERO + (D_CUMBRE-D_ALERO)*(m-0.5)/(NSEG//2)
def m_seg(i):  return i+1 if i < NSEG//2 else NSEG-i
def trib(f):   return SEP/2.0 if f in F_HAS else SEP
def area_franja(xa,xb):
    if xb<=xa: return 0.0
    def prim(x): return H_ALERO*x + TAN10*x*x/2.0
    if xb<=LUZ/2.0: return prim(xb)-prim(xa)
    if xa>=LUZ/2.0: return area_franja(LUZ-xb,LUZ-xa)
    return area_franja(xa,LUZ/2.0)+area_franja(LUZ/2.0,xb)

assert SapModel.InitializeNewModel(6)==0
assert SapModel.File.NewBlank()==0
assert SapModel.PropMaterial.SetMaterial("A36",1)==0
assert SapModel.PropMaterial.SetMPIsotropic("A36",2.0e8,0.3,1.17e-5)==0
assert rc(SapModel.PropMaterial.SetWeightAndMass("A36",1,76.9822))==0
secs=[]
for k in range(1,NCOL+1):
    assert rc(SapModel.PropFrame.SetISection("COL_%d"%k,"A36",d_col(k),BF,TF,TW,BF,TF))==0; secs.append("COL_%d"%k)
for m in range(1,NSEG//2+1):
    assert rc(SapModel.PropFrame.SetISection("DIN_%d"%m,"A36",d_din(m),BF,TF,TW,BF,TF))==0; secs.append("DIN_%d"%m)
for nm,b,t in (("CAJ100X4",0.100,0.004),("CAJ75X4",0.075,0.004),("CAJ125X6",0.125,0.006)):
    assert rc(SapModel.PropFrame.SetTube(nm,"A36",b,b,t,t))==0; secs.append(nm)
assert rc(SapModel.PropFrame.SetISection("PIL400","A36",0.400,0.150,0.008,0.006,0.150,0.008))==0
secs.append("PIL400")
for nm in secs: assert rc(SapModel.PropFrame.SetModifiers(nm,[1.,1e6,1e6,1.,1.,1.,1.,1.]))==0

pts={}
def pt(nm,x,y,z):
    assert rc(SapModel.PointObj.AddCartesian(x,y,z,"",nm))==0; pts[nm]=(x,y,z)
for f in range(1,NMARCOS+1):
    y=y_of(f)
    for j in JS: pt(n_roof(f,j),x_roof(j),y,z_roof(j))
    for l,x in (("A",0.0),("B",LUZ)):
        for k in range(NCOL): pt(n_col(f,l,k),x,y,k*H_ALERO/NCOL)
for f in F_HAS:
    for j in J_PIL: pt("H%d_%02d"%(f,j), x_roof(j), y_of(f), 0.0)
for b in BAYS_ARR:
    for l,x in (("A",0.0),("B",LUZ)): pt("XM%s%d"%(l,b),x,y_of(b)+SEP/2.0,H_ALERO/2.0)
for (b,j1,j2) in PANELES:
    pt("XT%d_%02d"%(b,j1),0.5*(x_roof(j1)+x_roof(j2)),y_of(b)+SEP/2.0,0.5*(z_roof(j1)+z_roof(j2)))

fr={}; tapered=[]
def add(pi,pj,sec,nm):
    assert rc(SapModel.FrameObj.AddByPoint(pi,pj,"",sec,nm))==0,"add "+nm
    fr[nm]=(math.dist(pts[pi],pts[pj]),sec)
REL_M=[False,False,False,False,True,True]; REL_PMM=[True,False,False,False,True,True]
NOREL=[False]*6; Z6=[0.0]*6
def rel(nm,ri,rj): assert rc(SapModel.FrameObj.SetReleases(nm,ri,rj,Z6,Z6))==0,"rel "+nm
for f in range(1,NMARCOS+1):
    for l in ("A","B"):
        for k in range(1,NCOL+1):
            nm="COL%d%s_%d"%(f,l,k); add(n_col(f,l,k-1),n_col(f,l,k),"COL_%d"%k,nm); tapered.append(nm)
    for i,(j1,j2) in enumerate(SEGS):
        nm="DIN%d_%d"%(f,i+1); add(n_roof(f,j1),n_roof(f,j2),"DIN_%d"%m_seg(i),nm); tapered.append(nm)
for (b,j) in PUNTALES:
    nm="PUN%02d_%d"%(j,b); add(n_roof(b,j),n_roof(b+1,j),"CAJ125X6",nm); rel(nm,REL_M,REL_M)
def media(pa,cen,sec,nm,continua):
    add(pa,cen,sec,nm); rel(nm, REL_M, NOREL if continua else REL_M)
for b in BAYS_ARR:
    for l,jj in (("A",0),("B",NJ)):
        cen="XM%s%d"%(l,b)
        media(n_col(b,l,0),  cen,"CAJ100X4","ARW%s%d_1"%(l,b),True )   # diagonal continua
        media(n_roof(b+1,jj),cen,"CAJ100X4","ARW%s%d_4"%(l,b),True )
        media(n_col(b+1,l,0),cen,"CAJ100X4","ARW%s%d_2"%(l,b),False)   # diagonal apernada
        media(n_roof(b,jj),  cen,"CAJ100X4","ARW%s%d_3"%(l,b),False)
for (b,j1,j2) in PANELES:
    cen="XT%d_%02d"%(b,j1)
    media(n_roof(b,j1),  cen,"CAJ75X4","ART%d_%02d_1"%(b,j1),True )
    media(n_roof(b+1,j2),cen,"CAJ75X4","ART%d_%02d_4"%(b,j1),True )
    media(n_roof(b,j2),  cen,"CAJ75X4","ART%d_%02d_2"%(b,j1),False)
    media(n_roof(b+1,j1),cen,"CAJ75X4","ART%d_%02d_3"%(b,j1),False)
for f in F_HAS:
    for j in J_PIL:
        nm="PIL%d_%02d"%(f,j); add("H%d_%02d"%(f,j),n_roof(f,j),"PIL400",nm)
        assert rc(SapModel.FrameObj.SetLocalAxes(nm,90.0))==0; rel(nm,NOREL,REL_PMM)
BASE=[True,True,True,False,False,True]; nb=0
for f in range(1,NMARCOS+1):
    for l in ("A","B"): assert rc(SapModel.PointObj.SetRestraint(n_col(f,l,0),BASE))==0; nb+=1
for f in F_HAS:
    for j in J_PIL: assert rc(SapModel.PointObj.SetRestraint("H%d_%02d"%(f,j),BASE))==0; nb+=1
for nm in tapered: assert rc(SapModel.FrameObj.SetDesignProcedure(nm,2))==0

PAT=[("DSD",2),("LR",3),("SBAL",7),("SUNBI",7),("SUNBD",7),
     ("WTXP",6),("WTXN",6),("WLYP",6),("WLYN",6),("WPI",6)]
for nm,tp in PAT: assert SapModel.LoadPatterns.Add(nm,tp,0.0,True)==0,"pat "+nm
esp={nm:[0.0,0.0,0.0] for nm,_ in PAT}; esp["DEAD"]=[0.0,0.0,0.0]
def dist(barra,pat,direc,w,csys,vec):
    assert rc(SapModel.FrameObj.SetLoadDistributed(barra,pat,1,direc,0.0,1.0,w,w,csys,True,False))==0
    for i in range(3): esp[pat][i]+=vec[i]
NORM={"I":(-SIN10,0.0,COS10),"D":(SIN10,0.0,COS10)}
for f in range(1,NMARCOS+1):
    tl=trib(f)
    for i,(j1,j2) in enumerate(SEGS):
        nm="DIN%d_%d"%(f,i+1); Lm=fr[nm][0]; Lh=(j2-j1)*DXJ; lado="I" if j2<=9 else "D"
        dist(nm,"DSD",10,D_TECHO*tl,"Global",(0,0,-D_TECHO*tl*Lm))
        dist(nm,"LR",11,LR*tl,"Global",(0,0,-LR*tl*Lh))
        dist(nm,"SBAL",11,S_BAL*tl,"Global",(0,0,-S_BAL*tl*Lh))
        for pat,fac in (("SUNBI",1.0 if lado=="I" else F_UNB),("SUNBD",F_UNB if lado=="I" else 1.0)):
            dist(nm,pat,11,S_BAL*fac*tl,"Global",(0,0,-S_BAL*fac*tl*Lh))
    for l in ("A","B"):
        for k in range(1,NCOL+1):
            dist("COL%d%s_%d"%(f,l,k),"DSD",10,D_MURO*tl,"Global",(0,0,-D_MURO*tl*H_ALERO/NCOL))
for f in F_HAS:
    for j in J_PIL:
        A=area_franja(j*DXJ-2.0,j*DXJ+2.0)
        dist("PIL%d_%02d"%(f,j),"DSD",10,D_MURO*A/z_roof(j),"Global",(0,0,-D_MURO*A))
    for l,(xa,xb) in (("A",(0.0,2.0)),("B",(LUZ-2.0,LUZ))):     # revestimiento de esquina
        A=area_franja(xa,xb); w=D_MURO*A/H_ALERO
        for k in range(1,NCOL+1):
            dist("COL%d%s_%d"%(f,l,k),"DSD",10,w,"Global",(0,0,-w*H_ALERO/NCOL))

T05={"1":0.40,"2":-0.69,"3":-0.37,"4":-0.29,"1E":0.61,"2E":-1.07,"3E":-0.53,"4E":-0.43}
T20={"1":0.53,"2":-0.69,"3":-0.48,"4":-0.43,"1E":0.80,"2E":-1.07,"3E":-0.69,"4E":-0.64}
C1={k:T05[k]+(T20[k]-T05[k])*(PEND-5.0)/15.0 for k in T05}
C2={"1":-0.45,"2":-0.69,"3":-0.37,"4":-0.45,"5":0.40,"6":-0.29,
    "1E":-0.48,"2E":-1.07,"3E":-0.53,"4E":-0.48,"5E":0.61,"6E":-0.43}
FRL=2*A_ZONA/LARGO; FRH=area_franja(0.0,A_ZONA)/area_franja(0.0,LUZ)
G1={z:C1[z+"E"]*FRL+C1[z]*(1-FRL) for z in "1234"}
G2={z:C2[z+"E"]*FRL+C2[z]*(1-FRL) for z in "1234"}
G2.update({z:C2[z+"E"]*FRH+C2[z]*(1-FRH) for z in "56"})
VIENTO={"WTXP":{"mA":G1["1"],"mB":G1["4"],"fI":G1["2"],"fD":G1["3"],"h0":None,"h24":None},
        "WTXN":{"mA":G1["4"],"mB":G1["1"],"fI":G1["3"],"fD":G1["2"],"h0":None,"h24":None},
        "WLYP":{"mA":G2["1"],"mB":G2["4"],"fI":G2["2"],"fD":G2["3"],"h0":G2["5"],"h24":G2["6"]},
        "WLYN":{"mA":G2["4"],"mB":G2["1"],"fI":G2["3"],"fD":G2["2"],"h0":G2["6"],"h24":G2["5"]},
        "WPI" :{"mA":-GCPI,"mB":-GCPI,"fI":-GCPI,"fD":-GCPI,"h0":-GCPI,"h24":-GCPI}}
for pat,e in VIENTO.items():
    for f in range(1,NMARCOS+1):
        tl=trib(f)
        for i,(j1,j2) in enumerate(SEGS):
            nm="DIN%d_%d"%(f,i+1); Lm=fr[nm][0]
            g=e["fI"] if j2<=9 else e["fD"]; n=NORM["I" if j2<=9 else "D"]
            w=-QK*g*tl
            dist(nm,pat,2,w,"Local",tuple(w*Lm*n[q] for q in range(3)))
        for cara,l,signo in (("mA","A",1.0),("mB","B",-1.0)):
            g=e[cara]
            if g is None: continue
            w=signo*QK*g*tl
            for k in range(1,NCOL+1): dist("COL%d%s_%d"%(f,l,k),pat,4,w,"Global",(w*H_ALERO/NCOL,0,0))
    for cara,f,signo in (("h0",1,1.0),("h24",NMARCOS,-1.0)):
        g=e[cara]
        if g is None: continue
        for j in J_PIL:
            A=area_franja(j*DXJ-2.0,j*DXJ+2.0)
            dist("PIL%d_%02d"%(f,j),pat,5,signo*QK*g*A/z_roof(j),"Global",(0,signo*QK*g*A,0))
        for l,(xa,xb) in (("A",(0.0,2.0)),("B",(LUZ-2.0,LUZ))):
            A=area_franja(xa,xb); w=signo*QK*g*A/H_ALERO
            for k in range(1,NCOL+1): dist("COL%d%s_%d"%(f,l,k),pat,5,w,"Global",(0,signo*QK*g*A/NCOL,0))

assert rc(SapModel.SourceMass.SetMassSource("MASA_SIS",False,False,True,True,3,
                                            ["DEAD","DSD","SBAL"],[1.0,1.0,0.20]))==0
assert rc(SapModel.LoadCases.ModalEigen.SetCase("MODAL"))==0
assert rc(SapModel.LoadCases.ModalEigen.SetNumberModes("MODAL",60,1))==0
assert SapModel.File.Save(sap_temp_dir+"\\galpon_altiplano.sdb")==0
assert SapModel.Analyze.RunAnalysis()==0

props={nm:SapModel.PropFrame.GetSectProps(nm,0,0,0,0,0,0,0,0,0,0,0,0) for nm in secs}
esp["DEAD"][2]=-sum(props[s][0]*L for (L,s) in fr.values())*76.9822
err={}
for nm in ["DEAD"]+[p for p,_ in PAT]:
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
    assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput(nm))==0
    r=SapModel.Results.BaseReact(0,[],[],[],[],[],[],[],[],[],0.0,0.0,0.0)
    err[nm]=round(max(abs(r[4+i][0]+esp[nm][i]) for i in range(3)),10)
assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL"))==0
T=list(SapModel.Results.ModalPeriod(0,[],[],[],[],[],[])[4])
raw=SapModel.Results.ModalParticipatingMassRatios(0,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[])
ux,uy,sx,sy,sz=list(raw[5]),list(raw[6]),list(raw[8]),list(raw[9]),list(raw[10])
iX=max(range(len(ux)),key=lambda i:ux[i]); iY=max(range(len(uy)),key=lambda i:uy[i])
result["conteo"]={"nodos":len(pts),"barras":len(fr),"bases":nb,"tapered_no_design":len(tapered)}
result["residuo_max_kN"]=err
result["DSD_kN"]=-esp["DSD"][2]
result["masa_sismica_kN"]=-esp["DEAD"][2]-esp["DSD"][2]+0.20*691.2
result["modal"]={"T_estrella_X":T[iX],"T_estrella_Y":T[iY],"modo_X":iX+1,"modo_Y":iY+1,
                 "Ux":ux[iX],"Uy":uy[iY],"acum":{"X":sx[-1],"Y":sy[-1],"Z":sz[-1]}}
result["acero_kg"]=sum(props[s][0]*L for (L,s) in fr.values())*7850.0
