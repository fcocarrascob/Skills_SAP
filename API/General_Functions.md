# CreateObject

## Syntax

Helper.CreateObject

## VB6 Procedure

Function CreateObject(ByVal fullPath As String) As cOAPI

## Parameters

fullPath

The full path to SAP2000.exe.

## Remarks

Starts SAP2000 at the given path and returns an instance of SapObject if successful, nothing
otherwise.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI

Dim ret As Long

'create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObject("C:\Program Files\Computers and Structures\SAP
22\SAP2000.exe")

'start SAP2000 application

ret = SapObject.ApplicationStart()


'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 17.

## See Also

SapObject.ApplicationStart

# CreateObjectHost

## Syntax

Helper.CreateObjectHost

## VB6 Procedure

Function CreateObjectHost(ByVal hostName As String, ByVal fullPath As String) As cOAPI

## Parameters

hostname


The host computer name.

fullPath

The full path to SAP2000.exe.

## Remarks

Starts SAP2000 at the given path on a given computer using the default TCP port and returns an
instance of SapObject if successful, nothing otherwise.

CSiAPIService.exe must be running on the host computer and listening to the default TCP port for
the call to succeed.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObjectHost("RemoteServer", "C:\Program Files\Computers and
Structures\SAP2000 22\SAP2000.exe")

‘start SAP2000 application

ret = SapObject.ApplicationStart()

'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()


'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 22.

## See Also

SapObject.ApplicationStart

RemoteAPI

# CreateObjectHostPort

## Syntax

Helper.CreateObjectHostPort

## VB6 Procedure

Function CreateObjectHostPort(ByVal hostName As String, ByVal portNumber As Integer,
ByVal fullPath As String) As cOAPI

## Parameters

hostname

The host computer name.

portNumber

The TCP port to connect to the host computer.

fullPath

The full path to SAP2000.exe.


## Remarks

Starts SAP2000 at the given path on a given computer using the given TCP port and returns an
instance of SapObject if successful, nothing otherwise.

CSiAPIService.exe must be running on the host computer and listening to the given TCP port for
the call to succeed.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObjectHostPort("RemoteServer", 8500, "C:\Program
Files\Computers and Structures\SAP2000 22\SAP2000.exe")

‘start SAP2000 application

ret = SapObject.ApplicationStart()

'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)


'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 22.

## See Also

SapObject.ApplicationStart

RemoteAPI

# CreateObjectProgID

## Syntax

Helper.CreateObjectProgID

## VB6 Procedure

Function CreateObjectProgID(ByVal progID As String) As cOAPI

## Parameters

progID

The program ID of the API object. Use “CSI.SAP2000.API.SapObject” for SAP2000 and
“CSI.CSiBridge.API.SapObject” for CSiBridge.

## Remarks

Starts SAP2000 and returns an instance of SapObject if successful, nothing otherwise.

The function searches the registry for the newest installed version of SAP2000 unless overridden
with an environment variable containing the full path to SAP2000.exe. The overriding
environment variable is "CSI_SAP2000_API_SapObject_PATH" for SAP2000 and
"CSI_CSiBridge_API_SapObject_PATH" for CSiBridge.

## VBA Example


Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObjectProgID("CSI.SAP2000.API.SapObject")

‘start SAP2000 application

ret = SapObject.ApplicationStart()

'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub


## Release Notes

Initial release in version 19.

## See Also

SapObject.ApplicationStart

# CreateObjectProgIDHost

## Syntax

Helper.CreateObjectProgIDHost

## VB6 Procedure

Function CreateObjectProgIDHost(ByVal hostName As String, ByVal progID As String) As
cOAPI

## Parameters

hostname

The host computer name.

progID

The program ID of the API object. Use “CSI.SAP2000.API.SapObject” for SAP2000 and
“CSI.CSiBridge.API.SapObject” for CSiBridge.

## Remarks

Starts SAP2000 on a given computer using the default TCP port and returns an instance of
SapObject if successful, nothing otherwise.

CSiAPIService.exe must be running on the host computer and listening to the default TCP port for
the call to succeed.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel


Dim SapObject As cOAPI

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObjectProgIDHost("RemoteServer",
"CSI.SAP2000.API.SapObject")

‘start SAP2000 application

ret = SapObject.ApplicationStart()

'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 22.


## See Also

SapObject.ApplicationStart

RemoteAPI

# CreateObjectProgIDHostPort

## Syntax

Helper.CreateObjectProgIDHostPort

## VB6 Procedure

Function CreateObjectProgIDHostPort(ByVal hostName As String, ByVal portNumber As
Integer, ByVal progID As String) As cOAPI

## Parameters

hostname

The host computer name.

portNumber

The TCP port to connect to the host computer.

progID

The program ID of the API object. Use “CSI.SAP2000.API.SapObject” for SAP2000 and
“CSI.CSiBridge.API.SapObject” for CSiBridge.

## Remarks

Starts SAP2000 on a given computer using the given TCP port and returns an instance of
SapObject if successful, nothing otherwise.

CSiAPIService.exe must be running on the host computer and listening to the given TCP port for
the call to succeed.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI


Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObjectProgIDHostPort("RemoteServer", 8500,
"CSI.SAP2000.API.SapObject")

‘start SAP2000 application

ret = SapObject.ApplicationStart()

'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 22.

## See Also

SapObject.ApplicationStart


RemoteAPI

# GetObject

## Syntax

Helper.GetObject

## VB6 Procedure

Function GetObject(ByVal typeName As String) As cOAPI

## Parameters

typeName

The program ID of the API object. Use “CSI.SAP2000.API.SapObject” for SAP2000 and
“CSI.CSiBridge.API.SapObject” for CSiBridge.

## Remarks

Attaches to the active running instance of SAP2000 and returns an instance of SapObject if
successful, nothing otherwise.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.GetObject("CSI.SAP2000.API.SapObject")

'create SapModel object

Set SapModel = SapObject.SapModel


'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 17.

## See Also

SapObject.AplicationExit

SetAsActiveObject

UnsetAsActiveObject

# GetObjectHost

## Syntax

Helper.GetObjectHost

## VB6 Procedure

Function GetObjectHost(ByVal hostName As String, ByVal progID As String) As cOAPI

## Parameters

hostName


The host computer name.

progID

The program ID of the API object. Use “CSI.SAP2000.API.SapObject” for SAP2000 and
“CSI.CSiBridge.API.SapObject” for CSiBridge.

## Remarks

Attaches to the active running instance of SAP2000 on a given computer using the default TCP
port and returns an instance of SapObject if successful, nothing otherwise.

CSiAPIService.exe must be running on the host computer and listening to the default TCP port for
the call to succeed.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.GetObjectHost("RemoteServer", "CSI.SAP2000.API.SapObject")

'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)


'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 22.

## See Also

SapObject.AplicationExit

RemoteAPI

# GetObjectHostPort

## Syntax

Helper.GetObjectHostPort

## VB6 Procedure

Function GetObjectHostPort(ByVal hostName As String, ByVal portNumber As Integer, ByVal
progID As String) As cOAPI

## Parameters

hostName

The host computer name.

portNumber

The TCP port to connect to the host computer.

progID

The program ID of the API object. Use “CSI.SAP2000.API.SapObject” for SAP2000 and
“CSI.CSiBridge.API.SapObject” for CSiBridge.

## Remarks


Attaches to the active running instance of SAP2000 on a given computer using the given TCP
port. Returns an instance of SapObject if successful, nothing otherwise.

CSiAPIService.exe must be running on the host computer and listening to the given TCP port for
the call to succeed.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.GetObjectHostPort("RemoteServer", 8500,
"CSI.SAP2000.API.SapObject")

'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing


End Sub

## Release Notes

Initial release in version 22.

## See Also

SapObject.AplicationExit

RemoteAPI

# GetObjectProcess

## Syntax

Helper.GetObjectProcess

## VB6 Procedure

Function GetObjectProcess(ByVal typeName As String, ByVal pid As Integer) As cOAPI

## Parameters

typeName

The program ID of the API object. Use “CSI.SAP2000.API.SapObject” for SAP2000 and
“CSI.CSiBridge.API.SapObject” for CSiBridge.

pid

The system-generated unique identifier (process ID) of the desired instance of the program as
shown in Windows Task Manager and/or under “Tools” menu.

## Remarks

Attaches to the running instance of the program with the given process ID and returns an instance
of SapObject if successful, nothing otherwise.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapModel As cSapModel

Dim SapObject As cOAPI


Dim pid As Integer

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

pid = 15476 'set to process ID of the instance to attach to

Set SapObject = myHelper.GetObjectProcess("CSI.SAP2000.API.SapObject", pid)

'create SapModel object

Set SapModel = SapObject.SapModel

'initialize model

ret = SapModel.InitializeNewModel()

'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapModel = Nothing

Set SapObject = Nothing

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 24.1.

## See Also

GetObject

SetAsActiveObject


UnsetAsActiveObject

# GetOAPIVersionNumber

## Syntax

Helper.GetOAPIVersionNumber

## VB6 Procedure

Function GetOAPIVersionNumber() As Double

## Parameters

None

## Remarks

Retrieves the API version. The returned API version can be compared to
SapObject.GetOAPIVersionNumber to determine API compatibility with the started/attached
instance of SAP2000.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapObject As cOAPI

Dim clientAPIVersion As Double

Dim programAPIVersion As Double

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObjectProgID("CSI.SAP2000.API.SapObject")

'start SAP2000 application


ret = SapObject.ApplicationStart()

'get client API version

clientAPIVersion = myHelper.GetOAPIVersionNumber()

'get program API version

programAPIVersion = SapObject.GetOAPIVersionNumber()

‘API compatibility check

If clientAPIVersion > programAPIVersion Then

'API client uses a newer version of the API than SAP2000.

'All API functionality may be not be available.

Exit Sub

End If

'close SAP

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapObject = Nothingx

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 21.

## See Also

SapObject.GetOAPIVersionNumber


# ApplicationExit

## Syntax

SapObject.ApplicationExit

## VB6 Procedure

Function ApplicationExit(ByVal FileSave As Boolean) As Long

## Parameters

FileSave

```
If this item is True the existing model file is saved prior to closing Sap2000.
```
## Remarks

If the model file is saved then it is saved with its current name. You should set the Sap2000 object
variable to nothing after calling this function.

This function returns zero if the function succeeds and nonzero if it fails.

## VBA Example

```
Sub ExitExample()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
```
```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
SapObject.ApplicationStart
```
```
'create SapModel object
Set SapModel = SapObject.SapModel
```
```
'initialize model
ret = SapModel.InitializeNewModel(kip_ft_F)
```
```
'create a 3D frame model from template
ret = SapModel.File.New3DFrame(BeamSlab, 3, 12, 3, 28, 2, 36)
```
```
'close Sap2000
```

```
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub
```
## Release Notes

Initial release in version 11.00.

## See Also

ApplicationStart

# ApplicationStart

## Syntax

SapObject.ApplicationStart

## VB6 Procedure

```
Function ApplicationStart(Optional ByVal Units As eUnits = kip_in_F, Optional
ByVal Visible As Boolean = True, Optional ByVal FileName As String = "") As
Long
```
## Parameters

Units

```
The database units used when a new model is created. Data is internally stored in the
program in the database units. The database units may be one of the following items in the
eUnits enumeration:
lb_in_F = 1
lb_ft_F = 2
kip_in_F = 3
kip_ft_F = 4
kN_mm_C = 5
kN_m_C = 6
kgf_mm_C = 7
kgf_m_C = 8
N_mm_C = 9
N_m_C = 10
Ton_mm_C = 11
Ton_m_C = 12
kN_cm_C = 13
kgf_cm_C = 14
N_cm_C = 15
Ton_cm_C = 16
```

Visible

```
If this item is True then the application is visible when started. If it is False then the
application is hidden when started.
```
FileName

```
The full path of a model file to be opened when the Sap2000 application is started. If no
file name is specified, the application starts without loading an existing model.
```
## Remarks

This function starts the Sap2000 application.

When the model is not visible it does not appear on screen and it does not appear in the Windows
task bar.

If no filename is specified, you can later open a model or create a model through the API.

The file name must have an .sdb, .$2k, .s2k, .xls, or .mdb extension. Files with .sdb extensions are
opened as standard SAP2000 files. Files with .$2k and .s2k extensions are imported as text files.
Files with .xls extensions are imported as Microsoft Excel files. Files with .mdb extensions are
imported as Microsoft Access files.

This function returns zero if the application successfully starts and nonzero if it fails.

## VBA Example

```
Sub StartExample()
'dimension variables
Dim SapObject as cOAPI
```
```
Dim ret as Long
```
```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
ret = SapObject.ApplicationStart
```
```
'close Sap2000
SapObject.ApplicationExit False
Set SapObject = Nothing
End Sub
```
## Release Notes

Initial release in version 11.00.


## See Also

ApplicationExit

OpenFile

InitializeNewModel

# GetOAPIVersionNumber

## Syntax

SapObject.GetOAPIVersionNumber

## VB6 Procedure

Function GetOAPIVersionNumber() As Double

## Parameters

None

## Remarks

Retrieves the API version implemented by SAP2000. The returned API version can be
compared to Helper.GetOAPIVersionNumber to determine API compatibility with the
started/attached instance of SAP2000.

## VBA Example

Public Sub Example()

Dim myHelper As cHelper

Dim SapObject As cOAPI

Dim clientAPIVersion As Double

Dim programAPIVersion As Double

Dim ret As Integer

‘create SapObject

Set myHelper = New Helper

Set SapObject = myHelper.CreateObjectProgID("CSI.SAP2000.API.SapObject")


'start SAP2000 application

ret = SapObject.ApplicationStart()

'get client API version

clientAPIVersion = myHelper.GetOAPIVersionNumber()

'get program API version

programAPIVersion = SapObject.GetOAPIVersionNumber()

‘API compatibility check

If clientAPIVersion > programAPIVersion Then

'API client uses a newer version of the API than SAP2000.

'All API functionality may be not be available.

Exit Sub

End If

'close SAP2000

ret = SapObject.ApplicationExit(False)

'clean up variables

Set SapObject = Nothingx

Set myHelper = Nothing

End Sub

## Release Notes

Initial release in version 17.00


## See Also

Helper.GetOAPIVersionNumber

# Hide

## Syntax

SapObject.Hide

## VB6 Procedure

Function Hide() As Long

## Parameters

None

## Remarks

This function hides the Sap2000 application. When the application is hidden it is not visible on the
screen or on the Windows task bar.

The function returns zero if the Sap2000 application is successfully hidden and nonzero if the
function fails. If the application is already hidden calling this function returns an error.

## VBA Example

Sub HideSap()
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

'create model from template
ret = SapModel.File.New2DFrame(ConcentricBraced, 3, 124, 3, 200)

'hide application
ret = SapObject.Hide


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

Visible

Unhide

# Unhide

## Syntax

SapObject.Unhide

## VB6 Procedure

Function Unhide() As Long

## Parameters

None

## Remarks

This function unhides the Sap2000 application, that is, it makes it visible. When the application is
hidden, it is not visible on the screen or on the Windows task bar.

The function returns zero if the Sap2000 application is successfully unhidden (set visible) and
nonzero if the function fails. If the application is already visible (not hidden) calling this function
returns an error.

## VBA Example

Sub UnhideSap()
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

'create model from template
ret = SapModel.File.New2DFrame(ConcentricBraced, 3, 124, 3, 200)

'hide application
ret = SapObject.Hide

'unhide application
ret = SapObject.Unhide

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

Visible

Hide

# Visible

## Syntax

SapObject.Visible

## VB6 Procedure

Function Visible() As Boolean

## Parameters

None


## Remarks

The function returns True if the Sap2000 application is visible on the screen, otherwise it returns
False.

## VBA Example

Sub IsVisible()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as long
Dim Visible as Boolean

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'create model from template
ret = SapModel.File.New2DFrame(ConcentricBraced, 3, 124, 3, 200)

'get application visibility
Visible = SapObject.Visible

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

Hide

Unhide


# SetAsActiveObject

## Syntax

SapObject.SetAsActiveObject

## VB6 Procedure

Function SetAsActiveObject () As Long

## Parameters

```
None
```
## Remarks

This function sets the active instance of a SapObject in the system Running Object Table (ROT),
replacing the previous instance(s).

When a new SapObject is created using the API, it is automatically added to the system ROT if
none is already present. Subsequent instances of the SapObject do not alter the ROT as long as at
least one active instance of a SapObject is present in the ROT.

The Windows API call GetObject() can be used to attach to the active SapObject instance
registered in the ROT.

This function returns zero if the current instance is successfully added to the system ROT and
nonzero if it fails.

## VBA Example

```
Sub StartExample()
'dimension variables
Dim SapObject as cOAPI
Dim ret as Long
```
```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
ret = SapObject.ApplicationStart
```
```
'set as active SapObject instance
ret = SapObject.SetAsActiveObject
```

```
'close Sap2000
SapObject.ApplicationExit False
Set SapObject = Nothing
End Sub
```
## Release Notes

Initial release in version 15.01.

## See Also

UnsetAsActiveObject

# UnsetAsActiveObject

## Syntax

SapObject.UnsetAsActiveObject

## VB6 Procedure

Function UnsetAsActiveObject () As Long

## Parameters

```
None
```
## Remarks

This function removes the current instance of a SapObject from the system Running Object Table
(ROT).

This function returns zero if the current instance is successfully removed from the system ROT
and nonzero if it fails or if the current instance is not in the system ROT.

## VBA Example

```
Sub StartExample()
'dimension variables
Dim SapObject as cOAPI
Dim ret as Long
```
```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```

```
'start Sap2000 application
ret = SapObject.ApplicationStart
```
```
'unset as active SapObject instance
ret = SapObject.UnsetAsActiveObject
```
```
'close Sap2000
SapObject.ApplicationExit False
Set SapObject = Nothing
End Sub
```
## Release Notes

Initial release in version 15.01.

## See Also

SetAsActiveObject

# GetDatabaseUnits

## Syntax

SapObject.SapModel.GetDatabaseUnits

## VB6 Procedure

Function GetDatabasetUnits() As eUnits

## Parameters

None

## Remarks

This function returns one of the following items from the eUnits enumeration indicating the
database units for the model. All data is internally stored in the model in these units and converted
to the present units as needed.

```
lb_in_F = 1
lb_ft_F = 2
kip_in_F = 3
kip_ft_F = 4
kN_mm_C = 5
kN_m_C = 6
kgf_mm_C = 7
kgf_m_C = 8
```

```
N_mm_C = 9
N_m_C = 10
Ton_mm_C = 11
Ton_m_C = 12
kN_cm_C = 13
kgf_cm_C = 14
N_cm_C = 15
Ton_cm_C = 16
```
## VBA Example

Sub GetUnitsDatabase()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyUnits As eUnits

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

'get database units
MyUnits = SapModel.GetDatabaseUnits

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetPresentUnits

GetPresentUnits


# GetMergeTol

## Syntax

SapObject.SapModel.GetMergeTol

## VB6 Procedure

Function GetMergeTol(ByRef MergeTol As Double) As Long

## Parameters

MergeTol

The program auto merge tolerance. [L]

## Remarks

This function retrieves the value of the program auto merge tolerance.

The function returns zero if the tolerance is successfully retrieved; otherwise it returns a nonzero
value.

## VBA Example

Sub GetAutoMergeTolerance()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MergeTol As Double

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

'get auto merge tolerance
ret = SapModel.GetMergeTol(MergeTol)


'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

SetMergeTol

# GetModelFilename

## Syntax

SapObject.SapModel.GetModelFilename

## VB6 Procedure

Function GetModelFilename(Optional ByVal IncludePath As Boolean = True) As String

## Parameters

IncludePath

A boolean (True or False) value. When this item is True, the returned filename includes the full
path where the file is located.

## Remarks

The function returns a string that represents the filename of the current model, with or without the
full path.

## VBA Example

Sub GetModelFilename()
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

'start a new template model
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'save the model
ret = SapModel.File.Save("C:\SapAPI\API_1-001.sdb")

'display the filename of the model
MsgBox “Model filename = “ & SapModel.GetModelFilename

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.2.2

## See Also

GetModelFilepath

# GetModelFilepath

## Syntax

SapObject.SapModel.GetModelFilepath

## VB6 Procedure

Function GetModelFilepath() As String

## Parameters

None


## Remarks

The function returns a string that represents the filepath of the current model.

## VBA Example

Sub GetModelFilepath()
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

'start a new template model
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'save the model
ret = SapModel.File.Save("C:\SapAPI\API_1-001.sdb")

'display the path where the model is saved
MsgBox “Model filepath = “ & SapModel.GetModelFilepath

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 14.2.2

## See Also

GetModelFilename

# GetModelIsLocked


## Syntax

SapObject.SapModel.GetModelIsLocked

## VB6 Procedure

Function GetModelIsLocked() As Boolean

## Parameters

None

## Remarks

The function returns True if the model is locked and False if it is unlocked.

With some exceptions, definitions and assignments can not be changed in a model while the
model is locked. If an attempt is made to change a definition or assignment while the model is
locked and that change is not allowed in a locked model, an error will be returned.

## VBA Example

Sub GetModelLocked()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim IsLocked As Boolean

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

'check if model is locked
IsLocked = SapModel.GetModelIsLocked

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetModelIsLocked

# GetNotionalSize

## Syntax

SapObject.SapModel.PropArea.GetNotionalSize

## VB6 Procedure

Function GetNotionalSize(ByVal Name As String, ByRef stype As String, ByRef Value As
Double) As Long

## Parameters

Name

The name of an existing shell-type area section property.

stype

The type to define the notional size of a section. It can be:

```
"Auto" = Program will determine the notional size based on the average thickness of
an area element.
```
```
"User" = The notional size is based on the user-defined value.
```
```
"None" = Notional size will not be considered. In other words, the time-dependent
effect of this section will not be considered.
```
Value

For **stype** is "Auto", the Value represents for the scale factor to the program-determined notional
size; for **stype** is “User”, the **Value** represents for the user-defined notional size [L]; for **stype** is
“None”, the **Value** will not be used and can be set to 1.

## Remarks


This function retrieves the method to determine the notional size of an area section for the creep
and shrinkage calculations. This function is currently worked for shell type area section.

The function returns zero if the parameters are successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetAreaPropNotionalSize()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim i As Long

```
Dim stype As String
```
```
Dim Value As Double
```
```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
SapObject.ApplicationStart
```
```
'create SapModel object
Set SapModel = SapObject.SapModel
```
```
'initialize model
ret = SapModel.InitializeNewModel
```
```
'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)
```
```
'assign parameters
stype = “Auto”
Value = 1.1
ret = SapModel.PropArea.SetNotionalSize("ASEC1", “Auto”, 1.1)
```
```
'get parameters
ret = SapModel.PropArea.GetNotionalSize("ASEC1", stype, Value)
```
```
'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
```
End Sub


## Release Notes

Initial release in version 16.1.0

## See Also

SetNotionalSize

# GetPresentCoordSystem

## Syntax

SapObject.SapModel.GetPresentCoordSystem

## VB6 Procedure

Function GetPresentCoordSystem() As String

## Parameters

None

## Remarks

This function returns the name of the present coordinate system.

## VBA Example

Sub GetPresentCSys()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as long
Dim PresentCSys as String

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

'define new coordinate system
ret = SapModel.CoordSys.SetCoordSys("CSys1", 1000, 1000, 0, 0, 0, 0)

'set present coordinate system
ret = SapModel.SetPresentCoordSystem("CSys1")

'get present coordinate system
PresentCSys = SapModel.GetPresentCoordSystem

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetPresentCoordSystem

# GetPresentUnits

## Syntax

SapObject.SapModel.GetPresentUnits

## VB6 Procedure

Function GetPresentUnits() As eUnits

## Parameters

None

## Remarks

This function returns one of the following items from the eUnits enumeration indicating the units
presently specified for the model:

```
lb_in_F = 1
lb_ft_F = 2
kip_in_F = 3
```

```
kip_ft_F = 4
kN_mm_C = 5
kN_m_C = 6
kgf_mm_C = 7
kgf_m_C = 8
N_mm_C = 9
N_m_C = 10
Ton_mm_C = 11
Ton_m_C = 12
kN_cm_C = 13
kgf_cm_C = 14
N_cm_C = 15
Ton_cm_C = 16
```
## VBA Example

Sub GetUnitsPresent()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim MyUnits As eUnits

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

'get present units
MyUnits = SapModel.GetPresentUnits

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

SetPresentUnits

GetDatabaseUnits

# GetProjectInfo

## Syntax

SapObject.SapModel.GetProjectInfo

## VB6 Procedure

Function GetProjectInfo(ByRef NumberItems As Long, ByRef Item() As String, ByRef Data() As
String) As Long

## Parameters

NumberItems

The number of project info items returned.

Item

This is an array that includes the name of the project information item.

Data

This is an array that includes the data for the specified project information item.

## Remarks

This function retrieves the project information data.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetProjectInformationData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim NumberItems As Long
Dim Item() As String
Dim Data() As String


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

'set project information data
ret = SapModel.SetProjectInfo("Company Name", "Computers and Structures, Inc.")
ret = SapModel.SetProjectInfo("Project Name", "API Testing")
ret = SapModel.SetProjectInfo("My Item", "My Data")

'get project information data
ret = SapModel.GetProjectInfo(NumberItems, Item, Data)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

SetProjectInfo

# GetUserComment

## Syntax

SapObject.SapModel.GetUserComment

## VB6 Procedure

Function GetUserComment(ByRef Comment As String) As Long


## Parameters

Comment

The data in the user comments and log.

## Remarks

This function retrieves the data in the user comments and log.

The function returns zero if the data is successfully retrieved; otherwise it returns a nonzero value.

## VBA Example

Sub GetComments()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Comment As String

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

'add comments
ret = SapModel.SetUserComment("Testing the Sap2000 API.")
ret = SapModel.SetUserComment("Adding a second comment.")
ret = SapModel.SetUserComment("Adding a third comment.", 3)

'get comments
ret = SapModel.GetUserComment(Comment)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.03.

## See Also

SetUserComment

# GetVersion

## Syntax

SapObject.SapModel.GetVersion

## VB6 Procedure

Function GetVersion(ByRef Version As String, ByRef MyVersionNumber As Double) As Long

## Parameters

Version

The program version name that is externally displayed to the user.

MyVersionNumber

The program version number that is used internally by the program and not displayed to the user.

## Remarks

This function returns the SAP2000 program version.

The function returns zero if the information is successfully retrieved; otherwise it returns a
nonzero value.

## VBA Example

Sub GetProgramVersion()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim Version As String
Dim MyVersionNumber As Double
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")


'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'get program version
ret = SapModel.GetVersion(Version,MyVersionNumber)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 12.01.

## See Also

# InitializeNewModel

## Syntax

SapObject.SapModel.InitializeNewModel

## VB6 Procedure

Function InitializeNewModel(Optional ByVal Units As eUnits = kip_in_F) As Long

## Parameters

Units

This is the database units for the new model. All data is internally stored in the model in these
units. The units are one of the following items in the eUnits enumeration:

```
lb_in_F = 1
lb_ft_F = 2
kip_in_F = 3
kip_ft_F = 4
kN_mm_C = 5
kN_m_C = 6
kgf_mm_C = 7
kgf_m_C = 8
N_mm_C = 9
```

```
N_m_C = 10
Ton_mm_C = 11
Ton_m_C = 12
kN_cm_C = 13
kgf_cm_C = 14
N_cm_C = 15
Ton_cm_C = 16
```
## Remarks

This function clears the previous model and initializes the program for a new model. If it is later
needed, you should save your previous model prior to calling this function.

After calling the InitializeNewModel function, it is not necessary to also call the ApplicationStart
function because the functionality of the ApplicationStart function is included in the
InitializeNewModel function.

The function returns zero if a new model is successfully initialized, otherwise it returns a nonzero
value.

## VBA Example

Sub InitializeNewModel()
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
ret = SapModel.InitializeNewModel(kip_ft_F)

'create model from template
ret = SapModel.File.New2DFrame(ConcentricBraced, 3, 12, 3, 30)

'save model
ret = SapModel.File.Save("C:\SapAPI\MyFirstSapModel.sdb")

'initialize new model
SapModel.InitializeNewModel(kN_m_C)

'create model from template
ret = SapModel.File.New3DFrame(FlatPlate, 2, 4, 2, 10, 4, 10, False, , , , 2, 2)


'save model
ret = SapModel.File.Save("C:\SapAPI\MySecondSapModel.sdb")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

ApplicationStart

# SetMergeTol

## Syntax

SapObject.SapModel.SetMergeTol

## VB6 Procedure

Function SetMergeTol(ByVal MergeTol As Double) As Long

## Parameters

MergeTol

The program auto merge tolerance. [L]

## Remarks

This function sets the program auto merge tolerance.

The function returns zero if the tolerance is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetAutoMergeTolerance()
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

'set auto merge tolerance
ret = SapModel.SetMergeTol(0.05)

'create model from template
ret = SapModel.File.New2DFrame(PortalFrame, 2, 144, 2, 288)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

GetMergeTol

# SetModelIsLocked

## Syntax

SapObject.SapModel.SetModelIsLocked

## VB6 Procedure

Function SetModelIsLocked(LockIt as Boolean) As Long

## Parameters

LockIt

The item is True if the model is to be locked and False if it is to be unlocked.


## Remarks

The function returns zero if the locked status of the model is successfully set. Otherwise it returns
a nonzero value.

With some exceptions, definitions and assignments can not be changed in a model while the
model is locked. If an attempt is made to change a definition or assignment while the model is
locked and that change is not allowed in a locked model, an error will be returned.

## VBA Example

Sub SetModelLocked()
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
ret = SapModel.File.New2DFrame(ConcentricBraced, 3, 124, 3, 200)

'Lock model
ret = SapModel.SetModelIsLocked(True)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetModelIsLocked


# SetNotionalSize

## Syntax

SapObject.SapModel.PropArea.SetNotionalSize

## VB6 Procedure

Function SetNotionalSize(ByVal Name As String, ByVal stype As String, ByVal Value As
Double) As Long

## Parameters

Name

The name of an existing shell-type area section property.

stype

The type to define the notional size of a section. It can be:

```
"Auto" = Program will determine the notional size based on the average thickness of
an area element.
```
```
"User" = The notional size is based on the user-defined value.
```
```
"None" = Notional size will not be considered. In other words, the time-dependent
effect of this section will not be considered.
```
Value

For **stype** is "Auto", the Value represents for the scale factor to the program-determined notional
size; for **stype** is “User”, the **Value** represents for the user-defined notional size [L]; for **stype** is
“None”, the **Value** will not be used and can be set to 1.

## Remarks

This function assigns the method to determine the notional size of an area section for the creep
and shrinkage calculations. This function is currently worked for shell type area section.

The function returns zero if the parameters are successfully assigned; otherwise it returns a
nonzero value.

## VBA Example

Sub AssignAreaPropNotionalSize()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel


Dim ret As Long
Dim i As Long

```
Dim stype As String
```
```
Dim Value As Double
```
```
'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")
```
```
'start Sap2000 application
SapObject.ApplicationStart
```
```
'create SapModel object
Set SapModel = SapObject.SapModel
```
```
'initialize model
ret = SapModel.InitializeNewModel
```
```
'create model from template
ret = SapModel.File.NewWall(2, 48, 2, 48)
```
```
'assign parameters
stype = “Auto”
Value = 1.1
ret = SapModel.PropArea.SetNotionalSize("ASEC1", stype, Value)
```
```
'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
```
End Sub

## Release Notes

Initial release in version 16.1.0

## See Also

GetNotionalSize

# SetPresentCoordSystem

## Syntax

SapObject.SapModel.SetPresentCoordSystem


## VB6 Procedure

Function SetPresentCoordSystem(ByVal CSys As String) As Long

## Parameters

CSys

The name of a defined coordinate system.

## Remarks

This function sets the present coordinate system.

The function returns zero if the present coordinate system is successfully set. Otherwise it returns
a nonzero value.

## VBA Example

Sub SetPresentCSys()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as long
Dim PresentCSys as String

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

'define new coordinate system
ret = SapModel.CoordSys.SetCoordSys("CSys1", 1000, 1000, 0, 0, 0, 0)

'set present coordinate system
ret = SapModel.SetPresentCoordSystem("CSys1")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetPresentCoordSystem

# SetPresentUnits

## Syntax

SapObject.SapModel.SetPresentUnits

## VB6 Procedure

Function SetPresentUnits(ByVal Units As eUnits) As Long

## Parameters

Units

```
One of the following items in the eUnits enumeration:
lb_in_F = 1
lb_ft_F = 2
kip_in_F = 3
kip_ft_F = 4
kN_mm_C = 5
kN_m_C = 6
kgf_mm_C = 7
kgf_m_C = 8
N_mm_C = 9
N_m_C = 10
Ton_mm_C = 11
Ton_m_C = 12
kN_cm_C = 13
kgf_cm_C = 14
N_cm_C = 15
Ton_cm_C = 16
```
## Remarks

This function returns zero if the units are successfully set and nonzero if they are not set.


## VBA Example

Sub SetUnitsPresent()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim FileName As String
Dim ret As Long

'create Sap2000 object
Set SapObject = CreateObject("CSI.SAP2000.API.SapObject")

'start Sap2000 application
SapObject.ApplicationStart

'create SapModel object
Set SapModel = SapObject.SapModel

'initialize model
ret = SapModel.InitializeNewModel

'start a new template model
ret = SapModel.File.New2DFrame(ConcentricBraced, 3, 124, 3, 200)

'set present units to KN-m
ret = SapModel.SetPresentUnits(KN_m_C)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

GetDatabaseUnits

GetPresentUnits

# SetProjectInfo

## Syntax

SapObject.SapModel.SetProjectInfo


## VB6 Procedure

Function SetProjectInfo(ByVal Item As String, ByVal Data As String) As Long

## Parameters

Item

The name of the project information item to be set.

Data

The data for the specified project information item.

## Remarks

This function sets the data for an item in the project information.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub SetProjectInfoData()
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

'set project information data
ret = SapModel.SetProjectInfo("Company Name", "Computers and Structures, Inc.")
ret = SapModel.SetProjectInfo("Project Name", "API Testing")
ret = SapModel.SetProjectInfo("My Item", "My Data")

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing


Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

GetUserComment

# SetUserComment

## Syntax

SapObject.SapModel.SetUserComment

## VB6 Procedure

Function SetUserComment(ByVal Comment As String, Optional ByVal NumLines As Long = 1,
Optional ByVal Replace As Boolean = False) As Long

## Parameters

Comment

The data to be added to the user comments and log.

NumLines

The number of carriage return and line feeds to be included before the specified comment. This
item is ignored if Replace = True. It is also ignored if there are no existing comments.

Replace

If this item is True, all existing comments are replaced with the specified comment.

## Remarks

This function sets the user comments and log data.

The function returns zero if the data is successfully set; otherwise it returns a nonzero value.

## VBA Example

Sub AddCommentToLog()
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

'add comments
ret = SapModel.SetUserComment("Testing the Sap2000 API.")
ret = SapModel.SetUserComment("Adding a second comment.")
ret = SapModel.SetUserComment("Adding a third comment.", 3)

'close Sap2000
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.03.

## See Also

GetUserComment

# GetKeyStringsExtendedEntityData

## Syntax

SapObject.SapModel.GetKeyStringsExtendedEntityData

## VB6 Procedure

Function GetKeyStringsExtendedEntityData (ByVal AppName As String, ByVal Key As String,
ByRef NumberValues As Long, ByRef Values As String()) As Long


## Parameters

AppName

This is an application name of your choice under which your application previously stored some
data. It is recommended you choose a unique name to guarantee no other third-party application
resets the data that was set by your application. Application names are stored in their original
capitalization and character set, but are compared in a case insensitive and culturally invariant
manner for retrieval purposes.

Key

This is an entry name under which the data provided in the remaining arguments was stored. Entry
names are stored in their original capitalization and character set, but are compared in a case
insensitive and culturally invariant manner for retrieval purposes.

NumberValues

The number of strings stored for the given application name and entry name.

Values

This is one-dimensional array of string values. The Values array is created as a dynamic, zero-
based, array by the API user:

Dim Values() as String

The array is dimensioned to (NumberValues – 1) inside the Sap2000 program, filled with the
string values previously stored under the application name AppName and entry name Key, and
returned to the API user.

## Release Notes

Initial release in version 17.2.0.

## See Also

GetKeysWithStringsExtendedEntityData

SetKeyStringsExtendedEntityData

# GetKeysWithStringsExtendedEntityData

## Syntax

SapObject.SapModel.GetKeysWithStringsExtendedEntityData

## VB6 Procedure


Function GetKeysWithStringsExtendedEntityData (ByVal AppName As String, ByRef
NumberKeys As Long, ByRef Keys() As String) As Long

## Parameters

AppName

This is an application name of your choice under which your application previously stored some
data. It is recommended you choose a unique name to guarantee no other third-party application
resets the data that was set by your application. Application names are stored in their original
capitalization and character set, but are compared in a case insensitive and culturally invariant
manner for retrieval purposes.

NumberKeys

The number of different entries for which data was previously stored under the application name
AppName.

Key

This is a one-dimensional array of entry names. The Keys array is created as a dynamic, zero-
based, array by the API user:

Dim Keys() as String

The array is dimensioned to (NumberKeys – 1) inside the Sap2000 program, filled with the entry
names for which data was previously stored under the application name AppName, and returned
to the API user.

## Release Notes

Initial release in version 17.2.0.

## See Also

GetKeyStringsExtendedEntityData

SetKeyStringsExtendedEntityData

# SetStringsExtendedEntityData

## Syntax

SapObject.SapModel.SetStringsExtendedEntityData

## VB6 Procedure

Function SetStringsExtendedEntityData (ByVal AppName As String, ByVal Key As String,
ByRef NumberValues As Long, ByRef Values As String()) As Long


## Parameters

AppName

This is an application name of your choice under which your application previously stored some
data. It is recommended you choose a unique name to guarantee no other third-party application
resets the data that was set by your application. Application names are stored in their original
capitalization and character set, but are compared in a case insensitive and culturally invariant
manner for retrieval purposes.

Key

This is an entry name under which the data provided in the remaining arguments was stored. This
data can later be retrieved, reset, or deleted by providing a valid application name and entry name.
Entry names are stored in their original capitalization and character set, but are compared in a case
insensitive and culturally invariant manner for retrieval purposes.

NumberValues

The number of strings to store for the given application name and entry name.

Values

A one-dimensional array of strings containing NumberValues strings. These strings replace any
strings previously stored for the given application name and entry name. Calling this function with
NumberValues equal to zero is equivalent to erasing any previously stored data.

## Remarks

This function can be used to store metadata for a model, or any other data specific to your
application.

## Release Notes

Initial release in version 17.2.0.

## See Also

GetKeysWithStringsExtendedEntityData

GetKeyStringsExtendedEntityData


