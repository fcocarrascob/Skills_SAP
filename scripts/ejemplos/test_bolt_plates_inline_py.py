# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        test_bolt_plates_inline_py
# Description: 
# Created:     2026-03-30 01:52:47 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"sep": 16.0, "n_pts": 96, "n_areas": 72, "n_links": 48, "areas_expected": 72, "links_expected": 48, "all_ok": true}
# Tags:        
# ──────────────────────────────────────────────────────────────


# test_bolt_plates_inline.py
# Valida la lógica completa de BoltPlatesBackend inline (sin importar el módulo).
# Parámetros: t1=20, t2=12 → sep=16, ∅perno=27, exterior Cuadrado 90, 12×3 anillos, plano XY.
import math

GAP_PROP   = "GAP_BOLT_INLINE"
AREA_PROP  = "Default"
T1, T2     = 20.0, 12.0
SEP        = (T1 + T2) / 2.0
BOLT_D     = 27.0
OUTER_D    = 90.0
OUTER_S    = "Cuadrado"
NA, NR     = 12, 3
CX, CY, CZ = 500.0, 500.0, 0.0
K_GAP      = 2.0e6

# ── Fase 1: Propiedad Gap ─────────────────────────────────────────────────────
dof=  [True, False,False,False,False,False]
fix=  [False,False,False,False,False,False]
nl=   [True, False,False,False,False,False]
ke=   [K_GAP,0,0,0,0,0]
ce=   [0,0,0,0,0,0]
k_nl= [K_GAP,0,0,0,0,0]
d_nl= [0,0,0,0,0,0]
rg = SapModel.PropLink.SetGap(GAP_PROP, dof, fix, nl, ke, ce, k_nl, d_nl, 0.0, 0.0)
assert (int(rg[-1]) if isinstance(rg,(list,tuple)) else int(rg)) == 0, "SetGap fallo"

# ── Fase 2: Coordenadas locales ───────────────────────────────────────────────
def ring_coords_2d(shape, dim, n):
    pts = []
    r = dim / 2.0
    sh = shape.lower().replace("í","i").replace("ó","o")
    for i in range(n):
        if "circulo" in sh or "circle" in sh:
            a = -2*math.pi*i/n
            pts.append((r*math.cos(a), r*math.sin(a)))
        else:
            perim = 4*dim; step = perim/n; dist = i*step
            if dist < r:              u,v = r, -dist
            elif dist < r+dim:        u,v = r-(dist-r), -r
            elif dist < r+2*dim:      u,v = -r, -r+(dist-r-dim)
            elif dist < r+3*dim:      u,v = -r+(dist-r-2*dim), r
            else:                     u,v = r, r-(dist-r-3*dim)
            pts.append((u, v))
    return pts

inner_pts = ring_coords_2d("Círculo", BOLT_D, NA)
outer_pts = ring_coords_2d(OUTER_S, OUTER_D, NA)

# ── Fases 3/4: Crear puntos ───────────────────────────────────────────────────
def add_pt(x,y,z):
    raw = SapModel.PointObj.AddCartesian(x,y,z,"","","Global")
    assert int(raw[-1])==0; return str(raw[0])

all_p1, all_p2 = [], []
n_pts = 0
for r in range(NR+1):
    frac = r/float(NR)
    rp1, rp2 = [], []
    for i in range(NA):
        u = inner_pts[i][0]+(outer_pts[i][0]-inner_pts[i][0])*frac
        v = inner_pts[i][1]+(outer_pts[i][1]-inner_pts[i][1])*frac
        rp1.append(add_pt(CX+u, CY+v, CZ-SEP/2))
        rp2.append(add_pt(CX+u, CY+v, CZ+SEP/2))
        n_pts += 2
    all_p1.append(rp1); all_p2.append(rp2)

# ── Áreas ─────────────────────────────────────────────────────────────────────
n_areas = 0
for r in range(NR):
    for i in range(NA):
        j=(i+1)%NA
        for ring in (all_p1, all_p2):
            pts=[ring[r][i],ring[r][j],ring[r+1][j],ring[r+1][i]]
            ra=SapModel.AreaObj.AddByPoint(4,pts,"",AREA_PROP,"")
            assert int(ra[-1])==0; n_areas+=1

# ── Links ─────────────────────────────────────────────────────────────────────
n_links = 0
for r in range(NR+1):
    for i in range(NA):
        rl=SapModel.LinkObj.AddByPoint(all_p1[r][i],all_p2[r][i],"",False,GAP_PROP,"")
        assert int(rl[-1])==0; n_links+=1

SapModel.View.RefreshView(0, False)

result["sep"] = SEP
result["n_pts"] = n_pts
result["n_areas"] = n_areas
result["n_links"] = n_links
result["areas_expected"] = NR*NA*2
result["links_expected"] = (NR+1)*NA
result["all_ok"] = (n_areas==NR*NA*2 and n_links==(NR+1)*NA)
