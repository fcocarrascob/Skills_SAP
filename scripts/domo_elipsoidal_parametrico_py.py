# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        domo_elipsoidal_parametrico_py
# Description: 
# Created:     2026-03-24 02:49:38 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"status": "OK", "num_areas": 160, "total_quads": 140, "total_tris": 20, "semi_eje_X_m": 5.0, "semi_eje_Y_m": 3.5, "altura_m": 2.0, "anillos": 8, "segmentos": 20, "espesor_m": 0.15, "model_path": "C:\\Users\\fcoca\\AppData\\Local\\Temp\\sap2000_scripts\\domo_elipsoidal.sdb"}
# Tags:        
# ──────────────────────────────────────────────────────────────


# math ya está pre-inyectado en el sandbox — no se necesita import

# ─── PARÁMETROS CONFIGURABLES ─────────────────────────────────────────────────
a       = 5.0    # semi-eje X (m)
b       = 3.5    # semi-eje Y (m)  — elipse si b != a
c       = 2.0    # altura del domo (m)
nr      = 8      # anillos en dirección meridional
ns      = 20     # segmentos en dirección circunferencial
espesor = 0.15   # espesor del shell (m)

# ─── INICIALIZAR MODELO EN kN-m ───────────────────────────────────────────────
ret = SapModel.InitializeNewModel(6)   # 6 = kN-m
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

# ─── MATERIAL: CONCRETO ───────────────────────────────────────────────────────
ret = SapModel.PropMaterial.SetMaterial("CONC", 2)   # 2 = Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

# E = 25,000 MPa = 25,000,000 kN/m²
ret = SapModel.PropMaterial.SetMPIsotropic("CONC", 25_000_000.0, 0.2, 9.9e-6)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# ─── PROPIEDAD SHELL-THIN ─────────────────────────────────────────────────────
# SetShell_1(Name, ShellType=1, IncludeDrillingDOF, MatProp, MatAng, Thickness, Bending)
ret = SapModel.PropArea.SetShell_1("SH_ELIPSE", 1, True, "CONC", 0.0, espesor, espesor)
assert ret == 0, f"SetShell_1 failed: {ret}"

# ─── GENERAR DOMO ELIPSOIDAL ──────────────────────────────────────────────────
x_apex, y_apex, z_apex = 0.0, 0.0, c
areas_created = []

for i in range(nr):
    phi1 = (math.pi / 2) * (i / nr)
    phi2 = (math.pi / 2) * ((i + 1) / nr)

    cos_phi1 = math.cos(phi1)
    sin_phi1 = math.sin(phi1)
    cos_phi2 = math.cos(phi2)
    sin_phi2 = math.sin(phi2)

    for j in range(ns):
        theta1 = 2 * math.pi * (j / ns)
        theta2 = 2 * math.pi * ((j + 1) / ns)

        x1 = a * cos_phi1 * math.cos(theta1)
        y1 = b * cos_phi1 * math.sin(theta1)
        z1 = c * sin_phi1

        x2 = a * cos_phi1 * math.cos(theta2)
        y2 = b * cos_phi1 * math.sin(theta2)
        z2 = c * sin_phi1

        if i < nr - 1:
            # ── QUAD (4 nodos) ────────────────────────────────────────────────
            x3 = a * cos_phi2 * math.cos(theta2)
            y3 = b * cos_phi2 * math.sin(theta2)
            z3 = c * sin_phi2

            x4 = a * cos_phi2 * math.cos(theta1)
            y4 = b * cos_phi2 * math.sin(theta1)
            z4 = c * sin_phi2

            raw = SapModel.AreaObj.AddByCoord(
                4,
                [x1, x2, x3, x4],
                [y1, y2, y3, y4],
                [z1, z2, z3, z4],
                "", "SH_ELIPSE"
            )
            assert raw[-1] == 0, f"AddByCoord quad [i={i},j={j}] failed: {raw[-1]}"
            areas_created.append(raw[0])
        else:
            # ── TRIÁNGULO → ápice ─────────────────────────────────────────────
            raw = SapModel.AreaObj.AddByCoord(
                3,
                [x1, x2, x_apex],
                [y1, y2, y_apex],
                [z1, z2, z_apex],
                "", "SH_ELIPSE"
            )
            assert raw[-1] == 0, f"AddByCoord tri [j={j}] failed: {raw[-1]}"
            areas_created.append(raw[0])

# ─── REFRESCAR VISTA ──────────────────────────────────────────────────────────
SapModel.View.RefreshView(0, False)

# ─── GUARDAR MODELO ───────────────────────────────────────────────────────────
ret = SapModel.File.Save(sap_temp_dir + r"\domo_elipsoidal.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# ─── REPORTE ──────────────────────────────────────────────────────────────────
result["status"]       = "OK"
result["num_areas"]    = len(areas_created)
result["total_quads"]  = (nr - 1) * ns
result["total_tris"]   = ns
result["semi_eje_X_m"] = a
result["semi_eje_Y_m"] = b
result["altura_m"]     = c
result["anillos"]      = nr
result["segmentos"]    = ns
result["espesor_m"]    = espesor
result["model_path"]   = sap_temp_dir + r"\domo_elipsoidal.sdb"
