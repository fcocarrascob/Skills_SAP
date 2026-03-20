# New2DFrame

## Syntax

SapObject.SapModel.File.New2DFrame

## VB6 Procedure

Function New2DFrame(ByVal TempType As e2DFrameType, ByVal NumberStorys As Long,
ByVal StoryHeight As Double, ByVal NumberBays As Long, ByVal BayWidth As Double,
Optional ByVal Restraint As Boolean = True, Optional ByVal Beam As String = "Default",
Optional ByVal Column As String = "Default", Optional ByVal Brace As String = "Default") As
Long

## Parameters

TempType

One of the following 2D frame template types in the e2DFrameType enumeration.

```
PortalFrame = 0
ConcentricBraced = 1
EccentricBraced = 2
```
NumberStorys

The number of stories in the frame.

StoryHeight

The height of each story. [L]

NumberBays

The number of bays in the frame.

BayWidth

The width of each bay. [L]

Restraint

Joint restraints are provided at the base of the frame when this item is True.

Beam

The frame section property used for all beams in the frame. This must either be Default or the
name of a defined frame section property.


Column

The frame section property used for all columns in the frame. This must either be Default or the
name of a defined frame section property.

Brace

The frame section property used for all braces in the frame. This must either be Default or the
name of a defined frame section property. This item does not apply to the portal frame.

## Remarks

Do not use this function to add to an existing model. This function should be used only for
creating a new model and typically would be preceded by calls to ApplicationStart or
InitializeNewModel.

The function returns zero if the new 2D frame model is successfully created, otherwise it returns a
nonzero value.

## VBA Example

Sub New2DFrameModel()
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
ret = SapModel.InitializeNewModel(kip_ft_F)

'create a 2D frame model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 12, 3, 28)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

New3DFrame

NewBeam

NewBlank

NewSolidBlock

NewWall

ApplicationStart

InitializeNewModel

# New3DFrame

## Syntax

SapObject.SapModel.File.New3DFrame

## VB6 Procedure

Function New3DFrame(ByVal TempType As e3DFrameType, ByVal NumberStorys As Long,
ByVal StoryHeight As Double, ByVal NumberBaysX As Long, ByVal BayWidthX As Double,
ByVal NumberBaysY As Long, ByVal BayWidthY As Double, Optional ByVal Restraint As
Boolean = True, Optional ByVal Beam As String = "Default", Optional ByVal Column As String
= "Default", Optional ByVal Area As String = "Default", Optional ByVal NumberXDivisions As
Long = 4, Optional ByVal NumberYDivisions As Long = 4) As Long

## Parameters

TempType

One of the following 3D frame template types in the e3DFrameType enumeration.

```
OpenFrame = 0
PerimeterFrame = 1
BeamSlab = 2
```
```
FlatPlate = 3
```
NumberStorys

The number of stories in the frame.

StoryHeight


The height of each story. [L]

NumberBaysX

The number of bays in the global X direction of the frame.

BayWidthX

The width of each bay in the global X direction of the frame. [L]

NumberBaysY

The number of bays in the global Y direction of the frame.

BayWidthY

The width of each bay in the global Y direction of the frame. [L]

Restraint

Joint restraints are provided at the base of the frame when this item is True.

Beam

The frame section property used for all beams in the frame. This must either be Default or the
name of a defined frame section property.

Column

The frame section property used for all columns in the frame. This must either be Default or the
name of a defined frame section property.

Area

The shell section property used for all floor slabs in the frame. This must either be Default or the
name of a defined shell section property. This item does not apply to the open and perimeter
frames.

NumberXDivisions

The number of divisions for each floor area object in the global X direction. This item does not
apply to the open and perimeter frames.

NumberYDivisions

The number of divisions for each floor area object in the global Y direction. This item does not
apply to the open and perimeter frames.

## Remarks

Do not use this function to add to an existing model. This function should be used only for
creating a new model and typically would be preceded by calls to ApplicationStart or
InitializeNewModel.


The function returns zero if the new 3D frame model is successfully created, otherwise it returns a
nonzero value.

## VBA Example

Sub New3DFrameModel()
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
ret = SapModel.InitializeNewModel(kip_ft_F)

'create a 3D frame model from template
ret = SapModel.File.New3DFrame(BeamSlab, 3, 12, 3, 28, 2, 36)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

NewBeam

NewBlank

New2DFrame

NewSolidBlock

NewWall

ApplicationStart

InitializeNewModel


# NewBeam

## Syntax

SapObject.SapModel.File.NewBeam

## VB6 Procedure

Function NewBeam(ByVal NumberSpans As Long, ByVal SpanLength As Double, Restraint As
Boolean = True, Optional ByVal Beam As String = "Default") As Long

## Parameters

NumberSpans

The number of spans for the beam.

SpanLength

The length of each span. [L]

Restraint

Joint restraints are provided at the ends of each span when this item is True.

Beam

The frame section property used for the beam. This must either be Default or the name of a
defined frame section property.

## Remarks

Do not use this function to add to an existing model. This function should be used only for
creating a new model and typically would be preceded by calls to ApplicationStart or
InitializeNewModel.

The function returns zero if the new beam model is successfully created, otherwise it returns a
nonzero value.

## VBA Example

Sub NewBeam()
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
ret = SapModel.InitializeNewModel(kip_ft_F)

'create a beam from template
ret = SapModel.File.NewBeam(3, 30)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

NewBlank

New2DFrame

New3DFrame

NewSolidBlock

NewWall

ApplicationStart

InitializeNewModel

# NewBlank

## Syntax

SapObject.SapModel.File.NewBlank


## VB6 Procedure

Function NewBlank() As Long

## Parameters

None

## Remarks

Do not use this function to add to an existing model. This function should be used only for
creating a new model and typically would be preceded by calls to ApplicationStart or
InitializeNewModel.

The function returns zero if the new blank model is successfully created, otherwise it returns a
nonzero value.

## VBA Example

Sub NewBlankModel()
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

'create a blank model from template
ret = SapModel.File.NewBlank

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

NewBeam

New2DFrame

New3DFrame

NewSolidBlock

NewWall

ApplicationStart

InitializeNewModel

# NewSolidBlock

## Syntax

SapObject.SapModel.File.NewSolidBlock

## VB6 Procedure

Function NewSolidBlock(ByVal XWidth As Double, ByVal YWidth As Double, ByVal Height
As Double, Optional ByVal Restraint As Boolean = True, Optional ByVal Solid As String =
"Default", Optional ByVal NumberXDivisions As Long = 5, Optional ByVal NumberYDivisions
As Long = 8, Optional ByVal NumberZDivisions As Long = 10) As Long

## Parameters

XWidth

The total width of the solid block measured in the global X direction. [L]

YWidth

The total width of the solid block measured in the global Y direction. [L]

Height

The total height of the solid block measured in the global Z direction. [L]

Restraint

Joint restraints are provided at the base of the solid block when this item is True.

Solid


The solid property used for the solid block. This must either be Default or the name of a defined
solid property.

NumberXDivisions

The number of solid objects in the global X direction of the block.

NumberYDivisions

The number of solid objects in the global Y direction of the block.

NumberZDivisions

The number of solid objects in the global Z direction of the block.

## Remarks

The function returns zero if the new solid block model is successfully created, otherwise it returns
a nonzero value.

## VBA Example

Sub NewSolidBlock()
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
ret = SapModel.InitializeNewModel(kip_ft_F)

'create a solid model from template
ret = SapModel.File.NewSolidBlock(20, 50, 20)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.00.

## See Also

NewBlank

NewBeam

New2DFrame

New3DFrame

NewWall

# NewWall

## Syntax

SapObject.SapModel.File.NewWall

## VB6 Procedure

Function NewWall(ByVal NumberXDivisions As Long, ByVal DivisionWidthX As Double,
ByVal NumberZDivisions As Long, ByVal DivisionWidthZ As Double, Optional ByVal Restraint
As Boolean = True, Optional ByVal Area As String = "Default") As Long

## Parameters

NumberXDivisions

The number of area objects in the global X direction of the wall.

DivisionWidthX

The width of each area object measured in the global X direction. [L]

NumberZDivisions

The number of area objects in the global Z direction of the wall.

DivisionWidthZ

The height of each area object measured in the global Z direction. [L]

Restraint

Joint restraints are provided at the base of the wall when this item is True.

Area


The shell section property used for the wall. This must either be Default or the name of a defined
shell section property.

## Remarks

Do not use this function to add to an existing model. This function should be used only for
creating a new model and typically would be preceded by calls to ApplicationStart or
InitializeNewModel.

The function returns zero if the new wall model is successfully created, otherwise it returns a
nonzero value.

## VBA Example

Sub NewWall()
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
ret = SapModel.InitializeNewModel(kip_ft_F)

'create a wall model from template
ret = SapModel.File.NewWall(6, 4, 6, 4)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

NewBlank

NewBeam


New2DFrame

New3DFrame

NewSolidBlock

ApplicationStart

InitializeNewModel

# OpenFile

## Syntax

SapObject.SapModel.File.OpenFile

## VB6 Procedure

Function OpenFile(ByVal FileName As String) As Long

## Parameters

FileName

```
The full path of a model file to be opened in the Sap2000 application.
```
## Remarks

This function opens an existing Sap2000 file. The file name must have an sdb, $2k, s2k, xlsx, xls,
or mdb extension. Files with sdb extensions are opened as standard Sap2000 files. Files with $2k
and s2k extensions are imported as text files. Files with xlsx and xls extensions are imported as
Microsoft Excel files. Files with mdb extensions are imported as Microsoft Access files.

This function returns zero if the file is successfully opened and nonzero if it is not opened.

The function is only applicable when you are accessing the Sap2000 API from an external
application. It will return an error if you call it from VBA inside Sap2000.

## VBA Example

Sub OpenSDB()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim FileName as String
Dim ret as Long


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\Example 1-019a.sdb"
ret = SapModel.File.OpenFile(FileName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Added reference to xlsx file extension in SAP2000 v15.0.0 and CSiBridge v15.1.0.

## See Also

ApplicationStart

Save

# Save

## Syntax

SapObject.SapModel.File.Save

## VB6 Procedure

Function FileSave(Optional ByVal FileName As String = "") As Long

## Parameters


FileName

```
The full path to which the model file is saved.
```
## Remarks

If a file name is specified, it should have an .sdb extension. If no file name is specified, the file is
saved using its current name.

If there is no current name for the file (the file has not been saved previously) and this function is
called with no file name specified, an error will be returned.

This function returns zero if the file is successfully saved and nonzero if it is not saved.

## VBA Example

Sub SaveSDB()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim FileName as String
Dim ret as Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'start a new template model
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'save SDB file
ret=SapModel.File.Save("C:\SapAPI\x.sdb")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

OpenFile


