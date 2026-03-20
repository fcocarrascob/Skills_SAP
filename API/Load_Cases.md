# ChangeName

## Syntax

SapObject.SapModel.LoadCases.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined load case.

NewName

The new name for the load case.

## Remarks

This function changes the name of an existing load case.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeLoadCaseName()
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

'change load case name
ret = SapModel.LoadCases.ChangeName("DEAD", "DL")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# Count

## Syntax

SapObject.SapModel.LoadCases.Count

## VB6 Procedure

Function Count(Optional ByVal CaseType As eLoadCaseType) As Long

## Parameters

```
CaseType
```
This optional value is one of the following items in the eLoadCaseType enumeration.

```
CASE_LINEAR_STATIC = 1
```
```
CASE_NONLINEAR_STATIC = 2
```
```
CASE_MODAL = 3
```
```
CASE_RESPONSE_SPECTRUM = 4
```
```
CASE_LINEAR_HISTORY = 5 (Modal Time History)
```
```
CASE_NONLINEAR_HISTORY = 6 (Modal Time History)
```
```
CASE_LINEAR_DYNAMIC = 7 (Direct Integration Time History)
```

```
CASE_NONLINEAR_DYNAMIC = 8 (Direct Integration Time History)
```
```
CASE_MOVING_LOAD = 9
```
```
CASE_BUCKLING = 10
```
```
CASE_STEADY_STATE = 11
```
```
CASE_POWER_SPECTRAL_DENSITY = 12
```
```
CASE_LINEAR_STATIC_MULTISTEP = 13
```
```
CASE_HYPERSTATIC = 14
```
If no value is input for CaseType, a count is returned for all load cases in the model regardless of
type.

**Remarks**

This function returns the total number of defined load cases in the model. If desired, counts can be
returned for all load cases of a specified type in the model.

**VBA Example**

Sub CountLoadCases()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Count As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'return number of load cases of all types
Count = SapModel.LoadCases.Count

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Added optional CaseType parameter in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Added one item to the eLoadCaseType enumeration in version 12.00.

## See Also

# Delete

## Syntax

SapObject.SapModel.LoadCases.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing load case.

## Remarks

The function deletes the specified load case.

The function returns zero if the load case is successfully deleted, otherwise it returns a nonzero
value.

## VBA Example

Sub DeleteLoadCase()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'delete load case
ret = SapModel.LoadCases.Delete("DEAD")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# GetNameList_

## Syntax

SapObject.SapModel.LoadCases.GetNameList_

## VB6 Procedure

Function GetNameList_1(ByRef NumberNames As Long, ByRef MyName() As String, Optional
ByVal CaseType As eLoadCaseType) As Long

## Parameters

**NumberNames**

The number of load case names retrieved by the program.


**MyName**

This is a one-dimensional array of load case names. The MyName array is created as a dynamic,
zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

**CaseType**

This optional value is one of the following items in the eLoadCaseType enumeration.

```
Linear Static = 1
```
```
Nonlinear_Static = 2
```
```
Modal = 3
```
```
Response_Spectrum = 4
```
```
Linear_History = 5 (Modal Time History)
```
```
Nonlinear_History = 6 (Modal Time History)
```
```
Linear_Dynamic = 7 (Direct Integration Time History)
```
```
Nonlinear_Dynamic = 8 (Direct Integration Time History)
```
```
Moving_Load = 9
```
```
Buckling = 10
```
```
Steady_State = 11
```
```
Power_Spectral_Density = 12
```
```
Linear_Static_Multistep = 13
```
```
Hyperstatic = 14
```
```
External_Results = 15
```
```
StagedConstruction = 16
```
```
NonlinearStaticMultiStep = 17
```
If no value is input for CaseType, names are returned for all load cases in the model regardless of
type.

**Remarks**

This function retrieves the names of all defined load cases of the specified type.


The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetLoadCaseNames()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberNames As Long
Dim MyName() As String

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

'get load case names
ret = SapModel.LoadCases.GetNameList_1(NumberNames, MyName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

This function supersedes GetNameList {Load Case}.

## See Also

# GetTypeOAPI_

## Syntax

SapObject.SapModel.LoadCases.GetTypeOAPI_


**VB6 Procedure**

Function GetTypeOAPI_2(ByVal Name As String, ByRef CaseType As eLoadCaseType, ByRef
SubType As Long, ByRef DesignType As eLoadPatternType, ByRef DesignTypeOption As
Long, ByRef Auto As Long) As Long

**Parameters**

Name

The name of an existing load case.

CaseType

This is one of the following items in the eLoadCaseType enumeration.

```
LinearStatic = 1
```
```
NonlinearStatic = 2
```
```
Modal = 3
```
```
ResponseSpectrum = 4
```
```
LinearHistory = 5 (Modal Time History)
```
```
NonlinearHistory = 6 (Modal Time History)
```
```
LinearDynamic = 7 (Direct Integration Time History)
```
```
NonlinearDynamic = 8 (Direct Integration Time History)
```
```
MovingLoad = 9
```
```
Buckling = 10
```
```
SteadyState = 11
```
```
PowerSpectralDensity = 12
```
```
LinearStaticMultistep = 13
```
```
Hyperstatic = 14
```
```
ExternalResults = 15
```
```
StagedConstruction = 16
```
```
NonlinearStaticMultiStep = 17
```
SubType

This is an integer representing the load case sub type. This item applies only for certain case types.


## For CASE_MODAL:

```
1 = Eigen
2 = Ritz
```
For CASE_LINEAR_HISTORY:

```
1 = Transient
2 = Periodic
```
DesignType


```
DeadWearing = 40
DeadWater = 41
DeadManufacture = 42
EarthHydrostatic = 43
PassiveEarthPressure = 44
ActiveEarthPressure = 45
PedestrianLLReduced = 46
SnowHighAltitude = 47
EuroLm1Char = 48
EuroLm1Freq = 49
EuroLm2 = 50
EuroLm3 = 51
EuroLm4 = 52
```
DesignTypeOption

This is one of the following options for the DesignType item.

```
0 = Program determined
1 = User specified
```
Auto

This is one of the following values indicating if the load case has been automatically created.

```
0 = Not automatically created
1 = Automatically created by the bridge construction scheduler
```
**Remarks**

This function retrieves the case type, design type, and auto flag for the specified load case.

The function returns zero if the type is successfully retrieved; otherwise it returns nonzero.

This function supersedes. GetTypeOAPI_1 {LoadCase}.

**VBA Example**

Sub GetLoadCaseType_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim CaseType As eLoadCaseType
Dim SubType As Long
Dim DesignType As Long
Dim DesignTypeOption As Long
Dim Auto As Long

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

'get load case type
ret = SapModel.LoadCases.GetTypeOAPI_2("DEAD", CaseType, SubType, DesignType,
DesignTypeOption, Auto)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

This function supersedes GetTypeOAPI _1{Load Case}.

## See Also

# SetDesignType

## Syntax

SapObject.SapModel.LoadCases.SetDesignType

## VB6 Procedure

Function SetDesignType(ByVal Name As String, ByVal DesignTypeOption As Long, Optional
ByVal DesignType As eLoadPatternType = LTYPE_DEAD) As Long

## Parameters

Name

The name of an existing load case.

DesignTypeOption


## This is one of the following options for the DesignType item.

```
0 = Program determined
1 = User specified
```
DesignType

This item only applies when the DesignTypeOption is 1 (user specified). It is one of the following

**Remarks**

- Dead = This is one of the following items in the eLoadPatternType enumeration.
- SuperDead =
- Live =
- ReduceLive =
- Quake =
- Wind =
- Snow =
- Other =
- Move =
- Temperature =
- RoofLive =
- Notional =
- PatternLive =
- Wave=
- Braking =
- Centrifugal =
- Friction =
- Ice =
- WindOnLiveLoad =
- HorizontalEarthPressure =
- VerticalEarthPressure =
- EarthSurcharge =
- DownDrag =
- VehicleCollision =
- VesselCollision =
- TemperatureGradient =
- Settlement =
- Shrinkage =
- Creep =
- WaterLoadPressure =
- LiveLoadSurcharge =
- LockedInForces =
- PedestrianLL =
- Prestress =
- Hyperstatic =
- Bouyancy =
- StreamFlow =
- Impact =
- Construction =
- LTYPE_DEAD = items in the eLoadPatternType enumeration.
- LTYPE_SUPERDEAD =
- LTYPE_LIVE =
- LTYPE_REDUCELIVE =
- LTYPE_QUAKE =
- LTYPE_WIND=
- LTYPE_SNOW =
- LTYPE_OTHER =
- LTYPE_MOVE =
- LTYPE_TEMPERATURE =
- LTYPE_ROOFLIVE =
- LTYPE_NOTIONAL =
- LTYPE_PATTERNLIVE =
- LTYPE_WAVE=
- LTYPE_BRAKING =
- LTYPE_CENTRIFUGAL =
- LTYPE_FRICTION =
- LTYPE_ICE =
- LTYPE_WINDONLIVELOAD =
- LTYPE_HORIZONTALEARTHPRESSURE =
- LTYPE_VERTICALEARTHPRESSURE =
- LTYPE_EARTHSURCHARGE =
- LTYPE_DOWNDRAG =
- LTYPE_VEHICLECOLLISION =
- LTYPE_VESSELCOLLISION =
- LTYPE_TEMPERATUREGRADIENT =
- LTYPE_SETTLEMENT =
- LTYPE_SHRINKAGE =
- LTYPE_CREEP =
- LTYPE_WATERLOADPRESSURE =
- LTYPE_LIVELOADSURCHARGE =
- LTYPE_LOCKEDINFORCES =
- LTYPE_PEDESTRIANLL =
- LTYPE_PRESTRESS =
- LTYPE_HYPERSTATIC =
- LTYPE_BOUYANCY =
- LTYPE_STREAMFLOW =
- LTYPE_IMPACT =
- LTYPE_CONSTRUCTION =


The function returns zero if the type is successfully set; otherwise it returns nonzero.

## VBA Example

Sub SetLoadCaseDesignType

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

'set load case design type
ret = SapModel.LoadCases.SetDesignType("DEAD", 1, LTYPE_SUPERDEAD)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetType_

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.Buckling.GetInitialCase


**VB6 Procedure**

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

**Parameters**

Name

The name of an existing buckling load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else then zero initial
conditions are assumed.

**Remarks**

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseBucklingInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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


'add buckling load case
ret = SapModel.LoadCases.Buckling.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.Buckling.GetInitialCase("LCASE1", InitialCase)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.Buckling.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef SF() As Double) As Long

## Parameters

Name

The name of an existing buckling load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.


LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseBucklingLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim SF() As Double

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

'add buckling load case
ret = SapModel.LoadCases.Buckling.SetCase("LCASE1")


'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MySF(1) = 1.
ret = SapModel.LoadCases.Buckling.SetLoads("LCASE1", 2, MyLoadType, MyLoadName,
MySF)

'get load data
ret = SapModel.LoadCases.Buckling.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, SF)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetParameters

## Syntax

SapObject.SapModel.LoadCases.Buckling.GetParameters

## VB6 Procedure

Function GetParameters(ByVal Name As String, ByRef NumBucklingModes As Long, ByRef
EigenTol As Double) As Long

## Parameters


Name

The name of an existing buckling load case.

NumBucklingModes

The number of buckling modes requested.

EigenTol

The relative convergence tolerance for eigenvalues.

**Remarks**

This function retrieves various parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseBucklingParameters()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumBucklingModes As Long
Dim EigenTol As Double

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

'add buckling load case
ret = SapModel.LoadCases.Buckling.SetCase("LCASE1")

'get parameters
ret = SapModel.LoadCases.Buckling.GetParameters("LCASE1", NumBucklingModes,
EigenTol)

'close Sap


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetParameters

# SetCase

## Syntax

SapObject.SapModel.LoadCases.Buckling.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case then that case is modified,
otherwise, a new case is added.

## Remarks

This function initializes a buckling load case. If this function is called for an existing load case, all
items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseBuckling()
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

'add buckling load case
ret = SapModel.LoadCases.Buckling.SetCase("LCASE1")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.Buckling.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name


The name of an existing buckling load case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseBucklingInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add buckling load case
ret = SapModel.LoadCases.Buckling.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.Buckling.SetInitialCase("LCASE1", "SN1")

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.Buckling.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef SF() As Double) As Long

## Parameters

Name

The name of an existing buckling load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.


If the LoadType item is Acce, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of
the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseBucklingLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double

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

'add buckling load case
ret = SapModel.LoadCases.Buckling.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"


MySF(1) = 1.2
ret = SapModel.LoadCases.Buckling.SetLoads("LCASE1", 2, MyLoadType, MyLoadName,
MySF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# SetParameters

## Syntax

SapObject.SapModel.LoadCases.Buckling.SetParameters

## VB6 Procedure

Function SetParameters(ByVal Name As String, ByVal NumBucklingModes As Long, ByVal
EigenTol As Double) As Long

## Parameters

Name

The name of an existing buckling load case.

NumBucklingModes

The number of buckling modes requested.

EigenTol

The relative convergence tolerance for eigenvalues.

## Remarks


This function sets various parameters for the specified buckling load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseBucklingParameters()
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

'add buckling load case
ret = SapModel.LoadCases.Buckling.SetCase("LCASE1")

'set parameters
ret = SapModel.LoadCases.Buckling.SetParameters("LCASE1", 4, 1E-10)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetParameters


# GetDampProportional

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.GetDampProportional

## VB6 Procedure

Function GetDampProportional(ByVal Name As String, ByRef DampType As Long, ByRef
Dampa As Double, ByRef Dampb As Double, ByRef Dampf1 As Double, ByRef Dampf2 As
Double, ByRef Dampd1 As Double, ByRef Dampd2 As Double) As Long

## Parameters

Name

The name of an existing linear direct integration time history load case that has proportional
damping.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient.

Dampb

The stiffness proportional damping coefficient.

Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).


This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.

**Remarks**

This function retrieves the proportional modal damping data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseDirHistLinearDampProportional()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim Dampa As Double
Dim Dampb As Double
Dim Dampf1 As Double
Dim Dampf2 As Double
Dim Dampd1 As Double
Dim Dampd2 As Double

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

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.DirHistLinear.SetDampProportional("LCASE1", 2, 0, 0, 0.1, 1,
0.05, 0.06)


'get proportional damping
ret = SapModel.LoadCases.DirHistLinear.GetDampProportional("LCASE1", DampType,
Dampa, Dampb, Dampf1, Dampf2, Dampd1, Dampd2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampProportional

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing linear direct integration time history load case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.


**Remarks**

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseDirHistLinearInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.DirHistLinear.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef
TF() As Double, ByRef AT() As Double, ByRef CSys() As String, ByRef Ang() As Double) As
Long

## Parameters

Name

The name of an existing linear direct integration time history load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load or Accel, indicating the type of each load assigned to the load
case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the time history function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

TF


This is an array that includes the time scale factor of each load assigned to the load case.

AT

This is an array that includes the arrival time of each load assigned to the load case.

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseDirHistLinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyTF() As Double
Dim MyAT() As Double
Dim MyCSys() As String
Dim MyAng() As Double
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim Func() As String
Dim SF() As Double
Dim TF() As Double
Dim AT() As Double
Dim CSys() As String
Dim Ang() As Double

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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyTF(1)
ReDim MyAT(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "RAMPTH"
MySF(0) = 1
MyTF(0) = 1
MyAT(0) = 0
MyCSys(0) = "Global"
MyAng(0) = 0
MyLoadType(1) = "Accel"
MyLoadName(1) = "U2"
MyFunc(1) = "TH-1"
MySF(1) = 2
MyTF(1) = 1.5
MyAT(1) = 10
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.DirHistLinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'get load data
ret = SapModel.LoadCases.DirHistLinear.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, Func, SF, TF, AT, CSys, Ang)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetTimeIntegration

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.GetTimeIntegration

## VB6 Procedure

Function GetTimeIntegration(ByVal Name As String, ByRef IntegrationType As Long, ByRef
Alpha As Double, ByRef Beta As Double, ByRef Gamma As Double, ByRef Theta As Double,
ByRef m As Double) As Long

## Parameters

Name

The name of an existing linear direct integration time history load case.

IntegrationType

This is 1, 2, 3, 4 or 5, indicating the time integration type.

```
1 = Newmark
2 = Wilson
3 = Collocation
4 = Hilber-Hughes-Taylor
5 = Chung and Hulbert
```
Alpha

The alpha factor (-1/3 <= Alpha <= 0).

This item applies only when IntegrationType = 4 or 5.


Beta

The beta factor (Beta >= 0).

This item applies only when IntegrationType = 1, 3 or 5. It is returned for informational purposes
when IntegrationType = 4.

Gamma

The gamma factor (Gamma >= 0.5).

This item applies only when IntegrationType = 1, 3 or 5. It is returned for informational purposes
when IntegrationType = 4.

Theta

The theta factor (Theta > 0).

This item applies only when IntegrationType = 2 or 3.

m

The alpha-m factor.

This item only applies when IntegrationType = 5.

**Remarks**

This function retrieves the time integration data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseDirHistLinearTimeIntegration()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim IntegrationType As Long
Dim Alpha As Double
Dim Beta As Double
Dim Gamma As Double
Dim Theta As Double
Dim m As Double

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

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'set time integration parameters
ret = SapModel.LoadCases.DirHistLinear.SetTimeIntegration("LCASE1", 3, 0, 0.17, 0.52,
0.9)

'get time integration parameters
ret = SapModel.LoadCases.DirHistLinear.GetTimeIntegration("LCASE1", IntegrationType,
Alpha, Beta, Gamma, Theta, m)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetTimeIntegration

# GetTimeStep

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.GetTimeStep

## VB6 Procedure

Function GetTimeStep(ByVal Name As String, ByRef nstep As Long, ByRef DT As Double) As
Long


**Parameters**

Name

The name of an existing linear direct integration time history load case.

nstep

The number of output time steps.

DT

The output time step size.

**Remarks**

This function retrieves the time step data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseDirHistLinearTimeStep()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim nstep As Long
Dim DT As Double

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

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'get time step data
ret = SapModel.LoadCases.DirHistLinear.GetTimeStep ("LCASE1", nstep, DT )

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetTimeStep

# SetCase

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise a new case is added.

## Remarks

This function initializes a linear direct integration time history load case. If this function is called
for an existing load case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseDirHistLinear()
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

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetDampProportional

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.SetDampProportional

## VB6 Procedure

Function SetDampProportional(ByVal Name As String, ByVal DampType As Long, ByVal
Dampa As Double, ByVal Dampb As Double, ByVal Dampf1 As Double, ByVal Dampf2 As
Double, ByVal Dampd1 As Double, ByVal Dampd2 As Double) As Long


**Parameters**

Name

The name of an existing linear direct integration time history load case.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient. This item applies only when DampType = 1.

Dampb

The stiffness proportional damping coefficient. This item applies only when DampType = 1.

Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is either the period or the frequency (depending on the value of the DampType item) for
point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.

**Remarks**

This function sets proportional modal damping data for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.


## VBA Example

Sub SetCaseDirHistLinearDampProportional()
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

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.DirHistLinear.SetDampProportional("LCASE1", 2, 0, 0, 0.1, 1,
0.05, 0.06)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampProportional

# SetInitialCase


**Syntax**

SapObject.SapModel.LoadCases.DirHistLinear.SetInitialCase

**VB6 Procedure**

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

**Parameters**

Name

The name of an existing linear direct integration time history load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case. the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseDirHistLinearInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.DirHistLinear.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef TF
() As Double, ByRef AT() As Double, ByRef CSys() As String, ByRef Ang() As Double) As
Long

## Parameters

Name

The name of an existing linear direct integration time history load case.


NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load or Accel, indicating the type of each load assigned to the load
case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the time history function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

TF

This is an array that includes the time scale factor of each load assigned to the load case.

AT

This is an array that includes the arrival time of each load assigned to the load case.

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.


**VBA Example**

Sub SetCaseDirHistLinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyTF() As Double
Dim MyAT() As Double
Dim MyCSys() As String
Dim MyAng() As Double

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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyTF(1)
ReDim MyAT(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "RAMPTH"
MySF(0) = 1
MyTF(0) = 1
MyAT(0) = 0


MyCSys(0) = "Global"
MyAng(0) = 0
MyLoadType(1) = "Accel"
MyLoadName(1) = "U2"
MyFunc(1) = "TH-1"
MySF(1) = 2
MyTF(1) = 1.5
MyAT(1) = 10
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.DirHistLinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# SetTimeIntegration

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.SetTimeIntegration

## VB6 Procedure

Function SetTimeIntegration(ByVal Name As String, ByVal IntegrationType As Long, ByVal
Alpha As Double, ByVal Beta As Double, ByVal Gamma As Double, ByVal Theta As Double,
Optional ByVal m As Double = 0) As Long

## Parameters

Name

The name of an existing linear direct integration time history load case.


IntegrationType

This is 1, 2, 3, 4 or 5, indicating the time integration type.

```
1 = Newmark
2 = Wilson
3 = Collocation
4 = Hilber-Hughes-Taylor
5 = Chung and Hulbert
```
Alpha

The alpha factor (-1/3 <= Alpha <= 0).

This item applies only when IntegrationType = 4 or 5.

Beta

The beta factor (Beta >= 0).

This item applies only when IntegrationType = 1, 3 or 5.

Gamma

The gamma factor (Gamma >= 0.5).

This item applies only when IntegrationType = 1, 3 or 5.

Theta

The theta factor (Theta > 0).

This item applies only when IntegrationType = 2 or 3.

m

The alpha-m factor.

This item applies only when IntegrationType = 5.

**Remarks**

This function sets time integration data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseDirHistLinearTimeIntegration()
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

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'set time integration parameters
ret = SapModel.LoadCases.DirHistLinear.SetTimeIntegration("LCASE1", 3, 0, 0.17, 0.52,
0.9)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetTimeIntegration

# SetTimeStep

## Syntax

SapObject.SapModel.LoadCases.DirHistLinear.SetTimeStep

## VB6 Procedure

Function SetTimeStep(ByVal Name As String, ByVal nstep As Long, ByVal DT As Double) As
Long


**Parameters**

Name

The name of an existing linear direct integration time history load case.

nstep

The number of output time steps.

DT

The output time step size.

**Remarks**

This function sets the time step data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseDirHistLinearTimeStep()
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

'add linear direct history load case
ret = SapModel.LoadCases.DirHistLinear.SetCase("LCASE1")

'set time step data
ret = SapModel.LoadCases.DirHistLinear.SetTimeStep("LCASE1", 120, 0.05)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetTimeStep

# GetDampProportional

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.GetDampProportional

## VB6 Procedure

Function GetDampProportional(ByVal Name As String, ByRef DampType As Long, ByRef
Dampa As Double, ByRef Dampb As Double, ByRef Dampf1 As Double, ByRef Dampf2 As
Double, ByRef Dampd1 As Double, ByRef Dampd2 As Double) As Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case that has proportional
damping.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient.

Dampb

The stiffness proportional damping coefficient.


Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.

**Remarks**

This function retrieves the proportional modal damping data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseDirHistNonlinearDampProportional()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim Dampa As Double
Dim Dampb As Double
Dim Dampf1 As Double
Dim Dampf2 As Double
Dim Dampd1 As Double
Dim Dampd2 As Double

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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.DirHistNonlinear.SetDampProportional("LCASE1", 2, 0, 0, 0.1,
1, 0.05, 0.06)

'get proportional damping
ret = SapModel.LoadCases.DirHistNonlinear.GetDampProportional("LCASE1", DampType,
Dampa, Dampb, Dampf1, Dampf2, Dampd1, Dampd2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampProportional

# GetGeometricNonlinearity

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.GetGeometricNonlinearity

## VB6 Procedure

Function GetGeometricNonlinearity(ByVal Name As String, ByRef NLGeomType As Long) As
Long


**Parameters**

Name

The name of an existing nonlinear direct integration time history load case.

NLGeomType

This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.

```
0 = None
1 = P-delta
2 = P-delta plus large displacements
```
**Remarks**

This function retrieves the geometric nonlinearity option for the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseDirHistNonlinearGeometricNonlinearity()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NLGeomType As Long

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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'get geometric nonlinearity option
ret = SapModel.LoadCases.DirHistNonlinear.GetGeometricNonlinearity("LCASE1",
NLGeomType)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetGeometricNonlinearity

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts from the state at the end
of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the state at the end of that case is used. If the initial case is anything else then zero initial
conditions are assumed.

## Remarks

This function retrieves the initial condition assumed for the specified load case.


The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseDirHistNonlinearInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.DirHistNonlinear.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

SetInitialCase


# GetLoads

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef
TF() As Double, ByRef AT() As Double, ByRef CSys() As String, ByRef Ang() As Double) As
Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load or Accel, indicating the type of each load assigned to the load
case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the time history function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

TF

This is an array that includes the time scale factor of each load assigned to the load case.

AT


This is an array that includes the arrival time of each load assigned to the load case.

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseDirHistNonlinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyTF() As Double
Dim MyAT() As Double
Dim MyCSys() As String
Dim MyAng() As Double
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim Func() As String
Dim SF() As Double
Dim TF() As Double
Dim AT() As Double
Dim CSys() As String
Dim Ang() As Double

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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyTF(1)
ReDim MyAT(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "RAMPTH"
MySF(0) = 1
MyTF(0) = 1
MyAT(0) = 0
MyCSys(0) = "Global"
MyAng(0) = 0
MyLoadType(1) = "Accel"
MyLoadName(1) = "U2"
MyFunc(1) = "TH-1"
MySF(1) = 2
MyTF(1) = 1.5
MyAT(1) = 10
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.DirHistNonlinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'get load data
ret = SapModel.LoadCases.DirHistNonlinear.GetLoads("LCASE1", NumberLoads,
LoadType, LoadName, Func, SF, TF, AT, CSys, Ang)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetMassSource

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.GetMassSource

## VB6 Procedure

Function GetMassSource(ByVal Name As String, ByRef Source As String) As Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

Source

This is the name of an existing mass source or a blank string. Blank indicates to use the mass
source from the previous load case or the default mass source if the load case starts from zero
initial conditions.

## Remarks

This function sets the mass source to be used for the specified load case.

The function returns zero if the mass source is data is successfully set; otherwise it returns a
nonzero value.

## VBA Example

Sub GetCaseDirHistNonlinearMassSource()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim Source as String

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

'add static nonlinear load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'get a mass source from the static nonlinear load case

ret = SapModel.LoadCases.DirHistNonlinear.GetMassSource("LCASE1", "Source")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.20.

## See Also

SetMassSource

# GetSolControlParameters

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.GetSolControlParameters


**VB6 Procedure**

Function GetSolControlParameters(ByVal Name As String, ByRef DTMax As Double, ByRef
DTMin As Double, ByRef MaxIterCS As Long, ByRef MaxIterNR As Long, ByRef TolConvD
As Double, ByRef UseEventStepping As Boolean, ByRef TolEventD As Double, ByRef
MaxLineSearchPerIter As Long, ByRef TolLineSearch As Double, ByRef LineSearchStepFact As
Double) As Long

**Parameters**

Name

The name of an existing nonlinear direct integration time history load case.

DTMax

The maximum substep size.

DTMin

The minimum substep size.

MaxIterCS

The maximum constant-stiffness iterations per step.

MaxIterNR

The maximum Newton_Raphson iterations per step.

TolConvD

The relative iteration convergence tolerance.

UseEventStepping

This item is True if event-to-event stepping is used.

TolEventD

The relative event lumping tolerance.

MaxLineSearchPerIter

The maximum number of line searches per iteration.

TolLineSearch

The relative line-search acceptance tolerance.

LineSearchStepFact

The line-search step factor.


**Remarks**

This function retrieves the solution control parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseDirHistNonlinearSolutionControlParameters()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DTMax As Double
Dim DTMin As Double
Dim MaxIterCS As Long
Dim MaxIterNR As Long
Dim TolConvD As Double
Dim UseEventStepping As Boolean
Dim TolEventD As Double
Dim MaxLineSearchPerIter As Long
Dim TolLineSearch As Double
Dim LineSearchStepFact As Double

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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'get solution control parameters
ret = SapModel.LoadCases.DirHistNonlinear.GetSolControlParameters("LCASE1", DTMax,
DTMin, MaxIterCS, MaxIterNR, TolConvD, UseEventStepping, TolEventD,
MaxLineSearchPerIter, TolLineSearch, LineSearchStepFact)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetSolControlParameters

# GetTimeIntegration

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.GetTimeIntegration

## VB6 Procedure

Function GetTimeIntegration(ByVal Name As String, ByRef IntegrationType As Long, ByRef
Alpha As Double, ByRef Beta As Double, ByRef Gamma As Double, ByRef Theta As Double,
ByRef m As Double) As Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

IntegrationType

This is 1, 2, 3, 4 or 5; indicating the time integration type.

```
1 = Newmark
2 = Wilson
3 = Collocation
4 = Hilber-Hughes-Taylor
5 = Chung and Hulbert
```
Alpha

The alpha factor (-1/3 <= Alpha <= 0).

This item applies only when IntegrationType = 4 or 5.

Beta


The beta factor (Beta >= 0).

This item applies only when IntegrationType = 1, 3 or 5. It is returned for informational purposes
when IntegrationType = 4.

Gamma

The gamma factor (Gamma >= 0.5).

This item applies only when IntegrationType = 1, 3 or 5. It is returned for informational purposes
when IntegrationType = 4.

Theta

The theta factor (Theta > 0).

This item applies only when IntegrationType = 2 or 3.

m

The alpha-m factor.

This item applies only when IntegrationType = 5.

**Remarks**

This function retrieves the time integration data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseDirHistNonlinearTimeIntegration()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim IntegrationType As Long
Dim Alpha As Double
Dim Beta As Double
Dim Gamma As Double
Dim Theta As Double
Dim m As Double

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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set time integration parameters
ret = SapModel.LoadCases.DirHistNonlinear.SetTimeIntegration("LCASE1", 3, 0, 0.17, 0.52,
0.9)

'get time integration parameters
ret = SapModel.LoadCases.DirHistNonlinear.GetTimeIntegration("LCASE1",
IntegrationType, Alpha, Beta, Gamma, Theta, m)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetTimeIntegration

# GetTimeStep

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.GetTimeStep

## VB6 Procedure

Function GetTimeStep(ByVal Name As String, ByRef nstep As Long, ByRef DT As Double) As
Long

## Parameters


Name

The name of an existing nonlinear direct integration time history load case.

nstep

The number of output time steps.

DT

The output time step size.

**Remarks**

This function retrieves the time step data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseDirHistNonlinearTimeStep()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim nstep As Long
Dim DT As Double

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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'get time step data
ret = SapModel.LoadCases.DirHistNonlinear.GetTimeStep ("LCASE1", nstep, DT )

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetTimeStep

# SetCase

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

## Remarks

This function initializes a nonlinear direct integration time history load case. If this function is
called for an existing load case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseDirHistNonlinear()
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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetDampProportional

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetDampProportional

## VB6 Procedure

Function SetDampProportional(ByVal Name As String, ByVal DampType As Long, ByVal
Dampa As Double, ByVal Dampb As Double, ByVal Dampf1 As Double, ByVal Dampf2 As
Double, ByVal Dampd1 As Double, ByVal Dampd2 As Double) As Long

## Parameters

Name


The name of an existing nonlinear direct integration time history load case.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient. This item applies only when DampType = 1.

Dampb

The stiffness proportional damping coefficient. This item applies only when DampType = 1.

Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.

**Remarks**

This function sets proportional modal damping data for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseDirHistNonlinearDampProportional()
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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.DirHistNonlinear.SetDampProportional("LCASE1", 2, 0, 0, 0.1,
1, 0.05, 0.06)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampProportional

# SetGeometricNonlinearity

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetGeometricNonlinearity


**VB6 Procedure**

Function SetGeometricNonlinearity(ByVal Name As String, ByVal NLGeomType As Long) As
Long

**Parameters**

Name

The name of an existing nonlinear direct integration time history load case.

NLGeomType

This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.

```
0 = None
1 = P-delta
2 = P-delta plus large displacements
```
**Remarks**

This function sets the geometric nonlinearity option for the specified load case.

The function returns zero if the option is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseDirHistNonlinearGeometricNonlinearity()
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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")


'set geometric nonlinearity option
ret = SapModel.LoadCases.DirHistNonlinear.SetGeometricNonlinearity("LCASE1", 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetGeometricNonlinearity

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts from the state at the end
of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the state at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks


This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseDirHistNonlinearInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.DirHistNonlinear.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**


GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef TF
() As Double, ByRef AT() As Double, ByRef CSys() As String, ByRef Ang() As Double) As
Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load or Accel, indicating the type of each load assigned to the load
case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the time history function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

TF

This is an array that includes the time scale factor of each load assigned to the load case.


### AT

This is an array that includes the arrival time of each load assigned to the load case.

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseDirHistNonlinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyTF() As Double
Dim MyAT() As Double
Dim MyCSys() As String
Dim MyAng() As Double

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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyTF(1)
ReDim MyAT(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "RAMPTH"
MySF(0) = 1
MyTF(0) = 1
MyAT(0) = 0
MyCSys(0) = "Global"
MyAng(0) = 0
MyLoadType(1) = "Accel"
MyLoadName(1) = "U2"
MyFunc(1) = "TH-1"
MySF(1) = 2
MyTF(1) = 1.5
MyAT(1) = 10
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.DirHistNonlinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetLoads

# SetMassSource

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetMassSource

## VB6 Procedure

Function SetMassSource(ByVal Name As String, ByVal Source As String) As Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

Source

This is the name of an existing mass source or a blank string. Blank indicates to use the mass
source from the previous load case or the default mass source if the load case starts from zero
initial conditions.

## Remarks

This function sets the mass source to be used for the specified load case.

The function returns zero if the mass source is data is successfully set; otherwise it returns a
nonzero value.

## VBA Example

Sub SetCase DirHistNonlinear MassSource()
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

'add static nonlinear load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'add a new mass source and make it the default mass source

LoadPat(0) = "DEAD"

SF(0) = 1.25

ret = SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True, True, 1,
LoadPat, SF)

'assign a mass source to the static nonlinear load case

ret = SapModel.LoadCases.DirHistNonlinear.SetMassSource("LCASE1", "MyMassSource")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.20.

## See Also

GeGetMassSourcetMassSource

# SetSolControlParameters

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetSolControlParameters

## VB6 Procedure

Function SetSolControlParameters(ByVal Name As String, ByVal DTMax As Double, ByVal
DTMin As Double, ByVal MaxIterCS As Long, ByVal MaxIterNR As Long, ByVal TolConvD


As Double, ByVal UseEventStepping As Boolean, ByVal TolEventD As Double, ByVal
MaxLineSearchPerIter As Long, ByVal TolLineSearch As Double, ByVal LineSearchStepFact As
Double) As Long

**Parameters**

Name

The name of an existing nonlinear direct integration time history load case.

DTMax

The maximum substep size.

DTMin

The minimum substep size.

MaxIterCS

The maximum constant-stiffness iterations per step.

MaxIterNR

The maximum Newton_Raphson iterations per step.

TolConvD

The relative iteration convergence tolerance.

UseEventStepping

This item is True if event-to-event stepping is used.

TolEventD

The relative event lumping tolerance.

MaxLineSearchPerIter

The maximum number of line searches per iteration.

TolLineSearch

The relative line-search acceptance tolerance.

LineSearchStepFact

The line-search step factor.

**Remarks**

This function sets the solution control parameters for the specified load case.


The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseDirHistNonlinearSolutionControlParameters()
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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set solution control parameters
ret = SapModel.LoadCases.DirHistNonlinear.SetSolControlParameters("LCASE1", 0.01,
0.00001, 15, 50, 0.00005, False, 0.02, 10, 0.2, 1.7)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetSolControlParameters


# SetTimeIntegration

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetTimeIntegration

## VB6 Procedure

Function SetTimeIntegration(ByVal Name As String, ByVal IntegrationType As Long, ByVal
Alpha As Double, ByVal Beta As Double, ByVal Gamma As Double, ByVal Theta As Double,
Optional ByVal m As Double = 0) As Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

IntegrationType

This is 1, 2, 3, 4 or 5, indicating the time integration type.

```
1 = Newmark
2 = Wilson
3 = Collocation
4 = Hilber-Hughes-Taylor
5 = Chung and Hulbert
```
Alpha

The alpha factor (-1/3 <= Alpha <= 0).

This item applies only when IntegrationType = 4 or 5.

Beta

The beta factor (Beta >= 0).

This item applies only when IntegrationType = 1, 3 or 5.

Gamma

The gamma factor (Gamma >= 0.5).

This item applies only when IntegrationType = 1, 3 or 5.

Theta

The theta factor (Theta > 0).

This item applies only when IntegrationType = 2 or 3.


m

The alpha-m factor.

This item applies only when IntegrationType = 5.

**Remarks**

This function sets time integration data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseDirHistNonlinearTimeIntegration()
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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set time integration parameters
ret = SapModel.LoadCases.DirHistNonlinear.SetTimeIntegration("LCASE1", 3, 0, 0.17, 0.52,
0.9)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetTimeIntegration

# SetTimeStep

## Syntax

SapObject.SapModel.LoadCases.DirHistNonlinear.SetTimeStep

## VB6 Procedure

Function SetTimeStep(ByVal Name As String, ByVal nstep As Long, ByVal DT As Double) As
Long

## Parameters

Name

The name of an existing nonlinear direct integration time history load case.

nstep

The number of output time steps.

DT

The output time step size.

## Remarks

This function sets the time step data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseDirHistNonlinearTimeStep()
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

'add nonlinear direct history load case
ret = SapModel.LoadCases.DirHistNonlinear.SetCase("LCASE1")

'set time step data
ret = SapModel.LoadCases.DirHistNonlinear.SetTimeStep("LCASE1", 120, 0.05)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetTimeStep

# SetCase

## Syntax

```
SapObject.SapModel.LoadCases.ExternalResults.SetCase
```
## VB6 Procedure

```
Function SetCase(ByVal Name As String) As Long
```
## Parameters


```
Name
```
```
The name of an existing or new load case for which user-supplied external analysis results
are available for some frame objects. If this is an existing case, that case is modified;
otherwise, a new case is added.
```
**Remarks**

```
This function initializes an external results load case. If this function is called for an
existing load case, all items for the case are reset to their default value.
```
```
The function returns zero if the load case is successfully initialized; otherwise it returns a
nonzero value.
```
**VBA Example**

```
Sub SetFrameExternalResultStations()
```
```
'dimension variables
```
```
Dim SapObject As Sap2000v16.SapObject
```
```
Dim SapModel As cSapModel
```
```
Dim ret As Long
```
```
Dim ObjSta() As Double = New Double() {0.0, 124.0}
```
```
Dim LoadCase() As String = New String() {"EXTERNAL"}
```
```
Dim P() As Double = New Double() {5.0, 5.0}
```
```
Dim V2() As Double = New Double() {-5.0, 5.0}
```
```
Dim V3() As Double = Nothing
```
```
Dim T() As Double = Nothing
```
```
Dim M2() As Double = Nothing
```
```
Dim M3() As Double = New Double() {100.0, 100.0}
```
'create Sap2000 object

```
SapObject = New Sap2000v16.SapObject
```
'start Sap2000 application

```
SapObject.ApplicationStart()
```

'create SapModel object

```
SapModel = SapObject.SapModel
```
'initialize model

```
ret = SapModel.InitializeNewModel
```
'create model from template

```
ret = SapModel.File.New2DFrame
(e2DFrameType.PortalFrame, 3, 124, 3, 200)
```
'create load case for external results

```
ret = SapModel.LoadCases.ExternalResults.SetCase
("EXTERNAL")
```
'set cases and stations for frame external results

```
ret = SapModel.ExternalAnalysisResults.PresetFrameCases("1", 1,
LoadCase)
```
```
ret = SapModel.ExternalAnalysisResults.SetFrameStations("1", ObjSta)
```
'set frame external result forces at case first step

```
ret = SapModel.ExternalAnalysisResults.SetFrameForce("1",
"EXTERNAL", 0, P, V2, V3, T, M2, M3)
```
'close Sap2000

```
SapObject.ApplicationExit(False)
SapModel = Nothing
```
```
SapObject = Nothing
```
```
End Sub
```
**Release Notes**

Initial release in version 16.0


# SetNumberSteps

## Syntax

```
SapObject.SapModel.LoadCases.ExternalResults.SetNumberSteps
```
## VB6 Procedure

```
Function SetNumberSteps (ByVal Name As String, ByVal FirstStep As Long, ByVal
LastStep As Long) As Long
```
## Parameters

```
Name
```
```
The name of an existing external results load case.
```
```
FirstStep
```
```
The number of the first step for which external results are to be subsequently provided for
frame objects in conjunction with this load case. The value may be 0 or 1. A value of zero
is typically used for cases that include the initial conditions, such as time-history cases.
```
```
LastStep
```
```
The number of the last step for which external results are to be subsequently provided for
frame objects in conjunction with this load case. The value must be greater than or equal to
FirstStep.
```
## Remarks

```
In the absence of a call to this function, the default values are FirstStep = 1 and LastStep =
1.
```
```
The number of steps available for this load case will be LastStep – FirstStep + 1.
```
```
The function returns zero if the number of steps is successfully initialized; otherwise it
returns a nonzero value.
```
## VBA Example

```
Sub SetFrameExternalResultStations()
```
```
'dimension variables
```
```
Dim SapObject As Sap2000v16.SapObject
```
```
Dim SapModel As cSapModel
```
```
Dim ret As Long
```

```
Dim ObjSta() As Double = New Double() {0.0, 124.0}
```
```
Dim LoadCase() As String = New String()
{"EXTERNAL"}
```
```
Dim P() As Double = New Double() {5.0, 5.0}
```
```
Dim V2() As Double = New Double() {-5.0, 5.0}
```
```
Dim V3() As Double = Nothing
```
```
Dim T() As Double = Nothing
```
```
Dim M2() As Double = Nothing
```
```
Dim M3() As Double = New Double() {100.0, 100.0}
```
'create Sap2000 object

```
SapObject = New Sap2000v16.SapObject
```
'start Sap2000 application

```
SapObject.ApplicationStart()
```
'create SapModel object

```
SapModel = SapObject.SapModel
```
'initialize model

```
ret = SapModel.InitializeNewModel
```
'create model from template

```
ret = SapModel.File.New2DFrame
(e2DFrameType.PortalFrame, 3, 124, 3, 200)
```
'create load case for external results

```
ret = SapModel.LoadCases.ExternalResults.SetCase
("EXTERNAL")
```
```
ret =
SapModel.LoadCases.ExternalResults.SetNumberSteps("EXTERNAL",
1, 1)
```

```
'set cases and stations for frame external results
```
```
ret =
SapModel.ExternalAnalysisResults.PresetFrameCases("1", 1,
LoadCase)
```
```
ret =
SapModel.ExternalAnalysisResults.SetFrameStations("1", ObjSta)
```
```
'set frame external result forces at case first step
```
```
ret = SapModel.ExternalAnalysisResults.SetFrameForce
("1", "EXTERNAL", 0, P, V2, V3, T, M2, M3)
```
```
'close Sap2000
```
```
SapObject.ApplicationExit(False)
```
```
SapModel = Nothing
```
```
SapObject = Nothing
```
```
End Sub
```
## Release Notes

Initial release in version 16.0

# GetBaseCase

## Syntax

SapObject.SapModel.LoadCases.HyperStatic.GetBaseCase

## VB6 Procedure

Function GetBaseCase(ByVal Name As String, ByRef BaseCase As String) As Long


**Parameters**

Name

The name of an existing hyperstatic load case.

BaseCase

The name of an existing static linear load case that is the base case for the specified hyperstatic
load case.

**Remarks**

This function retrieves the base case for the specified hyperstatic load case.

The function returns zero if the base case is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseHyperStaticInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim BaseCase As String

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

'add hyperstatic load case
ret = SapModel.LoadCases.HyperStatic.SetCase("LCASE1")

'set base case
ret = SapModel.LoadCases.HyperStatic.SetBaseCase("LCASE1", "DEAD")

'get base case
ret = SapModel.LoadCases.HyperStatic.GetBaseCase("LCASE1", BaseCase)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetBaseCase

# SetBaseCase

## Syntax

SapObject.SapModel.LoadCases.HyperStatic.SetBaseCase

## VB6 Procedure

Function SetBaseCase(ByVal Name As String, ByVal BaseCase As String) As Long

## Parameters

Name

The name of an existing hyperstatic load case.

BaseCase

The name of an existing static linear load case that is the base case for the specified hyperstatic
load case.

## Remarks

This function sets the base case for the specified hyperstatic load case.

The function returns zero if the base case is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseHyperStaticBaseCase()
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

'add hyperstatic load case
ret = SapModel.LoadCases.HyperStatic.SetCase("LCASE1")

'set base case
ret = SapModel.LoadCases.HyperStatic.SetBaseCase("LCASE1", "DEAD")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetBaseCase

# SetCase

## Syntax

SapObject.SapModel.LoadCases.HyperStatic.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long


**Parameters**

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

**Remarks**

This function initializes a hyperstatic load case. If this function is called for an existing load case,
all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseHyperStatic()
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

'add hyperstatic load case
ret = SapModel.LoadCases.HyperStatic.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 12.00.


## See Also

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing modal eigen load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetCaseModalEigenInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.ModalEigen.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef TargetPar() As Double, ByRef StaticCorrect() As
Boolean) As Long

## Parameters


Name

The name of an existing modal eigen load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load, Accel or Link, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

If the LoadType item is Link, this item is not used.

TargetPar

This is an array that includes the target mass participation ratio.

StaticCorrect

This is an array that includes either 0 or 1, indicating if static correction modes are to be
calculated.

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseModalEigenLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyTargetPar() As Double
Dim MyStaticCorrect() As Boolean
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String


Dim TargetPar() As Double
Dim StaticCorrect() As Boolean

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

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'set load data
ReDim MyLoadType(2)
ReDim MyLoadName(2)
ReDim MyTargetPar(2)
ReDim MyStaticCorrect(2)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyTargetPar(0) = 99
MyStaticCorrect(0) = 1
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MyTargetPar(1) = 99
MyStaticCorrect(1) = 0
MyLoadType(2) = "Link"
MyTargetPar(2) = 99
MyStaticCorrect(2) = 0
ret = SapModel.LoadCases.ModalEigen.SetLoads("LCASE1", 3, MyLoadType,
MyLoadName, MyTargetPar, MyStaticCorrect)

'get load data
ret = SapModel.LoadCases.ModalEigen.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, TargetPar, StaticCorrect)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**


Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetNumberModes

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.GetNumberModes

## VB6 Procedure

Function GetNumberModes(ByVal Name As String, ByRef MaxModes As Long, ByRef
MinModes As Long) As Long

## Parameters

Name

The name of an existing modal eigen load case.

MaxModes

The maximum number of modes requested.

MinModes

The minimum number of modes requested.

## Remarks

This function retrieves the number of modes requested for the specified load case.

The function returns zero if the number of modes is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetCaseModalEigenNumberModes()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim MaxModes As Long
Dim MinModes As Long

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

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'get number of modes requested
ret = SapModel.LoadCases.ModalEigen.GetNumberModes("LCASE1", MaxModes,
MinModes)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetNumberModes

# GetParameters

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.GetParameters


**VB6 Procedure**

Function GetParameters(ByVal Name As String, ByRef EigenShiftFreq As Double, ByRef
EigenCutOff As Double, ByRef EigenTol As Double, ByRef AllowAutoFreqShift As Long) As
Long

**Parameters**

Name

The name of an existing modal eigen load case.

EigenShiftFreq

The eigenvalue shift frequency. [cyc/s]

EigenCutOff

The eigencutoff frequency radius. [cyc/s]

EigenTol

The relative convergence tolerance for eigenvalues.

AllowAutoFreqShift

This is either 0 or 1, indicating if automatic frequency shifting is allowed.

```
0 = Automatic frequency shifting is NOT allowed
1 = Automatic frequency shifting is allowed
```
**Remarks**

This function retrieves various parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseModalEigenParameters()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim EigenShiftFreq As Double
Dim EigenCutOff As Double
Dim EigenTol As Double
Dim AllowAutoFreqShift As Long

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

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'get parameters
ret = SapModel.LoadCases.ModalEigen.GetParameters("LCASE1", EigenShiftFreq,
EigenCutOff, EigenTol, AllowAutoFreqShift)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetParameters

# SetCase

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long


**Parameters**

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

**Remarks**

This function initializes a modal eigen load case. If this function is called for an existing load case,
all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseModalEigen()
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

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing modal eigen load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseModalEigenInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.ModalEigen.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.SetLoads

## VB6 Procedure


Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef TargetPar() As Double, ByRef StaticCorrect() As
Boolean) As Long

**Parameters**

Name

The name of an existing modal eigen load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load, Accel or Link, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

If the LoadType item is Link, this item is not used.

TargetPar

This is an array that includes the target mass participation ratio.

StaticCorrect

This is an array that includes either 0 or 1, indicating if static correction modes are to be
calculated.

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModalEigenLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String


Dim MyLoadName() As String
Dim MyTargetPar() As Double
Dim MyStaticCorrect() As Boolean

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

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'set load data
ReDim MyLoadType(2)
ReDim MyLoadName(2)
ReDim MyTargetPar(2)
ReDim MyStaticCorrect(2)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyTargetPar(0) = 99
MyStaticCorrect(0) = 1
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MyTargetPar(1) = 99
MyStaticCorrect(1) = 0
MyLoadType(2) = "Link"
MyTargetPar(2) = 99
MyStaticCorrect(2) = 0
ret = SapModel.LoadCases.ModalEigen.SetLoads("LCASE1", 3, MyLoadType,
MyLoadName, MyTargetPar, MyStaticCorrect)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# SetNumberModes

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.SetNumberModes

## VB6 Procedure

Function SetNumberModes(ByVal Name As String, ByVal MaxModes As Long, ByVal
MinModes As Long) As Long

## Parameters

Name

The name of an existing modal eigen load case.

MaxModes

The maximum number of modes requested.

MinModes

The minimum number of modes requested.

## Remarks

This function sets the number of modes requested for the specified load case.

The function returns zero if the number of modes is successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseModalEigenNumberModes()
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

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'set number of modes
ret = SapModel.LoadCases.ModalEigen.SetNumberModes("LCASE1", 10, 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetNumberModes

# SetParameters

## Syntax

SapObject.SapModel.LoadCases.ModalEigen.SetParameters

## VB6 Procedure

Function SetParameters(ByVal Name As String, ByVal EigenShiftFreq As Double, ByVal
EigenCutOff As Double, ByVal EigenTol As Double, ByVal AllowAutoFreqShift As Long) As
Long


**Parameters**

Name

The name of an existing modal eigen load case.

EigenShiftFreq

The eigenvalue shift frequency. [cyc/s]

EigenCutOff

The eigencutoff frequency radius. [cyc/s]

EigenTol

The relative convergence tolerance for eigenvalues.

AllowAutoFreqShift

This is either 0 or 1, indicating if automatic frequency shifting is allowed.

```
0 = Automatic frequency shifting is NOT allowed
1 = Automatic frequency shifting is allowed
```
**Remarks**

This function sets various parameters for the specified modal eigen load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseModalEigenParameters()
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

'add modal eigen load case
ret = SapModel.LoadCases.ModalEigen.SetCase("LCASE1")

'set parameters
ret = SapModel.LoadCases.ModalEigen.SetParameters("LCASE1", 0.05, 0.0001, 1E-10, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetParameters

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.ModalRitz.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing modal ritz load case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.


If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseModalRitzInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'add modal ritz load case
ret = SapModel.LoadCases.ModalRitz.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.ModalRitz.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.ModalRitz.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef RitzMaxCyc() As Long, ByRef TargetPar() As
Double) As Long

## Parameters

Name

The name of an existing modal ritz load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load, Accel or Link, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

If the LoadType item is Link, this item is not used.

RitzMaxCyc

This is an array that includes the maximum number of generation cycles to be performed for the
specified ritz starting vector. A value of 0 means there is no limit on the number of cycles.


TargetPar

This is an array that includes the target dynamic participation ratio.

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseModalRitzLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyRitzMaxCyc() As Long
Dim MyTargetPar() As Double
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim RitzMaxCyc() As Long
Dim TargetPar() As Double

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

'add modal ritz load case
ret = SapModel.LoadCases.ModalRitz.SetCase("LCASE1")

'set load data
ReDim MyLoadType(2)
ReDim MyLoadName(2)
ReDim MyRitzMaxCyc(2)
ReDim MyTargetPar(2)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"


MyRitzMaxCyc(0) = 0
MyTargetPar(0) = 99
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MyRitzMaxCyc(1) = 0
MyTargetPar(1) = 99
MyLoadType(2) = "Link"
MyRitzMaxCyc(2) = 0
MyTargetPar(2) = 99
ret = SapModel.LoadCases.ModalRitz.SetLoads("LCASE1", 3, MyLoadType, MyLoadName,
MyRitzMaxCyc, MyTargetPar)

'get load data
ret = SapModel.LoadCases.ModalRitz.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, RitzMaxCyc, TargetPar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetNumberModes

## Syntax

SapObject.SapModel.LoadCases.ModalRitz.GetNumberModes

## VB6 Procedure

Function GetNumberModes(ByVal Name As String, ByRef MaxModes As Long, ByRef
MinModes As Long) As Long

## Parameters

Name


The name of an existing modal ritz load case.

MaxModes

The maximum number of modes requested.

MinModes

The minimum number of modes requested.

**Remarks**

This function retrieves the number of modes requested for the specified load case.

The function returns zero if the number of modes is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseModalRitzNumberModes()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MaxModes As Long
Dim MinModes As Long

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

'add modal ritz load case
ret = SapModel.LoadCases.ModalRitz.SetCase("LCASE1")

'get number of modes requested
ret = SapModel.LoadCases.ModalRitz.GetNumberModes("LCASE1", MaxModes,
MinModes)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetNumberModes

# SetCase

## Syntax

SapObject.SapModel.LoadCases.ModalRitz.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

## Remarks

This function initializes a modal ritz load case. If this function is called for an existing load case,
all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseModalRitz()
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

'add modal ritz load case
ret = SapModel.LoadCases.ModalRitz.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.ModalRitz.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing modal ritz load case.


InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseModalRitzInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add modal ritz load case
ret = SapModel.LoadCases.ModalRitz.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.ModalRitz.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.ModalRitz.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef RitzMaxCyc() As Long, ByRef TargetPar() As
Double) As Long

## Parameters

Name

The name of an existing modal ritz load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load, Accel or Link, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.


If the LoadType item is Link, this item is not used.

RitzMaxCyc

This is an array that includes the maximum number of generation cycles to be performed for the
specified ritz starting vector. A value of 0 means there is no limit on the number of cycles.

TargetPar

This is an array that includes the target dynamic participation ratio.

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModalRitzLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyRitzMaxCyc() As Long
Dim MyTargetPar() As Double

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

'add modal ritz load case
ret = SapModel.LoadCases.ModalRitz.SetCase("LCASE1")

'set load data
ReDim MyLoadType(2)
ReDim MyLoadName(2)
ReDim MyRitzMaxCyc(2)
ReDim MyTargetPar(2)


MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyRitzMaxCyc(0) = 0
MyTargetPar(0) = 99
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MyRitzMaxCyc(1) = 0
MyTargetPar(1) = 99
MyLoadType(2) = "Link"
MyRitzMaxCyc(2) = 0
MyTargetPar(2) = 99
ret = SapModel.LoadCases.ModalRitz.SetLoads("LCASE1", 3, MyLoadType, MyLoadName,
MyRitzMaxCyc, MyTargetPar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# SetNumberModes

## Syntax

SapObject.SapModel.LoadCases.ModalRitz.SetNumberModes

## VB6 Procedure

Function SetNumberModes(ByVal Name As String, ByVal MaxModes As Long, ByVal
MinModes As Long) As Long

## Parameters

Name

The name of an existing modal ritz load case.


MaxModes

The maximum number of modes requested.

MinModes

The minimum number of modes requested.

**Remarks**

This function sets the number of modes requested for the specified load case.

The function returns zero if the number of modes is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseModalRitzNumberModes()
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

'add modal ritz load case
ret = SapModel.LoadCases.ModalRitz.SetCase("LCASE1")

'set number of modes
ret = SapModel.LoadCases.ModalRitz.SetNumberModes("LCASE1", 10, 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetNumberModes

# GetDampConstant

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetDampConstant

## VB6 Procedure

Function GetDampConstant(ByVal Name As String, ByRef Damp As Double) As Long

## Parameters

Name

The name of an existing linear modal history analysis case that has constant damping.

Damp

The constant damping for all modes (0 <= Damp < 1).

## Remarks

This function retrieves the constant modal damping for all modes assigned to the specified load
case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCaseModHistLinearDampConstant()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim Damp As Double


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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ModHistLinear.SetDampConstant("LCASE1", 0.04)

'get constant damping
ret = SapModel.LoadCases.ModHistLinear.GetDampType("LCASE1", DampType)
If DampType = 4 Then
ret = SapModel.LoadCases.ModHistLinear.GetDampConstant("LCASE1", Damp)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampConstant

# GetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetDampInterpolated


**VB6 Procedure**

Function GetDampInterpolated(ByVal Name As String, ByRef DampType As Long, ByRef
NumberItems As Long, ByRef Time() As Double, ByRef Damp() As Double) As Long

**Parameters**

Name

The name of an existing linear modal history analysis case that has interpolated damping.

DampType

This is 5 or 6, indicating the interpolated modal damping type.

```
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
NumberItems

The number of Time and Damp pairs.

Time

This is an array that includes the period or the frequency, depending on the value of the
DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6

Damp

This is an array that includes the damping for the specified period of frequency (0 <= Damp < 1).

**Remarks**

This function retrieves the interpolated modal damping data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseModHistLinearDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyTime() As Double
Dim MyDamp() As Double
Dim DampType As Long
Dim NumberItems As Long
Dim Time() As Double
Dim Damp() As Double


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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set interpolated damping
ReDim MyTime(2)
ReDim MyDamp(2)
MyTime(0) = 0.001
MyDamp(0) = 0.1
MyTime(1) = 0.3
MyDamp(1) = 0.03
MyTime(2) = 1
MyDamp(2) = 0.05
ret = SapModel.LoadCases.ModHistLinear.SetDampInterpolated("LCASE1", 5, 3, MyTime,
MyDamp)

'get interpolated damping
ret = SapModel.LoadCases.ModHistLinear.GetDampType("LCASE1", DampType)
If DampType = 5 or DampType = 6 Then
ret = SapModel.LoadCases.ModHistLinear.GetDampInterpolated("LCASE1", DampType,
NumberItems, Time, Damp)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

SetDampInterpolated

# GetDampOverrides

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetDampInterpolated

## VB6 Procedure

Function GetDampInterpolated(ByVal Name As String, ByRef NumberItems As Long, ByRef
Mode() As Long, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.

NumberItems

The number of Mode and Damp pairs.

Mode

This is an array that includes a mode number.

Damp

This is an array that includes the damping for the specified mode (0 <= Damp < 1).

## Remarks

This function retrieves the modal damping overrides assigned to the specified load case.

The function returns zero if the overrides are successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCaseModHistLinearDampOverrides()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMode() As Long
Dim MyDamp() As Double


Dim NumberItems As Long
Dim Mode() As Long
Dim Damp() As Double

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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ModHistLinear.SetDampConstant("LCASE1", 0.04)

'set modal damping overrides
ReDim MyMode(1)
ReDim MyDamp(1)
MyMode(0) = 1
MyDamp(0) = 0.02
MyMode(1) = 2
MyDamp(1) = 0.03
ret = SapModel.LoadCases.ModHistLinear.SetDampOverrides("LCASE1", 2, MyMode,
MyDamp)

'get modal damping overrides
ret = SapModel.LoadCases.ModHistLinear.GetDampOverrides("LCASE1", NumberItems,
Mode, Damp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

SetDampOverrides

# GetDampProportional

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetDampProportional

## VB6 Procedure

Function GetDampProportional(ByVal Name As String, ByRef DampType As Long, ByRef
Dampa As Double, ByRef Dampb As Double, ByRef Dampf1 As Double, ByRef Dampf2 As
Double, ByRef Dampd1 As Double, ByRef Dampd2 As Double) As Long

## Parameters

Name

The name of an existing linear modal history analysis case that has proportional damping.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient.

Dampb

The stiffness proportional damping coefficient.

Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.


Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.

**Remarks**

This function retrieves the proportional modal damping data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseModHistLinearDampProportional()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim Dampa As Double
Dim Dampb As Double
Dim Dampf1 As Double
Dim Dampf2 As Double
Dim Dampd1 As Double
Dim Dampd2 As Double

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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")


'set proportional damping
ret = SapModel.LoadCases.ModHistLinear.SetDampProportional("LCASE1", 2, 0, 0, 0.1, 1,
0.05, 0.06)

'get proportional damping
ret = SapModel.LoadCases.ModHistLinear.GetDampType("LCASE1", DampType)
If DampType >= 1 or DampType <= 3 Then
ret = SapModel.LoadCases.ModHistLinear.GetDampProportional("LCASE1", DampType,
Dampa, Dampb, Dampf1, Dampf2, Dampd1, Dampd2)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampProportional

# GetDampType

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetDampType

## VB6 Procedure

Function GetDampType(ByVal Name As String, ByRef DampType As Long) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.

DampType

This is 1, 2, 3, 4, 5 or 6, indicating the modal damping type for the load case.

```
1 = Mass and stiffness proportional damping by direct specification
```

```
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
4 = Constant damping for all modes
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
**Remarks**

This function retrieves the modal damping type for the specified load case.

The function returns zero if the type is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseModHistLinearDampType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long

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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'get damping type
ret = SapModel.LoadCases.ModHistLinear.GetDampType("LCASE1", DampType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampConstant

GetDampInterpolated

GetDampProportional

GetDampOverrides

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef
TF() As Double, ByRef AT() As Double, ByRef CSys() As String, ByRef Ang() As Double) As
Long

## Parameters

Name

The name of an existing linear modal history analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load or Accel, indicating the type of each load assigned to the load
case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.


Func

This is an array that includes the name of the time history function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

TF

This is an array that includes the time scale factor of each load assigned to the load case.

AT

This is an array that includes the arrival time of each load assigned to the load case.

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseModHistLinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyTF() As Double
Dim MyAT() As Double
Dim MyCSys() As String
Dim MyAng() As Double


Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim Func() As String
Dim SF() As Double
Dim TF() As Double
Dim AT() As Double
Dim CSys() As String
Dim Ang() As Double

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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyTF(1)
ReDim MyAT(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "RAMPTH"
MySF(0) = 1
MyTF(0) = 1
MyAT(0) = 0
MyCSys(0) = "Global"
MyAng(0) = 0
MyLoadType(1) = "Accel"
MyLoadName(1) = "U2"
MyFunc(1) = "TH-1"
MySF(1) = 2
MyTF(1) = 1.5


MyAT(1) = 10
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.ModHistLinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'get load data
ret = SapModel.LoadCases.ModHistLinear.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, Func, SF, TF, AT, CSys, Ang)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetModalCase

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetModalCase

## VB6 Procedure

Function GetModalCase(ByVal Name As String, ByRef ModalCase As String) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.

ModalCase

This is None or the name of an existing modal analysis case. It specifies the modal load case on
which any mode-type load assignments to the specified load case are based.


**Remarks**

This function retrieves the modal case assigned to the specified load case.

The function returns zero if the modal case is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseModHistLinearModalCase()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ModalCase As String

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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'get modal case
ret = SapModel.LoadCases.ModHistLinear.GetModalCase("LCASE1", ModalCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

SetModalCase

# GetMotionType

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetMotionType

## VB6 Procedure

Function GetMotionType(ByVal Name As String, ByRef MotionType As Long) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.

MotionType

This is 1 or 2, indicating the time history motion type.

```
1 = Transient
2 = Periodic
```
## Remarks

This function retrieves the motion type for the specified load case.

The function returns zero if the motion type is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetCaseModHistLinearMotionType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MotionType As Long

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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'get motion type
ret = SapModel.LoadCases.ModHistLinear.GetMotionType ("LCASE1", MotionType )

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetMotionType

# GetTimeStep

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.GetTimeStep

## VB6 Procedure

Function GetTimeStep(ByVal Name As String, ByRef nstep As Long, ByRef DT As Double) As
Long

## Parameters

Name


The name of an existing linear modal history analysis case.

nstep

The number of output time steps.

DT

The output time step size.

**Remarks**

This function retrieves the time step data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseModHistLinearTimeStep()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim nstep As Long
Dim DT As Double

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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'get time step data
ret = SapModel.LoadCases.ModHistLinear.GetTimeStep ("LCASE1", nstep, DT )

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetTimeStep

# SetCase

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise a new case is added.

## Remarks

This function initializes a linear modal history analysis case. If this function is called for an
existing load case then all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseModHistLinear()
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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetDampConstant

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetDampConstant

## VB6 Procedure

Function SetDampConstant(ByVal Name As String, ByVal Damp As Double) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.

Damp

The constant damping for all modes (0 <= Damp < 1).


**Remarks**

This function sets constant modal damping for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModHistLinearDampConstant()
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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ModHistLinear.SetDampConstant("LCASE1", 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**


GetDampConstant

# SetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetDampInterpolated

## VB6 Procedure

Function SetDampInterpolated(ByVal Name As String, ByVal DampType As Long, ByVal
NumberItems As Long, ByRef Time() As Double, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.

DampType

This is 5 or 6, indicating the interpolated modal damping type.

```
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
NumberItems

The number of Time and Damp pairs.

Time

This is an array that includes the period or the frequency, depending on the value of the
DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6

Damp

This is an array that includes the damping for the specified period of frequency (0 <= Damp < 1).

## Remarks

This function sets interpolated modal damping data for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseModHistLinearDampInterpolated()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim MyTime() As Double
Dim MyDamp() As Double

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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set interpolated damping
ReDim MyTime(2)
ReDim MyDamp(2)
MyTime(0) = 0.001
MyDamp(0) = 0.1
MyTime(1) = 0.3
MyDamp(1) = 0.03
MyTime(2) = 1
MyDamp(2) = 0.05
ret = SapModel.LoadCases.ModHistLinear.SetDampInterpolated("LCASE1", 5, 3, MyTime,
MyDamp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetDampInterpolated


# SetDampOverrides

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetDampOverrides

## VB6 Procedure

Function SetDampOverrides(ByVal Name As String, ByVal NumberItems As Long, ByRef Mode
() As Long, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.

NumberItems

The number of Mode and Damp pairs.

Mode

This is an array that includes a mode number.

Damp

This is an array that includes the damping for the specified mode (0 <= Damp < 1).

## Remarks

This function sets the modal damping overrides for the specified load case.

The function returns zero if the overrides are successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseModHistLinearDampOverrides()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMode() As Long
Dim MyDamp() As Double

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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ModHistLinear.SetDampConstant("LCASE1", 0.04)

'set modal damping overrides
ReDim MyMode(1)
ReDim MyDamp(1)
MyMode(0) = 1
MyDamp(0) = 0.02
MyMode(1) = 2
MyDamp(1) = 0.03
ret = SapModel.LoadCases.ModHistLinear.SetDampOverrides("LCASE1", 2, MyMode,
MyDamp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampOverrides

# SetDampProportional

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetDampProportional


**VB6 Procedure**

Function SetDampProportional(ByVal Name As String, ByVal DampType As Long, ByVal
Dampa As Double, ByVal Dampb As Double, ByVal Dampf1 As Double, ByVal Dampf2 As
Double, ByVal Dampd1 As Double, ByVal Dampd2 As Double) As Long

**Parameters**

Name

The name of an existing linear modal history analysis case.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient. This item applies only when DampType = 1.

Dampb

The stiffness proportional damping coefficient. This item applies only when DampType = 1.

Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.


**Remarks**

This function sets proportional modal damping data for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModHistLinearDampProportional()
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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.ModHistLinear.SetDampProportional("LCASE1", 2, 0, 0, 0.1, 1,
0.05, 0.06)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetDampProportional

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef TF
() As Double, ByRef AT() As Double, ByRef CSys() As String, ByRef Ang() As Double) As
Long

## Parameters

Name

The name of an existing linear modal history analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load or Accel, indicating the type of each load assigned to the load
case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the time history function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

TF


This is an array that includes the time scale factor of each load assigned to the load case.

AT

This is an array that includes the arrival time of each load assigned to the load case.

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModHistLinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyTF() As Double
Dim MyAT() As Double
Dim MyCSys() As String
Dim MyAng() As Double

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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyTF(1)
ReDim MyAT(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "RAMPTH"
MySF(0) = 1
MyTF(0) = 1
MyAT(0) = 0
MyCSys(0) = "Global"
MyAng(0) = 0
MyLoadType(1) = "Accel"
MyLoadName(1) = "U2"
MyFunc(1) = "TH-1"
MySF(1) = 2
MyTF(1) = 1.5
MyAT(1) = 10
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.ModHistLinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetLoads

# SetModalCase

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetModalCase

## VB6 Procedure

Function SetModalCase(ByVal Name As String, ByVal ModalCase As String) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.

ModalCase

This is the name of an existing modal load case. It specifies the modal load case on which any
mode-type load assignments to the specified load case are based.

## Remarks

This function sets the modal case for the specified analysis case.

The function returns zero if the modal case is successfully set; otherwise it returns a nonzero
value.

If the specified modal case is not actually a modal case, the program automatically replaces it with
the first modal case it can find. If no modal load cases exist, an error is returned.

## VBA Example

Sub SetCaseModHistLinearModalCase()
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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set modal case
ret = SapModel.LoadCases.ModHistLinear.SetModalCase("LCASE1", "MODAL")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetModalCase

# SetMotionType

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetMotionType

## VB6 Procedure

Function SetMotionType(ByVal Name As String, ByVal MotionType As Long) As Long

## Parameters

Name

The name of an existing linear modal history analysis case.


MotionType

This is 1 or 2, indicating the time history motion type.

```
1 = Transient
2 = Periodic
```
**Remarks**

This function sets the motion type for the specified analysis case.

The function returns zero if the motion type is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseModHistLinearMotionType()
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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set motion type
ret = SapModel.LoadCases.ModHistLinear.SetMotionType("LCASE1", 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**


Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetMotionType

# SetTimeStep

## Syntax

SapObject.SapModel.LoadCases.ModHistLinear.SetTimeStep

## VB6 Procedure

Function SetTimeStep(ByVal Name As String, ByVal nstep As Long, ByVal DT As Double) As
Long

## Parameters

Name

The name of an existing linear modal history analysis case.

nstep

The number of output time steps.

DT

The output time step size.

## Remarks

This function sets the time step data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseModHistLinearTimeStep()
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

'add linear modal history load case
ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

'set time step data
ret = SapModel.LoadCases.ModHistLinear.SetTimeStep("LCASE1", 120, 0.05)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetTimeStep

# GetDampConstant

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetDampConstant

## VB6 Procedure

Function GetDampConstant(ByVal Name As String, ByRef Damp As Double) As Long


**Parameters**

Name

The name of an existing nonlinear modal history analysis case that has constant damping.

Damp

The constant damping for all modes (0 <= Damp < 1).

**Remarks**

This function retrieves the constant modal damping for all modes assigned to the specified load
case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseModHistNonlinearDampConstant()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim Damp As Double

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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ModHistNonlinear.SetDampConstant("LCASE1", 0.04)

'get constant damping
ret = SapModel.LoadCases.ModHistNonlinear.GetDampType("LCASE1", DampType)


If DampType = 4 Then
ret = SapModel.LoadCases.ModHistNonlinear.GetDampConstant("LCASE1", Damp)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampConstant

# GetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetDampInterpolated

## VB6 Procedure

Function GetDampInterpolated(ByVal Name As String, ByRef DampType As Long, ByRef
NumberItems As Long, ByRef Time() As Double, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case that has interpolated damping.

DampType

This is 5 or 6, indicating the interpolated modal damping type.

```
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
NumberItems

The number of Time and Damp pairs.


Time

This is an array that includes the period or the frequency, depending on the value of the
DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6

Damp

This is an array that includes the damping for the specified period of frequency (0 <= Damp < 1).

**Remarks**

This function retrieves the interpolated modal damping data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseModHistNonlinearDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyTime() As Double
Dim MyDamp() As Double
Dim DampType As Long
Dim NumberItems As Long
Dim Time() As Double
Dim Damp() As Double

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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set interpolated damping
ReDim MyTime(2)
ReDim MyDamp(2)
MyTime(0) = 0.001


MyDamp(0) = 0.1
MyTime(1) = 0.3
MyDamp(1) = 0.03
MyTime(2) = 1
MyDamp(2) = 0.05
ret = SapModel.LoadCases.ModHistNonlinear.SetDampInterpolated("LCASE1", 5, 3,
MyTime, MyDamp)

'get interpolated damping
ret = SapModel.LoadCases.ModHistNonlinear.GetDampType("LCASE1", DampType)
If DampType = 5 or DampType = 6 Then
ret = SapModel.LoadCases.ModHistNonlinear.GetDampInterpolated("LCASE1",
DampType, NumberItems, Time, Damp)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampInterpolated

# GetDampOverrides

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetDampInterpolated

## VB6 Procedure

Function GetDampInterpolated(ByVal Name As String, ByRef NumberItems As Long, ByRef
Mode() As Long, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case.


NumberItems

The number of Mode and Damp pairs.

Mode

This is an array that includes a mode number.

Damp

This is an array that includes the damping for the specified mode (0 <= Damp < 1).

**Remarks**

This function retrieves the modal damping overrides assigned to the specified load case.

The function returns zero if the overrides are successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseModHistNonlinearDampOverrides()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMode() As Long
Dim MyDamp() As Double
Dim NumberItems As Long
Dim Mode() As Long
Dim Damp() As Double

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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ModHistNonlinear.SetDampConstant("LCASE1", 0.04)


'set modal damping overrides
ReDim MyMode(1)
ReDim MyDamp(1)
MyMode(0) = 1
MyDamp(0) = 0.02
MyMode(1) = 2
MyDamp(1) = 0.03
ret = SapModel.LoadCases.ModHistNonlinear.SetDampOverrides("LCASE1", 2, MyMode,
MyDamp)

'get modal damping overrides
ret = SapModel.LoadCases.ModHistNonlinear.GetDampOverrides("LCASE1", NumberItems,
Mode, Damp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampOverrides

# GetDampProportional

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetDampProportional

## VB6 Procedure

Function GetDampProportional(ByVal Name As String, ByRef DampType As Long, ByRef
Dampa As Double, ByRef Dampb As Double, ByRef Dampf1 As Double, ByRef Dampf2 As
Double, ByRef Dampd1 As Double, ByRef Dampd2 As Double) As Long

## Parameters

Name


The name of an existing nonlinear modal history analysis case that has proportional damping.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient.

Dampb

The stiffness proportional damping coefficient.

Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.

**Remarks**

This function retrieves the proportional modal damping data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**


Sub GetCaseModHistNonlinearDampProportional()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim Dampa As Double
Dim Dampb As Double
Dim Dampf1 As Double
Dim Dampf2 As Double
Dim Dampd1 As Double
Dim Dampd2 As Double

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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.ModHistNonlinear.SetDampProportional("LCASE1", 2, 0, 0, 0.1,
1, 0.05, 0.06)

'get proportional damping
ret = SapModel.LoadCases.ModHistNonlinear.GetDampType("LCASE1", DampType)
If DampType >= 1 or DampType <= 3 Then
ret = SapModel.LoadCases.ModHistNonlinear.GetDampProportional("LCASE1",
DampType, Dampa, Dampb, Dampf1, Dampf2, Dampd1, Dampd2)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampProportional

# GetDampType

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetDampType

## VB6 Procedure

Function GetDampType(ByVal Name As String, ByRef DampType As Long) As Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case.

DampType

This is 1, 2, 3, 4, 5 or 6, indicating the modal damping type for the load case.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
4 = Constant damping for all modes
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
## Remarks

This function retrieves the modal damping type for the specified load case.

The function returns zero if the type is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetCaseModHistNonlinearDampType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long


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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'get damping type
ret = SapModel.LoadCases.ModHistNonlinear.GetDampType("LCASE1", DampType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampConstant

GetDampInterpolated

GetDampProportional

GetDampOverrides

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetInitialCase


**VB6 Procedure**

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

**Parameters**

Name

The name of an existing nonlinear modal history analysis case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it continues from the end of
another nonlinear modal time history load case.

If the specified initial case is not a nonlinear modal time history load case, zero initial conditions
are assumed.

**Remarks**

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseModHistNonlinearInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'add nonlinear modal history load cases


ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE2")

'set initial condition
ret = SapModel.LoadCases.ModHistNonlinear.SetInitialCase("LCASE1", "LCASE2")

'get initial condition
ret = SapModel.LoadCases.ModHistNonlinear.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef
TF() As Double, ByRef AT() As Double, ByRef CSys() As String, ByRef Ang() As Double) As
Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.


LoadType

This is an array that includes Load or Accel, indicating the type of each load assigned to the load
case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the time history function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

TF

This is an array that includes the time scale factor of each load assigned to the load case.

AT

This is an array that includes the arrival time of each load assigned to the load case.

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**


Sub GetCaseModHistNonlinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyTF() As Double
Dim MyAT() As Double
Dim MyCSys() As String
Dim MyAng() As Double
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim Func() As String
Dim SF() As Double
Dim TF() As Double
Dim AT() As Double
Dim CSys() As String
Dim Ang() As Double

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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyTF(1)
ReDim MyAT(1)
ReDim MyCSys(1)
ReDim MyAng(1)


MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "RAMPTH"
MySF(0) = 1
MyTF(0) = 1
MyAT(0) = 0
MyCSys(0) = "Global"
MyAng(0) = 0
MyLoadType(1) = "Accel"
MyLoadName(1) = "U2"
MyFunc(1) = "TH-1"
MySF(1) = 2
MyTF(1) = 1.5
MyAT(1) = 10
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.ModHistNonlinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'get load data
ret = SapModel.LoadCases.ModHistNonlinear.GetLoads("LCASE1", NumberLoads,
LoadType, LoadName, Func, SF, TF, AT, CSys, Ang)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetModalCase

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetModalCase

## VB6 Procedure

Function GetModalCase(ByVal Name As String, ByRef ModalCase As String) As Long


**Parameters**

Name

The name of an existing nonlinear modal history analysis case.

ModalCase

This is None or the name of an existing modal analysis case. It specifies the modal load case on
which any mode-type load assignments to the specified load case are based.

**Remarks**

This function retrieves the modal case assigned to the specified load case.

The function returns zero if the modal case is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseModHistNonlinearModalCase()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ModalCase As String

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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'get modal case
ret = SapModel.LoadCases.ModHistNonlinear.GetModalCase("LCASE1", ModalCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetModalCase

# GetSolControlParameters

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetSolControlParameters

## VB6 Procedure

Function GetSolControlParameters(ByVal Name As String, ByRef tstat As Double, ByRef dtmax
As Double, ByRef dtmin As Double, ByRef ftol As Double, ByRef etol As Double, ByRef itmax
As Long, ByRef itmin As Long, ByRef Cf As Double) As Long

## Parameters

Name

The name of an existing nonlinear modal time history analysis case.

tstat

The static period.

dtmax

The maximum substep size.

dtmin

The minimum substep size.

ftol

The relative force convergence tolerance.

etol


The relative energy convergence tolerance.

itmax

The maximum iteration limit.

itmin

The minimum iteration limit.

Cf

The convergence factor.

**Remarks**

This function retrieves the solution control parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseModHistNonlinearSolutionControlParameters()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim tstat As Double
Dim dtmax As Double
Dim dtmin As Double
Dim ftol As Double
Dim etol As Double
Dim itmax As Long
Dim itmin As Long
Dim Cf As Double

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


'add nonlinear modal time history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'get solution control parameters
ret = SapModel.LoadCases.ModHistNonlinear.GetSolControlParameters("LCASE1", tstat,
dtmax, dtmin, ftol, etol, itmax, itmin, Cf)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetSolControlParameters

# GetTimeStep

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.GetTimeStep

## VB6 Procedure

Function GetTimeStep(ByVal Name As String, ByRef nstep As Long, ByRef DT As Double) As
Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case.

nstep

The number of output time steps.

DT

The output time step size.


**Remarks**

This function retrieves the time step data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseModHistNonlinearTimeStep()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim nstep As Long
Dim DT As Double

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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'get time step data
ret = SapModel.LoadCases.ModHistNonlinear.GetTimeStep ("LCASE1", nstep, DT )

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

**See Also**

SetTimeStep


# SetCase

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

## Remarks

This function initializes a nonlinear modal history analysis case. If this function is called for an
existing load case, all items for the case are reset to their default values.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseModHistNonlinear()
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

'add nonlinear modal history load case


ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetDampConstant

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetDampConstant

## VB6 Procedure

Function SetDampConstant(ByVal Name As String, ByVal Damp As Double) As Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case.

Damp

The constant damping for all modes (0 <= Damp < 1).

## Remarks

This function sets constant modal damping for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseModHistNonlinearDampConstant()
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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ModHistNonlinear.SetDampConstant("LCASE1", 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampConstant

# SetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetDampInterpolated

## VB6 Procedure


Function SetDampInterpolated(ByVal Name As String, ByVal DampType As Long, ByVal
NumberItems As Long, ByRef Time() As Double, ByRef Damp() As Double) As Long

**Parameters**

Name

The name of an existing nonlinear modal history analysis case.

DampType

This is 5 or 6, indicating the interpolated modal damping type.

```
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
NumberItems

The number of Time and Damp pairs.

Time

This is an array that includes the period or the frequency, depending on the value of the
DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6

Damp

This is an array that includes the damping for the specified period of frequency (0 <= Damp < 1).

**Remarks**

This function sets interpolated modal damping data for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModHistNonlinearDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyTime() As Double
Dim MyDamp() As Double

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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set interpolated damping
ReDim MyTime(2)
ReDim MyDamp(2)
MyTime(0) = 0.001
MyDamp(0) = 0.1
MyTime(1) = 0.3
MyDamp(1) = 0.03
MyTime(2) = 1
MyDamp(2) = 0.05
ret = SapModel.LoadCases.ModHistNonlinear.SetDampInterpolated("LCASE1", 5, 3,
MyTime, MyDamp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampInterpolated

# SetDampOverrides

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetDampOverrides

## VB6 Procedure


Function SetDampOverrides(ByVal Name As String, ByVal NumberItems As Long, ByRef Mode
() As Long, ByRef Damp() As Double) As Long

**Parameters**

Name

The name of an existing nonlinear modal history analysis case.

NumberItems

The number of Mode and Damp pairs.

Mode

This is an array that includes a mode number.

Damp

This is an array that includes the damping for the specified mode (0 <= Damp < 1).

**Remarks**

This function sets the modal damping overrides for the specified load case.

The function returns zero if the overrides are successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModHistNonlinearDampOverrides()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMode() As Long
Dim MyDamp() As Double

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


'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ModHistNonlinear.SetDampConstant("LCASE1", 0.04)

'set modal damping overrides
ReDim MyMode(1)
ReDim MyDamp(1)
MyMode(0) = 1
MyDamp(0) = 0.02
MyMode(1) = 2
MyDamp(1) = 0.03
ret = SapModel.LoadCases.ModHistNonlinear.SetDampOverrides("LCASE1", 2, MyMode,
MyDamp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampOverrides

# SetDampProportional

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetDampProportional

## VB6 Procedure

Function SetDampProportional(ByVal Name As String, ByVal DampType As Long, ByVal
Dampa As Double, ByVal Dampb As Double, ByVal Dampf1 As Double, ByVal Dampf2 As
Double, ByVal Dampd1 As Double, ByVal Dampd2 As Double) As Long

## Parameters

Name


The name of an existing nonlinear modal history analysis case.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient. This item applies only when DampType = 1.

Dampb

The stiffness proportional damping coefficient. This item applies only when DampType = 1.

Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.

**Remarks**

This function sets proportional modal damping data for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModHistNonlinearDampProportional()
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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.ModHistNonlinear.SetDampProportional("LCASE1", 2, 0, 0, 0.1,
1, 0.05, 0.06)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampProportional

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetInitialCase


**VB6 Procedure**

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

**Parameters**

Name

The name of an existing nonlinear modal history analysis case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it continues from the end of
another nonlinear modal time history load case.

If the specified initial case is not a nonlinear modal time history load case, zero initial conditions
are assumed.

**Remarks**

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseModHistNonlinearInitialCondition()
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

'add nonlinear modal history load cases
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")


ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE2")

'set initial condition
ret = SapModel.LoadCases.ModHistNonlinear.SetInitialCase("LCASE1", "LCASE2")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef TF
() As Double, ByRef AT() As Double, ByRef CSys() As String, ByRef Ang() As Double) As
Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes Load or Accel, indicating the type of each load assigned to the load
case.


LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the time history function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

TF

This is an array that includes the time scale factor of each load assigned to the load case.

AT

This is an array that includes the arrival time of each load assigned to the load case.

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseModHistNonlinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyTF() As Double
Dim MyAT() As Double
Dim MyCSys() As String
Dim MyAng() As Double

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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyTF(1)
ReDim MyAT(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "RAMPTH"
MySF(0) = 1
MyTF(0) = 1
MyAT(0) = 0
MyCSys(0) = "Global"
MyAng(0) = 0
MyLoadType(1) = "Accel"
MyLoadName(1) = "U2"
MyFunc(1) = "TH-1"
MySF(1) = 2
MyTF(1) = 1.5
MyAT(1) = 10


MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.ModHistNonlinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# SetModalCase

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetModalCase

## VB6 Procedure

Function SetModalCase(ByVal Name As String, ByVal ModalCase As String) As Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case.

ModalCase

This is the name of an existing modal load case. It specifies the modal load case on which any
mode-type load assignments to the specified load case are based.

## Remarks

This function sets the modal case for the specified analysis case.


The function returns zero if the modal case is successfully set; otherwise it returns a nonzero
value.

If the specified modal case is not actually a modal case, the program automatically replaces it with
the first modal case it can find. If no modal load cases exist, an error is returned.

**VBA Example**

Sub SetCaseModHistNonlinearModalCase()
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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set modal case
ret = SapModel.LoadCases.ModHistNonlinear.SetModalCase("LCASE1", "MODAL")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetModalCase


# SetSolControlParameters

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetSolControlParameters

## VB6 Procedure

Function SetSolControlParameters(ByVal Name As String, ByVal tstat As Double, ByVal dtmax
As Double, ByVal dtmin As Double, ByVal ftol As Double, ByVal etol As Double, ByVal itmax
As Long, ByVal itmin As Long, ByVal Cf As Double) As Long

## Parameters

Name

The name of an existing nonlinear modal time history analysis case.

tstat

The static period.

dtmax

The maximum substep size.

dtmin

The minimum substep size.

ftol

The relative force convergence tolerance.

etol

The relative energy convergence tolerance.

itmax

The maximum iteration limit.

itmin

The minimum iteration limit.

Cf

The convergence factor.


**Remarks**

This function sets the solution control parameters for the specified load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseModHistNonlinearSolutionControlParameters()
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

'add nonlinear modal time history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set solution control parameters
ret = SapModel.LoadCases.ModHistNonlinear.SetSolControlParameters("LCASE1", 0.1,
0.001, 0.000001, 0.00002, 0.00003, 80, 10, 1.5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetSolControlParameters

# SetTimeStep

## Syntax

SapObject.SapModel.LoadCases.ModHistNonlinear.SetTimeStep

## VB6 Procedure

Function SetTimeStep(ByVal Name As String, ByVal nstep As Long, ByVal DT As Double) As
Long

## Parameters

Name

The name of an existing nonlinear modal history analysis case.

nstep

The number of output time steps.

DT

The output time step size.

## Remarks

This function sets the time step data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseModHistNonlinearTimeStep()
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

'add nonlinear modal history load case
ret = SapModel.LoadCases.ModHistNonlinear.SetCase("LCASE1")

'set time step data
ret = SapModel.LoadCases.ModHistNonlinear.SetTimeStep("LCASE1", 120, 0.05)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetTimeStep

# GetDirectionalFactors

## Syntax

SapObject.SapModel.LoadCases.Moving.GetDirectionalFactors

## VB6 Procedure

Function GetDirectionalFactors(ByVal Name As String, ByRef Vertical As Double, ByRef
Braking As Double, ByRef Centrifugal As Double) As Integer

## Parameters

Name


The name of an existing moving load case.

Vertical

The moving load directional factor for vertical load.

Braking

The moving load directional factor.

Centrifugal

The moving directional factor for centrifugal load.

**Remarks**

This function retrieves the directional factors for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetDirectionalFactors()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Vertical As Double
Dim Braking As Double
Dim Centrifugal As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'set directional factors


ret = SapModel.LoadCases.Moving.SetDirectionalFactors("LCASE1", 1, 0.7, 0.4)

'get directional factors
ret = SapModel.LoadCases.Moving.GetDirectionalFactors("LCASE1", 1, Vertical, Braking,
Centrifugal)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

## See Also

SetDirectionalFactors

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.Moving.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing moving load load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks


This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseMovingInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.Moving.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

SetInitialCase


# GetLanesLoaded

## Syntax

SapObject.SapModel.LoadCases.Moving.GetLanesLoaded

## VB6 Procedure

Function GetLanesLoaded(ByVal Name As String, ByVal LoadNumber As Long, ByRef
NumberItems As Long, ByRef MyName() As String) As Long

## Parameters

Name

The name of an existing moving load case.

LoadNumber

The load assignment number.

NumberItems

The number of lanes loaded for the specified load assignment number.

MyName

This is an array that includes the name of each lane loaded for the specified load assignment
number.

## Remarks

This function retrieves the lanes loaded data for a specified load assignment number in a specified
load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetCaseMovingLanesLoaded()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMyClass() As String
Dim MySF() As Double
Dim MyMin() As Double
Dim MyMax() As Double
Dim MyMyName() As String


Dim NumberItems As Long
Dim MyName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'set load data
ReDim MyMyClass(1)
ReDim MySF(1)
ReDim MyMin(1)
ReDim MyMax(1)
MyMyClass(0) = "VECL1"
MySF(0) = 1.5
MyMin(0) = 1
MyMax(0) = 1
MyMyClass(1) = "VECL1"
MySF(1) = 0.8
MyMin(1) = 0
MyMax(1) = 0
ret = SapModel.LoadCases.Moving.SetLoads("LCASE1", 2, MyMyClass, MySF, MyMin,
MyMax)

'set lanes loaded data for first load assignment
ReDim MyMyName(0)
MyMyName(0) = "LANE1"
ret = SapModel.LoadCases.Moving.SetLanesLoaded("LCASE1", 1, 1, MyMyName)

'get lanes loaded data for first load assignment
ret = SapModel.LoadCases.Moving.GetLanesLoaded("LCASE1", 1, NumberItems, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLanesLoaded

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.Moving.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef MyClass() As
String, ByRef SF() As Double, ByRef Min() As Double, ByRef Max() As Double) As Long

## Parameters

Name

The name of an existing moving load case.

NumberLoads

The number of loads assigned to the specified analysis case.

MyClass

This is an array that includes the vehicle class for each load assigned to the load case.

SF

This is an array that includes the scale factor for each load assigned to the load case.

Min

This is an array that includes the minimum number of lanes loaded for each load assigned to the
load case.

Max

This is an array that includes the maximum number of lanes loaded for each load assigned to the
load case. This item must be 0, or it must be greater than or equal to Min. If this item is 0, all
available lanes are loaded.


**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseMovingLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMyClass() As String
Dim MySF() As Double
Dim MyMin() As Double
Dim MyMax() As Double
Dim NumberLoads As Long
Dim MyClass() As String
Dim SF() As Double
Dim Min() As Double
Dim Max() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'set load data
ReDim MyMyClass(1)
ReDim MySF(1)
ReDim MyMin(1)
ReDim MyMax(1)
MyMyClass(0) = "VECL1"
MySF(0) = 1.5
MyMin(0) = 1
MyMax(0) = 1
MyMyClass(1) = "VECL1"
MySF(1) = 0.8


MyMin(1) = 0
MyMax(1) = 0
ret = SapModel.LoadCases.Moving.SetLoads("LCASE1", 2, MyMyClass, MySF, MyMin,
MyMax)

'get load data
ret = SapModel.LoadCases.Moving.GetLoads("LCASE1", NumberLoads, MyClass, SF, Max,
Min)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetMultiLaneSF

## Syntax

SapObject.SapModel.LoadCases.Moving.GetMultiLaneSF

## VB6 Procedure

Function GetMultiLaneSF(ByVal Name As String, ByRef NumberItems As Long, ByRef SF() As
Double) As Long

## Parameters

Name

The name of an existing moving load case.

NumberItems

The number of lanes loaded up to which reduction scale factors are provided.

SF


This is an array that includes the reduction scale factor for the number of lanes loaded from 1 up
to NumberItems.

**Remarks**

This function retrieves the multilane scale factor data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseMovingMultiLaneSF()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MySF() As Double
Dim NumberItems As Long
Dim SF() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'set multilane scale factor data
ReDim MySF(1)
MySF(0) = 1.2
MySF(1) = 0.8
ret = SapModel.LoadCases.Moving.SetMultiLaneSF("LCASE1", 2, MySF)

'get multilane scale factor data
ret = SapModel.LoadCases.Moving.GetMultiLaneSF("LCASE1", NumberItems, SF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetMultiLaneSF

# SetCase

## Syntax

SapObject.SapModel.LoadCases.Moving.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case then that case is modified,
otherwise, a new case is added.

## Remarks

This function initializes a moving load load case. If this function is called for an existing load
case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseMoving()
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

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetDirectionalFactors

## Syntax

SapObject.SapModel.LoadCases.Moving.SetDirectionalFactors

## VB6 Procedure

Function SetDirectionalFactors(ByVal Name As String, ByVal Vertical As Double, ByVal
Braking As Double, ByVal Centrifugal As Double) As Integer

## Parameters

Name


The name of an existing moving load case.

Vertical

The moving load directional factor for vertical load.

Braking

The moving load directional factor.

Centrifugal

The moving directional factor for centrifugal load.

**Remarks**

This function sets the directional factors for the specified load case. Calling this function is
optional. By default, the directional factors are set to Vertical = 1, Braking = 0, and Centrifugal =
0 when the moving load case is defied or re-defined. If this function is called, the three directional
factors must be nonnegative, and at least one must be positive.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub SetDirectionalFactors()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Vertical As Double
Dim Braking As Double
Dim Centrifugal As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")


'set directional factors
Vertical = 1.0

Braking - 0.7

Centrifugal = 0.4

ret = SapModel.LoadCases.Moving.SetDirectionalFactors("LCASE1", Vertical, Braking,
Centrifugal)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

## See Also

GetDirectionalFactors

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.Moving.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing moving load load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.


If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseMovingInitialCondition()
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

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add moving load load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.Moving.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**


Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLanesLoaded

## Syntax

SapObject.SapModel.LoadCases.Moving.SetMultiLaneSF

## VB6 Procedure

Function SetMultiLaneSF(ByVal Name As String, ByVal LoadNumber As Long, ByVal
NumberItems As Long, ByRef MyName() As String) As Long

## Parameters

Name

The name of an existing moving load case.

LoadNumber

The load assignment number.

NumberItems

The number of lanes loaded for the specified load assignment number.

MyName

This is an array that includes the name of each lane loaded for the specified load assignment
number.

## Remarks

This function sets the lanes loaded data for a specified load assignment number in a specified load
case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

## VBA Example


Sub SetCaseMovingLanesLoaded()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMyClass() As String
Dim MySF() As Double
Dim MyMin() As Double
Dim MyMax() As Double
Dim MyMyName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'set load data
ReDim MyMyClass(1)
ReDim MySF(1)
ReDim MyMin(1)
ReDim MyMax(1)
MyMyClass(0) = "VECL1"
MySF(0) = 1.5
MyMin(0) = 1
MyMax(0) = 1
MyMyClass(1) = "VECL1"
MySF(1) = 0.8
MyMin(1) = 0
MyMax(1) = 0
ret = SapModel.LoadCases.Moving.SetLoads("LCASE1", 2, MyMyClass, MySF, MyMin,
MyMax)

'set lanes loaded data for first load assignment
ReDim MyMyName(0)
MyMyName(0) = "LANE1"
ret = SapModel.LoadCases.Moving.SetLanesLoaded("LCASE1", 1, 1, MyMyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLanesLoaded

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.Moving.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef MyClass() As
String, ByRef SF() As Double, ByRef Min() As Double, ByRef Max() As Double) As Long

## Parameters

Name

The name of an existing moving load case.

NumberLoads

The number of loads assigned to the specified analysis case.

MyClass

This is an array that includes the vehicle class for each load assigned to the load case.

SF

This is an array that includes the scale factor for each load assigned to the load case.

Min

This is an array that includes the minimum number of lanes loaded for each load assigned to the
load case.

Max


This is an array that includes the maximum number of lanes loaded for each load assigned to the
load case. This item must be 0, or it must be greater than or equal to Min. If this item is 0, all
available lanes are loaded.

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseMovingLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMyClass() As String
Dim MySF() As Double
Dim MyMin() As Double
Dim MyMax() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'set load data
ReDim MyMyClass(1)
ReDim MySF(1)
ReDim MyMin(1)
ReDim MyMax(1)
MyMyClass(0) = "VECL1"
MySF(0) = 1.5
MyMin(0) = 1
MyMax(0) = 1
MyMyClass(1) = "VECL1"
MySF(1) = 0.8


MyMin(1) = 0
MyMax(1) = 0
ret = SapModel.LoadCases.Moving.SetLoads("LCASE1", 2, MyMyClass, MySF, MyMin,
MyMax)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# SetMultiLaneSF

## Syntax

SapObject.SapModel.LoadCases.Moving.SetMultiLaneSF

## VB6 Procedure

Function SetMultiLaneSF(ByVal Name As String, ByVal NumberItems As Long, ByRef SF() As
Double) As Long

## Parameters

Name

The name of an existing moving load case.

NumberItems

The number of lanes loaded up to which reduction scale factors are provided (NumberItems >= 1).

SF

This is an array that includes the reduction scale factor for the number of lanes loaded from 1 up
to NumberItems.


**Remarks**

This function sets the multilane scale factor data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseMovingMultiLaneSF()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MySF() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
SapModel.File.OpenFile("C:\SapAPI\Example 1-030.SDB")

'add moving load case
ret = SapModel.LoadCases.Moving.SetCase("LCASE1")

'set multilane scale factor data
ReDim MySF(1)
MySF(0) = 1.2
MySF(1) = 0.8
ret = SapModel.LoadCases.Moving.SetMultiLaneSF("LCASE1", 2, MySF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetMultiLaneSF

# GetDampConstant

## Syntax

SapObject.SapModel.LoadCases.PSD.GetDampConstant

## VB6 Procedure

Function GetDampConstant(ByVal Name As String, ByRef HysConMassCoeff As Double,
ByRef HysConStiffCoeff As Double) As Long

## Parameters

Name

The name of an existing power spectral density analysis case that has constant damping.

HysConMassCoeff

The mass proportional damping coefficient.

HysConStiffCoeff

The stiffness proportional damping coefficient.

## Remarks

This function retrieves the constant hysteretic damping for all frequencies assigned to the
specified load case.

The function returns zero if the damping is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCasePSDDampConstant()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim HysConMassCoeff As Double
Dim HysConStiffCoeff As Double


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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.PSD.SetDampConstant("LCASE1", 0.8, 0.04)

'get constant damping
ret = SapModel.LoadCases.PSD.GetDampType("LCASE1", DampType)
If DampType = 1 Then
ret = SapModel.LoadCases.PSD.GetDampConstant("LCASE1", HysConMassCoeff,
HysConStiffCoeff)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampConstant

# GetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.PSD.GetDampInterpolated


**VB6 Procedure**

Function GetDampInterpolated(ByVal Name As String, ByRef HysIntFreqUnits As Long, ByRef
HysIntNumFreqs As Long, ByRef HysIntFreq() As Double, ByRef HysIntMassCoeff() As
Double, ByRef HysIntStiffCoeff() As Double) As Long

**Parameters**

Name

The name of an existing power spectral density analysis case that has interpolated damping.

HysIntFreqUnits

This is 1 or 2, indicating the units for the frequency.

```
1 = Hz [cyc/s]
2 = RPM
```
HysIntNumFreqs

The number of sets of frequency, mass coefficient and stiffness coefficient data.

HysIntFreq

This is an array of frequencies. The frequency is either in Hz or RPM depending on the value of
HysIntFreqUnits.

HysIntMassCoeff

This is an array that includes the mass proportional damping coefficient.

HysIntStiffCoeff

This is an array that includes the stiffness proportional damping coefficient.

**Remarks**

This function retrieves the interpolated hysteretic damping by frequency assigned to the specified
load case.

The function returns zero if the damping is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCasePSDDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyHysIntFreq() As Double


Dim MyHysIntMassCoeff() As Double
Dim MyHysIntStiffCoeff() As Double
Dim DampType As Long
Dim HysIntFreqUnits As Long
Dim HysIntNumFreqs As Long
Dim HysIntFreq() As Double
Dim HysIntMassCoeff() As Double
Dim HysIntStiffCoeff() As Double

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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'set interpolated damping
ReDim MyHysIntFreq(2)
ReDim MyHysIntMassCoeff(2)
ReDim MyHysIntStiffCoeff(2)
MyHysIntFreq(0) = 1
MyHysIntMassCoeff(0) = 0.6
MyHysIntStiffCoeff(0) = 0.04
MyHysIntFreq(1) = 10
MyHysIntMassCoeff(1) = 0.7
MyHysIntStiffCoeff(1) = 0.05
MyHysIntFreq(2) = 100
MyHysIntMassCoeff(2) = 0.8
MyHysIntStiffCoeff(2) = 0.08
ret = SapModel.LoadCases.PSD.SetDampInterpolated("LCASE1", 2, 3, MyHysIntFreq,
MyHysIntMassCoeff, MyHysIntStiffCoeff)

'get interpolated damping
ret = SapModel.LoadCases.PSD.GetDampType("LCASE1", DampType)
If DampType = 2 Then
ret = SapModel.LoadCases.PSD.GetDampInterpolated("LCASE1", HysIntFreqUnits,
HysIntNumFreqs, HysIntFreq, HysIntMassCoeff, HysIntStiffCoeff)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampInterpolated

# GetDampType

## Syntax

SapObject.SapModel.LoadCases.PSD.GetDampType

## VB6 Procedure

Function GetDampType(ByVal Name As String, ByRef DampType As Long) As Long

## Parameters

Name

The name of an existing power spectral density analysis case.

DampType

This is 1 or 2, indicating the hysteretic damping type for the load case.

```
1 = Constant hysteretic damping for all frequencies
2 = Interpolated hysteretic damping by frequency
```
## Remarks

This function retrieves the hysteretic damping type for the specified load case.

The function returns zero if the type is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetCasePSDDampType()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long

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

'add response spectrum load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'get damping type
ret = SapModel.LoadCases.PSD.GetDampType("LCASE1", DampType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampConstant

GetDampInterpolated

# GetFreqData

## Syntax

SapObject.SapModel.LoadCases.PSD.GetFreqData


**VB6 Procedure**

Function GetFreqData(ByVal Name As String, ByRef FreqFirst As Double, ByRef FreqLast As
Double, ByRef FreqNumIncs As Long, ByRef FreqAddModal As Boolean, ByRef
FreqAddModalDev As Boolean, ByRef FreqAddSpecified As Boolean, ByRef
FreqNumModalDev As Long, ByRef FreqModalDev() As Double, ByRef FreqNumSpecified As
Long, ByRef FreqSpecified() As Double) As Long

**Parameters**

Name

The name of an existing power spectral density analysis case.

FreqFirst

The first frequency. [cyc/s]

FreqLast

The last frequency. [cyc/s]

FreqNumIncs

The number of frequency increments.

FreqAddModal

If this item is True, modal frequencies are added.

FreqAddModalDev

If this item is True, signed fractional deviations from modal frequencies are added.

FreqAddSpecified

If this item is True, specified frequencies are added.

ModalCase

This is the name of an existing modal load case. It specifies the modal load case on which modal
frequencies and modal frequency deviations are based.

FreqNumModalDev

The number of signed fractional deviations from modal frequencies that are added. This item
applies only when FreqAddModalDev = True.

FreqModalDev

This is an array that includes the added signed fractional deviations from modal frequencies. This
item applies only when FreqAddModalDev = True.

FreqNumSpecified


The number of specified frequencies that are added. This item applies only when
FreqAddSpecified = True.

FreqSpecified

This is an array that includes the added specified frequencies. This item applies only when
FreqAddModalDev = True.

**Remarks**

This function retrieves the frequency data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCasePSDFreqData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyFreqModalDev() As Double
Dim MyFreqSpecified() As Double
Dim FreqFirst As Double
Dim FreqLast As Double
Dim FreqNumIncs As Long
Dim FreqAddModal As Boolean
Dim FreqAddModalDev As Boolean
Dim FreqAddSpecified As Boolean
Dim ModalCase As String
Dim FreqNumModalDev As Long
Dim FreqModalDev() As Double
Dim FreqNumSpecified As Long
Dim FreqSpecified() As Double

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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")


'set frequency data
ReDim MyFreqModalDev(1)
ReDim MyFreqSpecified(1)
MyFreqModalDev(0) = -0.1
MyFreqModalDev(1) = 0.2
MyFreqSpecified(0) = 1.2
MyFreqSpecified(1) = 11.4
ret = SapModel.LoadCases.PSD.SetFreqData("LCASE1", .6, 20.6, 10, True, True, True,
"MODAL", 2, MyFreqModalDev, 2, MyFreqSpecified)

'get frequency data
ret = SapModel.LoadCases.PSD.GetFreqData("LCASE1", FreqFirst, FreqLast, FreqNumIncs,
FreqAddModal, FreqAddModalDev, FreqAddSpecified, ModalCase, FreqNumModalDev,
FreqModalDev, FreqNumSpecified, FreqSpecified)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetFreqData

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.PSD.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing power spectral density analysis case.


InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCasePSDInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.PSD.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.PSD.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef
PhaseAngle() As Double, ByRef CSys() As String, ByRef Ang() As Double) As Long

## Parameters

Name

The name of an existing power spectral density analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func


This is an array that includes the name of the power spectral density function associated with each
load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

PhaseAngle

This is an array that includes the phase angle. [deg]

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCasePSDLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyPhaseAngle() As Double
Dim MyCSys() As String
Dim MyAng() As Double
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim Func() As String
Dim SF() As Double
Dim PhaseAngle() As Double


Dim CSys() As String
Dim Ang() As Double

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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyPhaseAngle(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "UNIFPSD"
MySF(0) = 1.5
MyPhaseAngle(0) = 90
MyLoadType(1) = "Accel"
MyLoadName(1) = "U3"
MyFunc(1) = "UNIFPSD"
MySF(1) = 1
MyPhaseAngle(1) = 90
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.PSD.SetLoads("LCASE1", 2, MyLoadType, MyLoadName,
MyFunc, MySF, MyPhaseAngle, MyCSys, MyAng)

'get load data
ret = SapModel.LoadCases.PSD.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, Func, SF, PhaseAngle, CSys, Ang)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# SetCase

## Syntax

SapObject.SapModel.LoadCases.PSD.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

## Remarks

This function initializes a power spectral density analysis case. If this function is called for an
existing load case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCasePSD()
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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetDampConstant

## Syntax

SapObject.SapModel.LoadCases.PSD.SetDampConstant

## VB6 Procedure

Function SetDampConstant(ByVal Name As String, ByVal HysConMassCoeff As Double, ByVal
HysConStiffCoeff As Double) As Long

## Parameters

Name

The name of an existing power spectral density analysis case.

HysConMassCoeff


The mass proportional damping coefficient.

HysConStiffCoeff

The stiffness proportional damping coefficient.

**Remarks**

This function sets constant hysteretic damping for all frequencies for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCasePSDDampConstant()
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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.PSD.SetDampConstant("LCASE1", 0.8, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampConstant

# SetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.PSD.SetDampInterpolated

## VB6 Procedure

Function SetDampInterpolated(ByVal Name As String, ByVal HysIntFreqUnits As Long, ByVal
HysIntNumFreqs As Long, ByRef HysIntFreq() As Double, ByRef HysIntMassCoeff() As
Double, ByRef HysIntStiffCoeff() As Double) As Long

## Parameters

Name

The name of an existing power spectral density analysis case.

HysIntFreqUnits

This is either 1 or 2, indicating the units for the frequency.

```
1 = Hz [cyc/s]
2 = RPM
```
HysIntNumFreqs

The number of sets of frequency, mass coefficient and stiffness coefficient data.

HysIntFreq

This is an array of frequencies. The frequency is either in Hz or RPM depending on the value of
HysIntFreqUnits.

HysIntMassCoeff

This is an array that includes the mass proportional damping coefficient.

HysIntStiffCoeff

This is an array that includes the stiffness proportional damping coefficient.


**Remarks**

This function sets interpolated hysteretic damping by frequency for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCasePSDDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyHysIntFreq() As Double
Dim MyHysIntMassCoeff() As Double
Dim MyHysIntStiffCoeff() As Double

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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'set interpolated damping
ReDim MyHysIntFreq(2)
ReDim MyHysIntMassCoeff(2)
ReDim MyHysIntStiffCoeff(2)
MyHysIntFreq(0) = 1
MyHysIntMassCoeff(0) = 0.6
MyHysIntStiffCoeff(0) = 0.04
MyHysIntFreq(1) = 10
MyHysIntMassCoeff(1) = 0.7
MyHysIntStiffCoeff(1) = 0.05
MyHysIntFreq(2) = 100
MyHysIntMassCoeff(2) = 0.8
MyHysIntStiffCoeff(2) = 0.08
ret = SapModel.LoadCases.PSD.SetDampInterpolated("LCASE1", 2, 3, MyHysIntFreq,
MyHysIntMassCoeff, MyHysIntStiffCoeff)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampInterpolated

# SetFreqData

## Syntax

SapObject.SapModel.LoadCases.PSD.SetFreqData

## VB6 Procedure

Function SetFreqData(ByVal Name As String, ByVal FreqFirst As Double, ByVal FreqLast As
Double, ByVal FreqNumIncs As Long, ByVal FreqAddModal As Boolean, ByVal
FreqAddModalDev As Boolean, ByVal FreqAddSpecified As Boolean, ByVal
FreqNumModalDev As Long, ByRef FreqModalDev() As Double, ByVal FreqNumSpecified As
Long, ByRef FreqSpecified() As Double) As Long

## Parameters

Name

The name of an existing power spectral density analysis case.

FreqFirst

The first frequency. [cyc/s]

FreqLast

The last frequency. [cyc/s]

FreqNumIncs

The number of frequency increments.

FreqAddModal


If this item is True, modal frequencies are added.

FreqAddModalDev

If this item is True, signed fractional deviations from modal frequencies are added.

FreqAddSpecified

If this item is True, specified frequencies are added.

ModalCase

This is the name of an existing modal load case. It specifies the modal load case on which modal
frequencies and modal frequency deviations are based.

FreqNumModalDev

The number of signed fractional deviations from modal frequencies that are added. This item
applies only when FreqAddModalDev = True.

FreqModalDev

This is an array that includes the added signed fractional deviations from modal frequencies. This
item applies only when FreqAddModalDev = True.

FreqNumSpecified

The number of specified frequencies that are added. This item applies only when
FreqAddSpecified = True.

FreqSpecified

This is an array that includes the added specified frequencies. This item applies only when
FreqAddModalDev = True.

**Remarks**

This function sets the frequency data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCasePSDFreqData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyFreqModalDev() As Double
Dim MyFreqSpecified() As Double

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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'set frequency data
ReDim MyFreqModalDev(1)
ReDim MyFreqSpecified(1)
MyFreqModalDev(0) = -0.1
MyFreqModalDev(1) = 0.2
MyFreqSpecified(0) = 1.2
MyFreqSpecified(1) = 11.4
ret = SapModel.LoadCases.PSD.SetFreqData("LCASE1", .6, 20.6, 10, True, True, True,
"MODAL", 2, MyFreqModalDev, 2, MyFreqSpecified)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetFreqData

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.PSD.SetInitialCase


**VB6 Procedure**

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

**Parameters**

Name

The name of an existing power spectral density analysis case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCasePSDInitialCondition()
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

'add static nonlinear load case


ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.PSD.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.PSD.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef
PhaseAngle() As Double, ByRef CSys() As String, ByRef Ang() As Double) As Long

## Parameters

Name

The name of an existing power spectral density analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType


This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the power spectral density function associated with each
load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

PhaseAngle

This is an array that includes the phase angle. [deg]

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies pnly when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCasePSDLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyPhaseAngle() As Double
Dim MyCSys() As String
Dim MyAng() As Double

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

'add power spectral density load case
ret = SapModel.LoadCases.PSD.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyPhaseAngle(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "UNIFPSD"
MySF(0) = 1.5
MyPhaseAngle(0) = 90
MyLoadType(1) = "Accel"
MyLoadName(1) = "U3"
MyFunc(1) = "UNIFPSD"
MySF(1) = 1
MyPhaseAngle(1) = 90
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.PSD.SetLoads("LCASE1", 2, MyLoadType, MyLoadName,
MyFunc, MySF, MyPhaseAngle, MyCSys, MyAng)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# GetDampConstant

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetDampConstant

## VB6 Procedure

Function GetDampConstant(ByVal Name As String, ByRef Damp As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case that has constant damping.

Damp

The constant damping for all modes (0 <= Damp < 1).

## Remarks

This function retrieves the constant modal damping for all modes assigned to the specified load
case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCaseResponseSpectrumDampConstant()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim Damp As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant("LCASE1", 0.04)

'get constant damping
ret = SapModel.LoadCases.ResponseSpectrum.GetDampType("LCASE1", DampType)
If DampType = 4 Then
ret = SapModel.LoadCases.ResponseSpectrum.GetDampConstant("LCASE1", Damp)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

SetDampConstant


# GetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetDampInterpolated

## VB6 Procedure

Function GetDampInterpolated(ByVal Name As String, ByRef DampType As Long, ByRef
NumberItems As Long, ByRef Time() As Double, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case that has interpolated damping.

DampType

This is either 5 or 6, indicating the interpolated modal damping type.

```
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
NumberItems

The number of Time and Damp pairs.

Time

This is an array that includes the period or the frequency depending on the value of the DampType
item. [s] for DampType = 5 and [cyc/s] for DampType = 6

Damp

This is an array that includes the damping for the specified period of frequency (0 <= Damp < 1).

## Remarks

This function retrieves the interpolated modal damping data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCaseResponseSpectrumDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim MyTime() As Double
Dim MyDamp() As Double
Dim DampType As Long
Dim NumberItems As Long
Dim Time() As Double
Dim Damp() As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set interpolated damping
ReDim MyTime(2)
ReDim MyDamp(2)
MyTime(0) = 0.001
MyDamp(0) = 0.1
MyTime(1) = 0.3
MyDamp(1) = 0.03
MyTime(2) = 1
MyDamp(2) = 0.05
ret = SapModel.LoadCases.ResponseSpectrum.SetDampInterpolated("LCASE1", 5, 3,
MyTime, MyDamp)

'get interpolated damping
ret = SapModel.LoadCases.ResponseSpectrum.GetDampType("LCASE1", DampType)
If DampType = 5 or DampType = 6 Then
ret = SapModel.LoadCases.ResponseSpectrum.GetDampInterpolated("LCASE1",
DampType, NumberItems, Time, Damp)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampInterpolated

# GetDampOverrides

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetDampInterpolated

## VB6 Procedure

Function GetDampInterpolated(ByVal Name As String, ByRef NumberItems As Long, ByRef
Mode() As Long, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case.

NumberItems

The number of Mode and Damp pairs.

Mode

This is an array that includes a mode number.

Damp

This is an array that includes the damping for the specified mode (0 <= Damp < 1).

## Remarks

This function retrieves the modal damping overrides assigned to the specified load case.

The function returns zero if the overrides are successfully retrieved; otherwise it returns a nonzero
value.


**VBA Example**

Sub GetCaseResponseSpectrumDampOverrides()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMode() As Long
Dim MyDamp() As Double
Dim NumberItems As Long
Dim Mode() As Long
Dim Damp() As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant("LCASE1", 0.04)

'set modal damping overrides
ReDim MyMode(1)
ReDim MyDamp(1)
MyMode(0) = 1
MyDamp(0) = 0.02
MyMode(1) = 2
MyDamp(1) = 0.03
ret = SapModel.LoadCases.ResponseSpectrum.SetDampOverrides("LCASE1", 2, MyMode,
MyDamp)

'get modal damping overrides
ret = SapModel.LoadCases.ResponseSpectrum.GetDampOverrides("LCASE1",
NumberItems, Mode, Damp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampOverrides

# GetDampProportional

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetDampProportional

## VB6 Procedure

Function GetDampProportional(ByVal Name As String, ByRef DampType As Long, ByRef
Dampa As Double, ByRef Dampb As Double, ByRef Dampf1 As Double, ByRef Dampf2 As
Double, ByRef Dampd1 As Double, ByRef Dampd2 As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case that has proportional damping.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient.

Dampb

The stiffness proportional damping coefficient.

Dampf1


This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.

**Remarks**

This function retrieves the proportional modal damping data assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseResponseSpectrumDampProportional()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long
Dim Dampa As Double
Dim Dampb As Double
Dim Dampf1 As Double
Dim Dampf2 As Double
Dim Dampd1 As Double
Dim Dampd2 As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.ResponseSpectrum.SetDampProportional("LCASE1", 2, 0, 0, 0.1,
1, 0.05, 0.06)

'get proportional damping
ret = SapModel.LoadCases.ResponseSpectrum.GetDampType("LCASE1", DampType)
If DampType >= 1 or DampType <= 3 Then
ret = SapModel.LoadCases.ResponseSpectrum.GetDampProportional("LCASE1",
DampType, Dampa, Dampb, Dampf1, Dampf2, Dampd1, Dampd2)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampProportional

# GetDampType

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetDampType

## VB6 Procedure

Function GetDampType(ByVal Name As String, ByRef DampType As Long) As Long


**Parameters**

Name

The name of an existing response spectrum load case.

DampType

This is 1, 2, 3, 4, 5 or 6, indicating the modal damping type for the load case.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
4 = Constant damping for all modes
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
**Remarks**

This function retrieves the modal damping type for the specified load case.

The function returns zero if the type is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseResponseSpectrumDampType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'get damping type


ret = SapModel.LoadCases.ResponseSpectrum.GetDampType("LCASE1", DampType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampConstant

GetDampInterpolated

GetDampProportional

GetDampOverrides

# GetDiaphragmEccentricityOverride

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetDiaphragmEccentricityOverride

## VB6 Procedure

Function GetDiaphragmEccentricityOverride(ByVal Name As String, ByRef Num As Long,
ByRef Diaph() As String, ByRef Eccen() As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case.

Num

The number of diaphragm eccentricity overrides for the specified load case.

Diaph

This is an array that includes the names of the diaphragms that have eccentricity overrides.


Eccen

This is an array that includes the eccentricity applied to each diaphragm. [L]

**Remarks**

This function retrieves the diaphragm eccentricity overrides for a response spectrum load case.

The function returns zero if the overrides are successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetResponseSpectrumDiaphragmEccentricityOverride()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Diaph() As String
Dim Eccen() As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")


'assign diaphragm eccentricity override
ret = SapModel.LoadCases.ResponseSpectrum.SetDiaphragmEccentricityOverride
("LCASE1", "Diaph1", 50)

'get diaphragm eccentricity override
ret = SapModel.LoadCases.ResponseSpectrum.GetDiaphragmEccentricityOverride
("LCASE1", Num, Diaph, Eccen)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDiaphragmEccentricityOverride

GetSpecialRigidDiaphragmList

# GetDirComb

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetDirComb

## VB6 Procedure

Function GetDirComb(ByVal Name As String, ByRef MyType As Long, ByRef SF As Double)
As Long

## Parameters

Name

The name of an existing response spectrum load case.

MyType

This is 1, 2, or 3, indicating the directional combination option.


### 1 = SRSS

### 2 = ABS

### 3 = CQC3

### SF

This item applies only when MyType = 2. It is the ABS scale factor.

**Remarks**

This function retrieves the directional combination option assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseResponseSpectrumDirComb()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyType As Long
Dim SF As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'get directional combination option
ret = SapModel.LoadCases.ResponseSpectrum.GetDirComb("LCASE1", MyType, SF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Removed Modified SRSS (Chinese) directional combination option in version 14.00.

Added CQC3 directional combination option in version 14.20.

## See Also

SetDirComb

# GetEccentricity

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetEccentricity

## VB6 Procedure

Function GetEccentricity(ByVal Name As String, ByRef Eccen As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case.

Eccen

The eccentricity ratio that applies to all diaphragms.

## Remarks

This function retrieves the eccentricity ratio that applies to all diaphragms for the specified load
case.

The function returns zero if the ratio is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetCaseResponseSpectrumEccentricity()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim Eccen As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'get eccentricity ratio
ret = SapModel.LoadCases.ResponseSpectrum.GetEccentricity("LCASE1", Eccen)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetEccentricity

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetLoads

## VB6 Procedure


Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadName()
As String, ByRef Func() As String, ByRef SF() As Double, ByRef CSys() As String, ByRef Ang()
As Double) As Long

**Parameters**

Name

The name of an existing response spectrum load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadName

This is an array that includes U1, U2, U3, R1, R2 or R3, indicating the direction of the load.

Func

This is an array that includes the name of the response spectrum function associated with each
load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseResponseSpectrumLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyCSys() As String
Dim MyAng() As Double
Dim NumberLoads As Long
Dim LoadName() As String
Dim Func() As String
Dim SF() As Double
Dim CSys() As String
Dim Ang() As Double

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

'add UBC97 RS function
ret = SapModel.Func.FuncRS.SetUBC97("RS-1", 0.36, 0.54, 0.04)

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set load data
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadName(0) = "U1"
MyFunc(0) = "RS-1"
MySF(0) = 386
MyCSys(0) = "Global"
MyAng(0) = 10
MyLoadName(1) = "U2"
MyFunc(1) = "RS-1"
MySF(1) = 386
ret = SapModel.LoadCases.ResponseSpectrum.SetLoads("LCASE1", 2, MyLoadName,
MyFunc, MySF, MyCSys, MyAng)

'get load data
ret = SapModel.LoadCases.ResponseSpectrum.GetLoads("LCASE1", NumberLoads,
LoadName, Func, SF, CSys, Ang)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetModalCase

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.GetModalCase

## VB6 Procedure

Function GetModalCase(ByVal Name As String, ByRef ModalCase As String) As Long

## Parameters

Name

The name of an existing response spectrum load case.

ModalCase

This is None or the name of an existing modal analysis case. It specifies the modal load case on
which any mode-type load assignments to the specified load case are based.

## Remarks

This function retrieves the modal case assigned to the specified load case.

The function returns zero if the modal case is successfully retrieved; otherwise it returns a nonzero
value.


## VBA Example

Sub GetCaseResponseSpectrumModalCase()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ModalCase As String

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'get modal case
ret = SapModel.LoadCases.ResponseSpectrum.GetModalCase("LCASE1", ModalCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetModalCase

# GetModalComb_1


**Syntax**

SapObject.SapModel.LoadCases.ResponseSpectrum.GetModalComb_1

**VB6 Procedure**

Function GetModalComb_1(ByVal Name As String, ByRef MyType As Long, ByRef F1 As
Double, ByRef F2 As Double, ByRef PeriodicRigidCombType As Long, ByRef td As Double) As
Long

**Parameters**

Name

The name of an existing response spectrum load case.

MyType

This is 1, 2, 3, 4, 5 or 6, indicating the modal combination option.

```
1 = CQC
```
```
2 = SRSS
```
```
3 = Absolute
```
```
4 = GMC
```
```
5 = NRC 10 percent
```
```
6 = Double sum
```
F1

The GMC f1 factor. This item does not apply when MyType = 3. [cyc/s]

F2

The GMC f2 factor. This item does not apply when MyType = 3. [cyc/s]

PeriodicRigidCombType

This is 1 or 2, indicating the periodic plus rigid modal combination option.

```
1 = SRSS
```
```
2 = Absolute
```
td

This item applies only when MyType = 6. It is the factor td. [s]


**Remarks**

This function retrieves the modal combination option assigned to the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseResponseSpectrumModalComb_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyType As Long
Dim F1 As Double
Dim F2 As Double
Dim PeriodicRigidCombType As Long
Dim td As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'get modal combination option
ret = SapModel.LoadCases.ResponseSpectrum.GetModalComb_1("LCASE1", MyType,F1,
F2, PeriodicRigidCombType, td)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 14.00.


This function supersedes GetModalComb.

## See Also

SetModalComb_1

# SetCase

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

## Remarks

This function initializes a response spectrum analysis case. If this function is called for an existing
load case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseResponseSpectrum()
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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetDampConstant

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetDampConstant

## VB6 Procedure

Function SetDampConstant(ByVal Name As String, ByVal Damp As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case.

Damp

The constant damping for all modes (0 <= Damp < 1).

## Remarks

This function sets constant modal damping for the specified load case.


The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseResponseSpectrumDampConstant()
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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant("LCASE1", 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetDampConstant


# SetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetDampInterpolated

## VB6 Procedure

Function SetDampInterpolated(ByVal Name As String, ByVal DampType As Long, ByVal
NumberItems As Long, ByRef Time() As Double, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case.

DampType

This is either 5 or 6, indicating the interpolated modal damping type.

```
5 = Interpolated damping by period
6 = Interpolated damping by frequency
```
NumberItems

The number of Time and Damp pairs.

Time

This is an array that includes the period or the frequency depending on the value of the DampType
item. [s] for DampType = 5 and [cyc/s] for DampType = 6

Damp

This is an array that includes the damping for the specified period of frequency (0 <= Damp < 1).

## Remarks

This function sets interpolated modal damping data for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseResponseSpectrumDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim MyTime() As Double
Dim MyDamp() As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set interpolated damping
ReDim MyTime(2)
ReDim MyDamp(2)
MyTime(0) = 0.001
MyDamp(0) = 0.1
MyTime(1) = 0.3
MyDamp(1) = 0.03
MyTime(2) = 1
MyDamp(2) = 0.05
ret = SapModel.LoadCases.ResponseSpectrum.SetDampInterpolated("LCASE1", 5, 3,
MyTime, MyDamp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetDampInterpolated


# SetDampOverrides

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetDampOverrides

## VB6 Procedure

Function SetDampOverrides(ByVal Name As String, ByVal NumberItems As Long, ByRef Mode
() As Long, ByRef Damp() As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case.

NumberItems

The number of Mode and Damp pairs.

Mode

This is an array that includes a mode number.

Damp

This is an array that includes the damping for the specified mode (0 <= Damp < 1).

## Remarks

This function sets the modal damping overrides for the specified load case.

The function returns zero if the overrides are successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseResponseSpectrumDampOverrides()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyMode() As Long
Dim MyDamp() As Double

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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant("LCASE1", 0.04)

'set modal damping overrides
ReDim MyMode(1)
ReDim MyDamp(1)
MyMode(0) = 1
MyDamp(0) = 0.02
MyMode(1) = 2
MyDamp(1) = 0.03
ret = SapModel.LoadCases.ResponseSpectrum.SetDampOverrides("LCASE1", 2, MyMode,
MyDamp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampOverrides

# SetDampProportional

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetDampProportional


**VB6 Procedure**

Function SetDampProportional(ByVal Name As String, ByVal DampType As Long, ByVal
Dampa As Double, ByVal Dampb As Double, ByVal Dampf1 As Double, ByVal Dampf2 As
Double, ByVal Dampd1 As Double, ByVal Dampd2 As Double) As Long

**Parameters**

Name

The name of an existing response spectrum load case.

DampType

This is 1, 2 or 3, indicating the proportional modal damping type.

```
1 = Mass and stiffness proportional damping by direct specification
2 = Mass and stiffness proportional damping by period
3 = Mass and stiffness proportional damping by frequency
```
Dampa

The mass proportional damping coefficient. This item applies only when DampType = 1.

Dampb

The stiffness proportional damping coefficient. This item applies only when DampType = 1.

Dampf1

This is the period or the frequency (depending on the value of the DampType item) for point 1. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampf2

This is the period or the frequency (depending on the value of the DampType item) for point 2. [s]
for DampType = 2 and [cyc/s] for DampType = 3

This item applies only when DampType = 2 or 3.

Dampd1

This is the damping at point 1 (0 <= Dampd1 < 1).

This item applies only when DampType = 2 or 3.

Dampd2

This is the damping at point 2 (0 <= Dampd2 < 1).

This item applies only when DampType = 2 or 3.


**Remarks**

This function sets proportional modal damping data for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseResponseSpectrumDampProportional()
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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set proportional damping
ret = SapModel.LoadCases.ResponseSpectrum.SetDampProportional("LCASE1", 2, 0, 0, 0.1,
1, 0.05, 0.06)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetDampProportional

# SetDiaphragmEccentricityOverride

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetDiaphragmEccentricityOverride

## VB6 Procedure

Function SetDiaphragmEccentricityOverride(ByVal Name As String, ByVal Diaph As String,
ByVal Eccen As Double, Optional ByVal Delete As Boolean = False) As Long

## Parameters

Name

The name of an existing response spectrum load case.

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

This function assigns diaphragm eccentricity overrides for response spectrum load cases.

The function returns zero if the overrides are successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub AssignResponseSpectrumDiaphragmEccentricityOverride()
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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'assign diaphragm eccentricity override
ret = SapModel.LoadCases.ResponseSpectrum.SetDiaphragmEccentricityOverride
("LCASE1", "Diaph1", 50)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


Modified optional argument Delete to be ByVal in version 12.0.1.

## See Also

GetDiaphragmEccentricityOverride

GetSpecialRigidDiaphragmList

# SetDirComb

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetDirComb

## VB6 Procedure

Function SetDirComb(ByVal Name As String, ByVal MyType As Long, ByVal SF As Double)
As Long

## Parameters

Name

The name of an existing response spectrum load case.

MyType

This is 1, 2, or 3, indicating the directional combination option.

```
1 = SRSS
2 = ABS
3 = CQC3
```
SF

This item applies only when MyType = 2. It is the ABS scale factor.

## Remarks

This function sets the directional combination option for the specified load case.

The function returns zero if the option is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseResponseSpectrumDirComb()
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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set directional combination option
ret = SapModel.LoadCases.ResponseSpectrum.SetDirComb("LCASE1", 2, 1.2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Removed Modified SRSS (Chinese) directional combination option in version 14.00.

Added CQC3 directional combination option in version 14.20.

## See Also

GetDirComb

# SetEccentricity

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetEccentricity


**VB6 Procedure**

Function SetEccentricity(ByVal Name As String, ByVal Eccen As Double) As Long

**Parameters**

Name

The name of an existing response spectrum load case.

Eccen

The eccentricity ratio that applies to all diaphragms.

**Remarks**

This function sets the eccentricity ratio that applies to all diaphragms for the specified load case.

The function returns zero if the ratio is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseResponseSpectrumEccentricity()
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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set eccentricity ratio
ret = SapModel.LoadCases.ResponseSpectrum.SetEccentricity("LCASE1", 0.05)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetEccentricity

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadName()
As String, ByRef Func() As String, ByRef SF() As Double, ByRef CSys() As String, ByRef Ang()
As Double) As Long

## Parameters

Name

The name of an existing response spectrum load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadName

This is an array that includes U1, U2, U3, R1, R2 or R3, indicating the direction of the load.

Func

This is an array that includes the name of the response spectrum function associated with each
load.

SF


This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseResponseSpectrumLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyCSys() As String
Dim MyAng() As Double

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

'add UBC97 RS function
ret = SapModel.Func.FuncRS.SetUBC97("RS-1", 0.36, 0.54, 0.04)

'add response spectrum load case


ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set load data
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadName(0) = "U1"
MyFunc(0) = "RS-1"
MySF(0) = 386
MyCSys(0) = "Global"
MyAng(0) = 10
MyLoadName(1) = "U2"
MyFunc(1) = "RS-1"
MySF(1) = 386
ret = SapModel.LoadCases.ResponseSpectrum.SetLoads("LCASE1", 2, MyLoadName,
MyFunc, MySF, MyCSys, MyAng)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# SetModalCase

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetModalCase

## VB6 Procedure

Function SetModalCase(ByVal Name As String, ByVal ModalCase As String) As Long

## Parameters


Name

The name of an existing response spectrum load case.

ModalCase

This is the name of an existing modal load case. It specifies the modal load case on which any
mode-type load assignments to the specified load case are based.

**Remarks**

This function sets the modal case for the specified analysis case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

If the specified modal case is not actually a modal case, the program automatically replaces it with
the first modal case it can find. If no modal load cases exist, an error is returned.

**VBA Example**

Sub SetCaseResponseSpectrumModalCase()
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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set modal case
ret = SapModel.LoadCases.ResponseSpectrum.SetModalCase("LCASE1", "MODAL")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetModalCase

# SetModalComb_1

## Syntax

SapObject.SapModel.LoadCases.ResponseSpectrum.SetModalComb_1

## VB6 Procedure

Function SetModalComb_1(ByVal Name As String, ByVal MyType As Long, Optional ByVal F1
As Double = 1, Optional ByVal F2 As Double = 0, Optional ByVal PeriodicRigidCombType As
Long = 1, Optional ByVal td As Double = 60) As Long

## Parameters

Name

The name of an existing response spectrum load case.

MyType

This is 1, 2, 3, 4, 5 or 6, indicating the modal combination option.

```
1 = CQC
```
```
2 = SRSS
```
```
3 = Absolute
```
```
4 = GMC
```
```
5 = NRC 10 percent
```
```
6 = Double sum
```
F1


The GMC f1 factor. This item does not apply when MyType = 3. [cyc/s]

F2

The GMC f2 factor. This item does not apply when MyType = 3. [cyc/s]

PeriodicRigidCombType

This is 1 or 2, indicating the periodic plus rigid modal combination option.

```
1 = SRSS
```
```
2 = Absolute
```
td

This item applies only when MyType = 6. It is the factor td. [s]

**Remarks**

This function sets the modal combination option for the specified load case.

The function returns zero if the option is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseResponseSpectrumModalComb_1()
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

'add response spectrum load case
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("LCASE1")

'set modal combination option
ret = SapModel.LoadCases.ResponseSpectrum.SetModalComb_1("LCASE1", 4, 0.5, 1.2, 1)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.00.

This function supersedes SetModalComb.

## See Also

GetModalComb_1

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticLinear.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing static linear load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetCaseStaticLinearInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'get initial condition
ret = SapModel.LoadCases.StaticLinear.GetInitialCase("DEAD", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.StaticLinear.GetLoads


**VB6 Procedure**

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef SF() As Double) As Long

**Parameters**

Name

The name of an existing static linear load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseStaticLinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double
Dim NumberLoads As Long
Dim LoadType() As String


Dim LoadName() As String
Dim SF() As Double

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

'add static linear load case
ret = SapModel.LoadCases.StaticLinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MySF(1) = 1.2
ret = SapModel.LoadCases.StaticLinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MySF)

'get load data
ret = SapModel.LoadCases.StaticLinear.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, SF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

SetLoads

# SetCase

## Syntax

SapObject.SapModel.LoadCases.StaticLinear.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

## Remarks

This function initializes a static linear load case. If this function is called for an existing load case,
all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseStaticLinear()
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

'add static linear load case
ret = SapModel.LoadCases.StaticLinear.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticLinear.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing static linear load case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else then zero initial
conditions are assumed.


**Remarks**

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticLinearInitialCondition()
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

'add static linear load case
ret = SapModel.LoadCases.StaticLinear.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.StaticLinear.SetInitialCase("LCASE1", "None")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.StaticLinear.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef SF() As Double) As Long

## Parameters

Name

The name of an existing static linear load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

## Remarks

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.


**VBA Example**

Sub SetCaseStaticLinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double

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

'add static linear load case
ret = SapModel.LoadCases.StaticLinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MySF(1) = 1.2
ret = SapModel.LoadCases.StaticLinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MySF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticLinearMultistep.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing static linear multistep analysis case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise, it returns a
nonzero value.

## VBA Example

Sub GetCaseStaticLinearMultistepInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String


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

'add static linear multistep load case
ret = SapModel.LoadCases.StaticLinearMultistep.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.StaticLinearMultistep.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoads_1

## Syntax

SapObject.SapModel.LoadCases.StaticLinearMultistep.GetLoads_1

## VB6 Procedure

Function GetLoads_1(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef SF() As Double, ByRef StepRange() as Integer,


ByRef FirstLoadStep() As Integer, ByRef LastLoadStep() As Integer, ByRef StartCaseStep() As
Integer, ByRef ExtrapolateOption() As Integer) As Long

**Parameters**

Name

The name of an existing static linear multistep analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

StepRange

This is an array that identifies the step range type to consider for each load assigned to the load
case. The allowed values are:

```
0 = All
1 = User
```
FirstLoadStep

This is an array that specifies the first load step to consider for each load assigned to the load case.
This value is only applicable when StepRange = User.

LastLoadStep

This is an array that specifies the last load step to consider for each load assigned to the load case.
This value is only applicable when StepRange = User.

StartCaseStep

This is an array that specifies the load case step at which to start applying each load assigned to
the load case.


ExtrapolateOption

This is an array that identifies the extrapolation option for each load assigned to the load case. The
allowed values are:

```
0 = None
1 = Last Step
2 = Repeat Range
```
**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise, it returns a nonzero
value.

**VBA Example**

Sub GetCaseStaticLinearMultistepLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double
Dim MyStepRange() As Long

Dim MyFirstLoadStep() As Long

Dim MyLastLoadStep() As Long

Dim MyStartCaseStep() As Long

Dim MyExtrapolateOption() As Long

Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim SF() As Double

Dim StepRange() As Long

Dim FirstLoadStep() As Long

Dim LastLoadStep() As Long

Dim StartCaseStep() As Long

Dim ExtrapolateOption() As Long

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

'add static linear multistep load case
ret = SapModel.LoadCases.StaticLinearMultistep.SetCase_1("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)

ReDim MyStepRange(1)

ReDim MyFirstLoadStep(1)

ReDim MyLastLoadStep(1)

ReDim MyStartCaseStep(1)

ReDim MyExtrapolateOption(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7

MyStepRange(0) = 0

MyFirstLoadStep(0) = 1

MyLastLoadStep(0) = 1
MyStartCaseStep(0) = 1

MyExtrapolateOption(0) = 1

MyLoadType(1) = "Accel0"
MyLoadName(1) = "UZ"
MySF(1) = 1.2
ret = SapModel.LoadCases.StaticLinearMultistep.SetLoads_1("LCASE1", 2, MyLoadType,
MyLoadName, MySF, MyStepRange, MyFirstLoadStep, MyLastLoadStep, MyStartCaseStep,
MyExtrapolateOption)

'get load data
ret = SapModel.LoadCases.StaticLinearMultistep.GetLoads_1("LCASE1", NumberLoads,
LoadType, LoadName, SF, StepRange, FirstLoadStep, LastLoadStep, StartCaseStep,
ExtrapolateOption)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

This function supersedes GetLoads.

## See Also

SetLoads_1

# SetCase

## Syntax

SapObject.SapModel.LoadCases.StaticLinearMultistep.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

## Remarks

This function initializes a static linear multistep analysis case. If this function is called for an
existing load case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise, it returns a nonzero
value.

## VBA Example

Sub SetCaseStaticLinearMultistep()
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

'add static linear multistep load case
ret = SapModel.LoadCases.StaticLinearMultistep.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticLinearMultistep.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters


Name

The name of an existing static linear multistep analysis case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticLinearMultistepInitialCondition()
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

'add static linear load case
ret = SapModel.LoadCases.StaticLinear.SetCase("SN1" )

'add static linear multistep load case
ret = SapModel.LoadCases.StaticLinearMultistep.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.StaticLinearMultistep.SetInitialCase("LCASE1", "SN1")


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLoads_1

## Syntax

SapObject.SapModel.LoadCases.StaticLinearMultistep.SetLoads_1

## VB6 Procedure

Function SetLoads_1(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef SF() As Double, ByRef StepRange() as Integer,
ByRef FirstLoadStep() As Integer, ByRef LastLoadStep() As Integer, ByRef StartCaseStep() As
Integer, ByRef ExtrapolateOption() As Integer) As Long

## Parameters

Name

The name of an existing static linear multistep analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.


If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

StepRange

This is an array that identifies the step range type to consider for each load assigned to the load
case. The allowed values are:

```
0 = All
1 = User
```
FirstLoadStep

This is an array that specifies the first load step to consider for each load assigned to the load case.
This value is only applicable when StepRange = User.

LastLoadStep

This is an array that specifies the last load step to consider for each load assigned to the load case.
This value is only applicable when StepRange = User.

StartCaseStep

This is an array that specifies the load case step at which to start applying each load assigned to
the load case.

ExtrapolateOption

This is an array that identifies the extrapolation option for each load assigned to the load case. The
allowed values are:

```
0 = None
1 = Last Step
2 = Repeat Range
```
**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseStaticLinearMultistepLoads()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double

Dim MyStepRange() As Long

Dim MyFirstLoadStep() As Long

Dim MyLastLoadStep() As Long

Dim MyStartCaseStep() As Long

Dim MyExtrapolateOption() As Long

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

'add static linear multistep load case
ret = SapModel.LoadCases.StaticLinearMultistep.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)

ReDim MyStepRange(1)

ReDim MyFirstLoadStep(1)

ReDim MyLastLoadStep(1)

ReDim MyStartCaseStep(1)

ReDim MyExtrapolateOption(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7


MyStepRange(0) = 0

MyFirstLoadStep(0) = 1

MyLastLoadStep(0) = 1
MyStartCaseStep(0) = 1

MyExtrapolateOption(0) = 1
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MySF(1) = 1.2
ret = SapModel.LoadCases.StaticLinearMultistep.SetLoads_1("LCASE1", 2, MyLoadType,
MyLoadName, MySF, MyStepRange, MyFirstLoadStep, MyLastLoadStep, MyStartCaseStep,
MyExtrapolateOption)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

This function supersedes Set Loads.

## See Also

GetLoads_1

# GetGeometricNonlinearity

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetGeometricNonlinearity

## VB6 Procedure

Function GetGeometricNonlinearity(ByVal Name As String, ByRef NLGeomType As Long) As
Long

## Parameters

Name

The name of an existing static nonlinear load case.

NLGeomType


This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.

```
0 = None
1 = P-delta
2 = P-delta plus large displacements
```
**Remarks**

This function retrieves the geometric nonlinearity option for the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseStaticNonlinearGeometricNonlinearity()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NLGeomType As Long

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'get geometric nonlinearity option
ret = SapModel.LoadCases.StaticNonlinear.GetGeometricNonlinearity("LCASE1",
NLGeomType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetGeometricNonlinearity

# GetHingeUnloading

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetHingeUnloading

## VB6 Procedure

Function GetHingeUnloading(ByVal Name As String, ByRef UnloadType As Long) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

UnloadType

This is 1, 2 or 3, indicating the hinge unloading option selected for the load case.

```
1 = Unload entire structure
2 = Apply local redistribution
3 = Restart using secant stiffness
```
## Remarks

This function retrieves the hinge unloading option for the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCaseStaticNonlinearHingeUnloading()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim UnloadType As Long

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'get hinge unloading option
ret = SapModel.LoadCases.StaticNonlinear.GetHingeUnloading("LCASE1", UnloadType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetHingeUnloading

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetInitialCase

## VB6 Procedure


Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

**Parameters**

Name

The name of an existing static nonlinear load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts from the state at the end
of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the state at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")


'get initial condition
ret = SapModel.LoadCases.StaticNonlinear.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoadApplication

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetLoadApplication

## VB6 Procedure

Function GetLoadApplication(ByVal Name As String, ByRef LoadControl As Long, ByRef
DispType As Long, ByRef Displ As Double, ByRef Monitor As Long, ByRef DOF As Long,
ByRef PointName As String, ByRef GDispl As String) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

LoadControl

This is either 1 or 2, indicating the load application control method.

```
1 = Full load
2 = Displacement control
```
DispType

This is either 1 or 2, indicating the control displacement type.


```
1 = Conjugate displacement
2 = Monitored displacement
```
This item applies only when displacement control is used, that is, LoadControl = 2.

Displ

This item applies only when displacement control is used, that is, LoadControl = 2. The structure
is loaded to a monitored displacement of this magnitude. [L] when DOF = 1, 2 or 3 and [rad]
when DOF = 4, 5 or 6

Monitor

This is either 1 or 2, indicating the monitored displacement.

```
1 = Displacement at a specified point object
2 = Generalized displacement
```
DOF

This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom for which the displacement at a point
object is monitored.

```
1 = U1
2 = U2
3 = U3
4 = R1
5 = R2
6 = R3
```
This item applies only when Monitor = 1.

PointName

The name of the point object at which the displacement is monitored. This item applies only when
Monitor = 1.

GDispl

The name of the generalized displacement for which the displacement is monitored. This item
applies only when Monitor = 2.

**Remarks**

This function retrieves the load application control parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**


Sub GetCaseStaticNonlinearLoadApplication()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim SF() As Double
Dim LoadControl As Long
Dim DispType As Long
Dim Displ As Double
Dim Monitor As Long
Dim DOF As Long
Dim PointName As String
Dim GDispl As String

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

'add generalized displacement
ret = SapModel.GDispl.Add("GD1", 1)

'add point to generalized displacement
ReDim SF(5)
SF(0) = 0.5
ret = SapModel.GDispl.SetPoint("GD1", "2", SF)
ret = SapModel.GDispl.SetPoint("GD1", "3", SF)

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set load application parameters
ret = SapModel.LoadCases.StaticNonlinear.SetLoadApplication("LCASE1", 2, 1, 12, 2, 0, "",
"GD1")

'get load application parameters
ret = SapModel.LoadCases.StaticNonlinear.GetLoadApplication("LCASE1", LoadControl,
DispType, Displ, Monitor, DOF, PointName, GDispl)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoadApplication

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef SF() As Double) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

SF


This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim SF() As Double

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"


MySF(1) = 1.2
ret = SapModel.LoadCases.StaticNonlinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MySF)

'get load data
ret = SapModel.LoadCases.StaticNonlinear.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, SF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# GetMassSource

## Syntax

SapObject.SapModel.LoadCases.Static Nonlinear.GetMassSource

## VB6 Procedure

Function GetMassSource(ByVal Name As String, ByRef Source As String) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

Source

This is the name of an existing mass source or a blank string. Blank indicates to use the mass
source from the previous load case or the default mass source if the load case starts from zero
initial conditions.


**Remarks**

This function sets the mass source to be used for the specified load case.

The function returns zero if the mass source is data is successfully set; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearMassSource()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim Source as String

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'get a mass source from the static nonlinear load case

ret = SapModel.LoadCases.StaticNonlinear.GetMassSource("LCASE1", "Source")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 17.20.


## See Also

SetMassSource

# GetModalCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetModalCase

## VB6 Procedure

Function GetModalCase(ByVal Name As String, ByRef ModalCase As String) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

ModalCase

This is either None or the name of an existing modal analysis case. It specifies the modal load case
on which any mode-type load assignments to the specified load case are based.

## Remarks

This function retrieves the modal case assigned to the specified load case.

The function returns zero if the modal case is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCaseStaticNonlinearModalCase()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ModalCase As String

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'get modal case
ret = SapModel.LoadCases.StaticNonlinear.GetModalCase("LCASE1", ModalCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetModalCase

# GetResultsSaved

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetResultsSaved

## VB6 Procedure

Function GetResultsSaved(ByVal Name As String, ByRef SaveMultipleSteps As Boolean, ByRef
MinSavedStates As Long, ByRef MaxSavedStates As Long, ByRef PositiveOnly As Boolean) As
Long

## Parameters

Name

The name of an existing static nonlinear load case.


SaveMultipleSteps

This item is True if multiple states are saved for the nonlinear analysis. It is False only if the final
state is saved.

MinSavedStates

This item applies only when SaveMultipleSteps = True. It is the minimum number of saved steps.

MaxSavedStates

This item applies only when SaveMultipleSteps = True. It is the maximum number of saved steps.

PositiveOnly

If this item is True, only positive displacement increments are saved. If it is False, all
displacement increments are saved.

**Remarks**

This function retrieves the results saved parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearResultsSaved()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim SaveMultipleSteps As Boolean
Dim MinSavedStates As Long
Dim MaxSavedStates As Long
Dim PositiveOnly As Boolean

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


'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set results saved parameters
ret = SapModel.LoadCases.StaticNonlinear.SetResultsSaved("LCASE1", True, 12, 84, False)

'get results saved parameters
ret = SapModel.LoadCases.StaticNonlinear.GetResultsSaved("LCASE1", SaveMultipleSteps,
MinSavedStates, MaxSavedStates, PositiveOnly)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetResultsSaved

# GetSolControlParameters

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetSolControlParameters

## VB6 Procedure

Function GetSolControlParameters(ByVal Name As String, ByRef MaxTotalSteps As Long,
ByRef MaxFailedSubSteps As Long, ByRef MaxIterCS As Long, ByRef MaxIterNR As Long,
ByRef TolConvD As Double, ByRef UseEventStepping As Boolean, ByRef TolEventD As
Double, ByRef MaxLineSearchPerIter As Long, ByRef TolLineSearch As Double, ByRef
LineSearchStepFact As Double) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

MaxTotalSteps


The maximum total steps per stage.

MaxFailedSubSteps

The maximum null (zero) steps per stage.

MaxIterCS

The maximum constant-stiffness iterations per step.

MaxIterNR

The maximum Newton_Raphson iterations per step.

TolConvD

The relative iteration convergence tolerance.

UseEventStepping

This item is True if event-to-event stepping is used.

TolEventD

The relative event lumping tolerance.

MaxLineSearchPerIter

The maximum number of line searches per iteration.

TolLineSearch

The relative line-search acceptance tolerance.

LineSearchStepFact

The line-search step factor.

**Remarks**

This function retrieves the solution control parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearSolutionControlParameters()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MaxTotalSteps As Long
Dim MaxFailedSubSteps As Long


Dim MaxIterCS As Long
Dim MaxIterNR As Long
Dim TolConvD As Double
Dim UseEventStepping As Boolean
Dim TolEventD As Double
Dim MaxLineSearchPerIter As Long
Dim TolLineSearch As Double
Dim LineSearchStepFact As Double

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'get solution control parameters
ret = SapModel.LoadCases.StaticNonlinear.GetSolControlParameters("LCASE1",
MaxTotalSteps, MaxFailedSubSteps, MaxIterCS, MaxIterNR, TolConvD, UseEventStepping,
TolEventD, MaxLineSearchPerIter, TolLineSearch, LineSearchStepFact)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

SetSolControlParameters


# GetTargetForceParameters

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.GetTargetForceParameters

## VB6 Procedure

Function GetTargetForceParameters(ByVal Name As String, ByRef TolConvF As Double, ByRef
MaxIter As Long, ByRef AccelFact As Double, ByRef NoStop As Boolean) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

TolConvF

The relative convergence tolerance for target force iteration.

MaxIter

The maximum iterations per stage for target force iteration.

AccelFact

The acceleration factor.

NoStop

If this item is True, the analysis is continued when there is no convergence in the target force
iteration.

## Remarks

This function retrieves the target force iteration parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetCaseStaticNonlinearTargetForceParameters()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim TolConvF As Double
Dim MaxIter As Long


Dim AccelFact As Double
Dim NoStop As Boolean

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'get target force iteration parameters
ret = SapModel.LoadCases.StaticNonlinear.GetTargetForceParameters("LCASE1",
TolConvF, MaxIter, AccelFact, NoStop)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetTargetForceParameters

# SetCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetCase


**VB6 Procedure**

Function SetCase(ByVal Name As String) As Long

**Parameters**

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

**Remarks**

This function initializes a static nonlinear analysis case. If this function is called for an existing
load case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticNonlinear()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetGeometricNonlinearity

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetGeometricNonlinearity

## VB6 Procedure

Function SetGeometricNonlinearity(ByVal Name As String, ByVal NLGeomType As Long) As
Long

## Parameters

Name

The name of an existing static nonlinear load case.

NLGeomType

This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.

```
0 = None
1 = P-delta
2 = P-delta plus large displacements
```
## Remarks

This function sets the geometric nonlinearity option for the specified load case.

The function returns zero if the option is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseStaticNonlinearGeometricNonlinearity()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set geometric nonlinearity option
ret = SapModel.LoadCases.StaticNonlinear.SetGeometricNonlinearity("LCASE1", 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetGeometricNonlinearity

# SetHingeUnloading

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetHingeUnloading

## VB6 Procedure

Function SetHingeUnloading(ByVal Name As String, ByVal UnloadType As Long) As Long


**Parameters**

Name

The name of an existing static nonlinear load case.

UnloadType

This is 1, 2 or 3, indicating the hinge unloading option selected for the load case.

```
1 = Unload entire structure
2 = Apply local redistribution
3 = Restart using secant stiffness
```
**Remarks**

This function sets the hinge unloading option for the specified load case.

The function returns zero if the option is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseStaticNonlinearHingeUnloading()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set hinge unloading option
ret = SapModel.LoadCases.StaticNonlinear.SetHingeUnloading("LCASE1", 2)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetHingeUnloading

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts from the state at the end
of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the state at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.


**VBA Example**

Sub SetCaseStaticNonlinearInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add static nonlinear multistep load case
ret = SapModel.LoadCases.StaticNonlinearMultistep.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.StaticNonlinearMultistep.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetInitialCase


# SetLoadApplication

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetLoadApplication

## VB6 Procedure

Function SetLoadApplication(ByVal Name As String, ByVal LoadControl As Long, ByVal
DispType As Long, ByVal Displ As Double, ByVal Monitor As Long, ByVal DOF As Long,
ByVal PointName As String, ByVal GDispl As String) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

LoadControl

This is either 1 or 2, indicating the load application control method.

```
1 = Full load
2 = Displacement control
```
DispType

This is either 1 or 2 indicating the control displacement type.

```
1 = Conjugate displacement
2 = Monitored displacement
```
This item applies only when displacement control is used, that is, LoadControl = 2.

Displ

This item applies only when displacement control is used, that is, LoadControl = 2. The structure
is loaded to a monitored displacement of this magnitude. [L] when DOF = 1, 2 or 3 and [rad]
when DOF = 4, 5 or 6

Monitor

This is either 1 or 2, indicating the monitored displacement.

```
1 = Displacement at a specified point object
2 = Generalized displacement
```
DOF

This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom for which the displacement at a point
object is monitored.


### 1 = U1

### 2 = U2

### 3 = U3

### 4 = R1

### 5 = R2

### 6 = R3

This item applies only when Monitor = 1.

PointName

The name of the point object at which the displacement is monitored. This item applies only when
Monitor = 1.

GDispl

The name of the generalized displacement for which the displacement is monitored. This item
applies only when Monitor = 2.

**Remarks**

This function sets the load application control parameters for the specified load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticNonlinearLoadApplication()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim SF() As Double

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

'add generalized displacement


ret = SapModel.GDispl.Add("GD1", 1)

'add point to generalized displacement
ReDim SF(5)
SF(0) = 0.5
ret = SapModel.GDispl.SetPoint("GD1", "2", SF)
ret = SapModel.GDispl.SetPoint("GD1", "3", SF)

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set load application parameters
ret = SapModel.LoadCases.StaticNonlinear.SetLoadApplication("LCASE1", 2, 1, 12, 2, 0, "",
"GD1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoadApplication

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef SF() As Double) As Long

## Parameters

Name

The name of an existing static nonlinear load case.


NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ indicating the direction of
the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseStaticNonlinearLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MySF(1) = 1.2
ret = SapModel.LoadCases.StaticNonlinear.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MySF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetLoads

# SetMassSource

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetMassSource

## VB6 Procedure

Function SetMassSource(ByVal Name As String, ByVal Source As String) As Long

## Parameters

Name


The name of an existing static nonlinear load case.

Source

This is the name of an existing mass source or a blank string. Blank indicates to use the mass
source from the previous load case or the default mass source if the load case starts from zero
initial conditions.

**Remarks**

This function sets the mass source to be used for the specified load case.

The function returns zero if the mass source is data is successfully set; otherwise it returns a
nonzero value.

**VBA Example**

Sub SetCaseStaticNonlinearMassSource()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'add a new mass source and make it the default mass source

LoadPat(0) = "DEAD"

SF(0) = 1.25

ret = SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True, True, 1,
LoadPat, SF)


'assign a mass source to the static nonlinear load case

ret = SapModel.LoadCases.StaticNonlinear.SetMassSource("LCASE1", "MyMassSource")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.20.

## See Also

GetMassSource

# SetModalCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetModalCase

## VB6 Procedure

Function SetModalCase(ByVal Name As String, ByVal ModalCase As String) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

ModalCase

This is the name of an existing modal load case. It specifies the modal load case on which any
mode-type load assignments to the specified load case are based.

## Remarks

This function sets the modal case for the specified analysis case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.


If the specified modal case is not actually a modal case, the program automatically replaces it with
the first modal case it can find. If no modal load cases exist, an error is returned.

**VBA Example**

Sub SetCaseStaticNonlinearModalCase()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set modal case
ret = SapModel.LoadCases.StaticNonlinear.SetModalCase("LCASE1", "MODAL")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetModalCase


# SetResultsSaved

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetResultsSaved

## VB6 Procedure

Function SetResultsSaved(ByVal Name As String, ByVal SaveMultipleSteps As Boolean,
Optional ByVal MinSavedStates As Long = 10, Optional ByVal MaxSavedStates As Long = 100,
Optional ByVal PositiveOnly As Boolean = True) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

SaveMultipleSteps

This item is True if multiple states are saved for the nonlinear analysis. It is False only if the final
state is saved.

MinSavedStates

This item only applies when SaveMultipleSteps = True. It is the minimum number of saved steps.

MaxSavedStates

This item only applies when SaveMultipleSteps = True. It is the maximum number of saved steps.

PositiveOnly

If this item is True, only positive displacement increments are saved. If it is False, all
displacement increments are saved.

## Remarks

This function sets the results saved parameters for the specified load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseStaticNonlinearResultsSaved()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set results saved parameters
ret = SapModel.LoadCases.StaticNonlinear.SetResultsSaved("LCASE1", True, 12, 84, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetResultsSaved

# SetSolControlParameters

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetSolControlParameters

## VB6 Procedure

Function SetSolControlParameters(ByVal Name As String, ByVal MaxTotalSteps As Long,
ByVal MaxFailedSubSteps As Long, ByVal MaxIterCS As Long, ByVal MaxIterNR As Long,


ByVal TolConvD As Double, ByVal UseEventStepping As Boolean, ByVal TolEventD As
Double, ByVal MaxLineSearchPerIter As Long, ByVal TolLineSearch As Double, ByVal
LineSearchStepFact As Double) As Long

**Parameters**

Name

The name of an existing static nonlinear load case.

MaxTotalSteps

The maximum total steps per stage.

MaxFailedSubSteps

The maximum null (zero) steps per stage.

MaxIterCS

The maximum constant-stiffness iterations per step.

MaxIterNR

The maximum Newton_Raphson iterations per step.

TolConvD

The relative iteration convergence tolerance.

UseEventStepping

This item is True if event-to-event stepping is used.

TolEventD

The relative event lumping tolerance.

MaxLineSearchPerIter

The maximum number of line searches per iteration.

TolLineSearch

The relative line-search acceptance tolerance.

LineSearchStepFact

The line-search step factor.

**Remarks**

This function sets the solution control parameters for the specified load case.


The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticNonlinearSolutionControlParameters()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set solution control parameters
ret = SapModel.LoadCases.StaticNonlinear.SetSolControlParameters("LCASE1", 240, 40,
15, 50, 0.00005, False, 0.02, 10, 0.2, 1.7)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetSolControlParameters


# SetTargetForceParameters

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinear.SetTargetForceParameters

## VB6 Procedure

Function SetTargetForceParameters(ByVal Name As String, ByVal TolConvF As Double, ByVal
MaxIter As Long, ByVal AccelFact As Double, ByVal NoStop As Boolean) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

TolConvF

The relative convergence tolerance for target force iteration.

MaxIter

The maximum iterations per stage for target force iteration.

AccelFact

The acceleration factor.

NoStop

If this item is True, the analysis is continued when there is no convergence in the target force
iteration.

## Remarks

This function sets the target force iteration parameters for the specified load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseStaticNonlinearTargetForceParameters()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("LCASE1")

'set target force iteration parameters
ret = SapModel.LoadCases.StaticNonlinear.SetTargetForceParameters("LCASE1", 0.008, 6,
5, True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetTargetForceParameters

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearMultistep.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long


**Parameters**

Name

The name of an existing static nonlinear multistep load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the state at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearMultistepInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinearMultistep.SetCase("LCASE1")

'get initial condition


ret = SapModel.LoadCases.StaticNonlinearMultistep.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearMultistep.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef SF() As Double, ByRef StepRange() as Integer,
ByRef FirstLoadStep() As Integer, ByRef LastLoadStep() As Integer, ByRef StartCaseStep() As
Integer, ByRef ExtrapolateOption() As Integer ) As Long

## Parameters

Name

The name of an existing static nonlinear multistep load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.


If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

StepRange

This is an array that identifies the step range type to consider for each load assigned to the load
case. The allowed values are:

```
0 = All
1 = User
```
FirstLoadStep

This is an array that specifies the first load step to consider for each load assigned to the load case.
This value is only applicable when StepRange = User.

LastLoadStep

This is an array that specifies the last load step to consider for each load assigned to the load case.
This value is only applicable when StepRange = User.

StartCaseStep

This is an array that specifies the load case step at which to start applying each load assigned to
the load case.

ExtrapolateOption

This is an array that identifies the extrapolation option for each load assigned to the load case. The
allowed values are:

```
0 = None
1 = Last Step
2 = Repeat Range
```
**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearMultistepLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double
Dim MyStepRange() As Long

Dim MyFirstLoadStep() As Long

Dim MyLastLoadStep() As Long

Dim MyStartCaseStep() As Long

Dim MyExtrapolateOption() As Long

Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim SF() As Double

Dim StepRange() As Long

Dim FirstLoadStep() As Long

Dim LastLoadStep() As Long

Dim StartCaseStep() As Long

Dim ExtrapolateOption() As Long

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinearMultistep.SetCase("LCASE1")
'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)

ReDim MyStepRange(1)

ReDim MyFirstLoadStep(1)


ReDim MyLastLoadStep(1)

ReDim MyStartCaseStep(1)

ReDim MyExtrapolateOption(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7

MyStepRange(0) = 0

MyFirstLoadStep(0) = 1

MyLastLoadStep(0) = 1
MyStartCaseStep(0) = 1

MyExtrapolateOption(0) = 1

MyLoadType(1) = "Accel0"
MyLoadName(1) = "UZ"
MySF(1) = 1.2
ret = SapModel.LoadCases.StaticNonlinearMultistep.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MySF, MyStepRange, MyFirstLoadStep, MyLastLoadStep, MyStartCaseStep,
MyExtrapolateOption )

'get load data
ret = SapModel.LoadCases.StaticNonlinearMultistep.GetLoads("LCASE1", NumberLoads,
LoadType, LoadName, SF, StepRange, FirstLoadStep, LastLoadStep, StartCaseStep,
ExtrapolateOption )

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

SetLoads

# SetCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearMultistep.SetCase


**VB6 Procedure**

Function SetCase(ByVal Name As String) As Long

**Parameters**

Name

The name of an existing or new load case. If this is an existing case, that case is modified;
otherwise, a new case is added.

**Remarks**

This function initializes a static nonlinear multistep analysis case. If this function is called for an
existing load case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise, it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticNonlinearMultistep()
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

'add static nonlinear multistep load case
ret = SapModel.LoadCases.StaticNonlinearMultistep.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 21.0.0.

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearMultistep.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing static nonlinear multistep load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts from the state at the end
of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseStaticNonlinearMultistepInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add static nonlinear multistep load case

ret = SapModel.LoadCases.StaticNonlinearMultistep.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.StaticNonlinearMultistep.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearMultistep.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef SF() As Double, ByRef StepRange() as Integer,


ByRef FirstLoadStep() As Integer, ByRef LastLoadStep() As Integer, ByRef StartCaseStep() As
Integer, ByRef ExtrapolateOption() As Integer ) As Long

**Parameters**

Name

The name of an existing static nonlinear multistep analysis case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction
of the load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for
Accel UX UY and UZ; otherwise unitless

StepRange

This is an array that identifies the step range type to consider for each load assigned to the load
case. The allowed values are:

```
0 = All
1 = User
```
FirstLoadStep

This is an array that specifies the first load step to consider for each load assigned to the load case.
This value is only applicable when StepRange = User.

LastLoadStep

This is an array that specifies the last load step to consider for each load assigned to the load case.
This value is only applicable when StepRange = User.

StartCaseStep

This is an array that specifies the load case step at which to start applying each load assigned to
the load case.


ExtrapolateOption

This is an array that identifies the extrapolation option for each load assigned to the load case. The
allowed values are:

```
0 = None
1 = Last Step
2 = Repeat Range
```
**Remarks**

This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseStaticNonlinearMultistepLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MySF() As Double

Dim MyStepRange() As Long

Dim MyFirstLoadStep() As Long

Dim MyLastLoadStep() As Long

Dim MyStartCaseStep() As Long

Dim MyExtrapolateOption() As Long

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

'add static nonlinear multistep load case


ret = SapModel.LoadCases.StaticNonlinearMultistep.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MySF(1)

ReDim MyStepRange(1)

ReDim MyFirstLoadStep(1)

ReDim MyLastLoadStep(1)

ReDim MyStartCaseStep(1)

ReDim MyExtrapolateOption(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MySF(0) = 0.7

MyStepRange(0) = 0

MyFirstLoadStep(0) = 1

MyLastLoadStep(0) = 1
MyStartCaseStep(0) = 1

MyExtrapolateOption(0) = 1
MyLoadType(1) = "Accel"
MyLoadName(1) = "UZ"
MySF(1) = 1.2
ret = SapModel.LoadCases.StaticNonlinearMultistep.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MySF, MyStepRange, MyFirstLoadStep, MyLastLoadStep, MyStartCaseStep,
MyExtrapolateOption)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0..

## See Also

GetLoads

# GetGeometricNonlinearity


**Syntax**

SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetGeometricNonlinearity

**VB6 Procedure**

Function GetGeometricNonlinearity(ByVal Name As String, ByRef NLGeomType As Long) As
Long

**Parameters**

Name

The name of an existing static nonlinear staged analysis case.

NLGeomType

This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.

```
0 = None
1 = P-delta
2 = P-delta plus large displacements
```
**Remarks**

This function retrieves the geometric nonlinearity option for the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseStaticNonlinearStagedGeometricNonlinearity()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NLGeomType As Long

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'get geometric nonlinearity option
ret = SapModel.LoadCases.StaticNonlinearStaged.GetGeometricNonlinearity("LCASE1",
NLGeomType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetGeometricNonlinearity

# GetHingeUnloading

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetHingeUnloading

## VB6 Procedure

Function GetHingeUnloading(ByVal Name As String, ByRef UnloadType As Long) As Long

## Parameters

Name

The name of an existing static nonlinear staged analysis case.

UnloadType

This is 1, 2 or 3, indicating the hinge unloading option selected for the load case.

```
1 = Unload entire structure
```

```
2 = Apply local redistribution
3 = Restart using secant stiffness
```
**Remarks**

This function retrieves the hinge unloading option for the specified load case.

The function returns zero if the option is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetCaseStaticNonlinearStagedHingeUnloading()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim UnloadType As Long

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'get hinge unloading option
ret = SapModel.LoadCases.StaticNonlinearStaged.GetHingeUnloading("LCASE1",
UnloadType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetHingeUnloading

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetInitialCase

## VB6 Procedure

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

## Parameters

Name

The name of an existing static nonlinear staged analysis case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts from the state at the end
of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the state at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetCaseStaticNonlinearStagedInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String


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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.StaticNonlinearStaged.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetMassSource

## Syntax

SapObject.SapModel.LoadCases.Static NonlinearStaged.GetMassSource

## VB6 Procedure

Function GetMassSource(ByVal Name As String, ByRef Source As String) As Long


**Parameters**

Name

The name of an existing static nonlinear staged load case.

Source

This is the name of an existing mass source or a blank string. Blank indicates to use the mass
source from the previous load case or the default mass source if the load case starts from zero
initial conditions.

**Remarks**

This function sets the mass source to be used for the specified load case.

The function returns zero if the mass source is data is successfully set; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearStagedMassSource()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim Source as String

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'get a mass source from the static nonlinear load case


ret = SapModel.LoadCases.StaticNonlinearStaged.GetMassSource("LCASE1", "Source")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.20.

## See Also

SetMassSource

# GetMaterialNonlinearity

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetMaterialNonlinearity

## VB6 Procedure

Function GetMaterialNonlinearity(ByVal Name As String, ByRef TimeDepMatProp As Boolean)
As Long

## Parameters

Name

The name of an existing static nonlinear staged analysis case.

TimeDepMatProp

When this is True, any specified time dependent material properties are considered in the analysis.

## Remarks

This function retrieves the material nonlinearity options for the specified load case.

The function returns zero if the options are successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example


Sub GetCaseStaticNonlinearStagedMaterialNonlinearity()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim TimeDepMatProp As Boolean

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'get material nonlinearity options
ret = SapModel.LoadCases.StaticNonlinearStaged.GetMaterialNonlinearity("LCASE1",
TimeDepMatProp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetMaterialNonlinearity

# GetResultsSaved

## Syntax


SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetResultsSaved

**VB6 Procedure**

Function GetResultsSaved(ByVal Name As String, ByRef StagedSaveOption As Long, ByRef
StagedMinSteps As Long, ByRef StagedMinStepsTD As Long) As Long

**Parameters**

Name

The name of an existing static nonlinear staged analysis case.

StagedSaveOption

This is 0, 1, 2 or 3, indicating the results saved option for the load case.

```
0 = End of final stage
1 = End of each stage
2 = Start and end of each stage
3 = Two or more times in each stage
```
StagedMinSteps

The minimum number of steps for application of instantaneous load. This item applies only when
StagedSaveOption = 3.

StagedMinStepsTD

The minimum number of steps for analysis of time dependent items. This item applies only when
StagedSaveOption = 3.

**Remarks**

This function retrieves the results saved parameters for the specified load case.

The function returns zero if the parameters are retrieved successfully; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearStagedResultsSaved()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim StagedSaveOption As Long
Dim StagedMinSteps As Long
Dim StagedMinStepsTD As Long

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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'set results saved parameters
ret = SapModel.LoadCases.StaticNonlinearStaged.SetResultsSaved("LCASE1", 3, 4, 10)

'get results saved parameters
ret = SapModel.LoadCases.StaticNonlinearStaged.GetResultsSaved("LCASE1",
StagedSaveOption , StagedMinSteps, StagedMinStepsTD)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetResultsSaved

# GetSolControlParameters

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetSolControlParameters

## VB6 Procedure


Function GetSolControlParameters(ByVal Name As String, ByRef MaxTotalSteps As Long,
ByRef MaxFailedSubSteps As Long, ByRef MaxIterCS As Long, ByRef MaxIterNR As Long,
ByRef TolConvD As Double, ByRef UseEventStepping As Boolean, ByRef TolEventD As
Double, ByRef MaxLineSearchPerIter As Long, ByRef TolLineSearch As Double, ByRef
LineSearchStepFact As Double) As Long

**Parameters**

Name

The name of an existing static nonlinear load case.

MaxTotalSteps

The maximum total steps per stage.

MaxFailedSubSteps

The maximum null (zero) steps per stage.

MaxIterCS

The maximum constant-stiffness iterations per step.

MaxIterNR

The maximum Newton_Raphson iterations per step.

TolConvD

The relative iteration convergence tolerance.

UseEventStepping

This item is True if event-to-event stepping is used.

TolEventD

The relative event lumping tolerance.

MaxLineSearchPerIter

The maximum number of line searches per iteration.

TolLineSearch

The relative line-search acceptance tolerance.

LineSearchStepFact

The line-search step factor.

**Remarks**


This function retrieves the solution control parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearStagedSolutionControlParameters()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MaxTotalSteps As Long
Dim MaxFailedSubSteps As Long
Dim MaxIterCS As Long
Dim MaxIterNR As Long
Dim TolConvD As Double
Dim UseEventStepping As Boolean
Dim TolEventD As Double
Dim MaxLineSearchPerIter As Long
Dim TolLineSearch As Double
Dim LineSearchStepFact As Double

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'get solution control parameters
ret = SapModel.LoadCases.StaticNonlinearStaged.GetSolControlParameters("LCASE1",
MaxTotalSteps, MaxFailedSubSteps, MaxIterCS, MaxIterNR, TolConvD, UseEventStepping,
TolEventD, MaxLineSearchPerIter, TolLineSearch, LineSearchStepFact)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetSolControlParameters

# GetStageData_2

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetStageData_2

## VB6 Procedure

Function GetStageData_2(ByVal Name As String, ByVal Stage As Long, ByRef
NumberOperations As Long, ByRef Operation() As Long, ByRef ObjectType() As String, ByRef
ObjectName() As String, ByRef Age() As Double, ByRef MyType() As String, ByRef MyName()
As String, ByRef SF() As Double) As Long

## Parameters

Name

The name of an existing static nonlinear staged load case.

Stage

The stage in the specified load case for which data is requested. Stages are numbered sequentially
starting from 1.

NumberOperations

The number of operations in the specified stage.

Operation

This is an array that includes 1, 2, 3, 4, 5, 6, 7, or 11, indicating an operation type.

```
1 = Add structure
2 = Remove structure
3 = Load objects if new
4 = Load objects
5 = Change section properties
6 = Change section property modifiers
```

```
7 = Change releases
11 = Change section properties and age
```
ObjectType

This is an array that includes the object type associated with the specified operation. The object
type may be one of the following:

```
Group
Frame
Cable
Tendon
Area
Solid
Link
Point
```
The following list shows which object types are applicable to each operation type:

```
Operation = 1 (Add structure): All object types
Operation = 2 (Remove structure): All object types
Operation = 3 (Load objects if new): All object types
Operation = 4 (Load objects): All object types
Operation = 5 (Change section properties): All object types except Point
Operation = 6 (Change section property modifiers): Group, Frame, Cable, Area
Operation = 7 (Change releases): Group, Frame
Operation = 11 (Change section properties and age): All object types except Point
```
ObjectName

This is an array that includes the name of the object associated with the specified operation. This
is the name of a Group, Frame object, Cable object, Tendon object, Area object, Solid object, Link
object or Point object, depending on the ObjectType item.

Age

This is an array that includes the age of the added structure, at the time it is added, in days. This
item applies only to operations with Operation = 1.

MyType

This is an array that includes a load type or an object type, depending on what is specified for the
Operation item. This item applies only to operations with Operation = 3, 4, 5, 6, 7, or 11.

When Operation = 3 or 4, this is an array that includes Load or Accel, indicating the load type of
an added load.

When Operation = 5 or 11, and the ObjectType item is Group, this is an array that includes Frame,
Cable, Tendon, Area, Solid or Link, indicating the object type for which the section property is
changed.

When Operation = 6 and the ObjectType item is Group, this is an array that includes Frame, Cable
or Area, indicating the object type for which the section property modifiers are changed.


When Operation = 7 and the ObjectType item is Group, this is an array that includes Frame,
indicating the object type for which the releases are changed.

When Operation = 5, 6, 7, or 11, and the ObjectType item is not Group and not Point, this item is
ignored and the type is picked up from the ObjectType item.

MyName

This is an array that includes a load assignment or an object name, depending on what is specified
for the Operation item. This item applies only to operations with Operation = 3, 4, 5, 6, 7, or 11.

When Operation = 3 or 4, this is an array that includes the name of the load assigned to the
operation. If the associated LoadType item is Load, this item is the name of a defined load pattern.
If the associated LoadType item is Accel , this item is UX, UY, UZ, RX, RY or RZ, indicating the
direction of the load.

When Operation = 5 or 11, this is the name of a Frame, Cable, Tendon, Area, Solid or Link object,
depending on the object type specified.

When Operation = 6, this is the name of a Frame, Cable or Area object, depending on the object
type specified.

When Operation = 7, this is the name of a Frame object.

SF

This is an array that includes the scale factor for the load assigned to the operation, if any. [L/s^2 ]
for Accel UX UY and UZ; otherwise unitless

This item applies only to operations with Operation = 3 or 4.

**Remarks**

This function retrieves stage data for the specified stage in the specified load case.

The function returns zero if the data is successfully retrieved; otherwise, it returns a nonzero
value.

**VBA Example**

Sub GetCaseStaticNonlinearStagedStageData_2()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDuration() As Double
Dim MyOutput() As Boolean
Dim MyOutputName() As String
Dim MyComment() As String
Dim MyOperation() As Long
Dim MyObjectType() As String
Dim MyObjectName() As String
Dim MyAge() As Double


Dim MyMyType() As String
Dim MyMyName() As String
Dim MySF() As Double
Dim NumberOperations As Long
Dim Operation() As Long
Dim ObjectType() As String
Dim ObjectName() As String
Dim Age() As Double
Dim MyType() As String
Dim MyName() As String
Dim SF() As Double

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("ACASE1")

'initialize stage definitions
ReDim MyDuration(1)
ReDim MyOutput(1)
ReDim MyOutputName(1)
ReDim MyComment(1)
MyDuration(0) = 0
MyOutput(0) = False
MyComment(0) = "Build structure"
MyDuration(1) = 60
MyOutput(1) = True
MyOutputName(1) = "HBC2"
MyComment(1) = "Wait"
ret = SapModel.LoadCases.StaticNonlinearStaged.SetStageDefinitions_2("ACASE1", 2,
MyDuration, MyOutput, MyOutputName, MyComment)

'set stage data
ReDim MyOperation(1)
ReDim MyObjectType(1)
ReDim MyObjectName(1)
ReDim MyAge(1)
ReDim MyMyType(1)
ReDim MyMyName(1)
ReDim MySF(1)


MyOperation(0) = 1
MyObjectType(0) = "Group"
MyObjectName(0) = "ALL"
MyAge(0) = 3
MyOperation(1) = 4
MyObjectType(1) = "Frame"
MyObjectName(1) = "8"
MyMyType(1) = "Load"
MyMyName(1) = "DEAD"
MySF(1) = 0.85
ret = SapModel.LoadCases.StaticNonlinearStaged.SetStageData_2("ACASE1", 1, 2,
MyOperation, MyObjectType, MyObjectName, MyAge, MyMyType, MyMyName, MySF)

'get stage data
ret = SapModel.LoadCases.StaticNonlinearStaged.GetStageData_2("ACASE1", 1,
NumberOperations, Operation, ObjectType, ObjectName, Age, MyType, MyName, SF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

This function supersedes GetStageData_1.

## See Also

SetStageData_2

# GetStageDefinitions_2

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetStageDefinitions_2

## VB6 Procedure

Function GetStageDefinitions_2(ByVal Name As String, ByRef NumberStages As Long, ByRef
Duration() As Double, ByRef Output() As Boolean, ByRef OutputName() As String, ByRef
Comment() As String) As Long

## Parameters

Name


The name of an existing static nonlinear staged load case.

NumberStages

The number of stages defined for the specified load case.

Duration

This is an array that includes the duration in days for each stage.

Output

This is an array that includes True or False, indicating if analysis output is to be saved for each
stage.

OutputName

This is an array that includes a user-specified output name for each stage.

Comment

This is an array that includes a comment for each stage. The comment may be a blank string.

**Remarks**

This function retrieves the stage definition data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearStagedStageDefinitions_2()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDuration() As Double
Dim MyOutput() As Boolean
Dim MyOutputName() As String
Dim MyComment() As String
Dim NumberStages As Long
Dim Duration() As Double
Dim Output() As Boolean
Dim OutputName() As String
Dim Comment() As String

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("ACASE1")

'initialize stage definitions
ReDim MyDuration(1)
ReDim MyOutput(1)
ReDim MyOutputName(1)
ReDim MyComment(1)
MyDuration(0) = 0
MyOutput(0) = False
MyComment(0) = "Build structure"
MyDuration(1) = 60
MyOutput(1) = True
MyOutputName(1) = "HBC2"
MyComment(1) = "Wait"
ret = SapModel.LoadCases.StaticNonlinearStaged.SetStageDefinitions_2("ACASE1", 2,
MyDuration, MyOutput, MyOutputName, MyComment)

'get stage definitions
ret = SapModel.LoadCases.StaticNonlinearStaged.GetStageDefinitions_2("ACASE1",
NumberStages, Duration, Output, OutputName, Comment)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

This function supersedes GetStageDefinitions_1

## See Also

SetStageDefinitions_2

# GetTargetForceParameters

## Syntax


SapObject.SapModel.LoadCases.StaticNonlinearStaged.GetTargetForceParameters

**VB6 Procedure**

Function GetTargetForceParameters(ByVal Name As String, ByRef TolConvF As Double, ByRef
MaxIter As Long, ByRef AccelFact As Double, ByRef NoStop As Boolean) As Long

**Parameters**

Name

The name of an existing static nonlinear staged analysis case.

TolConvF

The relative convergence tolerance for target force iteration.

MaxIter

The maximum iterations per stage for target force iteration.

AccelFact

The acceleration factor.

NoStop

If this item is True, the analysis is continued when there is no convergence in the target force
iteration.

**Remarks**

This function retrieves the target force iteration parameters for the specified load case.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseStaticNonlinearStagedTargetForceParameters()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim TolConvF As Double
Dim MaxIter As Long
Dim AccelFact As Double
Dim NoStop As Boolean

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'get target force iteration parameters
ret = SapModel.LoadCases.StaticNonlinearStaged.GetTargetForceParameters("LCASE1",
TolConvF, MaxIter, AccelFact, NoStop)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetTargetForceParameters

# SetCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long


**Parameters**

Name

The name of an existing or new load case. If this is an existing case, that case is modified,
otherwise, a new case is added.

**Remarks**

This function initializes a static nonlinear staged analysis case. If this function is called for an
existing load case, all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticNonlinearStaged()
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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetGeometricNonlinearity

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetGeometricNonlinearity

## VB6 Procedure

Function SetGeometricNonlinearity(ByVal Name As String, ByVal NLGeomType As Long) As
Long

## Parameters

Name

The name of an existing static nonlinear staged analysis case.

NLGeomType

This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.

```
0 = None
1 = P-delta
2 = P-delta plus large displacements
```
## Remarks

This function sets the geometric nonlinearity option for the specified load case.

The function returns zero if the option is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetCaseStaticNonlinearStagedGeometricNonlinearity()
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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'set geometric nonlinearity option
ret = SapModel.LoadCases.StaticNonlinearStaged.SetGeometricNonlinearity("LCASE1", 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetGeometricNonlinearity

# SetHingeUnloading

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetHingeUnloading

## VB6 Procedure

Function SetHingeUnloading(ByVal Name As String, ByVal UnloadType As Long) As Long

## Parameters

Name


The name of an existing static nonlinear staged analysis case.

UnloadType

This is 1, 2 or 3, indicating the hinge unloading option selected for the load case.

```
1 = Unload entire structure
2 = Apply local redistribution
3 = Restart using secant stiffness
```
**Remarks**

This function sets the hinge unloading option for the specified load case.

The function returns zero if the option is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseStaticNonlinearStagedHingeUnloading()
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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'set hinge unloading option
ret = SapModel.LoadCases.StaticNonlinearStaged.SetHingeUnloading("LCASE1", 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetHingeUnloading

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing static nonlinear staged analysis case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts from the state at the end
of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the state at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseStaticNonlinearStagedInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.StaticNonlinearStaged.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetMassSource

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetMassSource


**VB6 Procedure**

Function SetMassSource(ByVal Name As String, ByVal Source As String) As Long

**Parameters**

Name

The name of an existing static nonlinear load case.

Source

This is the name of an existing mass source or a blank string. Blank indicates to use the mass
source from the previous load case or the default mass source if the load case starts from zero
initial conditions.

**Remarks**

This function sets the mass source to be used for the specified load case.

The function returns zero if the mass source is data is successfully set; otherwise it returns a
nonzero value.

**VBA Example**

Sub SetCaseStaticNonlinearStagedMassSource()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")


'add a new mass source and make it the default mass source

LoadPat(0) = "DEAD"

SF(0) = 1.25

ret = SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True, True, 1,
LoadPat, SF)

'assign a mass source to the static nonlinear load case

ret = SapModel.LoadCases.StaticNonlinearStaged.SetMassSource("LCASE1",
"MyMassSource")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.20.

## See Also

GetMassSource

# SetMaterialNonlinearity

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetMaterialNonlinearity

## VB6 Procedure

Function SetMaterialNonlinearity(ByVal Name As String, ByVal TimeDepMatProp As Boolean)
As Long

## Parameters

Name

The name of an existing static nonlinear staged analysis case.

TimeDepMatProp

When this is True, any specified time dependent material properties are considered in the analysis.


**Remarks**

This function sets the material nonlinearity options for the specified load case.

The function returns zero if the options are successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseStaticNonlinearStagedMaterialNonlinearity()
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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'set geometric nonlinearity options
ret = SapModel.LoadCases.StaticNonlinearStaged.SetMaterialNonlinearity("LCASE1", True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**


GetMaterialNonlinearity

# SetResultsSaved

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetResultsSaved

## VB6 Procedure

Function SetResultsSaved(ByVal Name As String, ByVal StagedSaveOption As Long, Optional
ByVal StagedMinSteps As Long = 1, Optional ByVal StagedMinStepsTD As Long = 1) As Long

## Parameters

Name

The name of an existing static nonlinear staged analysis case.

StagedSaveOption

This is 0, 1, 2 or 3, indicating the results saved option for the load case.

```
0 = End of final stage
1 = End of each stage
2 = Start and end of each stage
3 = Two or more times in each stage
```
StagedMinSteps

The minimum number of steps for application of instantaneous load. This item applies only when
StagedSaveOption = 3.

StagedMinStepsTD

The minimum number of steps for analysis of time dependent items. This item applies only when
StagedSaveOption = 3.

## Remarks

This function sets the results saved parameters for the specified load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseStaticNonlinearStagedResultsSaved()
'dimension variables|


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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'set results saved parameters
ret = SapModel.LoadCases.StaticNonlinearStaged.SetResultsSaved("LCASE1", 3, 4, 10)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetResultsSaved

# SetStageData_2

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetStageData_2


**VB6 Procedure**

Function SetStageData_2(ByVal Name As String, ByVal Stage As Long, ByVal
NumberOperations As Long, ByRef Operation() As Long, ByRef ObjectType() As String, ByRef
ObjectName() As String, ByRef Age() As Double, ByRef MyType() As String, ByRef MyName()
As String, ByRef SF() As Double) As Long

**Parameters**

Name

The name of an existing static nonlinear staged load case.

Stage

The stage in the specified load case to which the data applies. Stages are numbered sequentially
starting from 1.

NumberOperations

The number of operations in the specified stage.

Operation

This is an array that includes 1, 2, 3, 4, 5, 6, 7, or 11, indicating an operation type.

```
1 = Add structure
2 = Remove structure
3 = Load objects if new
4 = Load objects
5 = Change section properties
6 = Change section property modifiers
7 = Change releases
11 = Change section properties and age
```
ObjectType

This is an array that includes the object type associated with the specified operation. The object
type may be one of the following:

```
Group
Frame
Cable
Tendon
Area
Solid
Link
Point
```
The following list shows which object types are applicable to each operation type:

```
Operation = 1 (Add structure): All object types
```

```
Operation = 2 (Remove structure): All object types
Operation = 3 (Load objects if new): All object types
Operation = 4 (Load objects): All object types
Operation = 5 (Change section properties): All object types except Point
Operation = 6 (Change section property modifiers): Group, Frame, Cable, Area
Operation = 7 (Change releases): Group, Frame
Operation = 11 (Change section properties and age): All object types except Point
```
ObjectName

This is an array that includes the name of the object associated with the specified operation. This
is the name of a Group, Frame object, Cable object, Tendon object, Area object, Solid object, Link
object or Point object, depending on the ObjectType item.

Age

This is an array that includes the age of the added structure, at the time it is added, in days. This
item applies only to operations with Operation = 1.

MyType

This is an array that includes a load type or an object type, depending on what is specified for the
Operation item. This item applies only to operations with Operation = 3, 4, 5, 6, 7, or 11.

When Operation = 3 or 4, this is an array that includes Load or Accel, indicating the load type of
an added load.

When Operation = 5 or 11, and the ObjectType item is Group, this is an array that includes Frame,
Cable, Tendon, Area, Solid or Link, indicating the object type for which the section property is
changed.

When Operation = 6 and the ObjectType item is Group, this is an array that includes Frame, Cable
or Area, indicating the object type for which the section property modifiers are changed.

When Operation = 7 and the ObjectType item is Group, this is an array that includes Frame,
indicating the object type for which the releases are changed.

When Operation = 5, 6, 7, or 11, and the ObjectType item is not Group and not Point, this item is
ignored and the type is picked up from the ObjectType item.

MyName

This is an array that includes a load assignment or an object name, depending on what is specified
for the Operation item. This item applies only to operations with Operation = 3, 4, 5, 6, 7 or 11.

When Operation = 3 or 4, this is an array that includes the name of the load assigned to the
operation. If the associated LoadType item is Load, this item is the name of a defined load pattern.
If the associated LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the
direction of the load.

When Operation = 5 or 11, this is the name of a Frame, Cable, Tendon, Area, Solid or Link object,
depending on the object type specified.

When Operation = 6, this is the name of a Frame, Cable or Area object, depending on the object
type specified.


When Operation = 7, this is the name of a Frame object.

SF

This is an array that includes the scale factor for the load assigned to the operation, if any. [L/s^2 ]
for Accel UX UY and UZ; otherwise unitless

This item applies only to operations with Operation = 3 or 4.

**Remarks**

This function sets the stage data for the specified stage in the specified load case. All previous
stage data for the specified stage is cleared when this function is called.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseStaticNonlinearStagedStageData_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDuration() As Double
Dim MyOutput() As Boolean
Dim MyOutputName() As String
Dim MyComment() As String
Dim MyOperation() As Long
Dim MyObjectType() As String
Dim MyObjectName() As String
Dim MyAge() As Double
Dim MyMyType() As String
Dim MyMyName() As String
Dim MySF() As Double

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("ACASE1")


'initialize stage definitions
ReDim MyDuration(1)
ReDim MyOutput(1)
ReDim MyOutputName(1)
ReDim MyComment(1)
MyDuration(0) = 0
MyOutput(0) = False
MyComment(0) = "Build structure"
MyDuration(1) = 60
MyOutput(1) = True
MyOutputName(1) = "HBC2"
MyComment(1) = "Wait"
ret = SapModel.LoadCases.StaticNonlinearStaged.SetStageDefinitions_2("ACASE1", 2,
MyDuration, MyOutput, MyOutputName, MyComment)

'set stage data
ReDim MyOperation(1)
ReDim MyObjectType(1)
ReDim MyObjectName(1)
ReDim MyAge(1)
ReDim MyMyType(1)
ReDim MyMyName(1)
ReDim MySF(1)
MyOperation(0) = 1
MyObjectType(0) = "Group"
MyObjectName(0) = "ALL"
MyAge(0) = 3
MyOperation(1) = 4
MyObjectType(1) = "Frame"
MyObjectName(1) = "8"
MyMyType(1) = "Load"
MyMyName(1) = "DEAD"
MySF(1) = 0.85
ret = SapModel.LoadCases.StaticNonlinearStaged.SetStageData_2("ACASE1", 1, 2,
MyOperation, MyObjectType, MyObjectName, MyAge, MyMyType, MyMyName, MySF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 19.0.0.

This function supersedes SetStageData_1.

**See Also**


GetStageData_2

# SetStageDefinitions_2

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetStageDefinitions_2

## VB6 Procedure

Function SetStageDefinitions_2(ByVal Name As String, ByVal NumberStages As Long, ByRef
Duration() As Double, ByRef Output() As Boolean, ByRef OutputName() As String, ByRef
Comment() As String) As Long

## Parameters

Name

The name of an existing static nonlinear staged load case.

NumberStages

The number of stages defined for the specified load case.

Duration

This is an array that includes the duration in days for each stage.

Output

This is an array that includes True or False, indicating if analysis output is to be saved for each
stage.

OutputName

This is an array that includes a user-specified output name for each stage.

Comment

This is an array that includes a comment for each stage. The comment may be a blank string.

## Remarks

This function initializes the stage definition data for the specified load case. All previous stage
definition data for the case is cleared when this function is called.

The function returns zero if the data is successfully initialized; otherwise, it returns a nonzero
value.


**VBA Example**

Sub SetCaseStaticNonlinearStagedStageDefinitions_2()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDuration() As Double
Dim MyOutput() As Boolean
Dim MyOutputName() As String
Dim MyComment() As String

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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("ACASE1")

'initialize stage definitions
ReDim MyDuration(1)
ReDim MyOutput(1)
ReDim MyOutputName(1)
ReDim MyComment(1)
MyDuration(0) = 0
MyOutput(0) = False
MyComment(0) = "Build structure"
MyDuration(1) = 60
MyOutput(1) = True
MyOutputName(1) = "HBC2"
MyComment(1) = "Wait"
ret = SapModel.LoadCases.StaticNonlinearStaged.SetStageDefinitions_2("ACASE1", 2,
MyDuration, MyOutput, MyOutputName, MyComment)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 19.0.0.

This function supersedes GetStageDefinitions_1.

## See Also

GetStageDefinitions_2

# SetSolControlParameters

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetSolControlParameters

## VB6 Procedure

Function SetSolControlParameters(ByVal Name As String, ByVal MaxTotalSteps As Long,
ByVal MaxFailedSubSteps As Long, ByVal MaxIterCS As Long, ByVal MaxIterNR As Long,
ByVal TolConvD As Double, ByVal UseEventStepping As Boolean, ByVal TolEventD As
Double, ByVal MaxLineSearchPerIter As Long, ByVal TolLineSearch As Double, ByVal
LineSearchStepFact As Double) As Long

## Parameters

Name

The name of an existing static nonlinear load case.

MaxTotalSteps

The maximum total steps per stage.

MaxFailedSubSteps

The maximum null (zero) steps per stage.

MaxIterCS

The maximum constant-stiffness iterations per step.

MaxIterNR

The maximum Newton_Raphson iterations per step.

TolConvD

The relative iteration convergence tolerance.


UseEventStepping

This item is True if event-to-event stepping is used.

TolEventD

The relative event lumping tolerance.

MaxLineSearchPerIter

The maximum number of line searches per iteration.

TolLineSearch

The relative line-search acceptance tolerance.

LineSearchStepFact

The line-search step factor.

**Remarks**

This function sets the solution control parameters for the specified load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticNonlinearStagedSolutionControlParameters()
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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")


'set solution control parameters
ret = SapModel.LoadCases.StaticNonlinearStaged.SetSolControlParameters("LCASE1", 240,
40, 15, 50, 0.00005, False, 0.02, 10, 0.2, 1.7)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetSolControlParameters

# SetTargetForceParameters

## Syntax

SapObject.SapModel.LoadCases.StaticNonlinearStaged.SetTargetForceParameters

## VB6 Procedure

Function SetTargetForceParameters(ByVal Name As String, ByVal TolConvF As Double, ByVal
MaxIter As Long, ByVal AccelFact As Double, ByVal NoStop As Boolean) As Long

## Parameters

Name

The name of an existing static nonlinear staged analysis case.

TolConvF

The relative convergence tolerance for target force iteration.

MaxIter

The maximum iterations per stage for target force iteration.

AccelFact

The acceleration factor.


NoStop

If this item is True, the analysis is continued when there is no convergence in the target force
iteration.

**Remarks**

This function sets the target force iteration parameters for the specified load case.

The function returns zero if the parameters are successfully set; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetCaseStaticNonlinearStagedTargetForceParameters()
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

'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASE1")

'set target force iteration parameters
ret = SapModel.LoadCases.StaticNonlinearStaged.SetTargetForceParameters("LCASE1",
0.008, 6, 5, True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetTargetForceParameters

# GetDampConstant

## Syntax

SapObject.SapModel.LoadCases.SteadyState.GetDampConstant

## VB6 Procedure

Function GetDampConstant(ByVal Name As String, ByRef HysConMassCoeff As Double,
ByRef HysConStiffCoeff As Double) As Long

## Parameters

Name

The name of an existing steady state load case that has constant damping.

HysConMassCoeff

The mass proportional damping coefficient.

HysConStiffCoeff

The stiffness proportional damping coefficient.

## Remarks

This function retrieves the constant hysteretic damping for all frequencies assigned to the
specified load case.

The function returns zero if the damping is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCaseSteadyStateDampConstant()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long


Dim HysConMassCoeff As Double
Dim HysConStiffCoeff As Double

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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'set constant damping
ret = SapModel.LoadCases.SteadyState.SetDampConstant("LCASE1", 0.8, 0.04)

'get constant damping
ret = SapModel.LoadCases.SteadyState.GetDampType("LCASE1", DampType)
If DampType = 1 Then
ret = SapModel.LoadCases.SteadyState.GetDampConstant("LCASE1",HysConMassCoeff,
HysConStiffCoeff)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampConstant

# GetDampInterpolated


**Syntax**

SapObject.SapModel.LoadCases.SteadyState.GetDampInterpolated

**VB6 Procedure**

Function GetDampInterpolated(ByVal Name As String, ByRef HysIntFreqUnits As Long, ByRef
HysIntNumFreqs As Long, ByRef HysIntFreq() As Double, ByRef HysIntMassCoeff() As
Double, ByRef HysIntStiffCoeff() As Double) As Long

**Parameters**

Name

The name of an existing steady state load case that has interpolated damping.

HysIntFreqUnits

This is 1 or 2, indicating the units for the frequency.

```
1 = Hz [cyc/s]
2 = RPM
```
HysIntNumFreqs

The number of sets of frequency, mass coefficient and stiffness coefficient data.

HysIntFreq

This is an array of frequencies. The frequency is in Hz or RPM, depending on the value of
HysIntFreqUnits.

HysIntMassCoeff

This is an array that includes the mass proportional damping coefficient.

HysIntStiffCoeff

This is an array that includes the stiffness proportional damping coefficient.

**Remarks**

This function retrieves the interpolated hysteretic damping by frequency assigned to the specified
load case.

The function returns zero if the damping is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**


Sub GetCaseSteadyStateDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyHysIntFreq() As Double
Dim MyHysIntMassCoeff() As Double
Dim MyHysIntStiffCoeff() As Double
Dim DampType As Long
Dim HysIntFreqUnits As Long
Dim HysIntNumFreqs As Long
Dim HysIntFreq() As Double
Dim HysIntMassCoeff() As Double
Dim HysIntStiffCoeff() As Double

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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'set interpolated damping
ReDim MyHysIntFreq(2)
ReDim MyHysIntMassCoeff(2)
ReDim MyHysIntStiffCoeff(2)
MyHysIntFreq(0) = 1
MyHysIntMassCoeff(0) = 0.6
MyHysIntStiffCoeff(0) = 0.04
MyHysIntFreq(1) = 10
MyHysIntMassCoeff(1) = 0.7
MyHysIntStiffCoeff(1) = 0.05
MyHysIntFreq(2) = 100
MyHysIntMassCoeff(2) = 0.8
MyHysIntStiffCoeff(2) = 0.08
ret = SapModel.LoadCases.SteadyState.SetDampInterpolated("LCASE1", 2, 3,
MyHysIntFreq, MyHysIntMassCoeff, MyHysIntStiffCoeff)

'get interpolated damping
ret = SapModel.LoadCases.SteadyState.GetDampType("LCASE1", DampType)
If DampType = 2 Then
ret = SapModel.LoadCases.SteadyState.GetDampInterpolated("LCASE1",


HysIntFreqUnits, HysIntNumFreqs, HysIntFreq, HysIntMassCoeff, HysIntStiffCoeff)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetDampInterpolated

# GetDampType

## Syntax

SapObject.SapModel.LoadCases.SteadyState.GetDampType

## VB6 Procedure

Function GetDampType(ByVal Name As String, ByRef DampType As Long) As Long

## Parameters

Name

The name of an existing steady state load case.

DampType

This is 1 or 2, indicating the hysteretic damping type for the load case.

```
1 = Constant hysteretic damping for all frequencies
2 = Interpolated hysteretic damping by frequency
```
## Remarks

This function retrieves the hysteretic damping type for the specified load case.

The function returns zero if the type is successfully retrieved; otherwise it returns a nonzero value.


**VBA Example**

Sub GetCaseSteadyStateDampType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DampType As Long

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

'add response spectrum load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'get damping type
ret = SapModel.LoadCases.SteadyState.GetDampType("LCASE1", DampType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetDampConstant

GetDampInterpolated


# GetFreqData

## Syntax

SapObject.SapModel.LoadCases.SteadyState.GetFreqData

## VB6 Procedure

Function GetFreqData(ByVal Name As String, ByRef FreqFirst As Double, ByRef FreqLast As
Double, ByRef FreqNumIncs As Long, ByRef FreqAddModal As Boolean, ByRef
FreqAddModalDev As Boolean, ByRef FreqAddSpecified As Boolean, ByRef
FreqNumModalDev As Long, ByRef FreqModalDev() As Double, ByRef FreqNumSpecified As
Long, ByRef FreqSpecified() As Double) As Long

## Parameters

Name

The name of an existing steady state load case.

FreqFirst

The first frequency. [cyc/s]

FreqLast

The last frequency. [cyc/s]

FreqNumIncs

The number of frequency increments.

FreqAddModal

If this item is True then modal frequencies are added.

FreqAddModalDev

If this item is True then signed fractional deviations from modal frequencies are added.

FreqAddSpecified

If this item is True, specified frequencies are added.

ModalCase

This is the name of an existing modal load case. It specifies the modal load case on which modal
frequencies and modal frequency deviations are based.

FreqNumModalDev


The number of signed fractional deviations from modal frequencies that are added. This item
applies only when FreqAddModalDev = True.

FreqModalDev

This is an array that includes the added signed fractional deviations from modal frequencies. This
item applies only when FreqAddModalDev = True.

FreqNumSpecified

The number of specified frequencies that are added. This item applies only when
FreqAddSpecified = True.

FreqSpecified

This is an array that includes the added specified frequencies. This item applies only when
FreqAddModalDev = True.

**Remarks**

This function retrieves the frequency data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseSteadyStateFreqData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyFreqModalDev() As Double
Dim MyFreqSpecified() As Double
Dim FreqFirst As Double
Dim FreqLast As Double
Dim FreqNumIncs As Long
Dim FreqAddModal As Boolean
Dim FreqAddModalDev As Boolean
Dim FreqAddSpecified As Boolean
Dim ModalCase As String
Dim FreqNumModalDev As Long
Dim FreqModalDev() As Double
Dim FreqNumSpecified As Long
Dim FreqSpecified() As Double

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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'set frequency data
ReDim MyFreqModalDev(1)
ReDim MyFreqSpecified(1)
MyFreqModalDev(0) = -0.1
MyFreqModalDev(1) = 0.2
MyFreqSpecified(0) = 1.2
MyFreqSpecified(1) = 11.4
ret = SapModel.LoadCases.SteadyState.SetFreqData("LCASE1", .6, 20.6, 10, True, True,
True, "MODAL", 2, MyFreqModalDev, 2, MyFreqSpecified)

'get frequency data
ret = SapModel.LoadCases.SteadyState.GetFreqData("LCASE1", FreqFirst, FreqLast,
FreqNumIncs, FreqAddModal, FreqAddModalDev, FreqAddSpecified, ModalCase,
FreqNumModalDev, FreqModalDev, FreqNumSpecified, FreqSpecified)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetFreqData

# GetInitialCase

## Syntax

SapObject.SapModel.LoadCases.SteadyState.GetInitialCase


**VB6 Procedure**

Function GetInitialCase(ByVal Name As String, ByRef InitialCase As String) As Long

**Parameters**

Name

The name of an existing steady state load case.

InitialCase

This is blank, None, or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

**Remarks**

This function retrieves the initial condition assumed for the specified load case.

The function returns zero if the initial condition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetCaseSteadyStateInitialCondition()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim InitialCase As String

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


'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'get initial condition
ret = SapModel.LoadCases.SteadyState.GetInitialCase("LCASE1", InitialCase)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetInitialCase

# GetLoads

## Syntax

SapObject.SapModel.LoadCases.SteadyState.GetLoads

## VB6 Procedure

Function GetLoads(ByVal Name As String, ByRef NumberLoads As Long, ByRef LoadType()
As String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef
PhaseAngle() As Double, ByRef CSys() As String, ByRef Ang() As Double) As Long

## Parameters

Name

The name of an existing steady state load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.


LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the steady state function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

PhaseAngle

This is an array that includes the phase angle. [deg]

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**

This function retrieves the load data for the specified load case.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

**VBA Example**

Sub GetCaseSteadyStateLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String


Dim MySF() As Double
Dim MyPhaseAngle() As Double
Dim MyCSys() As String
Dim MyAng() As Double
Dim NumberLoads As Long
Dim LoadType() As String
Dim LoadName() As String
Dim Func() As String
Dim SF() As Double
Dim PhaseAngle() As Double
Dim CSys() As String
Dim Ang() As Double

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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyPhaseAngle(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "UNIFSS"
MySF(0) = 1.5
MyPhaseAngle(0) = 90
MyLoadType(1) = "Accel"
MyLoadName(1) = "U3"
MyFunc(1) = "UNIFSS"
MySF(1) = 1
MyPhaseAngle(1) = 90
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.SteadyState.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyPhaseAngle, MyCSys, MyAng)


'get load data
ret = SapModel.LoadCases.SteadyState.GetLoads("LCASE1", NumberLoads, LoadType,
LoadName, Func, SF, PhaseAngle, CSys, Ang)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetLoads

# SetCase

## Syntax

SapObject.SapModel.LoadCases.SteadyState.SetCase

## VB6 Procedure

Function SetCase(ByVal Name As String) As Long

## Parameters

Name

The name of an existing or new load case. If this is an existing case then that case is modified,
otherwise, a new case is added.

## Remarks

This function initializes a steady state load case. If this function is called for an existing load case,
all items for the case are reset to their default value.

The function returns zero if the load case is successfully initialized; otherwise it returns a nonzero
value.


## VBA Example

Sub SetCaseSteadyState()
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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# SetDampConstant

## Syntax

SapObject.SapModel.LoadCases.SteadyState.SetDampConstant


**VB6 Procedure**

Function SetDampConstant(ByVal Name As String, ByVal HysConMassCoeff As Double, ByVal
HysConStiffCoeff As Double) As Long

**Parameters**

Name

The name of an existing steady state load case.

HysConMassCoeff

The mass proportional damping coefficient.

HysConStiffCoeff

The stiffness proportional damping coefficient.

**Remarks**

This function sets constant hysteretic damping for all frequencies for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseSteadyStateDampConstant()
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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")


'set constant damping
ret = SapModel.LoadCases.SteadyState.SetDampConstant("LCASE1", 0.8, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampConstant

# SetDampInterpolated

## Syntax

SapObject.SapModel.LoadCases.SteadyState.SetDampInterpolated

## VB6 Procedure

Function SetDampInterpolated(ByVal Name As String, ByVal HysIntFreqUnits As Long, ByVal
HysIntNumFreqs As Long, ByRef HysIntFreq() As Double, ByRef HysIntMassCoeff() As
Double, ByRef HysIntStiffCoeff() As Double) As Long

## Parameters

Name

The name of an existing steady state load case.

HysIntFreqUnits

This is either 1 or 2, indicating the units for the frequency.

```
1 = Hz [cyc/s]
2 = RPM
```
HysIntNumFreqs

The number of sets of frequency, mass coefficient and stiffness coefficient data.


HysIntFreq

This is an array of frequencies. The frequency is either in Hz or RPM depending on the value of
HysIntFreqUnits.

HysIntMassCoeff

This is an array that includes the mass proportional damping coefficient.

HysIntStiffCoeff

This is an array that includes the stiffness proportional damping coefficient.

**Remarks**

This function sets interpolated hysteretic damping by frequency for the specified load case.

The function returns zero if the damping is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseSteadyStateDampInterpolated()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyHysIntFreq() As Double
Dim MyHysIntMassCoeff() As Double
Dim MyHysIntStiffCoeff() As Double

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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'set interpolated damping
ReDim MyHysIntFreq(2)
ReDim MyHysIntMassCoeff(2)
ReDim MyHysIntStiffCoeff(2)


MyHysIntFreq(0) = 1
MyHysIntMassCoeff(0) = 0.6
MyHysIntStiffCoeff(0) = 0.04
MyHysIntFreq(1) = 10
MyHysIntMassCoeff(1) = 0.7
MyHysIntStiffCoeff(1) = 0.05
MyHysIntFreq(2) = 100
MyHysIntMassCoeff(2) = 0.8
MyHysIntStiffCoeff(2) = 0.08
ret = SapModel.LoadCases.SteadyState.SetDampInterpolated("LCASE1", 2, 3,
MyHysIntFreq, MyHysIntMassCoeff, MyHysIntStiffCoeff)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetDampInterpolated

# SetFreqData

## Syntax

SapObject.SapModel.LoadCases.SteadyState.SetFreqData

## VB6 Procedure

Function SetFreqData(ByVal Name As String, ByVal FreqFirst As Double, ByVal FreqLast As
Double, ByVal FreqNumIncs As Long, ByVal FreqAddModal As Boolean, ByVal
FreqAddModalDev As Boolean, ByVal FreqAddSpecified As Boolean, ByVal
FreqNumModalDev As Long, ByRef FreqModalDev() As Double, ByVal FreqNumSpecified As
Long, ByRef FreqSpecified() As Double) As Long

## Parameters

Name

The name of an existing steady state load case.


FreqFirst

The first frequency. [cyc/s]

FreqLast

The last frequency. [cyc/s]

FreqNumIncs

The number of frequency increments.

FreqAddModal

If this item is True, modal frequencies are added.

FreqAddModalDev

If this item is True, signed fractional deviations from modal frequencies are added.

FreqAddSpecified

If this item is True, specified frequencies are added.

ModalCase

This is the name of an existing modal load case. It specifies the modal load case on which modal
frequencies and modal frequency deviations are based.

FreqNumModalDev

The number of signed fractional deviations from modal frequencies that are added. This item
applies only when FreqAddModalDev = True.

FreqModalDev

This is an array that includes the added signed fractional deviations from modal frequencies. This
item applies only when FreqAddModalDev = True.

FreqNumSpecified

The number of specified frequencies that are added. This item applies only when
FreqAddSpecified = True.

FreqSpecified

This is an array that includes the added specified frequencies. This item applies only when
FreqAddModalDev = True.

**Remarks**

This function sets the frequency data for the specified load case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.


**VBA Example**

Sub SetCaseSteadyStateFreqData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyFreqModalDev() As Double
Dim MyFreqSpecified() As Double

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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'set frequency data
ReDim MyFreqModalDev(1)
ReDim MyFreqSpecified(1)
MyFreqModalDev(0) = -0.1
MyFreqModalDev(1) = 0.2
MyFreqSpecified(0) = 1.2
MyFreqSpecified(1) = 11.4
ret = SapModel.LoadCases.SteadyState.SetFreqData("LCASE1", .6, 20.6, 10, True, True,
True, "MODAL", 2, MyFreqModalDev, 2, MyFreqSpecified)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.


## See Also

GetFreqData

# SetInitialCase

## Syntax

SapObject.SapModel.LoadCases.SteadyState.SetInitialCase

## VB6 Procedure

Function SetInitialCase(ByVal Name As String, ByVal InitialCase As String) As Long

## Parameters

Name

The name of an existing steady state load case.

InitialCase

This is blank, None or the name of an existing analysis case. This item specifies if the load case
starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that
occurs at the end of a nonlinear static or nonlinear direct integration time history load case.

If the specified initial case is a nonlinear static or nonlinear direct integration time history load
case, the stiffness at the end of that case is used. If the initial case is anything else, zero initial
conditions are assumed.

## Remarks

This function sets the initial condition for the specified load case.

The function returns zero if the initial condition is successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCaseSteadyStateInitialCondition()
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

'add static nonlinear load case
ret = SapModel.LoadCases.StaticNonlinear.SetCase("SN1")

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'set initial condition
ret = SapModel.LoadCases.SteadyState.SetInitialCase("LCASE1", "SN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetInitialCase

# SetLoads

## Syntax

SapObject.SapModel.LoadCases.SteadyState.SetLoads

## VB6 Procedure

Function SetLoads(ByVal Name As String, ByVal NumberLoads As Long, ByRef LoadType() As
String, ByRef LoadName() As String, ByRef Func() As String, ByRef SF() As Double, ByRef
PhaseAngle() As Double, ByRef CSys() As String, ByRef Ang() As Double) As Long


**Parameters**

Name

The name of an existing steady state load case.

NumberLoads

The number of loads assigned to the specified analysis case.

LoadType

This is an array that includes either Load or Accel, indicating the type of each load assigned to the
load case.

LoadName

This is an array that includes the name of each load assigned to the load case.

If the LoadType item is Load, this item is the name of a defined load pattern.

If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of
the load.

Func

This is an array that includes the name of the steady state function associated with each load.

SF

This is an array that includes the scale factor of each load assigned to the load case. [L/s^2 ] for U1
U2 and U3; otherwise unitless

PhaseAngle

This is an array that includes the phase angle. [deg]

CSys

This is an array that includes the name of the coordinate system associated with each load. If this
item is a blank string, the Global coordinate system is assumed.

This item applies only when the LoadType item is Accel.

Ang

This is an array that includes the angle between the acceleration local 1 axis and the +X-axis of the
coordinate system specified by the CSys item. The rotation is about the Z-axis of the specified
coordinate system. [deg]

This item applies only when the LoadType item is Accel.

**Remarks**


This function sets the load data for the specified analysis case.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

**VBA Example**

Sub SetCaseSteadyStateLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyLoadType() As String
Dim MyLoadName() As String
Dim MyFunc() As String
Dim MySF() As Double
Dim MyPhaseAngle() As Double
Dim MyCSys() As String
Dim MyAng() As Double

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

'add steady state load case
ret = SapModel.LoadCases.SteadyState.SetCase("LCASE1")

'set load data
ReDim MyLoadType(1)
ReDim MyLoadName(1)
ReDim MyFunc(1)
ReDim MySF(1)
ReDim MyPhaseAngle(1)
ReDim MyCSys(1)
ReDim MyAng(1)
MyLoadType(0) = "Load"
MyLoadName(0) = "DEAD"
MyFunc(0) = "UNIFSS"
MySF(0) = 1.5
MyPhaseAngle(0) = 90
MyLoadType(1) = "Accel"
MyLoadName(1) = "U3"


MyFunc(1) = "UNIFSS"
MySF(1) = 1
MyPhaseAngle(1) = 90
MyCSys(1) = "Global"
MyAng(1) = 10
ret = SapModel.LoadCases.SteadyState.SetLoads("LCASE1", 2, MyLoadType,
MyLoadName, MyFunc, MySF, MyPhaseAngle, MyCSys, MyAng)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

**See Also**

GetLoads


