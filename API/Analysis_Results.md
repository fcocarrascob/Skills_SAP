# DeselectAllCasesAndCombosForOutput

## Syntax

SapObject.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

## VB6 Procedure

Function DeselectAllCasesAndCombosForOutput() As Long

## Parameters

None

## Remarks

The function deselects all load cases and response combinations for output.

The function returns zero if the cases and combos are successfully deselected, otherwise it returns
a nonzero value.

## VBA Example

Sub DeselectCasesAndCombos()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'deselect all cases and combos
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

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

GetCaseSelectedForOutput

GetComboSelectedForOutput

SetCaseSelectedForOutput

SetComboSelectedForOutput

# GetCaseSelectedForOutput

## Syntax

SapObject.SapModel.Results.Setup.GetCaseSelectedForOutput

## VB6 Procedure

Function GetCaseSelectedForOutput(ByVal Name As String, ByRef Selected As Boolean) As
Long


## Parameters

Name

The name of an existing load case.

Selected

This item is True if the specified load case is selected for output.

## Remarks

This function checks if an load case is selected for output.

The function returns 0 if the selected flag is successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetLoadCaseSelected()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
dim Selected As Boolean

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'check if case is selected
ret = SapModel.Results.Setup.GetCaseSelectedForOutput("DEAD", Selected)

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

DeselectAllCasesAndCombosForOutput

GetComboSelectedForOutput

SetCaseSelectedForOutput

SetComboSelectedForOutput

# GetComboSelectedForOutput

## Syntax

SapObject.SapModel.Results.Setup.GetComboSelectedForOutput

## VB6 Procedure

Function GetComboSelectedForOutput(ByVal Name As String, ByRef Selected As Boolean) As
Long

## Parameters

Name

The name of an existing load combination.

Selected

This item is True if the specified load combination is selected for output.

## Remarks

This function checks if a load combination is selected for output.


The function returns 0 if the selected flag is successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetComboSelected()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Selected As Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 7-002.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis

'check if combo is selected
ret = SapModel.Results.Setup.GetComboSelectedForOutput("COMB1", Selected)

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

DeselectAllCasesAndCombosForOutput

GetCaseSelectedForOutput


SetCaseSelectedForOutput

SetComboSelectedForOutput

# GetOptionBaseReactLoc

## Syntax

SapObject.SapModel.Results.Setup.GetOptionBaseReactLoc

## VB6 Procedure

Function GetOptionBaseReactLoc(ByRef gx As Double, ByRef gy As Double, ByRef gz As
Double) As Long

## Parameters

gx, gy, gz

The global coordinates of the location at which the base reactions are reported.

## Remarks

This function retrieves the global coordinates of the location at which the base reactions are
reported.

The function returns 0 if the coordinates are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetBaseReactLoc()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim gx As Double, gy As Double, gz As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create a SapModel object
Set SapModel = SapObject.SapModel


'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'get base reaction location
ret = SapModel.Results.Setup.GetOptionBaseReactLoc(gx, gy, gz)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetOptionBaseReactLoc

# GetOptionBucklingMode

## Syntax

SapObject.SapModel.Results.Setup.GetOptionBucklingMode

## VB6 Procedure

Function GetOptionBucklingMode(ByRef BuckModeStart As Long, ByRef BuckModeEnd As
Long, ByRef BuckModeAll As Boolean) As Long

## Parameters

BuckModeStart

The first buckling mode for which the buckling factor is reported when the BuckModeAll item is
False.

BuckModeEnd

The last buckling mode for which the buckling factor is reported when the BuckModeAll item is
False.

BuckModeAll


If this item is True, buckling factors are reported for all calculated buckling modes. If it is False,
buckling factors are reported for the buckling modes indicated by the BuckModeStart and
BuckModeEnd items.

## Remarks

This function retrieves the buckling modes for which buckling factors are reported.

The function returns 0 if the modes are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetBucklingModeData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim BuckModeStart As Long
Dim BuckModeEnd As Long
Dim BuckModeAll As Boolean

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

'get buckling mode data
ret = SapModel.Results.Setup.GetOptionBucklingMode(BuckModeStart, BuckModeEnd,
BuckModeAll)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

SetOptionBucklingMode

# GetOptionDirectHist

## Syntax

SapObject.SapModel.Results.Setup.GetOptionDirectHist

## VB6 Procedure

Function GetOptionDirectHist(ByRef Value As Long) As Long

## Parameters

Value

This item is either 1, 2 or 3

```
1 = Envelopes
2 = Step-by-Step
3 = Last Step
```
## Remarks

This function retrieves the output option for direct history results.

The function returns 0 if the output option is successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetDirectHistOutputOption()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value As Long

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

'get output option
ret = SapModel.Results.Setup.GetOptionDirectHist(Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetOptionDirectHist

# GetOptionModalHist

## Syntax

SapObject.SapModel.Results.Setup.GetOptionModalHist

## VB6 Procedure

Function GetOptionModalHist(ByRef Value As Long) As Long

## Parameters

Value

This item is either 1, 2 or 3

```
1 = Envelopes
2 = Step-by-Step
3 = Last Step
```
## Remarks

This function retrieves the output option for modal history results.

The function returns 0 if the output option is successfully retrieved, otherwise it returns nonzero.


## VBA Example

Sub GetModalHistOutputOption()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value As Long

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

'get output option
ret = SapModel.Results.Setup.GetOptionModalHist(Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetOptionModalHist

# GetOptionModeShape

## Syntax

SapObject.SapModel.Results.Setup.GetOptionModeShape


## VB6 Procedure

Function GetOptionModeShape(ByRef ModeShapeStart As Long, ByRef ModeShapeEnd As
Long, ByRef ModeShapesAll As Boolean) As Long

## Parameters

ModeShapeStart

The first mode for which results are reported when the ModeShapesAll item is False.

ModeShapeEnd

The last mode for which results are reported when the ModeShapesAll item is False.

ModeShapesAll

If this item is True, results are reported for all calculated modes. If it is False, results are reported
for the modes indicated by the ModeShapeStart and ModeShapeEnd items.

## Remarks

This function retrieves the modes for which mode shape results are reported.

The function returns 0 if the modes are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetModeShapeData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ModeShapeStart As Long
Dim ModeShapeEnd As Long
Dim ModeShapesAll As Boolean

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


'get buckling mode data
ret = SapModel.Results.Setup.GetOptionModeShape(ModeShapeStart, ModeShapeEnd,
ModeShapesAll)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetOptionModeShape

# GetOptionMultiStepStatic

## Syntax

SapObject.SapModel.Results.Setup.GetOptionMultiStepStatic

## VB6 Procedure

Function GetOptionMultiStepStatic(ByRef Value As Long) As Long

## Parameters

Value

This item is either 1, 2 or 3

```
1 = Envelopes
2 = Step-by-Step
3 = Last Step
```
## Remarks

This function retrieves the output option for multistep static linear results.

The function returns 0 if the output option is successfully retrieved, otherwise it returns nonzero.


## VBA Example

Sub GetMultiStepStaticOutputOption()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value As Long

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

'get output option
ret = SapModel.Results.Setup.GetOptionMultiStepStatic(Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetOptionMultiStepStatic

# GetOptionMultiValuedCombo

## Syntax

SapObject.SapModel.Results.Setup.GetOptionMultiValuedCombo


## VB6 Procedure

Function GetOptionMultiValuedCombo(ByRef Value As Long) As Long

## Parameters

Value

This item is either 1, 2, or 3

```
1 = Envelopes
2 = Multiple values, if possible
3 = Correspondence
```
## Remarks

This function retrieves the output option for multi-valued load combination results.

The function returns 0 if the output option is successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetMultiValuedComboOutputOption()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value As Long

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

'get output option
ret = SapModel.Results.Setup.GetOptionMultiValuedCombo(Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Added option for correspondence in version 16.02.

## See Also

SetOptionMultiValuedCombo

# GetOptionNLStatic

## Syntax

SapObject.SapModel.Results.Setup.GetOptionNLStatic

## VB6 Procedure

Function GetOptionNLStatic(ByRef Value As Long) As Long

## Parameters

Value

This item is either 1, 2 or 3

```
1 = Envelopes
2 = Step-by-Step
3 = Last Step
```
## Remarks

This function retrieves the output option for nonlinear static results.

The function returns 0 if the output option is successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetNonlinearStaticOutputOption()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim Value As Long

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

'get output option
ret = SapModel.Results.Setup.GetOptionNLStatic(Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetOptionNLStatic

# GetOptionPSD

## Syntax

SapObject.SapModel.Results.Setup.GetOptionPSD

## VB6 Procedure

Function GetOptionPSD(ByRef Value As Long) As Long

## Parameters


Value

This item is either 1 or 2

```
1 = RMS
2 = sqrt(PSD)
```
## Remarks

This function retrieves the output option for power spectral density results.

The function returns 0 if the output option is successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetPSDOutputOption()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value As Long

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

'get output option
ret = SapModel.Results.Setup.GetOptionPSD(Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

SetOptionPSD

# GetOptionSteadyState

## Syntax

SapObject.SapModel.Results.Setup.GetOptionSteadyState

## VB6 Procedure

Function GetOptionSteadyState(ByRef Value As Long, ByRef SteadyStateOption As Long) As
Long

## Parameters

Value

This item is either 1 or 2

```
1 = Envelopes
2 = At Frequencies
```
SteadyStateOption

This item is 1, 2 or 3

```
1 = In and Out of Phase
2 = Magnitude
3 = All
```
## Remarks

This function retrieves the output option for steady state results.

The function returns 0 if the output option is successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetSteadyStateOutputOption()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Value As Long
Dim SteadyStateOption As Long


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

'get output option
ret = SapModel.Results.Setup.GetOptionSteadyState(Value, SteadyStateOption)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetOptionSteadyState

# GetSectionCutSelectedForOutput

## Syntax

SapObject.SapModel.Results.Setup.GetSectionCutSelectedForOutput

## VB6 Procedure

Function GetSectionCutSelectedForOutput (ByVal Name As String, ByRef Selected As Boolean)
AsLong

## Parameters

Name

The name of a defined section cut.


Selected

This item is True if the section cut is to be selected for output, or False if the section cut is not
selected for output.

## Remarks

This function retrieves whether a defined section cut is selected for output.

The function returns 0 if the selected flag is successfully retrieved, otherwise it returns nonzero.

Please note that all section cuts are, by default, selected for output when they are created.

## VBA Example

Sub SelectAllSectionCuts()

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
Dim Selected As Boolean
```
```
'create Sap2000 object
```
```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
```
```
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
```
```
ret = SapModel.InitializeNewModel
```
```
'create model from template
```

```
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 288)
```
```
'define new group
```
```
ret = SapModel.GroupDef.SetGroup("Group1")
```
```
'add objects to group
```
```
ret = SapModel.PointObj.SetGroupAssign("1", "Group1")
```
```
ret = SapModel.FrameObj.SetGroupAssign("1", "Group1")
```
```
'define section cut
```
```
ret = SapModel.SectCut.SetByGroup("SCut1", "Group1", 1)
```
```
'Check if the section cut is selected for output
```
```
ret = SapModel.Results.Setup.GetSectionCutSelectedForOutput("SCut1",
Selected)
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

SelectAllSectionCutsForOutput

SetSectionCutSelectedForOutput


# SelectAllSectionCutsForOutput

## Syntax

SapObject.SapModel.Results.Setup.SelectAllSectionCutsForOutput

## VB6 Procedure

Function SelectAllSectionCutsForOutput (Selected as Boolean) AsLong

## Parameters

Selected

This item is True if all section cuts are to be selected for output, or False if no section cuts are to
be selected for output.

## Remarks

This function selects or deselects all section cuts for output.

The function returns 0 if the selected flag is successfully set, otherwise it returns nonzero.

Please note that all section cuts are, by default, selected for output when they are created.

## VBA Example

Sub SelectAllSectionCuts()

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
'create Sap2000 object
```
```
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
```
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 288)
```
'define new group

```
ret = SapModel.GroupDef.SetGroup("Group1")
```
'add objects to group

```
ret = SapModel.PointObj.SetGroupAssign("1", "Group1")
```
```
ret = SapModel.FrameObj.SetGroupAssign("1", "Group1")
```
'define section cut

```
ret = SapModel.SectCut.SetByGroup("SCut1", "Group1", 1)
```
'Deselect all section cuts for output

```
ret = SapModel.Results.Setup.SelectAllSectionCutsForOutput(False)
```
'Select all section cuts for output

```
ret = SapModel.Results.Setup.SelectAllSectionCutsForOutput
(True)
```
'close Sap2000

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

```
GetSectionCutSelectedForOutput
```
```
SetSectionCutSelectedForOutput
```
# SetCaseSelectedForOutput

## Syntax

SapObject.SapModel.Results.Setup.SetCaseSelectedForOutput

## VB6 Procedure

Function SetCaseSelectedForOutput(ByVal Name As String, Optional ByVal Selected As
Boolean = True) As Long

## Parameters

Name

The name of an existing load case.

Selected

This item is True if the specified load case is to be selected for output, otherwise it is False.

## Remarks


This function sets an load case selected for output flag.

The function returns 0 if the selected flag is successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetLoadCaseSelected()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Selected As Boolean

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'deselect all cases and combos
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case selected for output
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

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

DeselectAllCasesAndCombosForOutput

GetCaseSelectedForOutput

GetComboSelectedForOutput

SetComboSelectedForOutput

# SetComboSelectedForOutput

## Syntax

SapObject.SapModel.Results.Setup.SetComboSelectedForOutput

## VB6 Procedure

Function SetComboSelectedForOutput(ByVal Name As String, Optional ByVal Selected As
Boolean = True) As Long

## Parameters

Name

The name of an existing load combination.

Selected

This item is True if the specified load combination is to be selected for output, otherwise it is
False.

## Remarks

This function sets a load combination selected for output flag.

The function returns 0 if the selected flag is successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetComboSelected()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Selected As Boolean

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 7-002.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis

'deselect all cases and combos
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set combo selected for output
ret = SapModel.Results.Setup.SetComboSelectedForOutput("COMB1")

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

DeselectAllCasesAndCombosForOutput

GetCaseSelectedForOutput

GetComboSelectedForOutput

SetCaseSelectedForOutput

# SetOptionBaseReactLoc


## Syntax

SapObject.SapModel.Results.Setup.SetOptionBaseReactLoc

## VB6 Procedure

Function SetOptionBaseReactLoc(ByVal gx As Double, ByVal gy As Double, ByVal gz As
Double) As Long

## Parameters

gx, gy, gz

The global coordinates of the location at which the base reactions are reported.

## Remarks

This function sets the global coordinates of the location at which the base reactions are reported.

The function returns 0 if the coordinates are successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetBaseReactLoc()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim gx As Double, gy As Double, gz As Double

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

'set base reaction location
ret = SapModel.Results.Setup.SetOptionBaseReactLoc(0, 0, 0)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetOptionBaseReactLoc

# SetOptionBucklingMode

## Syntax

SapObject.SapModel.Results.Setup.SetOptionBucklingMode

## VB6 Procedure

Function SetOptionBucklingMode(ByVal BuckModeStart As Long, ByVal BuckModeEnd As
Long, Optional ByVal BuckModeAll As Boolean = False) As Long

## Parameters

BuckModeStart

The first buckling mode for which the buckling factor is reported when the BuckModeAll item is
False.

BuckModeEnd

The last buckling mode for which the buckling factor is reported when the BuckModeAll item is
False.

BuckModeAll

If this item is True, buckling factors are reported for all calculated buckling modes. If it is False,
buckling factors are reported for the buckling modes indicated by the BuckModeStart and
BuckModeEnd items.

## Remarks

This function sets the buckling modes for which buckling factors are reported.

The function returns 0 if the modes are successfully set, otherwise it returns nonzero.


## VBA Example

Sub SetBucklingModeData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim BuckModeStart As Long
Dim BuckModeEnd As Long
Dim BuckModeAll As Boolean

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

'set buckling mode data
ret = SapModel.Results.Setup.SetOptionBucklingMode(1, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetOptionBucklingMode

# SetOptionDirectHist

## Syntax

SapObject.SapModel.Results.Setup.SetOptionDirectHist


## VB6 Procedure

Function SetOptionDirectHist(ByVal Value As Long) As Long

## Parameters

Value

This item is 1, 2 or 3

```
1 = Envelopes
2 = Step-by-Step
3 = Last Step
```
## Remarks

This function sets the output option for direct history results.

The function returns 0 if the output option is successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetDirectHistOutputOption()
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

'set output option
ret = SapModel.Results.Setup.SetOptionDirectHist(1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetOptionDirectHist

# SetOptionModalHist

## Syntax

SapObject.SapModel.Results.Setup.SetOptionModalHist

## VB6 Procedure

Function SetOptionModalHist(ByVal Value As Long) As Long

## Parameters

Value

This item is 1, 2 or 3

```
1 = Envelopes
2 = Step-by-Step
3 = Last Step
```
## Remarks

This function sets the output option for modal history results.

The function returns 0 if the output option is successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetModalHistOutputOption()
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

'set output option
ret = SapModel.Results.Setup.SetOptionModalHist(1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetOptionModalHist

# SetOptionModeShape

## Syntax

SapObject.SapModel.Results.Setup.SetOptionModeShape

## VB6 Procedure

Function SetOptionModeShape(ByVal ModeShapeStart As Long, ByVal ModeShapeEnd As
Long, Optional ByVal ModeShapesAll As Boolean = False) As Long

## Parameters

ModeShapeStart

The first mode for which results are reported when the ModeShapesAll item is False.

ModeShapeEnd


The last mode for which results are reported when the ModeShapesAll item is False.

ModeShapesAll

If this item is True, results are reported for all calculated modes. If it is False, results are reported
for the modes indicated by the ModeShapeStart and ModeShapeEnd items.

## Remarks

This function sets the modes for which mode shape results are reported.

The function returns 0 if the modes are successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetModeShapeData()
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

'set mode shape data
ret = SapModel.Results.Setup.SetOptionModeShape(1, 3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

GetOptionModeShape

# SetOptionMultiStepStatic

## Syntax

SapObject.SapModel.Results.Setup.SetOptionMultiStepStatic

## VB6 Procedure

Function SetOptionMultiStepStatic(ByVal Value As Long) As Long

## Parameters

Value

This item is 1, 2 or 3

```
1 = Envelopes
2 = Step-by-Step
3 = Last Step
```
## Remarks

This function sets the output option for multistep static linear results.

The function returns 0 if the output option is successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetMultiStepStaticOutputOption()
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

'set output option
ret = SapModel.Results.Setup.SetOptionMultiStepStatic(1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetOptionMultiStepStatic

# SetOptionMultiValuedCombo

## Syntax

SapObject.SapModel.Results.Setup.SetOptionMultiValuedCombo

## VB6 Procedure

Function SetOptionMultiValuedCombo(ByVal Value As Long) As Long

## Parameters

Value

This item is either 1, 2, or 3.

```
1 = Envelopes
2 = Multiple values, if possible
3 = Correspondence
```
## Remarks

This function sets the output option for multi-valued load combination results.

The function returns 0 if the output option is successfully set, otherwise it returns nonzero.


## VBA Example

Sub SetMultiValuedComboOutputOption()
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

'set output option
ret = SapModel.Results.Setup.SetOptionMultiValuedCombo(1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Added option for correspondence in version 16.02.

## See Also

GetOptionMultiValuedCombo

# SetOptionNLStatic

## Syntax


SapObject.SapModel.Results.Setup.SetOptionNLStatic

## VB6 Procedure

Function SetOptionNLStatic(ByVal Value As Long) As Long

## Parameters

Value

This item is 1, 2 or 3

```
1 = Envelopes
2 = Step-by-Step
3 = Last Step
```
## Remarks

This function sets the output option for nonlinear static results.

The function returns 0 if the output option is successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetNonlinearStaticOutputOption()
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

'set output option
ret = SapModel.Results.Setup.SetOptionNLStatic(1)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetOptionNLStatic

# SetOptionPSD

## Syntax

SapObject.SapModel.Results.Setup.SetOptionPSD

## VB6 Procedure

Function SetOptionPSD(ByVal Value As Long) As Long

## Parameters

Value

This item is either 1 or 2

```
1 = RMS
2 = sqrt(PSD)
```
## Remarks

This function sets the output option for power spectral density results.

The function returns 0 if the output option is successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetPSDOutputOption()
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

'set output option
ret = SapModel.Results.Setup.SetOptionPSD(1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetOptionPSD

# SetOptionSteadyState

## Syntax

SapObject.SapModel.Results.Setup.SetOptionSteadyState

## VB6 Procedure

Function SetOptionSteadyState(ByVal Value As Long, ByVal SteadyStateOption As Long) As
Long

## Parameters

Value

This item is either 1 or 2

```
1 = Envelopes
```

```
2 = At Frequencies
```
SteadyStateOption

This item is 1, 2 or 3

```
1 = In and Out of Phase
2 = Magnitude
3 = All
```
## Remarks

This function sets the output option for steady state results.

The function returns 0 if the output option is successfully set, otherwise it returns nonzero.

## VBA Example

Sub SetSteadyStateOutputOption()
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

'set output option
ret = SapModel.Results.Setup.SetOptionSteadyState(1, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

GetOptionSteadyState

# SetSectionCutSelectedForOutput

## Syntax

SapObject.SapModel.Results.Setup.SetSectionCutSelectedForOutput

## VB6 Procedure

Function SetSectionCutSelectedForOutput (ByVal Name As String, ByVal Selected As Boolean)
AsLong

## Parameters

Name

The name of a defined section cut.

Selected

This item is True if the section cut is to be selected for output, or False if no section cut should not
be selected for output.

## Remarks

This function selects or deselects a defined section cut for output.

The function returns 0 if the selected flag is successfully set, otherwise it returns nonzero.

Please note that all section cuts are, by default, selected for output when they are created.

## VBA Example

Sub SelectAllSectionCuts()

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
'create Sap2000 object
```

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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 288)
```
'define new group

```
ret = SapModel.GroupDef.SetGroup("Group1")
```
'add objects to group

```
ret = SapModel.PointObj.SetGroupAssign("1", "Group1")
```
```
ret = SapModel.FrameObj.SetGroupAssign("1", "Group1")
```
'define section cut

```
ret = SapModel.SectCut.SetByGroup("SCut1", "Group1", 1)
```
'Deselect section cut for output

```
ret = SapModel.Results.Setup.SetSectionCutSelectedForOutput("SCut1", False)
```
'Select section cut for output


```
ret = SapModel.Results.Setup.SetSectionCutSelectedForOutput
("SCut1", True)
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

```
GetSectionCutSelectedForOutput
```
```
SelectAllSectionCutsForOutput
```
# AreaForceShell

## Syntax

SapObject.Sap2000.Results.AreaForceShell

## VB6 Procedure

Function AreaForceShell(ByVal name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef F11() As Double, ByRef F22() As Double, ByRef F12() As Double, ByRef FMax() As
Double, ByRef FMin() As Double, ByRef FAngle() As Double, ByRef FVM() As Double, ByRef
M11() As Double, ByRef M22() As Double, ByRef M12() As Double, ByRef MMax() As
Double, ByRef MMin() As Double, ByRef MAngle() As Double, ByRef V13() As Double, ByRef
V23() As Double, ByRef VMax() As Double, ByRef VAngle() As Double) As Long


## Parameters

Name

The name of an existing area object, area element or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the area elements corresponding to the area
object specified by the Name item.

If this item is Element, the result request is for the area element specified by the Name item.

If this item is GroupElm, the result request is for the area elements corresponding to all area
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for area elements corresponding to all selected
area objects, and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the area object name associated with each result, if any.

Elm

This is an array that includes the area element name associated with each result.

PointElm

This is an array that includes the name of the point element where the results are reported.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum


This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

F11

The area element internal F11 membrane direct force per length reported in the area element local
coordinate system. [F/L]

F22

The area element internal F22 membrane direct force per length reported in the area element local
coordinate system. [F/L]

F12

The area element internal F12 membrane shear force per length reported in the area element local
coordinate system. [F/L]

FMax

The maximum principal membrane force per length. [F/L]

FMin

The minimum principal membrane force per length. [F/L]

FAngle

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of the maximum principal membrane force. [deg]

FVM

The area element internal Von Mises membrane force per length. [F/L]

M11

The area element internal M11 plate bending moment per length reported in the area element local
coordinate system. This item is only reported for area elements with properties that allow plate
bending behavior. [FL/L]

M22

The area element internal M22 plate bending moment per length reported in the area element local
coordinate system. This item is only reported for area elements with properties that allow plate
bending behavior. [FL/L]

M12

The area element internal M12 plate twisting moment per length reported in the area element local
coordinate system. This item is only reported for area elements with properties that allow plate
bending behavior. [FL/L]

MMax


The maximum principal plate moment per length. This item is only reported for area elements
with properties that allow plate bending behavior. [FL/L]

MMin

The minimum principal plate moment per length. This item is only reported for area elements with
properties that allow plate bending behavior. [FL/L]

MAngle

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of the maximum principal plate moment. This item is only
reported for area elements with properties that allow plate bending behavior. [deg]

V13

The area element internal V13 plate transverse shear force per length reported in the area element
local coordinate system. This item is only reported for area elements with properties that allow
plate bending behavior. [F/L]

V23

The area element internal V23 plate transverse shear force per length reported in the area element
local coordinate system. This item is only reported for area elements with properties that allow
plate bending behavior. [F/L]

VMax

The maximum plate transverse shear force. It is equal to the square root of the sum of the squares
of V13 and V23. This item is only reported for area elements with properties that allow plate
bending behavior. [F/L]

VAngle

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of Vmax. This item is only reported for area elements with
properties that allow plate bending behavior. [deg]

## Remarks

This function reports the area forces for the specified area elements that are assigned shell section
properties (not plane or asolid properties). Note that the forces reported are per unit of in-plane
length.

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetAreaForces()
'dimension variables


Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim F11() As Double
Dim F22() As Double
Dim F12() As Double
Dim FMax() As Double
Dim FMin() As Double
Dim FAngle() As Double
Dim FVM() As Double
Dim M11() As Double
Dim M22() As Double
Dim M12() As Double
Dim MMax() As Double
Dim MMin() As Double
Dim MAngle() As Double
Dim V13() As Double
Dim V23() As Double
Dim VMax() As Double
Dim VAngle() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(6, 48, 6, 48)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")


'get area forces for area object "1"
ret = SapModel.Results.AreaForceShell("1", Object, NumberResults, Obj, Elm, PointElm,
LoadCase, StepType, StepNum, F11, F22, F12, FMax, FMin, FAngle, FVM, M11, M22, M12,
MMax, MMin, MAngle, V13, V23, VMax, VAngle)

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

AreaStressShell

AreaStressShellLayered

AreaJointForcePlane

# AreaJointForcePlane

## Syntax

SapObject.Sap2000.Results.AreaJointForcePlane

## VB6 Procedure

Function AreaJointForcePlane(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm,
ByRef NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm
() As String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As
Double, ByRef F1() As Double, ByRef F2() As Double, ByRef F3() As Double, ByRef M1) As
Double, ByRef M2() As Double, ByRef M3() As Double) As Long

## Parameters

Name

The name of an existing area object, area element or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElm


This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the plane elements corresponding to the area
object specified by the Name item.

If this item is Element, the result request is for the plane element specified by the Name item.

If this item is GroupElm, the result request is for the plane elements corresponding to all area
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for plane elements corresponding to all selected
area objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the area object name associated with each result, if any.

Elm

This is an array that includes the plane element name associated with each result.

PointElm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

F1, F2, F3

These are one dimensional arrays that include the joint force components in the point element
local axes directions. [F]

M1, M2, M3


These are one dimensional arrays that include the joint moment components about the point
element local axes. [FL]

## Remarks

This function reports the area joint forces for the point elements at each corner of the specified
plane elements that have plane-type or asolid-type properties (not shell).

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetPlaneJointForces()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim F1() As Double
Dim F2() As Double
Dim F3() As Double
Dim M1() As Double
Dim M2() As Double
Dim M3() As Double

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

'run analysis
ret = SapModel.Analyze.RunAnalysis


'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MEMBRANE")

'get plane joint forces for area object "1"
ret = SapModel.Results.AreaJointForcePlane("1", ObjectElm, NumberResults, Obj, Elm,
PointElm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3)

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

AreaStressPlane

# AreaJointForceShell

## Syntax

SapObject.Sap2000.Results.AreaJointForceShell

## VB6 Procedure

Function AreaJointForceShell(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm,
ByRef NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm
() As String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As
Double, ByRef F1() As Double, ByRef F2() As Double, ByRef F3() As Double, ByRef M1() As
Double, ByRef M2() As Double, ByRef M3() As Double) As Long

## Parameters

Name

The name of an existing area object, area element or group of objects, depending on the value of
the ItemTypeElm item.


ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the area elements corresponding to the area
object specified by the Name item.

If this item is Element, the result request is for the area element specified by the Name item.

If this item is GroupElm, the result request is for the area elements corresponding to all area
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for area elements corresponding to all selected
area objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the area object name associated with each result, if any.

Elm

This is an array that includes the area element name associated with each result.

PointElm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

F1, F2, F3

These are one dimensional arrays that include the joint force components in the point element
local axes directions. [F]

M1, M2, M3


These are one dimensional arrays that include the joint moment components about the point
element local axes. [FL]

## Remarks

This function reports the area joint forces for the point elements at each corner of the specified
area elements that have shell-type properties (not plane or asolid).

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetAreaJointForceShells()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim F1() As Double
Dim F2() As Double
Dim F3() As Double
Dim M1() As Double
Dim M2() As Double
Dim M3() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(6, 48, 6, 48)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis


'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get area joint forces for area object "1"
ret = SapModel.Results.AreaJointForceShell("1", ObjectElm, NumberResults, Obj, Elm,
PointElm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3)

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

AreaForceShell

AreaStressShell

AreaStressShellLayered

# AreaStrainShell

## Syntax

SapObject.SapModel.Results.AreaStrainShell

## VB6 Procedure

Function AreaStrainShell(ByVal name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef E11Top() As Double, ByRef E22Top() As Double, ByRef G12Top() As Double, ByRef
EMaxTop() As Double, ByRef EMinTop() As Double, ByRef EAngleTop() As Double, ByRef
EVMTop() As Double, ByRef E11Bot() As Double, ByRef E22Bot() As Double, ByRef G12Bot()
As Double, ByRef EMaxBot() As Double, ByRef EMinBot() As Double, ByRef EAngleBot() As
Double, ByRef EVMBot() As Double, ByRef G13Avg() As Double, ByRef G23Avg() As Double,
ByRef GMaxAvg() As Double, ByRef GAngleAvg() As Double) As Long


## Parameters

Name

The name of an existing area object, area element or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the area elements corresponding to the area
object specified by the Name item.

If this item is Element, the result request is for the area element specified by the Name item.

If this item is GroupElm, the result request is for the area elements corresponding to all area
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for area elements corresponding to all selected
area objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the area object name associated with each result, if any.

Elm

This is an array that includes the area element name associated with each result.

PointElm

This is an array that includes the name of the point element where the results are reported.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum


This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

E11Top, E22Top, G12Top, E11Bot, E22Bot, G12Bot

The area element internal E11, E22 and G12 strains, at the top or bottom of the specified area
element, at the specified point element location, reported in the area element local coordinate
system.

EMaxTop, EMinTop, EMaxBot, EMinBot

The area element maximum and minimum principal strains, at the top or bottom of the specified
area element, at the specified point element location.

EAngleTop, EAngleBot

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of the maximum principal strain, at the top or bottom of the
specified area element. [deg]

EVMTop, EVMBot

The area element internal top or bottom Von Mises strain at the specified point element.

G13Avg, G23Avg

The area element average G13 or G23 out-of-plane shear strain at the specified point element.
These items are only reported for area elements with properties that allow plate bending behavior.

GMaxAvg

The area element maximum average out-of-plane shear strain. It is equal to the square root of the
sum of the squares of G13Avg and G23Avg. This item is only reported for area elements with
properties that allow plate bending behavior.

GAngleAvg

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of GMaxAvg. This item is only reported for area elements with
properties that allow plate bending behavior. [deg]

## Remarks

This function reports the area strains for the specified area elements that are assigned shell section
properties (not plane or asolid properties). Strains are reported at each point element associated
with the area element.

The function returns zero if the strains are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.


## VBA Example

Sub GetAreaStrainsShell()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim E11Top() As Double
Dim E22Top() As Double
Dim G12Top() As Double
Dim EMaxTop() As Double
Dim EMinTop() As Double
Dim EAngleTop() As Double
Dim EVMTop() As Double
Dim E11Bot() As Double
Dim E22Bot() As Double
Dim G12Bot() As Double
Dim EMaxBot() As Double
Dim EMinBot() As Double
Dim EAngleBot() As Double
Dim EVMBot() As Double
Dim G13Avg() As Double
Dim G23Avg() As Double
Dim GMaxAvg() As Double
Dim GAngleAvg() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(6, 48, 6, 48)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis


'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get area strains for area object "1"
ret = SapModel.Results.AreaStrainShell("1", Object, NumberResults, Obj, Elm, PointElm,
LoadCase, StepType, StepNum, E11Top, E22Top, G12Top, EMaxTop, EMinTop, EAngleTop,
EVMTop, E11Bot, E22Bot, G12Bot, EMaxBot, EMinBot, EAngleBot, EVMBot, G13Avg,
G23Avg, GMaxAvg, GAngleAvg)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 20.1.0.

## See Also

AreaStrainShellLayered

# AreaStrainShellLayered

## Syntax

SapObject.Sap2000.Results.AreaStrainShellLayered

## VB6 Procedure

Function AreaStrainShellLayered(ByVal name As String, ByVal ItemTypeElm As
eItemTypeElm, ByRef NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String,
ByRef Layer() As String, ByRef IntPtNum() As Long, ByRef IntPtLoc() As Double, ByRef
PointElm() As String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef
StepNum() As Double, ByRef E11() As Double, ByRef E22() As Double, ByRef G12() As
Double, ByRef EMax() As Double, ByRef EMin() As Double, ByRef EAngle() As Double,
ByRef EVM() As Double, ByRef G13Avg() As Double, ByRef G23Avg() As Double, ByRef
GMaxAvg() As Double, ByRef GAngleAvg() As Double) As Long

## Parameters

Name


The name of an existing area object, area element or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the area elements corresponding to the area
object specified by the Name item.

If this item is Element, the result request is for the area element specified by the Name item.

If this item is GroupElm, the result request is for the area elements corresponding to all area
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for area elements corresponding to all selected
area objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the area object name associated with each result, if any.

Elm

This is an array that includes the area element name associated with each result.

Layer

This is an array that includes the layer name associated with each result.

IntPtNum

This is an array that includes the integration point number within the specified layer of the area
element.

IntPtLoc

This is an array that includes the integration point relative location within the specified layer of the
area element. The location is between -1 (bottom of layer) and +1 (top of layer), inclusive. The
midheight of the layer is at a value of 0.

PointElm

This is an array that includes the name of the point element where the results are reported.

LoadCase


This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

E11, E22, G12

The area element internal E11, E22 and G12 strains, at the specified point element location, for
the specified layer and layer integration point, reported in the area element local coordinate
system.

EMax, EMin

The area element maximum and minimum principal strains, at the specified point element
location, for the specified layer and layer integration point.

EAngle

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of the maximum principal strain. [deg]

EVM

The area element internal Von Mises strain at the specified point element location, for the
specified layer and layer integration point.

G13Avg, G23Avg

The area element average G13 or G23 out-of-plane shear strain at the specified point element
location, for the specified layer and layer integration point.

GMaxAvg

The area element maximum average out-of-plane shear strain for the specified layer and layer
integration point. It is equal to the square root of the sum of the squares of G13Avg and G23Avg.

GAngleAvg

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of GMaxAvg. [deg]

## Remarks

This function reports the area strains for the specified area elements that are assigned layered shell
section properties.


The function returns zero if the strains are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Similar to AreaStrainShell

'get area strains for area object "1"
ret = SapModel.Results.AreaStrainShellLayered("1", Object, NumberResults, Obj, Elm,
Layer, IntPtNum, IntPtLoc, PointElm, LoadCase, StepType, StepNum, E11, E22, G12, EMax,
EMin, EAngle, EVM, G13Avg, G23Avg, GMaxAvg, GAngleAvg )

## Release Notes

Initial release in version 20.1.0.

## See Also

AreaStrainShell

# AreaStressPlane

## Syntax

SapObject.Sap2000.Results.AreaStressPlane

## VB6 Procedure

Function AreaStressPlane(ByVal name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef S11() As Double, ByRef S22() As Double, ByRef S33() As Double, ByRef S12() As
Double, ByRef SMax() As Double, ByRef SMin() As Double, ByRef SAngle() As Double, ByRef
SVM() As Double) As Long

## Parameters

Name

The name of an existing area object, area element or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:


```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the plane elements corresponding to the area
object specified by the Name item.

If this item is Element, the result request is for the plane element specified by the Name item.

If this item is GroupElm, the result request is for the plane elements corresponding to all area
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for plane elements corresponding to all selected
area objects, and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the area object name associated with each result, if any.

Elm

This is an array that includes the plane element name associated with each result.

PointElm

This is an array that includes the name of the point element where the results are reported.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

S11, S22, S33, S12

The plane element internal S11, S22, S33 and S12 stresses, at the specified point element location,

reported in the area element local coordinate system. [F/L^2 ]

SMax, SMin

The plane element maximum and minimum principal stresses at the specified point element

location. [F/L^2 ]


SAngle

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
plane element local 1 axis to the direction of the maximum principal stress. [deg]

SVM

The plane element internal Von Mises stress at the specified point element. [F/L^2 ]

## Remarks

This function reports the stresses for the specified plane elements that are assigned plane or asolid
section properties (not shell properties).

The function returns zero if the stresses are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetPlaneStresses()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim S11() As Double
Dim S22() As Double
Dim S33() As Double
Dim S12() As Double
Dim SMax() As Double
Dim SMin() As Double
Dim SAngle() As Double
Dim SVM() As Double

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

'run analysis
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MEMBRANE")

'get plane stresses for area object "1"
ret = SapModel.Results.AreaStressPlane("1", ObjectElm, NumberResults, Obj, Elm,
PointElm, LoadCase, StepType, StepNum, S11, S22, S33, S12, SMax, SMin, SAngle, SVM)

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

AreaJointForcePlane

# AreaStressShell

## Syntax

SapObject.SapModel.Results.AreaStressShell

## VB6 Procedure

Function AreaStressShell(ByVal name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef S11Top() As Double, ByRef S22Top() As Double, ByRef S12Top() As Double, ByRef
SMaxTop() As Double, ByRef SMinTop() As Double, ByRef SAngleTop() As Double, ByRef
SVMTop() As Double, ByRef S11Bot() As Double, ByRef S22Bot() As Double, ByRef S12Bot()


As Double, ByRef SMaxBot() As Double, ByRef SMinBot() As Double, ByRef SAngleBot() As
Double, ByRef SVMBot() As Double, ByRef S13Avg() As Double, ByRef S23Avg() As Double,
ByRef SMaxAvg() As Double, ByRef SAngleAvg() As Double) As Long

## Parameters

Name

The name of an existing area object, area element or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the area elements corresponding to the area
object specified by the Name item.

If this item is Element, the result request is for the area element specified by the Name item.

If this item is GroupElm, the result request is for the area elements corresponding to all area
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for area elements corresponding to all selected
area objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the area object name associated with each result, if any.

Elm

This is an array that includes the area element name associated with each result.

PointElm

This is an array that includes the name of the point element where the results are reported.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.


StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

S11Top, S22Top, S12Top, S11Bot, S22Bot, S12Bot

The area element internal S11, S22 and S12 stresses, at the top or bottom of the specified area
element, at the specified point element location, reported in the area element local coordinate
system. [F/L^2 ]

SMaxTop, SMinTop, SMaxBot, SMinBot

The area element maximum and minimum principal stresses, at the top or bottom of the specified

area element, at the specified point element location. [F/L^2 ]

SAngleTop, SAngleBot

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of the maximum principal stress, at the top or bottom of the
specified area element. [deg]

SVMTop, SVMBot

The area element internal top or bottom Von Mises stress at the specified point element. [F/L^2 ]

S13Avg, S23Avg

The area element average S13 or S23 out-of-plane shear stress at the specified point element.
These items are only reported for area elements with properties that allow plate bending behavior.

[F/L^2 ]

SMaxAvg

The area element maximum average out-of-plane shear stress. It is equal to the square root of the
sum of the squares of S13Avg and S23Avg. This item is only reported for area elements with

properties that allow plate bending behavior. [F/L^2 ]

SAngleAvg

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of SMaxAvg. This item is only reported for area elements with
properties that allow plate bending behavior. [deg]

## Remarks

This function reports the area stresses for the specified area elements that are assigned shell
section properties (not plane or asolid properties). Stresses are reported at each point element
associated with the area element.

The function returns zero if the stresses are successfully recovered, otherwise it returns a nonzero
value.


See Analysis Results Remarks for more information.

## VBA Example

Sub GetAreaStressesShell()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim S11Top() As Double
Dim S22Top() As Double
Dim S12Top() As Double
Dim SMaxTop() As Double
Dim SMinTop() As Double
Dim SAngleTop() As Double
Dim SVMTop() As Double
Dim S11Bot() As Double
Dim S22Bot() As Double
Dim S12Bot() As Double
Dim SMaxBot() As Double
Dim SMinBot() As Double
Dim SAngleBot() As Double
Dim SVMBot() As Double
Dim S13Avg() As Double
Dim S23Avg() As Double
Dim SMaxAvg() As Double
Dim SAngleAvg() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.NewWall(6, 48, 6, 48)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")


ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get area stresses for area object "1"
ret = SapModel.Results.AreaStressShell("1", Object, NumberResults, Obj, Elm, PointElm,
LoadCase, StepType, StepNum, S11Top, S22Top, S12Top, SMaxTop, SMinTop, SAngleTop,
SVMTop, S11Bot, S22Bot, S12Bot, SMaxBot, SMinBot, SAngleBot, SVMBot, S13Avg,
S23Avg, SMaxAvg, SAngleAvg)

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

AreaJointForceShell

AreaStressShellLayered

AreaJointForceShell

# AreaStressShellLayered

## Syntax

SapObject.Sap2000.Results.AreaStressShellLayered

## VB6 Procedure

Function AreaStressShellLayered(ByVal name As String, ByVal ItemTypeElm As
eItemTypeElm, ByRef NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String,
ByRef Layer() As String, ByRef IntPtNum() As Long, ByRef IntPtLoc() As Double, ByRef
PointElm() As String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef
StepNum() As Double, ByRef S11() As Double, ByRef S22() As Double, ByRef S12() As
Double, ByRef SMax() As Double, ByRef SMin() As Double, ByRef SAngle() As Double, ByRef


SVM() As Double, ByRef S13Avg() As Double, ByRef S23Avg() As Double, ByRef SMaxAvg()
As Double, ByRef SAngleAvg() As Double) As Long

## Parameters

Name

The name of an existing area object, area element or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the area elements corresponding to the area
object specified by the Name item.

If this item is Element, the result request is for the area element specified by the Name item.

If this item is GroupElm, the result request is for the area elements corresponding to all area
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for area elements corresponding to all selected
area objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the area object name associated with each result, if any.

Elm

This is an array that includes the area element name associated with each result.

Layer

This is an array that includes the layer name associated with each result.

IntPtNum

This is an array that includes the integration point number within the specified layer of the area
element.

IntPtLoc


This is an array that includes the integration point relative location within the specified layer of the
area element. The location is between -1 (bottom of layer) and +1 (top of layer), inclusive. The
midheight of the layer is at a value of 0.

PointElm

This is an array that includes the name of the point element where the results are reported.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

S11, S22, S12

The area element internal S11, S22 and S12 stresses, at the specified point element location, for
the specified layer and layer integration point, reported in the area element local coordinate
system. [F/L^2 ]

SMax, SMin

The area element maximum and minimum principal stresses, at the specified point element

location, for the specified layer and layer integration point. [F/L^2 ]

SAngle

The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of the maximum principal stress. [deg]

SVM

The area element internal Von Mises stress at the specified point element location, for the

specified layer and layer integration point. [F/L^2 ]

S13Avg, S23Avg

The area element average S13 or S23 out-of-plane shear stress at the specified point element

location, for the specified layer and layer integration point. [F/L^2 ]

SMaxAvg

The area element maximum average out-of-plane shear stress for the specified layer and layer
integration point. It is equal to the square root of the sum of the squares of S13Avg and S23Avg.

[F/L^2 ]

SAngleAvg


The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
area local 1 axis to the direction of SMaxAvg. [deg]

## Remarks

This function reports the area stresses for the specified area elements that are assigned layered
shell section properties.

The function returns zero if the stresses are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Similar to AreaStressShell

'get area stresses for area object "1"
ret = SapModel.Results.AreaStressShellLayered("1", Object, NumberResults, Obj, Elm,
Layer, IntPtNum, IntPtLoc, PointElm, LoadCase, StepType, StepNum, S11, S22, S12, SMax,
SMin, SAngle, SVM, S13Avg, S23Avg, SMaxAvg, SAngleAvg)

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

AreaForceShell

AreaStressShell

AreaJointForceShell

# AssembledJointMass_1

## Syntax

SapObject.SapModel.Results.AssembledJointMass_1

## VB6 Procedure

Function AssembledJointMass_1(ByVal MassSourceName As String, ByVal Name As String,
ByVal ItemTypeElm As eItemTypeElm, ByRef PointElm() As String, ByRef MassSource() As


String, ByRef U1() As Double, ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As
Double, ByRef R2() As Double, ByRef R3() As Double) As Long

## Parameters

MassSource Name

The name of an existing mass source definition. If this value is left empty or unrecognized, data
for all mass sources will be returned.

Name

The name of an existing point element or group of objects, depending on the value of the
ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.

If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Type for Elements for more information.

NumberResults

The total number of results returned by the program.

PointElm

This is an array that includes the point element name associated with each result.

Mass Source

This is an array that includes the mass source name associated with each result.

U1, U2, U3

These are one dimensional arrays that include the translational mass in the point element local 1, 2
and 3 axes directions, respectively, for each result. [M]


### R1, R2, R3

These are one dimensional arrays that include the rotational mass moment of inertia about the

point element local 1, 2 and 3 axes, respectively, for each result. [ML^2 ]

## Remarks

This function reports the assembled joint masses for the specified point elements.

The function returns zero if the masses are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetAssembledJointMass()

'dimension variables

Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim PointElm() As String
Dim MassSource() As String
Dim U1() As Double
Dim U2() As Double
Dim U3() As Double
Dim R1() As Double
Dim R2() As Double
Dim R3() As Double
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'add new mass source andmake it the default mass source


LoadPat(0)="DEAD"

SF(0)=1.25

ret=SapModel.SourceMass.SetMassSource("MyMassSource", True, True, True, True, 1,
LoadPat, SF)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'get assembled joint mass for all point elements
ret = SapModel.Results.AssembledJointMass_1("","ALL", GroupElm, NumberResults,
PointElm, MassSource, U1, U2, U3, R1, R2, R3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v19.1.0.

This function supersedes AssembledJointMass

## See Also

# BaseReact

## Syntax

SapObject.SapModel.Results.BaseReact

## VB6 Procedure

Function BaseReact(ByRef NumberResults As Long, ByRef LoadCase() As String, ByRef
StepType() As String, ByRef StepNum() As Double, ByRef Fx() As Double, ByRef Fy() As
Double, ByRef Fz() As Double, ByRef Mx() As Double, ByRef My() As Double, ByRef Mz() As
Double, ByRef gx as Double, ByRef gy as Double, ByRef gz as Double) As Long

## Parameters

NumberResults

The total number of results returned by the program.


LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

Fx, Fy, Fz

These are one dimensional arrays that include the base reaction forces in the global X, Y and Z
directions, respectively, for each result. [F]

Mx, My, Mz

These are one dimensional arrays that include the base reaction moments about the global X, Y
and Z axes, respectively, for each result. [FL]

gx, gy, gz

These are the global X, Y and Z coordinates of the point at which the base reactions are reported.
[L]

## Remarks

This function reports the structure total base reactions.

The function returns zero if the reactions are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for additional information.

## VBA Example

Sub GetBaseReactions()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim Fx() As Double
Dim Fy() As Double
Dim Fz() As Double


Dim Mx() As Double
Dim My() As Double
Dim Mz() As Double
Dim gx As Double
Dim gy As Double
Dim gz As Double

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get base reactions
ret = SapModel.Results.BaseReact(NumberResults, LoadCase, StepType, StepNum, Fx, Fy,
Fz, Mx, My, Mz, gx, gy, gz)

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


BaseReactWithCentroid

GetJointReact

# BaseReactWithCentroid

## Syntax

SapObject.SapModel.Results.BaseReactWithCentroid

## VB6 Procedure

Function BaseReactWithCentroid(ByRef NumberResults As Long, ByRef LoadCase() As String,
ByRef StepType() As String, ByRef StepNum() As Double, ByRef Fx() As Double, ByRef Fy()
As Double, ByRef Fz() As Double, ByRef Mx() As Double, ByRef My() As Double, ByRef Mz()
As Double, ByRef gx as Double, ByRef gy as Double, ByRef gz as Double, ByRef
XCentroidForFX() as Double, ByRef YCentroidForFX() as Double, ByRef ZCentroidForFX() as
Double, ByRef XCentroidForFY() as Double, ByRef YCentroidForFY() as Double, ByRef
ZCentroidForFY() as Double, ByRef XCentroidForFZ() as Double, ByRef YCentroidForFZ() as
Double, ByRef ZCentroidForFZ() as Double) As Long

## Parameters

NumberResults

The total number of results returned by the program.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

Fx, Fy, Fz

These are one dimensional arrays that include the base reaction forces in the global X, Y and Z
directions, respectively, for each result. [F]

Mx, My, Mz

These are one dimensional arrays that include the base reaction moments about the global X, Y
and Z axes, respectively, for each result. [FL]


gx, gy, gz

These are the global X, Y and Z coordinates of the point at which the base reactions are reported.
[L]

XCentroidForFx, YCentroidForFx, ZCentroidForFx

These are arrays of the global X, Y and Z coordinates, respectively, of the centroid of all global X-
direction translational reaction forces for each result. See Base Reaction Centroids for more
information. [L]

XCentroidForFy, YCentroidForFy, ZCentroidForFy

These are arrays of the global X, Y and Z coordinates, respectively, of the centroid of all global Y-
direction translational reaction forces for each result. See Base Reaction Centroids for more
information. [L]

XCentroidForFz, YCentroidForFz, ZCentroidForFz

These are arrays of the global X, Y and Z coordinates, respectively, of the centroid of all global Z-
direction translational reaction forces for each result. See Base Reaction Centroids for more
information. [L]

## Remarks

This function reports the structure total base reactions and includes information on the centroid of
the translational reaction forces.

The function returns zero if the reactions are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

Note that the reported base reaction centroids are not the same as the centroid of the applied loads.
See Base Reaction Centroids for additional information.

## VBA Example

Sub GetBaseReactionsWithCentroids()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim Fx() As Double
Dim Fy() As Double
Dim Fz() As Double
Dim Mx() As Double
Dim My() As Double


Dim Mz() As Double
Dim gx As Double
Dim gy As Double
Dim gz As Double
Dim XCentroidForFx() As Double
Dim YCentroidForFx() As Double
Dim ZCentroidForFx() As Double
Dim XCentroidForFy() As Double
Dim YCentroidForFy() As Double
Dim ZCentroidForFy() As Double
Dim XCentroidForFz() As Double
Dim YCentroidForFz() As Double
Dim ZCentroidForFz() As Double

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get base reactions with centroids
ret = SapModel.Results.BaseReactWithCentroid(NumberResults, LoadCase, StepType,
StepNum, Fx, Fy, Fz, Mx, My, Mz, gx, gy, gz, XCentroidForFx, YCentroidForFx,
ZCentroidForFx, XCentroidForFy, YCentroidForFy, ZCentroidForFy, XCentroidForFz,
YCentroidForFz, ZCentroidForFz)

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

BaseReact

JointReact

# BridgeSuperCutLongitStress

## Syntax

SapObject.SapModel.Results.BridgeSuperCutLongitStress

## VB6 Procedure

Function BridgeSuperCutLongitStress(ByVal Name As String, ByVal CutIndex As Long, ByVal
PointIndex As Long, ByRef NumberResults As Long, ByRef LoadCase() As String, ByRef
StepType() As String, ByRef StepNum() As Double, ByRef Stress() As Double) As Long

## Parameters

Name

The name of an existing bridge object.

CutIndex

The index number of section cut in this bridge object. This must be from 0 to Count-1, where
Count is the value returned by function SapModel.BridgeObj.CountSuperCut.

PointIndex

The index number of the stress point in this section cut in this bridge object. This must be from 0
to Count-1, where Count is the value returned by function
SapModel.BridgeObj.CountSuperCutStressPoint.

NumberResults

The total number of results returned.

LoadCase

This is an array that includes the name of the load case or load combination associated with each
result.


StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

Stress

This is an array that includes the longitudinal stress value for each result. [F/L^2 ]

## Remarks

This function returns the longitudinal stresses for multiple cases/combos at a single stress point in
a superstructure section cut in a bridge object. Use the functions in SapModel.Results.Setup to
control the loads and steps for which results are to be obtained.

The function returns zero if the information is successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

This example assumes that a file MyBridge.sdb exists and has a linked bridge object named
BOBJ1 in it. It also assumes a load case named DEAD exists in the model.

Sub GetBridgeSuperCutLongitStress()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim StepType() As String
Dim StepNum() As Double
Dim Stress() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyBridge.sdb"
ret = SapModel.File.OpenFile(FileName)


'run analysis
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get bridge section cut results
ret = SapModel.Results.BridgeSuperCutLongitStress("BOBJ1", 1, 1, NumberResults,
LoadCase, StepType, StepNum, Stress)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

# BucklingFactor

## Syntax

SapObject.SapModel.Results.BucklingFactor

## VB6 Procedure

Function BucklingFactor(ByRef NumberResults As Long, ByRef LoadCase() As String, ByRef
StepType() As String, ByRef stepnum() As Double, ByRef Factor() As Double) As Long

## Parameters

NumberResults

The total number of results returned by the program.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType


This is an array that includes the step type for each result. For buckling factors, the step type is
always Mode. See Analysis Results Step Type.

StepNum

This is an array that includes the step number for each result. For buckling factors, the step
number is always the buckling mode number. See Analysis Results Step Number.

Factor

This is an array that includes the buckling factors.

## Remarks

This function reports buckling factors obtained from buckling load cases.

The function returns zero if the factors are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetBucklingFactors()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim Factor() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 1-019a.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis


'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("BUCK1")

'get buckling factors
ret = SapModel.Results.BucklingFactor(NumberResults, LoadCase, StepType, StepNum,
Factor)

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

# FrameForce

## Syntax

SapObject.SapModel.Results.FrameForce

## VB6 Procedure

Function FrameForce(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef ObjSta() As Double, ByRef Elm() As
String, ByRef ElmSta() As Double, ByRef LoadCase() As String, ByRef StepType() As String,
ByRef StepNum() As Double, ByRef P() As Double, ByRef V2() As Double, ByRef V3() As
Double, ByRef T() As Double, ByRef M2() As Double, ByRef M3() As Double) As Long

## Parameters

Name

The name of an existing line object, line element or group of objects depending on the value of the
ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:


```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the line elements corresponding to the line object
specified by the Name item.

If this item is Element, the result request is for the line element specified by the Name item.

If this item is GroupElm, the result request is for the line elements corresponding to all line objects
included in the group specified by the Name item.

If this item is SelectionElm, the result request is for line elements corresponding to all selected
line objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the line object name associated with each result, if any.

ObjSta

This is an array that includes the distance measured from the I-end of the line object to the result
location.

Elm

This is an array that includes the line element name associated with each result.

ElmSta

This is an array that includes the distance measured from the I-end of the line element to the result
location.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

P, V2, V3

These are one dimensional arrays that include the axial force, shear force in the local 2 direction,
and shear force in the local 3 direction, respectively, for each result. [F]


### T, M2, M3

These are one dimensional arrays that include the torsion, moment about the local 2axis, and
moment about the local 3-axis, respectively, for each result. [FL]

## Remarks

This function reports the frame forces for the specified line elements.

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for additional information.

## VBA Example

Sub GetFrameForces()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim ObjSta() As Double
Dim Elm() As String
Dim ElmSta() As Double
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim P() As Double
Dim V2() As Double
Dim V3() As Double
Dim T() As Double
Dim M2() As Double
Dim M3() As Double

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

'run analysis


ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get frame forces for line object "1"
ret = SapModel.Results.FrameForce("1", Object, NumberResults, Obj, ObjSta, Elm, ElmSta,
LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3)

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

FrameJointForce

# FrameJointForce

## Syntax

SapObject.SapModel.Results.FrameJointForce

## VB6 Procedure

Function FrameForce(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef F1() As Double, ByRef F2() As Double, ByRef F3() As Double, ByRef M1() As Double,
ByRef M2() As Double, ByRef M3() As Double) As Long

## Parameters

Name


The name of an existing line object, line element or group of objects depending on the value of the
ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the line elements corresponding to the line object
specified by the Name item.

If this item is Element, the result request is for the line element specified by the Name item.

If this item is GroupElm, the result request is for the line elements corresponding to all line objects
included in the group specified by the Name item.

If this item is SelectionElm, the result request is for line elements corresponding to all selected
line objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the line object name associated with each result, if any.

Elm

This is an array that includes the line element name associated with each result.

PointElm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

F1, F2, F3


These are one dimensional arrays that include the joint force components in the point element
local axes directions. [F]

M1, M2, M3

These are one dimensional arrays that include the joint moment components about the point
element local axes. [FL]

## Remarks

This function reports the frame joint forces for the point elements at each end of the specified line
elements.

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for additional information.

## VBA Example

Sub GetFrameJointForces()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim F1() As Double
Dim F2() As Double
Dim F3() As Double
Dim M1() As Double
Dim M2() As Double
Dim M3() As Double

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get frame joint forces for line object "1"
ret = SapModel.Results.FrameJointForce("1", ObjectElm, NumberResults, Obj, Elm,
PointElm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3)

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

FrameForce

# GeneralizedDispl

## Syntax

SapObject.SapModel.Results.GeneralizedDispl

## VB6 Procedure

Function GeneralizedDispl(ByVal Name As String, ByRef NumberResults As Long, ByRef GD()
As String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As
Double, ByRef DType() As String, ByRef Value() As Double) As Long

## Parameters

Name


The name of an existing generalized displacement for which results are returned. If the program
does not recognize this name as a defined generalized displacement, it returns results for all
selected generalized displacements, if any. For example, entering a blank string (i.e., "") for the
name will prompt the program to return results for all selected generalized displacements.

NumberResults

The total number of results returned by the program.

GD

This is an array that includes the generalized displacement name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

DType

This is an array that includes the generalized displacement type for each result. It is either
Translation or Rotation.

Value

This is an array of the generalized displacement values for each result.[L] when DType is
Translation , [rad] when DType is Rotation.

## Remarks

This function reports the displacement values for the specified generalized displacements.

The function returns zero if the displacements are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetGeneralizedDisplacements()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim NumberResults As Long
Dim GD() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim DType() As String
Dim Value() As Double
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'add generalized displacement
ret = SapModel.GDispl.Add("GD1", 1)

'add point to generalized displacement
ReDim SF(5)
SF(0) = 0.5
ret = SapModel.GDispl.SetPoint("GD1", "3", SF)

'get generalized displacement results
ret = SapModel.Results.GeneralizedDispl("GD1",NumberResults, GD, LoadCase, StepType,
StepNum, DType, Value)

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

JointDispl

JointDisplAbs

# JointAcc

## Syntax

SapObject.SapModel.Results.JointAcc

## VB6 Procedure

Function JointAcc(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,
ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects, depending on the value
of the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.


If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Item Type for Elements for more information.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For those cases, this item will be blank.

Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

U1, U2, U3

These are one dimensional arrays that include the translational acceleration in the point element

local 1, 2 and 3 axes directions, respectively, for each result. [L/s^2 ]

R1, R2, R3

These are one dimensional arrays that include the rotational acceleration about the point element

local 1, 2 and 3 axes, respectively, for each result. [rad/s^2 ]

## Remarks

This function reports the joint accelerations for the specified point elements. The accelerations
reported by this function are relative accelerations.

The function returns zero if the accelerations are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for additional information.


## VBA Example

Sub GetJointAcceleration()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 1-022.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MHIST1")

'set modal history output option to step-by-step
ret = SapModel.Results.Setup.SetOptionModalHist(2)

'get joint acceleration for point object "22"
ret = SapModel.Results.JointAcc("22", ObjectElm, NumberResults, Obj, Elm, LoadCase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

JointDispl

JointDisplAbs

JointVel

JointVelAbs

JointAccAbs

GeneralizedDispl

# JointAccAbs

## Syntax

SapObject.SapModel.Results.JointAccAbs

## VB6 Procedure

Function JointAccAbs(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,
ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElm


This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.

If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Item Type for Elements for more information.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For those cases, this item will be blank.

Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

U1, U2, U3

These are one dimensional arrays that include the translational acceleration in the point element
local 1, 2 and 3 axes directions, respectively, for each result. [L/s^2 ]

R1, R2, R3


These are one dimensional arrays that include the rotational acceleration about the point element
local 1, 2 and 3 axes, respectively, for each result. [rad/s^2 ]

## Remarks

This function reports the joint absolute accelerations for the specified point elements. Absolute
and relative accelerations are the same, except when reported for time history load cases subjected
to acceleration loading.

The function returns zero if the accelerations are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetJointAbsoluteAcceleration()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 1-022.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis


'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MHIST1")

'set modal history output option to step-by-step
ret = SapModel.Results.Setup.SetOptionModalHist(2)

'get joint absolute acceleration for point object "22"
ret = SapModel.Results.JointAccAbs("22", ObjectElm, NumberResults, Obj, Elm, LoadCase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

JointDispl

JointDisplAbs

JointVel

JointVelAbs

JointAcc

GeneralizedDispl

# JointDispl

## Syntax

SapObject.SapModel.Results.JointDispl

## VB6 Procedure


Function JointDispl(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,
ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.

If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Item Type for Elements for more information.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For these cases this item will be blank.

Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType


This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

U1, U2, U3

These are one dimensional arrays that include the displacement in the point element local 1, 2 and
3 axes directions, respectively, for each result. [L]

R1, R2, R3

These are one dimensional arrays that include the rotation about the point element local 1, 2 and 3
axes, respectively, for each result. [rad]

## Remarks

This function reports the joint displacements for the specified point elements. The displacements
reported by this function are relative displacements.

The function returns zero if the displacements are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetJointDisplacements()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get point displacements
ret = SapModel.Results.JointDispl("ALL", GroupElm, NumberResults, Obj, Elm, LoadCase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

JointDisplAbs

JointVel

JointVelAbs

JointAcc

JointAccAbs

GeneralizedDispl


# JointDisplAbs

## Syntax

SapObject.SapModel.Results.JointDisplAbs

## VB6 Procedure

Function JointDisplAbs(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,
ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.

If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Item Type for Elements for more information.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For those cases, this item will be blank.


Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

U1, U2, U3

These are one dimensional arrays that include the displacement in the point element local 1, 2 and
3 axes directions, respectively, for each result. [L]

R1, R2, R3

These are one dimensional arrays that include the rotation about the point element local 1, 2 and 3
axes, respectively, for each result. [rad]

## Remarks

This function reports the absolute joint displacements for the specified point elements. Absolute
and relative displacements are the same except when reported for time history load cases subjected
to acceleration loading.

The function returns zero if the displacements are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetJointAbsoluteDisplacement()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 1-022.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MHIST1")

'set modal history output option to step-by-step
ret = SapModel.Results.Setup.SetOptionModalHist(2)

'get joint absolute displacement for point object "22"
ret = SapModel.Results.JointDisplAbs("22", ObjectElm, NumberResults, Obj, Elm, LoadCase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

JointDispl

JointVel

JointVelAbs

JointAcc

JointAccAbs

GeneralizedDispl

# JointReact

## Syntax

SapObject.SapModel.Results.JointReact

## VB6 Procedure

Function JointReact(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef F1() As Double, ByRef
F2() As Double, ByRef F3() As Double, ByRef M1() As Double, ByRef M2() As Double, ByRef
M3() As Double) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElmc = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.


If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Item Type for Elements for more information.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For those cases, this item will be blank.

Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

F1, F2, F3

These are one dimensional arrays that include the reaction forces in the point element local 1, 2
and 3 axes directions, respectively, for each result. [F]

M1, M2, M3

These are one dimensional arrays that include the reaction moments about the point element local
1, 2 and 3 axes, respectively, for each result. [FL]

## Remarks

This function reports the joint reactions for the specified point elements. The reactions reported
are from restraints, springs and grounded (one-joint) links.

The function returns zero if the reactions are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.


## VBA Example

Sub GetJointReactions()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim F1() As Double
Dim F2() As Double
Dim F3() As Double
Dim M1() As Double
Dim M2() As Double
Dim M3() As Double

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get joint reactions
ret = SapModel.Results.JointReact("1", Element, NumberResults, Obj, Elm, LoadCase,
StepType, StepNum, F1, F2, F3, M1, M2, M3)

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

BaseReact

# JointRespSpec

## Syntax

SapObject.SapModel.Results.JointRespSpec

## VB6 Procedure

Function JointRespSpec(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByVal
edSet As String, ByRef NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String,
ByRef LoadCase() As String, ByRef CoordSys() As String, ByRef Dir() As Long, ByRef
Damping() As Double, ByRef SpecWidening() As Double, ByRef AbscissaValue() As Double,
ByRef OrdinateValue() As Double) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElem

This is one of the following items in the ItemTypeElm enumeration:

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
```
Default = 4
```

If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.

If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

If this item is Default, the result request is for the point object specified in the named set.

See Item Type for Elements for more information.

NamedSet

The name of an existing joint response spectrum named set. See
SapModel.NamedSet.SetJointRespSpec.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For those cases, this item will be blank.

Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the load case associated with each result.

CoordSys

This is an array that includes the coordinate system in which the results are reported.

Dir

This is an array that includes the direction for which the results are reported. Valid values for the
direction are:

```
1 = Local 1, Global X, or user-defined coordinate system X
```
```
2 = Local 2, Global Y, or user-defined coordinate system Y
```
```
3 = Local 3, Global Z, or user-defined coordinate system Z
```
Damping

This is an array that includes the critical damping ratio, for each result.


SpecWidening

This is an array that includes the percent spectrum widening, for each result.

AbscissaValue

This is an array that includes the period or frequency, as defined in each named set, for each
result. [s or 1/s]

OrdinateValue

This is an array of the response quantity, as defined in each named set, for each result. The
possible response quantities are spectral displacement [L], spectral velocity [L/s], pseudo spectral

velocity [L/s], spectral acceleration [L/s^2 ], or pseudo spectral acceleration [L/s^2 ].

## Remarks

This function reports the joint response spectra values, due to a time history analysis, for the
specified point elements.

The function returns zero if the response spectra data is successfully recovered, otherwise it
returns a nonzero value.

See Analysis Results Remarks for more information

## VBA Example

Sub GetJointResponseSpectra()
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

Dim Joints() As String

Dim UserFreq() As Double

Dim DampValues() As Double


Dim NumberResults As Long

Dim Obj() As String

Dim Elm() As String

Dim LoadCase() As String

Dim CoordSys() As String

Dim Dir() As Long

Dim Damping() As Double

Dim SpecWidening() As Double

Dim AbscissaValue() As Double

Dim OrdinateValue() As Double

'create Sap2000 object
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
ret = SapModel.Func.FuncTH.SetSine("TH-1, 1, 16, 4, 1.25)

'add linear modal history load case
ReDim MyLoadType(0)
ReDim MyLoadName(0)
ReDim MyFunc(0)
ReDim MySF(0)
ReDim MyTF(0)
ReDim MyAT(0)
ReDim MyCSys(0)
ReDim MyAng(0)
MyLoadType(0) = "Accel"
MyLoadName(0) = "U1"
MyFunc(0) = "TH-1"
MySF(0) = 2
MyTF(0) = 1.5


MyAT(0) = 10
MyCSys(0) = "Global"
MyAng(0) = 10

ret = SapModel.LoadCases.ModHistLinear.SetCase("LCASE1")

ret = SapModel.LoadCases.ModHistLinear.SetLoads("LCASE1", 1, MyLoadType,
MyLoadName, MyFunc, MySF, MyTF, MyAT, MyCSys, MyAng)

'define named set
ReDim Joints(1)
Joints(0) = "3"
Joints(1) = "6"
ReDim DampValues(1)
DampValues(0) = 0
DampValues(1) = 0.05

ret = SapModel.NamedSets.SetJointRespSpec("Sample", "LCASE1", 2, Joints, "Global", 1, 1,
4, True, True, 0, UserFreq, 2, DampValues)

'run analysis

ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections and select time history case
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("LCASE1")

'get point response spectra

ret = SapModel.Results.JointRespSpec("3", 4, "Sample", NumberResults, Obj, Elm,
LoadCase, CoordSys, Dir, Damping, SpecWidening, AbscissaValue, OrdinateValue)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.3.0.


## See Also

SetJointRespSpec

JointDisplAbs

JointVel

JointVelAbs

JointAcc

JointAccAbs

GeneralizedDispl

# JointVel

## Syntax

SapObject.SapModel.Results.JointVel

## VB6 Procedure

Function GJointVel(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,
ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.


If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Item Type for Elements for more information.

NumberResults

The number total of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For those cases, this item will be blank.

Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

U1, U2, U3

These are one dimensional arrays that include the translational velocity in the point element local
1, 2 and 3 axes directions, respectively, for each result. [L/s]

R1, R2, R3

These are one dimensional arrays that include the rotational velocity about the point element local
1, 2 and 3 axes, respectively, for each result. [rad/s]

## Remarks

This function reports the joint velocities for the specified point elements. The velocities reported
by this function are relative velocities.

The function returns zero if the velocities are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.


## VBA Example

Sub GetJointVelocity()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 1-022.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MHIST1")

'set modal history output option to step-by-step
ret = SapModel.Results.Setup.SetOptionModalHist(2)

'get joint velocity for point object "22"
ret = SapModel.Results.JointVel("22", ObjectElm, NumberResults, Obj, Elm, LoadCase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

JointDispl

JointDisplAbs

JointVelAbs

JointAcc

JointAccAbs

GeneralizedDispl

# JointVelAbs

## Syntax

SapObject.SapModel.Results.JointVelAbs

## VB6 Procedure

Function JointVelAbs(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,
ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long

## Parameters

Name

The name of an existing point object, point element, or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElm


This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.

If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Item Type for Elements for more information.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For those cases, this item will be blank.

Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

U1, U2, U3

These are one dimensional arrays that include the translational velocity in the point element local
1, 2 and 3 axes directions, respectively, for each result. [L/s]

R1, R2, R3

These are one dimensional arrays that include the rotational velocity about the point element local
1, 2 and 3 axes, respectively, for each result. [rad/s]


## Remarks

This function reports the joint absolute velocities for the specified point elements. Absolute and
relative velocities are the same, except when reported for time history load cases subjected to
acceleration loading.

The function returns zero if the velocities are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetJointAbsoluteVelocity()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 1-022.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput


'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MHIST1")

'set modal history output option to step-by-step
ret = SapModel.Results.Setup.SetOptionModalHist(2)

'get joint absolute velocity for point object "22"
ret = SapModel.Results.JointVelAbs("22", ObjectElm, NumberResults, Obj, Elm, LoadCase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

JointDispl

JointDisplAbs

JointVel

JointAcc

JointAccAbs

GeneralizedDispl

# LinkDeformation

## Syntax

SapObject.SapModel.Results.LinkDeformation

## VB6 Procedure

Function LinkDeformation(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm,
ByRef NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase
() As String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,
ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long


## Parameters

Name

The name of an existing link object, link element, or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm= = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the link element corresponding to the link object
specified by the Name item.

If this item is Element, the result request is for the link element specified by the Name item.

If this item is GroupElm, the result request is for all link elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for link elements directly or indirectly selected,
and the Name item is ignored.

For GroupElm and SelectionElm a link element may be indirectly specified through point objects
that have panel zone assignments and through line, area, and solid objects that have spring
assignments.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the link object name associated with each result, if any.

Elm

This is an array that includes the link element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum


This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

U1, U2, U3

These are one dimensional arrays that include the internal translational deformation of the link in
the link element local axes directions. [L]

R1, R2, R3

These are one dimensional arrays that include the internal rotational deformation of the link about
the link element local axes. [rad]

## Remarks

This function reports the link internal deformations.

The function returns zero if the deformations are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetLinkDeformations()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'open existing model
ret = SapModel.File.OpenFile("C:\SapAPI\Example 6-003a.sdb")

'run analysis
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("NLMHIST1")

'set modal history output option to step-by-step
ret = SapModel.Results.Setup.SetOptionModalHist(2)

'get link deformations for link object "1"
ret = SapModel.Results.LinkDeformation("1", ObjectElm, NumberResults, Obj, Elm,
LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

LinkForce

LinkJointForce

# LinkForce

## Syntax

SapObject.SapModel.Results.LinkForce

## VB6 Procedure


Function LinkForce(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef P() As Double, ByRef V2() As Double, ByRef V3() As Double, ByRef T() As Double,
ByRef M2() As Double, ByRef M3() As Double) As Long

## Parameters

Name

The name of an existing link object, link element, or group of objects ,depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the link element corresponding to the link object
specified by the Name item.

If this item is Element, the result request is for the link element specified by the Name item.

If this item is GroupElm, the result request is for all link elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for link elements directly or indirectly selected
and the Name item is ignored.

For GroupElm and SelectionElm a link element may be indirectly specified through point objects
that have panel zone assignments and through line, area and solid objects that have spring
assignments.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the link object name associated with each result, if any.

Elm

This is an array that includes the link element name associated with each result.

PointElm

This is an array that includes the point element name associated with each result.

LoadCase


This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

P

This is an array that includes the link axial force (in the link local 1-axis direction) at the specified
point element. [F]

V2, V3

These are one dimensional arrays that include the link shear force components in the link element
local axes directions. [F]

T

This is an array that includes the link torsion (about the link local 1-axis) at the specified point
element. [FL]

M2, M3

These are one dimensional arrays that include the link moment components about the link element
local axes. [FL]

## Remarks

This function reports the link forces at the point elements at the ends of the specified link
elements.

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetLinkForces()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String


Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim P() As Double
Dim V2() As Double
Dim V3() As Double
Dim T() As Double
Dim M2() As Double
Dim M3() As Double

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

'run analysis
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("NLMHIST1")

'set modal history output option to step-by-step
ret = SapModel.Results.Setup.SetOptionModalHist(2)

'get link forces for link object "1"
ret = SapModel.Results.LinkForce("1", ObjectElm, NumberResults, Obj, Elm, PointElm,
LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3)

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

LinkDeformation

LinkJointForce

# LinkJointForce

## Syntax

SapObject.SapModel.Results.LinkJointForce

## VB6 Procedure

Function LinkJointForce(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef F1() As Double, ByRef F2() As Double, ByRef F3() As Double, ByRef M1() As Double,
ByRef M2() As Double, ByRef M3() As Double) As Long

## Parameters

Name

The name of an existing link object, link element or group of objects depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the link element corresponding to the link object
specified by the Name item.

If this item is Element, the result request is for the link element specified by the Name item.

If this item is GroupElm, the result request is for all link elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for link elements directly or indirectly selected
and the Name item is ignored.


For GroupElm and SelectionElm a link element may be indirectly specified through point objects
that have panel zone assignments and through line, area and solid objects that have spring
assignments.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the link object name associated with each result, if any.

Elm

This is an array that includes the link element name associated with each result.

PointElm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

F1, F2, F3

These are one dimensional arrays that include the joint force components in the point element
local axes directions. [F]

M1, M2, M3

These are one dimensional arrays that include the joint moment components about the point
element local axes. [FL]

## Remarks

This function reports the joint forces for the point elements at the ends of the specified link
elements.

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.


## VBA Example

Similar to AreaJointForceShell

'get link joint forces for link object "1"
ret = SapModel.Results.LinkJointForce("1", ObjectElm, NumberResults, Obj, Elm, PointElm,
LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3)

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

LinkForce

LinkDeformation

# ModalLoadParticipationRatios

## Syntax

SapObject.SapModel.Results.ModalLoadParticipationRatios

## VB6 Procedure

Function ModalLoadParticipationRatios(ByRef NumberResults As Long, ByRef LoadCase() As
String, ByRef ItemType() As String, ByRef Item() As String, ByRef Stat() As Double, ByRef Dyn
() As Double) As Long

## Parameters

NumberResults

The total number of results returned by the program.

LoadCase

This is an array that includes the name of the modal load case associated with each result.

ItemType

This is an array that includes Load Pattern, Acceleration, Link or Panel Zone. It specifies the type
of item for which the modal load participation is reported.

Item


This is an array whose values depend on the ItemType. If the ItemType is Load Pattern, this is the
name of the load pattern.

If the ItemType is Acceleration, this is UX, UY, UZ, RX, RY, or RZ, indicating the acceleration
direction.

If the ItemType is Link, this is the name of the link followed by U1, U2, U3, R1, R2, or R3 (in
parenthesis), indicating the link degree of freedom for which the output is reported.

If the ItemType is Panel Zone, this is the name of the joint to which the panel zone is assigned,
followed by U1, U2, U3, R1, R2, or R3 (in parenthesis), indicating the degree of freedom for
which the output is reported.

Stat

This is an array that includes the percent static load participation ratio.

Dyn

This is an array that includes the percent dynamic load participation ratio.

## Remarks

This function reports the modal load participation ratios for each selected modal analysis case.

The function returns zero if the data is successfully recovered; otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetModalLoadParticipationRatios()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim LoadCase() As String
Dim ItemType() As String
Dim Item() As String
Dim Stat() As Double
Dim Dyn() As Double

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")

'get modal load participation ratios
ret = SapModel.Results.ModalLoadParticipationRatios(NumberResults, LoadCase, ItemType,
Item, Stat, Dyn)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

ModeShape

ModalPeriod

ModalParticipatingMassRatios

ModalParticipationFactors

# ModalParticipatingMassRatios

## Syntax

SapObject.SapModel.Results.ModalParticipatingMassRatios

## VB6 Procedure


Function ModalParticipatingMassRatios(ByRef NumberResults As Long, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef Period() As Double,
ByRef Ux() As Double, ByRef Uy() As Double, ByRef Uz() As Double, ByRef SumUx() As
Double, ByRef SumUy() As Double, ByRef SumUz() As Double, ByRef Rx() As Double, ByRef
Ry() As Double, ByRef Rz() As Double, ByRef SumRx() As Double, ByRef SumRy() As Double,
ByRef SumRz() As Double) As Long

## Parameters

NumberResults

The total number of results returned by the program.

LoadCase

This is an array that includes the name of the modal load case associated with each result.

StepType

This is an array that includes the step type, if any, for each result. For modal results, this will
always be Mode.See Analysis Results Step Type.

StepNum

This is an array that includes the step number for each result. For modal results, this is always the
mode number. See Analysis Results Step Number.

Period

This is an array that includes the period for each result. [s]

Ux

This is an array that includes the modal participating mass ratio for the structure Ux degree of
freedom. The ratio applies to the specified mode.

Uy

This is an array that includes the modal participating mass ratio for the structure Uy degree of
freedom. The ratio applies to the specified mode.

Uz

This is an array that includes the modal participating mass ratio for the structure Uz degree of
freedom. The ratio applies to the specified mode.

SumUx

This is an array that includes the cumulative sum of the modal participating mass ratios for the
structure Ux degree of freedom.

SumUy


This is an array that includes the cumulative sum of the modal participating mass ratios for the
structure Uy degree of freedom.

SumUz

This is an array that includes the cumulative sum of the modal participating mass ratios for the
structure Uz degree of freedom.

Rx

This is an array that includes the modal participating mass ratio for the structure Rx degree of
freedom. The ratio applies to the specified mode.

Ry

This is an array that includes the modal participating mass ratio for the structure Ry degree of
freedom. The ratio applies to the specified mode.

Rz

This is an array that includes the modal participating mass ratio for the structure Rz degree of
freedom. The ratio applies to the specified mode.

SumRx

This is an array that includes the cumulative sum of the modal participating mass ratios for the
structure Rx degree of freedom.

SumRy

This is an array that includes the cumulative sum of the modal participating mass ratios for the
structure Ry degree of freedom.

SumRz

This is an array that includes the cumulative sum of the modal participating mass ratios for the
structure Rz degree of freedom.

## Remarks

This function reports the modal participating mass ratios for each mode of each selected modal
analysis case.

The function returns zero if the data is successfully recovered; otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetModalParticipatingMassRatios()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim Period() As Double
Dim Ux() As Double
Dim Uy() As Double
Dim Uz() As Double
Dim SumUx() As Double
Dim SumUy() As Double
Dim SumUz() As Double
Dim Rx() As Double
Dim Ry() As Double
Dim Rz() As Double
Dim SumRx() As Double
Dim SumRy() As Double
Dim SumRz() As Double

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")

'get modal participating mass ratios
ret = SapModel.Results.ModalParticipatingMassRatios(NumberResults, LoadCase, StepType,
StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

ModeShape

ModalPeriod

ModalParticipationFactors

ModalLoadParticipationRatios

# ModalParticipationFactors

## Syntax

SapObject.SapModel.Results.ModalParticipationFactors

## VB6 Procedure

Function ModalParticipationFactors(ByRef NumberResults As Long, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef Period() As Double,
ByRef Ux() As Double, ByRef Uy() As Double, ByRef Uz() As Double, ByRef Rx() As Double,
ByRef Ry() As Double, ByRef Rz() As Double, ByRef ModalMass() As Double, ByRef
ModalStiff() As Double) As Long

## Parameters

NumberResults

The total number of results returned by the program.

LoadCase

This is an array that includes the name of the modal load case associated with each result.

StepType

This is an array that includes the step type, if any, for each result. For modal results, this will
always be Mode.See Analysis Results Step Type.

StepNum


This is an array that includes the step number for each result. For modal results, this will always
be the mode number. See Analysis Results Step Number.

Period

This is an array that includes the period for each result. [s]

Ux

This is an array that includes the modal participation factor for the structure Ux degree of freedom.
The factor applies to the specified mode. [Fs^2 ]

Uy

This is an array that includes the modal participation factor for the structure Uy degree of freedom.
The factor applies to the specified mode. [Fs^2 ]

Uz

This is an array that includes the modal participation factor for the structure Uz degree of freedom.
The factor applies to the specified mode. [Fs^2 ]

Rx

This is an array that includes the modal participation factor for the structure Rx degree of freedom.
The factor applies to the specified mode. [FLs^2 ]

Ry

This is an array that includes the modal participation factor for the structure Ry degree of freedom.
The factor applies to the specified mode. [FLs^2 ]

Rz

This is an array that includes the modal participation factor for the structure Rz degree of freedom.
The factor applies to the specified mode. [FLs^2 ]

ModalMass

This is an array that includes the modal mass for the specified mode. This is a measure of the
kinetic energy in the structure as it is deforming in the specified mode. [FLs^2 ]

ModalStiff

This is an array that includes the modal stiffness for the specified mode. This is a measure of the
strain energy in the structure as it is deforming in the specified mode. [FL]

## Remarks

This function reports the modal participation factors for each mode of each selected modal
analysis case.

The function returns zero if the data is successfully recovered; otherwise it returns a nonzero
value.


See Analysis Results Remarks for more information.

## VBA Example

Sub GetModalParticipationFactors()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim Period() As Double
Dim Ux() As Double
Dim Uy() As Double
Dim Uz() As Double
Dim Rx() As Double
Dim Ry() As Double
Dim Rz() As Double
Dim ModalMass() As Double
Dim ModalStiff() As Double

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")

'get modal participation factors
ret = SapModel.Results.ModalParticipationFactors(NumberResults, LoadCase, StepType,
StepNum, Period, Ux, Uy, Uz, Rx, Ry, Rz, ModalMass, ModalStiff)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

ModeShape

ModalPeriod

ModalParticipatingMassRatios

ModalLoadParticipationRatios

# ModalPeriod

## Syntax

SapObject.SapModel.Results.ModalPeriod

## VB6 Procedure

Function ModalPeriod(ByRef NumberResults As Long, ByRef LoadCase() As String, ByRef
StepType() As String, ByRef StepNum() As Double, ByRef Period() As Double, ByRef
Frequency() As Double, ByRef CircFreq() As Double, ByRef EigenValue() As Double) As Long

## Parameters

NumberResults

The number total of results returned by the program.

LoadCase

This is an array that includes the name of the modal analysis case associated with each result.

StepType

This is an array that includes the step type, if any, for each result. For modal results this is always
be Mode. See Analysis Results Step Type.

StepNum


This is an array that includes the step number for each result. For modal results this is always the
mode number. See Analysis Results Step Number.

Period

This is an array that includes the period for each result. [s]

Frequency

This is an array that includes the cyclic frequency for each result. [1/s]

CircFreq

This is an array that includes the circular frequency for each result. [rad/s]

EigenValue

This is an array that includes the eigenvalue for the specified mode for each result. [rad^2 /s^2 ]

## Remarks

This function reports the modal period, cyclic frequency, circular frequency and eigenvalue for
each selected modal load case.

The function returns zero if the data is successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetPeriod()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim Period() As Double
Dim Frequency() As Double
Dim CircFreq() As Double
Dim EigenValue() As Double

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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")

'get modal period
ret = SapModel.Results.ModalPeriod(NumberResults, LoadCase, StepType, StepNum, Period,
Frequency, CircFreq, EigenValue)

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

ModeShape

# ModeShape

## Syntax

SapObject.SapModel.Results.ModeShape

## VB6 Procedure

Function ModeShape(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,


ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long

## Parameters

Name

The name of an existing point element or group of objects, depending on the value of the
ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the point element corresponding to the point
object specified by the Name item.

If this item is Element, the result request is for the point element specified by the Name item.

If this item is GroupElm, the result request is for all point elements directly or indirectly specified
in the group specified by the Name item.

If this item is SelectionElm, the result request is for all point elements directly or indirectly
selected and the Name item is ignored.

See Item Type for Elements for more information.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the point object name associated with each result, if any. Some
results will have no point object associated with them. For these cases this item will be blank.

Elm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the modal analysis case associated with each result.

StepType

This is an array that includes the step type, if any, for each result. For mode shape results, this is
always be Mode. See Analysis Results Step Type.

StepNum


This is an array that includes the step number for each result. For mode shape results, this is
always the mode number. See Analysis Results Step Number.

U1, U2, U3

These are one dimensional arrays that include the displacement in the point element local 1, 2 and
3 axes directions, respectively, for each result. [L]

R1, R2, R3

These are one dimensional arrays that include the rotation about the point element local 1, 2 and 3
axes, respectively, for each result. [rad]

## Remarks

This function reports the modal displacements (mode shapes) for the specified point elements.

The function returns zero if the displacements are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetModeShapes()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")

'get mode shape
ret = SapModel.Results.ModeShape("ALL", GroupElm, NumberResults, Obj, Elm, LoadCase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

ModalPeriod

# PanelZoneDeformation

## Syntax

SapObject.SapModel.Results.PanelZoneDeformation

## VB6 Procedure

Function PanelZoneDeformation(ByVal Name As String, ByVal ItemTypeElm As
eItemTypeElm, ByRef NumberResults As Long, ByRef Elm() As String, ByRef LoadCase() As
String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef U1() As Double,
ByRef U2() As Double, ByRef U3() As Double, ByRef R1() As Double, ByRef R2() As Double,
ByRef R3() As Double) As Long


## Parameters

Name

The name of an existing link object, link element, or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the panel zone (link) element corresponding to
the panel zone assignment to the point object specified by the Name item.

If this item is Element, the result request is for the panel zone (link) element specified by the
Name item.

If this item is GroupElm, the result request is for all panel zone (link) elements directly or
indirectly specified in the group specified by the Name item.

If this item is SelectionElm, the result request is for panel zone (link) elements directly or
indirectly selected and the Name item is ignored.

For GroupElm and SelectionElm a panel zone (link) element may be indirectly specified through
point objects that have panel zone assignments.

NumberResults

The total number of results returned by the program.

Elm

This is an array that includes the panel zone (link) element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

U1, U2, U3


These are one dimensional arrays that include the internal translational deformation of the panel
zone (link) in the link element local axes directions. [L]

R1, R2, R3

These are one dimensional arrays that include the internal rotational deformation of the panel zone
(link) about the link element local axes. [rad]

## Remarks

This function reports the panel zone (link) internal deformations.

The function returns zero if the deformations are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetPanelZoneDeformation()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Elm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'assign panel zone to point object "3"


ret = SapModel.PointObj.SetPanelZone("3", 1, 2, 0, 0, "", 0, 0, 0)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get panel zone deformation for point object "3"
ret = SapModel.Results.PanelZoneDeformation("3", ObjectElm, NumberResults, Elm,
LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)

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

PanelZoneForce

# PanelZoneForce

## Syntax

SapObject.SapModel.Results.PanelZoneForce

## VB6 Procedure

Function PanelZoneForce(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm,
ByRef NumberResults As Long, ByRef Elm() As String, ByRef PointElm() As String, ByRef
LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef P() As
Double, ByRef V2() As Double, ByRef V3() As Double, ByRef T() As Double, ByRef M2() As
Double, ByRef M3() As Double) As Long


## Parameters

Name

The name of an existing point object, point element, or group of objects, depending on the value
of the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the panel zone (link) element corresponding to
the panel zone assignment to the point object specified by the Name item.

If this item is Element, the result request is for the panel zone (link) element specified by the
Name item.

If this item is GroupElm, the result request is for all panel zone (link) elements directly or
indirectly specified in the group specified by the Name item.

If this item is SelectionElm, the result request is for panel zone (link) elements directly or
indirectly selected and the Name item is ignored.

For GroupElm and SelectionElm a panel zone (link) element may be indirectly specified through
point objects that have panel zone assignments.

NumberResults

The total number of results returned by the program.

Elm

This is an array that includes the panel zone (link) element name associated with each result.

PointElm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum


This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

P

This is an array that includes the panel zone (link) axial force (in the link local 1-axis direction) at
the specified point element. [F]

V2, V3

These are one dimensional arrays that include the panel zone (link) shear force components in the
link element local axes directions. [F]

T

This is an array that includes the panel zone (link) torsion (about the link local 1-axis) at the
specified point element. [FL]

M2, M3

These are one dimensional arrays that include the panel zone (link) moment components about the
link element local axes. [FL]

## Remarks

This function reports the panel zone (link) forces at the point elements at the ends of the specified
panel zone (link) elements.

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Result Remarks for more information.

## VBA Example

Sub GetPanelZoneForce()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim P() As Double
Dim V2() As Double
Dim V3() As Double
Dim T() As Double
Dim M2() As Double
Dim M3() As Double


'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'assign panel zone to point object "3"
ret = SapModel.PointObj.SetPanelZone("3", 1, 2, 0, 0, "", 0, 0, 0)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get panel zone force for point object "3"
ret = SapModel.Results.PanelZoneForce("3", ObjectElm, NumberResults, Elm, PointElm,
LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3)

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

PanelZoneDeformation


# SectionCutAnalysis

## Syntax

SapObject.SapModel.Results.SectionCutAnalysis

## VB6 Procedure

Function SectionCutAnalysis(ByRef NumberResults As Long, ByRef SCut() As String, ByRef
LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef F1() As
Double, ByRef F2() As Double, ByRef F3() As Double, ByRef M1() As Double, ByRef M2() As
Double, ByRef M3() As Double) As Long

## Parameters

NumberResults

The number total of results returned by the program.

SCut

This is an array that includes the name of the section cut associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

F1, F2, F3

These are one dimensional arrays that include the forces in the section cut local axes directions for
each result. [F]

M1, M2, M3

These are one dimensional arrays that include the moments about the section cut local axes for
each result. [FL]

## Remarks

This function reports the section cut force for sections cuts that are specified to have an Analysis
(F1, F2, F3, M1, M2, M3) result type.


The function returns zero if the section cut forces are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Similar to FrameJointForce

'get section cut forces with analysis output convention
ret = SapModel.Results.SectionCutAnalysis(NumberResults, SCut, LoadCase, StepType,
StepNum, F1, F2, F3, M1, M2, M3)

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SectionCutDesign

# SectionCutDesign

## Syntax

SapObject.SapModel.Results.SectionCutDesign

## VB6 Procedure

Function SectionCutDesign(ByRef NumberResults As Long, ByRef SCut() As String, ByRef
LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double, ByRef P() As
Double, ByRef V2() As Double, ByRef V3() As Double, ByRef T() As Double, ByRef M2() As
Double, ByRef M3() As Double) As Long

## Parameters

NumberResults

The total number of results returned by the program.

SCut

This is an array that includes the name of the section cut associated with each result.

LoadCase


This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

P, V2, V3

These are one dimensional arrays that include the axial force, shear force in the section cut local 2
direction and shear force in the section cut local 3 direction, respectively, for each result. [F]

T, M2, M3

These are one dimensional arrays that include the torsion, moment about the section cut local 2
axis and moment about the section cut local 3-axis, respectively, for each result. [FL]

## Remarks

This function reports the section cut force for sections cuts that are specified to have a Design (P,
V2, V3, T, M2, M3) result type.

The function returns zero if the section cut forces are successfully recovered, otherwise it returns a
nonzero value.

See Analysis Results Remarks for more information.

## VBA Example

Similar to FrameForce

'get section cut forces with design output convention
ret = SapModel.Results.SectionCutDesign(NumberResults, SCut, LoadCase, StepType,
StepNum, P, V2, V3, T, M2, M3)

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SectionCutAnalysis


# SolidJointForce

## Syntax

SapObject.SapModel.Results.SolidJointForce

## VB6 Procedure

Function SolidJointForce(ByVal Name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef F1() As Double, ByRef F2() As Double, ByRef F3() As Double, ByRef M1() As Double,
ByRef M2() As Double, ByRef M3() As Double) As Long

## Parameters

Name

The name of an existing solid object, solid element, or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the solid elements corresponding to the solid
object specified by the Name item.

If this item is Element, the result request is for the solid element specified by the Name item.

If this item is GroupElm, the result request is for the solid elements corresponding to all solid
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for solid elements corresponding to all selected
solid objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the solid object name associated with each result, if any.

Elm


This is an array that includes the solid element name associated with each result.

PointElm

This is an array that includes the point element name associated with each result.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

F1, F2, F3

These are one dimensional arrays that include the joint force components in the point element
local axes directions. [F]

M1, M2, M3

These are one dimensional arrays that include the joint moment components about the point
element local axes. [FL]

## Remarks

This function reports the joint forces for the point elements at each corner of the specified solid
elements.

The function returns zero if the forces are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetSolidJointForces()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String


Dim StepNum() As Double
Dim F1() As Double
Dim F2() As Double
Dim F3() As Double
Dim M1() As Double
Dim M2() As Double
Dim M3() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create a solid model from template
ret = SapModel.File.NewSolidBlock(20, 50, 20)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get solid joint forces for solid object "1"
ret = SapModel.Results.SolidJointForce("1", ObjectElm, NumberResults, Obj, Elm, PointElm,
LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3)

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

SolidStress

# SolidStrain

## Syntax

SapObject.SapModel.Results.SolidStrain

## VB6 Procedure

Function SolidStrain(ByVal name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef E11() As Double, ByRef E22() As Double, ByRef E33() As Double, ByRef G12() As
Double, ByRef G13() As Double, ByRef G23() As Double, ByRef EMax() As Double, ByRef
EMid() As Double, ByRef EMin() As Double, ByRef EVM() As Double, ByRef DirCosMax1()
As Double, ByRef DirCosMax2() As Double, ByRef DirCosMax3() As Double, ByRef
DirCosMid1() As Double, ByRef DirCosMid2() As Double, ByRef DirCosMid3() As Double,
ByRef DirCosMin1() As Double, ByRef DirCosMin2() As Double, ByRef DirCosMin3() As
Double) As Long

## Parameters

Name

The name of an existing solid object, solid element, or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the solid elements corresponding to the solid
object specified by the Name item.

If this item is Element, the result request is for the solid element specified by the Name item.

If this item is GroupElm, the result request is for the solid elements corresponding to all solid
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for solid elements corresponding to all selected
solid objects and the Name item is ignored.


NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the solid object name associated with each result, if any.

Elm

This is an array that includes the solid element name associated with each result.

PointElm

This is an array that includes the name of the point element where the results are reported.

LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

E11, E22, E33, G12, G13, G23

The solid element internal E11, E22, E33, G12, G13 and G23 strains at the specified point element
location, reported in the solid element local coordinate system.

EMax, EMid, EMin

The solid element maximum, middle and minimum principal strains at the specified point element
location.

EVM

The solid element internal Von Mises strain at the specified point element location.

DirCosMax1, DirCosMax2, DirCosMax3

These are three direction cosines defining the orientation of the maximum principal strain with
respect to the solid element local axes.

DirCosMid1, DirCosMid2, DirCosMid3

These are three direction cosines defining the orientation of the middle principal strain with
respect to the solid element local axes.

DirCosMin1, DirCosMin2, DirCosMin3


These are three direction cosines defining the orientation of the minimum principal strain with
respect to the solid element local axes.

## Remarks

This function reports the strains for the specified solid elements. Strains are reported at each point
element associated with the solid element.

The function returns zero if the strains are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.

## VBA Example

Sub GetSolidStrains()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim E11() As Double
Dim E22() As Double
Dim E33() As Double
Dim G12() As Double
Dim G13() As Double
Dim G23() As Double
Dim EMax() As Double
Dim EMid() As Double
Dim EMin() As Double
Dim EVM() As Double
Dim DirCosMax1() As Double
Dim DirCosMax2() As Double
Dim DirCosMax3() As Double
Dim DirCosMid1() As Double
Dim DirCosMid2() As Double
Dim DirCosMid3() As Double
Dim DirCosMin1() As Double
Dim DirCosMin2() As Double
Dim DirCosMin3() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart


'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create a solid model from template
ret = SapModel.File.NewSolidBlock(20, 50, 20)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get solid strains for solid object "1"
ret = SapModel.Results.SolidStrain("1", ObjectElm, NumberResults, Obj, Elm, PointElm,
LoadCase, StepType, StepNum, E11, E22, E33, G12, G13, G23, EMax, EMid, EMin, EVM,
DirCosMax1, DirCosMax2, DirCosMax3, DirCosMid1, DirCosMid2, DirCosMid3, DirCosMin1,
DirCosMin2, DirCosMin3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 20.1.0.

## See Also

SolidStress

# SolidStress

## Syntax

SapObject.SapModel.Results.SolidStress

## VB6 Procedure


Function SolidStress(ByVal name As String, ByVal ItemTypeElm As eItemTypeElm, ByRef
NumberResults As Long, ByRef Obj() As String, ByRef Elm() As String, ByRef PointElm() As
String, ByRef LoadCase() As String, ByRef StepType() As String, ByRef StepNum() As Double,
ByRef S11() As Double, ByRef S22() As Double, ByRef S33() As Double, ByRef S12() As
Double, ByRef S13() As Double, ByRef S23() As Double, ByRef SMax() As Double, ByRef
SMid() As Double, ByRef SMin() As Double, ByRef SVM() As Double, ByRef DirCosMax1()
As Double, ByRef DirCosMax2() As Double, ByRef DirCosMax3() As Double, ByRef
DirCosMid1() As Double, ByRef DirCosMid2() As Double, ByRef DirCosMid3() As Double,
ByRef DirCosMin1() As Double, ByRef DirCosMin2() As Double, ByRef DirCosMin3() As
Double) As Long

## Parameters

Name

The name of an existing solid object, solid element, or group of objects, depending on the value of
the ItemTypeElm item.

ItemTypeElm

This is one of the following items in the eItemTypeElm enumeration:

```
ObjectElm = 0
Element = 1
GroupElm = 2
SelectionElm = 3
```
If this item is ObjectElm, the result request is for the solid elements corresponding to the solid
object specified by the Name item.

If this item is Element, the result request is for the solid element specified by the Name item.

If this item is GroupElm, the result request is for the solid elements corresponding to all solid
objects included in the group specified by the Name item.

If this item is SelectionElm, the result request is for solid elements corresponding to all selected
solid objects and the Name item is ignored.

NumberResults

The total number of results returned by the program.

Obj

This is an array that includes the solid object name associated with each result, if any.

Elm

This is an array that includes the solid element name associated with each result.

PointElm

This is an array that includes the name of the point element where the results are reported.


LoadCase

This is an array that includes the name of the analysis case or load combination associated with
each result.

StepType

This is an array that includes the step type, if any, for each result. See Analysis Results Step Type.

StepNum

This is an array that includes the step number, if any, for each result. See Analysis Results Step
Number.

S11, S22, S33, S12, S13, S23

The solid element internal S11, S22, S33, S12, S13 and S23 stresses at the specified point element

location, reported in the solid element local coordinate system. [F/L^2 ]

SMax, SMid, SMin

The solid element maximum, middle and minimum principal stresses at the specified point

element location. [F/L^2 ]

SVM

The solid element internal Von Mises stress at the specified point element location. [F/L^2 ]

DirCosMax1, DirCosMax2, DirCosMax3

These are three direction cosines defining the orientation of the maximum principal stress with
respect to the solid element local axes.

DirCosMid1, DirCosMid2, DirCosMid3

These are three direction cosines defining the orientation of the middle principal stress with
respect to the solid element local axes.

DirCosMin1, DirCosMin2, DirCosMin3

These are three direction cosines defining the orientation of the minimum principal stress with
respect to the solid element local axes.

## Remarks

This function reports the stresses for the specified solid elements. Stresses are reported at each
point element associated with the solid element.

The function returns zero if the stresses are successfully recovered, otherwise it returns a nonzero
value.

See Analysis Results Remarks for more information.


## VBA Example

Sub GetSolidStresses()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberResults As Long
Dim Obj() As String
Dim Elm() As String
Dim PointElm() As String
Dim LoadCase() As String
Dim StepType() As String
Dim StepNum() As Double
Dim S11() As Double
Dim S22() As Double
Dim S33() As Double
Dim S12() As Double
Dim S13() As Double
Dim S23() As Double
Dim SMax() As Double
Dim SMid() As Double
Dim SMin() As Double
Dim SVM() As Double
Dim DirCosMax1() As Double
Dim DirCosMax2() As Double
Dim DirCosMax3() As Double
Dim DirCosMid1() As Double
Dim DirCosMid2() As Double
Dim DirCosMid3() As Double
Dim DirCosMin1() As Double
Dim DirCosMin2() As Double
Dim DirCosMin3() As Double

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create a solid model from template
ret = SapModel.File.NewSolidBlock(20, 50, 20)

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis


'clear all case and combo output selections
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput

'set case and combo output selections
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

'get solid stresses for solid object "1"
ret = SapModel.Results.SolidStress("1", ObjectElm, NumberResults, Obj, Elm, PointElm,
LoadCase, StepType, StepNum, S11, S22, S33, S12, S13, S23, SMax, SMid, SMin, SVM,
DirCosMax1, DirCosMax2, DirCosMax3, DirCosMid1, DirCosMid2, DirCosMid3, DirCosMin1,
DirCosMin2, DirCosMin3)

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

SolidJointForce

# StepLabel

## Syntax

SapObject.SapModel.Results.StepLabel

## VB6 Procedure

Function StepLabel(ByVal LoadCase As String, ByVal StepNum As Double, ByRef Label As
String) As Long

## Parameters

LoadCase

The name of an existing linear multi-step, nonlinear multi-step, or staged-construction load case.

StepNum


This is an overall step number from the specified load case. The range of values of StepNum for a
given load case can be obtained from most analysis results calls, such as
SapObject.SapModel.Results.JointDispl. See Analysis Results Step Number.

Label

The is the step label, including the name or number of the stage, the step number within the stage,
and the age of the structure for time-dependent load cases

## Remarks

This function generates the step label for analyzed linear multi-step, nonlinear multi-step, or
staged-construction load cases. For other load case types, the label will be blank.

The function returns zero if the step label is successfully generated; otherwise it returns a nonzero
value.

## VBA Example

Sub GetStepLabel()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As Sap2000v16.cSapModel
Dim ret As Long
Dim MyDuration() As Long
Dim MyOutput() As Boolean
Dim MyOutputName() As String
Dim MyComment() As String
Dim MyOperation() As Long
Dim MyObjectType() As String
Dim MyObjectName() As String
Dim MyAge() As Long
Dim MyMyType() As String
Dim MyMyName() As String
Dim MySF() As Double
Dim Label() as String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'create model from template
ret = SapModel.File.New2DFrame(Sap2000v16.PortalFrame, 2, 144, 2, 288)


'add static nonlinear staged load case
ret = SapModel.LoadCases.StaticNonlinearStaged.SetCase("ACASE1")

'initialize stage definitions
ReDim MyDuration(1)
ReDim MyOutput(1)
ReDim MyOutputName(1)
ReDim MyComment(1)

Redim Label(1)
MyDuration(0) = 0
MyOutput(0) = False
MyComment(0) = "Build structure"
MyDuration(1) = 60
MyOutput(1) = True
MyOutputName(1) = "HBC2"
MyComment(1) = "Wait"
ret = SapModel.LoadCases.StaticNonlinearStaged.SetStageDefinitions_1("ACASE1", 2,
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
ret = SapModel.LoadCases.StaticNonlinearStaged.SetStageData_1("ACASE1", 1, 2,
MyOperation, MyObjectType, MyObjectName, MyAge, MyMyType, MyMyName, MySF)

'set results saved parameters
ret = SapModel.LoadCases.StaticNonlinearStaged.SetResultsSaved("ACASE1", 3, 4, 10)

'save model
ret = SapModel.File.Save("C:\SapAPI\x.sdb")

'run model (this will create the analysis model)
ret = SapModel.Analyze.RunAnalysis

'Get step label
ret = SapModel.Results.StepLabel("ACASE1", 3, Label(0))


ret = SapModel.Results.StepLabel("ACASE1", 8, Label(1))

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 16.00.

# Analysis Results Remarks

The analysis results are returned in a collection of one-dimensional result arrays. Each result array
is created as a dynamic array by the API user. As an example, in VBA a dynamic string array is
defined by:

Dim MyArray() as String

The array is dimensioned to (NumberResults– 1) inside the Sap2000 program, filled with the
result values, and returned to the API user.

The arrays are zero-based. Thus the first result is at array index 0, and the last result is at array
index (NumberResults- 1). For example, the StepType() array is filled as:

StepType(0) = Step type for first result returned
StepType(1) = Step type for second result
.
.
StepType(NumberResults- 1) = Step type for last result

Immediately before requesting results data, it is a good idea to clear the SelectedForOutput flag
for all load cases and response combinations and then to set the flag True for those cases and
combos for which output is to be generated. This avoids confusion as to which cases and combos
are currently selected for output.

## Release Notes

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

# Analysis Results Step Number

The step number varies depending on the type of output case considered. For linear static and
response spectrum load cases, this step number is not used.

For nonlinear static load cases, it reports the step number when the step type is Step.


For modal cases, the step number is the mode number.

For buckling cases, the step number is the buckling mode number.

For linear modal history, nonlinear modal history, linear direct integration history, and nonlinear
direct integration history cases, the step number reports the time in seconds when the step type is
Time.

For steady state and power spectral density load cases, the step number is the frequency in Hz
when the step type is Real at Freq, Imag at Freq, or Mag at Freq."

## Release Notes

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

# Analysis Results Step Type

The step type varies depending on the type of output case considered. For linear static and
response spectrum load cases, the step type is not used.

For nonlinear static load cases, the step type is Step, Max, or Min.

For modal cases, the step type is Mode.

For buckling cases, the step type is Mode, which refers to the buckling mode number.

For linear modal history, nonlinear modal history, linear direct integration history, and nonlinear
direct integration history cases, the step type is Time, Max or Min.

For steady state and power spectral density load cases, the step type is Real at Freq, Imag at Freq,
Real Min, Real Max, ImagMin, Imag Max, Mag at Freq, Mag Min, Mag Max, or RMS. Freq is
short for frequency, Imag is short for imaginary and Mag is short for magnitude.

For double-valued combinations, this is either Max or Min.

For moving load patterns, this is the force correspondence if it has been requested. It may be M3
Min, M3 Max, M2 Min, M2 Max, T Min, T Max, V3 Min, V3 Max, V2 Min, V2 Max, P Min, or
P Max.

Release Notes

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

# Item Type For Elements

The ItemTypeElm is one of the following items in the eItemTypeElmenumeration:

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
If this item is ObjectElm, the item request is for the point element corresponding to the point
object specified by the Name item.

If the ItemTypeElm is Element, the item request is for the point element specified by the Name
item.

If the ItemTypeElm is GroupElm, the item request is for all point elements directly or indirectly
specified in the group specified by the Name item. If a point object is in the specified group, data
is requested for its corresponding point element. If line, area, solid or link objects are in the
specified group, data is requested for all point elements associated with those objects, including
those point elements created as a result of automatic internal meshing of the object by the
program.

If the ItemTypeElm is SelectionElm, the item request is for all point elements directly or indirectly
selected and the Name item is ignored. If a point object is selected, data is requested for its
corresponding point element. If line, area, solid or link objects are selected, data is requested for
all point elements associated with those objects, including those point elements created as a result
of automatic internal meshing of the object by the program.


