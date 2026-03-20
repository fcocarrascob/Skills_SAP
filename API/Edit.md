# Divide

## Syntax

SapObject.SapModel.EditArea.Divide

## VB6 Procedure

Function Divide(ByVal Name As String, ByVal MeshType As Long, ByRef NumberAreas As
Long, ByRef AreaName() As String, Optional ByVal n1 As Long = 2, Optional ByVal n2 As
Long = 2, Optional ByVal MaxSize1 As Double = 0, Optional ByVal MaxSize2 As Double = 0,
Optional ByVal PointOnEdgeFromGrid As Boolean = False, Optional ByVal
PointOnEdgeFromLine As Boolean = False, Optional ByVal PointOnEdgeFromPoint As Boolean
= False, Optional ByVal ExtendCookieCutLines As Boolean = False, Optional ByVal Rotation As
Double = 0, Optional ByVal MaxSizeGeneral As Double = 0, Optional ByVal LocalAxesOnEdge
As Boolean = False, Optional ByVal LocalAxesOnFace As Boolean = False, Optional ByVal
RestraintsOnEdge As Boolean = False, Optional ByVal RestraintsOnFace As Boolean = False) As
Long

## Parameters

Name

The name of an existing area object.

MeshType

This item is 1, 2, 3, 4, 5 or 6, indicating the mesh type for the area object.

```
1 = Mesh area into a specified number of objects
2 = Mesh area into objects of a specified maximum size
3 = Mesh area based on points on area edges
4 = Cookie cut mesh area based on lines intersecting edges
5 = Cookie cut mesh area based on points
6 = Mesh area using General Divide Tool
```
Mesh options 1, 2 and 3 apply to quadrilaterals and triangles only.

NumberAreas

The number of area objects created when the specified area object is divided.

AreaName

This is an array of the name of each area object created when the specified area object is divided.

n


This item applies when MeshType = 1. It is the number of objects created along the edge of the
meshed area object that runs from point 1 to point 2.

n

This item applies when MeshType = 1. It is the number of objects created along the edge of the
meshed area object that runs from point 1 to point 3.

MaxSize

This item applies when MeshType = 2. It is the maximum size of objects created along the edge of
the meshed area object that runs from point 1 to point 2. [L]

If this item is input as 0, the default value is used. The default value is 48 inches if the database
units are English or 120 centimeters if the database units are metric.

MaxSize

This item applies when MeshType = 2. It is the maximum size of objects created along the edge of
the meshed area object that runs from point 1 to point 3. [L]

If this item is input as 0, the default value is used. The default value is 48 inches if the database
units are English or 120 centimeters if the database units are metric.

PointOnEdgeFromGrid

This item applies when MeshType = 3. If it is True, points on the area object edges are determined
from intersections of visible grid lines with the area object edges.

PointOnEdgeFromLine

This item applies when MeshType = 3. If it is True, points on the area object edges are determined
from intersections of selected straight line objects with the area object edges.

PointOnEdgeFromPoint

This item applies when MeshType = 3. If it is True, points on the area object edges are determined
from selected point objects that lie on the area object edges.

ExtendCookieCutLines

This item applies when MeshType = 4. MeshType = 4 provides cookie cut meshing based on
selected straight line objects that intersect the area object edges. If the ExtendCookieCutLines
item is True, all selected straight line objects are extended to intersect the area object edges for the
purpose of meshing the area object.

Rotation

This item applies when MeshType = 5. MeshType = 5 provides cookie cut meshing based on two
perpendicular lines passing through selected point objects. By default these lines align with the
area object local 1 and 2 axes. The Rotation item is an angle in degrees that the meshing lines are
rotated from their default orientation. [deg]

MaxSizeGeneral


This item applies when MeshType = 6. It is the maximum size of objects created by the General
Divide Tool.

If this item is input as 0, the default value is used. The default value is 48 inches if the database
units are English or 120 centimeters if the database units are metric.

LocalAxesOnEdge

If this item is True, and if both points along an edge of the original area object have the same local
axes, the program makes the local axes for added points along the edge the same as the edge end
points.

LocalAxesOnFace

If this item is True, and if all points around the perimeter of the original area object have the same
local axes, the program makes the local axes for all added points the same as the perimeter points.

RestraintsOnEdge

If this item is True, and if both points along an edge of the original area object have the same
restraint/constraint, then, if the added point and the adjacent corner points have the same local
axes definition, the program includes the restraint/constraint for added points along the edge.

RestraintsOnFace

If this item is True, and if all points around the perimeter of the original area object have the same
restraint/constraint, then, if an added point and the perimeter points have the same local axes
definition, the program includes the restraint/constraint for the added point.

## Remarks

This function meshes area objects.

The function returns zero if the meshing is successful; otherwise it returns a nonzero value.

## VBA Example

Sub DivideAreaObject()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberAreas As Long
Dim AreaName() As String

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

'divide area object
ret = SapModel.EditArea.Divide("1", 1, NumberAreas, AreaName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# ExpandShrink

## Syntax

SapObject.SapModel.EditArea.ExpandShrink

## VB6 Procedure

Function Divide(ByVal OffsetType As Long, ByVal Offset As Double) As Long

## Parameters

OffsetType

This item is 0, 1 or 2, indicating the offset type for the selected area objects.

```
0 = Offset all area edges
1 = Offset selected area edges only
2 = Offset selected points of selected areas only
```
Offset

The area edge offset distance. Positive distances expand the object and negative distances shrink
the object.[L]


## Remarks

This function expands or shrinks selected area objects.

The function returns zero if it is successful; otherwise it returns a nonzero value.

## VBA Example

Sub ExpandAreaObject()
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

'expand area object
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.AreaObj.SetSelectedEdge("4", 2, True)
ret = SapModel.EditArea.ExpandShrink(1, 48)

'refresh view, updating zoom
ret = SapModel.View.RefreshView(0, False)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also


# Merge

## Syntax

SapObject.SapModel.EditArea.Merge

## VB6 Procedure

Function Merge(ByRef NumberAreas As Long, ByRef AreaName() As String) As Long

## Parameters

NumberAreas

The number of originally selected area objects that remain when the merge is successfully
completed.

AreaName

This is an array that includes the names of the selected area objects that remain when the merge is
successfully completed.

## Remarks

This function merges selected area objects.

The function returns zero if it is successful; otherwise it returns a nonzero value.

## VBA Example

Sub MergeAreaObjects()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberAreas As Long
Dim AreaName() As String

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

'merge area objects
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.AreaObj.SetSelected("1", True)
ret = SapModel.AreaObj.SetSelected("2", True)
ret = SapModel.AreaObj.SetSelected("4", True)
ret = SapModel.EditArea.Merge(NumberAreas, AreaName)

'refresh window
ret = SapModel.View.RefreshWindow

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# PointAdd

## Syntax

SapObject.SapModel.EditArea.PointAdd

## VB6 Procedure

Function PointAdd() As Long

## Parameters

None

## Remarks

This function adds a point object at the midpoint of selected area object edges.

The function returns zero if it is successful; otherwise it returns a nonzero value.


## VBA Example

Sub AddPointToAreaObject()
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

'add point to area object
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.AreaObj.SetSelectedEdge("4", 2, True)
ret = SapModel.EditArea.PointAdd

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

PointRemove

# PointRemove

## Syntax

SapObject.SapModel.EditArea.PointRemove


## VB6 Procedure

Function PointRemove() As Long

## Parameters

None

## Remarks

This function removes selected point objects from selected area objects. Note that in some cases
this command can cause the area object to be deleted.

The function returns zero if it is successful; otherwise it returns a nonzero value.

## VBA Example

Sub RemovePointFromAreaObject()
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

'remove point from area object
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.AreaObj.SetSelected("4", True)
ret = SapModel.PointObj.SetSelected("9", True)
ret = SapModel.EditArea.PointRemove

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.00.

## See Also

PointAdd

# ChangeConnectivity

## Syntax

SapObject.SapModel.EditArea.ChangeConnectivity

## VB6 Procedure

Function ChangeConnectivity(ByVal Name As String, ByVal NumberPoints As Long, ByRef
Point() As String) As Long

## Parameters

Name

The name of an existing area object.

NumberPoints

The number of points in the area abject.

Point

This is an array containing the names of the point objects that define the added area object. The
point object names should be ordered to run clockwise or counter-clockwise around the area
object.

## Remarks

This function modifies the connectivity of an area object.

The function returns zero if the area object connectivity is successfully modified; otherwise it
returns a nonzero value.

## VBA Example

Sub ModifyAreaObjConnectivity()
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

'get names of points
ret = SapModel.AreaObj.GetPoints("2", NumberPoints, Point)

'modify connectivity
NumberPoints = NumberPoints - 1
ReDim Preserve Point(NumberPoints )
ret = SapModel.EditArea.ChangeConnectivity("2", NumberPoints, Point)
ret = SapModel.View.RefreshWindow

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

# DivideAtDistance

## Syntax

SapObject.SapModel.EditFrame.DivideAtDistance

## VB6 Procedure


Function DivideAtDistance(ByVal Name As String, ByVal Dist As Double, ByVal IEnd As
Boolean, ByRef NewName() As String) As Long

## Parameters

Name

The name of an existing straight frame object.

Dist

The frame object is divided at this distance from the end specified by the IEnd item.[L]

IEnd

If this item is True, the Dist item is measured from the I-end of the frame object. Otherwise it is
measured from the J-end of the frame object.

Num

This is the number of frame objects into which the specified frame object is divided.

NewName

This is an array that includes the names of the two new frame objects.

## Remarks

This function divides straight frame objects into two objects at a location defined by the Dist and
IEnd items. Curved frame objects are not divided.

The function returns zero if the frame objects are successfully divided; otherwise it returns a
nonzero value.

## VBA Example

Sub DivideFrameObjectAtDistance()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NewName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel


'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'divide frame object at distance
ret = SapModel.EditFrame.DivideAtDistance("8", 100, True, NewName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

DivideByRatio

DivideAtIntersections

# DivideAtIntersections

## Syntax

SapObject.SapModel.EditFrame.DivideAtIntersections

## VB6 Procedure

Function DivideAtIntersections(ByVal Name As String, ByRef Num As Double, ByRef
NewName() As String) As Long

## Parameters

Name

The name of an existing straight frame object.

Num

This is the number of frame objects into which the specified frame object is divided.

NewName

This is an array that includes the names of the new frame objects.


## Remarks

This function divides straight frame objects at intersections with selected point objects, line
objects, area edges and solid edges. Curved frame objects are not divided.

The function returns zero if the frame objects are successfully divided; otherwise it returns a
nonzero value.

## VBA Example

Sub DivideFrameObjectAtIntersections()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim NewName() As String
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

'add point objects to model and select them
ret = SapModel.PointObj.AddCartesian(-188, 0, 288, Name)
ret = SapModel.PointObj.SetSelected(Name, True)
ret = SapModel.PointObj.AddCartesian(-88, 0, 288, Name)
ret = SapModel.PointObj.SetSelected(Name, True)

'divide frame object at intersections
ret = SapModel.EditFrame.DivideAtIntersections("8", Num, NewName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.00.

## See Also

DivideByRatio

DivideAtDistance

# DivideByRatio

## Syntax

SapObject.SapModel.EditFrame.DivideByRatio

## VB6 Procedure

Function DivideByRatio(ByVal Name As String, ByVal Num As long, ByVal Ratio As Double,
ByRef NewName() As String) As Long

## Parameters

Name

The name of an existing straight frame object.

Num

The frame object is divided into this number of new objects.

Ratio

The Last/First length ratio for the new frame objects.

NewName

This is an array that includes the names of the new frame objects.

## Remarks

This function divides straight frame objects based on a specified Last/First length ratio. Curved
frame objects are not divided.

The function returns zero if the frame objects are successfully divided; otherwise it returns a
nonzero value.

## VBA Example

Sub DivideFrameObjectByRatio()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NewName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'divide frame object by ratio
ret = SapModel.EditFrame.DivideByRatio("8", 3, 0.3, NewName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

DivideAtDistance

DivideAtIntersections

# Extend

## Syntax

SapObject.SapModel.EditFrame.Extend

## VB6 Procedure

Function Extend(ByVal Name As String, ByVal IEnd As Boolean, ByVal JEnd As Boolean,
ByVal Item1 As String, Optional ByVal Item2 As String = "") As Long


## Parameters

Name

The name of an existing straight frame object to be extended.

IEnd

This item is True if the I-End of the frame object specified by the Name item is to be extended.

JEnd

This item is True if the J-End of the frame object specified by the Name item is to be extended.

Item

The name of an existing straight frame object used as a extension line.

Item

The name of an existing straight frame object used as a extension line.

## Remarks

This function extends straight frame objects. Curved frame objects are not extended.

The function returns zero if the frame objects are successfully extended; otherwise it returns a
nonzero value.

## VBA Example

Sub ExtendFrameObject()
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


'add frame object by coordinates
ret = SapModel.FrameObj.AddByCoord(-180, 0, 180, -180, 0, 240, Name)

'refresh window
ret = SapModel.View.RefreshWindow

'extend frame object
ret = SapModel.EditFrame.Extend(Name, True, True, "7", "8")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

Trim

# Join

## Syntax

SapObject.SapModel.EditFrame.Join

## VB6 Procedure

Function Join(ByVal Name As String, ByVal Item2 As String) As Long

## Parameters

Name

The name of an existing frame object to be joined. The new, joined frame object keeps this name.

Item

The name of an existing frame object to be joined.

## Remarks

This function joins two straight frame objects that have a common end point and are colinear.


The function returns zero if the frame objects are successfully joined; otherwise it returns a
nonzero value.

## VBA Example

Sub JoinFrameObjects()
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

'join frame objects
ret = SapModel.EditFrame.Join("8", "10")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

DivideAtDistance

DivideAtIntersections

DivideByRatio

# Trim


## Syntax

SapObject.SapModel.EditFrame.Trim

## VB6 Procedure

Function Trim(ByVal Name As String, ByVal IEnd As Boolean, ByVal JEnd As Boolean, ByVal
Item1 As String, Optional ByVal Item2 As String = "") As Long

## Parameters

Name

The name of an existing straight frame object to be trimmed.

IEnd

This item is True if the I-End of the frame object specified by the Name item is to be trimmed.

JEnd

This item is True if the J-End of the frame object specified by the Name item is to be trimmed.

Item

The name of an existing straight frame object used as a trim line.

Item

The name of an existing straight frame object used as a trim line.

## Remarks

This function trims straight frame objects. Curved frame objects are not trimmed.

The function returns zero if the frame objects are successfully trimmed; otherwise it returns a
nonzero value.

## VBA Example

Sub TrimFrameObject()
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

'add frame object by coordinates
ret = SapModel.FrameObj.AddByCoord(-180, 0, 100, -180, 0, 360, Name)

'refresh window
ret = SapModel.View.RefreshWindow

'trim frame object
ret = SapModel.EditFrame.Trim(Name, True, True, "7", "8")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

Extend

# ChangeConnectivity

## Syntax

SapObject.SapModel.EditFrame.ChangeConnectivity

## VB6 Procedure

Function ChangeConnectivity(ByVal Name As String, ByVal Point1 As String, ByVal Point2 As
String) As Long

## Parameters

Name


The name of an existing frame object.

Point1

The name of the point object at the I-End of the frame object.

Point2

The name of the point object at the J-End of the frame object.

## Remarks

This function modifies the connectivity of a frame object.

The function returns zero if the frame object connectivity is successfully modified; otherwise it
returns a nonzero value.

## VBA Example

Sub ModifyFrameObjConnectivity()
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

'modify connectivity
ret = SapModel.EditFrame.ChangeConnectivity("8", "3", "5")
ret = SapModel.View.RefreshWindow

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.03.

## See Also

# Align

## Syntax

SapObject.SapModel.EditPoint.Align

## VB6 Procedure

Function Align(ByVal MyType As Long, ByVal Ordinate As Double, ByRef NumberPoints As
Long, ByRef PointName() As String) As Long

## Parameters

MyType

This is 1, 2, 3 or 4, indicating the alignment option.

```
1 = Align points to X-ordinate in present coordinate system
2 = Align points to Y-ordinate in present coordinate system
3 = Align points to Z-ordinate in present coordinate system
4 = Align points to nearest selected line object, area object edge or solid object edge
```
Ordinate

The X, Y or Z ordinate that applies if MyType is 1, 2 or 3, respectively. [L]

NumberPoints

The number of point objects that are in a new location after the alignment is complete.

PointName

This is an array of the name of each point object that is in a new location after the alignment is
complete.

## Remarks

This function aligns selected point objects.

The function returns zero if the alignment is successful; otherwise it returns a nonzero value.


## VBA Example

Sub AlignPointObjects()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberPoints As Long
Dim PointName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'align point objects
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.PointObj.SetSelected("1", True)
ret = SapModel.PointObj.SetSelected("2", True)
ret = SapModel.PointObj.SetSelected("3", True)
ret = SapModel.EditPoint.Align(1, -300, NumberPoints, PointName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Connect

## Syntax

SapObject.SapModel.EditPoint.Connect


## VB6 Procedure

Function Connect(ByRef NumberPoints As Long, ByRef PointName() As String) As Long

## Parameters

NumberPoints

The number of the point objects that remain at locations where connections were made.

PointName

This is an array of the name of each point object that remains at locations where connections were
made.

## Remarks

This function connects objects that have been disconnected using the Disconnect function. If two
or more objects have different end points objects that are at the same location, all of those objects
can be connected together by selecting the objects, and selecting their end points, and calling the
Connect function. The result will be that all of the objects are connected at a single point.

The function returns zero if the connect is successful; otherwise it returns a nonzero value.

## VBA Example

Sub ConnectObjects()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim Point1 As String, Point2 As String
Dim NumberPoints As Long
Dim PointName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)


'disconnect point objects
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.PointObj.SetSelected("3", True)
ret = SapModel.PointObj.SetSelected("9", True)
ret = SapModel.EditPoint.Disconnect(NumberPoints, PointName)

'connect objects
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.FrameObj.SetSelected("2", True)
ret = SapModel.FrameObj.SetSelected("8", True)
ret = SapModel.FrameObj.GetPoints("2", Point1, Point2)
ret = SapModel.PointObj.SetSelected(Point2, True)
ret = SapModel.FrameObj.GetPoints("8", Point1, Point2)
ret = SapModel.PointObj.SetSelected(Point1, True)
ret = SapModel.EditPoint.Connect(NumberPoints, PointName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

Disconnect

# Disconnect

## Syntax

SapObject.SapModel.EditPoint.Disconnect

## VB6 Procedure

Function Disconnect(ByRef NumberPoints As Long, ByRef PointName() As String) As Long

## Parameters

NumberPoints

The number of the point objects (including the original selected point objects) that are created by
the disconnect action.

PointName


This is an array of the name of each point object (including the original selected point objects) that
is created by the disconnect action.

## Remarks

This function disconnects selected point objects. Disconnect creates a separate point for each
object that frames into the selected point object.

The function returns zero if the disconnect is successful; otherwise it returns a nonzero value.

## VBA Example

Sub DisconnectPointObjects()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberPoints As Long
Dim PointName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'disconnect point objects
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.PointObj.SetSelected("3", True)
ret = SapModel.EditPoint.Disconnect(NumberPoints, PointName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

Connect

# Merge

## Syntax

SapObject.SapModel.EditPoint.Merge

## VB6 Procedure

Function Merge(ByVal MergeTol As Double, ByRef NumberPoints As Long, ByRef PointName()
As String) As Long

## Parameters

MergeTol

Point objects within this distance of one another are merged into one point object. [L]

NumberPoints

The number of the selected point objects that still exist after the merge is complete.

PointName

This is an array of the name of each selected point object that still exists after the merge is
complete.

## Remarks

This function merges selected point objects that are within a specified distance of one another.

The function returns zero if the merge is successful; otherwise it returns a nonzero value.

## VBA Example

Sub MergePointObjects()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim Point1 As String, Point2 As String
Dim NumberPoints As Long
Dim PointName() As String


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'add frame object by coordinates
ret = SapModel.FrameObj.AddByCoord(-400, 0, 288, -289, 0, 288, Name)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'merge point objects
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.PointObj.SetSelected("3", True)
ret = SapModel.FrameObj.GetPoints(Name, Point1, Point2)
ret = SapModel.PointObj.SetSelected(Point2, True)
ret = SapModel.EditPoint.Merge(2, NumberPoints, PointName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# ChangeCoordinates_1

## Syntax

SapObject.SapModel.EditPoint.ChangeCoordinates_1

## VB6 Procedure


Function ChangeCoordinates_1(ByVal Name As String, ByVal x As Double, ByVal y As Double,
ByVal z As Double, Optional ByVal NoRefresh As Boolean = False) As Long

## Parameters

Name

The name of an existing point object.

x, y, z

These are the new x, y and z coordinates, in the present coordinate system, for the specified point
object.

NoRefresh

If this item is True, the model display window is not refreshed after the point object is moved.

## Remarks

This function changes the coordinates of a specified point object.

The function returns zero if the coordinate change is successful; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangePointCoordinates_1()
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

'change point coordinates
ret = SapModel.EditPoint.ChangeCoordinates_1("1", -288, 0, 36)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.05.

This function supersedes ChangeCoordinates.

Modified optional argument NoRefresh to be ByVal in version 12.0.1.

## See Also

# Divide

## Syntax

SapObject.SapModel.EditSolid.Divide

## VB6 Procedure

Function Divide(ByVal Name As String, ByVal n1 As Long, ByVal n2 As Long, ByVal n3 As
Long, ByRef NumberSolids As Long, ByRef SolidName() As String) As Long

## Parameters

Name

The name of an existing solid object.

n1

This is the number of objects created between faces 2 and 4 of the solid object.

n2

This is the number of objects created between faces 1 and 3 of the solid object.

n3

This is the number of objects created between faces 5 and 6 of the solid object.

NumberSolids

The number of solid objects created when the specified solid object is divided.

SolidName


This is an array of the name of each solid object created when the specified solid object is divided.

## Remarks

This function meshes solid objects.

The function returns zero if the meshing is successful; otherwise it returns a nonzero value.

## VBA Example

Sub DivideSolidObject()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberSolids As Long
Dim SolidName() As String

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

'divide solid object
ret = SapModel.EditSolid.Divide("1", 2, 3, 4, NumberSolids, SolidName)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# ExtrudeAreaToSolidLinearNormal

## Syntax

SapObject.SapModel.EditGeneral.ExtrudeAreaToSolidLinearNormal

## VB6 Procedure

Function ExtrudeAreaToSolidLinearNormal(ByVal Name As String, ByVal PropName As String,
ByVal nPlus3 As Long, ByVal tPlus3 As Double, ByVal nMinus3 As Long, ByVal tMinus3 As
Double, ByRef NumberSolids As Long, ByRef SolidName() As String, Optional ByVal Remove
As Boolean = True) As Long

## Parameters

Name

The name of an existing area object to be extruded.

PropName

This is either Default or the name of a defined solid property to be used for the new extruded solid
objects.

nPlus3

The number of solid objects created in the positive local 3-axis direction of the specified area
object.

tPlus3

The thickness of the solid objects created in the positive local 3-axis direction of the specified area
object.

nMinus3

The number of solid objects created in the negative local 3-axis direction of the specified area
object.

tMinus3

The thickness of the solid objects created in the negative local 3-axis direction of the specified
area object.

NumberSolids

The number of solid objects created when the specified area object is extruded.

SolidName


This is an array of the name of each solid object created when the specified area object is
extruded.

Remove

If this item is True, the area object indicated by the Name item is deleted after the extrusion is
complete.

## Remarks

This function creates new solid objects by linearly extruding a specified area object, in the local 3-
axis direction of the area object, into solid objects.

The function returns zero if the extrusion is successful; otherwise it returns a nonzero value.

## VBA Example

Sub LinearNormalAreaExtrusionToSolids()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberSolids As Long
Dim SolidName() As String

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

'linearly extrude area to solids normal to area
ret = SapModel.EditGeneral.ExtrudeAreaToSolidLinearNormal("2", "Default", 1, 48, 1, 48,
NumberSolids, SolidName, True)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.00.

Modified optional argument Remove to be ByVal in version 12.0.1.

## See Also

ExtrudeAreaToSolidLinearUser

ExtrudeAreaToSolidRadial

# ExtrudeAreaToSolidLinearUser

## Syntax

SapObject.SapModel.EditGeneral.ExtrudeAreaToSolidLinearUser

## VB6 Procedure

Function ExtrudeAreaToSolidLinearUser(ByVal Name As String, ByVal PropName As String,
ByVal dx As Double, ByVal dy As Double, ByVal dz As Double, ByVal Number As Long,
ByRef NumberSolids As Long, ByRef SolidName() As String, Optional ByVal Remove As
Boolean = True) As Long

## Parameters

Name

The name of an existing area object to be extruded.

PropName

This is either Default or the name of a defined solid property to be used for the new extruded solid
objects.

dx, dy, dz

These are the x, y and z offsets used, in the present coordinate system, to create each new solid
object.

Number

The number of increments for the extrusion.

NumberSolids

The number of solid objects created when the specified area object is extruded. Usually this item
is returned the same as the Number item. However, in some cases, such as when an area object
with more than four sides is extruded, this item will be larger than the Number item.


SolidName

This is an array of the name of each solid object created when the specified area object is
extruded.

Remove

If this item is True, the area object indicated by the Name item is deleted after the extrusion is
complete.

## Remarks

This function creates new solid objects by linearly extruding a specified area object, in a user
specified direction, into solid objects.

The function returns zero if the extrusion is successful; otherwise it returns a nonzero value.

## VBA Example

Sub LinearUserAreaExtrusionToSolids()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberSolids As Long
Dim SolidName() As String

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

'linearly extrude area to solids in user direction
ret = SapModel.EditGeneral.ExtrudeAreaToSolidLinearUser("2", "Default", 20, 144, 0, 3,
NumberSolids, SolidName, True)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Modified optional argument Remove to be ByVal in version 12.0.1.

## See Also

ExtrudeAreaToSolidLinearNormal

ExtrudeAreaToSolidRadial

# ExtrudeAreaToSolidRadial

## Syntax

SapObject.SapModel.EditGeneral.ExtrudeAreaToSolidRadial

## VB6 Procedure

Function ExtrudeAreaToSolidRadial(ByVal Name As String, ByVal PropName As String, ByVal
RotateAxis As Long, ByVal x As Double, ByVal y As Double, ByVal z As Double, ByVal
IncrementAng As Double, ByVal TotalRise As Double, ByVal Number As Long, ByRef
NumberSolids As Long, ByRef SolidName() As String, Optional ByVal Remove As Boolean =
True) As Long

## Parameters

Name

The name of an existing area object to be extruded.

PropName

This is either Default or the name of a defined solid property to be used for the new extruded solid
objects.

RotateAxis

This is 0, 1 or 2, indicating the axis that the radial extrusion is around.

```
0 = X axis
1 = Y axis
2 = Z axis
```
x, y, z


These are the x, y and z coordinates, in the present coordinate system, of the point that the radial
extrusion is around. For rotation about the X axis the value of the x coordinate is irrelevant.
Similarly, for rotation about the Y and Z axes the y and z coordinates, respectively, are irrelevant.
[L]

IncrementAng

The angle is rotated by this amount for each added solid object. [deg]

TotalRise

The total rise over the full length of the extrusion. [L]

Number

The number of angle increments for the extrusion.

NumberSolids

The number of solid objects created when the specified area object is extruded. Usually this item
is returned the same as the Number item. However, in some cases, such as when an area object
with more than four sides is extruded, this item will be larger than the Number item.

SolidName

This is an array of the name of each solid object created when the specified area object is
extruded.

Remove

If this item is True, the area object indicated by the Name item is deleted after the extrusion is
complete.

## Remarks

This function creates new solid objects by radially extruding a specified area object into solid
objects.

The function returns zero if the extrusion is successful; otherwise it returns a nonzero value.

## VBA Example

Sub RadialAreaExtrusionToSolids()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberSolids As Long
Dim SolidName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(5, 48, 2, 48)

'radially extrude area to solid
ret = SapModel.EditGeneral.ExtrudeAreaToSolidRadial("2", "Default", 2, 0, 0, 96, 30, 0, 6,
NumberSolids, SolidName)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Modified optional argument Remove to be ByVal in version 12.0.1.

## See Also

ExtrudeAreaToSolidLinearNormal

ExtrudeAreaToSolidLinearUser

# ExtrudeFrameToAreaLinear

## Syntax

SapObject.SapModel.EditGeneral.ExtrudeFrameToAreaLinear

## VB6 Procedure


Function ExtrudeFrameToAreaLinear(ByVal Name As String, ByVal PropName As String,
ByVal dx As Double, ByVal dy As Double, ByVal dz As Double, ByVal NumberAreas As Long,
ByRef AreaName() As String, Optional ByVal Remove As Boolean = True) As Long

## Parameters

Name

The name of an existing straight frame object to be extruded.

PropName

This is Default, None or the name of a defined area property to be used for the new extruded area
objects.

dx, dy, dz

These are the x, y and z offsets used, in the present coordinate system, to create each new area
object.

NumberAreas

The number of area objects created when the specified line object is extruded.

AreaName

This is an array of the name of each area object created when the specified line object is extruded.

Remove

If this item is True, the straight frame object indicated by the Name item is deleted after the
extrusion is complete.

## Remarks

This function creates new area objects by linearly extruding a specified straight frame object into
area objects.

The function returns zero if the extrusion is successful; otherwise it returns a nonzero value.

## VBA Example

Sub LinearFrameExtrusionToAreas()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim AreaName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'linearly extrude frame to areas
ret = SapModel.EditGeneral.ExtrudeFrameToAreaLinear("8", "Default", 0, 144, 0, 3,
AreaName, True)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Modified optional argument Remove to be ByVal in version 12.0.1.

## See Also

ExtrudeFrameToAreaRadial

# ExtrudeFrameToAreaRadial

## Syntax

SapObject.SapModel.EditGeneral.ExtrudeFrameToAreaRadial

## VB6 Procedure

Function ExtrudeFrameToAreaRadial(ByVal Name As String, ByVal PropName As String,
ByVal RotateAxis As Long, ByVal x As Double, ByVal y As Double, ByVal z As Double, ByVal
IncrementAng As Double, ByVal TotalRise As Double, ByVal NumberAreas As Long, ByRef
AreaName() As String, Optional ByVal Remove As Boolean = True) As Long


## Parameters

Name

The name of an existing line object to be extruded.

PropName

This is Default, None or the name of a defined area property to be used for the new extruded area
objects.

RotateAxis

This is 0, 1 or 2, indicating the axis that the radial extrusion is around.

```
0 = X axis
1 = Y axis
2 = Z axis
```
x, y, z

These are the x, y and z coordinates, in the present coordinate system, of the point that the radial
extrusion is around. For rotation about the X axis the value of the x coordinate is irrelevant.
Similarly, for rotation about the Y and Z axes the y and z coordinates, respectively, are irrelevant.
[L]

IncrementAng

The angle is rotated by this amount for each added area object. [deg]

TotalRise

The total rise over the full length of the extrusion. [L]

NumberAreas

The number of area objects created when the specified line object is extruded.

AreaName

This is an array of the name of each area object created when the specified line object is extruded.

Remove

If this item is True, the straight frame object indicated by the Name item is deleted after the
extrusion is complete.

## Remarks

This function creates new area objects by radially extruding a specified straight frame object into
area objects.

The function returns zero if the extrusion is successful; otherwise it returns a nonzero value.


## VBA Example

Sub RadialFrameExtrusionToAreas()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim AreaName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 3, 288)

'radially extrude frame to areas
ret = SapModel.EditGeneral.ExtrudeFrameToAreaRadial("10", "Default", 2, 0, 0, 288, 30, 0,
6, AreaName)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Modified optional argument Remove to be ByVal in version 12.0.1.

## See Also

ExtrudeFrameToAreaLinear

# ExtrudePointToFrameLinear


## Syntax

SapObject.SapModel.EditGeneral.ExtrudePointToFrameLinear

## VB6 Procedure

Function ExtrudePointToFrameLinear(ByVal Name As String, ByVal PropName As String,
ByVal dx As Double, ByVal dy As Double, ByVal dz As Double, ByVal NumberFrames As
Long, ByRef FrameName() As String) As Long

## Parameters

Name

The name of an existing point object to be extruded.

PropName

This is Default, None or the name of a defined frame section property to be used for the new
extruded frame objects.

dx, dy, dz

These are the x, y and z offsets used, in the present coordinate system, to create each new frame
object.

NumberFrames

The number of frame objects created when the specified point object is extruded.

FrameName

This is an array of the name of each frame object created when the specified point object is
extruded.

## Remarks

This function creates new frame objects by linearly extruding a specified point object into frame
objects.

The function returns zero if the extrusion is successful; otherwise it returns a nonzero value.

## VBA Example

Sub LinearPointExtrusionToFrames()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FrameName() As String


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'linearly extrude point to frames
ret = SapModel.EditGeneral.ExtrudePointToFrameLinear("3", "FSec1", 0, 144, 0, 3,
FrameName)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

ExtrudePointToFrameRadial

# ExtrudePointToFrameRadial

## Syntax

SapObject.SapModel.EditGeneral.ExtrudePointToFrameRadial

## VB6 Procedure

Function ExtrudePointToFrameRadial(ByVal Name As String, ByVal PropName As String,
ByVal RotateAxis As Long, ByVal x As Double, ByVal y As Double, ByVal z As Double, ByVal
IncrementAng As Double, ByVal TotalRise As Double, ByVal NumberFrames As Long, ByRef
FrameName() As String) As Long


## Parameters

Name

The name of an existing point object to be extruded.

PropName

This is Default, None or the name of a defined frame section property to be used for the new
extruded frame objects.

RotateAxis

This is 0, 1 or 2, indicating the axis that the radial extrusion is around.

```
0 = X axis
1 = Y axis
2 = Z axis
```
x, y, z

These are the x, y and z coordinates, in the present coordinate system, of the point that the radial
extrusion is around. For rotation about the X axis, the value of the x coordinate is irrelevant.
Similarly, for rotation about the Y and Z axes, the y and z coordinates, respectively, are irrelevant.
[L]

IncrementAng

The angle is rotated by this amount for each added frame object. [deg]

TotalRise

The total rise over the full length of the extrusion. [L]

NumberFrames

The number of frame objects created when the specified point object is extruded.

FrameName

This is an array of the name of each frame object created when the specified point object is
extruded.

## Remarks

This function creates new frame objects by radially extruding a specified point object into frame
objects.

The function returns zero if the extrusion is successful; otherwise it returns a nonzero value.

## VBA Example


Sub RadialPointExtrusionToFrames()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FrameName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'radially extrude point to frames
ret = SapModel.EditGeneral.ExtrudePointToFrameRadial("3", "FSec1", 2, 0, 0, 288, 30, 0, 6,
FrameName)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

ExtrudePointToFrameLinear

# Move

## Syntax

SapObject.SapModel.EditGeneral.Move


## VB6 Procedure

Function Move(ByVal dx As Double, ByVal dy As Double, ByVal dz As Double) As Long

## Parameters

dx, dy, dz

These are the x, y and z offsets used, in the present coordinate system, for moving the selected
objects.

## Remarks

This function moves selected point, frame, cable, tendon, area, solid and link objects.

The function returns zero if the move is successful; otherwise it returns a nonzero value.

## VBA Example

Sub MoveObjects()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FrameName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'move objects
ret = SapModel.SelectObj.ClearSelection
ret = SapModel.PointObj.SetSelected("3", True)
ret = SapModel.PointObj.SetSelected("6", True)
ret = SapModel.PointObj.SetSelected("9", True)
ret = SapModel.FrameObj.SetSelected("8", True)
ret = SapModel.FrameObj.SetSelected("10", True)
ret = SapModel.EditGeneral.Move(0, 0, 12)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# ReplicateLinear

## Syntax

SapObject.SapModel.EditGeneral.ReplicateLinear

## VB6 Procedure

Function ReplicateLinear(ByVal dx As Double, ByVal dy As Double, ByVal dz As Double,
ByVal Number As Long, ByRef NumberObjects As Long, ByRef ObjectName() As String, ByRef
ObjectType() As Long, Optional ByVal Remove As Boolean = False) As Long

## Parameters

dx, dy, dz

These are the x, y and z offsets used, in the present coordinate system, to replicate the selected
objects.

Number

The number of times the selected objects are to be replicated.

NumberObjects

The number of new objects created by the replication process.

ObjectName

This is an array of the name of each object created by the replication process.

ObjectType

This is an array of the type of each object created by the replication process.

```
1 = Point object
2 = Frame object
```

```
3 = Cable object
4 = Tendon object
5 = Area object
6 = Solid object
7 = Link object
```
Remove

If this item is True, the originally selected objects are deleted after the replication is complete.

## Remarks

This function linearly replicates selected objects.

The function returns zero if the replication is successful; otherwise it returns a nonzero value.

## VBA Example

Sub LinearReplication()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberObjects As Long
Dim ObjectName() As String
Dim ObjectType() As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'linearly replicate
ret = SapModel.SelectObj.All
ret = SapModel.EditGeneral.ReplicateLinear(0, 288, 0, 1, NumberObjects, ObjectName,
ObjectType)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Modified optional argument Remove to be ByVal in version 12.0.1.

## See Also

ReplicateRadial

ReplicateMirror

# ReplicateMirror

## Syntax

SapObject.SapModel.EditGeneral.ReplicateMirror

## VB6 Procedure

Function ReplicateMirror(ByVal Plane As Long, ByVal x1 As Double, ByVal y1 As Double,
ByVal z1 As Double, ByVal x2 As Double, ByVal y2 As Double, ByVal z2 As Double, ByVal x3
As Double, ByVal y3 As Double, ByVal z3 As Double, ByRef NumberObjects As Long, ByRef
ObjectName() As String, ByRef ObjectType() As Long, Optional ByVal Remove As Boolean =
False) As Long

## Parameters

Plane

This is 1, 2, 3 or 4, indicating the mirror plane type.

```
1 = Parallel to Z
2 = Parallel to X
3 = Parallel to Y
4 = 3D plane
```
x1, y1, z1, x2, y2, z2, x3, y3, z3

These are the coordinates of three points used to define the mirror plane. [L]

When Plane = 1, x1, y1, x2 and y2 define the intersection of the mirror plane with the XY plane.

When Plane = 2, y1, z1, y2 and z2 define the intersection of the mirror plane with the YZ plane.


When Plane = 3, x1, z1, x2 and z2 define the intersection of the mirror plane with the XZ plane.

When Plane = 4, x1, y1, z1, x2, y2, z2, x3, y3 and z3 define three points that define the mirror
plane.

NumberObjects

The number of new objects created by the replication process.

ObjectName

This is an array of the name of each object created by the replication process.

ObjectType

This is an array of the type of each object created by the replication process.

```
1 = Point object
2 = Frame object
3 = Cable object
4 = Tendon object
5 = Area object
6 = Solid object
7 = Link object
```
Remove

If this item is True, the originally selected objects are deleted after the replication is complete.

## Remarks

This function mirror replicates selected objects.

The function returns zero if the replication is successful; otherwise it returns a nonzero value.

## VBA Example

Sub MirrorReplication()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberObjects As Long
Dim ObjectName() As String
Dim ObjectType() As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object


Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'mirror replicate
ret = SapModel.SelectObj.All
ret = SapModel.EditGeneral.ReplicateMirror(1, 300, 0, 0, 300, 100, 0, 0, 0, 0,
NumberObjects, ObjectName, ObjectType)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Modified optional argument Remove to be ByVal in version 12.0.1.

## See Also

ReplicateLinear

ReplicateRadial

# ReplicateRadial

## Syntax

SapObject.SapModel.EditGeneral.ReplicateRadial

## VB6 Procedure

Function ReplicateRadial(ByVal RotateAxis As Long, ByVal x1 As Double, ByVal y1 As
Double, ByVal z1 As Double, ByVal x2 As Double, ByVal y2 As Double, ByVal z2 As Double,
ByVal Number As Long, ByVal Ang As Double, ByRef NumberObjects As Long, ByRef
ObjectName() As String, ByRef ObjectType() As Long, Optional ByVal Remove As Boolean =
False) As Long


## Parameters

RotateAxis

This is 1, 2, 3 or 4, indicating the rotation axis.

```
1 = Parallel to X axis
2 = Parallel to Y axis
3 = Parallel to Z axis
4 = 3D line
```
x1, y1, z1

These are coordinates used to define the rotation axis. [L]

When RotateAxis = 1, y1 and z1 define the intersection of the rotation axis with the YZ plane.

When RotateAxis = 2, x1 and z1 define the intersection of the rotation axis with the XZ plane.

When RotateAxis = 3, x1 and y1 define the intersection of the rotation axis with the XY plane.

When RotateAxis = 4, x1, y1 and z1 define one point on the rotation axis.

x2, y2, z2

These are coordinates used to define the rotation axis when RotateAxis = 4. x2, y2 and z2 define a
second point on the rotation axis. [L]

Number

The increment angle for each replication.

Ang

The number of times the selected objects are to be replicated.

NumberObjects

The number of new objects created by the replication process.

ObjectName

This is an array of the name of each object created by the replication process.

ObjectType

This is an array of the type of each object created by the replication process.

```
1 = Point object
2 = Frame object
3 = Cable object
4 = Tendon object
5 = Area object
6 = Solid object
7 = Link object
```

Remove

If this item is True, the originally selected objects are deleted after the replication is complete.

## Remarks

This function radially replicates selected objects.

The function returns zero if the replication is successful; otherwise it returns a nonzero value.

## VBA Example

Sub RadialReplication()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberObjects As Long
Dim ObjectName() As String
Dim ObjectType() As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'radially replicate
ret = SapModel.SelectObj.All
ret = SapModel.EditGeneral.ReplicateRadial(3, -360, 0, 0, 0, 0, 0, 2, 45, NumberObjects,
ObjectName, ObjectType)

'refresh view
ret = SapModel.View.RefreshView(0, False)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.00.

Modified optional argument Remove to be ByVal in version 12.0.1.

## See Also

ReplicateLinear

ReplicateMirror


