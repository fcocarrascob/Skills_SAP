# Count

## Syntax

Sap2000.AreaElm.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

This function returns the total number of area elements in the analysis model.

## VBA Example

Sub CountAreaElements()
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
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign auto mesh options
ret = SapModel.AreaObj.SetAutoMesh("ALL", 1, 3, 3, , , , , , , , , , , , , , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel


'return number of area elements
Count = SapModel.AreaElm.Count

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetLoadGravity

## Syntax

SapObject.SapModel.AreaElm.GetLoadGravity

## VB6 Procedure

Function GetLoadGravity(ByVal Name As String, ByRef NumberItems As Long, ByRef
AreaName() As String, ByRef LoadPat() As String, ByRef CSys() As String, ByRef x() As
Double, ByRef y() As Double, ByRef z() As Double, Optional ByVal ItemTypeElm As
eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing area element or group, depending on the value of the ItemType item.

NumberItems

The total number of gravity loads retrieved for the specified area elements.

AreaName

This is an array that includes the name of the area element associated with each gravity load.

LoadPat

This is an array that includes the name of the coordinate system in which the gravity load
multipliers are specified.

CSys


This is an array that includes the name of the coordinate system associated with each gravity load.

x, y, z

These are arrays of gravity load multipliers in the x, y and z directions of the specified coordinate
system.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the area elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the area element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the area elements corresponding to
all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for area elements corresponding to
all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the gravity load assignments to area elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaElementGravityLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim AreaName() As String
Dim LoadPat() As String
Dim CSys() As String
Dim x() As Double
Dim y() As Double
Dim z() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign auto mesh options
ret = SapModel.AreaObj.SetAutoMesh("ALL", 1, 3, 3, , , , , , , , , , , , , , , Group)

'assign area object gravity loads
ret = SapModel.AreaObj.SetLoadGravity("ALL", "DEAD", 0, 0, -1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area element gravity load
ret = SapModel.AreaElm.GetLoadGravity("3-1", NumberItems, AreaName, LoadPat, CSys,
x, y, z)

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

# GetLoadPorePressure

## Syntax

SapObject.SapModel.AreaElm.GetLoadPorePressure

## VB6 Procedure


Function GetLoadPorePressure(ByVal Name As String, ByRef NumberItems As Long, ByRef
AreaName() As String, ByRef LoadPat() As String, ByRef Value() As Double, ByRef
PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing area element or group depending on the value of the ItemType item.

NumberItems

The total number of pore pressure loads retrieved for the specified area elements.

AreaName

This is an array that includes the name of the area element associated with each pore pressure
load.

LoadPat

This is an array that includes the name of the load pattern associated with each pore pressure load.

Value

This is an array that includes the pore pressure load value. [F/L^2 ]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the pore pressure load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the area elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the area element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the area elements corresponding to
all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for area elements corresponding to
all selected area objects, and the Name item is ignored.


## Remarks

This function retrieves the pore pressure load assignments to area elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaElementPorePressureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim AreaName() As String
Dim LoadPat() As String
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign area object pore pressure load
ret = SapModel.AreaObj.SetLoadPorePressure("ALL", "DEAD", .1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area element pore pressure load
ret = SapModel.AreaElm.GetLoadPorePressure("ALL", NumberItems, AreaName, LoadPat,
Value, PatternName, GroupElm)

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

# GetLoadStrain

## Syntax

SapObject.SapModel.AreaElm.GetLoadStrain

## VB6 Procedure

Function GetLoadStrain(ByVal Name As String, ByRef NumberItems As Long, ByRef
AreaName() As String, ByRef LoadPat() As String, ByRef Component() As Long, ByRef Value()
As Double, ByRef PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm =
Element) As Long

## Parameters

Name

The name of an existing area element or group, depending on the value of the ItemType item.

NumberItems

The total number of strain loads retrieved for the specified area elements.

AreaName

This is an array that includes the name of the area element associated with each strain load.

LoadPat

This is an array that includes the name of the load pattern associated with each strain load.

Component

This is an array that includes 1, 2, 3, 4, 5, 6, 7 or 8, indicating the component associated with each
strain load.

```
1 = Strain
2 = Strain
3 = Strain
4 = Curvature
5 = Curvature
```

```
6 = Curvature
7 = Strain
8 = Strain
```
Value

This is an array that includes the strain value. [L/L] for Component = 1, 2, 3, 7 and 8, and [1/L] for
Component = 4, 5 and 6

PatternName

This is an array that includes the joint pattern name, if any, used to specify the strain load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the area elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the area element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the area elements corresponding to
all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for area elements corresponding to
all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the strain load assignments to area elements.

The function returns zero if the strain load assignments are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetAreaElementStrainLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim AreaName() As String
Dim LoadPat() As String
Dim Component() As Long


Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign area object strain load
ret = SapModel.AreaObj.SetLoadStrain("ALL", "DEAD", 1, 0.001, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area element strain load
ret = SapModel.AreaElm.GetLoadStrain("3", NumberItems, AreaName, LoadPat,
Component, Value, PatternName)

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

# GetLoadSurfacePressure

## Syntax

SapObject.SapModel.AreaElm.GetLoadSurfacePressure


## VB6 Procedure

Function GetLoadSurfacePressure(ByVal Name As String, ByRef NumberItems As Long, ByRef
AreaName() As String, ByRef LoadPat() As String, ByRef Face() As Long, ByRef Value() As
Double, ByRef PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm =
Element) As Long

## Parameters

Name

The name of an existing area element or group, depending on the value of the ItemType item.

NumberItems

The total number of surface pressure loads retrieved for the specified area elements.

AreaName

This is an array that includes the name of the area element associated with each surface pressure
load.

LoadPat

This is an array that includes the name of the load pattern associated with each surface pressure
load.

Face

This is an array that includes -1, -2 or a nonzero, positive integer, indicating the area element face
to which the specified load assignment applies.

```
-1 = Bottom face
-2 = Top face
>0 = Edge face
```
Note that edge face n is from area element point n to area element point n + 1. For example, edge
face 2 is from area element point 2 to area element point 3.

Value

This is an array that includes the surface pressure load value. [F/L^2 ]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the surface pressure
load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
```

```
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the area elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the area element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the area elements corresponding to
all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for area elements corresponding to
all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the surface pressure load assignments to area elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaElementSurfacePressureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim AreaName() As String
Dim LoadPat() As String
Dim Face() As Long
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)


'assign area object surface pressure load
ret = SapModel.AreaObj.SetLoadSurfacePressure("ALL", "DEAD", -1, .1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area element surface pressure load
ret = SapModel.AreaElm.GetLoadSurfacePressure("ALL", NumberItems, AreaName,
LoadPat, Face, Value, PatternName, GroupElm)

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

# GetLoadTemperature

## Syntax

SapObject.SapModel.AreaElm.GetLoadTemperature

## VB6 Procedure

Function GetLoadTemperature(ByVal Name As String, ByRef NumberItems As Long, ByRef
AreaName() As String, ByRef LoadPat() As String, ByRef MyType() As Long, ByRef Value() As
Double, ByRef PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm =
Element) As Long

## Parameters

Name

The name of an existing area element or group, depending on the value of the ItemType item.

NumberItems

The total number of temperature loads retrieved for the specified area elements.


AreaName

This is an array that includes the name of the area element associated with each temperature load.

LoadPat

This is an array that includes the name of the load pattern associated with each temperature load.

MyType

This is an array that includes either 1 or 3, indicating the type of temperature load.

```
1 = Temperature
3 = Temperature gradient along local 3 axis
```
Value

This is an array that includes the temperature load value. [T] for MyType= 1 and [T/L] for
MyType= 3

PatternName

This is an array that includes the joint pattern name, if any, used to specify the temperature load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the area elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the area element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the area elements corresponding to
all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for area elements corresponding to
all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the temperature load assignments to area elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetAreaElementTemperatureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim AreaName() As String
Dim LoadPat() As String
Dim MyType() As Long
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign area object temperature load
ret = SapModel.AreaObj.SetLoadTemperature("All", "DEAD", 1, 50, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area element temperature load
ret = SapModel.AreaElm.GetLoadTemperature("ALL", NumberItems, AreaName, LoadPat,
MyType, Value, PatternName, GroupElm)

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

# GetLoadUniform

## Syntax

SapObject.SapModel.AreaElm.GetLoadUniform

## VB6 Procedure

Function GetLoadUniform(ByVal Name As String, ByRef NumberItems As Long, ByRef
AreaName() As String, ByRef LoadPat() As String, ByRef CSys() As String, ByRef Dir() As
Long, ByRef Value() As Double, Optional ByVal ItemTypeElm As eItemTypeElm = Element) As
Long

## Parameters

Name

The name of an existing area element or group, depending on the value of the ItemType item.

NumberItems

The total number of uniform loads retrieved for the specified area elements.

AreaName

This is an array that includes the name of the area element associated with each uniform load.

LoadPat

This is an array that includes the name of the coordinate system in which the uniform load is
specified.

CSys

This is an array that includes the name of the coordinate system associated with each uniform
load.

Dir

This is an integer between 1 and 11, indicating the direction of the load.

```
1 = Local 1 axis (applies only when CSys is Local)
2 = Local 2 axis (applies only when CSys is Local)
3 = Local 3 axis (applies only when CSys is Local)
4 = X direction (does not apply when CSys is Local)
5 = Y direction (does not apply when CSys is Local)
6 = Z direction (does not apply when CSys is Local)
7 = Projected X direction (does not apply when CSys is Local)
8 = Projected Y direction (does not apply when CSys is Local)
```

```
9 = Projected Z direction (does not apply when CSys is Local)
10 = Gravity direction (applies only when CSys is Global)
11 = Projected Gravity direction (applies only when CSys is Global)
```
The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.

Value

The uniform load value. [F/L^2 ]

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the area elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the area element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the area elements corresponding to
all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for area elements corresponding to
all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the uniform load assignments to area elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaElementUniformLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim AreaName() As String
Dim LoadPat() As String
Dim CSys() As String
Dim Dir() As Long
Dim Value() As Double


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign area object uniform loads
ret = SapModel.AreaObj.SetLoadUniform("ALL", "DEAD", -0.01, 2, False, "Local", Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area element uniform load
ret = SapModel.AreaElm.GetLoadUniform("3", NumberItems, AreaName, LoadPat, CSys,
Dir, Value)

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

# GetLocalAxes

## Syntax

SapObject.SapModel.AreaElm.GetLocalAxes

## VB6 Procedure


Function GetLocalAxes(ByVal Name As String, ByRef Ang As Double) As Long

## Parameters

Name

The name of an existing area element.

Ang

This is the angle that the local 1 and 2 axes are rotated about the positive local 3 axis from the
default orientation. The rotation for a positive angle appears counter clockwise when the local +
axis is pointing toward you. [deg]

## Remarks

This function retrieves the local axis angle assignment for area elements.

The function returns zero if the assignment is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetAreaElementLocalAxisAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Ang As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign area object local axis angle
ret = SapModel.AreaObj.SetLocalAxes("3", 30)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel


'get area element local axis angle
ret = SapModel.AreaElm.GetLocalAxes("3", Ang)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetMaterialOverwrite

## Syntax

SapObject.SapModel.AreaElm.GetMaterialOverwrite

## VB6 Procedure

Function GetMaterialOverwrite(ByVal Name As String, ByRef PropName As String) As Long

## Parameters

Name

The name of a defined area element.

PropName

This is None, indicating that no material overwrite exists for the specified area element, or it is the
name of an existing material property.

## Remarks

This function retrieves the material overwrite assigned to an area element, if any. The material
property name is indicated as None if there is no material overwrite assignment.

The function returns zero if the material overwrite assignment is successfully retrieved; otherwise
it returns a nonzero value.

## VBA Example


Sub GetAreaElementMaterialOverwrite()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropName As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign material overwrite
ret = SapModel.AreaObj.SetMaterialOverwrite("3", "A992Fy50")

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get material overwrite assignment to area element
ret = SapModel.AreaElm.GetMaterialOverwrite("3", PropName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetMatTemp

## Syntax

SapObject.SapModel.AreaElm.GetMatTemp


## VB6 Procedure

Function GetMatTemp(ByVal Name As String, ByRef Temp As Double, ByRef PatternName As
String) As Long

## Parameters

Name

The name of an existing area element.

Temp

This is the material temperature value assigned to the area element. [T]

PatternName

This is blank or the name of a defined joint pattern. If it is blank, the material temperature for the
area element is uniform over the element at the value specified by Temp.

If PatternName is the name of a defined joint pattern, the material temperature for the area element
may vary. The material temperature at each corner point around the area element perimeter is
equal to the specified temperature multiplied by the pattern value at the associated point element.
The material temperature at other points in the area element is calculated by interpolation from the
corner points.

## Remarks

This function retrieves the material temperature assignments to area elements.

The function returns zero if the material temperature assignments are successfully retrieved;
otherwise it returns a nonzero value.

## VBA Example

Sub GetAreaElementMatTemp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Temp As Double
Dim PatternName As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel


'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign material temperature
ret = SapModel.AreaObj.SetMatTemp("ALL", 50, , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get material temperature for area element
ret = SapModel.AreaElm.GetMatTemp("3", Temp, PatternName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetModifiers

## Syntax

SapObject.SapModel.AreaElm.GetModifiers

## VB6 Procedure

Function GetModifiers(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing area element.

Value

This is an array of ten unitless modifiers.

```
Value(0) = Membrane f11 modifier
```

```
Value(1) = Membrane f22 modifier
Value(2) = Membrane f12 modifier
Value(3) = Bending m11 modifier
Value(4) = Bending m22 modifier
Value(5) = Bending m12 modifier
Value(6) = Shear v13 modifier
Value(7) = Shear v23 modifier
Value(8) = Mass modifier
Value(9) = Weight modifier
```
## Remarks

This function retrieves the modifier assignment for area elements. The default value for all
modifiers is one.

The function returns zero if the modifier assignments are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetAreaElementModifiers()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
Dim Value() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign modifiers
ReDim Value(9)
For i = 0 To 9
Value(i) = 1
Next i
Value(0) = 0.01
ret = SapModel.AreaObj.SetModifiers("ALL", Value, Group)


'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get modifiers for area element
ReDim Value(9)
ret = SapModel.AreaElm.GetModifiers("3", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetNameList

## Syntax

SapObject.SapModel.AreaElm.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of area element names retrieved by the program.

MyName

This is a one-dimensional array of area element names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames – 1) inside the SAP2000 program, filled with the
names, and returned to the API user.


## Remarks

This function retrieves the names of all defined area elements.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetAreaElementNames()
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
ret = SapModel.File.NewWall(2, 48, 2, 48)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area element names
ret = SapModel.AreaElm.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also


# GetObj

## Syntax

Sap2000.AreaElm.GetObj

## VB6 Procedure

Function GetObj(ByVal Name As String, ByRef Obj As String) As Long

## Parameters

Name

The name of an existing area element.

Obj

The name of the area object from which the area element was created.

## Remarks

This function retrieves the name of the area object from which an area element was created.

The function returns zero if the information is successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetObjForAreaElm()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Obj As String
Dim ObjType As Long
Dim RDI As Double
Dim RDJ As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel


'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign auto mesh options
ret = SapModel.AreaObj.SetAutoMesh("ALL", 1, 3, 3, , , , , , , , , , , , , , , Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get object information for an area element
ret = SapModel.AreaElm.GetObj("3-2", Obj)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetOffsets

## Syntax

SapObject.SapModel.AreaElm.GetOffsets

## VB6 Procedure

Function GetOffsets(ByVal Name As String, ByRef OffsetType As Long, ByRef OffsetPattern As
String, ByRef OffsetPatternSF As Double, ByRef Offset() As Double) As Long

## Parameters

Name

The name of an existing area element.

OffsetType

This is 0, 1 or 2, indicating the joint offset type.

```
0 = No joint offsets
1 = User defined joint offsets specified by joint pattern
2 = User defined joint offsets specified by point
```

OffsetPattern

This item applies only when OffsetType = 1. It is the name of the defined joint pattern that is used
to calculate the joint offsets.

OffsetPatternSF

This item only applies when OffsetType = 1. It is the scale factor applied to the joint pattern when
calculating the joint offsets. [L]

Offset

This item applies only when OffsetType = 2. It is an array of joint offsets for each of the points
that define the area element. [L]

## Remarks

This function retrieves the joint offset assignments for area elements.

The function returns zero if the assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaElementJointOffsets()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i as long
Dim OffsetType As Long
Dim OffsetPattern As String
Dim OffsetPatternSF As Double
Dim Offset() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)


'assign joint offsets
ReDim Offset(3)
For i = 0 To 3
Offset(i) = 12
Next i
ret = SapModel.AreaObj.SetOffsets("ALL", 2, "", 1, Offset, Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get joint offsets for area element
ret = SapModel.AreaElm.GetOffsets("3", OffsetType, OffsetPattern, OffsetPatternSF, Offset)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetPoints

## Syntax

SapObject.SapModel.AreaElm.GetPoints

## VB6 Procedure

Function GetPoints(ByVal Name As String, ByRef NumberPoints As Long, ByRef Point() As
String) As Long

## Parameters

Name

The name of an area element.

NumberPoints

The number of point elements that define the area element.

Point


This is an array containing the names of the point elements that define the area element. The point
names are in order around the area element.

## Remarks

This function retrieves the names of the point elements that define an area element.

The function returns zero if the point element names are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetAreaElmPoints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberPoints As Long
Dim Point() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign auto mesh options
ret = SapModel.AreaObj.SetAutoMesh("ALL", 1, 3, 3, , , , , , , , , , , , , , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get names of points
ret = SapModel.AreaElm.GetPoints("3-2", NumberPoints, Point)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.00.

## See Also

# GetProperty

## Syntax

SapObject.SapModel.AreaElm.GetProperty

## VB6 Procedure

Function GetProperty(ByVal Name As String, ByRef PropName As String) As Long

## Parameters

Name

The name of a defined area element.

PropName

The name of the area property assigned to the area element. This item is None if there is no area
property assigned to the area element.

## Remarks

This function retrieves the area property assigned to an area element.

The function returns zero if the property is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetAreaElementProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropName As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application


SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area property for element
ret = SapModel.AreaElm.GetProperty("1", PropName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetThickness

## Syntax

SapObject.SapModel.AreaElm.GetThickness

## VB6 Procedure

Function GetThickness(ByVal Name As String, ByRef ThicknessType As Long, ByRef
ThicknessPattern As String, ByRef ThicknessPatternSF As Double, ByRef Thickness() As
Double) As Long

## Parameters

Name

The name of an existing area element.

ThicknessType


This is 0, 1 or 2, indicating the thickness overwrite type.

```
0 = No thickness overwrites
1 = User defined thickness overwrites specified by joint pattern
2 = User defined thickness overwrites specified by point
```
ThicknessPattern

This item applies only when ThicknessType = 1. It is the name of the defined joint pattern that is
used to calculate the thicknesses.

ThicknessPatternSF

This item applies only when ThicknessType = 1. It is the scale factor applied to the joint pattern
when calculating the thicknesses. [L]

Thickness

This item applies only when ThicknessType = 2. It is an array of thicknesses at each of the points
that define the area element. [L]

## Remarks

This function retrieves the thickness overwrite assignments for area elements.

The function returns zero if the assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaElementThicknessOverwrites()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i as long
Dim ThicknessType As Long
Dim ThicknessPattern As String
Dim ThicknessPatternSF As Double
Dim Thickness() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model


ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign thickness overwrites
ReDim Thickness(3)
For i = 0 To 3
Thickness(i) = 11
Next i
ret = SapModel.AreaObj.SetThickness("ALL", 2, "", 1, Thickness, Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get thickness overwrites for area element
ret = SapModel.AreaElm.GetThickness("3", ThicknessType, ThicknessPattern,
ThicknessPatternSF, Thickness)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetTransformationMatrix

## Syntax

Sap2000.AreaElm.GetTransformationMatrix

## VB6 Procedure

Function GetTransformationMatrix(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing area element.

Value


Value is an array of nine direction cosines that define the transformation matrix.

The following matrix equation shows how the transformation matrix is used to convert items from
the area element local coordinate system to the global coordinate system.

In the equation c0 through c8 are the nine values from the transformation array, (Local1, Local2,
Local3) are an item (such as a load) in the element local coordinate system, and (GlobalX,
GlobalY, GlobalZ) are the same item in the global coordinate system.

## Remarks

The function returns zero if the transformation matrix is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetAreaElementMatrix()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)

'assign area object local axis angle
ret = SapModel.AreaObj.SetLocalAxes("3", 30)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel


'get area element transformation matrix
redim Value(8)
ret = SapModel.AreaElm.GetTransformationMatrix("3", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Count

## Syntax

Sap2000.LineElm.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

This function returns the total number of line elements in the analysis model.

## VBA Example

Sub CountLineElements()
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'assign automesh options
ret = SapModel.FrameObj.SetAutoMesh("ALL", True, True, True, 2, 0, Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'return number of line elements
Count = SapModel.LineElm.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetEndLengthOffset

## Syntax

SapObject.SapModel.LineElm.GetEndLengthOffset

## VB6 Procedure

Function GetEndLengthOffset(ByVal Name As String, ByRef Length1 As Double, ByRef
Length2 As Double, ByRef rz As Double) As Long

## Parameters

Name


The name of an existing line element.

Length1

The offset length along the 1-axis of the line element at the I-End of the line element. [L]

Length2

The offset along the 1-axis of the line element at the J-End of the line element. [L]

rz

The rigid zone factor. This is the fraction of the end offset length assumed to be rigid for bending
and shear deformations.

## Remarks

This function retrieves the line element end offsets along the 1-axis of the element.

The function returns zero if the offsets are successfully retrieved, otherwise it returns a nonzero
value.

## VBA Example

Sub GetLineElmEndOffsets()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Length1 As Double
Dim Length2 As Double
Dim rz As Double

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

'assign offsets to frame object
ret = SapModel.FrameObj.SetEndLengthOffset("15", False, 12, 12, 0.5)

'assign frame object auto mesh options


ret = SapModel.FrameObj.SetAutoMesh("15", True, False, False, 2, 0)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get offsets for line element
ret = SapModel.LineElm.GetEndLengthOffset("15-1", Length1, Length2, rz)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetInsertionPoint

## Syntax

SapObject.SapModel.LineElm.GetInsertionPoint

## VB6 Procedure

Function GetInsertionPoint(ByVal Name As String, ByRef Offset1() As Double, ByRef Offset2()
As Double) As Long

## Parameters

Name

The name of an existing line element.

Offset1

This is an array of three joint offset distances, in the Global coordinate system, at the I-End of the
line element. [L]

```
Offset1(0) = I-End offset in the global X-axis direction
Offset1(1) = I-End offset in the global Y-axis direction
Offset1(2) = I-End offset in the global Z-axis direction
```
Offset2


This is an array of three joint offset distances, in the Global coordinate system, at the J-End of the
line element. [L]

```
Offset2(0) = J-End offset in the global X-axis direction
Offset2(1) = J-End offset in the global Y-axis direction
Offset2(2) = J-End offset in the global Z-axis direction
```
## Remarks

This function retrieves line element insertion point assignments. The assignments are reported as
end joint offsets.

The function returns zero if the insertion point data is successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmInsertionPoint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
Dim CardinalPoint As Long
Dim Mirror2 As Boolean
Dim StiffTransform As Boolean
Dim Offset1() As Double
Dim Offset2() As Double
Dim CSys As String

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

'assign frame object insertion point
ReDim Offset1(2)
ReDim Offset2(2)
For i=0 To 2
Offset1(i)=10 + i
Offset2(i)=20 + i
Next i


ret = SapModel.FrameObj.SetInsertionPoint("15", 7, False, True, Offset1, Offset2)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element insertion point
ReDim Offset1(2)
ReDim Offset2(2)
ret = SapModel.LineElm.GetInsertionPoint("15-1", Offset1, Offset2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetLoadDeformation

## Syntax

SapObject.SapModel.LineElm.GetLoadDeformation

## VB6 Procedure

Function GetLoadDeformation(ByVal Name As String, ByRef NumberItems As Long, ByRef
LineName() As String, ByRef LoadPat() As String, ByRef dof1() As Boolean, ByRef dof2() As
Boolean, ByRef dof3() As Boolean, ByRef dof4() As Boolean, ByRef dof5() As Boolean, ByRef
dof6() As Boolean, ByRef U1() As Double, ByRef U2() As Double, ByRef U3() As Double,
ByRef R1() As Double, ByRef R2() As Double, ByRef R3() As Double, Optional ByVal
ItemTypeElm As eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing line object, line element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of deformation loads retrieved for the specified line elements.

LineName


This is an array that includes the name of the line element associated with each deformation load.

LoadPat

This is an array that includes the name of the load pattern associated with each deformation load.

dof1, dof2, dof3, dof4, dof5, dof6

These are arrays of boolean values indicating if the considered degree of freedom has a
deformation load.

```
dof1 = U1
dof2 = U2
dof3 = U3
dof4 = R1
dof5 = R2
dof6 = R3
```
U1, U2, U3, R1, R2, R3

These are arrays of deformation load values. The deformations specified for a given degree of
freedom are applicable only if the corresponding DOF item for that degree of freedom is True.

```
U1 = U1 deformation [L]
U2 = U2 deformation [L]
U3 = U3 deformation [L]
R1 = R1 deformation [rad]
R2 = R2 deformation [rad]
R3 = R3 deformation [rad]
```
ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the line elements corresponding to
the line object specified by the Name item.

If this item is Element, the load assignments are retrieved for the line element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the line elements corresponding to
all line objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for line elements corresponding to
all selected line objects, and the Name item is ignored.

## Remarks


This function retrieves the deformation load assignments to line elements.

The function returns zero if the load assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmDeformationLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim d() As double
Dim NumberItems As Long
Dim LineName() As String
Dim LoadPat() As String
Dim dof1() As Boolean
Dim dof2() As Boolean
Dim dof3() As Boolean
Dim dof4() As Boolean
Dim dof5() As Boolean
Dim dof6() As Boolean
Dim U1() As Double
Dim U2() As Double
Dim U3() As Double
Dim R1() As Double
Dim R2() As Double
Dim R3() As Double

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

'assign frame object deformation loads
ReDim DOF(5)
ReDim d(5)
DOF(0) = True
D(0) = 2
ret = SapModel.FrameObj.SetLoadDeformation("ALL", "DEAD", DOF, d, Group)


'assign frame object auto mesh options
ret = SapModel.FrameObj.SetAutoMesh("ALL", True, False, False, 2, 0, Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element deformation loads
ret = SapModel.LineElm.GetLoadDeformation("3-1", NumberItems, LineName, LoadPat,
dof1, dof2, dof3, dof4, dof5, dof6, U1, U2, U3, R1, R2, R3)

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

# GetLoadDistributed

## Syntax

SapObject.SapModel.LineElm.GetLoadDistributed

## VB6 Procedure

Function GetLoadDistributed(ByVal Name As String, ByRef NumberItems As Long, ByRef
LineName() As String, ByRef LoadPat() As String, ByRef MyType() As Long, ByRef CSys() As
String, ByRef Dir() As Long, ByRef RD1() As Double, ByRef RD2() As Double, ByRef Dist1()
As Double, ByRef Dist2() As Double, ByRef Val1() As Double, ByRef Val2() As Double,
Optional ByVal ItemTypeElm As eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing line object, line element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of distributed loads retrieved for the specified line elements.


LineName

This is an array that includes the name of the line element associated with each distributed load.

LoadPat

This is an array that includes the name of the coordinate system in which the distributed loads are
specified.

MyType

This is an array that includes either 1 or 2, indicating the type of distributed load.

```
1 = Force
2 = Moment
```
CSys

This is an array that includes the name of the coordinate system in which each distributed load is
defined. It may be Local or the name of a defined coordinate system.

Dir

This is an array that includes an integer between 1 and 11, indicating the direction of the load.

```
1 = Local 1 axis (only applies when CSys is Local)
2 = Local 2 axis (only applies when CSys is Local)
3 = Local 3 axis (only applies when CSys is Local)
4 = X direction (does not apply when CSys is Local)
5 = Y direction (does not apply when CSys is Local)
6 = Z direction (does not apply when CSys is Local)
7 = Projected X direction (does not apply when CSys is Local)
8 = Projected Y direction (does not apply when CSys is Local)
9 = Projected Z direction (does not apply when CSys is Local)
10 = Gravity direction (only applies when CSys is Global)
11 = Projected Gravity direction (only applies when CSys is Global)
```
The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.

RD1

This is an array that includes the relative distance from the I-End of the line element to the start of
the distributed load.

RD2

This is an array that includes the relative distance from the I-End of the line element to the end of
the distributed load.

Dist1

This is an array that includes the actual distance from the I-End of the line element to the start of
the distributed load. [L]


Dist2

This is an array that includes the actual distance from the I-End of the line element to the end of
the distributed load. [L]

Val1

This is an array that includes the load value at the start of the distributed load. [F/L] when
MyType is 1 and [FL/L] when MyType is 2

Val2

This is an array that includes the load value at the end of the distributed load. [F/L] when MyType
is 1 and [FL/L] when MyType is 2

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the line elements corresponding to
the line object specified by the Name item.

If this item is Element, the load assignments are retrieved for the line element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the line elements corresponding to
all line objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for line elements corresponding to
all selected line objects, and the Name item is ignored.

## Remarks

This function retrieves the distributed load assignments to line elements.

The function returns zero if the load assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmDistributedLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim LineName() As String


Dim LoadPat() As String
Dim MyType() As Long
Dim CSys() As String
Dim Dir() As Long
Dim RD1() As Double
Dim RD2() As Double
Dim Dist1() As Double
Dim Dist2() As Double
Dim Val1() As Double
Dim Val2() As Double

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

'assign frame object distributed loads
ret = SapModel.FrameObj.SetLoadDistributed("14", "DEAD", 1, 10, 0, 1, 0.08, 0.04)

'assign frame object auto mesh options
ret = SapModel.FrameObj.SetAutoMesh("ALL", True, False, False, 2, 0, Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element distributed loads
ret = SapModel.LineElm.GetLoadDistributed("14-1", NumberItems, LineName, LoadPat,
MyType, CSys, Dir, RD1, RD2, Dist1, Dist2, Val1, Val2)

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

# GetLoadGravity

## Syntax

SapObject.SapModel.LineElm.GetLoadGravity

## VB6 Procedure

Function GetLoadGravity(ByVal Name As String, ByRef NumberItems As Long, ByRef
LineName() As String, ByRef LoadPat() As String, ByRef CSys() As String, ByRef x() As
Double, ByRef y() As Double, ByRef z() As Double, Optional ByVal ItemType As eItemType =
Object) As Long

## Parameters

Name

The name of an existing line object, line element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of gravity loads retrieved for the specified line elements.

LineName

This is an array that includes the name of the line element associated with each gravity load.

LoadPat

This is an array that includes the name of the coordinate system in which the gravity load
multipliers are specified.

CSys

This is an array that includes the name of the coordinate system associated with each gravity load.

x, y, z

These are arrays of gravity load multipliers in the x, y and z directions of the specified coordinate
system.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
```

```
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the line elements corresponding to
the line object specified by the Name item.

If this item is Element, the load assignments are retrieved for the line element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the line elements corresponding to
all line objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for line elements corresponding to
all selected line objects, and the Name item is ignored.

## Remarks

This function retrieves the gravity load assignments to line elements.

The function returns zero if the load assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmGravityLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim LineName() As String
Dim LoadPat() As String
Dim CSys() As String
Dim x() As Double
Dim y() As Double
Dim z() As Double

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


'assign frame object gravity loads
ret = SapModel.FrameObj.SetLoadGravity("ALL", "DEAD", 0, 0, -1, , , Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element gravity load
ret = SapModel.LineElm.GetLoadGravity("3-1", NumberItems, LineName, LoadPat, CSys, x,
y, z)

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

# GetLoadPoint

## Syntax

SapObject.SapModel.LineElm.GetLoadPoint

## VB6 Procedure

Function GetLoadPoint(ByVal Name As String, ByRef NumberItems As Long, ByRef LineName
() As String, ByRef LoadPat() As String, ByRef MyType() As Long, ByRef CSys() As String,
ByRef Dir() As Long, ByRef RelDist() As Double, ByRef Dist() As Double, ByRef Val() As
Double, Optional ByVal ItemType As eItemType = Object) As Long

## Parameters

Name

The name of an existing line object, line element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of point loads retrieved for the specified line elements.


LineName

This is an array that includes the name of the line element associated with each point load.

LoadPat

This is an array that includes the name of the coordinate system in which the point loads are
specified.

MyType

This is an array that includes either 1 or 2, indicating the type of point load.

```
1 = Force
2 = Moment
```
CSys

This is an array that includes the name of the coordinate system in which each point load is
defined. It may be Local or the name of a defined coordinate system.

Dir

This is an array that includes an integer between 1 and 11, indicating the direction of the load.

```
1 = Local 1 axis (only applies when CSys is Local)
2 = Local 2 axis (only applies when CSys is Local)
3 = Local 3 axis (only applies when CSys is Local)
4 = X direction (does not apply when CSys is Local)
5 = Y direction (does not apply when CSys is Local)
6 = Z direction (does not apply when CSys is Local)
7 = Projected X direction (does not apply when CSys is Local)
8 = Projected Y direction (does not apply when CSys is Local)
9 = Projected Z direction (does not apply when CSys is Local)
10 = Gravity direction (only applies when CSys is Global)
11 = Projected Gravity direction (only applies when CSys is Global)
```
The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.

RelDist

This is an array that includes the relative distance from the I-End of the line element to the
location where the point load is applied.

Dist

This is an array that includes the actual distance from the I-End of the line element to the location
where the point load is applied. [L]

Val

This is an array that includes the value of the point load. [F] when MyType is 1 and [FL] when
MyType is 2


ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the line elements corresponding to
the line object specified by the Name item.

If this item is Element, the load assignments are retrieved for the line element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the line elements corresponding to
all line objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for line elements corresponding to
all selected line objects, and the Name item is ignored.

## Remarks

This function retrieves the point load assignments to line elements.

The function returns zero if the load assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmPointLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim LineName() As String
Dim LoadPat() As String
Dim MyType() As Long
Dim CSys() As String
Dim Dir() As Long
Dim RelDist() As Double
Dim Dist() As Double
Dim Val() As Double

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

'assign frame object point loads
ret = SapModel.FrameObj.SetLoadPoint("14", "DEAD", 1, 10, .5, 20)
ret = SapModel.FrameObj.SetLoadPoint("15", "DEAD", 1, 10, .5, 20)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element point loads
ret = SapModel.LineElm.GetLoadPoint("ALL", NumberItems, LineName, LoadPat, MyType,
CSys, Dir, RelDist, Dist, Val, GroupElm)

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

# GetLoadStrain

## Syntax

SapObject.SapModel.LineElm.GetLoadStrain

## VB6 Procedure

Function GetLoadStrain(ByVal Name As String, ByRef NumberItems As Long, ByRef LineName
() As String, ByRef LoadPat() As String, ByRef DOF() As Long, ByRef Val() As Double, ByRef
PatternName() As String, Optional ByVal ItemType As eItemType = Object) As Long


## Parameters

Name

The name of an existing line object, line element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of strain loads retrieved for the specified line elements.

LineName

This is an array that includes the name of the line element associated with each strain load.

LoadPat

This is an array that includes the name of the load pattern associated with each strain load.

DOF

This is an array that includes 1, 2, 3, 4, 5 or 6, indicating the degree of freedom associated with
each strain load.

```
1 = Strain11
2 = Strain12
3 = Strain13
4 = Curvature1
5 = Curvature2
6 = Curvature3
```
Val

This is an array that includes the strain value. [L/L] for DOF = 1, 2 and 3 and [1/L] for DOF = 4, 5
and 6

PatternName

This is an array that includes the joint pattern name, if any, used to specify the strain load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the line elements corresponding to
the line object specified by the Name item.

If this item is Element, the load assignments are retrieved for the line element specified by the
Name item.


If this item is GroupElm, the load assignments are retrieved for the line elements corresponding to
all line objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for line elements corresponding to
all selected line objects, and the Name item is ignored.

## Remarks

This function retrieves the strain load assignments to line elements.

The function returns zero if the strain load assignments are successfully retrieved, otherwise it
returns a nonzero value.

## VBA Example

Sub GetLineElmStrainLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim LineName() As String
Dim LoadPat() As String
Dim DOF() As Long
Dim Val() As Double
Dim PatternName() As String

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

'assign frame object strain load
ret = SapModel.FrameObj.SetLoadStrain("1", "DEAD", 1, 0.001)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element strain load
ret = SapModel.LineElm.GetLoadStrain("1-1", NumberItems, LineName, LoadPat, DOF,
Val, PatternName)


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

# GetLoadTargetForce

## Syntax

SapObject.SapModel.LineElm.GetLoadTargetForce

## VB6 Procedure

Function GetLoadTargetForce(ByVal Name As String, ByRef NumberItems As Long, ByRef
LineName() As String, ByRef LoadPat() As String, ByRef dof1() As Boolean, ByRef dof2() As
Boolean, ByRef dof3() As Boolean, ByRef dof4() As Boolean, ByRef dof5() As Boolean, ByRef
dof6() As Boolean, ByRef P() As Double, ByRef V2() As Double, ByRef V3() As Double, ByRef
T() As Double, ByRef M2() As Double, ByRef M3() As Double, ByRef T1() As Double, ByRef
T2() As Double, ByRef T3() As Double, ByRef T4() As Double, ByRef T5() As Double, ByRef
T6() As Double, Optional ByVal ItemType As eItemType = Object) As Long

## Parameters

Name

The name of an existing line object, line element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of deformation loads retrieved for the specified line elements.

LineName

This is an array that includes the name of the line element associated with each target force.

LoadPat

This is an array that includes the name of the load pattern associated with each target force.


dof1, dof2, dof3, dof4, dof5, dof6

These are arrays of boolean values indicating if the considered degree of freedom has a target
force assignment.

```
dof1 = P
dof2 = V2
dof3 = V3
dof4 = T
dof5 = M2
dof6 = M3
```
P, V2, V3, T, M2, M3

These are arrays of target force values. The target forces specified for a given degree of freedom
are only applicable if the corresponding DOF item for that degree of freedom is True.

```
U1 = U1 deformation [L]
U2 = U2 deformation [L]
U3 = U3 deformation [L]
R1 = R1 deformation [rad]
R2 = R2 deformation [rad]
R3 = R3 deformation [rad]
```
T1, T2, T3, T4, T5, T6

These are arrays of the relative distances along the line elements where the target force values
apply. The relative distances specified for a given degree of freedom are only applicable if the
corresponding dofn item for that degree of freedom is True.

```
T1 = relative location for P target force
T2 = relative location for V2 target force
T3 = relative location for V3 target force
T4 = relative location for T target force
T5 = relative location for M2 target force
T6 = relative location for M3 target force
```
ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the line elements corresponding to
the line object specified by the Name item.

If this item is Element, the load assignments are retrieved for the line element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the line elements corresponding to
all line objects included in the group specified by the Name item.


If this item is SelectionElm, the load assignments are retrieved for line elements corresponding to
all selected line objects, and the Name item is ignored.

## Remarks

This function retrieves the target force assignments to line elements.

The function returns zero if the target force assignments are successfully retrieved, otherwise it
returns a nonzero value.

## VBA Example

Sub GetLineElmTargetForce()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim f() As double
Dim RD() As double
Dim NumberItems As Long
Dim LineName() As String
Dim LoadPat() As String
Dim dof1() As Boolean
Dim dof2() As Boolean
Dim dof3() As Boolean
Dim dof4() As Boolean
Dim dof5() As Boolean
Dim dof6() As Boolean
Dim P() As Double
Dim V2() As Double
Dim V3() As Double
Dim T() As Double
Dim M2() As Double
Dim M3() As Double
Dim T1() As Double
Dim T2() As Double
Dim T3() As Double
Dim T4() As Double
Dim T5() As Double
Dim T6() As Double

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

'assign frame object target force
ReDim DOF(5)
ReDim f(5)
ReDim RD(5)
DOF(0) = True
f(0) = 50
RD(0) = 0.4
ret = SapModel.FrameObj.SetLoadTargetForce("1", "DEAD", DOF, f, RD)

'assign frame object auto mesh options
ret = SapModel.FrameObj.SetAutoMesh("ALL", True, False, False, 2, 0, Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element target force
ret = SapModel.LineElm.GetLoadTargetForce("1-1", NumberItems, LineName, LoadPat,
dof1, dof2, dof3, dof4, dof5, dof6, P, V2, V3, T, M2, M3, T1, T2, T3, T4, T5, T6)

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

# GetLoadTemperature

## Syntax

SapObject.SapModel.LineElm.GetLoadTemperature

## VB6 Procedure


Function GetLoadTemperature(ByVal Name As String, ByRef NumberItems As Long, ByRef
LineName() As String, ByRef LoadPat() As String, ByRef MyType() As Long, ByRef Val() As
Double, ByRef PatternName() As String, Optional ByVal ItemType As eItemType = Object) As
Long

## Parameters

Name

The name of an existing line object, line element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of temperature loads retrieved for the specified line elements.

LineName

This is an array that includes the name of the line element associated with each temperature load.

LoadPat

This is an array that includes the name of the load pattern associated with each temperature load.

MyType

This is an array that includes 1, 2 or 3, indicating the type of temperature load.

```
1 = Temperature
2 = Temperature gradient along local 2 axis
3 = Temperature gradient along local 3 axis
```
Val

This is an array that includes the temperature load value. [T] for MyType= 1 and [T/L] for
MyType= 2 and 3

PatternName

This is an array that includes the joint pattern name, if any, used to specify the temperature load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the line elements corresponding to
the line object specified by the Name item.


If this item is Element, the load assignments are retrieved for the line element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the line elements corresponding to
all line objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for line elements corresponding to
all selected line objects, and the Name item is ignored.

## Remarks

This function retrieves the temperature load assignments to line elements.

The function returns zero if the load assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmTemperatureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim LineName() As String
Dim LoadPat() As String
Dim MyType() As Long
Dim Val() As Double
Dim PatternName() As String

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

'assign frame object temperature load
ret = SapModel.FrameObj.SetLoadTemperature("All", "DEAD", 1, 50, , , Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element temperature load


ret = SapModel.LineElm.GetLoadTemperature("ALL", NumberItems, LineName, LoadPat,
MyType, Val, PatternName, GroupElm)

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

# GetLocalAxes

## Syntax

SapObject.SapModel.LineElm.GetLocalAxes

## VB6 Procedure

Function GetLocalAxes(ByVal Name As String, ByRef Ang As Double) As Long

## Parameters

Name

The name of an existing line element.

Ang

This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis, from the
default orientation. The rotation for a positive angle appears counterclockwise when the local +1
axis is pointing toward you. [deg]

## Remarks

This function retrieves the local axis angle assignment for line elements.

The function returns zero if the assignment is successfully retrieved, otherwise it returns a nonzero
value.


## VBA Example

Sub GetLineElmLocalAxisAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Ang As Double

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

'assign frame object local axis angle
ret = SapModel.FrameObj.SetLocalAxes("1", 30)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element local axis angle
ret = SapModel.LineElm.GetLocalAxes("1-1", Ang)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetMaterialOverwrite

## Syntax


SapObject.SapModel.LineElm.GetMaterialOverwrite

## VB6 Procedure

Function GetMaterialOverwrite(ByVal Name As String, ByRef PropName As String) As Long

## Parameters

Name

The name of a defined line element.

PropName

This is None, indicating that no material overwrite exists for the specified line element, or it is the
name of an existing material property.

## Remarks

This function retrieves the material overwrite assigned to a line element, if any. It returns None if
there is no material overwrite assignment.

The function returns zero if the material overwrite assignment is successfully retrieved, otherwise
it returns a nonzero value.

## VBA Example

Sub GetLineElmMaterialOverwrite()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropName As String

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

'assign material overwrite to frame object
ret = SapModel.FrameObj.SetMaterialOverwrite("1", "4000Psi")


'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get material overwrite assignment for line element
ret = SapModel.LineElm.GetMaterialOverwrite("1-1", PropName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetMatTemp

## Syntax

SapObject.SapModel.LineElm.GetMatTemp

## VB6 Procedure

Function GetMatTemp(ByVal Name As String, ByRef Temp As Double, ByRef PatternName As
String) As Long

## Parameters

Name

The name of an existing line element.

Temp

This is the material temperature value assigned to the line element. [T]

PatternName

This is blank or the name of a defined joint pattern. If it is blank, the material temperature for the
line element is uniform along the element at the value specified by Temp.

If PatternName is the name of a defined joint pattern, the material temperature for the line element
may vary from one end to the other. The material temperature at each end of the element is equal
to the specified temperature multiplied by the pattern value at the joint at the end of the line
element.


## Remarks

This function retrieves the material temperature assignments to line elements.

The function returns zero if the material temperature assignments are successfully retrieved,
otherwise it returns a nonzero value.

## VBA Example

Sub GetLineElmMatTemp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Temp As Double
Dim PatternName As String

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

'assign material temperature to frame objects
ret = SapModel.FrameObj.SetMatTemp("ALL", 50, , Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get material temperature for line element
ret = SapModel.LineElm.GetMatTemp("1-1", Temp, PatternName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# GetModifiers

## Syntax

SapObject.SapModel.LineElm.GetModifiers

## VB6 Procedure

Function GetModifiers(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing line element.

Value

This is an array of eight unitless modifiers.

```
Value(0) = Cross sectional area modifier
Value(1) = Shear area in local 2 direction modifier
Value(2) = Shear area in local 3 direction modifier
Value(3) = Torsional constant modifier
Value(4) = Moment of inertia about local 2 axis modifier
Value(5) = Moment of inertia about local 3 axis modifier
Value(6) = Mass modifier
Value(7) = Weight modifier
```
## Remarks

This function retrieves the section modifier assignment for line elements. The default value for all
modifiers is one.

The function returns zero if the modifier assignments are successfully retrieved, otherwise it
returns a nonzero value.

## VBA Example

Sub GetLineElmModifiers()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
Dim Value() As Double


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

'assign modifiers to frame objects
ReDim Value(7)
For i = 0 To 7
Value(i) = 1
Next i
Value(5) = 100
ret = SapModel.FrameObj.SetModifiers("3", Value)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get modifiers for line element
ReDim Value(7)
ret = SapModel.LineElm.GetModifiers("3-1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetNameList

## Syntax

SapObject.SapModel.LineElm.GetNameList


## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of line element names retrieved by the program.

MyName

This is a one-dimensional array of line element names. The MyName array is created as a
dynamic, zero-based, array by the APIuser:

Dim MyName() as String

The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined line elements.

The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetLineElementNames()
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)


'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element names
ret = SapModel.LineElm.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetObj

## Syntax

Sap2000.LineElm.GetObj

## VB6 Procedure

Function GetObj(ByVal Name As String, ByRef Obj As String, ByRef ObjType As Long, ByRef
RDI As Double, RDJ As Double) As Long

## Parameters

Name

The name of an existing line element.

Obj

The name of the frame, cable or tendon object from which the line element was created.

ObjType

This is 0, 1, 2 or 3, indicating the type of object from which the line element was created.

```
0 = Straight frame object
1 = Curved frame object
2 = Cable object
3 = Tendon object
```
RDI


The relative distance from the I-End of the object identified by the Obj item to the I-End of the
considered line element. The relative distance is calculated as the distance from the I-End of the
object to the I-End of the line element divided by the length of the object.

RDJ

The relative distance from the I-End of the object identified by the Obj item to the J-End of the
considered line element. The relative distance is calculated as the distance from the I-End of the
object to the J-End of the line element divided by the length of the object.

## Remarks

This function retrieves information about the object from which a line element was created.

The function returns zero if the information is successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetObjForLineElm()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Obj As String
Dim ObjType As Long
Dim RDI As Double
Dim RDJ As Double

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

'assign auto mesh options
ret = SapModel.FrameObj.SetAutoMesh("ALL", True, True, True, 2, 0, Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get object information for a line element
ret = SapModel.LineElm.GetObj("3-1", Obj, ObjType, RDI, RDJ)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetPDeltaForce

## Syntax

SapObject.SapModel.LineElm.GetPDeltaForce

## VB6 Procedure

Function GetPDeltaForce(ByVal Name As String, ByRef NumberForces As Long, ByRef
PDeltaForce() As Double, ByRef Dir() As Long, ByRef CSys() As String) As Long

## Parameters

Name

The name of an existing line element.

NumberForces

The number of P-Delta forces assigned to the line element.

PDeltaForce

This is an array of the P-Delta force values assigned to the line element. [F]

Dir

This is an array that contains 0, 1, 2 or 3, indicating the direction of each P-Delta force
assignment.

```
0 = Frame object local 1-axis direction
1 = Projected X direction in CSys coordinate system
2 = Projected Y direction in CSys coordinate system
3 = Projected Z direction in CSys coordinate system
```
CSys


This is an array that contains the name of the coordinate system in which each projected P-Delta
force is defined. This item is blank when the Dir item is zero, that is, when the P-Delta force is
defined in the line element local 1-axis direction.

## Remarks

This function retrieves the P-Delta force assignments to line elements.

The function returns zero if the assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmPDeltaForce()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberForces As Long
Dim PDeltaForce() As Double
Dim Dir() As Long
Dim CSys() As String

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

'assign P-Delta force to frame object
ret = SapModel.FrameObj.SetPDeltaForce("ALL", 100, 0, True, , Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get P-Delta force for line element
ret = SapModel.LineElm.GetPDeltaForce("3-1", NumberForces, PDeltaForce, Dir, CSys)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetPoints

## Syntax

SapObject.SapModel.LineElm.GetPoints

## VB6 Procedure

Function GetPoints(ByVal Name As String, ByRef Point1 As String, ByRef Point2 As String) As
Long

## Parameters

Name

The name of a defined line element.

Point1

The name of the point element at the I-End of the specified line element.

Point2

The name of the point element at the J-End of the specified line element.

## Remarks

This function retrieves the names of the point elements at each end of a specified line element.

The function returns zero if the point names are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmPoints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim Point1 As String
Dim Point2 As String

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

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get names of points
ret = SapModel.LineElm.GetPoints("1-1", Point1, Point2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetProperty

## Syntax

SapObject.SapModel.LineElm.GetProperty

## VB6 Procedure

Function GetProperty(ByVal Name As String, ByRef PropName As String, ByRef ObjType As
Long, ByRef Var As Boolean, ByRef sVarRelStartLoc As Double, sVarTotalLength As Double)
As Long


## Parameters

Name

The name of an existing line element.

PropName

The name of the frame section, cable or tendon property assigned to the line element.

ObjType

This is 0, 1, 2 or 3, indicating the type of object from which the line element was created.

```
0 = Straight frame object
1 = Curved frame object
2 = Cable object
3 = Tendon object
```
Var

This item is True if the specified property is a nonprismatic (variable) frame section property.

sVarTotalLength

This is the total assumed length of the nonprismatic section. A zero value for this item means that
the section length is the same as the line element length.

sVarRelStartLoc

This is the relative distance along the nonprismatic section to the I-End (start) of the line element.
This item is ignored when the sVarTotalLengthitem is 0.

## Remarks

This function retrieves the property assignment to a line element.

The function returns zero if the property data is successfully retrieved, otherwise it returns a
nonzero value.

The sVarTotalLength and sVarRelStartLoc items apply only when the Var item is True.

## VBA Example

Sub GetLineElementProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropName As String
Dim ObjType As Long
Dim Var As Boolean
Dim sVarRelStartLoc As Double


Dim sVarTotalLength As Double

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

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get property information for a line element
ret = SapModel.LineElm.GetProperty("3-1", PropName, ObjType, Var, sVarRelStartLoc,
sVarTotalLength)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetReleases

## Syntax

SapObject.SapModel.LineElm.GetReleases

## VB6 Procedure

Function GetReleases(ByVal Name As String, ByRef ii() As Boolean, ByRef jj() As Boolean,
ByRef StartValue() As Double, ByRef EndValue() As Double) As Long


## Parameters

Name

The name of an existing line element.

ii, jj

These are arrays of six booleans indicating the I-End and J-End releases for the line element.

```
ii(0) and jj(0) = U1 release
ii(1) and jj(1) = U2 release
ii(2) and jj(2) = U3 release
ii(3) and jj(3) = R1 release
ii(4) and jj(4) = R2 release
ii(5) and jj(5) = R3 release
```
StartValue, EndValue

These are arrays of six values indicating the I-End and J-End partial fixity springs for the line
element.

```
StartValue(0) and EndValue(0) = U1 partial fixity [F/L]
StartValue(1) and EndValue(1) = U2 partial fixity [F/L]
StartValue(2) and EndValue(2) = U3 partial fixity [F/L]
StartValue(3) and EndValue(3) = R1 partial fixity [FL/rad]
StartValue(4) and EndValue(4) = R2 partial fixity [FL/rad]
StartValue(5) and EndValue(5) = R3 partial fixity [FL/rad]
```
## Remarks

This function retrieves the line element end release and partial fixity assignments.

The function returns zero if the assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineElmEndReleases()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ii() As Boolean
Dim jj() As Boolean
Dim StartValue() As Double
Dim EndValue() As Double

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

'assign end releases to frame object
ReDim ii(5)
ReDim jj(5)
ReDim StartValue(5)
ReDim EndValue(5)
ii(5) = True
jj(5) = True
ret = SapModel.FrameObj.SetReleases("13", ii, jj, StartValue, EndValue)

'assign frame object automesh options
ret = SapModel.FrameObj.SetAutoMesh("13", True, False, False, 2, 0)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get end releases for line element
ReDim ii(5)
ReDim jj(5)
ReDim StartValue(5)
ReDim EndValue(5)
ret = SapModel.LineElm.GetReleases("13-1", ii, jj, StartValue, EndValue)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetTCLimits

## Syntax


SapObject.SapModel.LineElm.GetTCLimits

## VB6 Procedure

Function GetTCLimits(ByVal Name As String, ByRef LimitCompressionExists As Boolean,
ByRef LimitCompression As Double, ByRef LimitTensionExists As Boolean, ByRef
LimitTension As Double) As Long

## Parameters

Name

The name of an existing line element.

LimitCompressionExists

This item is True if a compression force limit exists for the line element.

LimitCompression

The compression force limit for the line element. [F]

LimitTensionExists

This item is True if a tension force limit exists for the line element.

LimitTension

The tension force limit for the line element. [F]

## Remarks

This function retrieves the tension/compression force limit assignments to line elements.

The function returns zero if the assignments are successfully retrieved, otherwise it returns a
nonzero value.

Note that the tension and compression limits are only used in nonlinear analyses.

## VBA Example

Sub GetLineElmTCLimits()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim LimitCompressionExists As Boolean
Dim LimitCompression As Double
Dim LimitTensionExists As Boolean
Dim LimitTension As Double


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

'assign tension/compression limits to frame object
ret = SapModel.FrameObj.SetTCLimits("1", True, -200, True, 30)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get tension/compression limits for line element
ret = SapModel.LineElm.GetTCLimits("1-1", LimitCompressionExists, LimitCompression,
LimitTensionExists, LimitTension)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetTransformationMatrix

## Syntax

Sap2000.LineElm.GetTransformationMatrix

## VB6 Procedure

Function GetTransformationMatrix(ByVal Name As String, ByRef Value() As Double) As Long


## Parameters

Name

The name of an existing line element.

Value

Value is an array of nine direction cosines that define the transformation matrix.

The following matrix equation shows how the transformation matrix is used to convert items from
the line element local coordinate system to the global coordinate system.

In the equation, c0 through c8 are the nine values from the transformation array, (Local1, Local2,
Local3) are an item (such as a load) in the element local coordinate system, and (GlobalX,
GlobalY, GlobalZ) are the same item in the global coordinate system.

## Remarks

The function returns zero if the transformation matrix is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetLineElementMatrix()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value() As Double

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

'assign frame local axis angle
ret = SapModel.FrameObj.SetLocalAxes("3", 30)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get line element transformation matrix
ReDim Value(8)
ret = SapModel.LineElm.GetTransformationMatrix("3-1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Count

## Syntax

Sap2000.LinkElm.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

This function returns the total number of link elements in the analysis model.

## VBA Example

Sub CountLinkElements()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name1 As String
Dim Name2 As String
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add link object by points
ret = SapModel.LinkObj.AddByPoint("3", "", Name1, True)
ret = SapModel.LinkObj.AddByPoint("1", "5", Name2)

'refresh view
ret = SapModel.View.RefreshView

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'return number of link elements
Count = SapModel.LinkElm.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# GetLoadDeformation

## Syntax

SapObject.SapModel.LinkElm.GetLoadDeformation

## VB6 Procedure

Function GetLoadDeformation(ByVal Name As String, ByRef NumberItems As Long, ByRef
LinkName() As String, ByRef LoadPat() As String, ByRef dof1() As Boolean, ByRef dof2() As
Boolean, ByRef dof3() As Boolean, ByRef dof4() As Boolean, ByRef dof5() As Boolean, ByRef
dof6() As Boolean, ByRef U1() As Double, ByRef U2() As Double, ByRef U3() As Double,
ByRef R1() As Double, ByRef R2() As Double, ByRef R3() As Double, Optional ByVal
ItemTypeElm As eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing link object, link element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of deformation loads retrieved for the specified link elements.

LinkName

This is an array that includes the name of the link element associated with each deformation load.

LoadPat

This is an array that includes the name of the load pattern associated with each deformation load.

dof1, dof2, dof3, dof4, dof5, dof6

These are arrays of boolean values, indicating if the considered degree of freedom has a
deformation load.

```
dof1 = U1
dof2 = U2
dof3 = U3
dof4 = R1
dof5 = R2
dof6 = R3
```
U1, U2, U3, R1, R2, R3


These are arrays of deformation load values. The deformations specified for a given degree of
freedom are applicable only if the corresponding DOF item for that degree of freedom is True.

```
U1 = U1 deformation [L]
U2 = U2 deformation [L]
U3 = U3 deformation [L]
R1 = R1 deformation [rad]
R2 = R2 deformation [rad]
R3 = R3 deformation [rad]
```
ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the link elements corresponding to
the link object specified by the Name item.

If this item is Element, the load assignments are retrieved for the link element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the link elements corresponding to
all link objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for link elements corresponding to
all selected link objects, and the Name item is ignored.

## Remarks

This function retrieves the deformation load assignments to link elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkElmDeformationLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim d() As double
Dim NumberItems As Long
Dim LinkName() As String
Dim LoadPat() As String
Dim dof1() As Boolean
Dim dof2() As Boolean


Dim dof3() As Boolean
Dim dof4() As Boolean
Dim dof5() As Boolean
Dim dof6() As Boolean
Dim U1() As Double
Dim U2() As Double
Dim U3() As Double
Dim R1() As Double
Dim R2() As Double
Dim R3() As Double
Dim Name1 As String
Dim Name2 As String

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

'add link object by points
ret = SapModel.LinkObj.AddByPoint("3", "", Name1, True)
ret = SapModel.LinkObj.AddByPoint("1", "5", Name2)

'refresh view
ret = SapModel.View.RefreshView

'assign link object deformation loads
ReDim DOF(5)
ReDim d(5)
DOF(0) = True
D(0) = 2
ret = SapModel.LinkObj.SetLoadDeformation("ALL", "DEAD", DOF, d, Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get link element deformation loads
ret = SapModel.LinkElm.GetLoadDeformation("ALL", NumberItems, LinkName, LoadPat,
dof1, dof2, dof3, dof4, dof5, dof6, U1, U2, U3, R1, R2, R3, GroupElm)

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

# GetLoadGravity

## Syntax

SapObject.SapModel.LinkElm.GetLoadGravity

## VB6 Procedure

Function GetLoadGravity(ByVal Name As String, ByRef NumberItems As Long, ByRef
LinkName() As String, ByRef LoadPat() As String, ByRef CSys() As String, ByRef x() As
Double, ByRef y() As Double, ByRef z() As Double, Optional ByVal ItemType As eItemType =
Object) As Long

## Parameters

Name

The name of an existing link object, link element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of gravity loads retrieved for the specified link elements.

LinkName

This is an array that includes the name of the link element associated with each gravity load.

LoadPat

This is an array that includes the name of the coordinate system in which the gravity load
multipliers are specified.

CSys

This is an array that includes the name of the coordinate system associated with each gravity load.

x, y, z


These are arrays of gravity load multipliers in the x, y and z directions of the specified coordinate
system.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the link elements corresponding to
the link object specified by the Name item.

If this item is Element, the load assignments are retrieved for the link element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the link elements corresponding to
all link objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for link elements corresponding to
all selected link objects, and the Name item is ignored.

## Remarks

This function retrieves the gravity load assignments to link elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkElmGravityLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim LinkName() As String
Dim LoadPat() As String
Dim CSys() As String
Dim x() As Double
Dim y() As Double
Dim z() As Double
Dim Name1 As String
Dim Name2 As String

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

'add link object by points
ret = SapModel.LinkObj.AddByPoint("3", "", Name1, True)
ret = SapModel.LinkObj.AddByPoint("1", "5", Name2)

'refresh view
ret = SapModel.View.RefreshView

'assign link object gravity loads
ret = SapModel.LinkObj.SetLoadGravity("ALL", "DEAD", 0, 0, -1, , , Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get link element gravity load
ret = SapModel.LinkElm.GetLoadGravity("ALL", NumberItems, LinkName, LoadPat, CSys,
x, y, z, GroupElm)

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

# GetLoadTargetForce

## Syntax

SapObject.SapModel.LinkElm.GetLoadTargetForce


## VB6 Procedure

Function GetLoadTargetForce(ByVal Name As String, ByRef NumberItems As Long, ByRef
LinkName() As String, ByRef LoadPat() As String, ByRef dof1() As Boolean, ByRef dof2() As
Boolean, ByRef dof3() As Boolean, ByRef dof4() As Boolean, ByRef dof5() As Boolean, ByRef
dof6() As Boolean, ByRef P() As Double, ByRef V2() As Double, ByRef V3() As Double, ByRef
T() As Double, ByRef M2() As Double, ByRef M3() As Double, ByRef T1() As Double, ByRef
T2() As Double, ByRef T3() As Double, ByRef T4() As Double, ByRef T5() As Double, ByRef
T6() As Double, Optional ByVal ItemType As eItemType = Object) As Long

## Parameters

Name

The name of an existing link object, link element or group of objects, depending on the value of
the ItemTypeElm item.

NumberItems

The total number of deformation loads retrieved for the specified link elements.

LinkName

This is an array that includes the name of the link element associated with each target force.

LoadPat

This is an array that includes the name of the load pattern associated with each target force.

dof1, dof2, dof3, dof4, dof5, dof6

These are arrays of boolean values indicating if the considered degree of freedom has a target
force assignment.

```
dof1 = P
dof2 = V2
dof3 = V3
dof4 = T
dof5 = M2
dof6 = M3
```
P, V2, V3, T, M2, M3

These are arrays of target force values. The target forces specified for a given degree of freedom
are applicable only if the corresponding DOF item for that degree of freedom is True.

```
U1 = U1 deformation [L]
U2 = U2 deformation [L]
U3 = U3 deformation [L]
R1 = R1 deformation [rad]
R2 = R2 deformation [rad]
R3 = R3 deformation [rad]
```

### T1, T2, T3, T4, T5, T6

These are arrays of the relative distances along the link elements where the target force values
apply. The relative distances specified for a given degree of freedom are applicable only if the
corresponding dofn item for that degree of freedom is True.

```
T1 = relative location for P target force
T2 = relative location for V2 target force
T3 = relative location for V3 target force
T4 = relative location for T target force
T5 = relative location for M2 target force
T6 = relative location for M3 target force
```
ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the link elements corresponding to
the link object specified by the Name item.

If this item is Element, the load assignments are retrieved for the link element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the link elements corresponding to
all link objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for link elements corresponding to
all selected link objects, and the Name item is ignored.

## Remarks

This function retrieves the target force assignments to link elements.

The function returns zero if the target force assignments are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetLinkElmTargetForce()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim f() As double
Dim RD() As double
Dim NumberItems As Long


Dim LinkName() As String
Dim LoadPat() As String
Dim dof1() As Boolean
Dim dof2() As Boolean
Dim dof3() As Boolean
Dim dof4() As Boolean
Dim dof5() As Boolean
Dim dof6() As Boolean
Dim P() As Double
Dim V2() As Double
Dim V3() As Double
Dim T() As Double
Dim M2() As Double
Dim M3() As Double
Dim T1() As Double
Dim T2() As Double
Dim T3() As Double
Dim T4() As Double
Dim T5() As Double
Dim T6() As Double
Dim Name1 As String
Dim Name2 As String

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

'add link object by points
ret = SapModel.LinkObj.AddByPoint("3", "", Name1, True)
ret = SapModel.LinkObj.AddByPoint("1", "5", Name2)

'refresh view
ret = SapModel.View.RefreshView

'assign link object target force
ReDim DOF(5)
ReDim f(5)
ReDim RD(5)
DOF(0) = True
f(0) = 50
RD(0) = 0.4
ret = SapModel.LinkObj.SetLoadTargetForce("ALL", "DEAD", DOF, f, RD, Group)


'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get link element target force
ret = SapModel.LinkElm.GetLoadTargetForce("ALL", NumberItems, LinkName, LoadPat,
dof1, dof2, dof3, dof4, dof5, dof6, P, V2, V3, T, M2, M3, T1, T2, T3, T4, T5, T6, GroupElm)

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

# GetLocalAxes

## Syntax

SapObject.SapModel.LinkElm.GetLocalAxes

## VB6 Procedure

Function GetLocalAxes(ByVal Name As String, ByRef Ang As Double) As Long

## Parameters

Name

The name of an existing link element.

Ang

This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis, from the
default orientation. The rotation for a positive angle appears counter clockwise when the local +1
axis is pointing toward you. [deg]

## Remarks

This function retrieves the local axis angle assignment for link elements.


The function returns zero if the assignment is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetLinkElmLocalAxisAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim Ang As Double

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

'add link object by points
ret = SapModel.LinkObj.AddByPoint("1", "5", Name)

'refresh view
ret = SapModel.View.RefreshView

'assign link object local axis angle
ret = SapModel.LinkObj.SetLocalAxes(Name, 30)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get link element local axis angle
ret = SapModel.LinkElm.GetLocalAxes(Name, Ang)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.00.

## See Also

# GetNameList

## Syntax

SapObject.SapModel.LinkElm.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of link element names retrieved by the program.

MyName

This is a one-dimensional array of link element names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames – 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined link elements.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetLinkElementNames()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name1 As String
Dim Name2 As String
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

'add link object by points
ret = SapModel.LinkObj.AddByPoint("3", "", Name1, True)
ret = SapModel.LinkObj.AddByPoint("1", "5", Name2)

'refresh view
ret = SapModel.View.RefreshView

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get link element names
ret = SapModel.LinkElm.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetObj

## Syntax

Sap2000.LinkElm.GetObj


## VB6 Procedure

Function GetObj(ByVal Name As String, ByRef Obj As String, ByRef ObjType As Long) As
Long

## Parameters

Name

The name of an existing link element.

Obj

The name of the object associated with the specified link element. The type of object or item is
determined from the ObjType variable.

ObjType

A number indicating the type of object that is associated with the point element.

```
2
Obj is a line object that has a line spring assignment. The springs are modeled using
link elements.
```
```
3
Obj is a area object that has an area spring assignment. The springs are modeled
using link elements.
```
```
6
Obj is a solid object that has a surface spring assignment. The springs are modeled
using link elements.
```
```
9
Obj is a point object that has a panel zone assignment. The specified link element is
internally added by the program at the point object (panel zone) location to model
the panel zone.
```
```
101
Obj is a point element
```
```
102
Obj is a line element
```
```
103
Obj is an area element
```
```
104
Obj is a plane element
```
```
106
Obj is a solid element
```

## Remarks

This function retrieves the object associated with a specified link element.

The function returns zero if the object is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetObjForLinkElm()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Obj As String
Dim ObjType As Long
Dim Vec() As Double

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

'assign springs to frame
ReDim Vec(2)
ret = SapModel.FrameObj.SetSpring("8", 1, 1, 1, "", 1, 2, 0, Vec, 0, False, "Local")

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get object for link element
ret = SapModel.LinkElm.GetObj("~1", Obj, ObjType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Added point, line, area, and solid element as ObjType options in v22.1.0.

Initial release in version 11.00.

## See Also

# GetPoints

## Syntax

SapObject.SapModel.LinkElm.GetPoints

## VB6 Procedure

Function GetPoints(ByVal Name As String, ByRef Point1 As String, ByRef Point2 As String) As
Long

## Parameters

Name

The name of a defined link element.

Point1

The name of the point element at the I-End of the specified link element.

Point2

The name of the point element at the J-End of the specified link element.

## Remarks

This function retrieves the names of the point elements at each end of a specified link element.
The points at each end have the same name if the link element is a one-joint element.

The function returns zero if the point names are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkElmPoints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim Point1 As String


Dim Point2 As String

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

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add link object by points
ret = SapModel.LinkObj.AddByPoint("1", "5", Name)

'refresh view
ret = SapModel.View.RefreshView

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get names of points
ret = SapModel.LinkElm.GetPoints(Name, Point1, Point2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetProperty

## Syntax

SapObject.SapModel.LinkElm.GetProperty


## VB6 Procedure

Function GetProperty(ByVal Name As String, ByRef PropName As String) As Long

## Parameters

Name

The name of an existing link element.

PropName

The name of the link property assigned to the link element.

## Remarks

This function retrieves the property assignment to a link element.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

The sVarTotalLength and sVarRelStartLoc items apply only when the Var item is True.

## VBA Example

Sub GetLinkElementProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropName As String
Dim Name As String

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

'add link object by points
ret = SapModel.LinkObj.AddByPoint("1", "5", Name)


'refresh view
ret = SapModel.View.RefreshView

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get property for link element
ret = SapModel.LinkElm.GetProperty(Name, PropName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetPropertyFD

## Syntax

SapObject.SapModel.LinkElm.GetPropertyFD

## VB6 Procedure

Function GetPropertyFD(ByVal Name As String, ByRef PropName As String) As Long

## Parameters

Name

The name of an existing link element.

PropName

The name of the frequency dependent link property assigned to the link element.

## Remarks

This function retrieves the frequency dependent property assignment to a link element. If no
frequency dependent property is assigned to the link, the PropName is returned as None.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetLinkElementFDProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropName As String
Dim Name As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 6-012.sdb")

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get frequency dependent property for link element
ret = SapModel.LinkElm.GetPropertyFD("1", PropName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetTransformationMatrix

## Syntax

Sap2000.LinkElm.GetTransformationMatrix


## VB6 Procedure

Function GetTransformationMatrix(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing link element.

Value

Value is an array of nine direction cosines that define the transformation matrix.

The following matrix equation shows how the transformation matrix is used to convert items from
the link element local coordinate system to the global coordinate system.

In the equation, c0 through c8 are the nine values from the transformation array, (Local1, Local2,
Local3) are an item (such as a load) in the element local coordinate system, and (GlobalX,
GlobalY, GlobalZ) are the same item in the global coordinate system.

## Remarks

The function returns zero if the transformation matrix is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetLinkElementMatrix()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value() As Double
Dim Name As String

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

'add link object by points
ret = SapModel.LinkObj.AddByPoint("1", "5", Name)

'refresh view
ret = SapModel.View.RefreshView

'assign link local axis angle
ret = SapModel.LinkObj.SetLocalAxes(Name, 30)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get link element transformation matrix
ReDim Value(8)
ret = SapModel.LinkElm.GetTransformationMatrix(Name, Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Count

## Syntax

Sap2000.PlaneElm.Count

## VB6 Procedure

Function Count() As Long

## Parameters


None

## Remarks

This function returns the total number of plane elements in the analysis model.

## VBA Example

Sub CountPlaneElements()
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign auto mesh options
ret = SapModel.AreaObj.SetAutoMesh("ALL", 1, 2, 2, , , , , , , , , , , , , , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'return number of plane elements
Count = SapModel.PlaneElm.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# GetLoadGravity

## Syntax

SapObject.SapModel.PlaneElm.GetLoadGravity

## VB6 Procedure

Function GetLoadGravity(ByVal Name As String, ByRef NumberItems As Long, ByRef
PlaneName() As String, ByRef LoadPat() As String, ByRef CSys() As String, ByRef x() As
Double, ByRef y() As Double, ByRef z() As Double, Optional ByVal ItemTypeElm As
eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing plane element or group, depending on the value of the ItemType item.

NumberItems

The total number of gravity loads retrieved for the specified plane elements.

PlaneName

This is an array that includes the name of the plane element associated with each gravity load.

LoadPat

This is an array that includes the name of the coordinate system in which the gravity load
multipliers are specified.

CSys

This is an array that includes the name of the coordinate system associated with each gravity load.

x, y, z

These are arrays of gravity load multipliers in the x, y and z directions of the specified coordinate
system.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```

If this item is ObjectElm, the load assignments are retrieved for the plane elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the plane element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the plane elements corresponding
to all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for plane elements corresponding
to all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the gravity load assignments to plane elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetPlaneElementGravityLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim PlaneName() As String
Dim LoadPat() As String
Dim CSys() As String
Dim x() As Double
Dim y() As Double
Dim z() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign auto mesh options


ret = SapModel.AreaObj.SetAutoMesh("ALL", 1, 3, 3, , , , , , , , , , , , , , , Group)

'assign area object gravity loads
ret = SapModel.AreaObj.SetLoadGravity("ALL", "Membrane", 0, 0, -1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element gravity load
ret = SapModel.PlaneElm.GetLoadGravity("3-1", NumberItems, PlaneName, LoadPat, CSys,
x, y, z)

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

# GetLoadPorePressure

## Syntax

SapObject.SapModel.PlaneElm.GetLoadPorePressure

## VB6 Procedure

Function GetLoadPorePressure(ByVal Name As String, ByRef NumberItems As Long, ByRef
PlaneName() As String, ByRef LoadPat() As String, ByRef Value() As Double, ByRef
PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing plane element or group, depending on the value of the ItemType item.

NumberItems

The total number of pore pressure loads retrieved for the specified plane elements.


PlaneName

This is an array that includes the name of the plane element associated with each pore pressure
load.

LoadPat

This is an array that includes the name of the load pattern associated with each pore pressure load.

Value

This is an array that includes the pore pressure load value. [F/L^2 ]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the pore pressure load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the plane elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the plane element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the plane elements corresponding
to all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for plane elements corresponding
to all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the pore pressure load assignments to plane elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetPlaneElementPorePressureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim NumberItems As Long
Dim PlaneName() As String
Dim LoadPat() As String
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign area object pore pressure load
ret = SapModel.AreaObj.SetLoadPorePressure("ALL", "Membrane", .1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element pore pressure load
ret = SapModel.PlaneElm.GetLoadPorePressure("ALL", NumberItems, PlaneName, LoadPat,
Value, PatternName, GroupElm)

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

# GetLoadRotate

## Syntax


SapObject.SapModel.PlaneElm.GetLoadRotate

## VB6 Procedure

Function GetLoadRotate(ByVal Name As String, ByRef NumberItems As Long, ByRef
PlaneName() As String, ByRef LoadPat() As String, ByRef Value() As Double, ByRef
PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing plane element or group, depending on the value of the ItemType item.

NumberItems

The total number of rotate loads retrieved for the specified plane elements.

PlaneName

This is an array that includes the name of the plane element associated with each rotate load.

LoadPat

This is an array that includes the name of the load pattern associated with each rotate load.

Value

This is an array that includes the rotate load value. [F/L^2 ]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the rotate load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the plane elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the plane element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the plane elements corresponding
to all area objects included in the group specified by the Name item.


If this item is SelectionElm, the load assignments are retrieved for plane elements corresponding
to all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the rotate load assignments to plane elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetPlaneElementRotateLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim PlaneName() As String
Dim LoadPat() As String
Dim Value() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 4-001-incomp.sdb")

'assign area object rotate load
ret = SapModel.AreaObj.SetLoadRotate("ALL", "FTG", 30, , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element rotate load
ret = SapModel.PlaneElm.GetLoadRotate("ALL", NumberItems, PlaneName, LoadPat,
Value, GroupElm)

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

# GetLoadStrain

## Syntax

SapObject.SapModel.PlaneElm.GetLoadStrain

## VB6 Procedure

Function GetLoadStrain(ByVal Name As String, ByRef NumberItems As Long, ByRef
PlaneName() As String, ByRef LoadPat() As String, ByRef Component() As Long, ByRef Value
() As Double, ByRef PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm
= Element) As Long

## Parameters

Name

The name of an existing plane element or group, depending on the value of the ItemType item.

NumberItems

The total number of strain loads retrieved for the specified plane elements.

PlaneName

This is an array that includes the name of the plane element associated with each strain load.

LoadPat

This is an array that includes the name of the load pattern associated with each strain load.

Component

This is an array that includes 1, 2, 3, 4, 5 or 6, indicating the component associated with each
strain load.

```
1 = Strain11
2 = Strain22
```

```
3 = Strain12
4 = Strain13
5 = Strain23
6 = Strain33
```
Value

This is an array that includes the strain value. [L/L]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the strain load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the plane elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the plane element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the plane elements corresponding
to all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for plane elements corresponding
to all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the strain load assignments to plane elements.

The function returns zero if the strain load assignments are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetPlaneElementStrainLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim PlaneName() As String
Dim LoadPat() As String
Dim Component() As Long


Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign area object strain load
ret = SapModel.AreaObj.SetLoadStrain("ALL", "Membrane", 1, 0.001, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element strain load
ret = SapModel.PlaneElm.GetLoadStrain("3", NumberItems, PlaneName, LoadPat,
Component, Value, PatternName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Added strain in the 33 direction for version 24.1.0.

## See Also

# GetLoadSurfacePressure

## Syntax

SapObject.SapModel.PlaneElm.GetLoadSurfacePressure


## VB6 Procedure

Function GetLoadSurfacePressure(ByVal Name As String, ByRef NumberItems As Long, ByRef
PlaneName() As String, ByRef LoadPat() As String, ByRef Face() As Long, ByRef Value() As
Double, ByRef PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm =
Element) As Long

## Parameters

Name

The name of an existing plane element or group, depending on the value of the ItemType item.

NumberItems

The total number of surface pressure loads retrieved for the specified plane elements.

PlaneName

This is an array that includes the name of the plane element associated with each surface pressure
load.

LoadPat

This is an array that includes the name of the load pattern associated with each surface pressure
load.

Face

This is an array that includes -1, -2 or a nonzero, positive integer, indicating the area element face
to which the specified load assignment applies.

```
-1 = Bottom face
-2 = Top face
>0 = Edge face
```
Note that edge face n is from plane element point n to plane element point n + 1. For example,
edge face 2 is from plane element point 2 to plane element point 3.

Value

This is an array that includes the surface pressure load value. [F/L^2 ]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the surface pressure
load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
```

```
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the plane elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the plane element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the plane elements corresponding
to all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for plane elements corresponding
to all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the surface pressure load assignments to plane elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetPlaneElementSurfacePressureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim PlaneName() As String
Dim LoadPat() As String
Dim Face() As Long
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")


'assign area object surface pressure load
ret = SapModel.AreaObj.SetLoadSurfacePressure("ALL", "Membrane", -1, .1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element surface pressure load
ret = SapModel.PlaneElm.GetLoadSurfacePressure("ALL", NumberItems, PlaneName,
LoadPat, Face, Value, PatternName, GroupElm)

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

# GetLoadTemperature

## Syntax

SapObject.SapModel.PlaneElm.GetLoadTemperature

## VB6 Procedure

Function GetLoadTemperature(ByVal Name As String, ByRef NumberItems As Long, ByRef
PlaneName() As String, ByRef LoadPat() As String, ByRef MyType() As Long, ByRef Value()
As Double, ByRef PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm =
Element) As Long

## Parameters

Name

The name of an existing plane element or group, depending on the value of the ItemType item.

NumberItems

The total number of temperature loads retrieved for the specified plane elements.


PlaneName

This is an array that includes the name of the plane element associated with each temperature load.

LoadPat

This is an array that includes the name of the load pattern associated with each temperature load.

MyType

This is an array that includes either 1 or 3, indicating the type of temperature load.

```
1 = Temperature
3 = Temperature gradient along local 3 axis
```
Value

This is an array that includes the temperature load value. [T] for MyType= 1 and [T/L] for
MyType= 3

PatternName

This is an array that includes the joint pattern name, if any, used to specify the temperature load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the plane elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the plane element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the plane elements corresponding
to all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for plane elements corresponding
to all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the temperature load assignments to plane elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetPlaneElementTemperatureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim PlaneName() As String
Dim LoadPat() As String
Dim MyType() As Long
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign area object temperature load
ret = SapModel.AreaObj.SetLoadTemperature("All", "Membrane", 1, 50, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element temperature load
ret = SapModel.PlaneElm.GetLoadTemperature("ALL", NumberItems, PlaneName, LoadPat,
MyType, Value, PatternName, GroupElm)

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

# GetLoadUniform

## Syntax

SapObject.SapModel.PlaneElm.GetLoadUniform

## VB6 Procedure

Function GetLoadUniform(ByVal Name As String, ByRef NumberItems As Long, ByRef
PlaneName() As String, ByRef LoadPat() As String, ByRef CSys() As String, ByRef Dir() As
Long, ByRef Value() As Double, Optional ByVal ItemTypeElm As eItemTypeElm = Element) As
Long

## Parameters

Name

The name of an existing plane element or group, depending on the value of the ItemType item.

NumberItems

The total number of uniform loads retrieved for the specified plane elements.

PlaneName

This is an array that includes the name of the plane element associated with each uniform load.

LoadPat

This is an array that includes the name of the coordinate system in which the uniform load is
specified.

CSys

This is an array that includes the name of the coordinate system associated with each uniform
load.

Dir

This is an integer between 1 and 11, indicating the direction of the load.

```
1 = Local 1 axis (applies only when CSys is Local)
2 = Local 2 axis (applies only when CSys is Local)
3 = Local 3 axis (applies only when CSys is Local)
4 = X direction (does not apply when CSys is Local)
5 = Y direction (does not apply when CSys is Local)
6 = Z direction (does not apply when CSys is Local)
7 = Projected X direction (does not apply when CSys is Local)
8 = Projected Y direction (does not apply when CSys is Local)
```

```
9 = Projected Z direction (does not apply when CSys is Local)
10 = Gravity direction (applies only when CSys is Global)
11 = Projected Gravity direction (applies only when CSys is Global)
```
The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.

Value

The uniform load value. [F/L^2 ]

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the plane elements corresponding
to the area object specified by the Name item.

If this item is Element, the load assignments are retrieved for the plane element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the plane elements corresponding
to all area objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for plane elements corresponding
to all selected area objects, and the Name item is ignored.

## Remarks

This function retrieves the uniform load assignments to plane elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetPlaneElementUniformLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim PlaneName() As String
Dim LoadPat() As String
Dim CSys() As String
Dim Dir() As Long
Dim Value() As Double


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign area object uniform loads
ret = SapModel.AreaObj.SetLoadUniform("ALL", "Membrane", -0.01, 2, False, "Local",
Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element uniform load
ret = SapModel.PlaneElm.GetLoadUniform("3", NumberItems, PlaneName, LoadPat, CSys,
Dir, Value)

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

# GetLocalAxes

## Syntax

SapObject.SapModel.PlaneElm.GetLocalAxes


## VB6 Procedure

Function GetLocalAxes(ByVal Name As String, ByRef Ang As Double) As Long

## Parameters

Name

The name of an existing plane element.

Ang

This is the angle that the local 1 and 2 axes are rotated about the positive local 3 axis from the
default orientation. The rotation for a positive angle appears counter clockwise when the local +3
axis is pointing toward you. [deg]

## Remarks

This function retrieves the local axis angle assignment for plane elements.

The function returns zero if the assignment is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetPlaneElementLocalAxisAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Ang As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign area object local axis angle
ret = SapModel.AreaObj.SetLocalAxes("3", 30)

'create analysis model


ret = SapModel.Analyze.CreateAnalysisModel

'get plane element local axis angle
ret = SapModel.PlaneElm.GetLocalAxes("3", Ang)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetMatTemp

## Syntax

SapObject.SapModel.PlaneElm.GetMatTemp

## VB6 Procedure

Function GetMatTemp(ByVal Name As String, ByRef Temp As Double, ByRef PatternName As
String) As Long

## Parameters

Name

The name of an existing plane element.

Temp

This is the material temperature value assigned to the plane element. [T]

PatternName

This is blank or the name of a defined joint pattern. If it is blank, the material temperature for the
plane element is uniform over the element at the value specified by Temp.

If PatternName is the name of a defined joint pattern, the material temperature for the plane
element may vary. The material temperature at each corner point around the plane element
perimeter is equal to the specified temperature multiplied by the pattern value at the associated
point element. The material temperature at other points in the plane element is calculated by
interpolation from the corner points.


## Remarks

This function retrieves the material temperature assignments to plane elements.

The function returns zero if the material temperature assignments are successfully retrieved;
otherwise it returns a nonzero value.

## VBA Example

Sub GetPlaneElementMatTemp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Temp As Double
Dim PatternName As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign material temperature
ret = SapModel.AreaObj.SetMatTemp("ALL", 50, , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get material temperature for plane element
ret = SapModel.PlaneElm.GetMatTemp("3", Temp, PatternName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# GetNameList

## Syntax

SapObject.SapModel.PlaneElm.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of plane element names retrieved by the program.

MyName

This is a one-dimensional array of plane element names. The MyName array is created as a
dynamic, zero-based, array by the API user:

Dim MyName() as String

The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined plane elements.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetPlaneElementNames()
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element names
ret = SapModel.PlaneElm.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetObj

## Syntax

Sap2000.PlaneElm.GetObj

## VB6 Procedure

Function GetObj(ByVal Name As String, ByRef Obj As String) As Long

## Parameters

Name

The name of an existing plane element.

Obj

The name of the area object from which the plane element was created.


## Remarks

This function retrieves the name of the area object from which an plane element was created.

The function returns zero if the information is successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetObjForPlaneElm()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Obj As String
Dim ObjType As Long
Dim RDI As Double
Dim RDJ As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign auto mesh options
ret = SapModel.AreaObj.SetAutoMesh("ALL", 1, 3, 3, , , , , , , , , , , , , , , Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get object information for an plane element
ret = SapModel.PlaneElm.GetObj("3-2", Obj)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# GetPoints

## Syntax

SapObject.SapModel.PlaneElm.GetPoints

## VB6 Procedure

Function GetPoints(ByVal Name As String, ByRef NumberPoints As Long, ByRef Point() As
String) As Long

## Parameters

Name

The name of an plane element.

NumberPoints

The number of point elements that define the plane element.

Point

This is an array containing the names of the point elements that define the plane element. The
point names are in order around the plane element.

## Remarks

This function retrieves the names of the point elements that define an plane element.

The function returns zero if the point element names are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetPlaneElmPoints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberPoints As Long
Dim Point() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign auto mesh options
ret = SapModel.AreaObj.SetAutoMesh("ALL", 1, 3, 3, , , , , , , , , , , , , , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get names of points
ret = SapModel.PlaneElm.GetPoints("3-2", NumberPoints, Point)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetProperty

## Syntax

SapObject.SapModel.PlaneElm.GetProperty

## VB6 Procedure

Function GetProperty(ByVal Name As String, ByRef PropName As String) As Long

## Parameters

Name

The name of a defined plane element.


PropName

The name of the area property assigned to the plane element. This item is None if there is no area
property assigned to the plane element.

## Remarks

This function retrieves the area property assigned to an plane element.

The function returns zero if the property is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetPlaneElementProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropName As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get area property for plane element
ret = SapModel.PlaneElm.GetProperty("1", PropName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# GetTransformationMatrix

## Syntax

Sap2000.PlaneElm.GetTransformationMatrix

## VB6 Procedure

Function GetTransformationMatrix(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing plane element.

Value

Value is an array of nine direction cosines that define the transformation matrix.

The following matrix equation shows how the transformation matrix is used to convert items from
the plane element local coordinate system to the global coordinate system.

In the equation, c0 through c8 are the nine values from the transformation array, (Local1, Local2,
Local3) are an item (such as a load) in the element local coordinate system, and (GlobalX,
GlobalY, GlobalZ) are the same item in the global coordinate system.

## Remarks

The function returns zero if the transformation matrix is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetPlaneElementMatrix()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim Value() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 3-001-incomp.sdb")

'assign area object local axis angle
ret = SapModel.AreaObj.SetLocalAxes("3", 30)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get plane element transformation matrix
redim Value(8)
ret = SapModel.PlaneElm.GetTransformationMatrix("3", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Count

## Syntax

SapObject.SapModel.PointElm.Count

## VB6 Procedure

Function Count() As Long


## Parameters

None

## Remarks

This function returns the total number of point elements in the analysis model.

## VBA Example

Sub CountPointElements()
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

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'return number of point elements
Count = SapModel.PointElm.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# CountConstraint

## Syntax

SapObject.SapModel.PointElm.CountConstraint

## VB6 Procedure

Function CountConstraint(ByRef Count As Long, Optional ByVal Name As String = "") As Long

## Parameters

Count

The number of counted constraints.

Name

This optional item is the name of an existing point element.

## Remarks

If the Name item is provided, the Count item returns the total number of constraint assignments
made to the specified point element. If the Name item is not specified or is specified as an empty
string, the Count item returns the total number of constraint assignments to all point elements in
the model. If the Name item is specified but it is not recognized by the program as a valid point
element, an error is returned.

This function returns zero if the count is successfully completed, otherwise it returns a nonzero
value.

## VBA Example

Sub CountConstraintElmAssignments()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
Dim Count as Long

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

'add constraint definition
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1")

'make constraint assignment
ret = SapModel.PointObj.SetConstraint("3", "Diaph1")

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get number of constraint assignments to point elements
ret = SapModel.PointElm.CountConstraint(Count)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetConstraint

# CountLoadDispl

## Syntax

SapObject.SapModel.PointElm.CountLoadDispl

## VB6 Procedure

Function CountLoadDispl(ByRef Count As Long, Optional ByVal Name As String = "", Optional
ByVal LoadPat As String = "") As Long

## Parameters


Count

The number of counted ground displacement loads.

Name

This optional item is the name of an existing point element.

LoadPat

This optional item is the name of an existing load pattern.

## Remarks

If neither the Name item nor the LoadPat item is provided, the Count item returns the total number
of ground displacement load assignments to point elements in the model.

If the Name item is provided but not the LoadPat item, the Count item returns the total number of
ground displacement load assignments made for the specified point element.

If the Name item is not provided but the LoadPat item is specified, the Count item returns the total
number of ground displacement load assignments made to all point elements for the specified load
pattern.

If both the Name item and the LoadPat item are provided, the Count item returns the total number
of ground displacement load assignments made to the specified point element for the specified
load pattern.

If the Name item or the LoadPat item is provided but is not recognized by the program as valid, an
error is returned.

This function returns zero if the count is successfully completed, otherwise it returns a nonzero
value.

## VBA Example

Sub CountGroundDisplacementElmLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value() As Double
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

'add ground displacement load
Redim Value(5)
Value(0) = 10
ret = SapModel.PointObj.SetLoadDispl("1", "DEAD", Value)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get number of ground displacement loads for point elements
ret = SapModel.PointElm.CountLoadDispl(Count)

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

GetLoadDispl

# CountLoadForce

## Syntax

SapObject.SapModel.PointElm.CountLoadForce

## VB6 Procedure

Function CountLoadForce(ByRef Count As Long, Optional ByVal Name As String = "", Optional
ByVal LoadPat As String = "") As Long

## Parameters

Count


The number of counted point loads.

Name

This optional item is the name of an existing point element.

LoadPat

This optional item is the name of an existing load pattern.

## Remarks

If neither the Name item nor the LoadPat item is provided, the Count item returns the total number
of point load assignments to point elements in the model.

If the Name item is provided but not the LoadPat item, the Count item returns the total number of
point load assignments made for the specified point element.

If the Name item is not provided but the LoadPat item is specified, the Count item returns the total
number of point load assignments made to all point elements for the specified load pattern.

If both the Name item and the LoadPat item are provided, the Count item returns the total number
of point load assignments made to the specified point element for the specified load pattern.

If the Name item or the LoadPat item is provided but is not recognized by the program as valid, an
error is returned.

This function returns zero if the count is successfully completed, otherwise it returns a nonzero
value.

## VBA Example

Sub CountPointElmLoads()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value() As Double
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

'add point load
Redim Value(5)
Value(0) = 10
ret = SapModel.PointObj.SetLoadForce("3", "DEAD", Value)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get number of point loads assigned to point elements
ret = SapModel.PointElm.CountLoadForce(Count)

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

GetLoadForce

# CountRestraint

## Syntax

SapObject.SapModel.PointElm.CountRestraint

## VB6 Procedure

Function CountRestraint() As Long

## Parameters

None

## Remarks

This function returns the total number of point elements in the model with restraint assignments.


## VBA Example

Sub CountRestrainedPointElements()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
Dim Count as Long

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

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get number of restrained point elements
Count = SapModel.PointElm.CountRestraint

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetRestraint

# CountSpring

## Syntax

SapObject.SapModel.PointElm.CountSpring


## VB6 Procedure

Function CountSpring() As Long

## Parameters

None

## Remarks

This function returns the total number of point elements in the model with spring assignments.

## VBA Example

Sub CountPointElementsWithSprings()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
Dim i as Long
Dim k() as Double
Dim Count as Long

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

'add joint spring assignment
ReDim k(5)
For i = 0 to 5
k(i) = i + 1
Next i
ret = SapModel.PointObj.SetSpring("3", k)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get number of point elements with springs
Count = SapModel.PointElm.CountSpring


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetSpring

GetSpringCoupled

# GetConnectivity

## Syntax

SapObject.SapModel.PointElm.GetConnectivity

## VB6 Procedure

Function GetConnectivity(ByVal Name As String, ByRef NumberItems As Long, ByRef
ObjectType() As Long, ByRef ObjectName() As String, ByRef PointNumber() As Long) As Long

## Parameters

Name

The name of an existing point element.

NumberItems

This is the total number of elements connected to the specified point element.

ObjectType

This is an array that includes the element type of each element connected to the specified point
element.

```
2 = Frame element
3 = Cable element
4 = Tendon element
5 = Area element
6 = Solid element
7 = Link element
```

ObjectName

This is an array that includes the element name of each element connected to the specified point
element.

PointNumber

This is an array that includes the point number within the considered element that corresponds to
the specified point element.

## Remarks

This function returns a list of elements connected to a specified point element.

The function returns zero if the list is successfully filled; otherwise it returns nonzero.

## VBA Example

Sub GetPointElementConnectivity()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems as Long
Dim ObjectType() As Long
Dim ObjectName() As String
Dim PointNumber() As Long

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

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get elements connected to point element 11
ret = SapModel.PointElm.GetConnectivity("11", NumberItems, ObjectType, ObjectName,
PointNumber)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

# GetConstraint

## Syntax

SapObject.SapModel.PointElm.GetConstraint

## VB6 Procedure

Function GetConstraint(ByVal Name As String, ByRef NumberItems As Long, ByRef PointName
() As String, ByRef ConstraintName() As String, Optional ByVal ItemTypeElm As
eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects, depending on the value
of the ItemTypeElm item.

NumberItems

This is the total number of constraint assignments returned.

PointName

This is an array that includes the name of the point element to which the specified constraint
assignment applies.

ConstraintName

This is an array that includes the name of the constraint that is assigned to the point element
specified by the PointName item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:


```
ObjectElm = 0
```
```
Element = 1
```
```
GroupElm = 2
```
```
SelectionElm = 3
```
If this item is ObjectElm, the constraint assignments are retrieved for the point element
corresponding to the point object specified by the Name item.

If this item is Element, the constraint assignments are retrieved for the point element specified by
the Name item.

If this item is GroupElm, the constraint assignments are retrieved for all point elements directly or
indirectly specified in the group specified by the Name item.

If this item is SelectionElm, the constraint assignments are retrieved for all point elements directly
or indirectly selected, and the Name item is ignored.

See Item Type for Elements for more information.

## Remarks

This function returns a list of constraint assignments made to one or more specified point
elements.

The function returns zero if the constraint name list is successfully filled, otherwise it returns
nonzero.

The PointName and ConstraintName items are returned in one-dimensional arrays. Each array is
created as a dynamic array by the API user. In VBA a dynamic string array is defined by:

Dim PointName() as String

The arrays are dimensioned to (NumberItems – 1) inside the Sap2000 program, filled with values,
and returned to the API user.

The arrays are zero-based. Thus the first item is at array index 0, and the last item is at array index
(NumberItems - 1).

## VBA Example

Sub GetConstraintElmAssignments()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems as Long
Dim PointName() As String


Dim ConstraintName() As String
Dim i As Long

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

'define a new constraint
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1")

'define new constraint assignments
For i = 4 To 16 Step 4
ret = SapModel.PointObj.SetConstraint(Format(i), "Diaph1")
Next i

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get constraint assignments to point elements
ret = SapModel.PointElm.GetConstraint("ALL", NumberItems, PointName, ConstraintName,
GroupElm)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetCoordCartesian

## Syntax

SapObject.SapModel.PointElm.GetCoordCartesian


## VB6 Procedure

Function GetCoordCartesian(ByVal Name As String, ByRef x As Double, ByRef y As Double,
ByRef z As Double, Optional ByVal CSys As String = "Global") As Long

## Parameters

Name

The name of an existing point element.

x

The X-coordinate of the specified point element in the specified coordinate system. [L]

y

The Y-coordinate of the specified point element in the specified coordinate system. [L]

z

The Z-coordinate of the specified point element in the specified coordinate system. [L]

CSys

The name of the coordinate system in which the joint coordinates are returned.

## Remarks

The function returns zero if the coordinates are successfully returned; otherwise it returns nonzero.
If successful, the function returns the x, y and z coordinates of the specified point element in the
Present Units. The coordinates are reported in the coordinate system specified by CSys.

## VBA Example

Sub GetPointElmCoordCartesian()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim x As Double, y As Double, z As Double
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get cartesian point element coordinates
ret = SapModel.PointElm.GetCoordCartesian("5", x, y, z)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetCoordCylindrical

GetCoordSpherical

# GetCoordCylindrical

## Syntax

SapObject.SapModel.PointElm.GetCoordCylindrical

## VB6 Procedure

Function GetCoordCylindrical(ByVal Name As String, ByRef r As Double, ByRef Theta As
Double, ByRef z As Double, Optional ByVal CSys As String = "Global") As Long

## Parameters

Name

The name of an existing point element.

r

The radius for the point element in the specified coordinate system. [L]


Theta

The angle for the specified point element in the specified coordinate system. The angle is
measured in the XY plane from the positive X axis. When looking in the XY plane with the
positive Z axis pointing toward you, a positive Theta angle is counter clockwise. [deg]

z

The Z-coordinate of the specified point element in the specified coordinate system. [L]

CSys

The name of the coordinate system in which the joint coordinates are returned.

## Remarks

The function returns zero if the coordinates are successfully returned; otherwise it returns nonzero.
If successful, the function returns the r, Theta and z coordinates of the specified point element in
the Present Units. The coordinates are reported in the coordinate system specified by CSys.

## VBA Example

Sub GetPointElmCoordCylindrical()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim r As Double, Theta As Double, z As Double
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get cylindrical point element coordinates
ret = SapModel.PointElm.GetCoordCylindrical("5", r, Theta, z)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetCoordCartesian

GetCoordSpherical

# GetCoordSpherical

## Syntax

SapObject.SapModel.PointElm.GetCoordSpherical

## VB6 Procedure

Function GetCoordSpherical(ByVal Name As String, ByRef r As Double, ByRef a As Double,
ByRef b As Double, Optional ByVal CSys As String = "Global") As Long

## Parameters

Name

The name of an existing point element.

r

The radius for the point element in the specified coordinate system. [L]

a

The plan angle for the point element in the specified coordinate system. This angle is measured in
the XY plane from the positive global X axis. When looking in the XY plane with the positive Z
axis pointing toward you, a positive a angle is counter clockwise. [deg]

b

The elevation angle for the point element in the specified coordinate system. This angle is
measured in an X'Z plane that is perpendicular to the XY plane with the positive X' axis oriented
at angle a from the positive global X axis. Angle b is measured from the positive global Z axis.
When looking in the X’Z plane with the positive Y' axis pointing toward you, a positive b angle is
counter clockwise. [deg]


CSys

The name of the coordinate system in which the joint coordinates are returned.

## Remarks

The function returns zero if the coordinates are successfully returned; otherwise it returns nonzero.
If successful, the function returns the r, a and b coordinates of the specified point element in the
Present Units. The coordinates are reported in the coordinate system specified by CSys.

## VBA Example

Sub GetPointElmCoordSpherical()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim r As Double, a As Double, b As Double
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get spherical point element coordinates
ret = SapModel.PointElm.GetCoordSpherical("5", r, a, b)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

GetCoordCartesian

GetCoordCylindrical

# GetLoadDispl

## Syntax

SapObject.SapModel.PointElm.GetLoadDispl

## VB6 Procedure

Function GetLoadDispl(ByVal Name As String, ByRef NumberItems As Long, ByRef PointName
() As String, ByRef LoadPat() As String, ByRef LCStep() As Long, ByRef CSys() As String,
ByRef U1() As Double, ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double,
ByRef R2() As Double, ByRef R3() As Double, Optional ByVal ItemTypeElm As eItemTypeElm
= Element) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects, depending on the value
of the ItemTypeElm item.

NumberItems

This is the total number of joint ground displacement assignments returned.

PointName

This is an array that includes the name of the point element to which the specified ground
displacement assignment applies.

LoadPat

This is an array that includes the name of the load pattern for the ground displacement load.

LCStep

This is an array that includes the load pattern step for the ground displacement load. In most cases,
this item does not apply and will be returned as 0.

CSys

This is an array that includes the name of the coordinate system for the ground displacement load.
This is either Local or the name of a defined coordinate system.

U1


This is an array that includes the assigned translational ground displacement in the local 1-axis or
coordinate system X-axis direction, depending on the specified CSys. [L]

U2

This is an array that includes the assigned translational ground displacement in the local 2-axis or
coordinate system Y-axis direction, depending on the specified CSys. [L]

U3

This is an array that includes the assigned translational ground displacement in the local 3-axis or
coordinate system Z-axis direction, depending on the specified CSys. [L]

R1

This is an array that includes the assigned rotational ground displacement about the local 1-axis or
coordinate system X-axis, depending on the specified CSys. [rad]

R2

This is an array that includes the assigned rotational ground displacement about the local 2-axis or
coordinate system Y-axis, depending on the specified CSys. [rad]

R3

This is an array that includes the assigned rotational ground displacement about the local 3-axis or
coordinate system Z-axis, depending on the specified CSys. [rad]

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
```
```
Element = 1
```
```
GroupElm = 2
```
```
SelectionElm = 3
```
If this item is ObjectElm, the ground displacement assignments are retrieved for the point element
corresponding to the point object specified by the Name item.

If this item is Element, the ground displacement assignments are retrieved for the point element
specified by the Name item.

If this item is GroupElm, the ground displacement assignments are retrieved for all point elements
directly or indirectly specified in the group specified by the Name item.

If this item is SelectionElm, the ground displacement assignments are retrieved for all point
elements directly or indirectly selected, and the Name item is ignored.

See Item Type for Elements for more information.


## Remarks

This function retrieves the ground displacement load assignments to point elements.

The function returns zero if the load assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetPointElmDisplLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim PointName() As String
Dim LoadPat() As String
Dim LCStep() As Long
Dim CSys() As String
Dim U1() As Double
Dim U2() As Double
Dim U3() As Double
Dim R1() As Double
Dim R2() As Double
Dim R3() As Double
Dim Value() As Double

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

'add ground displacement load
Redim Value(5)
Value(0) = 10
ret = SapModel.PointObj.SetLoadDispl("1", "DEAD", Value)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get ground displacement load at point elements
ret = SapModel.PointElm.GetLoadDispl("ALL", NumberItems, PointName, LoadPat,


LCStep, CSys, U1, U2, U3, R1, R2, R3, GroupElm)

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

# GetLoadForce

## Syntax

SapObject.SapModel.PointElm.GetLoadForce

## VB6 Procedure

Function GetLoadForce(ByVal Name As String, ByRef NumberItems As Long, ByRef
PointName() As String, ByRef LoadPat() As String, ByRef LCStep() As Long, ByRef CSys() As
String, ByRef F1() As Double, ByRef F2() As Double, ByRef F3() As Double, ByRef M1() As
Double, ByRef M2() As Double, ByRef M3() As Double, Optional ByVal ItemTypeElm As
eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects, depending on the value
of the ItemTypeElm item.

NumberItems

This is the total number of joint force load assignments returned.

PointName

This is an array that includes the name of the point element to which the specified load assignment
applies.

LoadPat


This is an array that includes the name of the load pattern for the load.

LCStep

This is an array that includes the load pattern step for the load. In most cases this item does not
apply and will be returned as 0.

CSys

This is an array that includes the name of the coordinate system for the load. This is either Local
or the name of a defined coordinate system.

F1

This is an array that includes the assigned translational force in the local 1-axis or coordinate
system X-axis direction, depending on the specified CSys. [F]

F2

This is an array that includes the assigned translational force in the local 2-axis or coordinate
system Y-axis direction, depending on the specified CSys. [F]

F3

This is an array that includes the assigned translational force in the local 3-axis or coordinate
system Z-axis direction, depending on the specified CSys. [F]

M1

This is an array that includes the assigned moment about the local 1-axis or coordinate system X-
axis, depending on the specified CSys. [FL]

M2

This is an array that includes the assigned moment about the local 2-axis or coordinate system Y-
axis, depending on the specified CSys. [FL]

M3

This is an array that includes the assigned moment about the local 3-axis or coordinate system Z-
axis, depending on the specified CSys. [FL]

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the point element corresponding
to the point object specified by the Name item.


If this item is Element, the load assignments are retrieved for the point element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for all point elements directly or
indirectly specified in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for all point elements directly or
indirectly selected and the Name item is ignored.

See Item Type for Elements for more information.

## Remarks

This function retrieves the joint force load assignments to point elements.

The function returns zero if the load assignments are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetPointElmForceLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim PointName() As String
Dim LoadPat() As String
Dim LCStep() As Long
Dim CSys() As String
Dim F1() As Double
Dim F2() As Double
Dim F3() As Double
Dim M1() As Double
Dim M2() As Double
Dim M3() As Double
Dim Value() As Double

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


'add joint force load
Redim Value(5)
Value(0) = 10
ret = SapModel.PointObj.SetLoadForce("1", "DEAD", Value)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get point element force load
ret = SapModel.PointElm.GetLoadForce("ALL", NumberItems, PointName, LoadPat,
LCStep, CSys, F1, F2, F3, M1, M2, M3, GroupElm)

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

# GetLocalAxes

## Syntax

SapObject.SapModel.PointElm.GetLocalAxes

## VB6 Procedure

Function GetLocalAxes(ByVal Name As String, ByRef a As Double, ByRef b As Double, ByRef
c As Double) As Long

## Parameters

Name

The name of an existing point element.

a, b, c

The local axes of the point are defined by first setting the positive local 1, 2 and 3 axes the same as
the positive global X, Y and Z axes and then doing the following: [deg]


1. Rotate about the 3 axis by angle a.
2. Rotate about the resulting 2 axis by angle b.
3. Rotate about the resulting 1 axis by angle c.

## Remarks

This function retrieves the local axes angles for a point element.

The function returns zero if the local axes angles are successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetPointElmLocalAxes()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim a As Double, b As Double, c As Double

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

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get local axes assignments
ret = SapModel.PointElm.GetLocalAxes("1", a, b, c)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# GetMergeNumber

## Syntax

SapObject.SapModel.PointElm.GetMergeNumber

## VB6 Procedure

Function GetMergeNumber(ByVal Name As String, ByRef MergeNumber As Long) As Long

## Parameters

Name

The name of an existing point element.

MergeNumber

The merge number assigned to the specified point element.

## Remarks

This function retrieves the merge number for a point element. By default the merge number for a
point is zero. Points with different merge numbers are not automatically merged by the program.

The function returns zero if the merge number is successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetPointElmMergeNumber()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim m As Long

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

'set merge number
ret = SapModel.PointObj.SetMergeNumber("3", 2)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get merge number
ret = SapModel.PointElm.GetMergeNumber("3", m)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetNameList

## Syntax

SapObject.SapModel.PointElm.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of point element names retrieved by the program.

MyName

This is a one-dimensional array of point element names. The MyName array is created as a
dynamic, zero-based, array by the API user:


Dim MyName() as String

The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined point elements.

The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetPointElementNames()
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get point element names
ret = SapModel.PointElm.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.00.

## See Also

# GetObj

## Syntax

SapObject.SapModel.PointElm.GetObj

## VB6 Procedure

Function GetObj(ByVal Name As String, ByRef Obj As String, ByRef ObjType As Long) As
Long

## Parameters

Name

The name of an existing point element.

Obj

The name of the object or defined item associated with the specified point element. The type of
object or item is determined from the ObjType variable.

ObjType

A number indicating the type of object or defined item that is associated with the point element.

```
1
Obj is the point object corresponding to the specified point element.
```
```
2
Obj is a line object that is internally meshed by the program to create the specified
point element.
```
```
3
Obj is an area object that is internally meshed by the program to create the specified
point element.
```
```
6
Obj is a solid object that is internally meshed by the program to create the specified
point element.
```
```
9
Obj is a point object that has a panel zone assignment. The specified point element is
internally added by the program at the point object (panel zone) location to model
the panel zone. The specified point element does not directly correspond to the point
object returned; it is an added point at the same location as the point object.
```

### 21

```
Obj is a defined diaphragm constraint. The specified point element was internally
added by the program for application of auto wind and auto seismic loads.
```
```
107
Obj is a link element that was generated as part of the analysis model.
```
## Remarks

This function retrieves the object or defined item associated with a specified point element.

The function returns zero if the object is successfully retrieved, otherwise it returns a nonzero
value.

## VBA Example

Sub GetObjForPointElm()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Obj As String
Dim ObjType As Long

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

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get object or defined item for point element "3"
ret = SapModel.PointElm.GetObj("3", Obj, ObjType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Added link element as an ObjType option in v22.1.0.

Initial release in version 11.00.

## See Also

# GetPatternValue

## Syntax

SapObject.SapModel.PointElm.GetPatternValue

## VB6 Procedure

Function GetPatternValue(ByVal Name As String, ByVal PatternName As String, ByRef Value
As Double) As Long

## Parameters

Name

The name of an existing point element.

PatternName

The name of a defined joint pattern.

Value

The value that the specified point element has for the specified joint pattern.

## Remarks

This function retrieves the joint pattern value for a specific point element and joint pattern.

The function returns zero if the value is successfully retrieved, otherwise it returns a nonzero
value.

Joint pattern values are unitless.

## VBA Example

Sub GetPointElmPatternData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim Value As Double

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

'add joint pattern assignment
ret = SapModel.PointObj.SetPatternByXYZ("ALL", "Default", 0, 0, 10, 0, Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get joint pattern assignment for point element
ret = SapModel.PointElm.GetPatternValue("3", "Default", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetRestraint

## Syntax

SapObject.SapModel.PointElm.GetRestraint

## VB6 Procedure

Function GetRestraint(ByVal Name As String, ByRef Value() As Boolean) As Long


## Parameters

Name

The name of an existing point element.

Value

This is an array of six restraint values.

```
Value(0) = U1
Value(1) = U2
Value(2) = U3
Value(3) = R1
Value(4) = R2
Value(5) = R3
```
## Remarks

This function retrieves the restraint assignments for a point element. The restraint assignments are
always returned in the point local coordinate system.

The function returns zero if the restraint assignments are successfully retrieved, otherwise it
returns a nonzero value.

## VBA Example

Sub GetPointElmRestraints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value() As Boolean

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

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel


'get point element restraints
Redim Value(5)
ret = SapModel.PointElm.GetRestraint("5", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetSpring

## Syntax

SapObject.SapModel.PointElm.GetSpring

## VB6 Procedure

Function GetSpring(ByVal Name As String, ByRef k() As Double) As Long

## Parameters

Name

The name of an existing point element.

k

This is an array of six spring stiffness values.

```
Value(0) = U1 [F/L]
Value(1) = U2 [F/L]
Value(2) = U3 [F/L]
Value(3) = R1 [FL/rad]
Value(4) = R2 [FL/rad]
Value(5) = R3 [FL/rad]
```
## Remarks

This function retrieves uncoupled spring stiffness assignments for a point element; that is, it
retrieves the diagonal terms in the 6x6 spring matrix for the point element.


The spring stiffnesses reported are the sum of all springs assigned to the point element either
directly or indirectly through line, area and solid spring assignments. The spring stiffness values
are reported in the point local coordinate system.

The function returns zero if the stiffnesses are successfully retrieved, otherwise it returns a
nonzero value. If no springs exist at the point element, the function returns a nonzero value.

## VBA Example

Sub GetPointElmSpring()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim k() As Double

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

'assign spring to a point
ReDim k(5)
k(2) = 10
ret = SapModel.PointObj.SetSpring("3", k)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get spring values at point element
ReDim k(5)
ret = SapModel.PointElm.GetSpring("3", k)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.00.

## See Also

GetSpringCoupled

IsSpringCoupled

# GetSpringCoupled

## Syntax

SapObject.SapModel.PointElm.GetSpringCoupled

## VB6 Procedure

Function GetSpringCoupled(ByVal Name As String, ByRef k() As Double) As Long

## Parameters

Name

The name of an existing point element.

k

This is an array of twenty one spring stiffness values.

```
Value(0) = U1U1 [F/L]
Value(1) = U1U2 [F/L]
Value(2) = U2U2 [F/L]
Value(3) = U1U3 [F/L]
Value(4) = U2U3 [F/L]
Value(5) = U3U3 [F/L]
Value(6) = U1R1 [F/rad]
Value(7) = U2R1 [F/rad]
Value(8) = U3R1 [F/rad]
Value(9) = R1R1 [FL/rad]
Value(10) = U1R2 [F/rad]
Value(11) = U2R2 [F/rad]
Value(12) = U3R2 [F/rad]
Value(13) = R1R2 [FL/rad]
Value(14) = R2R2 [FL/rad]
Value(15) = U1R3 [F/rad]
Value(16) = U2R3 [F/rad]
Value(17) = U3R3 [F/rad]
Value(18) = R1R3 [FL/rad]
Value(19) = R2R3 [FL/rad]
Value(20) = R3R3 [FL/rad]
```

## Remarks

This function retrieves coupled spring stiffness assignments for a point element.

The spring stiffnesses reported are the sum of all springs assigned to the point element either
directly or indirectly through line, area and solid spring assignments. The spring stiffness values
are reported in the point local coordinate system.

The function returns zero if the stiffnesses are successfully retrieved, otherwise it returns a
nonzero value. If no springs exist at the point element, the function returns a nonzero value.

## VBA Example

Sub GetPointElmCoupledSpring()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim k() As Double

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

'assign coupled spring to a point
ReDim k(20)
k(2) = 10
k(17) = 4
ret = SapModel.PointObj.SetSpringCoupled("3", k)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get point element coupled spring values
ReDim k(20)
ret = SapModel.PointElm.GetSpringCoupled("3", k)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetSpring

IsSpringCoupled

# GetTransformationMatrix

## Syntax

SapObject.SapModel.PointElm.GetTransformationMatrix

## VB6 Procedure

Function GetTransformationMatrix(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing point element.

Value

Value is an array of nine direction cosines that define the transformation matrix.

The following matrix equation shows how the transformation matrix is used to convert items from
the point element local coordinate system to the global coordinate system.

In the equation, c0 through c8 are the nine values from the transformation array; (Local1, Local2,
Local3) are an item (such as a point load) in the point element local coordinate system; and
(GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.


## Remarks

The function returns zero if the transformation matrix is successfully retrieved, otherwise it returns
a nonzero value.

## VBA Example

Sub GetPointElementMatrix()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value() As double

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

'set local axes
ret = SapModel.PointObj.SetLocalAxes("3", 33, 14, 12)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get point element transformation matrix
redim Value(8)
ret = SapModel.PointElm.GetTransformationMatrix("3", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# IsSpringCoupled

## Syntax

SapObject.SapModel.PointElm.IsSpringCoupled

## VB6 Procedure

Function IsSpringCoupled(ByVal Name As String, ByVal IsCoupled As Boolean) As Long

## Parameters

Name

The name of an existing point element.

IsCoupled

This item is True if the spring assignment to the specified point element is coupled, otherwise it is
False.

## Remarks

This function indicates if the spring assignments to a point element are coupled, that is, if there are
off-diagonal terms in the 6x6 spring matrix for the point element.

The function returns zero if the coupled status is successfully retrieved, otherwise it returns a
nonzero value. If no springs exist at the point object, the function returns a nonzero value.

## VBA Example

Sub CheckIsPointElmSpringCoupled()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim k() As Double
Dim IsCoupled As Boolean

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

'assign spring to a point
ReDim k(5)
k(2) = 10
ret = SapModel.PointObj.SetSpring("3", k)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'determine if point element spring is coupled
ret = SapModel.PointElm.IsSpringCoupled("3", IsCoupled)
'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetSpring

GetSpringCoupled

# Count

## Syntax

Sap2000.SolidElm.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None


## Remarks

This function returns the total number of solid elements in the analysis model.

## VBA Example

Sub CountSolidElements()
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
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign auto mesh options
ret = SapModel.SolidObj.SetAutoMesh("ALL", 1, 2, 2, 2, , , , , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'return number of solid elements
Count = SapModel.SolidElm.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also


# GetLoadGravity

## Syntax

SapObject.SapModel.SolidElm.GetLoadGravity

## VB6 Procedure

Function GetLoadGravity(ByVal Name As String, ByRef NumberItems As Long, ByRef
SolidName() As String, ByRef LoadPat() As String, ByRef CSys() As String, ByRef x() As
Double, ByRef y() As Double, ByRef z() As Double, Optional ByVal ItemTypeElm As
eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing solid element or group, depending on the value of the ItemType item.

NumberItems

The total number of gravity loads retrieved for the specified solid elements.

SolidName

This is an array that includes the name of the solid element associated with each gravity load.

LoadPat

This is an array that includes the name of the coordinate system in which the gravity load
multipliers are specified.

CSys

This is an array that includes the name of the coordinate system associated with each gravity load.

x, y, z

These are arrays of gravity load multipliers in the x, y and z directions of the specified coordinate
system.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```

If this item is ObjectElm, the load assignments are retrieved for the solid elements corresponding
to the solid object specified by the Name item.

If this item is Element, the load assignments are retrieved for the solid element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the solid elements corresponding
to all solid objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for solid elements corresponding
to all selected solid objects, and the Name item is ignored.

## Remarks

This function retrieves the gravity load assignments to solid elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSolidElementGravityLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim SolidName() As String
Dim LoadPat() As String
Dim CSys() As String
Dim x() As Double
Dim y() As Double
Dim z() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign auto mesh options
ret = SapModel.SolidObj.SetAutoMesh("ALL", 1, 2, 2, 2, , , , , , Group)


'assign solid object gravity loads
ret = SapModel.SolidObj.SetLoadGravity("ALL", "DEAD", 0, 0, -1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get solid element gravity load
ret = SapModel.SolidElm.GetLoadGravity("3-1", NumberItems, SolidName, LoadPat, CSys,
x, y, z)

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

# GetLoadPorePressure

## Syntax

SapObject.SapModel.SolidElm.GetLoadPorePressure

## VB6 Procedure

Function GetLoadPorePressure(ByVal Name As String, ByRef NumberItems As Long, ByRef
SolidName() As String, ByRef LoadPat() As String, ByRef Value() As Double, ByRef
PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing solid element or group, depending on the value of the ItemType item.

NumberItems

The total number of pore pressure loads retrieved for the specified solid elements.

SolidName


This is an array that includes the name of the solid element associated with each pore pressure
load.

LoadPat

This is an array that includes the name of the load pattern associated with each pore pressure load.

Value

This is an array that includes the pore pressure load value. [F/L^2 ]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the pore pressure load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the solid elements corresponding
to the solid object specified by the Name item.

If this item is Element, the load assignments are retrieved for the solid element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the solid elements corresponding
to all solid objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for solid elements corresponding to
all selected solid objects, and the Name item is ignored.

## Remarks

This function retrieves the pore pressure load assignments to solid elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSolidElementPorePressureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim SolidName() As String


Dim LoadPat() As String
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign solid object pore pressure load
ret = SapModel.SolidObj.SetLoadPorePressure("ALL", "DEAD", .1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get solid element pore pressure load
ret = SapModel.SolidElm.GetLoadPorePressure("ALL", NumberItems, SolidName, LoadPat,
Value, PatternName, GroupElm)

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

# GetLoadStrain

## Syntax

SapObject.SapModel.SolidElm.GetLoadStrain


## VB6 Procedure

Function GetLoadStrain(ByVal Name As String, ByRef NumberItems As Long, ByRef
SolidName() As String, ByRef LoadPat() As String, ByRef Component() As Long, ByRef Value()
As Double, ByRef PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm =
Element) As Long

## Parameters

Name

The name of an existing solid element or group, depending on the value of the ItemType item.

NumberItems

The total number of strain loads retrieved for the specified solid elements.

SolidName

This is an array that includes the name of the solid element associated with each strain load.

LoadPat

This is an array that includes the name of the load pattern associated with each strain load.

Component

This is 1, 2, 3, 4, 5 or 6, indicating the component to which the strain load is applied.

```
1 = Strain11
2 = Strain22
3 = Strain33
4 = Strain12
5 = Strain13
6 = Strain23
```
Value

This is an array that includes the strain value. [L/L]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the strain load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```

If this item is ObjectElm, the load assignments are retrieved for the solid elements corresponding
to the solid object specified by the Name item.

If this item is Element, the load assignments are retrieved for the solid element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the solid elements corresponding
to all solid objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for solid elements corresponding to
all selected solid objects, and the Name item is ignored.

## Remarks

This function retrieves the strain load assignments to solid elements.

The function returns zero if the strain load assignments are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetSolidElementStrainLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim SolidName() As String
Dim LoadPat() As String
Dim Component() As Long
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign solid object strain load
ret = SapModel.SolidObj.SetLoadStrain("ALL", "DEAD", 1, 0.001, , , Group)

'create analysis model


ret = SapModel.Analyze.CreateAnalysisModel

'get solid element strain load
ret = SapModel.SolidElm.GetLoadStrain("1", NumberItems, SolidName, LoadPat,
Component, Value, PatternName)

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

# GetLoadSurfacePressure

## Syntax

SapObject.SapModel.SolidElm.GetLoadSurfacePressure

## VB6 Procedure

Function GetLoadSurfacePressure(ByVal Name As String, ByRef NumberItems As Long, ByRef
SolidName() As String, ByRef LoadPat() As String, ByRef Face() As Long, ByRef Value() As
Double, ByRef PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm =
Element) As Long

## Parameters

Name

The name of an existing solid element or group, depending on the value of the ItemType item.

NumberItems

The total number of surface pressure loads retrieved for the specified solid elements.

SolidName

This is an array that includes the name of the solid element associated with each surface pressure
load.


LoadPat

This is an array that includes the name of the load pattern associated with each surface pressure
load.

Face

This is an array that includes 1, 2, 3, 4, 5 or 6, indicating the solid element face to which the
specified load assignment applies.

Value

This is an array that includes the surface pressure load value. [F/L^2 ]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the surface pressure
load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the load assignments are retrieved for the solid elements corresponding
to the solid object specified by the Name item.

If this item is Element, the load assignments are retrieved for the solid element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the solid elements corresponding
to all solid objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for solid elements corresponding to
all selected solid objects, and the Name item is ignored.

## Remarks

This function retrieves the surface pressure load assignments to solid objects.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSolidElementSurfacePressureLoad()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim SolidName() As String
Dim LoadPat() As String
Dim Face() As Long
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign solid object surface pressure load
ret = SapModel.SolidObj.SetLoadSurfacePressure("ALL", "DEAD", 1, .1, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get solid element surface pressure load
ret = SapModel.SolidElm.GetLoadSurfacePressure("ALL", NumberItems,
SolidName,LoadPat, Face, Value, PatternName, GroupElm)

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

# GetLoadTemperature

## Syntax

SapObject.SapModel.SolidElm.GetLoadTemperature

## VB6 Procedure

Function GetLoadTemperature(ByVal Name As String, ByRef NumberItems As Long, ByRef
SolidName() As String, ByRef LoadPat() As String, ByRef Value() As Double, ByRef
PatternName() As String, Optional ByVal ItemTypeElm As eItemTypeElm = Element) As Long

## Parameters

Name

The name of an existing solid element or group, depending on the value of the ItemType item.

NumberItems

The total number of temperature loads retrieved for the specified solid elements.

SolidName

This is an array that includes the name of the solid element associated with each temperature load.

LoadPat

This is an array that includes the name of the load pattern associated with each temperature load.

Value

This is an array that includes the temperature load value. [T]

PatternName

This is an array that includes the joint pattern name, if any, used to specify the temperature load.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```

If this item is ObjectElm, the load assignments are retrieved for the solid elements corresponding
to the solid object specified by the Name item.

If this item is Element, the load assignments are retrieved for the solid element specified by the
Name item.

If this item is GroupElm, the load assignments are retrieved for the solid elements corresponding
to all solid objects included in the group specified by the Name item.

If this item is SelectionElm, the load assignments are retrieved for solid elements corresponding to
all selected solid objects, and the Name item is ignored.

## Remarks

This function retrieves the temperature load assignments to solid elements.

The function returns zero if the load assignments are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSolidElementTemperatureLoad()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim SolidName() As String
Dim LoadPat() As String
Dim Value() As Double
Dim PatternName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign solid object temperature load
ret = SapModel.SolidObj.SetLoadTemperature("All", "DEAD", 50, , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel


'get solid element temperature load
ret = SapModel.SolidElm.GetLoadTemperature("ALL", NumberItems, SolidName, LoadPat,
Value, PatternName, GroupElm)

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

# GetLocalAxes

## Syntax

SapObject.SapModel.SolidElm.GetLocalAxes

## VB6 Procedure

Function GetLocalAxes(ByVal Name As String, ByRef a As Double, ByRef b As Double, ByRef
c As Double) As Long

## Parameters

Name

The name of an existing solid element.

a, b, c

The local axes of the solid element are defined by first setting the positive local 1, 2 and 3 axes the
same as the positive global X, Y and Z axes and then doing the following: [deg]

1. Rotate about the 3 axis by angle a.
2. Rotate about the resulting 2 axis by angle b.
3. Rotate about the resulting 1 axis by angle c.

## Remarks


This function retrieves the local axis angle assignment for solid elements.

The function returns zero if the assignment is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetSolidElementLocalAxisAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim a As Double, b As Double, c As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign local axes angles
ret = SapModel.SolidObj.SetLocalAxes("ALL", 30, 40, 50, Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get solid element local axis angle
ret = SapModel.SolidElm.GetLocalAxes("1", a, b, c)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also


# GetMatTemp

## Syntax

SapObject.SapModel.SolidElm.GetMatTemp

## VB6 Procedure

Function GetMatTemp(ByVal Name As String, ByRef Temp As Double, ByRef PatternName As
String) As Long

## Parameters

Name

The name of an existing solid element.

Temp

This is the material temperature value assigned to the solid element. [T]

PatternName

This is blank or the name of a defined joint pattern. If it is blank, the material temperature for the
solid element is uniform over the element at the value specified by Temp.

If PatternName is the name of a defined joint pattern, the material temperature for the solid
element may vary. The material temperature at each corner point of the solid element is equal to
the specified temperature multiplied by the pattern value at the associated point element. The
material temperature at other locations in the solid element is calculated by interpolation from the
corner points.

## Remarks

This function retrieves the material temperature assignments to solid elements.

The function returns zero if the material temperature assignments are successfully retrieved;
otherwise it returns a nonzero value.

## VBA Example

Sub GetSolidElementMatTemp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Temp As Double
Dim PatternName As String


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign material temperature
ret = SapModel.SolidObj.SetMatTemp("ALL", 50, , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get material temperature for solid element
ret = SapModel.SolidElm.GetMatTemp("1", Temp, PatternName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetNameList

## Syntax

SapObject.SapModel.SolidElm.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters


NumberNames

The number of solid element names retrieved by the program.

MyName

This is a one-dimensional array of solid element names. The MyName array is created as a
dynamic, zero-based, array by the API user:

Dim MyName() as String

The array is dimensioned to (NumberNames – 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined solid elements.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetSolidElementNames()
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
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get solid element names
ret = SapModel.SolidElm.GetNameList(NumberNames, MyName)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetObj

## Syntax

Sap2000.SolidElm.GetObj

## VB6 Procedure

Function GetObj(ByVal Name As String, ByRef Obj As String) As Long

## Parameters

Name

The name of an existing solid element.

Obj

The name of the solid object from which the solid element was created.

## Remarks

This function retrieves the name of the solid object from which a solid element was created.

The function returns zero if the information is successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetObjForSolidElm()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Obj As String


Dim ObjType As Long
Dim RDI As Double
Dim RDJ As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign auto mesh options
ret = SapModel.SolidObj.SetAutoMesh("ALL", 1, 2, 2, 2, , , , , , Group)

'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get object information for an solid element
ret = SapModel.SolidElm.GetObj("3-2", Obj)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetPoints

## Syntax

SapObject.SapModel.SolidElm.GetPoints

## VB6 Procedure

Function GetPoints(ByVal Name As String, ByRef Point() As String) As Long


## Parameters

Name

The name of an solid element.

Point

This is an array containing the names of the eight point elements that define the solid element. The
point names are in order around the solid element.

## Remarks

This function retrieves the names of the eight point elements that define a solid element.

The function returns zero if the point element names are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetSolidElmPoints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Point() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign auto mesh options
ret = SapModel.SolidObj.SetAutoMesh("ALL", 1, 2, 2, 2, , , , , , Group)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get names of eight corner points
ret = SapModel.SolidElm.GetPoints("3-2", Point)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetProperty

## Syntax

SapObject.SapModel.SolidElm.GetProperty

## VB6 Procedure

Function GetProperty(ByVal Name As String, ByRef PropName As String) As Long

## Parameters

Name

The name of a defined solid element.

PropName

The name of the solid property assigned to the solid element.

## Remarks

This function retrieves the solid property assigned to a solid element.

The function returns zero if the property is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetSolidElementProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropName As String


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get solid property for element
ret = SapModel.SolidElm.GetProperty("1", PropName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetTransformationMatrix

## Syntax

Sap2000.SolidElm.GetTransformationMatrix

## VB6 Procedure

Function GetTransformationMatrix(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name


The name of an existing solid element.

Value

Value is an array of nine direction cosines that define the transformation matrix.

The following matrix equation shows how the transformation matrix is used to convert items from
the solid element local coordinate system to the global coordinate system.

In the equation, c0 through c8 are the nine values from the transformation array, (Local1, Local2,
Local3) are an item (such as a load) in the element local coordinate system, and (GlobalX,
GlobalY, GlobalZ) are the same item in the global coordinate system.

## Remarks

The function returns zero if the transformation matrix is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetSolidElementMatrix()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewSolidBlock(300, 400, 200, , , 2, 2, 2)

'assign local axes angles
ret = SapModel.SolidObj.SetLocalAxes("ALL", 30, 40, 50, Group)


'create analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'get solid element transformation matrix
redim Value(8)
ret = SapModel.SolidElm.GetTransformationMatrix("1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also


