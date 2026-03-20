# ApplyEditedTables

## Syntax

cDatabaseTables.ApplyEditedTables

## VB6 Procedure

Function ApplyEditedTables (FillImportLog As Boolean, ByRef NumFatalErrors As Integer, ByRef NumErrorMsgs
As Integer, ByRef NumWarnMsgs As Integer, ByRef NumInfoMsgs As Integer, ByRef ImportLog As String ) As
Integer

## Parameters

FillImportLog

Whether the ImportLog string should be filled. Please note that the import log may be very large.

```
0 = Import log not requested
1 = Import log requested
```
NumFatalErrors

Returned Item: The number of fatal errors that occurred during the import

NumErrorMsgs

Returned Item: The number of error messages logged during the import

NumWarnMsgs

Returned Item: The number of warning messages logged during the import

NumInfoMsgs

Returned Item: The number of informational messages logged during the import

ImportLog

Returned Item: A string containing all messages logged during the import

## Remarks

Instructs the program to interactively import all of the tables stored in the table list using the SetTableForEditing...
functions.

If the model is locked at the time this command is called then only tables that can be interactively imported when the
model is locked will be imported.

## Release Notes

Initial release in version 23.0.

## See Also

SetTableForEditingArray

SetTableForEditingCSVFile


SetTableForEditngCSVString

# CancelTableEditing

## Syntax

cDatabaseTables.CancelTableEditing

## VB6 Procedure

Function CancelTableEditing As Integer

## Parameters

## Remarks

Clears all tables that were stored in the table list using one of the SetTableForEditing... functions.

Returns 0 if the function executes correctly, otherwise returns nonzero.

## Release Notes

Initial release in version 23.0.

## See Also

SetTableForEditingArray

SetTableForEditingCSVFile

SetTableForEditngCSVString

# GetAllFieldsinTable

## Syntax

cDatabaseTables.GetAllFieldsInTable

## VB6 Procedure

Function GetAllFieldsInTable (TableKey As String, ByRef TableVersion As Integer, ByRef NumberFields As Integer,
ByRef FieldKey As String(), FieldName As String(), ByRef Description As String(), ByRef UnitsString As String(),
ByRef IsImportable As Boolean() ) As Integer

## Parameters

TableKey

Input Item: The table key for the table for which the fields will be returned.

TableVersion

Returned Item: The version number of the specified table.


NumberFields

Returned Item: The number of available fields in the specified table.

FieldKey

Returned Item: A zero-based array of the field keys for the specified table

FieldName

Returned Item: A zero-based array of the field names for the specified table

Description

Returned Item: A zero-based array of the field descriptions for the specified table

UnitsString

Returned Item: A zero-based array of the field units for the specified table.

IsImportable

Returned Item: A zero-based array of whether the field is importable for the specified table

## Remarks

Returns the available fields in a specified table.

## Release Notes

Initial release in version 23.0.

## See Also

# GetAllTables

## Syntax

cDatabaseTables.GetAllTables

## VB6 Procedure

Function GetAllTables (ByRef NumberTables As Integer, ByRef TableKey As As String(), ByRef TableName As As
String(), ByRef ImportType As Integer (), IsEmpty As Boolean() ) As Integer

## Parameters

NumberTables

Returned Item: The number of tables that are currently available for display.

TableKey

Returned Item: zero-based array of the table keys for the available tables.

TableName

Returned Item: A zero-based array of the table names for the available tables.


ImportType

Returned Item: This is either 0, 1, 2 or 3 indicating the import type for the table.

0= not importable

1= importable, but not interactively importable

2= importable and interactive importable when he model is unlocked

3= importable and interactive importable when he model is unlocked and locked

IsEmpty

Returned Item: False means data is available in the model to fill the table. True means there is no data in the model to
fill the table.

## Remarks

Returns all of the tables along with their import type and indicates if any data is available in the model to fill the table.

## Release Notes

Initial release in version 23.0.

## See Also

GetAvailableTables

# GetAvailableTables

## Syntax

cDatabaseTables.GetAvailableTables

## VB6 Procedure

Function GetAvailableTables(ByRef NumberTables As Integer, ByRef TableKey As As String(), ByRef TableName
As As String(), ByRef ImportType As Integer () ) As Integer

## Parameters

NumberTables

Returned Item: The number of tables that are currently available for display.

TableKey

Returned Item: zero-based array of the table keys for the available tables.

TableName

Returned Item: A zero-based array of the table names for the available tables.

ImportType

Returned Item: This is either 0, 1, 2 or 3 indicating the import type for the table.


0= not importable

1= importable, but not interactively importable

2= importable and interactive importable when he model is unlocked

3= importable and interactive importable when he model is unlocked and locked

## Remarks

Returns a list of load cases that are selected for table display.

## Release Notes

Initial release in version 23.0.

## See Also

GetAllTables

# GetElementVirtualWorkNamedSetsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay

## VB6 Procedure

Function GetElementVirtualWorkNamedSetsSelectedForDisplay (ByRef
NumberSelectedElementVirtualWorkNamedSets As Integer, ByRef ElementVirtualWorkNamedSetList() As String)
As Integer

## Parameters

NumberSelectedElementVirtualWorkNamedSets

The number of element virtual work named sets selected for display in the analysis result tables.

ElementVirtualWorkNamedSetList

A zero-based list of the names of the element virtual work named sets selected for display in the analysis result tables.

## Remarks

This function returns the element virtual work named sets selected for display in the analysis result tables.

The function returns zero if the information is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists.

Sub GetElementVirtualWorkNamedSetSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim FileName As String
Dim NumberItems As Integer
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

'get element virtual work named sets selected for display in the analysis result tables
ret = SapModel. DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay (NumberItems, ItemList)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

SetElementVirtualWorkNamedSetsSelectedForDisplay

# GetGeneralizedDisplacementsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay

## VB6 Procedure

Function GetGeneralizedDisplacementsSelectedForDisplay (ByRef NumberSelectedGeneralizedDisplacements As
Integer, ByRef GeneralizedDisplacementList() As String) As Integer

## Parameters

NumberSelectedGeneralizedDisplacements

The number of generalized displacements selected for display in the analysis result tables.

GeneralizedDisplacementList

A zero-based list of the names of the generalized displacements selected for display in the analysis result tables.


## Remarks

This function returns the generalized displacements selected for display in the analysis result tables.

The function returns zero if the information is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists.

Sub GetGeneralizedDisplacementSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim NumberItems As Integer
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

'get generalized displacements selected for display in the analysis result tables
ret = SapModel. DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay (NumberItems, ItemList)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

SetGeneralizedDisplacementsSelectedForDisplay

# GetJointResponseSpectraNamedSetsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay


## VB6 Procedure

Function GetJointResponseSpectraNamedSetsSelectedForDisplay (ByRef
NumberSelectedJointResponseSpectraNamedSets As Integer, ByRef JointResponseSpectraNamedSetList() As String)
As Integer

## Parameters

NumberSelectedJointResponseSpectraNamedSets

The number of joint response spectra named sets selected for display in the analysis result tables.

JointResponseSpectraNamedSetList

A zero-based list of the names of the joint response spectra named sets selected for display in the analysis result tables.

## Remarks

This function returns the joint response spectra named sets selected for display in the analysis result tables.

The function returns zero if the information is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists.

Sub GetJointResponseSpectraNamedSetSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim NumberItems As Integer
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

'get joint response spectra named sets selected for display in the analysis result tables
ret = SapModel. DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay (NumberItems,
ItemList)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 23.00.

## See Also

SetJointResponseSpectraNamedSetsSelectedForDisplay

# GetLoadCasesSelectedForDisplay

## Syntax

cDatabaseTables.GetLoadCasesSelectedForDisplay

## VB6 Procedure

Function GetLoadCasesSelectedForDisplay (ByRef NumberSelectedLoadCases As Integer, ByRef LoadCaseList As
As String()) As Integer

## Parameters

NumberSelectedLoadCases

Returned Item: The number of load cases selected for table display.

LoadCaseList

Returned Item: The zero-based list of load cases selected for table display.

## Remarks

Returns a list of load cases that are selected for table display.

This list sets the load cases that are included when displaying load assignments on the model.

## Release Notes

Initial release in version 23.0.

## See Also

SetLoadCasesSelectedForDisplay

# GetLoadCombinationsSelectedForDisplay

## Syntax

cDatabaseTables.GetLoadCombinationsSelectedForDisplay

## VB6 Procedure

Function GetLoadCombinationsSelectedForDisplay (ByRef NumberSelectedLoadCombinations As Integer, ByRef
LoadCombinationList As As String()) As Integer


## Parameters

NumberSelectedLoadCombinations

Returned Item: The number of load combinations selected for table display.

LoadCombinationList

Returned Item: The zero-based list of load combinations selected for table display.

## Remarks

Returns a list of load combinations that are selected for table display.

This list sets the load combinations that are included when displaying load assignments on the model.

## Release Notes

Initial release in version 23.0.

## See Also

SetLoadCombinationsSelectedForDisplay

# GetLoadPatternsSelectedForDisplay

## Syntax

cDatabaseTables.GetLoadPatternsSelectedForDisplay

## VB6 Procedure

Function GetLoadPatternsSelectedForDisplay (ByRef NumberSelectedLoadPatterns As Integer, ByRef
LoadPatternList As As String()) As Integer

## Parameters

NumberSelectedLoadPatterns

Returned Item: The number of load pattern selected for table display.

LoadPatternList

Returned Item: The zero-based list of load patterns selected for table display.

## Remarks

Returns a list of load patterns that are selected for table display.

This list sets the load patterns that are included when displaying load assignments on the model.

## Release Notes

Initial release in version 23.0.


## See Also

SetLoadPatternsSelectedForDisplay

# GetObsoleteTableKeyList

## Syntax

SapObject.DatabaseTables.GetObsoleteTableKeyList

## VB6 Procedure

Function GetObsoleteTableKeyList(ByRef NumberTableKeys As Long, ByRef TableKeyList() As String, ByRef
NotesList() As String) As Long

## Parameters

NumberTableKeys

```
The number of obsolete table keys for the program.
```
TableKeyList

```
A zero-based array of the obsolete table keys in the program.
```
NotesList

```
A zero-based array of notes associated with each obsolete table key.
```
## Remarks

This function retrieves a list of obsolete table keys for the program.

The function returns zero if the list is successfully retrieved; otherwise it returns nonzero value.

## VBA Example

Sub GetObsoleteTableKeys()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberTableKeys As Long
Dim TableKeyList() As String
Dim NotesList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel


'initialize model
ret = SapModel.InitializeNewModel

'create a template model
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'get obsolete table key data
ret = SapModel.DatabaseTables. GetObsoleteTableKeyList(NumberTableKeys, TableKeyList, NotesList)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.20.

# GetPlotFunctionTracesNamedSetsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay

## VB6 Procedure

Function GetPlotFunctionTracesNamedSetsSelectedForDisplay (ByRef
NumberSelectedPlotFunctionTracesNamedSets As Integer, ByRef PlotFunctionTracesNamedSetList() As String) As
Integer

## Parameters

NumberSelectedPlotFunctionTracesNamedSets

The number of plot function traces named sets selected for display in the analysis result tables.

PlotFunctionTracesNamedSetList

A zero-based list of the names of the plot function traces named sets selected for display in the analysis result tables.

## Remarks

This function returns the plot function traces named sets selected for display in the analysis result tables.

The function returns zero if the information is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists.

Sub GetPlotFunctionTracesNamedSetSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim FileName As String
Dim NumberItems As Integer
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

'get plot function traces named sets selected for display in the analysis result tables
ret = SapModel. DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay (NumberItems, ItemList)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

SetPlotFunctionTracesNamedSetsSelectedForDisplay

# GetPushoverNamedSetsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.GetPushoverNamedSetsSelectedForDisplay

## VB6 Procedure

Function GetPushoverNamedSetsSelectedForDisplay (ByRef NumberSelectedPushoverNamedSets As Integer, ByRef
PushoverNamedSetList() As String) As Integer

## Parameters

NumberSelectedPushoverNamedSets

The number of pushover named sets selected for display in the analysis result tables.

PushoverNamedSetList

A zero-based list of the names of the pushover named sets selected for display in the analysis result tables.


## Remarks

This function returns the pushover named sets selected for display in the analysis result tables.

The function returns zero if the information is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists.

Sub GetPushoverNamedSetSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim NumberItems As Integer
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

'get pushover named sets selected for display in the analysis result tables
ret = SapModel. DatabaseTables.GetPushoverNamedSetsSelectedForDisplay (NumberItems, ItemList)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

SetPushoverNamedSetsSelectedForDisplay

# GetSectionCutsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.GetSectionCutsSelectedForDisplay


## VB6 Procedure

Function GetSectionCutsSelectedForDisplay (ByRef NumberSelectedSectionCuts As Integer, ByRef SectionCutList()
As String) As Integer

## Parameters

NumberSelectedSectionCuts

The number of section cuts selected for display in the analysis result tables.

SectionCutList

A zero-based list of the names of the section cuts selected for display in the analysis result tables.

## Remarks

This function returns the section cuts selected for display in the analysis result tables.

The function returns zero if the information is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists.

Sub GetSectionCutSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim NumberItems As Integer
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

'get section cuts selected for display in the analysis result tables
ret = SapModel. DatabaseTables.GetSectionCutsSelectedForDisplay (NumberItems, ItemList)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes


Initial release in version 23.00.

## See Also

SetSectionCutsSelectedForDisplay

# GetTableForDisplayArray

## Syntax

cDatabaseTables.GetTableForDisplayArray

## VB6 Procedure

Function GetTableForDisplayArray (TableKey As String(), ByRef FieldKeyList As String(), GroupName As String(),
ByRef TableVersion As Integer, ByRef FieldKeysIncluded As String(), ByRef NumberRecords As Integer, ByRef
TableData As String() ) As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

FieldKeyList

Input Item: A zero-based array listing the field keys associated with the specified table for which data is requested.

GroupName

Input Item: The name of the group for which data will be returned.

TableVersion

Returned Item: The version number of the specified table.

FieldKeysIncluded

Returned Item: A zero-based array listing the field keys associated with the specified table for which data is reported in
the order it is reported in the TableData array. These are essentially the column headers of the data returned in
TableData.

NumberRecords

Returned Item: The number of records of data returned for each field. This is essentially the number of rows of data.

TableData

Returned Item: A zero-based, one-dimensional array of the table data, excluding headers, returned row by row. The
format of the data is explained below.

As an example, suppose there are three fields in the FieldsKeysIncluded array and the NumberRecords is five.

```
EXAMPLE Material Name Type Density
```
```
A992Fy50 Steel 490
```
```
4000Psi Concrete 150
```

```
A615Gr60 Rebar 480
```
```
A416Gr270 Tendon 470
```
```
6061T6 Aluminum 170
```
The data is returned row by row, and items 0 thru 2 in this array would be the first row, items 3 thru 5 the second row,
etc, and items 12 thru 14 the fifth row. Using the example of the table above, the returned array would look like this:
(A992Fy50, Steel, 490, 4000Psi, Concrete, 150, A615Gr60, Rebar, 480, A416Gr270, Tendon, 470, 6061T6,
Aluminum, 170)

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.

Returns data for a single table in a single array. If there is nothing to be shown in the table then no data is returned

If the FieldKeyList array contains a single blank string the data will be provided for all fields. If the GroupName is All,
or a blank string, then data will be returned for all applicable objects in the model.

## Release Notes

Initial release in version 23.0.

## See Also

GetTableForEditingArray

# GetTableForDisplayCSVFile

## Syntax

cDatabaseTables.GetTableForDisplayCSVFile

## VB6 Procedure

Function GetTableForDisplayCSVFile (TableKey As String(), ByRef FieldKeyList As String(), GroupName As String
(), ByRef TableVersion As Integer, csvFilePath As String(), Optional sepChar as string = ",") As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

FieldKeyList

Input Item: A zero-based array listing the field keys associated with the specified table for which data is requested.

GroupName

Input Item: The name of the group for which data will be returned.

TableVersion

Returned Item: The version number of the specified table.


csvFilePath

Input Item: The fully-qualified path for the CSV file containing the table data.

sepChar (Optional)

Optional Input Item: The delimiter between data items, by default ","

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.

Returns data for a single table in a CSV file. If there is nothing to be shown in the table then no data is returned

If the FieldKeyList array contains a single blank string the data will be provided for all fields. If the GroupName is All,
or a blank string, then data will be returned for all applicable objects in the model.

## Release Notes

Initial release in version 23.0.

## See Also

GetTableForEditingCSVFile

# GetTableForDisplayCSVString

## Syntax

cDatabaseTables.GetTableForDisplayCSVString

## VB6 Procedure

Function GetTableForDisplayCSVString (TableKey As String(), ByRef FieldKeyList As String(), GroupName As
String(), ByRef TableVersion As Integer, csvString As String(), Optional sepChar as string = ",") As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

FieldKeyList

Input Item: A zero-based array listing the field keys associated with the specified table for which data is requested.

GroupName

Input Item: The name of the group for which data will be returned.

TableVersion

Returned Item: The version number of the specified table.

csvString

Input Item: A CSV-formatted string containing all the table data.

sepChar (Optional)


Optional Input Item: The delimiter between data items, by default ","

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.

Returns data for a single table in a CSV string. If there is nothing to be shown in the table then no data is returned

If the FieldKeyList array contains a single blank string the data will be provided for all fields. If the GroupName is All,
or a blank string, then data will be returned for all applicable objects in the model.

## Release Notes

Initial release in version 23.0.

## See Also

GetTableForEditingCSVString

# GetTableForDisplayXMLString

## Syntax

cDatabaseTables.GetTableForDisplayXMLString

## VB6 Procedure

Function GetTableForDisplayXMLString (TableKey As String, ByRef FieldKeyList As String(), GroupName As
String(), IncludeSchema As Boolean, ByRef TableVersion As Integer, ByRef XMLTableData As String) As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

FieldKeyList

Input Item: A zero-based array listing the field keys associated with the specified table for which data is requested.

GroupName

Input Item: The name of the group for which data will be returned.

IncludeSchema

Input Item: Flag indicating if the schema should be included with the table data.

TableVersion

Returned Item: The version number of the specified table.

XMLTableData

Returned Item: A string containing the XML data for the table.

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.


Returns data for a single table as XML in a single string. If there is nothing to be shown in the table then no data is
returned

If the FieldKeyList array contains a single blank string the data will be provided for all fields. If the GroupName is All,
or a blank string, then data will be returned for all applicable objects in the model.

## Release Notes

Initial release in version 23.0.

## See Also

# GetTableForEditingArray

## Syntax

cDatabaseTables.GetTableForEditingArray

## VB6 Procedure

Function GetTableForEditingArray (TableKey As String(), GroupName As String(), ByRef TableVersion As Integer,
ByRef FieldKeysIncluded As String(), ByRef NumberRecords As Integer, ByRef TableData As String()) As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

GroupName

Input Item: The name of the group for which data will be returned.

TableVersion

Returned Item: The version number of the specified table.

FieldKeysIncluded

Returned Item: A zero-based array listing the field keys associated with the specified table for which data is reported in
the order it is reported in the TableData array. These are essentially the column headers of the data returned in
TableData.

NumberRecords

Returned Item: The number of records of data returned for each field. This is essentially the number of rows of data.

TableData

Returned Item: A zero-based, one-dimensional array of the table data, excluding headers, returned row by row. The
format of the data is explained below.

As an example, suppose there are three fields in the FieldsKeysIncluded array and the NumberRecords is five.

```
EXAMPLE Material Name Type Density
```
```
A992Fy50 Steel 490
```
```
4000Psi Concrete 150
```

```
A615Gr60 Rebar 480
```
```
A416Gr270 Tendon 470
```
```
6061T6 Aluminum 170
```
The data is returned row by row, and items 0 thru 2 in this array would be the first row, items 3 thru 5 the second row,
etc, and items 12 thru 14 the fifth row. Using the example of the table above, the returned array would look like this:
(A992Fy50, Steel, 490, 4000Psi, Concrete, 150, A615Gr60, Rebar, 480, A416Gr270, Tendon, 470, 6061T6,
Aluminum, 170)

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.

Returns a single table in a string array for interactive editing.

## Release Notes

Initial release in version 23.0.0

## See Also

SetTableForEditingArray

# GetTableForEditingCSVFile

## Syntax

cDatabaseTables.GetTableForEditingCSVFile

## VB6 Procedure

Function GetTableForEditingCSVFile (TableKey As String(), GroupName As String(), ByRef TableVersion As
Integer, csvFilePath As String, Optional sepChar as string = ",") As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

GroupName

Input Item: The name of the group for which data will be returned.

TableVersion

Returned Item: The version number of the specified table.

csvFilePath

Input Item: The fully-qualified path for the CSV file containing the table data.

sepChar (Optional)

Optional Input Item: The delimiter between data items, by default ","


## Remarks:

Returns a single table in a CSV file for interactive editing.

Returns a single table in a string array for interactive editing.

## Release Notes

Initial release in version 23.0.0

## See Also

SetTableForEditingCSVFile

# GetTableForEditingCSVString

## Syntax

cDatabaseTables.GetTableForEditingCSVString

## VB6 Procedure

Function GetTableForEditingCSVString (TableKey As String, GroupName As String, ByRef TableVersion As Integer,
ByRef csvString As String, Optional sepChar as string = ",") As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

GroupName

Input Item: The name of the group for which data will be returned.

TableVersion

Returned Item: The version number of the specified table.

csvString

Input Item: A CSV-formatted string containing all the table data.

sepChar (Optional)

Optional Input Item: The delimiter between data items, by default ","

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.

Returns a single table in a string array for interactive editing.

## Release Notes

Initial release in version 23.0.0


## See Also

SetTableForEditingCSVFile

# GetTableOutputOptionsForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.GetTableOutputOptionsForDisplay

## VB6 Procedure

Function GetTableOutputOptionsForDisplay (ByRef BaseReactionGX As Double, ByRef BaseReactionGY As
Double, ByRef BaseReactionGZ As Double, ByRef IsAllModes As Boolean, ByRef StartMode As Integer, ByRef
EndMode As Integer, ByRef IsAllBucklingModes As Boolean, ByRef StartBucklingMode As Integer, ByRef
EndBucklingMode As Integer, ByRef ModalHistory As Integer, ByRef DirectHistory As Integer, ByRef
NonlinearStatic As Integer, ByRef MultistepStatic As Integer, ByRef SteadyState As Integer, ByRef
SteadyStateOption As Integer, ByRef PowerSpectralDensity As Integer, ByRef Combo As Integer, ByRef
BridgeDesign As Integer) As Integer

## Parameters

BaseReactionGX

The global X coordinate of the base reaction location.

BaseReactionGY

The global Y coordinate of the base reaction location.

BaseReactionGZ

The global Z coordinate of the base reaction location.

IsAllModes

This item is true if results are displayed for all modes of modal load cases.

StartMode

The first mode for which results are shown for modal load cases. This item only applies when the IsAllModes item is
False.

EndMode

The last mode for which results are shown for modal load cases. This item only applies when the IsAllModes item is
False.

IsAllBucklingModes

This item is true if results are displayed for all modes of buckling load cases.

StartBucklingMode

The first mode for which results are shown for buckling load cases. This item only applies when the
IsAllBucklingModes item is False.

EndBucklingMode

The last mode for which results are shown for buckling load cases. This item only applies when the
IsAllBucklingModes item is False.


ModalHistory

Indicates how multistep modal time history load case results are displayed: 1=Envelopes, 2=Step-by-step, 3=Last Step.

DirectHistory

Indicates how direct integration time history load case results are displayed: 1=Envelopes, 2=Step-by-step, 3=Last
Step.

NonlinearStatic

Indicates how nonlinear static load case results are displayed: 1=Envelopes, 2=Step-by-step, 3=Last Step.

MultistepStaticStatic

Indicates how multistep static load case results are displayed: 1=Envelopes, 2=Step-by-step, 3=Last Step.

SteadyState

Indicates how steady state load case results are displayed: 1=Envelopes, 2=At Frequencies.

SteadyStateOption

Indicates how type of steady state load case results displayed: 1=In and Out of Phase, 2=Magnitude, 3=All.

PowerSpectralDensity

Indicates how power spectral density load case results are displayed: 1=RMS, 2=sqrt(PSD).

Combo

Indicates how load combination results are displayed: 1=Envelopes, 2=Multiple Values If Possible, 3=Correspondence.

BridgeDesign

Indicates which bridge design results are displayed: 1=Controlling Combo, 2=All Combos.

## Remarks

This function returns the output option data used for display of analysis result tables.

The function returns zero if the information is successfully retrieved, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists.

Sub GetTableOutputOptions()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim BaseReactionGX As Double
Dim BaseReactionGY As Double
Dim BaseReactionGZ As Double
Dim IsAllModes As Boolean
Dim StartMode As Integer
Dim EndMode As Integer
Dim IsAllBucklingModes As Boolean
Dim StartBucklingMode As Integer
Dim EndBucklingMode As Integer
Dim ModalHistory As Integer
Dim DirectHistory As Integer
Dim NonlinearStatic As Integer


Dim MultistepStatic As Integer
Dim SteadyState As Integer
Dim SteadyStateOption As Integer
Dim PowerSpectralDensity As Integer
Dim Combo As Integer
Dim BridgeDesign As Integer

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

'get table output options used for display in the analysis result tables
ret = SapModel. DatabaseTables.GetTableOutputOptionsForDisplay (BaseReactionGX, BaseReactionGY,
BaseReactionGZ, IsAllModes, StartMode, EndMode, IsAllBucklingModes,

StartBucklingMode, EndBucklingMode, ModalHistory, DirectHistory, NonlinearStatic, MultistepStatic, SteadyState,
SteadyStateOption, PowerSpectralDensity, Combo, BridgeDesign)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

SetTableOutputOptionsForDisplay

# SetElementVirtualWorkNamedSetsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay

## VB6 Procedure

Function SetElementVirtualWorkNamedSetsSelectedForDisplay (ByRef ElementVirtualWorkNamedSetList() As
String) As Integer

## Parameters


ElementVirtualWorkNamedSetList

The zero-based list of element virtual work named sets selected for table display.

## Remarks

This function sets the element virtual work named sets that are included when displaying analysis results. If no element
virtual work named sets are to be selected then the list should include a blank string.

The function returns zero if the information is successfully set, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists and that it contains element virtual work named sets named Set1
and Set2.

Sub SetElementVirtualWorkNamedSetSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

fill ItemList
Redim ItemList(1)
ItemList(0) = Set1
ItemList(1) = Set2

'set element virtual work named sets selected for display in the analysis result tables
ret = SapModel. DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay(ItemList)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

GetElementVirtualWorkNamedSetsSelectedForDisplay


# SetGeneralizedDisplacementsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay

## VB6 Procedure

Function SetGeneralizedDisplacementsSelectedForDisplay (ByRef GeneralizedDisplacementList() As String) As
Integer

## Parameters

GeneralizedDisplacementList

The zero-based list of generalized displacements selected for table display.

## Remarks

This function sets the generalized displacements that are included when displaying analysis results. If no generalized
displacements are to be selected then the list should include a blank string.

The function returns zero if the information is successfully set, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists and that it contains generalized displacements named GDisp1
and GDisp2.

Sub SetGeneralizedDisplacementSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

fill ItemList
Redim ItemList(1)
ItemList(0) = GDisp1
ItemList(1) = GDisp2


'set generalized displacements selected for display in the analysis result tables
ret = SapModel. DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay(ItemList)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

GetGeneralizedDisplacementsSelectedForDisplay

# SetJointResponseSpectraNamedSetsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay

## VB6 Procedure

Function SetJointResponseSpectraNamedSetsSelectedForDisplay (ByRef JointResponseSpectraNamedSetList() As
String) As Integer

## Parameters

JointResponseSpectraNamedSetList

The zero-based list of joint response spectra named sets selected for table display.

## Remarks

This function sets the joint response spectra named sets that are included when displaying analysis results. If no joint
response spectra named sets are to be selected then the list should include a blank string.

The function returns zero if the information is successfully set, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists and that it contains joint response spectra named sets named Set1
and Set2.

Sub SetJointResponseSpectraNamedSetSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim ItemList() As String

'create Sap2000 object


Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

fill ItemList
Redim ItemList(1)
ItemList(0) = Set1
ItemList(1) = Set2

'set joint response spectra named sets selected for display in the analysis result tables
ret = SapModel. DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay(ItemList)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

GetJointResponseSpectraNamedSetsSelectedForDisplay

# SetLoadCasesSelectedForDisplay

## Syntax

cDatabaseTables.SetLoadCasesSelectedForDisplay

## VB6 Procedure

Function SetLoadCasesSelectedForDisplay (ByRef LoadCaseList As As String() ) As Integer

## Parameters

LoadCaseList

Returned Item: The zero-based list of load cases selected for table display.

## Remarks

Sets the load cases that are selected for table display. Returns a 0 if the function executes correctly.


This list sets the load cases that are included when displaying analysis results. If no load cases are to be selected then
the LoadCaseList item should include a single blank string.

## Release Notes

Initial release in version 23.0.0

## See Also

GetLoadCasesSelectedForDisplay

# SetLoadCombinationsSelectedForDisplay

## Syntax

cDatabaseTables.SetLoadCombinationsSelectedForDisplay

## VB6 Procedure

Function SetLoadCombinationsSelectedForDisplay (ByRef LoadCombinationList As As String()) As Integer

## Parameters

LoadCombinationList

Returned Item: The zero-based list of load combinations selected for table display.

## Remarks

Sets the load combinations that are selected for table display. Returns a 0 if the function executes correctly.

This list sets the load combinations that are included when displaying analysis results. If no load combinations are to
be selected then the LoadCombinationList item should include a single blank string.

## Release Notes

Initial release in version 23.0.0

## See Also

GetLoadCombinationsSelectedForDisplay

# SetLoadPatternsSelectedForDisplay

## Syntax

cDatabaseTables.SetLoadPatternsSelectedForDisplay

## VB6 Procedure

Function SetLoadPatternsSelectedForDisplay (ByRef LoadPatternList As As String()) As Integer


## Parameters

LoadCombinationList

Returned Item: The zero-based list of load patterns selected for table display.

## Remarks

Sets the load patterns that are selected for table display. Returns a 0 if the function executes correctly.

This list sets the load patterns that are included when displaying load assignments on the model. If no load patterns are
to be selected then the LoadPatternList item should include a single blank string.

## Release Notes

Initial release in version 23.0.0

## See Also

GetLoadPatternsSelectedForDisplay

# SetPlotFunctionTracesNamedSetsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay

## VB6 Procedure

Function SetPlotFunctionTracesNamedSetsSelectedForDisplay (ByRef PlotFunctionTracesNamedSetList() As String)
As Integer

## Parameters

PlotFunctionTracesNamedSetList

The zero-based list of plot function traces named sets selected for table display.

## Remarks

This function sets the plot function traces named sets that are included when displaying analysis results. If no plot
function traces named sets are to be selected then the list should include a blank string.

The function returns zero if the information is successfully set, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists and that it contains plot function traces named sets named Set1
and Set2.

Sub SetPlotFunctionTracesNamedSetSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long


Dim FileName As String
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

fill ItemList
Redim ItemList(1)
ItemList(0) = Set1
ItemList(1) = Set2

'set plot function traces named sets selected for display in the analysis result tables
ret = SapModel. DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay(ItemList)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

GetPlotFunctionTracesNamedSetsSelectedForDisplay

# SetPushoverNamedSetsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.SetPushoverNamedSetsSelectedForDisplay

## VB6 Procedure

Function SetPushoverNamedSetsSelectedForDisplay (ByRef PushoverNamedSetList() As String) As Integer

## Parameters

**PushoverNamedSetList**

The zero-based list of pushover named sets selected for table display.


## Remarks

This function sets the pushover named sets that are included when displaying analysis results. If no pushover named
sets are to be selected then the list should include a blank string.

The function returns zero if the information is successfully set, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists and that it contains pushover named sets named Set1 and Set2.

Sub SetPushoverNamedSetSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

fill ItemList
Redim ItemList(1)
ItemList(0) = Set1
ItemList(1) = Set2

'set pushover named sets selected for display in the analysis result tables
ret = SapModel. DatabaseTables.SetPushoverNamedSetsSelectedForDisplay(ItemList)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

GetPushoverNamedSetsSelectedForDisplay


# SetSectionCutsSelectedForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.SetSectionCutsSelectedForDisplay

## VB6 Procedure

Function SetSectionCutsSelectedForDisplay (ByRef SectionCutList() As String) As Integer

## Parameters

SectionCutList

The zero-based list of section cuts selected for table display.

## Remarks

This function sets the section cuts that are included when displaying analysis results. If no section cuts are to be
selected then the list should include a blank string.

The function returns zero if the information is successfully set, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists and that it contains section cuts named SCut1 and SCut2.

Sub SetSectionCutSelectionData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim ItemList() As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

fill ItemList
Redim ItemList(1)
ItemList(0) = SCut1
ItemList(1) = SCut2

'set section cuts selected for display in the analysis result tables
ret = SapModel. DatabaseTables.SetSectionCutsSelectedForDisplay(ItemList)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

GetSectionCutsSelectedForDisplay

# SetTableForEditingArray

## Syntax

cDatabaseTables.SetTableForEditingArray

## VB6 Procedure

Function SetTableForEditingArray (TableKey As String(), ByRef TableVersion As Integer, ByRef FieldKeysIncluded
As String(), NumberRecords As Integer, ByRef TableData As String() ) As Integer

## Parameters

TableKey

Input Item: The table key for a table which has been interactively edited. The table must be one that can be
interactively edited.

TableVersion

Returned Item: The version number of the specified table.

FieldKeysIncluded

Input Item: A zero-based array listing the field keys associated with the specified table for which data is reported in the
order it is reported in the TableData array. These are essentially the column headers of the data reported in TableData.

NumberRecords

Input Item: The number of records of data returned for each field. This is essentially the number of rows of data.

Table Data

Input Item: A zero-based, one-dimensional array of the table data, excluding headers, reported row by row. See
GetTableForDisplayArray for a more detailed explanation of the data format.

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.

Reads a table from a string array and adds it to a stored table list until either the ApplyEditedTables or
CancelTableEditing command is issued.


Here is an example for how to set the inputs.

TableKey = "EXAMPLE Material Table",

FieldsKeysIncluded = ("Material Name", "Material Type", "Density")

TableData = (A992Fy50, Steel, 490, 4000Psi, Concrete, 150, A615Gr60, Rebar, 480, A416Gr270, Tendon, 470,
6061T6, Aluminum, 170)

Executing the function with these inputs would be equivalent to setting the following table interactively:

```
EXAMPLE Material Name Type Density
```
```
A992Fy50 Steel 490
```
```
4000Psi Concrete 150
```
```
A615Gr60 Rebar 480
```
```
A416Gr270 Tendon 470
```
```
6061T6 Aluminum 170
```
## Release Notes

Initial release in version 23.0.0

## See Also

GetTableForDisplayArray

# SetTableForEditingCSVFile

## Syntax

cDatabaseTables.SetTableForEditingCSVFile

## VB6 Procedure

Function SetTableForEditingCSVFile (TableKey As String(), ByRef TableVersion As Integer, csvFilePath As String(),
Optional sepChar as string = ",") As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

TableVersion

Returned Item: The version number of the specified table.

csvFilePath

Input Item: The fully-qualified path for the CSV file containing the table data.


sepChar (Optional)

Optional Input Item: The delimiter between data items, by default ",". This delimiter must match what is used in the
csvString.

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.

Reads a table from a CSV file and adds it to a stored table list until either the ApplyEditedTables or
CancelTableEditing command is issued.

## Release Notes

Initial release in version 23.0.0

## See Also

GetTableForDisplayCSVFile

# SetTableForEditingCSVString

## Syntax

cDatabaseTables.SetTableForEditingCSVString

## VB6 Procedure

Function SetTableForEditingCSVString (TableKey As String, ByRef TableVersion As Integer, ByRef csvString As
String, Optional sepChar as string = ",") As Integer

## Parameters

TableKey

Input Item: The table key of the table for which data is requested.

TableVersion

Returned Item: The version number of the specified table.

csvString

Input Item: A CSV-formatted string containing all the table data.

sepChar (Optional)

Optional Input Item: The delimiter between data items, by default ",". This delimiter must match what is used in the
csvString.

## Remarks:

Returns 0 if the function executes correctly, otherwise returns nonzero.

Reads a table from a CSV-formatted string and adds it to a stored table list until either the ApplyEditedTables or
CancelTableEditing command is issued


## Release Notes

Initial release in version 23.0.0

## See Also

GetTableForDisplayCSVString

# SetTableOutputOptionsForDisplay

## Syntax

SapObject.SapModel.DatabaseTables.SetTableOutputOptionsForDisplay

## VB6 Procedure

Function SetTableOutputOptionsForDisplay (ByVal BaseReactionGX As Double, ByVal BaseReactionGY As Double,
ByVal BaseReactionGZ As Double, ByVal IsAllModes As Boolean, ByVal StartMode As Integer, ByVal EndMode
As Integer, ByVal IsAllBucklingModes As Boolean, ByVal StartBucklingMode As Integer, ByVal EndBucklingMode
As Integer, ByVal ModalHistory As Integer, ByVal DirectHistory As Integer, ByVal NonlinearStatic As Integer,
ByVal MultistepStatic As Integer, ByVal SteadyState As Integer, ByVal SteadyStateOption As Integer, ByVal
PowerSpectralDensity As Integer, ByVal Combo As Integer, ByVal BridgeDesign As Integer) As Integer

## Parameters

BaseReactionGX

The global X coordinate of the base reaction location.

BaseReactionGY

The global Y coordinate of the base reaction location.

BaseReactionGZ

The global Z coordinate of the base reaction location.

IsAllModes

This item is true if results are displayed for all modes of modal load cases.

StartMode

The first mode for which results are shown for modal load cases. This item only applies when the IsAllModes item is
False.

**EndMode**

The last mode for which results are shown for modal load cases. This item only applies when the IsAllModes item is
False.

IsAllBucklingModes

This item is true if results are displayed for all modes of buckling load cases.

StartBucklingMode

The first mode for which results are shown for buckling load cases. This item only applies when the
IsAllBucklingModes item is False.


EndBucklingMode

The last mode for which results are shown for buckling load cases. This item only applies when the
IsAllBucklingModes item is False.

ModalHistory

Indicates how multistep modal time history load case results are displayed: 1=Envelopes, 2=Step-by-step, 3=Last Step.

DirectHistory

Indicates how direct integration time history load case results are displayed: 1=Envelopes, 2=Step-by-step, 3=Last
Step.

NonlinearStatic

Indicates how nonlinear static load case results are displayed: 1=Envelopes, 2=Step-by-step, 3=Last Step.

MultistepStaticStatic

Indicates how multistep static load case results are displayed: 1=Envelopes, 2=Step-by-step, 3=Last Step.

SteadyState

Indicates how steady state load case results are displayed: 1=Envelopes, 2=At Frequencies.

SteadyStateOption

Indicates how type of steady state load case results displayed: 1=In and Out of Phase, 2=Magnitude, 3=All.

PowerSpectralDensity

Indicates how power spectral density load case results are displayed: 1=RMS, 2=sqrt(PSD).

Combo

Indicates how load combination results are displayed: 1=Envelopes, 2=Multiple Values If Possible, 3=Correspondence.

BridgeDesign

Indicates which bridge design results are displayed: 1=Controlling Combo, 2=All Combos.

## Remarks

This function sets the output option data used for display of analysis result tables.

The function returns zero if the information is successfully set, otherwise it returns a nonzero value.

## VBA Example

This example assumes that a file MyModel.sdb exists.

Sub SetTableOutputOptions()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart


'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'open an existing file
FileName = "C:\SapAPI\MyModel.sdb"
ret = SapModel.File.OpenFile(FileName)

'set table output options used for display in the analysis result tables
ret = SapModel. DatabaseTables.SetTableOutputOptionsForDisplay (0, 0, 0, False, 1, 12, False, 1, 6, 1, 1, 2, 2, 1,
1, 2, 2, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 23.00.

## See Also

GetTableOutputOptionsForDisplay

# ShowTablesInExcel

## Syntax

cDatabaseTables.ShowTablesInExcel

## VB6 Procedure

Function ShowTablesInExcel(ByRef TableKeyList() As String, WindowHandle As Integer) As Integer

## Parameters

TableKeyList

A zero-based array of the table keys for the tables to be included in the output.

WindowHandle

If a valid window handle is entered here Excel will be located in front of that window.

## Remarks

Exports the specified tables to Excel.

Excel must be present on the computer for this function to work. If there is nothing to be shown in the table then no
data is returned and Excel is not displayed.


## VBA Example

Sub Example()

Dim myHelper As cHelper

Dim SapObject As cOAPI

Dim SapModel As cSapModel

Dim ret As Long

ret = -1

'create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObjectProgID("CSI.SAP2000.API.SapObject")

'start SAP2000 application

ret = SapObject.ApplicationStart()

'create SapModel object

Set SapModel = SapObject.SapModel

'Initialize model

ret = SapModel.InitializeNewModel()

'Create 2D Frame Model

ret = SapModel.File.New2DFrame(e2DFrameType_PortalFrame, 2, 10, 3, 20)

'Get available tables

Dim NumberTables As Long

Dim TableKey() As String

Dim TableName() As String

Dim ImportType() As Long

Dim IsEmpty() As Boolean

ret = SapModel.DatabaseTables.GetAvailableTables(NumberTables, TableKey, TableName, ImportType)

Dim TableKeyList() As String


ReDim TableKeyList(2)

TableKeyList(0) = TableKey(5) ' "Connectivity - Frame"

TableKeyList(1) = TableKey(21) ' "Grid Lines"

TableKeyList(2) = TableKey(31) ' "Material Properties 03a - Steel Data"

Dim WindowHandle As Long

WindowHandle = 1

'View some tables in Excel

ret = SapModel.DatabaseTables.ShowTablesInExcel(TableKeyList, WindowHandle)

'close Sap2000

SapObject.ApplicationExit (False)

Set SapModel = Nothing

Set SapObject = Nothing

End Sub

## Release Notes

Initial release in version 23.0.0.

Added VBA Example in 24.2.0.

## See Also


