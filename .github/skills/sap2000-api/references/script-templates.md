# SAP2000 Script Templates

This file provides reusable parametric templates for common SAP2000 scripting patterns. Each template includes:
- **Parameters** — What the script generator agent should ask the user
- **Code pattern** — Python template with documented placeholders
- **Expected result** — What the `result` dict should contain

---

## Template 1: Parametric Rectangular Grid

**Use case:** Generate a rectangular plate or frame grid with parametric spacing.

### Parameters to Ask User:
```
✓ Unit system (default: kN_m_C = 6)
✓ Grid dimensions: length (L), width (W)
✓ Grid divisions: nx (along length), ny (along width)
✓ Elevation: z coordinate (default: 0)
✓ Element type: "frame" or "area"
✓ Material: type (1=Steel, 2=Concrete) and properties (E, ν, α)
✓ Section: 
  - For frames: section type (rect, circle, I-section) + dimensions
  - For areas: shell thickness
✓ Supports: which boundary edges? (e.g., "all edges", "corners only", "long edges")
✓ Loads: uniform load magnitude (if applicable)
```

### Code Pattern:

```python
# ─── Parametric Rectangular Grid ──────────────────────────────────────
# Description: {L}m × {W}m grid with {nx}×{ny} divisions
# Element type: {frame|area}
# Units: {unit_system_name}
# ─────────────────────────────────────────────────────────────────────

# ── 1. Initialize ─────────────────────────────────────────────────────
ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

ret = SapModel.SetPresentUnits({unit_enum})  # e.g., 6 = kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# ── 2. Material ───────────────────────────────────────────────────────
ret = SapModel.PropMaterial.SetMaterial("{mat_name}", {mat_type})
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("{mat_name}", {E}, {nu}, {alpha})
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# ── 3. Section ────────────────────────────────────────────────────────
# For frames:
ret = SapModel.PropFrame.SetRectangle("{sec_name}", "{mat_name}", {depth}, {width})
assert ret == 0, f"SetRectangle failed: {ret}"

# For areas (shell):
ret = SapModel.PropArea.SetShell_1("{sec_name}", 1, True, "{mat_name}", 0, {thickness}, {thickness})
assert ret == 0, f"SetShell_1 failed: {ret}"

# ── 4. Geometry — Parametric Grid ────────────────────────────────────
L = {length}      # Total length [units]
W = {width}       # Total width [units]
nx = {nx}         # Number of divisions along length
ny = {ny}         # Number of divisions along width
z = {elevation}   # Elevation

dx = L / nx
dy = W / ny

# Generate grid points
point_names = {}
for i in range(nx + 1):
    for j in range(ny + 1):
        x = i * dx
        y = j * dy
        raw = SapModel.PointObj.AddCartesian(x, y, z, "", f"P_{i}_{j}")
        point_names[(i, j)] = raw[0]
        assert raw[-1] == 0, f"AddCartesian failed at ({x},{y},{z})"

# Connect points with frames OR areas
if "{element_type}" == "frame":
    # Frames along X direction
    for j in range(ny + 1):
        for i in range(nx):
            pt_i = point_names[(i, j)]
            pt_j = point_names[(i+1, j)]
            raw = SapModel.FrameObj.AddByPoint(pt_i, pt_j, "", "{sec_name}", "")
            assert raw[-1] == 0, f"AddByPoint failed: {pt_i}-{pt_j}"
    
    # Frames along Y direction
    for i in range(nx + 1):
        for j in range(ny):
            pt_i = point_names[(i, j)]
            pt_j = point_names[(i, j+1)]
            raw = SapModel.FrameObj.AddByPoint(pt_i, pt_j, "", "{sec_name}", "")
            assert raw[-1] == 0, f"AddByPoint failed: {pt_i}-{pt_j}"

elif "{element_type}" == "area":
    # Areas (4-point quads)
    for i in range(nx):
        for j in range(ny):
            pts = [
                point_names[(i, j)],
                point_names[(i+1, j)],
                point_names[(i+1, j+1)],
                point_names[(i, j+1)]
            ]
            raw = SapModel.AreaObj.AddByPoint(4, pts, "", "{sec_name}", "")
            assert raw[-1] == 0, f"AddByPoint area failed at grid ({i},{j})"

# ── 5. Supports ───────────────────────────────────────────────────────
# Example: Pin all perimeter points (all edges)
for i in range(nx + 1):
    for j in range(ny + 1):
        if i == 0 or i == nx or j == 0 or j == ny:  # Perimeter
            pt_name = point_names[(i, j)]
            raw = SapModel.PointObj.SetRestraint(pt_name, [True, True, True, False, False, False])
            assert raw[-1] == 0, f"SetRestraint failed: {pt_name}"

# ── 6. Loads (optional) ───────────────────────────────────────────────
# Example: Uniform area load (if element_type == "area")
if "{element_type}" == "area":
    # Get all area names
    num_areas = SapModel.AreaObj.Count()
    all_areas = SapModel.AreaObj.GetNameList(0, [], [])[1]
    
    load_value = {load_magnitude}  # e.g., 10 kN/m²
    for area_name in all_areas:
        ret = SapModel.AreaObj.SetLoadUniform(area_name, "DEAD", load_value, 10, False)
        assert ret == 0, f"SetLoadUniform failed: {area_name}"

# ── 7. Save ───────────────────────────────────────────────────────────
ret = SapModel.File.Save(sap_temp_dir + r"\parametric_grid_{nx}x{ny}.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# ── 8. Results ────────────────────────────────────────────────────────
result["num_points"] = len(point_names)
result["num_frames"] = SapModel.FrameObj.Count() if "{element_type}" == "frame" else 0
result["num_areas"] = SapModel.AreaObj.Count() if "{element_type}" == "area" else 0
result["grid_dimensions"] = f"{nx}×{ny}"
result["model_saved"] = True

print(f"Grid {nx}×{ny} created: {result['num_points']} points, {result['num_frames']} frames, {result['num_areas']} areas")
```

### Expected Result:
```python
{
    "num_points": (nx+1) * (ny+1),
    "num_frames": 2*nx*ny + nx + ny,  # if element_type == "frame"
    "num_areas": nx * ny,              # if element_type == "area"
    "grid_dimensions": "4×6",
    "model_saved": True
}
```

---

## Template 2: Circular Geometry (Ring or Full Disc)

**Use case:** Generate circular structures like circular plates, ring beams, radial frames.

### Parameters to Ask User:
```
✓ Unit system (default: kN_m_C = 6)
✓ Center coordinates: (xc, yc, zc)
✓ Radius: R_outer (for ring: also R_inner)
✓ Number of points around circumference: n_circ
✓ Radial divisions (if full disc): n_radial
✓ Element type: "frame" (ring beam) or "area" (plate)
✓ Material: type and properties
✓ Section: dimensions
✓ Supports: "perimeter", "center", or "none"
✓ Loads: radial, tangential, or gravity
```

### Code Pattern:

```python
import math

# ─── Circular Geometry ────────────────────────────────────────────────
# Description: Circular {ring|disc} with R={R_outer}m, {n_circ} points
# Units: {unit_system_name}
# ─────────────────────────────────────────────────────────────────────

# ── 1. Initialize ─────────────────────────────────────────────────────
ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

ret = SapModel.SetPresentUnits({unit_enum})
assert ret == 0, f"SetPresentUnits failed: {ret}"

# ── 2. Material ───────────────────────────────────────────────────────
ret = SapModel.PropMaterial.SetMaterial("{mat_name}", {mat_type})
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("{mat_name}", {E}, {nu}, {alpha})
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# ── 3. Section ────────────────────────────────────────────────────────
ret = SapModel.PropFrame.SetRectangle("{sec_name}", "{mat_name}", {depth}, {width})
# or PropArea.SetShell_1 for plates
assert ret == 0, f"SetRectangle failed: {ret}"

# ── 4. Geometry — Circular Pattern ───────────────────────────────────
xc, yc, zc = {center_x}, {center_y}, {center_z}
R_outer = {R_outer}
n_circ = {n_circ}  # Number of points around circumference

# Outer ring points
outer_points = []
for i in range(n_circ):
    theta = 2 * math.pi * i / n_circ
    x = xc + R_outer * math.cos(theta)
    y = yc + R_outer * math.sin(theta)
    z = zc
    raw = SapModel.PointObj.AddCartesian(x, y, z, "", f"P_outer_{i}")
    outer_points.append(raw[0])
    assert raw[-1] == 0, f"AddCartesian failed at theta={theta}"

# For RING (two concentric circles):
R_inner = {R_inner}  # Only if ring
inner_points = []
if R_inner > 0:
    for i in range(n_circ):
        theta = 2 * math.pi * i / n_circ
        x = xc + R_inner * math.cos(theta)
        y = yc + R_inner * math.sin(theta)
        z = zc
        raw = SapModel.PointObj.AddCartesian(x, y, z, "", f"P_inner_{i}")
        inner_points.append(raw[0])
        assert raw[-1] == 0, f"AddCartesian failed at inner theta={theta}"

# Connect with frames (tangential + radial)
# Outer ring frames
for i in range(n_circ):
    pt_i = outer_points[i]
    pt_j = outer_points[(i+1) % n_circ]  # Wrap around
    raw = SapModel.FrameObj.AddByPoint(pt_i, pt_j, "", "{sec_name}", "")
    assert raw[-1] == 0

# Radial frames (if ring)
if R_inner > 0:
    # Inner ring frames
    for i in range(n_circ):
        pt_i = inner_points[i]
        pt_j = inner_points[(i+1) % n_circ]
        raw = SapModel.FrameObj.AddByPoint(pt_i, pt_j, "", "{sec_name}", "")
        assert raw[-1] == 0
    
    # Radial spokes
    for i in range(n_circ):
        pt_i = inner_points[i]
        pt_j = outer_points[i]
        raw = SapModel.FrameObj.AddByPoint(pt_i, pt_j, "", "{sec_name}", "")
        assert raw[-1] == 0

# Or connect with areas (triangular sectors for full disc)
# Example: radial triangular areas from center
if "{element_type}" == "area" and R_inner == 0:
    raw_center = SapModel.PointObj.AddCartesian(xc, yc, zc, "", "P_center")
    center_pt = raw_center[0]
    assert raw_center[-1] == 0
    
    for i in range(n_circ):
        pts = [
            center_pt,
            outer_points[i],
            outer_points[(i+1) % n_circ]
        ]
        raw = SapModel.AreaObj.AddByPoint(3, pts, "", "{sec_name}", "")
        assert raw[-1] == 0

# ── 5. Supports ───────────────────────────────────────────────────────
# Example: Pin perimeter
for pt_name in outer_points:
    raw = SapModel.PointObj.SetRestraint(pt_name, [True, True, True, False, False, False])
    assert raw[-1] == 0

# ── 6. Save ───────────────────────────────────────────────────────────
ret = SapModel.File.Save(sap_temp_dir + r"\circular_R{R_outer}_n{n_circ}.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# ── 7. Results ────────────────────────────────────────────────────────
result["num_points"] = SapModel.PointObj.Count()
result["num_frames"] = SapModel.FrameObj.Count()
result["num_areas"] = SapModel.AreaObj.Count()
result["radius_outer"] = R_outer
result["circumference_points"] = n_circ
result["model_saved"] = True

print(f"Circular structure created: R={R_outer}m, {n_circ} points")
```

### Expected Result:
```python
{
    "num_points": n_circ + (n_circ if ring else 1),  # outer + inner or center
    "num_frames": n_circ * 2 + n_circ,  # outer ring + inner ring + radial (if ring)
    "num_areas": n_circ,  # triangular sectors (if disc)
    "radius_outer": 5.0,
    "circumference_points": 24,
    "model_saved": True
}
```

---

## Template 3: Plate with Circular Hole

**Use case:** Rectangular plate with a centered or offset circular hole.

### Parameters to Ask User:
```
✓ Unit system (default: kN_m_C = 6)
✓ Plate dimensions: L × W
✓ Plate thickness: t
✓ Hole center: (xh, yh) relative to plate corner
✓ Hole radius: Rh
✓ Points around hole: n_hole
✓ Material: properties
✓ Supports: edges or corners
✓ Loads: uniform pressure
```

### Code Pattern:

```python
import math

# ─── Plate with Circular Hole ─────────────────────────────────────────
# Description: {L}m × {W}m plate with centered hole (R={Rh}m)
# Units: {unit_system_name}
# ─────────────────────────────────────────────────────────────────────

# ── 1. Initialize ─────────────────────────────────────────────────────
ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

ret = SapModel.SetPresentUnits({unit_enum})
assert ret == 0, f"SetPresentUnits failed: {ret}"

# ── 2. Material ───────────────────────────────────────────────────────
ret = SapModel.PropMaterial.SetMaterial("{mat_name}", 2)  # Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("{mat_name}", {E}, {nu}, {alpha})
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# ── 3. Section (Shell) ────────────────────────────────────────────────
ret = SapModel.PropArea.SetShell_1("{sec_name}", 1, True, "{mat_name}", 0, {thickness}, {thickness})
assert ret == 0, f"SetShell_1 failed: {ret}"

# ── 4. Geometry ───────────────────────────────────────────────────────
L = {length}
W = {width}
xh = {hole_center_x}  # Hole center X (e.g., L/2 for centered)
yh = {hole_center_y}  # Hole center Y (e.g., W/2 for centered)
Rh = {hole_radius}
n_hole = {n_hole}  # Points around hole circumference
z = 0

# Create outer rectangle (4 corners)
pt_corners = []
for (x, y) in [(0, 0), (L, 0), (L, W), (0, W)]:
    raw = SapModel.PointObj.AddCartesian(x, y, z, "", f"P_corner")
    pt_corners.append(raw[0])
    assert raw[-1] == 0

# Create hole points
pt_hole = []
for i in range(n_hole):
    theta = 2 * math.pi * i / n_hole
    x = xh + Rh * math.cos(theta)
    y = yh + Rh * math.sin(theta)
    raw = SapModel.PointObj.AddCartesian(x, y, z, "", f"P_hole_{i}")
    pt_hole.append(raw[0])
    assert raw[-1] == 0

# Create outer area (4-point quad)
raw = SapModel.AreaObj.AddByPoint(4, pt_corners, "OUTER_AREA", "{sec_name}", "")
outer_area = raw[0]
assert raw[-1] == 0

# Create hole area (polygon)
raw = SapModel.AreaObj.AddByPoint(n_hole, pt_hole, "HOLE_AREA", "{sec_name}", "")
hole_area = raw[0]
assert raw[-1] == 0

# Mesh the model (required to subtract hole from plate)
ret = SapModel.View.RefreshView(0, False)
assert ret == 0

# Delete the hole area (subtract it from the plate)
# SAP2000 workflow: mesh the outer area, then delete internal area objects
# Alternative: Use EditArea.Divide on outer area, then delete elements inside hole
# Simplified approach: keep both, user manually meshes in SAP2000 GUI
# For automated meshing:
raw = SapModel.EditArea.Divide(
    outer_area, 
    {mesh_size},  # Max element size
    {mesh_size},
    0,  # PointOnEdgeFromGrid
    False,  # PointOnEdgeFromLine
    False,  # ExtendStraightLines
    0,  # Rotation
    "",  # CSys
    False,  # Delete original
    0, [], [], [], [], [], []  # ByRef outputs
)
assert raw[-1] == 0, f"EditArea.Divide failed: {raw[-1]}"

# ── 5. Supports ───────────────────────────────────────────────────────
# Pin the 4 corners
for pt_name in pt_corners:
    raw = SapModel.PointObj.SetRestraint(pt_name, [True, True, True, False, False, False])
    assert raw[-1] == 0

# ── 6. Loads ──────────────────────────────────────────────────────────
# Uniform load on all areas (excluding hole if deleted)
load_value = {load_magnitude}  # kN/m²
all_areas = SapModel.AreaObj.GetNameList(0, [], [])[1]
for area_name in all_areas:
    ret = SapModel.AreaObj.SetLoadUniform(area_name, "DEAD", load_value, 10, False)
    assert ret == 0

# ── 7. Save ───────────────────────────────────────────────────────────
ret = SapModel.File.Save(sap_temp_dir + r"\plate_with_hole_{L}x{W}_Rh{Rh}.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# ── 8. Results ────────────────────────────────────────────────────────
result["num_points"] = SapModel.PointObj.Count()
result["num_areas"] = SapModel.AreaObj.Count()
result["plate_dimensions"] = f"{L}×{W}"
result["hole_radius"] = Rh
result["model_saved"] = True

print(f"Plate {L}×{W}m with hole R={Rh}m created")
```

### Expected Result:
```python
{
    "num_points": 4 + n_hole + (additional mesh points),
    "num_areas": varies (depends on meshing strategy),
    "plate_dimensions": "6×4",
    "hole_radius": 1.5,
    "model_saved": True
}
```

---

## Template 4: Complete Model Minimum Viable

**Use case:** Absolute minimum script to create a valid SAP2000 model.

### Parameters:
None — this is a hardcoded minimal example for quick testing.

### Code Pattern:

```python
# ─── Minimal SAP2000 Model ────────────────────────────────────────────
# Description: Single frame element for connection testing
# Units: kN_m_C
# ─────────────────────────────────────────────────────────────────────

# ── Initialize ────────────────────────────────────────────────────────
ret = SapModel.InitializeNewModel()
assert ret == 0

ret = SapModel.File.NewBlank()
assert ret == 0

ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# ── Material ──────────────────────────────────────────────────────────
ret = SapModel.PropMaterial.SetMaterial("MAT1", 1)  # Steel
assert ret == 0

# ── Section ───────────────────────────────────────────────────────────
ret = SapModel.PropFrame.SetRectangle("SEC1", "MAT1", 0.3, 0.3)
assert ret == 0

# ── Geometry ──────────────────────────────────────────────────────────
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC1", "")
frame_name = raw[0]
assert raw[-1] == 0

# ── Save ──────────────────────────────────────────────────────────────
ret = SapModel.File.Save(sap_temp_dir + r"\minimal_model.sdb")
assert ret == 0

# ── Results ───────────────────────────────────────────────────────────
result["frame_name"] = frame_name
result["num_frames"] = SapModel.FrameObj.Count()
result["model_saved"] = True

print(f"Minimal model created: 1 frame ({frame_name})")
```

### Expected Result:
```python
{
    "frame_name": "1",  # SAP2000 auto-assigned name
    "num_frames": 1,
    "model_saved": True
}
```

---

## Usage Notes

### For the Script Generator Agent:
1. **Always ask for parameters first** — Don't hardcode values like `{4}` or `{6}` without confirming with the user.
2. **Reference these templates** when the user describes a matching pattern (grid, circular, hole).
3. **Adapt templates** — Copy the structure but substitute user-provided values.
4. **Combine templates** — If user wants "circular grid", merge Template 1 (grid logic) + Template 2 (circular pattern).
5. **Verify against wrappers** — If a wrapper exists for a function used in the template, load it and confirm the signature matches.

### For Advanced Users:
- These templates are starting points — complex models may combine multiple patterns.
- For irregular geometry, use conditional loops or manual point lists.
- For meshing control, consult `EditArea.Divide` wrapper for exact 18-argument signature.
