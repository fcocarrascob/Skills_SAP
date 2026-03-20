# GetASCE716_

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetASCE716_

## VB6 Procedure

Function GetASCE716_1(ByVal Name As String, ByRef nDir() As Boolean, ByRef Eccen As
Double, ByRef PeriodFlag As Integer, ByRef CtType As Integer, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef R As Double,
ByRef Omega As Double, ByRef Cd As Double, ByRef I As Double, ByRef Ss As Double,
ByRef S1 As Double, ByRef TL As Double, ByRef SiteClass As Integer, ByRef Fa As Double,
ByRef Fv As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a ASCE 7-16 auto seismic load assignment.

nDir

This is an array with 2 inputs that indicate the seismic load direction.

```
nDir(1) = True = Global X
nDir(2) = True = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CtType

This is 0, 1, 2 or 3, indicating the values of Ct and x. This item is meaningful when the PeriodFlag
item is 1 or 2.

```
0 = Ct = 0.028 (ft), x = 0.
1 = Ct = 0.016 (ft), x = 0.
2 = Ct = 0.03 (ft), x = 0.
3 = Ct = 0.02 (ft), x = 0.
```

UserT

The user specified time period. This item is meaningful when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

R

The response modification factor.

Omega

The system overstrength factor.

Cd

The deflection amplification factor.

I

The occupancy importance factor.

SS, S

The seismic coefficients Ss and S1.

TL

The long-period transition period. [s]

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa, Fv


The site coefficients Fa and Fv.

## Remarks

This function retrieves auto seismic loading parameters for the 2016 ASCE 7 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersASCE716_1()

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(e3DFrameType.BeamSlab, 2, 144, 3, 336, 2, 432 )

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", eLoadPatternType.Quake)

'dimension ASCE716 parameters

Dim nDir() As Boolean

Dim Eccen As Double

Dim PeriodFlag As Long

Dim CtType As Long

Dim UserT As Double

Dim UserZ As Boolean

Dim TopZ As Double

Dim BottomZ As Double

Dim R As Double


Dim Omega As Double

Dim Cd As Double

Dim I As Double

Dim SS As Double

Dim S1 As Double

Dim TL As Double

Dim SiteClass As Long

Dim Fa As Double

Dim Fv As Double

ReDim nDir(1)

nDir(0) = True

TopZ = 32

BottomZ = 14

'set ASCE716 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetASCE716_1("EQX", nDir, 0.04, 3, 1, 1.76,
True, TopZ, BottomZ, 6, 3.5, 6.5, 1.5, 1.9, 1.1, 8, 3, 0, 0)

'get ASCE716 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetASCE716_1("EQX", nDir, Eccen, PeriodFlag,
CtType, UserT, UserZ, TopZ, BottomZ, R, Omega, Cd, I, SS, S1, TL, SiteClass, Fa, Fv)

'close SAP
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.2.0.

This function replaced the obsolete function GetASCE.

## See Also

SetASCE


# GetAS

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetAS

## VB6 Procedure

Function GetAS11702007(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As
Double, ByRef PeriodFlag As Long, ByRef CT As Double, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef AS2007SiteClass
As Long, ByRef AS2007kp As Double, ByRef AS2007Z As Double, ByRef AS2007Sp As
Double, ByRef AS2007Mu As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a AS 1170 2007 auto seismic load
assignment.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified kt factor. This item applies when the PeriodFlag item is 1.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.


TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

AS2007SiteClass

This is 1, 2, 3, 4 or 5, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
AS2007kp

The probability factor, kp.

AS2007Z

The hazard factor, Z.

AS2007Sp

The structural performance factor, Sp.

AS2007Mu

The structural ductility factor, u.

## Remarks

This function retrieves auto seismic loading parameters for the AS 1170 2007 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersAS11702007()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long


Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim AS2007SiteClass As Long
Dim AS2007kp As Double
Dim AS2007Z As Double
Dim AS2007Sp As Double
Dim AS2007Mu As Double

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign AS 1170 2007 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetAS11702007("EQX", 2, 0.1, 2, 0.075, 0, False,
0, 0, 3, 1.3, 0.09, 0.77, 2)

'get AS 1170 2007 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetAS11702007("EQX", DirFlag, Eccen,
PeriodFlag, CT, UserT, UserZ, TopZ, BottomZ, AS2007SiteClass, AS2007kp, AS2007Z,
AS2007Sp, AS2007Mu)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.00.

## See Also

SetAS


# GetBOCA

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetBOCA

## VB6 Procedure

Function GetBOCA96(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As Double,
ByRef PeriodFlag As Long, ByRef CT As Double, ByRef UserT As Double, ByRef UserZ As
Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef BOCA96Aa As Double,
ByRef BOCA96Av As Double, ByRef BOCA96S As Double, ByRef BOCA96R As Double) As
Long

## Parameters

Name

The name of an existing Quake-type load pattern with a BOCA96 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor. This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.


TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

BOCA96Aa

The effective peak acceleration coefficient.

BOCA96Av

The effective peak velocity-related coefficient.

BOCA96S

This is 1, 1.2, 1.5 or 2, indicating the site coefficient.

BOCA96R

The response modification factor.

## Remarks

This function retrieves auto seismic loading parameters for the 1996 BOCA code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersBOCA96()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim BOCA96Aa As Double
Dim BOCA96Av As Double
Dim BOCA96S As Double
Dim BOCA96R As Double


'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign BOCA96 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetBOCA96("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 0.4, 0.4, 1.5, 8)

'get BOCA96 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetBOCA96("EQX", DirFlag, Eccen, PeriodFlag,
CT, UserT, UserZ, TopZ, BottomZ, BOCA96Aa, BOCA96Av, BOCA96S, BOCA96R)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetBOCA

# GetChinese

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetChinese


## VB6 Procedure

Function GetChinese2010(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As
Double, ByRef PeriodFlag As Long, ByRef UserT As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef JGJ32010AlphaMax As Double, ByRef
JGJ32010SI As Long, ByRef JGJ32010DampRatio As Double, ByRef JGJ32010Tg As Double,
ByRef JGJ32010PTDF As Double, ByRef EnhancementFactor As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a Chinese 2010 auto seismic load
assignment.

DirFlag

This is 1, 2 or 3, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
3 = Global Z
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is either 2 or 3, indicating the time period option.

```
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

JGJ32010AlphaMax


The maximum influence factor.

JGJ32010SI

This is 1, 2, 3, 4, 5 or 6, indicating the seismic intensity.

```
1 = 6 (0.05g)
2 = 7 (0.10g)
3 = 7 (0.15g)
4 = 8 (0.20g)
5 = 8 (0.30g)
6 = 9 (0.40g)
```
JGJ32010DampRatio

The damping ratio.

JGJ32010Tg

The characteristic ground period. [s]

JGJ32010PTDF

The period time discount factor.

EnhancementFactor

The enhancement factor.

## Remarks

This function retrieves auto seismic loading parameters for the Chinese 2010 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersChinese2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim JGJ32010AlphaMax As Double
Dim JGJ32010SI As Long
Dim JGJ32010DampRatio As Double


Dim JGJ32010Tg As Double
Dim JGJ32010PTDF As Double
Dim EnhancementFactor As Double

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign Chinese 2010 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetChinese2010("EQX", 1, 0.05, 2, 0, False, 0, 0,
0.16, 4, 0.06, 0.4, 1, 1)

'get Chinese 2010 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetChinese2010("EQX", DirFlag, Eccen,
PeriodFlag, UserT, UserZ, TopZ, BottomZ, JGJ32010AlphaMax, JGJ32010SI,
JGJ32010DampRatio, JGJ32010Tg, JGJ32010PTDF, EnhancementFactor)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 15.0.2.

## See Also

SetChinese

# GetDiaphragmEccentricityOverride

## Syntax


SapObject.SapModel.LoadPatterns.AutoSeismic.GetDiaphragmEccentricityOverride

## VB6 Procedure

Function GetDiaphragmEccentricityOverride(ByVal Name As String, ByRef Num As Long,
ByRef Diaph() As String, ByRef Eccen() As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern that has an auto seismic load assigned.

Num

The number of diaphragm eccentricity overrides for the specified load pattern.

Diaph

This is an array that includes the names of the diaphragms which have eccentricity overrides.

Eccen

This is an array that includes the eccentricity applied to each diaphragm. [L]

## Remarks

This function retrieves diaphragm eccentricity overrides for auto seismic loads. This function does
not apply for User Load type auto seismic loads.

The function returns zero if the overrides are successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetSeismicDiaphragmEccentricityOverride()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Diaph() As String
Dim Eccen() As Double

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object


Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign BOCA96 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetBOCA96("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 0.4, 0.4, 1.5, 8)

'assign diaphragm eccentricity override
ret = SapModel.LoadPatterns.AutoSeismic.SetDiaphragmEccentricityOverride("EQX",
"Diaph1", 50)

'get diaphragm eccentricity override
ret = SapModel.LoadPatterns.AutoSeismic.GetDiaphragmEccentricityOverride("EQX", Num,
Diaph, Eccen)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also


SetDiaphragmEccentricityOverride

GetSpecialRigidDiaphragmList

# GetEurocode82004_

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetEurocode82004_

## VB6 Procedure

Function GetEurocode82004_1(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen
As Double, ByRef PeriodFlag As Long, ByRef CT As Double, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef
EURO2004Country As Long, ByRef EURO2004SpectrumType As Long, ByRef
EURO2004GroundType As Long, ByRef EURO2004ag As Double, ByRef EURO2004S As
Double, ByRef EURO2004Tb As Double, ByRef EURO2004Tc As Double, ByRef
EURO2004Td As Double, ByRef EURO2004Beta As Double, ByRef EURO2004q As Double,
ByRef EURO2004Lambda As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a Eurocode 8 2004 auto seismic load
assignment.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
```
```
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
```
```
2 = Program calculated
```
```
3 = User defined
```

### CT

The code-specified Ct factor. This item applies when the PeriodFlag item is 1.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

EURO2004Country

This is 0, 1, 5, 6 or 10 indicating the country for which the Nationally Determined Parameters
(NDPs) are specified.

```
0 = Other (NDPs are user specified)
```
```
1 = CEN Default
```
```
5 = Norway
```
```
6 = Singapore
```
```
10 = Portugal
```
EURO2004SpectrumType

This is 1 or 2, indicating the spectrum type.

```
1 = Type 1
```
```
2 = Type 2 (Does not apply when EURO2004Country = 5 or 6)
```
EURO2004GroundType

This is 1, 2, 3, 4 or 5, or 6, indicating the ground type.

```
1 = A (Does not apply when EURO2004Country = 6)
```
```
2 = B (Does not apply when EURO2004Country = 6)
```
```
3 = C
```

### 4 = D

```
5 = E (Does not apply when EURO2004Country = 6)
```
```
6 = S1 (Only applies when EURO2004Country = 6)
```
EURO2004ag

The design ground acceleration in g, ag.

EURO2004S

The soil factor, S.

EURO2004Tb

The lower limit of period of the constant spectral acceleration branch, Tb.

EURO2004Tc

The upper limit of period of the constant spectral acceleration branch, Tc.

EURO2004Td

The period defining the start of the constant displacement range, Td.

EURO2004Beta

The lower bound factor, Beta.

EURO2004q

The behavior factor, q.

EURO2004Lambda

The correction factor, Lambda.

## Remarks

This function retrieves auto seismic loading parameters for the Eurocode 8 2004 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersEurocode82004()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double


Dim PeriodFlag As Long
Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim EURO2004Country As Long
Dim EURO2004SpectrumType As Long
Dim EURO2004GroundType As Long
Dim EURO2004ag As Double
Dim EURO2004S As Double
Dim EURO2004Tb As Double
Dim EURO2004Tc As Double
Dim EURO2004Td As Double
Dim EURO2004Beta As Double
Dim EURO2004q As Double
Dim EURO2004Lambda As Double

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign Eurocode 8 2004 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetEurocode82004_1("EQX", 2, 0.1, 2, 0.075, 0,
False, 0, 0, 1, 1, 2, 0.4, 1, 1, 1, 1, 0.2, 2, 1)

'get Eurocode 8 2004 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetEurocode82004_1("EQX", DirFlag, Eccen,
PeriodFlag, CT, UserT, UserZ, TopZ, BottomZ, EURO2004Country, EURO2004SpectrumType,
EURO2004GroundType, EURO2004ag, EURO2004S, EURO2004Tb, EURO2004Tc,
EURO2004Td, EURO2004Beta, EURO2004q, EURO2004Lambda)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 14.1.0.

This function supersedes GetEurocode.

Added Portugal as a Country parameter in SAP2000 Version 15.0.0 and CSiBridge Version
15.1.0.

Added Singapore as a Country parameter in v20.1.0.

## See Also

SetEurocode82004_

# GetIBC

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetIBC

## VB6 Procedure

Function GetIBC2003(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As Double,
ByRef PeriodFlag As Long, ByRef CT As Double, ByRef UserT As Double, ByRef UserZ As
Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef IBC2003SG As Long,
ByRef IBC2003SeismicCoeffFlag As Long, ByRef IBC2003Site As Long, ByRef IBC2003SS As
Double, ByRef IBC2003S1 As Double, ByRef IBC2003Fa As Double, ByRef IBC2003Fv As
Double, ByRef IBC2003R As Double, ByRef IBC2003Omega As Double, ByRef IBC2003Cd As
Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a IBC2003 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag


This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor (ft). This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

IBC2003SG

This is 1, 2 or 3, indicating the seismic group.

```
1 = I
2 = II
3 = III
```
IBC2003SeismicCoeffFlag

This is either 1 or 2, indicating the seismic coefficient option.

```
1 = Coefficients are per code
2 = Coefficients are user defined
```
IBC2003Site

This is either 1, 2, 3, 4 or 5, indicating the site class. This item is filled only when the
IBC2003SeismicCoeffFlag = 1.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```

### IBC2003SS

The response acceleration for short periods, (g).

IBC2003S1

The response acceleration for a one second period, (g).

IBC2003Fa

The site coefficient Fa.

IBC2003Fv

The site coefficient Fv.

IBC2003R

The response modification factor.

IBC2003Omega

The system overstrength factor.

IBC2003Cd

The deflection amplification factor.

## Remarks

This function retrieves auto seismic loading parameters for the 2003 IBC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersIBC2003()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim IBC2003SG As Long
Dim IBC2003SeismicCoeffFlag As Long
Dim IBC2003Site As Long


Dim IBC2003SS As Double
Dim IBC2003S1 As Double
Dim IBC2003Fa As Double
Dim IBC2003Fv As Double
Dim IBC2003R As Double
Dim IBC2003Omega As Double
Dim IBC2003Cd As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IBC2003 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIBC2003("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 1, 1, 3, 1, 0.4, 0, 0, 8, 3, 5.5)

'get IBC2003parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetIBC2003("EQX", DirFlag, Eccen, PeriodFlag,
CT, UserT, UserZ, TopZ, BottomZ, IBC2003SG, IBC2003SeismicCoeffFlag, IBC2003Site,
IBC2003SS, IBC2003S1, IBC2003Fa, IBC2003Fv, IBC2003R, IBC2003Omega, IBC2003Cd)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetIBC2003


# GetIBC2006

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetIBC2006

## VB6 Procedure

Function GetIBC2006(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As Double,
ByRef PeriodFlag As Long, ByRef IBC2006CtType As Long, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef IBC2006R As
Double, ByRef IBC2006Omega As Double, ByRef IBC2006Cd As Double, ByRef IBC2006I As
Double, ByRef IBC2006Option As Long, ByRef IBC2006Latitude As Double, ByRef
IBC2006Longitude As Double, ByRef IBC2006ZipCode As String, ByRef IBC2006SS As
Double, ByRef IBC2006S1 As Double, ByRef IBC2006TL As Double, ByRef IBC2006SiteClass
As Long, ByRef IBC2006Fa As Double, ByRef IBC2006Fv As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a IBC2006 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
IBC2006CtType

This is 0, 1, 2 or 3, indicating the values of Ct and x. This item is meaningful when the PeriodFlag
item is 1 or 2.

```
0 = Ct = 0.028 (ft), x = 0.8
1 = Ct = 0.016 (ft), x = 0.9
2 = Ct = 0.03 (ft), x = 0.75
3 = Ct = 0.02 (ft), x = 0.75
```

UserT

The user specified time period. This item is meaningful when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

IBC2006R

The response modification factor.

IBC2006Omega

The system overstrength factor.

IBC2006Cd

The deflection amplification factor.

IBC2006I

The occupancy importance factor.

IBC2006Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
IBC2006Latitude, IBC2006Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when IBC2006Option = 0 or 1.

IBC2006ZipCode

The zip code for which the seismic coefficients are obtained. This item is meaningful only when
IBC2006Option = 1.

IBC2006SS, IBC2006S1

The seismic coefficients Ss and S1.


### IBC2006TL

The long-period transition period. [s]

IBC2006SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
IBC2006Fa, IBC2006Fv

The site coefficients Fa and Fv.

## Remarks

This function retrieves auto seismic loading parameters for the 2006 IBC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersIBC2006()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim IBC2006CtType As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim IBC2006R As Double
Dim IBC2006Omega As Double
Dim IBC2006Cd As Double
Dim IBC2006I As Double
Dim IBC2006Option As Long
Dim IBC2006Latitude As Double
Dim IBC2006Longitude As Double
Dim IBC2006ZipCode As String
Dim IBC2006SS As Double
Dim IBC2006S1 As Double
Dim IBC2006TL As Double


Dim IBC2006SiteClass As Long
Dim IBC2006Fa As Double
Dim IBC2006Fv As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IBC2006 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIBC2006("EQX", 1, 0.05, 1, 1, 0, False, 0, 0, 8,
3, 5.5, 1, 1, 0, 0, "94704", 0, 0, 8, 3, 0, 0)

'get IBC2006 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetIBC2006("EQX", DirFlag, Eccen, PeriodFlag,
IBC2006CtType, UserT, UserZ, TopZ, BottomZ, IBC2006R, IBC2006Omega, IBC2006Cd,
IBC2006I, IBC2006Option, IBC2006Latitude, IBC2006Longitude, IBC2006ZipCode,
IBC2006SS, IBC2006S1, IBC2006TL, IBC2006SiteClass, IBC2006Fa, IBC2006Fv)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetIBC2006


# GetIBC2009

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetIBC2009

## VB6 Procedure

Function GetIBC2009(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As Double,
ByRef PeriodFlag As Long, ByRef CtType As Long, ByRef UserT As Double, ByRef UserZ As
Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef R As Double, ByRef
Omega As Double, ByRef Cd As Double, ByRef I As Double, ByRef IBC2009Option As Long,
ByRef Latitude As Double, ByRef Longitude As Double, ByRef ZipCode As String, ByRef SS As
Double, ByRef S1 As Double, ByRef TL As Double, ByRef SiteClass As Long, ByRef Fa As
Double, ByRef Fv As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a IBC2009 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CtType

This is 0, 1, 2 or 3, indicating the values of Ct and x. This item is meaningful when the PeriodFlag
item is 1 or 2.

```
0 = Ct = 0.028 (ft), x = 0.8
1 = Ct = 0.016 (ft), x = 0.9
2 = Ct = 0.03 (ft), x = 0.75
3 = Ct = 0.02 (ft), x = 0.75
```

UserT

The user specified time period. This item is meaningful when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

R

The response modification factor.

Omega

The system overstrength factor.

Cd

The deflection amplification factor.

I

The occupancy importance factor.

IBC2009Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when IBC2009Option = 0 or 1.

ZipCode

The zip code for which the seismic coefficients are obtained. This item is meaningful only when
IBC2009Option = 1.

SS, S1

The seismic coefficients Ss and S1.


### TL

The long-period transition period. [s]

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa, Fv

The site coefficients Fa and Fv.

## Remarks

This function retrieves auto seismic loading parameters for the 2009 IBC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersIBC2009()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim CtType As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim R As Double
Dim Omega As Double
Dim Cd As Double
Dim I As Double
Dim IBC2009Option As Long
Dim Latitude As Double
Dim Longitude As Double
Dim ZipCode As String
Dim SS As Double
Dim S1 As Double
Dim TL As Double


Dim SiteClass As Long
Dim Fa As Double
Dim Fv As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IBC2009 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIBC2009("EQX", 1, 0.05, 1, 1, 0, False, 0, 0, 8,
3, 5.5, 1, 1, 0, 0, "94704", 0, 0, 8, 3, 0, 0)

'get IBC2009 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetIBC2009("EQX", DirFlag, Eccen, PeriodFlag,
CtType, UserT, UserZ, TopZ, BottomZ, R, Omega, Cd, I, IBC2009Option, Latitude, Longitude,
ZipCode, SS, S1, TL, SiteClass, Fa, Fv)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

SetIBC2009

# GetIBC2012

## Syntax


SapObject.SapModel.LoadPatterns.AutoSeismic.GetIBC2012

## VB6 Procedure

Function GetIBC2012(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As Double,
ByRef PeriodFlag As Long, ByRef CtType As Long, ByRef UserT As Double, ByRef UserZ As
Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef R As Double, ByRef
Omega As Double, ByRef Cd As Double, ByRef I As Double, ByRef IBC2012Option As Long,
ByRef Latitude As Double, ByRef Longitude As Double, ByRef ZipCode As String, ByRef SS As
Double, ByRef S1 As Double, ByRef TL As Double, ByRef SiteClass As Long, ByRef Fa As
Double, ByRef Fv As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a IBC2012 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CtType

This is 0, 1, 2 or 3, indicating the values of Ct and x. This item is meaningful when the PeriodFlag
item is 1 or 2.

```
0 = Ct = 0.028 (ft), x = 0.8
1 = Ct = 0.016 (ft), x = 0.9
2 = Ct = 0.03 (ft), x = 0.75
3 = Ct = 0.02 (ft), x = 0.75
```
UserT

The user specified time period. This item is meaningful when the PeriodFlag item is 3. [s]

UserZ


This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

R

The response modification factor.

Omega

The system overstrength factor.

Cd

The deflection amplification factor.

I

The occupancy importance factor.

IBC2012Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when IBC2012Option = 0 or 1.

ZipCode

The zip code for which the seismic coefficients are obtained. This item is meaningful only when
IBC2012Option = 1.

SS, S1

The seismic coefficients Ss and S1.

TL

The long-period transition period. [s]

SiteClass


This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa, Fv

The site coefficients Fa and Fv.

## Remarks

This function retrieves auto seismic loading parameters for the 2012 IBC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersIBC2012()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim CtType As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim R As Double
Dim Omega As Double
Dim Cd As Double
Dim I As Double
Dim IBC2012Option As Long
Dim Latitude As Double
Dim Longitude As Double
Dim ZipCode As String
Dim SS As Double
Dim S1 As Double
Dim TL As Double
Dim SiteClass As Long
Dim Fa As Double
Dim Fv As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IBC2012 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIBC2012("EQX", 1, 0.05, 1, 1, 0, False, 0, 0, 8,
3, 5.5, 1, 1, 0, 0, "94704", 0, 0, 8, 3, 0, 0)

'get IBC2012 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetIBC2012("EQX", DirFlag, Eccen, PeriodFlag,
CtType, UserT, UserZ, TopZ, BottomZ, R, Omega, Cd, I, IBC2012Option, Latitude, Longitude,
ZipCode, SS, S1, TL, SiteClass, Fa, Fv)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

SetIBC2012

# GetIS1893_2002

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetIS1893_2002

## VB6 Procedure

Function GetIS1893_2002(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As
Double, ByRef PeriodFlag As Long, ByRef CT As Double, ByRef UserT As Double, ByRef


UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef INZFlag As
Long, ByRef INZ As Double, ByRef INS As Long, ByRef INI As Double, ByRef INR As
Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with an IS1893_2002 auto seismic load
assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor (m). This item applies when the PeriodFlag item is 1.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

INZFlag


This is either 1 or 2, indicating if the seismic zone factor is per code or user defined.

```
1 = Per code
2 = User defined
```
INZ

The seismic zone factor, Z.

If the seismic zone factor is per code (INZFlag = 1), this item should be one of the following:
0.10, 0.16, 0.24, 0.36.

INS

This is 1, 2 or 3, indicating the soil type.

```
1 = I
2 = II
3 = III
```
BOCA96R

The response modification factor.

INR

The importance factor.

INR

The response modification factor.

## Remarks

This function retrieves auto seismic loading parameters for the 2002 IS1893 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersIS18932002()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double


Dim BottomZ As Double
Dim INZFlag As Long
Dim INZ As Double
Dim INS As Long
Dim INI As Double
Dim INR As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IS1893_2002 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIS1893_2002("EQX", 1, 0.05, 1, 0.075, 0,
False, 0, 0, 1, 0.36, 3, 1, 5)

'get IS1893_2002 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetIS1893_2002("EQX", DirFlag, Eccen,
PeriodFlag, CT, UserT, UserZ, TopZ, BottomZ, INZFlag, INZ, INS, INI, INR)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetIS1893_2002


# GetNBCC2015

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetNBCC2015

## VB6 Procedure

Function GetNBCC2015(ByVal Name As String, ByRef DirFlag As Long, ByRef eccen As
Double, ByRef CtType As Long, ByRef PeriodFlag As Long, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef PGA As Double,
ByRef S02 As Double, ByRef S05 As Double, ByRef S1 As Double, ByRef S2 As Double, ByRef
S5 As Double, ByRef S10 As Double, ByRef SiteClass As Long, ByRef F02 As Double, ByRef
F05 As Double, ByRef F1 As Double, ByRef F2 As Double, ByRef F5 As Double, ByRef F10 As
Double, ByRef I As Double, ByRef Mv As Double, ByRef Rd As Double, ByRef Ro As Double)
As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NBCC2015 auto seismic load assignment.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

CtType

This is 0, 1, 2, 3 or 4, indicating the structure type.

```
0 = Steel moment frame
1 = Concrete moment frame
2 = Other moment frame
3 = Braced frame
4 = Shear wall
```
PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Code
2 = Program calculated
3 = User defined
```

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

PGA

The peak ground acceleration.

S02

The spectral acceleration at a 0.2 second period.

S05

The spectral acceleration at a 0.5 second period.

S1

The spectral acceleration at a 1 second period.

S2

The spectral acceleration at a 2 second period.

S5

The spectral acceleration at a 5 second period.

S10

The spectral acceleration at a 10 second period.

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```

### 6 = F

### F02

The site coefficient at a 0.2 second period. This item is read when the site class is F only.

F05

The site coefficient at a 0.5 second period. This item is read when the site class is F only.

F1

The site coefficient at a 1 second period. This item is read when the site class is F only.

F2

The site coefficient at a 2 second period. This item is read when the site class is F only.

F5

The site coefficient at a 5 second period. This item is read when the site class is F only.

F10

The site coefficient at a 10 second period. This item is read when the site class is F only.

I

The importance factor.

Mv

The higher mode factor.

Rd

The ductility modifier.

Ro

The overstrength modifier.

## Remarks

This function retrieves auto seismic loading parameters for the 2015 NBCC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersNBCC2015()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim CtType As Long
Dim PeriodFlag As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim PGA As Double
Dim S02 As Double
Dim S05 As Double
Dim S1 As Double
Dim S2 As Double

Dim S5 As Double

Dim S10 As Double
Dim SiteClass As Long
Dim F02 As Double
Dim F05 As Double

Dim F1 As Double

Dim F5 As Double

Dim F10 As Double
Dim I As Double
Dim Mv As Double
Dim Rd As Double
Dim Ro As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NBCC2015 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNBCC2015("EQX", 2, 0.1, 2, 1, 0, False, 0, 0,


### 0.6, 1.1, 0.7, 0.35, 0.2, 0.03, 0.01, 6, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.2, 6, 1.6)

'get NBCC2015 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetNBCC2015("EQX", DirFlag, Eccen, CtType,
PeriodFlag, UserT, UserZ, TopZ, BottomZ, PGA, S02, S05, S1, S2, S5, S10, SiteClass, F02, F05,
F1, F2, F5, F10, I, Mv, Rd, Ro)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

## See Also

SetNBCC2015

# GetNBCC2010

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetNBCC2010

## VB6 Procedure

Function GetNBCC2010(ByVal Name As String, ByRef DirFlag As Long, ByRef eccen As
Double, ByRef CtType As Long, ByRef PeriodFlag As Long, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef PGA As Double,
ByRef S02 As Double, ByRef S05 As Double, ByRef S1 As Double, ByRef S2 As Double, ByRef
S4 As Double, ByRef SiteClass As Long, ByRef Fa As Double, ByRef Fv As Double, ByRef I As
Double, ByRef Mv As Double, ByRef Rd As Double, ByRef Ro As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NBCC2010 auto seismic load assignment.

DirFlag

This is 1 or 2, indicating the seismic load direction.


```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

CtType

This is 0, 1, 2, 3 or 4, indicating the structure type.

```
0 = Steel moment frame
1 = Concrete moment frame
2 = Other moment frame
3 = Braced frame
4 = Shear wall
```
PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Code
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

PGA

The peak ground acceleration.

S02

The spectral acceleration at a 0.2 second period.

S05

The spectral acceleration at a 0.5 second period.


### S1

The spectral acceleration at a 1 second period.

S2

The spectral acceleration at a 2 second period.

S4

The spectral acceleration at a 4 second period.

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa

The site coefficient, Fa.

Fv

The site coefficient, Fv.

I

The importance factor.

Mv

The higher mode factor.

Rd

The ductility modifier.

Ro

The overstrength modifier.

## Remarks

This function retrieves auto seismic loading parameters for the 2010 NBCC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetSeismicParametersNBCC2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim CtType As Long
Dim PeriodFlag As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim PGA As Double
Dim S02 As Double
Dim S05 As Double
Dim S1 As Double
Dim S2 As Double

Dim S4 As Double
Dim SiteClass As Long
Dim Fa As Double
Dim Fv As Double
Dim I As Double
Dim Mv As Double
Dim Rd As Double
Dim Ro As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NBCC2010 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNBCC2010("EQX", 2, 0.1, 2, 1, 0, False, 0, 0,
0.6, 1.1, 0.7, 0.35, 0.2, 0.1, 6, 1.8, 2, 1.5, 1.2, 6, 1.6)


'get NBCC2010 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetNBCC2005("EQX", DirFlag, Eccen,
NBCC2005CtType, CtType, PeriodFlag, UserT, UserZ, TopZ, BottomZ, PGA, S02, S05, S1, S2,
S4, SiteClass, Fa, Fv, I, Mv, Rd, Ro)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

## See Also

SetNBCC2010

# GetNBCC2005

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetNBCC2005

## VB6 Procedure

Function GetNBCC2005(ByVal Name As String, ByRef DirFlag As Long, ByRef eccen As
Double, ByRef NBCC2005CtType As Long, ByRef PeriodFlag As Long, ByRef UserT As
Double, ByRef UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef
NBCC2005PGA As Double, ByRef NBCC2005S02 As Double, ByRef NBCC2005S05 As
Double, ByRef NBCC2005S1 As Double, ByRef NBCC2005S2 As Double, ByRef
NBCC2005SiteClass As Long, ByRef NBCC2005Fa As Double, ByRef NBCC2005Fv As
Double, ByRef NBCC2005I As Double, ByRef NBCC2005Mv As Double, ByRef NBCC2005Rd
As Double, ByRef NBCC2005Ro As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NBCC2005 auto seismic load assignment.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
```

```
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

NBCC2005CtType

This is 0, 1, 2, 3 or 4, indicating the structure type.

```
0 = Steel moment frame
1 = Concrete moment frame
2 = Other moment frame
3 = Braced frame
4 = Shear wall
```
NBCC95DS

This item applies only when the NBCCPFlag = 2. It is the dimension of the lateral load resisting
system in the direction of the applied forces. [L]

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Code
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

NBCC2005PGA

The peak ground acceleration.

NBCC2005S02

The spectral acceleration at a 0.2 second period.


### NBCC2005S05

The spectral acceleration at a 0.52 second period.

NBCC2005S1

The spectral acceleration at a 1 second period.

NBCC2005S2

The spectral acceleration at a 2 second period.

NBCC2005SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
NBCC2005Fa

The site coefficient, Fa.

NBCC2005Fv

The site coefficient, Fv.

NBCC2005I

The importance factor.

NBCC2005Mv

The higher mode factor.

NBCC2005Rd

The ductility modifier.

NBCC2005Ro

The overstrength modifier.

## Remarks

This function retrieves auto seismic loading parameters for the 2005 NBCC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetSeismicParametersNBCC2005()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim NBCC2005CtType As Long
Dim PeriodFlag As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim NBCC2005PGA As Double
Dim NBCC2005S02 As Double
Dim NBCC2005S05 As Double
Dim NBCC2005S1 As Double
Dim NBCC2005S2 As Double
Dim NBCC2005SiteClass As Long
Dim NBCC2005Fa As Double
Dim NBCC2005Fv As Double
Dim NBCC2005I As Double
Dim NBCC2005Mv As Double
Dim NBCC2005Rd As Double
Dim NBCC2005Ro As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NBCC2005 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNBCC2005("EQX", 2, 0.1, 2, 1, 0, False, 0, 0,
0.6, 1.1, 0.7, 0.35, 0.2, 6, 1.8, 2, 1.5, 1.2, 6, 1.6)

'get NBCC2005 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetNBCC2005("EQX", DirFlag, Eccen,


NBCC2005CtType, PeriodFlag, UserT, UserZ, TopZ, BottomZ, NBCC2005PGA,
NBCC2005S02, NBCC2005S05, NBCC2005S1, NBCC2005S2, NBCC2005SiteClass,
NBCC2005Fa, NBCC2005Fv, NBCC2005I, NBCC2005Mv, NBCC2005Rd, NBCC2005Ro)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetNBCC2005

# GetNBCC95

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetNBCC95

## VB6 Procedure

Function GetNBCC95(ByVal Name As String, ByRef DirFlag As Long, ByRef eccen As Double,
ByRef NBCCPFlag As Long, ByRef NBCC95DS As Double, ByRef PeriodFlag As Long, ByRef
UserT As Double, ByRef UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As
Double, ByRef NBCC95ZA As Long, ByRef NBCC95ZV As Long, ByRef NBCC95ZVFlag As
Long, ByRef NBCC95ZVR As Double, ByRef NBCC95I As Double, ByRef NBCC95F As
Double, ByRef NBCC95R As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NBCC95 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.


NBCCPFlag

This is either 1 or 2, indicating the structure type.

```
1 = Moment frame
2 = Other
```
NBCC95DS

This item applies only when the NBCCPFlag = 2. It is the dimension of the lateral load resisting
system in the direction of the applied forces. [L]

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Code
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

NBCC95ZA

This is 0, 1, 2, 3, 4, 5 or 6, indicating the acceleration related zone, Za.

NBCC95ZV

This is 0, 1, 2, 3, 4, 5 or 6, indicating the velocity related zone, Zv.

NBCC95ZVFlag

This is either 1 or 2, indicating how the zonal velocity ratio, V, is specified.

```
1 = From code based on Zv
2 = User specified
```
NBCC95ZVR


The zonal velocity ratio, V.

NBCC95I

The importance factor.

NBCC95F

The foundation factor.

NBCC95R

The force modification factor.

## Remarks

This function retrieves auto seismic loading parameters for the 1995 NBCC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersNBCC95()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim NBCCPFlag As Long
Dim NBCC95DS As Double
Dim PeriodFlag As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim NBCC95ZA As Long
Dim NBCC95ZV As Long
Dim NBCC95ZVFlag As Long
Dim NBCC95ZVR As Double
Dim NBCC95I As Double
Dim NBCC95F As Double
Dim NBCC95R As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object


Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NBCC95 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNBCC95("EQX", 1, 0.05, 1, 0, 1, 0, False, 0, 0,
4, 5, 1, 0, 1, 1.3, 4)

'get NBCC95 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetNBCC95("EQX", DirFlag, Eccen,
NBCCPFlag, NBCC95DS, PeriodFlag, UserT, UserZ, TopZ, BottomZ, NBCC95ZA,
NBCC95ZV, NBCC95ZVFlag, NBCC95ZVR, NBCC95I, NBCC95F, NBCC95R)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetNBCC95

# GetNEHRP97

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetNEHRP97

## VB6 Procedure

Function GetNEHRP97(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As
Double, ByRef PeriodFlag As Long, ByRef CT As Double, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef NEHRP97SG As
Long, ByRef NEHRP97SeismicCoeffFlag As Long, ByRef NEHRP97Site As Long, ByRef


NEHRP97SS As Double, ByRef NEHRP97S1 As Double, ByRef NEHRP97Fa As Double, ByRef
NEHRP97Fv As Double, ByRef NEHRP97R As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NEHRP97 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor. This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

NEHRP97SG

This is 1, 2 or 3, indicating the seismic group.


### 1 = I

### 2 = II

### 3 = III

NEHRP97SeismicCoeffFlag

This is 1 or 2, indicating the seismic coefficient option.

```
1 = Coefficients are per code
2 = Coefficients are user defined
```
NEHRP97Site

This is 1, 2, 3, 4 or 5, indicating the site class. This item is only filled when the
NEHRP97SeismicCoeffFlag = 1.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
NEHRP97SS

The response acceleration for short periods, (g).

NEHRP97S1

The response acceleration for a one second period, (g).

NEHRP97Fa

The site coefficient Fa.

NEHRP97Fv

The site coefficient Fv.

NEHRP97R

The response modification factor.

## Remarks

This function retrieves auto seismic loading parameters for the 1997 NEHRP code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersNEHRP97()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim NEHRP97SG As Long
Dim NEHRP97SeismicCoeffFlag As Long
Dim NEHRP97Site As Long
Dim NEHRP97SS As Double
Dim NEHRP97S1 As Double
Dim NEHRP97Fa As Double
Dim NEHRP97Fv As Double
Dim NEHRP97R As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NEHRP97 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNEHRP97("EQX", 1, 0.05, 1, 0.035, 0, False,
0, 0, 1, 1, 3, 1, 0.4, 0, 0, 8)

'get NEHRP97parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetNEHRP97("EQX", DirFlag, Eccen,
PeriodFlag, CT, UserT, UserZ, TopZ, BottomZ, NEHRP97SG, NEHRP97SeismicCoeffFlag,
NEHRP97Site, NEHRP97SS, NEHRP97S1, NEHRP97Fa, NEHRP97Fv, NEHRP97R)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetNEHRP97

# GetNTC2008

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetNTC2008

## VB6 Procedure

Function GetNTC2008(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As
Double, ByRef PeriodFlag As Long, ByRef C1Type As Long, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef ParamsOption As
Long, ByRef Latitude As Double, ByRef Longitude As Double, ByRef Island As Long, ByRef
LimitState As Long, ByRef UsageClass As Long, ByRef NomLife As Double, ByRef PeakAccel
As Double, ByRef F0 As Double, ByRef Tcs As Double, ByRef SpecType As Long, ByRef
SoilType As Long, ByRef Topography As Long, ByRef hRatio As Double, ByRef Damping As
Double, ByRef q As Double, ByRef lambda As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NTC 2008 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.


```
1 = Approximate
2 = Program calculated
3 = User defined
```
CIType

This is 0, 1, 2 or 3, indicating the values of C1. This item applies when the PeriodFlag item is 1 or
2.

```
1 = C1 = 0.085 (m)
2 = C1 = 0.075 (m)
3 = C1 = 0.05 (m)
```
UserT

The user specified time period. This item is meaningful when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

ParamsOption

This is 1, 2, or 3, indicating the option for defining the parameters.

```
1 = by latitude and longitude
2 = by island
3 = user specified
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when ParamsOption = 1.

Island

This is one of the following values. This item is used only when ParamsOption = 2.

```
1 = Alicudi
2 = Arcipelago Toscano
3 = Filcudi
4 = Isole Egadi
5 = Lampedusa
6 = Linosa
```

```
7 = Lipari
8 = Palmarola
9 = Panarea
10 = Pantelleria
11 = Ponza
12 = Salina
13 = Santo Stefano
14 = Sardegna
15 = Stromboli
16 = Tremiti
17 = Ustica
18 = Ventotene
19 = Vulcano
20 = Zannone
```
LimitState

This is 1, 2, 3, or 4, indicating the limit state.

```
1 = SLO
2 = SLD
3 = SLV
4 = SLC
```
UsageClass

This is 1, 2, 3, or 4, indicating the usage class.

```
1 = I
2 = II
3 = III
4 = IV
```
NomLife

The nominal life to be considered.

PeakAccel

The peak ground acceleration, ag/g.

F0

The magnitude factor, F0.

Tcs

The reference period, Tc* [s].

SpecType

This is 1, 2, 3, or 4, indicating the type of spectrum to consider.

```
1 = Elastic horizontal
2 = Elastic vertical
```

```
3 = Design horizontal
4 = Design vertical
```
SoilType

This is 1, 2, 3, 4, or 5, indicating the subsoil type.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
Topography

This is 1, 2, 3, or 4, indicating the topography type.

```
1 = T1
2 = T2
3 = T3
4 = T4
```
hRatio

The ratio for the site altitude at the base of the hill to the height of the hill.

Damping

The damping, in percent. This is only applicable for SpecType 1 and 2.

q

The behavior correction factor. This is only applicable for SpecType 3 and 4.

lambda

A correction factor.

## Remarks

This function retrieves auto seismic loading parameters for the NTC 2008 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersNTC2008()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim C1Type As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim ParamsOption As Long
Dim Latitude As Double
Dim Longitude As Double
Dim Island As Long
Dim LimitState As Long
Dim UsageClass As Long
Dim NomLife As Double
Dim PeakAccel As Double
Dim F0 As Double
Dim Tcs As Double
Dim SpecType As Long
Dim SoilType As Long
Dim Topography As Long
Dim hRatio As Double
Dim Damping As Double
Dim q As Double
Dim lambda As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", eLoadPatternType_QUAKE)

'assign NTC2008 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNTC2008("EQX", 1, 0.05, 1, 1, 0, False, 0, 0,
3, 0, 0, 1, 1, 1, 50, 0.2, 2.4, 0.3, 3, 2, 1, 1, 5, 1, 0.85)

'get NTC2008 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetNTC2008("EQX", DirFlag, Eccen, PeriodFlag,
C1Type, UserT, UserZ, TopZ, BottomZ, ParamsOption, Latitude, Longitude, Island, LimitState,
UsageClass, NomLife, PeakAccel, F0, Tcs, SpecType, SoilType, Topography, hRatio, Damping,
q, lambda)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 18.1.0.

## See Also

SetNTC2008

# GetNTC2018

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetNTC2018

## VB6 Procedure

Function GetNTC2018(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As
Double, ByRef PeriodFlag As Long, ByRef UserT As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef ParamsOption As Long, ByRef Latitude As
Double, ByRef Longitude As Double, ByRef Island As Long, ByRef LimitState As Long, ByRef
UsageClass As Long, ByRef NomLife As Double, ByRef PeakAccel As Double, ByRef F0 As
Double, ByRef Tcs As Double, ByRef SpecType As Long, ByRef SoilType As Long, ByRef
Topography As Long, ByRef hRatio As Double, ByRef Damping As Double, ByRef q As Double,
ByRef lambda As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NTC 2018 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.


PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item is meaningful when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

ParamsOption

This is 1, 2, or 3, indicating the option for defining the parameters.

```
1 = by latitude and longitude
2 = by island
3 = user specified
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when ParamsOption = 1.

Island

This is one of the following values. This item is used only when ParamsOption = 2.

```
1 = Alicudi
2 = Arcipelago Toscano
3 = Filcudi
4 = Isole Egadi
5 = Lampedusa
6 = Linosa
7 = Lipari
8 = Palmarola
9 = Panarea
10 = Pantelleria
11 = Ponza
```

```
12 = Salina
13 = Santo Stefano
14 = Sardegna
15 = Stromboli
16 = Tremiti
17 = Ustica
18 = Ventotene
19 = Vulcano
20 = Zannone
```
LimitState

This is 1, 2, 3, or 4, indicating the limit state.

```
1 = SLO
2 = SLD
3 = SLV
4 = SLC
```
UsageClass

This is 1, 2, 3, or 4, indicating the usage class.

```
1 = I
2 = II
3 = III
4 = IV
```
NomLife

The nominal life to be considered.

PeakAccel

The peak ground acceleration, ag/g.

F0

The magnitude factor, F0.

Tcs

The reference period, Tc* [s].

SpecType

This is 1, 2, 3, or 4, indicating the type of spectrum to consider.

```
1 = Elastic horizontal
2 = Elastic vertical
3 = Design horizontal
4 = Design vertical
```
SoilType


This is 1, 2, 3, 4, or 5, indicating the subsoil type.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
Topography

This is 1, 2, 3, or 4, indicating the topography type.

```
1 = T1
2 = T2
3 = T3
4 = T4
```
hRatio

The ratio for the site altitude at the base of the hill to the height of the hill.

Damping

The damping, in percent. This is only applicable for SpecType 1 and 2.

q

The behavior correction factor. This is only applicable for SpecType 3 and 4.

lambda

A correction factor.

## Remarks

This function retrieves auto seismic loading parameters for the NTC 2018 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersNTC2018()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim UserT As Double
Dim UserZ As Boolean


Dim TopZ As Double
Dim BottomZ As Double
Dim ParamsOption As Long
Dim Latitude As Double
Dim Longitude As Double
Dim Island As Long
Dim LimitState As Long
Dim UsageClass As Long
Dim NomLife As Double
Dim PeakAccel As Double
Dim F0 As Double
Dim Tcs As Double
Dim SpecType As Long
Dim SoilType As Long
Dim Topography As Long
Dim hRatio As Double
Dim Damping As Double
Dim q As Double
Dim lambda As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", eLoadPatternType_QUAKE)

'assign NTC2018 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNTC2018("EQX", 1, 0.05, 1, 0, False, 0, 0, 3,
0, 0, 1, 1, 1, 50, 0.2, 2.4, 0.3, 3, 2, 1, 1, 5, 1, 0.85 )

'get NTC2018 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetNTC2018("EQX", DirFlag, Eccen, PeriodFlag,
UserT, UserZ, TopZ, BottomZ, ParamsOption, Latitude, Longitude, Island, LimitState,
UsageClass, NomLife, PeakAccel, F0, Tcs, SpecType, SoilType, Topography, hRatio, Damping,
q, lambda)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in v20.1.0.

## See Also

SetNTC2018

# GetNZS11702004_2

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetNZS11702004_2

## VB6 Procedure

Function GetNZS11702004_2(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As
Double, ByRef PeriodFlag As Long, ByRef UserT As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef NZS2004SiteClass As Long, ByRef
NZS2004Z As Double, ByRef NZS2004R As Double, ByRef NZS2004DIST As Double, ByRef
NZS2004Sp As Double, ByRef NZS2004Mu As Double, ByRef NZS2004ConsiderTSite As
Boolean, ByRef NZS2004TSite As Double, ByRef NZS2004ConsiderSingleStory) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NZS 1170 2004 auto seismic load
assignment.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

NZS2004SiteClass

This is 1, 2, 3, 4 or 5, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
NZS2004Z

The hazard factor, Z.

NZS2004R

The return period factor, R.

NZS2004DIST

Distance to the fault in km, used to calculate the near fault factor..

NZS2004Sp

The structural performance factor, Sp.

NZS2004Mu

The structural ductility factor, u.

NZS2004ConsiderTSite

Indicates whether to consider the site period for the spectral shape factor.

NZS2004TSite

The low amplitude site period.


NZS2004ConsiderSingleStory

Indicates whether to consider the structure as a single story, in which case F t = 0.

## Remarks

This function retrieves auto seismic loading parameters for the NZS 1170 2004 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersNZS11702004_2()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim NZS2004SiteClass As Long
Dim NZS2004Z As Double
Dim NZS2004R As Double
Dim NZS2004DIST As Double
Dim NZS2004Sp As Double
Dim NZS2004Mu As Double
Dim NZS2004ConsiderTSite As Boolean
Dim NZS2004TSite As Double
Dim NZS2004ConsiderSingleStory As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)


'assign NZS 1170 2004 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNZS11702004_2("EQX", 2, 0.1, 2, 0, False, 0,
0, 3, 0.4, 1.3, 20, 0.7, 3, True, 1, False)

'get NZS 1170 2004 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetNZS11702004_2("EQX", DirFlag, Eccen,
PeriodFlag, UserT, UserZ, TopZ, BottomZ, NZS2004SiteClass, NZS2004Z, NZS2004R,
NZS2004DIST, NZS2004Sp, NZS2004Mu, NZS2004ConsiderTSite, NZS2004TSite,
NZS2004ConsiderSingleStory)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v22.0.0.

This function supersedes GetNZS11702004_1.

## See Also

SetNZS11702004_2.

# GetUBC94

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetUBC94

## VB6 Procedure

Function GetUBC94(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As Double,
ByRef PeriodFlag As Long, ByRef CT As Double, ByRef UserT As Double, ByRef UserZ As
Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef UBC94ZFlag As Long,
ByRef UBC94Z As Double, ByRef UBC94S As Double, ByRef UBC94I As Double, ByRef
UBC94RW As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a UBC94 auto seismic load assignment.

DirFlag


This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor. This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

UBC94ZFlag

This is 1 or 2, indicating if the seismic zone factor is per code or user defined.

```
1 = Per code
2 = User defined
```
UBC94Z

The seismic zone factor, Z.

If the seismic zone factor is per code (UBC94ZFlag = 1), this item should be one of the following:
0.075, 0.15, 0.20, 0.30, 0.40.

UBC94S


This is 1, 1.2, 1.5 or 2, indicating the site coefficient.

UBC94I

The importance factor.

UBC94RW

The numerical coefficient, Rw.

## Remarks

This function retrieves auto seismic loading parameters for the 1994 UBC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersUBC94()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim UBC94ZFlag As Long
Dim UBC94Z As Double
Dim UBC94S As Double
Dim UBC94I As Double
Dim UBC94RW As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)


'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign UBC94 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetUBC94("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 1, 0.4, 1.2, 1.15, 8)

'get UBC94 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetUBC94("EQX", DirFlag, Eccen, PeriodFlag,
CT, UserT, UserZ, TopZ, BottomZ, UBC94ZFlag, UBC94Z, UBC94S, UBC94I, UBC94RW)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUBC94

# GetUBC97

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetUBC97

## VB6 Procedure

Function GetUBC97(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As Double,
ByRef PeriodFlag As Long, ByRef CT As Double, ByRef UserT As Double, ByRef UserZ As
Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef UBC97SeismicCoeffFlag
As Long, ByRef UBC97SoilProfileType As Long, ByRef UBC97Z As Double, ByRef UBC97Ca
As Double, ByRef UBC97Cv As Double, ByRef UBC97NearSourceFlag As Long, ByRef
UBC97SourceType As Long, ByRef UBC97Dist As Double, ByRef UBC97Na As Double, ByRef
UBC97Nv As Double, ByRef UBC97I As Double, ByRef UBC97R As Double) As Long


## Parameters

Name

The name of an existing Quake-type load pattern with a UBC97 auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor. This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

UBC97SeismicCoeffFlag

This is either 1 or 2, indicating if the seismic coefficients Ca and Cv are per code or user defined.

```
1 = Per code
2 = User defined
```

UBC97SoilProfileType

This is 1, 2, 3, 4 or 5, indicating the soil profile type.

```
1 = SA
2 = SB
3 = SC
4 = SD
5 = SE
```
This item is applicable only when the seismic coefficients Ca and Cv are calculated per code
(UBC97SeismicCoeffFlag = 1).

UBC97Z

This is 0.075, 0.15, 0.2, 0.3 or 0.4, indicating the seismic zone factor.

This item is applicable only when the seismic coefficients Ca and Cv are calculated in accordance
with code (UBC97SeismicCoeffFlag = 1).

UBC97Ca

The seismic coefficient, Ca.

UBC97Cv

The seismic coefficient, Cv.

UBC97NearSourceFlag

This is 1 or 2, indicating if the near source factor coefficients Na and Nv are per code or user
defined.

```
1 = Per code
2 = User defined
```
This item is applicable only when the seismic coefficients Ca and Cv are calculated per code
(UBC97SeismicCoeffFlag = 1) and UBC97Z = 0.4.

UBC97SourceType

This is 1, 2 or 3, indicating the seismic source type.

```
1 = A
2 = B
3 = C
```
This item is applicable only when the seismic coefficients Ca and Cv are calculated per code
(UBC97SeismicCoeffFlag = 1), UBC97Z = 0.4, and the near source factor coefficients Na and Nv
are calculated per code (UBC97NearSourceFlag = 1).

UBC97Dist


This is the distance to the seismic source in kilometers.

This item is only applicable when the seismic coefficients Ca and Cv are calculated per code
(UBC97SeismicCoeffFlag = 1), UBC97Z = 0.4, and the near source factor coefficients Na and Nv
are calculated per code (UBC97NearSourceFlag = 1).

UBC97Na

The near source factor coefficient, Na.

This item is applicable only when the seismic coefficients Ca and Cv are user defined
(UBC97SeismicCoeffFlag = 2).

UBC97Nv

The near source factor coefficient, Nv.

This item is applicable only when the seismic coefficients Ca and Cv are user defined
(UBC97SeismicCoeffFlag = 2).

UBC97I

The importance factor.

UBC97R

The overstrength factor.

## Remarks

This function retrieves auto seismic loading parameters for the 1997 UBC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersUBC97()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long
Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim UBC97SeismicCoeffFlag As Long
Dim UBC97SoilProfileType As Long
Dim UBC97Z As Double


Dim UBC97Ca As Double
Dim UBC97Cv As Double
Dim UBC97NearSourceFlag As Long
Dim UBC97SourceType As Long
Dim UBC97Dist As Double
Dim UBC97Na As Double
Dim UBC97Nv As Double
Dim UBC97I As Double
Dim UBC97R As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign UBC97 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetUBC97("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 1, 3, 0.4, 0, 0, 1, 3, 5, 0, 0, 1.15, 6)

'get UBC97 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetUBC97("EQX", DirFlag, Eccen, PeriodFlag,
CT, UserT, UserZ, TopZ, BottomZ, UBC97SeismicCoeffFlag, UBC97SoilProfileType, UBC97Z,
UBC97Ca, UBC97Cv, UBC97NearSourceFlag, UBC97SourceType, UBC97Dist, UBC97Na,
UBC97Nv, UBC97I, UBC97R)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

SetUBC97

# GetUBC97Iso

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetUBC97Iso

## VB6 Procedure

Function GetUBC97Iso(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As
Double, ByRef UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef
UBC97IsoSeismicCoeffFlag As Long, ByRef UBC97IsoSoilProfileType As Long, ByRef
UBC97IsoZ As Double, ByRef UBC97IsoCv As Double, ByRef UBC97IsoNearSourceFlag As
Long, ByRef UBC97IsoSourceType As Long, ByRef UBC97IsoDist As Double, ByRef
UBC97IsoNv As Double, ByRef UBC97IsoRI As Double, ByRef UBC97IsoBD As Double,
ByRef UBC97IsoKDmax As Double, ByRef UBC97IsoKDmin As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a UBC97Iso auto seismic load assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ


This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

UBC97IsoSeismicCoeffFlag

This is either 1 or 2, indicating if the seismic coefficient Cv is per code or user defined.

```
1 = Per code
2 = User defined
```
UBC97IsoSoilProfileType

This is 1, 2, 3, 4 or 5, indicating the soil profile type.

```
1 = SA
2 = SB
3 = SC
4 = SD
5 = SE
```
This item is applicable only when the seismic coefficients Ca and Cv are calculated per code
(UBC97SeismicCoeffFlag = 1).

UBC97IsoZ

This is 0.075, 0.15, 0.2, 0.3 or 0.4, indicating the seismic zone factor.

This item is applicable only when the seismic coefficient Cv is calculated per code
(UBC97IsoSeismicCoeffFlag = 1).

UBC97IsoCv

The seismic coefficient, Cv.

UBC97IsoNearSourceFlag

This is either 1 or 2, indicating if the near source factor coefficient Nv is per code or user defined.

```
1 = Per code
2 = User defined
```
This item is applicable only when the seismic coefficient Cv is calculated per code
(UBC97IsoSeismicCoeffFlag = 1) and UBC97IsoZ = 0.4.

UBC97IsoSourceType

This is 1, 2 or 3, indicating the seismic source type.

```
1 = A
2 = B
3 = C
```

This item is applicable only when the seismic coefficient Cv is calculated per code
(UBC97IsoSeismicCoeffFlag = 1), UBC97IsoZ = 0.4, and the near source factor coefficient Nv is
calculated per code (UBC97IsoNearSourceFlag = 1).

UBC97IsoDist

This is the distance to the seismic source in kilometers.

This item is applicable only when the seismic coefficient Cv is calculated per code
(UBC97IsoSeismicCoeffFlag = 1), UBC97IsoZ = 0.4, and the near source factor coefficient Nv is
calculated per code (UBC97IsoNearSourceFlag = 1).

UBC97IsoNv

The near source factor coefficient, Nv.

This item is applicable only when the seismic coefficient Cv is user defined
(UBC97IsoSeismicCoeffFlag = 2).

UBC97IsoRI

The overstrength factor, Ri.

UBC97IsoBD

The coefficient for damping.

UBC97IsoKDmax

The maximum effective stiffness of the isolation system. [F/L]

UBC97IsoKDmin

The minimum effective stiffness of the isolation system. [F/L]

## Remarks

This function retrieves auto seismic loading parameters for seismically isolated buildings using the
1997 UBC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersUBC97Iso()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim PeriodFlag As Long


Dim CT As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim UBC97IsoSeismicCoeffFlag As Long
Dim UBC97IsoSoilProfileType As Long
Dim UBC97IsoZ As Double
Dim UBC97IsoCv As Double
Dim UBC97IsoNearSourceFlag As Long
Dim UBC97IsoSourceType As Long
Dim UBC97IsoDist As Double
Dim UBC97IsoNv As Double
Dim UBC97IsoRI As Double
Dim UBC97IsoBD As Double
Dim UBC97IsoKDmax As Double
Dim UBC97IsoKDmin As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign UBC97Iso parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetUBC97Iso("EQX", 1, 0.05, False, 0, 0, 1, 3,
0.4, 0, 1, 3, 5, 0, 2, 1.25, 200, 150)

'get UBC97Iso parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetUBC97Iso("EQX", DirFlag, Eccen, UserZ,
TopZ, BottomZ, UBC97IsoSeismicCoeffFlag, UBC97IsoSoilProfileType, UBC97IsoZ,
UBC97IsoCv, UBC97IsoNearSourceFlag, UBC97IsoSourceType, UBC97IsoDist, UBC97IsoNv,
UBC97IsoRI, UBC97IsoBD, UBC97IsoKDmax, UBC97IsoKDmin)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUBC97Iso

# GetUserCoefficient

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetBOCA96

## VB6 Procedure

Function GetBOCA96(ByVal Name As String, ByRef DirFlag As Long, ByRef Eccen As Double,
ByRef UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef c As
Double, ByRef k As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a User Coefficient auto seismic load
assignment.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]


BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

c

The base shear coefficient.

k

The building height exponent.

## Remarks

This function retrieves auto seismic loading parameters for User Coefficient type loading.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicParametersUserCoefficient()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DirFlag As Long
Dim Eccen As Double
Dim UserT As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim c As Double
Dim k As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern


ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign user coefficient parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetUserCoefficient("EQX", 1, 0.06, False, 0, 0,
0.15, 1.3)

'get user coefficient parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetUserCoefficient("EQX", DirFlag, Eccen,
UserZ, TopZ, BottomZ, c, k)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUserCoefficient

# GetUserLoad

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.GetUserLoad

## VB6 Procedure

Function GetUserLoad(ByVal Name As String, ByRef MyType As Long, ByRef Eccen As
Double, ByRef Num As Long, ByRef Diaph() As String, ByRef Fx() As Double, ByRef Fy() As
Double, ByRef Mz() As Double, ByRef x() As Double, ByRef y() As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern which has been assigned a User Load auto
seismic type.

MyType

This is either 1 or 2, indicating the application point type for the user load.


```
1 = User specified application point
2 = At center of mass with optional additional eccentricity
```
Eccen

The eccentricity ratio that applies to all diaphragms. This item is only applicable when MyType =
2.

Num

The number of diaphragms that can be loaded by the auto seismic load.

Diaph

This is an array that includes the names of the diaphragms that can be loaded by the auto seismic
load.

Fx

This is an array that includes the global X direction force assigned to each diaphragm. [F]

Fy

This is an array that includes the global Y direction force assigned to each diaphragm. [F]

Mz

This is an array that includes the moment about the global Z axis for each diaphragm. [FL]

x

This is an array that includes the global X-coordinate of the point where the seismic force is
applied to each diaphragm. [L]

This item is applicable only when MyType = 1.

y

This is an array that includes the global Y-coordinate of the point where the seismic force is
applied to each diaphragm. [L]

This item is applicable only when MyType = 1.

## Remarks

This function retrieves auto seismic loading parameters for User Load type auto seismic loads.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSeismicUserLoad()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyType As Long
Dim Eccen As Double
Dim Num As Long
Dim Diaph() As String
Dim Fx() As Double
Dim Fy() As Double
Dim Mz() As Double
Dim x() As Double
Dim y() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'set to auto seismic user load
ret = SapModel.LoadPatterns.AutoSeismic.SetUserLoad("EQX", 1)

'set to auto seismic user load values
ret = SapModel.LoadPatterns.AutoSeismic.SetUserLoadValue("EQX", "Diaph1", 20, 4, 1000,
0, 0)
ret = SapModel.LoadPatterns.AutoSeismic.SetUserLoadValue("EQX", "Diaph2", 40, 8, 2000,
0, 0)


'get auto seismic user load parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetUserLoad("EQX", MyType, Eccen, Num,
Diaph, Fx, Fy, Mz, x, y)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUserLoad

SetUserLoadValue

# SetASCE716_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetASCE716

## VB6 Procedure

Function SetASCE716_1(ByVal Name As String, ByRef nDir() As Boolean, ByRef Eccen As
Double, ByRef PeriodFlag As Long, ByRef CtType As Long, ByRef UserT As Double, ByRef
UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef R As Double,
ByRef Omega As Double, ByRef Cd As Double, ByRef I As Double, ByRef Ss As Double,
ByRef S1 As Double, ByRef TL As Double, ByRef SiteClass As Long, ByRef Fa As Double,
ByRef Fv As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

nDir

This is an array with 2 inputs that indicate the seismic load direction.

```
nDir(1) = True = Global X
```

```
nDir(2) = True = Global Y
```
If nDir(1) and nDir(2) are both True or False, the default direction in Global X will be assigned.

Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CtType

This is 0, 1, 2 or 3, indicating the values of Ct and x. This item applies when the PeriodFlag item
is 1 or 2.

```
0 = Ct = 0.028 (ft), x = 0.8
1 = Ct = 0.016 (ft), x = 0.9
2 = Ct = 0.03 (ft), x = 0.75
3 = Ct = 0.02 (ft), x = 0.75
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

R

The response modification factor.

Omega

The system overstrength factor.

Cd

The deflection amplification factor.


### I

The occupancy importance factor.

SS, S1

The seismic coefficients Ss and S1. This item is used only when ASCE716Option = 2.

TL

The long-period transition period. [s]

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa, Fv

The site coefficients Fa and Fv. These items are used only when ASCE716SiteClass is 5 or 6.

## Remarks

This function assigns auto seismic loading parameters for the 2016 ASCE 7 code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicASCE716_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim nDir() As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart


'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(e3DFrameType.BeamSlab, 2, 144, 3, 336, 2, 432 )

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", eLoadPatternType.Quake)

'dimension ASCE716 parameters

Dim nDir() As Boolean

Dim Eccen As Double

Dim PeriodFlag As Long

Dim CtType As Long

Dim UserT As Double

Dim UserZ As Boolean

Dim TopZ As Double

Dim BottomZ As Double

Dim R As Double

Dim Omega As Double

Dim Cd As Double

Dim I As Double

Dim SS As Double

Dim S1 As Double

Dim TL As Double

Dim SiteClass As Long

Dim Fa As Double

Dim Fv As Double

ReDim nDir(1)


nDir(0) = True

TopZ = 32

BottomZ = 14

'set ASCE716 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetASCE716_1("EQX", nDir, 0.04, 3, 1, 1.76,
True, TopZ, BottomZ, 6, 3.5, 6.5, 1.5, 1.9, 1.1, 8, 3, 0, 0)

'get ASCE716 parameters
ret = SapModel.LoadPatterns.AutoSeismic.GetASCE716_1("EQX", nDir, Eccen, PeriodFlag,
CtType, UserT, UserZ, TopZ, BottomZ, R, Omega, Cd, I, SS, S1, TL, SiteClass, Fa, Fv)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.2.0.

This function replaced the obsolete function SetASCE16.

## See Also

GetASCE716_1

# SetAS11702007

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetAS11702007

## VB6 Procedure

Function SetAS11702007(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal PeriodFlag As Long, ByVal CT As Double, ByVal UserT As Double, ByVal
UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal AS2007SiteClass
As Long, ByVal AS2007kp As Double, ByVal AS2007Z As Double, ByVal AS2007Sp As
Double, ByVal AS2007Mu As Double) As Long


## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified kt factor. This item applies when the PeriodFlag item is 1.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

AS2007SiteClass

This is 1, 2, 3, 4 or 5, indicating the site class.

```
1 = A
2 = B
3 = C
```

### 4 = D

### 5 = E

AS2007kp

The probability factor, kp.

AS2007Z

The hazard factor, Z.

AS2007Sp

The structural performance factor, Sp.

AS2007Mu

The structural ductility factor, u.

## Remarks

This function assigns auto seismic loading parameters for the AS 1170.4 2007 code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicAS11702007()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign AS 1170 2007 parameters


ret = SapModel.LoadPatterns.AutoSeismic.SetAS11702007("EQX", 2, 0.1, 2, 0.075, 0, False,
0, 0, 3, 1.3, 0.09, 0.77, 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.00.

## See Also

GetAS11702007

# SetBOCA96

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetBOCA96

## VB6 Procedure

Function SetBOCA96(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal CT As Double, ByVal UserT As Double, ByVal UserZ As
Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal BOCA96Aa As Double,
ByVal BOCA96Av As Double, ByVal BOCA96S As Double, ByVal BOCA96R As Double) As
Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag


This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor. This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

BOCA96Aa

The effective peak acceleration coefficient.

BOCA96Av

The effective peak velocity-related coefficient.

BOCA96S

This is 1, 1.2, 1.5 or 2, indicating the site coefficient.

BOCA96R

The response modification factor.

## Remarks

This function assigns auto seismic loading parameters for the 1996 BOCA code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example


Sub AssignSeismicBOCA96()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign BOCA96 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetBOCA96("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 0.4, 0.4, 1.5, 8)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetBOCA96

# SetChinese2010

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetChinese2010


## VB6 Procedure

Function SetChinese2010(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal PeriodFlag As Long, ByVal UserT As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal JGJ32010AlphaMax As Double, ByVal
JGJ32010SI As Long, ByVal JGJ32010DampRatio As Double, ByVal JGJ32010Tg As Double,
ByVal JGJ32010PTDF As Double, ByVal EnhancementFactor As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is 1, 2 or 3, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
3 = Global Z
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is either 2 or 3, indicating the time period option.

```
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

JGJ32010AlphaMax


The maximum influence factor.

JGJ32010SI

This is 1, 2, 3, 4, 5 or 6, indicating the seismic intensity.

```
1 = 6 (0.05g)
2 = 7 (0.10g)
3 = 7 (0.15g)
4 = 8 (0.20g)
5 = 8 (0.30g)
6 = 9 (0.40g)
```
JGJ32010DampRatio

The damping ratio.

JGJ32010Tg

The characteristic ground period. [s]

JGJ32010PTDF

The period time discount factor.

EnhancementFactor

The enhancement factor.

## Remarks

This function assigns auto seismic loading parameters for the Chinese 2010 code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicChinese2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel


'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign Chinese 2010 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetChinese2010("EQX", 1, 0.05, 2, 0, False, 0, 0,
0.16, 4, 0.06, 0.4, 1, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 15.0.2.

## See Also

GetChinese2010

# SetDiaphragmEccentricityOverride

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetDiaphragmEccentricityOverride

## VB6 Procedure

Function SetDiaphragmEccentricityOverride(ByVal Name As String, ByVal Diaph As String,
ByVal Eccen As Double, Optional ByVal Delete As Boolean = False) As Long

## Parameters

Name

The name of an existing Quake-type load pattern that has an auto seismic load assigned.

Diaph

The name of an existing special rigid diaphragm constraint, that is, a diaphragm constraint with
the following features:


1. The constraint type is CONSTRAINT_DIAPHRAGM = 2.
2. The constraint coordinate system is Global.
3. The constraint axis is Z.

Eccen

The eccentricity applied to the specified diaphragm. [L]

Delete

If this item is True, the eccentricity override for the specified diaphragm is deleted.

## Remarks

This function assigns diaphragm eccentricity overrides for auto seismic loads. This function does
not apply for User Load type auto seismic loads.

The function returns zero if the overrides are successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub AssignSeismicDiaphragmEccentricityOverride()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection


ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign BOCA96 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetBOCA96("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 0.4, 0.4, 1.5, 8)

'assign diaphragm eccentricity override
ret = SapModel.LoadPatterns.AutoSeismic.SetDiaphragmEccentricityOverride("EQX",
"Diaph1", 50)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Modified optional argument Delete to be ByVal in version 12.0.1.

## See Also

GetDiaphragmEccentricityOverride

GetSpecialRigidDiaphragmList

# SetEurocode82004_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetEurocode82004_1

## VB6 Procedure

Function SetEurocode82004_1(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal PeriodFlag As Long, ByVal CT As Double, ByVal UserT As Double, ByVal
UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal
EURO2004Country As Long, ByVal EURO2004SpectrumType As Long, ByVal
EURO2004GroundType As Long, ByVal EURO2004ag As Double, ByVal EURO2004S As


Double, ByVal EURO2004Tb As Double, ByVal EURO2004Tc As Double, ByVal
EURO2004Td As Double, ByVal EURO2004Beta As Double, ByVal EURO2004q As Double,
ByVal EURO2004Lambda As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
```
```
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
```
```
2 = Program calculated
```
```
3 = User defined
```
CT

The code-specified Ct factor. This item applies when the PeriodFlag item is 1.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3.[s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]


EURO2004Country

This is 0, 1, 5, 6, or 10 indicating the country for which the Nationally Determined Parameters
(NDPs) are specified.

```
0 = Other (NDPs are user specified)
```
```
1 = CEN Default
```
```
5 = Norway
```
```
6 = Singapore
10 = Portugal
```
EURO2004SpectrumType

This is 1 or 2, indicating the spectrum type.

```
1 = Type 1
```
```
2 = Type 2 (Does not apply when EURO2004Country = 6)
```
EURO2004GroundType

This is 1, 2, 3, 4, 5, or 6, indicating the ground type.

```
1 = A (Does not apply when EURO2004Country = 6)
```
```
2 = B (Does not apply when EURO2004Country = 6)
```
```
3 = C
```
```
4 = D
```
```
5 = E (Does not apply when EURO2004Country = 6)
```
```
6 = S1 (Only applies when EURO2004Country = 6)
```
EURO2004ag

The design ground acceleration in g, ag.

EURO2004S

The soil factor, S. If the EURO2004Country item is not 0, the input value for this item is ignored.

EURO2004Tb

The lower limit of period of the constant spectral acceleration branch, Tb. If the
EURO2004Country item is not 0, the input value for this item is ignored.

EURO2004Tc


The upper limit of period of the constant spectral acceleration branch, Tc. If the
EURO2004Country item is not 0, the input value for this item is ignored.

EURO2004Td

The period defining the start of the constant displacement range, Td. If the EURO2004Country
item is not 0, the input value for this item is ignored.

EURO2004Beta

The lower bound factor, Beta. If the EURO2004Country item is not 0, the input value for this item
is ignored.

EURO2004q

The behavior factor, q.

EURO2004Lambda

The correction factor, Lambda.

## Remarks

This function assigns auto seismic loading parameters for the Eurocode 8 2004 code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicEurocode82004()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign Eurocode 8 2004 parameters


ret = SapModel.LoadPatterns.AutoSeismic.SetEurocode82004_1("EQX", 2, 0.1, 2, 0.075, 0,
False, 0, 0, 1, 1, 2, 0.4, 1, 1, 1, 1, 0.2, 2, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.1.0.

This function supersedes SetEurocode82004.

Added Portugal as a Country parameter in SAP2000 Version 15.0.0 and CSiBridge Version
15.1.0.

Added Singapore as a Country parameter in v20.1.0.

## See Also

GetEurocode82004_1

# SetIBC2003

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetIBC2003

## VB6 Procedure

Function SetIBC2003(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal CT As Double, ByVal UserT As Double, ByVal UserZ As
Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal IBC2003SG As Long,
ByVal IBC2003SeismicCoeffFlag As Long, ByVal IBC2003Site As Long, ByVal IBC2003SS As
Double, ByVal IBC2003S1 As Double, ByVal IBC2003Fa As Double, ByVal IBC2003Fv As
Double, ByVal IBC2003R As Double, ByVal IBC2003Omega As Double, ByVal IBC2003Cd As
Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.


```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor (ft). This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

IBC2003SG

This is 1, 2 or 3, indicating the seismic group.

```
1 = I
2 = II
3 = III
```
IBC2003SeismicCoeffFlag

This is either 1 or 2, indicating the seismic coefficient option.

```
1 = Coefficients are per code
2 = Coefficients are user defined
```
IBC2003Site


This is 1, 2, 3, 4 or 5, indicating the site class. This item is only used when the
IBC2003SeismicCoeffFlag = 1.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
IBC2003SS

The response acceleration for short periods, (g).

IBC2003S1

The response acceleration for a one second period, (g).

IBC2003Fa

The site coefficient Fa. This item is used only when the IBC2003SeismicCoeffFlag = 2.

IBC2003Fv

The site coefficient Fv. This item is used only when the IBC2003SeismicCoeffFlag = 2

IBC2003R

The response modification factor.

IBC2003Omega

The system overstrength factor.

IBC2003Cd

The deflection amplification factor.

## Remarks

This function assigns auto seismic loading parameters for the 2003 IBC code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicIBC2003()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IBC2003 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIBC2003("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 1, 1, 3, 1, 0.4, 0, 0, 8, 3, 5.5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetIBC2003

# SetIBC2006

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetIBC2006

## VB6 Procedure

Function SetIBC2006(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal IBC2006CtType As Long, ByVal UserT As Double, ByVal
UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal IBC2006R As


Double, ByVal IBC2006Omega As Double, ByVal IBC2006Cd As Double, ByVal IBC2006I As
Double, ByVal IBC2006Option As Long, ByVal IBC2006Latitude As Double, ByVal
IBC2006Longitude As Double, ByVal IBC2006ZipCode As String, ByVal IBC2006SS As
Double, ByVal IBC2006S1 As Double, ByVal IBC2006TL As Double, ByVal IBC2006SiteClass
As Long, ByVal IBC2006Fa As Double, ByVal IBC2006Fv As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
IBC2006CtType

This is 0, 1, 2 or 3, indicating the values of Ct and x. This item applies when the PeriodFlag item
is 1 or 2.

```
0 = Ct = 0.028 (ft), x = 0.8
1 = Ct = 0.016 (ft), x = 0.9
2 = Ct = 0.03 (ft), x = 0.75
3 = Ct = 0.02 (ft), x = 0.75
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]


BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

IBC2006R

The response modification factor.

IBC2006Omega

The system overstrength factor.

IBC2006Cd

The deflection amplification factor.

IBC2006I

The occupancy importance factor.

IBC2006Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
IBC2006Latitude, IBC2006Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when IBC2006Option = 0.

IBC2006ZipCode

The zip code for which the seismic coefficients are obtained. This item is used only when
IBC2006Option = 1.

IBC2006SS, IBC2006S1

The seismic coefficients Ss and S1. This item is used only when IBC2006Option = 2.

IBC2006TL

The long-period transition period. [s]

IBC2006SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```

### 6 = F

IBC2006Fa, IBC2006Fv

The site coefficients Fa and Fv. These items are used only when IBC2006SiteClass= 6.

## Remarks

This function assigns auto seismic loading parameters for the 2006 IBC code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicIBC2006()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IBC2006 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIBC2006("EQX", 1, 0.05, 1, 1, 0, False, 0, 0, 8,
3, 5.5, 1, 1, 0, 0, "94704", 0, 0, 8, 3, 0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetIBC2006

# SetIBC2009

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetIBC2009

## VB6 Procedure

Function SetIBC2009(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal CtType As Long, ByVal UserT As Double, ByVal UserZ As
Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal R As Double, ByVal
Omega As Double, ByVal Cd As Double, ByVal I As Double, ByVal IBC2009Option As Long,
ByVal Latitude As Double, ByVal Longitude As Double, ByVal ZipCode As String, ByVal SS As
Double, ByVal S1 As Double, ByVal TL As Double, ByVal SiteClass As Long, ByVal Fa As
Double, ByVal Fv As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```

CtType

This is 0, 1, 2 or 3, indicating the values of Ct and x. This item applies when the PeriodFlag item
is 1 or 2.

```
0 = Ct = 0.028 (ft), x = 0.8
1 = Ct = 0.016 (ft), x = 0.9
2 = Ct = 0.03 (ft), x = 0.75
3 = Ct = 0.02 (ft), x = 0.75
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

R

The response modification factor.

Omega

The system overstrength factor.

Cd

The deflection amplification factor.

I

The occupancy importance factor.

IBC2009Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
Latitude, Longitude


The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when IBC2009Option = 0.

ZipCode

The zip code for which the seismic coefficients are obtained. This item is used only when
IBC2009Option = 1.

SS, S1

The seismic coefficients Ss and S1. This item is used only when IBC2009Option = 2.

TL

The long-period transition period. [s]

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa, Fv

The site coefficients Fa and Fv. These items are used only when IBC2009SiteClass= 6.

## Remarks

This function assigns auto seismic loading parameters for the 2009 IBC code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicIBC2009()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object


Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IBC2009 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIBC2009("EQX", 1, 0.05, 1, 1, 0, False, 0, 0, 8,
3, 5.5, 1, 1, 0, 0, "94704", 0, 0, 8, 3, 0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

GetIBC2009

# SetIBC2012

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetIBC2012

## VB6 Procedure

Function SetIBC2012(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal CtType As Long, ByVal UserT As Double, ByVal UserZ As
Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal R As Double, ByVal
Omega As Double, ByVal Cd As Double, ByVal I As Double, ByVal IBC2012Option As Long,
ByVal Latitude As Double, ByVal Longitude As Double, ByVal ZipCode As String, ByVal SS As
Double, ByVal S1 As Double, ByVal TL As Double, ByVal SiteClass As Long, ByVal Fa As
Double, ByVal Fv As Double) As Long

## Parameters

Name


The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CtType

This is 0, 1, 2 or 3, indicating the values of Ct and x. This item applies when the PeriodFlag item
is 1 or 2.

```
0 = Ct = 0.028 (ft), x = 0.8
1 = Ct = 0.016 (ft), x = 0.9
2 = Ct = 0.03 (ft), x = 0.75
3 = Ct = 0.02 (ft), x = 0.75
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

R

The response modification factor.

Omega


The system overstrength factor.

Cd

The deflection amplification factor.

I

The occupancy importance factor.

IBC2012Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when IBC2012Option = 0.

ZipCode

The zip code for which the seismic coefficients are obtained. This item is used only when
IBC2012Option = 1.

SS, S1

The seismic coefficients Ss and S1. This item is used only when IBC2012Option = 2.

TL

The long-period transition period. [s]

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa, Fv

The site coefficients Fa and Fv. These items are used only when IBC2012SiteClass= 6.

## Remarks

This function assigns auto seismic loading parameters for the 2012 IBC code.


The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicIBC2012()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IBC2012 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIBC2012("EQX", 1, 0.05, 1, 1, 0, False, 0, 0, 8,
3, 5.5, 1, 1, 0, 0, "94704", 0, 0, 8, 3, 0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

GetIBC2012

# SetIS1893_2002


## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetIS1893_2002

## VB6 Procedure

Function SetIS1893_2002(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal PeriodFlag As Long, ByVal CT As Double, ByVal UserT As Double, ByVal
UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal INZFlag As
Long, ByVal INZ As Double, ByVal INS As Long, ByVal INI As Double, ByVal INR As
Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor (m). This item applies when the PeriodFlag item is 1.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ


This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

INZFlag

This is either 1 or 2, indicating if the seismic zone factor is per code or user defined.

```
1 = Per code
2 = User defined
```
INZ

The seismic zone factor, Z.

If the seismic zone factor is per code (INZFlag = 1), this item should be one of the following:
0.10, 0.16, 0.24, 0.36.

INS

This is 1, 2 or 3, indicating the soil type.

```
1 = I
2 = II
3 = III
```
BOCA96R

The response modification factor.

INR

The importance factor.

INR

The response modification factor.

## Remarks

This function assigns auto seismic loading parameters for the 2002 IS1893 code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicIS18932002()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign IS1893_2002 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetIS1893_2002("EQX", 1, 0.05, 1, 0.075, 0,
False, 0, 0, 1, 0.36, 3, 1, 5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetIS1893_2002

# SetNBCC2015

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNBCC2015


## VB6 Procedure

Function SetNBCC2015(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal CtType As Long, ByVal PeriodFlag As Long, ByVal UserT As Double, ByVal
UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal PGA As Double,
ByVal S02 As Double, ByVal S05 As Double, ByVal S1 As Double, ByVal S2 As Double, ByVal
S5 As Double, ByVal S10 As Double, ByVal SiteClass As Long, ByVal F02 As Double, ByVal
F05 As Double, ByVal F1 As Double, ByVal F2 As Double, ByVal F5 As Double, ByVal F10 As
Double, ByVal I As Double, ByVal Mv As Double, ByVal Rd As Double, ByVal Ro As Double)
As Long

## Parameters

Name

The name of an existing Quake-type load pattern

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

CtType

This is 0, 1, 2, 3 or 4, indicating the structure type.

```
0 = Steel moment frame
1 = Concrete moment frame
2 = Other moment frame
3 = Braced frame
4 = Shear wall
```
PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Code
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.


TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

PGA

The peak ground acceleration.

S02

The spectral acceleration at a 0.2 second period.

S05

The spectral acceleration at a 0.5 second period.

S1

The spectral acceleration at a 1 second period.

S2

The spectral acceleration at a 2 second period.

S5

The spectral acceleration at a 5 second period.

S10

The spectral acceleration at a 10 second period.

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
F02

The site coefficient at a 0.2 second period. This item is read when the site class is F only.

F05

The site coefficient at a 0.5 second period. This item is read when the site class is F only.


### F1

The site coefficient at a 1 second period. This item is read when the site class is F only.

F2

The site coefficient at a 2 second period. This item is read when the site class is F only.

F5

The site coefficient at a 5 second period. This item is read when the site class is F only.

F10

The site coefficient at a 10 second period. This item is read when the site class is F only.

I

The importance factor.

Mv

The higher mode factor.

Rd

The ductility modifier.

Ro

The overstrength modifier.

## Remarks

This function retrieves auto seismic loading parameters for the 2015 NBCC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNBCC2015()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart


'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NBCC2015 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNBCC2015("EQX", 2, 0.1, 2, 1, 0, False, 0, 0,
0.6, 1.1, 0.7, 0.35, 0.2, 0.03, 0.01, 6, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.2, 6, 1.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

## See Also

GetNBCC2015

# SetNBCC2010

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNBCC2010

## VB6 Procedure

Function SetNBCC2010(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal CtType As Long, ByVal PeriodFlag As Long, ByVal UserT As Double, ByVal
UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal PGA As Double,
ByVal S02 As Double, ByVal S05 As Double, ByVal S1 As Double, ByVal S2 As Double, ByVal


S4 As Double, ByVal SiteClass As Long, ByVal Fa As Double, ByVal Fv As Double, ByVal I As
Double, ByVal Mv As Double, ByVal Rd As Double, ByVal Ro As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern with a NBCC2010 auto seismic load assignment.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

CtType

This is 0, 1, 2, 3 or 4, indicating the structure type.

```
0 = Steel moment frame
1 = Concrete moment frame
2 = Other moment frame
3 = Braced frame
4 = Shear wall
```
PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Code
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ


This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

PGA

The peak ground acceleration.

S02

The spectral acceleration at a 0.2 second period.

S05

The spectral acceleration at a 0.5 second period.

S1

The spectral acceleration at a 1 second period.

S2

The spectral acceleration at a 2 second period.

S4

The spectral acceleration at a 4 second period.

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa

The site coefficient, Fa. This item is read when the site class is F only.

Fv

The site coefficient, Fv. This item is read when the site class is F only.

I

The importance factor.

Mv

The higher mode factor.


Rd

The ductility modifier.

Ro

The overstrength modifier.

## Remarks

This function retrieves auto seismic loading parameters for the 2010 NBCC code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNBCC2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NBCC2010 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNBCC2010("EQX", 2, 0.1, 2, 1, 0, False, 0, 0,
0.6, 1.1, 0.7, 0.35, 0.2, 0.1, 6, 1.8, 2, 1.5, 1.2, 6, 1.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 19.0.0.

## See Also

GetNBCC2010

# SetNBCC2005

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNBCC2005

## VB6 Procedure

Function SetNBCC2005(ByVal Name As String, ByVal DirFlag As Long, ByVal eccen As
Double, ByVal NBCC2005CtType As Long, ByVal PeriodFlag As Long, ByVal UserT As
Double, ByVal UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal
NBCC2005PGA As Double, ByVal NBCC2005S02 As Double, ByVal NBCC2005S05 As
Double, ByVal NBCC2005S1 As Double, ByVal NBCC2005S2 As Double, ByVal
NBCC2005SiteClass As Long, ByVal NBCC2005Fa As Double, ByVal NBCC2005Fv As
Double, ByVal NBCC2005I As Double, ByVal NBCC2005Mv As Double, ByVal NBCC2005Rd
As Double, ByVal NBCC2005Ro As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

NBCC2005CtType

This is 0, 1, 2, 3 or 4, indicating the structure type.


```
0 = Steel moment frame
1 = Concrete moment frame
2 = Other moment frame
3 = Braced frame
4 = Shear wall
```
NBCC95DS

This item applies only when the NBCCPFlag = 2. It is the dimension of the lateral load resisting
system in the direction of the applied forces. [L]

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Code
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

NBCC2005PGA

The peak ground acceleration.

NBCC2005S02

The spectral acceleration at a 0.2 second period.

NBCC2005S05

The spectral acceleration at a 0.52 second period.

NBCC2005S1

The spectral acceleration at a 1 second period.

NBCC2005S2


The spectral acceleration at a 2 second period.

NBCC2005SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
NBCC2005Fa

The site coefficient, Fa. This item is read when the site class is F only.

NBCC2005Fv

The site coefficient, Fv. This item is read when the site class is F only.

NBCC2005I

The importance factor.

NBCC2005Mv

The higher mode factor.

NBCC2005Rd

The ductility modifier.

NBCC2005Ro

The overstrength modifier.

## Remarks

This function assigns auto seismic loading parameters for the 2005 NBCC code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNBCC2005()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NBCC2005 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNBCC2005("EQX", 2, 0.1, 2, 1, 0, False, 0, 0,
0.6, 1.1, 0.7, 0.35, 0.2, 6, 1.8, 2, 1.5, 1.2, 6, 1.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetNBCC2005

# SetNBCC95

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNBCC95

## VB6 Procedure

Function SetNBCC95(ByVal Name As String, ByVal DirFlag As Long, ByVal eccen As Double,
ByVal NBCCPFlag As Long, ByVal NBCC95DS As Double, ByVal PeriodFlag As Long, ByVal
UserT As Double, ByVal UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As
Double, ByVal NBCC95ZA As Long, ByVal NBCC95ZV As Long, ByVal NBCC95ZVFlag As
Long, ByVal NBCC95ZVR As Double, ByVal NBCC95I As Double, ByVal NBCC95F As
Double, ByVal NBCC95R As Double) As Long


## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

NBCCPFlag

This is either 1 or 2, indicating the structure type.

```
1 = Moment frame
2 = Other
```
NBCC95DS

This item applies only when the NBCCPFlag = 2. It is the dimension of the lateral load resisting
system in the direction of the applied forces. [L]

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Code
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]


### NBCC95ZA

This is 0, 1, 2, 3, 4, 5 or 6, indicating the acceleration related zone, Za.

NBCC95ZV

This is 0, 1, 2, 3, 4, 5 or 6, indicating the velocity related zone, Zv.

NBCC95ZVFlag

This is either 1 or 2, indicating how the zonal velocity ratio, V, is specified.

```
1 = From code based on Zv
2 = User specified
```
NBCC95ZVR

The zonal velocity ratio, V. This item is used only when NBCC95ZVFlag = 2.

NBCC95I

The importance factor.

NBCC95F

The foundation factor.

NBCC95R

The force modification factor.

## Remarks

This function assigns auto seismic loading parameters for the 1995 NBCC code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNBCC95()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object


Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NBCC95 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNBCC95("EQX", 1, 0.05, 1, 0, 1, 0, False, 0, 0,
4, 5, 1, 0, 1, 1.3, 4)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetNBCC95

# SetNEHRP97

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNEHRP97

## VB6 Procedure

Function SetNEHRP97(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal PeriodFlag As Long, ByVal CT As Double, ByVal UserT As Double, ByVal
UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal NEHRP97SG As
Long, ByVal NEHRP97SeismicCoeffFlag As Long, ByVal NEHRP97Site As Long, ByVal
NEHRP97SS As Double, ByVal NEHRP97S1 As Double, ByVal NEHRP97Fa As Double, ByVal
NEHRP97Fv As Double, ByVal NEHRP97R As Double) As Long


## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor. This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

NEHRP97SG

This is 1, 2 or 3, indicating the seismic group.

```
1 = I
2 = II
3 = III
```

NEHRP97SeismicCoeffFlag

This is either 1 or 2, indicating the seismic coefficient option.

```
1 = Coefficients are per code
2 = Coefficients are user defined
```
NEHRP97Site

This is 1, 2, 3, 4 or 5, indicating the site class. This item is used only when the
NEHRP97SeismicCoeffFlag = 1.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
NEHRP97SS

The response acceleration for short periods, (g).

NEHRP97S1

The response acceleration for a one second period, (g).

NEHRP97Fa

The site coefficient Fa. This item is used only when the NEHRP97SeismicCoeffFlag = 2.

NEHRP97Fv

The site coefficient Fv. This item is used only when the NEHRP97SeismicCoeffFlag = 2

NEHRP97R

The response modification factor.

## Remarks

This function assigns auto seismic loading parameters for the 1997 NEHRP code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNEHRP97()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NEHRP97 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNEHRP97("EQX", 1, 0.05, 1, 0.035, 0, False,
0, 0, 1, 1, 3, 1, 0.4, 0, 0, 8)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetNEHRP97

# SetNone

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNone

## VB6 Procedure

Function SetNone(ByVal Name As String) As Long


## Parameters

Name

The name of an existing Quake-type load pattern.

## Remarks

This function sets the auto seismic loading type for the specified load pattern to None.

The function returns zero if the loading type is successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNone()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign BOCA96 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetBOCA96("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 0.4, 0.4, 1.5, 8)

'set auto seismic loading type to None
ret = SapModel.LoadPatterns.AutoSeismic.SetNone("EQX")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetNTC2008

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNTC2008

## VB6 Procedure

Function SetNTC2008(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal C1Type As Long, ByVal UserT As Double, ByVal UserZ As
Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal ParamsOption As Long,
ByVal Latitude As Double, ByVal Longitude As Double, ByVal Island As Long, ByVal
LimitState As Long, ByVal UsageClass As Long, ByVal NomLife As Double, ByVal PeakAccel
As Double, ByVal F0 As Double, ByVal Tcs As Double, ByVal SpecType As Long, ByVal
SoilType As Long, ByVal Topography As Long, ByVal hRatio As Double, ByVal Damping As
Double, ByVal q As Double, ByVal lambda As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```

CIType

This is 0, 1, 2 or 3, indicating the values of C1. This item applies when the PeriodFlag item is 1 or
2.

```
1 = C1 = 0.085 (m)
2 = C1 = 0.075 (m)
3 = C1 = 0.05 (m)
```
UserT

The user specified time period. This item is meaningful when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

ParamsOption

This is 1, 2, or 3, indicating the option for defining the parameters.

```
1 = by latitude and longitude
2 = by island
3 = user specified
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when ParamsOption = 1.

Island

This is one of the following values. This item is used only when ParamsOption = 2.

```
1 = Alicudi
2 = Arcipelago Toscano
3 = Filcudi
4 = Isole Egadi
5 = Lampedusa
6 = Linosa
7 = Lipari
8 = Palmarola
9 = Panarea
10 = Pantelleria
```

```
11 = Ponza
12 = Salina
13 = Santo Stefano
14 = Sardegna
15 = Stromboli
16 = Tremiti
17 = Ustica
18 = Ventotene
19 = Vulcano
20 = Zannone
```
LimitState

This is 1, 2, 3, or 4, indicating the limit state.

```
1 = SLO
2 = SLD
3 = SLV
4 = SLC
```
UsageClass

This is 1, 2, 3, or 4, indicating the usage class.

```
1 = I
2 = II
3 = III
4 = IV
```
NomLife

The nominal life to be considered.

PeakAccel

The peak ground acceleration, ag/g.

F0

The magnitude factor, F0.

Tcs

The reference period, Tc* [s].

SpecType

This is 1, 2, 3, or 4, indicating the type of spectrum to consider.

```
1 = Elastic horizontal
2 = Elastic vertical
3 = Design horizontal
4 = Design vertical
```
SoilType


This is 1, 2, 3, 4, or 5, indicating the subsoil type.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
Topography

This is 1, 2, 3, or 4, indicating the topography type.

```
1 = T1
2 = T2
3 = T3
4 = T4
```
hRatio

The ratio for the site altitude at the base of the hill to the height of the hill.

Damping

The damping, in percent. This is only applicable for SpecType 1 and 2.

q

The behavior correction factor. This is only applicable for SpecType 3 and 4.

lambda

A correction factor.

## Remarks

This function assigns auto seismic loading parameters for the NTC 2008 code.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNTC2008()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application


SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", eLoadPatternType_QUAKE)

'assign NTC2008 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNTC2008("EQX", 1, 0.05, 1, 1, 0, False, 0, 0,
3, 0, 0, 1, 1, 1, 50, 0.2, 2.4, 0.3, 3, 2, 1, 1, 5, 1, 0.85)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 18.1.0.

## See Also

GetNTC2008

# SetNTC2018

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNTC2018

## VB6 Procedure

Function SetNTC2018(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal UserT As Double, ByVal UserZ As Boolean, ByVal TopZ As
Double, ByVal BottomZ As Double, ByVal ParamsOption As Long, ByVal Latitude As Double,
ByVal Longitude As Double, ByVal Island As Long, ByVal LimitState As Long, ByVal
UsageClass As Long, ByVal NomLife As Double, ByVal PeakAccel As Double, ByVal F0 As
Double, ByVal Tcs As Double, ByVal SpecType As Long, ByVal SoilType As Long, ByVal
Topography As Long, ByVal hRatio As Double, ByVal Damping As Double, ByVal q As Double,
ByVal lambda As Double ) As Long


## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item is meaningful when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

ParamsOption

This is 1, 2, or 3, indicating the option for defining the parameters.

```
1 = by latitude and longitude
2 = by island
3 = user specified
```
Latitude, Longitude


The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when ParamsOption = 1.

Island

This is one of the following values. This item is used only when ParamsOption = 2.

```
1 = Alicudi
2 = Arcipelago Toscano
3 = Filcudi
4 = Isole Egadi
5 = Lampedusa
6 = Linosa
7 = Lipari
8 = Palmarola
9 = Panarea
10 = Pantelleria
11 = Ponza
12 = Salina
13 = Santo Stefano
14 = Sardegna
15 = Stromboli
16 = Tremiti
17 = Ustica
18 = Ventotene
19 = Vulcano
20 = Zannone
```
LimitState

This is 1, 2, 3, or 4, indicating the limit state.

```
1 = SLO
2 = SLD
3 = SLV
4 = SLC
```
UsageClass

This is 1, 2, 3, or 4, indicating the usage class.

```
1 = I
2 = II
3 = III
4 = IV
```
NomLife

The nominal life to be considered.

PeakAccel

The peak ground acceleration, ag/g.

F0


The magnitude factor, F0.

Tcs

The reference period, Tc* [s].

SpecType

This is 1, 2, 3, or 4, indicating the type of spectrum to consider.

```
1 = Elastic horizontal
2 = Elastic vertical
3 = Design horizontal
4 = Design vertical
```
SoilType

This is 1, 2, 3, 4, or 5, indicating the subsoil type.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
Topography

This is 1, 2, 3, or 4, indicating the topography type.

```
1 = T1
2 = T2
3 = T3
4 = T4
```
hRatio

The ratio for the site altitude at the base of the hill to the height of the hill.

Damping

The damping, in percent. This is only applicable for SpecType 1 and 2.

q

The behavior correction factor. This is only applicable for SpecType 3 and 4.

lambda

A correction factor.

## Remarks

This function assigns auto seismic loading parameters for the NTC 2018 code.


The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNTC2018()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", eLoadPatternType_QUAKE)

'assign NTC2018 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNTC2018("EQX", 1, 0.05, 1, 0, False, 0, 0, 3,
0, 0, 1, 1, 1, 50, 0.2, 2.4, 0.3, 3, 2, 1, 1, 5, 1, 0.85)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v20.1.0.

## See Also

GetNTC2018


# SetUBC94

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetUBC94

## VB6 Procedure

Function SetUBC94(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal CT As Double, ByVal UserT As Double, ByVal UserZ As
Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal UBC94ZFlag As Long,
ByVal UBC94Z As Double, ByVal UBC94S As Double, ByVal UBC94I As Double, ByVal
UBC94RW As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor. This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.


TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

UBC94ZFlag

This is either 1 or 2, indicating if the seismic zone factor is per code or user defined.

```
1 = Per code
2 = User defined
```
UBC94Z

The seismic zone factor, Z.

If the seismic zone factor is per code (UBC94ZFlag = 1), this item should be one of the following:
0.075, 0.15, 0.20, 0.30, 0.40.

UBC94S

This is 1, 1.2, 1.5 or 2, indicating the site coefficient.

UBC94I

The importance factor.

UBC94RW

The numerical coefficient, Rw.

## Remarks

This function assigns auto seismic loading parameters for the 1994 UBC code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicUBC94()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign UBC94 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetUBC94("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 1, 0.4, 1.2, 1.15, 8)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetUBC94

# SetNZS11702004_2

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetNZS11702004_2

## VB6 Procedure

Function SetNZS11702004_2(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal PeriodFlag As Long, ByVal UserT As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal NZS2004SiteClass As Long, ByVal
NZS2004Z As Double, ByVal NZS2004R As Double, ByVal NZS2004DIST As Double, ByVal


NZS2004Sp As Double, ByVal NZS2004Mu As Double, ByVal NZS2004ConsiderTSite As
Boolean, ByVal NZS2004TSite As Double, ByVal NZS2004ConsiderSingleStory As Boolean) As
Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

**UserZ**

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

NZS2004SiteClass

This is 1, 2, 3, 4 or 5, indicating the site class.

```
1 = A
2 = B
3 = C
```

### 4 = D

### 5 = E

### NZS2004Z

The hazard factor, Z.

NZS2004R

The return period factor, R.

NZS2004DIST

Distance to the fault in km, used to calculate the near fault factor.

NZS2004Sp

The structural performance factor, Sp.

NZS2004Mu

The structural ductility factor, u.

NZS2004ConsiderTSite

Indicates whether to consider the site period for the spectral shape factor.

NZS2004TSite

The low amplitude site period.

NZS2004ConsiderSingleStory

Indicates whether to consider the structure as a single story, in which case F t = 0.

## Remarks

This function assigns auto seismic loading parameters for the NZS 1170.5 2004 code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicNZS11702004_2()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application


SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign NZS 1170 2004 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetNZS11702004_2("EQX", 2, 0.1, 2, 0, False, 0,
0, 3, 0.4, 1.3, 20, 0.7, 3, True, 1, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v22.0.0.

This function supersedes SetNZS11702004_1.

## See Also

GetNZS11702004_2

# SetUBC97

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetUBC97

## VB6 Procedure

Function SetUBC97(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As Double,
ByVal PeriodFlag As Long, ByVal CT As Double, ByVal UserT As Double, ByVal UserZ As
Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal UBC97SeismicCoeffFlag
As Long, ByVal UBC97SoilProfileType As Long, ByVal UBC97Z As Double, ByVal UBC97Ca
As Double, ByVal UBC97Cv As Double, ByVal UBC97NearSourceFlag As Long, ByVal


UBC97SourceType As Long, ByVal UBC97Dist As Double, ByVal UBC97Na As Double, ByVal
UBC97Nv As Double, ByVal UBC97I As Double, ByVal UBC97R As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

PeriodFlag

This is 1, 2 or 3, indicating the time period option.

```
1 = Approximate
2 = Program calculated
3 = User defined
```
CT

The code-specified CT factor. This item applies when the PeriodFlag item is 1 or 2.

UserT

The user specified time period. This item applies when the PeriodFlag item is 3. [s]

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

UBC97SeismicCoeffFlag

This is either 1 or 2, indicating if the seismic coefficients Ca and Cv are per code or user defined.


```
1 = Per code
2 = User defined
```
UBC97SoilProfileType

This is 1, 2, 3, 4 or 5, indicating the soil profile type.

```
1 = SA
2 = SB
3 = SC
4 = SD
5 = SE
```
This item is applicable only when the seismic coefficients Ca and Cv are calculated in accordance
with the code (UBC97SeismicCoeffFlag = 1).

UBC97Z

This is 0.075, 0.15, 0.2, 0.3 or 0.4, indicating the seismic zone factor.

This item is applicable only when the seismic coefficients Ca and Cv are calculated in accordance
with code (UBC97SeismicCoeffFlag = 1).

UBC97Ca

The seismic coefficient, Ca.

This item is applicable only when the seismic coefficients Ca and Cv are user defined
(UBC97SeismicCoeffFlag = 2).

UBC97Cv

The seismic coefficient, Cv.

This item is applicable only when the seismic coefficients Ca and Cv are user defined
(UBC97SeismicCoeffFlag = 2).

UBC97NearSourceFlag

This is either 1 or 2, indicating if the near source factor coefficients Na and Nv are per code or
user defined.

```
1 = Per code
2 = User defined
```
This item is applicable only when the seismic coefficients Ca and Cv are calculated in accordance
with the code (UBC97SeismicCoeffFlag = 1) and UBC97Z = 0.4.

UBC97SourceType

This is 1, 2 or 3, indicating the seismic source type.

```
1 = A
```

### 2 = B

### 3 = C

This item is applicable only when the seismic coefficients Ca and Cv are calculated in accordance
with code (UBC97SeismicCoeffFlag = 1), UBC97Z = 0.4, and the near source factor coefficients
Na and Nv are calculated in accordance with code (UBC97NearSourceFlag = 1).

UBC97Dist

This is the distance to the seismic source in kilometers.

This item is applicable only when the seismic coefficients Ca and Cv are calculated in accordance
with code (UBC97SeismicCoeffFlag = 1), UBC97Z = 0.4, and the near source factor coefficients
Na and Nv are calculated in accordance with code (UBC97NearSourceFlag = 1).

UBC97Na

The near source factor coefficient, Na.

This item is applicable only when the seismic coefficients Ca and Cv are user defined
(UBC97SeismicCoeffFlag = 2) and the near source factor coefficients Na and Nv are user defined
(UBC97NearSourceFlag = 2).

UBC97Nv

The near source factor coefficient, Nv.

This item is applicable only when the seismic coefficients Ca and Cv are user defined
(UBC97SeismicCoeffFlag = 2) and the near source factor coefficients Na and Nv are user defined
(UBC97NearSourceFlag = 2).

UBC97I

The importance factor.

UBC97R

The overstrength factor.

## Remarks

This function assigns auto seismic loading parameters for the 1997 UBC code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicUBC97()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign UBC97 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetUBC97("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 1, 3, 0.4, 0, 0, 1, 3, 5, 0, 0, 1.15, 6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetUBC97

# SetUBC97Iso

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetUBC97Iso

## VB6 Procedure


Function SetUBC97Iso(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal
UBC97IsoSeismicCoeffFlag As Long, ByVal UBC97IsoSoilProfileType As Long, ByVal
UBC97IsoZ As Double, ByVal UBC97IsoCv As Double, ByVal UBC97IsoNearSourceFlag As
Long, ByVal UBC97IsoSourceType As Long, ByVal UBC97IsoDist As Double, ByVal
UBC97IsoNv As Double, ByVal UBC97IsoRI As Double, ByVal UBC97IsoBD As Double,
ByVal UBC97IsoKDmax As Double, ByVal UBC97IsoKDmin As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```
Eccen

The eccentricity ratio that applies to all diaphragms.

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

UBC97IsoSeismicCoeffFlag

This is either 1 or 2, indicating if the seismic coefficient Cv is per code or user defined.

```
1 = Per code
2 = User defined
```
UBC97IsoSoilProfileType

This is 1, 2, 3, 4 or 5, indicating the soil profile type.

```
1 = SA
2 = SB
3 = SC
```

### 4 = SD

### 5 = SE

This item is applicable only when the seismic coefficients Ca and Cv are calculated in accordance
with code (UBC97SeismicCoeffFlag = 1).

UBC97IsoZ

This is 0.075, 0.15, 0.2, 0.3 or 0.4, indicating the seismic zone factor.

This item is applicable only when the seismic coefficient Cv is calculated in accordance with code
(UBC97IsoSeismicCoeffFlag = 1).

UBC97IsoCv

The seismic coefficient, Cv.

This item is applicable only when the seismic coefficient Cv is user defined
(UBC97IsoSeismicCoeffFlag = 2).

UBC97IsoNearSourceFlag

This is either 1 or 2, indicating if the near source factor coefficient Nv is per code or user defined.

```
1 = Per code
2 = User defined
```
This item is applicable only when the seismic coefficient Cv is calculated per code
(UBC97IsoSeismicCoeffFlag = 1) and UBC97IsoZ = 0.4.

UBC97IsoSourceType

This is 1, 2 or 3, indicating the seismic source type.

```
1 = A
2 = B
3 = C
```
This item is applicable only when the seismic coefficient Cv is calculated in accordance with code
(UBC97IsoSeismicCoeffFlag = 1), UBC97IsoZ = 0.4, and the near source factor coefficient Nv is
calculated in accordance with code (UBC97IsoNearSourceFlag = 1).

UBC97IsoDist

This is the distance to the seismic source in kilometers.

This item is only applicable when the seismic coefficient Cv is calculated in accordance with code
(UBC97IsoSeismicCoeffFlag = 1), UBC97IsoZ = 0.4, and the near source factor coefficient Nv is
calculated in accordance with code (UBC97IsoNearSourceFlag = 1).

UBC97IsoNv


The near source factor coefficient, Nv.

This item is applicable only when the seismic coefficient Cv is user defined
(UBC97IsoSeismicCoeffFlag = 2) and the near source factor coefficient Nv is user defined
(UBC97IsoNearSourceFlag = 2).

UBC97IsoRI

The overstrength factor, Ri.

UBC97IsoBD

The coefficient for damping.

UBC97IsoKDmax

The maximum effective stiffness of the isolation system. [F/L]

UBC97IsoKDmin

The minimum effective stiffness of the isolation system. [F/L]

## Remarks

This function assigns auto seismic loading parameters for seismically isolated buildings using the
1997 UBC code.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicUBC97Iso()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)


'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign UBC97Iso parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetUBC97Iso("EQX", 1, 0.05, False, 0, 0, 1, 3,
0.4, 0, 1, 3, 5, 0, 2, 1.25, 200, 150)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetUBC97Iso

# SetUserCoefficient

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetUserCoefficient

## VB6 Procedure

Function SetUserCoefficient(ByVal Name As String, ByVal DirFlag As Long, ByVal Eccen As
Double, ByVal UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal c
As Double, ByVal k As Double) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

DirFlag

This is either 1 or 2, indicating the seismic load direction.

```
1 = Global X
2 = Global Y
```

Eccen

The eccentricity ratio that applies to all diaphragms.

UserZ

This item is True if the top and bottom elevations of the seismic load are user specified. It is False
if the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto seismic loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto seismic loads are applied. [L]

c

The base shear coefficient.

k

The building height exponent.

## Remarks

This function assigns auto seismic loading parameters for User Coefficient type loading.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignSeismicUserCoefficient()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel


'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign user coefficient parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetUserCoefficient("EQX", 1, 0.06, False, 0, 0,
0.15, 1.3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetUserCoefficient

# SetUserLoad

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetUserLoad

## VB6 Procedure

Function SetUserLoad(ByVal Name As String, ByVal MyType As Long, Optional ByVal Eccen
As Double = 0.05) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

MyType

This is either 1 or 2, indicating the application point type for the user load.


```
1 = User specified application point
2 = At center of mass with optional additional eccentricity
```
Eccen

The eccentricity ratio that applies to all diaphragms. This item is only applicable when MyType =
2.

## Remarks

This function sets the auto seismic load type to User Load. User load values are assigned using the
SetUserLoadValue function.

The function returns zero if the load type is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub AssignSeismicUserLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern


ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'set to auto seismic user load
ret = SapModel.LoadPatterns.AutoSeismic.SetUserLoad("EQX", 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUserLoadValue

GetUserLoad

# SetUserLoadValue

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeismic.SetUserLoadValue

## VB6 Procedure

Function SetUserLoadValue(ByVal Name As String, ByVal Diaph As String, ByVal Fx As
Double, ByVal Fy As Double, ByVal Mz As Double, Optional ByVal x As Double = 0, Optional
ByVal y As Double = 0) As Long

## Parameters

Name

The name of an existing Quake-type load pattern that has been assigned a User Load auto seismic
type.

Diaph

The name of an existing special rigid diaphragm constraint, that is, a diaphragm constraint with
the following features:

1. The constraint type is CONSTRAINT_DIAPHRAGM = 2.


2. The constraint coordinate system is Global.
3. The constraint axis is Z.

Fx

The global X direction force assigned to the specified diaphragm. [F]

Fy

The global Y direction force assigned to the specified diaphragm. [F]

Mz

The moment about the global Z axis assigned to the specified diaphragm. [FL]

x

The global X-coordinate of the point where the seismic force is applied. [L]

This item is applicable only when the auto seismic load is specified to have a user specified
application point (see the SetUserLoad function).

y

The global Y-coordinate of the point where the seismic force is applied. [L]

This item is applicable only when the auto seismic load is specified to have a user specified
application point (see the SetUserLoad function).

## Remarks

This function assigns loading to an auto seismic load that is a User Load type. The SetUserLoad
function is used to specify that an auto seismic load is a User Load type

The function returns zero if the loading is successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub AssignSeismicUserLoadValue()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel


'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'set to auto seismic user load
ret = SapModel.LoadPatterns.AutoSeismic.SetUserLoad("EQX", 1)

'set to auto seismic user load values
ret = SapModel.LoadPatterns.AutoSeismic.SetUserLoadValue("EQX", "Diaph1", 20, 4, 1000,
0, 0)
ret = SapModel.LoadPatterns.AutoSeismic.SetUserLoadValue("EQX", "Diaph2", 40, 8, 2000,
0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUserLoad

GetUserLoad


# GetAASHTO2018

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.GetAASHTO2018

## VB6 Procedure

Function GetAASHTO2018(ByVal Name As String, ByRef LimitState As Long, ByRef
Superstructure As Boolean, ByRef Substructure As Boolean, ByRef Vertical As Boolean, ByRef
GroundElevation As Double, ByRef SuperZProgCalc As Boolean, ByRef SuperstructureZ As
Double, ByRef SubZProgCalc As Boolean, ByRef SubstructureZ As Double, ByRef WindSpeed
As Double, ByRef ExposureCategory As Long, ByRef G As Double, ByRef CdSuper As Double,
ByRef CdSub As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

LimitState

The limit state associated with the wind load.

```
1 = Strength III
```
```
2 = Strength V
```
```
3 = Service I
```
```
4 = Service IV
```
Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc


This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

SubZProgCalc

This item is True if the substructure height, Z, should be program calculated, otherwise it is false.

SuperstructureZ

The substructure height Z. This item applies only when SubProgCalc = False. [L]

WindSpeed

The wind speed in mph.

Exposure Category

The wind exposure category.

```
1 = B
```
```
2 = C
```
```
3 = D
```
### G

The gust effect factor, G.

CdSuper

The drag coefficient for the superstructure.

CdSub

The drag coefficient for the substructure.

## Remarks

This function retrieves bridge auto wind loading parameters for AASHTO 2018.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetBridgeWindAASHTO2018()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim LimitState As Long
Dim Superstructure As Boolean
Dim Substructure As Boolean
Dim Vertical As Boolean
Dim GroundElevation As Double
Dim SuperZProgCalc As Boolean

Dim SuperstructureZ As Double
Dim SubZProgCalc As Boolean

Dim SubstructureZ As Double
Dim WindSpeed As Double
Dim ExposureCategory As Long

Dim G As Double

Dim CdSuper As Double

Dim CdSub As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign AASHTO2018 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetAASHTO2018("WIND", 1, True, True,
True, -100, True, 10, True, 10, 100, 2, 1, 1.3, 1.6)

'get AASHTO 2018 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.GetAASHTO2018("WIND", LimitState,
Superstructure, Substructure, Vertical, GroundElevation, SuperZProgCalc, SuperstructureZ,
SubZProgCalc, SubstructureZ, WindSpeed, ExposureCategory, G, CdSuper, CdSub)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

SetAASHTO2018

# GetAASHTO2020

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.GetAASHTO2020

## VB6 Procedure

Function GetAASHTO2020(ByVal Name As String, ByRef LimitState As Long, ByRef
Superstructure As Boolean, ByRef Substructure As Boolean, ByRef Vertical As Boolean, ByRef
GroundElevation As Double, ByRef SuperZProgCalc As Boolean, ByRef SuperstructureZ As
Double, ByRef SubZProgCalc As Boolean, ByRef SubstructureZ As Double, ByRef WindSpeed
As Double, ByRef ExposureCategory As Long, ByRef G As Double, ByRef CdSuper As Double,
ByRef CdSub As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

LimitState

The limit state associated with the wind load.

```
1 = Strength III
```
```
2 = Strength V
```
```
3 = Service I
```
```
4 = Service IV
```

Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

SubZProgCalc

This item is True if the substructure height, Z, should be program calculated, otherwise it is false.

SuperstructureZ

The substructure height Z. This item applies only when SubProgCalc = False. [L]

WindSpeed

The wind speed in mph.

Exposure Category

The wind exposure category.

```
1 = B
```
```
2 = C
```
```
3 = D
```
### G

The gust effect factor, G.

CdSuper

The drag coefficient for the superstructure.


CdSub

The drag coefficient for the substructure.

## Remarks

This function retrieves bridge auto wind loading parameters for AASHTO 2020.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetBridgeWindAASHTO2020()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim LimitState As Long
Dim Superstructure As Boolean
Dim Substructure As Boolean
Dim Vertical As Boolean
Dim GroundElevation As Double
Dim SuperZProgCalc As Boolean

Dim SuperstructureZ As Double
Dim SubZProgCalc As Boolean

Dim SubstructureZ As Double
Dim WindSpeed As Double
Dim ExposureCategory As Long

Dim G As Double

Dim CdSuper As Double

Dim CdSub As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel


'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign AASHTO2020 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetAASHTO2020("WIND", 1, True, True,
True, -100, True, 10, True, 10, 100, 2, 1, 1.3, 1.6)

'get AASHTO 2020 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.GetAASHTO2020("WIND", LimitState,
Superstructure, Substructure, Vertical, GroundElevation, SuperZProgCalc, SuperstructureZ,
SubZProgCalc, SubstructureZ, WindSpeed, ExposureCategory, G, CdSuper, CdSub)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v25.3.0.

## See Also

SetAASHTO2020

# GetAngles

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.GetAngles

## VB6 Procedure

Function GetAngles(ByVal Name As String, ByRef SymmetricTran As Boolean, ByRef
SymmetricLong As Boolean, ByRef UserDefined As Boolean, ByRef NumberAngles As Long,
ByRef Angles() As Double, ByRef TranCoeff() As Double, ByRef LongCoeff() As Double) As
Long

## Parameters

Name


The name of an existing bridge wind load pattern.

SymmetricTran

This is True if the angles are symmetric about the transverse axis, otherwise False.

SymmetricLong

This is True if the angles are symmetric about the longitudinal axis, otherwise False.

UserDefined

This is True if the angles are user defined, otherwise False.

NumberAngles

The number of angles specified for the load pattern. This is only used if UserDefined = True.

Angles

This is an array containing the wind angles. All angles are returned, including those generated due
to the symmetry options.

TranCoeff

This is an array containing the transverse coefficients corresponding with the angles. This is only
used if UserDefined = True.

LongCoeff

This is an array containing the longitudinal coefficients corresponding with the angles. This is
only used if UserDefined = True.

## Remarks

This function retrieves the bridge wind angle data for a specified load pattern.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAngles()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim Angles() As Double

Dim TranCoeff() As Double

Dim LongCoeff() As Double


Dim MySymTran As Boolean

Dim MySymLong As Boolean

Dim MyUserDefined As Boolean

Dim MyNumberAngles As Long

Dim MyAngles() As Double

Dim MyTranCoeff() As Double

Dim MyLongCoeff() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign AASHTO2018 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetAASHTO2018("WIND", 1, True, True,
True, -100, True, 10, True, 10, 100, 2, 1, 1.3, 1.6)

'set angle data

ReDim Angles(4)

ReDim TranCoeff(4)

ReDim LongCoeff(4)

Angles(0) = 0

TranCoeff(0) = 1

LongCoeff(0) = 0


Angles(1) = 20

TranCoeff(1) = 0.85

LongCoeff(1) = 0.18

Angles(2) = 40

TranCoeff(2) = 0.7

LongCoeff(2) = 0.26

Angles(3) = 60

TranCoeff(3) = 0.34

LongCoeff(3) = 0.38

Angles(4) = 80

TranCoeff(4) = 0.12

LongCoeff(4) = 0.42

ret = SapModel.LoadPatterns.AutoWindBridge.SetAngles("WIND", False, False, True, 5,
Angles, TranCoeff, LongCoeff)

'get angle data
ret = SapModel.LoadPatterns.AutoWindBridge.GetAngles("WIND", MySymTran,
MySymLong, MyUserDefined, MyNumberAngles, MyAngles, MyTranCoeff, MyLongCoeff)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

SetAngles


# GetAutoLiveLoad_1 {Bridge Wind Load}

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.GetAutoLiveLoad_1

## VB6 Procedure

Function GetAutoLiveLoad_1(ByVal Name As String, ByRef RefLoadPat As String, ByRef
Height As Double, ByRef LLHeight As Double) As Long

## Parameters

Name

The name of an existing bridge wind - live load type pattern.

RefLoadPat

The name of an existing bridge wind load pattern that is referenced from this wind on live load
pattern.

Height

The height above the roadway surface at which the wind on live load should be applied. [L]

LLHeight

The height of the live load surface to which the wind should be applied. This parameter does not
apply for AASHTO 2018 or AASHTO 2020. [L]

## Remarks

This function retrieves auto wind on live load parameters.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAutoWindLiveLoad_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim RefLoadPat As String


Dim Height As Double

Dim LLHeight As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WINDONLIVELOAD)

'set auto wind live load loading type to Auto
ret = SapModel.LoadPatterns.AutoWindBridge.SetAutoLiveLoad_1("WINDLIVE", "WIND",
0, 2.5)

'get auto wind live load parameters

ret = SapModel.LoadPatterns.AutoWindBridge.GetAutoLiveLoad_1("WINDLIVE",
RefLoadPat, Height, LLHeight)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v25.2.0.

This function supersedes GetAutoLiveLoad.

## See Also

SetAutoLiveLoad_1


# GetCSAS614

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.GetCSAS614

## VB6 Procedure

Function GetCSAS614(ByVal Name As String, ByRef Superstructure As Boolean, ByRef
Substructure As Boolean, ByRef Vertical As Boolean, ByRef GroundElevation As Double, ByRef
SuperZProgCalc As Boolean, ByRef SuperstructureZ As Double, ByRef q As Double, ByRef Cg
As Double, ByRef CeProgCalc As Boolean, ByRef Ce As Double, ByRef ChStructure As Double,
ByRef ChLiveLoad As Double, ByRef Cv As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

q


The reference wind pressure, q. [F/L^2 ]

Cg

The gust effect factor.

CeProgCalc

This item is True if the wind exposure factor, Ce, should be program calculated, otherwise it is
false.

Ce

The wind exposure factor. This item applies only when CeProgCalc = False.

ChStructure

The Ch factor for wind acting on the structure.

ChLiveLoad

The Ch factor for wind acting on the live load.

Cv

The Cv factor for vertical wind.

## Remarks

This function retrieves bridge auto wind loading parameters for CSA S6-14.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetBridgeWindCSAS614()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim Superstructure As Boolean
Dim Substructure As Boolean
Dim Vertical As Boolean
Dim GroundElevation As Double
Dim SuperZProgCalc As Boolean

Dim SuperstructureZ As Double
Dim q As Double


Dim Cg As Double
Dim CeProgCalc As Boolean
Dim Ce As Double

Dim ChStructure As Double

Dim ChLiveLoad As Double

Dim Cv As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign CSA S6-14 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetCSAS614("WIND", True, True, True, -
100, True, 10, 1, 2, True, 1, 2, 1.2, 1)

'get CSA S6-14 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.GetCSAS614("WIND", Superstructure,
Substructure, Vertical, GroundElevation, SuperZProgCalc, SuperstructureZ, q, Cg, CeProgCalc,
Ce, ChStructure, ChLiveLoad, Cv)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

SetCSAS614


# GetEurocode12005

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.GetEurocode12005

## VB6 Procedure

Function GetEurocode12005(ByVal Name As String, ByRef Superstructure As Boolean, ByRef
Substructure As Boolean, ByRef Vertical As Boolean, ByRef GroundElevation As Double, ByRef
SuperZProgCalc As Boolean, ByRef SuperstructureZ As Double, ByRef SubZProgCalc As
Boolean, ByRef SubstructureZ As Double, ByRef WindSpeed As Double, ByRef Terrain As
Long, ByRef Orography As Double, ByRef k1 As Double, ByRef Rho As Double, ByRef Cfx As
Double, ByRef CfzUp As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

SubZProgCalc

This item is True if the substructure height, Z, should be program calculated, otherwise it is false.

SuperstructureZ


The substructure height Z. This item applies only when SubProgCalc = False. [L]

WindSpeed

The basic wind speed, vb, in meters per second.

Terrain

The terrain category.

```
0 = 0
```
```
1 = I
```
```
2 = II
```
```
3 = III
```
```
4 = IV
```
Orography

The orography factor, Co.

k1

The turbulence factor, k1.

Rho

The air density in kg/m^3 , Rho.

Cfx

The force coefficient, Cf, in the horizontal direction.

CfzUp

The force coefficient, Cf, in the vertical up direction.

## Remarks

This function retrieves bridge auto wind loading parameters for Eurocode 1-2005.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetBridgeWindEurocode12005()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long

Dim Superstructure As Boolean
Dim Substructure As Boolean
Dim Vertical As Boolean
Dim GroundElevation As Double
Dim SuperZProgCalc As Boolean

Dim SuperstructureZ As Double

Dim SubZProgCalc As Boolean

Dim SubstructureZ As Double
Dim WindSpeed As Double

Dim Terrain As Long
Dim Orography As Double
Dim k1 As Double

Dim Rho As Double

Dim Cfx As Double

Dim CfzUp As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign Eurocode 1-2005 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetEurocode12005("WIND", True, True,
True, -100, True, 10, True, 10, 35, 2, 1, 1.25, 1.3, 0.9)

'get Eurocode 1-2005 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.GetEurocode12005("WIND", Superstructure,
Substructure, Vertical, GroundElevation, SuperZProgCalc, SuperstructureZ, SubZProgCalc,
SubstructureZ, WindSpeed, Terrain, Orography, k1, Rho, Cfx, CfzUp)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

SetEurocode12005

# SetAngles {Bridge Wind Load}

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.SetAngles

## VB6 Procedure

Function SetAngles(ByVal Name As String, ByVal SymmetricTran As Boolean, ByVal
SymmetricLong As Boolean, ByVal UserDefined As Boolean, ByVal NumberAngles As Long,
ByRef Angles() As Double, ByRef TranCoeff() As Double, ByRef LongCoeff() As Double) As
Long

## Parameters

Name

The name of an existing bridge wind load pattern.

SymmetricTran

This is True if the angles are symmetric about the transverse axis, otherwise False.

SymmetricLong

This is True if the angles are symmetric about the longitudinal axis, otherwise False.

UserDefined

This is True if the angles are user defined, otherwise False.

NumberAngles


The number of angles specified for the load pattern. This is only used if UserDefined = True.

Angles

This is an array containing the wind angles. If duplicates are included, only the first one will be
used. If SymmetricTran = True and/or SymmetricLong = True, only angles between 0 and 90
degrees will be used. Additional angles will be generated via the symmetry conditions. This is
only used if UserDefined = True.

TranCoeff

This is an array containing the transverse coefficients corresponding with the angles. This is only
used if UserDefined = True.

LongCoeff

This is an array containing the longitudinal coefficients corresponding with the angles. This is
only used if UserDefined = True.

## Remarks

This function sets the bridge wind angle data for a specified load pattern.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetAngles()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim Angles() As Double

Dim TranCoeff() As Double

Dim LongCoeff() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel


'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign AASHTO2018 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetAASHTO2018("WIND", 1, True, True,
True, -100, True, 10, True, 10, 100, 2, 1, 1.3, 1.6)

'set angle data

ReDim Angles(4)

ReDim TranCoeff(4)

ReDim LongCoeff(4)

Angles(0) = 0

TranCoeff(0) = 1

LongCoeff(0) = 0

Angles(1) = 20

TranCoeff(1) = 0.85

LongCoeff(1) = 0.18

Angles(2) = 40

TranCoeff(2) = 0.7

LongCoeff(2) = 0.26

Angles(3) = 60

TranCoeff(3) = 0.34

LongCoeff(3) = 0.38

Angles(4) = 80

TranCoeff(4) = 0.12

LongCoeff(4) = 0.42

ret = SapModel.LoadPatterns.AutoWindBridge.SetAngles("WIND", False, False, True, 5,
Angles, TranCoeff, LongCoeff)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

GetAngles

# SetAASHTO2018

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.SetAASHTO2018

## VB6 Procedure

Function SetAASHTO2018(ByVal Name As String, ByVal LimitState As Long, ByVal
Superstructure As Boolean, ByVal Substructure As Boolean, ByVal Vertical As Boolean, ByVal
GroundElevation As Double, ByVal SuperZProgCalc As Boolean, ByVal SuperstructureZ As
Double, ByVal SubZProgCalc As Boolean, ByVal SubstructureZ As Double, ByVal WindSpeed
As Double, ByVal ExposureCategory As Long, ByVal G As Double, ByVal CdSuper As Double,
ByVal CdSub As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

LimitState

The limit state associated with the wind load.

```
1 = Strength III
```
```
2 = Strength V
```
```
3 = Service I
```

```
4 = Service IV
```
Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

SubZProgCalc

This item is True if the substructure height, Z, should be program calculated, otherwise it is false.

SuperstructureZ

The substructure height Z. This item applies only when SubProgCalc = False. [L]

WindSpeed

The wind speed in mph.

Exposure Category

The wind exposure category.

```
1 = B
```
```
2 = C
```
```
3 = D
```
G

The gust effect factor, G.

CdSuper


The drag coefficient for the superstructure.

CdSub

The drag coefficient for the substructure.

## Remarks

This function sets bridge auto wind loading parameters for AASHTO 2018.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetBridgeWindAASHTO2018()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign AASHTO2018 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetAASHTO2018("WIND", 1, True, True,
True, -100, True, 10, True, 10, 100, 2, 1, 1.3, 1.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in v21.0.0.

## See Also

GetAASHTO2018

# SetAASHTO2020

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.SetAASHTO2020

## VB6 Procedure

Function SetAASHTO2020(ByVal Name As String, ByVal LimitState As Long, ByVal
Superstructure As Boolean, ByVal Substructure As Boolean, ByVal Vertical As Boolean, ByVal
GroundElevation As Double, ByVal SuperZProgCalc As Boolean, ByVal SuperstructureZ As
Double, ByVal SubZProgCalc As Boolean, ByVal SubstructureZ As Double, ByVal WindSpeed
As Double, ByVal ExposureCategory As Long, ByVal G As Double, ByVal CdSuper As Double,
ByVal CdSub As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

LimitState

The limit state associated with the wind load.

```
1 = Strength III
```
```
2 = Strength V
```
```
3 = Service I
```
```
4 = Service IV
```
Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.


Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

SubZProgCalc

This item is True if the substructure height, Z, should be program calculated, otherwise it is false.

SuperstructureZ

The substructure height Z. This item applies only when SubProgCalc = False. [L]

WindSpeed

The wind speed in mph.

Exposure Category

The wind exposure category.

```
1 = B
```
```
2 = C
```
```
3 = D
```
G

The gust effect factor, G.

CdSuper

The drag coefficient for the superstructure.

CdSub

The drag coefficient for the substructure.

## Remarks

This function sets bridge auto wind loading parameters for AASHTO 2020.


The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetBridgeWindAASHTO2020()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign AASHTO2020 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetAASHTO2020("WIND", 1, True, True,
True, -100, True, 10, True, 10, 100, 2, 1, 1.3, 1.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v25.3.0.

## See Also

GetAASHTO2020


# SetAutoLiveLoad_1 {Bridge Wind Load}

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.SetAutoLiveLoad_1

## VB6 Procedure

Function SetAutoLiveLoad_1(ByVal Name As String, ByVal RefLoadPat As String, ByVal
Height As Double, ByVal LLHeight As Double) As Long

## Parameters

Name

The name of an existing bridge wind - live load type pattern.

RefLoadPat

The name of an existing bridge wind load pattern that is referenced from this wind on live load
pattern.

Height

The height above the roadway surface at which the wind on live load should be applied. [L]

LLHeight

The height of the live load surface to which the wind should be applied. This parameter does not
apply for AASHTO 2018 or AASHTO 2020. [L]

## Remarks

This function applies auto wind on live load parameters.

The function returns zero if the parameters are successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub SetAutoWindLiveLoad_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WINDONLIVELOAD)

'set auto wind live load loading type to Auto
ret = SapModel.LoadPatterns.AutoWindBridge.SetAutoLiveLoad_1("WINDLIVE", "WIND",
0, 2.5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v25.2.0.

This function supersedes SetAutoLiveLoad.

## See Also

GetAutoLiveLoad_1

# SetCSAS614 {Bridge Wind Load}

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.SetCSAS614

## VB6 Procedure


Function SetCSAS614(ByVal Name As String, ByVal Superstructure As Boolean, ByVal
Substructure As Boolean, ByVal Vertical As Boolean, ByVal GroundElevation As Double, ByVal
SuperZProgCalc As Boolean, ByVal SuperstructureZ As Double, ByVal q As Double, ByVal Cg
As Double, ByVal CeProgCalc As Boolean, ByVal Ce As Double, ByVal ChStructure As Double,
ByVal ChLiveLoad As Double, ByVal Cv As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

q

The reference wind pressure, q. [F/L^2 ]

Cg

The gust effect factor.

CeProgCalc

This item is True if the wind exposure factor, Ce, should be program calculated, otherwise it is
false.

Ce

The wind exposure factor. This item applies only when CeProgCalc = False.


ChStructure

The Ch factor for wind acting on the structure.

ChLiveLoad

The Ch factor for wind acting on the live load.

Cv

The Cv factor for vertical wind.

## Remarks

This function sets bridge auto wind loading parameters for CSA S6-14.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetBridgeWindCSAS614()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign CSA S6-14 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetCSAS614("WIND", True, True, True, -
100, True, 10, 1, 2, True, 1, 2, 1.2, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

GetCSAS614

# SetEurocode12005

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.SetEurocode12005

## VB6 Procedure

Function SetEurocode12005(ByVal Name As String, ByVal Superstructure As Boolean, ByVal
Substructure As Boolean, ByVal Vertical As Boolean, ByVal GroundElevation As Double, ByVal
SuperZProgCalc As Boolean, ByVal SuperstructureZ As Double, ByVal SubZProgCalc As
Boolean, ByVal SubstructureZ As Double, ByVal WindSpeed As Double, ByVal Terrain As
Long, ByVal Orography As Double, ByVal k1 As Double, ByVal Rho As Double, ByVal Cfx As
Double, ByVal CfzUp As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]


SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

SubZProgCalc

This item is True if the substructure height, Z, should be program calculated, otherwise it is false.

SuperstructureZ

The substructure height Z. This item applies only when SubProgCalc = False. [L]

WindSpeed

The basic wind speed, vb, in meters per second.

Terrain

The terrain category.

```
0 = 0
```
```
1 = I
```
```
2 = II
```
```
3 = III
```
```
4 = IV
```
Orography

The orography factor, Co.

k1

The turbulence factor, k1.

Rho

The air density in kg/m^3 , Rho.

Cfx

The force coefficient, Cf, in the horizontal direction.

CfzUp

The force coefficient, Cf, in the vertical up direction.


## Remarks

This function sets bridge auto wind loading parameters for Eurocode 1-2005.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetBridgeWindEurocode12005()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign Eurocode 1-2005 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetEurocode12005("WIND", True, True,
True, -100, True, 10, True, 10, 35, 2, 1, 1.25, 1.3, 0.9)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.


## See Also

GetEurocode12005

# GetIRC62017

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.GetIRC62017

## VB6 Procedure

Function GetIRC62017(ByVal Name As String, ByRef Superstructure As Boolean, ByRef
Substructure As Boolean, ByRef Vertical As Boolean, ByRef GroundElevation As Double,
ByRef SuperZProgCalc As Boolean, ByRef SuperstructureZ As Double, ByRef
SubZProgCalc As Boolean, ByRef SubstructureZ As Double, ByRef vb As Double, ByRef
Terrain As Long, ByRef G As Double, ByRef CDSuper As Double, ByRef CDSub As
Double, ByRef CL As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

SubZProgCalc


This item is True if the substructure height, Z, should be program calculated, otherwise it is false.

SubstructureZ

The substructure height Z. This item applies only when SubProgCalc = False. [L]

vb

The basic wind speed. [m/s]

Terrain

The terrain type.

```
0 = Plain
```
```
1 = Obstructions
```
### G

The gust factor, G.

CDSuper

The drag coefficient for the superstructure, C D.

CDSub

The drag coefficient for the substructure, C D.

CL

The lift coefficient, C L, for vertical wind.

## Remarks

This function retrieves bridge auto wind loading parameters for IRC:6-2017.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindIRC62017()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Superstructure As Boolean
Dim Substructure As Boolean
Dim Vertical As Boolean
Dim GroundElevation As Double


Dim SuperZProgCalc As Boolean
Dim SuperstructureZ As Double
Dim SubZProgCalc As Boolean
Dim SubstructureZ As Double
Dim vb As Double

Dim Terrain As Long
Dim G As Double
Dim CDSuper As Double
Dim CDSub As Double
Dim CL As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign IRC62017 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.SetIRC62017("WIND", True, True, True, -
100, True, 10, True, 10, 33, 0, 2, 1.5, 1.5, 0.75)

'get IRC62017 parameters
ret = SapModel.LoadPatterns.AutoWindBridge.GetIRC62017("WIND", Superstructure,
Substructure, Vertical, GroundElevation, SuperZProgCalc, SuperstructureZ, SubZProgCalc,
SubstructureZ, vb, Terrain, G, CDSuper, CDSub, CL)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v23.1.0.

## See Also


SetIRC62017

# SetIRC62017

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.SetIRC62017

## VB6 Procedure

Function SetIRC62017(ByVal Name As String, ByVal Superstructure As Boolean, ByVal
Substructure As Boolean, ByVal Vertical As Boolean, ByVal GroundElevation As Double,
ByVal SuperZProgCalc As Boolean, ByVal SuperstructureZ As Double, ByVal
SubZProgCalc As Boolean, ByVal SubstructureZ As Double, ByVal vb As Double, ByVal
Terrain As Long, ByVal G As Double, ByVal CDSuper As Double, ByVal CDSub As
Double, ByVal CL As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

Superstructure

This item is True if wind on the superstructure should be considered, otherwise it is false.

Substructure

This item is True if wind on the substructure should be considered, otherwise it is false.

Vertical

This item is True if vertical wind should be considered, otherwise it is false

GroundElevation

The ground elevation used for determining heights used for wind pressure values. [L]

SuperZProgCalc

This item is True if the superstructure height, Z, should be program calculated, otherwise it is
false.

SuperstructureZ

The superstructure height Z. This item applies only when SuperProgCalc = False. [L]

SubZProgCalc


This item is True if the substructure height, Z, should be program calculated, otherwise it is false.

SubstructureZ

The substructure height Z. This item applies only when SubProgCalc = False. [L]

vb

The basic wind speed. [m/s]

Terrain

The terrain type.

```
0 = Plain
```
```
1 = Obstructions
```
### G

The gust factor, G.

CDSuper

The drag coefficient for the superstructure, C D.

CDSub

The drag coefficient for the substructure, C D.

CL

The lift coefficient, C L, for vertical wind.

## Remarks

This function sets bridge auto wind loading parameters for IRC:6-2017.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindIRC62017()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign CSA S6-14 parameters
ret = SapModel.LoadPatterns.AutoWindBridge. SetIRC62017("WIND", True, True, True, -
100, True, 10, True, 10, 33, 0, 2, 1.5, 1.5, 0.75)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing

End Sub

## Release Notes

Initial release in v23.1.0.

## See Also

GetIRC62017

# SetNoneLiveLoad

## Syntax

SapObject.SapModel.LoadPatterns.AutoWindBridge.SetNoneLiveLoad

## VB6 Procedure

Function SetNoneLiveLoad(ByVal Name As String) As Long

## Parameters


Name

The name of an existing bridge wind - live load type pattern.

## Remarks

This function sets the auto wind – live load type for the specified load pattern to None.

The function returns zero if the loading type is successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindLiveLoadNone()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model containing a bridge object
ret = SapModel.File.OpenFile(“C:\Temp\BridgeModel.bdb” )

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WINDONLIVELOAD)

'set auto wind live load loading type to None
ret = SapModel.LoadPatterns.AutoWindBridge.SetNoneLiveLoad("WINDLIVE")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in v21.0.0.

# GetAPI4F2008_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetAPI4F2008_1

## VB6 Procedure

Function GetAPI4F2008_1(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As
Double, ByRef WindSpeed As Double, ByRef SSLFactor As Double, ByRef ShieldingFactor As
Double) As Long

## Parameters

Name

The name of an existing Wind-type load case with an API 4F 2008 auto wind assignment.

ExposureFrom

This is 2, 3, or 4, indicating the source of the wind exposure.

```
2 = From area objects
```
```
3 = From frame objects (open structure)
```
```
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 3 or 4.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified.

It is False if the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ


This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The design reference wind velocity, Vref, in knots.

SSLFactor

The structural safety level multiplier.

ShieldingFactor

The shielding factor.

## Remarks

This function retrieves auto wind loading parameters for API 4F 2008.

The function returns zero if the parameters are successfully assigned; otherwise, it returns a
nonzero value.

## VBA Example

Sub GetWindAPI4F2008()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim SSLFactor As Double
Dim ShieldingFactor As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)


'add new load case
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign API 4F 2008 parameters
ret = SapModel.LoadPatterns.AutoWind.SetAPI4F2008_1("WIND", 3, 0, False, 0, 0,93, 1.1,
0.85)

'get API 4F 2008 parameters
ret = SapModel.LoadPatterns.AutoWind.GetAPI4F2008_1("WIND", ExposureFrom,
DirAngle, UserZ, TopZ, BottomZ, WindSpeed, SSLFactor, ShieldingFactor)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.1.0.

This function supersedes GetAPI4F2008.

## See Also

SetAPI4F2008_1

# GetAPI4F2013

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetAPI4F2013

## VB6 Procedure

Function GetAPI4F2013(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef UserZ As Boolean, ByRef TopZ As Double, ByRef BottomZ As
Double, ByRef WindSpeed As Double, ByRef SSLFactor As Double, ByRef ShieldingFactor As
Double) As Long

## Parameters

Name

The name of an existing Wind-type load case with an API 4F 2013 auto wind assignment.

ExposureFrom

This is 2, 3, or 4, indicating the source of the wind exposure.


```
2 = From area objects
```
```
3 = From frame objects (open structure)
```
```
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 3 or 4.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified.

It is False if the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The design reference wind velocity, Vref, in knots.

SSLFactor

The structural safety level multiplier.

ShieldingFactor

The shielding factor.

## Remarks

This function retrieves auto wind loading parameters for API 4F 2013.

The function returns zero if the parameters are successfully assigned; otherwise, it returns a
nonzero value.

## VBA Example

Sub GetWindAPI4F2013()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim UserZ As Boolean
Dim TopZ As Double


Dim BottomZ As Double
Dim WindSpeed As Double
Dim SSLFactor As Double
Dim ShieldingFactor As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load case
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign API 4F 2013 parameters
ret = SapModel.LoadPatterns.AutoWind.SetAPI4F2013("WIND", 3, 0, False, 0, 0,93, 1.1,
0.85)

'get API 4F 2013 parameters
ret = SapModel.LoadPatterns.AutoWind.GetAPI4F2013("WIND", ExposureFrom, DirAngle,
UserZ, TopZ, BottomZ, WindSpeed, SSLFactor, ShieldingFactor)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.1.0.

## See Also

SetAPI4F2013

# GetASCE702

## Syntax


SapObject.SapModel.LoadPatterns.AutoWind.GetASCE702

## VB6 Procedure

Function GetASCE702(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef ASCECase As Long, ByRef
ASCEe1 As Double, ByRef ASCEe2 As Double, ByRef UserZ As Boolean, ByRef TopZ As
Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef ExposureType As
Long, ByRef ImportanceFactor As Double, ByRef Kzt As Double, ByRef GustFactor As Double,
ByRef Kd As Double, ByRef SolidGrossRatio As Double, ByRef UserExposure As Boolean) As
Long

## Parameters

Name

The name of an existing Wind-type load pattern with an ASCE7-02 auto wind assignment.

ExposureFrom

This is 1, 2, 3 or 4, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
3 = From frame objects (open structure)
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1, 3, or 4.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

ASCECase

This is 1, 2, 3, 4 or 5, indicating the desired case from ASCE7-02 Figure 6-9. 1, 2, 3 and 4 refer to
cases 1 through 4 in the figure. 5 means to create all cases. This item applies only when
ExposureFrom = 1.

ASCEe1

This is the value e1 in ASCE7-02 Figure 6-9. This item applies only when ExposureFrom = 1.

ASCEe2

This is the value e2 in ASCE7-02 Figure 6-9. This item applies only when ExposureFrom = 1.

UserZ


This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2, 3 or 4, indicating the exposure category.

```
1 = A
2 = B
3 = C
4 = D
```
ImportanceFactor

The importance factor.

Kzt

The topographical factor.

GustFactor

The gust factor.

Kd

The directionality factor.

SolidGrossRatio

The solid area divided by gross area ratio for open frame structure loading. This item applies only
when the loading is from open structure wind loading (ExposureFrom = 3 or ExposureFrom = 4).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for ASCE 7-02.


The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindASCE702()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim ASCECase As Long
Dim ASCEe1 As Double
Dim ASCEe2 As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim ImportanceFactor As Double
Dim Kzt As Double
Dim GustFactor As Double
Dim Kd As Double
Dim SolidGrossRatio As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)


ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE702 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE702("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,
False, 0, 0, 80, 3, 1, 1.1, 0.85, 0.88)

'get ASCE702 parameters
ret = SapModel.LoadPatterns.AutoWind.GetASCE702("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, ASCECase, ASCEe1, ASCEe2, UserZ, TopZ, BottomZ, WindSpeed, ExposureType,
ImportanceFactor, Kzt, GustFactor, Kd, SolidGrossRatio, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetASCE702

# GetASCE705

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetASCE705

## VB6 Procedure

Function GetASCE705(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef ASCECase As Long, ByRef
ASCEe1 As Double, ByRef ASCEe2 As Double, ByRef UserZ As Boolean, ByRef TopZ As
Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef ExposureType As
Long, ByRef ImportanceFactor As Double, ByRef Kzt As Double, ByRef GustFactor As Double,
ByRef Kd As Double, ByRef SolidGrossRatio As Double, ByRef UserExposure As Boolean) As
Long


## Parameters

Name

The name of an existing Wind-type load pattern with an ASCE7-05 auto wind assignment.

ExposureFrom

This is 1, 3 or 4, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
3 = From frame objects (open structure)
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1, 3, or 4.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

ASCECase

This is 1, 2, 3, 4 or 5, indicating the desired case from ASCE7-05 Figure 6-9. 1, 2, 3 and 4 refer to
cases 1 through 4 in the figure. 5 means to create all cases. This item applies only when
ExposureFrom = 1.

ASCEe1

This is the value e1 in ASCE7-05 Figure 6-9. This item applies only when ExposureFrom = 1.

ASCEe2

This is the value e2 in ASCE7-05 Figure 6-9. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed


The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
ImportanceFactor

The importance factor.

Kzt

The topographical factor.

GustFactor

The gust factor.

Kd

The directionality factor.

SolidGrossRatio

The solid area divided by the gross area ratio for open frame structure loading. This item applies
only when the loading is from open structure wind loading (ExposureFrom = 3 or ExposureFrom
= 4).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for ASCE 7-05.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindASCE705()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double


Dim Cpw As Double
Dim Cpl As Double
Dim ASCECase As Long
Dim ASCEe1 As Double
Dim ASCEe2 As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim ImportanceFactor As Double
Dim Kzt As Double
Dim GustFactor As Double
Dim Kd As Double
Dim SolidGrossRatio As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE705 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE705("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,
False, 0, 0, 80, 3, 1, 1.1, 0.85, 0.88)

'get ASCE705 parameters


ret = SapModel.LoadPatterns.AutoWind.GetASCE705("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, ASCECase, ASCEe1, ASCEe2, UserZ, TopZ, BottomZ, WindSpeed, ExposureType,
ImportanceFactor, Kzt, GustFactor, Kd, SolidGrossRatio, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetASCE705

# GetASCE788

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetASCE788

## VB6 Procedure

Function GetASCE788(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef
ExposureType As Long, ByRef ImportanceFactor As Double, ByRef GustFactor As Double,
ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an ASCE7-88 auto wind assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle


The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2, 3 or 4, indicating the exposure category.

```
1 = A
2 = B
3 = C
4 = D
```
ImportanceFactor

The importance factor.

GustFactor

The gust factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for ASCE 7-88.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.


## VBA Example

Sub GetWindASCE788()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim ImportanceFactor As Double
Dim GustFactor As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE788 parameters


ret = SapModel.LoadPatterns.AutoWind.SetASCE788("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 0.85)

'get ASCE788 parameters
ret = SapModel.LoadPatterns.AutoWind.GetASCE788("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, ExposureType, ImportanceFactor, GustFactor,
UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetASCE788

# GetASCE795

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetASCE795

## VB6 Procedure

Function GetASCE795(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef
ExposureType As Long, ByRef ImportanceFactor As Double, ByRef Kzt As Double, ByRef
GustFactor As Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an ASCE7-95 auto wind assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.


```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2, 3 or 4, indicating the exposure category.

```
1 = A
2 = B
3 = C
4 = D
```
ImportanceFactor

The importance factor.

Kzt

The topographical factor.

GustFactor

The gust factor.

UserExposure


If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for ASCE 7-95.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindASCE795()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim ImportanceFactor As Double
Dim Kzt As Double
Dim GustFactor As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm


ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE795 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE795("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 1.1, 0.85)

'get ASCE795 parameters
ret = SapModel.LoadPatterns.AutoWind.GetASCE795("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, ExposureType, ImportanceFactor, Kzt,
GustFactor, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetASCE795

# GetASCE710

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetASCE710

## VB6 Procedure

Function GetASCE710(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef ASCECase As Long, ByRef
ASCEe1 As Double, ByRef ASCEe2 As Double, ByRef UserZ As Boolean, ByRef TopZ As
Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef ExposureType As


Long, ByRef ImportanceFactor As Double, ByRef Kzt As Double, ByRef GustFactor As Double,
ByRef Kd As Double, ByRef SolidGrossRatio As Double, ByRef UserExposure As Boolean) As
Long

## Parameters

Name

The name of an existing Wind-type load pattern with an ASCE7-10 auto wind assignment.

ExposureFrom

This is 1, 2, 3 or 4, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
3 = From frame objects (open structure)
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1, 3, or 4.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

ASCECase

This is 1, 2, 3, 4 or 5, indicating the desired case from ASCE7-10 Figure 27.4-8. 1, 2, 3 and 4 refer
to cases 1 through 4 in the figure. 5 means to create all cases. This item applies only when
ExposureFrom = 1.

ASCEe1

This is the value e1 in ASCE7-10 Figure 27.4-8. This item applies only when ExposureFrom = 1.

ASCEe2

This is the value e2 in ASCE7-10 Figure 27.4-8. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ


This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
ImportanceFactor

The importance factor.

Kzt

The topographical factor.

GustFactor

The gust factor.

Kd

The directionality factor.

SolidGrossRatio

The solid area divided by the gross area ratio for open frame structure loading. This item applies
only when the loading is from open structure wind loading (ExposureFrom = 3 or ExposureFrom
= 4).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for ASCE 7-10.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindASCE710()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim ASCECase As Long
Dim ASCEe1 As Double
Dim ASCEe2 As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim ImportanceFactor As Double
Dim Kzt As Double
Dim GustFactor As Double
Dim Kd As Double
Dim SolidGrossRatio As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE710 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE710("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,


False, 0, 0, 80, 3, 1, 1.1, 0.85, 0.88)

'get ASCE710 parameters
ret = SapModel.LoadPatterns.AutoWind.GetASCE710("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, ASCECase, ASCEe1, ASCEe2, UserZ, TopZ, BottomZ, WindSpeed, ExposureType,
ImportanceFactor, Kzt, GustFactor, Kd, SolidGrossRatio, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 15.0.0

## See Also

SetASCE710

# GetASCE716

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetASCE716

## VB6 Procedure

Function GetASCE716(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef ASCECase As Long, ByRef
ASCEe1 As Double, ByRef ASCEe2 As Double, ByRef UserZ As Boolean, ByRef TopZ As
Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef ExposureType As
Long, ByRef Kzt As Double, ByRef GustFactor As Double, ByRef Kd As Double, ByRef
SolidGrossRatio As Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an ASCE7-16 auto wind assignment.

ExposureFrom

This is 1, 2, 3 or 4, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
3 = From frame objects (open structure)
```

```
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1, 3, or 4.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

ASCECase

This is 1, 2, 3, 4 or 5, indicating the desired case from ASCE7-16 Figure 27.3-8. 1, 2, 3 and 4 refer
to cases 1 through 4 in the figure. 5 means to create all cases. This item applies only when
ExposureFrom = 1.

ASCEe1

This is the value e1 in ASCE7-16 Figure 27.3-8. This item applies only when ExposureFrom = 1.

ASCEe2

This is the value e2 in ASCE7-16 Figure 27.3-8. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
Kzt

The topographical factor.


GustFactor

The gust factor.

Kd

The directionality factor.

SolidGrossRatio

The solid area divided by the gross area ratio for open frame structure loading. This item applies
only when the loading is from open structure wind loading (ExposureFrom = 3 or ExposureFrom
= 4).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for ASCE 7-16.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindASCE716()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim ASCECase As Long
Dim ASCEe1 As Double
Dim ASCEe2 As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim Kzt As Double
Dim GustFactor As Double
Dim Kd As Double
Dim SolidGrossRatio As Double
Dim UserExposure As Boolean

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE716 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE716("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,
False, 0, 0, 80, 3, 1.1, 0.85, 0.88)

'get ASCE716 parameters
ret = SapModel.LoadPatterns.AutoWind.GetASCE716("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, ASCECase, ASCEe1, ASCEe2, UserZ, TopZ, BottomZ, WindSpeed, ExposureType,
Kzt, GustFactor, Kd, SolidGrossRatio, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.2.0

## See Also


SetASCE716

# GetASNZS117022002

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetASNZS117022002

## VB6 Procedure

Function GetASNZS117022002(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByRef Ka As Double,
ByRef Kc As Double, ByRef Kl As Double, ByRef Kp As Double, ByRef UserZ As Boolean,
ByRef TopZ As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef Cat
As Long, ByRef CycloneRegion As Boolean, ByRef Md As Double, ByRef Ms As Double,
ByRef Mt As Double, ByRef Cdyn As Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load case with an AS/NZS 1170.2:2002 auto wind assignment.

ExposureFrom

This is 1, or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
```
```
2 = From area objects
```
DirAngle

The direction angle for the wind load.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

Ka

The area reduction factor, Ka.

Kc

The combination factor, Kc.

Kl


The local pressure factor, Kl.

Kp

The porous cladding factor, Kp.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The regional wind speed, Vr, in m/s.

Cat

This is 1, 2, 3 or 4, indicating the terrain category.

CycloneRegion

This is True or False, indicating if the structure is in a cyclone region.

Md

The directional multiplier, Md.

Ms

The shielding multiplier, Ms.

Mt

The topographic multiplier, Mt.

Cdyn

The dynamic response factor, Cdyn.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for AS/NZS 1170.2:2002.


The function returns zero if the parameters are successfully assigned; otherwise, it returns a
nonzero value.

## VBA Example

Sub GetWindASNZS117022002()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim Ka As Double
Dim Kc As Double
Dim Kl As Double
Dim Kp As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim Cat As Long
Dim CycloneRegion As Boolean
Dim Md As Double
Dim Ms As Double
Dim Mt As Double
Dim Cdyn As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load case
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign AS/NZS 1170.2:2002 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASNZS117022002("WIND", 1, 0, 0.8, 0.5, 1, 1,
1, 1, False, 0, 0, 50, 2, False, 1, 1, 1, 1)


'get AS/NZS 1170.2:2002 parameters
ret = SapModel.LoadPatterns.AutoWind.GetASNZS117022002("WIND", ExposureFrom,
DirAngle, Cpw, Cpl, Ka, Kc, Kl, Kp, UserZ, TopZ, BottomZ, WindSpeed, Cat, CycloneRegion,
Md, Ms, Mt, Cdyn, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.1.0.

## See Also

SetASNZS117022002

# GetBOCA96

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetBOCA96

## VB6 Procedure

Function GetBOCA96(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef
ExposureType As Long, ByRef ImportanceFactor As Double, ByRef UserGust As Boolean,
ByRef GustFactor As Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an BOCA 96 auto wind assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.


Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2, 3 or 4, indicating the exposure category.

```
1 = A
2 = B
3 = C
4 = D
```
ImportanceFactor

The importance factor.

UserGust

If this item is True, the gust factor is user defined. If it is False, the gust factor is determined from
the code specified values.

GustFactor

The user defined gust factor. This item applies only when UserGust is True.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for BOCA 96.


The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindBOCA96()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim ImportanceFactor As Double
Dim UserGust As Boolean
Dim GustFactor As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection


'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign BOCA96 parameters
ret = SapModel.LoadPatterns.AutoWind.SetBOCA96("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 0.85, True, False)

'get BOCA96 parameters
ret = SapModel.LoadPatterns.AutoWind.GetBOCA96("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, ExposureType, ImportanceFactor, UserGust,
GustFactor, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetBOCA96

# GetBS639995

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetBS639995

## VB6 Procedure

Function GetBS639995(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef Ve As Double, ByRef Ca As Double, ByRef
Cr As Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an BS6399-95 auto wind assignment.


ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The front coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The rear coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

Ve

The effective wind speed in meters per second.

Ca

The size effect factor.

Cr

The dynamic augmentation factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for BS6399-95.


The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindBS639995()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim Ve As Double
Dim Ca As Double
Dim Cr As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)


'assign BS639995 parameters
ret = SapModel.LoadPatterns.AutoWind.SetBS639995("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 32,
1.1,0.28)

'get BS639995 parameters
ret = SapModel.LoadPatterns.AutoWind.GetBS639995("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, Ve, Ca, Cr, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetBS639995

# GetChinese2010

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetChinese2010

## VB6 Procedure

Function GetChinese2010_1(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef BuildingWidth As Double, ByRef Us As Double, ByRef
UniformTaper As Boolean, ByRef BHoverB0 As Double, ByRef UserZ As Boolean, ByRef TopZ
As Double, ByRef BottomZ As Double, ByRef wzero As Double, ByRef Rt As Long, ByRef
PhiZOpt As Long, ByRef T1Opt As Long, ByRef UserT As Double, ByRef DampRatio As
Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an Chinese 2010 auto wind assignment.

ExposureFrom


This is 1 or 2 indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

BuildingWidth

The building width. [L]

Us

The shape coefficient. This item applies only when ExposureFrom = 1.

UniformTaper

This item is True if a correction is to be applied to the wind load for a uniform taper.

BHoverB0

The taper ratio, Bh/B0. This item applies only when UniformTaper = True.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

wzero

The basic wind pressure in kN/m^2.

Rt

This is 1, 2, 3 or 4, indicating the ground roughness.

```
1 = A
2 = B
3 = C
4 = D
```
PhiZOpt

This is 0 or 1, indicating the Phi Z source.


```
0 = Modal analysis
1 = Z/H ratio
```
T1Opt

This is 0 or 1, indicating the T1 source.

```
0 = Modal analysis
1 = User defined
```
UserT

This item only applies when the T1 source is user defined (T1Opt = 1). It is the user defined T1
period. [s]

DampRatio

The damping ratio.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for Chinese 2010.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindChinese2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim BuildingWidth As Double
Dim Us As Double
Dim UniformTaper As Boolean
Dim BHoverB0 As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim wzero As Double
Dim Rt As Long
Dim PhiZOpt As Long
Dim T1Opt As Long
Dim UserT As Double
Dim DampRatio As Double


Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign Chinese2010 parameters
ret = SapModel.LoadPatterns.AutoWind.SetChinese2010("WIND", 1, 0, 1200, 0.5, False, 1,
False, 0, 0, 0.48, 3, 1, 1, 0.6, 0.04)

'get Chinese2010 parameters
ret = SapModel.LoadPatterns.AutoWind.GetChinese2010("WIND", ExposureFrom,
DirAngle, BuildingWidth, Us, UniformTaper, BHoverB0, UserZ, TopZ, BottomZ, wzero, Rt,
PhiZOpt, T1Opt, UserT, DampRatio, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 15.0.2.


## See Also

SetChinese2010

# GetEurocode12005_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetEurocode12005_1

## VB6 Procedure

Function GetEurocode12005_1(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean,
ByRef TopZ As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef
Terrain As Long, ByRef Orography As Double, ByRef k1 As Double, ByRef CsCd As Double,
ByRef Rho As Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with a Eurocode 1 2005 auto wind assignment.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]


BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The basic wind speed, vb, in meters per second.

Terrain

This is 0, 1, 2, 3 or 4, indicating the terrain category.

```
0 = 0
1 = I
2 = II
3 = III
4 = IV
```
Orography

The orography factor, Co.

k1

The turbulence factor, k1.

CsCd

The structural factor, CsCd.

Rho

The air density in kg/m^3 , Rho.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for Eurocode 1 2005.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindEurocode12005()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim Terrain As Long
Dim Orography As Double
Dim k1 As Double
Dim CsCd As Double
Dim Rho As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign Eurocode 1 2005 parameters
ret = SapModel.LoadPatterns.AutoWind.SetEurocode12005_1("WIND", 1, 0, 0.8, 0.5, False,
0, 0, 35, 2, 1, 1, 1)

'get Eurocode 1 2005 parameters
ret = SapModel.LoadPatterns.AutoWind.GetEurocode12005_1("WIND", ExposureFrom,
DirAngle, Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, Terrain, Orography, k1, CsCd,


UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.1.0.

This function supersedes GetEurocode12005.

## See Also

SetEurocode12005_1

# GetExposure_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetExposure_1

## VB6 Procedure

Function GetExposure_1(ByVal Name As String, ByRef Num As Long, ByRef Diaph() As String,
ByRef x() As Double, ByRef y() As Double, ByRef MyWidth() As Double, ByRef MyDepth() As
Double, ByRef Height() As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern that has an auto wind load assigned.

Num

The number of diaphragms at which exposure data is reported.

Diaph

This is an array that includes the names of the diaphragms that have eccentricity overrides.

x


This is an array that includes the global X-coordinate of the point where the wind force load is
applied to the diaphragm. [L]

y

This is an array that includes the global Y-coordinate of the point where the wind force load is
applied to the diaphragm. [L]

MyWidth

This is an array that includes the exposure width for the wind load applied to the specified
diaphragm. [L]

MyDepth

This is an array that includes the exposure depth for the wind load applied to the specified
diaphragm. [L]

Height

This is an array that includes the exposure height for the wind load applied to the specified
diaphragm. [L]

## Remarks

This function retrieves exposure parameters for auto wind loads determined from extents of rigid
diaphragms. This function does not apply for User-type auto wind loads.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindExposure_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Diaph() As String
Dim x() As Double
Dim y() As Double
Dim MyWidth() As Double
Dim MyDepth() As Double
Dim Height() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object


Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE788 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE788("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 0.85, True)

'assign user exposure data
ret = SapModel.LoadPatterns.AutoWind.SetExposure_1("WIND", "Diaph2", 0, 0, 900, 90,
125)

'get exposure data
ret = SapModel.LoadPatterns.AutoWind.GetExposure_1("WIND", Num, Diaph, x, y,
MyWidth, MyDepth, Height)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.3.0.

This function supersedes GetExposure.

## See Also

SetExposure_1


# GetIS8751987

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetIS8751987

## VB6 Procedure

Function GetIS8751987(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef Terrain As
Long, ByRef Class As Long, ByRef K1 As Double, ByRef K3 As Double, ByRef UserExposure
As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an Indian IS875-1987 auto wind assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ


This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in meters per second.

Terrain

This is 1, 2, 3 or 4, indicating the terrain category.

Class

This is 1, 2 or 3, indicating the terrain category.

```
1 = A
2 = B
3 = C
```
K1

The risk coefficient (k1 factor).

K3

The topography factor (k3 factor).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for Indian IS875-1987.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindIS8751987()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double


Dim WindSpeed As Double
Dim Terrain As Long
Dim Class As Long
Dim K1 As Double
Dim K3 As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign IS8751987 parameters
ret = SapModel.LoadPatterns.AutoWind.SetIS8751987("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
60, 3, 3, 1.1, 1.2)

'get IS8751987 parameters
ret = SapModel.LoadPatterns.AutoWind.GetIS8751987("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, Terrain, Class, K1, K3, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetIS8751987

# GetIS8752015

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetIS8752015

## VB6 Procedure

Function GetIS8752015(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef
TerrainCategory As Long, ByRef ImportanceFactor As Long, ByRef k1 As Double, ByRef k3 As
Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an Indian IS 875:2015 auto wind
assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.


UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in meters per second.

TerrainCategory

This is 1, 2, 3 or 4, indicating the terrain category.

ImportanceFactor

This is 1, 2 or 3, depending on the importance factor.

```
1 = 1.00
2 = 1.15
3 = 1.30
```
k1

The risk coefficient (k1 factor).

k3

The topography factor (k3 factor).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for Indian IS875-2015.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example


Sub GetWindIS8752015()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim TerrainCategory As Long
Dim ImportanceFactor As Long
Dim k1 As Double
Dim k3 As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign IS8752015 parameters
ret = SapModel.LoadPatterns.AutoWind.SetIS8752015("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
60, 3, 3, 1.1, 1.2)


'get IS8752015 parameters
ret = SapModel.LoadPatterns.AutoWind.GetIS8752015("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, TerrainCategory, ImportanceFactor, k1, k3,
UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.2.0.

## See Also

SetIS8752015

# GetMexican

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetMexican

## VB6 Procedure

Function GetMexican(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef
UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an Indian IS875-1987 auto wind assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.


Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in meters per second.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves the Mexican auto wind loading parameters.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindMexican()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double


Dim WindSpeed As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign Mexican parameters
ret = SapModel.LoadPatterns.AutoWind.SetMexican("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 40)

'get Mexican parameters
ret = SapModel.LoadPatterns.AutoWind.GetMexican("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetMexican

# GetNBCC2015{Wind Load}

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetNBCC2015

## VB6 Procedure

Function GetNBCC2015(ByVal Name As String, ByVal ExposureFrom As Long, ByRef
DirAngle As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByVal NBCCCase As Long,
ByVal e1 As Double, ByVal e2 As Double, ByVal UserZ As Boolean, ByVal TopZ As Double,
ByVal BottomZ As Double, ByRef q As Double, ByRef GustFactor As Double, ByVal
TopographicFactor As Double, ByRef ImportanceFactor As Double, ByRef TerrainType As
Long, ByRef CeWindward As Double, ByRef CeLeeward As Double, ByRef UserExposure As
Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an NBCC 2015 auto wind assignment..

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

NBCCCase


This is 1, 2, 3, 4, or 5, indicating the desired case from NBCC 2105 Figure A-4.1.7.9(1). 1,2,3, and
4 refer to cases 1 through 4 in the figure, while 5 means all cases. This item applies only when
ExposureFrom = 1.

**e1**

This is the value e1 in the NBCC 2015 Figure A-4.1.7.9(1). This item applies only when
ExposureFrom = 1.

**e2**

This is the value e2 in the NBCC 2015 Figure A-4.1.7.9(1). This item applies only when
ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

q

The velocity pressure in kPa.

GustFactor

The gust effect factor, Cg.

TopographicFactor

The importance factor, Ct.

ImportanceFactor

The importance Factor, Iw.

TerrainType

This is 1, 2, or 3, indicating the terrain type.

```
1 = Open
```
```
2 = Rough
```
```
3 = User
```
CeWindward


The windward exposure factor, Ce. This item applies only when TerrainType = 3.

CeLeeward

The windward exposure factor, Ce. This item applies only when TerrainType = 3.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NBCC 2015.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindNBCC2015()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim ExposureFrom As Long

Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim NBCCCase As Long

Dim e1 As Double

Dim e2 As Double

Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim q As Double
Dim GustFactor As Double
Dim ImportanceFactor As Double

Dim TerrainType As Long

Dim CeWindward As Double

Dim CeLeeward As Double
Dim UserExposure As Boolean

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign NBCC2015 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNBCC2015("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
0.75, 2.1, 1.1, 1, 0, 0)

'get NBCC2015 parameters
ret = SapModel.LoadPatterns.AutoWind.GetNBCC2015("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, Case, e1, e2, UserZ, TopZ, BottomZ, q, GustFactor, TopographicFactor,
ImportanceFactor, TerrainType, CeWindward, CeLeeward, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

## See Also


Set NBCC2015

# GetNBCC2010_1 {Wind Load}

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetNBCC2010_1

## VB6 Procedure

Function GetNBCC2010_1(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean,
ByRef TopZ As Double, ByRef BottomZ As Double, ByRef q As Double, ByRef GustFactor As
Double, ByRef ImportanceFactor As Double, ByRef TerrainType As Long, ByRef CeWindward
As Double, ByRef CeLeeward As Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an NBCC 2010 auto wind assignment.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ


This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

q

The velocity pressure in kPa.

GustFactor

The gust effect factor.

ImportanceFactor

The importance factor.

TerrainType

This is 1, 2, or 3, indicating the terrain type.

```
1 = Open
```
```
2 = Rough
```
```
3 = User
```
CeWindward

The windward exposure factor, Ce. This item applies only when TerrainType = 3.

CeLeeward

The windward exposure factor, Ce. This item applies only when TerrainType = 3.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NBCC 2010.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindNBCC2010()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim q As Double
Dim GustFactor As Double
Dim ImportanceFactor As Double

Dim TerrainType As Long

Dim CeWindward As Double

Dim CeLeeward As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign NBCC2010 parameters


ret = SapModel.LoadPatterns.AutoWind.SetNBCC2010_1("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
0.75, 2.1, 1.1, 1, 0, 0)

'get NBCC2010 parameters
ret = SapModel.LoadPatterns.AutoWind.GetNBCC2010_1("WIND", ExposureFrom,
DirAngle, Cpw, Cpl, UserZ, TopZ, BottomZ, q, GustFactor, ImportanceFactor, TerrainType,
CeWindward, CeLeeward, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

This function supersedes GetNBCCC2010.

## See Also

SetNBCC2010_1

# GetNBCC2005

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetNBCC2005

## VB6 Procedure

Function GetNBCC2005(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean,
ByRef TopZ As Double, ByRef BottomZ As Double, ByRef q As Double, ByRef GustFactor As
Double, ByRef ImportanceFactor As Double, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an NBCC 2005 auto wind assignment.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```

DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

q

The velocity pressure in kPa.

GustFactor

The gust effect factor.

ImportanceFactor

The importance factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NBCC 2005.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindNBCC2005()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim q As Double
Dim GustFactor As Double
Dim ImportanceFactor As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign NBCC2005 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNBCC2005("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
0.75, 2.1, 1.1)

'get NBCC2005 parameters
ret = SapModel.LoadPatterns.AutoWind.GetNBCC2005("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, q, GustFactor, ImportanceFactor, UserExposure)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetNBCC2005

# GetNBCC95

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetNBCC95

## VB6 Procedure

Function GetNBCC95(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle
As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef
TopZ As Double, ByRef BottomZ As Double, ByRef q As Double, ByRef GustFactor As Double,
ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an NBCC 95 auto wind assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl


The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

q

The velocity pressure in kPa.

GustFactor

The gust effect factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NBCC 95.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindNBCC95()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim q As Double
Dim GustFactor As Double
Dim UserExposure As Boolean


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign NBCC95 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNBCC95("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
0.75, 2.1)

'get NBCC95 parameters
ret = SapModel.LoadPatterns.AutoWind.GetNBCC95("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, q, GustFactor, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

SetNBCC95

# GetNTC2008_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetNTC2008_1

## VB6 Procedure

Function GetNTC2008_1(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean,
ByRef TopZ As Double, ByRef BottomZ As Double, ByRef vr As Double, ByRef
ExposureCategory As Long, ByRef ct As Double, ByRef cd As Double, ByRef UserExposure As
Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an NTC 2008 auto wind assignment.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]


BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

vr

The wind velocity in m/s.

ExposureCategory

This is 1, 2, 3, 4, or 5, indicating the exposure category.

```
1 = I
2 = II
3 = III
4 = IV
5 = V
```
ct

The topography factor, ct.

cd

The dynamic coefficient, cd.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NTC 2008.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindNTC2008()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double


Dim vr As Double
Dim ExposureCategory As Long

Dim ct As Double

Dim cd As Double

Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", eLoadPatternType_WIND)

'assign NTC2008 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNTC2008_1("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 35, 3,
1, 1, False)

'get NTC2008 parameters
ret = SapModel.LoadPatterns.AutoWind.GetNTC2008_1("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, vr, ExposureCategory, ct, cd, UserExposure )

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 25.2.0.

This function supersedes GetNTC2008.

## See Also

SetNTC2008_1

# GetNTC2018_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetNTC2018_1

## VB6 Procedure

Function GetNTC2018_1(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean,
ByRef TopZ As Double, ByRef BottomZ As Double, ByRef vr As Double, ByRef
ExposureCategory As Long, ByRef ct As Double, ByRef cd As Double, ByRef UserExposure As
Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an NTC 2018 auto wind assignment.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ


This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

Vr

The wind velocity in m/s.

ExposureCategory

This is 1, 2, 3, 4, or 5, indicating the exposure category.

```
1 = I
2 = II
3 = III
4 = IV
5 = V
```
ct

The topography factor, ct.

cd

The dynamic coefficient, cd.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NTC 2018.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindNTC2018()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long


Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim vr As Double
Dim ExposureCategory As Long

Dim ct As Double

Dim cd As Double

Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", eLoadPatternType_WIND)

'assign NTC2018 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNTC2018_1("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 35, 3,
1, 1, False)

'get NTC2018 parameters
ret = SapModel.LoadPatterns.AutoWind.GetNTC2018_1("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, vr, ExposureCategory, ct, cd, UserExposure )


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.2.0.

This function supersedes GetNTC2018.

## See Also

SetNTC2018_1

# GetSP20133302016

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetSP20133302016

## VB6 Procedure

Function GetSP20133302016 (ByVal Name As String, ByRef LoadingType As Long, ByRef
ExposureFrom As Long, ByRef DirAngle As Double, ByRef Cp As Double, ByRef UserZ As
Boolean, ByRef TopZ As Double, ByRef BottomZ As Double, ByRef StructureType As Integer,
ByRef LogDecrement As Integer, ByRef BuildingWidth As Double, ByRef BuildingDepth As
Double, ByRef Zeq As Double, ByRef WindDistrict As Long, ByRef WindPressure As Double,
ByRef TerrainType As Long, ByRef LimitFreq As Double, ByRef ModalCase As String, ByRef
FirstValMode As Long, ByRef UserExposure As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with a SP 20.13330.2016 auto wind assignment.

LoadingType

This indicates whether the loads should be calculated as static or dynamic.

```
1 = Static
2 = Dynamic
```
ExposureFrom


This is 1 or 2, indicating the source of the wind exposure. This item applies only when
LoadingType = 1.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item does not apply when ExposureFrom = 2.

Cp

The wind coefficient, Cp. This item applies only when LoadingType = 1 and ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

StructureType

This indicates the structure type for calculating the wind pressure.

```
1 = Building
2 = Other
```
LogDecrement

This specifies a value for the logarithmic decrement. This item applies only when LoadingType =
2.

```
1 = 0.15
2 = 0.30
```
BuildingWidth

This is the building width, normal to the wind direction. [L]

BuildingDepth

This is the building depth, in the direction of the wind. This item applies only when LoadingType
= 2. [L]

Zeq


This is the equivalent height, Zeq, of the structure. This item applies only when LoadingType = 2.
[L]

WindDistrict

This is the wind district to consider.

```
0 = Ia
1 = I
2 = II
3 = III
4 = IV
5 = V
6 = VI
7 = VII
8 = User Defined
```
WindPressure

This is the wind pressure. This item applies only when WindDistrict = 8. [F/L^2 ]

TerrainType

This is the terrain type being considered.

```
1 = A
2 = B
3 = C
```
LimitFreq

The limit frequency. This item applies only when LoadingType = 2 and WindDistrict = 8.

ModalCase

The name of an existing modal load case to be used in determining dynamic wind loads. This item
applies only when LoadingType = 2.

FirstValMode

The first valuable mode number from the specified modal case. This item applies only when
LoadingType = 2.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms. This item
applies only when LoadingType = 1.

## Remarks

This function retrieves auto wind loading parameters for SP 20.13330.2016.


The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindSP20133302016()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim LoadingType As Long

Dim ExposureFrom As Long

Dim DirAngle As Double

Dim Cp As Double

Dim UserZ As Boolean

Dim TopZ As Double

Dim BottomZ As Double

Dim StructureType As Long

Dim LogDecrement As Long

Dim BuildingWidth As Double

Dim Building Depth As Double

Dim Zeq As Double

Dim WindDistrict As Long

Dim WindPressure As Double

Dim TerrainType As Long

Dim LimitFreq As Double

Dim ModalCase As String

Dim FirstValMode As Long

Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection

ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign SP 20.13330.2016 parameters
ret = SapModel.LoadPatterns.AutoWind.SetSP20133302016("WIND", 1, 1, 0, 0.8, False, 0,
0, 1, 1, 10, 10, 10, 3, 0.1, 2, 10, “MODAL”, 1)

'get SP 20.13330.2016 parameters

ret = SapModel.LoadPatterns.AutoWind.GetSP20133302016("WIND", LoadingType,
ExposureFrom, DirAngle, Cp, UserZ, TopZ, BottomZ, StructureType, LogDecrement,
BuildingWidth, BuildingDepth, Zeq, WindDistrict, WindPressure, TerrainType, LimitFreq,
ModalCase, FirstValMode, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in v21.0.0.

## See Also

SetSP20133302016

# GetUBC94

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetUBC94

## VB6 Procedure

Function GetUBC94(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle As
Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef TopZ
As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef ExposureType As
Long, ByRef ImportanceFactor As Double, ByRef GustFactor As Double, ByRef UserExposure
As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an UBC94 auto wind assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.


UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
ImportanceFactor

The importance factor.

GustFactor

The gust factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for 1994 UBC.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindUBC94()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double


Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim ImportanceFactor As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign UBC94 parameters
ret = SapModel.LoadPatterns.AutoWind.SetUBC94("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80, 3,
1.15)

'get UBC94 parameters
ret = SapModel.LoadPatterns.AutoWind.GetUBC94("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, ExposureType, ImportanceFactor, UserExposure)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUBC94

# GetUBC97

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetUBC97

## VB6 Procedure

Function GetUBC97(ByVal Name As String, ByRef ExposureFrom As Long, ByRef DirAngle As
Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean, ByRef TopZ
As Double, ByRef BottomZ As Double, ByRef WindSpeed As Double, ByRef ExposureType As
Long, ByRef ImportanceFactor As Double, ByRef GustFactor As Double, ByRef UserExposure
As Boolean) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an UBC97 auto wind assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.


Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
ImportanceFactor

The importance factor.

GustFactor

The gust factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for 1997 UBC.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindUBC97()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim ExposureFrom As Long
Dim DirAngle As Double
Dim Cpw As Double
Dim Cpl As Double
Dim UserZ As Boolean
Dim TopZ As Double
Dim BottomZ As Double
Dim WindSpeed As Double
Dim ExposureType As Long
Dim ImportanceFactor As Double
Dim UserExposure As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign UBC97 parameters
ret = SapModel.LoadPatterns.AutoWind.SetUBC97("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80, 3,
1.15)

'get UBC97 parameters
ret = SapModel.LoadPatterns.AutoWind.GetUBC97("WIND", ExposureFrom, DirAngle,
Cpw, Cpl, UserZ, TopZ, BottomZ, WindSpeed, ExposureType, ImportanceFactor, UserExposure)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUBC97

# GetUserLoad

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.GetUserLoad

## VB6 Procedure

Function GetUserLoad(ByVal Name As String, ByRef Num As Long, ByRef Diaph() As String,
ByRef Fx() As Double, ByRef Fx() As Double, ByRef Mz() As Double, ByRef x() As Double,
ByRef y() As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern that has a User-type auto wind load assigned.

Num

The number of diaphragms at which user wind loads are reported.

Diaph

This is an array that includes the names of the diaphragms that have user wind loads.

Fx

This is an array that includes the global X direction force assigned to the specified diaphragm. [F]

Fy


This is an array that includes the global Y direction force assigned to the specified diaphragm. [F]

Mz

This is an array that includes the moment about the global Z axis assigned to the specified
diaphragm. [FL]

x

This is an array that includes the global X-coordinate of the point where the wind force load is
applied to the diaphragm. [L]

y

This is an array that includes the global Y-coordinate of the point where the wind force load is
applied to the diaphragm. [L]

## Remarks

This function retrieves auto wind loading parameters for User-type wind loading.

The function returns zero if the parameters are successfully assigned, otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindUser()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Diaph() As String
Dim Fx() As Double
Dim Fy() As Double
Dim Mz() As Double
Dim x() As Double
Dim y() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template


ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign user wind load parameters
ret = SapModel.LoadPatterns.AutoWind.SetUserLoad("WIND", "Diaph1", 100, 20, 5000, 0,
0)
ret = SapModel.LoadPatterns.AutoWind.SetUserLoad("WIND", "Diaph2", 50, 10, 2500, 0, 0)

'get user wind load parameters
ret = SapModel.LoadPatterns.AutoWind.GetUserLoad("WIND", Num, Diaph, Fx, Fy, Mz, x,
y)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetUserLoad

GetSpecialRigidDiaphragmList

# SetAPI4F2008_1

## Syntax


SapObject.SapModel.LoadPatterns.AutoWind.SetAPI4F2008_1

## VB6 Procedure

Function SetAPI4F2008_1(ByVal Name As String, ByVal ExposureFrom As Long, ByVal
DirAngle As Double, ByVal UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As
Double, ByVal WindSpeed As Double, ByVal SSLFactor As Double, ByVal ShieldingFactor As
Double) As Long

## Parameters

Name

The name of an existing Wind-type load case.

ExposureFrom

This is 2, 3, or 4, indicating the source of the wind exposure.

```
2 = From area objects
```
```
3 = From frame objects (open structure)
```
```
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 3 or 4.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The design reference wind velocity, Vref, in knots.

SSLFactor

The structural safety level multiplier.

ShieldingFactor

The shielding factor.


## Remarks

This function assigns auto wind loading parameters for API 4F 2008.

The function returns zero if the parameters are successfully assigned; otherwise, it returns a
nonzero value.

## VBA Example

Sub AssignWindAPI4F2008()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load case
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign API 4F 2008 parameters
ret = SapModel.LoadPatterns.AutoWind.SetAPI4F2008_1("WIND", 3, 0, False, 0, 0, 93, 1.1,
0.85)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.1.0.

This function supersedes SetAPI4F2008.


## See Also

GetAPI4F2008_1

# SetAPI4F2013

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetAPI4F2013

## VB6 Procedure

Function SetAPI4F2013(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal UserZ As Boolean, ByVal TopZ As Double, ByVal BottomZ As Double,
ByVal WindSpeed As Double, ByVal SSLFactor As Double, ByVal ShieldingFactor As Double)
As Long

## Parameters

Name

The name of an existing Wind-type load case.

ExposureFrom

This is 2, 3, or 4, indicating the source of the wind exposure.

```
2 = From area objects
```
```
3 = From frame objects (open structure)
```
```
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 3 or 4.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed


The design reference wind velocity, Vref, in knots.

SSLFactor

The structural safety level multiplier.

ShieldingFactor

The shielding factor.

## Remarks

This function assigns auto wind loading parameters for API 4F 2013.

The function returns zero if the parameters are successfully assigned; otherwise, it returns a
nonzero value.

## VBA Example

Sub AssignWindAPI4F2013()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load case
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign API 4F 2013 parameters
ret = SapModel.LoadPatterns.AutoWind.SetAPI4F2013("WIND", 3, 0, False, 0, 0, 93, 1.1,
0.85)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 16.1.0.

## See Also

GetAPI4F2013

# SetASCE702

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetASCE702

## VB6 Procedure

Function SetASCE702(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal ASCECase As Long, ByVal
ASCEe1 As Double, ByVal ASCEe2 As Double, ByVal UserZ As Boolean, ByVal TopZ As
Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal ExposureType As
Long, ByVal ImportanceFactor As Double, ByVal Kzt As Double, ByVal GustFactor As Double,
ByVal Kd As Double, Optional ByVal SolidGrossRatio As Double = 0.2, Optional ByVal
UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1, 2, 3 or 4, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
3 = From frame objects (open structure)
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1, 3, or 4.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl


The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

ASCECase

This is either 1, 2, 3, 4 or 5, indicating the desired case from ASCE7-02 Figure 6-9. 1, 2, 3 and 4
refer to cases 1 through 4 in the figure. 5 means to create all cases. This item applies only when
ExposureFrom = 1.

ASCEe1

This is the value e1 in ASCE7-02 Figure 6-9. This item applies only when ExposureFrom = 1.

ASCEe2

This is the value e2 in ASCE7-02 Figure 6-9. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies pnly when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2, 3 or 4, indicating the exposure category.

```
1 = A
2 = B
3 = C
4 = D
```
ImportanceFactor

The importance factor.

Kzt

The topographical factor.

GustFactor

The gust factor.


Kd

The directionality factor.

SolidGrossRatio

The solid area divided by gross area ratio for open frame structure loading. This item applies only
when the loading is from open structure wind loading (ExposureFrom = 3 or ExposureFrom = 4).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for ASCE 7-02.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindASCE702()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)


ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE702 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE702("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,
False, 0, 0, 80, 3, 1, 1.1, 0.85, 0.88)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetASCE702

# SetASCE705

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetASCE705

## VB6 Procedure

Function SetASCE705(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal ASCECase As Long, ByVal
ASCEe1 As Double, ByVal ASCEe2 As Double, ByVal UserZ As Boolean, ByVal TopZ As
Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal ExposureType As
Long, ByVal ImportanceFactor As Double, ByVal Kzt As Double, ByVal GustFactor As Double,
ByVal Kd As Double, Optional ByVal SolidGrossRatio As Double = 0.2, Optional ByVal
UserExposure As Boolean = False) As Long

## Parameters

Name


The name of an existing Wind-type load pattern.

ExposureFrom

This is 1, 2, 3 or 4, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
3 = From frame objects (open structure)
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1, 3, or 4.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

ASCECase

This is 1, 2, 3, 4 or 5, indicating the desired case from ASCE7-05 Figure 6-9. 1, 2, 3 and 4 refer to
cases 1 through 4 in the figure. 5 means to create all cases. This item applies only when
ExposureFrom = 1.

ASCEe1

This is the value e1 in ASCE7-05 Figure 6-9. This item applies only when ExposureFrom = 1.

ASCEe2

This is the value e2 in ASCE7-05 Figure 6-9. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.


ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
ImportanceFactor

The importance factor.

Kzt

The topographical factor.

GustFactor

The gust factor.

Kd

The directionality factor.

SolidGrossRatio

The solid area divided by gross area ratio for open frame structure loading. This item applies only
when the loading is from open structure wind loading (ExposureFrom = 3 or ExposureFrom = 4).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for ASCE 7-05.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindASCE705()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application


SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE705 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE705("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,
False, 0, 0, 80, 3, 1, 1.1, 0.85, 0.88)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetASCE705

# SetASCE788


## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetASCE788

## VB6 Procedure

Function SetASCE788(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal
ExposureType As Long, ByVal ImportanceFactor As Double, ByVal GustFactor As Double,
Optional ByVal UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed


The wind speed in miles per hour.

ExposureType

This is 1, 2, 3 or 4, indicating the exposure category.

```
1 = A
2 = B
3 = C
4 = D
```
ImportanceFactor

The importance factor.

GustFactor

The gust factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for ASCE 7-88.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindASCE788()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)


'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE788 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE788("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 0.85)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetASCE788

# SetASCE795

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetASCE795

## VB6 Procedure

Function SetASCE795(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal


ExposureType As Long, ByVal ImportanceFactor As Double, ByVal Kzt As Double, ByVal
GustFactor As Double, Optional ByVal UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2, 3 or 4, indicating the exposure category.

```
1 = A
2 = B
3 = C
4 = D
```

ImportanceFactor

The importance factor.

Kzt

The topographical factor.

GustFactor

The gust factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for ASCE 7-95.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindASCE795()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm


ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE795 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE795("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 1.1, 0.85)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetASCE795

# SetASCE710

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetASCE710

## VB6 Procedure

Function SetASCE710(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal ASCECase As Long, ByVal
ASCEe1 As Double, ByVal ASCEe2 As Double, ByVal UserZ As Boolean, ByVal TopZ As
Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal ExposureType As
Long, ByVal ImportanceFactor As Double, ByVal Kzt As Double, ByVal GustFactor As Double,
ByVal Kd As Double, Optional ByVal SolidGrossRatio As Double = 0.2, Optional ByVal
UserExposure As Boolean = False) As Long


## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1, 2, 3 or 4, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
3 = From frame objects (open structure)
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1, 3, or 4.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

ASCECase

This is 1, 2, 3, 4 or 5, indicating the desired case from ASCE7-10 Figure 27.4-8. 1, 2, 3 and 4 refer
to cases 1 through 4 in the figure. 5 means to create all cases. This item applies only when
ExposureFrom = 1.

ASCEe1

This is the value e1 in ASCE7-10 Figure 27.4-8. This item applies only when ExposureFrom = 1.

ASCEe2

This is the value e2 in ASCE7-10 Figure 27.4-8. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]


WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
ImportanceFactor

The importance factor.

Kzt

The topographical factor.

GustFactor

The gust factor.

Kd

The directionality factor.

SolidGrossRatio

The solid area divided by gross area ratio for open frame structure loading. This item applies only
when the loading is from open structure wind loading (ExposureFrom = 3 or ExposureFrom = 4).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for ASCE 7-10.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindASCE710()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE710 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE710("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,
False, 0, 0, 80, 3, 1, 1.1, 0.85, 0.88)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 15.0.0

## See Also

GetASCE710

# SetASCE716


## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetASCE716

## VB6 Procedure

Function SetASCE716(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal ASCECase As Long, ByVal
ASCEe1 As Double, ByVal ASCEe2 As Double, ByVal UserZ As Boolean, ByVal TopZ As
Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal ExposureType As
Long, ByVal Kzt As Double, ByVal GustFactor As Double, ByVal Kd As Double, Optional
ByVal SolidGrossRatio As Double = 0.2, Optional ByVal UserExposure As Boolean =
False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1, 2, 3 or 4, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
3 = From frame objects (open structure)
4 = From area objects and frame objects (open structure)
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1, 3, or 4.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

ASCECase

This is 1, 2, 3, 4 or 5, indicating the desired case from ASCE7-16 Figure 27.3-8. 1, 2, 3 and 4
refer to cases 1 through 4 in the figure. 5 means to create all cases. This item applies only when
ExposureFrom = 1.

ASCEe1

This is the value e1 in ASCE7-16 Figure 27.3-8. This item applies only when ExposureFrom = 1.

ASCEe2


This is the value e2 in ASCE7-16 Figure 27.3-8. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
Kzt

The topographical factor.

GustFactor

The gust factor.

Kd

The directionality factor.

SolidGrossRatio

The solid area divided by gross area ratio for open frame structure loading. This item applies only
when the loading is from open structure wind loading (ExposureFrom = 3 or ExposureFrom = 4).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for ASCE 7-16.


The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindASCE716()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE716 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE716("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,
False, 0, 0, 80, 3, 1.1, 0.85, 0.88)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 23.2.0

## See Also

GetASCE716

# SetASNZS117022002

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetASNZS117022002

## VB6 Procedure

Function SetASNZS117022002(ByVal Name As String, ByVal ExposureFrom As Long, ByVal
DirAngle As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal Ka As Double,
ByVal Kc As Double, ByVal Kl As Double, ByVal Kp As Double, ByVal UserZ As Boolean,
ByVal TopZ As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal Cat
As Long, ByVal CycloneRegion As Boolean, ByVal Md As Double, ByVal Ms As Double,
ByVal Mt As Double, ByVal Cdyn As Double, Optional ByVal UserExposure As Boolean =
False) As Long

## Parameters

Name

The name of an existing Wind-type load case.

ExposureFrom

This is 1, or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
```
```
2 = From area objects
```
DirAngle

The direction angle for the wind load.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.


Ka

The area reduction factor, Ka.

Kc

The combination factor, Kc.

Kl

The local pressure factor, Kl.

Kp

The porous cladding factor, Kp.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item is the global Z-coordinate at the highest level where auto wind loads are applied. [L]

BottomZ

This item is the global Z-coordinate at the lowest level where auto wind loads are applied. [L]

WindSpeed

The regional wind speed, Vr, in m/s.

Cat

This is 1, 2, 3 or 4, indicating the terrain category.

CycloneRegion

This is True or False, indicating if the structure is in a cyclone region.

Md

The directional multiplier, Md.

Ms

The shielding multiplier, Ms.

Mt

The topographic multiplier, Mt.

Cdyn

The dynamic response factor, Cdyn.


UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for AS/NZS 1170.2:2002.

The function returns zero if the parameters are successfully assigned; otherwise, it returns a
nonzero value.

## VBA Example

Sub AssignWindASNZS117022002()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'add new load case
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign AS/NZS 1170.2:2002 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASNZS117022002("WIND", 1, 0, 0.8, 0.5, 1, 1,
1, 1, False, 0, 0, 50, 2, False, 1, 1, 1, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.1.0.


## See Also

GetASNZS117022002

# SetBOCA96

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetBOCA96

## VB6 Procedure

Function SetBOCA96(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal
ExposureType As Long, ByVal ImportanceFactor As Double, ByVal GustFactor As Double,
Optional ByVal UserGust As Boolean = False, Optional ByVal UserExposure As Boolean =
False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ


This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2, 3 or 4, indicating the exposure category.

```
1 = A
2 = B
3 = C
4 = D
```
ImportanceFactor

The importance factor.

GustFactor

The user defined gust factor. This item applies only when UserGust is True.

UserGust

If this item is True, the gust factor is user defined. If it is False, the gust factor is determined from
the code specified values.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for BOCA 96.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindBOCA96()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign BOCA96 parameters
ret = SapModel.LoadPatterns.AutoWind.SetBOCA96("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 0.85, True, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also


GetBOCA96

# SetBS639995

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetBS639995

## VB6 Procedure

Function SetBS639995(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal Ve As Double, ByVal Ca As Double, ByVal
Cr As Double, Optional ByVal UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The front coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The rear coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ


This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

Ve

The effective wind speed in meters per second.

Ca

The size effect factor.

Cr

The dynamic augmentation factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for BS6399-95.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindBS639995()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)


'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign BS639995 parameters
ret = SapModel.LoadPatterns.AutoWind.SetBS639995("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 32,
1.1, 0.28)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetBS639995

# SetChinese2010

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetChinese2010

## VB6 Procedure

Function SetChinese2010(ByVal Name As String, ByVal ExposureFrom As Long, ByVal
DirAngle As Double, ByVal BuildingWidth As Double, ByVal Us As Double, ByVal
UniformTaper As Boolean, ByVal BHoverB0 As Double, ByVal UserZ As Boolean, ByVal TopZ
As Double, ByVal BottomZ As Double, ByVal wzero As Double, ByVal Rt As Long, ByVal
PhiZOpt As Long, ByVal T1Opt As Long, ByVal UserT As Double, ByVal DampRatio As
Double, Optional ByVal UserExposure As Boolean = False) As Long


## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item only applies when ExposureFrom = 1.

BuildingWidth

The building width. [L]

Us

The shape coefficient. This item applies only when ExposureFrom = 1.

UniformTaper

This item is True if a correction is to be applied to the wind load for a uniform taper.

BHoverB0

The taper ratio, Bh/B0. This item applies only when UniformTaper = True.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

wzero

The basic wind pressure in kN/m^2.

Rt

This is 1, 2, 3 or 4, indicating the ground roughness.


### 1 = A

### 2 = B

### 3 = C

### 4 = D

PhiZOpt

This is 0 or 1, indicating the Phi Z source.

```
0 = Modal analysis
1 = Z/H ratio
```
T1Opt

This is 0 or 1, indicating the T1 source.

```
0 = Modal analysis
1 = User defined
```
UserT

This item applies only when the T1 source is user defined (T1Opt = 1). It is the user defined T1
period. [s]

DampRatio

The damping ratio.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for Chinese 2010.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindChinese2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart


'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign Chinese2010 parameters
ret = SapModel.LoadPatterns.AutoWind.SetChinese2010("WIND", 1, 0, 1200, 0.5, False, 1,
False, 0, 0, 0.48, 3, 1, 1, 0.6, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 15.0.2.

## See Also

GetChinese2010

# SetEurocode12005_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetEurocode12005_1


## VB6 Procedure

Function SetEurocode12005_1(ByVal Name As String, ByVal ExposureFrom As Long, ByVal
DirAngle As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean,
ByVal TopZ As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal
Terrain As Long, ByVal Orography As Double, ByVal k1 As Double, ByVal CsCd As Double,
ByVal Rho As Double, Optional ByVal UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The basic wind speed, vb, in meters per second.

Terrain


This is 0, 1, 2, 3 or 4, indicating the terrain category.

```
0 = 0
1 = I
2 = II
3 = III
4 = IV
```
Orography

The orography factor, Co.

k1

The turbulence factor, k1.

CsCd

The structural factor, CsCd.

Rho

The air density in kg/m^3 , Rho.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for Eurocode 1 2005.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindEurocode12005()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel


'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign Eurocode 1 2005 parameters
ret = SapModel.LoadPatterns.AutoWind.SetEurocode12005_1("WIND", 1, 0, 0.8, 0.5, False,
0, 0, 35, 2, 1, 1, 1, 1.25)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.1.0.

This function supersedes SetEurocode12005.

## See Also

GetEurocode12005_1

# SetExposure_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetExposure_1


## VB6 Procedure

Function SetExposure_1(ByVal Name As String, ByVal Diaph As String, ByVal x As Double,
ByVal y As Double, ByVal Width As Double, ByVal Depth As Double, ByVal Height As
Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern that has an auto wind load assigned.

Diaph

The name of an existing special rigid diaphragm constraint, that is, a diaphragm constraint with
the following features:

1. The constraint type is CONSTRAINT_DIAPHRAGM = 2.
2. The constraint coordinate system is Global.
3. The constraint axis is Z.

x

The global X-coordinate of the point where the wind force is applied. [L]

y

The global Y-coordinate of the point where the wind force is applied. [L]

Width

The exposure width for the wind load applied to the specified diaphragm. [L]

Depth

The exposure depth for the wind load applied to the specified diaphragm. [L]

Height

The exposure height for the wind load applied to the specified diaphragm. [L]

## Remarks

This function assigns exposure parameters for auto wind loads determined from extents of rigid
diaphragms. This function does not apply for User-type auto wind loads.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value. The function returns an error if the auto wind load is not specified to have user
exposure parameters.

## VBA Example


Sub AssignWindUserExposure()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE788 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE788("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 0.85, True)

'assign user exposure data
ret = SapModel.LoadPatterns.AutoWind.SetExposure_1("WIND", "Diaph2", 0, 0, 900, 90,
124)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 17.3.0.

## See Also

GetExposure_1

# SetIS8751987

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetIS8751987

## VB6 Procedure

Function SetIS8751987(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal Terrain As
Long, ByVal Class As Long, ByVal K1 As Double, ByVal K3 As Double, Optional ByVal
UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ


This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in meters per second.

Terrain

This is 1, 2, 3 or 4, indicating the terrain category.

Class

This is 1, 2 or 3, indicating the terrain category.

```
1 = A
2 = B
3 = C
```
K1

The risk coefficient (k1 factor).

K3

The topography factor (k3 factor).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for Indian IS875-1987.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindIS8751987()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign IS8751987 parameters
ret = SapModel.LoadPatterns.AutoWind.SetIS8751987("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
60, 3, 3, 1.1, 1.2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetIS8751987

# SetIS8752015

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetIS8752015

## VB6 Procedure

Function SetIS8752015(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal
TerrainCategory As Long, ByVal ImportanceFactor As Long, ByVal k1 As Double, ByVal k3 As
Double, Optional ByVal UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern with an Indian IS 875:2015 auto wind
assignment.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ


This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in meters per second.

TerrainCategory

This is 1, 2, 3 or 4, indicating the terrain category.

ImportanceFactor

This is 1, 2 or 3, depending on the importance factor.

```
1 = 1.00
2 = 1.15
3 = 1.30
```
k1

The risk coefficient (k1 factor).

k3

The topography factor (k3 factor).

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for Indian IS875:2015.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindIS8752015()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign IS8752015 parameters
ret = SapModel.LoadPatterns.AutoWind.SetIS8752015("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
60, 3, 3, 1.1, 1.2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.2.0.

## See Also

GetIS8752015

# SetMexican


## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetMexican

## VB6 Procedure

Function SetMexican(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, Optional ByVal
UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed


The wind speed in meters per second.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns the Mexican auto wind loading parameters.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindMexican()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)


'assign Mexican parameters
ret = SapModel.LoadPatterns.AutoWind.SetMexican("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 40)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetMexican

# SetNBCC2015 {Wind Load}

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetNBCC2015

## VB6 Procedure

Function SetNBCC2015(ByVal Name As String, ByVal ExposureFrom As Long, ByVal
DirAngle As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal NBCCCase As Long,
ByVal e1 As Double, ByVal e2 As Double, ByVal UserZ As Boolean, ByVal TopZ As Double,
ByVal BottomZ As Double, ByVal q As Double, ByVal GustFactor As Double, ByVal
TopographicFactor As Double, ByVal ImportanceFactor As Double, ByVal TerrainType As
Long, ByVal CeWindward As Double, ByVal CeLeeward As Double, Optional ByVal
UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```

DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

NBCCCase

This is 1, 2, 3, 4, or 5, indicating the desired case from NBCC 2105 Figure A-4.1.7.9(1). 1,2,3, and
4 refer to cases 1 through 4 in the figure, while 5 means all cases. This item applies only when
ExposureFrom = 1.

**e1**

This is the value e1 in the NBCC 2015 Figure A-4.1.7.9(1). This item applies only when
ExposureFrom = 1.

**e2**

This is the value e2 in the NBCC 2015 Figure A-4.1.7.9(1). This item applies only when
ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

q

The velocity pressure in kPa.

GustFactor

The gust effect factor, Cg.

ImportanceFactor

The importance factor, Ct.

ImportanceFactor


The importance Factor, Iw.

TerrainType

This is 1, 2, or 3, indicating the terrain type.

```
1 = Open
```
```
2 = Rough
```
```
3 = User
```
CeWindward

The windward exposure factor, Ce. This item applies only when TerrainType = 3.

CeLeeward

The windward exposure factor, Ce. This item applies only when TerrainType = 3.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NBCC 2015.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub GetWindNBCC2015()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template


ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign NBCC2015 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNBCC2015("WIND", 1, 0, 0.8, 0.5, 2, 0.15, 0.18,
False, 0, 0, 0.75, 2.1, 1.1, 1.1, 1, 0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

## See Also

Get NBCC2015

# SetNBCC2010_1 {Wind Load}

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetNBCC2010_1

## VB6 Procedure

Function SetNBCC2010_1(ByVal Name As String, ByVal ExposureFrom As Long, ByVal
DirAngle As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean,
ByVal TopZ As Double, ByVal BottomZ As Double, ByVal q As Double, ByVal GustFactor As
Double, ByVal ImportanceFactor As Double, ByVal TerrainType As Long, ByVal CeWindward


As Double, ByVal CeLeeward As Double, Optional ByVal UserExposure As Boolean = False) As
Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

q

The velocity pressure in kPa.

GustFactor

The gust effect factor.

ImportanceFactor

The importance factor.


TerrainType

This is 1, 2, or 3, indicating the terrain type.

```
1 = Open
```
```
2 = Rough
```
```
3 = User
```
CeWindward

The windward exposure factor, Ce. This item applies only when TerrainType = 3.

CeLeeward

The windward exposure factor, Ce. This item applies only when TerrainType = 3.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NBCC 2010.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindNBCC2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)


'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign NBCC2010 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNBCC2010_1("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
0.75, 2.1, 1.1, 1, 0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

This function supersedes SetNBCCC2010.

## See Also

GetNBCC2010_1

# SetNBCC2005

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetNBCC2005

## VB6 Procedure

Function SetNBCC2005(ByVal Name As String, ByVal ExposureFrom As Long, ByVal
DirAngle As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean,
ByVal TopZ As Double, ByVal BottomZ As Double, ByVal q As Double, ByVal GustFactor As


Double, ByVal ImportanceFactor As Double, Optional ByVal UserExposure As Boolean = False)
As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

q

The velocity pressure in kPa.

GustFactor

The gust effect factor.

ImportanceFactor

The importance factor.


UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for NBCC 2005.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindNBCC2005()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign NBCC2005 parameters


ret = SapModel.LoadPatterns.AutoWind.SetNBCC2005("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
0.75, 2.1, 1.1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetNBCC2005

# SetNBCC95

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetNBCC95

## VB6 Procedure

Function SetNBCC95(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle
As Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal
TopZ As Double, ByVal BottomZ As Double, ByVal q As Double, ByVal GustFactor As Double,
Optional ByVal UserExposure As Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw


The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

q

The velocity pressure in kPa.

GustFactor

The gust effect factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for NBCC 95.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindNBCC95()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application


SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign NBCC95 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNBCC95("WIND", 1, 0, 0.8, 0.5, False, 0, 0,
0.75, 2.1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetNBCC95

# SetNTC2008_1


## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetNTC2008_1

## VB6 Procedure

Function SetNTC2008_1(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean,
ByRef TopZ As Double, ByRef BottomZ As Double, ByRef vr As Double, ByRef
ExposureCategory As Long, ByRef ct As Double, ByRef cd As Double, ByRef UserExposure As
Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

vr


The wind velocity in m/s.

ExposureCategory

This is 1, 2, 3, 4, or 5, indicating the exposure category.

```
1 = I
2 = II
3 = III
4 = IV
5 = V
```
ct

The topography factor, ct.

cd

The dynamic coefficient, cd.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NTC 2008.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetWindNTC2008()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template


ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", eLoadPatternType_WIND)

'assign NTC2008 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNTC2008_1("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 35, 3,
1, 1, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.2.0.

This function supersedes SetNTC2008.

## See Also

GetNTC2008_1

# SetNTC2018_1

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetNTC2018_1

## VB6 Procedure


Function SetNTC2018_1(ByVal Name As String, ByRef ExposureFrom As Long, ByRef
DirAngle As Double, ByRef Cpw As Double, ByRef Cpl As Double, ByRef UserZ As Boolean,
ByRef TopZ As Double, ByRef BottomZ As Double, ByRef vr As Double, ByRef
ExposureCategory As Long, ByRef ct As Double, ByRef cd As Double, ByRef UserExposure As
Boolean = False) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cp. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cp. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

vr

The wind velocity in m/s.

ExposureCategory

This is 1, 2, 3, 4, or 5, indicating the exposure category.

```
1 = I
```

### 2 = II

### 3 = III

### 4 = IV

### 5 = V

ct

The topography factor, ct.

cd

The dynamic coefficient, cd.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function retrieves auto wind loading parameters for NTC 2018.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetWindNTC2018()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)


'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", eLoadPatternType_WIND)

'assign NTC2018 parameters
ret = SapModel.LoadPatterns.AutoWind.SetNTC2018_1("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 35, 3,
1, 1, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.2.0.

This function supersedes SetNTC2018.

## See Also

GetNTC2018_1

# SetSP20133302016

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetSP20133302016

## VB6 Procedure

Function SetSP20133302016 (ByVal Name As String, ByVal LoadingType As Long, ByVal
ExposureFrom As Long, ByVal DirAngle As Double, ByVal Cp As Double, ByVal UserZ As
Boolean, ByVal TopZ As Double, ByVal BottomZ As Double, ByVal StructureType As Integer,
ByVal LogDecrement As Integer, ByVal BuildingWidth As Double, ByVal BuildingDepth As
Double, ByVal Zeq As Double, ByVal WindDistrict As Long, ByVal WindPressure As Double,
ByVal TerrainType As Long, ByVal LimitFreq As Double, ByVal ModalCase As String, ByVal
FirstValMode As Long, Optional ByVal UserExposure As Boolean = False) As Long


## Parameters

Name

The name of an existing Wind-type load pattern with a SP 20.13330.2016 auto wind assignment.

LoadingType

This indicates whether the loads should be calculated as static or dynamic.

```
1 = Static
2 = Dynamic
```
ExposureFrom

This is 1 or 2, indicating the source of the wind exposure. This item applies only when
LoadingType = 1.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item does not apply when ExposureFrom = 2.

Cp

The wind coefficient, Cp. This item applies only when LoadingType = 1 and ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

StructureType

This indicates the structure type for calculating the wind pressure.

```
1 = Building
2 = Other
```
LogDecrement

This specifies a value for the logarithmic decrement. This item applies only when LoadingType =
2.


### 1 = 0.15

### 2 = 0.30

BuildingWidth

This is the building width, normal to the wind direction. [L]

BuildingDepth

This is the building depth, in the direction of the wind. This item applies only when LoadingType
= 2. [L]

Zeq

This is the equivalent height, Zeq, of the structure. This item applies only when LoadingType = 2.
[L]

WindDistrict

This is the wind district to consider.

```
0 = Ia
1 = I
2 = II
3 = III
4 = IV
5 = V
6 = VI
7 = VII
8 = User Defined
```
WindPressure

This is the wind pressure. This item applies only when WindDistrict = 8. [F/L^2 ]

TerrainType

This is the terrain type being considered.

```
1 = A
2 = B
3 = C
```
LimitFreq

The limit frequency. This item applies only when LoadingType = 2 and WindDistrict = 8.

ModalCase

The name of an existing modal load case to be used in determining dynamic wind loads. This item
applies only when LoadingType = 2.

FirstValMode


The first valuable mode number from the specified modal case. This item applies only when
LoadingType = 2.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms. This item
applies only when LoadingType = 1.

## Remarks

This function assigns auto wind loading parameters for SP 20.13330.2016.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetWindSP20133302016()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection

ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection


ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign SP 20.13330.2016 parameters
ret = SapModel.LoadPatterns.AutoWind.SetSP20133302016("WIND", 1, 1, 0, 0.8, False, 0,
0, 1, 1, 10, 10, 10, 3, 0.1, 2, 10, “MODAL”, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

GetSP20133302016

# SetUBC94

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetUBC94

## VB6 Procedure

Function SetUBC94(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle As
Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal TopZ
As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal ExposureType As
Long, ByVal ImportanceFactor As Double, Optional ByVal UserExposure As Boolean = False)
As Long

## Parameters

Name


The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cq. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cq. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]

BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
ImportanceFactor

The importance factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.


## Remarks

This function assigns auto wind loading parameters for 1994 UBC.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindUBC94()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign UBC94 parameters
ret = SapModel.LoadPatterns.AutoWind.SetUBC94("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80, 3,
1.15)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetUBC94

# SetNone

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetNone

## VB6 Procedure

Function SetNone(ByVal Name As String) As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

## Remarks

This function set the auto wind loading type for the specified load pattern to None.

The function returns zero if the loading type is successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindNone()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign ASCE788 parameters
ret = SapModel.LoadPatterns.AutoWind.SetASCE788("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80,
3, 1, 0.85)

'set auto wind loading type to None
ret = SapModel.LoadPatterns.AutoWind.SetNone("WIND")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

# SetUBC97

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetUBC97

## VB6 Procedure

Function SetUBC97(ByVal Name As String, ByVal ExposureFrom As Long, ByVal DirAngle As
Double, ByVal Cpw As Double, ByVal Cpl As Double, ByVal UserZ As Boolean, ByVal TopZ
As Double, ByVal BottomZ As Double, ByVal WindSpeed As Double, ByVal ExposureType As
Long, ByVal ImportanceFactor As Double, Optional ByVal UserExposure As Boolean = False)
As Long

## Parameters

Name

The name of an existing Wind-type load pattern.

ExposureFrom

This is either 1 or 2, indicating the source of the wind exposure.

```
1 = From extents of rigid diaphragms
2 = From area objects
```
DirAngle

The direction angle for the wind load. This item applies only when ExposureFrom = 1.

Cpw

The windward coefficient, Cq. This item applies only when ExposureFrom = 1.

Cpl

The leeward coefficient, Cq. This item applies only when ExposureFrom = 1.

UserZ

This item is True if the top and bottom elevations of the wind load are user specified. It is False if
the elevations are determined by the program.

TopZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the highest
level where auto wind loads are applied. [L]


BottomZ

This item applies only when the UserZ item is True. It is the global Z-coordinate at the lowest
level where auto wind loads are applied. [L]

WindSpeed

The wind speed in miles per hour.

ExposureType

This is 1, 2 or 3, indicating the exposure category.

```
1 = B
2 = C
3 = D
```
ImportanceFactor

The importance factor.

UserExposure

If this item is True, the wind exposure widths are provided by the user. If it is False, the wind
exposure widths are calculated by the program from the extents of the diaphragms.

## Remarks

This function assigns auto wind loading parameters for 1997 UBC.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindUBC97()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel


'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign UBC97 parameters
ret = SapModel.LoadPatterns.AutoWind.SetUBC97("WIND", 1, 0, 0.8, 0.5, False, 0, 0, 80, 3,
1.15)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetUBC97

# SetUserLoad

## Syntax

SapObject.SapModel.LoadPatterns.AutoWind.SetUserLoad

## VB6 Procedure


Function SetUserLoad(ByVal Name As String, ByVal Diaph As String, ByVal Fx As Double,
ByVal Fy As Double, ByVal Mz As Double, ByVal x As Double, ByVal y As Double) As Long

## Parameters

Name

The name of an existing Wind-type load pattern that has an auto wind load assigned.

Diaph

The name of an existing special rigid diaphragm constraint, that is, a diaphragm constraint with
the following features:

1. The constraint type is CONSTRAINT_DIAPHRAGM = 2.
2. The constraint coordinate system is Global.
3. The constraint axis is Z.

Fx

The global X direction force assigned to the specified diaphragm. [F]

Fy

The global Y direction force assigned to the specified diaphragm. [F]

Mz

The moment about the global Z axis assigned to the specified diaphragm. [FL]

x

The global X-coordinate of the point where the wind force is applied. [L]

y

The global Y-coordinate of the point where the wind force is applied. [L]

## Remarks

This function assigns auto wind loading parameters for User-type wind loads.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignWindUserLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("2")
ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.SelectObj.PlaneXY("3")
ret = SapModel.PointObj.SetConstraint("", "Diaph2", SelectedObjects)
ret = SapModel.SelectObj.ClearSelection

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'assign user wind load parameters
ret = SapModel.LoadPatterns.AutoWind.SetUserLoad("WIND", "Diaph1", 100, 20, 5000, 0,
0)
ret = SapModel.LoadPatterns.AutoWind.SetUserLoad("WIND", "Diaph2", 50, 10, 2500, 0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also


GetUserLoad

GetSpecialRigidDiaphragmList

# GetAuto

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeastate.GetAuto

## VB6 Procedure

Function GetAuto(ByVal Name As String, ByRef LoadMethod As Long, ByRef CSys As String,
ByRef AdjustGravityLat As Boolean, ByRef AdjustGravityLatFactor As Double, ByRef
AdjustGravityVert As Boolean, ByRef AdjustGravityVertFactor As Double, ByRef
CenterRotation() As Double, ByRef Parameters() As Double, ByRef IgnorePhase As Boolean) As
Long

## Parameters

Name

The name of an existing seastate-type load pattern.

LoadMethod

This is one of the following three options defining what parameters are being specified.

```
1 = Rotation / Translations Vertical Input
```
```
2 = Rotations / Translations Full Input
```
```
3 = Accelerations / Velocities
```
CSys

The coordinate system used as a reference for specifying the center of rotation location and the
inertia load parameters.

AdjustGravityLat

This item only applies when using LoadMethod 1 or 2. It is True if generated lateral loads should
include the effects of the rotated structure, otherwise it is False.

AdjustGravityLatFactor

This item only applies when using LoadMethod 1 or 2. This is a scale factor on the lateral effects
generated as a result of the rotated structure.

AdjustGravityVert


This item only applies when using LoadMethod 1 or 2. It is True if generated vertical loads should
include the effects of the rotated structure, otherwise it is False.

AdjustGravityVertFactor

This item only applies when using LoadMethod 1 or 2. This is a scale factor on the vertical effects
generated as a result of the rotated structure.

CenterRotation

This is an array dimensioned to 2 (3 doubles) that defines the coordinates of the center of rotation,
with respect to the selected coordinate system.

Parameters

This is an array of the inertia load parameters, based on the specified LoadMethod, as described
below.

If LoadMethod = 1, the following 9 parameters should be input:

```
Parameters(0) - UZ amplitude
```
```
Parameters(1) - UZ period
```
```
Parameters(2) - UZ phase
```
```
Parameters(3) - RX amplitude
```
```
Parameters(4) - RX period
```
```
Parameters(5) - RX phase
```
```
Parameters(6) - RY amplitude
```
```
Parameters(7) - RY period
```
```
Parameters(8) - RY phase
```
If the LoadMethod = 2, the following 18 parameters should be input:

```
Parameters(0) - UX amplitude
```
```
Parameters(1) - UX period
```
```
Parameters(2) - UX phase
```
```
Parameters(3) - UY amplitude
```
```
Parameters(4) - UY period
```
```
Parameters(5) - UY phase
```
```
Parameters(6) - UZ amplitude
```
```
Parameters(7) - UZ period
```

```
Parameters(8) - UZ phase
```
```
Parameters(9) - RX amplitude
```
```
Parameters(10) - RX period
```
```
Parameters(11) - RX phase
```
```
Parameters(12) - RY amplitude
```
```
Parameters(13) - RY period
```
```
Parameters(14) - RY phase
```
```
Parameters(15) - RZ amplitude
```
```
Parameters(16) - RZ period
```
```
Parameters(17) - RZ phase
```
If the LoadMethod = 3, the following 9 parameters should be input:

```
Parameters(0) - Acceleration UX
```
```
Parameters(1) - Acceleration UY
```
```
Parameters(2) - Acceleration UZ
```
```
Parameters(3) - Acceleration RX
```
```
Parameters(4) - Acceleration RY
```
```
Parameters(5) - Acceleration RZ
```
```
Parameters(6) - Velocity RX
```
```
Parameters(7) - Velocity RY
```
```
Parameters(8) - Velocity RZ
```
IgnorePhase

This item only applies when using LoadMethod 1 or 2. It is True if the input phases should be
ignored, otherwise it is False.

## Remarks

This function retrieves auto seastate loading parameters.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example


Sub GetAutoSeastate()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim MyCenter(2) As Double

Dim MyParams(8) As Double

Dim LoadMethod As Long

Dim CSys As String

Dim AdjustGravityLat As Boolean

Dim LatScaleFactor As Double

Dim AdjustGravityVert As Boolean

Dim VertScaleFactor As Double

Dim Center() As Double

Dim Params() As Double

Dim IgnorePhase As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints

ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)

ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'add new load pattern
ret = SapModel.LoadPatterns.Add("SEASTATE", LTYPE_SEASTATE)


'assign seastate parameters

MyCenter(0) = 0

MyCenter(1) = 0

MyCenter(2) = 0

MyParams(0) = 0

MyParams(1) = 0

MyParams(2) = 0

MyParams(3) = 0.5

MyParams(4) = 0

MyParams(5) = 0

MyParams(6) = 0

MyParams(7) = 0

MyParams(8) = 0

ret = SapModel.LoadPatterns.AutoSeastate.SetAuto("SEASTATE", 3, "Global", True, 1, True,
1, MyCenter, MyParms, False)

'get seastate parameters

ret = SapModel.LoadPatterns.AutoSeastate.GetAuto("SEASTATE", LoadMethod, CSys,
AdjustGravityLat, LatScaleFactor, AdjustGravityVert, VertScaleFactor, Center, Params,
IgnorePhase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

## See Also

SetAuto


# SetAuto

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeastate.SetAuto

## VB6 Procedure

Function SetAuto(ByVal Name As String, ByVal LoadMethod As Long, ByVal CSys As String,
ByVal AdjustGravityLat As Boolean, ByVal AdjustGravityLatFactor As Double, ByVal
AdjustGravityVert As Boolean, ByVal AdjustGravityVertFactor As Double, ByVal
CenterRotation() As Double, ByVal Parameters() As Double, ByVal IgnorePhase As Boolean) As
Long

## Parameters

Name

The name of an existing seastate-type load pattern.

LoadMethod

This is one of the following three options defining what parameters are being specified.

```
1 = Rotation / Translations Vertical Input
```
```
2 = Rotations / Translations Full Input
```
```
3 = Accelerations / Velocities
```
CSys

The coordinate system used as a reference for specifying the center of rotation location and the
inertia load parameters.

AdjustGravityLat

This item only applies when using LoadMethod 1 or 2. It is True if generated lateral loads should
include the effects of the rotated structure, otherwise it is False.

AdjustGravityLatFactor

This item only applies when using LoadMethod 1 or 2. This is a scale factor on the lateral effects
generated as a result of the rotated structure.

AdjustGravityVert

This item only applies when using LoadMethod 1 or 2. It is True if generated vertical loads should
include the effects of the rotated structure, otherwise it is False.

AdjustGravityVertFactor


This item only applies when using LoadMethod 1 or 2. This is a scale factor on the vertical effects
generated as a result of the rotated structure.

CenterRotation

This is an array dimensioned to 2 (3 doubles) that defines the coordinates of the center of rotation,
with respect to the selected coordinate system.

Parameters

This is an array of the inertia load parameters, based on the specified LoadMethod, as described
below.

If LoadMethod = 1, the following 9 parameters should be input:

```
Parameters(0) - UZ amplitude
```
```
Parameters(1) - UZ period
```
```
Parameters(2) - UZ phase
```
```
Parameters(3) - RX amplitude
```
```
Parameters(4) - RX period
```
```
Parameters(5) - RX phase
```
```
Parameters(6) - RY amplitude
```
```
Parameters(7) - RY period
```
```
Parameters(8) - RY phase
```
If the LoadMethod = 2, the following 18 parameters should be input:

```
Parameters(0) - UX amplitude
```
```
Parameters(1) - UX period
```
```
Parameters(2) - UX phase
```
```
Parameters(3) - UY amplitude
```
```
Parameters(4) - UY period
```
```
Parameters(5) - UY phase
```
```
Parameters(6) - UZ amplitude
```
```
Parameters(7) - UZ period
```
```
Parameters(8) - UZ phase
```
```
Parameters(9) - RX amplitude
```
```
Parameters(10) - RX period
```

```
Parameters(11) - RX phase
```
```
Parameters(12) - RY amplitude
```
```
Parameters(13) - RY period
```
```
Parameters(14) - RY phase
```
```
Parameters(15) - RZ amplitude
```
```
Parameters(16) - RZ period
```
```
Parameters(17) - RZ phase
```
If the LoadMethod = 3, the following 9 parameters should be input:

```
Parameters(0) - Acceleration UX
```
```
Parameters(1) - Acceleration UY
```
```
Parameters(2) - Acceleration UZ
```
```
Parameters(3) - Acceleration RX
```
```
Parameters(4) - Acceleration RY
```
```
Parameters(5) - Acceleration RZ
```
```
Parameters(6) - Velocity RX
```
```
Parameters(7) - Velocity RY
```
```
Parameters(8) - Velocity RZ
```
IgnorePhase

This item only applies when using LoadMethod 1 or 2. It is True if the input phases should be
ignored, otherwise it is False.

## Remarks

This function retrieves auto seastate loading parameters.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub SetAutoSeastate()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim MyCenter(2) As Double

Dim MyParams(8) As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints

ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)

ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'add new load pattern
ret = SapModel.LoadPatterns.Add("SEASTATE", LTYPE_SEASTATE)

'assign seastate parameters

MyCenter(0) = 0

MyCenter(1) = 0

MyCenter(2) = 0

MyParams(0) = 0

MyParams(1) = 0

MyParams(2) = 0

MyParams(3) = 0.5

MyParams(4) = 0

MyParams(5) = 0

MyParams(6) = 0


MyParams(7) = 0

MyParams(8) = 0

ret = SapModel.LoadPatterns.AutoSeastate.SetAuto("SEASTATE", 3, "Global", True, 1, True,
1, MyCenter, MyParms, False)

'get seastate parameters

ret = SapModel.LoadPatterns.AutoSeastate.GetAuto("SEASTATE", LoadMethod, CSys,
AdjustGravity, Center, Params)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

## See Also

GetAuto

# SetNone

## Syntax

SapObject.SapModel.LoadPatterns.AutoSeastate.SetNone

## VB6 Procedure

Function SetNone(ByVal Name As String) As Long

## Parameters

Name

The name of an existing seastate-type load pattern.

## Remarks

This function sets the auto seastate loading type for the specified load pattern to None.


The function returns zero if the loading type is successfully assigned; otherwise it returns a
nonzero vale.

## VBA Example

Sub AssignSeastateNone()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim MyCenter(2) As Double

Dim MyParams(8) As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints

ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)

ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2", Z)

'assign points to diaphragm

ret = SaModel.SelectObj.ClearSelection

ret = SapModel.SelectObj.PlaneXY("2)

ret = SapModel.PointObj.SetConstraint("", "Diaph1", SelectedObjects)

ret = SapModel.SelectObj.ClearsSelection

ret = SapModel.SelectObj.PlaneXY("3")

ret = SapModel.PointObject.SetConstraint("", Diaph2", SelectedObjects)

ret = SapModel.SelectObj.ClearSelection


'add new load pattern
ret = SapModel.LoadPatterns.Add("SEASTATE", LTYPE_SEASTATE)

'assign seastate parameters

MyCenter(0) = 0

MyCenter(1) = 0

MyCenter(2) = 0

MyParams(0) = 0

MyParams(1) = 0

MyParams(2) = 0

MyParams(3) = 0.5

MyParams(4) = 0

MyParams(5) = 0

MyParams(6) = 0

MyParams(7) = 0

MyParams(8) = 0

ret = SapModel.LoadPatterns.AutoSeastate.SetAuto("SEASTATE", 3, "Global", True,
MyCenter, MyParms)

'set auto seastate loading type to None

ret = SapModel.LoadPatterns.AutoSWind.SetNone("SEASTATE")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

## See Also


# Add

## Syntax

SapObject.SapModel.LoadPatterns.Add

## VB6 Procedure

Function Add(ByVal Name As String, ByVal MyType As eLoadPatternType, Optional ByVal
SelfWTMultiplier As Double = 0, Optional ByVal AddLoadCase As Boolean = True) As Long

## Parameters

Name

The name for the new load pattern.

MyType

This is one of the following items in the eLoadPatternType enumeration:

```
LTYPE_DEAD = 1
LTYPE_SUPERDEAD = 2
LTYPE_LIVE = 3
LTYPE_REDUCELIVE = 4
LTYPE_QUAKE = 5
LTYPE_WIND= 6
LTYPE_SNOW = 7
LTYPE_OTHER = 8
LTYPE_MOVE = 9
LTYPE_TEMPERATURE = 10
LTYPE_ROOFLIVE = 11
LTYPE_NOTIONAL = 12
LTYPE_PATTERNLIVE = 13
LTYPE_WAVE= 14
LTYPE_BRAKING = 15
LTYPE_CENTRIFUGAL = 16
LTYPE_FRICTION = 17
LTYPE_ICE = 18
LTYPE_WINDONLIVELOAD = 19
LTYPE_HORIZONTALEARTHPRESSURE = 20
LTYPE_VERTICALEARTHPRESSURE = 21
LTYPE_EARTHSURCHARGE = 22
LTYPE_DOWNDRAG = 23
LTYPE_VEHICLECOLLISION = 24
LTYPE_VESSELCOLLISION = 25
LTYPE_TEMPERATUREGRADIENT = 26
LTYPE_SETTLEMENT = 27
LTYPE_SHRINKAGE = 28
LTYPE_CREEP = 29
```

### LTYPE_WATERLOADPRESSURE = 30

### LTYPE_LIVELOADSURCHARGE = 31

### LTYPE_LOCKEDINFORCES = 32

### LTYPE_PEDESTRIANLL = 33

### LTYPE_PRESTRESS = 34

### LTYPE_HYPERSTATIC = 35

### LTYPE_BOUYANCY = 36

### LTYPE_STREAMFLOW = 37

### LTYPE_IMPACT = 38

### LTYPE_CONSTRUCTION = 39

SelfWTMultiplier

The self weight multiplier for the new load pattern.

AddLoadCase

If this item is True, a linear static load case corresponding to the new load pattern is added.

## Remarks

This function adds a new load pattern.

The function returns 0 if the load pattern is successfully added; otherwise it returns nonzero. An
error is returned if the Name item is already used for an existing load pattern.

## VBA Example

Sub AddNewLoadPattern()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberAreas As Long
Dim AreaName() As String

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add new load pattern


ret = SapModel.LoadPatterns.Add("LIVE", LTYPE_LIVE)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Added three items to the eLoadPatternType enumeration in version 12.00.

## See Also

# ChangeName

## Syntax

SapObject.SapModel.LoadPatterns.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The name of a defined load pattern.

NewName

The new name for the load pattern.

## Remarks

This function applies a new name to a load pattern.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example


Sub ChangeLoadPatternName()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'change name
ret = SapModel.LoadPatterns.ChangeName("DEAD", "DL")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# Count

## Syntax

SapObject.SapModel.LoadPatterns.Count

## VB6 Procedure

Function Count() As Long


## Parameters

None

## Remarks

The function returns the number of defined load patterns.

## VBA Example

Sub CountLoadPatterns()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'get number of defined load patterns
ret = SapModel.LoadPatterns.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also


# Delete

## Syntax

SapObject.SapModel.LoadPatterns.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing load pattern.

## Remarks

The function deletes the specified load pattern.

The function returns zero if the load pattern is successfully deleted, otherwise it returns a nonzero
value.

The load pattern is not deleted and the function returns an error if the load pattern is assigned to an
load case or if it is the only defined load pattern.

## VBA Example

Sub DeleteLoadPattern()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)


'delete load case
'Note: ret in the above line returns 1, indicating an error.
'This is the case because the load pattern DEAD is assigned to
'load case DEAD. This is also the case because the load
'case DEAD is the only load pattern defined.
ret = SapModel.LoadPatterns.Delete("DEAD")

'Note: ret in the above line returns 1, indicating an error. This is the case because the load
pattern DEAD is assigned to load case DEAD. This is also the case because the load pattern
DEAD is the only load pattern defined.

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# GetAutoSeismicCode

## Syntax

SapObject.SapModel.LoadPatterns.GetAutoSeismicCode

## VB6 Procedure

Function GetAutoSeismicCode(ByVal Name As String, ByRef CodeName As String) As Long

## Parameters

Name

The name of an existing Quake-type load pattern.

CodeName

This is either blank or the name code used for the auto seismic parameters. Blank means no auto
seismic load is specified for the Quake-type load pattern.


## Remarks

This function retrieves the code name used for auto seismic parameters in Quake-type load
patterns.

The function returns zero if the code is successfully retrieved; otherwise it returns a nonzero value.
An error is returned if the specified load pattern is not a Quake-type load pattern.

## VBA Example

Sub GetAutoSeismicType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim CodeName As String

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add new load pattern
ret = SapModel.LoadPatterns.Add("EQX", LTYPE_QUAKE)

'assign BOCA96 parameters
ret = SapModel.LoadPatterns.AutoSeismic.SetBOCA96("EQX", 1, 0.05, 1, 0.035, 0, False, 0,
0, 0.4, 0.4, 1.5, 8)

'get auto seismic code
ret = SapModel.LoadPatterns.GetAutoSeismicCode("EQX", CodeName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetAutoWindCode

GetAutoWaveCode

# GetAutoWaveCode

## Syntax

SapObject.SapModel.LoadPatterns.GetAutoWaveCode

## VB6 Procedure

Function GetAutoWaveCode(ByVal Name As String, ByRef CodeName As String) As Long

## Parameters

Name

The name of an existing Wave-type load pattern.

CodeName

This is either blank or the name code used for the auto wave parameters. Blank means no auto
wave load is specified for the Wave-type load pattern.

## Remarks

This function retrieves the code name used for auto wave parameters in Wave-type load patterns.

The function returns zero if the code is successfully retrieved; otherwise it returns a nonzero value.
An error is returned if the specified load pattern is not a Wave-type load pattern.

## VBA Example

Sub GetAutoWaveType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim CodeName As String

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add new load pattern
ret = SapModel.LoadPatterns.Add("WAVE", LTYPE_WAVE)

'get auto wave code
ret = SapModel.LoadPatterns.GetAutoWaveCode("WAVE", CodeName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetAutoSeismicCode

GetAutoWindCode

# GetAutoWindCode

## Syntax

SapObject.SapModel.LoadPatterns.GetAutoWindCode

## VB6 Procedure

Function GetAutoWindCode(ByVal Name As String, ByRef CodeName As String) As Long


## Parameters

Name

The name of an existing Wind-type load pattern.

CodeName

This is either blank or the name code used for the auto wind parameters. Blank means no auto
wind load is specified for the Wind-type load pattern.

## Remarks

This function retrieves the code name used for auto wind parameters in Wind-type load patterns.

The function returns zero if the code is successfully retrieved; otherwise it returns a nonzero value.
An error is returned if the specified load pattern is not a Wind-type load pattern.

## VBA Example

Sub GetAutoWindType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim CodeName As String

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add new load pattern
ret = SapModel.LoadPatterns.Add("WIND", LTYPE_WIND)

'get auto wind code
ret = SapModel.LoadPatterns.GetAutoWindCode("WIND", CodeName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetAutoSeismicCode

GetAutoWaveCode

# GetLoadType

## Syntax

SapObject.SapModel.LoadPatterns.GetLoadType

## VB6 Procedure

Function GetLoadType(ByVal Name As String, ByRef MyType As eLoadPatternType) As Long

## Parameters

Name

The name of an existing load pattern.

MyType

This is one of the following items in the eLoadPatternType enumeration:

```
LTYPE_DEAD = 1
LTYPE_SUPERDEAD = 2
LTYPE_LIVE = 3
LTYPE_REDUCELIVE = 4
LTYPE_QUAKE = 5
LTYPE_WIND= 6
LTYPE_SNOW = 7
LTYPE_OTHER = 8
LTYPE_MOVE = 9
LTYPE_TEMPERATURE = 10
LTYPE_ROOFLIVE = 11
LTYPE_NOTIONAL = 12
LTYPE_PATTERNLIVE = 13
```

### LTYPE_WAVE= 14

### LTYPE_BRAKING = 15

### LTYPE_CENTRIFUGAL = 16

### LTYPE_FRICTION = 17

### LTYPE_ICE = 18

### LTYPE_WINDONLIVELOAD = 19

### LTYPE_HORIZONTALEARTHPRESSURE = 20

### LTYPE_VERTICALEARTHPRESSURE = 21

### LTYPE_EARTHSURCHARGE = 22

### LTYPE_DOWNDRAG = 23

### LTYPE_VEHICLECOLLISION = 24

### LTYPE_VESSELCOLLISION = 25

### LTYPE_TEMPERATUREGRADIENT = 26

### LTYPE_SETTLEMENT = 27

### LTYPE_SHRINKAGE = 28

### LTYPE_CREEP = 29

### LTYPE_WATERLOADPRESSURE = 30

### LTYPE_LIVELOADSURCHARGE = 31

### LTYPE_LOCKEDINFORCES = 32

### LTYPE_PEDESTRIANLL = 33

### LTYPE_PRESTRESS = 34

### LTYPE_HYPERSTATIC = 35

### LTYPE_BOUYANCY = 36

### LTYPE_STREAMFLOW = 37

### LTYPE_IMPACT = 38

### LTYPE_CONSTRUCTION = 39

## Remarks

This function retrieves the load type for a specified load pattern.

The function returns zero if the load type is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetLoadPatternType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyType As eLoadPatternType

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel


'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'get load pattern type
ret = SapModel.LoadPatterns.GetLoadType("DEAD", MyType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Added three items to the eLoadPatternType enumeration in version 12.00.

## See Also

SetLoadType

# GetNameList

## Syntax

SapObject.SapModel.LoadPatterns.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of load pattern names retrieved by the program.

MyName

This is a one-dimensional array of load pattern names. The MyName array is created as a
dynamic, zero-based, array by the API user:


Dim MyName() as String

The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined load cases.

The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetLoadPatternNames()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberNames As Long
Dim MyName() As String

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'get load pattern names
ret = SapModel.LoadPatterns.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# GetSelfWtMultiplier

## Syntax

SapObject.SapModel.LoadPatterns.GetSelfWtMultiplier

## VB6 Procedure

Function GetSelfWtMultiplier(ByVal Name As String, ByRef SelfWTMultiplier As Double) As
Long

## Parameters

Name

The name of an existing load pattern.

SelfWTMultiplier

The self weight multiplier for the specified load pattern.

## Remarks

This function retrieves the self weight multiplier for a specified load pattern.

The function returns zero if the multiplier is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetSelfWeightMultiplier()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim SelfWTMultiplier As Double

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart


'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'get self weight multiplier
ret = SapModel.LoadPatterns.GetSelfWtMultiplier("DEAD", SelfWTMultiplier)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetSelfWtMultiplier

# SetLoadType

## Syntax

SapObject.SapModel.LoadPatterns.SetLoadType

## VB6 Procedure

Function SetLoadType(ByVal Name As String, ByVal MyType As eLoadPatternType) As Long

## Parameters

Name

The name of an existing load pattern.

MyType

This is one of the following items in the eLoadPatternType enumeration:


### LTYPE_DEAD = 1

### LTYPE_SUPERDEAD = 2

### LTYPE_LIVE = 3

### LTYPE_REDUCELIVE = 4

### LTYPE_QUAKE = 5

### LTYPE_WIND= 6

### LTYPE_SNOW = 7

### LTYPE_OTHER = 8

### LTYPE_MOVE = 9

### LTYPE_TEMPERATURE = 10

### LTYPE_ROOFLIVE = 11

### LTYPE_NOTIONAL = 12

### LTYPE_PATTERNLIVE = 13

### LTYPE_WAVE= 14

### LTYPE_BRAKING = 15

### LTYPE_CENTRIFUGAL = 16

### LTYPE_FRICTION = 17

### LTYPE_ICE = 18

### LTYPE_WINDONLIVELOAD = 19

### LTYPE_HORIZONTALEARTHPRESSURE = 20

### LTYPE_VERTICALEARTHPRESSURE = 21

### LTYPE_EARTHSURCHARGE = 22

### LTYPE_DOWNDRAG = 23

### LTYPE_VEHICLECOLLISION = 24

### LTYPE_VESSELCOLLISION = 25

### LTYPE_TEMPERATUREGRADIENT = 26

### LTYPE_SETTLEMENT = 27

### LTYPE_SHRINKAGE = 28

### LTYPE_CREEP = 29

### LTYPE_WATERLOADPRESSURE = 30

### LTYPE_LIVELOADSURCHARGE = 31

### LTYPE_LOCKEDINFORCES = 32

### LTYPE_PEDESTRIANLL = 33

### LTYPE_PRESTRESS = 34

### LTYPE_HYPERSTATIC = 35

### LTYPE_BOUYANCY = 36

### LTYPE_STREAMFLOW = 37

### LTYPE_IMPACT = 38

### LTYPE_CONSTRUCTION = 39

## Remarks

This function assigns a load type to a load pattern.

The function returns zero if the load type is successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub AssignLoadType()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'assign load type
ret = SapModel.LoadPatterns.SetLoadType("DEAD", LTYPE_SUPERDEAD)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Added three items to the eLoadPatternType enumeration in version 12.00.

## See Also

GetLoadType

# SetSelfWtMultiplier

## Syntax

SapObject.SapModel.LoadPatterns.SetSelfWtMultiplier

## VB6 Procedure


Function SetSelfWtMultiplier(ByVal Name As String, ByVal SelfWTMultiplier As Double) As
Long

## Parameters

Name

The name of an existing load pattern.

SelfWTMultiplier

The self weight multiplier for the specified load pattern.

## Remarks

This function assigns a self weight multiplier to a load case.

The function returns zero if the multiplier is successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub AssignSelfWeightMultiplier()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

'create Sap2000 object
Set SapObject = New Sap2000v16.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'assign self weight multiplier
ret = SapModel.LoadPatterns.SetSelfWtMultiplier("DEAD", 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetSelfWtMultiplier


