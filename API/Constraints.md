# ChangeName

## Syntax

SapObject.SapModel.ConstraintDef.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined constraint.

NewName

The new name for the constraint.

## Remarks

The function returns zero if the new name is successfully applied, otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeConstraintName()
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


'define new contraint
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", AutoAxis)

'change name of contraint
ret = SapModel.ConstraintDef.ChangeName("Diaph1", "MyConstraint")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Count

## Syntax

SapObject.SapModel.ConstraintDef.Count

## VB6 Procedure

Function Count(Optional ByVal ConstraintType As eConstraintType) As Long

## Parameters

ConstraintType

This optional value is one of the following items in the eConstraintType enumeration.

```
CONSTRAINT_BODY = 1
```
```
CONSTRAINT_DIAPHRAGM = 2
```
```
CONSTRAINT_PLATE = 3
```
```
CONSTRAINT_ROD = 4
```
```
CONSTRAINT_BEAM = 5
```
```
CONSTRAINT_EQUAL = 6
```
```
CONSTRAINT_LOCAL = 7
```

### CONSTRAINT_WELD = 8

### CONSTRAINT_LINE = 13

## Remarks

If the ConstraintType item is specified, the function returns the number of defined constraints of
the specified type. Otherwise it returns the total number of defined constraints without regard for
type.

## VBA Example

Sub CountConstraints()
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

'return number of defined constraints
ret = SapModel.ConstraintDef.Count

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Modified optional argument ConstraintType to be ByVal in version 12.0.1.

## See Also


# Delete

## Syntax

SapObject.SapModel.ConstraintDef.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing constraint.

## Remarks

The function deletes the specified constraint. All constraint assignments for that constraint are also
deleted.

The function returns zero if the constraint is successfully deleted, otherwise it returns a nonzero
value.

## VBA Example

Sub DeleteConstraint()
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

'define new contraint
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", AutoAxis)


'delete constraint
ret = SapModel.ConstraintDef.Delete("Diaph1")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetBeam

SetBody

SetDiaphragm

SetEqual

SetLine

SetLocal

SetPlate

SetRod

SetWeld

# GetBeam

## Syntax

SapObject.SapModel.ConstraintDef.GetBeam

## VB6 Procedure

Function GetBeam(ByVal Name As String, ByRef Axis As eConstraintAxis, ByRef CSys As
String) As Long

## Parameters

Name


The name of an existing constraint.

Axis

This is one of the following items from the eConstraintAxis enumeration. It specifies the axis in
the specified coordinate system that is parallel to the axis of the constraint. If AutoAxis is
specified, the axis of the constraint is automatically determined from the joints assigned to the
constraint.

```
X = 1
Y = 2
Z = 3
```
```
AutoAxis = 4
```
CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetBeamConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ConstraintType As eConstraintType
Dim Axis As eConstraintAxis
Dim CSys as String

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


'define new contraint
ret = SapModel.ConstraintDef.SetBeam("Beam1")

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Beam1", ConstraintType)
If ConstraintType = CONSTRAINT_BEAM Then
ret = SapModel.ConstraintDef.GetBeam("Beam1", Axis, CSys)
End If

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetBeam

# GetBody

## Syntax

SapObject.SapModel.ConstraintDef.GetBody

## VB6 Procedure

Function GetBody(ByVal Name As String, ByRef Value() As Boolean, ByRef CSys As String)
As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and
RZ.

CSys

The name of the coordinate system in which the constraint is defined.


## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetBodyConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
Dim ret As Long
Dim Value() As Boolean
Dim CSys as String
Dim UY as Boolean
Dim ConstraintType As eConstraintType

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

'define new contraint
redim Value(5)
for i = 0 To 5
Value(i) = True
Next i
ret = SapModel.ConstraintDef.SetBody("Body1", Value)

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Body1", ConstraintType)
If ConstraintType = CONSTRAINT_BODY Then
ret = SapModel.ConstraintDef.GetBody("Body1", Value, CSys)
if ret = 0 Then UY = Value(1)
End If

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetBody

# GetConstraintType

## Syntax

SapObject.SapModel.ConstraintDef.GetConstraintType

## VB6 Procedure

Function GetConstraintType(ByVal Name As String, ByRef ConstraintType As eConstraintType)
As Long

## Parameters

Name

The name of an existing constraint.

ConstraintType

This value is one of the following items in the eConstraintType enumeration.

```
CONSTRAINT_BODY = 1
```
```
CONSTRAINT_DIAPHRAGM = 2
```
```
CONSTRAINT_PLATE = 3
```
```
CONSTRAINT_ROD = 4
```
```
CONSTRAINT_BEAM = 5
```
```
CONSTRAINT_EQUAL = 6
```
```
CONSTRAINT_LOCAL = 7
```
```
CONSTRAINT_WELD = 8
```
```
CONSTRAINT_LINE = 13
```

## Remarks

The function returns the constraint type for the specified constraint.

The function returns zero if the constraint type is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub ConstraintType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
Dim ConstraintType As eConstraintType

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

'define new constraint
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", AutoAxis)

'get constraint type
ret = SapModel.ConstraintDef.GetConstraintType("Diaph1", ConstraintType)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetBeam


GetBody

GetDiaphragm

GetEqual

GetLine

GetLocal

GetPlate

GetRod

GetWeld

# GetDiaphragm

## Syntax

SapObject.SapModel.ConstraintDef.GetDiaphragm

## VB6 Procedure

Function GetDiaphragm(ByVal Name As String, ByRef Axis As eConstraintAxis, ByRef CSys
As String) As Long

## Parameters

Name

The name of an existing constraint.

Axis

This is one of the following items from the eConstraintAxis enumeration. It specifies the axis in
the specified coordinate system that is perpendicular to the plane of the constraint. If AutoAxis is
specified, the axis of the constraint is automatically determined from the joints assigned to the
constraint.

```
X = 1
Y = 2
Z = 3
```
```
AutoAxis = 4
```
CSys

The name of the coordinate system in which the constraint is defined.


## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetDiaphragmConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ConstraintType As eConstraintType
Dim Axis As eConstraintAxis
Dim CSys as String

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

'define new constraint
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1")

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Diaph1", ConstraintType)
If ConstraintType = CONSTRAINT_DIAPHRAGM Then
ret = SapModel.ConstraintDef.GetDiaphragm("Diaph1", Axis, CSys)
End If

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

SetDiaphragm

# GetEqual

## Syntax

SapObject.SapModel.ConstraintDef.GetEqual

## VB6 Procedure

Function GetEqual(ByVal Name As String, ByRef Value() As Boolean, ByRef CSys As String)
As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and
RZ.

CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetEqualConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
Dim ret As Long
Dim Value() As Boolean
Dim CSys as String


Dim UY as Boolean
Dim ConstraintType As eConstraintType

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

'define new constraint
redim Value(5)
for i = 0 To 5
Value(i) = True
Next i
ret = SapModel.ConstraintDef.SetEqual("Equal1", Value)

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Equal1", ConstraintType)
If ConstraintType = CONSTRAINT_EQUAL Then
ret = SapModel.ConstraintDef.GetEqual("Equal1", Value, CSys)
if ret = 0 Then UY = Value(1)
End If

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetEqual


# GetLine

## Syntax

SapObject.SapModel.ConstraintDef.GetLine

## VB6 Procedure

Function GetLine(ByVal Name As String, ByRef Value() As Boolean, ByRef CSys As String) As
Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and
RZ.

CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLineConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
Dim ret As Long
Dim Value() As Boolean
Dim CSys as String
Dim UY as Boolean
Dim ConstraintType As eConstraintType

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

'define new contraint
redim Value(5)
for i = 0 To 5
Value(i) = True
Next i
ret = SapModel.ConstraintDef.SetLine("Line1", Value)

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Line1", ConstraintType)
If ConstraintType = CONSTRAINT_LINE Then
ret = SapModel.ConstraintDef.GetLine("Line1", Value, CSys)
if ret = 0 Then UY = Value(1)
End If

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetLine

# GetLocal

## Syntax

SapObject.SapModel.ConstraintDef.GetLocal

## VB6 Procedure


Function GetLocal(ByVal Name As String, ByRef Value() As Boolean) As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are U1, U2, U3, R1, R2 and R3.

## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetLocalConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
Dim ret As Long
Dim Value() As Boolean
Dim UY as Boolean
Dim ConstraintType As eConstraintType

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

'define new constraint
redim Value(5)
for i = 0 To 5
Value(i) = True


Next i
ret = SapModel.ConstraintDef.SetLocal("Local1", Value)

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Local1", ConstraintType)
If ConstraintType = CONSTRAINT_LOCAL Then
ret = SapModel.ConstraintDef.GetLocal("Local1", Value)
if ret = 0 Then UY = Value(1)
End If

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetLocal

# GetNameList

## Syntax

SapObject.SapModel.ConstraintDef.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of joint constraint names retrieved by the program.

MyName

This is a one-dimensional array of joint constraint names. The MyName array is created as a
dynamic, zero-based, array by the API user:

Dim MyName() as String


The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined joint constraints.

The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetJointConstraintNames()
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

'define new constraint
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", AutoAxis)

'get constraint names
ret = SapModel.ConstraintDef.GetNameList(NumberNames, MyName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# GetPlate

## Syntax

SapObject.SapModel.ConstraintDef.GetPlate

## VB6 Procedure

Function GetPlate(ByVal Name As String, ByRef Axis As eConstraintAxis, ByRef CSys As
String) As Long

## Parameters

Name

The name of an existing constraint.

Axis

This is one of the following items from the eConstraintAxis enumeration. It specifies the axis in
the specified coordinate system that is perpendicular to the plane of the constraint. If AutoAxis is
specified, the axis of the constraint is automatically determined from the joints assigned to the
constraint.

```
X = 1
Y = 2
Z = 3
```
```
AutoAxis = 4
```
CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetPlateConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim ConstraintType As eConstraintType
Dim Axis As eConstraintAxis
Dim CSys as String

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

'define new constraint
ret = SapModel.ConstraintDef.SetPlate("Plate1")

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Plate1", ConstraintType)
If ConstraintType = CONSTRAINT_PLATE Then
ret = SapModel.ConstraintDef.GetPlate("Plate1", Axis, CSys)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetPlate

# GetRod

## Syntax

SapObject.SapModel.ConstraintDef.GetRod


## VB6 Procedure

Function GetRod(ByVal Name As String, ByRef Axis As eConstraintAxis, ByRef CSys As
String) As Long

## Parameters

Name

The name of an existing constraint.

Axis

This is one of the following items from the eConstraintAxis enumeration. It specifies the axis in
the specified coordinate system that is parallel to the axis of the constraint. If AutoAxis is
specified, the axis of the constraint is automatically determined from the joints assigned to the
constraint.

```
X = 1
Y = 2
Z = 3
```
```
AutoAxis = 4
```
CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetRodConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ConstraintType As eConstraintType
Dim Axis As eConstraintAxis
Dim CSys as String

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

'define new constraint
ret = SapModel.ConstraintDef.SetRod("Rod1")

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Rod1", ConstraintType)
If ConstraintType = CONSTRAINT_ROD Then
ret = SapModel.ConstraintDef.GetRod("Rod1", Axis, CSys)
End If

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetRod

# GetSpecialRigidDiaphragmList

## Syntax

SapObject.SapModel.ConstraintDef.GetSpecialRigidDiaphragmList

## VB6 Procedure

Function GetSpecialRigidDiaphragmList(ByRef Num As Long, ByRefDiaph() As String) As
Long

## Parameters

Num


The number of special rigid diaphragm constraints.

Diaph

This is an array that includes the name of each special rigid diaphragm constraint.

## Remarks

This function retrieves the list of the names of each special rigid diaphragm constraint. A special
rigid diaphragm constraint is required for assignment of auto seismic load diaphragm eccentricity
overwrites. It is also required for calculation of auto wind loads whose exposure widths are
determined from the extents of rigid diaphragms.

A special rigid diaphragm constraint is a constraint with the following features:

1. The constraint type is CONSTRAINT_DIAPHRAGM = 2.
2. The constraint coordinate system is Global.
3. The constraint axis is Z.

The function returns zero if the name list is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetSpecialDiaphragmList()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Diaph() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'createSapModelobject
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New3DFrame(BeamSlab, 2, 144, 3, 336, 2, 432)

'define diaphragm constraints
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1", Z)
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph2")
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph3", Z)


'get special rigid diaphragm name list
ret = SapModel.ConstraintDef.GetSpecialRigidDiaphragmList(Num, Diaph)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetWeld

## Syntax

SapObject.SapModel.ConstraintDef.GetWeld

## VB6 Procedure

Function GetWeld(ByVal Name As String, ByRef Value() As Boolean, ByRef Tolerance As
Double, ByRef CSys As String) As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and
RZ.

Tolerance

Joints within this distance of each other are constrained together.

CSys

The name of the coordinate system in which the constraint is defined.


## Remarks

The function returns the definition for the specified constraint.

The function returns zero if the constraint data is successfully obtained, otherwise it returns a
nonzero value.

## VBA Example

Sub GetWeldConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
Dim ret As Long
Dim Value() As Boolean
Dim Tolerance As Double
Dim CSys as String
Dim UY as Boolean
Dim ConstraintType As eConstraintType

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

'define new constraint
redim Value(5)
for i = 0 To 5
Value(i) = True
Next i
Tolerance = 2
ret = SapModel.ConstraintDef.SetWeld("Weld1", Value, Tolerance)

'get constraint data
ret = SapModel.ConstraintDef.GetConstraintType("Weld1", ConstraintType)
If ConstraintType = CONSTRAINT_WELD Then
ret = SapModel.ConstraintDef.GetWeld("Weld1", Value, Tolerance, CSys)
if ret = 0 Then UY = Value(1)
End If

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetWeld

# SetBeam

## Syntax

SapObject.SapModel.ConstraintDef.SetBeam

## VB6 Procedure

Function SetBeam(ByVal Name As String, Optional ByVal Axis As eConstraintAxis = AutoAxis,
Optional ByVal CSys As String = "Global") As Long

## Parameters

Name

The name of a constraint.

Axis

This is one of the following items from the eConstraintAxis enumeration. It specifies the axis in
the specified coordinate system that is parallel to the axis of the constraint. If AutoAxis is
specified, the axis of the constraint is automatically determined from the joints assigned to the
constraint.

```
X = 1
Y = 2
Z = 3
```
```
AutoAxis = 4
```
CSys

The name of the coordinate system in which the constraint is defined.


## Remarks

This function defines a Beam constraint. If the specified name is not used for a constraint, a new
constraint is defined using the specified name. If the specified name is already used for another
Beam constraint, the definition of that constraint is modified. If the specified name is already used
for some constraint that is not a Beam constraint, an error is returned.

The function returns zero if the constraint data is successfully added or modified, otherwise it
returns a nonzero value.

## VBA Example

Sub SetBeamConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Axis As eConstraintAxis
Dim CSys as String

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

'define new constraint
ret = SapModel.ConstraintDef.SetBeam("Beam1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also


GetBeam

# SetBody

## Syntax

SapObject.SapModel.ConstraintDef.SetBody

## VB6 Procedure

Function SetBody(ByVal Name As String, ByRef Value() As Boolean, Optional ByVal CSys As
String = "Global") As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and
RZ.

CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

This function defines a Body constraint. If the specified name is not used for a constraint, a new
constraint is defined using the specified name. If the specified name is already used for another
Body constraint, the definition of that constraint is modified. If the specified name is already used
for some constraint that is not a Body constraint, an error is returned.

The function returns zero if the constraint data is successfully added or modified, otherwise it
returns a nonzero value.

## VBA Example

Sub SetBodyConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
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

'define new constraint
redim Value(5)
for i = 0 To 5
Value(i) = True
Next i
ret = SapModel.ConstraintDef.SetBody("Body1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetBody

# SetDiaphragm

## Syntax

SapObject.SapModel.ConstraintDef.SetDiaphragm

## VB6 Procedure

Function SetDiaphragm(ByVal Name As String, Optional ByVal Axis As eConstraintAxis =
AutoAxis, Optional ByVal CSys As String = "Global") As Long


## Parameters

Name

The name of a constraint.

Axis

This is one of the following items from the eConstraintAxis enumeration. It specifies the axis in
the specified coordinate system that is perpendicular to the plane of the constraint. If AutoAxis is
specified, the axis of the constraint is automatically determined from the joints assigned to the
constraint.

```
X = 1
Y = 2
Z = 3
```
```
AutoAxis = 4
```
CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

This function defines a Diaphragm constraint. If the specified name is not used for a constraint, a
new constraint is defined using the specified name. If the specified name is already used for
another Diaphragm constraint, the definition of that constraint is modified. If the specified name is
already used for some constraint that is not a Diaphragm constraint, an error is returned.

The function returns zero if the constraint data is successfully added or modified, otherwise it
returns a nonzero value.

## VBA Example

Sub SetDiaphragmConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Axis As eConstraintAxis
Dim CSys as String

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

'define new constraint
ret = SapModel.ConstraintDef.SetDiaphragm("Diaph1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetDiaphragm

# SetEqual

## Syntax

SapObject.SapModel.ConstraintDef.SetEqual

## VB6 Procedure

Function SetEqual(ByVal Name As String, ByRef Value() As Boolean, Optional ByVal CSys As
String = "Global") As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and
RZ.

CSys

The name of the coordinate system in which the constraint is defined.


## Remarks

```
This function defines an Equal constraint. If the specified name is not used for a constraint,
a new constraint is defined using the specified name. If the specified name is already used
for another Equal constraint, the definition of that constraint is modified. If the specified
name is already used for some constraint that is not an Equal constraint, an error is
returned.
```
```
The function returns zero if the constraint data is successfully added or modified,
otherwise it returns a nonzero value.
```
## VBA Example

Sub SetEqualConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
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

'define new contraint
redim Value(5)
for i = 0 To 5
Value(i) = True
Next i
ret = SapModel.ConstraintDef.SetEqual("Equal1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.00.

## See Also

GetEqual

# SetLine

## Syntax

SapObject.SapModel.ConstraintDef.SetLine

## VB6 Procedure

Function SetLine(ByVal Name As String, ByRef Value() As Boolean, Optional ByVal CSys As
String = "Global") As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and
RZ.

CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

This function defines a Line constraint. If the specified name is not used for a constraint, a new
constraint is defined using the specified name. If the specified name is already used for another
Line constraint, the definition of that constraint is modified. If the specified name is already used
for some constraint that is not a Line constraint, an error is returned.

The function returns zero if the constraint data is successfully added or modified, otherwise it
returns a nonzero value.

## VBA Example

Sub SetLineConstraint()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim i as long
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

'define new constraint
redim Value(5)
for i = 0 To 5
Value(i) = True
Next i
ret = SapModel.ConstraintDef.SetLine("Line1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetLine

# SetLocal

## Syntax

SapObject.SapModel.ConstraintDef.SetLocal

## VB6 Procedure


Function SetLocal(ByVal Name As String, ByRef Value() As Boolean) As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are U1, U2, U3, R1, R2 and R3.

## Remarks

This function defines a Local constraint. If the specified name is not used for a constraint, a new
constraint is defined using the specified name. If the specified name is already used for another
Local constraint, the definition of that constraint is modified. If the specified name is already used
for some constraint that is not a Local constraint, an error is returned.

The function returns zero if the constraint data is successfully added or modified, otherwise it
returns a nonzero value.

## VBA Example

Sub SetLocalConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
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

'define new constraint
redim Value(5)
for i = 0 To 5


Value(i) = True
Next i
ret = SapModel.ConstraintDef.SetLocal("Local1", Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetLocal

# SetPlate

## Syntax

SapObject.SapModel.ConstraintDef.SetPlate

## VB6 Procedure

Function SetPlate(ByVal Name As String, Optional ByVal Axis As eConstraintAxis = AutoAxis,
Optional ByVal CSys As String = "Global") As Long

## Parameters

Name

The name of a constraint.

Axis

This is one of the following items from the eConstraintAxis enumeration. It specifies the axis in
the specified coordinate system that is perpendicular to the plane of the constraint. If AutoAxis is
specified, the axis of the constraint is automatically determined from the joints assigned to the
constraint.

```
X = 1
Y = 2
Z = 3
```
```
AutoAxis = 4
```
CSys


The name of the coordinate system in which the constraint is defined.

## Remarks

This function defines a Plate constraint. If the specified name is not used for a constraint, a new
constraint is defined using the specified name. If the specified name is already used for another
Plate constraint, the definition of that constraint is modified. If the specified name is already used
for some constraint that is not a Plate constraint, an error is returned.

The function returns zero if the constraint data is successfully added or modified, otherwise it
returns a nonzero value.

## VBA Example

Sub SetPlateConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Axis As eConstraintAxis
Dim CSys as String

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

'define new constraint
ret = SapModel.ConstraintDef.SetPlate("Plate1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

GetPlate

# SetRod

## Syntax

SapObject.SapModel.ConstraintDef.SetRod

## VB6 Procedure

Function SetRod(ByVal Name As String, Optional ByVal Axis As eConstraintAxis = AutoAxis,
Optional ByVal CSys As String = "Global") As Long

## Parameters

Name

The name of a constraint.

Axis

This is one of the following items from the eConstraintAxis enumeration. It specifies the axis in
the specified coordinate system that is parallel to the axis of the constraint. If AutoAxis is
specified, the axis of the constraint is automatically determined from the joints assigned to the
constraint.

```
X = 1
Y = 2
Z = 3
```
```
AutoAxis = 4
```
CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

This function defines a Rod constraint. If the specified name is not used for a constraint, a new
constraint is defined using the specified name. If the specified name is already used for another
Rod constraint, the definition of that constraint is modified. If the specified name is already used
for some constraint that is not a Rod constraint, an error is returned.

The function returns zero if the constraint data is successfully added or modified, otherwise it
returns a nonzero value.


## VBA Example

Sub SetRodConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Axis As eConstraintAxis
Dim CSys as String

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

'define new constraint
ret = SapModel.ConstraintDef.SetRod("Rod1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetRod

# SetWeld

## Syntax

SapObject.SapModel.ConstraintDef.SetWeld


## VB6 Procedure

Function SetWeld(ByVal Name As String, ByRef Value() As Boolean, ByVal Tolerance As
Double, Optional ByVal CSys As String = "Global") As Long

## Parameters

Name

The name of an existing constraint.

Value

Value is an array of six booleans that indicate which joint degrees of freedom are included in the
constraint. In order, the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and
RZ.

Tolerance

Joints within this distance of each other are constrained together.

CSys

The name of the coordinate system in which the constraint is defined.

## Remarks

This function defines a Weld constraint. If the specified name is not used for a constraint, a new
constraint is defined using the specified name. If the specified name is already used for another
Weld constraint, the definition of that constraint is modified. If the specified name is already used
for some constraint that is not a Weld constraint, an error is returned.

The function returns zero if the constraint data is successfully added or modified, otherwise it
returns a nonzero value.

## VBA Example

Sub SetWeldConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim i as long
Dim ret As Long
Dim Value() As Boolean
Dim Tolerance As Double

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

'define new contraint
redim Value(5)
for i = 0 To 5
Value(i) = True
Next i
Tolerance = 1
ret = SapModel.ConstraintDef.SetWeld("Weld1", Value, Tolerance)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetWeld


