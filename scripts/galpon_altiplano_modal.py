# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        galpon_altiplano_modal
# Description: Galpón altiplano — paso 2.5: fuente de masa D + 0,20·S, caso modal de 30 modos, y lectura de períodos y masa modal acumulada
# Created:     2026-08-12 18:54:48 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"n_modos": 30, "tabla_12": [[1, 0.841863, 0.93708, 0.0, 0.0, 0.93708, 0.0, 0.0], [2, 0.384067, 0.0, 0.0, 0.54226, 0.93708, 0.0, 0.54226], [3, 0.358759, 0.0, 0.04958, 0.0, 0.93708, 0.04958, 0.54226], [4, 0.338662, 0.0, 0.0, 0.0, 0.93708, 0.04958, 0.54226], [5, 0.338036, 0.0, 0.0, 0.00188, 0.93708, 0.04958, 0.54414], [6, 0.337792, 0.0, 0.00106, 0.0, 0.93708, 0.05064, 0.54414], [7, 0.337709, 0.00155, 0.0, 0.0, 0.93863, 0.05064, 0.54414], [8, 0.26805, 0.0, 0.3074, 0.0, 0.93863, 0.35804, 0.54414], [9, 0.261173, 0.0, 0.0, 0.0, 0.93863, 0.35804, 0.54414], [10, 0.260607, 0.0, 0.0, 0.00103, 0.93863, 0.35804, 0.54517], [11, 0.257518, 0.00099, 0.0, 0.0, 0.93962, 0.35804, 0.54517], [12, 0.25682, 0.0, 0.0, 0.00477, 0.93962, 0.35804, 0.54994]], "dominantes": {"X": {"modo": 1, "T": 0.8418633344241585, "Ux": 0.9370795579466139}, "Y": {"modo": 8, "T": 0.26804971727320237, "Uy": 0.307397783327667}, "Z": {"modo": 2, "T": 0.38406657689024704, "Uz": 0.542257263665537}}, "masa_acumulada_final": {"X": 0.9397833295823973, "Y": 0.467198701237363, "Z": 0.5560268168662846}, "modos_para_90pct": {"X": 1, "Y": null, "Z": null}, "T_rango": {"T1": 0.8418633344241585, "T_ultimo": 0.23327061201863442}}
# Tags:        
# ──────────────────────────────────────────────────────────────


# Galpon altiplano — PASO 2.5: MASA SISMICA Y MODAL.
# Masa desde patrones: D + 0,20 S. El 0,20 no sale de §5.1.2 (que da un CRITERIO, no un
# numero: valor esperado o probabilidad de ocurrencia simultanea) sino de la combinacion (5)
# de NCh3171 §9.1.1, `1,2D + 1,4E + L + 0,2S`, que es el juicio de la propia normativa sobre
# cuanta nieve acompana al sismo de diseno. L_r queda fuera: Tabla C-2 de NCh2369 da a = 0
# para techos. SAP divide por su g interno = 9,80665 m/s2.
def rc(raw): return raw if isinstance(raw,int) else raw[-1]

assert SapModel.SetModelIsLocked(False)==0
assert rc(SapModel.SourceMass.SetMassSource("MASA_SIS", False, False, True, True,
                                            3, ["DEAD","DSD","SBAL"], [1.0,1.0,0.20]))==0
assert rc(SapModel.LoadCases.ModalEigen.SetCase("MODAL"))==0
assert rc(SapModel.LoadCases.ModalEigen.SetNumberModes("MODAL",30,1))==0
assert SapModel.File.Save(sap_temp_dir+"\\galpon_altiplano.sdb")==0
assert SapModel.Analyze.RunAnalysis()==0

assert rc(SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput())==0
assert rc(SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL"))==0
raw = SapModel.Results.ModalPeriod(0,[],[],[],[],[],[])
assert raw[-1]==0
T = list(raw[4])
raw = SapModel.Results.ModalParticipatingMassRatios(0,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[])
assert raw[-1]==0
ux,uy,uz = list(raw[5]),list(raw[6]),list(raw[7])
sx,sy,sz = list(raw[8]),list(raw[9]),list(raw[10])

iX = max(range(len(ux)), key=lambda i: ux[i])
iY = max(range(len(uy)), key=lambda i: uy[i])
iZ = max(range(len(uz)), key=lambda i: uz[i])
def primero(sumas, meta):
    for i,v in enumerate(sumas):
        if v >= meta: return i+1
    return None

result["n_modos"] = len(T)
result["tabla_12"] = [[i+1, round(T[i],6), round(ux[i],5), round(uy[i],5), round(uz[i],5),
                       round(sx[i],5), round(sy[i],5), round(sz[i],5)] for i in range(min(12,len(T)))]
result["dominantes"] = {
  "X": {"modo":iX+1, "T":T[iX], "Ux":ux[iX]},
  "Y": {"modo":iY+1, "T":T[iY], "Uy":uy[iY]},
  "Z": {"modo":iZ+1, "T":T[iZ], "Uz":uz[iZ]}}
result["masa_acumulada_final"] = {"X":sx[-1], "Y":sy[-1], "Z":sz[-1]}
result["modos_para_90pct"] = {"X":primero(sx,0.90), "Y":primero(sy,0.90), "Z":primero(sz,0.90)}
result["T_rango"] = {"T1":T[0], "T_ultimo":T[-1]}
