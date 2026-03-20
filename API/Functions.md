# ChangeName

## Syntax

SapObject.SapModel.Func.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined function.

NewName

The new name for the function.

## Remarks

This function changes the name of an existing function.

The function returns zero if the new name is successfully applied; otherwise it returns a nonzero
value.

## VBA Example

Sub ChangeFunctionName()
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

'change name of function
ret = SapModel.Func.ChangeName("UNIFRS", "MyFunc")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

## See Also

# ConvertToUser

## Syntax

SapObject.SapModel.Func.ConvertToUser

## VB6 Procedure

Function ConvertToUser(ByVal Name As String) As Long

## Parameters

Name

The name of an existing function that is not a user defined function.

## Remarks

This function converts an existing function to a user defined function.

The function returns zero if the function definition is successfully converted; otherwise it returns a
nonzero value. An error is returned if the specified function is already a user defined function.

## VBA Example

Sub ConvertFuncToUser()
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

'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'convert to user function
ret = SapModel.Func.ConvertToUser("TH-1")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# Count

## Syntax

SapObject.SapModel.Func.Count

## VB6 Procedure

Function Count(Optional ByVal FuncType As Long = 0) As Long

## Parameters

FuncType


This optional value is one of the following numbers, indicating the type of function for which the
count is desired.

```
0 = All function types
1 = Response spectrum
2 = Time history
3 = Power spectral density
4 = Steady state
```
**Remarks**

This function returns the total number of defined functions in the model of the specified type.

**VBA Example**

Sub CountFunctions()
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

'return number of defined functions of all types
Count = SapModel.Func.Count

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.01.


## See Also

# Delete

## Syntax

SapObject.SapModel.Func.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing function.

## Remarks

The function deletes a specified function.

The function returns zero if the function is successfully deleted; otherwise it returns a nonzero
value. It returns an error if the specified function can not be deleted if, for example, it is being
used in an load case.

## VBA Example

Sub DeleteFunction()
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

'delete function
ret = SapModel.Func.Delete("UNIFRS")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.01.

Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.

## See Also

# GetNameList

## Syntax

SapObject.SapModel.Func.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String, Optional
ByVal FuncType As Long = 0) As Long

## Parameters

NumberNames

The number of function names retrieved by the program.

MyName

This is a one-dimensional array of function names. The MyName array is created as a dynamic,
zero-based array by the API user:

```
Dim MyName() as String
```
The array is dimensioned to (NumberNames - 1) inside the SAP2000 program, filled with the
names, and returned to the API user.

FuncType


This is one of the following numbers, indicating the type of function for which the name list is
desired.

```
0 = All function types
1 = Response spectrum
2 = Time history
3 = Power spectral density
4 = Steady state
```
**Remarks**

This function retrieves the names of all defined functions of the specified type.

The function returns zero if the names are successfully retrieved; otherwise it returns nonzero.

**VBA Example**

Sub GetFunctionNames()
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
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'get function names
ret = SapModel.Func.GetNameList(NumberNames, MyName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**


Initial release in version 11.01.

## See Also

# GetTypeOAPI

## Syntax

SapObject.SapModel.Func.GetTypeOAPI

## VB6 Procedure

Function GetTypeOAPI(ByVal Name As String, ByRef FuncType As Long, ByRef AddType As
Long) As Long

## Parameters

Name

The name of an existing function.

FuncType

This is one of the following numbers, indicating the type of function.

```
1 = Response spectrum
2 = Time history
3 = Power spectral density
4 = Steady state
```
AddType

The is one of the following items, indicating the function subtype.

```
Response Spectrum Functions
```
```
0 = From file
1 = User
2 = UBC 94
3 = UBC 97
4 = BOCA 96
```
## 16 = NBCC

## 15 = IBC

### 7 = NEHRP 97

## 17 = Eurocode 8-

### 9 = NZS4203 1992

```
10 = Chinese 2010
11 = Italian Ordinanza 3274
12 = IS1893:
13 = AASHTO LRFD 2006
```

## 14 = NCHRP Project 20-

## 29 = SI 413(1995)

Time History Functions

```
0 = From file
1 = User
2 = Sine
3 = Cosine
4 = Ramp
5 = Sawtooth
6 = Triangular
7 = User periodic
```
- 14 = NCHRP Project 20-
- 15 = IBC
- 16 = NBCC
- 17 = Eurocode 8-
- 18 = AS 1170.4-
- 19 = NZS 1170.5-
- 20 = AASHTO
- 21 = Chinese JTG/T B02-
- 22 = Chinese GB 50111-
- 23 = IBC
- 24 = NBCC
- 25 = NTC
- 26 = AASHTO
- 27 = IBC
- 28 = TSC
- 30 = Argentina INPRES-CIRSOC
- 31 = Chile Norma NCh433+DS
- 32 = Chile Norma NCh2369-
- 33 = Colombia NSR-
- 34 = Ecuador NEC-11 Capitulo
- 35 = Guatemala AGIES NSE 2-
- 36 = Mexico NTC
- 37 = Peru Norma E.
- 38 = Dominican Republic R-
- 39 = Venezuela COVENIN 1756-2:
- 40 = KBC
- 41 = Mexico CFE-
- 42 = Peru NTE E.030
- 43 = Mexico CFE-
- 44 = Ecuado Norma NEC-SE-DS
- 45 = Costa Rica Seismic Code
- 46 = SP 14.13330.
- 47 = Chinese CJJ 166-
- 48 = NBCC
- 49 = IS 1893:
- 50 = ASCE 7-
- 51 = KBC
- 52 = NTC
- 53 = TSC


```
0 = From file
1 = User
```
```
Steady State Functions
```
```
0 = From file
1 = User
```
**Remarks**

This function retrieves the function type for the specified function.

The function returns zero if the type is successfully retrieved; otherwise it returns nonzero.

**VBA Example**

Sub GetFunctionType()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FuncType As Long
Dim AddType As Long

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

'get function type
ret = SapModel.Func.GetTypeOAPI("UNIFRS", FuncType, AddType)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.01.

Changed function name to GetTypeOAPI in v17.0.0.

Updated list of AddType values for response spectrum functions in v18.2.0.

## See Also

# GetValues

## Syntax

SapObject.SapModel.Func.GetValues

## VB6 Procedure

Function GetValues(ByVal Name As String, ByRef NumberItems As Long, ByRef MyTime() As
Double, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing function.

NumberItems

The number of time and function value pairs retrieved.

MyTime

This is an array that includes the time value for each data point. [s] for response spectrum and time
history functions, [cyc/s] for power spectral density and steady state functions

Value

This is an array that includes the function value for each data point.

## Remarks

This function retrieves the time and function values for any defined function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.


## VBA Example

Sub GetFuncValues()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim MyTime() As Double
Dim Value() As Double

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
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'get function values
ret = SapModel.Func.GetValues("TH-1", NumberItems, MyTime, Value)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

# GetFromFile

## Syntax

SapObject.SapModel.Func.FuncPSD.GetFromFile


**VB6 Procedure**

Function GetFromFile(ByVal Name As String, ByRef FileName As String, ByRef HeadLines As
Long, ByRef PreChars As Long, ByRef PointsPerLine As Long, ByRef ValueType As Long,
ByRef FreeFormat As Boolean, ByRef NumberFixed As Long, ByRef FreqTypeInFile As Long)
As Long

**Parameters**

Name

The name of a defined power spectral density function specified to be from a text file.

FileName

The full path of the text file containing the function data.

HeadLines

The number of header lines in the text file to be skipped before starting to read function data.

PreChars

The number of prefix characters to be skipped on each line in the text file.

PointsPerLine

The number of function points included on each text file line.

ValueType

This is either 1 or 2, indicating value type.

```
1 = Values at equal time intervals
2 = Time and function values
```
FreeFormat

This item is True if the data is provided in a free format. It is False if it is in a fixed format.

NumberFixed

This item applies only when the FreeFormat item is False. It is the number of characters per item.

FreqTypeInFile

This is either 1 or 2, indicating frequency type.

```
1 = Hz
2 = RPM
```
**Remarks**


This function retrieves the definition of a power spectral density function from file.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetPSDFuncFromFile()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim HeadLines As Long
Dim PreChars As Long
Dim PointsPerLine As Long
Dim ValueType As Long
Dim FreeFormat As Boolean
Dim NumberFixed As Long
Dim FreqTypeInFile As Long

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

'add PSD function from file
ret = SapModel.Func.FuncPSD.SetFromFile("PSD-1", "C:\SapAPI\FuncPSD.txt", 2, 0, 1, 2,
True)

'get PSD function from file
ret = SapModel.Func.FuncPSD.GetFromFile("PSD-1", FileName, HeadLines, PreChars,
PointsPerLine, ValueType, FreeFormat, NumberFixed, FreqTypeInFile)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Text File

Following is the contents of the text file name FuncPSD.txt used in the VBA Example.

Power Spectral Density Function

One pair of Frequency (Hz) and Value items per line

0 1

1 1

2 2

3 2

## Release Notes

Initial release in version 11.02.

## See Also

SetFromFile

# GetUser

## Syntax

SapObject.SapModel.Func.FuncPSD.GetUser

## VB6 Procedure

Function GetUser(ByVal Name As String, ByRef NumberItems As Long, ByRef Frequency() As
Double, ByRef Value() As Double) As Long

## Parameters

Name

The name of a user defined power spectral density function.

NumberItems

The number of frequency and value pairs defined.

Frequency

This is an array that includes the frequency in Hz for each data point. [cyc/s]


Value

This is an array that includes the function value for each data point.

**Remarks**

This function retrieves the definition of a user defined power spectral density function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetPSDFuncUser()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Freq() As Double
Dim Val() As Double
Dim NumberItems As Long
Dim Frequency() As Double
Dim Value() As Double

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

'add user PSD function
Num = 4
ReDim Freq(Num - 1)
ReDim Val(Num - 1)
Freq(0) = 0: Val(0) = 1
Freq(1) = 1: Val(1) = 1
Freq(2) = 2: Val(2) = 2
Freq(3) = 3: Val(3) = 2
ret = SapModel.Func.FuncPSD.SetUser("PSD-1", Num, Freq, Val)

'get user PSD function
ret = SapModel.Func.FuncPSD.GetUser("PSD-1", NumberItems, Frequency, Value)


'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetUser

# SetFromFile

## Syntax

SapObject.SapModel.Func.FuncPSD.SetFromFile

## VB6 Procedure

Function SetFromFile(ByVal Name As String, ByVal FileName As String, ByVal HeadLines As
Long, ByVal PreChars As Long, ByVal PointsPerLine As Long, ByVal ValueType As Long,
ByVal FreeFormat As Boolean, Optional ByVal NumberFixed As Long = 10, Optional ByVal
FreqTypeInFile As Long = 1) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

FileName

The full path of the text file containing the function data.

HeadLines

The number of header lines in the text file to be skipped before starting to read function data.

PreChars

The number of prefix characters to be skipped on each line in the text file.

PointsPerLine


The number of function points included on each text file line.

ValueType

This is either 1 or 2, indicating value type.

```
1 = Values at equal time intervals
2 = Time and function values
```
FreeFormat

This item is True if the data is provided in a free format. It is False if it is in a fixed format.

NumberFixed

This item only applies when the FreeFormat item is False. It is the number of characters per item.

FreqTypeInFile

This is either 1 or 2, indicating frequency type.

```
1 = Hz
2 = RPM
```
**Remarks**

This function defines a power spectral density function from file.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetPSDFuncFromFile()
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


'add PSD function from file
ret = SapModel.Func.FuncPSD.SetFromFile("PSD-1", "C:\SapAPI\FuncPSD.txt", 2, 0, 1, 2,
True)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Text File

Following is the contents of the text file name FuncPSD.txt used in the VBA Example.

Power Spectral Density Function

One pair of Frequency (Hz) and Value items per line

0 1

1 1

2 2

3 2

## Release Notes

Initial release in version 11.02.

## See Also

GetFromFile

# SetUser

## Syntax

SapObject.SapModel.Func.FuncPSD.SetUser

## VB6 Procedure

Function SetUser(ByVal Name As String, ByVal NumberItems As Long, ByRef Frequency() As
Double, ByRef Value() As Double) As Long

## Parameters


Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

NumberItems

The number of frequency and value pairs defined.

Frequency

This is an array that includes the frequency in Hz for each data point. [cyc/s]

Value

This is an array that includes the function value for each data point.

**Remarks**

This function defines a user power spectral density function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetPSDFuncUser()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim Frequency() As Double
Dim Value() As Double

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

'add user PSD function
NumberItems = 4


ReDim Frequency(NumberItems - 1)
ReDim Value(NumberItems - 1)
Frequency(0) = 0: Value(0) = 1
Frequency(1) = 1: Value(1) = 1
Frequency(2) = 2: Value(2) = 2
Frequency(3) = 3: Value(3) = 2
ret = SapModel.Func.FuncPSD.SetUser("PSD-1", NumberItems, Frequency, Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetUser

# GetAASHTO2006

## Syntax

SapObject.SapModel.Func.FuncRS.GetAASHTO2006

## VB6 Procedure

Function GetAASHTO2006(ByVal Name As String, ByRef AASHTO2006A As Double, ByRef
AASHTO2006SoilProfileType As Long, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of an AASHTO2006 response spectrum function.

AASHTO2006A

The acceleration coefficient, A.

AASHTO2006SoilProfileType

This is 1, 2, 3 or 4, indicating the soil profile type.

```
1 = I
2 = II
```

### 3 = III

### 4 = IV

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of an AASHTO2006 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncAASHTO2006()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim AASHTO2006A As Double
Dim AASHTO2006SoilProfileType As Long
Dim DampRatio As Double

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

'add AASHTO2006 RS function
ret = SapModel.Func.FuncRS.SetAASHTO2006("RS-1", 0.3, 4, 0.04)

'get AASHTO2006 RS function
ret = SapModel.Func.FuncRS.GetAASHTO2006("RS-1", AASHTO2006A,
AASHTO2006SoilProfileType, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

SetAASHTO2006

# GetAASHTO2007

## Syntax

SapObject.SapModel.Func.FuncRS.GetAASHTO2007

## VB6 Procedure

Function GetAASHTO2007(ByVal Name As String, ByRef AASHTO2007Option As Long,
ByRef AASHTO2007Latitude As Double, ByRef AASHTO2007Longitude As Double, ByRef
AASHTO2007ZipCode As String, ByRef AASHTO2007SS As Double, ByRef AASHTO2007S1
As Double, ByRef AASHTO2007PGA As Double, ByRef AASHTO2007SiteClass As Long,
ByRef AASHTO2007Fa As Double, ByRef AASHTO2007Fv As Double, ByRef
AASHTO2007Fpga As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of an AASHTO 20-07 response spectrum function.

AASHTO2007Option

This is 0, 1, or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
AASHTO2007Latitude, AASHTO2007Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when AASHTO2007Option = 0.

AASHTO2007ZipCode

The zip code for which the seismic coefficients are obtained. This item is used only when
AASHTO2007Option = 1.

AASHTO2007SS, AASHTO2007S1, AASHTO2007PGA


The seismic coefficients Ss, S1 and PGA. These items are used only when AASHTO2007Option
= 2.

AASHTO2007SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
AASHTO2007Fa, AASHTO2007Fv, AASHTO2007Fpga

The site coefficients Fa, Fv and Fpga. These items are used only when AASHTO2007SiteClass=
6.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a AASHTO 20-07 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncAASHTO2007()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim AASHTO2007Option As Long
Dim AASHTO2007Latitude As Double
Dim AASHTO2007Longitude As Double
Dim AASHTO2007ZipCode As String
Dim AASHTO2007SS As Double
Dim AASHTO2007S1 As Double
Dim AASHTO2007PGA As Double
Dim AASHTO2007SiteClass As Long
Dim AASHTO2007Fa As Double
Dim AASHTO2007Fv As Double
Dim AASHTO2007Fpga As Double
Dim DampRatio As Double

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

'add AASHTO2007 RS function
ret = SapModel.Func.FuncRS.SetAASHTO2007("RS-1", 1, 0, 0, "94704", 0, 0, 0, 4, 0, 0, 0,
0.04)

'get AASHTO2007 RS function
ret = SapModel.Func.FuncRS.GetAASHTO2007("RS-1", AASHTO2007Option,
AASHTO2007Latitude, AASHTO2007Longitude, AASHTO2007ZipCode, AASHTO2007SS,
AASHTO2007S1, AASHTO2007PGA, AASHTO2007SiteClass, AASHTO2007Fa,
AASHTO2007Fv, AASHTO2007Fpga, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.00.

## See Also

SetAASHTO2007

# GetAS11702007

## Syntax

SapObject.SapModel.Func.FuncRS.GetAS11702007

## VB6 Procedure

Function GetAS11702007(ByVal Name As String, ByRef AS2007SiteClass As Long, ByRef
AS2007kp As Double, ByRef AS2007Z As Double, ByRef AS2007Sp As Double, ByRef
AS2007Mu As Double, ByRef DampRatio As Double) As Long


**Parameters**

Name

The name of a AS 1170 2007 response spectrum function.

AS2007SiteClass

This is 1, 2, 3, 4 or 5, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
AS2007kp

The probability factor, kp.

AS2007Z

The hazard factor, Z.

AS2007Sp

The structural performance factor, Sp.

AS2007Mu

The structural ductility factor, u.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of an AS 1170 2007 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncAS11702007()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim AS2007SiteClass As Long
Dim AS2007kp As Double
Dim AS2007Z As Double


Dim AS2007Sp As Double
Dim AS2007Mu As Double
Dim DampRatio As Double

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

'add AS 1170 2007 RS function

ret = SapModel.Func.FuncRS.SetAS11702007("RS-1", 3, 1.3, 0.9, 0.77, 2, 0.04)

'get AS 1170 2007 RS function
ret = SapModel.Func.FuncRS.GetAS11702007("RS-1", AS2007SiteClass, AS2007kp,
AS2007Z, AS2007Sp, AS2007Mu, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing

Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.00.

## See Also

SetAS11702007

# GetBOCA96

## Syntax

SapObject.SapModel.Func.FuncRS.GetBOCA96


**VB6 Procedure**

Function GetBOCA96(ByVal Name As String, ByRef BOCA96Aa As Double, ByRef
BOCA96Av As Double, ByRef BOCA96S As Double, ByRef BOCA96R As Double, ByRef
DampRatio As Double) As Long

**Parameters**

Name

The name of a BOCA96 response spectrum function.

BOCA96Aa

The effective peak acceleration, Aa.

BOCA96Av

The effective peak velocity, Av.

BOCA96S

The soil profile coefficient, S.

BOCA96R

The response modification factor, R.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a BOCA96 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncBOCA96()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim BOCA96Aa As Double
Dim BOCA96Av As Double
Dim BOCA96S As Double
Dim BOCA96R As Double
Dim DampRatio As Double


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

'add BOCA96 RS function
ret = SapModel.Func.FuncRS.SetBOCA96("RS-1", 0.3, 0.3, 1.2, 1, 0.04)

'get BOCA96 RS function
ret = SapModel.Func.FuncRS.GetBOCA96("RS-1", BOCA96Aa, BOCA96Av, BOCA96S,
BOCA96R, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetBOCA96

# GetChinese2010

## Syntax

SapObject.SapModel.Func.FuncRS.GetChinese2010

## VB6 Procedure

Function GetChinese2010(ByVal Name As String, ByRef JGJ32010AlphaMax As Double, ByRef
JGJ32010SI As Long, ByRef JGJ32010Tg As Double, ByRef JGJ32010PTDF As Double, ByRef
DampRatio As Double) As Long


**Parameters**

Name

The name of a Chinese 2010 response spectrum function.

JGJ32010AlphaMax

The maximum influence factor.

JGJ32010SI

This is 1, 2, 3, 4, 5 or 6, indicating the seismic intensity.

```
1 = 6 (0.05g)
2 = 7 (0.10g)
3 = 7 (0.15g)
4 = 8 (0.20g)
5 = 8 (0.30g)
6 = 9 (0.40g)
```
JGJ32010Tg

The characteristic ground period, Tg > 0.1. [s]

JGJ32010PTDF

The period time discount factor.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a Chinese 2010 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncChinese2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim JGJ32010AlphaMax As Double
Dim JGJ32010SI As Long
Dim JGJ32010Tg As Double
Dim JGJ32010PTDF As Double
Dim DampRatio As Double


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

'add Chinese2010 RS function
ret = SapModel.Func.FuncRS.SetChinese2010("RS-1", 0.18, 5, 0.36, 1, 0.04)

'get Chinese2010 RS function
ret = SapModel.Func.FuncRS.GetChinese2010("RS-1", JGJ32010AlphaMax, JGJ32010SI,
JGJ32010Tg, JGJ32010PTDF, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 15.0.2.

## See Also

SetChinese2010

# GetCJJ1662011 {RS}

## Syntax

SapObject.SapModel.Func.FuncRS.GetCJJ1662011

## VB6 Procedure

Function GetCJJ1662011(ByVal Name As String, ByRef Direction As Integer, ByRef PeakAccel
As Double, ByRef Tg As Double, ByRef DampRatio As Double) As Long


**Parameters**

Name

The name of a CJJ 166-2011 response spectrum function.

Direction

This is 1 or 2, indicating the response spectrum direction.

```
1 = Horizontal
2 = Vertical
```
PeakAccel

The peak acceleration, A.

Tg

The characteristic ground period , Tg > 0.1. [s]

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a CJJ 166-2011 response spectrum function.

The function returns zero if the function is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetRSFuncCJJ1662011()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim Direction As Long

Dim PeakAccel As Double

Dim Tg As Double

Dim DampRatio As Double


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

'add CJJ 166-2011 RS function
ret = SapModel.Func.FuncRS.SetCJJ1662011("RS-1", 0.35, 0.25, 0.04)

'get CJJ 166-2011 RS function

ret = SapModel.Func.FuncRS.GetCJJ1662011("RS-1", Direction, PeakAccel, Tg, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 18.2.0.

## See Also

SetCJJ1662011

# GetEuroCode8

## Syntax

SapObject.SapModel.Func.FuncRS.GetEuroCode8

## VB6 Procedure

Function GetEuroCode8(ByVal Name As String, ByRef EuroCode8AG As Double, ByRef
EuroCode8S As Long, ByRef EuroCode8n As Double, ByRef DampRatio As Double) As Long


**Parameters**

Name

The name of a EuroCode8 response spectrum function.

EuroCode8AG

The design ground acceleration, Ag.

EuroCode8S

This is 1, 2 or 3, indicating the subsoil class.

```
1 = A
2 = B
3 = C
```
EuroCode8n

The damping correction factor, n, where n >= 0.7.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a EuroCode8 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncEuroCode8()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim EuroCode8AG As Double
Dim EuroCode8S As Long
Dim EuroCode8n As Double
Dim DampRatio As Double

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

'add EuroCode8 RS function
ret = SapModel.Func.FuncRS.SetEuroCode8("RS-1", 0.3, 3, 1.2, 0.04)

'get EuroCode8 RS function
ret = SapModel.Func.FuncRS.GetEuroCode8("RS-1", EuroCode8AG, EuroCode8S,
EuroCode8n, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetEuroCode8

# GetEurocode82004_1

## Syntax

SapObject.SapModel.Func.FuncRS.GetEurocode82004_1

## VB6 Procedure

Function GetEurocode82004_1(ByVal Name As String, ByRef EURO2004Country As Long,
ByRef EURO2004Direction As Long, ByRef EURO2004SpectrumType As Long, ByRef
EURO2004GroundType As Long, ByRef EURO2004ag As Double, ByRef EURO2004S As
Double, ByRef EURO2004AvgoverAg As Double, ByRef EURO2004Tb As Double, ByRef
EURO2004Tc As Double, ByRef EURO2004Td As Double, ByRef EURO2004Beta As Double,
ByRef EURO2004q As Double, ByRef DampRatio As Double) As Long

## Parameters

Name


The name of a Eurocode 8 2004 response spectrum function.

EURO2004Country

This is 0, 1, 5, 6, or 10 indicating the country for which the Nationally Determined Parameters
(NDPs) are specified.

```
0 = Other (NDPs are user specified)
```
```
1 = CEN Default
```
```
5 = Norway
```
```
6 = Singapore
```
```
10 = Portugal
```
EURO2004Direction

This is 1 or 2, indicating the ground motion direction.

```
1 = Horizontal
```
```
2 = Vertical (Does not apply when EURO2004Country = 6)
```
EURO2004SpectrumType

This is 1 or 2, indicating the spectrum type.

```
1 = Type 1
```
```
2 = Type 2 (Does not apply when EURO2004Country = 5 or 6)
```
EURO2004GroundType

This is 1, 2, 3, 4, 5 or 6, indicating the ground type. This item only applies when the
EURO2004Direction item is 1 (horizontal).

```
1 = A (Does not apply when EURO2004Country = 6)
```
```
2 = B (Does not apply when EURO2004Country = 6)
```
```
3 = C
```
```
4 = D
```
```
5 = E (Does not apply when EURO2004Country = 6)
```
```
6 = S1 (Only applies when EURO2004Country = 6)
```
EURO2004ag

The design ground acceleration in g, ag.


### EURO2004S

The soil factor, S. This item only applies when the EURO2004Direction item is 1 (horizontal).

EURO2004AvgoverAg

The vertical ground acceleration divided by the horizontal ground acceleration, Avg/Ag. This item
only applies when the EURO2004Direction item is 2 (vertical).

EURO2004Tb

The lower limit of period of the constant spectral acceleration branch, Tb.

EURO2004Tc

The upper limit of period of the constant spectral acceleration branch, Tc.

EURO2004Td

The period defining the start of the constant displacement range, Td.

EURO2004Beta

The lower bound factor, Beta.

EURO2004q

The behavior factor, q.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a Eurocode 8 2004 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncEurocode82004()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim EURO2004Country As Long
Dim EURO2004Direction As Long
Dim EURO2004SpectrumType As Long
Dim EURO2004GroundType As Long
Dim EURO2004ag As Double
Dim EURO2004S As Double


Dim EURO2004AvgoverAg As Double
Dim EURO2004Tb As Double
Dim EURO2004Tc As Double
Dim EURO2004Td As Double
Dim EURO2004Beta As Double
Dim EURO2004q As Double
Dim DampRatio As Double

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

'add Eurocode 8 2004 RS function
ret = SapModel.Func.FuncRS.SetEurocode82004_1("RS-1", 1, 1, 1, 2, 0.4, 1.2, 0.9, 0.15, 0.5,
2, 0.2, 2, 0.04)

'get Eurocode 8 2004 RS function
ret = SapModel.Func.FuncRS.GetEurocode82004_1("RS-1", EURO2004Country,
EURO2004Direction, EURO2004SpectrumType, EURO2004GroundType, EURO2004ag,
EURO2004S, EURO2004AvgoverAg, EURO2004Tb, EURO2004Tc, EURO2004Td,
EURO2004Beta, EURO2004q, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 14.1.0.

This function supersedes GetEurocode82004.

Added Portugal as a Country parameter in SAP2000 Version 15.0.0 and CSiBridge Version
15.1.0.

Added Singapore as a Country parameter in v20.1.0.

**See Also**


SetEurocode82004_1

# GetFromFile

## Syntax

SapObject.SapModel.Func.FuncRS.GetFromFile

## VB6 Procedure

Function GetFromFile(ByVal Name As String, ByRef FileName As String, ByRef HeadLines As
Long, ByRef DampRatio As Double, ByRef ValueType As Long) As Long

## Parameters

Name

The name of a defined response spectrum function specified to be from a text file.

FileName

The full path of the text file containing the function data.

HeadLines

The number of header lines in the text file to be skipped before starting to read function data.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

ValueType

This is either 1 or 2, indicating time value type.

```
1 = Frequency
2 = Period
```
## Remarks

This function retrieves the definition of a response spectrum function from file.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetRSFuncFromFile()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim HeadLines As Long
Dim DampRatio As Double
Dim ValueType As Long

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

'add RS function from file
ret = SapModel.Func.FuncRS.SetFromFile("RS-1", "C:\SapAPI\FuncRS.txt", 3, 0.04)

'get RS function from file
ret = SapModel.Func.FuncRS.GetFromFile("RS-1", FileName, HeadLines, DampRatio,
ValueType)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Text File**

Following is the contents of the text file name FuncRS.txt used in the VBA Example.

Reponse Spectrum Function

One pair of Period (sec) and Acceleration (g) values per line

Acceleration values at equal spacing of 0.01 seconds.

0.030 0.500

0.125 1.355

0.587 1.355

0.660 1.355


### 1.562 0.576

### 4.000 0.219

### 10.00 0.037

## Release Notes

Initial release in version 11.02.

## See Also

SetFromFile

# GetJTGB022013

## Syntax

SapObject.SapModel.Func.FuncRS.GetJTGB022013

## VB6 Procedure

Function GetJTGB022013(ByVal Name As String, ByRef Direction As Integer, ByRef PeakAccel
As Double, ByRef Tg As Double, ByRef Ci As Double, ByRef Cs As Double, ByRef DampRatio
As Double) As Long

## Parameters

Name

The name of a JTG B02-2013 response spectrum function.

Direction

This is 1, 2 or 3, indicating the response spectrum direction.

```
1 = Horizontal
2 = Vertical-Rock
3 = Vertical-Soil
```
PeakAccel

The peak acceleration, A.

Tg

The characteristic ground period, Tg > 0.1. [s]

Ci


The importance coefficient.

Cs

The site soil coefficient.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a JTG B02-2013 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncJTGB022013()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Direction As Long
Dim PeakAccel As Double
Dim Tg As Double
Dim Ci As Double
Dim Cs As Double
Dim DampRatio As Double

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

'add JTG B02-2013 RS function
ret = SapModel.Func.FuncRS.SetJTGB022013("RS-1", 1, 0.18, 0.36, 0.4, 1, 0.04)

'get JTG B02-2013 RS function
ret = SapModel.Func.FuncRS.GetJTGB022013("RS-1", Direction, PeakAccel, Tg, Ci, Cs,


DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v18.2.0.

## See Also

SetJTBG022013

# GetJTGT2231012020

## Syntax

SapObject.SapModel.Func.FuncRS.GetJTGT2231012020

## VB6 Procedure

Function GetJTGT2231012020(ByVal Name As String, ByRef PeakAccel As Double, ByRef Tg
As Double, ByRef Ci As Double, ByRef Cs As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a JTGT2231012020 response spectrum function.

PeakAccel

The peak ground acceleration.

Tg

The characteristic ground period, Tg > 0.1 [s]

Ci

The importance coefficient.

Cs

The site soil coefficient.


DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a JTGT2231012020 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncJTGT2231012020()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PeakAccel As Double
Dim Tg As Double

Dim Ci As Double

Dim Cs As Double

Dim DampRatio As Double

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

'add JTGT2231012020 RS function
ret = SapModel.Func.FuncRS.SetJTGT2231012020("RS-1", 0.18, 0.36, 0.4, 1, 0.04)

'get JTG/T 2231-01-2020 RS function
ret = SapModel.Func.FuncRS.GetJTGT2231012020("RS-1", PeakAccel, Tg, Ci, Cs,
DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v23.2.0

## See Also

SetJTGT2231012020

# GetIBC2003

## Syntax

SapObject.SapModel.Func.FuncRS.GetIBC2003

## VB6 Procedure

Function GetIBC2003(ByVal Name As String, ByRef IBC2003SS As Double, ByRef IBC2003S1
As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a IBC2003 response spectrum function.

IBC2003SS

The design spectral acceleration at short periods, Sds.

IBC2003S1

The design spectral acceleration at a one second period, Sd1.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

## Remarks

This function retrieves the definition of a IBC2003 response spectrum function.


The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncIBC2003()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim IBC2003SS As Double
Dim IBC2003S1 As Double
Dim DampRatio As Double

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

'add IBC2003 RS function
ret = SapModel.Func.FuncRS.SetIBC2003("RS-1", 1.2, 0.3, 0.04)

'get IBC2003 RS function
ret = SapModel.Func.FuncRS.GetIBC2003("RS-1", IBC2003SS, IBC2003S1, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

**See Also**

SetIBC2003


# GetIBC2006

## Syntax

SapObject.SapModel.Func.FuncRS.GetIBC2006

## VB6 Procedure

Function GetIBC2006(ByVal Name As String, ByRef IBC2006Option As Long, ByRef
IBC2006Latitude As Double, ByRef IBC2006Longitude As Double, ByRef IBC2006ZipCode As
String, ByRef IBC2006SS As Double, ByRef IBC2006S1 As Double, ByRef IBC2006TL As
Double, ByRef IBC2006SiteClass As Long, ByRef IBC2006Fa As Double, ByRef IBC2006Fv As
Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a IBC2006 response spectrum function.

IBC2006Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitiude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
IBC2006Latitude, IBC2006Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when IBC2006Option = 0.

IBC2006ZipCode

The zip code for which the seismic coefficients are obtained. This item is used only when
IBC2006Option = 1.

IBC2006SS, IBC2006S1

The seismic coefficients Ss and S1. This item is used only when IBC2006Option = 2.

IBC2006TL

The long-period transition period. [s]

IBC2006SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
```

### 3 = C

### 4 = D

### 5 = E

### 6 = F

IBC2006Fa, IBC2006Fv

The site coefficients Fa and Fv. These items are used only when IBC2006SiteClass= 6.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a IBC2006 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncIBC2006()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim IBC2006Option As Long
Dim IBC2006Latitude As Double
Dim IBC2006Longitude As Double
Dim IBC2006ZipCode As String
Dim IBC2006SS As Double
Dim IBC2006S1 As Double
Dim IBC2006TL As Double
Dim IBC2006SiteClass As Long
Dim IBC2006Fa As Double
Dim IBC2006Fv As Double
Dim DampRatio As Double

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

'add IBC2006 RS function
ret = SapModel.Func.FuncRS.SetIBC2006("RS-1", 1, 0, 0, "94704", 0, 0, 7.5, 4, 0, 0, 0.04)

'get IBC2006 RS function
ret = SapModel.Func.FuncRS.GetIBC2006("RS-1", IBC2006Option, IBC2006Latitude,
IBC2006Longitude, IBC2006ZipCode, IBC2006SS, IBC2006S1, IBC2006TL, IBC2006SiteClass,
IBC2006Fa, IBC2006Fv, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetIBC2006

# GetIS18932002

## Syntax

SapObject.SapModel.Func.FuncRS.GetIS18932002

## VB6 Procedure

Function GetIS18932002(ByVal Name As String, ByRef INZ As Double, ByRef INS As Long,
ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a IS1893-2002 response spectrum function.

INZ

The seismic zone factor, Z.

INS

This is 1, 2 or 3, indicating the soil type.


### 1 = I

### 2 = II

### 3 = III

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a IS1893-2002 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncIS18932002()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim INZ As Double
Dim INS As Long
Dim DampRatio As Double

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

'add IS18932002 RS function
ret = SapModel.Func.FuncRS.SetIS18932002("RS-1", 0.3, 3, 0.04)

'get IS18932002 RS function
ret = SapModel.Func.FuncRS.GetIS18932002("RS-1", INZ, INS, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

SetIS18932002

# GetItalian3274

## Syntax

SapObject.SapModel.Func.FuncRS.GetItalian3274

## VB6 Procedure

Function GetItalian3274(ByVal Name As String, ByRef Italag As Double, ByRef ItalSoilType As
Long, ByRef Italq As Double, ByRef ItalLevel As Double, ByRef DampRatio As Double) As
Long

## Parameters

Name

The name of a Italian 3274 response spectrum function.

Italag

The peak ground acceleration.

ItalSoilType

This is 1, 2, 3, 4 or 5, indicating the seismic intensity.

```
1 = A
2 = B
3 = C
4 = E
5 = D
```
Italq

The structure factor.

ItalLevel

This is 0, 1, 2, 3, 4, 5, 6 or 7, indicating the spectral level, direction and building type.

```
0 = SLU/H/Building
1 = SLU/H/Bridge
```

```
2 = SLU/V/Building
3 = SLU/V/Bridge
4 = EL/H/Building
5 = EL/H/Bridge
6 = EL/V/Building
7 = EL/V/Bridge
```
SLU refers to ultimate strength design and EL refers to elastic design. H and V are horizontal and
vertical, respectively.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a Italian 3274 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncItalian3274()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Italag As Double
Dim ItalSoilType As Long
Dim Italq As Double
Dim ItalLevel As Double
Dim DampRatio As Double

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

'add Italian3274 RS function
ret = SapModel.Func.FuncRS.SetItalian3274("RS-1", 0.3, 2, 1.1, 4, 0.04)


'get Italian3274 RS function
ret = SapModel.Func.FuncRS.GetItalian3274("RS-1", Italag, ItalSoilType, Italq, ItalLevel,
DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetItalian3274

# GetNBCC2015

## Syntax

SapObject.SapModel.Func.FuncRS.GetNBCC2015

## VB6 Procedure

Function GetNBCC2015(ByVal Name As String, ByRef PGA As Double, ByRef S02 As Double,
ByRef S05 As Double, ByRef S1 As Double, ByRef S2 As Double, ByRef S5 As Double, ByRef
S10 As Double, ByRef SiteClass As Long, ByRef F02 As Double, ByRef F05 As Double, ByRef
F1 As Double, ByRef F2 As Double, ByRef F5 As Double, ByRef F10 As Double, ByRef
DampRatio As Double) As Long

## Parameters

Name

The name of a NBCC2015 response spectrum function.

PGA

The peak ground acceleration.

S02

The spectral acceleration at a 0.2 second period.

S05


The spectral acceleration at a 0.5 second period.

S1

The spectral acceleration at a 1 second period.

S2

The spectral acceleration at a 2 second period.

S5

The spectral acceleration at a 5 second period.

S10

The spectral acceleration at a 10 second period.

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
F02

The site coefficient at a 0.2 second period. This item is read when the site class is F only.

F05

The site coefficient at a 0.5 second period. This item is read when the site class is F only.

F1

The site coefficient at a 1 second period. This item is read when the site class is F only.

F2

The site coefficient at a 2 second period. This item is read when the site class is F only.

F5

The site coefficient at a 5 second period. This item is read when the site class is F only.

F10

The site coefficient at a 10 second period. This item is read when the site class is F only.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.


**Remarks**

This function retrieves the definition of a NBCC2015 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncNBCC2015()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim PGA As Double
Dim S02 As Double

Dim S05 As Double

Dim S1 As Double

Dim S2 As Double

Dim S5 As Double

Dim S10 As Double

Dim SiteClass As Long
Dim F02 As Double

Dim F05 As Double

Dim F1 As Double

Dim F2 As Double

Dim F5 As Double

Dim F10 As Double
Dim DampRatio As Double

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

'add NBCC2015 RS function
ret = SapModel.Func.FuncRS.SetNBCC2015("RS-1", 0.6, 1.1, 0.7, 0.35, 0.2, 0.035, 0.01, 6,
1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 0.04)

'get NBCC2015 RS function
ret = SapModel.Func.FuncRS.GetNBCC2015("RS-1", PGA, S02, S05, S1, S2, S5, S10,
SiteClass, F02, F05, F1, F2, F5, F10, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

## See Also

SetNBCC2015

# GetNBCC2010

## Syntax

SapObject.SapModel.Func.FuncRS.GetNBCC2010

## VB6 Procedure

Function GetNBCC2010(ByVal Name As String, ByRef PGA As Double, ByRef S02 As Double,
ByRef S05 As Double, ByRef S1 As Double, ByRef S2 As Double, ByRef SiteClass As Long,
ByRef Fa As Double, ByRef Fv As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a NBCC2010 response spectrum function.

PGA


The peak ground acceleration.

S02

The spectral acceleration at a 0.2 second period.

S05

The spectral acceleration at a 0.5 second period.

S1

The spectral acceleration at a 1 second period.

S2

The spectral acceleration at a 2 second period.

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa

The site coefficient, Fa. This item is read when the site class is F only.

Fv

The site coefficient, Fv. This item is read when the site class is F only.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a NBCC2010 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncNBCC2010()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim PGA As Double
Dim S02 As Double

Dim S05 As Double

Dim S1 As Double

Dim S2 As Double

Dim SiteClass As Long
Dim Fa As Double

Dim Fv As Double
Dim DampRatio As Double

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

'add NBCC2010 RS function
ret = SapModel.Func.FuncRS.SetNBCC2010("RS-1", 0.6, 1.1, 0.7, 0.35, 0.2, 6, 1.8, 2, 0.04)

'get NBCC2010 RS function
ret = SapModel.Func.FuncRS.GetNBCC2010("RS-1", PGA, S02, S05, S1, S2, SiteClass, Fa,
Fv, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 19.0.0.

**See Also**

SetNBCC2010


# GetNBCC2005

## Syntax

SapObject.SapModel.Func.FuncRS.GetNBCC2005

## VB6 Procedure

Function GetNBCC2005(ByVal Name As String, ByRef NBCC2005PGA As Double, ByRef
NBCC2005S02 As Double, ByRef NBCC2005S05 As Double, ByRef NBCC2005S1 As Double,
ByRef NBCC2005S2 As Double, ByRef NBCC2005SiteClass As Long, ByRef NBCC2005Fa As
Double, ByRef NBCC2005Fv As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a NBCC2005 response spectrum function.

NBCC2005PGA

The peak ground acceleration.

NBCC2005S02

The spectral acceleration at a 0.2 second period.

NBCC2005S05

The spectral acceleration at a 0.52 second period.

NBCC2005S1

The spectral acceleration at a 1 second period.

NBCC2005S2

The spectral acceleration at a 2 second period.

NBCC2005SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```

NBCC2005Fa

The site coefficient, Fa. This item is read when the site class is F only.

NBCC2005Fv

The site coefficient, Fv. This item is read when the site class is F only.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a NBCC2005 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncNBCC2005()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NBCC2005PGA As Double
Dim NBCC2005S02 As Double
Dim NBCC2005S05 As Double
Dim NBCC2005S1 As Double
Dim NBCC2005S2 As Double
Dim NBCC2005SiteClass As Long
Dim NBCC2005Fa As Double
Dim NBCC2005Fv As Double
Dim DampRatio As Double

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

'add NBCC2005 RS function


ret = SapModel.Func.FuncRS.SetNBCC2005("RS-1", 0.6, 1.1, 0.7, 0.35, 0.2, 6, 1.8, 2, 0.04)

'get NBCC2005 RS function
ret = SapModel.Func.FuncRS.GetNBCC2005("RS-1", NBCC2005PGA, NBCC2005S02,
NBCC2005S05, NBCC2005S1, NBCC2005S2, NBCC2005SiteClass, NBCC2005Fa,
NBCC2005Fv, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.00.

## See Also

SetNBCC2005

# GetNBCC95

## Syntax

SapObject.SapModel.Func.FuncRS.GetNBCC95

## VB6 Procedure

Function GetNBCC95(ByVal Name As String, ByRef NBCC95ZVR As Double, ByRef
NBCC95ZA As Long, ByRef NBCC95ZV As Long, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a NBCC95 response spectrum function.

NBCC95ZVR

The zonal velocity ratio.

NBCC95ZA

The acceleration-related seismic zone.

NBCC95ZV

The velocity-related seismic zone.


DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a NBCC95 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncNBCC95()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NBCC95ZVR As Double
Dim NBCC95ZA As Long
Dim NBCC95ZV As Long
Dim DampRatio As Double

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

'add NBCC95 RS function
ret = SapModel.Func.FuncRS.SetNBCC95("RS-1", 0.3, 5, 5, 0.04)

'get NBCC95 RS function
ret = SapModel.Func.FuncRS.GetNBCC95("RS-1", NBCC95ZVR, NBCC95ZA,
NBCC95ZV, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

SetNBCC95

# GetNCHRP2007

## Syntax

SapObject.SapModel.Func.FuncRS.GetNCHRP2007

## VB6 Procedure

Function GetNCHRP2007(ByVal Name As String, ByRef NCHRP2007Option As Long, ByRef
NCHRP2007Latitude As Double, ByRef NCHRP2007Longitude As Double, ByRef
NCHRP2007ZipCode As String, ByRef NCHRP2007SS As Double, ByRef NCHRP2007S1 As
Double, ByRef NCHRP2007SiteClass As Long, ByRef NCHRP2007Fa As Double, ByRef
NCHRP2007Fv As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a NCHRP 20-07 response spectrum function.

NCHRP2007Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitiude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
NCHRP2007Latitude, NCHRP2007Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when NCHRP2007Option = 0.

NCHRP2007ZipCode

The zip code for which the seismic coefficients are obtained. This item is used only when
NCHRP2007Option = 1.

NCHRP2007SS, NCHRP2007S1

The seismic coefficients Ss and S1. This item is used only when NCHRP2007Option = 2.


NCHRP2007SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
NCHRP2007Fa, NCHRP2007Fv

The site coefficients Fa and Fv. These items are used only when NCHRP2007SiteClass= 6.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a NCHRP 20-07 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncNCHRP2007()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NCHRP2007Option As Long
Dim NCHRP2007Latitude As Double
Dim NCHRP2007Longitude As Double
Dim NCHRP2007ZipCode As String
Dim NCHRP2007SS As Double
Dim NCHRP2007S1 As Double
Dim NCHRP2007SiteClass As Long
Dim NCHRP2007Fa As Double
Dim NCHRP2007Fv As Double
Dim DampRatio As Double

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

'add NCHRP2007 RS function
ret = SapModel.Func.FuncRS.SetNCHRP2007("RS-1", 1, 0, 0, "94704", 0, 0, 4, 0, 0, 0.04)

'get NCHRP2007 RS function
ret = SapModel.Func.FuncRS.GetNCHRP2007("RS-1", NCHRP2007Option,
NCHRP2007Latitude, NCHRP2007Longitude, NCHRP2007ZipCode, NCHRP2007SS,
NCHRP2007S1, NCHRP2007SiteClass, NCHRP2007Fa, NCHRP2007Fv, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetNCHRP2007

# GetNEHRP97

## Syntax

SapObject.SapModel.Func.FuncRS.GetNEHRP97

## VB6 Procedure

Function GetNEHRP97(ByVal Name As String, ByRef NEHRP97SS As Double, ByRef
NEHRP97S1 As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a NEHRP97 response spectrum function.

NEHRP97SS


The design spectral acceleration at short periods, Sds.

NEHRP97S1

The design spectral acceleration at a one second period, Sd1.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a NEHRP97 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncNEHRP97()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NEHRP97SS As Double
Dim NEHRP97S1 As Double
Dim DampRatio As Double

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

'add NEHRP97 RS function
ret = SapModel.Func.FuncRS.SetNEHRP97("RS-1", 1.2, 0.3, 0.04)

'get NEHRP97 RS function
ret = SapModel.Func.FuncRS.GetNEHRP97("RS-1", NEHRP97SS, NEHRP97S1,
DampRatio)

'close Sap2000
SapObject.ApplicationExit False


Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetNEHRP97

# GetNZS11702004_1

## Syntax

SapObject.SapModel.Func.FuncRS.GetNZS11702004_1

## VB6 Procedure

Function GetNZS11702004_1(ByVal Name As String, ByRef NZS2004SpectrumType As Long,
ByRef NZS2004SiteClass As Long, ByRef NZS2004Z As Double, ByRef NZS2004R As Double,
ByRef NZS2004DIST As Double, ByRef NZS2004ConsiderTSite As Boolean, ByRef
NZS2004TSite As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a NZS 1170 2004 response spectrum function.

NZS2004SpectrumType

This is 1 or 2, indicating the spectrum type.

```
1 = Horizontal
2 = Vertical
```
NZS2004SiteClass

This is 1, 2, 3, 4 or 5, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```

### NZS2004Z

The hazard factor, Z.

NZS2004R

The return period factor, R.

NZS2004DIST

Distance to the fault in km, used to calculate the near fault factor.

NZS2004ConsiderTSite

Indicates whether to consider the site period for the spectral shape factor.

NZS2004TSite

The low amplitude site period.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of an NZS 1170 2004 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncNZS11702004()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim NZS2004SpectrumType As Long
Dim NZS2004SiteClass As Long
Dim NZS2004Z As Double
Dim NZS2004R As Double
Dim NZS2004DIST As Double

Dim NZS2004ConsiderTSite As Boolean

Dim NZS2004TSite As Double
Dim DampRatio As Double

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

'add NZS 1170 2004 RS function
ret = SapModel.Func.FuncRS.SetNZS11702004_1("RS-1", 1, 3, 0.4, 1.3, 20, True, 1, 0.04)

'get NZS 1170 2004 RS function
ret = SapModel.Func.FuncRS.GetNZS11702004_1("RS-1", NZS2004SpectrumType,
NZS2004SiteClass, NZS2004Z, NZS2004R, NZS2004DIST, NZS2004ConsiderTSite,
NZS2004TSite, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v21.0.0.

This function supersedes GetNZS11702004

## See Also

SetNZS11702004_1

# GetNZS42031992

## Syntax

SapObject.SapModel.Func.FuncRS.GetNZS42031992

## VB6 Procedure

Function GetNZS42031992(ByVal Name As String, ByRef NZS4203SF As Double, ByRef
NZS4203S As Long, ByRef DampRatio As Double) As Long


**Parameters**

Name

The name of a NZS4203-1992 response spectrum function.

NZS4203SF

The scaling factor (Sm * Sp * R * Z * L).

NZS4203S

This is 1, 2 or 3, indicating the site subsoil category.

```
1 = A
2 = B
3 = C
```
DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a NZS4203-1992 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncNZS42031992()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NZS4203SF As Double
Dim NZS4203S As Long
Dim DampRatio As Double

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

'add NZS42031992 RS function
ret = SapModel.Func.FuncRS.SetNZS42031992("RS-1", 1.2, 3, 0.04)

'get NZS42031992 RS function
ret = SapModel.Func.FuncRS.GetNZS42031992("RS-1", NZS4203SF, NZS4203S,
DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetNZS42031992

# GetNTC2008

## Syntax

SapObject.SapModel.Func.FuncRS.GetNTC2008

## VB6 Procedure

Function GetNTC2008(ByVal Name As String, ByRef ParamsOption As Long, ByRef Latitude
As Double, ByRef Longitude As Double, ByRef Island As Long, ByRef LimitState As Long,
ByRef UsageClass As Long, ByRef NomLife As Double, ByRef PeakAccel As Double, ByRef F0
As Double, ByRef Tcs As Double, ByRef SpecType As Long, ByRef SoilType As Long, ByRef
Topography As Long, ByRef hRatio As Double, ByRef Damping As Double, ByRef q As
Double) As Long

## Parameters

Name

The name of a NTC2008 response spectrum function.

ParamsOption

This is 1, 2, or 3, indicating the option for defining the parameters.

```
1 = by latitude and longitude
```

```
2 = by island
3 = user specified
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when ParamsOption = 1.

Island

This is one of the following values. This item is used only when ParamsOption = 2.

```
1 = Alicudi
2 = Arcipelago Toscano
3 = Filcudi
4 = Isole Egadi
5 = Lampedusa
6 = Linosa
7 = Lipari
8 = Palmarola
9 = Panarea
10 = Pantelleria
11 = Ponza
12 = Salina
13 = Santo Stefano
14 = Sardegna
15 = Stromboli
16 = Tremiti
17 = Ustica
18 = Ventotene
19 = Vulcano
20 = Zannone
```
LimitState

This is 1, 2, 3, or 4, indicating the limit state.

```
1 = SLO
2 = SLD
3 = SLV
4 = SLC
```
UsageClass

This is 1, 2, 3, or 4, indicating the usage class.

```
1 = I
2 = II
3 = III
4 = IV
```
NomLife

The nominal life to be considered.


PeakAccel

The peak ground acceleration, ag/g.

F0

The magnitude factor, F0.

Tcs

The reference period, Tc* [s].

SpecType

This is 1, 2, 3, or 4, indicating the type of spectrum to consider.

```
1 = Elastic horizontal
2 = Elastic vertical
3 = Design horizontal
4 = Design vertical
```
SoilType

This is 1, 2, 3, 4, or 5, indicating the subsoil type.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
Topography

This is 1, 2, 3, or 4, indicating the topography type.

```
1 = T1
2 = T2
3 = T3
4 = T4
```
hRatio

The ratio for the site altitude at the base of the hill to the height of the hill.

Damping

The damping, in percent. This is only applicable for SpecType 1 and 2.

q

The behavior correction factor. This is only applicable for SpecType 3 and 4.

**Remarks**


This function retrieves the definition of a NTC2008 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetRSFuncNTC2008()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim ParamsOption As Long

Dim Latitude As Double

Dim Longitude As Double

Dim Island As Long

Dim LimitState As Long

Dim UsageClass As Long

Dim NomLife As Double

Dim PeakAccel As Double

Dim F0 As Double

Dim Tcs As Double

Dim SpecType As Long

Dim SoilType As Long

Dim Topography As Long

Dim hRatio As Double

Dim Damping As Double

Dim q As Double

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

'add NTC2008 RS function
ret = SapModel.Func.FuncRS.SetNTC2008("RS-1", 1, 45.9, 12.6, 1, 3, 2, 50, 0.2, 2.4, 0.3, 3,
2, 1, 1, 5, 1)

'get NTC2008 RS function

ret = SapModel.Func.FuncRS.GetNTC2008("RS-1", ParamsOption, Latitude, Longitude,
Island, LimitState, UsageClass, NomLife, PeakAccel, F0, Tcs, SpecType, SoilType, Topography,
hRatio, Damping, q)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 18.1.0.

## See Also

SetNTC2008

# GetNTC2018

## Syntax

SapObject.SapModel.Func.FuncRS.GetNTC2018

## VB6 Procedure

Function GetNTC2018(ByVal Name As String, ByRef ParamsOption As Long, ByRef Latitude
As Double, ByRef Longitude As Double, ByRef Island As Long, ByRef LimitState As Long,
ByRef UsageClass As Long, ByRef NomLife As Double, ByRef PeakAccel As Double, ByRef F0
As Double, ByRef Tcs As Double, ByRef SpecType As Long, ByRef SoilType As Long, ByRef
Topography As Long, ByRef hRatio As Double, ByRef Damping As Double, ByRef q As
Double) As Long

## Parameters


Name

The name of a NTC2018 response spectrum function.

ParamsOption

This is 1, 2, or 3, indicating the option for defining the parameters.

```
1 = by latitude and longitude
2 = by island
3 = user specified
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when ParamsOption = 1.

Island

This is one of the following values. This item is used only when ParamsOption = 2.

```
1 = Alicudi
2 = Arcipelago Toscano
3 = Filcudi
4 = Isole Egadi
5 = Lampedusa
6 = Linosa
7 = Lipari
8 = Palmarola
9 = Panarea
10 = Pantelleria
11 = Ponza
12 = Salina
13 = Santo Stefano
14 = Sardegna
15 = Stromboli
16 = Tremiti
17 = Ustica
18 = Ventotene
19 = Vulcano
20 = Zannone
```
LimitState

This is 1, 2, 3, or 4, indicating the limit state.

```
1 = SLO
2 = SLD
3 = SLV
4 = SLC
```
UsageClass

This is 1, 2, 3, or 4, indicating the usage class.


### 1 = I

### 2 = II

### 3 = III

### 4 = IV

NomLife

The nominal life to be considered.

PeakAccel

The peak ground acceleration, ag/g.

F0

The magnitude factor, F0.

Tcs

The reference period, Tc* [s].

SpecType

This is 1, 2, 3, or 4, indicating the type of spectrum to consider.

```
1 = Elastic horizontal
2 = Elastic vertical
3 = Design horizontal
4 = Design vertical
```
SoilType

This is 1, 2, 3, 4, or 5, indicating the subsoil type.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
Topography

This is 1, 2, 3, or 4, indicating the topography type.

```
1 = T1
2 = T2
3 = T3
4 = T4
```
hRatio

The ratio for the site altitude at the base of the hill to the height of the hill.

Damping


The damping, in percent. This is only applicable for SpecType 1 and 2.

q

The behavior correction factor. This is only applicable for SpecType 3 and 4.

**Remarks**

This function retrieves the definition of a NTC2018 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetRSFuncNTC2018()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim ParamsOption As Long

Dim Latitude As Double

Dim Longitude As Double

Dim Island As Long

Dim LimitState As Long

Dim UsageClass As Long

Dim NomLife As Double

Dim PeakAccel As Double

Dim F0 As Double

Dim Tcs As Double

Dim SpecType As Long

Dim SoilType As Long

Dim Topography As Long

Dim hRatio As Double

Dim Damping As Double

Dim q As Double

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

'add NTC2018 RS function
ret = SapModel.Func.FuncRS.SetNTC2018("RS-1", 1, 45.9, 12.6, 1, 3, 2, 50, 0.2, 2.4, 0.3, 3,
2, 1, 1, 5, 1)

'get NTC2018 RS function

ret = SapModel.Func.FuncRS.GetNTC2018("RS-1", ParamsOption, Latitude, Longitude,
Island, LimitState, UsageClass, NomLife, PeakAccel, F0, Tcs, SpecType, SoilType, Topography,
hRatio, Damping, q)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v20.1.0.

## See Also

SetNTC2018

# GetSP14133302014

## Syntax

SapObject.SapModel.Func.FuncRS.GetSP14133302014

## VB6 Procedure

Function GetSP14133302014(ByVal Name As String, ByRef Direction As Long, ByRef
Seismicity As Long, ByRef SoilCat As Long, ByRef K0Factor As Double, ByRef K1Factor As


Double, ByRef KPsiFactor As Double, ByRef NonlinSoil As Boolean, ByRef ASoil As Double,
ByRef DampRatio As Double) As Long

**Parameters**

Name

The name of a SP 14.13330.2014 response spectrum function.

Direction

This is 1, 2, 3, or 4, indicating the direction and structure type for which the response spectrum is
generated.

```
1 = Building Horizontal
2 = Building Vertical
3 = Bridge Horizontal
4 = Bridge Vertical
```
Seismicity

This is 1, 2, 3, or 4, indicating the region seismicity of the construction site.

```
1 = 6
2 = 7
3 = 8
4 = 9
```
SoilCat

This is 1, 2, 3, or 4, indicating the soil category.

```
1 = I
2 = II
3 = III
4 = IV
```
K0Factor

The K0Factor, 0 < K0 <= 2.0. This is only applicable when the Direction parameter is 1 or 3 for
horizontal spectra.

K1Factor

The K1Factor, 0 < K1 <= 1.0.

KPsiFactor


The KPsiFactor, 0.5 < KPsi <= 1.5. This is only applicable when the Direction parameter is 1 or 3
for horizontal spectra.

NonlinSoil

This item is True if nonlinear soil deformation should be accounted for. This is only applicable
when the Direction parameter is 1 or 2 for buildings and the SoilCat parameter is 3 or 4.

ASoil

The nonlinear soil deformation factor, 0 > a_soil <= 1.0. This is only applicable when the
NonlinSoil parameter is True, the Direction parameter is 1 or 2 buildings, and the SoilCat
parameter is 3 or 4.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a SP 14.13330.2014 response spectrum function.

The function returns zero if the function is successfully retrieved; otherwise it returns a nonzero
value.

**VBA Example**

Sub GetRSFuncSP14133302014()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long

Dim Direction As Long

Dim Seismicity As Long

Dim SoilCat As Long

Dim K0Factor As Double

Dim K1Factor As Double

Dim KPsiFactor As Double

Dim NonlinSoil As Boolean

Dim ASoil As Double

Dim DampRatio As Double

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

'add SP 14.13330.2014 RS function
ret = SapModel.Func.FuncRS.SetSP14133302014("RS-1", 1, 2, 2, 1.0, 0.25, 1.0, False, 0.7,
0.04)

'get SP 14.13330.2014 RS function

ret = SapModel.Func.FuncRS.GetSP14133302014("RS-1", Direction, Seismicity, SoilCat,
K0Factor, K1Factor, KPsiFactor, NonlinSoil, ASoil, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 18.2.0.

## See Also

SetSP14133302014

# GetUBC94

## Syntax

SapObject.SapModel.Func.FuncRS.GetUBC94

## VB6 Procedure

Function GetUBC94(ByVal Name As String, ByRef UBC94Z As Double, ByRef UBC94S As
Long, ByRef DampRatio As Double) As Long


**Parameters**

Name

The name of a UBC94 response spectrum function.

UBC94Z

The seismic zone factor, Z.

UBC94S

This is 1, 2 or 3, indicating the soil type.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a UBC94 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncUBC94()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim UBC94Z As Double
Dim UBC94S As Long
Dim DampRatio As Double

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

'add UBC94 RS function


ret = SapModel.Func.FuncRS.SetUBC94("RS-1", 0.35, 3, 0.04)

'get UBC94 RS function
ret = SapModel.Func.FuncRS.GetUBC94("RS-1", UBC94Z, UBC94S, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetUBC94

# GetUBC97

## Syntax

SapObject.SapModel.Func.FuncRS.GetUBC97

## VB6 Procedure

Function GetUBC97(ByVal Name As String, ByRef UBC97Ca As Double, ByRef UBC97Cv As
Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a UBC97 response spectrum function.

UBC97Ca

The seismic coefficient, Ca.

UBC97Cv

The seismic coefficient, Cv.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.


**Remarks**

This function retrieves the definition of a UBC97 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetRSFuncUBC97()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim UBC97Ca As Double
Dim UBC97Cv As Double
Dim DampRatio As Double

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

'add UBC97 RS function
ret = SapModel.Func.FuncRS.SetUBC97("RS-1", 0.36, 0.54, 0.04)

'get UBC97 RS function
ret = SapModel.Func.FuncRS.GetUBC97("RS-1", UBC97Ca, UBC97Cv, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


## See Also

SetUBC97

# GetUser

## Syntax

SapObject.SapModel.Func.FuncRS.GetUser

## VB6 Procedure

Function GetUser(ByVal Name As String, ByRef NumberItems As Long, ByRef Period() As
Double, ByRef Value() As Double, ByRef DampRatio As Double) As Long

## Parameters

Name

The name of a user defined response spectrum function.

NumberItems

The number of frequency and value pairs defined.

Period

This is an array that includes the time for each data point. [s]

Value

This is an array that includes the function value for each data point.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

## Remarks

This function retrieves the definition of a user defined response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetRSFuncUser()
'dimension variables
Dim SapObject as cOAPI


Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Tmp() As Double
Dim Val() As Double
Dim NumberItems As Long
Dim Period() As Double
Dim Value() As Double
Dim DampRatio As Double

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

'add user RS function
NumberItems = 6
ReDim Tmp(NumberItems - 1)
ReDim Val(NumberItems - 1)
Tmp(0) = 0.03: Val(0) = 0.4
Tmp(1) = 0.05: Val(1) = 2.2
Tmp(2) = 0.80: Val(2) = 2.2
Tmp(3) = 1.20: Val(3) = 1.0
Tmp(4) = 4.00: Val(4) = 0.2
Tmp(5) = 10.0: Val(5) = 0.05
ret = SapModel.Func.FuncRS.SetUser("RS-1", NumberItems, Tmp, Val, 0.04)

'get user RS function
ret = SapModel.Func.FuncRS.GetUser("RS-1", NumberItems, Period, Value, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


## See Also

SetUser

# SetAASHTO2006

## Syntax

SapObject.SapModel.Func.FuncRS.SetAASHTO2006

## VB6 Procedure

Function SetAASHTO2006(ByVal Name As String, ByVal AASHTO2006A As Double, ByVal
AASHTO2006SoilProfileType As Long, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function then that function is
modified, otherwise, a new function is added.

AASHTO2006A

The acceleration coefficient, A.

AASHTO2006SoilProfileType

This is 1, 2, 3 or 4, indicating the soil profile type.

```
1 = I
2 = II
3 = III
4 = IV
```
DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

## Remarks

This function defines an AASHTO2006 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

## VBA Example


Sub SetRSFuncAASHTO2006()
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

'add AASHTO2006 RS function
ret = SapModel.Func.FuncRS.SetAASHTO2006("RS-1", 0.3, 4, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetAASHTO2006

# SetAASHTO2007

## Syntax

SapObject.SapModel.Func.FuncRS.SetAASHTO2007

## VB6 Procedure

Function SetAASHTO2007(ByVal Name As String, ByVal AASHTO2007Option As Long,
ByVal AASHTO2007Latitude As Double, ByVal AASHTO2007Longitude As Double, ByVal
AASHTO2007ZipCode As String, ByVal AASHTO2007SS As Double, ByVal AASHTO2007S1


As Double, ByVal AASHTO2007PGA As Double, ByVal AASHTO2007SiteClass As Long,
ByVal AASHTO2007Fa As Double, ByRef AASHTO2007Fv As Double, ByVal
AASHTO2007Fpga As Double, ByVal DampRatio As Double) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

AASHTO2007Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
AASHTO2007Latitude, AASHTO2007Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when AASHTO2007Option = 0.

AASHTO2007ZipCode

The zip code for which the seismic coefficients are obtained. This item is used only when
AASHTO2007Option = 1.

AASHTO2007SS, AASHTO2007S1, AASHTO2007PGA

The seismic coefficients Ss, S1 and PGA. These items are used only when AASHTO2007Option
= 2.

AASHTO2007SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
AASHTO2007Fa, AASHTO2007Fv, AASHTO2007Fpga

The site coefficients Fa, Fv and Fpga. These items are used only when AASHTO2007SiteClass=
6.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.


**Remarks**

This function defines a AASHTO 2007 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncAASHTO2007()
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

'add AASHTO2007 RS function
ret = SapModel.Func.FuncRS.SetAASHTO2007("RS-1", 1, 0, 0, "94704", 0, 0, 0, 4, 0, 0, 0,
0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 14.00.

**See Also**

GetAASHTO2007


# SetAS11702007

## Syntax

SapObject.SapModel.Func.FuncRS.SetAS11702007

## VB6 Procedure

Function SetAS11702007(ByVal Name As String, ByVal AS2007SiteClass As Long, ByVal
AS2007kp As Double, ByVal AS2007Z As Double, ByVal AS2007Sp As Double, ByVal
AS2007Mu As Double, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function then that function is
modified, otherwise, a new function is added.

AS2007SiteClass

This is 1, 2, 3, 4 or 5, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
AS2007kp

The probability factor, kp.

AS2007Z

The hazard factor, Z.

AS2007Sp

The structural performance factor, Sp.

AS2007Mu

The structural ductility factor, u.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

## Remarks


This function defines an AS 1170.4 2007 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetRSFuncAS11702007()
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

'add AS 1170 2007 RS function
ret = SapModel.Func.FuncRS.SetAS11702007("RS-1", 3, 1.3, 0.9, 0.77, 2, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.00.

## See Also

GetAS11702007

# SetBOCA96

## Syntax


SapObject.SapModel.Func.FuncRS.SetBOCA96

**VB6 Procedure**

Function SetBOCA96(ByVal Name As String, ByVal BOCA96Aa As Double, ByVal
BOCA96Av As Double, ByVal BOCA96S As Double, ByVal BOCA96R As Double, ByVal
DampRatio As Double) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

BOCA96Aa

The effective peak acceleration, Aa.

BOCA96Av

The effective peak velocity, Av.

BOCA96S

The soil profile coefficient, S.

BOCA96R

The response modification factor, R.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a BOCA96 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncBOCA96()
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

'add BOCA96 RS function
ret = SapModel.Func.FuncRS.SetBOCA96("RS-1", 0.3, 0.3, 1.2, 1, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetBOCA96

# SetChinese2010

## Syntax

SapObject.SapModel.Func.FuncRS.SetChinese2010

## VB6 Procedure

Function SetChinese2010(ByVal Name As String, ByVal JGJ32010AlphaMax As Double, ByVal
JGJ32010SI As Long, ByVal JGJ32010Tg As Double, ByVal JGJ32010PTDF As Double, ByVal
DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.


JGJ32010AlphaMax

The maximum influence factor.

JGJ32010SI

This is 1, 2, 3, 4, 5 or 6, indicating the seismic intensity.

```
1 = 6 (0.05g)
2 = 7 (0.10g)
3 = 7 (0.15g)
4 = 8 (0.20g)
5 = 8 (0.30g)
6 = 9 (0.40g)
```
JGJ32010Tg

The characteristic ground period, Tg > 0.1. [s]

JGJ32010PTDF

The period time discount factor.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a Chinese 2010 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncChinese2010()
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

'add Chinese2010 RS function
ret = SapModel.Func.FuncRS.SetChinese2010("RS-1", 0.18, 5, 0.36, 1, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 15.0.2.

## See Also

GetChinese2010

# SetCJJ1662011

## Syntax

SapObject.SapModel.Func.FuncRS.SetCJJ1662011

## VB6 Procedure

Function SetCJJ1662011(ByVal Name As String, ByVal Direction As Long, ByVal PeakAccel As
Double, ByVal Tg As Double, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

Direction

This is 1 or 2, indicating the response spectrum direction.

```
1 = Horizontal
2 = Vertical
```
PeakAccel


The peak acceleration, A.

Tg

The characteristic ground period, Tg > 0.1. [s]

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a CJJ 166-2011 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncCJJ1662011()
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

'add CJJ 166-2011 RS function
ret = SapModel.Func.FuncRS.SetCJJ1662011("RS-1", 1, 0.35, 0.25, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**


Initial release in v18.2.0.

## See Also

GetCJJ1662011

# SetEuroCode8

## Syntax

SapObject.SapModel.Func.FuncRS.SetEuroCode8

## VB6 Procedure

Function SetEuroCode8(ByVal Name As String, ByVal EuroCode8AG As Double, ByVal
EuroCode8S As Long, ByVal EuroCode8n As Double, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

EuroCode8AG

The design ground acceleration, Ag.

EuroCode8S

This is 1, 2 or 3, indicating the subsoil class.

```
1 = A
2 = B
3 = C
```
EuroCode8n

The damping correction factor, n, where n >= 0.7.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

## Remarks

This function defines a EuroCode8 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.


## VBA Example

Sub SetRSFuncEuroCode8()
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

'add EuroCode8 RS function
ret = SapModel.Func.FuncRS.SetEuroCode8("RS-1", 0.3, 3, 1.2, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetEuroCode8

# SetEurocode82004_1

## Syntax

SapObject.SapModel.Func.FuncRS.SetEurocode82004_1

## VB6 Procedure


Function SetEurocode82004_1(ByVal Name As String, ByVal EURO2004Country As Long,
ByVal EURO2004Direction As Long, ByVal EURO2004SpectrumType As Long, ByVal
EURO2004GroundType As Long, ByVal EURO2004ag As Double, ByVal EURO2004S As
Double, ByVal EURO2004AvgoverAg As Double, ByVal EURO2004Tb As Double, ByVal
EURO2004Tc As Double, ByVal EURO2004Td As Double, ByVal EURO2004Beta As Double,
ByVal EURO2004q As Double, ByVal DampRatio As Double) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function,n that function is modified;
otherwise, a new function is added.

EURO2004Country

This is 0, 1, 5, 6, or 10 indicating the country for which the Nationally Determined Parameters
(NDPs) are specified.

```
0 = Other (NDPs are user specified)
```
```
1 = CEN Default
```
```
5 = Norway
```
```
6 = Singapore
```
```
10 = Portugal
```
EURO2004Direction

This is 1 or 2, indicating the ground motion direction.

```
1 = Horizontal
```
```
2 = Vertical (Does not apply when EURO2004Country = 6)
```
EURO2004SpectrumType

This is 1 or 2, indicating the spectrum type.

```
1 = Type 1
```
```
2 = Type 2 (Does not apply when EURO2004Country = 5 or 6)
```
EURO2004GroundType

This is 1, 2, 3, 4, 5 or 6, indicating the ground type. This item only applies when the
EURO2004Direction item is 1 (horizontal).

```
1 = A (Does not apply when EURO2004Country = 6)
```
```
2 = B (Does not apply when EURO2004Country = 6)
```

### 3 = C

### 4 = D

```
5 = E (Does not apply when EURO2004Country = 6)
```
```
6 = S1 (Only applies when EURO2004Country = 6)
```
EURO2004ag

The design ground acceleration in g, ag.

EURO2004S

The soil factor, S. This item only applies when the EURO2004Direction item is 1 (horizontal). If
the EURO2004Country item is not 0, then the input value for this item is ignored.

EURO2004AvgoverAg

The vertical ground acceleration divided by the horizontal ground acceleration, Avg/Ag. This item
only applies when the EURO2004Direction item is 2 (vertical). If the EURO2004Country item is
not 0, then the input value for this item is ignored.

EURO2004Tb

The lower limit of period of the constant spectral acceleration branch, Tb. If the
EURO2004Country item is not 0, then the input value for this item is ignored.

EURO2004Tc

The upper limit of period of the constant spectral acceleration branch, Tc. If the
EURO2004Country item is not 0, then the input value for this item is ignored.

EURO2004Td

The period defining the start of the constant displacement range, Td. If the EURO2004Country
item is not 0, then the input value for this item is ignored.

EURO2004Beta

The lower bound factor, Beta. If the EURO2004Country item is not 0, then the input value for this
item is ignored.

EURO2004q

The behavior factor, q.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a Eurocode 8 2004 response spectrum function.


The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncEurocode82004()
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

'add Eurocode 8 2004 RS function
ret = SapModel.Func.FuncRS.SetEurocode82004_1("RS-1", 1, 1, 1, 2, 0.4, 1.2, 0.9, 0.15, 0.5,
2, 0.2, 2, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 14.1.0.

This function supersedes SetEurocode82004.

Added Portugal as a Country parameter in SAP2000 Version 15.0.0 and CSiBridge Version
15.1.0.

Added Singapore as a Country parameter in v20.1.0.

**See Also**

GetEurocode82004_1


# SetFromFile

## Syntax

SapObject.SapModel.Func.FuncRS.SetFromFile

## VB6 Procedure

Function SetFromFile(ByVal Name As String, ByVal FileName As String, ByVal HeadLines As
Long, ByVal DampRatio As Double, Optional ByVal ValueType As Long = 2) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function. that function is modified;
otherwise, a new function is added.

FileName

The full path of the text file containing the function data.

HeadLines

The number of header lines in the text file to be skipped before starting to read function data.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

ValueType

This is either 1 or 2, indicating time value type.

```
1 = Frequency
2 = Period
```
## Remarks

This function defines a response spectrum function from file.

The function returns zero if the function is successfully defined, otherwise it returns a nonzero
value.

## VBA Example

Sub SetRSFuncFromFile()
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

'add RS function from file
ret = SapModel.Func.FuncRS.SetFromFile("RS-1", "C:\SapAPI\FuncRS.txt", 3, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Text File**

Following is the contents of the text file name FuncRS.txt used in the VBA Example.

Reponse Spectrum Function

One pair of Period (sec) and Acceleration (g) values per line

Acceleration values at equal spacing of 0.01 seconds.

0.030 0.500

0.125 1.355

0.587 1.355

0.660 1.355

1.562 0.576

4.000 0.219

10.00 0.037

**Release Notes**

Initial release in version 11.02.


## See Also

GetFromFile

# SetJTBG022013

## Syntax

SapObject.SapModel.Func.FuncRS.SetJTGB022013

## VB6 Procedure

Function SetJTGB022013(ByVal Name As String, ByVal Direction As Long, ByVal PeakAccel
As Double, ByVal Tg As Double, ByVal Ci As Double, ByVal Cs As Double, ByVal DampRatio
As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

Direction

This is 1, 2 or 3, indicating the response spectrum direction.

```
1 = Horizontal
2 = Vertical-Rock
3 = Vertical-Soil
```
PeakAccel

The peak acceleration, A.

Tg

The characteristic ground period, Tg > 0.1. [s]

Ci

The importance coefficient.

Cs

The site soil coefficient.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.


## Remarks

This function defines a JTG B02-2013 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetRSFuncJTGB022013()
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

'add JTG B02-2013 RS function
ret = SapModel.Func.FuncRS.SetJTGB022013("RS-1", 1, 0.18, 0.36, 0.4, 1, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v18.2.0.

## See Also

GetJTBG022013

# SetJTGT2231012020


**Syntax**

SapObject.SapModel.Func.FuncRS.SetJTGT2231012020

**VB6 Procedure**

Function SetJTGT2231012020(ByVal Name As String, ByVal PeakAccel As Double, ByVal Tg
As Double, ByVal Ci As Double, ByVal Cs As Double, ByVal DampRatio As Double) As Long

**Parameters**

Name

The name of a JTGT2231012020 response spectrum function.

PeakAccel

The peak ground acceleration.

Tg

The characteristic ground period, Tg > 0.1 [s]

Ci

The importance coefficient.

Cs

The site soil coefficient.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a JTGT2231012020 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub SetRSFuncJTGT2231012020()
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

'add JTG/T 2231-01-2020 RS function
ret = SapModel.Func.FuncRS.SetJTGT2231012020("RS-1", 0.18, 0.36, 0.4, 1, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in v23.2.0

## See Also

GetJTGT2231012020

# SetIBC2003

## Syntax

SapObject.SapModel.Func.FuncRS.SetIBC2003

## VB6 Procedure

Function SetIBC2003(ByVal Name As String, ByVal IBC2003SS As Double, ByVal IBC2003S1
As Double, ByVal DampRatio As Double) As Long


**Parameters**

Name

The name of an existing or new function. If this is an existing function then that function is
modified, otherwise, a new function is added.

IBC2003SS

The design spectral acceleration at short periods, Sds.

IBC2003S1

The design spectral acceleration at a one second period, Sd1.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a IBC2003 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncIBC2003()
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

'add IBC2003 RS function
ret = SapModel.Func.FuncRS.SetIBC2003("RS-1", 1.2, 0.3, 0.04)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetIBC2003

# SetIBC2006

## Syntax

SapObject.SapModel.Func.FuncRS.SetIBC2006

## VB6 Procedure

Function SetIBC2006(ByVal Name As String, ByVal IBC2006Option As Long, ByVal
IBC2006Latitude As Double, ByVal IBC2006Longitude As Double, ByVal IBC2006ZipCode As
String, ByVal IBC2006SS As Double, ByVal IBC2006S1 As Double, ByVal IBC2006TL As
Double, ByVal IBC2006SiteClass As Long, ByVal IBC2006Fa As Double, ByRef IBC2006Fv As
Double, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function then that function is
modified; otherwise, a new function is added.

IBC2006Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitiude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
IBC2006Latitude, IBC2006Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when IBC2006Option = 0.

IBC2006ZipCode


The zip code for which the seismic coefficients are obtained. This item is used only when
IBC2006Option = 1.

IBC2006SS, IBC2006S1

The seismic coefficients Ss and S1. This item is used only when IBC2006Option = 2.

IBC2006TL

The long-period transition period. [s]

IBC2006SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
IBC2006Fa, IBC2006Fv

The site coefficients Fa and Fv. These items are used only when IBC2006SiteClass= 6.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a IBC2006 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncIBC2006()
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

'add IBC2006 RS function
ret = SapModel.Func.FuncRS.SetIBC2006("RS-1", 1, 0, 0, "94704", 0, 0, 7.5, 4, 0, 0, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetIBC2006

# SetIS18932002

## Syntax

SapObject.SapModel.Func.FuncRS.SetIS18932002

## VB6 Procedure

Function SetIS18932002(ByVal Name As String, ByVal INZ As Double, ByVal INS As Long,
ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

INZ

The seismic zone factor, Z.

INS

This is 1, 2 or 3, indicating the soil type.


### 1 = I

### 2 = II

### 3 = III

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a IS1893-2002 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncIS18932002()
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

'add IS18932002 RS function
ret = SapModel.Func.FuncRS.SetIS18932002("RS-1", 0.3, 3, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


## See Also

GetIS18932002

# SetItalian3274

## Syntax

SapObject.SapModel.Func.FuncRS.SetItalian3274

## VB6 Procedure

Function SetItalian3274(ByVal Name As String, ByVal Italag As Double, ByVal ItalSoilType As
Long, ByVal Italq As Double, ByVal ItalLevel As Double, ByVal DampRatio As Double) As
Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

Italag

The peak ground acceleration.

ItalSoilType

This is 1, 2, 3, 4 or 5, indicating the seismic intensity.

```
1 = A
2 = B
3 = C
4 = E
5 = D
```
Italq

The structure factor.

ItalLevel

This is 0, 1, 2, 3, 4, 5, 6 or 7, indicating the spectral level, direction and building type.

```
0 = SLU/H/Building
1 = SLU/H/Bridge
2 = SLU/V/Building
3 = SLU/V/Bridge
4 = EL/H/Building
```

```
5 = EL/H/Bridge
6 = EL/V/Building
7 = EL/V/Bridge
```
SLU refers to ultimate strength design and EL refers to elastic design. H and V are horizontal and
vertical, respectively.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a Italian 3274 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncItalian3274()
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

'add Italian3274 RS function
ret = SapModel.Func.FuncRS.SetItalian3274("RS-1", 0.3, 2, 1.1, 4, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.02.

## See Also

GetItalian3274

# SetNBCC2015

## Syntax

SapObject.SapModel.Func.FuncRS.SetNBCC2015

## VB6 Procedure

Function SetNBCC2015(ByVal Name As String, ByVal PGA As Double, ByVal S02 As Double,
ByVal S05 As Double, ByVal S1 As Double, ByVal S2 As Double, ByVal S5 As Double, ByVal
S10 As Double, ByVal SiteClass As Long, ByVal F02 As Double, ByVal F05 As Double, ByVal
F1 As Double, ByVal F2 As Double, ByVal F5 As Double, ByVal F10 As Double, ByVal
DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

PGA

The peak ground acceleration.

S02

The spectral acceleration at a 0.2 second period.

S05

The spectral acceleration at a 0.5 second period.

S1

The spectral acceleration at a 1 second period.

S2

The spectral acceleration at a 2 second period.

S5


The spectral acceleration at a 5 second period.

S10

The spectral acceleration at a 10 second period.

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
F02

The site coefficient at a 0.2 second period. This item is read when the site class is F only.

F05

The site coefficient at a 0.5 second period. This item is read when the site class is F only.

F1

The site coefficient at a 1 second period. This item is read when the site class is F only.

F2

The site coefficient at a 2 second period. This item is read when the site class is F only.

F5

The site coefficient at a 5 second period. This item is read when the site class is F only.

F10

The site coefficient at a 10 second period. This item is read when the site class is F only.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a NBCC2015 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**


Sub SetRSFuncNBCC2015()
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

'add NBCC2015 RS function
ret = SapModel.Func.FuncRS.SetNBCC2015("RS-1", 0.6, 1.1, 0.7, 0.35, 0.2, 0.035, 0.01, 6,
1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 19.0.0.

## See Also

GetNBCC2015

# SetNBCC2010

## Syntax

SapObject.SapModel.Func.FuncRS.SetNBCC2010


**VB6 Procedure**

Function SetNBCC2010(ByVal Name As String, ByVal PGA As Double, ByVal S02 As Double,
ByVal S05 As Double, ByVal S1 As Double, ByVal S2 As Double, ByVal SiteClass As Long,
ByVal Fa As Double, ByVal Fv As Double, ByVal DampRatio As Double) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

PGA

The peak ground acceleration.

S02

The spectral acceleration at a 0.2 second period.

S05

The spectral acceleration at a 0.5 second period.

S1

The spectral acceleration at a 1 second period.

S2

The spectral acceleration at a 2 second period.

SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
Fa

The site coefficient, Fa. This item is read when the site class is F only.

Fv

The site coefficient, Fv. This item is read when the site class is F only.

DampRatio


The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a NBCC2010 response spectrum function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub SetRSFuncNBCC2010()
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

'add NBCC2010 RS function
ret = SapModel.Func.FuncRS.SetNBCC2010("RS-1", 0.6, 1.1, 0.7, 0.35, 0.2, 6, 1.8, 2, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 19.0.0.

**See Also**

GetNBCC2010


# SetNBCC2005

## Syntax

SapObject.SapModel.Func.FuncRS.SetNBCC2005

## VB6 Procedure

Function SetNBCC2005(ByVal Name As String, ByVal NBCC2005PGA As Double, ByVal
NBCC2005S02 As Double, ByVal NBCC2005S05 As Double, ByVal NBCC2005S1 As Double,
ByVal NBCC2005S2 As Double, ByVal NBCC2005SiteClass As Long, ByVal NBCC2005Fa As
Double, ByVal NBCC2005Fv As Double, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

NBCC2005PGA

The peak ground acceleration.

NBCC2005S02

The spectral acceleration at a 0.2 second period.

NBCC2005S05

The spectral acceleration at a 0.52 second period.

NBCC2005S1

The spectral acceleration at a 1 second period.

NBCC2005S2

The spectral acceleration at a 2 second period.

NBCC2005SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```

### 6 = F

NBCC2005Fa

The site coefficient, Fa. This item is read when the site class is F only.

NBCC2005Fv

The site coefficient, Fv. This item is read when the site class is F only.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a NBCC2005 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncNBCC2005()
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

'add NBCC2005 RS function
ret = SapModel.Func.FuncRS.SetNBCC2005("RS-1", 0.6, 1.1, 0.7, 0.35, 0.2, 6, 1.8, 2, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 12.00.

## See Also

GetNBCC2005

# SetNBCC95

## Syntax

SapObject.SapModel.Func.FuncRS.SetNBCC95

## VB6 Procedure

Function SetNBCC95(ByVal Name As String, ByVal NBCC95ZVR As Double, ByVal
NBCC95ZA As Long, ByVal NBCC95ZV As Long, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function then that function is
modified; otherwise, a new function is added.

NBCC95ZVR

The zonal velocity ratio.

NBCC95ZA

The acceleration-related seismic zone.

NBCC95ZV

The velocity-related seismic zone.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

## Remarks

This function defines a NBCC95 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.


## VBA Example

Sub SetRSFuncNBCC95()
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

'add NBCC95 RS function
ret = SapModel.Func.FuncRS.SetNBCC95("RS-1", 0.3, 5, 5, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetNBCC95

# SetNCHRP2007

## Syntax

SapObject.SapModel.Func.FuncRS.SetNCHRP2007

## VB6 Procedure


Function SetNCHRP2007(ByVal Name As String, ByVal NCHRP2007Option As Long, ByVal
NCHRP2007Latitude As Double, ByVal NCHRP2007Longitude As Double, ByVal
NCHRP2007ZipCode As String, ByVal NCHRP2007SS As Double, ByVal NCHRP2007S1 As
Double, ByVal NCHRP2007SiteClass As Long, ByVal NCHRP2007Fa As Double, ByRef
NCHRP2007Fv As Double, ByVal DampRatio As Double) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

NCHRP2007Option

This is 0, 1 or 2, indicating the seismic coefficient option.

```
0 = Ss and S1 from USGS by latitiude and longitude
1 = Ss and S1 from USGS by zip code
2 = Ss and S1 are user defined
```
NCHRP2007Latitude, NCHRP2007Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are used
only when NCHRP2007Option = 0.

NCHRP2007ZipCode

The zip code for which the seismic coefficients are obtained. This item is used only when
NCHRP2007Option = 1.

NCHRP2007SS, NCHRP2007S1

The seismic coefficients Ss and S1. This item is used only when NCHRP2007Option = 2.

NCHRP2007SiteClass

This is 1, 2, 3, 4, 5 or 6, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
6 = F
```
NCHRP2007Fa, NCHRP2007Fv

The site coefficients Fa and Fv. These items are used only when NCHRP2007SiteClass= 6.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.


## Remarks

This function defines a NCHRP 20-07 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetRSFuncNCHRP2007()
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

'add NCHRP2007 RS function
ret = SapModel.Func.FuncRS.SetNCHRP2007("RS-1", 1, 0, 0, "94704", 0, 0, 4, 0, 0, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetNCHRP2007

# SetNEHRP97


**Syntax**

SapObject.SapModel.Func.FuncRS.SetNEHRP97

**VB6 Procedure**

Function SetNEHRP97(ByVal Name As String, ByVal NEHRP97SS As Double, ByVal
NEHRP97S1 As Double, ByVal DampRatio As Double) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function then that function is
modified; otherwise, a new function is added.

NEHRP97SS

The design spectral acceleration at short periods, Sds.

NEHRP97S1

The design spectral acceleration at a one second period, Sd1.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a NEHRP97 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncNEHRP97()
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

'add NEHRP97 RS function
ret = SapModel.Func.FuncRS.SetNEHRP97("RS-1", 1.2, 0.3, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetNEHRP97

# SetNTC2008

## Syntax

SapObject.SapModel.Func.FuncRS.SetNTC2008

## VB6 Procedure

Function SetNTC2008(ByVal Name As String, ByVal ParamsOption As Long, ByVal Latitude
As Double, ByVal Longitude As Double, ByVal Island As Long, ByVal LimitState As Long,
ByVal UsageClass As Long, ByVal NomLife As Double, ByVal PeakAccel As Double, ByVal F0
As Double, ByVal Tcs As Double, ByVal SpecType As Long, ByVal SoilType As Long, ByVal
Topography As Long, ByVal hRatio As Double, ByVal Damping As Double, ByVal q As
Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

ParamsOption


This is 1, 2, or 3, indicating the option for defining the parameters.

```
1 = by latitude and longitude
2 = by island
3 = user specified
```
Latitude, Longitude

The latitude and longitude for which the seismic coefficients are obtained. These items are
meaningful only when ParamsOption = 1.

Island

This is one of the following values. This item is used only when ParamsOption = 2.

```
1 = Alicudi
2 = Arcipelago Toscano
3 = Filcudi
4 = Isole Egadi
5 = Lampedusa
6 = Linosa
7 = Lipari
8 = Palmarola
9 = Panarea
10 = Pantelleria
11 = Ponza
12 = Salina
13 = Santo Stefano
14 = Sardegna
15 = Stromboli
16 = Tremiti
17 = Ustica
18 = Ventotene
19 = Vulcano
20 = Zannone
```
LimitState

This is 1, 2, 3, or 4, indicating the limit state.

```
1 = SLO
2 = SLD
3 = SLV
4 = SLC
```
UsageClass

This is 1, 2, 3, or 4, indicating the usage class.

```
1 = I
2 = II
3 = III
4 = IV
```

NomLife

The nominal life to be considered.

PeakAccel

The peak ground acceleration, ag/g.

F0

The magnitude factor, F0.

Tcs

The reference period, Tc* [s].

SpecType

This is 1, 2, 3, or 4, indicating the type of spectrum to consider.

```
1 = Elastic horizontal
2 = Elastic vertical
3 = Design horizontal
4 = Design vertical
```
SoilType

This is 1, 2, 3, 4, or 5, indicating the subsoil type.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
Topography

This is 1, 2, 3, or 4, indicating the topography type.

```
1 = T1
2 = T2
3 = T3
4 = T4
```
hRatio

The ratio for the site altitude at the base of the hill to the height of the hill.

Damping

The damping, in percent. This is only applicable for SpecType 1 and 2.

q

The behavior correction factor. This is only applicable for SpecType 3 and 4.


**Remarks**

This function defines a NTC2008 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncNTC2008()
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

'add NTC2008 RS function
ret = SapModel.Func.FuncRS.SetNTC2008("RS-1", 1, 45.9, 12.6, 1, 3, 2, 50, 0.2, 2.4, 0.3, 3,
2, 1, 1, 5, 1)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 18.1.0.

**See Also**

GetNTC2008


# SetNZS11702004_1

## Syntax

SapObject.SapModel.Func.FuncRS.SetNZS11702004_1

## VB6 Procedure

Function SetNZS11702004_1(ByVal Name As String, ByRef NZS2004SpectrumType As Long,
ByVal NZS2004SiteClass As Long, ByVal NZS2004Z As Double, ByVal NZS2004R As Double,
ByVal NZS2004DIST As Double, ByVal NZS2004ConsiderTSite As Boolean, ByVal
NZS2004TSite As Double, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

NZS2004SpectrumType

This is 1 or 2, indicating the spectrum type.

```
1 = Horizontal
2 = Vertical
```
NZS2004SiteClass

This is 1, 2, 3, 4 or 5, indicating the site class.

```
1 = A
2 = B
3 = C
4 = D
5 = E
```
NZS2004Z

The hazard factor, Z.

NZS2004R

The return period factor, R.

NZS2004DIST

Distance to the fault in kim, used to calculate the near fault factor.

NZS2004ConsiderTSite


Indicates whether to consider the site period for the spectral shape factor.

NZS2004TSite

The low amplitude site period.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines an NZS 1170.5 2004 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncNZS11702004()
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

'add NZS 1170 2004 RS function
ret = SapModel.Func.FuncRS.SetNZS11702004_1("RS-1", 1, 3, 0.4, 1.3, 20, True, 1, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**


Initial release in v21.0.0.

This function supersedes SetNZS11702004

## See Also

GetNZS11702004_1

# SetNZS42031992

## Syntax

SapObject.SapModel.Func.FuncRS.SetNZS42031992

## VB6 Procedure

Function SetNZS42031992(ByVal Name As String, ByVal NZS4203SF As Double, ByVal
NZS4203S As Long, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

NZS4203SF

The scaling factor (Sm * Sp * R * Z * L).

NZS4203S

This is 1, 2 or 3, indicating the site subsoil category.

```
1 = A
2 = B
3 = C
```
DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

## Remarks

This function defines a NZS4203-1992 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.


## VBA Example

Sub SetRSFuncNZS42031992()
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

'add NZS42031992 RS function
ret = SapModel.Func.FuncRS.SetNZS42031992("RS-1", 1.2, 3, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetNZS42031992

# SetSP14133302014

## Syntax

SapObject.SapModel.Func.FuncRS.SetSP14133302014

## VB6 Procedure


Function SetSP14133302014(ByVal Name As String, ByVal Direction As Long, ByVal
Seismicity As Long, ByVal SoilCat As Long, ByVal K0Factor As Double, ByVal K1Factor As
Double, ByVal KPsiFactor As Double, ByVal NonlinSoil As Boolean, ByVal ASoil As Double,
ByVal DampRatio As Double) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

Direction

This is 1, 2, 3, or 4, indicating the direction and structure type for which the response spectrum is
generated.

```
1 = Building Horizontal
2 = Building Vertical
3 = Bridge Horizontal
4 = Bridge Vertical
```
Seismicity

This is 1, 2, 3, or 4, indicating the region seismicity of the construction site.

```
1 = 6
2 = 7
3 = 8
4 = 9
```
SoilCat

This is 1, 2, 3, or 4, indicating the soil category.

```
1 = I
2 = II
3 = III
4 = IV
```
K0Factor

The K0Factor, 0 < K0 <= 2.0. This is only applicable when the Direction parameter is 1 or 3 for
horizontal spectra.

K1Factor

The K1Factor, 0 < K1 <= 1.0.


KPsiFactor

The KPsiFactor, 0.5 < KPsi <= 1.5. This is only applicable when the Direction parameter is 1 or 3
for horizontal spectra.

NonlinSoil

This item is True if nonlinear soil deformation should be accounted for. This is only applicable
when the Direction parameter is 1 or 2 for buildings and the SoilCat parameter is 3 or 4.

ASoil

The nonlinear soil deformation factor, 0 > a_soil <= 1.0. This is only applicable when the
NonlinSoil parameter is True, the Direction parameter is 1 or 2 buildings, and the SoilCat
parameter is 3 or 4.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function retrieves the definition of a SP 14.13330.2014 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncSP14133302014()
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

'add SP 14.13330.2014 RS function


ret = SapModel.Func.FuncRS.SetSP14133302014("RS-1", 1, 2, 2, 1.0, 0.25, 1.0, False, 0.7,
0.04)

'get SP 14.13330.2014 RS function

ret = SapModel.Func.FuncRS.GetSP14133302014("RS-1", Direction, Seismicity, SoilCat,
K0Factor, K1Factor, KPsiFactor, NonlinSoil, ASoil, DampRatio)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 18.2.0.

## See Also

GetSP14133302014

# SetUBC94

## Syntax

SapObject.SapModel.Func.FuncRS.SetUBC94

## VB6 Procedure

Function SetUBC94(ByVal Name As String, ByVal UBC94Z As Double, ByVal UBC94S As
Long, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

UBC94Z

The seismic zone factor, Z.

UBC94S

This is 1, 2 or 3, indicating the soil type.


DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a UBC94 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncUBC94()
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

'add UBC94 RS function
ret = SapModel.Func.FuncRS.SetUBC94("RS-1", 0.35, 3, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

**See Also**

GetUBC94


# SetUBC97

## Syntax

SapObject.SapModel.Func.FuncRS.SetUBC97

## VB6 Procedure

Function SetUBC97(ByVal Name As String, ByVal UBC97Ca As Double, ByVal UBC97Cv As
Double, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

UBC97Ca

The seismic coefficient, Ca.

UBC97Cv

The seismic coefficient, Cv.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

## Remarks

This function defines a UBC97 response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetRSFuncUBC97()
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

'add UBC97 RS function
ret = SapModel.Func.FuncRS.SetUBC97("RS-1", 0.36, 0.54, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetUBC97

# SetUser

## Syntax

SapObject.SapModel.Func.FuncRS.SetUser

## VB6 Procedure

Function SetUser(ByVal Name As String, ByVal NumberItems As Long, ByRef Period() As
Double, ByRef Value() As Double, ByVal DampRatio As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

NumberItems


The number of period and value pairs defined.

Period

This is an array that includes the period for each data point. [s]

Value

This is an array that includes the function value for each data point.

DampRatio

The damping ratio for the function, 0 <= DampRatio < 1.

**Remarks**

This function defines a user response spectrum function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetRSFuncUser()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim Period() As Double
Dim Value() As Double

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

'add user RS function
NumberItems = 6
ReDim Period(NumberItems - 1)
ReDim Value(NumberItems - 1)
Period(0) = 0.03: Value(0) = 0.4


Period(1) = 0.05: Value(1) = 2.2
Period(2) = 0.80: Value(2) = 2.2
Period(3) = 1.20: Value(3) = 1.0
Period(4) = 4.00: Value(4) = 0.2
Period(5) = 10.0: Value(5) = 0.05
ret = SapModel.Func.FuncRS.SetUser("RS-1", NumberItems, Period, Value, 0.04)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetUser

# GetFromFile

## Syntax

SapObject.SapModel.Func.FuncSS.GetFromFile

## VB6 Procedure

Function GetFromFile(ByVal Name As String, ByRef FileName As String, ByRef HeadLines As
Long, ByRef PreChars As Long, ByRef PointsPerLine As Long, ByRef ValueType As Long,
ByRef FreeFormat As Boolean, ByRef NumberFixed As Long, ByRef FreqTypeInFile As Long)
As Long

## Parameters

Name

The name of a defined steady state function specified to be from a text file.

FileName

The full path of the text file containing the function data.

HeadLines

The number of header lines in the text file to be skipped before starting to read function data.

PreChars


The number of prefix characters to be skipped on each line in the text file.

PointsPerLine

The number of function points included on each text file line.

ValueType

This is either 1 or 2, indicating value type.

```
1 = Values at equal time intervals
2 = Time and function values
```
FreeFormat

This item is True if the data is provided in a free format. It is False if it is in a fixed format.

NumberFixed

This item only applies when the FreeFormat item is False. It is the number of characters per item.

FreqTypeInFile

This is either 1 or 2, indicating frequency type.

```
1 = Hz
2 = RPM
```
**Remarks**

This function retrieves the definition of a steady state function from file.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetSSFuncFromFile()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim HeadLines As Long
Dim PreChars As Long
Dim PointsPerLine As Long
Dim ValueType As Long
Dim FreeFormat As Boolean
Dim NumberFixed As Long
Dim FreqTypeInFile As Long

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

'add SS function from file
ret = SapModel.Func.FuncSS.SetFromFile("SS-1", "C:\SapAPI\FuncSS.txt", 2, 0, 1, 2, True)

'get SS function from file
ret = SapModel.Func.FuncSS.GetFromFile("SS-1", FileName, HeadLines, PreChars,
PointsPerLine, ValueType, FreeFormat, NumberFixed, FreqTypeInFile)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Text File**

Following is the contents of the text file name FuncSS.txt used in the VBA Example.

Steady State Function

One pair of Frequency (Hz) and Value items per line

0 1

1 1

2 2

3 2

**Release Notes**

Initial release in version 11.02.

**See Also**

SetFromFile


# GetUser

## Syntax

SapObject.SapModel.Func.FuncSS.GetUser

## VB6 Procedure

Function GetUser(ByVal Name As String, ByRef NumberItems As Long, ByRef Frequency() As
Double, ByRef Value() As Double) As Long

## Parameters

Name

The name of a user defined steady state function.

NumberItems

The number of frequency and value pairs defined.

Frequency

This is an array that includes the frequency in Hz for each data point. [cyc/s]

Value

This is an array that includes the function value for each data point.

## Remarks

This function retrieves the definition of a user defined steady state function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetSSFuncUser()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Freq() As Double
Dim Val() As Double
Dim NumberItems As Long
Dim Frequency() As Double
Dim Value() As Double


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

'add user SS function
Num = 4
ReDim Freq(Num - 1)
ReDim Val(Num - 1)
Freq(0) = 0: Val(0) = 1
Freq(1) = 1: Val(1) = 1
Freq(2) = 2: Val(2) = 2
Freq(3) = 3: Val(3) = 2
ret = SapModel.Func.FuncSS.SetUser("SS-1", Num, Freq, Val)

'get user SS function
ret = SapModel.Func.FuncSS.GetUser("SS-1", NumberItems, Frequency, Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetUser

# SetFromFile

## Syntax

SapObject.SapModel.Func.FuncSS.SetFromFile


**VB6 Procedure**

Function SetFromFile(ByVal Name As String, ByVal FileName As String, ByVal HeadLines As
Long, ByVal PreChars As Long, ByVal PointsPerLine As Long, ByVal ValueType As Long,
ByVal FreeFormat As Boolean, Optional ByVal NumberFixed As Long = 10, Optional ByVal
FreqTypeInFile As Long = 1) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

FileName

The full path of the text file containing the function data.

HeadLines

The number of header lines in the text file to be skipped before starting to read function data.

PreChars

The number of prefix characters to be skipped on each line in the text file.

PointsPerLine

The number of function points included on each text file line.

ValueType

This is either 1 or 2, indicating value type.

```
1 = Values at equal time intervals
2 = Time and function values
```
FreeFormat

This item is True if the data is provided in a free format. It is False if it is in a fixed format.

NumberFixed

This item only applies when the FreeFormat item is False. It is the number of characters per item.

FreqTypeInFile

This is either 1 or 2, indicating frequency type.

```
1 = Hz
2 = RPM
```

**Remarks**

This function defines a steady state function from file.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetSSFuncFromFile()
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

'add SS function from file
ret = SapModel.Func.FuncSS.SetFromFile("SS-1", "C:\SapAPI\FuncSS.txt", 2, 0, 1, 2, True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Text File**

Following is the contents of the text file name FuncSS.txt used in the VBA Example.

Steady State Function

One pair of Frequency (Hz) and Value items per line

0 1

1 1

2 2


### 3 2

## Release Notes

Initial release in version 11.02.

## See Also

GetFromFile

# SetUser

## Syntax

SapObject.SapModel.Func.FuncSS.SetUser

## VB6 Procedure

Function SetUser(ByVal Name As String, ByVal NumberItems As Long, ByRef Frequency() As
Double, ByRef Value() As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

NumberItems

The number of frequency and value pairs defined.

Frequency

This is an array that includes the frequency in Hz for each data point. [cyc/s]

Value

This is an array that includes the function value for each data point.

## Remarks

This function defines a user steady state function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.


**VBA Example**

Sub SetSSFuncUser()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim Frequency() As Double
Dim Value() As Double

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

'add user SS function
NumberItems = 4
ReDim Frequency(NumberItems - 1)
ReDim Value(NumberItems - 1)
Frequency(0) = 0: Value(0) = 1
Frequency(1) = 1: Value(1) = 1
Frequency(2) = 2: Value(2) = 2
Frequency(3) = 3: Value(3) = 2
ret = SapModel.Func.FuncSS.SetUser("SS-1", NumberItems, Frequency, Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

**See Also**

GetUser


# GetCosine

## Syntax

SapObject.SapModel.Func.FuncTH.GetCosine

## VB6 Procedure

Function GetCosine(ByVal Name As String, ByRef CosineP As Double, ByRef CosineSteps As
Long, ByRef CosineCycles As Long, ByRef CosineAmp As Double) As Long

## Parameters

Name

The name of a cosine-type time history function.

CosineP

The period of the cosine function. [s]

CosineSteps

The number of steps in the cosine function. This item can not be less than 8.

CosineCycles

The number of cycles in the cosine function.

CosineAmp

The amplitude of the cosine function.

## Remarks

This function retrieves the definition of a cosine-type time history function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetTHFuncCosine()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim CosineP As Double
Dim CosineSteps As Long
Dim CosineCycles As Long


Dim CosineAmp As Double

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

'add cosine TH function
ret = SapModel.Func.FuncTH.SetCosine("TH-1", 1, 16, 4, 1.25)

'get cosine TH function
ret = SapModel.Func.FuncTH.GetCosine("TH-1", CosineP, CosineSteps, CosineCycles,
CosineAmp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetCosine

# GetFromFile_1

## Syntax

SapObject.SapModel.Func.FuncTH.GetFromFile_1

## VB6 Procedure

Function GetFromFile_1(ByVal Name As String, ByRef FileName As String, ByRef HeadLines
As Long, ByRef PreChars As Long, ByRef PointsPerLine As Long, ByRef ValueType As Long,
ByRef FreeFormat As Boolean, ByRef NumberFixed As Long, DT As Double) As Long


**Parameters**

Name

The name of a defined time history function specified to be from a text file.

FileName

The full path of the text file containing the function data.

HeadLines

The number of header lines in the text file to be skipped before starting to read function data.

PreChars

The number of prefix characters to be skipped on each line in the text file.

PointsPerLine

The number of function points included on each text file line.

ValueType

This is 1 or 2, indicating value type.

```
1 = Values at equal time intervals
```
```
2 = Time and function values
```
FreeFormat

This item is True if the data is provided in a free format. It is False if it is in a fixed format.

NumberFixed

This item applies only when the FreeFormat item is False. It is the number of characters per item.

DT

This item applies only when the ValueType item is 1 (equal time intervals). It is the time interval
between function points.

**Remarks**

This function retrieves the definition of a time history function from file.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**


Sub GetTHFuncFromFile_1()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim FileName As String
Dim HeadLines As Long
Dim PreChars As Long
Dim PointsPerLine As Long
Dim ValueType As Long
Dim FreeFormat As Boolean
Dim NumberFixed As Long
Dim DT As Double

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

'add TH function from file
ret = SapModel.Func.FuncTH.SetFromFile_1("TH-1", "C:\SapAPI\FuncTH.txt", 3, 0, 3, 2,
True)

'get TH function from file
ret = SapModel.Func.FuncTH.GetFromFile_1("TH-1", FileName, HeadLines, PreChars,
PointsPerLine, ValueType, FreeFormat, NumberFixed, DT)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Text File**

Following is the contents of the text file name FuncTH.txt used in the VBA Example.

Time History Function

Time (sec) and Acceleration (g) values

3 points per line


### 0.00000 .01080 .04200 .00100 .09700 .01590

### .16100 -.00010 .22100 .01890 .26300 .00010

### .29100 .00590 .33200 -.00120 .37400 .02000

### .42900 -.02370 .47100 .00760 .58100 .04250

### .62300 .00940 .66500 .01380 .72000 -.00880

### .72010 -.02560 .78900 -.03870 .78910 -.05680

### .87200 -.02320 .87210 -.03430 .94100 -.04020

### .94110 -.06030 .99700 -.07890 1.06600 -.06660

### 1.06610 -.03810 1.09400 -.04290 1.16800 .08970

### 1.31500 -.16960 1.38400 -.08280 1.41200 -.08280

### 1.44000 -.09450 1.48100 -.08850 1.50900 -.10800

### 1.53700 -.12800 1.62800 .11440 1.70300 .23550

### 1.80000 .14280 1.85500 .17770 1.92400 -.26100

### 2.00700 -.31940 2.21500 .29520 2.27000 .26340

### 2.32000 -.29840 2.39500 .00540 2.45000 .28650

### 2.51900 -.04690 2.57500 .15160 2.65200 .20770

### 2.70800 .10870 2.76900 -.03250 2.89300 .10330

### 2.97600 -.08030 3.06800 .05200 3.12900 -.15470

### 3.21200 .00650 3.25300 -.20600 3.38600 .19270

### 3.41900 -.09370 3.53000 .17080 3.59900 -.03590

### 3.66800 .03650 3.73800 -.07360 3.83500 .03110

### 3.90400 -.18330 4.01400 .02270 4.05600 -.04350

### 4.10600 .02160 4.22200 -.19720 4.31400 -.17620

### 4.41600 .14600 4.47100 -.00470 4.61800 .25720

### 4.66500 -.20450 4.75600 .06080 4.83100 -.27330

### 4.97000 .17790 5.03900 .03010 5.10800 .21830

### 5.19900 .02670 5.23300 .12520 5.30200 .12900

### 5.33000 .10890 5.34300 -.02390 5.45400 .17230

### 5.51000 -.10210 5.60600 .01410 5.69000 -.19490

### 5.77300 -.02420 5.80000 -.00500 5.80900 -.02750

### 5.86900 -.05730 5.88300 -.03270 5.92500 .02160

### 5.98000 .01080 6.01300 .02350 6.08500 -.06650

### 6.13200 .00140 6.17400 .04930 6.18800 .01490

### 6.18810 -.02000 6.22900 -.03810 6.27900 .02070

### 6.32600 -.00580 6.36800 -.06030 6.38200 -.01620

### 6.40900 .02000 6.45900 -.01760 6.47800 -.00330

### 6.52000 .00430 6.53400 -.00400 6.56200 -.00990

### 6.57500 -.00170 6.60300 -.01700 6.64500 .03730

### 6.68600 .04570 6.71400 .03850 6.72800 .00090

### 6.76900 -.02880 6.76910 .00160 6.81100 .01130

### 6.85200 .00220 6.90800 .00920 6.99100 -.09960

### 7.07400 .03600 7.12100 .00780 7.14300 -.02770

### 7.14900 .00260 7.17100 .02720 7.22600 .05760

### 7.29500 -.04920 7.37000 .02970 7.40600 .01090

### 7.42500 .01860 7.46100 -.02530 7.52500 -.03470

### 7.57200 .00360 7.60000 -.06280 7.64100 -.02800

### 7.66900 -.01960 7.69100 .00680 7.75200 -.00540

### 7.79400 -.06030 7.83500 -.03570 7.87700 -.07160

### 7.96000 -.01400 7.98700 -.00560 8.00100 .02220

### 8.07000 .04680 8.12600 .02600 8.12610 -.03350

### 8.19500 -.01280 8.22300 .06610 8.27800 .03050

### 8.33400 .02460 8.40300 .03470 8.45800 -.03690

### 8.53300 -.03440 8.59600 -.01040 8.63800 -.02600


### 8.73500 .15340 8.81800 -.00280 8.86000 .02330

### 8.88200 -.02610 8.91500 -.00220 8.95600 -.18490

### 9.05300 .12600 9.09500 .03200 9.12300 .09550

### 9.15000 .12460 9.25300 -.03280 9.28900 -.04510

### 9.42700 .13010 9.44100 -.16570 9.51000 .04190

### 9.63500 -.09360 9.70400 .08160 9.81500 -.08810

### 9.89800 .00640 9.93900 -.00060 9.99500 .05860

### 10.02200 -.07130 10.05000 -.04480 10.05010 -.02210

### 10.10500 .00930 10.10510 .00240 10.18800 .05100

### 10.27200 -.12430 10.38200 .05870 10.42400 .01330

### 10.45200 .03860 10.46500 .11640 10.50700 -.03740

### 10.53400 -.05720 10.64500 .03080 10.70100 .02230

### 10.71400 .05150 10.77000 .09030 10.83900 -.01940

### 10.92200 .04710 10.92210 -.06770 10.96400 -.07940

### 10.99100 -.01200 11.07400 .06080 11.08800 -.02690

### 11.11600 -.04160 11.20700 .02930 11.20710 .05520

### 11.22700 .07560 11.26800 .04310 11.32400 .02080

### 11.43400 .11800 11.57300 -.09990 11.65600 -.12470

### 11.72500 -.20940 11.72510 -.14180 11.78000 -.11630

### 11.80800 0.00000 11.87700 .07620 11.91900 .05700

### 11.98800 .13540 12.04300 .06730 12.11300 .08650

## Release Notes

Initial release in version 14.12.

This function supersedes GetFromFile.

## See Also

SetFromFile_1

# GetRamp

## Syntax

SapObject.SapModel.Func.FuncTH.GetRamp

## VB6 Procedure

Function GetRamp(ByVal Name As String, ByRef RampTime As Double, ByRef RampAmp As
Double, ByRef RampMaxTime As Double) As Long

## Parameters

Name

The name of a ramp-type time history function.


RampTime

The time it takes for the ramp function to initially reach its maximum value. [s]

RampAmp

The maximum amplitude of the ramp function.

RampMaxTime

The time at the end of the ramp function. This time must be greater than the RampTime. [s]

**Remarks**

This function retrieves the definition of a ramp-type time history function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetTHFuncRamp()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim RampTime As Double
Dim RampAmp As Double
Dim RampMaxTime As Double

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

'add ramp TH function
ret = SapModel.Func.FuncTH.SetRamp("TH-1", 1, 1.25, 8)

'get ramp TH function
ret = SapModel.Func.FuncTH.GetRamp("TH-1", RampTime, RampAmp, RampMaxTime)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetRamp

# GetSawtooth

## Syntax

SapObject.SapModel.Func.FuncTH.GetSawtooth

## VB6 Procedure

Function GetSawtooth(ByVal Name As String, ByRef SawP As Double, ByRef SawTime As
Double, ByRef SawCycles As Long, ByRef SawAmp As Double) As Long

## Parameters

Name

The name of a sawtooth-type time history function.

SawP

The period of the sawtooth function. [s]

SawTime

The time it takes for the sawtooth function to ramp up from a function value of zero to its
maximum amplitude. [s]

SawCycles

The number of cycles in the function.

SawAmp

The maximum amplitude of the sawtooth function.

## Remarks


This function retrieves the definition of a sawtooth-type time history function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetTHFuncSawtooth()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim SawP As Double
Dim SawTime As Double
Dim SawCycles As Long
Dim SawAmp As Double

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

'add sawtooth TH function
ret = SapModel.Func.FuncTH.SetSawtooth("TH-1", 1, 0.25, 4, 1.75)

'get sawtooth TH function
ret = SapModel.Func.FuncTH.GetSawtooth("TH-1", SawP, SawTime, SawCycles, SawAmp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

**See Also**

SetSawtooth


# GetSine

## Syntax

SapObject.SapModel.Func.FuncTH.GetSine

## VB6 Procedure

Function GetSine(ByVal Name As String, ByRef SineP As Double, ByRef SineSteps As Long,
ByRef SineCycles As Long, ByRef SineAmp As Double) As Long

## Parameters

Name

The name of a sine-type time history function.

SineP

The period of the sine function. [s]

SineSteps

The number of steps in the sine function. This item can not be less than 8.

SineCycles

The number of cycles in the sine function.

SineAmp

The amplitude of the sine function.

## Remarks

This function retrieves the definition of a sine-type time history function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetTHFuncSine()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim SineP As Double
Dim SineSteps As Long
Dim SineCycles As Long


Dim SineAmp As Double

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
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'get sine TH function
ret = SapModel.Func.FuncTH.GetSine("TH-1", SineP, SineSteps, SineCycles, SineAmp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetSine

# GetTriangular

## Syntax

SapObject.SapModel.Func.FuncTH.GetTriangular

## VB6 Procedure

Function GetTriangular(ByVal Name As String, ByRef TriP As Double, ByRef TriCycles As
Long, ByRef TriAmp As Double) As Long


**Parameters**

Name

The name of a triangular-type time history function.

TriP

The period of the triangular function. [s]

TriCycles

The number of cycles in the function.

TriAmp

The maximum amplitude of the triangular function.

**Remarks**

This function retrieves the definition of a triangular-type time history function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetTHFuncTriangular()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim TriP As Double
Dim TriCycles As Long
Dim TriAmp As Double

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

'add triangular TH function


ret = SapModel.Func.FuncTH.SetTriangular("TH-1", 1, 4, 1.75)

'get triangular TH function
ret = SapModel.Func.FuncTH.GetTriangular("TH-1", TriP, TriCycles, TriAmp)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetTriangular

# GetUser

## Syntax

SapObject.SapModel.Func.FuncTH.GetUser

## VB6 Procedure

Function GetUser(ByVal Name As String, ByRef NumberItems As Long, ByRef MyTime() As
Double, ByRef Value() As Double) As Long

## Parameters

Name

The name of a user defined time history function.

NumberItems

The number of frequency and value pairs defined.

MyTime

This is an array that includes the time for each data point. [s]

Value

This is an array that includes the function value for each data point.


**Remarks**

This function retrieves the definition of a user defined time history function.

The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetTHFuncUser()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Tmp() As Double
Dim Val() As Double
Dim NumberItems As Long
Dim MyTime() As Double
Dim Value() As Double

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

'add user TH function
NumberItems = 6
ReDim Tmp(NumberItems - 1)
ReDim Val(NumberItems - 1)
Tmp(0) = 0: Val(0) = 0.1
Tmp(1) = 1: Val(1) = 0.02
Tmp(2) = 2: Val(2) = -0.06
Tmp(3) = 3: Val(3) = -0.02
Tmp(4) = 4: Val(4) = 0.05
Tmp(5) = 5: Val(5) = 0.02
ret = SapModel.Func.FuncTH.SetUser("TH-1", NumberItems, Tmp, Val)

'get user TH function
ret = SapModel.Func.FuncTH.GetUser("TH-1", NumberItems, MyTime, Value)

'close Sap2000


SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetUser

# GetUserPeriodic

## Syntax

SapObject.SapModel.Func.FuncTH.GetUserPeriodic

## VB6 Procedure

Function GetUserPeriodic(ByVal Name As String, ByRef UPCycles As Long, ByRef
NumberItems As Long, ByRef MyTime() As Double, ByRef Value() As Double) As Long

## Parameters

Name

The name of a user periodic time history function.

UPCycles

The number of cycles in the function.

NumberItems

The number of frequency and value pairs defined.

MyTime

This is an array that includes the time for each data point. [s]

Value

This is an array that includes the function value for each data point.

## Remarks

This function retrieves the definition of a user periodic time history function.


The function returns zero if the function definition is successfully retrieved; otherwise it returns a
nonzero value.

**VBA Example**

Sub GetTHFuncUserPeriodic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Num As Long
Dim Tmp() As Double
Dim Val() As Double
Dim UPCycles As Long
Dim NumberItems As Long
Dim MyTime() As Double
Dim Value() As Double

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

'add user periodic TH function
NumberItems = 6
ReDim Tmp(NumberItems - 1)
ReDim Val(NumberItems - 1)
Tmp(0) = 0: Val(0) = 0.1
Tmp(1) = 1: Val(1) = 0.02
Tmp(2) = 2: Val(2) = -0.06
Tmp(3) = 3: Val(3) = -0.02
Tmp(4) = 4: Val(4) = 0.05
Tmp(5) = 5: Val(5) = 0.02
ret = SapModel.Func.FuncTH.SetUserPeriodic("TH-1", 4, NumberItems, Tmp, Val)

'get user periodic TH function
ret = SapModel.Func.FuncTH.GetUserPeriodic("TH-1", UPCycles, NumberItems, MyTime,
Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

SetUserPeriodic

# SetCosine

## Syntax

SapObject.SapModel.Func.FuncTH.SetCosine

## VB6 Procedure

Function SetCosine(ByVal Name As String, ByVal CosineP As Double, ByVal CosineSteps As
Long, ByVal CosineCycles As Long, ByVal CosineAmp As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

CosineP

The period of the cosine function. [s]

CosineSteps

The number of steps in the cosine function. This item can not be less than 8.

CosineCycles

The number of cycles in the cosine function.

CosineAmp

The amplitude of the cosine function.

## Remarks

This function defines a cosine-type time history function.


The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetTHFuncCosine()
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

'add cosine TH function
ret = SapModel.Func.FuncTH.SetCosine("TH-1", 1, 16, 4, 1.25)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetCosine

# SetFromFile_1

## Syntax

SapObject.SapModel.Func.FuncTH.SetFromFile_1


**VB6 Procedure**

Function SetFromFile_1(ByVal Name As String, ByVal FileName As String, ByVal HeadLines
As Long, ByVal PreChars As Long, ByVal PointsPerLine As Long, ByVal ValueType As Long,
ByVal FreeFormat As Boolean, Optional ByVal NumberFixed As Long = 10, Optional ByVal DT
As Double = 0.02) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

FileName

The full path of the text file containing the function data.

HeadLines

The number of header lines in the text file to be skipped before starting to read function data.

PreChars

The number of prefix characters to be skipped on each line in the text file.

PointsPerLine

The number of function points included on each text file line.

ValueType

This is 1 or 2, indicating value type.

```
1 = Values at equal time intervals
```
```
2 = Time and function values
```
FreeFormat

This item is True if the data is provided in a free format. It is False if it is in a fixed format.

NumberFixed

This item applies only when the FreeFormat item is False. It is the number of characters per item.

DT

This item applies only when the ValueType item is 1 (equal time intervals). It is the time interval
between function points.

**Remarks**


This function defines a time history function from file.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetTHFuncFromFile_1()
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

'add TH function from file
ret = SapModel.Func.FuncTH.SetFromFile_1("TH-1", "C:\SapAPI\FuncTH.txt", 3, 0, 3, 2,
True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Text File**

Following is the contents of the text file name FuncTH.txt used in the VBA Example.

Time History Function

Time (sec) and Acceleration (g) values

3 points per line

0.00000 .01080 .04200 .00100 .09700 .01590
.16100 -.00010 .22100 .01890 .26300 .00010
.29100 .00590 .33200 -.00120 .37400 .02000
.42900 -.02370 .47100 .00760 .58100 .04250


### .62300 .00940 .66500 .01380 .72000 -.00880

### .72010 -.02560 .78900 -.03870 .78910 -.05680

### .87200 -.02320 .87210 -.03430 .94100 -.04020

### .94110 -.06030 .99700 -.07890 1.06600 -.06660

### 1.06610 -.03810 1.09400 -.04290 1.16800 .08970

### 1.31500 -.16960 1.38400 -.08280 1.41200 -.08280

### 1.44000 -.09450 1.48100 -.08850 1.50900 -.10800

### 1.53700 -.12800 1.62800 .11440 1.70300 .23550

### 1.80000 .14280 1.85500 .17770 1.92400 -.26100

### 2.00700 -.31940 2.21500 .29520 2.27000 .26340

### 2.32000 -.29840 2.39500 .00540 2.45000 .28650

### 2.51900 -.04690 2.57500 .15160 2.65200 .20770

### 2.70800 .10870 2.76900 -.03250 2.89300 .10330

### 2.97600 -.08030 3.06800 .05200 3.12900 -.15470

### 3.21200 .00650 3.25300 -.20600 3.38600 .19270

### 3.41900 -.09370 3.53000 .17080 3.59900 -.03590

### 3.66800 .03650 3.73800 -.07360 3.83500 .03110

### 3.90400 -.18330 4.01400 .02270 4.05600 -.04350

### 4.10600 .02160 4.22200 -.19720 4.31400 -.17620

### 4.41600 .14600 4.47100 -.00470 4.61800 .25720

### 4.66500 -.20450 4.75600 .06080 4.83100 -.27330

### 4.97000 .17790 5.03900 .03010 5.10800 .21830

### 5.19900 .02670 5.23300 .12520 5.30200 .12900

### 5.33000 .10890 5.34300 -.02390 5.45400 .17230

### 5.51000 -.10210 5.60600 .01410 5.69000 -.19490

### 5.77300 -.02420 5.80000 -.00500 5.80900 -.02750

### 5.86900 -.05730 5.88300 -.03270 5.92500 .02160

### 5.98000 .01080 6.01300 .02350 6.08500 -.06650

### 6.13200 .00140 6.17400 .04930 6.18800 .01490

### 6.18810 -.02000 6.22900 -.03810 6.27900 .02070

### 6.32600 -.00580 6.36800 -.06030 6.38200 -.01620

### 6.40900 .02000 6.45900 -.01760 6.47800 -.00330

### 6.52000 .00430 6.53400 -.00400 6.56200 -.00990

### 6.57500 -.00170 6.60300 -.01700 6.64500 .03730

### 6.68600 .04570 6.71400 .03850 6.72800 .00090

### 6.76900 -.02880 6.76910 .00160 6.81100 .01130

### 6.85200 .00220 6.90800 .00920 6.99100 -.09960

### 7.07400 .03600 7.12100 .00780 7.14300 -.02770

### 7.14900 .00260 7.17100 .02720 7.22600 .05760

### 7.29500 -.04920 7.37000 .02970 7.40600 .01090

### 7.42500 .01860 7.46100 -.02530 7.52500 -.03470

### 7.57200 .00360 7.60000 -.06280 7.64100 -.02800

### 7.66900 -.01960 7.69100 .00680 7.75200 -.00540

### 7.79400 -.06030 7.83500 -.03570 7.87700 -.07160

### 7.96000 -.01400 7.98700 -.00560 8.00100 .02220

### 8.07000 .04680 8.12600 .02600 8.12610 -.03350

### 8.19500 -.01280 8.22300 .06610 8.27800 .03050

### 8.33400 .02460 8.40300 .03470 8.45800 -.03690

### 8.53300 -.03440 8.59600 -.01040 8.63800 -.02600

### 8.73500 .15340 8.81800 -.00280 8.86000 .02330

### 8.88200 -.02610 8.91500 -.00220 8.95600 -.18490

### 9.05300 .12600 9.09500 .03200 9.12300 .09550

### 9.15000 .12460 9.25300 -.03280 9.28900 -.04510


### 9.42700 .13010 9.44100 -.16570 9.51000 .04190

### 9.63500 -.09360 9.70400 .08160 9.81500 -.08810

### 9.89800 .00640 9.93900 -.00060 9.99500 .05860

### 10.02200 -.07130 10.05000 -.04480 10.05010 -.02210

### 10.10500 .00930 10.10510 .00240 10.18800 .05100

### 10.27200 -.12430 10.38200 .05870 10.42400 .01330

### 10.45200 .03860 10.46500 .11640 10.50700 -.03740

### 10.53400 -.05720 10.64500 .03080 10.70100 .02230

### 10.71400 .05150 10.77000 .09030 10.83900 -.01940

### 10.92200 .04710 10.92210 -.06770 10.96400 -.07940

### 10.99100 -.01200 11.07400 .06080 11.08800 -.02690

### 11.11600 -.04160 11.20700 .02930 11.20710 .05520

### 11.22700 .07560 11.26800 .04310 11.32400 .02080

### 11.43400 .11800 11.57300 -.09990 11.65600 -.12470

### 11.72500 -.20940 11.72510 -.14180 11.78000 -.11630

### 11.80800 0.00000 11.87700 .07620 11.91900 .05700

### 11.98800 .13540 12.04300 .06730 12.11300 .08650

## Release Notes

Initial release in version 14.12.

This function supersedes SetFromFile.

## See Also

GetFromFile_1

# SetRamp

## Syntax

SapObject.SapModel.Func.FuncTH.SetRamp

## VB6 Procedure

Function SetRamp(ByVal Name As String, ByVal RampTime As Double, ByVal RampAmp As
Double, ByVal RampMaxTime As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

RampTime

The time it takes for the ramp function to initially reach its maximum value. [s]


RampAmp

The maximum amplitude of the ramp function.

RampMaxTime

The time at the end of the ramp function. This time must be greater than the RampTime. [s]

**Remarks**

This function defines a ramp-type time history function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetTHFuncRamp()
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

'add ramp TH function
ret = SapModel.Func.FuncTH.SetRamp("TH-1", 1, 1.25, 8)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.


## See Also

GetRamp

# SetSawtooth

## Syntax

SapObject.SapModel.Func.FuncTH.SetSawtooth

## VB6 Procedure

Function SetSawtooth(ByVal Name As String, ByVal SawP As Double, ByVal SawTime As
Double, ByVal SawCycles As Long, ByVal SawAmp As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

SawP

The period of the sawtooth function. [s]

SawTime

The time it takes for the sawtooth function to ramp up from a function value of zero to its
maximum amplitude. [s]

SawCycles

The number of cycles in the function.

SawAmp

The maximum amplitude of the sawtooth function.

## Remarks

This function defines a sawtooth-type time history function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

## VBA Example


Sub SetTHFuncSawtooth()
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

'add sawtooth TH function
ret = SapModel.Func.FuncTH.SetSawtooth("TH-1", 1, 0.25, 4, 1.75)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetSawtooth

# SetSine

## Syntax

SapObject.SapModel.Func.FuncTH.SetSine

## VB6 Procedure

Function SetSine(ByVal Name As String, ByVal SineP As Double, ByVal SineSteps As Long,
ByVal SineCycles As Long, ByVal SineAmp As Double) As Long


**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

SineP

The period of the sine function. [s]

SineSteps

The number of steps in the sine function. This item can not be less than 8.

SineCycles

The number of cycles in the sine function.

SineAmp

The amplitude of the sine function.

**Remarks**

This function defines a sine-type time history function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetTHFuncSine()
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


'add sine TH function
ret = SapModel.Func.FuncTH.SetSine("TH-1", 1, 16, 4, 1.25)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetSine

# SetTriangular

## Syntax

SapObject.SapModel.Func.FuncTH.SetTriangular

## VB6 Procedure

Function SetTriangular(ByVal Name As String, ByVal TriP As Double, ByVal TriCycles As
Long, ByVal TriAmp As Double) As Long

## Parameters

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

TriP

The period of the triangular function. [s]

TriCycles

The number of cycles in the function.

TriAmp

The maximum amplitude of the triangular function.


## Remarks

This function defines a triangular-type time history function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

## VBA Example

Sub SetTHFuncTriangular()
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

'add triangular TH function
ret = SapModel.Func.FuncTH.SetTriangular("TH-1", 1, 4, 1.75)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetTriangular

# SetUser


**Syntax**

SapObject.SapModel.Func.FuncTH.SetUser

**VB6 Procedure**

Function SetUser(ByVal Name As String, ByVal NumberItems As Long, ByRef MyTime() As
Double, ByRef Value() As Double) As Long

**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

NumberItems

The number of time and value pairs defined.

MyTime

This is an array that includes the time for each data point. [s]

Value

This is an array that includes the function value for each data point.

**Remarks**

This function defines a user time history function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetTHFuncUser()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim MyTime() As Double
Dim Value() As Double

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

'add user TH function
NumberItems = 6
ReDim MyTime(NumberItems - 1)
ReDim Value(NumberItems - 1)
MyTime(0) = 0: Value(0) = 0.1
MyTime(1) = 1: Value(1) = 0.02
MyTime(2) = 2: Value(2) = -0.06
MyTime(3) = 3: Value(3) = -0.02
MyTime(4) = 4: Value(4) = 0.05
MyTime(5) = 5: Value(5) = 0.02
ret = SapModel.Func.FuncTH.SetUser("TH-1", NumberItems, MyTime, Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.02.

## See Also

GetUser

# SetUserPeriodic

## Syntax

SapObject.SapModel.Func.FuncTH.SetUserPeriodic

## VB6 Procedure

Function SetUserPeriodic(ByVal Name As String, ByVal UPCycles As Long, ByVal
NumberItems As Long, ByRef MyTime() As Double, ByRef Value() As Double) As Long


**Parameters**

Name

The name of an existing or new function. If this is an existing function, that function is modified;
otherwise, a new function is added.

UPCycles

The number of cycles in the function.

NumberItems

The number of time and value pairs defined.

MyTime

This is an array that includes the time for each data point. [s]

Value

This is an array that includes the function value for each data point.

**Remarks**

This function defines a user periodic time history function.

The function returns zero if the function is successfully defined; otherwise it returns a nonzero
value.

**VBA Example**

Sub SetTHFuncUserPeriodic()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim MyTime() As Double
Dim Value() As Double

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

'add user periodic TH function
NumberItems = 6
ReDim MyTime(NumberItems - 1)
ReDim Value(NumberItems - 1)
MyTime(0) = 0: Value(0) = 0.1
MyTime(1) = 1: Value(1) = 0.02
MyTime(2) = 2: Value(2) = -0.06
MyTime(3) = 3: Value(3) = -0.02
MyTime(4) = 4: Value(4) = 0.05
MyTime(5) = 5: Value(5) = 0.02
ret = SapModel.Func.FuncTH.SetUserPeriodic("TH-1", 4, NumberItems, MyTime, Value)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

**Release Notes**

Initial release in version 11.02.

**See Also**

GetUserPeriodic


