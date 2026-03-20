# ChangeName

## Syntax

SapObject.SapModel.PatternDef.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined joint pattern.

NewName

The new name for the joint pattern.

## Remarks

The function returns zero if the new name is successfully applied, otherwise it returns a nonzero
value.

## VBA Example

Sub ChangePatternName()
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


'change name of group
ret = SapModel.PatternDef.ChangeName("Default", "MyPattern")

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

SapObject.SapModel.PatternDef.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None

## Remarks

The function returns the number of defined joint patterns.

## VBA Example

Sub CountPatterns()
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

'return number of defined joint patterns
ret = SapModel.PatternDef.Count

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

SapObject.SapModel.PatternDef.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing joint pattern.

## Remarks

The function deletes the specified joint pattern. At least one joint pattern must be defined. The
function will return an error if an attempt is made to delete the last joint pattern.

The function returns zero if the joint pattern is successfully deleted, otherwise it returns a nonzero
value.


## VBA Example

Sub DeletePattern()
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

'add joint pattern
ret = SapModel.PatternDef.SetPattern("MyPattern")

'delete joint pattern
ret = SapModel.PatternDef.Delete("MyPattern")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetPattern

# GetNameList

## Syntax

SapObject.SapModel.PatternDef.GetNameList


## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of joint pattern names retrieved by the program.

MyName

This is a one-dimensional array of joint pattern names. The MyName array is created as a
dynamic, zero-based, array by the API user:

Dim MyName() as String

The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined joint patterns.

The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetJointPatternNames()
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

'get joint pattern names
ret = SapModel.PatternDef.GetNameList(NumberNames, MyName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# SetPattern

## Syntax

SapObject.SapModel.PatternDef.SetPattern

## VB6 Procedure

Function SetPattern(ByVal Name As String) As Long

## Parameters

Name

The name of a new joint pattern.

## Remarks

The function defines a new joint pattern. It returns an error if the specified joint pattern name is
already in use.

The function returns zero if the new joint pattern is successfully defined, otherwise it returns a
nonzero value.

## VBA Example

Sub AddPattern()
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

'add joint pattern
ret = SapModel.PatternDef.SetPattern("MyPattern")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also


