# SAP2000 Enumeration Reference

## eUnits (Unit Systems)

| Value | Name | Description |
|-------|------|-------------|
| 1 | lb_in_F | Pound, Inch, Fahrenheit |
| 2 | lb_ft_F | Pound, Foot, Fahrenheit |
| 3 | kip_in_F | Kip, Inch, Fahrenheit |
| 4 | kip_ft_F | Kip, Foot, Fahrenheit |
| 5 | kN_mm_C | KiloNewton, Millimeter, Celsius |
| 6 | kN_m_C | KiloNewton, Meter, Celsius |
| 7 | kgf_mm_C | Kilogram-force, Millimeter, Celsius |
| 8 | kgf_m_C | Kilogram-force, Meter, Celsius |
| 9 | N_mm_C | Newton, Millimeter, Celsius |
| 10 | N_m_C | Newton, Meter, Celsius |
| 11 | Ton_mm_C | Metric Ton, Millimeter, Celsius |
| 12 | Ton_m_C | Metric Ton, Meter, Celsius |

## eMatType (Material Types)

| Value | Name |
|-------|------|
| 1 | Steel |
| 2 | Concrete |
| 3 | NoDesign |
| 4 | Aluminum |
| 5 | ColdFormed |
| 6 | Rebar |
| 7 | Tendon |

## eLoadPatternType

| Value | Name |
|-------|------|
| 1 | Dead |
| 2 | SuperDead |
| 3 | Live |
| 4 | ReduceLive |
| 5 | Quake |
| 6 | Wind |
| 7 | Snow |
| 8 | Other |
| 11 | Temperature |
| 12 | Roof Live |
| 13 | Notional |

## e2DFrameType

| Value | Name |
|-------|------|
| 0 | PortalFrame |
| 1 | ConcentricBraced |
| 2 | EccentricBraced |

## e3DFrameType

| Value | Name |
|-------|------|
| 0 | OpenFrame |
| 1 | PerimeterFrame |
| 2 | BeamSlab |
| 3 | FlatPlate |

## eLoadCaseType

| Value | Name |
|-------|------|
| 1 | LinearStatic |
| 2 | NonlinearStatic |
| 3 | Modal |
| 4 | ResponseSpectrum |
| 5 | LinearHistory |
| 6 | NonlinearHistory |
| 7 | LinearDynamic |
| 8 | NonlinearDynamic |
| 9 | MovingLoad |
| 10 | Buckling |
| 11 | SteadyState |
| 12 | PowerSpectralDensity |

## eItemTypeElm

| Value | Name |
|-------|------|
| 0 | ObjectElm |
| 1 | Element |
| 2 | GroupElm |
| 3 | SelectionElm |

## eConstraintType

| Value | Name |
|-------|------|
| 1 | Body |
| 2 | Diaphragm |
| 3 | Plate |
| 4 | Rod |
| 5 | Beam |
| 6 | Equal |
| 7 | Local |
| 13 | Weld |

## eCombType (Combination Types)

| Value | Name |
|-------|------|
| 0 | LinearAdd |
| 1 | Envelope |
| 2 | AbsoluteAdd |
| 3 | SRSS |
| 4 | RangeAdd |
