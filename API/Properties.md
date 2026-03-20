# ChangeName

## Syntax

SapObject.SapModel.PropArea.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined area property.

NewName

The new name for the area property.

## Remarks

This function changes the name of an existing area property.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeAreaPropName()
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


ret = SapModel.File.NewWall(2, 48, 2, 48)

'change name of area property
ret = SapModel.PropArea.ChangeName("ASEC1", "MyArea")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Count

## Syntax

SapObject.SapModel.PropArea.Count

## VB6 Procedure

Function Count(Optional ByVal PropType As Long = 0) As Long

## Parameters

PropType

This optional value is 0, 1, 2 or 3, indicating the type of area properties included in the count.

```
0 = All
1 = Shell
2 = Plane
3 = Asolid
```
## Remarks

This function returns the total number of defined area properties in the model. If desired, counts
can be returned for all area properties of a specified type in the model.

## VBA Example

Sub CountAreaProps()
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

'return number of defined area properties of all types
Count = SapModel.PropArea.Count

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Delete

## Syntax

SapObject.SapModel.PropArea.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name


The name of an existing area property.

## Remarks

The function deletes a specified area property.

The function returns zero if the area property is successfully deleted; otherwise it returns a
nonzero value. It returns an error if the specified area property can not be deleted, for example, if
it is being used by an area object.

## VBA Example

Sub DeleteAreaProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
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

'set new area property
ret = SapModel.PropArea.SetShell("A1", 1, "4000Psi", 0, 16, 16)

'get area object names
ret = SapModel.AreaObj.GetNameList(NumberNames, MyName)

'assign area property
For i = 1 to NumberNames
ret = SapModel.AreaObj.SetProperty(MyName(i - 1), "A1")
Next i

'delete area property
ret = SapModel.PropArea.Delete("ASEC1")

'close Sap


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetAsolid

## Syntax

SapObject.SapModel.PropArea.GetAsolid

## VB6 Procedure

Function GetAsolid(ByVal Name As String, ByRef MatProp As String, ByRef MatAng As
Double, ByRef Arc As Double, ByRef Incompatible As Boolean, ByRef CSys As String, ByRef
Color As Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing asolid-type area property.

MatProp

The name of the material property for the area property.

MatAng

The material angle. [deg]

Arc

The arc angle through which the area object is passed to define the asolid element. [deg]

A value of zero means 1 radian (approximately 57.3 degrees).

Incompatible

If this item is True, incompatible bending modes are included in the stiffness formulation. In
general, incompatible modes significantly improve the bending behavior of the object.

CSys


The area object is rotated about the Z-axis in this coordinate system to define the asolid element.

Color

The display color assigned to the property.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves area property data for an asolid-type area section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaPropAsolid()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim MatAng As Double
Dim Arc As Double
Dim Incompatible As Boolean
Dim CSys As String
Dim Color As Long
Dim Notes As String
Dim GUID As String

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


'set new area property
ret = SapModel.PropArea.SetAsolid("AS1", "4000Psi", 0, 45, True)

'get area property data
ret = SapModel.PropArea.GetAsolid("AS1", MatProp, MatAng, Arc, Incompatible, CSys,
Color, Notes, GUID)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetAsolid

# GetModifiers

## Syntax

SapObject.SapModel.PropArea.GetModifiers

## VB6 Procedure

Function GetModifiers(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing area property.

Value

This is an array of 10 unitless modifiers.

```
Value(0) = Membrane f11 modifier
Value(1) = Membrane f22 modifier
Value(2) = Membrane f12 modifier
Value(3) = Bending m11 modifier
Value(4) = Bending m22 modifier
Value(5) = Bending m12 modifier
Value(6) = Shear v13 modifier
Value(7) = Shear v23 modifier
```

```
Value(8) = Mass modifier
Value(9) = Weight modifier
```
## Remarks

This function retrieves the modifier assignments for an area property. The default value for all
modifiers is one.

The function returns zero if the modifier assignments are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetAreaPropModifiers()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
Dim MyValue() As Double
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
ReDim MyValue(9)
For i = 0 To 9
MyValue(i) = 1
Next i
MyValue(0) = 0.
ret = SapModel.PropArea.SetModifiers("ASEC1", MyValue)

'get modifiers
ret = SapModel.PropArea.GetModifiers("ASEC1", Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetModifiers

# GetNameList

## Syntax

SapObject.SapModel.PropArea.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String, Optional
ByVal PropType As Long = 0) As Long

## Parameters

NumberNames

The number of area property names retrieved by the program.

MyName

This is a one-dimensional array of area property names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

PropType

This optional value is 0, 1, 2 or 3, indicating the type of area properties included in the name list.

```
0 = All
1 = Shell
2 = Plane
3 = Asolid
```

## Remarks

This function retrieves the names of all defined area properties of the specified type.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetAreaPropNames()
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

'get area property names
ret = SapModel.PropArea.GetNameList(NumberNames, MyName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetPlane


## Syntax

SapObject.SapModel.PropArea.GetPlane

## VB6 Procedure

Function GetPlane(ByVal Name As String, ByRef MyType As Long, ByRef MatProp As String,
ByRef MatAng As Double, ByRef Thickness As Double, ByRef Incompatible As Boolean, ByRef
Color As Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing plane-type area property.

MyType

This is either 1 or 2, indicating the plane type.

```
1 = Plane-stress
2 = Plane-strain
```
MatProp

The name of the material property for the area property.

MatAng

The material angle. [deg]

Thickness

The plane thickness. [L]

Incompatible

If this item is True, incompatible bending modes are included in the stiffness formulation. In
general, incompatible modes significantly improve the bending behavior of the object.

Color

The display color assigned to the property.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.


## Remarks

This function retrieves area property data for a plane-type area section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaPropPlane()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyType As Long
Dim MatProp As String
Dim MatAng As Double
Dim Thickness As Double
Dim Incompatible As Boolean
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new area property
ret = SapModel.PropArea.SetPlane("P1", 1, "4000Psi", 0, 9, True)

'get area property data
ret = SapModel.PropArea.GetPlane("P1", MyType, MatProp, MatAng, Thickness,
Incompatible, Color, Notes, GUID)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

SetPlane

# GetShell_

## Syntax

SapObject.SapModel.PropArea.GetShell

## VB6 Procedure

Function GetShell_1(ByVal Name As String, ByRef ShellType As Long, ByRef
IncludeDrillingDOF As Boolean, ByRef MatProp As String, ByRef MatAng As Double, ByRef
Thickness As Double, ByRef Bending As Double, ByRef Color As Long, ByRef Notes As String,
ByRef GUID As String) As Long

## Parameters

Name

The name of an existing shell-type area property.

ShellType

This is 1, 2, 3, 4, 5 or 6, indicating the shell type.

```
1 = Shell - thin
2 = Shell - thick
3 = Plate - thin
4 = Plate - thick
5 = Membrane
6 = Shell layered/nonlinear
```
IncludeDrillingDOF

This item is True if drilling degrees of freedom are included in the element formulation in the
analysis model. This item does not apply when ShellType = 3, 4 or 6.

MatProp

The name of the material property for the area property. This item does not apply when ShellType
= 6.

MatAng


The material angle. [deg]

This item does not apply when ShellType = 6.

Thickness

The membrane thickness. [L]

This item does not apply when ShellType = 6.

Bending

The bending thickness. [L]

This item does not apply when ShellType = 6.

Color

The display color assigned to the property.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves area property data for a shell-type area section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaPropShell_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ShellType As Long
Dim IncludeDrillingDOF As Boolean
Dim MatProp As String
Dim MatAng As Double
Dim Thickness As Double
Dim Bending As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new area property
ret = SapModel.PropArea.SetShell("A1", 1, "4000Psi", 0, 16, 16)

'get area property data
ret = SapModel.PropArea.GetShell_1("A1", ShellType, IncludeDrillingDOF, MatProp,
MatAng, Thickness, Bending, Color, Notes, GUID)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.00.

This function supersedes GetShell.

## See Also

SetShell_

# GetShellDesign

## Syntax

SapObject.SapModel.PropArea.GetShellDesign

## VB6 Procedure

Function GetShellDesign(ByVal Name As String, ByRef MatProp As String, ByRef
SteelLayoutOption As Long, ByRef DesignCoverTopDir1 As Double, ByRef
DesignCoverTopDir2 As Double, ByRef DesignCoverBotDir1 As Double, ByRef
DesignCoverBotDir2 As Double) As Long


## Parameters

Name

The name of an existing shell-type area property.

MatProp

The name of the material property for the area property.

SteelLayoutOption

This is 0, 1 or 2 indicating, the rebar layout option.

```
0 = Default
1 = One layer
2 = Two layers
```
DesignCoverTopDir1, DesignCoverTopDir

The cover to the centroid of the top reinforcing steel running in the local 1 and 2 axes directions of
the area object, respectively. [L]

This item applies only when SteelLayoutOption = 1 or 2.

DesignCoverBotDir1, DesignCoverBotDir

The cover to the centroid of the bottom reinforcing steel running in the local 1 and 2 axes
directions of the area object, respectively. [L]

This item applies only when SteelLayoutOption = 2.

## Remarks

This function retrieves area property design parameters for a shell-type area section.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaPropShellDesign()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MatProp As String
Dim SteelLayoutOption As Long
Dim DesignCoverTopDir1 As Double
Dim DesignCoverTopDir2 As Double
Dim DesignCoverBotDir1 As Double


Dim DesignCoverBotDir2 As Double

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

'set new area property
ret = SapModel.PropArea.SetShell("A1", 1, "4000Psi", 0, 16, 16)

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'set area property design parameters
ret = SapModel.PropArea.SetShellDesign("A1", Name, 2, 2, 3, 2.5, 3.5)

'get area property design parameters
ret = SapModel.PropArea.GetShellDesign("A1", MatProp, SteelLayoutOption,
DesignCoverTopDir1, DesignCoverTopDir2, DesignCoverBotDir1, DesignCoverBotDir2)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetShellDesign

# GetShellLayer_

## Syntax


SapObject.SapModel.PropArea.GetShellLayer_

## VB6 Procedure

Function GetShellLayer_2(ByVal Name As String, ByRef NumberLayers As Long, ByRef
LayerName() As String, ByRef Dist() As Double, ByRef Thickness() As Double, ByRef MyType
() As Long, ByRef NumIntegrationPts() As Long, ByRef MatProp() As String, ByRef Matang()
As Double, ByRef MatBehavior() As Long, ByRef S11Type() As Long, ByRef S22Type() As
Long, ByRef S12Type() As Long) As Long

## Parameters

Name

The name of an existing shell-type area property that is specified to be a layered shell property.

NumberLayers

The number of layers in the area property.

LayerName

This is an array that includes the name of each layer.

Dist

This is an array that includes the distance from the area reference surface (area object joint
location plus offsets) to the mid-height of the layer. [L]

Thickness

This is an array that includes the thickness of each layer. [L]

Type

This is an array that includes 1, 2 or 3, indicating the layer type.

```
1 = Shell
```
```
2 = Membrane
```
```
3 = Plate
```
NumIntegrationPts

The number of integration points in the thickness direction for the layer. The locations are
determined by the program using standard Guass-quadrature rules.

MatProp

This is an array that includes the name of the material property for the layer.


MatAng

This is an array that includes the material angle for the layer. [deg]

MatBehavior

This is an array that includes 0 or 1,indicating the material behavior for the layer.

```
0 = Directional
```
```
1 = Coupled
```
S11Type, S22Type, S12Type

These are arrays that include 0, 1 or 2, indicating the material component behavior.

```
0 = Inactive
```
```
1 = Linear
```
```
2 = Nonlinear
```
## Remarks

This function retrieves area property layer parameters for a shell-type area section.

The function returns zero if the parameters are successfully retrieved, otherwise it returns a
nonzero value.

The function returns an error if the specified area property is not a shell-type property specified to
be a layered shell.

## VBA Example

Sub GetAreaPropShellLayer2()

'dimension variables

Dim SapObject as cOAPI

Dim SapModel As cSapModel

Dim ret As Long

Dim Name As String

Dim MyNumberLayers As Long

Dim MyLayerName() As String

Dim MyDist() As Double


Dim MyThickness() As Double

Dim MyType() As Long

Dim MyNumIntegrationPts() As Long

Dim MyMatProp() As String

Dim MyMatAng() As Double

Dim MyMatBehavior() As Long

Dim MyS11Type() As Long

Dim MyS22Type() As Long

Dim MyS12Type() As Long

Dim NumberLayers As Long

Dim LayerName() As String

Dim Dist() As Double

Dim Thickness() As Double

Dim SType() As Long

Dim MatProp() As String

Dim MatAng() As Double

Dim MatBehavior() As Long

Dim S11Type() As Long

Dim S22Type() As Long

Dim S12Type() As Long

Dim NumIntegrationPts() As Long

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

'set new area property

ret = SapModel.PropArea.SetShell("A1", 6, "", 0, 0, 0)

'add A615Gr60 rebar material

ret = SapModel.PropMaterial.AddMaterial(Name, eMatType_Rebar, "United States", "ASTM
A706", "Grade 60")

'set area property layer parameters

MyNumberLayers = 5

ReDim MyLayerName(4)

ReDim MyDist(4)

ReDim MyThickness(4)

ReDim MyType(4)

ReDim MyNumIntegrationPts(4)

ReDim MyMatProp(4)

ReDim MyMatAng(4)

ReDim MyMatBehavior(4)

ReDim MyS11Type(4)

ReDim MyS22Type(4)

ReDim MyS12Type(4)


MyLayerName(0) = "Concrete"

MyDist(0) = 0

MyThickness(0) = 16

MyType(0) = 1

MyNumIntegrationPts(0) = 2

MyMatProp(0) = "4000Psi"

MyMatAng(0) = 0

MyMatBehavior(0) = 1

MyS11Type(0) = 1

MyS22Type(0) = 1

MyS12Type(0) = 1

MyLayerName(1) = "Top Bar 1"

MyDist(1) = 6

MyThickness(1) = 0.03

MyType(1) = 1

MyNumIntegrationPts(1) = 1

MyMatProp(1) = Name

MyMatAng(1) = 0

MyMatBehavior(1) = 0

MyS11Type(1) = 1

MyS22Type(1) = 1

MyS12Type(1) = 1

MyLayerName(2) = "Top Bar 2"

MyDist(2) = 6

MyThickness(2) = 0.03


MyType(2) = 1

MyNumIntegrationPts(2) = 1

MyMatProp(2) = Name

MyMatAng(2) = 90

MyMatBehavior(2) = 0

MyS11Type(2) = 1

MyS22Type(2) = 1

MyS12Type(2) = 1

MyLayerName(3) = "Bot Bar 1"

MyDist(3) = -6

MyThickness(3) = 0.03

MyType(3) = 1

MyNumIntegrationPts(3) = 1

MyMatProp(3) = Name

MyMatAng(3) = 0

MyMatBehavior(3) = 0

MyS11Type(3) = 1

MyS22Type(3) = 1

MyS12Type(3) = 1

MyLayerName(4) = "Bot Bar 2"

MyDist(4) = -6

MyThickness(4) = 0.03

MyType(4) = 1

MyNumIntegrationPts(4) = 1

MyMatProp(4) = Name

MyMatAng(4) = 90


MyMatBehavior(4) = 0

MyS11Type(4) = 1

MyS22Type(4) = 1

MyS12Type(4) = 1

ret = SapModel.PropArea.SetShellLayer_2("A1", MyNumberLayers, MyLayerName, MyDist,
MyThickness, MyType, MyNumIntegrationPts, MyMatProp, MyMatAng, MyMatBehavior,
MyS11Type, MyS22Type, MyS12Type)

'get area property layer parameters

ret = SapModel.PropArea.GetShellLayer_2("A1", NumberLayers, LayerName, Dist,
Thickness, SType, NumIntegrationPts, MatProp, MatAng, MatBehavior, S11Type, S22Type,
S12Type)

'close Sap2000

SapObject.ApplicationExit False

Set SapModel = Nothing

Set SapObject = Nothing

End Sub

## Release Notes

Initial release in version 22.1.0

This function supersedes GetShellLayer_1

## See Also

SetShellLayer_2

# GetTypeOAPI

## Syntax


SapObject.SapModel.PropArea.GetTypeOAPI

## VB6 Procedure

Function GetTypeOAPI(ByVal Name As String, ByRef PropType As Long) As Long

## Parameters

Name

The name of an existing area property.

PropType

This is 1, 2 or 3, indicating the type of area property.

```
1 = Shell
2 = Plane
3 = Asolid
```
## Remarks

This function retrieves the property type for the specified area property.

The function returns zero if the type is successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetAreaPropType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropType As Long

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

'get area property type


ret = SapModel.PropArea.GetTypeOAPI("ASEC1", PropType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed function name to GetTypeOAPI in v17.0.0.

## See Also

# SetAsolid

## Syntax

SapObject.SapModel.PropArea.SetAsolid

## VB6 Procedure

Function SetAsolid(ByVal Name As String, ByVal MatProp As String, ByVal MatAng As
Double, ByVal Arc As Double, ByVal Incompatible As Boolean, Optional ByVal CSys As String
= "Global", Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional
ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new area property. If this is an existing property, that property is
modified; otherwise, a new property is added.

MatProp

The name of the material property for the area property.

MatAng

The material angle. [deg]

Arc

The arc angle through which the area object is passed to define the asolid element. [deg]

A value of zero means 1 radian (approximately 57.3 degrees).


Incompatible

If this item is True, incompatible bending modes are included in the stiffness formulation. In
general, incompatible modes significantly improve the bending behavior of the object.

CSys

The area object is rotated about the Z-axis in this coordinate system to define the asolid element.

Color

The display color assigned to the property. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes an asolid-type area property. If this function is called for an existing area
property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetAreaPropAsolid()
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
ret = SapModel.File.NewWall(2, 48, 2, 48)


'set new area property
ret = SapModel.PropArea.SetAsolid("AS1", "4000Psi", 0, 45, True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetAsolid

# SetModifiers

## Syntax

SapObject.SapModel.PropArea.SetModifiers

## VB6 Procedure

Function SetModifiers(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing area property.

Value

This is an array of 10 unitless modifiers.

```
Value(0) = Membrane f11 modifier
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

This function assigns property modifiers to an area property. The default value for all modifiers is
one.

The function returns zero if the modifiers are successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub AssignAreaPropModifiers()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
Dim MyValue() As Double

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
ReDim MyValue(9)
For i = 0 To 9
MyValue(i) = 1
Next i
MyValue(0) = 0.1
ret = SapModel.PropArea.SetModifiers("ASEC1", MyValue)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

GetModifiers

# SetPlane

## Syntax

SapObject.SapModel.PropArea.SetPlane

## VB6 Procedure

Function SetPlane(ByVal Name As String, ByVal MyType As Long, ByVal MatProp As String,
ByVal MatAng As Double, ByVal Thickness As Double, ByVal Incompatible As Boolean,
Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID
As String = "") As Long

## Parameters

Name

The name of an existing or new area property. If this is an existing property, that property is
modified; otherwise, a new property is added.

MyType

This is either 1 or 2, indicating the plane type.

```
1 = Plane-stress
2 = Plane-strain
```
MatProp

The name of the material property for the area property.

MatAng

The material angle. [deg]

Thickness

The plane thickness. [L]

Incompatible

If this item is True, incompatible bending modes are included in the stiffness formulation. In
general, incompatible modes significantly improve the bending behavior of the object.

Color


The display color assigned to the property. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a plane-type area property. If this function is called for an existing area
property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetAreaPropPlane()
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
ret = SapModel.File.NewWall(2, 48, 2, 48)

'set new area property
ret = SapModel.PropArea.SetPlane("P1", 1, "4000Psi", 0, 9, True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

GetPlane

# SetShell_1

## Syntax

SapObject.SapModel.PropArea.SetShell_1

## VB6 Procedure

Function SetShell(ByVal Name As String, ByVal ShellType As Long, ByVal IncludeDrillingDOF
As Boolean, ByVal MatProp As String, ByVal MatAng As Double, ByVal Thickness As Double,
ByVal Bending As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String
= "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new area property. If this is an existing property, that property is
modified; otherwise, a new property is added.

ShellType

This is 1, 2, 3, 4, 5 or 6, indicating the shell type.

```
1 = Shell - thin
2 = Shell - thick
3 = Plate - thin
4 = Plate - thick
5 = Membrane
6 = Shell layered/nonlinear
```
IncludeDrillingDOF

This item is True if drilling degrees of freedom are included in the element formulation in the
analysis model. This item does not apply when ShellType = 3, 4 or 6.

MatProp

The name of the material property for the area property. This item does not apply when ShellType
= 6.


MatAng

The material angle. [deg]

This item does not apply when ShellType = 6.

Thickness

The membrane thickness. [L]

This item does not apply when ShellType = 6.

Bending

The bending thickness. [L]

This item does not apply when ShellType = 6.

Color

The display color assigned to the property. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, then the program assigns a GUID to the property.

## Remarks

This function initializes a shell-type area property. If this function is called for an existing area
property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetAreaPropShell_1()
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
ret = SapModel.File.NewWall(2, 48, 2, 48)

'set new area property
ret = SapModel.PropArea.SetShell_1("A1", 1, True, "4000Psi", 0, 16, 16)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.00.

This function supersedes SetShell.

## See Also

GetShell_1

# SetShellDesign

## Syntax

SapObject.SapModel.PropArea.SetShellDesign

## VB6 Procedure

Function SetShellDesign(ByVal Name As String, ByVal MatProp As String, ByVal
SteelLayoutOption As Long, ByVal DesignCoverTopDir1 As Double, ByVal
DesignCoverTopDir2 As Double, ByVal DesignCoverBotDir1 As Double, ByVal
DesignCoverBotDir2 As Double) As Long

## Parameters

Name

The name of an existing shell-type area property.


MatProp

The name of the material property for the area property.

SteelLayoutOption

This is 0, 1 or 2, indicating the rebar layout option.

```
0 = Default
1 = One layer
2 = Two layers
```
DesignCoverTopDir1, DesignCoverTopDir2

The cover to the centroid of the top reinforcing steel running in the local 1 and 2 axes directions of
the area object, respectively. [L]

This item applies only when SteelLayoutOption = 1 or 2.

DesignCoverBotDir1, DesignCoverBotDir2

The cover to the centroid of the bottom reinforcing steel running in the local 1 and 2 axes
directions of the area object, respectively. [L]

This item applies only when SteelLayoutOption = 2.

## Remarks

This function assigns the design parameters for shell-type area properties.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetAreaPropShellDesign()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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
ret = SapModel.File.NewWall(2, 48, 2, 48)

'set new area property
ret = SapModel.PropArea.SetShell("A1", 1, "4000Psi", 0, 16, 16)

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'set area property design parameters
ret = SapModel.PropArea.SetShellDesign("A1", Name, 2, 2, 3, 2.5, 3.5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetShellDesign

# SetShellLayer_2

## Syntax

SapObject.SapModel.PropArea.SetShellLayer_2

## VB6 Procedure

Function SetShellLayer_2(ByVal Name As String, ByRef NumberLayers As Long, ByRef
LayerName() As String, ByRef Dist() As Double, ByRef Thickness() As Double, ByRef MyType
() As Long, ByRef NumIntegrationPts() As Long, ByRef MatProp() As String, ByRef Matang()
As Double, ByRef MatBehavior() As Long, ByRef S11Type() As Long, ByRef S22Type() As
Long, ByRef S12Type() As Long) As Long

## Parameters

Name

The name of an existing shell-type area property that is specified to be a layered shell property.


NumberLayers

The number of layers in the area property.

LayerName

This is an array that includes the name of each layer.

Dist

This is an array that includes the distance from the area reference surface (area object joint
location plus offsets) to the mid-height of the layer. [L]

Thickness

This is an array that includes the thickness of each layer. [L]

Type

This is an array that includes 1, 2 or 3, indicating the layer type.

```
1 = Shell
```
```
2 = Membrane
```
```
3 = Plate
```
NumIntegrationPts

The number of integration points in the thickness direction for the layer. The locations are
determined by the program using standard Guass-quadrature rules.

MatProp

This is an array that includes the name of the material property for the layer.

MatAng

This is an array that includes the material angle for the layer. [deg]

MatBehavior

This is an array that includes 0 or 1,indicating the material behavior for the layer.

```
0 = Directional
```
```
1 = Coupled
```
S11Type, S22Type, S12Type

These are arrays that include 0, 1 or 2, indicating the material component behavior.


```
0 = Inactive
```
```
1 = Linear
```
```
2 = Nonlinear
```
## Remarks

This function assigns the layer parameters for shell-type area properties.

The function returns zero if the parameters are successfully assigned; otherwise, it returns a
nonzero value.

The function returns an error if the specified area property is not a shell-type property specified to
be a layered shell.

## VBA Example

Sub SetAreaPropShellLayer2()

'dimension variables

Dim SapObject as cOAPI

Dim SapModel As cSapModel

Dim ret As Long

Dim Name As String

Dim MyNumberLayers As Long

Dim MyLayerName() As String

Dim MyDist() As Double

Dim MyThickness() As Double

Dim MyType() As Long

Dim MyNumIntegrationPts() As Long

Dim MyMatProp() As String

Dim MyMatAng() As Double

Dim MyMatBehavior() As Long

Dim MyS11Type() As Long

Dim MyS22Type() As Long

Dim MyS12Type() As Long


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

'set new area property

ret = SapModel.PropArea.SetShell("A1", 6, "", 0, 0, 0)

'add A615Gr60 rebar material

ret = SapModel.PropMaterial.AddMaterial(Name, eMatType_Rebar, "United States", "ASTM
A706", "Grade 60")

'set area property layer parameters

MyNumberLayers = 5

ReDim MyLayerName(4)

ReDim MyDist(4)

ReDim MyThickness(4)

ReDim MyType(4)


ReDim MyNumIntegrationPts(4)

ReDim MyMatProp(4)

ReDim MyMatAng(4)

ReDim MyMatBehavior(4)

ReDim MyS11Type(4)

ReDim MyS22Type(4)

ReDim MyS12Type(4)

MyLayerName(0) = "Concrete"

MyDist(0) = 0

MyThickness(0) = 16

MyType(0) = 1

MyNumIntegrationPts(0) = 2

MyMatProp(0) = "4000Psi"

MyMatAng(0) = 0

MyMatBehavior(0) = 1

MyS11Type(0) = 1

MyS22Type(0) = 1

MyS12Type(0) = 1

MyLayerName(1) = "Top Bar 1"

MyDist(1) = 6

MyThickness(1) = 0.03

MyType(1) = 1

MyNumIntegrationPts(1) = 1

MyMatProp(1) = Name

MyMatAng(1) = 0

MyMatBehavior(1) = 0


MyS11Type(1) = 1

MyS22Type(1) = 1

MyS12Type(1) = 1

MyLayerName(2) = "Top Bar 2"

MyDist(2) = 6

MyThickness(2) = 0.03

MyType(2) = 1

MyNumIntegrationPts(2) = 1

MyMatProp(2) = Name

MyMatAng(2) = 90

MyMatBehavior(2) = 0

MyS11Type(2) = 1

MyS22Type(2) = 1

MyS12Type(2) = 1

MyLayerName(3) = "Bot Bar 1"

MyDist(3) = -6

MyThickness(3) = 0.03

MyType(3) = 1

MyNumIntegrationPts(3) = 1

MyMatProp(3) = Name

MyMatAng(3) = 0

MyMatBehavior(3) = 0

MyS11Type(3) = 1

MyS22Type(3) = 1

MyS12Type(3) = 1


MyLayerName(4) = "Bot Bar 2"

MyDist(4) = -6

MyThickness(4) = 0.03

MyType(4) = 1

MyNumIntegrationPts(4) = 1

MyMatProp(4) = Name

MyMatAng(4) = 90

MyMatBehavior(4) = 0

MyS11Type(4) = 1

MyS22Type(4) = 1

MyS12Type(4) = 1

ret = SapModel.PropArea.SetShellLayer_2("A1", MyNumberLayers, MyLayerName, MyDist,
MyThickness, MyType, MyNumIntegrationPts, MyMatProp, MyMatAng, MyMatBehavior,
MyS11Type, MyS22Type, MyS12Type)

'close Sap2000

SapObject.ApplicationExit False

Set SapModel = Nothing

Set SapObject = Nothing

End Sub

## Release Notes

Initial release in version 22.1.0

This function supersedes SetShellLayer_1

## See Also

GetShellLayer_2


# ChangeName

## Syntax

SapObject.SapModel.PropCable.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined cable property.

NewName

The new name for the cable property.

## Remarks

This function changes the name of an existing cable property.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeCablePropName()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new cable property
ret = SapModel.PropCable.SetProp("C1", Name, 2.25)

'change name of cable property
ret = SapModel.PropCable.ChangeName("C1", "MyCable")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Count

## Syntax

SapObject.SapModel.PropCable.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

This function returns the total number of defined cable properties in the model.

## VBA Example

Sub CountCableProps()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
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

'add material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new cable property
ret = SapModel.PropCable.SetProp("C1", Name, 2.25)

'return number of defined cable properties
Count = SapModel.PropCable.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Delete

## Syntax

SapObject.SapModel.PropCable.Delete


## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing cable property.

## Remarks

The function deletes a specified cable property.

The function returns zero if the property is successfully deleted; otherwise it returns a nonzero
value. It returns an error if the specified property can not be deleted, for example, if it is assigned
to an existing object.

## VBA Example

Sub DeleteCableProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim i As Long
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

'add material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new cable properties


ret = SapModel.PropCable.SetProp("C1", Name, 2.25)
ret = SapModel.PropCable.SetProp("C2", Name, 3.25)

'delete cable property
ret = SapModel.PropCable.Delete("C1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetModifiers

## Syntax

SapObject.SapModel.PropCable.GetModifiers

## VB6 Procedure

Function GetModifiers(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing cable property.

Value

This is an array of three unitless modifiers.

```
Value(0) = Cross sectional area modifier
Value(1) = Mass modifier
Value(2) = Weight modifier
```
## Remarks

This function retrieves the modifier assignments for a cable property. The default value for all
modifiers is one.


The function returns zero if the modifier assignments are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetCablePropModifiers()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new cable property
ret = SapModel.PropCable.SetProp("C1", Name, 2.25)

'assign modifiers
ReDim Value(2)
For i = 0 To 2
Value(i) = 1
Next i
Value(1) = 2
Value(2) = 2
ret = SapModel.PropCable.SetModifiers("C1", Value)

'get modifiers
ReDim Value(2)
ret = SapModel.PropCable.GetModifiers("C1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetModifiers

# GetNameList

## Syntax

SapObject.SapModel.PropCable.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of cable property names retrieved by the program.

MyName

This is a one-dimensional array of cable property names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined cable properties in the model.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetCableNames()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
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

'add material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new cable properties
ret = SapModel.PropCable.SetProp("C1", Name, 2.25)
ret = SapModel.PropCable.SetProp("C2", Name, 3.25)

'get cable property names
ret = SapModel.PropCable.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetProp

## Syntax

SapObject.SapModel.PropCable.GetProp


## VB6 Procedure

Function GetProp(ByVal Name As String, ByRef MatProp As String, ByRef Area As Double,
ByRef Color As Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing cable property.

MatProp

The name of the material property assigned to the cable property.

Area

The cross-sectional area of the cable. [L^2 ]

Color

The display color assigned to the property.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves cable property definition data.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetCableProperty()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MatProp As String
Dim Area As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String


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

'add material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new cable property
ret = SapModel.PropCable.SetProp("C1", Name, 2.25)

'get cable property data
ret = SapModel.PropCable.GetProp("C1", MatProp, Area, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetProp

# SetModifiers

## Syntax

SapObject.SapModel.PropCable.SetModifiers

## VB6 Procedure

Function SetModifiers(ByVal Name As String, ByRef Value() As Double) As Long


## Parameters

Name

The name of an existing cable property.

Value

This is an array of 3 unitless modifiers.

```
Value(0) = Cross sectional area modifier
Value(1) = Mass modifier
Value(2) = Weight modifier
```
## Remarks

This function assigns property modifiers to a cable property. The default value for all modifiers is
one.

The function returns zero if the modifiers are successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub AssignCablePropModifiers()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)


'set new cable property
ret = SapModel.PropCable.SetProp("C1", Name, 2.25)

'assign modifiers
ReDim Value(2)
For i = 0 To 2
Value(i) = 1
Next i
Value(1) = 2
Value(2) = 2
ret = SapModel.PropCable.SetModifiers("C1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetModifiers

# SetProp

## Syntax

SapObject.SapModel.PropCable.SetProp

## VB6 Procedure

Function SetProp(ByVal Name As String, ByVal MatProp As String, ByVal Area As Double,
Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID
As String = "") As Long

## Parameters

Name

The name of an existing or new cable property. If this is an existing property, that property is
modified; otherwise, a new property is added.

MatProp


The name of the material property assigned to the cable property.

Area

The cross-sectional area of the cable. [L^2 ]

Color

The display color assigned to the property. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function defines a cable property.

The function returns zero if the property is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetCableProperty()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add material


ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new cable property
ret = SapModel.PropCable.SetProp("C1", Name, 2.25)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetProp

# ChangeName

## Syntax

SapObject.SapModel.PropFrame.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined frame section property.

NewName

The new name for the frame section property.

## Remarks

This function changes the name of an existing frame section property.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.


## VBA Example

Sub ChangeFramePropName()
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'change name of frame section property
ret = SapModel.PropFrame.ChangeName("FSEC1", "MySection")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Count

## Syntax

SapObject.SapModel.PropFrame.Count

## VB6 Procedure

Function Count(Optional ByVal PropType As eFramePropType) As Long


## Parameters

PropType

This optional value is one of the following items in the eFramePropType enumeration.

```
SECTION_I = 1
SECTION_CHANNEL = 2
SECTION_T = 3
SECTION_ANGLE = 4
SECTION_DBLANGLE = 5
SECTION_BOX = 6
SECTION_PIPE = 7
SECTION_RECTANGULAR = 8
SECTION_CIRCLE = 9
SECTION_GENERAL = 10
SECTION_DBCHANNEL = 11
SECTION_AUTO = 12
SECTION_SD = 13
SECTION_VARIABLE = 14
SECTION_JOIST = 15
SECTION_BRIDGE = 16
SECTION_COLD_C = 17
SECTION_COLD_2C = 18
SECTION_COLD_Z = 19
SECTION_COLD_L = 20
SECTION_COLD_2L = 21
SECTION_COLD_HAT = 22
SECTION_BUILTUP_I_COVERPLATE = 23
SECTION_PCC_GIRDER_I = 24
SECTION_PCC_GIRDER_U = 25
SECTION_BUILTUP_I_HYBRID = 26
SECTION_BUILTUP_U_HYBRID = 27
```
If no value is input for PropType, a count is returned for all frame section properties in the model
regardless of type.

## Remarks

This function returns the total number of defined frame section properties in the model. If desired,
counts can be returned for all frame section properties of a specified type in the model.

## VBA Example

Sub CountFrameProps()
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

'return number of defined materials of all types
Count = SapModel.PropFrame.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Builtup I Hybrid and Builitup U Hybrid added with Version 16.0.0.

## See Also

# Delete

## Syntax

SapObject.SapModel.PropFrame.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing frame section property.


## Remarks

The function deletes a specified frame section property.

The function returns zero if the frame section property is successfully deleted; otherwise it returns
a nonzero value. It returns an error if the specified frame section property can not be deleted; for
example, if it is being used by a frame object.

## VBA Example

Sub DeleteFrameProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
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

'set new frame section property
ret = SapModel.PropFrame.SetGeneral("GEN1", "A992Fy50", 24, 14, 100, 80, 80, 4, 1000,
2400, 140, 200, 150, 220, 3, 5, -1, "API example", "Default")

'get frame object names
ret = SapModel.FrameObj.GetNameList(NumberNames, MyName)

'set frame section property
For i = 1 to NumberNames
ret = SapModel.FrameObj.SetSection(MyName(i - 1), "GEN1")
Next i

'delete frame property
ret = SapModel.PropFrame.Delete("FSEC1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetAngle_1

## Syntax

SapObject.SapModel.PropFrame.GetAngle-1

## VB6 Procedure

Function GetAngle_1(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef tf As Double, ByRef tw As Double,
ByRef FilletRadius As Double, ByRef Color As Long, ByRef Notes As String, ByRef GUID As
String) As Long

## Parameters

Name

The name of an existing frame section property.

FileName

If the section property was imported from a property file; this is the name of that file. If the section
property was not imported; this item is blank.

MatProp

The name of the material property for the section.

t3

The vertical leg depth. [L]

t2

The horizontal leg width. [L]

tf

The horizontal leg thickness. [L]

tw


The vertical leg thickness. [L]

FilletRadius

The fillet radius. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for an angle-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim tf As Double
Dim tw As Double

Dim FilletRadius As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new frame section property
ret = SapModel.PropFrame.SetAngle_1("ANGLE1", "A992Fy50", 6, 4, 0.5, 0.5, 0.2)

'get frame section property data
ret = SapModel.PropFrame.GetAngle_1("ANGLE1", FileName, MatProp, t3, t2, tf, tw,
FilletRadius, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the GetAngle.

## See Also

SetAngle_1

# GetAutoSelectAluminum

## Syntax

SapObject.SapModel.PropFrame.GetAutoSelectAluminum

## VB6 Procedure

Function GetAutoSelectAluminum(ByVal Name As String, ByVal NumberItems As Long, ByRef
SectName() As String, ByRef AutoStartSection As String, ByRef Notes As String, ByRef GUID
As String) As Long

## Parameters

Name

The name of an existing auto select section list-type frame section property.

NumberItems


The number of frame section properties included in the auto select list.

SectName

This is an array of the names of the frame section properties included in the auto select list.

AutoStartSection

This is Median or the name of a frame section property in the SectName array. It is the starting
section for the auto select list.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a aluminum auto select lists.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetFramePropAutoSelectAluminum()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MyName() As String
Dim NumberItems As Long
Dim SectName() As String
Dim AutoStartSection As String
Dim Notes As String
Dim GUID As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'add aluminum material


ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_ALUMINUM, , ,
MATERIAL_ALUMINUM_SUBTYPE_6061_T6)

'create new aluminum frame section properties
ret = SapModel.PropFrame.SetISection("AI", Name , 18, 6, 0.5, 0.3, 6, 0.5)
ret = SapModel.PropFrame.SetISection("AI2", Name , 18, 6, 0.6, 0.3, 6, 0.6)
ret = SapModel.PropFrame.SetISection("AI3", Name , 18, 6, 0.7, 0.3, 6, 0.7)

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288, True, "AI", "AI")

'define new auto select list frame section property
ReDim MyName(2)
MyName(0) = "AI"
MyName(1) = "AI2"
MyName(2) = "AI3"
ret = SapModel.PropFrame.SetAutoSelectAluminum("AUTO1", 3, MyName)

'get auto select list data
ret = SapModel.PropFrame.GetAutoSelectAluminum("AUTO1", NumberItems, SectName,
AutoStartSection, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetAutoSelectAluminum

# GetAutoSelectColdFormed

## Syntax

SapObject.SapModel.PropFrame.GetAutoSelectColdFormed

## VB6 Procedure

Function GetAutoSelectColdFormed(ByVal Name As String, ByVal NumberItems As Long,
ByRef SectName() As String, ByRef AutoStartSection As String, ByRef Notes As String, ByRef
GUID As String) As Long


## Parameters

Name

The name of an existing auto select section list-type frame section property.

NumberItems

The number of frame section properties included in the auto select list.

SectName

This is an array of the names of the frame section properties included in the auto select list.

AutoStartSection

This is Median or the name of a frame section property in the SectName array. It is the starting
section for the auto select list.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed auto select lists.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetFramePropAutoSelectColdFormed()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MyName() As String
Dim NumberItems As Long
Dim SectName() As String
Dim AutoStartSection As String
Dim Notes As String
Dim GUID As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application


SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'create new cold formed frame section properties
ret = SapModel.PropFrame.SetISection("CI", Name , 18, 6, 0.5, 0.3, 6, 0.5)
ret = SapModel.PropFrame.SetISection("CI2", Name , 18, 6, 0.6, 0.3, 6, 0.6)
ret = SapModel.PropFrame.SetISection("CI3", Name , 18, 6, 0.7, 0.3, 6, 0.7)

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288, True, "CI", "CI")

'define new auto select list frame section property
ReDim MyName(2)
MyName(0) = "CI"
MyName(1) = "CI2"
MyName(2) = "CI3"
ret = SapModel.PropFrame.SetAutoSelectColdFormed("AUTO1", 3, MyName)

'get auto select list data
ret = SapModel.PropFrame.GetAutoSelectColdFormed("AUTO1", NumberItems, SectName,
AutoStartSection, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetAutoSelectColdFormed

# GetAutoSelectSteel

## Syntax


SapObject.SapModel.PropFrame.GetAutoSelectSteel

## VB6 Procedure

Function GetAutoSelectSteel(ByVal Name As String, ByVal NumberItems As Long, ByRef
SectName() As String, ByRef AutoStartSection As String, ByRef Notes As String, ByRef GUID
As String) As Long

## Parameters

Name

The name of an existing auto select section list–type frame section property.

NumberItems

The number of frame section properties included in the auto select list.

SectName

This is an array of the names of the frame section properties included in the auto select list.

AutoStartSection

This is either Median or the name of a frame section property in the SectName array. It is the
starting section for the auto select list.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a steel auto select lists.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetFramePropAutoSelectSteel()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyName() As String
Dim NumberItems As Long
Dim SectName() As String
Dim AutoStartSection As String


Dim Notes As String
Dim GUID As String

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

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC1", "A992Fy50", 24, 8, 0.5, 0.3, 8, 0.5)

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC2", "A992Fy50", 20, 8, 0.5, 0.3, 8, 0.5)

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC3", "A992Fy50", 16, 8, 0.5, 0.3, 8, 0.5)

'set new auto select list frame section property
ReDim MyName(2)
MyName(0) = "ISEC1"
MyName(1) = "ISEC2"
MyName(2) = "ISEC3"
ret = SapModel.PropFrame.SetAutoSelectSteel("AUTO1", 3, MyName, "ISEC2")

'get auto select list data
ret = SapModel.PropFrame.GetAutoSelectSteel("AUTO1", NumberItems, SectName,
AutoStartSection, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetAutoSelectSteel


# GetChannel_2

## Syntax

SapObject.SapModel.PropFrame.GetChannel_2

## VB6 Procedure

Function GetChannel_2(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef tf As Double, ByRef tw As Double,
ByRef FilletRadius As Double, ByRef MirrorAbout2 As Boolean, ByRef Color As Long, ByRef
Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The flange width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

FilletRadius

The fillet radius. [L]

MirrorAbout2 (not applicable)

Indicates whether the section is mirrored about the local 2-axis.


Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a channel-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropChannel()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim tf As Double
Dim tw As Double

```
Dim FilletRadius As Double
```
```
Dim MirrorAbout2 As Boolean
```
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new frame section property
ret = SapModel.PropFrame.SetChannel_2("CHN1", "A992Fy50", 24, 6, 0.5, 0.3, 0.2, False)

'get frame section property data
ret = SapModel.PropFrame.GetChannel_2("CHN1", FileName, MatProp, t3, t2, tf, tw,
FiletRadius, MirrorAbout2, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the GetChannel

## See Also

SetChannel_2

# GetCircle

## Syntax

SapObject.SapModel.PropFrame.GetCircle

## VB6 Procedure

Function GetCircle(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef Color As Long, ByRef Notes As String, ByRef GUID As
String) As Long

## Parameters

Name

The name of an existing circular frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp


The name of the material property for the section.

t3

The section diameter. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a circular frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropCircle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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


'set new frame section property
ret = SapModel.PropFrame.SetCircle("C1", "4000Psi", 20)

'get frame section property data
ret = SapModel.PropFrame.GetCircle("C1", FileName, MatProp, t3, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetCircle

SetRebarBeam

SetRebarColumn

GetRebarBeam

GetRebarColumn

# GetColdBox

## Syntax

SapObject.SapModel.PropFrame.GetColdBox

## VB6 Procedure

Function GetColdBox(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef Thickness As Double, ByRef Radius As
Double, ByRef Color As Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing cold formed box frame section property.

FileName


If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section top flange width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed box frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropColdBox()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double


Dim Thickness As Double
Dim Radius As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdBox("CB1", Name, 10, 3.2, 0.08, 0.3)

'get frame section property data
ret = SapModel.PropFrame.GetColdBox("CB1", FileName, MatProp, t3, Thickness , Radius,
Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.

## See Also

SetColdBox


# GetColdC

## Syntax

SapObject.SapModel.PropFrame.GetColdC

## VB6 Procedure

Function GetColdC(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef Thickness As Double, ByRef Radius As
Double, ByRef LipDepth As Double, ByRef Color As Long, ByRef Notes As String, ByRef
GUID As String) As Long

## Parameters

Name

The name of an existing cold formed C-type frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

LipDepth

The lip depth, if any. [L]

Color

The display color assigned to the section.


Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed C-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropColdC()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim Thickness As Double
Dim Radius As Double
Dim LipDepth As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)


'set new frame section property
ret = SapModel.PropFrame.SetColdC("CC1", Name, 10, 3.2, 0.08, 0.3, 0.6)

'get frame section property data
ret = SapModel.PropFrame.GetColdC("CC1", FileName, MatProp, t3, t2, Thickness , Radius,
LipDepth, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetColdC

# GetColdHat

## Syntax

SapObject.SapModel.PropFrame.GetColdHat

## VB6 Procedure

Function GetColdHat(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef Thickness As Double, ByRef Radius As
Double, ByRef LipDepth As Double, ByRef Color As Long, ByRef Notes As String, ByRef
GUID As String) As Long

## Parameters

Name

The name of an existing cold formed hat-type frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.


t3

The section depth. [L]

t2

The section width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

LipDepth

The lip depth, if any. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed hat-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropColdHat()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim Thickness As Double
Dim Radius As Double


Dim LipDepth As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdHat("CH1", Name, 10, 3.2, 0.08, 0.3, 0.6)

'get frame section property data
ret = SapModel.PropFrame.GetColdHat("CH1", FileName, MatProp, t3, t2, Thickness ,
Radius, LipDepth, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetColdHat

# GetColdI

## Syntax


SapObject.SapModel.PropFrame.GetColdI

## VB6 Procedure

Function GetColdI(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef t2b As Double, ByRef Thickness As
Double, ByRef Radius As Double, ByRef Color As Long, ByRef Notes As String, ByRef GUID
As String) As Long

## Parameters

Name

The name of an existing cold formed I-shape frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section top flange width. [L]

t2b

The section bottom flange width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID


The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed I-shape frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropColdI()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double

Dim t2b As Double
Dim Thickness As Double
Dim Radius As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdI("CI1", Name, 10, 3.2, 2.5, 0.08, 0.3)

'get frame section property data


ret = SapModel.PropFrame.GetColdI("CI1", FileName, MatProp, t3, t2, t2b, Thickness ,
Radius, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.

## See Also

SetColdI

# GetColdL

## Syntax

SapObject.SapModel.PropFrame.GetColdL

## VB6 Procedure

Function GetColdL(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef Thickness As Double, ByRef Radius As Double, ByRef
LipDepth As Double, ByRef Color As Long, ByRef Notes As String, ByRef GUID As String) As
Long

## Parameters

Name

The name of an existing cold formed Angle frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3


The section depth. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

LipDepth

The lip depth, if any. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed Angle frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropColdL()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim Thickness As Double
Dim Radius As Double
Dim LipDepth As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdL("CL1", Name, 4.0, 0.08, 0.3, 0.6)

'get frame section property data
ret = SapModel.PropFrame.GetColdL("CL1", FileName, MatProp, t3, Thickness , Radius,
LipDepth, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.

## See Also

SetColdL

# GetColdPipe

## Syntax

SapObject.SapModel.PropFrame.GetColdPipe

## VB6 Procedure


Function GetColdPipe(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef Thickness As Double, ByRef Color As Long, ByRef Notes As
String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing cold formed pipe frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

Thickness

The section thickness. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed pipe frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropColdPipe()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim Name As String
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim Thickness As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdPipe("CP1", Name, 8.0, 0.08)

'get frame section property data
ret = SapModel.PropFrame.GetColdPipe("CP1", FileName, MatProp, t3, Thickness, Color,
Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.

## See Also

SetColdPipe


# GetColdT

## Syntax

SapObject.SapModel.PropFrame.GetColdT

## VB6 Procedure

Function GetColdT(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef Thickness As Double, ByRef Radius As
Double, ByRef Color As Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing cold formed Tee frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section top flange width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID


The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed Tee frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropColdT()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim Thickness As Double
Dim Radius As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdT("CT1", Name, 10, 3.2, 2.5, 0.08, 0.3)

'get frame section property data
ret = SapModel.PropFrame.GetColdT("CT1", FileName, MatProp, t3, t2, Thickness , Radius,


Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.

## See Also

SetColdT

# GetColdZ

## Syntax

SapObject.SapModel.PropFrame.GetColdZ

## VB6 Procedure

Function GetColdZ(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef Thickness As Double, ByRef Radius As
Double, ByRef LipDepth As Double, ByRef LipAngle As Double, ByRef Color As Long, ByRef
Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing cold formed Z-type frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]


t2

The section width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

LipDepth

The lip depth, if any. [L]

LipAngle

The lip angle measured from horizontal (0 <= LipAngle <= 90). [deg]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a cold formed Z-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropColdZ()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim Thickness As Double
Dim Radius As Double


Dim LipDepth As Double
Dim LipAngle As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdZ("CZ1", Name, 10, 3.2, 0.08, 0.3, 0.6, 60)

'get frame section property data
ret = SapModel.PropFrame.GetColdZ("CZ1", FileName, MatProp, t3, t2, Thickness , Radius,
LipDepth, LipAngle, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetColdZ


# GetCoverPlatedI

## Syntax

SapObject.SapModel.PropFrame.GetCoverPlatedI

## VB6 Procedure

Function GetCoverPlatedI(ByVal Name As String, ByRef SectName As String, ByRef
FyTopFlange As Double, ByRef FyWeb As Double, ByRef FyBotFlange As Double, ByRef tc As
Double, ByRef bc As Double, ByRef MatPropTop As String, ByRef tcb As Double, ByRef bcb
As Double, ByRef MatPropBot As String, ByRef Color As Long, ByRef Notes As String, ByRef
GUID As String) As Long

## Parameters

Name

The name of an existing frame section property.

SectName

The name of an existing I-type frame section property that is used for the I-section portion of the
coverplated I section.

FyTopFlange

The yield strength of the top flange of the I-section. [F/L^2 ]

If this item is 0, the yield strength of the I-section specified by the SectName item is used.

FyWeb

The yield strength of the web of the I-section. [F/L^2 ]

If this item is 0, the yield strength of the I-section specified by the SectName item is used.

FyBotFlange

The yield strength of the bottom flange of the I-section. [F/L^2 ]

If this item is 0, the yield strength of the I-section specified by the SectName item is used.

tc

The thickness of the top cover plate. [L]

If the tc or the bc item is less than or equal to 0, no top cover plate exists.

bc

The width of the top cover plate. [L]


If the tc or the bc item is less than or equal to 0, no top cover plate exists.

MatPropTop

The name of the material property for the top cover plate.

This item applies only if both the tc and the bc items are greater than 0.

tcb

The thickness of the bottom cover plate. [L]

If the tcb or the bcb item is less than or equal to 0, no bottom cover plate exists.

bcb

The width of the bottom cover plate. [L]

If the tcb or the bcb item is less than or equal to 0, no bottom cover plate exists.

MatPropBot

The name of the material property for the bottom cover plate.

This item applies only if both the tcb and the bcb items are greater than 0.

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a tube-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropCoverPlatedI()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim SectName As String
Dim FyTopFlange As Double


Dim FyWeb As Double
Dim FyBotFlange As Double
Dim tc As Double
Dim bc As Double
Dim MatPropTop As String
Dim tcb As Double
Dim bcb As Double
Dim MatPropBot As String
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC", "A992Fy50", 24, 8, 0.5, 0.3, 8, 0.5)

'set new cover plated I-type frame section property
ret = SapModel.PropFrame.SetCoverPlatedI("CPI1", "ISEC", 0, 36, 0, 0.75, 14, "A992Fy50",
0.5, 6, "A992Fy50")

'get frame section property data for cover plated I
ret = SapModel.PropFrame.GetCoverPlatedI("CPI1", SectName, FyTopFlange, FyWeb,
FyBotFlange, tc, bc, MatPropTop, tcb, bcb, MatPropBot, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetCoverPlatedI


# GetDblAngle_2

## Syntax

SapObject.SapModel.PropFrame.GetDblAngle_2

## VB6 Procedure

Function GetDblAngle_2(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef tf As Double, ByRef tw As Double,
ByRef dis As Double, ByRef FilletRadius As Double, ByRef MirrorAbout3 As Boolean, ByRef
Color As Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The vertical leg depth. [L]

t2

The total width of the section, that is, the sum of the widths of each horizontal leg plus the back-to
-back distance. [L]

tf

The horizontal leg thickness. [L]

tw

The vertical leg thickness. [L]

dis

The back-to-back distance between the angles. [L]

FilletRadius

The fillet radius. [L]


MirrorAbout3 (not applicable)

Indicates whether the section is mirrored about the local 3-axis.

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a double angle-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropDblAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim tf As Double
Dim tw As Double
Dim dis As Double

```
Dim FilletRadius As Double
```
```
Dim MirrorAbout3 As Boolean
```
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new frame section property
ret = SapModel.PropFrame.SetDblAngle_2("DBANG1", "A992Fy50", 6, 9, 0.5, 0.5, 1, 0.2,
False)

'get frame section property data
ret = SapModel.PropFrame.GetDblAngle_2("DBANG1", FileName, MatProp, t3, t2, tf, tw,
dis, FilletRadius, MirrorAbout3, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the GetDblAngle.

## See Also

SetDblAngle_2

# GetDblChannel_1

## Syntax

SapObject.SapModel.PropFrame.GetDblChannel_1

## VB6 Procedure

Function GetDblChannel_1(ByVal Name As String, ByRef FileName As String, ByRef MatProp
As String, ByRef t3 As Double, ByRef t2 As Double, ByRef tf As Double, ByRef tw As Double,
ByRef dis As Double, ByRef FilletRadius As Double, ByRef Color As Long, ByRef Notes As
String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing frame section property.


FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The total width of the section, that is, the sum of the widths of each flange plus the back-to-back
distance. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

dis

The back-to-back distance between the channels. [L]

FilletRadius

The fillet radius. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a double channel-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.


## VBA Example

Sub GetFramePropDblChannel()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim tf As Double
Dim tw As Double
Dim dis As Double

Dim FilletRadius As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new frame section property
ret = SapModel.PropFrame.SetDblChannel_1("DBCHN1", "A992Fy50", 12, 6.5, 0.5, 0.3, 0.5,
0.2)

'get frame section property data
ret = SapModel.PropFrame.GetDblChannel_1("DBCHN1", FileName, MatProp, t3, t2, tf, tw,
dis, FilletRadius, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the GetDblChannel.


## See Also

SetDblChannel_1

# GetGeneral

## Syntax

SapObject.SapModel.PropFrame.GetGeneral

## VB6 Procedure

Function GetGeneral(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef Area As Double, ByRef As2 As Double,
ByRef As3 As Double, ByRef Torsion As Double, ByRef I22 As Double, ByRef I33 As Double,
ByRef S22 As Double, ByRef S33 As Double, ByRef Z22 As Double, ByRef Z33 As Double,
ByRef R22 As Double, ByRef R33 As Double, ByRef Color As Long, ByRef Notes As String,
ByRef GUID As String) As Long

## Parameters

Name

The name of an existing frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]

Area

The cross-sectional area. [L^2 ]

As2

The shear area for forces in the section local 2-axis direction. [L^2 ]

As3


The shear area for forces in the section local 3-axis direction. [L^2 ]

Torsion

The torsional constant. [L^4 ]

I22

The moment of inertia for bending about the local 2 axis. [L^4 ]

I33

The moment of inertia for bending about the local 3 axis. [L^4 ]

S22

The section modulus for bending about the local 2 axis. [L^3 ]

S33

The section modulus for bending about the local 3 axis. [L^3 ]

Z22

The plastic modulus for bending about the local 2 axis. [L^3 ]

Z33

The plastic modulus for bending about the local 3 axis. [L^3 ]

R22

The radius of gyration about the local 2 axis. [L]

R33

The radius of gyration about the local 3 axis. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a general frame section.


The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropGeneral()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim Area As Double
Dim as2 As Double
Dim as3 As Double
Dim Torsion As Double
Dim I22 As Double
Dim I33 As Double
Dim S22 As Double
Dim S33 As Double
Dim Z22 As Double
Dim Z33 As Double
Dim R22 As Double
Dim R33 As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new frame section property
ret = SapModel.PropFrame.SetGeneral("GEN1", "A992Fy50", 24, 14, 100, 80, 80, 4, 1000,
2400, 140, 200, 150, 220, 3, 5, -1, "API example", "Default")

'get frame section property data
ret = SapModel.PropFrame.GetGeneral("GEN1", FileName, MatProp, t3, t2, Area, As2, As3,
Torsion, I22, I33, S22, S33, Z22, Z33, R22, R33, Color, Notes, GUID)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetGeneral

# GetHybridISection

## Syntax

SapObject.SapModel.PropFrame.GetHybridISection

## VB6 Procedure

Function GetHybridISection(ByVal name As String, ByRef MatPropTopFlange As String, ByRef
MatPropWeb As String, ByRef MatPropBotFlange As String, ByRef t3 As Double, ByRef t2 As
Double, ByRef TF As Double, ByRef TW As Double, ByRef t2b As Double, ByRef tfb As
Double,

ByRef color As Long, ByRef notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing frame section property.

MatPropTopFlange

The name of the material property for the top flange.

MatPropWeb

The name of the material property for the web.

MatPropBotFlange

The name of the material property for the bottom flange.

t3


The height of the section. [L]

t2

The width of the top flange. [L]

TF

The thickness of the top flange. [L]

TW

The thickness of the web. [L]

t2b

The width of the bottom flange. [L]

tfb

The thickness of the bottom flange. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a steel hybrid I frame section.

The function returns zero if the section property data is successfully retrieved, otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropHybridISection()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatPropTopFlange As String
Dim MatPropWeb As String
Dim MatPropBotFlange As String
Dim t3 As Double
Dim t2 As Double
Dim TF As Double


Dim TW As Double
Dim t2b As Double
Dim tfb As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new Hybrid I-type frame section property
ret = SapModel.PropFrame.SetHybridISection("HybridI", "A992Fy50", "A992Fy50",
"A992Fy50", 24, 8, 0.5, 0.3, 8, 0.5)

'get frame section property data for cover plated I
ret = SapModel.PropFrame.GetHybridISection("HybridI", MatPropTopFlange, MatPropWeb,
MatPropBotFlange, t3, t2, TF, TW, t2b, tfb, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# GetHybridUSection

## Syntax

SapObject.SapModel.PropFrame.GetHybridUSection


## VB6 Procedure

Function GetHybridUSection(ByVal name As String, ByRef WebMaterial As String, ByRef
TopFlangeMaterial As String, ByRef BotFlangeMaterial As String, ByRef T() As Double, ByRef
color As Long, ByRef notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing frame section property.

WebMaterial

The name of the material property for the webs.

TopFlangeMaterial

The name of the material property for the top flanges.

BotFlangeMaterial

The name of the material property for the bottom flange.

T()

The dimension array of the section:

(0) D1 = Web Depth (vertical, inside to inside of flanges). [L]

(1) B1 = Web Distance at Top (CL to CL). [L]

(2) B2 = Bottom Flange Width. [L]

(3) B3 = Top Flange Width (per each). [L]

(4) B4 = Bottom Flange Lip (Web CL to flange edge, may be zero). [L]

(5) tw = Web Thickness. [L]

(6) tf = Top Flange Thickness. [L]

(7) tfb = Bottom Flange Thickness. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.


### GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a steel hybrid U frame section.

The function returns zero if the section property data is successfully retrieved, otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropHybridUSection()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim WebMaterial As String
Dim TopFlangeMaterial As String
Dim BotFlangeMaterial As String
Dim T() As Double
Dim MyT() As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new Hybrid U-type frame section property
Redim T(7)
T(0) = 48
T(1) = 64
T(2) = 48
T(3) = 15
T(4) = 1.5
T(5) = 1
T(6) = 2
T(7) = 2


ret = SapModel.PropFrame.SetHybridUSection("HybridU", "A992Fy50", "A992Fy50",
"A992Fy50", T())

'get frame section property data for cover plated I
ret = SapModel.PropFrame.GetHybridUSection("HybridI", WebMaterial, TopFlangeMaterial,
BotFlangeMaterial, MyT(), Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# GetISection_1

## Syntax

SapObject.SapModel.PropFrame.GetISection_1

## VB6 Procedure

Function GetISection_1(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef tf As Double, ByRef tw As Double,
ByRef t2b As Double, ByRef tfb As Double, ByRef FilletRadius As Double, ByRef Color As
Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing I-type frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3


The section depth. [L]

t2

The top flange width. [L]

tf

The top flange thickness. [L]

tw

The web thickness. [L]

t2b

The bottom flange width. [L]

tfb

The bottom flange thickness. [L]

FilletRadius

The fillet radius. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for an I-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropISection()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String


Dim t3 As Double
Dim t2 As Double
Dim tf As Double
Dim tw As Double
Dim t2b As Double
Dim tfb As Double

```
Dim FilletRadius As Double
```
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'get frame section property data
ret = SapModel.PropFrame.GetISection_1("FSEC1", FileName, MatProp, t3, t2, tf, tw, t2b,
tfb, FilletRadius, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the GetISection.

## See Also

SetISection_1

# GetModifiers

## Syntax


SapObject.SapModel.PropFrame.GetModifiers

## VB6 Procedure

Function GetModifiers(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing frame section property.

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

This function retrieves the modifier assignments for a frame section property. The default value
for all modifiers is one.

The function returns zero if the modifier assignments are successfully retrieved; otherwise it
returns a nonzero value.

## VBA Example

Sub GetFramePropModifiers()
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

'assign modifiers
ReDim Value(7)
For i = 0 To 7
Value(i) = 1
Next i
Value(5) = 100
ret = SapModel.PropFrame.SetModifiers("FSEC1", Value)

'get modifiers
ReDim Value(7)
ret = SapModel.PropFrame.GetModifiers("FSEC1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetModifiers

# GetNameInPropFile

## Syntax

SapObject.SapModel.PropFrame.GetNameInPropFile

## VB6 Procedure

Function GetNameInPropFile(ByVal Name As String, ByRef NameInFile As String, ByRef
FileName As String, ByRef MatProp As String, ByRef PropType As eFramePropType) As Long

## Parameters

Name


The name of an existing frame section property.

NameInFile

The name of the specified frame section property in the frame section property file.

FileName

The name of the frame section property file from which the specified frame section property was
obtained.

MatProp

The name of the material property for the section.

PropType

This is one of the following items in the eFramePropType enumeration.

```
SECTION_I = 1
```
```
SECTION_CHANNEL = 2
```
```
SECTION_T = 3
```
```
SECTION_ANGLE = 4
```
```
SECTION_DBLANGLE = 5
```
```
SECTION_BOX = 6
```
```
SECTION_PIPE = 7
```
```
SECTION_RECTANGULAR = 8
```
```
SECTION_CIRCLE = 9
```
```
SECTION_GENERAL = 10
```
```
SECTION_DBCHANNEL = 11
```
```
SECTION_AUTO = 12
```
```
SECTION_SD = 13
```
```
SECTION_VARIABLE = 14
```
```
SECTION_JOIST = 15
```
```
SECTION_BRIDGE = 16
```
```
SECTION_COLD_C = 17
```
```
SECTION_COLD_2C = 18
```
```
SECTION_COLD_Z = 19
```

### SECTION_COLD_L = 20

### SECTION_COLD_2L = 21

### SECTION_COLD_HAT = 22

### SECTION_BUILTUP_I_COVERPLATE = 23

### SECTION_PCC_GIRDER_I = 24

### SECTION_PCC_GIRDER_U = 25

## Remarks

This function retrieves the names of the section property file from which an imported frame
section originated, and it also retrieves the section name used in the property file.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

If the specified frame section property was not imported, blank strings are returned for
NameInFile and FileName.

## VBA Example

Sub GetFramePropNameInFile()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NameInFile As String
Dim FileName As String
Dim MatProp As String
Dim PropType As eFramePropType

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

'import new frame section property
ret = SapModel.PropFrame.ImportProp("MyFrame", "A992Fy50", "Sections8.pro",
"W18X35")


'get frame property name in file
ret = SapModel.PropFrame.GetNameInPropFile("MyFrame", NameInFile, FileName,
MatProp, PropType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

# GetNameList

## Syntax

SapObject.SapModel.PropFrame.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String, Optional
ByVal PropType As eFramePropType) As Long

## Parameters

NumberNames

The number of frame section property names retrieved by the program.

MyName

This is a one-dimensional array of frame section property names. The MyName array is created as
a dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

PropType

This optional value is one of the following items in the eFramePropType enumeration.

```
SECTION_I = 1
```

### SECTION_CHANNEL = 2

### SECTION_T = 3

### SECTION_ANGLE = 4

### SECTION_DBLANGLE = 5

### SECTION_BOX = 6

### SECTION_PIPE = 7

### SECTION_RECTANGULAR = 8

### SECTION_CIRCLE = 9

### SECTION_GENERAL = 10

### SECTION_DBCHANNEL = 11

### SECTION_AUTO = 12

### SECTION_SD = 13

### SECTION_VARIABLE = 14

### SECTION_JOIST = 15

### SECTION_BRIDGE = 16

### SECTION_COLD_C = 17

### SECTION_COLD_2C = 18

### SECTION_COLD_Z = 19

### SECTION_COLD_L = 20

### SECTION_COLD_2L = 21

### SECTION_COLD_HAT = 22

### SECTION_BUILTUP_I_COVERPLATE = 23

### SECTION_PCC_GIRDER_I = 24

### SECTION_PCC_GIRDER_U = 25

### SECTION_BUILTUP_I_HYBRID = 26

### SECTION_BUILTUP_U_HYBRID = 27

If no value is input for PropType, names are returned for all frame section properties in the model
regardless of type.

## Remarks

This function retrieves the names of all defined frame section properties of the specified type.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetFramePropNames()
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

'get frame section property names
ret = SapModel.PropFrame.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Builtup I Hybrid and Builitup U Hybrid added with Version 15.0.0.

## See Also

# GetNonPrismatic

## Syntax

SapObject.SapModel.PropFrame.GetNonPrismatic

## VB6 Procedure

Function GetNonPrismatic(ByVal Name As String, ByRef NumberItems As Long, ByRef
StartSec() As String, ByRef EndSec() As String, ByRef MyLength() As Double, ByRef MyType()
As Long, ByRef EI33() As Long, ByRef EI22() As Long, ByRef Color As Long, ByRef Notes As
String, ByRef GUID As String) As Long

## Parameters

NumberItems

The number of segments assigned to the nonprismatic section.

StartSec

This is an array of the names of the frame section properties at the start of each segment.


EndSec

This is an array of the names of the frame section properties at the end of each segment.

MyLength

This is an array that includes the length of each segment. The length may be variable or absolute
as indicated by the MyType item. [L] when length is absolute

MyType

This is an array of either 1 or 2, indicating the length type for each segment.

```
1 = Variable (relative length)
2 = Absolute
```
EI33, EI22

This is an array of either 1, 2 or 3, indicating the variation type for EI33 and EI22 in each
segment.

```
1 = Linear
2 = Parabolic
3 = Cubic
```
Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for nonprismatic (variable) sections.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetFramePropNonPrismatic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim StartSec() As String
Dim EndSec() As String


Dim MyLength() As Double
Dim MyType() As Long
Dim EI33() As Long
Dim EI22() As Long
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC1", "A992Fy50", 24, 8, 0.5, 0.3, 8, 0.5)

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC2", "A992Fy50", 20, 8, 0.5, 0.3, 8, 0.5)

'set new nonprismatic frame section property
ReDim StartSec(2)
ReDim EndSec(2)
ReDim MyLength(2)
ReDim MyType(2)
ReDim EI33(2)
ReDim EI22(2)
StartSec(0) = "ISEC2"
EndSec(0) = "ISEC1"
MyLength(0) = 60
MyType(0) = 2
EI33(0)= 2
EI22(0)= 1

StartSec(1) = "ISEC1"
EndSec(1) = "ISEC1"
MyLength(1) = 1
MyType(1) = 1
EI33(1)= 2
EI22(1)= 1

StartSec(2) = "ISEC1"
EndSec(2) = "ISEC2"
MyLength(2) = 60


MyType(2) = 2
EI33(2)= 2
EI22(2)= 1

ret = SapModel.PropFrame.SetNonPrismatic("NP1", 3, StartSec, EndSec, MyLength,
MyType, EI33, EI22)

'clear arrays
ReDim StartSec(0)
ReDim EndSec(0)
ReDim MyLength(0)
ReDim MyType(0)
ReDim EI33(0)
ReDim EI22(0)

'get nonprismatic section data
ret = SapModel.PropFrame.GetNonPrismatic("NP1", NumberItems, StartSec, EndSec,
MyLength, MyType, EI33, EI22, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetNonPrismatic

# GetPipe

## Syntax

SapObject.SapModel.PropFrame.GetPipe

## VB6 Procedure

Function GetPipe(ByVal Name As String, ByRef FileName As String, ByRef MatProp As String,
ByRef t3 As Double, ByRef tw As Double, ByRef Color As Long, ByRef Notes As String, ByRef
GUID As String) As Long

## Parameters

Name


The name of an existing frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The outside diameter. [L]

tw

The wall thickness. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a pipe-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropPipe()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim tw As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String


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

'set new frame section property
ret = SapModel.PropFrame.SetPipe("PIPE1", "A992Fy50", 8, 0.375)

'get frame section property data
ret = SapModel.PropFrame.GetPipe("PIPE1", FileName, MatProp, t3, tw, Color, Notes,
GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetPipe

# GetPrecastI_1

## Syntax

SapObject.SapModel.PropFrame.GetPrecastI_1

## VB6 Procedure

Function GetPrecastI_1(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef b() As Double, ByRef d() As Double, ByRef t() As Double, ByRef c As Double,
ByRef Color As Long, ByRef Notes As String, ByRef GUID As String) As Long


## Parameters

Name

The name of an existing precast concrete I girder frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

b

This is an array, dimensioned to 3, containing the horizontal section dimensions. [L]

```
b(0) = B1 (> 0)
b(1) = B2 (> 0)
b(2) = B3 (>= 0)
b(3) = B4 (>= 0)
```
Section dimensions B1 through B4 are defined on the precast concrete I girder definition form.

d

This is an array, dimensioned to 6, containing the vertical section dimensions. [L]

```
d(0) = D1 (> 0)
d(1) = D2 (> 0)
d(2) = D3 (>= 0)
d(3) = D4 (>= 0)
d(4) = D5 (> 0)
d(5) = D6 (>= 0)
d(6) = D7 (>=0)
```
Section dimensions D1 through D7 are defined on the precast concrete I girder definition form.

t

This is an array, dimensioned to 1, containing the web thickness dimensions. [L]

```
T(0) = T1 (> 0)
```
```
T(1) = T2 (> 0)
```
Section dimensions T1 and T2 are defined on the precast I girder definition form.

c

The bottom flange chamfer dimension, denoted as C1 on the precast concrete I girder definition
form.


Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a precast concrete I girder frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropPrecastI_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim bb() As Double
Dim dd() As Double

Dim tt() As Double
Dim b() As Double
Dim d() As Double

Dim t() As Double

Dim cc As Double

Dim c As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new frame section property
ReDim bb(3)
ReDim dd(6)

ReDim tt(1)
bb(0) = 12
bb(1) = 16
bb(2) = 0
bb(3) = 0
dd(0) = 28
dd(1) = 4
dd(2) = 3
dd(3) = 0
dd(4) = 5
dd(5) = 5

dd(6) = 0

tt(0) = 6

tt(1) = 6

cc = 0
ret = SapModel.PropFrame.SetPrecastI_1("PC1", "4000Psi", bb, dd, tt, cc)

'get frame section property data
ret = SapModel.PropFrame.GetPrecastI_1("PC1", FileName, MatProp, b, d, t, c, Color, Notes,
GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

This function supersedes GetPrecast1.

## See Also

SetPrecastI_1


# GetPrecastU

## Syntax

SapObject.SapModel.PropFrame.GetPrecastU

## VB6 Procedure

Function GetPrecastU(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef b() As Double, ByRef d() As Double, ByRef Color As Long, ByRef Notes As
String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing precast concrete U girder frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

b

This is an array, dimensioned to 5, containing the horizontal section dimensions. [L]

```
b(0) = B1 (> 0)
b(1) = B2 (> 0)
b(2) = B3 (> 0)
b(3) = B4 (>= 0)
b(4) = B5 (>= 0)
b(5) = B6 (>= 0)
```
Section dimensions B1 through B6 are defined on the precast concrete U girder definition form.

d

This is an array, dimensioned to 6, containing the vertical section dimensions. [L]

```
d(0) = D1 (> 0)
d(1) = D2 (> 0)
d(2) = D3 (>= 0)
d(3) = D4 (>= 0)
d(4) = D5 (>= 0)
d(5) = D6 (>= 0)
d(6) = D7 (>= 0)
```

Section dimensions D1 through D7 are defined on the precast concrete U girder definition form.

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a precast concrete U girder frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropPrecastU()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim bb() As Double
Dim dd() As Double
Dim b() As Double
Dim d() As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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


'set present units to kN-mm
ret = SapModel.SetPresentUnits(kN_mm_C)

'set new frame section property
ReDim bb(5)
ReDim dd(6)
bb(0) = 2350
bb(1) = 1500
bb(2) = 200
bb(3) = 75
bb(4) = 143.8447
bb(5) = 0
dd(0) = 1700
dd(1) = 175
dd(2) = 75
dd(3) = 0
dd(4) = 0
dd(5) = 125
dd(6) = 175
ret = SapModel.PropFrame.SetPrecastU("PC1", "4000Psi", bb, dd)

'get frame section property data
ret = SapModel.PropFrame.GetPrecastU("PC1", FileName, MatProp, b, d, Color, Notes,
GUID)

'set present units to kip-in
ret = SapModel.SetPresentUnits(kip_in_F)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetPrecastU

# GetPropFileNameList

## Syntax

SapObject.SapModel.PropFrame.GetPropFileNameList


## VB6 Procedure

Function GetPropFileNameList(ByVal FileName As String, ByRef NumberNames As Long,
ByRef MyName() As String, ByRef MyPropType() As eFramePropType, Optional ByVal
PropType As eFramePropType) As Long

## Parameters

FileName

The name of the frame section property file from which to get the name list.

In most cases, inputting only the name of the property file (e.g. Sections8.pro) is required, and the
program will be able to find it. In some cases, inputting the full path to the property file may be
necessary.

NumberNames

The number of frame section property names retrieved by the program.

MyName

This is an array the includes the property names obtained from the frame section property file.

MyType

This is an array the includes the property type for each property obtained from the frame section
property file. See the PropType item below for a list of the possible property types.

PropType

This optional value is one of the following items in the eFramePropType enumeration.

```
SECTION_I = 1
SECTION_CHANNEL = 2
SECTION_T = 3
SECTION_ANGLE = 4
SECTION_DBLANGLE = 5
SECTION_BOX = 6
SECTION_PIPE = 7
SECTION_RECTANGULAR = 8
SECTION_CIRCLE = 9
SECTION_GENERAL = 10
SECTION_DBCHANNEL = 11
SECTION_AUTO = 12
SECTION_SD = 13
SECTION_VARIABLE = 14
SECTION_JOIST = 15
SECTION_BRIDGE = 16
SECTION_COLD_C = 17
SECTION_COLD_2C = 18
SECTION_COLD_Z = 19
SECTION_COLD_L = 20
```

### SECTION_COLD_2L = 21

### SECTION_COLD_HAT = 22

### SECTION_BUILTUP_I_COVERPLATE = 23

### SECTION_PCC_GIRDER_I = 24

### SECTION_PCC_GIRDER_U = 25

### SECTION_BUILTUP_I_HYBRID = 26

### SECTION_BUILTUP_U_HYBRID = 27

If no value is input for PropType, names are returned for all frame section properties in the
specified file regardless of type.

## Remarks

This function retrieves the names of all defined frame section properties of a specified type in a
specified frame section property file.

The function returns zero if the names are successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetFramePropNamesFromFile()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberNames As Long
Dim MyName() As String
Dim MyType() As eFramePropType

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

'get frame section property names
ret = SapModel.PropFrame.GetPropFileNameList("Sections8.pro", NumberNames, MyName,
MyType, SECTION_I)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

Builtup I Hybrid and Builitup U Hybrid added with Version 15.0.0.

## See Also

ImportProp

# GetRebarBeam

## Syntax

SapObject.SapModel.PropFrame.GetRebarBeam

## VB6 Procedure

Function GetRebarBeam(ByVal Name As String, ByRef MatPropLong As String, ByRef
MatPropConfine As String, ByRef CoverTop As Double, ByRef CoverBot As Double, ByRef
TopLeftArea As Double, ByRef TopRightArea As Double, ByRef BotLeftArea As Double, ByRef
BotRightArea As Double) As Long

## Parameters

Name

The name of an existing frame section property.

MatPropLong

The name of the rebar material property for the longitudinal rebar.

MatPropConfine

The name of the rebar material property for the confinement rebar.

CoverTop

The distance from the top of the beam to the centroid of the top longitudinal reinforcement. [L]

CoverBot

The distance from the bottom of the beam to the centroid of the bottom longitudinal
reinforcement. [L]


TopLeftArea

The total area of longitudinal reinforcement at the top left end of the beam. [L^2 ]

TopRightArea

The total area of longitudinal reinforcement at the top right end of the beam. [L^2 ]

BotLeftArea

The total area of longitudinal reinforcement at the bottom left end of the beam. [L^2 ]

BotRightArea

The total area of longitudinal reinforcement at the bottom right end of the beam. [L^2 ]

## Remarks

This function retrieves beam rebar data for frame sections.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

This function applies only to the following section types. Calling this function for any other type
of frame section property returns an error.

```
SECTION_T = 3
SECTION_ANGLE = 4
SECTION_RECTANGULAR = 8
SECTION_CIRCLE = 9
```
The material assigned to the specified frame section property must be concrete or this function
returns an error.

## VBA Example

Sub GetBeamRebar()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim RebarName As String
Dim MatPropLong As String
Dim MatPropConfine As String
Dim CoverTop As Double
Dim CoverBot As Double
Dim TopLeftArea As Double
Dim TopRightArea As Double
Dim BotLeftArea As Double
Dim BotRightArea As Double

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

'set new frame section property
ret = SapModel.PropFrame.SetRectangle("R1", "4000Psi", 20, 12)

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(RebarName, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'set beam rebar data
ret = SapModel.PropFrame.SetRebarBeam("R1", RebarName, RebarName, 3.5, 3, 4.1, 4.2,
4.3, 4.4)

'get beam rebar data
ret = SapModel.PropFrame.GetRebarBeam("R1", MatPropLong, MatPropConfine, CoverTop,
CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetRebarBeam

# GetRebarColumn

## Syntax

SapObject.SapModel.PropFrame.GetRebarColumn

## VB6 Procedure


Function GetRebarColumn(ByVal Name As String, ByRef MatPropLong As String, ByRef
MatPropConfine As String, ByRef Pattern As Long, ByRef ConfineType As Long, ByRef Cover
As Double, ByRef NumberCBars As Long, ByRef NumberR3Bars As Long, ByRef
NumberR2Bars As Long, ByRef RebarSize As String, ByRef TieSize As String, ByRef
TieSpacingLongit As Double, ByRef Number2DirTieBars As Long, ByRef Number3DirTieBars
As Long, ByRef ToBeDesigned As Boolean) As Long

## Parameters

Name

The name of an existing frame section property.

MatPropLong

The name of the rebar material property for the longitudinal rebar.

MatPropConfine

The name of the rebar material property for the confinement rebar.

Pattern

This is either 1 or 2, indicating the rebar configuration.

```
1 = Rectangular
2 = Circular
```
For circular frame section properties, this item must be 2; otherwise an error is returned.

ConfineType

This is either 1 or 2, indicating the confinement bar type.

```
1 = Ties
2 = Spiral
```
This item applies only when Pattern = 2. If Pattern = 1, the confinement bar type is assumed to be
ties.

Cover

The clear cover for the confinement steel (ties). In the special case of circular reinforcement in a
rectangular column, this is the minimum clear cover. [L]

NumberCBars

This item applies to a circular rebar configuration, Pattern = 2. It is the total number of
longitudinal reinforcing bars in the column.

NumberR3Bars


This item applies to a rectangular rebar configuration, Pattern = 1. It is the number of longitudinal
bars (including the corner bar) on each face of the column that is parallel to the local 3-axis of the
column.

NumberR2Bars

This item applies to a rectangular rebar configuration, Pattern = 1. It is the number of longitudinal
bars (including the corner bar) on each face of the column that is parallel to the local 2-axis of the
column.

RebarSize

The rebar name for the longitudinal rebar in the column.

TieSize

The rebar name for the confinement rebar in the column.

TieSpacingLongit

The longitudinal spacing of the confinement bars (ties). [L]

Number2DirTieBars

This item applies to a rectangular reinforcing configuration, Pattern = 1. It is the number of
confinement bars (tie legs) extending in the local 2-axis direction of the column.

Number3DirTieBars

This item applies to a rectangular reinforcing configuration, Pattern = 1. It is the number of
confinement bars (tie legs) extending in the local 3-axis direction of the column.

ToBeDesigned

If this item is True, the column longitudinal rebar is to be designed; otherwise it is to be checked.

## Remarks

This function retrieves column rebar data for frame sections.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

This function applies only to the following section types. Calling this function for any other type
of frame section property returns an error.

```
SECTION_RECTANGULAR = 8
SECTION_CIRCLE = 9
```
The material assigned to the specified frame section property must be concrete or else this
function returns an error.

## VBA Example


Sub GetColumnRebar()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim RebarName As String
Dim MatPropLong As String
Dim MatPropConfine As String
Dim Pattern As Long
Dim ConfineType As Long
Dim Cover As Double
Dim NumberCBars As Long
Dim NumberR3Bars As Long
Dim NumberR2Bars As Long
Dim RebarSize As String
Dim TieSize As String
Dim TieSpacingLongit As Double
Dim Number2DirTieBars As Long
Dim Number3DirTieBars As Long
Dim ToBeDesigned As Boolean

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

'set new frame section property
ret = SapModel.PropFrame.SetRectangle("R1", "4000Psi", 20, 12)

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(RebarName, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'set column rebar data
ret = SapModel.PropFrame.SetRebarColumn("R1", RebarName, RebarName, 2, 2, 2, 10, 0, 0,
"#10", "#5", 4, 0, 0, False)

'get column rebar data
ret = SapModel.PropFrame.GetRebarColumn("R1", MatPropLong, MatPropConfine, Pattern,
ConfineType, Cover, NumberCBars, NumberR3Bars, NumberR2Bars, RebarSize, TieSize,
TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, ToBeDesigned)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetRebarColumn

# GetRectangle

## Syntax

SapObject.SapModel.PropFrame.GetRectangle

## VB6 Procedure

Function GetRectangle(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef Color As Long, ByRef Notes As String,
ByRef GUID As String) As Long

## Parameters

Name

The name of an existing rectangular frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]

Color


The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a rectangular frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropRectangle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new frame section property
ret = SapModel.PropFrame.SetRectangle("R1", "4000Psi", 20, 12)

'get frame section property data
ret = SapModel.PropFrame.GetRectangle("R1", FileName, MatProp, t3, t2, Color, Notes,


### GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetRectangle

SetRebarBeam

SetRebarColumn

GetRebarBeam

GetRebarColumn

# GetSDSection

## Syntax

SapObject.SapModel.PropFrame.GetSDSection

## VB6 Procedure

Function GetSDSection(ByVal Name As String, ByRef MatProp As String, ByRef NumberItems
As Long, ByRef ShapeName() As String, ByRef MyType() As Long, ByRef DesignType As
Long, ByRef Color As Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing section designer property.

MatProp

The name of the base material property for the section.

NumberItems

The number of shapes defined in the section designer section.


ShapeName

This is an array that includes the name of each shape in the section designer section.

MyType

This is an array that includes the type of each shape in the section designer section.

```
1 = I-section
2 = Channel
3 = Tee
4 = Angle
5 = Double Angle
6 = Box
7 = Pipe
8 = Plate
```
```
101 = Solid Rectangle
102 = Solid Circle
103 = Solid Segment
104 = Solid Sector
```
```
201 = Polygon
```
```
301 = Reinforcing Single
302 = Reinforcing Line
303 = Reinforcing Rectangle
304 = Reinforcing Circle
```
```
401 = Reference Line
402 = Reference Circle
```
```
501 = Caltrans Square
502 = Caltrans Circle
503 = Caltrans Hexagon
504 = Caltrans Octagon
```
DesignType

This is 0, 1, 2 or 3, indicating the design option for the section.

```
0 = No design
1 = Design as general steel section
2 = Design as a concrete column; check the reinforcing
3 = Design as a concrete column; design the reinforcing
```
Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.


### GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves section property data for a section designer section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropSDSection()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim NumberItems As Long
Dim ShapeName() As String
Dim MyType() As Long
Dim DesignType As Long
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add I-section shapes to new property
ret = SapModel.PropFrame.SDShape.SetISection("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5, 6, 1)
ret = SapModel.PropFrame.SDShape.SetISection("SD1", "SH2", "A992Fy50", "", -9, -9, 0, -


### 1, 18, 6, 1, 0.5, 6, 1)

ret = SapModel.PropFrame.SDShape.SetISection("SD1", "SH3", "A992Fy50", "", 9, -9, 0, -1,
18, 6, 1, 0.5, 6, 1)

'get section designer section property data
ret = SapModel.PropFrame.GetSDSection("SD1", MatProp, NumberItems, ShapeName,
MyType, DesignType, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetSDSection

# GetSectProps

## Syntax

SapObject.SapModel.PropFrame.GetSectProps

## VB6 Procedure

Function GetSectProps(ByVal Name As String, ByRef Area As Double, ByRef As2 As Double,
ByRef As3 As Double, ByRef Torsion As Double, ByRef I22 As Double, ByRef I33 As Double,
ByRef S22 As Double, ByRef S33 As Double, ByRef Z22 As Double, ByRef Z33 As Double,
ByRef R22 As Double, ByRef R33 As Double) As Long

## Parameters

Name

The name of an existing frame section property.

Area

The cross-sectional area. [L^2 ]

As2

The shear area for forces in the section local 2-axis direction. [L^2 ]


As3

The shear area for forces in the section local 3-axis direction. [L^2 ]

Torsion

The torsional constant. [L^4 ]

I22

The moment of inertia for bending about the local 2 axis. [L^4 ]

I33

The moment of inertia for bending about the local 3 axis. [L^4 ]

S22

The section modulus for bending about the local 2 axis. [L^3 ]

S33

The section modulus for bending about the local 3 axis. [L^3 ]

Z22

The plastic modulus for bending about the local 2 axis. [L^3 ]

Z33

The plastic modulus for bending about the local 3 axis. [L^3 ]

R22

The radius of gyration about the local 2 axis. [L]

R33

The radius of gyration about the local 3 axis. [L]

## Remarks

This function retrieves properties for frame section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFramePropProperties()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim Area As Double
Dim as2 As Double
Dim as3 As Double
Dim Torsion As Double
Dim I22 As Double
Dim I33 As Double
Dim S22 As Double
Dim S33 As Double
Dim Z22 As Double
Dim Z33 As Double
Dim R22 As Double
Dim R33 As Double

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

'get frame section properties
ret = SapModel.PropFrame.GetSectProps("FSEC1", Area, As2, As3, Torsion, I22, I33, S22,
S33, Z22, Z33, R22, R33)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetTee_1

## Syntax

SapObject.SapModel.PropFrame.GetTee_1


## VB6 Procedure

Function GetTee_1(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef tf As Double, ByRef tw As Double,
ByRef FilletRadius As Double, ByRef MirrorAbout3 As Boolean, ByRef Color As Long, ByRef
Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The flange width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

FilletRadius

The fillet radius. [L]

MirrorAbout3 (not applicable)

Indicates whether the section is mirrored about the local 3-axis.

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.


### GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a tee-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropTee()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim tf As Double
Dim tw As Double

```
Dim FilletRadius As Double
```
Dim MirrorAbout3 As Boolean
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'set new frame section property
ret = SapModel.PropFrame.SetTee_1("TEE1", "A992Fy50", 12, 10, 0.6, 0.3, 0.2, False)

'get frame section property data
ret = SapModel.PropFrame.GetTee_1("TEE1", FileName, MatProp, t3, t2, tf, tw,


FilletRadius, MirrorAbout3, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the GetTee.

## See Also

SetTee_1

SetRebarBeam

GetRebarBeam

# GetTube_1

## Syntax

SapObject.SapModel.PropFrame.GetTube_1

## VB6 Procedure

Function GetTube_1(ByVal Name As String, ByRef FileName As String, ByRef MatProp As
String, ByRef t3 As Double, ByRef t2 As Double, ByRef tf As Double, ByRef tw As Double,
ByRef Radius As Double, ByRef Color As Long, ByRef Notes As String, ByRef GUID As String)
As Long

## Parameters

Name

The name of an existing frame section property.

FileName

If the section property was imported from a property file, this is the name of that file. If the section
property was not imported, this item is blank.

MatProp

The name of the material property for the section.

t3


The section depth. [L]

t2

The section width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

Radius

The corner radius, if any. [L]

Color

The display color assigned to the section.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section.

## Remarks

This function retrieves frame section property data for a tube-type frame section.

The function returns zero if the section property data is successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetFramePropTube()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim MatProp As String
Dim t3 As Double
Dim t2 As Double
Dim tf As Double
Dim tw As Double

Dim Radius As Double
Dim Color As Long


Dim Notes As String
Dim GUID As String

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

'set new frame section property
ret = SapModel.PropFrame.SetTube_1("TUBE1", "A992Fy50", 8, 6, 0.5, 0.5, 1.0)

'get frame section property data
ret = SapModel.PropFrame.GetTube_1("TUBE1", FileName, MatProp, t3, t2, tf, tw, Radius,
Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 24.2.

This function supersedes GetTube.

## See Also

SetTube_1

# GetTypeOAPI

## Syntax

SapObject.SapModel.PropFrame.GetTypeOAPI

## VB6 Procedure


Function GetTypeOAPI(ByVal Name As String, ByRef PropType As eFramePropType) As Long

## Parameters

Name

The name of an existing frame section property.

PropType

This is one of the following items in the eFramePropType enumeration.

```
I = 1
Channel = 2
T = 3
Angle = 4
DblAngle = 5
Box = 6
Pipe = 7
Rectangular = 8
Circle = 9
General = 10
DbChannel = 11
Auto = 12
SD = 13
Variable = 14
Joist = 15
Bridge = 16
Cold_C = 17
Cold_2C = 18
Cold_Z = 19
Cold_L = 20
Cold_2L = 21
Cold_HAT = 22
BuiltupICoverplate = 23
PCCGIRDERI = 24
PCCGIRDERU = 25
```
BuiltupIHybrid = 26

BuiltupUHybrid = 27

PCCGirderSuperT = 41

Cold_Box = 42

Cold_I = 43

Cold_Pipe = 44

Cold_T = 45

Trapezoidal = 46


## Remarks

This function retrieves the property type for the specified frame section property.

The function returns zero if the type is successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetFramePropType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PropType As eFramePropType

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

'get frame property type
ret = SapModel.PropFrame.GetTypeOAPI("FSEC1", PropType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed function name to GetTypeOAPI in v17.0.0.

Added New PropType items in 23.1.0

## See Also


# GetTypeRebar

## Syntax

SapObject.SapModel.PropFrame.GetTypeRebar

## VB6 Procedure

Function GetTypeRebar(ByVal Name As String, ByRef MyType As Long) As Long

## Parameters

Name

The name of an existing frame section property.

PropType

This is 0, 1 or 2, indicating the rebar design type.

```
0 = None
1 = Column
2 = Beam
```
## Remarks

This function retrieves the rebar design type for the specified frame section property.

The function returns zero if the type is successfully retrieved; otherwise it returns nonzero.

This function applies only to the following section property types. Calling this function for any
other type of frame section property returns an error.

```
SECTION_T = 3
SECTION_ANGLE = 4
SECTION_RECTANGULAR = 8
SECTION_CIRCLE = 9
```
A nonzero rebar type is returned only if the frame section property has a concrete material.

## VBA Example

Sub GetFramePropRebarType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyType As Long


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

'set new frame section property
ret = SapModel.PropFrame.SetRectangle("R1", "4000Psi", 20, 12)

'get rebar design type
ret = SapModel.PropFrame.GetTypeRebar("R1", MyType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# ImportProp

## Syntax

SapObject.SapModel.PropFrame.ImportProp

## VB6 Procedure

Function ImportProp(ByVal Name As String, ByVal MatProp As String, ByVal FileName As
String, ByVal PropName As String, Optional ByVal Color As Long = -1, Optional ByVal Notes
As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name


The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added. This name does not need to be the same
as the PropName item.

MatProp

The name of the material property for the section.

FileName

The name of the frame section property file from which to get the frame section property specified
by the PropName item.

In most cases you can input just the name of the property file (e.g. Sections8.pro) and the program
will be able to find it. In some cases you may have to input the full path to the property file.

PropName

The name of the frame section property, inside the property file specified by the FileName item,
that is to be imported.

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function imports a frame section property from a property file.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

If the property file is not found, or the specified property name is not found in the property file,
the section is set to be a general section with default properties.

## VBA Example

Sub ImportFrameProp()
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

'import new frame section property
ret = SapModel.PropFrame.ImportProp("W18X35", "A992Fy50", "Sections8.pro",
"W18X35")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetPropFileNameList

# SetAngle_1

## Syntax

SapObject.SapModel.PropFrame.SetAngle_1

## VB6 Procedure

Function SetAngle_1(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal tf As Double, ByVal tw As Double, ByVal FilletRadius As Double,
Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID
As String = "") As Long

## Parameters


Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The vertical leg depth. [L]

t2

The horizontal leg width. [L]

tf

The horizontal leg thickness. [L]

tw

The vertical leg thickness. [L]

FilletRadius

The fillet radius. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, then the program assigns a GUID to the section.

## Remarks

This function initializes an angle-type frame section property. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example


Sub SetFramePropAngle()
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

'set new frame section property
ret = SapModel.PropFrame.SetAngle_1("ANGLE1", "A992Fy50", 6, 4, 0.5, 0.5, 0.2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the SetAngle.

## See Also

GetAngle_1

# SetAutoSelectAluminum

## Syntax

SapObject.SapModel.PropFrame.SetAutoSelectAluminum

## VB6 Procedure


Function SetAutoSelectAluminum(ByVal Name As String, ByVal NumberItems As Long, ByRef
SectName() As String, Optional ByVal AutoStartSection As String = "Median", Optional ByVal
Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

NumberItems

The number of frame section properties included in the auto select list.

SectName

This is an array of the names of the frame section properties included in the auto select list.

Auto select lists and nonprismatic (variable) sections are not allowed in this array.

AutoStartSection

This is Median or the name of a frame section property in the SectName array. It is the starting
section for the auto select list.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function assigns frame section properties to an auto select list. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the auto select list is successfully filled; otherwise it returns a nonzero
value.

## VBA Example

Sub SetFramePropAutoSelectAluminum()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MyName() As String


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'add aluminum material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_ALUMINUM, , ,
MATERIAL_ALUMINUM_SUBTYPE_6061_T6)

'create new aluminum frame section properties
ret = SapModel.PropFrame.SetISection("AI", Name , 18, 6, 0.5, 0.3, 6, 0.5)
ret = SapModel.PropFrame.SetISection("AI2", Name , 18, 6, 0.6, 0.3, 6, 0.6)
ret = SapModel.PropFrame.SetISection("AI3", Name , 18, 6, 0.7, 0.3, 6, 0.7)

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288, True, "AI", "AI")

'define new auto select list frame section property
ReDim MyName(2)
MyName(0) = "AI"
MyName(1) = "AI2"
MyName(2) = "AI3"
ret = SapModel.PropFrame.SetAutoSelectAluminum("AUTO1", 3, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetAutoSelectAluminum


# SetAutoSelectColdFormed

## Syntax

SapObject.SapModel.PropFrame.SetAutoSelectColdFormed

## VB6 Procedure

Function SetAutoSelectColdFormed(ByVal Name As String, ByVal NumberItems As Long,
ByRef SectName() As String, Optional ByVal AutoStartSection As String = "Median", Optional
ByVal Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

NumberItems

The number of frame section properties included in the auto select list.

SectName

This is an array of the names of the frame section properties included in the auto select list.

Auto select lists and nonprismatic (variable) sections are not allowed in this array.

AutoStartSection

This is Median or the name of a frame section property in the SectName array. It is the starting
section for the auto select list.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function assigns frame section properties to an auto select list. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the auto select list is successfully filled; otherwise it returns a nonzero
value.


## VBA Example

Sub SetFramePropAutoSelectColdFormed()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MyName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'create new cold formed frame section properties
ret = SapModel.PropFrame.SetISection("CI", Name , 18, 6, 0.5, 0.3, 6, 0.5)
ret = SapModel.PropFrame.SetISection("CI2", Name , 18, 6, 0.6, 0.3, 6, 0.6)
ret = SapModel.PropFrame.SetISection("CI3", Name , 18, 6, 0.7, 0.3, 6, 0.7)

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288, True, "CI", "CI")

'define new auto select list frame section property
ReDim MyName(2)
MyName(0) = "CI"
MyName(1) = "CI2"
MyName(2) = "CI3"
ret = SapModel.PropFrame.SetAutoSelectColdFormed("AUTO1", 3, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

GetAutoSelectColdFormed

# SetAutoSelectSteel

## Syntax

SapObject.SapModel.PropFrame.SetAutoSelectSteel

## VB6 Procedure

Function SetAutoSelectSteel(ByVal Name As String, ByVal NumberItems As Long, ByRef
SectName() As String, Optional ByVal AutoStartSection As String = "Median", Optional ByVal
Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

NumberItems

The number of frame section properties included in the auto select list.

SectName

This is an array of the names of the frame section properties included in the auto select list.

Auto select lists and nonprismatic (variable) sections are not allowed in this array.

AutoStartSection

This is either Median or the name of a frame section property in the SectName array. It is the
starting section for the auto select list.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks


This function assigns frame section properties to an auto select list. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the auto select list is successfully filled; otherwise it returns a nonzero
value.

## VBA Example

Sub SetFramePropAutoSelectSteel()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC1", "A992Fy50", 24, 8, 0.5, 0.3, 8, 0.5)

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC2", "A992Fy50", 20, 8, 0.5, 0.3, 8, 0.5)

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC3", "A992Fy50", 16, 8, 0.5, 0.3, 8, 0.5)

'set new auto select list frame section property
ReDim MyName(2)
MyName(0) = "ISEC1"
MyName(1) = "ISEC2"
MyName(2) = "ISEC3"
ret = SapModel.PropFrame.SetAutoSelectSteel("AUTO1", 3, MyName, "ISEC2")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

GetAutoSelectSteel

# SetChannel_2

## Syntax

SapObject.SapModel.PropFrame.SetChannel_2

## VB6 Procedure

Function SetChannel_2(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal tf As Double, ByVal tw As Double, ByVal FilletRadius As Double,
ByVal MirrorAbout2 As Boolean, Optional ByVal Color As Long = -1, Optional ByVal Notes As
String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The flange width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

FilletRadius


The fillet radius. [L]

MirrorAbout2 (not applicable)

Indicates whether the section is mirrored about the local 2-axis.

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a channel-type frame section property. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropChannel()
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

'set new frame section property
ret = SapModel.PropFrame.SetChannel_2("CHN1", "A992Fy50", 24, 6, 0.5, 0.3, 0.2, False)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the SetChannel

## See Also

GetChannel_2

# SetCircle

## Syntax

SapObject.SapModel.PropFrame.SetCircle

## VB6 Procedure

Function SetCircle(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID
As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section diameter. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes


The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a solid circular frame section property. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropCircle()
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

'set new frame section property
ret = SapModel.PropFrame.SetCircle("C1", "4000Psi", 20)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

GetCircle

SetRebarBeam

SetRebarColumn

GetRebarBeam

GetRebarColumn

# SetColdBox

## Syntax

SapObject.SapModel.PropFrame.SetColdBox

## VB6 Procedure

Function SetColdBox(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal Thickness As Double, ByVal Radius As Double, Optional ByVal
Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "")
As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section top flange width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]


Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a cold formed box frame section property. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropColdBox()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdBox("CB1", Name, 10, 3.2, 0.08, 0.3)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.

## See Also

GetColdBox

# SetColdC

## Syntax

SapObject.SapModel.PropFrame.SetColdC

## VB6 Procedure

Function SetColdC(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal Thickness As Double, ByVal Radius As Double, ByVal LipDepth As
Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional
ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]


Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

LipDepth

The lip depth, if any. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a cold formed C-type frame section property. If this function is called for
an existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropColdC()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdC("CC1", Name, 10, 3.2, 0.08, 0.3, 0.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetColdC

# SetColdHat

## Syntax

SapObject.SapModel.PropFrame.SetColdHat

## VB6 Procedure

Function SetColdHat(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal Thickness As Double, ByVal Radius As Double, ByVal LipDepth As
Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional
ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp


The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

LipDepth

The lip depth, if any. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, then the program assigns a GUID to the section.

## Remarks

This function initializes a cold formed hat-type frame section property. If this function is called
for an existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropColdHat()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdHat("CH1", Name, 10, 3.2, 0.08, 0.3, 0.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetColdHat

# SetColdI

## Syntax

SapObject.SapModel.PropFrame.SetColdI

## VB6 Procedure

Function SetColdI(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal t2b As Double, ByVal Thickness As Double, ByVal Radius As
Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional
ByVal GUID As String = "") As Long


## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section top flange width. [L]

t2b

The section bottom flange width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a cold formed I-shape frame section property. If this function is called for
an existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.


## VBA Example

Sub SetFramePropColdI()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdI("CI1", Name, 10, 3.2, 0.08, 0.3, 0.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.

## See Also

GetColdI

# SetColdL


## Syntax

SapObject.SapModel.PropFrame.SetColdL

## VB6 Procedure

Function SetColdL(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal Thickness As Double, ByVal Radius As Double, ByVal LipDepth As Double, Optional
ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID As
String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

LipDepth

The lip depth, if any. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.


## Remarks

This function initializes a cold formed Angle frame section property. If this function is called for
an existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropColdL()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdL("CL1", Name, 4.0, 0.08, 0.3, 0.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.


## See Also

GetColdL

# SetColdPipe

## Syntax

SapObject.SapModel.PropFrame.SetColdPipe

## VB6 Procedure

Function SetColdPipe(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal Thickness As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As
String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

Thickness

The section thickness. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.


## Remarks

This function initializes a cold formed pipe frame section property. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropColdPipe()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdPipe("CP1", Name, 8.0, 0.08)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.


## See Also

GetColdPipe

# SetColdT

## Syntax

SapObject.SapModel.PropFrame.SetColdT

## VB6 Procedure

Function SetColdT(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal Thickness As Double, ByVal Radius As Double, Optional ByVal
Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "")
As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section top flange width. [L]

Thickness

The section thickness. [L]

Radius

The corner radius, if any. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.


Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a cold formed Tee frame section property. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropColdT()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdT("CT1", Name, 10, 3.2, 0.08, 0.3, 0.6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 22.2.0.

## See Also

GetColdT

# SetColdZ

## Syntax

SapObject.SapModel.PropFrame.SetColdZ

## VB6 Procedure

Function SetColdZ(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal Thickness As Double, ByVal Radius As Double, ByVal LipDepth As
Double, ByVal LipAngle As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes
As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property then that
property is modified, otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]

Thickness

The section thickness. [L]

Radius


The corner radius, if any. [L]

LipDepth

The lip depth, if any. [L]

LipAngle

The lip angle measured from horizontal (0 <= LipAngle <= 90). [deg]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a cold formed Z-type frame section property. If this function is called for
an existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropColdZ()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add cold formed material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_COLDFORMED, , , ,
MATERIAL_COLDFORMED_SUBTYPE_ASTM_A653SQGr50)

'set new frame section property
ret = SapModel.PropFrame.SetColdZ("CZ1", Name, 10, 3.2, 0.08, 0.3, 0.6, 60)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetColdZ

# SetCoverPlatedI

## Syntax

SapObject.SapModel.PropFrame.SetCoverPlatedI

## VB6 Procedure

Function SetCoverPlatedI(ByVal Name As String, ByVal SectName As String, ByVal
FyTopFlange As Double, ByVal FyWeb As Double, ByVal FyBotFlange As Double, ByVal tc As
Double, ByVal bc As Double, ByVal MatPropTop As String, ByVal tcb As Double, ByVal bcb
As Double, ByVal MatPropBot As String, Optional ByVal Color As Long = -1, Optional ByVal
Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

SectName


The name of an existing I-type frame section property that is used for the I-section portion of the
coverplated I section.

FyTopFlange

The yield strength of the top flange of the I-section. [F/L^2 ]

If this item is 0, the yield strength of the I-section specified by the SectName item is used.

FyWeb

The yield strength of the web of the I-section. [F/L^2 ]

If this item is 0, the yield strength of the I-section specified by the SectName item is used.

FyBotFlange

The yield strength of the bottom flange of the I-section. [F/L^2 ]

If this item is 0, the yield strength of the I-section specified by the SectName item is used.

tc

The thickness of the top cover plate. [L]

If the tc or the bc item is less than or equal to 0, no top cover plate exists.

bc

The width of the top cover plate. [L]

If the tc or the bc item is less than or equal to 0, no top cover plate exists.

MatPropTop

The name of the material property for the top cover plate.

This item applies only if both the tc and the bc items are greater than 0.

tcb

The thickness of the bottom cover plate. [L]

If the tcb or the bcb item is less than or equal to 0, no bottom cover plate exists.

bcb

The width of the bottom cover plate. [L]

If the tcb or the bcb item is less than or equal to 0, no bottom cover plate exists.

MatPropBot

The name of the material property for the bottom cover plate.

This item applies only if both the tcb and the bcb items are greater than 0.


Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a cover plated I-type frame section property. If this function is called for
an existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropCoverPlatedI()
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

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC", "A992Fy50", 24, 8, 0.5, 0.3, 8, 0.5)

'set new cover plated I-type frame section property
ret = SapModel.PropFrame.SetCoverPlatedI("CPI1", "ISEC", 0, 36, 0, 0.75, 14, "A992Fy50",
0.5, 6, "A992Fy50")


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetCoverPlatedI

# SetDblAngle_2

## Syntax

SapObject.SapModel.PropFrame.SetDblAngle_2

## VB6 Procedure

Function SetDblAngle_2(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal tf As Double, ByVal tw As Double, ByVal dis As Double, ByVal
FilletRadius As Double, ByVal MirrorAbout3 As Boolean, Optional ByVal Color As Long = -1,
Optional ByVal Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The vertical leg depth. [L]

t2

The total width of the section, that is, the sum of the widths of each horizontal leg plus the back-to
-back distance. [L]

tf


The horizontal leg thickness. [L]

tw

The vertical leg thickness. [L]

dis

The back-to-back distance between the angles. [L]

FilletRadius

The fillet radius. [L]

MirrorAbout3 (not applicable)

Indicates whether the section is mirrored about the local 3-axis.

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a double angle-type frame section property. If this function is called for an
existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropDblAngle()
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

'set new frame section property
ret = SapModel.PropFrame.SetDblAngle_2("DBANG1", "A992Fy50", 6, 9, 0.5, 0.5, 1, 0.2,
False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the GetDblAngle.

## See Also

GetDblAngle_2

# SetDblChannel_1

## Syntax

SapObject.SapModel.PropFrame.SetDblChannel_1

## VB6 Procedure

Function SetDblChannel_1(ByVal Name As String, ByVal MatProp As String, ByVal t3 As
Double, ByVal t2 As Double, ByVal tf As Double, ByVal tw As Double, ByVal dis As Double,
ByVal FilletRadius As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As
String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.


MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The total width of the section, that is, the sum of the widths of each flange plus the back-to-back
distance. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

dis

The back-to-back distance between the channels. [L]

FilletRadius

The fillet radius. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a double channel-type frame section property. If this function is called for
an existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example


Sub SetFramePropDblChannel()
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

'set new frame section property
ret = SapModel.PropFrame.SetDblChannel_1("DBCHN1", "A992Fy50", 12, 6.5, 0.5, 0.3, 0.5,
0.2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the SetDblAngle.

## See Also

GetDblChannel_1

# SetGeneral

## Syntax

SapObject.SapModel.PropFrame.SetGeneral

## VB6 Procedure

Function SetGeneral(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal Area As Double, ByVal As2 As Double, ByVal As3 As Double,


ByVal Torsion As Double, ByVal I22 As Double, ByVal I33 As Double, ByVal S22 As Double,
ByVal S33 As Double, ByVal Z22 As Double, ByVal Z33 As Double, ByVal R22 As Double,
ByVal R33 As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String =
"", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]

Area

The cross-sectional area. [L^2 ]

As2

The shear area for forces in the section local 2-axis direction. [L^2 ]

As3

The shear area for forces in the section local 3-axis direction. [L^2 ]

Torsion

The torsional constant. [L^4 ]

I22

The moment of inertia for bending about the local 2 axis. [L^4 ]

I33

The moment of inertia for bending about the local 3 axis. [L^4 ]

S22

The section modulus for bending about the local 2 axis. [L^3 ]

S33

The section modulus for bending about the local 3 axis. [L^3 ]


### Z22

The plastic modulus for bending about the local 2 axis. [L^3 ]

Z33

The plastic modulus for bending about the local 3 axis. [L^3 ]

R22

The radius of gyration about the local 2 axis. [L]

R33

The radius of gyration about the local 3 axis. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a general frame section property. If this function is called for an existing
frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropGeneral()
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

'set new frame section property
ret = SapModel.PropFrame.SetGeneral("GEN1", "A992Fy50", 24, 14, 100, 80, 80, 4, 1000,
2400, 140, 200, 150, 220, 3, 5, -1, "API example", "Default")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetGeneral

# SetHybridISection

## Syntax

SapObject.SapModel.PropFrame.SetHybridISection

## VB6 Procedure

Function SetHybridISection(ByVal Name As String, ByRef MatPropTopFlange As String, ByRef
MatPropWeb As String, ByRef MatPropBotFlange As String, ByRef t3 As Double, ByRef t2 As
Double, ByRef TF As Double, ByRef TW As Double, ByRef t2b As Double, ByRef tfb As
Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional
ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property then that
property is modified, otherwise, a new property is added.

MatPropTopFlange


The name of the material property for the top flange.

MatPropWeb

The name of the material property for the web.

MatPropBotFlange

The name of the material property for the bottom flange.

t3

The height of the section. [L]

t2

The width of the top flange. [L]

TF

The thickness of the top flange. [L]

TW

The thickness of the web. [L]

t2b

The width of the bottom flange. [L]

tfb

The thickness of the bottom flange. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, then the program assigns a GUID to the section.

## Remarks

This function initializes a steel hybrid I frame section property. If this function is called for an
existing frame section property then all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized, otherwise it returns a
nonzero value.


## VBA Example

Sub SetFramePropHybridISection()
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

'set new Hybrid I-type frame section property
ret = SapModel.PropFrame.SetHybridISection("HybridI", "A992Fy50", "A992Fy50",
"A992Fy50", 24, 8, 0.5, 0.3, 8, 0.5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# SetHybridUSection

## Syntax

SapObject.SapModel.PropFrame.SetHybridUSection

## VB6 Procedure


Function SetHybridUSection(ByVal Name As String, ByRef WebMaterial As String, ByRef
TopFlangeMaterial As String, ByRef BotFlangeMaterial As String, ByRef T() As Double,
Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID
As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property then that
property is modified, otherwise, a new property is added.

MatPropTopFlange

The name of the material property for the top flange.

MatPropWeb

The name of the material property for the web.

MatPropBotFlange

The name of the material property for the bottom flange.

T()

The dimension array of the section:

(0) D1 = Web Depth (vertical, inside to inside of flanges). [L]

(1) B1 = Web Distance at Top (CL to CL). [L]

(2) B2 = Bottom Flange Width. [L]

(3) B3 = Top Flange Width (per each). [L]

(4) B4 = Bottom Flange Lip (Web CL to flange edge, may be zero). [L]

(5) tw = Web Thickness. [L]

(6) tf = Top Flange Thickness. [L]

(7) tfb = Bottom Flange Thickness. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.


### GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, then the program assigns a GUID to the section.

## Remarks

This function initializes a steel hybrid U frame section property. If this function is called for an
existing frame section property then all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized, otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropHybridUSection()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim T() As Double
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

'set new Hybrid U-type frame section property
Redim T(7)
T(0) = 48
T(1) = 64
T(2) = 48
T(3) = 15
T(4) = 1.5
T(5) = 1
T(6) = 2
T(7) = 2
ret = SapModel.PropFrame.SetHybridUSection("HybridU", "A992Fy50", "A992Fy50",
"A992Fy50", T())

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.0.0.

## See Also

# SetISection_1

## Syntax

SapObject.SapModel.PropFrame.SetISection_1

## VB6 Procedure

Function SetISection_1(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal tf As Double, ByVal tw As Double, ByVal t2b As Double, ByVal tfb
As Double, ByVal FilletRadius As Double, Optional ByVal Color As Long = -1, Optional ByVal
Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The top flange width. [L]

tf

The top flange thickness. [L]

tw

The web thickness. [L]


t2b

The bottom flange width. [L]

tfb

The bottom flange thickness. [L]

FilletRadius

The fillet radius. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes an I-type frame section property. If this function is called for an existing
frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropISection()
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

'set new frame section property
ret = SapModel.PropFrame.SetISection_1("ISEC1", "A992Fy50", 24, 10, 0.5, 0.3, 14, 0.6,
0.2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 25.0.0. This function replaces the SetISection.

## See Also

GetISection_1

# SetModifiers

## Syntax

SapObject.SapModel.PropFrame.SetModifiers

## VB6 Procedure

Function SetModifiers(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing frame section property.

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
```

```
Value(7) = Weight modifier
```
## Remarks

This function assigns property modifiers to a frame section property. The default value for all
modifiers is one.

The function returns zero if the modifiers are successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub AssignFramePropModifiers()
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

'assign modifiers
ReDim Value(7)
For i = 0 To 7
Value(i) = 1
Next i
Value(5) = 100
ret = SapModel.PropFrame.SetModifiers("FSEC1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.02.

## See Also

GetModifiers

# SetNonPrismatic

## Syntax

SapObject.SapModel.PropFrame.SetNonPrismatic

## VB6 Procedure

Function SetNonPrismatic(ByVal Name As String, ByVal NumberItems As Long, ByRef StartSec
() As String, ByRef EndSec() As String, ByRef MyLength() As Double, ByRef MyType() As
Long, ByRef EI33() As Long, ByRef EI22() As Long, Optional ByVal Color As Long = -1,
Optional ByVal Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

NumberItems

The number of segments assigned to the nonprismatic section.

StartSec

This is an array of the names of the frame section properties at the start of each segment.

Auto select lists and nonprismatic sections are not allowed in this array.

EndSec

This is an array of the names of the frame section properties at the end of each segment.

Auto select lists and nonprismatic sections are not allowed in this array.

MyLength

This is an array that includes the length of each segment. The length may be variable or absolute
as indicated by the MyType item. [L] when length is absolute

MyType

This is an array of either 1 or 2, indicating the length type for each segment.


```
1 = Variable (relative length)
2 = Absolute
```
EI33, EI22

This is an array of 1, 2 or 3, indicating the variation type for EI33 and EI22 in each segment.

```
1 = Linear
2 = Parabolic
3 = Cubic
```
Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function assigns data to a nonprismatic frame section property.

The function returns zero if the data is successfully filled; otherwise it returns a nonzero value.

## VBA Example

Sub SetFramePropNonprismatic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim StartSec() As String
Dim EndSec() As String
Dim MyLength() As Double
Dim MyType() As Long
Dim EI33() As Long
Dim EI22() As Long

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

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC1", "A992Fy50", 24, 8, 0.5, 0.3, 8, 0.5)

'set new I-type frame section property
ret = SapModel.PropFrame.SetISection("ISEC2", "A992Fy50", 20, 8, 0.5, 0.3, 8, 0.5)

'set new nonprismatic frame section property
ReDim StartSec(2)
ReDim EndSec(2)
ReDim MyLength(2)
ReDim MyType(2)
ReDim EI33(2)
ReDim EI22(2)
StartSec(0) = "ISEC2"
EndSec(0) = "ISEC1"
MyLength(0) = 60
MyType(0) = 2
EI33(0)= 2
EI22(0)= 1

StartSec(1) = "ISEC1"
EndSec(1) = "ISEC1"
MyLength(1) = 1
MyType(1) = 1
EI33(1)= 2
EI22(1)= 1

StartSec(2) = "ISEC1"
EndSec(2) = "ISEC2"
MyLength(2) = 60
MyType(2) = 2
EI33(2)= 2
EI22(2)= 1

ret = SapModel.PropFrame.SetNonPrismatic("NP1", 3, StartSec, EndSec, MyLength,
MyType, EI33, EI22)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.02.

## See Also

GetNonPrismatic

# SetPipe

## Syntax

SapObject.SapModel.PropFrame.SetPipe

## VB6 Procedure

Function SetPipe(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double, ByVal
tw As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "",
Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The outside diameter. [L]

tw

The wall thickness. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.


## Remarks

This function initializes a pipe-type frame section property. If this function is called for an existing
frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropPipe()
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

'set new frame section property
ret = SapModel.PropFrame.SetPipe("PIPE1", "A992Fy50", 8, 0.375)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetPipe


# SetPrecastI_1

## Syntax

SapObject.SapModel.PropFrame.SetPrecastI_1

## VB6 Procedure

Function SetPrecastI_1(ByVal Name As String, ByVal MatProp As String, ByRef b() As Double,
ByRef d() As Double, ByRef t() As Double, ByRef c As Double,Optional ByVal Color As Long =
-1, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

b

This is an array, dimensioned to 3, containing the horizontal section dimensions. [L]

```
b(0) = B1 (> 0)
b(1) = B2 (> 0)
b(2) = B3 (>= 0)
b(3) = B4 (>= 0)
```
Section dimensions B1 through B4 are defined on the precast concrete I girder definition form.

d

This is an array, dimensioned to 6, containing the vertical section dimensions. [L]

```
d(0) = D1 (> 0)
d(1) = D2 (> 0)
d(2) = D3 (>= 0)
d(3) = D4 (>= 0)
d(4) = D5 (> 0)
d(5) = D6 (>= 0)
d(6) = D7 (>=0)
```
Section dimensions D1 through D7 are defined on the precast concrete I girder definition form.

t

This is an array, dimensioned to 1, containing the web thickness dimensions. [L]


### T(0) = T1 (> 0)

### T(1) = T2 (> 0)

Section dimensions T1 and T2 are defined on the precast I girder definition form.

c

The bottom flange chamfer dimension, denoted as C1 on the precast concrete I girder definition
form.

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a precast concrete I girder frame section property. If this function is called
for an existing frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropPrecastI_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim bb() As Double
Dim dd() As Double

Dim tt() As Double

Dim cc As Double

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

'set new frame section property
ReDim bb(3)
ReDim dd(6)

ReDim tt(1)
bb(0) = 12
bb(1) = 16
bb(2) = 0
bb(3) = 0
dd(0) = 28
dd(1) = 4
dd(2) = 3
dd(3) = 0
dd(4) = 5
dd(5) = 5

dd(6) = 0

tt(0) = 6

tt(1) = 6

cc = 0
ret = SapModel.PropFrame.SetPrecastI_1("PC1", "4000Psi", bb, dd, tt, cc)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

The function supersedes by SetPrecastI.

## See Also

GetPrecastI_1


# SetPrecastU

## Syntax

SapObject.SapModel.PropFrame.SetPrecastU

## VB6 Procedure

Function SetPrecastU(ByVal Name As String, ByVal MatProp As String, ByRef b() As Double,
ByRef d() As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "",
Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

b

This is an array, dimensioned to 5, containing the horizontal section dimensions. [L]

```
b(0) = B1 (> 0)
b(1) = B2 (> 0)
b(2) = B3 (> 0)
b(3) = B4 (>= 0)
b(4) = B5 (>= 0)
b(5) = B6 (>= 0)
```
Section dimensions B1 through B6 are defined on the precast concrete U girder definition form.

d

This is an array, dimensioned to 6, containing the vertical section dimensions. [L]

```
d(0) = D1 (> 0)
d(1) = D2 (> 0)
d(2) = D3 (>= 0)
d(3) = D4 (>= 0)
d(4) = D5 (>= 0)
d(5) = D6 (>= 0)
d(6) = D7 (>= 0)
```
Section dimensions D1 through D7 are defined on the precast concrete U girder definition form.

Color


The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a precast concrete U girder frame section property. If this function is
called for an existing frame section property, all items for the section are reset to their default
value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropPrecastU()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim bb() As Double
Dim dd() As Double

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

'set present units to kN-mm
ret = SapModel.SetPresentUnits(kN_mm_C)

'set new frame section property
ReDim bb(5)
ReDim dd(6)


bb(0) = 2350
bb(1) = 1500
bb(2) = 200
bb(3) = 75
bb(4) = 143.8447
bb(5) = 0
dd(0) = 1700
dd(1) = 175
dd(2) = 75
dd(3) = 0
dd(4) = 0
dd(5) = 125
dd(6) = 175
ret = SapModel.PropFrame.SetPrecastU("PC1", "4000Psi", bb, dd)

'set present units to kip-in
ret = SapModel.SetPresentUnits(kip_in_F)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetPrecastU

# SetRebarBeam

## Syntax

SapObject.SapModel.PropFrame.SetRebarBeam

## VB6 Procedure

Function SetRebarBeam(ByVal Name As String, ByVal MatPropLong As String, ByVal
MatPropConfine As String, ByVal CoverTop As Double, ByVal CoverBot As Double, ByVal
TopLeftArea As Double, ByVal TopRightArea As Double, ByVal BotLeftArea As Double, ByVal
BotRightArea As Double) As Long

## Parameters

Name


The name of an existing frame section property.

MatPropLong

The name of the rebar material property for the longitudinal rebar.

MatPropConfine

The name of the rebar material property for the confinement rebar.

CoverTop

The distance from the top of the beam to the centroid of the top longitudinal reinforcement. [L]

CoverBot

The distance from the bottom of the beam to the centroid of the bottom longitudinal
reinforcement. [L]

TopLeftArea

The total area of longitudinal reinforcement at the top left end of the beam. [L^2 ]

TopRightArea

The total area of longitudinal reinforcement at the top right end of the beam. [L^2 ]

BotLeftArea

The total area of longitudinal reinforcement at the bottom left end of the beam. [L^2 ]

BotRightArea

The total area of longitudinal reinforcement at the bottom right end of the beam. [L^2 ]

## Remarks

This function assigns beam rebar data to frame sections.

The function returns zero if the rebar data is successfully assigned; otherwise it returns a nonzero
value.

This function applies only to the following section types. Calling this function for any other type
of frame section property returns an error.

```
SECTION_T = 3
SECTION_ANGLE = 4
SECTION_RECTANGULAR = 8
SECTION_CIRCLE = 9
```
The material assigned to the specified frame section property must be concrete or this function
returns an error.


## VBA Example

Sub AssignBeamRebar()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim RebarName As String

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

'set new frame section property
ret = SapModel.PropFrame.SetRectangle("R1", "4000Psi", 20, 12)

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(RebarName, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'set beam rebar data
ret = SapModel.PropFrame.SetRebarBeam("R1", RebarName, RebarName, 3.5, 3, 4.1, 4.2,
4.3, 4.4)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetRebarBeam


# SetRebarColumn

## Syntax

SapObject.SapModel.PropFrame.SetRebarColumn

## VB6 Procedure

Function SetRebarColumn(ByVal Name As String, ByVal MatPropLong As String, ByVal
MatPropConfine As String, ByVal Pattern As Long, ByVal ConfineType As Long, ByVal Cover
As Double, ByVal NumberCBars As Long, ByVal NumberR3Bars As Long, ByVal
NumberR2Bars As Long, ByVal RebarSize As String, ByVal TieSize As String, ByVal
TieSpacingLongit As Double, ByVal Number2DirTieBars As Long, ByVal Number3DirTieBars
As Long, ByVal ToBeDesigned As Boolean) As Long

## Parameters

Name

The name of an existing frame section property.

MatPropLong

The name of the rebar material property for the longitudinal rebar.

MatPropConfine

The name of the rebar material property for the confinement rebar.

Pattern

This is either 1 or 2, indicating the rebar configuration.

```
1 = Rectangular
2 = Circular
```
For circular frame section properties this item must be 2; otherwise an error is returned.

ConfineType

This is either 1 or 2, indicating the confinement bar type.

```
1 = Ties
2 = Spiral
```
This item applies only when Pattern = 2. If Pattern = 1, the confinement bar type is assumed to be
ties.

Cover

The clear cover for the confinement steel (ties). In the special case of circular reinforcement in a
rectangular column, this is the minimum clear cover. [L]


NumberCBars

This item applies to a circular rebar configuration, Pattern = 2. It is the total number of
longitudinal reinforcing bars in the column.

NumberR3Bars

This item applies to a rectangular rebar configuration, Pattern = 1. It is the number of longitudinal
bars (including the corner bar) on each face of the column that is parallel to the local 3-axis of the
column.

NumberR2Bars

This item applies to a rectangular rebar configuration, Pattern = 1. It is the number of longitudinal
bars (including the corner bar) on each face of the column that is parallel to the local 2-axis of the
column.

RebarSize

The rebar name for the longitudinal rebar in the column.

TieSize

The rebar name for the confinement rebar in the column.

TieSpacingLongit

The longitudinal spacing of the confinement bars (ties). [L]

Number2DirTieBars

This item applies to a rectangular reinforcing configuration, Pattern = 1. It is the number of
confinement bars (tie legs) running in the local 2-axis direction of the column.

Number3DirTieBars

This item applies to a rectangular reinforcing configuration, Pattern = 1. It is the number of
confinement bars (tie legs) running in the local 3-axis direction of the column.

ToBeDesigned

If this item is True, the column longitudinal rebar is to be designed; otherwise it is to be checked.

## Remarks

This function assigns column rebar data to frame sections.

The function returns zero if the rebar data is successfully assigned; otherwise it returns a nonzero
value.

This function applies only to the following section types. Calling this function for any other type
of frame section property returns an error.

```
SECTION_RECTANGULAR = 8
SECTION_CIRCLE = 9
```

The material assigned to the specified frame section property must be concrete or else this
function returns an error.

## VBA Example

Sub AssignColumnRebar()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim RebarName As String

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

'set new frame section property
ret = SapModel.PropFrame.SetRectangle("R1", "4000Psi", 30, 30)

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(RebarName, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'set column rebar data
ret = SapModel.PropFrame.SetRebarColumn("R1", RebarName, RebarName, 2, 2, 2, 10, 0, 0,
"#10", "#5", 4, 0, 0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetRebarColumn


# SetRectangle

## Syntax

SapObject.SapModel.PropFrame.SetRectangle

## VB6 Procedure

Function SetRectangle(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "",
Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a solid rectangular frame section property. If this function is called for an
existing frame section property, all items for the section are reset to their default value.


The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropRectangle()
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

'set new frame section property
ret = SapModel.PropFrame.SetRectangle("R1", "4000Psi", 20, 12)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetRectangle

SetRebarBeam

SetRebarColumn

GetRebarBeam

GetRebarColumn


# SetSDSection

## Syntax

SapObject.SapModel.PropFrame.SetSDSection

## VB6 Procedure

Function SetSDSection(ByVal Name As String, ByVal MatProp As String, Optional ByVal
DesignType As Long = 0, Optional ByVal Color As Long = -1, Optional ByVal Notes As String =
"", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the base material property for the section.

DesignType

This is 0, 1, 2 or 3, indicating the design option for the section.

```
0 = No design
1 = Design as general steel section
2 = Design as a concrete column; check the reinforcing
3 = Design as a concrete column; design the reinforcing
```
When DesignType = 1 is assigned, the material property specified by the MatProp item must be a
steel material; otherwise the program sets DesignType = 0.

Similarly, when DesignType = 2 or DesignType = 3 is assigned, the material property specified by
the MatProp item must be a concrete material; otherwise the program sets DesignType = 0.

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID


The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a section designer property.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropSDSection()
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

'set new frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetSDSection


# SetTee_1

## Syntax

SapObject.SapModel.PropFrame.SetTee_1

## VB6 Procedure

Function SetTee_1(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal tf As Double, ByVal tw As Double, ByVal FilletRadius As Double,
ByVal MirrorAbout3 As Boolean, Optional ByVal Color As Long = -1, Optional ByVal Notes As
String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The flange width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

FilletRadius

The fillet radius. [L]

MirrorAbout3 (not applicable)

Indicates whether the section is mirrored about the local 3-axis.

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.


Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a tee-type frame section property. If this function is called for an existing
frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropTee()
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

'set new frame section property
ret = SapModel.PropFrame.SetTee_1("TEE1", "A992Fy50", 12, 10, 0.6, 0.3, 0.2, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 25.0.0. This function replaces the SetTee.

## See Also

GetTee_1

SetRebarBeam

GetRebarBeam

# SetTube_1

## Syntax

SapObject.SapModel.PropFrame.SetTube_1

## VB6 Procedure

Function SetTube_1(ByVal Name As String, ByVal MatProp As String, ByVal t3 As Double,
ByVal t2 As Double, ByVal tf As Double, ByVal tw As Double, ByVal Radius As Double,
Optional ByVal Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID
As String = "") As Long

## Parameters

Name

The name of an existing or new frame section property. If this is an existing property, that
property is modified; otherwise, a new property is added.

MatProp

The name of the material property for the section.

t3

The section depth. [L]

t2

The section width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

Radius


The corner radius, may be zero. [L]

Color

The display color assigned to the section. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the section.

GUID

The GUID (global unique identifier), if any, assigned to the section. If this item is input as
Default, the program assigns a GUID to the section.

## Remarks

This function initializes a tube-type frame section property. If this function is called for an existing
frame section property, all items for the section are reset to their default value.

The function returns zero if the section property is successfully initialized; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFramePropTube()
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

'set new frame section property
ret = SapModel.PropFrame.SetTube_1("TUBE1", "A992Fy50", 8, 6, 0.5, 0.5, 0.75)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 24.2.

This function supersedes SetTube.

## See Also

GetTube_1

# Delete

## Syntax

SapObject.SapModel.PropFrame.SDShape.Delete

## VB6 Procedure

Function Delete(ByVal Name As String, ByRef ShapeName As String, Optional ByVal All As
Boolean = False) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing shape in a section designer property. If the All item is True, this item may
be specified as a blank string.

All

If this item is True, all shapes in the section designer property specified by the Name item are
deleted.

## Remarks

This function deletes shapes from a section designer property.

The function returns zero if the shape is successfully deleted; otherwise it returns a nonzero value.


## VBA Example

Sub DeleteFrameSDPropShape()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add I-section shapes to new property
ret = SapModel.PropFrame.SDShape.SetISection("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5, 6, 1)
ret = SapModel.PropFrame.SDShape.SetISection("SD1", "SH2", "A992Fy50", "", -9, -9, 0, -
1, 18, 6, 1, 0.5, 6, 1)
ret = SapModel.PropFrame.SDShape.SetISection("SD1", "SH3", "A992Fy50", "", 9, -9, 0, -1,
18, 6, 1, 0.5, 6, 1)

'delete shape from section designer property
ret = SapModel.PropFrame.SDShape.Delete("SD1", "SH1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

Modified optional argument All to be ByVal in version 12.0.1.

## See Also


# GetAngle

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetAngle

## VB6 Procedure

Function GetAngle(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef PropName As String, ByRef Color As Long, ByRef XCenter As Double, ByRef
YCenter As Double, ByRef h As Double, ByRef bf As Double, ByRef tf As Double, ByRef tw As
Double, ByRef Rotation As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing Angle shape in the specified frame section property.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Angle property that has been imported from a
section property file. If it is the name of a defined Angle property, the section dimensions are
taken from that property.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h

The section depth. [L]

bf

The flange width. [L]


tf

The flange thickness. [L]

tw

The web thickness. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

## Remarks

This function retrieves property data for an Angle shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim PropName As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim h As Double
Dim bf As Double
Dim tf As Double
Dim tw As Double
Dim Rotation As Double

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


'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Angle shape to new property
ret = SapModel.PropFrame.SDShape.SetAngle("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5)

'get Angle shape property data
ret = SapModel.PropFrame.SDShape.GetAngle("SD1", "SH1", MatProp, PropName, Color,
Xcenter, Ycenter, h, bf, tf, tw, Rotation)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetAngle

# GetChannel

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetChannel

## VB6 Procedure

Function GetChannel(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef PropName As String, ByRef Color As Long, ByRef XCenter As Double, ByRef
YCenter As Double, ByRef h As Double, ByRef bf As Double, ByRef tf As Double, ByRef tw As
Double, ByRef Rotation As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing Channel shape in the specified frame section property.

MatProp


The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Channel property that has been imported from a
section property file. If it is the name of a defined Channel property, the section dimensions are
taken from that property.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h

The section depth. [L]

bf

The flange width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

## Remarks

This function retrieves property data for a Channel shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropChannel()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim MatProp As String
Dim PropName As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim h As Double
Dim bf As Double
Dim tf As Double
Dim tw As Double
Dim Rotation As Double

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Channel shape to new property
ret = SapModel.PropFrame.SDShape.SetChannel("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5)

'get Channel shape property data
ret = SapModel.PropFrame.SDShape.GetChannel("SD1", "SH1", MatProp, PropName, Color,
Xcenter, Ycenter, h, bf, tf, tw, Rotation)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetChannel


# GetDblAngle

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetDblAngle

## VB6 Procedure

Function GetDblAngle(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef PropName As String, ByRef Color As Long, ByRef XCenter As Double, ByRef
YCenter As Double, ByRef h As Double, ByRef w As Double, ByRef tf As Double, ByRef tw As
Double, ByRef dis As Double, ByRef Rotation As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing Double Angle shape in the specified frame section property.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Double Angle property that has been imported from
a section property file. If it is the name of a defined Double Angle property, then the section
dimensions are taken from that property.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h

The section depth. [L]

w

The flange width. [L]


tf

The flange thickness. [L]

tw

The web thickness. [L]

dis

Separation between the two flanges that are parallel. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

## Remarks

This function retrieves property data for a Double Angle shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropDblAngle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim PropName As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim h As Double
Dim w As Double
Dim tf As Double
Dim tw As Double
Dim dis As Double
Dim Rotation As Double

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Double Angle shape to new property
ret = SapModel.PropFrame.SDShape.SetDblAngle("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -
1, 18, 6, 1, 0.5, 2)

'get Double Angle shape property data
ret = SapModel.PropFrame.SDShape.GetDblAngle("SD1", "SH1", MatProp, PropName,
Color, Xcenter, Ycenter, h, w, tf, tw, dis, Rotation)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetDblAngle

# GetISection

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetISection

## VB6 Procedure

Function GetISection(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef PropName As String, ByRef Color As Long, ByRef XCenter As Double, ByRef
YCenter As Double, ByRef h As Double, ByRef bf As Double, ByRef tf As Double, ByRef tw As
Double, ByRef bfb As Double, ByRef tfb As Double, ByRef Rotation As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.


ShapeName

The name of an existing I-section shape in the specified frame section property.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined I-section property that has been imported from a
section property file. If it is the name of a defined I-section property, the section dimensions are
taken from that property.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h

The section depth. [L]

bf

The top flange width. [L]

tf

The top flange thickness. [L]

tw

The web thickness. [L]

bfb

The bottom flange width. [L]

tfb

The bottom flange thickness. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]


## Remarks

This function retrieves property data for an I-section shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropISection()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim PropName As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim h As Double
Dim bf As Double
Dim tf As Double
Dim tw As Double
Dim bfb As Double
Dim tfb As Double
Dim Rotation As Double

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add I-section shape to new property
ret = SapModel.PropFrame.SDShape.SetISection("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5, 6, 1)

'get I-section shape property data
ret = SapModel.PropFrame.SDShape.GetISection("SD1", "SH1", MatProp, PropName, Color,


Xcenter, Ycenter, h, bf, tf, tw, bfb, tfb, Rotation)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetISection

# GetPipe

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetPipe

## VB6 Procedure

Function GetPipe(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef PropName As String, ByRef Color As Long, ByRef XCenter As Double, ByRef
YCenter As Double, ByRef diameter As Double, ByRef thickness As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing Pipe shape in the specified frame section property.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Pipe property that has been imported from a section
property file. If it is the name of a defined Pipe property, the section dimensions are taken from
that property.

Color


The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

diameter

The outer diameter of the Pipe. [L]

thickness

The wall thickness of the Pipe. [L]

## Remarks

This function retrieves property data for a Pipe shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropPipe()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim PropName As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim diameter As Double
Dim thickness As Double

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Pipe shape to new property
ret = SapModel.PropFrame.SDShape.SetPipe("SD1", "SH1", "A992Fy50", "", 0, -9, -1, 12, 1)

'get Pipe shape property data
ret = SapModel.PropFrame.SDShape.GetPipe("SD1", "SH1", MatProp, PropName, Color,
Xcenter, Ycenter, diameter, thickness)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetPipe

# GetPlate

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetPlate

## VB6 Procedure

Function GetPlate(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef Color As Long, ByRef XCenter As Double, ByRef YCenter As Double, ByRef
thickness As Double, ByRef w As Double, ByRef Rotation As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing Plate shape in the specified frame section property.

MatProp


The name of the material property for the shape.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

thickness

The thickness of the plate. [L]

w

The width of the Plate. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

## Remarks

This function retrieves property data for an Plate shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropPlate()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim thickness As Double
Dim w As Double
Dim Rotation As Double

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Plate shape to new property
ret = SapModel.PropFrame.SDShape.SetPlate("SD1", "SH1", "A992Fy50", 0, -9, 0, -1, 2, 6)

'get Plate shape property data
ret = SapModel.PropFrame.SDShape.GetPlate("SD1", "SH1", MatProp, Color, Xcenter,
Ycenter, thickness, w, Rotation)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetPlate

# GetPolygon

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetPolygon

## VB6 Procedure

Function GetPolygon(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef SSOverwrite As String, ByRef NumberPoints As Long, ByRef X() As Double,
ByRef Y() As Double, ByRef Radius() As Double, ByRef Color As Long, ByRef Reinf As
Boolean, ByRef MatRebar As String) As Long


## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing polygon shape in the specified frame section property.

MatProp

The name of the material property for the shape.

SSOverwrite

This is a blank string, Default, or the name of a defined stress-strain curve.

If this item is a blank string or Default, the shape stress-strain curve is based on the assigned
material property.

NumberPoints

The number of point coordinates used to define the polygon.

X

This is an array that contains the X-coordinates of the polygon points. [L]

Y

This is an array that contains the Y-coordinates of the polygon points. [L]

Radius

This is an array that contains the radius to be applied at each of the polygon points. [L]

Color

The fill color assigned to the shape.

Reinf

This item is True when there is edge and corner reinforcing steel associated with the shape. The
MatProp item must refer to a concrete material for this item to be True.

MatRebar

The material property for the edge and corner reinforcing steel associated with the shape. This
item applies only when the MatProp item is a concrete material and the Reinf item is True.

## Remarks

This function retrieves property data for a polygon shape in a section designer section.


The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropPolygon()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MatProp As String
Dim SSOverwrite As String

Dim NumberPoints As Long

Dim NumberPointsGet As Long
Dim X() As Double
Dim Y() As Double
Dim Radius() As Double
Dim XGet() As Double
Dim YGet() As Double
Dim RadiusGet() As Double
Dim Color As Long
Dim Reinf As Boolean
Dim MatRebar As String

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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, eMatType.eMatType_Rebar, , , , ,
eMatTypeRebar.eMatTypeRebar_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add polygon shape to new property
NumberPoints = 5
ReDim X(4)


ReDim Y(4)
ReDim Radius(4)
X(0) = -26
Y(0) = -26
Radius(0) = 0

X(1) = -20
Y(1) = -20
Radius(1) = 5
X(2) = -25
Y(2) = 15
Radius(2) = 0
X(3) = 20
Y(3) = 12
Radius(3) = 3
X(4) = 25
Y(4) = -15
Radius(4) = 0
ret = SapModel.PropFrame.SDShape.SetPolygon("SD1", "SH1", "4000Psi", "Default",
NumberPoints, X, Y, Radius, -1, True, Name)

'get polygon shape property data
ret = SapModel.PropFrame.SDShape.GetPolygon("SD1", "SH1", MatProp, SSOverwrite,
NumberPointsGet, XGet, YGet, RadiusGet, Color, Reinf, MatRebar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.1.0.

## See Also

SetPolygon

# GetRefCircle

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetRefCircle

## VB6 Procedure

Function GetRefCircle(ByVal Name As String, ByVal ShapeName As String, ByRef XCenter As
Double, ByRef YCenter As Double, ByRef Diameter As Double) As Long


## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Diameter

The diameter of the circular shape. [L]

## Remarks

This function retrieves property data for a reference circle shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropRefCircle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim XCenter As Double
Dim YCenter As Double
Dim Diameter As Double
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add reference circle shape to new property
ret = SapModel.PropFrame.SDShape.SetRefCircle("SD1", "SH1", 5, 5, 120)

'get reference circle shape property data
ret = SapModel.PropFrame.SDShape.GetRefCircle("SD1", "SH1", XCenter, YCenter,
Diameter)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetRefCircle

# GetRefLine

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetRefLine

## VB6 Procedure

Function GetRefLine(ByVal Name As String, ByVal ShapeName As String, ByRef X1 As
Double, ByRef Y1 As Double, ByRef X2 As Double, ByRef Y2 As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.


ShapeName

The name of a reference line shape in the section designer section.

X1

The section designer X coordinate of the first drawn end point of the line pattern reinforcing. [L]

Y1

The section designer Y coordinate of the first drawn end point of the line pattern reinforcing. [L]

X2

The section designer X coordinate of the second drawn end point of the line pattern reinforcing.
[L]

Y2

The section designer Y coordinate of the second drawn end point of the line pattern reinforcing.
[L]

## Remarks

This function retrieves property data for a reference line shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropRefLine()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatRebar As String
Dim X1 As Double
Dim Y1 As Double
Dim X2 As Double
Dim Y2 As Double

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000psi")

'add Line Pattern Reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetRefLine("SD1", "SH1", 5, 5, 2, 2)

'get Reference Line shape property data
ret = SapModel.PropFrame.SDShape.GetRefLine("SD1", "SH1", X1, Y1, X2, Y2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetRefLine

# GetReinfCircle

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetReinfCircle

## VB6 Procedure

Function GetReinfCircle(ByVal Name As String, ByVal ShapeName As String, ByRef XCenter
As Double, ByRef YCenter As Double, ByRef Diameter As Double, ByRef Numberbars As Long,
ByRef Rotation As Double, ByRef RebarSize As String, ByRef MatRebar As String) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of a circular reinforcing shape in the section designer section.


XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Diameter

The diameter of the circular shape. [L]

NumberBars

The number of equally spaced bars for the circular reinforcing.

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Barsize

It is the size of the reinforcing bar.

MatRebar

The material property for the reinforcing steel.

## Remarks

This function retrieves property data for a circular reinforcing shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropReinfCircle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatRebar As String
Dim XCenter As Double
Dim YCenter As Double
Dim Diameter As Double
Dim Numberbars As Long
Dim Rotation As Double
Dim RebarSize As String
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add circular reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetReinfCircle("SD1", "SH1", 0, 0, 12, 4, 45, "#9",
Name)

'get circular reinforcing shape property data
ret = SapModel.PropFrame.SDShape.GetReinfCircle("SD1", "SH1", Xcenter, Ycenter,
Diameter, Numberbars, Rotation, RebarSize, MatRebar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetReinfCircle

# GetReinfCorner

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetReinfCorner


## VB6 Procedure

Function GetReinfCorner(ByVal Name As String, ByVal ShapeName As String, ByRef
NumberItems As Long, ByRef PointNum() As Long, ByRef RebarSize() As String) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing solid rectangle shape in the specified frame section property.

NumberItems

The number of edges in the shape.

PointNum

This is an array that includes the corner point number in the shape.

RebarSize

This is an array that includes None or the name of a defined rebar, indicating the rebar assignment
to the considered corner point.

## Remarks

This function retrieves corner point reinforcing data for solid rectangle, circle and polygon shapes
in a section designer property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropReinfCorner()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim NumberItems As Long
Dim PointNum() As Long
Dim RebarSize() As String

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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add solid rectangle shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidRect("SD1", "SH1", "4000Psi", "Default", 0, 0,
24, 16, 0, -1, True, Name)

'specify corner reinforcing
ret = SapModel.PropFrame.SDShape.SetReinfCorner("SD1", "SH1", 1, "#9", True)
ret = SapModel.PropFrame.SDShape.SetReinfCorner("SD1", "SH1", 1, "#8")

'get corner point reinforcing
ret = SapModel.PropFrame.SDShape.GetReinfCorner("SD1", "SH1", NumberItems,
PointNum, RebarSize)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetReinfCorner

SetReinfEdge

GetReinfEdge


# GetReinfEdge

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetReinfEdge

## VB6 Procedure

Function GetReinfEdge(ByVal Name As String, ByVal ShapeName As String, ByRef
NumberItems As Long, ByRef EdgeNum() As Long, ByRef RebarSize() As String, ByRef
Spacing() As Double, ByRef Cover() As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing solid rectangle shape in the specified frame section property.

NumberItems

The number of edges in the shape.

EdgeNum

This is an array that includes the edge number in the shape.

RebarSize

This is an array that includes None or the name of a defined rebar, indicating the rebar assignment
to the considered edge.

Spacing

This is an array that includes the rebar maximum center-to-center along the considered edge. [L]

Cover

This is an array that includes the rebar clear cover along the considered edge. [L]

## Remarks

This function retrieves edge reinforcing data for solid rectangle, circle, polygon, and rectangular
reinforcing shapes in a section designer property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetFrameSDPropReinfEdge()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim NumberItems As Long
Dim EdgeNum() As Long
Dim RebarSize() As String
Dim Spacing() As Double
Dim Cover() As Double

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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add solid rectangle shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidRect("SD1", "SH1", "4000Psi", "Default", 0, 0,
24, 16, 0, -1, True, Name)

'specify edge reinforcing
ret = SapModel.PropFrame.SDShape.SetReinfEdge("SD1", "SH1", 1, "#7", 8, 1.75, True)
ret = SapModel.PropFrame.SDShape.SetReinfEdge("SD1", "SH1", 1, "#4", 4, 1.5)

'get edge reinforcing
ret = SapModel.PropFrame.SDShape.GetReinfEdge("SD1", "SH1", NumberItems, EdgeNum,
RebarSize, Spacing, Cover)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetReinfEdge

SetReinfCorner

GetReinfCorner

# GetReinfLine

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetReinfLine

## VB6 Procedure

Function GetReinfLine(ByVal Name As String, ByVal ShapeName As String, ByRef X1 As
Double, ByRef Y1 As Double, ByRef X2 As Double, ByRef Y2 As Double, ByRef Spacing As
Double, ByRef RebarSize As String, ByRef EndBars As Boolean, ByRef MatRebar As String) As
Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of a line reinforcing shape in the section designer section.

X1

The section designer X coordinate of the first drawn end point of the line reinforcing. [L]

Y1

The section designer Y coordinate of the first drawn end point of the line reinforcing. [L]

X2


The section designer X coordinate of the second drawn end point of the line reinforcing. [L]

Y2

The section designer Y coordinate of the second drawn end point of the line reinforcing. [L]

Spacing

The center-to-center spacing of the bars in the line pattern shape. [L]

Bar Size

The size of the reinforcing bars used in the line reinforcing shape.

EndBars

This item is True when there are bars at the end points of the line reinforcing.

MatRebar

The material property for the reinforcing steel.

## Remarks

This function retrieves property data for a line reinforcing shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropReinfLine()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatRebar As String
Dim X1 As Double
Dim Y1 As Double
Dim X2 As Double
Dim Y2 As Double
Dim Spacing As Double
Dim RebarSize As String
Dim EndBars As Boolean
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000psi")

'add line reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetReinfLine("SD1", "SH1", 0, 0, 5, 2, 12, "#9", True,
Name)

'get line reinforcing shape property data
ret = SapModel.PropFrame.SDShape.GetReinfLine("SD1", "SH1", X1, Y1, X2, Y2, Spacing,
RebarSize, EndBars, MatRebar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetReinfLine

# GetReinfRectangular

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetReinfRectangular

## VB6 Procedure

Function GetReinfRectangular(ByVal Name As String, ByVal ShapeName As String, ByRef
XCenter As Double, ByRef YCenter As Double, ByRef h As Double, ByRef w As Double, ByRef
Rotation As Double, ByRef MatRebar As String) As Long


## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of a rectangular reinforcing shape in the section designer section.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h

The section depth. [L]

w

The top flange width. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

MatRebar

The material property for the reinforcing steel.

## Remarks

This function retrieves property data for a rectangular reinforcing shape in a section designer
section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropReinfRectangular()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatRebar As String
Dim XCenter As Double
Dim YCenter As Double
Dim h As Double


Dim w As Double
Dim Rotation As Double
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000psi")

'add rectangular reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetReinfRectangular("SD1", "SH1", 0, 0, 12, 12, 45,
Name)

'get rectangular reinforcing shape property data
ret = SapModel.PropFrame.SDShape.GetReinfRectangular("SD1", "SH1", Xcenter, Ycenter,
h, w, Rotation, MatRebar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetReinfRectangular

# GetReinfSingle


## Syntax

SapObject.SapModel.PropFrame.SDShape.GetReinfSingle

## VB6 Procedure

Function GetReinfSingle(ByVal Name As String, ByVal ShapeName As String, ByRef XCenter
As Double, ByRef YCenter As Double, ByRef RebarSize As String, ByRef MatRebar As String)
As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of a single bar reinforcing shape in the section designer section.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Barsize

The size of the reinforcing bar.

MatRebar

The material property for the reinforcing steel.

## Remarks

This function retrieves property data for a single bar reinforcing shape in a section designer
section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropReinfSingle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim MatRebar As String
Dim XCenter As Double
Dim YCenter As Double
Dim RebarSize As String
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000psi")

'add single bar reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetReinfSingle("SD1", "SH1", 5, 5, "#9", Name)

'get single bar reinforcing shape property data
ret = SapModel.PropFrame.SDShape.GetReinfSingle("SD1", "SH1", XCenter, YCenter,
RebarSize, MatRebar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetReinfSingle


# GetSolidCircle

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetSolidCircle

## VB6 Procedure

Function GetSolidCircle(ByVal Name As String, ByValShapeName As String, ByRefMatProp As
String, ByRefSSOverwrite As String, ByRef Color As Long, ByRefXCenter As Double,
ByRefYCenter As Double, Optional ByRefDiameter As Double, ByRefReinfAs Boolean,
ByRefNumberBarsAs Long = 8, ByRef Rotation As Double, ByRef Cover As Double,
ByRefRebarSize As String, ByRefMatRebar As String) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing solid circle shape in the specified frame section property.

MatProp

The name of the material property for the shape.

SSOverwrite

This is a blank string, Default, or the name of a defined stress-strain curve.

If this item is a blank string or Default, the shape stress-strain curve is based on the assigned
material property.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Diameter

The diameter of the circle.[L]

Reinf


This item is True when there is edge and corner reinforcing steel associated with the shape. The
MatProp item must refer to a concrete material for this item to be True.

# Bars

This item is visible only if the Reinforcing item is set to True. It is the number of equally spaced
bars for the circular reinforcing.

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Barcover

This item is visible only if the Reinforcing item is set to True. It is the clear cover for the specified
rebar.

Bar Size

This item is visible only if the Reinforcing item is set to True. It is the size of the reinforcing bar.

MatRebar

The material property for the edge and corner reinforcing steel associated with the shape. This
item applies only when the MatProp item is a concrete material and the Reinf item is True.

## Remarks

This function retrieves property data for a solid circle shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropSolidCircle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MatProp As String
Dim SSOverwrite As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim Diameter As Long
Dim Reinf As Boolean
Dim NumberBars As Long
Dim Rotation As Double
Dim Cover As Double
Dim RebarSize As String
Dim MatRebar As String


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'createSapModelobject
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'addASTMA706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add solid circle shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidCircle("SD1", "SH1", "4000psi", "Default", 0,
0, 12, -1, True, 16, 0, 16, "#4", Name)

'get solid circle shape property data
ret = SapModel.PropFrame.SDShape.GetSolidCircle("SD1", "SH1", MatProp, SSOverwrite,
Color, XCenter, YCenter, Diameter, Reinf, NumberBars, Rotation, Cover, RebarSize, MatRebar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetSolidCircle

# GetSolidRect

## Syntax


SapObject.SapModel.PropFrame.SDShape.GetSolidRect

## VB6 Procedure

Function GetSolidRect(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef SSOverwrite As String, ByRef Color As Long, ByRef XCenter As Double, ByRef
YCenter As Double, ByRef h As Double, ByRef w As Double, ByRef Rotation As Double, ByRef
Reinf As Boolean, ByRef MatRebar As String) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing solid rectangle shape in the specified frame section property.

MatProp

The name of the material property for the shape.

SSOverwrite

This is a blank string, Default, or the name of a defined stress-strain curve.

If this item is a blank string or Default, the shape stress-strain curve is based on the assigned
material property.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h

The section depth. [L]

w

The section width. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]


Reinf

This item is True when there is edge and corner reinforcing steel associated with the shape. The
MatProp item must refer to a concrete material for this item to be True.

MatRebar

The material property for the edge and corner reinforcing steel associated with the shape. This
item applies only when the MatProp item is a concrete material and the Reinf item is True.

## Remarks

This function retrieves property data for a solid rectangular shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropSolidRect()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MatProp As String
Dim SSOverwrite As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim h As Double
Dim w As Double
Dim Rotation As Double
Dim Reinf As Boolean
Dim MatRebar As String

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

'add ASTM A706 rebar material


ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add solid rectangle shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidRect("SD1", "SH1", "4000Psi", "Default", 0, 0,
24, 16, 0, -1, True, Name)

'get solid rectangle shape property data
ret = SapModel.PropFrame.SDShape.GetSolidRect("SD1", "SH1", MatProp, SSOverwrite,
Color, Xcenter, Ycenter, h, w, Rotation, Reinf, MatRebar)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetSolidRect

# GetSolidSector

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetSolidSector

## VB6 Procedure

Function GetSolidSector(ByVal Name As String, ByValShapeName As String, ByRefMatProp As
String, ByRef Color As Long, ByRefXCenter As Double, ByRefYCenter As Double, ByRef
Angle As Double, ByRefRotation As Double, ByRef Radius As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName


The name of an existing solid sector shape in the specified frame section property.

MatProp

The name of the material property for the shape.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Angle

The angle between the two radii that define the circular sector. [deg]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Radius

The radius of the circle defining the Sector. [L]

## Remarks

This function retrieves property data for a solid sector shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropSolidSector()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MatProp As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim Angle As Double
Dim Rotation As Double
Dim Radius As Double


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'createSapModelobject
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'addASTMA706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add solid sector shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidSector("SD1", "SH1", "4000Psi", 0, 0, 95, 0,
10, -1)

'get solid sector shape property data
ret = SapModel.PropFrame.SDShape.GetSolidSector("SD1", "SH1", MatProp, Color,
Xcenter, Ycenter, Angle, Rotation, Radius)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetSolidSector

# GetSolidSegment

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetSolidSegment


## VB6 Procedure

Function GetSolidSegment(ByVal Name As String, ByValShapeName As String, ByRefMatProp
As String, ByRef Color As Long, ByRefXCenter As Double, ByRefYCenter As Double, ByRef
Angle As Double, ByRefRotation As Double, ByRef Radius As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing solid segment shape in the specified frame section property.

MatProp

The name of the material property for the shape.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Angle

The angle between lines drawn from the center of the circle to the end points of the chord tat
defines the segment. [deg]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Radius

The radius of the circle defining the segment.

## Remarks

This function retrieves property data for a solid segment shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetFrameSDPropSolidSegment()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MatProp As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim Angle As Double
Dim Rotation As Double
Dim Radius As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'createSapModelobject
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add solid segment shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidSegment("SD1", "SH1", "4000Psi", 0, 0, 95, 0,
10, -1)

'get solid segment shape property data
ret = SapModel.PropFrame.SDShape.GetSolidSegment("SD1", "SH1", MatProp, Color,
Xcenter, Ycenter, Angle, Rotation, Radius)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.


## See Also

SetSolidSegment

# GetTee

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetTee

## VB6 Procedure

Function GetTee(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef PropName As String, ByRef Color As Long, ByRef XCenter As Double, ByRef
YCenter As Double, ByRef h As Double, ByRef bf As Double, ByRef tf As Double, ByRef tw As
Double, ByRef Rotation As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing Tee shape in the specified frame section property.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Tee property that has been imported from a section
property file. If it is the name of a defined Tee property, the section dimensions are taken from
that property.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h


The section depth. [L]

bf

The section width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

## Remarks

This function retrieves property data for a Tee shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetFrameSDPropTee()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim PropName As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim h As Double
Dim bf As Double
Dim tf As Double
Dim tw As Double
Dim Rotation As Double

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Tee shape to new property
ret = SapModel.PropFrame.SDShape.SetTee("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1, 18,
6, 1, 0.5)

'get Tee shape property data
ret = SapModel.PropFrame.SDShape.GetTee("SD1", "SH1", MatProp, PropName, Color,
Xcenter, Ycenter, h, bf, tf, tw, Rotation)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetTee

# GetTube

## Syntax

SapObject.SapModel.PropFrame.SDShape.GetTube

## VB6 Procedure

Function GetTube(ByVal Name As String, ByVal ShapeName As String, ByRef MatProp As
String, ByRef PropName As String, ByRef Color As Long, ByRef XCenter As Double, ByRef
YCenter As Double, ByRef h As Double, ByRef w As Double, ByRef tf As Double, ByRef tw As
Double, ByRef Rotation As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.


ShapeName

The name of an existing Tube shape in the specified frame section property.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Tube property that has been imported from a
section property file. If it is the name of a defined Tube property, the section dimensions are taken
from that property.

Color

The fill color assigned to the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h

The section height. [L]

w

The section width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

## Remarks

This function retrieves property data for a Tube shape in a section designer section.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetFrameSDPropTube()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim PropName As String
Dim Color As Long
Dim XCenter As Double
Dim YCenter As Double
Dim h As Double
Dim w As Double
Dim tf As Double
Dim tw As Double
Dim Rotation As Double

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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Tube shape to new property
ret = SapModel.PropFrame.SDShape.SetTube("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5)

'get Tube shape property data
ret = SapModel.PropFrame.SDShape.GetTube("SD1", "SH1", MatProp, PropName, Color,
Xcenter, Ycenter, h, w, tf, tw, Rotation)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 12.00.

## See Also

SetTube

# SetAngle

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetAngle

## VB6 Procedure

Function SetAngle(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal PropName As String, ByVal XCenter As Double, ByVal YCenter As Double,
ByVal Rotation As Double, Optional ByVal Color As Long = -1, Optional ByVal h As Double =
24, Optional ByVal bf As Double = 24, Optional ByVal tf As Double = 2.4, Optional ByVal tw
As Double = 2.4) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Angle property that has been imported from a
section property file.

If this item is a blank string, the section dimensions are taken from the values input in this
function.


If this item is the name of a defined Angle property that has been imported from a section property
file, the section dimensions are taken from the specified Angle property.

If this item is not blank, and the specified property name is not an Angle that was imported from a
section property file, an error is returned.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

h

The section depth. [L]

bf

The flange width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

## Remarks

This function adds a new Angle shape or modifies an existing shape to be an Angle shape in a
section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropAngle()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Angle shape to new property
ret = SapModel.PropFrame.SDShape.SetAngle("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetAngle

# SetChannel

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetChannel

## VB6 Procedure

Function SetChannel (ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal PropName As String, ByVal XCenter As Double, ByVal YCenter As Double,
ByVal Rotation As Double, Optional ByVal Color As Long = -1, Optional ByVal h As Double =


24, Optional ByVal bf As Double = 24, Optional ByVal tf As Double = 2.4, Optional ByVal tw
As Double = 2.4) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Channel property that has been imported from a
section property file.

If this item is a blank string, the section dimensions are taken from the values input in this
function.

If this item is the name of a defined Channel property that has been imported from a section
property file, the section dimensions are taken from the specified Channel property.

If this item is not blank, and the specified property name is not an Channel that was imported from
a section property file, an error is returned.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

h

The section depth. [L]


bf

The flange width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

## Remarks

This function adds a new Channel shape or modifies an existing shape to be a Channel shape in a
section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropChannel()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Channel shape to new property
ret = SapModel.PropFrame.SDShape.SetChannel("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetChannel

# SetDblAngle

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetDblAngle

## VB6 Procedure

Function SetDblAngle(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal PropName As String, ByVal XCenter As Double, ByVal YCenter As Double,
ByVal Rotation As Double, Optional ByVal Color As Long = -1, Optional ByVal h As Double =
24, Optional ByVal w As Double = 24, Optional ByVal tf As Double = 2.4, Optional ByVal tw As
Double = 2.4, Optional ByVal dis As Double = 1.2) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined DblAngle property that has been imported from a
section property file.


If this item is a blank string, the section dimensions are taken from the values input in this
function.

If this item is the name of a defined DblAngle property that has been imported from a section
property file, the section dimensions are taken from the specified DblAngle property.

If this item is not blank and the specified property name is not an DblAngle that was imported
from a section property file, an error is returned.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

h

The section depth. [L]

w

The flange width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

dis

Separation between the two flanges that are parallel. [L]

## Remarks

This function adds a new Double Angle shape or modifies an existing shape to be an Double
Angle shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.


## VBA Example

Sub SetFrameSDPropDblAngle()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Double Angle shape to new property
ret = SapModel.PropFrame.SDShape.SetDblAngle("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -
1, 18, 6, 1, 0.5, 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetDblAngle

# SetISection

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetISection


## VB6 Procedure

Function SetISection(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal PropName As String, ByVal XCenter As Double, ByVal YCenter As Double,
ByVal Rotation As Double, Optional ByVal Color As Long = -1, Optional ByVal h As Double =
24, Optional ByVal bf As Double = 24, Optional ByVal tf As Double = 2.4, Optional ByVal tw
As Double = 2.4, Optional ByVal bfb As Double = 24, Optional ByVal tfb As Double = 2.4) As
Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined I-section property that has been imported from a
section property file.

If this item is a blank string, the section dimensions are taken from the values input in this
function.

If this item is the name of a defined I-section property that has been imported from a section
property file, the section dimensions are taken from the specified I-section property.

If this item is not blank, and the specified property name is not an I-section that was imported
from a section property file, an error is returned.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color


The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

h

The section depth. [L]

bf

The top flange width. [L]

tf

The top flange thickness. [L]

tw

The web thickness. [L]

bfb

The bottom flange width. [L]

tfb

The bottom flange thickness. [L]

## Remarks

This function adds a new I-section shape or modifies an existing shape to be an I-section shape in
a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropISection()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add I-section shape to new property
ret = SapModel.PropFrame.SDShape.SetISection("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5, 6, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetISection

# SetPipe

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetPipe

## VB6 Procedure

Function SetPipe(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal PropName As String, ByVal XCenter As Double, ByVal YCenter As Double,
Optional ByVal Color As Long = -1, Optional ByVal diameter As Double = 24, Optional ByVal
thickness As Double = 2.4) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName


The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Pipe property that has been imported from a section
property file.

If this item is a blank string, the section dimensions are taken from the values input in this
function.

If this item is the name of a defined Pipe property that has been imported from a section property
file, the section dimensions are taken from the specified Pipe property.

If this item is not blank and the specified property name is not a Pipe that was imported from a
section property file, an error is returned.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

diameter

The outer diameter of the Pipe. [L]

thickness

The wall thickness of the Pipe. [L]

## Remarks

This function adds a new Pipe shape or modifies an existing shape to be a Pipe shape in a section
designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.


## VBA Example

Sub SetFrameSDPropPipe()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Pipe shape to new property
ret = SapModel.PropFrame.SDShape.SetPipe("SD1", "SH1", "A992Fy50", "", 0, -9, -1, 12, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetPipe

# SetPlate

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetPlate


## VB6 Procedure

Function SetPlate(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal XCenter As Double, ByVal YCenter As Double, ByVal Rotation As Double,
Optional ByVal Color As Long = -1, Optional ByVal thickness As Double = 2.4, Optional ByVal
w As Double = 24) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,n
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

thickness

The thickness of the plate. [L]

w

The width of the Plate. [L]

## Remarks


This function adds a new Plate shape or modifies an existing shape to be a Plate shape in a section
designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropPlate()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Plate shape to new property
ret = SapModel.PropFrame.SDShape.SetPlate("SD1", "SH1", "A992Fy50", 0, -9, 0, -1, 2, 6)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetPlate


# SetPolygon

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetPolygon

## VB6 Procedure

Function SetPolygon(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal SSOverwrite As String, ByVal NumberPoints As Long, ByRef X() As Double,
ByRef Y() As Double, ByRef Radius() As Double, Optional ByVal Color As Long = -1, Optional
ByVal Reinf As Boolean = False, Optional ByVal MatRebar As String = "") As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

SSOverwrite

This is a blank string, Default, or the name of a defined stress-strain curve.

If this item is a blank string or Default, the shape stress-strain curve is based on the assigned
material property.

NumberPoints

The number of point coordinates used to define the polygon.

X

This is an array that contains the X-coordinates of the polygon points. [L]

Y

This is an array that contains the Y-coordinates of the polygon points. [L]

Radius


This is an array that contains the radius to be applied at each of the polygon points. [L]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

Reinf

This item is True when there is edge and corner reinforcing steel associated with the shape.

If the MatProp item is not a concrete material, this item is always assumed to be False.

MatRebar

The material property for the edge and corner reinforcing steel associated with the shape. This
item applies only when the MatProp item is a concrete material and the Reinf item is True.

## Remarks

This function adds a new polygon shape or modifies an existing shape to be a polygon shape in a
section designer property.

The polygon points must be defined in order around the polygon, otherwise the shape will be
created incorrectly or the creation of the shape will fail.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero val.

## VBA Example

Sub SetFrameSDPropPolygon()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String

Dim NumberPoints As Long

Dim X() As Double

Dim Y() As Double

Dim Radius() As Double

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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, eMatType.eMatType_Rebar, , , , ,
eMatTypeRebar.eMatTypeRebar_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add polygon shape to new property
NumberPoints = 5
ReDim X(4)
ReDim Y(4)
ReDim Radius(4)
X(0) = -26
Y(0) = -26
Radius(0) = 0

X(1) = -20
Y(1) = -20
Radius(1) = 5
X(2) = -25
Y(2) = 15
Radius(2) = 0
X(3) = 20
Y(3) = 12
Radius(3) = 3
X(4) = 25
Y(4) = -15
Radius(4) = 0
ret = SapModel.PropFrame.SDShape.SetPolygon("SD1", "SH1", "4000Psi", "Default",
NumberPoints, X, Y, Radius, -1, True, Name)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.1.0.

## See Also


GetPolygon

# SetRefCircle

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetRefCircle

## VB6 Procedure

Function SetRefCircle(ByVal Name As String, ByRef ShapeName As String, ByVal XCenter As
Double, ByVal YCenter As Double, ByVal Diameter As Double)As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Diameter

The diameter of the circular shape. [L]

## Remarks

This function adds a new reference circle shape or modifies an existing shape to be a reference
circle shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example


Sub SetFrameSDPropRefCircle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add reference circle shape to new property
ret = SapModel.PropFrame.SDShape.SetRefCircle("SD1", "SH1", 0, 0, 12)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetRefCircle

# SetRefLine

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetRefLine


## VB6 Procedure

Function SetRefLine(ByVal Name As String, ByRef ShapeName As String, ByVal X1 As
Double, ByVal Y1 As Double, ByVal X2 As Double, ByVal Y2 As Double) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

X1

The section designer X coordinate of the first drawn end point of the line pattern reinforcing. [L]

Y1

The section designer Y coordinate of the first drawn end point of the line pattern reinforcing. [L]

X2

The section designer X coordinate of the second drawn end point of the line pattern reinforcing.
[L]

Y2

The section designer Y coordinate of the second drawn end point of the line pattern reinforcing.
[L]

## Remarks

This function adds a new reference line shape or modifies an existing shape to be a reference line
shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropRefLine()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000psi")

'add Line Pattern Reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetRefLine("SD1", "SH1", 5, 5, 2, 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetRefLine

# SetReinfCircle

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetReinfCircle

## VB6 Procedure

Function SetReinfCircle(ByVal Name As String, ByRef ShapeName As String, ByVal XCenter
As Double, ByVal YCenter As Double, ByVal Diameter As Double, ByVal Numberbars As Long,
ByVal Rotation As Double, ByVal RebarSize As Double, Optional ByVal MatRebar As String =
"") As Long


## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Diameter

The diameter of the circular shape. [L]

NumberBars

The number of equally spaced bars for the circular reinforcing.

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Barsize

It is the size of the reinforcing bar.

MatRebar

The material property for the reinforcing steel.

## Remarks

This function adds a new circular reinforcing shape or modifies an existing shape to be an circular
reinforcing shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example


Sub SetFrameSDPropReinfCircle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add circular reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetReinfCircle("SD1", "SH1", 0, 0, 12, 4, 45, "#9",
Name)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetReinfCircle


# SetReinfCorner

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetReinfCorner

## VB6 Procedure

Function SetReinfCorner(ByVal Name As String, ByRef ShapeName As String, ByVal PointNum
As Long, ByVal RebarSize As String, Optional ByVal All As Boolean = False) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing solid rectangle, circle or polygon shape in the specified section.

PointNum

An corner point number in the shape. This item is ignored if the All item is True.

RebarSize

This is None or the name of a defined rebar, indicating the rebar assignment to the specified
corner.

All

If this item is True, the specified rebar data applies to all corners in the shape.

## Remarks

This function specifies corner reinforcing in solid rectangle, circle and polygon shapes in a section
designer property.

The function returns zero if the reinforcing is successfully specified; otherwise it returns a nonzero
value.

## VBA Example

Sub SetFrameSDPropReinfCorner()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add solid rectangle shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidRect("SD1", "SH1", "4000Psi", "Default", 0, 0,
24, 16, 0, -1, True, Name)

'specify corner reinforcing
ret = SapModel.PropFrame.SDShape.SetReinfCorner("SD1", "SH1", 1, "#9", True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetReinfCorner

SetReinfEdge

GetReinfEdge

# SetReinfEdge


## Syntax

SapObject.SapModel.PropFrame.SDShape.SetReinfEdge

## VB6 Procedure

Function SetReinfEdge(ByVal Name As String, ByRef ShapeName As String, ByVal EdgeNum
As Long, ByVal RebarSize As String, ByVal Spacing As Double, ByVal Cover As Double,
Optional ByVal All As Boolean = False) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing solid rectangle, circle or polygon shape in the specified section.

EdgeNum

An edge number in the shape. This item is ignored if the All item is True.

RebarSize

This is None or the name of a defined rebar, indicating the rebar assignment to the specified edge.

Spacing

This is the rebar maximum center-to-center along the specified edge. [L]

Cover

This is the rebar clear cover along the specified edge. [L]

All

If this item is True, the specified rebar data applies to all edges in the shape.

## Remarks

This function specifies edge reinforcing in solid rectangle, circle, polygon and rectangular
reinforcing shapes in a section designer property.

The function returns zero if the reinforcing is successfully specified; otherwise it returns a nonzero
value.

## VBA Example


Sub SetFrameSDPropReinfEdge()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add solid rectangle shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidRect("SD1", "SH1", "4000Psi", "Default", 0, 0,
24, 16, 0, -1, True, Name)

'specify edge reinforcing
ret = SapModel.PropFrame.SDShape.SetReinfEdge("SD1", "SH1", 1, "#7", 8, 1.75, True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetReinfEdge

SetReinfCorner


GetReinfCorner

# SetReinfLine

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetReinfLine

## VB6 Procedure

Function SetReinfLine(ByVal Name As String, ByRef ShapeName As String, ByVal X1 As
Double, ByVal Y1 As Double, ByVal X2 As Double, ByVal Y2 As Double, Optional ByVal
Spacing As Double = 6, Optional ByVal RebarSize As String = "", Optional ByVal EndBars As
Boolean = False, ByVal MatRebar As String) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

X1

The section designer X coordinate of the first drawn end point of the line reinforcing. [L]

Y1

The section designer Y coordinate of the first drawn end point of the line reinforcing. [L]

X2

The section designer X coordinate of the second drawn end point of the line reinforcing. [L]

Y2

The section designer Y coordinate of the second drawn end point of the line reinforcing. [L]

Spacing

The center-to-center spacing of the bars in the line pattern shape. [L]

Bar Size

The size of the reinforcing bars used in the line reinforcing shape.


EndBars

This item is True when there are bars at the end points of the line reinforcing.

MatRebar

The material property for the reinforcing steel.

## Remarks

This function adds a new line reinforcing shape or modifies an existing shape to be a line
reinforcing shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropReinfLine()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000psi")

'add Line Pattern Reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetReinfLine("SD1", "SH1", 0, 0, 5, 2, 12, "#9", True,
Name)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetReinfLine

# SetReinfRectangular

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetReinfRectangular

## VB6 Procedure

Function SetReinfRectangular(ByVal Name As String, ByRef ShapeName As String, ByVal
XCenter As Double, ByVal YCenter As Double, ByVal h As Double, ByVal Rotation As Double,
ByVal w As Double, Optional ByVal MatRebar As String = "") As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

h


The section depth. [L]

w

The top flange width. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

MatRebar

The material property for the reinforcing steel.

## Remarks

This function adds a new rectangular reinforcing shape or modifies an existing shape to be a
rectangular reinforcing shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropReinfRectangular()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000psi")


'add rectangular reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetReinfRectangular("SD1", "SH1", 0, 0, 12, 12, 45,
Name)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

Moved Rotation to after the width, w, in version 25.0.0

## See Also

GetReinfRectangular

# SetReinfSingle

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetReinfSingle

## VB6 Procedure

Function SetReinfSingle(ByVal Name As String, ByRef ShapeName As String, ByVal XCenter
As Double, ByVal YCenter As Double, Optional ByVal RebarSize As String = "", Optional
ByRef MatRebar As String = "") As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

XCenter


The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Barsize

It is the size of the reinforcing bar.

MatRebar

The material property for the reinforcing steel.

## Remarks

This function adds a new single bar reinforcing shape or modifies an existing shape to be a single
bar reinforcing shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropReinfSingle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000psi")


'add single bar reinforcing shape to new property
ret = SapModel.PropFrame.SDShape.SetReinfSingle("SD1", "SH1", 5, 5, "#9", Name)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetReinfSingle

# SetSolidCircle

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetSolidCircle

## VB6 Procedure

Function SetSolidCircle(ByVal Name As String, ByRefShapeNameAs String, ByValMatProp As
String, ByValSSOverwrite As String, ByValXCenter As Double, ByValYCenter As Double,
Optional ByVal diameter As Double = 24, Optional ByVal color As Long = -1, Optional
ByValReinf As Boolean = False, Optional ByValNumberBars As Long = 8, Option ByVal
Rotation As Double = 22.5, Optional ByVal Cover As Double = 2, Optional ByValRebarSize As
String = "", Optional ByValMatRebar As String = "") As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp


The name of the material property for the shape.

SSOverwrite

This is a blank string, Default, or the name of a defined stress-strain curve.

If this item is a blank string or Default, the shape stress-strain curve is based on the assigned
material property.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Diameter

The diameter of the circle.[L]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

Reinf

This item is True when there is edge and corner reinforcing steel associated with the shape.

If the MatProp item is not a concrete material, this item is always assumed to be False.

# Bars

This item is visible only if the Reinforcing item is set to True. It is the number of equally spaced
bars for the circular reinforcing.

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Bar Cover

This item is visible only if the Reinforcing item is set to True. It is the clear cover for the
specified rebar. [L]

Barsize

This item is visible only if the Reinforcing item is set to True. It is the size of the reinforcing bar.

MatRebar

The material property for the edge and corner reinforcing steel associated with the shape. This
item applies only when the MatProp item is a concrete material and the Reinf item is True.


## Remarks

This function adds a new solid circle shape or modifies an existing shape to be a solid circle shape
in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropSolidCircle()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'createSapModelobject
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'addASTMA706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add solid circle shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidCircle("SD1", "SH1", "4000psi", "Default", 0,
0, 12, -1, True, 16, 0, 16, "#4", Name)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 12.00.

## See Also

GetSolidCircle

# SetSolidRect

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetSolidRect

## VB6 Procedure

Function SetSolidRect(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal SSOverwrite As String, ByVal XCenter As Double, ByVal YCenter As Double,
ByVal h As Double, ByVal w As Double, ByVal Rotation As Double, Optional ByVal color As
Long = -1, Optional ByVal Reinf As Boolean = False, Optional ByVal MatRebar As String = "")
As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

SSOverwrite

This is a blank string, Default, or the name of a defined stress-strain curve.

If this item is a blank string or Default, the shape stress-strain curve is based on the assigned
material property.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter


The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

h

The section depth. [L]

w

The section width. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

Reinf

This item is True when there is edge and corner reinforcing steel associated with the shape.

If the MatProp item is not a concrete material, this item is always assumed to be False.

MatRebar

The material property for the edge and corner reinforcing steel associated with the shape. This
item applies only when the MatProp item is a concrete material and the Reinf item is True.

## Remarks

This function adds a new solid rectangle shape or modifies an existing shape to be an solid
rectangle shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropSolidRect()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


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

'add ASTM A706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add solid rectangle shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidRect("SD1", "SH1", "4000Psi", "Default", 0, 0,
24, 16, 0, -1, True, Name)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetSolidRect

# SetSolidSector

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetSolidSector


## VB6 Procedure

Function SetSolidSector(ByVal Name As String, ByRefShapeName As String, ByValMatProp As
String, ByValXCenter As Double, ByValYCenter As Double, ByVal Angle As Double, ByVal
Rotation As Double, ByValRadius As Double, Optional ByVal Color As Long = -1) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Angle

The angle between the two radii that define the circular sector. [deg]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Radius

The radius of the circle defining the Sector. [L]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

## Remarks

This function adds a new solid sector shape or modifies an existing shape to be a solid sector
shape in a section designer property.


The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropSolidSector()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'createSapModelobject
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'addASTMA706 rebar material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_REBAR, , , , ,
MATERIAL_REBAR_SUBTYPE_ASTM_A706)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add solid sector shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidSector("SD1", "SH1", "4000Psi", 0, 0, 95, 0,
10, -1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetSolidSector


# SetSolidSegment

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetSolidSegment

## VB6 Procedure

Function SetSolidSegment(ByVal Name As String, ByRefShapeName As String, ByValMatProp
As String, ByValXCenter As Double, ByValYCenter As Double, ByVal Angle As Double, ByVal
Rotation As Double, ByValRadius as Double, Optional ByVal Color As Long = -1) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Angle

The angle between lines drawn from the center of the circle to the end points of the chord tat
defines the segment. [deg]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Radius

The radius of the circle defining the segment.

Color


The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

## Remarks

This function adds a new solid segment shape or modifies an existing shape to be a solid segment
shape in a section designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropSolidSegment()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'createSapModelobject
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "4000Psi")

'add solid segment shape to new property
ret = SapModel.PropFrame.SDShape.SetSolidSegment("SD1", "SH1", "4000Psi", 0, 0, 95, 0,
10, -1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.


## See Also

GetSolidSegment

# SetTee

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetTee

## VB6 Procedure

Function SetTee(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal PropName As String, ByVal XCenter As Double, ByVal YCenter As Double,
ByVal Rotation As Double, Optional ByVal Color As Long = -1, Optional ByVal h As Double =
24, Optional ByVal bf As Double = 24, Optional ByVal tf As Double = 2.4, Optional ByVal tw
As Double = 2.4) As Long

## Parameters

Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Tee property that has been imported from a section
property file.

If this item is a blank string, the section dimensions are taken from the values input in this
function.

If this item is the name of a defined Tee property that has been imported from a section property
file, the section dimensions are taken from the specified Tee property.

If this item is not blank, and the specified property name is not a Tee that was imported from a
section property file, an error is returned.


XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

h

The section depth. [L]

bf

The section width. [L]

tf

The flange thickness. [L]

tw

The web thickness. [L]

## Remarks

This function adds a new Tee shape or modifies an existing shape to be a Tee shape in a section
designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropTee()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Tee shape to new property
ret = SapModel.PropFrame.SDShape.SetTee("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1, 18,
6, 1, 0.5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

GetTee

# SetTube

## Syntax

SapObject.SapModel.PropFrame.SDShape.SetTube

## VB6 Procedure

Function SetTube(ByVal Name As String, ByRef ShapeName As String, ByVal MatProp As
String, ByVal PropName As String, ByVal XCenter As Double, ByVal YCenter As Double,
ByVal Rotation As Double, Optional ByVal Color As Long = -1, Optional ByVal h As Double =
24, Optional ByVal w As Double = 24, Optional ByVal tf As Double = 2.4, Optional ByVal tw As
Double = 2.4) As Long

## Parameters


Name

The name of an existing frame section property that is a section designer section.

ShapeName

The name of an existing or new shape in a section designer property. If this is an existing shape,
that shape is modified; otherwise, a new shape is added.

This item may be input as a blank string, in which case the program will assign a shape name to
the shape and return that name in the ShapeName variable.

MatProp

The name of the material property for the shape.

PropName

This is a blank string or the name of a defined Tube property that has been imported from a
section property file.

If this item is a blank string, the section dimensions are taken from the values input in this
function.

If this item is the name of a defined Tube property that has been imported from a section property
file, the section dimensions are taken from the specified Tube property.

If this item is not blank and the specified property name is not an Tube that was imported from a
section property file, an error is returned.

XCenter

The X-coordinate of the center of the shape in the section designer coordinate system. [L]

YCenter

The Y-coordinate of the center of the shape in the section designer coordinate system. [L]

Rotation

The counter clockwise rotation of the shape from its default orientation. [deg]

Color

The fill color assigned to the shape. If Color is specified as -1, the program will automatically
assign the default fill color.

h

The section height. [L]

w

The section width. [L]

tf


The flange thickness. [L]

tw

The web thickness. [L]

## Remarks

This function adds a new Tube shape or modifies an existing shape to be a Tube shape in a section
designer property.

The function returns zero if the shape is successfully added or modified; otherwise it returns a
nonzero value.

## VBA Example

Sub SetFrameSDPropTube()
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

'add new section designer frame section property
ret = SapModel.PropFrame.SetSDSection("SD1", "A992Fy50")

'add Tube shape to new property
ret = SapModel.PropFrame.SDShape.SetTube("SD1", "SH1", "A992Fy50", "", 0, -9, 0, -1,
18, 6, 1, 0.5)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 12.00.

## See Also

GetTube

# AddMaterial

## Syntax

SapObject.SapModel.PropMaterial.AddMaterial

## VB6 Procedure

Function AddMaterial(ByRef Name As String, ByVal MatType As eMatType, ByVal Region As
String, ByVal Standard As String, ByVal Grade As String, Optional ByVal UserName As String =
"") As Long

## Parameters

Name

This item is returned by the program. It is the name that the program ultimately assigns for the
material property. If no UserName is specified, the program assigns a default name to the material
property. If a UserName is specified and that name is not used for another material property, the
UserName is assigned to the material property.

MatType

This is one of the following items in the eMatType enumeration.

```
eMatType_Steel = 1
eMatType_Concrete = 2
eMatType_NoDesign = 3
eMatType_Aluminum = 4
eMatType_ColdFormed = 5
eMatType_Rebar = 6
eMatType_Tendon = 7
```
Region

The region name of the material property that is user-predefined in the file
"CSiMaterialLibrary*.xml" located in subfolder "Property Libraries" under the CSiBridge
installation.

Standard


The Standard name of the material property with the specified MatType within the specified
region.

Grade

The Grade name of the material property with the specified MatType within the specified region
and Standard.

UserName

This is an optional user specified name for the material property. If a UserName is specified and
that name is already used for another material property, the program ignores the UserName.

## Remarks

This function adds a new material property to the model based on the Code-specified and other pre
-defined material properties defined in the installed file "CSiMaterialLibrary*.xml" located in
subfolder "Property Libraries" under the CSiBridge installation folder.

The function returns zero if the material property is successfully added, otherwise it returns a
nonzero value.

## VBA Example

Sub AddMaterial()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add ASTM A706 rebar material property in United states Region
ret = SapModel.PropMaterial.AddMaterial(Name, eMatType_Rebar, "United States", "ASTM
A706", "Grade 60")

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Updated the documentation of the eMatType enumeration in v22.1.0

Initial release in version 15.2.0.

The function supersedes AddQuick as of version 15.2.0.

# ChangeName

## Syntax

SapObject.SapModel.PropMaterial.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined material property.

NewName

The new name for the material property.

## Remarks

This function changes the name of an existing material property.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeMaterialName()
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'change name of material property
ret = SapModel.PropMaterial.ChangeName("4000Psi", "MatConc")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Count

## Syntax

SapObject.SapModel.PropMaterial.Count

## VB6 Procedure

Function Count(Optional ByVal MatType As eMatType) As Long

## Parameters

MatType

This optional value is one of the following items in the eMatType enumeration.

```
eMatType_Steel = 1
eMatType_Concrete = 2
eMatType_NoDesign = 3
```

```
eMatType_Aluminum = 4
eMatType_ColdFormed = 5
eMatType_Rebar = 6
eMatType_Tendon = 7
```
If no value is input for MatType, a count is returned for all material properties in the model
regardless of type.

## Remarks

This function returns the total number of defined material properties in the model. If desired,
counts can be returned for all material properties of a specified type in the model.

## VBA Example

Sub CountMaterials()
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

'return number of defined materials of all types
Count = SapModel.PropMaterial.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Updated the documentation of the eMatType enumeration in v22.1.0


Initial release in version 11.02.

## See Also

# Delete

## Syntax

SapObject.SapModel.PropMaterial.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing material property.

## Remarks

The function deletes a specified material property.

The function returns zero if the material property is successfully deleted; otherwise it returns a
nonzero value. It returns an error if the specified material property can not be deleted, for example,
if it is being used in a section property.

## VBA Example

Sub DeleteMaterial()
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'delete material
ret = SapModel.PropMaterial.Delete("4000Psi")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetCoupledModelType

## Syntax

SapObject.SapModel.PropMaterial.GetCoupledModelType

## VB6 Procedure

Function GetCoupledModelType(ByVal Name As String, ByRef MatCoupledType As
eMatCoupledType, Optional ByVal Temp As Double = 0.0) As Long

## Parameters

Name

The name of an existing material property.

MatCoupledType

This is one of the following items in the eMatCoupledType enumeration.

```
None = 1
VonMisesPlasticity = 2
ModifiedDarwinPecknoldConcrete = 3
```
Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.


This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the nonlinear coupled modeling type for a specified material

The function returns zero if the assignment data is successfully obtained; otherwise it returns a
nonzero value.

## VBA Example

Sub GetMatCoupledTypeData()

'dimension variables

Dim SapObject as cOAPI

Dim SapModel As cSapModel

Dim ret As Long

Dim MatCoupledType As eMatCoupledType

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


'initialize new material property

ret = SapModel.PropMaterial.SetMaterial("Steel", eMatType.eMatType_Steel, -1, "API
example test", "Default")

'get coupled material type data

ret = SapModel.PropMaterial.GetCoupledModelType("Steel", MatCoupledType)

'close Sap2000

SapObject.ApplicationExit False

Set SapModel = Nothing

Set SapObject = Nothing

End Sub

## Release Notes

Initial release in version 22.1.0

## See Also

SetCoupledModelType

# GetDamping

## Syntax

SapObject.SapModel.PropMaterial.GetDamping

## VB6 Procedure

Function GetDamping(ByVal Name As String, ByRef ModalRatio As Double, ByRef
ViscousMassCoeff As Double, ByRef ViscousStiffCoeff As Double, ByRef HystereticMassCoeff
As Double, ByRef HystereticStiffCoeff As Double, Optional ByVal Temp As Double = 0) As
Long

## Parameters


Name

The name of an existing material property.

ModalRatio

The modal damping ratio.

ViscousMassCoeff

The mass coefficient for viscous proportional damping.

ViscousStiffCoeff

The stiffness coefficient for viscous proportional damping.

HystereticMassCoeff

The mass coefficient for hysteretic proportional damping.

HystereticStiffCoeff

The stiffness coefficient for hysteretic proportional damping.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks

This function retrieves the additional material damping data for the material.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetMatPropDamping()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ModalRatio As Double
Dim ViscousMassCoeff As Double
Dim ViscousStiffCoeff As Double
Dim HystereticMassCoeff As Double
Dim HystereticStiffCoeff As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Conc", MATERIAL_CONCRETE)

'assign material damping data
ret = SapModel.PropMaterial.SetDamping("Conc", 0.04, 0, 0, 0, 0)

'get material damping data
ret = SapModel.PropMaterial.GetDamping("Conc", ModalRatio, ViscousMassCoeff,
ViscousStiffCoeff, HystereticMassCoeff, HystereticStiffCoeff)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

SetDamping

# GetMaterial

## Syntax

SapObject.SapModel.PropMaterial.GetMaterial

## VB6 Procedure


Function GetMaterial(ByVal Name As String, ByRef MatType As eMatType, ByRef Color As
Long, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing material property.

MatType

This is one of the following items in the eMatType enumeration.

```
eMatType_Steel = 1
eMatType_Concrete = 2
eMatType_NoDesign = 3
eMatType_Aluminum = 4
eMatType_ColdFormed = 5
eMatType_Rebar = 6
eMatType_Tendon = 7
```
Color

The display color assigned to the material.

Notes

The notes, if any, assigned to the material.

GUID

The GUID (global unique identifier), if any, assigned to the material.

## Remarks

This function retrieves some basic material property data.

The function returns zero if the material is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetBasicMatPropData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatType As eMatType
Dim Color As Long
Dim Notes As String
Dim GUID As String


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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", eMatType_Steel, -1, "API example test",
"Default")

'get basic material property data
ret = SapModel.PropMaterial.GetMaterial("Steel", MatType, Color, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Updated the documentation of the eMatType enumeration in v22.1.0

Initial release in version 11.02.

## See Also

SetMaterial

# GetMPAnisotropic

## Syntax

SapObject.SapModel.PropMaterial.GetMPAnisotropic

## VB6 Procedure

Function GetMPAnisotropic(ByVal Name As String, ByRef e As Double, ByRef u As Double,
ByRef a As Double, ByRef g As Double, Optional ByVal Temp As Double = 0) As Long


## Parameters

Name

The name of an existing material property.

e

This is an array that includes the modulus of elasticity.

```
e(0) = E1 [F/L^2 ]
e(1) = E2 [F/L^2 ]
e(2) = E3 [F/L^2 ]
```
u

This is an array that includes poisson’s ratio.

```
u(0) = U12
u(1) = U13
u(2) = U23
u(3) = U14
u(4) = U24
u(5) = U34
u(6) = U15
u(7) = U25
u(8) = U35
u(9) = U45
u(10) = U16
u(11) = U26
u(12) = U36
u(13) = U46
u(14) = U56
```
a

This is an array that includes the thermal coefficient.

```
a(0) = A1 [1/T]
a(1) = A2 [1/T]
a(2) = A3 [1/T]
a(3) = A12 [1/T]
a(4) = A13 [1/T]
a(5) = A23 [1/T]
```
g

This is an array that includes the shear modulus.

```
g(0) = G12 [F/L^2 ]
g(1) = G13 [F/L^2 ]
g(2) = G23 [F/L^2 ]
```

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks

This function retrieves the mechanical properties for a material with an anisotropic directional
symmetry type.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the symmetry type of the specified material is not anisotropic.

## VBA Example

Sub GetMatPropAnisotropic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyE() As Double
Dim MyU() As Double
Dim MyA() As Double
Dim MyG() As Double
Dim e() As Double
Dim u() As Double
Dim a() As Double
Dim g() As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign anisotropic mechanical properties
ReDim MyE(2)


ReDim MyU(14)
ReDim MyA(6)
ReDim MyG(2)
MyE(0)=30000
MyE(1)=10000
MyE(2)=2000
MyU(0)=0.2
MyU(1)=0.05
MyU(2)=0.1
MyU(3)=0
MyU(4)=0
MyU(5)=0
MyU(6)=0
MyU(7)=0
MyU(8)=0.01
MyU(9)=0
MyU(10)=0
MyU(11)=0
MyU(12)=0
MyU(13)=0
MyU(14)=0
MyA(0)=6.5E-6
MyA(1)=6.5E-6
MyA(2)=6.5E-6
MyA(3)=6.5E-6
MyA(4)=6.5E-6
MyA(5)=6.5E-6
MyG(0)=1500
MyG(1)=2500
MyG(2)=8700
ret = SapModel.PropMaterial.SetMPAnisotropic("Steel", MyE, MyU, MyA, MyG)

'get anisotropic mechanical properties
ret = SapModel.PropMaterial.GetMPAnisotropic("Steel", e, u, a, g)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetMPAnisotropic


# GetMPIsotropic

## Syntax

SapObject.SapModel.PropMaterial.GetMPIsotropic

## VB6 Procedure

Function GetMPIsotropic(ByVal Name As String, ByRef e As Double, ByRef u As Double,
ByRef a As Double, ByRef g As Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.

e

The modulus of elasticity. [F/L^2 ]

u

Poisson’s ratio.

a

The thermal coefficient. [1/T]

g

The shear modulus. For isotropic materials this value is program calculated from the modulus of
elasticity and poisson’s ratio. [F/L^2 ]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the mechanical properties for a material with an isotropic directional
symmetry type.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the symmetry type of the specified material is not isotropic.


## VBA Example

Sub GetMatPropIsotropic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim e As Double
Dim u As Double
Dim a As Double
Dim g As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign isotropic mechanical properties
ret = SapModel.PropMaterial.SetMPIsotropic("Steel", 29500, 0.25, 6E-06)

'get isotropic mechanical properties
ret = SapModel.PropMaterial.GetMPIsotropic("Steel", e, u, a, g)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetMPIsotropic


# GetMPOrthotropic

## Syntax

SapObject.SapModel.PropMaterial.GetMPOrthotropic

## VB6 Procedure

Function GetMPOrthotropic(ByVal Name As String, ByRef e As Double, ByRef u As Double,
ByRef a As Double, ByRef g As Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.

e

This is an array that includes the modulus of elasticity.

```
e(0) = E1 [F/L^2 ]
e(1) = E2 [F/L^2 ]
e(2) = E3 [F/L^2 ]
```
u

This is an array that includes poisson’s ratio.

```
u(0) = U12
u(1) = U13
u(2) = U23
```
a

This is an array that includes the thermal coefficient.

```
a(0) = A1 [1/T]
a(1) = A2 [1/T]
a(2) = A3 [1/T]
```
g

This is an array that includes the shear modulus.

```
g(0) = G12 [F/L^2 ]
g(1) = G13 [F/L^2 ]
g(2) = G23 [F/L^2 ]
```
Temp


This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the mechanical properties for a material with an orthotropic directional
symmetry type.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the symmetry type of the specified material is not orthotropic.

## VBA Example

Sub GetMatPropOrthotropic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyE() As Double
Dim MyU() As Double
Dim MyA() As Double
Dim MyG() As Double
Dim e() As Double
Dim u() As Double
Dim a() As Double
Dim g() As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign orthotropic mechanical properties
ReDim MyE(2)
ReDim MyU(2)
ReDim MyA(2)


ReDim MyG(2)
MyE(0)=30000
MyE(1)=10000
MyE(2)=2000
MyU(0)=0.2
MyU(1)=0.05
MyU(2)=0.1
MyA(0)=6.5E-6
MyA(1)=6.5E-6
MyA(2)=6.5E-6
MyG(0)=1500
MyG(1)=2500
MyG(2)=8700
ret = SapModel.PropMaterial.SetMPOrthotropic("Steel", MyE, MyU, MyA, MyG)

'get orthotropic mechanical properties
ret = SapModel.PropMaterial.GetMPOrthotropic("Steel", e, u, a, g)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetMPOrthotropic

# GetMPUniaxial

## Syntax

SapObject.SapModel.PropMaterial.GetMPUniaxial

## VB6 Procedure

Function GetMPUniaxial(ByVal Name As String, ByRef e As Double, ByRef a As Double,
Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.


e

The modulus of elasticity. [F/L^2 ]

a

The thermal coefficient. [1/T]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks

This function retrieves the mechanical properties for a material with a uniaxial directional
symmetry type.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the symmetry type of the specified material is not uniaxial.

## VBA Example

Sub GetMatPropUniaxial()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim e As Double
Dim a As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Rebar", MATERIAL_REBAR)


'assign uniaxial mechanical properties
ret = SapModel.PropMaterial.SetMPUniaxial("Rebar", 28500, 6E-06)

'get uniaxial mechanical properties
ret = SapModel.PropMaterial.GetMPUniaxial("Rebar", e, a)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetMPUniaxial

# GetNameList

## Syntax

SapObject.SapModel.PropMaterial.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String, Optional
ByVal MatType As eMatType) As Long

## Parameters

NumberNames

The number of material property names retrieved by the program.

MyName

This is a one-dimensional array of material property names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

MatType


This optional value is one of the following items in the eMatType enumeration.

```
eMatType_Steel = 1
eMatType_Concrete = 2
eMatType_NoDesign = 3
eMatType_Aluminum = 4
eMatType_ColdFormed = 5
eMatType_Rebar = 6
eMatType_Tendon = 7
```
If no value is input for MatType, names are returned for all material properties in the model
regardless of type.

## Remarks

This function retrieves the names of all defined material properties of the specified type.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetMaterialNames()
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

'get material property names
ret = SapModel.PropMaterial.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Updated the documentation of the eMatType enumeration in v22.1.0

Initial release in version 11.02.

## See Also

# GetOAluminum

## Syntax

SapObject.SapModel.PropMaterial.GetOAluminum

## VB6 Procedure

Function GetOAluminum(ByVal Name As String, ByVal MyType As Long, ByRef Alloy As
String, ByRef Fcy As Double, ByRef Fty As Double, ByRef Ftu As Double, ByRef Fsu As
Double, ByRef SSHysType As Long, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing aluminum material property.

MyType

This is 1, 2 or 3, indicating the type of aluminum.

```
1 = Wrought
2 = Cast-Mold
3 = Cast-Sand
```
Alloy

The Alloy designation for the aluminum, for example, 2014-T6 for wrought or 356.0-T7 for cast
(mold or sand) aluminum.

Fcy

The compressive yield strength of aluminum. [F/L^2 ]

Fty

The tensile yield strength of aluminum. [F/L^2 ]


Ftu

The tensile ultimate strength of aluminum. [F/L^2 ]

Fsu

The shear ultimate strength of aluminum. [F/L^2 ]

SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the other material property data for aluminum materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not aluminum.

## VBA Example

Sub GetMatPropAluminumData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyType As Long
Dim Alloy As String
Dim Fcy As Double
Dim Fty As Double
Dim Ftu As Double
Dim Fsu As Double
Dim SSHysType As Long

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Aluminum", MATERIAL_ALUMINUM)

'assign other properties
ret = SapModel.PropMaterial.SetOAluminum("Aluminum", 1, "2014-T6", 34, 34, 37, 23, 2)

'get other properties
ret = SapModel.PropMaterial.GetOAluminum("Aluminum", MyType, Alloy, Fcy, Fty, Ftu,
Fsu, SSHysType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetOAluminum

# GetOColdFormed

## Syntax

SapObject.SapModel.PropMaterial.GetOColdFormed

## VB6 Procedure

Function GetOColdFormed(ByVal Name As String, ByRef Fy As Double, ByRef Fu As Double,
ByRef SSHysType As Long, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing cold formed material property.


Fy

The minimum yield stress. [F/L^2 ]

Fu

The minimum tensile stress. [F/L^2 ]

SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the other material property data for cold formed materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not cold formed.

## VBA Example

Sub GetMatPropColdFormedData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Fy As Double
Dim Fu As Double
Dim SSHysType As Long

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("ColdFormed", MATERIAL_COLDFORMED)

'assign other properties
ret = SapModel.PropMaterial.SetOColdFormed("ColdFormed", 52, 67, 1)

'get other properties
ret = SapModel.PropMaterial.GetOColdFormed("ColdFormed", Fy, Fu, SSHysType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetOColdFormed

# GetOConcrete_1

## Syntax

SapObject.SapModel.PropMaterial.GetOConcrete_1

## VB6 Procedure

Function GetOConcrete_1(ByVal Name As String, ByRef fc As Double, ByRef IsLightweight As
Boolean, ByRef fcsfactor As Double, ByRef SSType As Long, ByRef SSHysType As Long,
ByRef StrainAtfc As Double, ByRef StrainUltimate As Double, ByRef FinalSlope As Double,
ByRef FrictionAngle As Double, ByRef DilatationalAngle As Double, Optional ByVal Temp As
Double = 0) As Long

## Parameters

Name

The name of an existing concrete material property.

fc


The concrete compressive strength. [F/L^2 ]

IsLightweight

If this item is True, the concrete is assumed to be lightweight concrete.

fcsfactor

The shear strength reduction factor for lightweight concrete.

SSType

This is 0, 1 or 2, indicating the stress-strain curve type.

```
0 = User defined
1 = Parametric - Simple
2 = Parametric - Mander
```
SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
StrainAtfc

This item applies only to parametric stress-strain curves. It is the strain at the unconfined
compressive strength.

StrainUltimate

This item applies only to parametric stress-strain curves. It is the ultimate unconfined strain
capacity.

FinalSlope

This item applies only to parametric stress-strain curves. It is a multiplier on the material modulus
of elasticity, E. This value multiplied times E gives the final slope on the compression side of the
curve.

FrictionAngle

The Drucker-Prager friction angle, 0 <= FrictionAngle < 90. [deg]

DilatationalAngle

The Drucker-Prager dilatational angle, 0 <= DilatationalAngle < 90. [deg]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.


This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the other material property data for concrete materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not concrete.

## VBA Example

Sub GetMatPropConcreteData_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim fc As Double
Dim IsLightweight As Boolean
Dim fcsfactor As Double
Dim SSType As Long
Dim SSHysType As Long
Dim StrainAtfc As Double
Dim StrainUltimate As Double
Dim FinalSlope As Double
Dim FrictionAngle As Double
Dim DilatationalAngle As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Concrete", MATERIAL_CONCRETE)

'assign other properties
ret = SapModel.PropMaterial.SetOConcrete_1("Concrete", 5, False, 0, 1, 2, 0.0022, 0.0052, -
0.1)

'get other properties


ret = SapModel.PropMaterial.GetOConcrete_1("Concrete", fc, IsLightweight, fcsfactor,
SSType, SSHysType, StrainAtfc, StrainUltimate, FinalSlope, FrictionAngle, DilatationalAngle)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

This function supersedes GetOConcrete.

## See Also

SetOConcrete_1

# GetONoDesign

## Syntax

SapObject.SapModel.PropMaterial.GetONoDesign

## VB6 Procedure

Function GetONoDesign(ByVal Name As String, ByRef FrictionAngle As Double, ByRef
DilatationalAngle As Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing concrete material property.

FrictionAngle

The Drucker-Prager friction angle, 0 <= FrictionAngle < 90. [deg]

DilatationalAngle

The Drucker-Prager dilatational angle, 0 <= DilatationalAngle < 90. [deg]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.


This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the other material property data for no design type materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not concrete.

## VBA Example

Sub GetMatPropNoDesignData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FrictionAngle As Double
Dim DilatationalAngle As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("NoDesign", MATERIAL_NODESIGN)

'assign other properties
ret = SapModel.PropMaterial.SetONoDesign("NoDesign", 10, 15)

'get other properties
ret = SapModel.PropMaterial.GetONoDesign("NoDesign", FrictionAngle, DilatationalAngle)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

SetONoDesign

# GetORebar_1

## Syntax

SapObject.SapModel.PropMaterial.GetORebar_1

## VB6 Procedure

Function GetORebar_1(ByVal Name As String, ByRef Fy As Double, ByRef Fu As Double,
ByRef eFy As Double, ByRef eFu As Double, ByRef SSType As Long, ByRef SSHysType As
Long, ByRef StrainAtHardening As Double, ByRef StrainUltimate As Double, ByRef FinalSlope
As Double, ByRef UseCaltransSSDefaults As Boolean, Optional ByVal Temp As Double = 0) As
Long

## Parameters

Name

The name of an existing rebar material property.

Fy

The minimum yield stress. [F/L^2 ]

Fu

The minimum tensile stress. [F/L^2 ]

eFy

The expected yield stress. [F/L^2 ]

eFu

The expected tensile stress. [F/L^2 ]

SSType

This is 0, 1 or 2, indicating the stress-strain curve type.

```
0 = User defined
```

```
1 = Parametric - Simple
2 = Parametric - Park
```
SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
StrainAtHardening

This item applies only when parametric stress-strain curves are used and when
UseCaltransSSDefaults is False. It is the strain at the onset of strain hardening.

StrainUltimate

This item applies only when parametric stress-strain curves are used and when
UseCaltransSSDefaults is False. It is the ultimate strain capacity. This item must be larger than the
StrainAtHardening item.

FinalSlope

This item applies only to parametric stress-strain curves. It is a multiplier on the material modulus
of elasticity, E. This value multiplied times E gives the final slope of the curve.

UseCaltransSSDefaults

If this item is True, the program uses Caltrans default controlling strain values, which are bar size
dependent.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the other material property data for rebar materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not rebar.

## VBA Example

Sub GetMatPropRebarData_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim Fy As Double
Dim Fu As Double
Dim eFy As Double
Dim eFu As Double
Dim SSType As Long
Dim SSHysType As Long
Dim StrainAtHardening As Double
Dim StrainUltimate As Double
Dim FinalSlope As Double
Dim UseCaltransSSDefaults As Boolean

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Rebar", MATERIAL_REBAR)

'assign other properties
ret = SapModel.PropMaterial.SetORebar_1("Rebar", 62, 93, 70, 102, 2, 2, 0.02, 0.1, -0.1,
False)

'get other properties
ret = SapModel.PropMaterial.GetORebar_1("Rebar", Fy, Fu, eFy, eFu, SSType, SSHysType,
StrainAtHardening, StrainUltimate, FinalSlope, UseCaltransSSDefaults)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

This function supersedes GetORebar.


## See Also

SetORebar_1

# GetOSteel_1

## Syntax

SapObject.SapModel.PropMaterial.GetOSteel_1

## VB6 Procedure

Function GetOSteel_1(ByVal Name As String, ByRef Fy As Double, ByRef Fu As Double,
ByRef eFy As Double, ByRef eFu As Double, ByRef SSType As Long, ByRef SSHysType As
Long, ByRef StrainAtHardening As Double, ByRef StrainAtMaxStress As Double, ByRef
StrainAtRupture As Double, ByRef FinalSlope As Double, Optional ByVal Temp As Double = 0)
As Long

## Parameters

Name

The name of an existing steel material property.

Fy

The minimum yield stress. [F/L^2 ]

Fu

The minimum tensile stress. [F/L^2 ]

eFy

The expected yield stress. [F/L^2 ]

eFu

The expected tensile stress. [F/L^2 ]

SSType

This is 0 or 1. indicating the stress-strain curve type.

```
0 = User defined
1 = Parametric - Simple
```
SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.


```
0 = Elastic
1 = Kinematic
2 = Takeda
```
StrainAtHardening

This item applies only to parametric stress-strain curves. It is the strain at the onset of strain
hardening.

StrainAtMaxStress

This item applies only to parametric stress-strain curves. It is the strain at maximum stress.

StrainAtRupture

This item applies only to parametric stress-strain curves. It is the strain at rupture.

FinalSlope

This item applies only to parametric stress-strain curves. It is a multiplier on the material modulus
of elasticity, E. This value multiplied times E gives the final slope of the curve.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the other material property data for steel materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not steel.

## VBA Example

Sub GetMatPropSteelData_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Fy As Double
Dim Fu As Double
Dim eFy As Double
Dim eFu As Double
Dim SSType As Long
Dim SSHysType As Long
Dim StrainAtHardening As Double
Dim StrainAtMaxStress As Double
Dim StrainAtRupture As Double


Dim FinalSlope As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign other properties
ret = SapModel.PropMaterial.SetOSteel_1("Steel", 55, 68, 60, 70, 1, 2, 0.02, 0.1, 0.2, -0.1)

'get other properties
ret = SapModel.PropMaterial.GetOSteel_1("Steel", Fy, Fu, eFy, eFu, SSType, SSHysType,
StrainAtHardening, StrainAtMaxStress, StrainAtRupture, FinalSlope)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

This function supersedes GetOSteel.

## See Also

SetOSteel_1

# GetOTendon_1

## Syntax

SapObject.SapModel.PropMaterial.GetOTendon_1


## VB6 Procedure

Function GetOTendon_1(ByVal Name As String, ByRef Fy As Double, ByRef Fu As Double,
ByRef SSType As Long, ByRef SSHysType As Long, ByRef FinalSlope As Double, Optional
ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing tendon material property.

Fy

The minimum yield stress. [F/L^2 ]

Fu

The minimum tensile stress. [F/L^2 ]

SSType

This is 0, 1 or 2, indicating the stress-strain curve type.

```
0 = User defined
1 = Parametric – 250 ksi strand
2 = Parametric – 270 ksi strand
```
SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
FinalSlope

This item applies only to parametric stress-strain curves. It is a multiplier on the material modulus
of elasticity, E. This value multiplied times E gives the final slope of the curve.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the other material property data for tendon materials.


The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not tendon.

## VBA Example

Sub GetMatPropTendonData_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Fy As Double
Dim Fu As Double
Dim SSType As Long
Dim SSHysType As Long
Dim FinalSlope As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Tendon", MATERIAL_TENDON)

'assign other properties
ret = SapModel.PropMaterial.SetOTendon_1("Tendon", 230, 255, 1, 1, -0.1)

'get other properties
ret = SapModel.PropMaterial.GetOTendon_1("Tendon", Fy, Fu, SSType, SSHysType,
FinalSlope)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.


This function supersedes GetOTendon.

## See Also

SetOTendon_1

# GetSSCurve

## Syntax

SapObject.SapModel.PropMaterial.GetSSCurve

## VB6 Procedure

Function GetMPIsotropic(ByVal Name As String, ByRef NumberPoints As Long, ByRef PointID
() As Long, ByRef Strain() As Double, ByRef Stress() As Double, Optional ByVal SectName As
String = "", Optional ByVal RebarArea As Double = 0, Optional ByVal Temp As Double = 0) As
Long

## Parameters

Name

The name of an existing material property.

NumberPoints

The number of points in the stress-strain curve.

PointID

This is one of the following integers which sets the point ID. The point ID controls the color that
will be displayed for hinges in a deformed shape plot.

```
-5 = -E
-4 = -D
-3 = -C
-2 = -B
0 = None
1 = A
2 = B
3 = C
4 = D
5 = E
```
Strain

This is an array that includes the strain at each point on the stress strain curve.


Stress

This is an array that includes the stress at each point on the stress strain curve. [F/L^2 ]

SectName

This item applies only if the specified material is concrete with a Mander concrete type.

This is the frame section property for which the Mander stress-strain curve is retrieved.

The section must be round or rectangular.

RebarArea

This item applies only if the specified material is rebar, which does not have a user-defined stress-
strain curve and is specified to use Caltrans default controlling strain values, which are bar size
dependent.

This is the area of the rebar for which the stress-strain curve is retrieved.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the material stress-strain curve.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

```
Sub GetMatPropSSCurve()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberPoints As Long
Dim PointID() As Long
Dim Strain() As Double
Dim Stress() As Double
```
```
'create Sap2000 object
Set SapObject = CreateObject
("CSI.SAP2000.API.SapObject")
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2,
288)
```
```
'get stress strain curve
ret = SapModel.PropMaterial.GetSSCurve("A992Fy50",
NumberPoints, PointID, Strain, Stress)
```
```
'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub
```
## Release Notes

Initial release in version 11.02.

## See Also

SetSSCurve

# GetTemp

## Syntax

SapObject.SapModel.PropMaterial.GetTemp

## VB6 Procedure

Function GetTemp(ByVal Name As String, ByRef NumberItems as long, ByRef Temp() As
Double) As Long

## Parameters

Name

The name of a material property.

NumberItems

The number of different temperatures at which properties are specified for the material.


Temp

This is an array that includes the different temperatures at which properties are specified for the
material.

## Remarks

This function retrieves the temperatures at which properties are specified for a material.

The function returns zero if the temperatures are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetMatPropTemps()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim MyTemp() As Double
Dim Temp() As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'specify temps at which properties will be provided
ReDim MyTemp(2)
MyTemp(0) = 0
MyTemp(1) = 50
MyTemp(2) = 100
ret = SapModel.PropMaterial.SetTemp("Steel", 3, MyTemp)

'get temps at which properties are provided
ret = SapModel.PropMaterial.GetTemp("Steel", NumberItems, Temp)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetTemp

# GetTypeOAPI

## Syntax

SapObject.SapModel.PropMaterial.GetTypeOAPI

## VB6 Procedure

Function GetTypeOAPI(ByVal Name As String, ByRef MatType As eMatType, ByRef SymType
As Long) As Long

## Parameters

Name

The name of an existing material property.

MatType

This is one of the following items in the eMatType enumeration.

```
eMatType_Steel = 1
eMatType_Concrete = 2
eMatType_NoDesign = 3
eMatType_Aluminum = 4
eMatType_ColdFormed = 5
eMatType_Rebar = 6
eMatType_Tendon = 7
```
SymType

This is 0, 1, 2 or 3, indicating the material directional symmetry type.

```
0 = Isotropic
1 = Orthotropic
```

```
2 = Anisotropic
3 = Uniaxial
```
## Remarks

This function retrieves the material type for the specified material.

The function returns zero if the type is successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetMaterialType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatType As eMatType
Dim SymType As Long

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

'get material type
ret = SapModel.PropMaterial.GetTypeOAPI("4000Psi", MatType, SymType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Updated the documentation of the eMatType enumeration in v22.1.0

Initial release in version 11.02.

Changed function name to GetTypeOAPI in v17.0.0.


## See Also

# GetVonMisesPlasticityParameters

## Syntax

SapObject.SapModel.PropMaterial.GetVonMisesPlasticityParameters

## VB6 Procedure

Function GetVonMisesPlasticityParameters(ByVal Name As String, ByRef UseIsoLinHardening
As Boolean, ByRef IsoLinHardeningModulus As Double, ByRef UseIsoNLHardening As
Boolean, ByRef IsoNLUltimateStressRatio As Double, ByRef IsoNLHardeningRate As Double,
ByRef UseKinLinHardening As Boolean, ByRef KinLinHardeningModulus As Double, ByRef
YieldStress As Double, Optional ByVal Temp As Double = 0.0) As Long

## Parameters

Name

The name of an existing material property.

UseIsoLinHardening

If this item is True, the linear isotropic hardening is enabled.

IsoLinHardeningModulus

The linear isotropic hardening modulus, used if UseIsoLinHardening = True.

UseIsoNLHardening

If this item is True, the nonlinear isotropic saturation hardening is enabled.

IsoNLUltimateStressRatio

The ultimate stress as a ratio of the yield stress, used if UseIsoNLHardening = True.

IsoNLHardeningRate

The hardening rate parameter, used if UseIsoNLHardening = True.

UseKinLinHardening

If this item is True, the linear kinematic hardening is enabled.

KinLinHardeningModulus

The linear kinematic hardening modulus, used if UseKinLinHardening = True.

YieldStress


The yield stress.

This item applies only if the specified material has a material type of eMatType.NoDesign.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function gets the Von Mises Plasticity coupled modeling parameters for a specified material

The function returns zero if the assignment data is successfully obtained; otherwise it returns a
nonzero value.

## VBA Example

Sub GetMatCoupledTypeData()

'dimension variables

Dim SapObject as cOAPI

Dim SapModel As cSapModel

Dim UseIsoLinHardening As Boolean

Dim IsoLinHardeningModulus As Double

Dim UseIsoNLHardening As Boolean

Dim IsoNLUltimateStressRatio As Double

Dim IsoNLHardeningRate As Double

Dim UseKinLinHardening As Boolean

Dim KinLinHardeningModulus As Double

Dim YieldStress As Double

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

'initialize new material property

ret = SapModel.PropMaterial.SetMaterial("Steel", eMatType.eMatType_Steel, -1, "API
example test", "Default")

'set coupled material type data

ret = SapModel.PropMaterial.SetCoupledModelType("Steel",
eMatCoupledType.eMatCoupledType_VonMisesPlasticity)

'get Von Mises Plasticity data

ret = SapModel.PropMaterial.GetVonMisesPlasticityParameters ("Steel",
UseIsoLinHardening, IsoLinHardeningModulus, UseIsoNLHardening, IsoNLUltimateStressRatio,
IsoNLHardeningRate, UseKinLinHardening, KinLinHardeningModulus, YieldStress)

'close Sap2000

SapObject.ApplicationExit False

Set SapModel = Nothing

Set SapObject = Nothing

End Sub


## Release Notes

Initial release in version 22.1.0

## See Also

GetCoupledModelType

SetCoupledModelType

SetVonMisesPlasticityParameters

# GetWeightAndMass

## Syntax

SapObject.SapModel.PropMaterial.GetWeightAndMass

## VB6 Procedure

Function GetWeightAndMass(ByVal Name As String, ByRef w As Double, ByRef m As Double,
Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.

w

The weight per unit volume for the material. [F/L^3 ]

m

The mass per unit volume for the material. [M/L^3 ]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function retrieves the weight per unit volume and mass per unit volume of the material.


The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetMatPropWeightAndMass()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim w As Double
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign material property weight per unit volume
ret = SapModel.PropMaterial.SetWeightAndMass("Steel", 1, 0.00029)

'get material weight and mass per unit volume
ret = SapModel.PropMaterial.GetWeightAndMass("Steel", w, m)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetWeightAndMass


# SetCoupledModelType

## Syntax

SapObject.SapModel.PropMaterial.SetCoupledModelType

## VB6 Procedure

Function SetCoupledModelType(ByVal Name As String, ByVal MatCoupledType As
eMatCoupledType, Optional ByVal Temp As Double = 0.0) As Long

## Parameters

Name

The name of an existing material property.

MatCoupledType

This is one of the following items in the eMatCoupledType enumeration.

```
None = 1
VonMisesPlasticity = 2
ModifiedDarwinPecknoldConcrete = 3
```
Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function sets the nonlinear coupled modeling type for a specified material

The function returns zero if the assignment data is successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetMatCoupledTypeData()

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

'initialize new material property

ret = SapModel.PropMaterial.SetMaterial("Steel", eMatType.eMatType_Steel, -1, "API
example test", "Default")

'set coupled material type data

ret = SapModel.PropMaterial.SetCoupledModelType("Steel",
eMatCoupledType.eMatCoupledType_VonMisesPlasticity)

'close Sap2000

SapObject.ApplicationExit False

Set SapModel = Nothing

Set SapObject = Nothing


End Sub

## Release Notes

Initial release in version 22.1.0

## See Also

GetCoupledModelType

# SetDamping

## Syntax

SapObject.SapModel.PropMaterial.SetDamping

## VB6 Procedure

Function SetDamping(ByVal Name As String, ByVal ModalRatio As Double, ByVal
ViscousMassCoeff As Double, ByVal ViscousStiffCoeff As Double, ByVal HystereticMassCoeff
As Double, ByVal HystereticStiffCoeff As Double, Optional ByVal Temp As Double = 0) As
Long

## Parameters

Name

The name of an existing material property.

ModalRatio

The modal damping ratio.

ViscousMassCoeff

The mass coefficient for viscous proportional damping.

ViscousStiffCoeff

The stiffness coefficient for viscous proportional damping.

HystereticMassCoeff

The mass coefficient for hysteretic proportional damping.

HystereticStiffCoeff

The stiffness coefficient for hysteretic proportional damping.

Temp


This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
previously defined for the material.

## Remarks

This function sets the additional material damping data for the material.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropDamping()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Conc", MATERIAL_CONCRETE)

'assign material damping data
ret = SapModel.PropMaterial.SetDamping("Conc", 0.04, 0, 0, 0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.


## See Also

GetDamping

# SetMaterial

## Syntax

SapObject.SapModel.PropMaterial.SetMaterial

## VB6 Procedure

Function SetMaterial(ByVal Name As String, ByVal MatType As eMatType, Optional ByVal
Color As Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "")
As Long

## Parameters

Name

The name of an existing or new material property. If this is an existing property, that property is
modified; otherwise, a new property is added.

MatType

This is one of the following items in the eMatType enumeration.

```
eMatType_Steel = 1
eMatType_Concrete = 2
eMatType_NoDesign = 3
eMatType_Aluminum = 4
eMatType_ColdFormed = 5
eMatType_Rebar = 6
eMatType_Tendon = 7
```
Color

The display color assigned to the material. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the material.

GUID

The GUID (global unique identifier), if any, assigned to the material. If this item is input as
Default, the program assigns a GUID to the material.


## Remarks

This function initializes a material property. If this function is called for an existing material
property, all items for the material are reset to their default value.

The function returns zero if the material is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub InitializeMatProp()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", eMatType_Steel)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Updated the documentation of the eMatType enumeration in v22.1.0

Initial release in version 11.02.

## See Also

GetMaterial


# SetMPAnisotropic

## Syntax

SapObject.SapModel.PropMaterial.SetMPAnisotropic

## VB6 Procedure

Function SetMPAnisotropic(ByVal Name As String, ByRef e() As Double, ByRef u() As Double,
ByRef a() As Double, ByRef g() As Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.

e

This is an array that includes the modulus of elasticity.

```
e(0) = E1 [F/L^2 ]
e(1) = E2 [F/L^2 ]
e(2) = E3 [F/L^2 ]
```
u

This is an array that includes poisson’s ratio.

```
u(0) = U12
u(1) = U13
u(2) = U23
u(3) = U14
u(4) = U24
u(5) = U34
u(6) = U15
u(7) = U25
u(8) = U35
u(9) = U45
u(10) = U16
u(11) = U26
u(12) = U36
u(13) = U46
u(14) = U56
```
a

```
This is an array that includes the thermal coefficient.
```
```
a(0) = A1 [1/T]
a(1) = A2 [1/T]
```

```
a(2) = A3 [1/T]
a(3) = A12 [1/T]
a(4) = A13 [1/T]
a(5) = A23 [1/T]
```
g

This is an array that includes the shear modulus.

```
g(0) = G12 [F/L^2 ]
g(1) = G13 [F/L^2 ]
g(2) = G23 [F/L^2 ]
```
Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the material directional symmetry type to anisotropic, and assigns the
anisotropic mechanical properties.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropAnisotropic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyE() As Double
Dim MyU() As Double
Dim MyA() As Double
Dim MyG() As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign anisotropic mechanical properties
ReDim MyE(2)
ReDim MyU(14)
ReDim MyA(6)
ReDim MyG(2)
MyE(0)=30000
MyE(1)=10000
MyE(2)=2000
MyU(0)=0.2
MyU(1)=0.05
MyU(2)=0.1
MyU(3)=0
MyU(4)=0
MyU(5)=0
MyU(6)=0
MyU(7)=0
MyU(8)=0.01
MyU(9)=0
MyU(10)=0
MyU(11)=0
MyU(12)=0
MyU(13)=0
MyU(14)=0
MyA(0)=6.5E-6
MyA(1)=6.5E-6
MyA(2)=6.5E-6
MyA(3)=6.5E-6
MyA(4)=6.5E-6
MyA(5)=6.5E-6
MyG(0)=1500
MyG(1)=2500
MyG(2)=8700
ret = SapModel.PropMaterial.SetMPAnisotropic("Steel", MyE, MyU, MyA, MyG)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

GetMPAnisotropic

# SetMPIsotropic

## Syntax

SapObject.SapModel.PropMaterial.SetMPIsotropic

## VB6 Procedure

Function SetMPIsotropic(ByVal Name As String, ByVal e As Double, ByVal u As Double,
ByVal a As Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.

e

The modulus of elasticity. [F/L^2 ]

u

Poisson’s ratio.

a

The thermal coefficient. [1/T]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the material directional symmetry type to isotropic, and assigns the isotropic
mechanical properties.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.


## VBA Example

Sub AssignMatPropIsotropic()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign isotropic mechanical properties
ret = SapModel.PropMaterial.SetMPIsotropic("Steel", 29500, 0.25, 6E-06)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetMPIsotropic

# SetMPOrthotropic

## Syntax

SapObject.SapModel.PropMaterial.SetMPOrthotropic


## VB6 Procedure

Function SetMPOrthotropic(ByVal Name As String, ByRef e() As Double, ByRef u() As Double,
ByRef a() As Double, ByRef g() As Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.

e

This is an array that includes the modulus of elasticity.

```
e(0) = E1 [F/L^2 ]
e(1) = E2 [F/L^2 ]
e(2) = E3 [F/L^2 ]
```
u

This is an array that includes poisson’s ratio.

```
u(0) = U12
u(1) = U13
u(2) = U23
```
a

```
This is an array that includes the thermal coefficient.
```
```
a(0) = A1 [1/T]
a(1) = A2 [1/T]
a(2) = A3 [1/T]
```
g

This is an array that includes the shear modulus.

```
g(0) = G12 [F/L^2 ]
g(1) = G13 [F/L^2 ]
g(2) = G23 [F/L^2 ]
```
Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks


This function sets the material directional symmetry type to orthotropic, and assigns the
orthotropic mechanical properties.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropOrthotropic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyE() As Double
Dim MyU() As Double
Dim MyA() As Double
Dim MyG() As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign orthotropic mechanical properties
ReDim MyE(2)
ReDim MyU(2)
ReDim MyA(2)
ReDim MyG(2)
MyE(0)=30000
MyE(1)=10000
MyE(2)=2000
MyU(0)=0.2
MyU(1)=0.05
MyU(2)=0.1
MyA(0)=6.5E-6
MyA(1)=6.5E-6
MyA(2)=6.5E-6
MyG(0)=1500
MyG(1)=2500
MyG(2)=8700


ret = SapModel.PropMaterial.SetMPOrthotropic("Steel", MyE, MyU, MyA, MyG)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetMPOrthotropic

# SetMPUniaxial

## Syntax

SapObject.SapModel.PropMaterial.SetMPUniaxial

## VB6 Procedure

Function SetMPUniaxial(ByVal Name As String, ByVal e As Double, ByVal a As Double,
Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.

e

The modulus of elasticity. [F/L^2 ]

a

The thermal coefficient. [1/T]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.


## Remarks

This function sets the material directional symmetry type to uniaxial, and assigns the uniaxial
mechanical properties.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropUniaxial()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Rebar", MATERIAL_REBAR)

'assign uniaxial mechanical properties
ret = SapModel.PropMaterial.SetMPUniaxial("Rebar", 28500, 6E-06)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetMPUniaxial


# SetOAluminum

## Syntax

SapObject.SapModel.PropMaterial.SetOAluminum

## VB6 Procedure

Function SetOAluminum(ByVal Name As String, ByVal MyType As Long, ByVal Alloy As
String, ByVal Fcy As Double, ByVal Fty As Double, ByVal Ftu As Double, ByVal Fsu As
Double, ByVal SSHysType As Long, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing aluminum material property.

MyType

This is 1, 2 or 3, indicating the type of aluminum.

```
1 = Wrought
2 = Cast-Mold
3 = Cast-Sand
```
Alloy

The Alloy designation for the aluminum, for example, 2014-T6 for wrought or 356.0-T7 for cast
(mold or sand) aluminum.

Fcy

The compressive yield strength of aluminum. [F/L^2 ]

Fty

The tensile yield strength of aluminum. [F/L^2 ]

Ftu

The tensile ultimate strength of aluminum. [F/L^2 ]

Fsu

The shear ultimate strength of aluminum. [F/L^2 ]

SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
```

```
1 = Kinematic
2 = Takeda
```
Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the other material property data for aluminum materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropAluminumData()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Aluminum", MATERIAL_ALUMINUM)

'assign other properties
ret = SapModel.PropMaterial.SetOAluminum("Aluminum", 1, "2014-T6", 34, 34, 37, 23, 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

GetOAluminum

# SetOColdFormed

## Syntax

SapObject.SapModel.PropMaterial.SetOColdFormed

## VB6 Procedure

Function SetOColdFormed(ByVal Name As String, ByVal Fy As Double, ByVal Fu As Double,
ByVal SSHysType As Long, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing cold formed material property.

Fy

The minimum yield stress. [F/L^2 ]

Fu

The minimum tensile stress. [F/L^2 ]

SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.


## Remarks

This function sets the other material property data for cold formed materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropColdFormedData()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("ColdFormed", MATERIAL_COLDFORMED)

'assign other properties
ret = SapModel.PropMaterial.SetOColdFormed("ColdFormed", 52, 67, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetOColdFormed


# SetOConcrete_1

## Syntax

SapObject.SapModel.PropMaterial.SetOConcrete_1

## VB6 Procedure

Function SetOConcrete_1(ByVal Name As String, ByVal fc As Double, ByVal IsLightweight As
Boolean, ByVal fcsfactor As Double, ByVal sstype As Long, ByVal SSHysType As Long, ByVal
StrainAtfc As Double, ByVal StrainUltimate As Double, ByVal FinalSlope As Double, Optional
ByVal FrictionAngle As Double = 0, Optional ByVal DilatationalAngle As Double = 0, Optional
ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing concrete material property.

fc

The concrete compressive strength. [F/L^2 ]

IsLightweight

If this item is True, the concrete is assumed to be lightweight concrete.

fcsfactor

The shear strength reduction factor for lightweight concrete.

SSType

This is 0, 1 or 2, indicating the stress-strain curve type.

```
0 = User defined
1 = Parametric - Simple
2 = Parametric - Mander
```
SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
StrainAtfc

This item applies only to parametric stress-strain curves. It is the strain at the unconfined
compressive strength.


StrainUltimate

This item applies only to parametric stress-strain curves. It is the ultimate unconfined strain
capacity. This item must be larger than the StrainAtfc item.

FinalSlope

This item applies only to parametric stress-strain curves. It is a multiplier on the material modulus
of elasticity, E. This value multiplied times E gives the final slope on the compression side of the
curve.

FrictionAngle

The Drucker-Prager friction angle, 0 <= FrictionAngle < 90. [deg]

DilatationalAngle

The Drucker-Prager dilatational angle, 0 <= DilatationalAngle < 90. [deg]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the other material property data for concrete materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropConcreteData_1()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Concrete", MATERIAL_CONCRETE)

'assign other properties
ret = SapModel.PropMaterial.SetOConcrete_1("Concrete", 5, False, 0, 1, 2, 0.0022, 0.0052, -
0.1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

This function supersedes SetOConcrete.

## See Also

GetOConcrete_1

# SetONoDesign

## Syntax

SapObject.SapModel.PropMaterial.SetONoDesign

## VB6 Procedure

Function SetONoDesign(ByVal Name As String, Optional ByVal FrictionAngle As Double = 0,
Optional ByVal DilatationalAngle As Double = 0, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing concrete material property.

FrictionAngle

The Drucker-Prager friction angle, 0 <= FrictionAngle < 90. [deg]

DilatationalAngle


The Drucker-Prager dilatational angle, 0 <= DilatationalAngle < 90. [deg]

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the other material property data for no design type materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropNoDesignData()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("NoDesign", MATERIAL_NODESIGN)

'assign other properties
ret = SapModel.PropMaterial.SetONoDesign("NoDesign", 10, 15)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

GetONoDesign

# SetORebar_1

## Syntax

SapObject.SapModel.PropMaterial.SetORebar_1

## VB6 Procedure

Function SetORebar_1(ByVal Name As String, ByVal Fy As Double, ByVal Fu As Double,
ByVal eFy As Double, ByVal eFu As Double, ByVal SSType As Long, ByVal SSHysType As
Long, ByVal StrainAtHardening As Double, ByVal StrainUltimate As Double, ByVal FinalSlope
As Double, ByVal UseCaltransSSDefaults As Boolean, Optional ByVal Temp As Double = 0) As
Long

## Parameters

Name

The name of an existing rebar material property.

Fy

The minimum yield stress. [F/L^2 ]

Fu

The minimum tensile stress. [F/L^2 ]

eFy

The expected yield stress. [F/L^2 ]

eFu

The expected tensile stress. [F/L^2 ]

SSType

This is 0, 1 or 2, indicating the stress-strain curve type.

```
0 = User defined
1 = Parametric - Simple
```

```
2 = Parametric - Park
```
SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
StrainAtHardening

This item applies only when parametric stress-strain curves are used and when
UseCaltransSSDefaults is False. It is the strain at the onset of strain hardening.

StrainUltimate

This item applies only when parametric stress-strain curves are used and when
UseCaltransSSDefaults is False. It is the ultimate strain capacity. This item must be larger than the
StrainAtHardening item.

FinalSlope

This item applies only to parametric stress-strain curves. It is a multiplier on the material modulus
of elasticity, E. This value multiplied times E gives the final slope of the curve.

UseCaltransSSDefaults

If this item is True, the program uses Caltrans default controlling strain values, which are bar size
dependent.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the other material property data for rebar materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropRebarData_1()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Rebar", MATERIAL_REBAR)

'assign other properties
ret = SapModel.PropMaterial.SetORebar_1("Rebar", 62, 93, 70, 102, 2, 2, 0.02, 0.1, -0.1,
False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

This function supersedes SetORebar.

## See Also

GetORebar_1

# SetOSteel_1

## Syntax

SapObject.SapModel.PropMaterial.SetOSteel_1

## VB6 Procedure

Function SetOSteel_1(ByVal Name As String, ByVal Fy As Double, ByVal Fu As Double, ByVal
eFy As Double, ByVal eFu As Double, ByVal SSType As Long, ByVal SSHysType As Long,
ByVal StrainAtHardening As Double, ByVal StrainAtMaxStress As Double, ByVal


StrainAtRupture As Double, ByVal FinalSlope As Double, Optional ByVal Temp As Double = 0)
As Long

## Parameters

Name

The name of an existing steel material property.

Fy

The minimum yield stress. [F/L^2 ]

Fu

The minimum tensile stress. [F/L^2 ]

eFy

The expected yield stress. [F/L^2 ]

eFu

The expected tensile stress. [F/L^2 ]

SSType

This is 0 or 1, indicating the stress-strain curve type.

```
0 = User defined
1 = Parametric - Simple
```
SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
StrainAtHardening

This item applies only to parametric stress-strain curves. It is the strain at the onset of strain
hardening.

StrainAtMaxStress

This item applies only to parametric stress-strain curves. It is the strain at maximum stress. This
item must be larger than the StrainAtHardening item.

StrainAtRupture

This item applies only to parametric stress-strain curves. It is the strain at rupture. This item must
be larger than the StrainAtMaxStress item.


FinalSlope

This item applies only to parametric stress-strain curves. It is a multiplier on the material modulus
of elasticity, E. This value multiplied times E gives the final slope of the curve.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the other material property data for steel materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropSteelData_1()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign other properties
ret = SapModel.PropMaterial.SetOSteel_1("Steel", 55, 68, 60, 70, 1, 2, 0.02, 0.1, 0.2, -0.1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

This function supersedes SetOSteel.

## See Also

GetOSteel_1

# SetSSCurve

## Syntax

SapObject.SapModel.PropMaterial.SetSSCurve

## VB6 Procedure

Function SetSSCurve(ByVal Name As String, ByVal NumberPoints As Long, ByRef PointID()
As Long, ByRef Strain() As Double, ByRef Stress() As Double, Optional ByVal Temp As Double
= 0) As Long

## Parameters

Name

The name of an existing material property.

NumberPoints

The number of points in the stress-strain curve. This item must be at least 3.

PointID

This is one of the following integers which sets the point ID. The point ID controls the color that
will be displayed for hinges in a deformed shape plot.

```
-5 = -E
-4 = -D
-3 = -C
-2 = -B
0 = None
1 = A
2 = B
3 = C
4 = D
```

### 5 = E

The point IDs must be input in numerically increasing order, except that 0 (None) values are
allowed anywhere. No duplicate values are allowed excepth for 0 (None).

Strain

This is an array that includes the strain at each point on the stress strain curve. The strains must
increase monotonically.

Stress

This is an array that includes the stress at each point on the stress strain curve. [F/L^2 ]

Points that have a negative strain must have a zero or negative stress. Similarly, points that have a
positive strain must have a zero or positive stress.

There must be one point defined that has zero strain and zero stress.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the material stress-strain curve for materials that are specified to have user-
defined stress-strain curves.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropUserSS()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PointID() As Long
Dim Strain() As Double
Dim Stress() As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign other properties
ret = SapModel.PropMaterial.SetOSteel("Steel", 55, 68, 60, 70, 0, 1, 0, 0, 0)

'assign user SS curve
ReDim PointID(4)
ReDim Strain(4)
ReDim Stress(4)
Strain(0) = -0.003: Stress(0) = -50: PointID(0) = -3
Strain(1) = -0.001: Stress(1) = -25: PointID(1) = 0
Strain(2) = 0: Stress(2) = -0: PointID(2) = 1
Strain(3) = 0.003: Stress(3) = 40: PointID(3) = 0
Strain(4) = 0.008: Stress(4) = 80: PointID(4) = 5
ret = SapModel.PropMaterial.SetSSCurve("Steel", 5, PointID, Strain, Stress)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetSSCurve

# SetOTendon_1

## Syntax

SapObject.SapModel.PropMaterial.SetOTendon_1

## VB6 Procedure


Function SetOTendon_1(ByVal Name As String, ByVal Fy As Double, ByVal Fu As Double,
ByVal SSType As Long, ByVal SSHysType As Long, ByVal FinalSlope As Double, Optional
ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing tendon material property.

Fy

The minimum yield stress. [F/L^2 ]

Fu

The minimum tensile stress. [F/L^2 ]

SSType

This is 0, 1 or 2, indicating the stress-strain curve type.

```
0 = User defined
1 = Parametric – 250 ksi strand
2 = Parametric – 270 ksi strand
```
SSHysType

This is 0, 1 or 2, indicating the stress-strain hysteresis type.

```
0 = Elastic
1 = Kinematic
2 = Takeda
```
FinalSlope

This item applies only to parametric stress-strain curves. It is a multiplier on the material modulus
of elasticity, E. This value multiplied times E gives the final slope of the curve.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
defined previously for the material.

## Remarks

This function sets the other material property data for tendon materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.


## VBA Example

Sub AssignMatPropTendonData_1()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Tendon", MATERIAL_TENDON)

'assign other properties
ret = SapModel.PropMaterial.SetOTendon_1("Tendon", 230, 255, 1, 1, -0.1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

This function supersedes SetOTendon.

## See Also

GetOTendon_1

# SetTemp

## Syntax


SapObject.SapModel.PropMaterial.SetTemp

## VB6 Procedure

Function SetTemp(ByVal Name As String, ByVal NumberItems as long, ByRef Temp() As
Double) As Long

## Parameters

Name

The name of an existing material property.

NumberItems

The number of different temperatures at which properties are specified for the material.

Temp

This is an array that includes the different temperatures at which properties are specified for the
material.

## Remarks

This function assigns the temperatures at which properties are specified for a material. This data is
required only for materials whose properties are temperature dependent.

The function returns zero if the temperatures are successfully set; otherwise it returns a nonzero
value.

## VBA Example

Sub SetMatPropTemps()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyTemp() As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'specify temps at which properties will be provided
ReDim MyTemp(2)
MyTemp(0) = 0
MyTemp(1) = 50
MyTemp(2) = 100
ret = SapModel.PropMaterial.SetTemp("Steel", 3, MyTemp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetTemp

# SetVonMisesPlasticityParameters

## Syntax

SapObject.SapModel.PropMaterial.SetVonMisesPlasticityParameters

## VB6 Procedure

Function SetVonMisesPlasticityParameters(ByVal Name As String, ByVal UseIsoLinHardening
As Boolean, ByVal IsoLinHardeningModulus As Double, ByVal UseIsoNLHardening As
Boolean, ByVal IsoNLUltimateStressRatio As Double, ByVal IsoNLHardeningRate As Double,
ByVal UseKinLinHardening As Boolean, ByVal KinLinHardeningModulus As Double, Optional
ByVal YieldStress As Double = 0.0, Optional ByVal Temp As Double = 0.0) As Long

## Parameters

Name

The name of an existing material property.

UseIsoLinHardening


If this item is True, the linear isotropic hardening is enabled.

IsoLinHardeningModulus

The linear isotropic hardening modulus, used if UseIsoLinHardening = True.

UseIsoNLHardening

If this item is True, the nonlinear isotropic saturation hardening is enabled.

IsoNLUltimateStressRatio

The ultimate stress as a ratio of the yield stress, used if UseIsoNLHardening = True.

IsoNLHardeningRate

The hardening rate parameter, used if UseIsoNLHardening = True.

UseKinLinHardening

If this item is True, the linear kinematic hardening is enabled.

KinLinHardeningModulus

The linear kinematic hardening modulus, used if UseKinLinHardening = True.

YieldStress

The yield stress.

This item applies only if the specified material has a material type of eMatType.NoDesign.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been defined previously for the material.

## Remarks

This function sets the Von Mises Plasticity coupled modeling parameters for a specified material

The function returns zero if the assignment data is successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub SetMatCoupledTypeData()

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

'initialize new material property

ret = SapModel.PropMaterial.SetMaterial("Steel", eMatType.eMatType_Steel, -1, "API
example test", "Default")

'set coupled material type data

ret = SapModel.PropMaterial.SetCoupledModelType("Steel",
eMatCoupledType.eMatCoupledType_VonMisesPlasticity)

'set Von Mises Plasticity data

ret = SapModel.PropMaterial.SetVonMisesPlasticityParameters ("Steel", True, 1000.0, True,
1.2, 50, True, 1000.0)


'close Sap2000

SapObject.ApplicationExit False

Set SapModel = Nothing

Set SapObject = Nothing

End Sub

## Release Notes

Initial release in version 22.1.0

## See Also

GetCoupledModelType

SetCoupledModelType

GetVonMisesPlasticityParameters

# SetWeightAndMass

## Syntax

SapObject.SapModel.PropMaterial.SetWeightAndMass

## VB6 Procedure

Function SetWeightAndMass(ByVal Name As String, ByVal MyOption As Long, ByVal Value
As Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing material property.

MyOption

This is either 1 or 2, indicating what is specified by the Value item.

```
1 = Weight per unit volume is specified
2 = Mass per unit volume is specified
```
If the weight is specified, the corresponding mass is program calculated based on the specified
weight. Similarly, if the mass is specified, the corresponding weight is program calculated based
on the specified mass.


Value

This is either the weight per unit volume or the mass per unit volume, depending on the value of
the MyOption item. [F/L^3 ] for MyOption = 1 (weight), and [M/L^3 ] for MyOption = 2 (mass)

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
define previously for the material.

## Remarks

This function assigns weight per unit volume or mass per unit volume to a material property.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropWeight()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Steel", MATERIAL_STEEL)

'assign material property weight per unit volume
ret = SapModel.PropMaterial.SetWeightAndMass("Steel", 1, 0.00029)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetWeightAndMass

# GetConcreteCEBFIP90

## Syntax

SapObject.SapModel.PropMaterial.GetConcreteCEBFIP90

## VB6 Procedure

Function GetConcreteCEBFIP90(ByVal Name As String, ByRef ConsiderConcreteAge As
Boolean, ByRef ConsiderConcreteCreep As Boolean, ByRef ConsiderConcreteShrinkage As
Boolean, ByRef CEBFIPsCoefficient As Double, ByRef RelativeHumidity As Double, ByRef
NotionalSize As Double, ByRef ShrinkageCoefficient As Double, ByRef ShrinkageStartAge As
Double, ByRef UseSeries As Long, ByRef NumberSeriesTerms As Long, Optional ByVal Temp
As Double = 0) As Long

## Parameters

Name

The name of an existing concrete material property.

ConsiderConcreteAge

If this item is True, time dependence is considered for concrete compressive strength and stiffness
(modulus of elasticity).

ConsiderConcreteCreep

If this item is True, time dependence is considered for concrete creep.

ConsiderConcreteShrinkage

If this item is True, time dependence is considered for concrete shrinkage.

CEBFIPsCoefficient

This is the cement type coefficient. This item applies only when ConsiderConcreteAge = True.


RelativeHumidity

This is relative humidity. This item applies only when ConsiderConcreteCreep = True or
ConsiderConcreteShrinkage = True.

NotionalSize

This is notional size of the member. This item applies only when ConsiderConcreteCreep = True
or ConsiderConcreteShrinkage = True.

As defined in Equation 2.1-69 of CEB_FIP Model Code 1990 the notional size is equal to two
times the cross-sectional area of the member divided by the perimeter of the member in contact
with the atmosphere.

ShrinkageCoefficient

This is the shrinkage coefficient as defined in Equation 2.1-76 of CEB_FIP Model Code 1990.
This item applies only when ConsiderConcreteShrinkage = True.

ShrinkageStartAge

This is the shrinkage start age in days as used in Section 2.1.6.4.4 of CEB_FIP Model Code 1990.
This item applies only when ConsiderConcreteShrinkage = True.

UseSeries

This is either 0 or 1, indicating the creep integration type.

```
0 = Full integration
1 = Dirichlet series
```
This item applies only when ConsiderConcreteCreep = True.

NumberSeriesTerms

This is the number of series terms used when integrating based on a Dirichlet series. This item
applies only when ConsiderConcreteCreep = True and UseSeries = 1.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks

This function retrieves the time dependent CEB FIP-90 material property data for concrete
materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not concrete.


## VBA Example

Sub GetMatPropConcreteTimeDepCEBFIP90()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ConsiderConcreteAge As Boolean
Dim ConsiderConcreteCreep As Boolean
Dim ConsiderConcreteShrinkage As Boolean
Dim CEBFIPsCoefficient As Double
Dim RelativeHumidity As Double
Dim NotionalSize As Double
Dim ShrinkageCoefficient As Double
Dim ShrinkageStartAge As Double
Dim UseSeries As Long
Dim NumberSeriesTerms As Long

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Concrete", MATERIAL_CONCRETE)

'assign CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.SetConcreteCEBFIP90("Concrete", True, True, True,
0.2, 40, 4, 4.9, 2, 1, 12)

'get CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.GetConcreteCEBFIP90("Concrete",
ConsiderConcreteAge, ConsiderConcreteCreep, ConsiderConcreteShrinkage,
CEBFIPsCoefficient, RelativeHumidity, NotionalSize, ShrinkageCoefficient, ShrinkageStartAge,
UseSeries, NumberSeriesTerms)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

SetConcreteCEBFIP90

# GetTendonScaleFactors

## Syntax

SapObject.SapModel.PropMaterial.TimeDep.GetTendonScaleFactors

## VB6 Procedure

Function GetTendonScaleFactors(ByVal Name As String, ByRef ScaleFactorRelaxation As
Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing tendon material property.

ScaleFactorRelaxation

This value multiplies the relaxation coefficient, and hence the relaxation strain, computed for the
material during a time-dependent analysis. It has no effect for load cases that do not consider time-
dependent effects, or for materials that do not consider relaxation effects. The default value is
unity, and the specified value must be positive.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks

This function retrieves the scale factors for the time-dependent material property data for tendon
materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not tendon.


## VBA Example

Sub GetMatPropTendonTimeDepScaleFactors()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim ScaleFactorRelaxation As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Tendon", eMatType,Tendon)

'assign CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.SetTendonCEBFIP90("Tendon", True, 2, 1, 12)

'assign time dependent scale factors
ret = SapModel.PropMaterial.TimeDep.SetTendonScaleFactors("Tendon", 1.15)

'get time dependent scale factors
ret = SapModel.PropMaterial.TimeDep.GetTendonScaleFactors("Tendon",
ScaleFactorRelaxation)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.


## See Also

SetTendonScaleFactors

# GetTendonCEBFIP90

## Syntax

SapObject.SapModel.PropMaterial.GetTendonCEBFIP90

## VB6 Procedure

Function GetTendonCEBFIP90(ByVal Name As String, ByRef ConsiderSteelRelaxation As
Boolean, ByRef CEBFIPClass As Long, ByRef UseSeries As Long, ByRef NumberSeriesTerms
As Long, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing tendon material property.

ConsiderSteelRelaxation

If this item is True, time dependence is considered for tendon steel relaxation.

CEBFIPClass

This is either 1 or 2, indicating the CEB FIP-90 class. This item applies only when
ConsiderSteelRelaxation = True.

UseSeries

This is either 0 or 1, indicating the steel relaxation integration type.

```
0 = Full integration
1 = Dirichlet series
```
This item applies only when ConsiderSteelRelaxation = True.

NumberSeriesTerms

This is the number of series terms used when integrating based on a Dirichlet series. This item
applies only when ConsiderSteelRelaxation = True and UseSeries = 1.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.


This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks

This function retrieves the time dependent CEB FIP-90 material property data for tendon
materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not tendon.

## VBA Example

Sub GetMatPropTendonTimeDepCEBFIP90()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ConsiderSteelRelaxation As Boolean
Dim CEBFIPClass As Long
Dim UseSeries As Long
Dim NumberSeriesTerms As Long

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Tendon", MATERIAL_TENDON)

'assign CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.SetTendonCEBFIP90("Tendon", True, 2, 1, 12)

'get CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.GetTendonCEBFIP90("Tendon",
ConsiderSteelRelaxation, CEBFIPClass, UseSeries, NumberSeriesTerms)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetTendonCEBFIP90

# GetConcreteScaleFactors

## Syntax

SapObject.SapModel.PropMaterial.TimeDep.GetConcreteScaleFactors

## VB6 Procedure

Function GetConcreteScaleFactors(ByVal Name As String, ByVal ScaleFactorAge As Double,
ByVal ScaleFactorCreep As Double, ByVal ScaleFactorShrinkage As Double, Optional ByVal
Temp As Double = 0) As Long

## Parameters

Name

The name of an existing concrete material property.

ScaleFactorAge

This value multiplies the stiffness (modulus of elasticity) computed with age for the material
during a time-dependent analysis. It has no effect for load cases that do not consider time-
dependent effects, or for materials that do not consider time-dependent age effects. The default
value is unity, and the specified value must be positive.

ScaleFactorCreep

This value multiplies the creep coefficient, and hence the creep strain, computed for the material
during a time-dependent analysis. It has no effect for load cases that do not consider time-
dependent effects, or for materials that do not consider creep effects. The default value is unity,
and the specified value must be positive.

ScaleFactorShrinkage

This value multiplies the shrinkage strain computed for the material during a time-dependent
analysis. It has no effect for load cases that do not consider time-dependent effects, or for
materials that do not consider shrinkage effects. The default value is unity, and the specified value
must be positive.


Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks

This function retrieves the scale factors for the time-dependent material property data for concrete
materials.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.
The function returns an error if the specified material is not concrete.

## VBA Example

Sub GetMatPropConcreteTimeDepScaleFactors()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim ScaleFactorAge As Double
Dim ScaleFactorCreep As Double
Dim ScaleFactorShrinkage As Double

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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Concrete", eMatType,Concrete)

'assign CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.SetConcreteCEBFIP90("Concrete", True, True, True,
0.2, 40, 4, 4.9, 2, 1, 12)


'assign time dependent scale factors
ret = SapModel.PropMaterial.TimeDep.SetConcreteScaleFactors("Concrete", 1.0, 1.2, 1.1)

'get time dependent scale factors
ret = SapModel.PropMaterial.TimeDep.GetConcreteScaleFactors("Concrete",
ScaleFactorAge, ScaleFactorCreep, ScaleFactorShrinkage)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

## See Also

SetConcreteCEBFIP90

# SetConcreteCEBFIP90

## Syntax

SapObject.SapModel.PropMaterial.TimeDep.SetConcreteCEBFIP90

## VB6 Procedure

Function SetConcreteCEBFIP90(ByVal Name As String, ByVal ConsiderConcreteAge As
Boolean, ByVal ConsiderConcreteCreep As Boolean, ByVal ConsiderConcreteShrinkage As
Boolean, ByVal CEBFIPsCoefficient As Double, ByVal RelativeHumidity As Double, ByVal
NotionalSize As Double, ByVal ShrinkageCoefficient As Double, ByVal ShrinkageStartAge As
Double, ByVal UseSeries As Long, ByVal NumberSeriesTerms As Long, Optional ByVal Temp
As Double = 0) As Long

## Parameters

Name

The name of an existing concrete material property.

ConsiderConcreteAge

If this item is True, time dependence is considered for concrete compressive strength and stiffness
(modulus of elasticity).

ConsiderConcreteCreep


If this item is True, time dependence is considered for concrete creep.

ConsiderConcreteShrinkage

If this item is True, time dependence is considered for concrete shrinkage.

CEBFIPsCoefficient

This is the cement type coefficient. This item applies only when ConsiderConcreteAge = True.

RelativeHumidity

This is relative humidity. This item applies only when ConsiderConcreteCreep = True or
ConsiderConcreteShrinkage = True.

NotionalSize

This is notional size of the member. This item applies only when ConsiderConcreteCreep = True
or ConsiderConcreteShrinkage = True.

As defined in Equation 2.1-69 of CEB_FIP Model Code 1990 the notional size is equal to two
times the cross-sectional area of the member divided by the perimeter of the member in contact
with the atmosphere.

ShrinkageCoefficient

This is the shrinkage coefficient as defined in Equation 2.1-76 of CEB_FIP Model Code 1990.
This item applies only when ConsiderConcreteShrinkage = True.

ShrinkageStartAge

This is the shrinkage start age in days as used in Section 2.1.6.4.4 of CEB_FIP Model Code 1990.
This item applies only when ConsiderConcreteShrinkage = True.

UseSeries

This is either 0 or 1, indicating the creep integration type.

```
0 = Full integration
1 = Dirichlet series
```
This item applies only when ConsiderConcreteCreep = True.

NumberSeriesTerms

This is the number of series terms used when integrating based on a Dirichlet series. This item
applies only when ConsiderConcreteCreep = True and UseSeries = 1.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data applies. The temperature must have been
previously defined for the material.


## Remarks

This function sets the time dependent CEB FIP-90 material property data for concrete materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropConcreteTimeDepCEBFIP90()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Concrete", MATERIAL_CONCRETE)

'assign CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.SetConcreteCEBFIP90("Concrete", True, True, True,
0.2, 40, 4, 4.9, 2, 1, 12)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetConcreteCEBFIP90


# SetConcreteScaleFactors

## Syntax

SapObject.SapModel.PropMaterial.TimeDep.SetConcreteScaleFactors

## VB6 Procedure

Function SetConcreteScaleFactors(ByVal Name As String, ByVal ScaleFactorAge As Double,
ByVal ScaleFactorCreep As Double, ByVal ScaleFactorShrinkage As Double, Optional ByVal
Temp As Double = 0) As Long

## Parameters

Name

The name of an existing concrete material property.

ScaleFactorAge

This value multiplies the stiffness (modulus of elasticity) computed with age for the material
during a time-dependent analysis. It has no effect for load cases that do not consider time-
dependent effects, or for materials that do not consider time-dependent age effects. The default
value is unity, and the specified value must be positive.

ScaleFactorCreep

This value multiplies the creep coefficient, and hence the creep strain, computed for the material
during a time-dependent analysis. It has no effect for load cases that do not consider time-
dependent effects, or for materials that do not consider creep effects. The default value is unity,
and the specified value must be positive.

ScaleFactorShrinkage

This value multiplies the shrinkage strain computed for the material during a time-dependent
analysis. It has no effect for load cases that do not consider time-dependent effects, or for
materials that do not consider shrinkage effects. The default value is unity, and the specified value
must be positive.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks


This function sets scale factors for the time-dependent material property data for concrete
materials. If this function is not called, default values of unity are assumed for all scale factors.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropConcreteTimeDepScaleFactors()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Concrete", eMatType,Concrete)

'assign CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.SetConcreteCEBFIP90("Concrete", True, True, True,
0.2, 40, 4, 4.9, 2, 1, 12)

'assign time dependent scale factors
ret = SapModel.PropMaterial.TimeDep.SetConcreteScaleFactors("Concrete", 1.0, 1.2, 1.1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.


## See Also

GetConcreteScaleFactors

# SetTendonCEBFIP90

## Syntax

SapObject.SapModel.PropMaterial.TimeDep.SetTendonCEBFIP90

## VB6 Procedure

Function SetTendonCEBFIP90(ByVal Name As String, ByVal ConsiderSteelRelaxation As
Boolean, ByVal CEBFIPClass As Long, ByVal UseSeries As Long, ByVal NumberSeriesTerms
As Long, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing tendon material property.

ConsiderSteelRelaxation

If this item is True, time dependence is considered for tendon steel relaxation.

CEBFIPClass

This is either 1 or 2, indicating the CEB FIP-90 class. This item applies only when
ConsiderSteelRelaxation = True.

UseSeries

This is either 0 or 1, indicating the steel relaxation integration type.

```
0 = Full integration
1 = Dirichlet series
```
This item applies only when ConsiderSteelRelaxation = True.

NumberSeriesTerms

This is the number of series terms used when integrating based on a Dirichlet series. This item
applies only when ConsiderSteelRelaxation = True and UseSeries = 1.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.


This item is the temperature at which the specified data applies. The temperature must have been
previously defined for the material.

## Remarks

This function sets the time dependent CEB FIP-90 material property data for tendon materials.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropTendonTimeDepCEBFIP90()
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Tendon", MATERIAL_TENDON)

'assign CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.SetTendonCEBFIP90("Tendon", True, 2, 1, 12)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also


GetTendonCEBFIP90

# SetTendonScaleFactors

## Syntax

SapObject.SapModel.PropMaterial.TimeDep.SetTendonScaleFactors

## VB6 Procedure

Function SetTendonScaleFactors(ByVal Name As String, ByRef ScaleFactorRelaxtion As
Double, Optional ByVal Temp As Double = 0) As Long

## Parameters

Name

The name of an existing tendon material property.

ScaleFactorRelaxation

This value multiplies the relaxation coefficient, and hence the relaxation strain, computed for the
material during a time-dependent analysis. It has no effect for load cases that do not consider time-
dependent effects, or for materials that do not consider relaxation effects. The default value is
unity, and the specified value must be positive.

Temp

This item applies only if the specified material has properties that are temperature dependent. That
is, it applies only if properties are specified for the material at more than one temperature.

This item is the temperature at which the specified data is to be retrieved. The temperature must
have been previously defined for the material.

## Remarks

This function sets scale factors for the time-dependent material property data for tendon materials.
If this function is not called, default values of unity are assumed for all scale factors.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub AssignMatPropTendonTimeDepCEBIFP90
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

'initialize new material property
ret = SapModel.PropMaterial.SetMaterial("Tendon", eMatType,Tendon)

'assign CEB FIP-90 time dependent data
ret = SapModel.PropMaterial.TimeDep.SetTendonCEBFIP90("Tendon", True, 2, 1, 12)

'assign time dependent scale factors
ret = SapModel.PropMaterial.TimeDep.SetTendonScaleFactors("Tendon", 1.15)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.0.

## See Also

GetTendonScaleFactors

# ChangeName

## Syntax

SapObject.SapModel.PropLink.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long


## Parameters

Name

The existing name of a defined link property.

NewName

The new name for the link property.

## Remarks

This function changes the name of an existing link property.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeLinkPropName()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double

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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12


ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'change name of link property
ret = SapModel.PropLink.ChangeName("L1", "MyLink")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Count

## Syntax

SapObject.SapModel.PropLink.Count

## VB6 Procedure

Function Count(Optional ByVal PropType As eLinkPropType) As Long

## Parameters

PropType

This optional value is one of the following items in the eLinkPropType enumeration.

```
NLPROP_LINEAR = 1
NLPROP_DAMPER = 2
NLPROP_GAP = 3
NLPROP_HOOK = 4
NLPROP_PLASTIC_WEN = 5
NLPROP_ISOLATOR1 = 6 (Rubber isolator)
NLPROP_ISOLATOR2 = 7 (Friction isolator)
NLPROP_MULTILINEAR_ELASTIC = 8
NLPROP_MULTILINEAR_PLASTIC = 9
NLPROP_ISOLATOR3 = 10 (T/C Friction isolator)
```
If no value is input for PropType, a count is returned for all link properties in the model regardless
of type.


## Remarks

This function returns the total number of defined link properties in the model. If desired, counts
can be returned for all link properties of a specified type in the model.

## VBA Example

Sub CountLinkProps()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'return number of defined links of all types
Count = SapModel.PropLink.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

# Delete

## Syntax

SapObject.SapModel.PropLink.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing link property.

## Remarks

The function deletes a specified link property.

The function returns zero if the link property is successfully deleted; otherwise it returns a nonzero
value. It returns an error if the specified link property can not be deleted, for example, if it is being
used by an existing link object.

## VBA Example

Sub DeleteLinkProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim i As Long
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

'add link properties
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)
ret = SapModel.PropLink.SetLinear("L2", DOF, Fixed, Ke, Ce, 0, 0)

'delete link property
ret = SapModel.PropLink.Delete("L1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetDamper

## Syntax

SapObject.SapModel.PropLink.GetDamper

## VB6 Procedure

Function GetDamper(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef


k() As Double, ByRef c() As Double, ByRef cexp() As Double, ByRef dj2 As Double, ByRef dj3
As Double, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing exponential damper-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke


This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

c

This is an array of nonlinear damping coefficient terms for the link property. The nonlinear
damping coefficient applies for nonlinear analyses.

```
c(0) = U1 [F/(L^cexp)]
c(1) = U2 [F/(L^cexp)]
c(2) = U3 [F/(L^cexp)]
c(3) = R1 [FL]
c(4) = R2 [FL]
c(5) = R3 [FL]
```

The term c(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

cexp

This is an array of the nonlinear damping exponent terms. The nonlinear damping exponent
applies for nonlinear analyses. It is applied to the velocity across the damper in the equation of
motion.

```
cexp(0) = U1
cexp(1) = U2
cexp(2) = U3
cexp(3) = R1
cexp(4) = R2
cexp(5) = R3
```
The term cexp(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for an exponential damper-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropDamper()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean


Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MyC() As Double
Dim MyCexp() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim k() As Double
Dim c() As Double
Dim cexp() As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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
'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyC(5)
ReDim MyCexp(5)
```
```
MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01
```
```
MyDOF(1) = True
MyNonLinear(1) = True
```

```
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MyC(1)=0.08
MyCexp(1) = 1.2
```
```
MyDOF(2) = True
MyFixed(2) = True
```
```
ret = SapModel.PropLink.SetDamper("D1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, MyK, MyC, MyCexp, 1, 0)
```
```
'get link property data
```
```
ret = SapModel.PropLink.GetDamper ("D1", DOF, Fixed, NonLinear, Ke, Ce, k, c,
cexp, dj2, dj3, Notes, GUID)
```
```
'close Sap2000
```
```
SapObject.ApplicationExit False
```
```
Set SapModel = Nothing
```
```
Set SapObject = Nothing
```
End Sub

## Release Notes

Initial release in version 11.02.

Clarification that damper type is exponential added in version 16.0.2.

## See Also

SetDamper

# GetDamperBilinear

## Syntax

SapObject.SapModel.PropLink.GetDamperBilinear

## VB6 Procedure


Function GetDamperBilinear (ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed()
As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByRef k() As Double, ByRef c() As Double, ByRef cy() As Double, ByRef ForceLimit() As
Double, ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal Notes As String = "",
Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing bilinear damper-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained.)

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.


```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) only applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

c

This is an array of nonlinear initial damping coefficient terms for the link property. The nonlinear
initial damping coefficient applies for nonlinear analyses.

```
c(0) = U1 [F/L]
c(1) = U2 [F/L]
c(2) = U3 [F/L]
c(3) = R1 [FL]
c(4) = R2 [FL]
c(5) = R3 [FL]
```
The term c(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

cy

This is an array of nonlinear yielded damping coefficient terms for the link property. The
nonlinear yielded damping coefficient applies for nonlinear analyses.

```
cy(0) = U1 [F/L]
cy(1) = U2 [F/L]
cy(2) = U3 [F/L]
```

```
cy(3) = R1 [FL]
cy(4) = R2 [FL]
cy(5) = R3 [FL]
```
The term cy(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

ForceLimit

This is an array of nonlinear linear force limit terms for the link property. The linear force limit
applies for nonlinear analyses.

```
ForceLimit(0) = U1 [F]
ForceLimit(1) = U2 [F]
ForceLimit(2) = U3 [F]
ForceLimit(3) = R1 [FL]
ForceLimit(4) = R2 [FL]
ForceLimit(5) = R3 [FL]
```
The term ForceLimit(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function retrieves link property data for a bilinear damper-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropDamperBilinear ()

```
'dimension variables
```
```
Dim SapObject as cOAPI
```

```
Dim SapModel As cSapModel
```
```
Dim ret As Long
```
```
Dim MyDOF() As Boolean
```
```
Dim MyFixed() As Boolean
```
```
Dim MyNonLinear() As Boolean
```
```
Dim MyKe() As Double
```
```
Dim MyCe() As Double
```
```
Dim MyK() As Double
```
```
Dim MyC() As Double
```
```
Dim MyCy() As Double
```
```
Dim MyForceLimit() As Double
```
```
Dim DOF() As Boolean
```
```
Dim Fixed() As Boolean
```
```
Dim NonLinear() As Boolean
```
```
Dim Ke() As Double
```
```
Dim Ce() As Double
```
```
Dim K() As Double
```
```
Dim C() As Double
```
```
Dim Cy() As Double
```
```
Dim ForceLimit() As Double
```
```
Dim dj2 As Double
```
```
Dim dj3 As Double
```
```
Dim Notes As String
```
```
Dim GUID As String
```
'create Sap2000 object

```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```

'start Sap2000 application

```
SapObject.ApplicationStart
```
'create SapModel object

```
Set SapModel = SapObject.SapModel
```
'initialize model

```
ret = SapModel.InitializeNewModel
```
'create model from template

```
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
'add link property

```
ReDim MyDOF(5)
```
```
ReDim MyFixed(5)
```
```
ReDim MyNonLinear(5)
```
```
ReDim MyKe(5)
```
```
ReDim MyCe(5)
```
```
ReDim MyK(5)
```
```
ReDim MyC(5)
```
```
ReDim MyCy(5)
```
```
ReDim MyForceLimit(5)
```
```
MyDOF(0) = True
```
```
MyKe(0) = 12
```
```
MyCe(0) = 0.01
```
```
MyDOF(1) = True
```

```
MyNonLinear(1) = True
```
```
MyKe(1) = 12
```
```
MyCe(1) = 0.01
```
```
MyK(1) = 20
```
```
MyC(1)=0.08
```
```
MyCy(1) = 0.008
```
```
MyForceLimit(1) = 50
```
```
MyDOF(2) = True
```
```
MyFixed(2) = True
```
```
ret = SapModel.PropLink.SetDamperBilinear("D1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, MyK, MyC, MyCy, MyForceLimit, 1, 0)
```
```
'get link property data
```
```
ret = SapModel.PropLink.GetDamperBilinear ("D1", DOF, Fixed, NonLinear, Ke,
Ce, k, c, cy, ForceLimit, dj2, dj3, Notes, GUID)
```
```
'close Sap2000
```
```
SapObject.ApplicationExit False
```
```
Set SapModel = Nothing
```
```
Set SapObject = Nothing
```
End Sub

## Release Notes

Initial release in version 16.0.2.

## See Also

SetDamperBilinear


# GetDamperFrictionSpring

## Syntax

SapObject.SapModel.PropLink.GetDamperFrictionSpring

## VB6 Procedure

Function GetDamperFrictionSpring(ByVal Name As String, ByRef DOF() As Boolean, ByRef
Fixed() As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As
Double, ByRef k() As Double, ByRef k1() As Double, ByRef k2() As Double, ByRef u0() As
Double, ByRef us() As Double, ByRef dir() As Long, ByRef dj2 As Double, ByRef dj3 As
Double, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing friction spring damper-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained.)

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
```

```
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial (nonslipping) stiffness terms for the link property. The initial stiffness
applies for nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) only applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

k1

This is an array of slipping stiffness when loading terms for the link property. The slipping
stiffness when loading applies for nonlinear analyses.

```
k1(0) = U1 [F/L]
k1(1) = U2 [F/L]
k1(2) = U3 [F/L]
k1(3) = R1 [FL]
k1(4) = R2 [FL]
k1(5) = R3 [FL]
```

The term k1(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

k2

This is an array of slipping stiffness when unloading terms for the link property. The slipping
stiffness when unloading applies for nonlinear analyses.

```
k2(0) = U1 [F/L]
k2(1) = U2 [F/L]
k2(2) = U3 [F/L]
k2(3) = R1 [FL]
k2(4) = R2 [FL]
k2(5) = R3 [FL]
```
The term k2(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

u0

This is an array of precompression displacement terms for the link property. The nonlinear
precompression displacement applies for nonlinear analyses.

```
u0(0) = U1 [L]
u0(1) = U2 [L]
u0(2) = U3 [L]
u0(3) = R1
u0(4) = R2
u0(5) = R3
```
The term u0(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

us

This is an array of stop displacement terms for the link property. The nonlinear stop displacement
applies for nonlinear analyses.

```
us(0) = U1 [L]
us(1) = U2 [L]
us(2) = U3 [L]
us(3) = R1
us(4) = R2
us(5) = R3
```
The term us(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.


### GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function retrieves link property data for a friction spring damper-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropDamperFrictionSpring()

```
'dimension variables
```
```
Dim SapObject as cOAPI
```
```
Dim SapModel As cSapModel
```
```
Dim ret As Long
```
```
Dim MyDOF() As Boolean
```
```
Dim MyFixed() As Boolean
```
```
Dim MyNonLinear() As Boolean
```
```
Dim MyKe() As Double
```
```
Dim MyCe() As Double
```
```
Dim MyK() As Double
```
```
Dim MyK1() As Double
```
```
Dim MyK2() As Double
```
```
Dim MyU0() As Double
```
```
Dim MyUs() As Double
```
```
Dim MyDir() As Long
```
```
Dim DOF() As Boolean
```
```
Dim Fixed() As Boolean
```
```
Dim NonLinear() As Boolean
```
```
Dim Ke() As Double
```

```
Dim Ce() As Double
```
```
Dim K() As Double
```
```
Dim K1() As Double
```
```
Dim K2() As Double
```
```
Dim U0() As Double
```
```
Dim Us() As Double
```
```
Dim Dir() As Long
```
```
Dim dj2 As Double
```
```
Dim dj3 As Double
```
```
Dim Notes As String
```
```
Dim GUID As String
```
'create Sap2000 object

```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
'start Sap2000 application

```
SapObject.ApplicationStart
```
'create SapModel object

```
Set SapModel = SapObject.SapModel
```
'initialize model

```
ret = SapModel.InitializeNewModel
```
'create model from template

```
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
'add link property


ReDim MyDOF(5)

ReDim MyFixed(5)

ReDim MyNonLinear(5)

ReDim MyKe(5)

ReDim MyCe(5)

ReDim MyK(5)

ReDim MyK1(5)

ReDim MyK2(5)

ReDim MyU0(5)

ReDim MyUs(5)

ReDim MyDir(5)

MyDOF(0) = True

MyKe(0) = 12

MyCe(0) = 0.01

MyDOF(1) = True

MyNonLinear(1) = True

MyKe(1) = 12

MyCe(1) = 0.01

MyK(1) = 20

MyK1(1)=2

MyK2(1) = 1

MyU0(1) = -.2

MyUs(1) = 1

MyDir(1) = 2

MyDOF(2) = True


```
MyFixed(2) = True
```
```
ret = SapModel.PropLink.SetDamperFrictionSpring("D1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, MyK, MyK1, MyK2, MyU0, MyUs, MyDir, 1, 0)
```
```
'get link property data
```
```
ret = SapModel.PropLink.GetDamperFrictionSpring ("D1", DOF, Fixed,
NonLinear, Ke, Ce, k, K1, K2, U0, Us, Dir, dj2, dj3, Notes, GUID)
```
```
'close Sap2000
```
```
SapObject.ApplicationExit False
```
```
Set SapModel = Nothing
```
```
Set SapObject = Nothing
```
End Sub

## Release Notes

Initial release in version 16.0.2.

## See Also

SetDamperFrictionSpring

# GetDamperLinearExponential

## Syntax

SapObject.SapModel.PropLink.GetDamperLinearExponential

## VB6 Procedure

Function GetDamperLinearExponential(ByVal Name As String, ByRef DOF() As Boolean,
ByRef Fixed() As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce()
As Double, ByRef k() As Double, ByRef c() As Double, ByRef cexp() As Double, ByRef
ForceLimit() As Double, ByRef dj2 As Double, ByRef dj3 As Double, ByRef Notes As String,
ByRef GUID As String) As Long

## Parameters


Name

The name of an existing linear exponential damper-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained.)

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```

The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) only applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

c

This is an array of nonlinear damping coefficient terms for the link property. The nonlinear
damping coefficient applies for nonlinear analyses.

```
c(0) = U1 [F/(L^cexp)]
c(1) = U2 [F/(L^cexp)]
c(2) = U3 [F/(L^cexp)]
c(3) = R1 [FL]
c(4) = R2 [FL]
c(5) = R3 [FL]
```
The term c(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

cexp

This is an array of the nonlinear damping exponent terms. The nonlinear damping exponent
applies for nonlinear analyses. It is applied to the velocity across the damper in the equation of
motion.

```
cexp(0) = U1
cexp(1) = U2
cexp(2) = U3
cexp(3) = R1
cexp(4) = R2
```

```
cexp(5) = R3
```
The term cexp(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

ForceLimit

This is an array of nonlinear linear force limit terms for the link property. The linear force limit
applies for nonlinear analyses.

```
ForceLimit(0) = U1 [F]
ForceLimit(1) = U2 [F]
ForceLimit(2) = U3 [F]
ForceLimit(3) = R1 [FL]
ForceLimit(4) = R2 [FL]
ForceLimit(5) = R3 [FL]
```
The term ForceLimit(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function retrieves link property data for a linear exponential damper-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropDamperLinearExponential()

```
'dimension variables
```
```
Dim SapObject as cOAPI
```
```
Dim SapModel As cSapModel
```

```
Dim ret As Long
```
```
Dim MyDOF() As Boolean
```
```
Dim MyFixed() As Boolean
```
```
Dim MyNonLinear() As Boolean
```
```
Dim MyKe() As Double
```
```
Dim MyCe() As Double
```
```
Dim MyK() As Double
```
```
Dim MyC() As Double
```
```
Dim MyCexp() As Double
```
```
Dim MyForceLimit() As Double
```
```
Dim DOF() As Boolean
```
```
Dim Fixed() As Boolean
```
```
Dim NonLinear() As Boolean
```
```
Dim Ke() As Double
```
```
Dim Ce() As Double
```
```
Dim K() As Double
```
```
Dim C() As Double
```
```
Dim Cexp() As Double
```
```
Dim ForceLimit() As Double
```
```
Dim dj2 As Double
```
```
Dim dj3 As Double
```
```
Dim Notes As String
```
```
Dim GUID As String
```
'create Sap2000 object

```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
'start Sap2000 application


```
SapObject.ApplicationStart
```
'create SapModel object

```
Set SapModel = SapObject.SapModel
```
'initialize model

```
ret = SapModel.InitializeNewModel
```
'create model from template

```
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
'add link property

```
ReDim MyDOF(5)
```
```
ReDim MyFixed(5)
```
```
ReDim MyNonLinear(5)
```
```
ReDim MyKe(5)
```
```
ReDim MyCe(5)
```
```
ReDim MyK(5)
```
```
ReDim MyC(5)
```
```
ReDim MyCexp(5)
```
```
ReDim MyForceLimit(5)
```
```
MyDOF(0) = True
```
```
MyKe(0) = 12
```
```
MyCe(0) = 0.01
```
```
MyDOF(1) = True
```
```
MyNonLinear(1) = True
```

```
MyKe(1) = 12
```
```
MyCe(1) = 0.01
```
```
MyK(1) = 20
```
```
MyC(1)=0.08
```
```
MyCexp(1) = 1.2
```
```
MyForceLimit(1) = 50
```
```
MyDOF(2) = True
```
```
MyFixed(2) = True
```
```
ret = SapModel.PropLink.SetDamperLinearExponential("D1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, MyK, MyC, MyCexp, MyForceLimit, 1, 0)
```
```
'get link property data
```
```
ret = SapModel.PropLink.GetDamperLinearExponential ("D1", DOF, Fixed,
NonLinear, Ke, Ce, k, c, cexp, ForceLimit, dj2, dj3, Notes, GUID)
```
```
'close Sap2000
```
```
SapObject.ApplicationExit False
```
```
Set SapModel = Nothing
```
```
Set SapObject = Nothing
```
End Sub

## Release Notes

Initial release in version 16.0.2.

## See Also

SetDamperLinearExponential

# GetFrictionIsolator


## Syntax

SapObject.SapModel.PropLink.GetFrictionIsolator

## VB6 Procedure

Function GetFrictionIsolator(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed()
As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByRef k() As Double, ByRef Slow() As Double, ByRef Fast() As Double, ByRef Rate() As
Double, ByRef Radius() As Double, ByRef Damping As Double, ByRef dj2 As Double, ByRef
dj3 As Double, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing friction isolator-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
```

```
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1, Not Used
NonLinear(4) = R2, Not Used
NonLinear(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U1, U2 and U3. For those degrees of
freedom, the term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1, Not Used
k(4) = R2, Not Used
k(5) = R3, Not Used
```

Note that this item is applicable only for degrees of freedom U1, U2 and U3. For those degrees of
freedom, the term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Slow

This is an array of the friction coefficient at zero velocity terms for the link property. This
coefficient applies for nonlinear analyses.

```
Slow(0) = U1, Not Used
Slow(1) = U2
Slow(2) = U3
Slow(3) = R1, Not Used
Slow(4) = R2, Not Used
Slow(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Slow(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Fast

This is an array of the friction coefficient at fast velocity terms for the link property. This
coefficient applies for nonlinear analyses.

```
Fast(0) = U1, Not Used
Fast(1) = U2
Fast(2) = U3
Fast(3) = R1, Not Used
Fast(4) = R2, Not Used
Fast(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Fast(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Rate

This is an array of the inverse of the characteristic sliding velocity terms for the link property. This
item applies for nonlinear analyses.

```
Rate(0) = U1, Not Used
Rate(1) = U2 [s/L]
Rate(2) = U3 [s/L]
Rate(3) = R1, Not Used
Rate(4) = R2, Not Used
Rate(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Rate(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.


Radius

This is an array of the radius of the sliding contact surface terms for the link property. Inputting 0
means there is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.

```
Radius(0) = U1, Not Used
Radius(1) = U2 [L]
Radius(2) = U3 [L]
Radius(3) = R1, Not Used
Radius(4) = R2, Not Used
Radius(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Radius(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.

Damping

This is the nonlinear damping coefficient used for the axial translational degree of freedom, U1.
This item applies for nonlinear analyses. [F/L]

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a friction isolator-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropFrictionIsolator()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MySlow() As Double
Dim MyFast() As Double
Dim MyRate() As Double
Dim MyRadius() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim k() As Double
Dim Slow() As Double
Dim Fast() As Double
Dim Rate() As Double
Dim Radius() As Double
Dim Damping As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MySlow(5)
ReDim MyFast(5)
ReDim MyRate(5)
ReDim MyRadius(5)


MyDOF(0) = True
MyNonLinear(0) = True
MyKe(0) = 12
MyCe(0) = 0.01
MyK(0) = 1000

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MySlow(1)= 0.6
MyFast(1)= 0.5
MyRate(1)= 10
MyRadius(1)= 80

MyDOF(2) = True
MyNonLinear(2) = True
MyKe(2) = 14
MyCe(2) = 0.008
MyK(2) = 22
MySlow(2)= 0.66
MyFast(2)= 0.55
MyRate(2)= 12
MyRadius(2)= 75

MyDOF(3) = True
MyKe(3) = 15
MyCe(3) = 0

MyDOF(4) = True
MyFixed(4) = True

ret = SapModel.PropLink.SetFrictionIsolator("FI1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, MyK, MySlow, MyFast, MyRate, MyRadius, 0.1, 2, 3)

'get link property data
ret = SapModel.PropLink.GetFrictionIsolator("FI1", DOF, Fixed, NonLinear, Ke, Ce, k,
Slow, Fast, Rate, Radius, Damping, dj2, dj3, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

SetFrictionIsolator

# GetGap

## Syntax

SapObject.SapModel.PropLink.GetGap

## VB6 Procedure

Function GetGap(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As Boolean,
ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef k() As
Double, ByRef dis() As Double, ByRef dj2 As Double, ByRef dj3 As Double, ByRef Notes As
String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing gap-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.


NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
```

```
k(5) = R3 [FL]
```
The term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dis

This is an array of initial gap opening terms for the link property. The initial gap opening applies
for nonlinear analyses.

```
dis(0) = U1 [L]
dis(1) = U2 [L]
dis(2) = U3 [L]
dis(3) = R1 [rad]
dis(4) = R2 [rad]
dis(5) = R3 [rad]
```
The term dis(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a gap-type link property.

The function returns zero if the property data is retrieved successfully; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropGap()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean


Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MyDis() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim k() As Double
Dim dis() As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyDis(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MyDis(1)=1.2


MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetGap("G1", MyDOF, MyFixed, MyNonLinear, MyKe, MyCe,
MyK, MyDis, 2, 0)

'get link property data
ret = SapModel.PropLink.GetGap("G1", DOF, Fixed, NonLinear, Ke, Ce, k, dis, dj2, dj3,
Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetGap

# GetHook

## Syntax

SapObject.SapModel.PropLink.GetHook

## VB6 Procedure

Function GetHook(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef
k() As Double, ByRef dis() As Double, ByRef dj2 As Double, ByRef dj3 As Double, ByRef Notes
As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing hook-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
```

### DOF(1) = U2

### DOF(2) = U3

### DOF(3) = R1

### DOF(4) = R2

### DOF(5) = R3

Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.


```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dis

This is an array of initial hook opening terms for the link property. The initial hook opening
applies for nonlinear analyses.

```
c(0) = U1 [L]
c(1) = U2 [L]
c(2) = U3 [L]
c(3) = R1 [rad]
c(4) = R2 [rad]
c(5) = R3 [rad]
```
The term dis(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID


The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a hook-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropHook()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MyDis() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim k() As Double
Dim dis() As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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

'add link property


ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyDis(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MyDis(1)=1.2

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetHook("H1", MyDOF, MyFixed, MyNonLinear, MyKe, MyCe,
MyK, MyDis, 2, 0)

'get link property data
ret = SapModel.PropLink.GetHook("H1", DOF, Fixed, NonLinear, Ke, Ce, k, dis, dj2, dj3,
Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetHook

# GetLinear

## Syntax

SapObject.SapModel.PropLink.GetLinear


## VB6 Procedure

Function GetLinear(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef dj2 As Double, ByRef dj3 As
Double, ByRef KeCoupled As Boolean, ByRef CeCoupled As Boolean, ByRef Notes As String,
ByRef GUID As String) As Long

## Parameters

Name

The name of an existing linear-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity if DOF(0) = True
Fixed(1) = U2 fixity if DOF(1) = True
Fixed(2) = U3 fixity if DOF(2) = True
Fixed(3) = R1 fixity if DOF(3) = True
Fixed(4) = R2 fixity if DOF(4) = True
Fixed(5) = R3 fixity if DOF(5) = True
```
Ke

This is an array of stiffness terms for the link property. There are 6 terms in the array if the
stiffness is uncoupled and 21 if it is coupled. The KeCoupled item indicates if the stiffness is
coupled.

If the stiffness is uncoupled:

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```

If the stiffness is coupled:

```
Ke(0) = U1U1 [F/L]
Ke(1) = U1U2 [F/L]
Ke(2) = U2U2 [F/L]
Ke(3) = U1U3 [F/L]
Ke(4) = U2U3 [F/L]
Ke(5) = U3U3 [F/L]
Ke(6) = U1R1 [F]
Ke(7) = U2R1 [F]
Ke(8) = U3R1 [F]
Ke(9) = R1R1 [FL]
Ke(10) = U1R2 [F]
Ke(11) = U2R2 [F]
Ke(12) = U3R2 [F]
Ke(13) = R1R2 [FL]
Ke(14) = R2R2 [FL]
Ke(15) = U1R3 [F]
Ke(16) = U2R3 [F]
Ke(17) = U3R3 [F]
Ke(18) = R1R3 [FL]
Ke(19) = R2R3 [FL]
Ke(20) = R3R3 [FL]
```
Ce

This is an array of damping terms for the link property. There are 6 terms in the array if the
damping is uncoupled and 21 if it is coupled. The CeCoupled item indicates if the damping is
coupled.

If the damping is uncoupled:

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
If the damping is coupled:

```
Ce(0) = U1U1 [F/L]
Ce(1) = U1U2 [F/L]
Ce(2) = U2U2 [F/L]
Ce(3) = U1U3 [F/L]
Ce(4) = U2U3 [F/L]
Ce(5) = U3U3 [F/L]
Ce(6) = U1R1 [F]
Ce(7) = U2R1 [F]
Ce(8) = U3R1 [F]
Ce(9) = R1R1 [FL]
Ce(10) = U1R2 [F]
Ce(11) = U2R2 [F]
```

```
Ce(12) = U3R2 [F]
Ce(13) = R1R2 [FL]
Ce(14) = R2R2 [FL]
Ce(15) = U1R3 [F]
Ce(16) = U2R3 [F]
Ce(17) = U3R3 [F]
Ce(18) = R1R3 [FL]
Ce(19) = R2R3 [FL]
Ce(20) = R3R3 [FL]
```
dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

KeCoupled

This item is True if the link stiffness, Ke, is coupled. There are 21 terms in the Ke array if Ke is
coupled; otherwise there are 6 terms.

CeCoupled

This item is True if the link damping, Ce, is coupled. There are 21 terms in the Ce array if Ce is
coupled; otherwise there are 6 terms.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a linear-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropLinear()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean


Dim MyFixed() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim dj2 As Double
Dim dj3 As Double
Dim KeCoupled As Boolean
Dim CeCoupled As Boolean
Dim Notes As String
Dim GUID As String

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyKe(5)
ReDim MyCe(5)
MyDOF(0) = True
MyKe(0) = 12
ret = SapModel.PropLink.SetLinear("L1", MyDOF, MyFixed, MyKe, MyCe, 0, 0)

'get link property data
ret = SapModel.PropLink.GetLinear("L1", DOF, Fixed, Ke, Ce, dj2, dj3, KeCoupled,
CeCoupled, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

SetLinear

# GetMultiLinearElastic

## Syntax

SapObject.SapModel.PropLink.GetMultiLinearElastic

## VB6 Procedure

Function GetMultiLinearElastic(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed
() As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByRef dj2 As Double, ByRef dj3 As Double, ByRef Notes As String, ByRef GUID As String) As
Long

## Parameters

Name

The name of an existing multilinear elastic-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.


NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies pnly when DOF(n) = True and Fixed(n) = False.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]


Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a multilinear elastic-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropMultiLinearElastic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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


'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetMultiLinearElastic("MLE1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, 2, 0)

'get link property data
ret = SapModel.PropLink.GetMultiLinearElastic("MLE1", DOF, Fixed, NonLinear, Ke,
Ce, dj2, dj3, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetMultiLinearElastic

GetMultiLinearPoints

SetMultiLinearPoints

# GetMultiLinearPlastic

## Syntax

SapObject.SapModel.PropLink.GetMultiLinearPlastic


## VB6 Procedure

Function GetMultiLinearPlastic(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed
() As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByRef dj2 As Double, ByRef dj3 As Double, ByRef Notes As String, ByRef GUID As String) As
Long

## Parameters

Name

The name of an existing multilinear plastic-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```

The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a multilinear plastic-type link property.


The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropMultiLinearPlastic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True


MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetMultiLinearPlastic("MLP1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, 2, 0)

'get link property data
ret = SapModel.PropLink.GetMultiLinearPlastic("MLP1", DOF, Fixed, NonLinear, Ke, Ce,
dj2, dj3, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetMultiLinearPlastic

GetMultiLinearPoints

SetMultiLinearPoints

# GetMultiLinearPoints

## Syntax

SapObject.SapModel.PropLink.GetMultiLinearPoints

## VB6 Procedure

Function GetMultiLinearPoints(ByVal Name As String, ByVal DOF As Long, ByRef
NumberPoints As Long, ByRef F() As Double, ByRef D() As Double, ByRef MyType As Long,
ByRef a1 As Double, ByRef a2 As Double, ByRef b1 As Double, ByRef b2 As Double, ByRef
eta As Double) As Long

## Parameters

Name


The name of an existing multilinear elastic or multilinear plastic link property.

DOF

This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom to which the multilinear points apply.

```
1 = U1
2 = U2
3 = U3
4 = R1
5 = R2
6 = R3
```
NumberPoints

The number of foce-defomation points for the specified degree of freedom.

F

This is an array, dimensioned to NumberPoints - 1, that includes the force at each point. When
DOF is U1, U2 or U3, this is a force. When DOF is R1, R2 or R3, this is a moment. [F] if DOF <=
3, and [FL} if DOF > 3

D

This is an array, dimensioned to NumberPoints - 1, that includes the displacement at each point.
When DOF is U1, U2 or U3, this is a translation. When DOF is R1, R2 or R3, this is a rotation.
[L] if DOF <= 3, and [rad] if DOF > 3

MyType

This item applies only to multilinear plastic link properties. It is 1, 2 or 3, indicating the hysteresis
type.

```
1 = Kinematic
2 = Takeda
3 = Pivot
```
a1

This item only applies to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Alpha1 hysteresis parameter.

a2

This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Alpha2 hysteresis parameter.

b1

This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Beta1 hysteresis parameter.

b2


This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Beta2 hysteresis parameter.

eta

This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Eta hysteresis parameter.

## Remarks

This function retrieves the force-deformation data for a specified degree of freedom in multilinear
elastic and multilinear plastic link properties.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

To successfully retrieve this data from the indicated link property, the following conditions must
be met:

1. The link property must be multilinear elastic or multilinear plastic.
2. The specified DOF must be active.
3. The specified DOF must not be fixed.
4. The specified DOF must be nonlinear.

## VBA Example

Sub GetLinkPropMultiLinearPoints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyF() As Double
Dim MyD() As Double
Dim NumberPoints As Long
Dim F() As Double
Dim D() As Double
Dim MyType As Long
Dim a1 As Double
Dim a2 As Double
Dim b1 As Double
Dim b2 As Double
Dim eta As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetMultiLinearPlastic("MLP1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, 2, 0)

'set multilinear force-defomation data
ReDim MyF(4)
ReDim MyD(4)

MyF(0) = -12
MyF(1) = -10
MyF(2) = 0
MyF(3) = 8
MyF(4) = 9

MyD(0) = -8
MyD(1) = -0.6
MyD(2) = 0
MyD(3) = 0.2
MyD(4) = 6

ret = SapModel.PropLink.SetMultiLinearPoints("MLP1", 2, 5, MyF, MyD, 3, 9, 12, 0.75, 0.8,
.1)

'get multilinear force-defomation data
ret = SapModel.PropLink.GetMultiLinearPoints("MLP1", 2, NumberPoints, F, D, MyType,


a1, a2, b1, b2, eta)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetMultiLinearPoints

SetMultiLinearElastic

GetMultiLinearElastic

SetMultiLinearPlastic

GetMultiLinearPlastic

# GetNameList

## Syntax

SapObject.SapModel.PropLink.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String, Optional
ByVal PropType As eLinkPropType) As Long

## Parameters

NumberNames

The number of link property names retrieved by the program.

MyName

This is a one-dimensional array of link property names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```

The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

PropType

This optional value is one of the following items in the eLinkPropType enumeration.

```
NLPROP_LINEAR = 1
NLPROP_DAMPER = 2
NLPROP_GAP = 3
NLPROP_HOOK = 4
NLPROP_PLASTIC_WEN = 5
NLPROP_ISOLATOR1 = 6 (Rubber isolator)
NLPROP_ISOLATOR2 = 7 (Friction isolator)
NLPROP_MULTILINEAR_ELASTIC = 8
NLPROP_MULTILINEAR_PLASTIC = 9
NLPROP_ISOLATOR3 = 10 (T/C Friction isolator)
```
If no value is input for PropType, names are returned for all link properties in the model regardless
of type.

## Remarks

This function retrieves the names of all defined link properties of the specified type.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetLinkPropNames()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
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

'add link properties
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)
ret = SapModel.PropLink.SetLinear("L2", DOF, Fixed, Ke, Ce, 0, 0)

'get link property names
ret = SapModel.PropLink.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetPDelta

## Syntax

SapObject.SapModel.PropLink.GetPDelta

## VB6 Procedure

Function GetPDelta(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing link property.

Value

This is an array of P-delta parameters.


```
Value(0) = M2 P-delta to I-end of link as moment, M2I
Value(1) = M2 P-delta to J-end of link as moment, M2J
Value(2) = M3 P-delta to I-end of link as moment, M3I
Value(3) = M3 P-delta to J-end of link as moment, M3J
```
## Remarks

This function retrieves P-delta parameters for a link property.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetLinkPropPDelta()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim MyValue() As Double
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'set link property P-delta parameters
ReDim MyValue(3)


MyValue(0) = 0.6
MyValue(1) = 0.4
MyValue(2) = 0.3
MyValue(3) = 0.2
ret = SapModel.PropLink.SetPDelta("L1", MyValue)

'get link property P-delta parameters
ret = SapModel.PropLink.GetPDelta("L1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetPDelta

# GetPlasticWen

## Syntax

SapObject.SapModel.PropLink.GetPlasticWen

## VB6 Procedure

Function GetPlasticWen(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef
k() As Double, ByRef Yield() As Double, ByRef Ratio() As Double, ByRef exp() As Double,
ByRef dj2 As Double, ByRef dj3 As Double, ByRef Notes As String, ByRef GUID As String) As
Long

## Parameters

Name

The name of an existing plastic Wen-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
```

### DOF(1) = U2

### DOF(2) = U3

### DOF(3) = R1

### DOF(4) = R2

### DOF(5) = R3

Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.


```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

Yield

This is an array of yield force terms for the link property. The yield force applies for nonlinear
analyses.

```
Yield(0) = U1 [F]
Yield(1) = U2 [F]
Yield(2) = U3 [F]
Yield(3) = R1 [FL]
Yield(4) = R2 [FL]
Yield(5) = R3 [FL]
```
The term Yield(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

Ratio

This is an array of post-yield stiffness ratio terms for the link property. The post-yield stiffness
ratio applies for nonlinear analyses. It is the post-yield stiffness divided by the initial stiffness.

```
Ratio(0) = U1
Ratio(1) = U2
Ratio(2) = U3
Ratio(3) = R1
Ratio(4) = R2
Ratio(5) = R3
```
The term Ratio(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.


exp

This is an array of yield exponent terms for the link property. The yield exponent applies for
nonlinear analyses. The yielding exponent that controls the sharpness of the transition from the
initial stiffness to the yielded stiffness.

```
exp(0) = U1
exp(1) = U2
exp(2) = U3
exp(3) = R1
exp(4) = R2
exp(5) = R3
```
The term exp(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a plastic Wen-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropPlasticWen()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double


Dim MyK() As Double
Dim MyYield() As Double
Dim MyRatio() As Double
Dim MyExp() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim k() As Double
Dim Yield() As Double
Dim Ratio() As Double
Dim exp() As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyYield(5)
ReDim MyRatio(5)
ReDim MyExp(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20


MyYield(1)= 50
MyRatio(1)= 0.1
MyExp(1)= 3

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetPlasticWen("PW1", MyDOF, MyFixed, MyNonLinear, MyKe,
MyCe, MyK, MyYield, MyRatio, MyExp, 2, 0)

'get link property data
ret = SapModel.PropLink.GetPlasticWen("PW1", DOF, Fixed, NonLinear, Ke, Ce, k, Yield,
Ratio, exp, dj2, dj3, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetPlasticWen

# GetRubberIsolator

## Syntax

SapObject.SapModel.PropLink.GetRubberIsolator

## VB6 Procedure

Function GetRubberIsolator(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef
k() As Double, ByRef Yield() As Double, ByRef Ratio() As Double, ByRef dj2 As Double,
ByRef dj3 As Double, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing rubber isolator-type link property.

DOF


This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1, Not Used
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1, Not Used
NonLinear(4) = R2, Not Used
NonLinear(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```

The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1, Not Used
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1, Not Used
k(4) = R2, Not Used
k(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Yield

This is an array of yield force terms for the link property. The yield force applies for nonlinear
analyses.

```
Yield(0) = U1, Not Used
Yield(1) = U2 [F]
Yield(2) = U3 [F]
Yield(3) = R1, Not Used
Yield(4) = R2, Not Used
Yield(5) = R3, Not Used
```
The term Yield(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

Ratio

This is an array of post-yield stiffness ratio terms for the link property. The post-yield stiffness
ratio applies for nonlinear analyses. It is the post-yield stiffness divided by the initial stiffness.

```
Ratio(0) = U1, Not Used
```

```
Ratio(1) = U2
Ratio(2) = U3
Ratio(3) = R1, Not Used
Ratio(4) = R2, Not Used
Ratio(5) = R3, Not Used
```
The term Ratio(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies pnly when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a rubber isolator-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropRubberIsolator()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MyYield() As Double
Dim MyRatio() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double


Dim Ce() As Double
Dim k() As Double
Dim Yield() As Double
Dim Ratio() As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyYield(5)
ReDim MyRatio(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MyYield(1)= 50
MyRatio(1)= 0.1

MyDOF(2) = True
MyNonLinear(2) = True
MyKe(2) = 15
MyCe(2) = 0.008
MyK(2) = 22
MyYield(2)= 60
MyRatio(2)= 0.15


MyDOF(3) = True
MyFixed(3) = True

ret = SapModel.PropLink.SetRubberIsolator("RI1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, MyK, MyYield, MyRatio, 2, 3)

'get link property data
ret = SapModel.PropLink.GetRubberIsolator("RI1", DOF, Fixed, NonLinear, Ke, Ce, k,
Yield, Ratio, dj2, dj3, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetRubberIsolator

# GetSpringData

## Syntax

SapObject.SapModel.PropLink.GetSpringData

## VB6 Procedure

Function GetSpringData(ByVal Name As String, ByRef DefinedForThisLength As Double,
ByRef DefinedForThisArea As Double) As Long

## Parameters

Name

The name of an existing link property.

DefinedForThisLength

The link property is defined for this length in a line (frame) spring. [L]

DefinedForThisArea

The link property is defined for this area in an area spring. [L^2 ]


## Remarks

This function retrieves length and area values for a link property that are used if the link property
is specified in line and area spring assignments.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetLinkPropSpringData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim DefinedForThisLength As Double
Dim DefinedForThisArea As Double

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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'set link property spring data
ret = SapModel.PropLink.SetSpringData("L1", 12, 2)

'get link property spring data
ret = SapModel.PropLink.GetSpringData("L1", DefinedForThisLength, DefinedForThisArea)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetSpringData

# GetTCFrictionIsolator

## Syntax

SapObject.SapModel.PropLink.GetTCFrictionIsolator

## VB6 Procedure

Function GetTCFrictionIsolator(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed
() As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByRef k() As Double, ByRef Slow() As Double, ByRef Fast() As Double, ByRef Rate() As
Double, ByRef Radius() As Double, ByRef SlowT() As Double, ByRef FastT() As Double, ByRef
RateT() As Double, ByRef kt As Double, ByRef dis As Double, ByRef dist As Double, ByRef
Damping As Double, ByRef dj2 As Double, ByRef dj3 As Double, ByRef Notes As String, ByRef
GUID As String) As Long

## Parameters

Name

The name of an existing T/C friction isolator-type link property.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed


This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies pnly when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1, Not Used
NonLinear(4) = R2, Not Used
NonLinear(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U1, U2 and U3. For those degrees of
freedom, the term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
```

```
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1, Not Used
k(4) = R2, Not Used
k(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U1, U2 and U3. For those degrees of
freedom, the term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Slow

This is an array of the friction coefficient at zero velocity terms when U1 is in compression for the
link property. This coefficient applies for nonlinear analyses.

```
Slow(0) = U1, Not Used
Slow(1) = U2
Slow(2) = U3
Slow(3) = R1, Not Used
Slow(4) = R2, Not Used
Slow(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Slow(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Fast

This is an array of the friction coefficient at fast velocity terms when U1 is in compression for the
link property. This coefficient applies for nonlinear analyses.

```
Fast(0) = U1, Not Used
Fast(1) = U2
Fast(2) = U3
Fast(3) = R1, Not Used
Fast(4) = R2, Not Used
Fast(5) = R3, Not Used
```

Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Fast(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Rate

This is an array of the inverse of the characteristic sliding velocity terms when U1 is in
compression for the link property. This item applies for nonlinear analyses.

```
Rate(0) = U1, Not Used
Rate(1) = U2 [s/L]
Rate(2) = U3 [s/L]
Rate(3) = R1, Not Used
Rate(4) = R2, Not Used
Rate(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Rate(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Radius

This is an array of the radius of the sliding contact surface terms for the link property. Inputting 0
means there is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.

```
Radius(0) = U1, Not Used
Radius(1) = U2 [L]
Radius(2) = U3 [L]
Radius(3) = R1, Not Used
Radius(4) = R2, Not Used
Radius(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Radius(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.

SlowT

This is an array of the friction coefficient at zero velocity terms when U1 is in tension for the link
property. This coefficient applies for nonlinear analyses.

```
SlowT(0) = U1, Not Used
SlowT(1) = U2
SlowT(2) = U3
SlowT(3) = R1, Not Used
SlowT(4) = R2, Not Used
SlowT(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term SlowT(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.


FastT

This is an array of the friction coefficient at fast velocity terms when U1 is in tension for the link
property. This coefficient applies for nonlinear analyses.

```
FastT(0) = U1, Not Used
FastT(1) = U2
FastT(2) = U3
FastT(3) = R1, Not Used
FastT(4) = R2, Not Used
FastT(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term FastT(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

RateT

This is an array of the inverse of the characteristic sliding velocity terms when U1 is in tension for
the link property. This item applies for nonlinear analyses.

```
RateT(0) = U1, Not Used
RateT(1) = U2 [s/L]
RateT(2) = U3 [s/L]
RateT(3) = R1, Not Used
RateT(4) = R2, Not Used
RateT(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term RateT(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

kt

The axial translational tension stiffness for the U1 degree of freedom. This item applies for
nonlinear analyses. [F/L]

dis

The U1 degree of freedom gap opening for compression. This item applies for nonlinear analyses.
[L]

dist

The U1 degree of freedom gap opening for tension. This item applies for nonlinear analyses. [L]

Damping

The nonlinear damping coefficient used for the axial translational degree of freedom, U1. This
item applies for nonlinear analyses. [F/L]

dj2


The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a T/C friction isolator-type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropTCFrictionIsolator()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MySlow() As Double
Dim MyFast() As Double
Dim MyRate() As Double
Dim MyRadius() As Double
Dim MySlowT() As Double
Dim MyFastT() As Double
Dim MyRateT() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim k() As Double
Dim Slow() As Double
Dim Fast() As Double
Dim Rate() As Double


Dim Radius() As Double
Dim SlowT() As Double
Dim FastT() As Double
Dim RateT() As Double
Dim kt As Double
Dim dis As Double
Dim dist As Double
Dim Damping As Double
Dim dj2 As Double
Dim dj3 As Double
Dim Notes As String
Dim GUID As String

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MySlow(5)
ReDim MyFast(5)
ReDim MyRate(5)
ReDim MyRadius(5)
ReDim MySlowT(5)
ReDim MyFastT(5)
ReDim MyRateT(5)

MyDOF(0) = True
MyNonLinear(0) = True
MyKe(0) = 12
MyCe(0) = 0.01
MyK(0) = 1000

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01


MyK(1) = 20
MySlow(1)= 0.6
MyFast(1)= 0.5
MyRate(1)= 10
MyRadius(1)= 80
MySlowT(1)= 0.61
MyFastT(1)= 0.51
MyRateT(1)= 10.1

MyDOF(2) = True
MyNonLinear(2) = True
MyKe(2) = 14
MyCe(2) = 0.008
MyK(2) = 22
MySlow(2)= 0.66
MyFast(2)= 0.55
MyRate(2)= 12
MyRadius(2)= 75
MySlowT(2)= 0.67
MyFastT(2)= 0.56
MyRateT(2)= 12.1

MyDOF(3) = True
MyKe(3) = 15
MyCe(3) = 0

MyDOF(4) = True
MyFixed(4) = True

ret = SapModel.PropLink.SetTCFrictionIsolator("TCFI1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, MyK, MySlow, MyFast, MyRate, MyRadius, MySlowT, MyFastT, MyRateT, 18,
2, 3, 0.1, 2, 3)

'get link property data
ret = SapModel.PropLink.GetTCFrictionIsolator("TCFI1", DOF, Fixed, NonLinear, Ke, Ce,
k, Slow, Fast, Rate, Radius, SlowT, FastT, RateT, kt, dis, dist, Damping, dj2, dj3, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetTCFrictionIsolator


# GetTriplePendulumIsolator

## Syntax

SapObject.SapModel.PropLink.GetTriplePendulumIsolator

## VB6 Procedure

Function GetTriplePendulumIsolator(ByVal Name As String, ByRef dof() As Boolean, ByRef
Fixed() As Boolean, ByRef Nonlinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As
Double, ByRef K1 As Double, ByRef Damping As Double, ByRef K() As Double, ByRef Slow()
As Double, ByRef Fast() As Double, ByRef Rate() As Double, ByRef Radius() As Double, ByRef
StopDist() As Double, ByRef HeightOut As Double, ByRef HeightIn As Double, ByRef dj2 As
Double, ByRef dj3 As Double, ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing Triple Pendulum Isolator type link property.

DOF

This is a Boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a Boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) only applies when DOF(n) = True.

NonLinear


This is a Boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1, Not Used
NonLinear(4) = R2, Not Used
NonLinear(5) = R3, Not Used
```
Note that this item is applicable for degrees of freedom U1, U2 and U3 only. For those degrees of
freedom, the term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses, and also for nonlinear analysis for those DOF for which NonLinear(n) = False.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

K1

This is the axial compression stiffness for the U1 degree of freedom. This item applies for
nonlinear analyses. [F/L]

Damping

This is the nonlinear damping coefficient for the axial degree of freedom, U1, when it is in
compression. This item applies for nonlinear analyses. [F/L]

K


This is an array, dimensioned to 3, of initial nonlinear stiffness (before sliding) for each sliding
surface.

```
K(0) = for the outer top sliding surface [F/L]
K(1) = for the outer bottom sliding surface [F/L]
K(2) = for the inner top sliding surface [F/L]
K(3) = for the inner bottom sliding surface [F/L]
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Slow

This is an array, dimensioned to 3, of the friction coefficient at zero velocity for each sliding
surface when U1 is in compression.

```
Slow(0) = for the outer top sliding surface
Slow(1) = for the outer bottom sliding surface
Slow(2) = for the inner top sliding surface
Slow(3) = for the inner bottom sliding surface
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term Slow(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Fast

This is an array, dimensioned to 3, of the friction coefficient at fast velocity for each sliding
surface when U1 is in compression.

```
Fast(0) = for the outer top sliding surface
Fast(1) = for the outer bottom sliding surface
Fast(2) = for the inner top sliding surface
Fast(3) = for the inner bottom sliding surface
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term Fast(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Rate

This is an array, dimensioned to 3, of the inverse of the characteristic sliding velocity for the Slow
and Fast friction coefficients for each sliding surface. This item applies for nonlinear analyses.

```
Rate(0) = for the outer top sliding surface [s/L]
Rate(1) = for the outer bottom sliding surface [s/L]
Rate(2) = for the inner top sliding surface [s/L]
Rate(3) = for the inner bottom sliding surface [s/L]
```

Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term Rate(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Radius

This is an array, dimensioned to 3, of the radius for each sliding surface. Inputting 0 means there
is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.

```
Radius(0) = for the outer top sliding surface [L]
Radius(1) = for the outer bottom sliding surface [L]
Radius(2) = for the inner top sliding surface [L]
Radius(3) = for the inner bottom sliding surface [L]
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term Radius(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.

StopDist

This is an array, dimensioned to 3, of the amount of displacement allowed before hitting a stiff
limit for each sliding surface. Inputting 0 means there is no stop. This item applies for nonlinear
analyses.

```
StopDist(0) = for the outer top sliding surface [L]
StopDist(1) = for the outer bottom sliding surface [L]
StopDist(2) = for the inner top sliding surface [L]
StopDist(3) = for the inner bottom sliding surface [L]
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term StopDist(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.

HeightOut

This is the height (distance) between the outer sliding surfaces at zero displacement. [L]

Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

HeightIn

This is the height (distance) between the inner sliding surfaces. [L]

Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring, that is, the center of the isolator.
This item applies only when DOF(2) = True. [L]

dj3


The distance from the J-End of the link to the U3 shear spring, that is, the center of the isolator.
This item applies only when DOF(3) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves link property data for a Triple Pendulum Isolator type link property.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetLinkPropTriplePendulumIsolator()
'dimension variables
Dim SapObject As Sap2000.SapObject
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MySlow() As Double
Dim MyFast() As Double
Dim MyRate() As Double
Dim MyRadius() As Double
Dim MyStopDist() As Double
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Nonlinear() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim K() As Double
Dim Slow() As Double
Dim Fast() As Double
Dim Rate() As Double
Dim Radius() As Double
Dim StopDist() As Double
Dim K1 As Double
Dim Damping As Double
Dim Hout As Double
Dim Hin As Double
Dim dj2 As Double


Dim dj3 As Double
Dim Notes As String
Dim GUID As String

'create Sap2000 object
Set SapObject = New SAP2000.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(3)
ReDim MySlow(3)
ReDim MyFast(3)
ReDim MyRate(3)
ReDim MyRadius(3)
ReDim MyStopDist(3)

MyDOF(0) = True
MyNonLinear(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01

MyDOF(2) = True
MyNonLinear(2) = True
MyKe(2) = 14
MyCe(2) = 0.008

MyK(0) = 20
MySlow(0)= 0.6
MyFast(0)= 0.5
MyRate(0)= 10
MyRadius(0)= 80
MyStopDist(0)= 8


MyK(1) = 22
MySlow(1)= 0.66
MyFast(1)= 0.55
MyRate(1)= 12
MyRadius(1)= 75
MyStopDist(1)= 8

MyK(2) = 20
MySlow(2)= 0.6
MyFast(2)= 0.5
MyRate(2)= 10
MyRadius(2)= 80
MyStopDist(2)= 8

MyK(3) = 20
MySlow(3)= 0.6
MyFast(3)= 0.5
MyRate(3)= 10
MyRadius(3)= 80
MyStopDist(3)= 8

MyDOF(3) = True
MyKe(3) = 15
MyCe(3) = 0

MyDOF(4) = True
MyFixed(4) = True

ret = SapModel.PropLink.SetTriplePendulumIsolator("TPI1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, 1000, 0.1, MyK, MySlow, MyFast, MyRate, MyRadius,
MyStopDist, 6, 3, 3, 3)

'get link property data
ret = SapModel.PropLink.GetTriplePendulumIsolator("TPI1", DOF, Fixed, NonLinear, Ke,
Ce, K1, Damping, K, Slow, Fast, Rate, Radius, StopDist, Hout, Hin, dj2, dj3, Notes, GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.00.

## See Also

SetTriplePendulumIsolator


# GetTypeOAPI

## Syntax

SapObject.SapModel.PropLink.GetTypeOAPI

## VB6 Procedure

Function GetTypeOAPI(ByVal Name As String, ByRef PropType As eLinkPropType) As Long

## Parameters

Name

The name of an existing link property.

PropType

This is one of the following items in the eLinkPropType enumeration.

```
NLPROP_LINEAR = 1
NLPROP_DAMPER = 2
NLPROP_GAP = 3
NLPROP_HOOK = 4
NLPROP_PLASTIC_WEN = 5
NLPROP_ISOLATOR1 = 6 (Rubber isolator)
NLPROP_ISOLATOR2 = 7 (Friction isolator)
NLPROP_MULTILINEAR_ELASTIC = 8
NLPROP_MULTILINEAR_PLASTIC = 9
NLPROP_ISOLATOR3 = 10 (T/C Friction isolator)
```
## Remarks

This function retrieves the property type for the specified link property.

The function returns zero if the type is successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetLinkPropType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim PropType As eLinkPropType


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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'get link property type
ret = SapModel.PropLink.GetTypeOAPI("L1", PropType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Changed function name to GetTypeOAPI in v17.0.0.

## See Also

# GetWeightAndMass

## Syntax

SapObject.SapModel.PropLink.GetWeightAndMass


## VB6 Procedure

Function GetWeightAndMass(ByVal Name As String, ByRef w As Double, ByRef m As Double,
ByRef R1 As Double, ByRef R2 As Double, ByRef R3 As Double) As Long

## Parameters

Name

The name of an existing link property.

w

The weight of the link. [F]

m

The translational mass of the link. [M]

R1

The rotational inertia of the link about its local 1 axis. [ML^2 ]

R2

The rotational inertia of the link about its local 2 axis. [ML^2 ]

R3

The rotational inertia of the link about its local 3 axis. [ML^2 ]

## Remarks

This function retrieves weight and mass data for a link property.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetLinkPropWeightAndMass()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim w As Double
Dim m As Double
Dim R1 As Double


Dim R2 As Double
Dim R3 As Double

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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'set link property weight and mass
ret = SapModel.PropLink.SetWeightAndMass("L1", 10, 0.26, 0.0012, 0.0014, 0.0016)

'get link property weight and mass
ret = SapModel.PropLink.GetWeightAndMass("L1", w, m, R1, R2, R3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetWeightAndMass


# SetDamper

## Syntax

SapObject.SapModel.PropLink.SetDamper

## VB6 Procedure

Function SetDamper(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef
k() As Double, ByRef c() As Double, ByRef cexp() As Double, ByVal dj2 As Double, ByVal dj3
As Double, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.


```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) only applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.


c

This is an array of nonlinear damping coefficient terms for the link property. The nonlinear
damping coefficient applies for nonlinear analyses.

```
c(0) = U1 [F/(L^cexp)]
c(1) = U2 [F/(L^cexp)]
c(2) = U3 [F/(L^cexp)]
c(3) = R1 [FL]
c(4) = R2 [FL]
c(5) = R3 [FL]
```
The term c(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

cexp

This is an array of the nonlinear damping exponent terms. The nonlinear damping exponent
applies for nonlinear analyses. It is applied to the velocity across the damper in the equation of
motion.

```
cexp(0) = U1
cexp(1) = U2
cexp(2) = U3
cexp(3) = R1
cexp(4) = R2
cexp(5) = R3
```
The term cexp(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes an exponential damper-type link property. If this function is called for an
existing link property, all items for the property are reset to their default values.


The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropDamper()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MyC() As Double
Dim MyCexp() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyC(5)
ReDim MyCexp(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01


MyK(1) = 20
MyC(1)=0.08
MyCexp(1) = 1.2

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetDamper("D1", MyDOF, MyFixed, MyNonLinear, MyKe,
MyCe, MyK, MyC, MyCexp, 1, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

Clarification that damper type is exponential added in version 16.0.2.

## See Also

GetDamper

# SetDamperBilinear

## Syntax

SapObject.SapModel.PropLink.SetDamperBilinear

## VB6 Procedure

Function SetDamperBilinear (ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed()
As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByRef k() As Double, ByRef c() As Double, ByRef cy() As Double, ByRef ForceLimit() As
Double, ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal Notes As String = "",
Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF


This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained.)

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
```

```
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) only applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

c

This is an array of nonlinear initial damping coefficient terms for the link property. The nonlinear
initial damping coefficient applies for nonlinear analyses.

```
c(0) = U1 [F/L]
c(1) = U2 [F/L]
c(2) = U3 [F/L]
c(3) = R1 [FL]
c(4) = R2 [FL]
c(5) = R3 [FL]
```
The term c(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

cy

This is an array of nonlinear yielded damping coefficient terms for the link property. The
nonlinear yielded damping coefficient applies for nonlinear analyses.

```
cy(0) = U1 [F/L]
cy(1) = U2 [F/L]
cy(2) = U3 [F/L]
cy(3) = R1 [FL]
cy(4) = R2 [FL]
cy(5) = R3 [FL]
```
The term cy(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

ForceLimit

This is an array of nonlinear linear force limit terms for the link property. The linear force limit
applies for nonlinear analyses.

```
ForceLimit(0) = U1 [F]
ForceLimit(1) = U2 [F]
ForceLimit(2) = U3 [F]
ForceLimit(3) = R1 [FL]
ForceLimit(4) = R2 [FL]
```

```
ForceLimit(5) = R3 [FL]
```
The term ForceLimit(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a bilinear damper-type link property. If this function is called for an
existing link property, all items for the property are reset to their default values.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropDamperBilinear ()

```
'dimension variables
```
```
Dim SapObject as cOAPI
```
```
Dim SapModel As cSapModel
```
```
Dim ret As Long
```
```
Dim MyDOF() As Boolean
```
```
Dim MyFixed() As Boolean
```
```
Dim MyNonLinear() As Boolean
```
```
Dim MyKe() As Double
```
```
Dim MyCe() As Double
```

```
Dim MyK() As Double
```
```
Dim MyC() As Double
```
```
Dim MyCy() As Double
```
```
Dim MyForceLimit() As Double
```
'create Sap2000 object

```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
'start Sap2000 application

```
SapObject.ApplicationStart
```
'create SapModel object

```
Set SapModel = SapObject.SapModel
```
'initialize model

```
ret = SapModel.InitializeNewModel
```
'create model from template

```
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
'add link property

```
ReDim MyDOF(5)
```
```
ReDim MyFixed(5)
```
```
ReDim MyNonLinear(5)
```
```
ReDim MyKe(5)
```
```
ReDim MyCe(5)
```
```
ReDim MyK(5)
```
```
ReDim MyC(5)
```

```
ReDim MyCy(5)
```
```
ReDim MyForceLimit(5)
```
```
MyDOF(0) = True
```
```
MyKe(0) = 12
```
```
MyCe(0) = 0.01
```
```
MyDOF(1) = True
```
```
MyNonLinear(1) = True
```
```
MyKe(1) = 12
```
```
MyCe(1) = 0.01
```
```
MyK(1) = 20
```
```
MyC(1)=0.08
```
```
MyCy(1) = 0.008
```
```
MyForceLimit(1) = 50
```
```
MyDOF(2) = True
```
```
MyFixed(2) = True
```
```
ret = SapModel.PropLink.SetDamperBilinear("D1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, MyK, MyC, MyCy, MyForceLimit, 1, 0)
```
```
'close Sap2000
```
```
SapObject.ApplicationExit False
```
```
Set SapModel = Nothing
```
```
Set SapObject = Nothing
```
End Sub

## Release Notes


Initial release in version 16.0.2.

## See Also

GetDamperBilinear

# SetDamperFrictionSpring

## Syntax

SapObject.SapModel.PropLink.SetDamperFrictionSpring

## VB6 Procedure

Function SetDamperFrictionSpring(ByVal Name As String, ByRef DOF() As Boolean, ByRef
Fixed() As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As
Double, ByRef k() As Double, ByRef k1() As Double, ByRef k2() As Double, ByRef u0() As
Double, ByRef us() As Double, ByRef dir() As Long, ByVal dj2 As Double, ByVal dj3 As
Double, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained.)

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.


NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial (nonslipping) stiffness terms for the link property. The initial stiffness
applies for nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) only applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

k1


This is an array of slipping stiffness when loading terms for the link property. The slipping
stiffness when loading applies for nonlinear analyses.

```
k1(0) = U1 [F/L]
k1(1) = U2 [F/L]
k1(2) = U3 [F/L]
k1(3) = R1 [FL]
k1(4) = R2 [FL]
k1(5) = R3 [FL]
```
The term k1(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

k2

This is an array of slipping stiffness when unloading terms for the link property. The slipping
stiffness when unloading applies for nonlinear analyses.

```
k2(0) = U1 [F/L]
k2(1) = U2 [F/L]
k2(2) = U3 [F/L]
k2(3) = R1 [FL]
k2(4) = R2 [FL]
k2(5) = R3 [FL]
```
The term k2(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

u0

This is an array of precompression displacement terms for the link property. The nonlinear
precompression displacement applies for nonlinear analyses.

```
u0(0) = U1 [L]
u0(1) = U2 [L]
u0(2) = U3 [L]
u0(3) = R1
u0(4) = R2
u0(5) = R3
```
The term u0(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

us

This is an array of stop displacement terms for the link property. The nonlinear stop displacement
applies for nonlinear analyses.

```
us(0) = U1 [L]
us(1) = U2 [L]
us(2) = U3 [L]
us(3) = R1
us(4) = R2
us(5) = R3
```
The term us(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]


dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a friction spring damper-type link property. If this function is called for an
existing link property, all items for the property are reset to their default values.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropDamperFrictionSpring()

```
'dimension variables
```
```
Dim SapObject as cOAPI
```
```
Dim SapModel As cSapModel
```
```
Dim ret As Long
```
```
Dim MyDOF() As Boolean
```
```
Dim MyFixed() As Boolean
```
```
Dim MyNonLinear() As Boolean
```
```
Dim MyKe() As Double
```
```
Dim MyCe() As Double
```
```
Dim MyK() As Double
```
```
Dim MyK1() As Double
```
```
Dim MyK2() As Double
```
```
Dim MyU0() As Double
```
```
Dim MyUs() As Double
```

```
Dim MyDir() As Long
```
'create Sap2000 object

```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
'start Sap2000 application

```
SapObject.ApplicationStart
```
'create SapModel object

```
Set SapModel = SapObject.SapModel
```
'initialize model

```
ret = SapModel.InitializeNewModel
```
'create model from template

```
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
'add link property

```
ReDim MyDOF(5)
```
```
ReDim MyFixed(5)
```
```
ReDim MyNonLinear(5)
```
```
ReDim MyKe(5)
```
```
ReDim MyCe(5)
```
```
ReDim MyK(5)
```
```
ReDim MyK1(5)
```
```
ReDim MyK2(5)
```
```
ReDim MyU0(5)
```
```
ReDim MyUs(5)
```

```
ReDim MyDir(5)
```
```
MyDOF(0) = True
```
```
MyKe(0) = 12
```
```
MyCe(0) = 0.01
```
```
MyDOF(1) = True
```
```
MyNonLinear(1) = True
```
```
MyKe(1) = 12
```
```
MyCe(1) = 0.01
```
```
MyK(1) = 20
```
```
MyK1(1)=2
```
```
MyK2(1) = 1
```
```
MyU0(1) = -.2
```
```
MyUs(1) = 1
```
```
MyDir(1) = 2
```
```
MyDOF(2) = True
```
```
MyFixed(2) = True
```
```
ret = SapModel.PropLink.SetDamperFrictionSpring("D1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, MyK, MyK1, MyK2, MyU0, MyUs, MyDir, 1, 0)
```
```
'close Sap2000
```
```
SapObject.ApplicationExit False
```
```
Set SapModel = Nothing
```
```
Set SapObject = Nothing
```
End Sub


## Release Notes

Initial release in version 16.0.2.

## See Also

GetDamperFrictionSpring

# SetDamperLinearExponential

## Syntax

SapObject.SapModel.PropLink.SetDamperLinearExponential

## VB6 Procedure

Function SetDamperLinearExponential(ByVal Name As String, ByRef DOF() As Boolean, ByRef
Fixed() As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As
Double, ByRef k() As Double, ByRef c() As Double, ByRef cexp() As Double, ByRef ForceLimit
() As Double, ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal Notes As String = "",
Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained.)

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
```

```
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
```

```
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) only applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

c

This is an array of nonlinear damping coefficient terms for the link property. The nonlinear
damping coefficient applies for nonlinear analyses.

```
c(0) = U1 [F/(L^cexp)]
c(1) = U2 [F/(L^cexp)]
c(2) = U3 [F/(L^cexp)]
c(3) = R1 [FL]
c(4) = R2 [FL]
c(5) = R3 [FL]
```
The term c(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

cexp

This is an array of the nonlinear damping exponent terms. The nonlinear damping exponent
applies for nonlinear analyses. It is applied to the velocity across the damper in the equation of
motion.

```
cexp(0) = U1
cexp(1) = U2
cexp(2) = U3
cexp(3) = R1
cexp(4) = R2
cexp(5) = R3
```
The term cexp(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

ForceLimit

This is an array of nonlinear linear force limit terms for the link property. The linear force limit
applies for nonlinear analyses.

```
ForceLimit(0) = U1 [F]
ForceLimit(1) = U2 [F]
ForceLimit(2) = U3 [F]
ForceLimit(3) = R1 [FL]
ForceLimit(4) = R2 [FL]
ForceLimit(5) = R3 [FL]
```
The term ForceLimit(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]


dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a linear exponential damper-type link property. If this function is called
for an existing link property, all items for the property are reset to their default values.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropDamperLinearExponential()

```
'dimension variables
```
```
Dim SapObject as cOAPI
```
```
Dim SapModel As cSapModel
```
```
Dim ret As Long
```
```
Dim MyDOF() As Boolean
```
```
Dim MyFixed() As Boolean
```
```
Dim MyNonLinear() As Boolean
```
```
Dim MyKe() As Double
```
```
Dim MyCe() As Double
```
```
Dim MyK() As Double
```
```
Dim MyC() As Double
```
```
Dim MyCexp() As Double
```
```
Dim MyForceLimit() As Double
```

'create Sap2000 object

```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
'start Sap2000 application

```
SapObject.ApplicationStart
```
'create SapModel object

```
Set SapModel = SapObject.SapModel
```
'initialize model

```
ret = SapModel.InitializeNewModel
```
'create model from template

```
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
```
'add link property

```
ReDim MyDOF(5)
```
```
ReDim MyFixed(5)
```
```
ReDim MyNonLinear(5)
```
```
ReDim MyKe(5)
```
```
ReDim MyCe(5)
```
```
ReDim MyK(5)
```
```
ReDim MyC(5)
```
```
ReDim MyCexp(5)
```
```
ReDim MyForceLimit(5)
```
```
MyDOF(0) = True
```
```
MyKe(0) = 12
```

```
MyCe(0) = 0.01
```
```
MyDOF(1) = True
```
```
MyNonLinear(1) = True
```
```
MyKe(1) = 12
```
```
MyCe(1) = 0.01
```
```
MyK(1) = 20
```
```
MyC(1)=0.08
```
```
MyCexp(1) = 1.2
```
```
MyForceLimit(1) = 50
```
```
MyDOF(2) = True
```
```
MyFixed(2) = True
```
```
ret = SapModel.PropLink.SetDamperLinearExponential("D1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, MyK, MyC, MyCexp, MyForceLimit, 1, 0)
```
```
'close Sap2000
```
```
SapObject.ApplicationExit False
```
```
Set SapModel = Nothing
```
```
Set SapObject = Nothing
```
End Sub

## Release Notes

Initial release in version 16.0.2.

## See Also

GetDamperLinearExponential

# SetFrictionIsolator


## Syntax

SapObject.SapModel.PropLink.SetFrictionIsolator

## VB6 Procedure

Function SetFrictionIsolator(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed()
As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByRef k() As Double, ByRef Slow() As Double, ByRef Fast() As Double, ByRef Rate() As
Double, ByRef Radius() As Double, ByVal Damping As Double, ByVal dj2 As Double, ByVal
dj3 As Double, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "") As
Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.


```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1, Not Used
NonLinear(4) = R2, Not Used
NonLinear(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U1, U2 and U3. For those degrees of
freedom, the term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1, Not Used
k(4) = R2, Not Used
k(5) = R3, Not Used
```

Note that this item is applicable only for degrees of freedom U1, U2 and U3. For those degrees of
freedom, the term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Slow

This is an array of the friction coefficient at zero velocity terms for the link property. This
coefficient applies for nonlinear analyses.

```
Slow(0) = U1, Not Used
Slow(1) = U2
Slow(2) = U3
Slow(3) = R1, Not Used
Slow(4) = R2, Not Used
Slow(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Slow(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Fast

This is an array of the friction coefficient at fast velocity terms for the link property. This
coefficient applies for nonlinear analyses.

```
Fast(0) = U1, Not Used
Fast(1) = U2
Fast(2) = U3
Fast(3) = R1, Not Used
Fast(4) = R2, Not Used
Fast(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Fast(n) applies pnly when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Rate

This is an array of the inverse of the characteristic sliding velocity terms for the link property. This
item applies for nonlinear analyses.

```
Rate(0) = U1, Not Used
Rate(1) = U2 [s/L]
Rate(2) = U3 [s/L]
Rate(3) = R1, Not Used
Rate(4) = R2, Not Used
Rate(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Rate(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.


Radius

This is an array of the radius of the sliding contact surface terms for the link property. Inputting 0
means there is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.

```
Radius(0) = U1, Not Used
Radius(1) = U2 [L]
Radius(2) = U3 [L]
Radius(3) = R1, Not Used
Radius(4) = R2, Not Used
Radius(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Radius(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.

Damping

This is the nonlinear damping coefficient used for the axial translational degree of freedom, U1.
This item applies for nonlinear analyses. [F/L]

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a friction isolator-type link property. If this function is called for an
existing link property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropFrictionIsolator()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MySlow() As Double
Dim MyFast() As Double
Dim MyRate() As Double
Dim MyRadius() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MySlow(5)
ReDim MyFast(5)
ReDim MyRate(5)
ReDim MyRadius(5)

MyDOF(0) = True
MyNonLinear(0) = True
MyKe(0) = 12
MyCe(0) = 0.01
MyK(0) = 1000

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MySlow(1)= 0.6


MyFast(1)= 0.5
MyRate(1)= 10
MyRadius(1)= 80

MyDOF(2) = True
MyNonLinear(2) = True
MyKe(2) = 14
MyCe(2) = 0.008
MyK(2) = 22
MySlow(2)= 0.66
MyFast(2)= 0.55
MyRate(2)= 12
MyRadius(2)= 75

MyDOF(3) = True
MyKe(3) = 15
MyCe(3) = 0

MyDOF(4) = True
MyFixed(4) = True

ret = SapModel.PropLink.SetFrictionIsolator("FI1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, MyK, MySlow, MyFast, MyRate, MyRadius, 0.1, 2, 3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetFrictionIsolator

# SetGap

## Syntax

SapObject.SapModel.PropLink.SetGap

## VB6 Procedure

Function SetGap(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As Boolean,
ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef k() As


Double, ByRef dis() As Double, ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal
Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property then that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke


This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dis

This is an array of initial gap opening terms for the link property. The initial gap opening applies
for nonlinear analyses.

```
dis(0) = U1 [L]
dis(1) = U2 [L]
dis(2) = U3 [L]
dis(3) = R1 [rad]
dis(4) = R2 [rad]
dis(5) = R3 [rad]
```

The term dis(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a gap-type link property. If this function is called for an existing link
property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropGap()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MyDis() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyDis(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MyDis(1)=1.2

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetGap("G1", MyDOF, MyFixed, MyNonLinear, MyKe, MyCe,
MyK, MyDis, 2, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetGap

# SetHook


## Syntax

SapObject.SapModel.PropLink.SetHook

## VB6 Procedure

Function SetHook(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As Boolean,
ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef k() As
Double, ByRef dis() As Double, ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal
Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property then that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
```

```
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dis


This is an array of initial hook opening terms for the link property. The initial hook opening
applies for nonlinear analyses.

```
c(0) = U1 [L]
c(1) = U2 [L]
c(2) = U3 [L]
c(3) = R1 [rad]
c(4) = R2 [rad]
c(5) = R3 [rad]
```
The term dis(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a hook-type link property. If this function is called for an existing link
property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropHook()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double


Dim MyDis() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyDis(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MyDis(1)=1.2

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetHook("H1", MyDOF, MyFixed, MyNonLinear, MyKe, MyCe,
MyK, MyDis, 2, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

GetHook

# SetLinear

## Syntax

SapObject.SapModel.PropLink.SetLinear

## VB6 Procedure

Function SetLinear(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByVal dj2 As Double, ByVal dj3 As
Double, Optional ByVal KeCoupled As Boolean = False, Optional ByVal CeCoupled As Boolean
= False, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity if DOF(0) = True
Fixed(1) = U2 fixity if DOF(1) = True
Fixed(2) = U3 fixity if DOF(2) = True
Fixed(3) = R1 fixity if DOF(3) = True
Fixed(4) = R2 fixity if DOF(4) = True
Fixed(5) = R3 fixity if DOF(5) = True
```
Ke


This is an array of stiffness terms for the link property. There are 6 terms in the array if the
stiffness is uncoupled and 21 if it is coupled. The KeCoupled item indicates if the stiffness is
coupled.

If the stiffness is uncoupled:

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
If the stiffness is coupled:

```
Ke(0) = U1U1 [F/L]
Ke(1) = U1U2 [F/L]
Ke(2) = U2U2 [F/L]
Ke(3) = U1U3 [F/L]
Ke(4) = U2U3 [F/L]
Ke(5) = U3U3 [F/L]
Ke(6) = U1R1 [F]
Ke(7) = U2R1 [F]
Ke(8) = U3R1 [F]
Ke(9) = R1R1 [FL]
Ke(10) = U1R2 [F]
Ke(11) = U2R2 [F]
Ke(12) = U3R2 [F]
Ke(13) = R1R2 [FL]
Ke(14) = R2R2 [FL]
Ke(15) = U1R3 [F]
Ke(16) = U2R3 [F]
Ke(17) = U3R3 [F]
Ke(18) = R1R3 [FL]
Ke(19) = R2R3 [FL]
Ke(20) = R3R3 [FL]
```
Ce

This is an array of damping terms for the link property. There are 6 terms in the array if the
damping is uncoupled and 21 if it is coupled. The CeCoupled item indicates if the damping is
coupled.

If the damping is uncoupled:

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```

If the damping is coupled:

```
Ce(0) = U1U1 [F/L]
Ce(1) = U1U2 [F/L]
Ce(2) = U2U2 [F/L]
Ce(3) = U1U3 [F/L]
Ce(4) = U2U3 [F/L]
Ce(5) = U3U3 [F/L]
Ce(6) = U1R1 [F]
Ce(7) = U2R1 [F]
Ce(8) = U3R1 [F]
Ce(9) = R1R1 [FL]
Ce(10) = U1R2 [F]
Ce(11) = U2R2 [F]
Ce(12) = U3R2 [F]
Ce(13) = R1R2 [FL]
Ce(14) = R2R2 [FL]
Ce(15) = U1R3 [F]
Ce(16) = U2R3 [F]
Ce(17) = U3R3 [F]
Ce(18) = R1R3 [FL]
Ce(19) = R2R3 [FL]
Ce(20) = R3R3 [FL]
```
dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

KeCoupled

This item is True if the link stiffness, Ke, is coupled. There are 21 terms in the Ke array if Ke is
coupled; otherwise there are 6 terms.

CeCoupled

This item is True if the link damping, Ce, is coupled. There are 21 terms in the Ce array if Ce is
coupled; otherwise there are 6 terms.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.


## Remarks

This function initializes a linear-type link property. If this function is called for an existing link
property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropLinear()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double

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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

GetLinear

# SetMultiLinearElastic

## Syntax

SapObject.SapModel.PropLink.SetMultiLinearElastic

## VB6 Procedure

Function SetMultiLinearElastic(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed()
As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal Notes As String = "", Optional
ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property then. that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
```

```
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]


dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a multilinear elastic-type link property. If this function is called for an
existing link property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropMultiLinearElastic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double

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

'add link property
ReDim MyDOF(5)


ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetMultiLinearElastic("MLE1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, 2, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetMultiLinearElastic

GetMultiLinearPoints

SetMultiLinearPoints

# SetMultiLinearPlastic

## Syntax

SapObject.SapModel.PropLink.SetMultiLinearPlastic

## VB6 Procedure

Function SetMultiLinearPlastic(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed()
As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,


ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal Notes As String = "", Optional
ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke


This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a multilinear plastic-type link property. If this function is called for an
existing link property, all items for the property are reset to their default values.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.


## VBA Example

Sub SetLinkPropMultiLinearPlastic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetMultiLinearPlastic("MLP1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, 2, 0)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetMultiLinearPlastic

GetMultiLinearPoints

SetMultiLinearPoints

# SetMultiLinearPoints

## Syntax

SapObject.SapModel.PropLink.SetMultiLinearPoints

## VB6 Procedure

Function SetMultiLinearPoints(ByVal Name As String, ByVal DOF As Long, ByVal
NumberPoints As Long, ByRef F() As Double, ByRef D() As Double, Optional ByVal MyType
As Long = 1, Optional ByVal a1 As Double = 0, Optional ByVal a2 As Double = 0, Optional
ByVal b1 As Double = 0, Optional ByVal b2 As Double = 0, Optional ByVal eta As Double = 0)
As Long

## Parameters

Name

The name of an existing multilinear elastic or multilinear plastic link property.

DOF

This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom to which the multilinear points apply.

```
1 = U1
2 = U2
3 = U3
4 = R1
5 = R2
6 = R3
```
NumberPoints


The number of foce-defomation points for the specified degree of freedom.

F

This is an array, dimensioned to NumberPoints - 1, that includes the force at each point. When
DOF is U1, U2 or U3, this is a force. When DOF is R1, R2 or R3. this is a moment. [F] if DOF <=
3, and [FL} if DOF > 3

D

This is an array, dimensioned to NumberPoints - 1, that includes the displacement at each point.
When DOF is U1, U2 or U3, this is a translation. When DOF is R1, R2 or R3, this is a rotation.
[L] if DOF <= 3, and [rad] if DOF > 3

MyType

This item applies only to multilinear plastic link properties. It is 1, 2 or 3, indicating the hysteresis
type.

```
1 = Kinematic
2 = Takeda
3 = Pivot
```
a1

This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Alpha1 hysteresis parameter.

a2

This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Alpha2 hysteresis parameter.

b1

This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Beta1 hysteresis parameter.

b2

This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Beta2 hysteresis parameter.

eta

This item applies only to multilinear plastic link properties that have a pivot hysteresis type
(MyType = 3). It is the Eta hysteresis parameter.

## Remarks

This function sets the force-deformation data for a specified degree of freedom in multilinear
elastic and multilinear plastic link properties.

The function returns zero if the data is successfully assigned; otherwise it returns a nonzero value.


To successfully apply this data to the indicated link property, the following conditions must be
met:

1. The link property must be multilinear elastic or multilinear plastic.
2. The specified DOF must be active.
3. The specified DOF must not be fixed.
4. The specified DOF must be nonlinear.

## VBA Example

Sub SetLinkPropMultiLinearPoints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyF() As Double
Dim MyD() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12


MyCe(1) = 0.01

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetMultiLinearPlastic("MLP1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, 2, 0)

'set multilinear force-defomation data
ReDim MyF(4)
ReDim MyD(4)

MyF(0) = -12
MyF(1) = -10
MyF(2) = 0
MyF(3) = 8
MyF(4) = 9

MyD(0) = -8
MyD(1) = -0.6
MyD(2) = 0
MyD(3) = 0.2
MyD(4) = 6

ret = SapModel.PropLink.SetMultiLinearPoints("MLP1", 2, 5, MyF, MyD, 3, 9, 12, 0.75, 0.8,
.1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetMultiLinearPoints

SetMultiLinearElastic

GetMultiLinearElastic

SetMultiLinearPlastic

GetMultiLinearPlastic

# SetPDelta


## Syntax

SapObject.SapModel.PropLink.SetPDelta

## VB6 Procedure

Function SetPDelta(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing link property.

Value

This is an array of P-delta parameters.

```
Value(0) = M2 P-delta to I-end of link as moment, M2I
Value(1) = M2 P-delta to J-end of link as moment, M2J
Value(2) = M3 P-delta to I-end of link as moment, M3I
Value(3) = M3 P-delta to J-end of link as moment, M3J
```
## Remarks

This function assigns P-delta parameters to a link property.

The function returns zero if the values are successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropPDelta()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double
Dim MyValue() As Double

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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'set link property P-delta parameters
ReDim MyValue(3)
MyValue(0) = 0.6
MyValue(1) = 0.4
MyValue(2) = 0.3
MyValue(3) = 0.2
ret = SapModel.PropLink.SetPDelta("L1", MyValue)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetPDelta

# SetPlasticWen

## Syntax

SapObject.SapModel.PropLink.SetPlasticWen

## VB6 Procedure

Function SetPlasticWen(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef


k() As Double, ByRef Yield() As Double, ByRef Ratio() As Double, ByRef exp() As Double,
ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal Notes As String = "", Optional
ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1 has nonlinear properties
NonLinear(4) = R2 has nonlinear properties
NonLinear(5) = R3 has nonlinear properties
```
The term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke


This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1 [FL]
k(4) = R2 [FL]
k(5) = R3 [FL]
```
The term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

Yield

This is an array of yield force terms for the link property. The yield force applies for nonlinear
analyses.

```
Yield(0) = U1 [F]
Yield(1) = U2 [F]
Yield(2) = U3 [F]
Yield(3) = R1 [FL]
Yield(4) = R2 [FL]
Yield(5) = R3 [FL]
```

The term Yield(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

Ratio

This is an array of post-yield stiffness ratio terms for the link property. The post-yield stiffness
ratio applies for nonlinear analyses. It is the post-yield stiffness divided by the initial stiffness.

```
Ratio(0) = U1
Ratio(1) = U2
Ratio(2) = U3
Ratio(3) = R1
Ratio(4) = R2
Ratio(5) = R3
```
The term Ratio(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

exp

This is an array of yield exponent terms for the link property. The yield exponent applies for
nonlinear analyses. The yielding exponent that controls the sharpness of the transition from the
initial stiffness to the yielded stiffness.

```
exp(0) = U1
exp(1) = U2
exp(2) = U3
exp(3) = R1
exp(4) = R2
exp(5) = R3
```
The term exp(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.


## Remarks

This function initializes a plastic Wen-type link property. If this function is called for an existing
link property, all items for the property are reset to their default values.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropPlasticWen()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MyYield() As Double
Dim MyRatio() As Double
Dim MyExp() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyYield(5)
ReDim MyRatio(5)
ReDim MyExp(5)

MyDOF(0) = True


MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MyYield(1)= 50
MyRatio(1)= 0.1
MyExp(1)= 3

MyDOF(2) = True
MyFixed(2) = True

ret = SapModel.PropLink.SetPlasticWen("PW1", MyDOF, MyFixed, MyNonLinear, MyKe,
MyCe, MyK, MyYield, MyRatio, MyExp, 2, 0)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetPlasticWen

# SetRubberIsolator

## Syntax

SapObject.SapModel.PropLink.SetRubberIsolator

## VB6 Procedure

Function SetRubberIsolator(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed() As
Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double, ByRef
k() As Double, ByRef Yield() As Double, ByRef Ratio() As Double, ByVal dj2 As Double,
ByVal dj3 As Double, Optional ByVal Notes As String = "", Optional ByVal GUID As String =
"") As Long

## Parameters


Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1, Not Used
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1, Not Used
NonLinear(4) = R2, Not Used
NonLinear(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
```

```
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.

```
k(0) = U1, Not Used
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1, Not Used
k(4) = R2, Not Used
k(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Yield

This is an array of yield force terms for the link property. The yield force applies for nonlinear
analyses.

```
Yield(0) = U1, Not Used
Yield(1) = U2 [F]
Yield(2) = U3 [F]
Yield(3) = R1, Not Used
Yield(4) = R2, Not Used
Yield(5) = R3, Not Used
```
The term Yield(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.


Ratio

This is an array of post-yield stiffness ratio terms for the link property. The post-yield stiffness
ratio applies for nonlinear analyses. It is the post-yield stiffness divided by the initial stiffness.

```
Ratio(0) = U1, Not Used
Ratio(1) = U2
Ratio(2) = U3
Ratio(3) = R1, Not Used
Ratio(4) = R2, Not Used
Ratio(5) = R3, Not Used
```
The term Ratio(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a rubber isolator-type link property. If this function is called for an
existing link property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropRubberIsolator()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double


Dim MyCe() As Double
Dim MyK() As Double
Dim MyYield() As Double
Dim MyRatio() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MyYield(5)
ReDim MyRatio(5)
ReDim MyExp(5)

MyDOF(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MyYield(1)= 50
MyRatio(1)= 0.1

MyDOF(2) = True
MyNonLinear(2) = True
MyKe(2) = 15
MyCe(2) = 0.008
MyK(2) = 22
MyYield(2)= 60
MyRatio(2)= 0.15

MyDOF(3) = True
MyFixed(3) = True


ret = SapModel.PropLink.SetRubberIsolator("RI1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, MyK, MyYield, MyRatio, 2, 3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetRubberIsolator

# SetSpringData

## Syntax

SapObject.SapModel.PropLink.SetSpringData

## VB6 Procedure

Function SetSpringData(ByVal Name As String, ByVal DefinedForThisLength As Double, ByVal
DefinedForThisArea As Double) As Long

## Parameters

Name

The name of an existing link property.

DefinedForThisLength

The link property is defined for this length in a line (frame) spring. [L]

DefinedForThisArea

The link property is defined for this area in an area spring. [L^2 ]

## Remarks

This function assigns length and area values to a link property that are used if the link property is
specified in line and area spring assignments.


The function returns zero if the values are successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropSpringData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double

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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'set link property spring data
ret = SapModel.PropLink.SetSpringData("L1", 12, 2)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

GetSpringData

# SetTCFrictionIsolator

## Syntax

SapObject.SapModel.PropLink.SetTCFrictionIsolator

## VB6 Procedure

Function SetTCFrictionIsolator(ByVal Name As String, ByRef DOF() As Boolean, ByRef Fixed()
As Boolean, ByRef NonLinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As Double,
ByRef k() As Double, ByRef Slow() As Double, ByRef Fast() As Double, ByRef Rate() As
Double, ByRef Radius() As Double, ByRef SlowT() As Double, ByRef FastT() As Double, ByRef
RateT() As Double, ByVal kt As Double, ByVal dis As Double, ByVal dist As Double, ByVal
Damping As Double, ByVal dj2 As Double, ByVal dj3 As Double, Optional ByVal Notes As
String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
Fixed

This is a boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```

The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1, Not Used
NonLinear(4) = R2, Not Used
NonLinear(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U1, U2 and U3. For those degrees of
freedom, the term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

k

This is an array of initial stiffness terms for the link property. The initial stiffness applies for
nonlinear analyses.


```
k(0) = U1 [F/L]
k(1) = U2 [F/L]
k(2) = U3 [F/L]
k(3) = R1, Not Used
k(4) = R2, Not Used
k(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U1, U2 and U3. For those degrees of
freedom, the term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Slow

This is an array of the friction coefficient at zero velocity terms when U1 is in compression for the
link property. This coefficient applies for nonlinear analyses.

```
Slow(0) = U1, Not Used
Slow(1) = U2
Slow(2) = U3
Slow(3) = R1, Not Used
Slow(4) = R2, Not Used
Slow(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Slow(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Fast

This is an array of the friction coefficient at fast velocity terms when U1 is in compression for the
link property. This coefficient applies for nonlinear analyses.

```
Fast(0) = U1, Not Used
Fast(1) = U2
Fast(2) = U3
Fast(3) = R1, Not Used
Fast(4) = R2, Not Used
Fast(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Fast(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Rate

This is an array of the inverse of the characteristic sliding velocity terms when U1 is in
compression for the link property. This item applies for nonlinear analyses.

```
Rate(0) = U1, Not Used
Rate(1) = U2 [s/L]
Rate(2) = U3 [s/L]
```

```
Rate(3) = R1, Not Used
Rate(4) = R2, Not Used
Rate(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Rate(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Radius

This is an array of the radius of the sliding contact surface terms for the link property. Inputting 0
means there is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.

```
Radius(0) = U1, Not Used
Radius(1) = U2 [L]
Radius(2) = U3 [L]
Radius(3) = R1, Not Used
Radius(4) = R2, Not Used
Radius(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term Radius(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.

SlowT

This is an array of the friction coefficient at zero velocity terms when U1 is in tension for the link
property. This coefficient applies for nonlinear analyses.

```
SlowT(0) = U1, Not Used
SlowT(1) = U2
SlowT(2) = U3
SlowT(3) = R1, Not Used
SlowT(4) = R2, Not Used
SlowT(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term SlowT(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.

FastT

This is an array of the friction coefficient at fast velocity terms when U1 is in tension for the link
property. This coefficient applies for nonlinear analyses.

```
FastT(0) = U1, Not Used
FastT(1) = U2
FastT(2) = U3
FastT(3) = R1, Not Used
FastT(4) = R2, Not Used
FastT(5) = R3, Not Used
```

Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term FastT(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

RateT

This is an array of the inverse of the characteristic sliding velocity terms when U1 is in tension for
the link property. This item applies for nonlinear analyses.

```
RateT(0) = U1, Not Used
RateT(1) = U2 [s/L]
RateT(2) = U3 [s/L]
RateT(3) = R1, Not Used
RateT(4) = R2, Not Used
RateT(5) = R3, Not Used
```
Note that this item is applicable only for degrees of freedom U2 and U3. For those degrees of
freedom, the term RateT(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

kt

The axial translational tension stiffness for the U1 degree of freedom. This item applies for
nonlinear analyses. [F/L]

dis

The U1 degree of freedom gap opening for compression. This item applies for nonlinear analyses.
[L]

dist

The U1 degree of freedom gap opening for tension. This item applies for nonlinear analyses. [L]

Damping

The nonlinear damping coefficient used for the axial translational degree of freedom, U1. This
item applies for nonlinear analyses. [F/L]

dj2

The distance from the J-End of the link to the U2 shear spring. This item applies only when DOF
(1) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring. This item applies only when DOF
(2) = True. [L]

Notes

The notes, if any, assigned to the property.


### GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function initializes a T/C friction isolator-type link property. If this function is called for an
existing link property, all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropTCFrictionIsolator()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double
Dim MyK() As Double
Dim MySlow() As Double
Dim MyFast() As Double
Dim MyRate() As Double
Dim MyRadius() As Double
Dim MySlowT() As Double
Dim MyFastT() As Double
Dim MyRateT() As Double

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

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)


ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(5)
ReDim MySlow(5)
ReDim MyFast(5)
ReDim MyRate(5)
ReDim MyRadius(5)
ReDim MySlowT(5)
ReDim MyFastT(5)
ReDim MyRateT(5)

MyDOF(0) = True
MyNonLinear(0) = True
MyKe(0) = 12
MyCe(0) = 0.01
MyK(0) = 1000

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01
MyK(1) = 20
MySlow(1)= 0.6
MyFast(1)= 0.5
MyRate(1)= 10
MyRadius(1)= 80
MySlowT(1)= 0.61
MyFastT(1)= 0.51
MyRateT(1)= 10.1

MyDOF(2) = True
MyNonLinear(2) = True
MyKe(2) = 14
MyCe(2) = 0.008
MyK(2) = 22
MySlow(2)= 0.66
MyFast(2)= 0.55
MyRate(2)= 12
MyRadius(2)= 75
MySlowT(2)= 0.67
MyFastT(2)= 0.56
MyRateT(2)= 12.1

MyDOF(3) = True
MyKe(3) = 15
MyCe(3) = 0

MyDOF(4) = True
MyFixed(4) = True

ret = SapModel.PropLink.SetTCFrictionIsolator("TCFI1", MyDOF, MyFixed, MyNonLinear,
MyKe, MyCe, MyK, MySlow, MyFast, MyRate, MyRadius, MySlowT, MyFastT, MyRateT, 18,


### 2, 3, 0.1, 2, 3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetTCFrictionIsolator

# SSetTriplePendulumIsolator

## Syntax

SapObject.SapModel.PropLink.SetTriplePendulumIsolator

## VB6 Procedure

Function SetTriplePendulumIsolator(ByVal Name As String, ByRef dof() As Boolean, ByRef
Fixed() As Boolean, ByRef Nonlinear() As Boolean, ByRef Ke() As Double, ByRef Ce() As
Double, ByVal K1 As Double, ByVal Damping As Double, ByRef K() As Double, ByRef Slow()
As Double, ByRef Fast() As Double, ByRef Rate() As Double, ByRef Radius() As Double, ByRef
StopDist() As Double, ByVal HeightOut As Double, ByVal HeightIn As Double, ByVal dj2 As
Double, ByVal dj3 As Double, Optional ByVal Notes As String = "", Optional ByVal GUID As
String = "") As Long

## Parameters

Name

The name of an existing or new link property. If this is an existing property, that property is
modified; otherwise, a new property is added.

DOF

This is a Boolean array, dimensioned to 5, indicating if properties exist for a specified degree of
freedom.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
```

### DOF(5) = R3

Fixed

This is a Boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed
(restrained).

```
Fixed(0) = U1 fixity
Fixed(1) = U2 fixity
Fixed(2) = U3 fixity
Fixed(3) = R1 fixity
Fixed(4) = R2 fixity
Fixed(5) = R3 fixity
```
The term Fixed(n) applies only when DOF(n) = True.

NonLinear

This is a Boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified
degree of freedom.

```
NonLinear(0) = U1 has nonlinear properties
NonLinear(1) = U2 has nonlinear properties
NonLinear(2) = U3 has nonlinear properties
NonLinear(3) = R1, Not Used
NonLinear(4) = R2, Not Used
NonLinear(5) = R3, Not Used
```
Note that this item is applicable for degrees of freedom U1, U2 and U3 only. For those degrees of
freedom, the term NonLinear(n) applies only when DOF(n) = True and Fixed(n) = False.

Ke

This is an array of effective stiffness terms for the link property. The effective stiffness applies for
linear analyses, and also for nonlinear analysis for those DOF for which NonLinear(n) = False.

```
Ke(0) = U1 [F/L]
Ke(1) = U2 [F/L]
Ke(2) = U3 [F/L]
Ke(3) = R1 [FL]
Ke(4) = R2 [FL]
Ke(5) = R3 [FL]
```
The term Ke(n) applies only when DOF(n) = True and Fixed(n) = False.

Ce

This is an array of effective damping terms for the link property. The effective damping applies
for linear analyses.

```
Ce(0) = U1 [F/L]
```

```
Ce(1) = U2 [F/L]
Ce(2) = U3 [F/L]
Ce(3) = R1 [FL]
Ce(4) = R2 [FL]
Ce(5) = R3 [FL]
```
The term Ce(n) applies only when DOF(n) = True and Fixed(n) = False.

K1

This is the axial compression stiffness for the U1 degree of freedom. This item applies for
nonlinear analyses. [F/L]

Damping

This is the nonlinear damping coefficient for the axial degree of freedom, U1, when it is in
compression. This item applies for nonlinear analyses. [F/L]

K

This is an array, dimensioned to 3, of initial nonlinear stiffness (before sliding) for each sliding
surface.

```
K(0) = for the outer top sliding surface [F/L]
K(1) = for the outer bottom sliding surface [F/L]
K(2) = for the inner top sliding surface [F/L]
K(3) = for the inner bottom sliding surface [F/L]
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term k(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Slow

This is an array, dimensioned to 3, of the friction coefficient at zero velocity for each sliding
surface when U1 is in compression.

```
Slow(0) = for the outer top sliding surface
Slow(1) = for the outer bottom sliding surface
Slow(2) = for the inner top sliding surface
Slow(3) = for the inner bottom sliding surface
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term Slow(n) only applies when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Fast

This is an array, dimensioned to 3, of the friction coefficient at fast velocity for each sliding
surface when U1 is in compression.

```
Fast(0) = for the outer top sliding surface
```

```
Fast(1) = for the outer bottom sliding surface
Fast(2) = for the inner top sliding surface
Fast(3) = for the inner bottom sliding surface
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term Fast(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) =
True.

Rate

This is an array, dimensioned to 3, of the inverse of the characteristic sliding velocity for the Slow
and Fast friction coefficients for each sliding surface. This item applies for nonlinear analyses.

```
Rate(0) = for the outer top sliding surface [s/L]
Rate(1) = for the outer bottom sliding surface [s/L]
Rate(2) = for the inner top sliding surface [s/L]
Rate(3) = for the inner bottom sliding surface [s/L]
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term Rate(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n)
= True.

Radius

This is an array, dimensioned to 3, of the radius for each sliding surface. Inputting 0 means there
is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.

```
Radius(0) = for the outer top sliding surface [L]
Radius(1) = for the outer bottom sliding surface [L]
Radius(2) = for the inner top sliding surface [L]
Radius(3) = for the inner bottom sliding surface [L]
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term Radius(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.

StopDist

This is an array, dimensioned to 3, of the amount of displacement allowed before hitting a stiff
limit for each sliding surface. Inputting 0 means there is no stop. This item applies for nonlinear
analyses.

```
StopDist(0) = for the outer top sliding surface [L]
StopDist(1) = for the outer bottom sliding surface [L]
StopDist(2) = for the inner top sliding surface [L]
StopDist(3) = for the inner bottom sliding surface [L]
```
Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term StopDist(n) applies only when DOF(n) = True, Fixed(n) = False and NonLinear
(n) = True.


HeightOut

This is the height (distance) between the outer sliding surfaces at zero displacement. [L]

Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

HeightIn

This is the height (distance) between the inner sliding surfaces. [L]

Note that this item is applicable for degrees of freedom U2 and U3 only. For those degrees of
freedom, the term applies only when DOF(n) = True, Fixed(n) = False and NonLinear(n) = True.

dj2

The distance from the J-End of the link to the U2 shear spring, that is, the center of the isolator.
This item applies only when DOF(2) = True. [L]

dj3

The distance from the J-End of the link to the U3 shear spring, that is, the center of the isolator.
This item applies only when DOF(3) = True. [L]

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, then the program assigns a GUID to the property.

## Remarks

This function initializes a Triple Pendulum Isolator type link property. If this function is called for
an existing link property, then all items for the property are reset to their default value.

The function returns zero if the property is successfully initialized, otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropTriplePendulumIsolator()
'dimension variables
Dim SapObject As Sap2000.SapObject
Dim SapModel As cSapModel
Dim ret As Long
Dim MyDOF() As Boolean
Dim MyFixed() As Boolean
Dim MyNonLinear() As Boolean
Dim MyKe() As Double
Dim MyCe() As Double


Dim MyK() As Double
Dim MySlow() As Double
Dim MyFast() As Double
Dim MyRate() As Double
Dim MyRadius() As Double
Dim MyStopDist () As Double

'create Sap2000 object
Set SapObject = New SAP2000.SapObject

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add link property
ReDim MyDOF(5)
ReDim MyFixed(5)
ReDim MyNonLinear(5)
ReDim MyKe(5)
ReDim MyCe(5)
ReDim MyK(3)
ReDim MySlow(3)
ReDim MyFast(3)
ReDim MyRate(3)
ReDim MyRadius(3)
ReDim MyStopDist(3)

MyDOF(0) = True
MyNonLinear(0) = True
MyKe(0) = 12
MyCe(0) = 0.01

MyDOF(1) = True
MyNonLinear(1) = True
MyKe(1) = 12
MyCe(1) = 0.01

MyDOF(2) = True
MyNonLinear(2) = True
MyKe(2) = 1
MyCe(2) = 0.008

MyK(0) = 20
MySlow(0)= 0.6
MyFast(0)= 0.5


MyRate(0)= 10
MyRadius(0)= 80
MyStopDist(0)= 8

MyK(1) = 22
MySlow(1)= 0.66
MyFast(1)= 0.55
MyRate(1)= 12
MyRadius(1)= 75
MyStopDist(1)= 8

MyK(2) = 20
MySlow(2)= 0.6
MyFast(2)= 0.5
MyRate(2)= 10
MyRadius(2)= 80
MyStopDist(2)= 8

MyK(3) = 20
MySlow(3)= 0.6
MyFast(3)= 0.5
MyRate(3)= 10
MyRadius(3)= 80
MyStopDist(3)= 8

MyDOF(3) = True
MyKe(3) = 15
MyCe(3) = 0

MyDOF(4) = True
MyFixed(4) = True

ret = SapModel.PropLink.SetTriplePendulumIsolator("TPI1", MyDOF, MyFixed,
MyNonLinear, MyKe, MyCe, 1000, 0.1, MyK, MySlow, MyFast, MyRate, MyRadius,
MyStopDist, 6, 3, 3, 3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.00.

## See Also

GetTriplePendulumIsolator


# SetWeightAndMass

## Syntax

SapObject.SapModel.PropLink.SetWeightAndMass

## VB6 Procedure

Function SetWeightAndMass(ByVal Name As String, ByVal w As Double, ByVal m As Double,
ByVal R1 As Double, ByVal R2 As Double, ByVal R3 As Double) As Long

## Parameters

Name

The name of an existing link property.

w

The weight of the link. [F]

m

The translational mass of the link. [M]

R1

The rotational inertia of the link about its local 1 axis. [ML^2 ]

R2

The rotational inertia of the link about its local 2 axis. [ML^2 ]

R3

The rotational inertia of the link about its local 3 axis. [ML^2 ]

## Remarks

This function assigns weight and mass values to a link property.

The function returns zero if the values are successfully assigned; otherwise it returns a nonzero
value.

## VBA Example

Sub SetLinkPropWeightAndMass()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim DOF() As Boolean
Dim Fixed() As Boolean
Dim Ke() As Double
Dim Ce() As Double

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

'add link property
ReDim DOF(5)
ReDim Fixed(5)
ReDim Ke(5)
ReDim Ce(5)
DOF(0) = True
Ke(0) = 12
ret = SapModel.PropLink.SetLinear("L1", DOF, Fixed, Ke, Ce, 0, 0)

'set link property weight and mass
ret = SapModel.PropLink.SetWeightAndMass("L1", 10, 0.26, 0.0012, 0.0014, 0.0016)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetWeightAndMass


# ChangeName

## Syntax

SapObject.SapModel.PropRebar.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined rebar property.

**NewName**

The new name for the rebar property.

## Remarks

This function changes the name of an existing rebar property.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeRebarPropName()
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


'set new rebar property
ret = SapModel.PropRebar.SetProp("R1", 1, 1.128)

'change name of rebar property
ret = SapModel.PropRebar.ChangeName("R1", "MyRebar")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.2.0.

## See Also

# Count

## Syntax

SapObject.SapModel.PropRebar.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

This function returns the total number of defined rebar properties in the model.

## VBA Example

Sub CountRebarProps()
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

'set new rebar property
ret = SapModel.PropRebar.SetProp("R1", 1, 1.128)

'return number of defined rebar properties
Count = SapModel.PropRebar.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.2.0.

## See Also

# Delete

## Syntax

SapObject.SapModel.PropRebar.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters


**Name**

The name of an existing rebar property.

## Remarks

The function deletes a specified rebar property.

The function returns zero if the property is successfully deleted; otherwise it returns a nonzero
value. It returns an error if the specified property can not be deleted, for example, if it is assigned
to an existing object.

## VBA Example

Sub DeleteRebarProp()
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

'set new rebar properties
ret = SapModel.PropRebar.SetProp("R1", 1, 1.128)
ret = SapModel.PropRebar.SetProp("R2", 1, 1.128)

'delete rebar property
ret = SapModel.PropRebar.Delete("R1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.2.0.


## See Also

# GetNameList

## Syntax

SapObject.SapModel.PropRebar.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

**NumberNames**

The number of rebar property names retrieved by the program.

**MyName**

This is a one-dimensional array of rebar property names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined rebar properties in the model.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetRebarNames()
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

'set new rebar properties
ret = SapModel.PropRebar.SetProp("R1", 1, 1.27)
ret = SapModel.PropRebar.SetProp("R2", 1, 1.27)

'get rebar property names
ret = SapModel.PropRebar.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.2.0.

## See Also

# GetProp

## Syntax

SapObject.SapModel.PropRebar.GetProp

## VB6 Procedure

Function GetProp(ByVal Name As String, ByRef Area As Double, ByRef Diameter As Double)
As Long

## Parameters

Name


The name of an existing rebar property.

**Area**

The cross-sectional area of the rebar. [L^2 ]

**Diameter**

The diameter of the rebar. [L]

## Remarks

This function retrieves rebar property definition data.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetRebarProperty()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Area As Double
Dim Diameter As Double

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

'set new rebar property
ret = SapModel.PropRebar.SetProp("R1", 1, 1.128)

'get rebar property data
ret = SapModel.PropRebar.GetProp("R1", Area, Diameter)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.2.0.

## See Also

SetProp

# SetProp

## Syntax

SapObject.SapModel.PropRebar.SetProp

## VB6 Procedure

Function SetProp(ByVal Name As String, ByVal Area As Double, ByVal Diameter As Double)
As Long

## Parameters

**Name**

The name of an existing or new rebar property. If this is an existing property, that property is
modified; otherwise, a new property is added.

**Area**

The cross-sectional area of the rebar. [L^2 ]

**Diameter**

The diameter of the rebar. [L]

## Remarks

This function defines a rebar property.

The function returns zero if the property is successfully defined; otherwise it returns a nonzero
value.

## VBA Example


Sub SetRebarProperty()
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

'set new rebar property
ret = SapModel.PropRebar.SetProp("R1", 1, 1.128)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.2.0.

## See Also

GetProp

# ChangeName

## Syntax

SapObject.SapModel.PropSolid.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long


## Parameters

Name

The existing name of a defined solid property.

NewName

The new name for the solid property.

## Remarks

This function changes the name of an existing solid property.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeSolidPropName()
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
ret = SapModel.File.NewSolidBlock(20, 50, 20)

'change name of solid property
ret = SapModel.PropSolid.ChangeName("SOLID1", "MySolid")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.02.

## See Also

# Count

## Syntax

SapObject.SapModel.PropSolid.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

This function returns the total number of defined solid properties in the model.

## VBA Example

Sub CountSolidProps()
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
ret = SapModel.File.NewSolidBlock(20, 50, 20)

'return number of defined solid properties
Count = SapModel.PropSolid.Count


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Delete

## Syntax

SapObject.SapModel.PropSolid.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing solid property.

## Remarks

The function deletes a specified solid property.

The function returns zero if the property is successfully deleted; otherwise it returns a nonzero
value. It returns an error if the specified property can not be deleted, for example, if it is assigned
to an existing object.

## VBA Example

Sub DeleteSolidProp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
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
ret = SapModel.File.NewSolidBlock(20, 50, 20)

'set new solid property
ret = SapModel.PropSolid.SetProp("S1", "4000Psi", 0, 10, 20, True)

'get solid object names
ret = SapModel.SolidObj.GetNameList(NumberNames, MyName)

'set solid property
For i = 1 to NumberNames
ret = SapModel.SolidObj.SetProperty(MyName(i - 1), "S1")
Next i

'delete solid property
ret = SapModel.PropSolid.Delete("SOLID1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetNameList

## Syntax

SapObject.SapModel.PropSolid.GetNameList


## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of solid property names retrieved by the program.

MyName

This is a one-dimensional array of solid property names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined solid properties in the model.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetSolidNames()
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
ret = SapModel.File.NewSolidBlock(20, 50, 20)


'get solid property names
ret = SapModel.PropSolid.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetProp

## Syntax

SapObject.SapModel.PropSolid.GetProp

## VB6 Procedure

Function GetProp(ByVal Name As String, ByRef MatProp As String, ByRef a As Double, ByRef
B As Double, ByRef c As Double, ByRef Incompatible As Boolean, ByRef Color As Long,
ByRef Notes As String, ByRef GUID As String) As Long

## Parameters

Name

The name of an existing solid property.

MatProp

The name of the material property assigned to the solid property.

a

The material angle A. [deg]

b

The material angle B. [deg]

c

The material angle C. [deg]


Incompatible

If this item is True, incompatible bending modes are included in the stiffness formulation. In
general, incompatible modes significantly improve the bending behavior of the object.

Color

The display color assigned to the property.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves solid property definition data.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSolidProperty()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MatProp As String
Dim a As Double
Dim b As Double
Dim c As Double
Dim Incompatible As Boolean
Dim Color As Long
Dim Notes As String
Dim GUID As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel


'create model from template
ret = SapModel.File.NewSolidBlock(20, 50, 20)

'get solid property data
ret = SapModel.PropSolid.GetProp("SOLID1", MatProp, a, b, c, Incompatible, Color, Notes,
GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetProp

# SetProp

## Syntax

SapObject.SapModel.PropSolid.SetProp

## VB6 Procedure

Function SetProp(ByVal Name As String, ByVal MatProp As String, ByVal a As Double, ByVal
B As Double, ByVal c As Double, ByVal Incompatible As Boolean, Optional ByVal Color As
Long = -1, Optional ByVal Notes As String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new solid property. If this is an existing property, that property is
modified; otherwise, a new property is added.

MatProp

The name of the material property assigned to the solid property.

a

The material angle A. [deg]

b


The material angle B. [deg]

c

The material angle C. [deg]

Incompatible

If this item is True, incompatible bending modes are included in the stiffness formulation. In
general, incompatible modes significantly improve the bending behavior of the object.

Color

The display color assigned to the property. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function defines a solid property.

The function returns zero if the property is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetSolidProperty()
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


ret = SapModel.File.NewSolidBlock(20, 50, 20)

'set new solid property
ret = SapModel.PropSolid.SetProp("S1", "4000Psi", 0, 10, 20, True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetProp

# ChangeName

## Syntax

SapObject.SapModel.PropTendon.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined tendon property.

NewName

The new name for the tendon property.

## Remarks

This function changes the name of an existing tendon property.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.


## VBA Example

Sub ChangeTendonPropName()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add tendon material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new tendon property
ret = SapModel.PropTendon.SetProp("T1", Name, 1, 2.25)

'change name of tendon property
ret = SapModel.PropTendon.ChangeName("T1", "MyTendon")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.


## See Also

# Count

## Syntax

SapObject.SapModel.PropTendon.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

This function returns the total number of defined tendon properties in the model.

## VBA Example

Sub CountTendonProps()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
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

'add tendon material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)


'set new tendon property
ret = SapModel.PropTendon.SetProp("T1", Name, 1, 2.25)

'return number of defined tendon properties
Count = SapModel.PropTendon.Count

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Delete

## Syntax

SapObject.SapModel.PropTendon.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing tendon property.

## Remarks

The function deletes a specified tendon property.

The function returns zero if the property is successfully deleted; otherwise it returns a nonzero
value. It returns an error if the specified property can not be deleted, for example, if it is assigned
to an existing object.

## VBA Example

Sub DeleteTendonProp()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim i As Long
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

'add tendon material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new tendon properties
ret = SapModel.PropTendon.SetProp("T1", Name, 1, 2.25)
ret = SapModel.PropTendon.SetProp("T2", Name, 1, 3.25)

'delete tendon property
ret = SapModel.PropTendon.Delete("T1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetNameList

## Syntax


SapObject.SapModel.PropTendon.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of tendon property names retrieved by the program.

MyName

This is a one-dimensional array of tendon property names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined tendon properties in the model.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

## VBA Example

Sub GetTendonNames()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
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

'add tendon material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new tendon properties
ret = SapModel.PropTendon.SetProp("T1", Name, 1, 2.25)
ret = SapModel.PropTendon.SetProp("T2", Name, 1, 3.25)

'get tendon property names
ret = SapModel.PropTendon.GetNameList(NumberNames, MyName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetProp

## Syntax

SapObject.SapModel.PropTendon.GetProp

## VB6 Procedure

Function GetProp(ByVal Name As String, ByRef MatProp As String, ByRef ModelingOption As
Long, ByRef Area As Double, ByRef Color As Long, ByRef Notes As String, ByRef GUID As
String) As Long

## Parameters

Name

The name of an existing tendon property.

MatProp

The name of the material property assigned to the tendon property.

ModelingOption


This is either 1 or 2, indicating the tendon modeling option.

```
1 = Model tendon as loads
2 = Model tendon as elements
```
Area

The cross-sectional area of the tendon. [L^2 ]

Color

The display color assigned to the property.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property.

## Remarks

This function retrieves tendon property definition data.

The function returns zero if the property data is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetTendonProperty()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim MatProp As String
Dim ModelingOption As Long
Dim Area As Double
Dim Color As Long
Dim Notes As String
Dim GUID As String

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

'add tendon material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new tendon property
ret = SapModel.PropTendon.SetProp("T1", Name, 1, 2.25)

'get tendon property data
ret = SapModel.PropTendon.GetProp("T1", MatProp, ModelingOption, Area, Color, Notes,
GUID)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetProp

# SetProp

## Syntax

SapObject.SapModel.PropTendon.SetProp

## VB6 Procedure

Function SetProp(ByVal Name As String, ByVal MatProp As String, ByVal ModelingOption As
Long, ByVal Area As Double, Optional ByVal Color As Long = -1, Optional ByVal Notes As
String = "", Optional ByVal GUID As String = "") As Long

## Parameters

Name

The name of an existing or new tendon property. If this is an existing property, that property is
modified; otherwise, a new property is added.


MatProp

The name of the material property assigned to the tendon property.

ModelingOption

This is either 1 or 2, indicating the tendon modeling option.

```
1 = Model tendon as loads
2 = Model tendon as elements
```
Area

The cross-sectional area of the tendon. [L^2 ]

Color

The display color assigned to the property. If Color is specified as -1, the program will
automatically assign a color.

Notes

The notes, if any, assigned to the property.

GUID

The GUID (global unique identifier), if any, assigned to the property. If this item is input as
Default, the program assigns a GUID to the property.

## Remarks

This function defines a tendon property.

The function returns zero if the property is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetTendonProperty()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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

'add tendon material
ret = SapModel.PropMaterial.AddQuick(Name, MATERIAL_TENDON, , , , , ,
MATERIAL_TENDON_SUBTYPE_ASTM_A416Gr270)

'set new tendon property
ret = SapModel.PropTendon.SetProp("T1", Name, 1, 2.25)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetProp


