# Change Name {Mass Source}

## Syntax

SapObject.SapModel.SourceMass.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name
The name of an existing mass source.
NewName
The new name for the mass source.

## Remarks

This function changes the name of an existing mass source.
The function returns zero if the mass source is successfully changed, otherwise it returns a
nonzero value. If the new name already exists, a nonzero value is returned and the mass source
name is not changed.

## VBA Example

Sub ChangeMassSourceName()
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

'change mass source name from MSSSRC1 to MyMassSource
ret = SapModel.SourceMass.ChangeName("MSSSRC1", "MyMassSource")
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0..

## See Also

# Count {Mass Source}

## Syntax

SapObject.SapModel.SourceMass.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

This function returns the number of defined mass sources.

## VBA Example

Sub CountMassSources()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Count As Long
Dim LoadPat(0) As String


Dim SF(0) As Double
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

'add a new mass source and make it the default mass sourc
LoadPat(0) = "DEAD"
SF(0) = 1.
ret = SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True, True, 1,
LoadPat, SF)

'get mass source count
Count = SapModel.SourceMass.Count
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# Delete {Mass Source}

## Syntax

SapObject.SapModel.SourceMass.Delete


## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name
The name of the mass source to be deleted.

## Remarks

This function deletes an existing mass source.
The function returns zero if the mass source is successfully deleted; otherwise it returns a nonzero
value. If the mass source to be deleted is the default mass source, a nonzero value is returned and
th mass source is not deleted.

## VBA Example

Sub DeleteMassSource()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Count As Long
Dim LoadPat(0) As String
Dim SF(0) As Double

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
'add a new mass source and make it the default mass source
LoadPat(0) = "DEAD"
SF(0) = 1.


ret = SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True, True, 1,
LoadPat, SF)

'delete mass source MSSSRC
ret = SapModel.SourceMass.Delete("MSSSRC1")
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# Get Default {Mass Source}

## Syntax

SapObject.SapModel.SourceMass.GetDefault

## VB6 Procedure

Function GetDefault(ByRef Name As String) As Long

## Parameters

Name
The name of the default mass source.

## Remarks

This function retrieves the default mass source.
The function returns zero if the default mass source is successfully retrieved, otherwise it returns
nonzero.

## VBA Example

Sub GetDefaultMassSource()
'dimension variables


```
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim LoadPat(0) As String
Dim SF(0) As Double
Dim DefaultMassSource As String
```
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

'add a new mass source and make it the default mass source
LoadPat(0) = "DEAD"
SF(0) = 1.
ret = SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True,
True, 1, LoadPat, SF)

'get the default mass source


```
ret = SapModel.SourceMass.GetDefault(DefaultMassSource)
```
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# Get Mass Source

## Syntax

SapObject.SapModel.SourceMass.GetMassSource

## VB6 Procedure

Function GetMassSource (ByVal Name As String, ByRef MassFromElements As Boolean, ByRef
MassFromMasses As Boolean, ByRef MassFromLoads As Boolean, ByRef IsDefault As Boolean,
ByRef NumberLoads As Long, ByRef LoadPat() As String, ByRef SF() As Double) As Long

## Parameters

Name
The mass source name.
MassFromElements
If this item is True then element self mass is included in the mass.
MassFromMasses
If this item is True then assigned masses are included in the mass.
MassFromLoads
If this item is True then specified load patterns are included in the mass.


IsDefault
If this item is True then the mass source is the default mass source.
NumberLoads
The number of load patterns specified for the mass source. This item is only applicable when the
MassFromLoads item is True.
LoadPat
This is an array of load pattern names specified for the mass source.
SF
This is an array of load pattern multipliers specified for the mass source.

## Remarks

This function gets the mass source data for an existing mass source.
The function returns zero if the mass source data is successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetMassSource()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MassFromElements As Boolean
Dim MassFromMasses As Boolean
Dim MassFromLoads As Boolean
Dim IsDefault As Boolean
Dim NumberLoads As Long
Dim LoadPat() As String
Dim SF() As Double

```
'create Sap2000 object
```

```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
SapObject.ApplicationStart
```
```
'create SapModel object
Set SapModel = SapObject.SapModel
```
```
'initialize model
ret = SapModel.InitializeNewModel
```
```
'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
```
'get data for mass source MSSSRC
ret = SapModel.SourceMass.GetMassSource("MSSSRC1", MassFromElements,
MassFromMasses, MassFromLoads, IsDefault, NumberLoads, LoadPat, SF)
```
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# Get Name List


## Syntax

SapObject.SapModel.SourceMass.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames
The number of mass source names retrieved by the program.
MyName
This is a one-dimensional array of mass source names. The MyName array is created as a
dynamic, zero-based, array by the API user:
Dim MyName() as String
The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined mass sources.
The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetMassSourceNames()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberNames As Long
Dim MyName() As String

```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```

```
'start Sap2000 application
SapObject.ApplicationStart
```
```
'create SapModel object
Set SapModel = SapObject.SapModel
```
```
'initialize model
ret = SapModel.InitializeNewModel
```
```
'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
```
'get mass source names
ret = SapModel.SourceMass.GetNameList(NumberNames, MyName)
```
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# Set Default

## Syntax


SapObject.SapModel.SourceMass.SetDefault

## VB6 Procedure

Function SetDefault(ByVal Name As String) As Long

## Parameters

Name
The name of the mass source to be flagged as the default mass source.

## Remarks

This function sets the default mass source.
The function returns zero if the mass source is successfully flagged as default, otherwise it returns
nonzero. Only one mass source can be the default mass source so when this assignment is set all
other mass sources are automatically set to have their IsDefault flag False.

## VBA Example

Sub SetDefaultMassSource()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim LoadPat(0) As String
Dim SF(0) As Double

```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
SapObject.ApplicationStart
```
```
'create SapModel object
```

```
Set SapModel = SapObject.SapModel
```
```
'initialize model
ret = SapModel.InitializeNewModel
```
```
'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
```
'add a new mass source and do NOT make it the default mass source
LoadPat(0) = "DEAD"
SF(0) = 1.
ret = SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True,
False, 1, LoadPat, SF)
```
```
'set MyMassSource as the default mass source
ret = SapModel.SourceMass.SetDefault("MyMassSource")
```
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.


## See Also

# Set Mass Source

## Syntax

SapObject.SapModel.SourceMass.SetMassSource

## VB6 Procedure

Function SetMassSource(ByVal Name As String, ByVal MassFromElements As Boolean, ByVal
MassFromMasses As Boolean, ByVal MassFromLoads As Boolean, ByVal IsDefault As Boolean,
ByVal NumberLoads As Long, ByRef LoadPat() As String, ByRef SF() As Double) As Long

## Parameters

Name
The mass source name. If a mass source with this name already exists then the mass source is
reinitialized with the new data. All previous data assigned to the mass source is lost. If a mass
source with this name does not exist then a new mass source is added.
MassFromElements
If this item is True then element self mass is included in the mass.
MassFromMasses
If this item is True then assigned masses are included in the mass.
MassFromLoads
If this item is True then specified load patterns are included in the mass.
IsDefault
If this item is True then the mass source is the default mass source. Only one mass source can be
the default mass source so when this assignment is True all other mass sources are automatically
set to have the IsDefault flag False.
NumberLoads
The number of load patterns specified for the mass source. This item is only applicable when the
MassFromLoads item is True.
LoadPat
This is an array of load pattern names specified for the mass source.
SF


This is an array of load pattern multipliers specified for the mass source.

## Remarks

This function adds a new mass source to the model or reinitializes an existing mass source.
The function returns zero if the mass source is successfully added or initialized, otherwise it
returns a nonzero value.

## VBA Example

Sub SetMassSource()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim LoadPat(0) As String
Dim SF(0) As Double

```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
SapObject.ApplicationStart
```
```
'create SapModel object
Set SapModel = SapObject.SapModel
```
```
'initialize model
ret = SapModel.InitializeNewModel
```
```
'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```

```
'add a new mass source and make it the default mass source
LoadPat(0) = "DEAD"
SF(0) = 1.
ret = SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True,
True, 1, LoadPat, SF)
```
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also


