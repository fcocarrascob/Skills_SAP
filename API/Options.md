# SetDimensions

## Syntax

SapObject.SapModel.Options.SetDimensions

## VB6 Procedure

Function SetDimensions(Optional ByVal CuttingPlaneTol As Double = 0, Optional ByVal
WorldSpacing As Double = 0, Optional ByVal NudgeValue As Double = 0, Optional ByVal
PixelClickSize As Long = 0, Optional ByVal PixelSnapSize As Long = 0, Optional ByVal
ScrLinThk As Long = 0, Optional ByVal PrtLinThk As Long = 0, Optional ByVal MaxFont As
Long = 0, Optional ByVal MinFont As Long = 0, Optional ByVal ZoomStep As Long = 0,
Optional ByVal ShrinkFact As Long = 0, Optional ByVal TextFileMaxChar As Long = 0) As
Long

## Parameters

CuttingPlaneTol
The tolerance for 2D view cutting planes. [L]
WorldSpacing
The plan fine grid spacing. [L]
NudgeValue
The plan nudge value. [L]
PixelClickSize
The screen selection tolerance in pixels.
PixelSnapSize
The screen snap tolerance in pixels.
ScrLinThk
The screen line thickness in pixels.
PrtLinThk
The printer line thickness in pixels.
MaxFont
The maximum graphic font size in points.
MinFont


The minimum graphic font size in points.
ZoomStep
The auto zoom step size in percent (0 < ZoomStep <= 100).
ShrinkFact
The shrink factor in percent (0 < ShrinkFact <= 100).
TextFileMaxChar
The maximum line length in the text file (ShrinkFact >= 80).

## Remarks

This function sets program dimension and tolerance items. Inputting 0 for any item means that the
item will be ignored by the program; that is, its current value will not be changed.
The function returns zero if the items are successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetDimensionItems()
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
'set dimensions and tolerances
ret = SapModel.Options.SetDimensions(12, 2, 1, 4, , , , , , , , 120)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.03.

## See Also

GetDimensions

# GetDimensions

## Syntax

SapObject.SapModel.Options.GetDimensions

## VB6 Procedure

Function GetDimensions(ByRef CuttingPlaneTol As Double, ByRef WorldSpacing As Double,
ByRef NudgeValue As Double, ByRef PixelClickSize As Long, ByRef PixelSnapSize As Long,
ByRef ScrLinThk As Long, ByRef PrtLinThk As Long, ByRef MaxFont As Long, ByRef
MinFont As Long, ByRef ZoomStep As Long, ByRef ShrinkFact As Long, ByRef
TextFileMaxChar As Long) As Long

## Parameters

CuttingPlaneTol
The tolerance for 2D view cutting planes. [L]
WorldSpacing
The plan fine grid spacing. [L]
NudgeValue
The plan nudge value. [L]
PixelClickSize
The screen selection tolerance in pixels.
PixelSnapSize
The screen snap tolerance in pixels.
ScrLinThk
The screen line thickness in pixels.
PrtLinThk


The printer line thickness in pixels.
MaxFont
The maximum graphic font size in points.
MinFont
The minimum graphic font size in points.
ZoomStep
The auto zoom step size in percent (0 < ZoomStep < = 100).
ShrinkFact
The shrink factor in percent (0 < ShrinkFact < = 100).
TextFileMaxChar
The maximum line length in the text file (ShrinkFact > = 80).

## Remarks

This function retrieves the program dimension and tolerance items.
The function returns zero if the items are successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetDimensionItems()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim CuttingPlaneTol As Double
Dim WorldSpacing As Double
Dim NudgeValue As Double
Dim PixelClickSize As Long
Dim PixelSnapSize As Long
Dim ScrLinThk As Long
Dim PrtLinThk As Long
Dim MaxFont As Long
Dim MinFont As Long
Dim ZoomStep As Long
Dim ShrinkFact As Long
Dim TextFileMaxChar As Long
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application


SapObject.ApplicationStart
'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)
'get dimensions and tolerances
ret = SapModel.Options.GetDimensions(CuttingPlaneTol, WorldSpacing, NudgeValue,
PixelClickSize, PixelSnapSize, ScrLinThk, PrtLinThk, MaxFont, MinFont, ZoomStep,
ShrinkFact, TextFileMaxChar)
'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

SetDimensions

# GetDefaultFunctionFolder

## Syntax

SapObject.SapModel.Options.GetDefaultFunctionFolder

## VB6 Procedure

Function GetDefaultFunctionFolder(ByRef Path As String) As Long

## Parameters

Path
Returned full path to the default function folder.

## Remarks


This function returns the default folder to (recursively) search if a function data file is not found in
the specified path or in the model folder. This is a global setting for the user and applies to all
models.
The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub Example()
Dim myHelper As cHelper
Dim SapModel As cSapModel
Dim SapObject As cOAPI
Dim ret As Long
Dim path As String

'create SapObject
Set myHelper = New Helper
Set SapObject = myHelper.CreateObjectProgID("CSI.SAP2000.API.SapObject")

'start SAP2000 application
ret = SapObject.ApplicationStart()

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel()

'get default function folder
ret = SapModel.Options.GetDefaultFunctionFolder(path)

'close SAP


ret = SapObject.ApplicationExit(False)

'clean up variables
Set SapModel = Nothing
Set SapObject = Nothing
Set myHelper = Nothing
End Sub

## Release Notes

Initial release in version 25.0.

## See Also

SetDefaultFunctionFolder

# SetDefaultFunctionFolder

## Syntax

SapObject.SapModel.Options.SetDefaultFunctionFolder

## VB6 Procedure

Function SetDefaultFunctionFolder(ByRef Path As String) As Long

## Parameters

Path
Full path to the default function folder.

## Remarks

This function sets the default folder to (recursively) search if a function data file is not found in
the specified path or in the model folder. This is a global setting for the user and applies to all
models.
The function returns zero if the data is successfully set; otherwise it returns a nonzero value.


## VBA Example

Sub Example()
Dim myHelper As cHelper
Dim SapModel As cSapModel
Dim SapObject As cOAPI
Dim ret As Long
Dim path As String

'create SapObject
Set myHelper = New Helper
Set SapObject = myHelper.CreateObjectProgID("CSI.SAP2000.API.SapObject")

'start SAP2000 application
ret = SapObject.ApplicationStart()

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel()

'set default function folder
path = "C:\WindTH"
ret = SapModel.Options.SetDefaultFunctionFolder(path)

'close SAP
ret = SapObject.ApplicationExit(False)


'clean up variables
Set SapModel = Nothing
Set SapObject = Nothing
Set myHelper = Nothing
End Sub

## Release Notes

Initial release in version 25.0.

## See Also

GetDefaultFunctionFolder


