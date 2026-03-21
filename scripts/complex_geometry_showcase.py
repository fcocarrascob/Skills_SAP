# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        complex_geometry_showcase
# Description: Complex geometry model: Helical Staircase + Hypar Shell + Twisted Tower
# Created:     2026-03-20 02:40:38 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"total_frames": 324, "total_areas": 136, "total_points": 239, "structures": {"1_helical_staircase": {"center": "x=10 m", "frames": 88, "areas": 24, "desc": "Double-helix stringers, 24 warped tread panels, 4-col core, tie rings"}, "2_hypar_shell": {"center": "x=50 m", "frames": 44, "areas": 100, "desc": "10\u00d710 saddle-shell (100 panels), curved edge beams, 4 support cols"}, "3_twisted_tower": {"center": "x=90 m", "frames": 192, "areas": 12, "desc": "12 stories \u00d7 6.0\u00b0/floor = 72.0\u00b0 total twist, X-bracing"}}}
# Tags:        
# ──────────────────────────────────────────────────────────────


# ── Initialize new blank model ─────────────────────────────────────────────
ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel: {ret}"
ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank: {ret}"
ret = SapModel.SetPresentUnits(6)   # kN, m, C
assert ret == 0, f"SetPresentUnits: {ret}"

# ── Materials ──────────────────────────────────────────────────────────────
ret = SapModel.PropMaterial.SetMaterial("STEEL", 1)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL", 200000000, 0.3, 0.0000117)
assert ret == 0
ret = SapModel.PropMaterial.SetMaterial("CONC", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC", 25000000, 0.2, 0.0000100)
assert ret == 0

# ── Frame sections ─────────────────────────────────────────────────────────
ret = SapModel.PropFrame.SetRectangle("COL250", "STEEL", 0.25, 0.25)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM150", "STEEL", 0.15, 0.15)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BRACE100", "STEEL", 0.10, 0.10)
assert ret == 0

print("Materials and sections defined.")

# ── Helper wrappers ────────────────────────────────────────────────────────
# AreaObj.AddByCoord returns [x_arr, y_arr, z_arr, Name_out, ret_code]
def add_area(xs, ys, zs, user_name, prop="Default"):
    raw = SapModel.AreaObj.AddByCoord(len(xs), xs, ys, zs, "", prop, user_name)
    assert raw[-1] == 0, f"AreaObj.AddByCoord '{user_name}': ret={raw[-1]}"
    return raw[-2]  # Name_out

# FrameObj.AddByCoord returns [Name_out, ret_code]
def add_frame(x1,y1,z1, x2,y2,z2, user_name, sect="BEAM150"):
    raw = SapModel.FrameObj.AddByCoord(x1,y1,z1, x2,y2,z2, "", sect, user_name)
    assert raw[-1] == 0, f"FrameObj.AddByCoord '{user_name}': ret={raw[-1]}"
    return raw[0]

# ==========================================================================
# STRUCTURE 1 – PARAMETRIC HELICAL STAIRCASE  (centre x=10, y=0)
#   Double helix (outer + inner stringers), horizontal treads,
#   trapezoidal area panels for each step, and a 4-column central core.
# ==========================================================================
print("Building helical staircase …")

HX, HY       = 10.0, 0.0
R_OUT, R_IN  = 3.5, 1.5     # outer / inner helical radius (m)
PITCH        = 4.0           # metres per full revolution
STEPS_PER_REV = 12           # 30° per step
N_REV        = 2             # 2 full revolutions → 8 m height
N_STEPS      = STEPS_PER_REV * N_REV   # 24 steps

def hpt(r, step):
    """Point on helix at 'step' count."""
    a = math.radians(step * 360.0 / STEPS_PER_REV)
    z = (step / STEPS_PER_REV) * PITCH
    return (HX + r*math.cos(a), HY + r*math.sin(a), z)

# Outer + inner helical stringers
for i in range(N_STEPS):
    p1o, p2o = hpt(R_OUT, i), hpt(R_OUT, i+1)
    add_frame(p1o[0],p1o[1],p1o[2], p2o[0],p2o[1],p2o[2], f"STAIR_OUT_{i}")
    p1i, p2i = hpt(R_IN, i), hpt(R_IN, i+1)
    add_frame(p1i[0],p1i[1],p1i[2], p2i[0],p2i[1],p2i[2], f"STAIR_IN_{i}")

# Tread frames (radial, at each step's leading edge)
for i in range(N_STEPS):
    po = hpt(R_OUT, i)
    pi = hpt(R_IN,  i)
    add_frame(pi[0],pi[1],pi[2], po[0],po[1],po[2], f"TREAD_FR_{i}")

# Tread area panels (trapezoidal quads, slightly warped)
for i in range(N_STEPS):
    po1, po2 = hpt(R_OUT, i), hpt(R_OUT, i+1)
    pi1, pi2 = hpt(R_IN,  i), hpt(R_IN,  i+1)
    xs = [po1[0], po2[0], pi2[0], pi1[0]]
    ys = [po1[1], po2[1], pi2[1], pi1[1]]
    zs = [po1[2], po2[2], pi2[2], pi1[2]]
    add_area(xs, ys, zs, f"STEP_{i}")

# 4-column structural core + horizontal tie rings at each landing
core_d = 0.4   # half-distance of core columns from centre
core_pts = [(HX+core_d, HY+core_d), (HX-core_d, HY+core_d),
            (HX-core_d, HY-core_d), (HX+core_d, HY-core_d)]
total_h = N_REV * PITCH
for ki, (cx, cy) in enumerate(core_pts):
    add_frame(cx,cy,0, cx,cy,total_h, f"CORE_COL_{ki}", "COL250")
for rev in range(N_REV + 1):
    z_ring = rev * PITCH
    for ki, (cx, cy) in enumerate(core_pts):
        nxt_cx, nxt_cy = core_pts[(ki+1)%4]
        add_frame(cx,cy,z_ring, nxt_cx,nxt_cy,z_ring, f"RING_{rev}_{ki}", "BEAM150")

stair_frames = SapModel.FrameObj.Count()
stair_areas  = SapModel.AreaObj.Count()
print(f"  Done → frames={stair_frames}, areas={stair_areas}")

# ==========================================================================
# STRUCTURE 2 – HYPERBOLIC PARABOLOID SHELL ROOF  (centre x=50, y=0)
#   Classic saddle surface: z = Z0 + C·(x·y)/L²
#   10×10 quad shell panels + curved perimeter edge beams + 4 corner columns
# ==========================================================================
print("Building hyperbolic paraboloid shell …")

OX, OY   = 50.0, 0.0
L        = 8.0      # half-span (16 m × 16 m total)
C        = 4.0      # maximum out-of-plane amplitude (m)
Z0_HP    = 2.0      # base elevation (m)
NQ       = 10       # divisions per side (100 panels total)
dx_hp = dy_hp = 2.0 * L / NQ

def hz(lx, ly):
    """Hypar elevation at local coords lx,ly (relative to OX,OY)."""
    return Z0_HP + C * (lx * ly) / (L * L)

# Shell panels
for i in range(NQ):
    for j in range(NQ):
        x0 = OX - L + i*dx_hp;  x1 = x0 + dx_hp
        y0 = OY - L + j*dy_hp;  y1 = y0 + dy_hp
        xs = [x0, x1, x1, x0]
        ys = [y0, y0, y1, y1]
        zs = [hz(x0-OX, y0-OY), hz(x1-OX, y0-OY),
              hz(x1-OX, y1-OY), hz(x0-OX, y1-OY)]
        add_area(xs, ys, zs, f"HP_{i}_{j}")

# Edge beams along South/North boundaries (Y = OY ± L)
for i in range(NQ):
    x0 = OX - L + i*dx_hp;  x1 = x0 + dx_hp
    for yb, sfx in [(OY-L,"S"), (OY+L,"N")]:
        ly = yb - OY
        z0 = hz(x0-OX, ly);  z1 = hz(x1-OX, ly)
        add_frame(x0,yb,z0, x1,yb,z1, f"HP_EX_{sfx}_{i}")

# Edge beams along West/East boundaries (X = OX ± L)
for j in range(NQ):
    y0 = OY - L + j*dy_hp;  y1 = y0 + dy_hp
    for xb, sfx in [(OX-L,"W"), (OX+L,"E")]:
        lx = xb - OX
        z0 = hz(lx, y0-OY);  z1 = hz(lx, y1-OY)
        add_frame(xb,y0,z0, xb,y1,z1, f"HP_EY_{sfx}_{j}")

# Corner support columns (from z=0 up to shell elevation)
for cx_off, cy_off, lbl in [(-L,-L,"SW"),(L,-L,"SE"),(L,L,"NE"),(-L,L,"NW")]:
    cx, cy = OX+cx_off, OY+cy_off
    z_top  = hz(cx_off, cy_off)
    add_frame(cx,cy,0, cx,cy,z_top, f"HP_COL_{lbl}", "COL250")

hp_frames = SapModel.FrameObj.Count() - stair_frames
hp_areas  = SapModel.AreaObj.Count()  - stair_areas
print(f"  Done → frames +{hp_frames}, areas +{hp_areas}")

# ==========================================================================
# STRUCTURE 3 – PROGRESSIVE-TWIST TOWER  (centre x=90, y=0)
#   Each storey's floor plan is rotated 6° more than the one below.
#   Columns are skewed (connect rotated corners), giving the structure
#   a continuous DNA-helix aesthetic.  X-bracing on all four façades.
# ==========================================================================
print("Building twisted tower …")

TX, TY    = 90.0, 0.0
W         = 5.0    # half-width of floor plan (m) → 10 m × 10 m
H_S       = 3.5    # storey height (m)
N_STORIES = 12     # total storeys = 42 m height
TWIST     = 6.0    # degrees per storey → 72° total rotation

def floor_pts(z, angle_deg):
    """4 corners of the square floor plan rotated by angle_deg."""
    a = math.radians(angle_deg)
    offsets = [(-W,-W),(W,-W),(W,W),(-W,W)]
    return [(TX + ddx*math.cos(a) - ddy*math.sin(a),
             TY + ddx*math.sin(a) + ddy*math.cos(a), z)
            for ddx,ddy in offsets]

prev_pts = floor_pts(0.0, 0.0)   # ground footprint

for s in range(1, N_STORIES + 1):
    z        = s * H_S
    angle    = s * TWIST
    cur_pts  = floor_pts(z, angle)

    # Floor slab
    xs = [p[0] for p in cur_pts]
    ys = [p[1] for p in cur_pts]
    zs = [p[2] for p in cur_pts]
    add_area(xs, ys, zs, f"FL_{s}")

    # Perimeter beams at floor level
    for k in range(4):
        p1, p2 = cur_pts[k], cur_pts[(k+1)%4]
        add_frame(p1[0],p1[1],p1[2], p2[0],p2[1],p2[2], f"TB_{s}_{k}")

    # Skewed columns (each corner connects rotated footprints → helical legs)
    for k in range(4):
        pb, pt = prev_pts[k], cur_pts[k]
        add_frame(pb[0],pb[1],pb[2], pt[0],pt[1],pt[2], f"TC_{s}_{k}", "COL250")

    # X-bracing on each façade
    for k in range(4):
        pb1, pb2 = prev_pts[k], prev_pts[(k+1)%4]
        pt1, pt2 = cur_pts[k],  cur_pts[(k+1)%4]
        add_frame(pb1[0],pb1[1],pb1[2], pt2[0],pt2[1],pt2[2], f"TXa_{s}_{k}", "BRACE100")
        add_frame(pb2[0],pb2[1],pb2[2], pt1[0],pt1[1],pt1[2], f"TXb_{s}_{k}", "BRACE100")

    prev_pts = cur_pts

tw_frames = SapModel.FrameObj.Count() - stair_frames - hp_frames
tw_areas  = SapModel.AreaObj.Count()  - stair_areas  - hp_areas
print(f"  Done → frames +{tw_frames}, areas +{tw_areas}")

# ==========================================================================
# FINAL SUMMARY
# ==========================================================================
ret = SapModel.View.RefreshView(0, False)

result["total_frames"] = SapModel.FrameObj.Count()
result["total_areas"]  = SapModel.AreaObj.Count()
result["total_points"] = SapModel.PointObj.Count()
result["structures"]   = {
    "1_helical_staircase": {"center": "x=10 m",
        "frames": stair_frames, "areas": stair_areas,
        "desc": "Double-helix stringers, 24 warped tread panels, 4-col core, tie rings"},
    "2_hypar_shell":       {"center": "x=50 m",
        "frames": hp_frames, "areas": NQ*NQ,
        "desc": "10×10 saddle-shell (100 panels), curved edge beams, 4 support cols"},
    "3_twisted_tower":     {"center": "x=90 m",
        "frames": tw_frames, "areas": N_STORIES,
        "desc": f"{N_STORIES} stories × {TWIST}°/floor = {N_STORIES*TWIST}° total twist, X-bracing"},
}

print("=== MODEL COMPLETE ===")
print(f"Total frames : {result['total_frames']}")
print(f"Total areas  : {result['total_areas']}")
print(f"Total points : {result['total_points']}")
