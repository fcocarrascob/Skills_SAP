# ChangeName

## Syntax

SapObject.SapModel.CoordSys.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined coordinate system.

NewName

The new name for the coordinate system.

## Remarks

The function returns zero if the new name is successfully applied, otherwise it returns a nonzero
value.

Changing the name of the Global coordinate system will fail and return an error.

## VBA Example

Sub ChangeCoordSystemName()
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

'define new coordinate system
ret = SapModel.CoordSys.SetCoordSys("CSys1", 1000, 1000, 0, 0, 0, 0)

'change name of new coordinate system
ret = SapModel.CoordSys.ChangeName("CSys1", "MyCSys")

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

SapObject.SapModel.CoordSys.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

The function returns the number of defined coordinate systems.

## VBA Example

Sub CountCoordSystems()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long

```
'create Sap2000 object
```

Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'return number of defined coordinate systems
ret = SapModel.CoordSys.Count

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Delete

## Syntax

SapObject.SapModel.CoordSys.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing coordinate system.

## Remarks


The function deletes the specified coordinate system. Attempting to delete the Global coordinate
system will fail and return an error.

The function returns zero if the coordinate system is successfully deleted, otherwise it returns a
nonzero value.

## VBA Example

Sub DeleteCoordSystem()
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

'define new coordinate system
ret = SapModel.CoordSys.SetCoordSys("CSys1", 1000, 1000, 0, 0, 0, 0)

'delete coordinate system
ret = SapModel.CoordSys.Delete("CSys1")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetCoordSys


# GetCoordSys

## Syntax

SapObject.SapModel.CoordSys.GetCoordSys

## VB6 Procedure

Function GetCoordSys(ByVal Name As String, ByRef x As Double, ByRef y As Double, ByRef z
As Double, ByRef RZ As Double, ByRef RY As Double, ByRef RX As Double) As Long

## Parameters

Name

The name of an existing coordinate system.

x

The global X coordinate of the origin of the coordinate system. [L]

y

The global Y coordinate of the origin of the coordinate system. [L]

z

The global Z coordinate of the origin of the coordinate system. [L]

RZ, RY, RX

The rotation of an axis of the new coordinate system relative to the global coordinate system is
defined as follows: (1) Rotate the coordinate system about the positive global Z-axis as defined by
the RZ item. (2) Rotate the coordinate system about the positive global Y-axis as defined by the
RY item. (3) Rotate the coordinate system about the positive global X-axis as defined by the RX
item. Note that the order in which these rotations are performed is important. RX, RY and RZ are
angles in degrees [deg].

## Remarks

The function returns zero if the coordinate system data is successfully retrieved, otherwise it
returns a nonzero value.

## VBA Example

Sub GetCoordSystem()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret as Long
Dim x as Double, y as Double, z as Double
Dim RX as Double, RY as Double, RZ as Double

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

'define new coordinate system
ret = SapModel.CoordSys.SetCoordSys("CSys1", 1000, 1000, 0, 0, 0, 0)

'get new coordinate system data
ret = SapModel.CoordSys.GetCoordSys("CSys1", x, y, z, RZ, RY, RX)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetCoordSys

# GetNameList

## Syntax

SapObject.SapModel.CoordSys.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long


## Parameters

NumberNames

The number of coordinate system names retrieved by the program.

MyName

This is a one-dimensional array of coordinate system names. The MyName array is created as a
dynamic, zero-based, array by the API user:

Dim MyName() as String

The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined coordinate systems.

The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetCoordinateSystemNames()
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

'get coordinate system names
ret = SapModel.CoordSys.GetNameList(NumberNames, MyName)


'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetTransformationMatrix

## Syntax

SapObject.SapModel.CoordSys.GetTransformationMatrix

## VB6 Procedure

Function GetTransformationMatrix(ByVal Name As String, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing coordinate system.

Value

Value is an array of nine direction cosines that define the transformation matrix from the specified
global coordinate system to the global coordinate system.

The following matrix equation shows how the transformation matrix is used to convert
coordinates from a coordinate system to the global coordinate system.

In the equation, c0 through c8 are the nine values from the transformation array; (x, y, z) are the
coordinates of a point in the CSys coordinate system; (ux, uy, uz) are the offset of the origin of the
CSys coordinate system from the global coordinate system; and (gx, gy, gz) are the global
coordinates of the point.


## Remarks

The function returns zero if the coordinate system transformation matrix is successfully returned,
otherwise it returns a nonzero value.

## VBA Example

Sub GetCoordSystemMatrix()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
Dim Value() as double

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

'define new coordinate system
ret = SapModel.CoordSys.SetCoordSys("CSys1", 1000, 1000, 0, 0, 0, 0)

'get coordinate system transformation matrix
redim Value(8)
ret = SapModel.CoordSys.GetTransformationMatrix("CSys1", Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# SetCoordSys

## Syntax

SapObject.SapModel.CoordSys.SetCoordSys

## VB6 Procedure

Function SetCoordSys(ByVal Name As String, ByVal x As Double, ByVal y As Double, ByVal z
As Double, ByVal RZ As Double, ByVal RY As Double, ByVal RX As Double) As Long

## Parameters

Name

This is the name of a coordinate system. If this is the name of an existing coordinate system, that
coordinate system is modified, otherwise a new coordinate system is added.

x

The global X coordinate of the origin of the coordinate system. [L]

y

The global Y coordinate of the origin of the coordinate system. [L]

z

The global Z coordinate of the origin of the coordinate system. [L]

RZ, RY, RX

The rotation of an axis of the new coordinate system relative to the global coordinate system is
defined as follows: (1) Rotate the coordinate system about the positive global Z-axis as defined by
the RZ item. (2) Rotate the coordinate system about the positive global Y-axis as defined by the
RY item. (3) Rotate the coordinate system about the positive global X-axis as defined by the RX
item. Note that the order in which these rotations are performed is important. RX, RY and RZ are
angles in degrees [deg].

## Remarks

The function returns zero if the coordinate system is successfully added or modified, otherwise it
returns a nonzero value.

Modifying the Global coordinate system will fail and return an error.


## VBA Example

Sub AddCoordSystem()
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

'define new coordinate system
ret = SapModel.CoordSys.SetCoordSys("CSys1", 1000, 1000, 0, 0, 0, 0)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetCoordSys

Delete


