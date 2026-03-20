# CreateAnalysisModel

## Syntax

SapObject.SapModel.Analyze.CreateAnalysisModel

## VB6 Procedure

Function CreateAnalysisModel() As Long

## Parameters

None

## Remarks

This function creates the analysis model. If the analysis model is already created and current,
nothing is done.

The function returns zero if the analysis model is successfully created or it already exists and is
current, otherwise it returns a nonzero value.

It is not necessary to call this function before running an analysis. The analysis model is
automatically created, if necessary, when the model is run.

## VBA Example

Sub CreateSapAnalysisModel()
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


'create the analysis model
ret = SapModel.Analyze.CreateAnalysisModel

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

RunAnalysis

# DeleteResults

## Syntax

SapObject.SapModel.Analyze.DeleteResults

## VB6 Procedure

Function DeleteResults(ByVal Name As String, Optional ByVal All As Boolean = False) As Long

## Parameters

Name

The name of an existing load case that is to have its results deleted.

This item is ignored when the All item is True.

All

If this item is True, the results are deleted for all load cases, and the Name item is ignored.

## Remarks

This function deletes results for load cases.

The function returns zero if the results are successfully deleted; otherwise it returns a nonzero
value.


## VBA Example

Sub DeleteLoadCaseResults()
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

'run analysis
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'delete load case results
ret = SapModel.Analyze.DeleteResults("MODAL")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# GetActiveDOF

## Syntax


SapObject.SapModel.Analyze.GetActiveDOF

## VB6 Procedure

Function GetActiveDOF(ByRef DOF() As Boolean) As Long

## Parameters

### DOF

This is an array of 6 boolean values, indicating if the specified model global degree of freedom is
active.

```
DOF(0) = UX
DOF(1) = UY
DOF(2) = UZ
DOF(3) = RX
DOF(4) = RY
DOF(5) = RZ
```
## Remarks

This function retrieves the model global degrees of freedom.

The function returns zero if the degrees of freedom are successfully retrieved; otherwise it returns
a nonzero value.

## VBA Example

Sub GetModelActiveDOF()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)


'get model degrees of freedom
ret = SapModel.Analyze.GetActiveDOF(DOF)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

SetActiveDOF

# GetCaseStatus

## Syntax

SapObject.SapModel.Analyze.GetCaseStatus

## VB6 Procedure

Function GetCaseStatus(ByRef NumberItems As Long, ByRef CaseName() As String, ByRef
Status() As Long) As Long

## Parameters

NumberItems

The number of load cases for which the status is reported.

CaseName

This is an array that includes the name of each analysis case for which the status is reported.

Status

This is an array of that includes 1, 2, 3 or 4, indicating the load case status.

```
1 = Not run
2 = Could not start
3 = Not finished
4 = Finished
```

## Remarks

This function retrieves the status for all load cases.

The function returns zero if the status is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetCaseStatusExample()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim CaseName() As String
Dim Status() As Long

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

'set load case run flag
ret = SapModel.Analyze.SetRunCaseFlag("MODAL", False)

'run model (this will create the analysis model)
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'get load case status
ret = SapModel.Analyze.GetCaseStatus(NumberItems, CaseName, Status)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 11.03.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# GetRunCaseFlag

## Syntax

SapObject.SapModel.Analyze.GetRunCaseFlag

## VB6 Procedure

Function GetRunCaseFlag(ByRef NumberItems As Long, ByRef CaseName() As String, ByRef
Run() As Boolean) As Long

## Parameters

NumberItems

The number of load cases for which the run flag is reported.

CaseName

This is an array that includes the name of each analysis case for which the run flag is reported.

Run

This is an array of boolean values indicating if the specified load case is to be run.

## Remarks

This function retrieves the run flags for all analysis cases.

The function returns zero if the flags are successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetRunCaseFlagExample()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim CaseName() As String


Dim Run() As Boolean

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

'set load case run flag
ret = SapModel.Analyze.SetRunCaseFlag("MODAL", False)

'get load case run flags
ret = SapModel.Analyze.GetRunCaseFlag(NumberItems, CaseName, Run)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

SetRunCaseFlag

# GetSolverOption_

## Syntax

SapObject.SapModel.Analyze.GetSolverOption_

## VB6 Procedure


Function GetSolverOption_3(ByRef SolverType As Long, ByRef SolverProcessType As Long,
ByRef NumberParallelRuns As Long, ByRef ResponseFileSizeMaxMB As Long, ByRef
NumberAnalysisThreads As Long, ByRef StiffCase As String) As Long

## Parameters

**SolverType**

This is 0, 1 or 2, indicating the solver type.

```
0 = Standard solver
1 = Advanced solver
2 = Multi-threaded solver
```
**SolverProcessType**

This is 0, 1 or 2, indicating the process the analysis is run.

```
0 = Auto (program determined)
1 = GUI process
2 = Separate process
```
**NumberParallelRuns**

This is an integer between -8 and 8, inclusive, not including -1 or 0.

```
-8 to -2 = The negative of the program determined value when the assigned value is
0 = Auto parallel (use up to all physical cores - max 8).
1 = Serial.
2 to 8 = User defined parallel (use up to this fixed number of cores - max 8
```
ResponseFileSizeMaxMB

The maximum size of a response file in MB before a new response file is created. Positive if user
specified, negative if program determined.

NumberAnalysisThreads

Number of threads that the analysis can use. Positive if user specified, negative if program
determined.

**StiffCase**

The name of the load case used when outputting the mass and stiffness matrices to text files. If
this item is blank, no matrices are output.

## Remarks

This function retrieves the model solver options.

The function returns zero if the options are successfully retrieved; otherwise it returns a nonzero
value.


## VBA Example

Sub GetModelSolverOption()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim SolverType As Long
Dim SolverProcessType As Long
Dim StiffCase As String

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

'set model solver options
ret = SapModel.Analyze.GetSolverOption_3(SolverType, SolverProcessType,
NumberParallelRuns, ResponseFileSizeMaxMB, NumberAnalysisThreads, StiffCase)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.1.0.

Modified the allowed values for NumberParallelRuns in v 22.1.0.

Added ResponseFileSizeMaxMB and NumberAnalysisThreads parameters in v23.2.

This function supersedes GetSolverOption_2 , adding the NumberParallelRuns parameter and
removing the previous Force32BitSolver parameter

## See Also

SetSolverOption_


# MergeAnalysisResults

## Syntax

SapObject.SapModel.Analyze.MergeAnalysisResults

## VB6 Procedure

Function MergeAnalysisResults(ByVal FileName As String) As Long

## Parameters

FileName

The full path of a model file from which the analysis results are to be merged.

## Remarks

See “Merging Analysis Results” section in program help file for requirements and limitations.

The analysis model is automatically created as part of this function.

The function returns zero if analysis results are successfully merged, otherwise it returns a
nonzero value.

IMPORTANT NOTE: Your model must have a file path defined before merging analysis results.
If the model is opened from an existing file, a file path is defined. If the model is created from
scratch, the File.Save function must be called with a file name before merging analysis results.
Saving the file creates the file path.

## VBA Example

Sub MergeSapAnalysisResults()
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

'save model
ret = SapModel.File.Save("C:\SapAPI\source\model.sdb")

'run model (this will create the analysis model)
ret = SapModel.Analyze.RunAnalysis

'initialize a new model
ret = SapModel.InitializeNewModel

'create the same model from template
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'merge analysis results
ret = SapModel.Analyze.SetSolverOption_2(1, 2, 0)

ret = SapModel.File.Save("C:\SapAPI\target\model.sdb")
ret = SapModel.Analyze.MergeAnalysisResults("C:\SapAPI\source\model.sdb")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing

End Sub

## Release Notes

Initial release in version 22.1.0.

## See Also

File.Save

Analyze.RunAnalysis

Analyze.SetSolverOption_

# ModifyUnDeformedGeometry

## Syntax

SapObject.SapModel.Analyze.ModifyUnDeformedGeometry


## VB6 Procedure

Function ModifyUnDeformedGeometry(ByVal CaseName As String, ByVal SF As Double,
Optional ByVal Stage As Long = -1, Optional ByVal Original As Boolean = False) As Long

## Parameters

CaseName

The name of the static load case from which displacements are obtained.

SF

The scale factor applied to the displacements.

Stage

This item applies only when the specified load case is a staged construction load case. It is the
stage number from which the displacements are obtained. Specifying a -1 for this item means to
use the last run stage.

Original

If this item is True, all other input items in this function are ignored and the original undeformed
geometry data is reinstated.

## Remarks

This function modifies the undeformed geometry based on displacements obtained from a
specified load case.

The function returns zero if it is successful; otherwise it returns a nonzero value.

## VBA Example

Sub ModifyUnDeformedGeometryExample()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
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
ret = SapModel.File.NewBeam(2, 288, False)

'assign point object restraints
Redim Value(5)
For i = 0 to 5
Value(i) = True
Next i
ret = SapModel.PointObj.SetRestraint("1", Value)

'run model
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'modify undeformed geometry
ret = SapModel.Analyze.ModifyUnDeformedGeometry("DEAD", 1)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# ModifyUndeformedGeometryModeShape

## Syntax

SapObject.SapModel.Analyze.ModifyUnDeformedGeometryModeShape

## VB6 Procedure

Function ModifyUndeformedGeometryModeShape(ByVal CaseName As String, ByVal Mode As
Integer, ByVal MaxDisp As Double, ByVal Direction As Integer, Optional ByVal Original As
Boolean = False) As Long


## Parameters

CaseName

The name of a modal or buckling load case.

Mode

The mode shape to consider.

MaxDisp

The maximum displacement to which the mode shape will be scaled.

Direction

The direction in which to apply the geometry modification.

Original

If this item is True, all other input items in this function are ignored and the original undeformed
geometry data is reinstated.

## Remarks

This function modifies the undeformed geometry based on the shape of a specified mode from a
specified modal or buckling load case.

The function returns zero if it is successful; otherwise it returns a nonzero value.

## VBA Example

Sub ModifyUndeformedGeometryModeShapeExample()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long
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
ret = SapModel.File.NewBeam(2, 288, False)

'assign point object restraints
Redim Value(5)
For i = 0 to 5
Value(i) = True
Next i
ret = SapModel.PointObj.SetRestraint("1", Value)

'run model
ret = SapModel.File.Save("C:\SapAPI\x.sdb")
ret = SapModel.Analyze.RunAnalysis

'modify undeformed geometry
ret = SapModel.Analyze.ModifyUndeformedGeometryModeShape("MODAL", 1, 1.0, 2)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 17.2.

## See Also

# RunAnalysis

## Syntax

SapObject.SapModel.Analyze.RunAnalysis

## VB6 Procedure

Function RunAnalysis() As Long

## Parameters

None

## Remarks

This function runs the analysis. The analysis model is automatically created as part of this
function.


The function returns zero if the analysis model is successfully run, otherwise it returns a nonzero
value.

**IMPORTANT NOTE:** Your model must have a file path defined before running the analysis. If
the model is opened from an existing file, a file path is defined. If the model is created from
scratch, the File.Save function must be called with a file name before running the analysis. Saving
the file creates the file path.

## VBA Example

Sub RunSapAnalysisModel()
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

'save model
ret = SapModel.File.Save("C:\SapAPI\x.sdb")

'run model (this will create the analysis model)
ret = SapModel.Analyze.RunAnalysis

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

File.Save


BridgeObj.SetBridgeUpdateForAnalysisFlag

# SetActiveDOF

## Syntax

SapObject.SapModel.Analyze.SetActiveDOF

## VB6 Procedure

Function SetActiveDOF(ByRef DOF() As Boolean) As Long

## Parameters

### DOF

This is an array of 6 boolean values, indicating if the specified model global degree of freedom is
active.

```
DOF(0) = UX
DOF(1) = UY
DOF(2) = UZ
DOF(3) = RX
DOF(4) = RY
DOF(5) = RZ
```
## Remarks

This function sets the model global degrees of freedom.

The function returns zero if the degrees of freedom are successfully set; otherwise it returns a
nonzero value.

## VBA Example

Sub SetModelActiveDOF()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'set model degrees of freedom
ReDim DOF(5)
DOF(0) = True
DOF(1) = True
DOF(2) = True
ret = SapModel.Analyze.SetActiveDOF(DOF)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

GetActiveDOF

# SetRunCaseFlag

## Syntax

SapObject.SapModel.Analyze.SetRunCaseFlag

## VB6 Procedure

Function SetRunCaseFlag(ByVal Name As String, ByVal Run As Boolean, Optional ByVal All
As Boolean = False) As Long

## Parameters

Name

The name of an existing load case that is to have its run flag set.

This item is ignored when the All item is True.


Run

If this item is True, the specified load case is to be run.

All

If this item is True, the run flag is set as specified by the Run item for all load cases, and the Name
item is ignored.

## Remarks

This function sets the run flag for load cases.

The function returns zero if the flag is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetRunCaseFlagExample()
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

'set load case run flag
ret = SapModel.Analyze.SetRunCaseFlag("MODAL", False)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.


Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

GetRunCaseFlag

# SetSolverOption_3

## Syntax

SapObject.SapModel.Analyze.SetSolverOption_3

## VB6 Procedure

Function SetSolverOption_3(ByVal SolverType As Long, ByVal SolverProcessType As Long,
ByVal NumberParallelRuns As Long, ByVal ResponseFileSizeMaxMB As Long, , ByVal
NumberAnalysisThreads As Long, Optional ByVal StiffCase As String = "") As Long

## Parameters

**SolverType**

This is 0, 1 or 2, indicating the solver type.

```
0 = Standard solver
1 = Advanced solver
2 = Multi-threaded solver
```
**SolverProcessType**

This is 0, 1 or 2, indicating the process the analysis is run.

```
0 = Auto (program determined)
1 = GUI process
2 = Separate process
```
**NumberParallelRuns**

This is an integer between -8 and 8, inclusive, not including -1.

-8 to -2 = Auto parallel (use up to all physical cores - max 8). Treated the same as 0.
-1 = Illegal value; will return an error.
0 = Auto parallel (use up to all physical cores).
1 = Serial.
2 to 8 = User defined parallel (use up to this fixed number of cores - max 8).

**R** esponseFileSizeMaxMB


The maximum size of a response file in MB before a new response file is created. Positive if user
specified, negative if program determined.

NumberAnalysisThreads

Number of threads that the analysis can use. Positive if user specified, negative if program
determined.

**StiffCase**

The name of the load case used when outputting the mass and stiffness matrices to text files If this
item is blank, no matrices are output.

## Remarks

This function sets the model solver options.

The function returns zero if the options are successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetModelSolverOption()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

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

'set model solver options
ret = SapModel.Analyze.SetSolverOption_3(1, 1, 3, 0, 0 "DEAD")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in v21.1.0.

Modified the allowed values for NumberParallelRuns in v 22.1.0.

Added ResponseFileSizeMaxMB and NumberAnalysisThreads parameters in v 23.2.0.

This function supersedes SetSolverOption_2 , adding the NumberParallelRuns parameter and
removing the previous Force32BitSolver parameter.

## See Also

GetSolverOption_3


