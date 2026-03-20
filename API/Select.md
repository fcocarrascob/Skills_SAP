# All

## Syntax

SapObject.SapModel.SelectObj.All

## VB6 Procedure

Function All(Optional ByVal DeSelect As Boolean = False) As Long

## Parameters

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all objects in the model.

This function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectAll()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(ConcentricBraced, 3, 124, 3, 200)

'select all
ret = SapModel.SelectObj.All


'deselect all
ret = SapModel.SelectObj.All(True)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# ClearSelection

## Syntax

SapObject.SapModel.SelectObj.ClearSelection

## VB6 Procedure

Function ClearSelection() As Long

## Parameters

None

## Remarks

This function deselects all objects in the model. It returns zero if the selection status is
successfully set, otherwise it returns nonzero.

## VBA Example

Sub ClearSelection()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application


SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(ConcentricBraced, 3, 124, 3, 200)

'select all
ret = SapModel.SelectObj.All

'clear selection
ret = SapModel.SelectObj.ClearSelection

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Constraint

## Syntax

SapObject.SapModel.SelectObj.Constraint

## VB6 Procedure

Function Constraint(ByVal Name As String, Optional ByVal DeSelect As Boolean = False) As
Long

## Parameters

Name

The name of an existing joint constraint.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.


## Remarks

This function selects or deselects all point objects to which the specified constraint has been
assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectConstraint()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
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

'select constraint
ret = SapModel.SelectObj.Constraint("Diaph1")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

# CoordinateRange

## Syntax

SapObject.SapModel.SelectObj.CoordinateRange

## VB6 Procedure

Function CoordinateRange(ByVal XMin As Double, ByVal XMax As Double, ByVal YMin As
Double, ByVal YMax As Double, ByVal ZMin As Double, ByVal ZMax As Double, Optional
ByVal DeSelect As Boolean = False, Optional ByVal CSys As String = "Global", Optional ByVal
IncludeIntersections As Boolean = False, Optional ByVal Point As Boolean = True, Optional
ByVal Line As Boolean = True, Optional ByVal Area As Boolean = True, Optional ByVal Solid
As Boolean = True, Optional ByVal Link As Boolean = True) As Long

## Parameters

XMin, XMax

The maximum and minimum X coordinates of the selection box in the specified coordinate
system.

YMin, YMax

The maximum and minimum Y coordinates of the selection box in the specified coordinate
system.

ZMin, ZMax

The maximum and minimum Z coordinates of the selection box in the specified coordinate
system.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

CSys

The name of the coordinate system in which XMin, XMax, YMin, YMax, ZMin and ZMax are
specified.

IncludeIntersections

When this item is True, objects that are inside the box or intersecting the sides and edges of the
box are selected or deselected.

When this item is False, only objects that are fully inside the box are selected or deselected.

Point


Point objects that fall inside the box are only selected or deselected when this item is True.

Line

Line objects that fall inside the box are only selected or deselected when this item is True.

Area

Area objects that fall inside the box are only selected or deselected when this item is True.

Solid

Solid objects that fall inside the box are only selected or deselected when this item is True.

Link

Link objects that fall inside the box are only selected or deselected when this item is True.

## Remarks

This function selects or deselects objects inside the box defined by the XMin, XMax, YMin,
YMax, ZMin and ZMax coordinates.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectCoordinateRange()
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

'select coordinate range
ret = SapModel.SelectObj.CoordinateRange(-100, 100, 0, 0, 100, 200, , , True)

'close Sap
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetSelected

## Syntax

SapObject.SapModel.SelectObj.GetSelected

## VB6 Procedure

Function GetSelected(ByRef NumberItems As Long, ByRef ObjectType() As Long, ByRef
ObjectName() As String) As Long

## Parameters

NumberItems

The number of selected objects.

ObjectType

This is an array that includes the object type of each selected object.

```
1 = Point object
2 = Frame object
3 = Cable object
4 = Tendon object
5 = Area object
6 = Solid object
7 = Link object
```
ObjectName

This is an array that includes the name of each selected object.

## Remarks

This function retrieves a list of selected objects.


The function returns zero if the selection list is successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetSelectedObjects()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim ObjectType() As Long
Dim ObjectName() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'set all point objects selected
ret = SapModel.PointObj.SetSelected("ALL", True, Group)

'set all frame objects selected
ret = SapModel.FrameObj.SetSelected("ALL", True, Group)

'get selected objects
ret = SapModel.SelectObj.GetSelected(NumberItems, ObjectType, ObjectName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also


# Group

## Syntax

SapObject.SapModel.SelectObj.Group

## VB6 Procedure

Function Group(ByVal Name As String, Optional ByVal DeSelect As Boolean = False) As Long

## Parameters

Name

The name of an existing group.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all objects in the specified group.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectGroup()
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


'select group
ret = SapModel.SelectObj.Group("ALL")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# InvertSelection

## Syntax

SapObject.SapModel.SelectObj.InvertSelection

## VB6 Procedure

Function InvertSelection() As Long

## Parameters

None

## Remarks

This function deselects all selected objects and selects all unselected objects; that is, it inverts the
selection.

The function returns zero if the selection is successfully inverted, otherwise it returns nonzero.

## VBA Example

Sub InvertTheSelection()
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

'select objects
ret = SapModel.SelectObj.PlaneXY("2")

'invert the selection
ret = SapModel.SelectObj.InvertSelection

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# LinesParallelToCoordAxis

## Syntax

SapObject.SapModel.SelectObj.LinesParallelToCoordAxis

## VB6 Procedure

Function LinesParallelToCoordAxis(ByRef ParallelTo() As Boolean, Optional ByVal CSys As
String = "Global", Optional ByVal Tolerance As Double = 0.057, Optional ByVal DeSelect As
Boolean = False) As Long

## Parameters

ParallelTo

This is an array of six booleans representing three coordinate axes and three coordinate planes.
Any combination of the six may be specified.


```
ParallelTo(0) = X axis
ParallelTo(1) = Y axis
ParallelTo(2) = Z axis
ParallelTo(3) = XY plane
ParallelTo(4) = XZ plane
ParallelTo(5) = YZ plane
```
CSys

The name of the coordinate system to which the ParallelTo items apply.

Tolerance

Line objects that are within this angle in degrees of being parallel to a specified coordinate axis or
plane are selected or deselected. [deg]

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects objects parallel to specified coordinate axes or planes.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectParallelToAxes()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
Dim ParallelTo() As Boolean

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

'select parallel to axes
ReDim ParallelTo(5)


ParallelTo(2) = True
ret = SapModel.SelectObj.LinesParallelToCoordAxis(ParallelTo)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

LinesParallelToLine

# LinesParallelToLine

## Syntax

SapObject.SapMoel.SelectObj.LinesParallelToLine

## VB6 Procedure

Function LinesParallelToLine(ByVal Name As String, Optional ByVal DeSelect As Boolean =
False) As Long

## Parameters

Name

The name of a line object.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all line objects that are parallel to a specified line object.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example


Sub SelectParallelToLine()
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

'select parallel to line
ret = SapModel.SelectObj.LinesParallelToLine("1")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

LinesParallelToCoordAxis

# PlaneXY

## Syntax

SapObject.SapModel.SelectObj.PlaneXY

## VB6 Procedure

Function PlaneXY(ByVal Name As String, Optional ByVal DeSelect As Boolean = False) As
Long


## Parameters

Name

The name of a point object.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all objects that are in the same XY plane (in the present
coordinate system) as the specified point object.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectPlaneXY()
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

'select in XY plane
ret = SapModel.SelectObj.PlaneXY("3")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.00.

## See Also

PlaneXZ

PlaneYZ

GetPresentCoordSystem

SetPresentCoordSystem

# PlaneXZ

## Syntax

SapObject.SapModel.SelectObj.PlaneXZ

## VB6 Procedure

Function PlaneXZ(ByVal Name As String, Optional ByVal DeSelect As Boolean = False) As
Long

## Parameters

Name

The name of a point object.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all objects that are in the same XZ plane (in the present
coordinate system) as the specified point object.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectPlaneXZ()
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

'select in XZ plane
ret = SapModel.SelectObj.PlaneXZ("3")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

PlaneXY

PlaneYZ

GetPresentCoordSystem

SetPresentCoordSystem

# PlaneYZ

## Syntax

SapObject.SapModel.SelectObj.PlaneYZ

## VB6 Procedure


Function PlaneYZ(ByVal Name As String, Optional ByVal DeSelect As Boolean = False) As
Long

## Parameters

Name

The name of a point object.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all objects that are in the same YZ plane (in the present
coordinate system) as the specified point object.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectPlaneYZ()
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

'select in YZ plane
ret = SapModel.SelectObj.PlaneYZ("3")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.00.

## See Also

PlaneXY

PlaneXZ

GetPresentCoordSystem

SetPresentCoordSystem

# PreviousSelection

## Syntax

SapObject.SapModel.SelectObj.PreviousSelection

## VB6 Procedure

Function PreviousSelection() As Long

## Parameters

None

## Remarks

This function restores the previous selection.

The function returns zero if the selection is successfully restored, otherwise it returns nonzero.

## VBA Example

Sub RestoreSelection()
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

'select objects
ret = SapModel.SelectObj.PlaneXY("2")

'clear selection
ret = SapModel.SelectObj.ClearSelection

'get previous selection
ret = SapModel.SelectObj.PreviousSelection

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# PropertyArea

## Syntax

SapObject.SapModel.SelectObj.PropertyArea

## VB6 Procedure

Function PropertyArea(ByVal Name As String, Optional ByVal DeSelect As Boolean = False) As
Long

## Parameters

Name

The name of an existing area section property.


DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all area objects to which the specified section has been assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectAreaProperty()
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
ret = SapModel.File.NewWall(4, 48, 4, 48)

'select by area property
ret = SapModel.SelectObj.PropertyArea("ASEC1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

PropertyFrame


PropertyCable

PropertyTendon

PropertySolid

PropertyLink

PropertyLinkFD

PropertyMaterial

# PropertyCable

## Syntax

SapObject.SapModel.SelectObj.PropertyCable

## VB6 Procedure

Function PropertyCable(ByVal Name As String, Optional ByVal DeSelect As Boolean = False)
As Long

## Parameters

Name

The name of an existing cable section property.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all cable objects to which the specified section has been
assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectCableProperty()
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 7-001.sdb")

'select by cable property
ret = SapModel.SelectObj.PropertyCable("CAB1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

PropertyFrame

PropertyTendon

PropertyArea

PropertySolid

PropertyLink

PropertyLinkFD

PropertyMaterial

# PropertyFrame

## Syntax

SapObject.SapModel.SelectObj.PropertyFrame


## VB6 Procedure

Function PropertyFrame(ByVal Name As String, Optional ByVal DeSelect As Boolean = False)
As Long

## Parameters

Name

The name of an existing frame section property.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all line objects to which the specified section has been assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectFrameProperty()
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

'select by frame property
ret = SapModel.SelectObj.PropertyFrame("FSEC1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

PropertyCable

PropertyTendon

PropertyArea

PropertySolid

PropertyLink

PropertyLinkFD

PropertyMaterial

# PropertyLink

## Syntax

SapObject.SapModel.SelectObj.PropertyLink

## VB6 Procedure

Function PropertyLink(ByVal Name As String, Optional ByVal DeSelect As Boolean = False) As
Long

## Parameters

Name

The name of an existing link property.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks


This function selects or deselects all link objects to which the specified section property has been
assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectLinkProperty()
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 6-003a.sdb")

'select by link property
ret = SapModel.SelectObj.PropertyLink("GAP1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

PropertyFrame

PropertyCable

PropertyTendon

PropertyArea


PropertySolid

PropertyLinkFD

PropertyMaterial

# PropertyLinkFD

## Syntax

SapObject.SapModel.SelectObj.PropertyLinkFD

## VB6 Procedure

Function PropertyLinkFD(ByVal Name As String, Optional ByVal DeSelect As Boolean = False)
As Long

## Parameters

Name

The name of an existing frequency dependent link property.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all link objects to which the specified frequency dependent link
property has been assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Similar to PropertyFrame

'select by frequency dependent link property
ret = SapModel.SelectObj.PropertyLinkFD("FD1")

## Release Notes

Initial release in version 11.00.


## See Also

PropertyFrame

PropertyCable

PropertyTendon

PropertyArea

PropertySolid

PropertyLink

PropertyMaterial

# PropertyMaterial

## Syntax

SapObject.SapModel.SelectObj.PropertyMaterial

## VB6 Procedure

Function PropertyMaterial(ByVal Name As String, Optional ByVal DeSelect As Boolean = False)
As Long

## Parameters

Name

The name of an existing material property.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all objects to which the specified material property has been
assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example


Sub SelectByMaterial()
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

'select by material property
ret = SapModel.SelectObj.PropertyMaterial("A992Fy50")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

PropertyFrame

PropertyCable

PropertyTendon

PropertyArea

PropertySolid

PropertyLink

PropertyLinkFD


# PropertySolid

## Syntax

SapObject.SapModel.SelectObj.PropertySolid

## VB6 Procedure

Function PropertySolid(ByVal Name As String, Optional ByVal DeSelect As Boolean = False) As
Long

## Parameters

Name

The name of an existing solid property.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all solid objects to which the specified property has been
assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Similar to PropertyFrame

'select by solid property
ret = SapModel.SelectObj.PropertySolid("SOLID1")

## Release Notes

Initial release in version 11.00.

## See Also

PropertyFrame

PropertyCable

PropertyTendon

PropertyArea


PropertyLink

PropertyLinkFD

PropertyMaterial

# PropertyTendon

## Syntax

SapObject.SapModel.SelectObj.PropertyTendon

## VB6 Procedure

Function PropertyTendon(ByVal Name As String, Optional ByVal DeSelect As Boolean = False)
As Long

## Parameters

Name

The name of an existing tendon section property.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

## Remarks

This function selects or deselects all tendon objects to which the specified section has been
assigned.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectTendonProperty()
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 1-009a.sdb")

'select by tendon property
ret = SapModel.SelectObj.PropertyTendon("TEN1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

PropertyFrame

PropertyCable

PropertyArea

PropertySolid

PropertyLink

PropertyLinkFD

PropertyMaterial

# SupportedPoints

## Syntax

SapObject.SapModel.SelectObj.SupportedPoints

## VB6 Procedure


Function SupportedPoints(ByRef DOF() As Boolean, Optional ByVal CSys As String = "Local",
Optional ByVal DeSelect As Boolean = False, Optional ByVal SelectRestraints As Boolean =
True, Optional ByVal SelectJointSprings As Boolean = True, Optional ByVal SelectLineSprings
As Boolean = True, Optional ByVal SelectAreaSprings As Boolean = True, Optional ByVal
SelectSolidSprings As Boolean = True, Optional ByVal SelectOneJointLinks As Boolean = True)
As Long

## Parameters

### DOF

This is an array of six booleans for the six degrees of freedom of a point object.

```
DOF(0) = U1
DOF(1) = U2
DOF(2) = U3
DOF(3) = R1
DOF(4) = R2
DOF(5) = R3
```
CSys

The name of the coordinate system in which degrees of freedom (DOF) are specified. This is
either Local or the name of a defined coordinate system. Local means the point local coordinate
system.

DeSelect

The item is False if objects are to be selected and True if they are to be deselected.

SelectRestraints

If this item is True then points with restraint assignments in one of the specified degrees of
freedom are selected or deselected.

SelectJointSprings

If this item is True then points with joint spring assignments in one of the specified degrees of
freedom are selected or deselected.

SelectLineSprings

If this item is True, points with a contribution from line spring assignments in one of the specified
degrees of freedom are selected or deselected.

SelectAreaSprings

If this item is True, points with a contribution from area spring assignments in one of the specified
degrees of freedom are selected or deselected.

SelectSolidSprings

If this item is True, points with a contribution from solid surface spring assignments in one of the
specified degrees of freedom are selected or deselected.


SelectOneJointLinks

If this item is True, points with one joint link assignments in one of the specified degrees of
freedom are selected or deselected.

## Remarks

This function selects or deselects point objects with support in the specified degrees of freedom.

The function returns zero if the selection is successfully completed, otherwise it returns nonzero.

## VBA Example

Sub SelectSupportedPoints()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
Dim DOF() As Boolean

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

'select supported points
Redim DOF(5)
DOF(2) = True
ret = SapModel.SelectObj.SupportedPoints(DOF)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also


