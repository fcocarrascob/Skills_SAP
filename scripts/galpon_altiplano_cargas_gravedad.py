# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        galpon_altiplano_cargas_gravedad
# Description: Galpón altiplano — paso 2.4a: estados de carga de gravedad (DSD, LR, SBAL, SUNBI, SUNBD) como cargas nodales en las líneas de costanera, con assert de equilibrio global
# Created:     2026-08-12 18:18:36 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"areas": {"planta": 576.0, "techo_inclinada": 584.8857284461892, "muro_longitudinal": 384.0, "muro_hastial": 434.7821704440379, "muro_total": 818.7821704440379}, "esperado_kN": {"DSD": 302.9638654094505, "LR": 172.79999999999995, "SBAL": 691.1999999999998, "SUNBI": 518.4000000000003, "SUNBD": 518.4000000000003}, "SAP_kN": {"DSD": {"FX": -8.527345496389671e-12, "FY": 1.427746809668014e-13, "FZ": 302.96386540944695}, "LR": {"FX": -7.333529616904144e-12, "FY": 1.195710197521346e-13, "FZ": 172.79999999999686}, "SBAL": {"FX": -2.9334118467616577e-11, "FY": 4.782840790085384e-13, "FZ": 691.1999999999874}, "SUNBI": {"FX": -1.196152447924259e-10, "FY": 1.5076716315426796e-13, "FZ": 518.3999999999965}, "SUNBD": {"FX": 7.584233935320484e-11, "FY": 6.46595013131551e-13, "FZ": 518.399999999986}}, "error_rel": {"DSD": 1.1657341758564144e-14, "LR": 1.787459069646502e-14, "SBAL": 1.787459069646502e-14, "SUNBI": 7.438494264988549e-15, "SUNBD": 2.7644553313166398e-14}, "chequeo_a_mano": {"DSD_techo": 204.71000495616622, "DSD_muro": 98.25386045328455, "LR": 172.79999999999998, "SBAL": 691.1999999999999, "SUNB": 518.4}}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Galpon altiplano — PASO 2.4a: CARGAS DE GRAVEDAD. Corre sobre el modelo ya construido.
# Las costaneras no son barras: se calculan aparte como viga simplemente apoyada de 6,0 m y
# su reaccion entra al dintel como CARGA NODAL en la linea de costanera. La malla del dintel
# se diseno para que esos nodos existan exactamente ahi.
# Distincion que el assert caza: la NIEVE y la SOBRECARGA DE TECHO van por PROYECCION
# HORIZONTAL; la carga muerta superpuesta va por AREA INCLINADA de techo.
import math
def rc(raw): return raw if isinstance(raw, int) else raw[-1]

LUZ, PEND, H_ALERO, SEP, NMARCOS = 24.0, 10.0, 8.0, 6.0, 5
NCOL, NFAL, NPIL = 8, 9, 4
TAN10, COS10 = math.tan(math.radians(PEND)), math.cos(math.radians(PEND))
DX, DZ = (LUZ/2.0)/NFAL, H_ALERO/NCOL
DS, NJ = DX/COS10, 2*NFAL
J_PIL, F_HAS = [3,6,9,12,15], [1,NMARCOS]

# --- Cargas declaradas (estudio de sitio / especificacion de proyecto) ------
D_TECHO = 0.35     # kPa sobre area INCLINADA de techo (panel + costaneras + colgados)
D_MURO  = 0.12     # kPa sobre area de muro
LR      = 0.30     # kPa sobre proyeccion horizontal
S_BAL   = 1.20     # kPa sobre proyeccion horizontal
F_UNB   = 0.50     # faldon descargado de la nieve desbalanceada

def z_roof(j): return H_ALERO + (j if j<=NFAL else NJ-j)*DX*TAN10
def n_roof(f,j): return "R%d_%02d"%(f,j)
def n_col(f,l,k): return n_roof(f, 0 if l=="A" else NJ) if k==NCOL else "K%d%s_%d"%(f,l,k)
def n_pil(f,j,k): return n_roof(f,j) if k==NPIL else "H%d_%02d_%d"%(f,j,k)
def trib_long(f): return SEP/2.0 if f in F_HAS else SEP

def medios(j):
    """Semi-vanos que llegan al nodo j: (ancho_horiz, ancho_incl, faldon)."""
    out = []
    if j >= 1:  out.append((DX/2.0, DS/2.0, "izq" if j <= NFAL   else "der"))
    if j <= NJ-1: out.append((DX/2.0, DS/2.0, "izq" if j <= NFAL-1 else "der"))
    return out

PAT = [("DSD",2), ("LR",3), ("SBAL",7), ("SUNBI",7), ("SUNBD",7)]
assert SapModel.SetModelIsLocked(False) == 0
for nm,_ in PAT:
    try: SapModel.LoadPatterns.Delete(nm)
    except Exception: pass
for nm,tp in PAT:
    assert SapModel.LoadPatterns.Add(nm, tp, 0.0, True) == 0, "add pat "+nm

esperado = {nm: 0.0 for nm,_ in PAT}
def nodal(nodo, pat, P):
    assert rc(SapModel.PointObj.SetLoadForce(nodo, pat, [0.0,0.0,-P,0.0,0.0,0.0], False, "Global")) == 0
    esperado[pat] += P

for f in range(1, NMARCOS+1):
    tl = trib_long(f)
    for j in range(NJ+1):
        ah = sum(h for h,_,_ in medios(j))
        ai = sum(i for _,i,_ in medios(j))
        nodal(n_roof(f,j), "DSD",  D_TECHO * tl * ai)
        nodal(n_roof(f,j), "LR",   LR      * tl * ah)
        nodal(n_roof(f,j), "SBAL", S_BAL   * tl * ah)
        pi = sum(h for h,_,s in medios(j) if s=="izq"); pd = sum(h for h,_,s in medios(j) if s=="der")
        nodal(n_roof(f,j), "SUNBI", S_BAL*tl*(pi + F_UNB*pd))
        nodal(n_roof(f,j), "SUNBD", S_BAL*tl*(F_UNB*pi + pd))

# --- Muros: distribuida sobre columnas (longitudinales) y pilares (hastiales)
def distrib(barra, pat, w):
    assert rc(SapModel.FrameObj.SetLoadDistributed(barra, pat, 1, 10, 0.0, 1.0, w, w, "Global", True, False)) == 0

def area_franja(xa, xb):
    """Area de muro de hastial entre xa y xb: integral de z(x), partida en la cumbrera."""
    def prim(x): return H_ALERO*x + TAN10*x*x/2.0 if x <= LUZ/2.0 else None
    if xb <= LUZ/2.0: return prim(xb) - prim(xa)
    if xa >= LUZ/2.0: return area_franja(LUZ-xb, LUZ-xa)
    return area_franja(xa, LUZ/2.0) + area_franja(LUZ/2.0, xb)

A_muro_long = 0.0
for f in range(1, NMARCOS+1):
    w = D_MURO * trib_long(f)
    for l in ("A","B"):
        for k in range(1, NCOL+1):
            distrib("COL%d%s_%d"%(f,l,k), "DSD", w)
    A_muro_long += 2 * trib_long(f) * H_ALERO
    esperado["DSD"] += 2 * w * H_ALERO

A_muro_hast = 0.0
for f in F_HAS:
    for j in J_PIL:
        A = area_franja(j*DX - 2.0, j*DX + 2.0)
        zt = z_roof(j); w = D_MURO * A / zt
        for k in range(1, NPIL+1): distrib("PIL%d_%02d_%d"%(f,j,k), "DSD", w)
        A_muro_hast += A; esperado["DSD"] += D_MURO * A
    for l,(xa,xb) in (("A",(0.0,2.0)), ("B",(LUZ-2.0,LUZ))):
        A = area_franja(xa,xb); w = D_MURO * A / H_ALERO
        for k in range(1, NCOL+1): distrib("COL%d%s_%d"%(f,l,k), "DSD", w)
        A_muro_hast += A; esperado["DSD"] += D_MURO * A

assert SapModel.File.Save(sap_temp_dir+"\\galpon_altiplano.sdb")==0
assert SapModel.Analyze.RunAnalysis()==0

obtenido, errores = {}, {}
for nm,_ in PAT:
    assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
    assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput(nm))==0
    raw = SapModel.Results.BaseReact(0,[],[],[],[],[],[],[],[],[],0.0,0.0,0.0)
    obtenido[nm] = {"FX":raw[4][0], "FY":raw[5][0], "FZ":raw[6][0]}
    errores[nm] = abs(raw[6][0]/esperado[nm] - 1.0)

A_techo_incl = LUZ/COS10 * (NMARCOS-1)*SEP
result["areas"] = {"planta":576.0, "techo_inclinada":A_techo_incl,
                   "muro_longitudinal":A_muro_long, "muro_hastial":A_muro_hast,
                   "muro_total":A_muro_long+A_muro_hast}
result["esperado_kN"] = esperado
result["SAP_kN"] = obtenido
result["error_rel"] = errores
result["chequeo_a_mano"] = {
    "DSD_techo": D_TECHO*A_techo_incl, "DSD_muro": D_MURO*(A_muro_long+A_muro_hast),
    "LR": LR*576.0, "SBAL": S_BAL*576.0, "SUNB": S_BAL*288.0*(1.0+F_UNB)}
