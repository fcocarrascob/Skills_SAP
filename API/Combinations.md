# Add

## Syntax

SapObject.SapModel.RespCombo.Add

## VB6 Procedure

Function Add(ByVal Name As String, ByVal ComboType As Long) As Long

## Parameters

Name

The name of a new load combination.

ComboType

This is 0, 1, 2, 3 or 4 indicating the load combination type.

```
0 = Linear Additive
1 = Envelope
2 = Absolute Additive
3 = SRSS
4 = Range Additive
```
## Remarks

This function adds a new load combination.

The function returns zero if the load combination is successfully added, otherwise it returns a
nonzero value.

The new load combination must have a different name from all other load combinations and all
load cases. If the name is not unique, an error will be returned.

## VBA Example

Sub AddNewCombo()
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 1)

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

AddDesignDefaultCombos

# AddDesignDefaultCombos

## Syntax

SapObject.SapModel.RespCombo.AddDesignDefaultCombos

## VB6 Procedure

Function AddDesignDefaultCombos(ByVal DesignSteel As Boolean, ByVal DesignConcrete As
Boolean, ByVal DesignAluminum As Boolean, ByVal DesignColdFormed As Boolean) As Long

## Parameters

DesignSteel


If this item is True, default steel design combinations are to be added to the model.

DesignConcrete

If this item is True, default concrete design combinations are to be added to the model.

DesignAluminum

If this item is True, default aluminum design combinations are to be added to the model.

DesignColdFormed

If this item is True, default cold formed design combinations are to be added to the model.

## Remarks

This function adds a new default design load combinations to the model.

The function returns zero if the load combinations are successfully added, otherwise it returns a
nonzero value.

## VBA Example

Sub AddNewDefaultSteelDesignCombos()
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

'add combo
ret = SapModel.RespCombo.AddDesignDefaultCombos(True, False, False, False)

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

Add

# ChangeName

## Syntax

SapObject.SapModel.RespCombo.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined load combination.

NewName

The new name for the combination.

## Remarks

The function returns zero if the new name is successfully applied, otherwise it returns a nonzero
value.

The new load combination name must be different from all other load combinations and all load
cases. If the name is not unique, an error will be returned.

## VBA Example

Sub ChangeComboName()
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 1)

'change combo name
ret = SapModel.RespCombo.ChangeName("COMB1", "MyCombo")

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

# Count

## Syntax

SapObject.SapModel.RespCombo.Count

## VB6 Procedure

Function Count() As Long

## Parameters

None


## Remarks

This function returns the total number of load combinations defined in the model.

## VBA Example

Sub CountCombos()
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 1)

'return number of combos
Count = SapModel.RespCombo.Count

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


# CountCase

## Syntax

SapObject.SapModel.RespCombo.CountCase

## VB6 Procedure

Function CountCase(ByVal Name As String, ByRef Count As Long) As Long

## Parameters

Name

The name of an existing load combination.

Count

The number of load case and/or combinations included in the specified combination.

## Remarks

This function retrieves the total number of load case and/or combinations included in a specified
load combination.

The function returns zero if the count is successfully retrieved, otherwise it returns a nonzero
value.

## VBA Example

Sub CountComboCases()
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 0)

'add load case to combo
ret = SapModel.RespCombo.SetCaseList("COMB1", LoadCase, "DEAD", 1.4)

'count cases and combos in combo COMB
ret = SapModel.RespCombo.CountCase("COMB1", Count)

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

GetCaseList

SetCaseList

# Delete

## Syntax

SapObject.SapModel.RespCombo.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing load combination.


## Remarks

This function deletes the specified load combination.

The function returns zero if the combination is successfully deleted, otherwise it returns a nonzero
value.

## VBA Example

Sub DeleteCombo()
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 0)

'delete combo
ret = SapModel.RespCombo.Delete("COMB1")

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

Add

# DeleteCase

## Syntax

SapObject.SapModel.RespCombo.DeleteCase

## VB6 Procedure

Function DeleteCase(ByVal Name As String, ByVal CType As eCNameType, ByVal CName As
String) As Long

## Parameters

Name

The name of an existing load combination.

CType

This is one of the following items in the eCNameType enumeration:

```
LoadCase = 0
LoadCombo = 1
```
This item indicates whether the CName item is an analysis case (LoadCase) or a load combination
(LoadCombo).

CName

The name of the load case or load combination to be deleted from the specified combination.

## Remarks

This function deletes one load case or load combination from the list of cases included in the
specified load combination.

The function returns zero if the item is successfully deleted, otherwise it returns a nonzero value.

## VBA Example

Sub DeleteComboCase()
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 0)

'add load case to combo
ret = SapModel.RespCombo.SetCaseList("COMB1", eCNameType_LoadCase, "DEAD", 1.4)

'delete load case from combo
ret = SapModel.RespCombo.DeleteCase("COMB1", eCNameType_LoadCase, "DEAD")

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

GetCaseList

SetCaseList

# GetCaseList

## Syntax

SapObject.SapModel.RespCombo.GetCaseList


## VB6 Procedure

Function GetCaseList(ByVal Name As String, ByRef NumberItems As Long, ByRef CType() As
eCNameType, ByRef CName() As String, ByRef SF() As Double) As Long

## Parameters

Name

The name of an existing load combination.

NumberItems

The total number of load cases and load combinations included in the load combination specified
by the Name item.

CType

This is an array of one of the following items in the eCNameType enumeration:

```
LoadCase = 0
LoadCombo = 1
```
This item indicates if the associated CName item is an load case (LoadCase) or a load
combination (LoadCombo).

CName

This is an array of the names of the load cases or load combinations included in the load
combination specified by the Name item.

SF

The scale factor multiplying the case or combination indicated by the CName item.

## Remarks

This function returns all load cases and response combinations included in the load combination
specified by the Name item.

The function returns zero if the data is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

Sub GetCasesInCombo()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim CType() As eCNameType


Dim CName() As String
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 0)

'add load case to combo
ret = SapModel.RespCombo.SetCaseList("COMB1", eCNameType_LoadCase, "DEAD", 1.4)

'get all cases and combos included in combo COMB
ret = SapModel.RespCombo.GetCaseList("COMB1", NumberItems, CType, CName, SF)

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

SetCaseList

# GetNameList

## Syntax

SapObject.SapModel.RespCombo.GetNameList


## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of load combination names retrieved by the program.

MyName

This is a one-dimensional array of load combination names. The MyName array is created as a
dynamic, zero-based, array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined response combinations.

The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetComboNames()
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


'add combos
ret = SapModel.RespCombo.Add("COMB1", 0)
ret = SapModel.RespCombo.Add("COMB2", 2)

'get combo names
ret = SapModel.RespCombo.GetNameList(NumberNames, MyName)

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

# GetNote

## Syntax

SapObject.SapModel.RespCombo.GetNote

## VB6 Procedure

Function GetNote(ByVal Name As String, ByRef Note As String) As Long

## Parameters

Name

The name of an existing load combination.

Note

The user note, if any, included with the specified combination.

## Remarks

This function retrieves the user note for specified response combination. The note may be blank.

The function returns zero if the note is successfully retrieved, otherwise it returns a nonzero value.


## VBA Example

Sub GetComboNote()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Note As String

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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 0)

'add note to combo
ret = SapModel.RespCombo.SetNote("COMB1", "My combo note")

'get note for combo
ret = SapModel.RespCombo.GetNote("COMB1", Note)

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

SetNote


# GetTypeOAPI

## Syntax

SapObject.SapModel.RespCombo.GetTypeOAPI

## VB6 Procedure

Function GetTypeOAPI(ByVal Name As String, ByRef ComboType As Long) As Long

## Parameters

Name

The name of an existing load combination.

ComboType

This is 0, 1, 2, 3 or 4 indicating the load combination type.

```
0 = Linear Additive
1 = Envelope
2 = Absolute Additive
3 = SRSS
4 = Range Additive
```
## Remarks

This function retrieves the combination type for specified load combination.

The function returns zero if the type is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

Sub GetComboType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim ComboType As Long

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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 2)

'get combo type
ret = SapModel.RespCombo.GetTypeOAPI("COMB1", ComboType )

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Changed function name to GetTypeOAPI in v17.0.0.

## See Also

SetTypeOAPI

# SetCaseList

## Syntax

SapObject.SapModel.RespCombo.SetCaseList

## VB6 Procedure

Function SetCaseList(ByVal Name As String, ByRef CNameType As eCNameType, ByVal
CName As String, ByVal SF As Double) As Long

## Parameters

Name

The name of an existing load combination.


CNameType

This is one of the following items in the eCNameType enumeration:

```
LoadCase = 0
LoadCombo = 1
```
This item indicates if the CName item is an load case (LoadCase) or a load combination
(LoadCombo).

CName

The name of the load case or load combination to be added to or modified in the combination
specified by the Name item. If the load case or combination already exists in the combination
specified by the Name item, the scale factor is modified as indicated by the SF item for that load
case or combination. If the analysis case or combination does not exist in the combination
specified by the Name item, it is added.

SF

The scale factor multiplying the case or combination indicated by the CName item.

## Remarks

This function adds or modifies one load case or response combination in the list of cases included
in the load combination specified by the Name item.

The function returns zero if the item is successfully added or modified, otherwise it returns a
nonzero value.

## VBA Example

Sub AddCaseToCombo()
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 0)

'add load case to combo
ret = SapModel.RespCombo.SetCaseList("COMB1", eCNameType_LoadCase, "DEAD", 1.4)

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

GetCaseList

# SetNote

## Syntax

SapObject.SapModel.RespCombo.SetNote

## VB6 Procedure

Function SetNote(ByVal Name As String, ByVal Note As String) As Long

## Parameters

Name

The name of an existing load combination.

Note

The user note included with the specified combination. It may be a blank string.

## Remarks

This function sets the user note for specified response combination. The note may be blank.


The function returns zero if the note is successfully set, otherwise it returns a nonzero value.

## VBA Example

Sub AddComboNote()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Note As String

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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 0)

'add note to combo
ret = SapModel.RespCombo.SetNote("COMB1", "My combo note")

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

GetNote


# SetTypeOAPI

## Syntax

SapObject.SapModel.RespCombo.SetTypeOAPI

## VB6 Procedure

Function SetTypeOAPI(ByVal Name As String, ByVal ComboType As Long) As Long

## Parameters

Name

The name of an existing load combination.

ComboType

This is 0, 1, 2, 3 or 4 indicating the load combination type.

```
0 = Linear Additive
1 = Envelope
2 = Absolute Additive
3 = SRSS
4 = Range Additive
```
## Remarks

This function sets the combination type for specified load combination.

The function returns zero if the type is successfully set, otherwise it returns a nonzero value.

## VBA Example

Sub SetComboType()
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

'add combo
ret = SapModel.RespCombo.Add("COMB1", 0)

'set combo type to Envelope
ret = SapModel.RespCombo.SetTypeOAPI("COMB1", 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

Changed function name to SetTypeOAPI in v17.0.0.

## See Also

GetTypeOAPI


