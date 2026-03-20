# Example 1 (VBA)

## Remarks

This example is written for Visual Basic for Applications (VBA). It can be run from a program
such as Microsoft Excel. It is based on the SAP2000 verification problem Example 1-001.
This example creates the example verification problem from scratch, runs the analysis, extracts
results, and compares the results with hand-calculated values.

## Example

1. Create a new VBA project.
2. Add a reference to "SAP2000v1.tlb" to the VBA prointerface. ject. This early binds to the API using the COM

With the release of SAP2000 v26.0.0, users will need to select the TLB file that corresponds to the
bitness of their VBA development environment, e.g. 32-bit Excel or 64-bit Excel. To locate these
files, the user should navigate to the directory where SAP2000 is installed. This is typically
C:\Program Files\Computers and Structures\SAP2000 26\.
Within this directory, the 32-bit library is found at NativeAPI\x86\SAP2000v1.tlb The 64-bit
library is found at NativeAPI\x64\SAP2000v1.tlb.

3. Add a new module to the VBA project and paste in the following code, ready-to-run code.
    Please pay attention to the comments in this code block; they contain important
    information about running the script:
Sub VerificationExample1001()
Dim ret As Long
'set the following flag to True to attach to an existing instance of the program
'otherwise a new instance of the program will be started
Dim AttachToInstance As Boolean
AttachToInstance = False
'set the following flag to True to manually specify the path to SAP2000.exe
'this allows for a connection to a version of SAP2000 other than the latest installation
'otherwise the latest installed version of SAP2000 will be launched
Dim SpecifyPath As Boolean
SpecifyPath = False
'if the above flag is set to True, specify the path to SAP2000 below


Dim ProgramPath As String
ProgramPath = "C:\Program Files\Computers and Structures\SAP2000 26\SAP2000.exe"
'full path to the model
'set it to the desired path of your model
Dim ModelDirectory As String
ModelDirectory = "C:\CSiAPIexample"
If Len(Dir(ModelDirectory, vbDirectory)) = 0 Then
MkDir ModelDirectory
End If
Dim ModelName As String
ModelName = "API_1-001.sdb"
Dim ModelPath As String
ModelPath = ModelDirectory & Application.PathSeparator & ModelName

'create API helper object
Dim myHelper As cHelper
Set myHelper = New Helper
'dimension the SapObject as cOAPI type
Dim mySapObject As cOAPI
Set mySapObject = Nothing

If AttachToInstance Then
'attach to a running instance of SAP
'get the active SapObject
Set mySapObject = myHelper.GetObject("CSI.SAP2000.API.SapObject")
Else
If SpecifyPath Then
'create an instance of the SapObject from the specified path


Set mySapObject = myHelper.CreateObject(ProgramPath)
Else
'create an instance of the SapObject from the latest installed SAP
Set mySapObject = myHelper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
End If
'start SAP2000 application
mySapObject.ApplicationStart
End If

'Get a reference to cSapModel to access all API classes and functions
Dim mySapModel As cSapModel
Set mySapModel = mySapObject.SapModel

'initialize model
ret = mySapModel.InitializeNewModel

'create new blank model
ret = mySapModel.File.NewBlank

'define material property
ret = mySapModel.PropMaterial.SetMaterial("CONC", eMatType_Concrete)

'assign isotropic mechanical properties to material
ret = mySapModel.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2, 0.0000055)

'define rectangular frame section property
ret = mySapModel.PropFrame.SetRectangle("R1", "CONC", 12, 12)


'define frame section property modifiers
Dim i As Long
Dim ModValue() As Double
ReDim ModValue(7)
For i = 0 To 7
ModValue(i) = 1
Next i
ModValue(0) = 1000
ModValue(1) = 0
ModValue(2) = 0
ret = mySapModel.PropFrame.SetModifiers("R1", ModValue)

'switch to k-ft units
ret = mySapModel.SetPresentUnits(eUnits_kip_ft_F)

'add frame object by coordinates
Dim FrameName(2) As String
ret = mySapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, FrameName(0), "R1", "1")
ret = mySapModel.FrameObj.AddByCoord(0, 0, 10, 8, 0, 16, FrameName(1), "R1", "2")
ret = mySapModel.FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10, FrameName(2), "R1", "3")

'assign point object restraint at base
Dim PointName() As String
ReDim PointName(1)
Dim Restraint() As Boolean
ReDim Restraint(5)
For i = 0 To 3
Restraint(i) = True


Next i

For i = 4 To 5
Restraint(i) = False
Next i
ret = mySapModel.FrameObj.GetPoints(FrameName(0), PointName(0), PointName(1))
ret = mySapModel.PointObj.SetRestraint(PointName(0), Restraint)

'assign point object restraint at top
For i = 0 To 1
Restraint(i) = True
Next i
For i = 2 To 5
Restraint(i) = False
Next i
ret = mySapModel.FrameObj.GetPoints(FrameName(1), PointName(0), PointName(1))
ret = mySapModel.PointObj.SetRestraint(PointName(1), Restraint)

'refresh view, update (initialize) zoom
ret = mySapModel.View.RefreshView(0, False)

'add load patterns
ret = mySapModel.LoadPatterns.Add("1", eLoadPatternType_Other, 1)
ret = mySapModel.LoadPatterns.Add("2", eLoadPatternType_Other)
ret = mySapModel.LoadPatterns.Add("3", eLoadPatternType_Other)
ret = mySapModel.LoadPatterns.Add("4", eLoadPatternType_Other)
ret = mySapModel.LoadPatterns.Add("5", eLoadPatternType_Other)
ret = mySapModel.LoadPatterns.Add("6", eLoadPatternType_Other)


ret = mySapModel.LoadPatterns.Add("7", eLoadPatternType_Other)

'assign loading for load pattern 2
ret = mySapModel.FrameObj.GetPoints(FrameName(2), PointName(0), PointName(1))
Dim PointLoadValue() As Double
ReDim PointLoadValue(5)
PointLoadValue(2) = -
ret = mySapModel.PointObj.SetLoadForce(PointName(0), "2", PointLoadValue)
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(2), "2", 1, 10, 0, 1, 1.8, 1.8)

'assign loading for load pattern 3
ret = mySapModel.FrameObj.GetPoints(FrameName(2), PointName(0), PointName(1))
ReDim PointLoadValue(5)
PointLoadValue(2) = -17.
PointLoadValue(4) = -54.
ret = mySapModel.PointObj.SetLoadForce(PointName(1), "3", PointLoadValue)

'assign loading for load pattern 4
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(1), "4", 1, 11, 0, 1, 2, 2)

'assign loading for load pattern 5
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(0), "5", 1, 2, 0, 1, 2, 2, "Local")
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(1), "5", 1, 2, 0, 1, -2, -2,
"Local")

'assign loading for load pattern 6
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(0), "6", 1, 2, 0, 1, 0.9984,
0.3744, "Local")
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(1), "6", 1, 2, 0, 1, -0.3744, 0,
"Local")


'assign loading for load pattern 7
ret = mySapModel.FrameObj.SetLoadPoint(FrameName(1), "7", 1, 2, 0.5, -15, "Local")

'switch to k-in units
ret = mySapModel.SetPresentUnits(eUnits_kip_in_F)

'save model
ret = mySapModel.File.Save(ModelPath)

'run model (this will create the analysis model)
ret = mySapModel.Analyze.RunAnalysis

'initialize for results
Dim SapResult(6) As Double
ret = mySapModel.FrameObj.GetPoints(FrameName(1), PointName(0), PointName(1))

'get results for load patterns 1 through 7
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
For i = 0 To 6
ret = mySapModel.Results.Setup.DeselectAllCasesAndCombosForOutput
ret = mySapModel.Results.Setup.SetCaseSelectedForOutput(Format(i + 1))
If i <= 3 Then
ret = mySapModel.Results.JointDispl(PointName(1), eItemTypeElm_ObjectElm,
NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
SapResult(i) = U3(0)
Else
ret = mySapModel.Results.JointDispl(PointName(0), eItemTypeElm_ObjectElm,
NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
SapResult(i) = U1(0)
End If
Next i

'close application
mySapObject.ApplicationExit False
Set mySapModel = Nothing
Set mySapObject = Nothing

'fill result strings
Dim SapResultString(6) As String
For i = 0 To 6
SapResultString(i) = Format(SapResult(i), "0.00000")
If Left(SapResultString(i), 1) <> "-" Then
SapResultString(i) = " " & SapResultString(i)
End If
Next i


'fill independent results (hand calculated)
Dim IndResult(6) As Double
Dim IndResultString(6) As String
IndResult(0) = -0.
IndResult(1) = 0.
IndResult(2) = 0.
IndResult(3) = -0.
IndResult(4) = 0.
IndResult(5) = 0.
IndResult(6) = 0.
For i = 0 To 6
IndResultString(i) = Format(IndResult(i), "0.00000")
If Left(IndResultString(i), 1) <> "-" Then
IndResultString(i) = " " & IndResultString(i)
End If
Next i

'fill percent difference
Dim PercentDiff(6) As Double
Dim PercentDiffString(6) As String
For i = 0 To 6
PercentDiff(i) = (SapResult(i) / IndResult(i)) - 1
PercentDiffString(i) = Format(PercentDiff(i), "0%")
If Left(PercentDiffString(i), 1) <> "-" Then
PercentDiffString(i) = " " & PercentDiffString(i)
End If
Next i


'display message box comparing results
Dim msg As String
msg = ""
msg = msg & "LC Sap2000 Independent %Diff" & vbCr & vbLf
For i = 0 To 5
msg = msg & Format(i + 1) & " " & SapResultString(i) & " " & IndResultString(i) & " " &
PercentDiffString(i) & vbCr & vbLf
Next i
msg = msg & Format(i + 1) & " " & SapResultString(i) & " " & IndResultString(i) & " " &
PercentDiffString(i)
MsgBox msg
End Sub

## Release Notes

Initial release in version 15.0.1.
Updated for version 22.1.0.
Updated for version 26.0.0.

# Example 2 (Visual Basic)

## Remarks

This Visual Basic example was created using Visual Studio 2022. It is based on the SAP
verification problem Example 1-001.
This example creates the example verification problem from scratch, runs the analysis, extracts
results, and compares the results with hand-calculated values.

## Example

1. Create a new Visual Basic project, of type "Console App". Your project can target .NET 8
    or .NET Framework 4.8, the example code is designed to be compatible with either.
2. Add a reference to SAP2000v1.dll to the project. This file is located in the directory where
    SAP2000 is installed, typically C:\Program Files\Computers and Structures\SAP2000 26\.


3. Copy the code below into the generated module. Please pay attention to the comments in
    this code block; they contain important information about running the script.v
Imports SAP2000v
Module Module
Sub Main()
'set the following flag to True to attach to an existing instance of
the program
'otherwise a new instance of the program will be started
Dim AttachToInstance As Boolean
AttachToInstance = False
'set the following flag to True to manually specify the path to
SAP2000.exe
'this allows for a connection to a version of SAP2000 other than the
latest installation
'otherwise the latest installed version of SAP2000 will be launched
Dim SpecifyPath As Boolean
SpecifyPath = False
'if the above flag is set to True, specify the path to SAP2000 below
Dim ProgramPath As String
ProgramPath = "C:\Program Files\Computers and Structures\SAP2000 26
\SAP2000.exe"
'full path to the model
'set it to the desired path of your model
Dim ModelDirectory As String = "C:\CSiAPIexample"
Try
System.IO.Directory.CreateDirectory(ModelDirectory)
Catch ex As Exception
Console.WriteLine("Could not create directory: " + ModelDirectory)
End Try
Dim ModelName As String = "API_1-001.sdb"


Dim ModelPath As String = ModelDirectory +
System.IO.Path.DirectorySeparatorChar + ModelName
'dimension the SapObject as cOAPI type
Dim mySapObject As cOAPI
mySapObject = Nothing
'Use ret to check if functions return successfully (ret = 0) or fail
(ret = nonzero)
Dim ret As Integer
ret = -
'create API helper object
Dim myHelper As cHelper
Try
myHelper = New Helper
Catch ex As Exception
Console.WriteLine("Cannot create an instance of the Helper
object")
End Try
If AttachToInstance Then
'attach to a running instance of SAP200 0
Try
'get the active SapObject
mySapObject = myHelper.GetObject("CSI.SAP2000.API.SapObject")
Catch ex As Exception
Console.WriteLine("No running instance of the program found or
failed to attach.")
Return
End Try
Else
If SpecifyPath Then
Try


'create an instance of the SapObject from the specified
path
mySapObject = myHelper.CreateObject(ProgramPath)
Catch ex As Exception
Console.WriteLine("Cannot start a new instance of the
program from " + ProgramPath)
Return
End Try
Else
Try
'create an instance of the SapObject from the latest
installed SAP
mySapObject = myHelper.CreateObjectProgID
("CSI.SAP2000.API.SapObject")
Catch ex As Exception
Console.WriteLine("Cannot start a new instance of the
program.")
Return
End Try
End If
'start SAP2000 application
ret = mySapObject.ApplicationStart()
End If
'Get a reference to cSapModel to access all API classes and functions
Dim mySapModel As cSapModel
mySapModel = mySapObject.SapModel
'initialize model
ret = mySapModel.InitializeNewModel()
'create new blank model
ret = mySapModel.File.NewBlank()
'define material property


ret = mySapModel.PropMaterial.SetMaterial("CONC", eMatType.Concrete)
'assign isotropic mechanical properties to material
ret = mySapModel.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2,
0.0000055)
'define rectangular frame section property
ret = mySapModel.PropFrame.SetRectangle("R1", "CONC", 12, 12)
'define frame section property modifiers
Dim ModValue(7) As Double
For i = 0 To 7
ModValue(i) = 1
Next i
ModValue(0) = 1000
ModValue(1) = 0
ModValue(2) = 0
ret = mySapModel.PropFrame.SetModifiers("R1", ModValue)
'switch to k-ft units
ret = mySapModel.SetPresentUnits(eUnits.kip_ft_F)
'add frame object by coordinates
Dim FrameName(2) As String
ret = mySapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, FrameName(0),
"R1", "1")
ret = mySapModel.FrameObj.AddByCoord(0, 0, 10, 8, 0, 16, FrameName(1),
"R1", "2")
ret = mySapModel.FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10, FrameName
(2), "R1", "3")
'assign point object restraint at base
Dim PointName(1) As String
Dim Restraint(5) As Boolean
For i = 0 To 3
Restraint(i) = True


Next i
For i = 4 To 5
Restraint(i) = False
Next i
ret = mySapModel.FrameObj.GetPoints(FrameName(0), PointName(0),
PointName(1))
ret = mySapModel.PointObj.SetRestraint(PointName(0), Restraint)
'assign point object restraint at top
For i = 0 To 1
Restraint(i) = True
Next i
For i = 2 To 5
Restraint(i) = False
Next i
ret = mySapModel.FrameObj.GetPoints(FrameName(1), PointName(0),
PointName(1))
ret = mySapModel.PointObj.SetRestraint(PointName(1), Restraint)
'refresh view, update (initialize) zoom
ret = mySapModel.View.RefreshView(0, False)
'add load patterns
ret = mySapModel.LoadPatterns.Add("1", eLoadPatternType.Other, 1)
ret = mySapModel.LoadPatterns.Add("2", eLoadPatternType.Other)
ret = mySapModel.LoadPatterns.Add("3", eLoadPatternType.Other)
ret = mySapModel.LoadPatterns.Add("4", eLoadPatternType.Other)
ret = mySapModel.LoadPatterns.Add("5", eLoadPatternType.Other)
ret = mySapModel.LoadPatterns.Add("6", eLoadPatternType.Other)
ret = mySapModel.LoadPatterns.Add("7", eLoadPatternType.Other)
'assign loading for load pattern 2
ret = mySapModel.FrameObj.GetPoints(FrameName(2), PointName(0),
PointName(1))


Dim PointLoadValue(5) As Double
PointLoadValue(2) = -
ret = mySapModel.PointObj.SetLoadForce(PointName(0), "2",
PointLoadValue)
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(2), "2", 1, 10,
0, 1, 1.8, 1.8)
'assign loading for load pattern 3
ret = mySapModel.FrameObj.GetPoints(FrameName(2), PointName(0),
PointName(1))
ReDim PointLoadValue(5)
PointLoadValue(2) = -17.
PointLoadValue(4) = -54.
ret = mySapModel.PointObj.SetLoadForce(PointName(1), "3",
PointLoadValue)
'assign loading for load pattern 4
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(1), "4", 1, 11,
0, 1, 2, 2)
'assign loading for load pattern 5
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(0), "5", 1, 2,
0, 1, 2, 2, "Local")
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(1), "5", 1, 2,
0, 1, -2, -2, "Local")
'assign loading for load pattern 6
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(0), "6", 1, 2,
0, 1, 0.9984, 0.3744, "Local")
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName(1), "6", 1, 2,
0, 1, -0.3744, 0, "Local")
'assign loading for load pattern 7
ret = mySapModel.FrameObj.SetLoadPoint(FrameName(1), "7", 1, 2, 0.5, -
15, "Local")
'switch to k-in units
ret = mySapModel.SetPresentUnits(eUnits.kip_in_F)
'save model


ret = mySapModel.File.Save(ModelPath)
'run model (this will create the analysis model)
ret = mySapModel.Analyze.RunAnalysis
'initialize for results
Dim SapResult(6) As Double
ret = mySapModel.FrameObj.GetPoints(FrameName(1), PointName(0),
PointName(1))
'get results for load patterns 1 through 7
Dim NumberResults As Integer = 0
Dim Obj(0) As String
Dim Elm(0) As String
Dim LoadCase(0) As String
Dim StepType(0) As String
Dim StepNum(0) As Double
Dim U1(0) As Double
Dim U2(0) As Double
Dim U3(0) As Double
Dim R1(0) As Double
Dim R2(0) As Double
Dim R3(0) As Double
For i = 0 To 6
ret = mySapModel.Results.Setup.DeselectAllCasesAndCombosForOutput
ret = mySapModel.Results.Setup.SetCaseSelectedForOutput(Format(i +
1))
If i <= 3 Then
ret = mySapModel.Results.JointDispl(PointName(1),
eItemTypeElm.ObjectElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum,
U1, U2, U3, R1, R2, R3)
SapResult(i) = U3(0)
Else


ret = mySapModel.Results.JointDispl(PointName(0),
eItemTypeElm.ObjectElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum,
U1, U2, U3, R1, R2, R3)
SapResult(i) = U1(0)
End If
Next i
'close the application
mySapObject.ApplicationExit(False)
mySapModel = Nothing
mySapObject = Nothing
'fill result strings
Dim SapResultString(6) As String
For i = 0 To 6
SapResultString(i) = Format(SapResult(i), "0.00000")
If Microsoft.VisualBasic.Left(SapResultString(i), 1) <> "-" Then
SapResultString(i) = " " & SapResultString(i)
End If
Next i
'fill independent results (hand calculated)
Dim IndResult(6) As Double
Dim IndResultString(6) As String
IndResult(0) = -0.
IndResult(1) = 0.
IndResult(2) = 0.
IndResult(3) = -0.
IndResult(4) = 0.
IndResult(5) = 0.
IndResult(6) = 0.
For i = 0 To 6


IndResultString(i) = Format(IndResult(i), "0.00000")
If Microsoft.VisualBasic.Left(IndResultString(i), 1) <> "-" Then
IndResultString(i) = " " & IndResultString(i)
End If
Next i
'fill percent difference
Dim PercentDiff(6) As Double
Dim PercentDiffString(6) As String
For i As Integer = 0 To 6
PercentDiff(i) = (SapResult(i) / IndResult(i)) - 1
PercentDiffString(i) = Format(PercentDiff(i), "0%")
If Microsoft.VisualBasic.Left(PercentDiffString(i), 1) <> "-" Then
PercentDiffString(i) = " " & PercentDiffString(i)
End If
Next i
'display message box comparing results
Dim msg As String = ""
msg = msg & "LC SAP2000 Independent %Diff" & vbCr & vbLf
For i As Integer = 0 To 6
msg = msg & Format(i + 1) & " " & SapResultString(i) & " " &
IndResultString(i) & " " & PercentDiffString(i) & If(i < 6, vbCr & vbLf,
"")
Next i
Console.WriteLine(msg)
End Sub
End Module

## Release Notes

```
Initial release in version 15.0.1.
Updated for version 22.1.0.
```

Updated for vesion 26.0.0.

# Example 3 (C#)

## Remarks

This C# example was created using Visual Studio 2022. It is based on the SAP2000 verification
problem Example 1-001.
This example creates the example verification problem from scratch, runs the analysis, extracts
results, and compares the results with hand calculated values.

## Example

1. Create a new C# project, of type "Console App". Your project can target .NET 8 or .NET
    Framework 4.8, the example code is designed to be compatible with either.
2. Add a reference to SAP2000v1.dll" to the project. >This file is located in the directory
    where SAP2000 is installed, typically C:\Program Files\Computers and
    Structures\SAP2000 26\.
3. Copy the code below into the created class. Please pay attention to the comments in this
    code block; they contain important information about running the script.
using System;
using SAP2000v1;
namespace ConsoleApplication
{
internal class Program
{
static void Main(string[] args)
{
//set the following flag to true to attach to an existing
instance of the program
//otherwise a new instance of the program will be started
bool AttachToInstance;
AttachToInstance = false;
//set the following flag to true to manually specify the path to
SAP2000.exe


//this allows for a connection to a version of SAP2000 other than
the latest installation
//otherwise the latest installed version of SAP2000 will be
launched
bool SpecifyPath;
SpecifyPath = false;
//if the above flag is set to true, specify the path to SAP2000
below
string ProgramPath;
ProgramPath = @"C:\Program Files\Computers and Structures\SAP2000
26\SAP2000.exe";
//full path to the model
//set it to the desired path of your model
string ModelDirectory = @"C:\CSiAPIexample";
try
{
System.IO.Directory.CreateDirectory(ModelDirectory);
}
catch (Exception ex)
{
Console.WriteLine("Could not create directory: " +
ModelDirectory);
return;
}
string ModelName = "API_1-001.sdb"; string ModelPath =
ModelDirectory + System.IO.Path.DirectorySeparatorChar + ModelName;
//dimension the SapObject as cOAPI type
cOAPI mySapObject = null;
//Use ret to check if functions return successfully (ret = 0) or
fail (ret = nonzero)
int ret = 0;
//create API helper object


cHelper myHelper;
try
{
myHelper = new Helper();
}
catch (Exception ex)
{
Console.WriteLine("Cannot create an instance of the Helper
object");
return;
}
if (AttachToInstance)
{
//attach to a running instance of SAP2000
try
{
mySapObject = myHelper.GetObject
("CSI.SAP2000.API.SapObject");
}
catch (Exception ex)
{
Console.WriteLine("No running instance of the program
found or failed to attach.");
return;
}
}
else
{
if (SpecifyPath)
{


//create an instance of the SapObject from the specified
path
try
{
mySapObject = myHelper.CreateObject(ProgramPath);
}
catch (Exception ex)
{
Console.WriteLine("Cannot start a new instance of the
program from " + ProgramPath);
return;
}
}
else
{
//create an instance of the SapObject from the latest
installed SAP2000
try
{
mySapObject = myHelper.CreateObjectProgID
("CSI.SAP2000.API.SapObject");
}
catch (Exception ex)
{
Console.WriteLine("Cannot start a new instance of the
program.");
return;
}
}
//start SAP2000 application
ret = mySapObject.ApplicationStart();


}
//create SapModel object
cSapModel mySapModel;
mySapModel = mySapObject.SapModel;
//initialize model
ret = mySapModel.InitializeNewModel((eUnits.kip_in_F));
//create new blank model
ret = mySapModel.File.NewBlank();
//define material property
ret = mySapModel.PropMaterial.SetMaterial("CONC",
eMatType.Concrete, -1, "", "");
//assign isotropic mechanical properties to material
ret = mySapModel.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2,
0.0000055, 0);
//define rectangular frame section property
ret = mySapModel.PropFrame.SetRectangle("R1", "CONC", 12, 12, 1,
"", "");
//define frame section property modifiers
double[] ModValue = new double[8];
int i;
for (i = 0; i <= 7; i++)
{
ModValue[i] = 1;
}
ModValue[0] = 1000;
ModValue[1] = 0;
ModValue[2] = 0;
ret = mySapModel.PropFrame.SetModifiers("R1", ref ModValue);
//switch to k-ft units
ret = mySapModel.SetPresentUnits(eUnits.kip_ft_F);


//add frame object by coordinates
string[] FrameName = new string[3];
string temp_string1 = FrameName[0];
string temp_string2 = FrameName[0];
ret = mySapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, ref
temp_string1, "R1", "1", "Global");
FrameName[0] = temp_string1;
ret = mySapModel.FrameObj.AddByCoord(0, 0, 10, 8, 0, 16, ref
temp_string1, "R1", "2", "Global");
FrameName[1] = temp_string1;
ret = mySapModel.FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10, ref
temp_string1, "R1", "3", "Global");
FrameName[2] = temp_string1;
//assign point object restraint at base
string[] PointName = new string[2];
bool[] Restraint = new bool[6];
for (i = 0; i <= 3; i++)
{
Restraint[i] = true;
}
for (i = 4; i <= 5; i++)
{
Restraint[i] = false;
}
ret = mySapModel.FrameObj.GetPoints(FrameName[0], ref
temp_string1, ref temp_string2);
PointName[0] = temp_string1;
PointName[1] = temp_string2;
ret = mySapModel.PointObj.SetRestraint(PointName[0], ref
Restraint, 0);
//assign point object restraint at top


for (i = 0; i <= 1; i++)
{
Restraint[i] = true;
}
for (i = 2; i <= 5; i++)
{
Restraint[i] = false;
}
ret = mySapModel.FrameObj.GetPoints(FrameName[1], ref
temp_string1, ref temp_string2);
PointName[0] = temp_string1;
PointName[1] = temp_string2;
ret = mySapModel.PointObj.SetRestraint(PointName[1], ref
Restraint, 0);
//refresh view, update (initialize) zoom
bool temp_bool = false;
ret = mySapModel.View.RefreshView(0, temp_bool);
//add load patterns
temp_bool = true;
ret = mySapModel.LoadPatterns.Add("1", eLoadPatternType.Other, 1,
temp_bool);
ret = mySapModel.LoadPatterns.Add("2", eLoadPatternType.Other, 0,
temp_bool);
ret = mySapModel.LoadPatterns.Add("3", eLoadPatternType.Other, 0,
temp_bool);
ret = mySapModel.LoadPatterns.Add("4", eLoadPatternType.Other, 0,
temp_bool);
ret = mySapModel.LoadPatterns.Add("5", eLoadPatternType.Other, 0,
temp_bool);
ret = mySapModel.LoadPatterns.Add("6", eLoadPatternType.Other, 0,
temp_bool);
ret = mySapModel.LoadPatterns.Add("7", eLoadPatternType.Other, 0,
temp_bool);


//assign loading for load pattern 2
ret = mySapModel.FrameObj.GetPoints(FrameName[2], ref
temp_string1, ref temp_string2);
PointName[0] = temp_string1;
PointName[1] = temp_string2;
double[] PointLoadValue = new double[6];
PointLoadValue[2] = -10;
ret = mySapModel.PointObj.SetLoadForce(PointName[0], "2", ref
PointLoadValue, false, "Global", 0);
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName[2], "2",
1, 10, 0, 1, 1.8, 1.8, "Global", true, true, 0);
//assign loading for load pattern 3
ret = mySapModel.FrameObj.GetPoints(FrameName[2], ref
temp_string1, ref temp_string2);
PointName[0] = temp_string1;
PointName[1] = temp_string2;
PointLoadValue = new double[6];
PointLoadValue[2] = -17.2;
PointLoadValue[4] = -54.4;
ret = mySapModel.PointObj.SetLoadForce(PointName[1], "3", ref
PointLoadValue, false, "Global", 0);
//assign loading for load pattern 4
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName[1], "4",
1, 11, 0, 1, 2, 2, "Global", true, true, 0);
//assign loading for load pattern 5
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName[0], "5",
1, 2, 0, 1, 2, 2, "Local", true, true, 0);
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName[1], "5",
1, 2, 0, 1, -2, -2, "Local", true, true, 0);
//assign loading for load pattern 6
ret = mySapModel.FrameObj.SetLoadDistributed(FrameName[0], "6",
1, 2, 0, 1, 0.9984, 0.3744, "Local", true, true, 0);


ret = mySapModel.FrameObj.SetLoadDistributed(FrameName[1], "6",
1, 2, 0, 1, -0.3744, 0, "Local", true, true, 0);
//assign loading for load pattern 7
ret = mySapModel.FrameObj.SetLoadPoint(FrameName[1], "7", 1, 2,
0.5, -15, "Local", true, true, 0);
//switch to k-in units
ret = mySapModel.SetPresentUnits(eUnits.kip_in_F);
//save model
ret = mySapModel.File.Save(ModelPath);
//run model (this will create the analysis model)
ret = mySapModel.Analyze.RunAnalysis();
//initialize for SAP2000 results
double[] SapResult = new double[7];
ret = mySapModel.FrameObj.GetPoints(FrameName[1], ref
temp_string1, ref temp_string2);
PointName[0] = temp_string1;
PointName[1] = temp_string2;
//get SAP2000 results for load patterns 1 through 7
int NumberResults = 0;
string[] Obj = new string[1];
string[] Elm = new string[1];
string[] LoadCase = new string[1];
string[] StepType = new string[1];
double[] StepNum = new double[1];
double[] U1 = new double[1];
double[] U2 = new double[1];
double[] U3 = new double[1];
double[] R1 = new double[1];
double[] R2 = new double[1];
double[] R3 = new double[1];


for (i = 0; i <= 6; i++)
{
ret =
mySapModel.Results.Setup.DeselectAllCasesAndCombosForOutput();
ret = mySapModel.Results.Setup.SetCaseSelectedForOutput
(Convert.ToString(i + 1), true);
if (i <= 3)
{
ret = mySapModel.Results.JointDispl(PointName[1],
eItemTypeElm.ObjectElm, ref NumberResults, ref Obj, ref Elm, ref LoadCase,
ref StepType, ref StepNum, ref U1, ref U2, ref U3, ref R1, ref R2, ref R3);
SapResult[i] = U3[0];
}
else
{
ret = mySapModel.Results.JointDispl(PointName[0],
eItemTypeElm.ObjectElm, ref NumberResults, ref Obj, ref Elm, ref LoadCase,
ref StepType, ref StepNum, ref U1, ref U2, ref U3, ref R1, ref R2, ref R3);
SapResult[i] = U1[0];
}
}
//close SAP2000
mySapObject.ApplicationExit(false);
mySapModel = null;
mySapObject = null;
//fill SAP2000 result strings
string[] SapResultString = new string[7];
for (i = 0; i <= 6; i++)
{
SapResultString[i] = string.Format("{0:0.00000}", SapResult
[i]);


ret = (string.Compare(SapResultString[i], 1, "-", 1, 1,
true));
if (ret != 0)
{
SapResultString[i] = " " + SapResultString[i];
}
}
//fill independent results
double[] IndResult = new double[7];
string[] IndResultString = new string[7];
IndResult[0] = -0.02639;
IndResult[1] = 0.06296;
IndResult[2] = 0.06296;
IndResult[3] = -0.2963;
IndResult[4] = 0.3125;
IndResult[5] = 0.11556;
IndResult[6] = 0.00651;
for (i = 0; i <= 6; i++)
{
IndResultString[i] = string.Format("{0:0.00000}", IndResult
[i]);
ret = (string.Compare(IndResultString[i], 1, "-", 1, 1,
true));
if (ret != 0)
{
IndResultString[i] = " " + IndResultString[i];
}
}
//fill percent difference
double[] PercentDiff = new double[7];


string[] PercentDiffString = new string[7];
for (i = 0; i <= 6; i++)
{
PercentDiff[i] = (SapResult[i] / IndResult[i]) - 1;
PercentDiffString[i] = string.Format("{0:0%}", PercentDiff
[i]);
ret = (string.Compare(PercentDiffString[i], 1, "-", 1, 1,
true));
if (ret != 0)
{
PercentDiffString[i] = " " + PercentDiffString[i];
}
}
//display message box comparing results
string msg = "";
msg = msg + "LC Sap2000 Independent %Diff\r\n";
for (i = 0; i <= 5; i++)
{
msg = msg + string.Format("{0:0}", i + 1) + " " +
SapResultString[i] + " " + IndResultString[i] + " " +
PercentDiffString[i] + "\r\n";
}
msg = msg + string.Format("{0:0}", i + 1) + " " +
SapResultString[i] + " " + IndResultString[i] + " " +
PercentDiffString[i];
Console.WriteLine(msg);
Console.Read();
}
}
}


## Release Notes

Initial release in version 15.0.1
Updated for version 22.1.0.
Updated for vesion 26.0.0.

# Example 4 (Intel Fortran)

## Remarks

This example is written for Intel Fortran with Microsoft Visual Studio Integration. It is based on
the SAP2000 verification problem Example 1-001.
This example creates the example verification problem from scratch, runs the analysis, extracts
results, and compares the results with hand-calculated values.

## Example

1. Create an empty Fortran project of type "Console App".
2. Using the Intel Fortran Module Wizard (under -> Intel Compiler menu), browse for
    SAP2000v1.tlb".
With the release of SAP2000 v26.0.0, users will need to select the TLB file that
corresponds to the bitness of their API client, e.g. 32-bit or 64-bit. To locate these files, the
user should navigate to the directory where SAP2000 is installed. This is typically
C:\Program Files\Computers and Structures\SAP2000 26\.
Within this directory, the 32-bit library is found at NativeAPI\x86\SAP2000v1.tlb The 64-
bit library is found at NativeAPI\x64\SAP2000v1.tlb.
3. Once you have selected SAP2000v1.tlb, click "Next", then select desired (or all)
    enumerations and interfaces to generate SAP2000v1.f90. The generated module contains
    explicit interfaces to all objects and member functions of the SAP2000 API. Add
    SAP2000v1.f90 to the project by right clicking on the "Source Files" folder in Solution
    Explorer and by selecting "Add -> Existing Item..."
    Some of the constants generated by the Module Wizard can exceed 64 characters and lead
    to compiler errors. If so, such constants can either be removed if not used, or shortened
    manually.
4. Add an empty source file by right clicking on the “Source Files” folder in Solution
    Explorer and by selecting "Add -> New Item -> Fortran Free-form File (.f90)".
5. Open the empty source file and paste in the following code. Please pay attention to the
    comments in this code block; they contain important information about running the script.
program APIExample


use SAP2000v1 !gives access to SAP2000 API calls
implicit none

```
!parameters
integer(kind=4), parameter :: nDimCON = 1! array dimension
!local variables
integer(kind=INT_PTR_KIND()) :: pHelper! pointer to API helper
object
integer(kind=INT_PTR_KIND()) :: pSapObject! pointer to a Sap object
integer(kind=INT_PTR_KIND()) :: pSapModel! pointer to a model object
integer(kind=INT_PTR_KIND()) :: pFile! pointer to a file object
integer(kind=INT_PTR_KIND()) :: pPropMaterial! pointer to a material
property object
integer(kind=INT_PTR_KIND()) :: pPropFrame! pointer to a model
object
integer(kind=INT_PTR_KIND()) :: pFrameObj! pointer to a frame object
integer(kind=INT_PTR_KIND()) :: pView! pointer to a view object
integer(kind=INT_PTR_KIND()) :: pPointObj! pointer to a point object
integer(kind=INT_PTR_KIND()) :: pLoadPatterns! pointer to a load
patterns object
integer(kind=INT_PTR_KIND()) :: pAnalyze! pointer to an analyze
object
integer(kind=INT_PTR_KIND()) :: pAnalysisResults! pointer to a
analysis results object
integer(kind=INT_PTR_KIND()) :: pAnalysisResultsSetup! pointer to a
setup object
integer(kind=4) :: iStatus! error code returned from COM subsystem
integer(kind=4) :: iRet! error code returned from SAP2000 API calls
integer(kind=4) :: iCol
integer(kind=4) :: iUnits
integer(kind=4) :: iColor
integer(kind=4) :: iWindow
```

integer(kind=4) :: iItemType
integer(kind=4) :: iTypleLoadPat
integer(kind=4) :: iMyType
integer(kind=4) :: iDir
integer(kind=4) :: iNumberResults
real(kind=8) :: dE
real(kind=8) :: dU
real(kind=8) :: dA
real(kind=8) :: dTemp
real(kind=8) :: dT3
real(kind=8) :: dT2
real(kind=8) :: dModValue
real(kind=8) :: dXi
real(kind=8) :: dYi
real(kind=8) :: dZi
real(kind=8) :: dXj
real(kind=8) :: dYj
real(kind=8) :: dZj
real(kind=8) :: dSelfWTMultiplier
real(kind=8) :: dDist1
real(kind=8) :: dDist2
real(kind=8) :: dVal1
real(kind=8) :: dVal2
real(kind=8) :: dSapResultsRA1(7)
real(kind=8) :: dIndResultsRA1(7)
logical(kind=2) :: bVisible
logical(kind=2) :: bFileSave
logical(kind=2) :: bZoom


logical(kind=2) :: bRestrained
logical(kind=2) :: bAddLoadCase
logical(kind=2) :: bReplace
logical(kind=2) :: bRelDist
logical(kind=2) :: bSelected
character(len=256) :: cModelPath
character(len=256) :: cNotes
character(len=256) :: cGUID
character(len=256) :: cCsys
character(len=256) :: cLoadPat
character(len=256) :: cFrameName(3)
character(len=256) :: cPointName(2)
! pointers to SafeArrays
type(SA_BOUNDS) :: saBounds! bounds object defining for SafeArray
integer(kind=INT_PTR_KIND()) :: pModValueSA! property modifiers
integer(kind=INT_PTR_KIND()) :: pRestraintSA! restraints
integer(kind=INT_PTR_KIND()) :: pPointLoadValueSA! load values
integer(kind=INT_PTR_KIND()) :: pObjSA! object names
integer(kind=INT_PTR_KIND()) :: pElmSA! element names
integer(kind=INT_PTR_KIND()) :: pLCaseSA! load case names
integer(kind=INT_PTR_KIND()) :: pStepTypeSA! step type names
integer(kind=INT_PTR_KIND()) :: pStepNumSA! step numbers
integer(kind=INT_PTR_KIND()) :: pU1SA! displacements along u1
integer(kind=INT_PTR_KIND()) :: pU2SA! displacements along u2
integer(kind=INT_PTR_KIND()) :: pU3SA! displacements along u3
integer(kind=INT_PTR_KIND()) :: pR1SA! displacements along r1
integer(kind=INT_PTR_KIND()) :: pR2SA! displacements along r2
integer(kind=INT_PTR_KIND()) :: pR3SA! displacements along r3


!set the following flag to true to attach to an existing instance of
the program
!otherwise a new instance of the program will be started
logical(kind=2) :: bAttachToInstance
!set the following flag to True to manually specify the path to
SAP2000.exe
!this allows for a connection to a version of SAP2000 other than the
latest installation
!otherwise the latest installed version of SAP2000 will be launched
logical(kind=2) :: bSpecifyPath
!full path to the program executable
character(len=256) :: cProgramPath
bAttachToInstance = .false.! .true.!
bSpecifyPath = .false.! .true.!
!full path to the program executable
!set it to the installation folder
cProgramPath = 'C:\Program Files\Computers and Structures\SAP2000 26
\SAP2000.exe'
!full path to the model
!set it to an already existing folder
cModelPath = 'C:\CSiAPIExample\API_1-001.sdb'
!initialize COM
call COMInitialize(iStatus)
if (bAttachToInstance) then
!attach to a running instance of SAP2000
call COMGetActiveObjectByProgID("CSI.SAP2000.API.SapObject",
pSapObject, iStatus)
call COMQueryInterface(pSapObject, IID_cOAPI, pSapObject, iStatus)
else
!create a new instance of SAP2000
!create helper object


call COMCreateObjectByGUID(CLSID_Helper, CLSCTX_ALL, IID_cHelper,
pHelper, iStatus)
if (bSpecifyPath) then
!create SAP2000 object
iStatus = $cHelper_CreateObject(pHelper, cProgramPath,
pSapObject)
else
!create SAP2000 object
iStatus = $cHelper_CreateObjectProgID(pHelper,
"CSI.SAP2000.API.SapObject", pSapObject)
end if
!start SAP2000 application
iUnits = eUnits_kip_in_F
bVisible = .true.
iStatus = $cOAPI_ApplicationStart(pSapObject, iUnits, bVisible,
'', iRet)
end if
!create SapModel object
iStatus = $cOAPI_GetSapModel(pSapObject, pSapModel)
!initialize model
iUnits = eUnits_kip_in_F
iStatus = $cSapModel_InitializeNewModel(pSapModel, iUnits, iRet)
!create new blank model
iStatus = $cSapModel_GetFile(pSapModel, pFile)
iStatus = $cFile_NewBlank(pFile, iRet)
!define material property
iStatus = $cSapModel_GetPropMaterial(pSapModel, pPropMaterial)
iColor = -1
cNotes = ''
cGUID = ''


iStatus = $cPropMaterial_SetMaterial(pPropMaterial, 'CONC',
eMatType_Concrete, iColor, cNotes, cGUID, iRet)
!assign isotropic mechanical properties to material
dE = 3600.
dU = 0.2
dA = 0.0000055
dTemp = 0.
iStatus = $cPropMaterial_SetMPIsotropic(pPropMaterial, 'CONC', dE,
dU, dA, dTemp, iRet)
!define rectangular frame section property
iStatus = $cSapModel_GetPropFrame(pSapModel, pPropFrame)
dT3 = 12.
dT2 = 12.
iColor = -1
cNotes = ''
cGUID = ''
iStatus = $cPropFrame_SetRectangle(pPropFrame, 'R1', 'CONC', dT3,
dT2, iColor, cNotes, cGUID, iRet)
!define frame section property modifiers
saBounds%lbound = 0
saBounds%extent = 8
pModValueSA = SafeArrayCreate(VT_R8, nDimCON, saBounds)
dModValue = 1.
do iCol = 0, 7
iRet = SafeArrayPutElement(pModValueSA, iCol, loc(dModValue))
end do
dModValue = 1000.
iRet = SafeArrayPutElement(pModValueSA, 0, loc(dModValue))
dModValue = 0.
iRet = SafeArrayPutElement(pModValueSA, 1, loc(dModValue))


iRet = SafeArrayPutElement(pModValueSA, 2, loc(dModValue))
iStatus = $cPropFrame_SetModifiers(pPropFrame, 'R1', pModValueSA,
iRet)
iRet = SafeArrayDestroy(pModValueSA)
!switch to k-ft units
iStatus = $cSapModel_SetPresentUnits(pSapModel, eUnits_kip_ft_F,
iRet)
!add frame object by coordinates
cCsys = 'Global'
dXi = 0.; dYi = 0.; dZi = 0.; dXj = 0.; dYj = 0.; dZj = 10.
iStatus = $cSapModel_GetFrameObj(pSapModel, pFrameObj)
iStatus = $cFrameObj_AddByCoord(pFrameObj, dXi, dYi, dZi, dXj, dYj,
dZj, cFrameName(1), 'R1', '1', cCsys, iRet)
dXi = 0.; dYi = 0.; dZi = 10.; dXj = 8.; dYj = 0.; dZj = 16.
iStatus = $cFrameObj_AddByCoord(pFrameObj, dXi, dYi, dZi, dXj, dYj,
dZj, cFrameName(2), 'R1', '2', cCsys, iRet)
dXi = -4.; dYi = 0.; dZi = 10.; dXj = 0.; dYj = 0.; dZj = 10.
iStatus = $cFrameObj_AddByCoord(pFrameObj, dXi, dYi, dZi, dXj, dYj,
dZj, cFrameName(3), 'R1', '3', cCsys, iRet)
!assign point object restraint at base
saBounds%lbound = 0
saBounds%extent = 6
pRestraintSA = SafeArrayCreate(VT_BOOL, nDimCON, saBounds)
bRestrained = .true.
do iCol = 0, 3
iRet = SafeArrayPutElement(pRestraintSA, iCol, loc(bRestrained))
end do
bRestrained = .false.
do iCol = 4, 5
iRet = SafeArrayPutElement(pRestraintSA, iCol, loc(bRestrained))
end do


iStatus = $cFrameObj_GetPoints(pFrameObj, cFrameName(1), cPointName
(1), cPointName(2), iRet)
iStatus = $cSapModel_GetPointObj(pSapModel, pPointObj)
iItemType = eItemType_Objects
iStatus = $cPointObj_SetRestraint(pPointObj, cPointName(1),
pRestraintSA, iItemType, iRet)
!assign point object restraint at top
bRestrained = .true.
do iCol = 0, 1
iRet = SafeArrayPutElement(pRestraintSA, iCol, loc(bRestrained))
end do
bRestrained = .false.
do iCol = 2, 5
iRet = SafeArrayPutElement(pRestraintSA, iCol, loc(bRestrained))
end do
iStatus = $cFrameObj_GetPoints(pFrameObj, cFrameName(2), cPointName
(1), cPointName(2), iRet)
iItemType = eItemType_Objects
iStatus = $cPointObj_SetRestraint(pPointObj, cPointName(2),
pRestraintSA, iItemType, iRet)
iRet = SafeArrayDestroy(pRestraintSA)
!refresh view, update (initialize) zoom
iStatus = $cSapModel_GetView(pSapModel, pView)
bZoom = .false.
iWindow = 0
iStatus = $cView_RefreshView(pView, iWindow, bZoom, iRet)
!add load patterns
iStatus = $cSapModel_GetLoadPatterns(pSapModel, pLoadPatterns)
iTypleLoadPat = eLoadPatternType_Other
dSelfWTMultiplier = 1.


bAddLoadCase = .true.
iStatus = $cLoadPatterns_Add(pLoadPatterns, '1', iTypleLoadPat,
dSelfWTMultiplier, bAddLoadCase, iRet)
dSelfWTMultiplier = 0.
iStatus = $cLoadPatterns_Add(pLoadPatterns, '2', iTypleLoadPat,
dSelfWTMultiplier, bAddLoadCase, iRet)
iStatus = $cLoadPatterns_Add(pLoadPatterns, '3', iTypleLoadPat,
dSelfWTMultiplier, bAddLoadCase, iRet)
iStatus = $cLoadPatterns_Add(pLoadPatterns, '4', iTypleLoadPat,
dSelfWTMultiplier, bAddLoadCase, iRet)
iStatus = $cLoadPatterns_Add(pLoadPatterns, '5', iTypleLoadPat,
dSelfWTMultiplier, bAddLoadCase, iRet)
iStatus = $cLoadPatterns_Add(pLoadPatterns, '6', iTypleLoadPat,
dSelfWTMultiplier, bAddLoadCase, iRet)
iStatus = $cLoadPatterns_Add(pLoadPatterns, '7', iTypleLoadPat,
dSelfWTMultiplier, bAddLoadCase, iRet)
!assign loading for load pattern 2
iStatus = $cSapModel_GetFrameObj(pSapModel, pFrameObj)
iStatus = $cFrameObj_GetPoints(pFrameObj, cFrameName(3), cPointName
(1), cPointName(2), iRet)
saBounds%lbound = 0
saBounds%extent = 6
pPointLoadValueSA = SafeArrayCreate(VT_R8, nDimCON, saBounds)
dModValue = 0.
do iCol = saBounds%lbound, saBounds%extent
iRet = SafeArrayPutElement(pPointLoadValueSA, iCol, loc
(dModValue))
end do
dModValue = -10.
iRet = SafeArrayPutElement(pPointLoadValueSA, 2, loc(dModValue))
bReplace = .false.
cCsys = 'Global'
iItemType = eItemType_Objects


iStatus = $cPointObj_SetLoadForce(pPointObj, cPointName(1), '2',
pPointLoadValueSA, bReplace, cCsys, iItemType, iRet)
iMyType = 1
iDir = 10
dDist1 = 0.
dDist2 = 1.
dVal1 = 1.8
dVal2 = 1.8
cCsys = 'Global'
bRelDist = .true.
bReplace = .true.
iItemType = eItemType_Objects
iStatus = $cFrameObj_SetLoadDistributed(pFrameObj, cFrameName(3),
'2', iMyType, iDir, dDist1, dDist2, dVal1, dVal2, cCsys, bRelDist,
bReplace, iItemType, iRet)
!assign loading for load pattern 3
iStatus = $cFrameObj_GetPoints(pFrameObj, cFrameName(3), cPointName
(1), cPointName(2), iRet)
dModValue = 0.
do iCol = saBounds%lbound, saBounds%extent
iRet = SafeArrayPutElement(pPointLoadValueSA, iCol, loc
(dModValue))
end do
dModValue = -17.2
iRet = SafeArrayPutElement(pPointLoadValueSA, 2, loc(dModValue))
dModValue = -54.4
iRet = SafeArrayPutElement(pPointLoadValueSA, 4, loc(dModValue))
bReplace = .false.
cCsys = 'Global'
iItemType = eItemType_Objects


iStatus = $cPointObj_SetLoadForce(pPointObj, cPointName(2), '3',
pPointLoadValueSA, bReplace, cCsys, iItemType, iRet)
iRet = SafeArrayDestroy(pPointLoadValueSA)
!assign loading for load pattern 4
iMyType = 1
iDir = 11
dDist1 = 0.
dDist2 = 1.
dVal1 = 2.
dVal2 = 2.
cCsys = 'Global'
bRelDist = .true.
bReplace = .true.
iItemType = eItemType_Objects
iStatus = $cFrameObj_SetLoadDistributed(pFrameObj, cFrameName(2),
'4', iMyType, iDir, dDist1, dDist2, dVal1, dVal2, cCsys, bRelDist,
bReplace, iItemType, iRet)
!assign loading for load pattern 5
iMyType = 1
iDir = 2
dDist1 = 0.
dDist2 = 1.
dVal1 = 2.
dVal2 = 2.
cCsys = 'Local'
bRelDist = .true.
bReplace = .true.
iItemType = eItemType_Objects
iStatus = $cFrameObj_SetLoadDistributed(pFrameObj, cFrameName(1),
'5', iMyType, iDir, dDist1, dDist2, dVal1, dVal2, cCsys, bRelDist,
bReplace, iItemType, iRet)


dVal1 = -2.
dVal2 = -2.
iStatus = $cFrameObj_SetLoadDistributed(pFrameObj, cFrameName(2),
'5', iMyType, iDir, dDist1, dDist2, dVal1, dVal2, cCsys, bRelDist,
bReplace, iItemType, iRet)
!assign loading for load pattern 6
iMyType = 1
iDir = 2
dDist1 = 0.
dDist2 = 1.
dVal1 = 0.9984
dVal2 = 0.3744
cCsys = 'Local'
bRelDist = .true.
bReplace = .true.
iItemType = eItemType_Objects
iStatus = $cFrameObj_SetLoadDistributed(pFrameObj, cFrameName(1),
'6', iMyType, iDir, dDist1, dDist2, dVal1, dVal2, cCsys, bRelDist,
bReplace, iItemType, iRet)
dVal1 = -0.3744
dVal2 = 0.
iStatus = $cFrameObj_SetLoadDistributed(pFrameObj, cFrameName(2),
'6', iMyType, iDir, dDist1, dDist2, dVal1, dVal2, cCsys, bRelDist,
bReplace, iItemType, iRet)
!assign loading for load pattern 7
iMyType = 1
iDir = 2
dDist1 = 0.5
dVal1 = -15.
cCsys = 'Local'
bRelDist = .true.


bReplace = .true.
iItemType = eItemType_Objects
iStatus = $cFrameObj_SetLoadPoint(pFrameObj, cFrameName(2), '7',
iMyType, iDir, dDist1, dVal1, cCsys, bRelDist, bReplace, iItemType,
iRet)
!switch to k-in units
iStatus = $cSapModel_SetPresentUnits(pSapModel, eUnits_kip_in_F,
iRet)
!save model
iStatus = $cFile_Save(pFile, cModelPath, iRet)
!run model (this will create the analysis model)
iStatus = $cSapModel_GetAnalyze(pSapModel, pAnalyze)
iStatus = $cAnalyze_RunAnalysis(pAnalyze, iRet)
!initialize for SAP2000 results
iStatus = $cFrameObj_GetPoints(pFrameObj, cFrameName(2), cPointName
(1), cPointName(2), iRet)
!get SAP2000 results for load patterns 1 through 7
saBounds%lbound = 0
saBounds%extent = 0
pObjSA = SafeArrayCreate(VT_BSTR, nDimCON, saBounds)
pElmSA = SafeArrayCreate(VT_BSTR, nDimCON, saBounds)
pLCaseSA = SafeArrayCreate(VT_BSTR, nDimCON, saBounds)
pStepTypeSA = SafeArrayCreate(VT_BSTR, nDimCON, saBounds)
pStepNumSA = SafeArrayCreate(VT_R8, nDimCON, saBounds)
pU1SA = SafeArrayCreate(VT_R8, nDimCON, saBounds)
pU2SA = SafeArrayCreate(VT_R8, nDimCON, saBounds)
pU3SA = SafeArrayCreate(VT_R8, nDimCON, saBounds)
pR1SA = SafeArrayCreate(VT_R8, nDimCON, saBounds)
pR2SA = SafeArrayCreate(VT_R8, nDimCON, saBounds)
pR3SA = SafeArrayCreate(VT_R8, nDimCON, saBounds)


dSapResultsRA1(:) = 0.
iItemType = eItemTypeElm_ObjectElm
bSelected = .true.
iStatus = $cSapModel_GetResults(pSapModel, pAnalysisResults)
do iCol = 0, 6
iStatus = $cAnalysisResults_GetSetup(pAnalysisResults,
pAnalysisResultsSetup)
write (cLoadPat, '(I1)') iCol+1
iStatus =
$cAnalysisResultsSetup_DeselectAllCasesAndCombosForOutput
(pAnalysisResultsSetup, iRet)
iStatus = $cAnalysisResultsSetup_SetCaseSelectedForOutput
(pAnalysisResultsSetup, cLoadPat, bSelected, iRet)
if (iCol <= 3) then
iStatus = $cAnalysisResults_JointDispl(pAnalysisResults,
cPointName(2), iItemType, iNumberResults, pObjSA, pElmSA, pLCaseSA,
pStepTypeSA, pStepNumSA, pU1SA, pU2SA, pU3SA, pR1SA, pR2SA, pR3SA,
iRet)
iRet = SafeArrayGetElement(pU3SA, 0, loc(dModValue))
else
iStatus = $cAnalysisResults_JointDispl(pAnalysisResults,
cPointName(1), iItemType, iNumberResults, pObjSA, pElmSA, pLCaseSA,
pStepTypeSA, pStepNumSA, pU1SA, pU2SA, pU3SA, pR1SA, pR2SA, pR3SA,
iRet)
iRet = SafeArrayGetElement(pU1SA, 0, loc(dModValue))
end if
dSapResultsRA1(iCol+1) = dModValue
end do
!close SAP2000 application
bFileSave = .false.
iStatus = $cOAPI_ApplicationExit(pSapObject, bFileSave, iRet)
!release SAP2000 object
iStatus = cOMReleaseObject(pSapObject)


!uninitialize COM
call COMUninitialize()
!deallocate SafeArrays
iRet = SafeArrayDestroy(pObjSA)
iRet = SafeArrayDestroy(pElmSA)
iRet = SafeArrayDestroy(pLCaseSA)
iRet = SafeArrayDestroy(pStepTypeSA)
iRet = SafeArrayDestroy(pStepNumSA)
iRet = SafeArrayDestroy(pU1SA)
iRet = SafeArrayDestroy(pU3SA)
iRet = SafeArrayDestroy(pR1SA)
iRet = SafeArrayDestroy(pR2SA)
iRet = SafeArrayDestroy(pR3SA)
!fill independent results
dIndResultsRA1(1) = -0.02639
dIndResultsRA1(2) = 0.06296
dIndResultsRA1(3) = 0.06296
dIndResultsRA1(4) = -0.29630
dIndResultsRA1(5) = 0.31250
dIndResultsRA1(6) = 0.11556
dIndResultsRA1(7) = 0.00651
!display results
print *, 'LC Sap2000 Independent %Diff'
print *, '-- -------- ----------- -----'
do iCol = 1, 7
print 1, iCol, dSapResultsRA1(iCol), dIndResultsRA1(iCol),
(dSapResultsRA1(iCol) / dIndResultsRA1(iCol)) - 1.
end do
1 format ( i3, f10.5, f13.5, f7.2)


```
pause
end program APIExample
```
## Release Notes

Initial release in version 15.0.1.
Updated for vesion 26.0.0.

# Example 5 (Microsoft Visual C++ 2022)

## Remarks

This example is written for Microsoft Visual C++ 2022. It is based on the SAP2000 verification
problem Example 1-001.
This example creates the example verification problem from scratch, runs the analysis, extracts
results, and compares the results with hand calculated values.

## Example

1. Create a Visual C++ project of type "Console App”.
2. Locate SAP2000v1.tlb
    With the release of SAP2000 v26.0.0 , users will need to select the TLB file that
    corresponds to the bitness of their API client, e.g. 32-bit or 64-bit. To locate these files,
    the user should navigate to the directory where SAP2000 is installed. This is typically
    C:\Program Files\Computers and Structures\SAP2000 26\
Within this directory, the 32-bit library is found at NativeAPI\x86\ SAP2000v1.tlb The 64
-bit library is found at NativeAPI\x64\ SAP2000v1.tlb.
Copy the 64-bit SAP2000v1.tlb file from the installation folder to the project directory. It
should be copied to the same level as your client application’s project file.
3. Open the .cpp file generated by the wizard by double-clithe following code. Please pay attention to the commentcking on it and paste in s in this code block, they
    contain important information about running the script.
#define _CRT_SECURE_NO_WARNINGS
#include <atlbase.h>
#include <atlstr.h>
#include <atlsafe.h>
#include <iostream>
#include <iomanip>


#include <sstream>
using namespace std;
#import "SAP2000v1.tlb" no_dual_interfaces rename("GetObject", "GetObject_") rename
("Yield", "Yield_") rename("GetProp", "GetProp_") rename("SetProp", "SetProp_")
bool CheckHRESULT(HRESULT hRes, const wchar_t* msg)
{
if (hRes == S_FALSE || FAILED(hRes)) {
MessageBox(0, msg, L"ERROR!", MB_SETFOREGROUND);
return (false);
}
return (true);
}
int main(int argc, char* argv[])
{
::SetConsoleOutputCP(CP_UTF8);
// set the following flag to true to attach to an existing instance of the program
// otherwise a new instance of the program will be started
bool bAttachToInstance = false;
// set the following flag to true to manually specify the path to SAP2000.exe
// this allows for a connection to a version of SAP2000 other than the latest installation
// otherwise the latest installed version of SAP2000 will be launched
bool bSpecifyPath = false;
// if the above flag is set to true, specify the path to SAP2000 below
std::wstring ProgramPath;
ProgramPath = L"C:\\Program Files\\Computers and Structures\\SAP2000 26\\SAP2000.exe";
// use res to check if functions return successfully (res = 0) or fail (res = nonzero)
HRESULT hRes = 0;
int res = 0;
// initialize COM


hRes = CoInitialize(NULL);
if (!CheckHRESULT(hRes, L"Error initializing COM subsystem!")) return (hRes);
// SapObject pointer
CComPtr<SAP2000v1::cOAPI> pSapObject;
try {
// create Helper
CComPtr<SAP2000v1::cHelper> pHelper;
hRes = pHelper.CoCreateInstance(L"SAP2000v1.Helper", NULL,
CLSCTX_INPROC_SERVER);
if (!CheckHRESULT(hRes, L"Cannot instantiate helper!")) return (hRes);
if (bAttachToInstance) {
// attach to a running instance of SAP2000
pSapObject = pHelper->GetObject_(L"CSI.SAP2000.API.SapObject");
hRes = ((pSapObject)? S_OK : S_FALSE);
if (!CheckHRESULT(hRes, L"Cannot attach to SapObject!")) return (hRes);
}
else {
// start a new instance of SAP2000
if (bSpecifyPath) {
// create an instance of the SAP2000 object from the specified path
pSapObject = pHelper->CreateObject(ProgramPath.c_str());
hRes = ((pSapObject)? S_OK : S_FALSE);
if (!CheckHRESULT(hRes, L"Cannot instantiate SapObject!")) return (hRes);
}
else {
// create an instance of the SapObject from the latest installed SAP2000
pSapObject = pHelper->CreateObjectProgID(L"CSI.SAP2000.API.SapObject");
hRes = ((pSapObject)? S_OK : S_FALSE);
if (!CheckHRESULT(hRes, L"Cannot instantiate SapObject!")) return (hRes);


### }

// start SAP2000 application
res = pSapObject->ApplicationStart(SAP2000v1::eUnits_kip_in_F, true, "");
if (!CheckHRESULT(hRes, L"SapObject.ApplicationStart failed!")) return (hRes);
}
// full path to the model
// set it to an already existing folder
const wchar_t* ModelPath = L"C:\\CSiAPIexample\\API_1-001.sdb";
// initialize model
res = pSapObject->SapModel->InitializeNewModel(SAP2000v1::eUnits_kip_in_F);
// create new blank model
res = pSapObject->SapModel->File->NewBlank();
// define material property
_bstr_t bstrPropMaterial = "CONC";
res = pSapObject->SapModel->PropMaterial->SetMaterial(bstrPropMaterial,
SAP2000v1::eMatType_Concrete, -1, L"", L"");
// assign isotropic mechanical properties to material
res = pSapObject->SapModel->PropMaterial->SetMPIsotropic(bstrPropMaterial, 3600, 0.2,
0.0000055, 0.0);
// define rectangular frame section property
_bstr_t bstrPropFrame("R1");
res = pSapObject->SapModel->PropFrame->SetRectangle(bstrPropFrame, bstrPropMaterial, 12,
12, -1, L"", L"");
// define frame section property modifiers
CComSafeArray<double> saMod(8); // CComSafeArray is a wrapper for the SAFEARRAY
structure.
for (int i = 0; i < 8; i++)
saMod[i] = 1.;
saMod[0] = 1000.;
saMod[1] = 0.;


saMod[2] = 0.;
LPSAFEARRAY psaMod = saMod.Detach();
res = pSapObject->SapModel->PropFrame->SetModifiers(bstrPropFrame, &psaMod);
saMod.Attach(psaMod);
// switch to k-ft units
res = pSapObject->SapModel->SetPresentUnits(SAP2000v1::eUnits_kip_ft_F);
// add frame object by coordinates
BSTR name1 = ::SysAllocString(L"");
BSTR name2 = ::SysAllocString(L"");
BSTR name3 = ::SysAllocString(L"");
_bstr_t FrameName0("1");
_bstr_t FrameName1("2");
_bstr_t FrameName2("3");
_bstr_t bstrCoordSys("Global");
res = pSapObject->SapModel->FrameObj->AddByCoord(0, 0, 0, 0, 0, 10, &name1,
bstrPropFrame, FrameName0, bstrCoordSys);
res = pSapObject->SapModel->FrameObj->AddByCoord(0, 0, 10, 8, 0, 16, &name2,
bstrPropFrame, FrameName1, bstrCoordSys);
res = pSapObject->SapModel->FrameObj->AddByCoord(-4, 0, 10, 0, 0, 10, &name3,
bstrPropFrame, FrameName2, bstrCoordSys);
// assign point object restraint at base
BSTR PointName;
BSTR PointName0 = ::SysAllocString(L"");
BSTR PointName1 = ::SysAllocString(L"");
CComSafeArray<VARIANT_BOOL, VT_BOOL> saRest(6);
for (int i = 0; i < 4; i++)
saRest[i] = VARIANT_TRUE;
for (int i = 4; i < 6; i++)
saRest[i] = VARIANT_FALSE;


res = pSapObject->SapModel->FrameObj->GetPoints(FrameName0, &PointName0,
&PointName1);
LPSAFEARRAY psaRest = saRest.Detach();
res = pSapObject->SapModel->PointObj->SetRestraint(PointName0, &psaRest,
SAP2000v1::eItemType_Objects);
saRest.Attach(psaRest);
// assign point object restraint at top
for (int i = 0; i < 2; i++)
saRest[i] = VARIANT_TRUE;
for (int i = 2; i < 6; i++)
saRest[i] = VARIANT_FALSE;
res = pSapObject->SapModel->FrameObj->GetPoints(FrameName1, &PointName0,
&PointName1);
psaRest = saRest.Detach();
res = pSapObject->SapModel->PointObj->SetRestraint(PointName1, &psaRest,
SAP2000v1::eItemType_Objects);
saRest.Attach(psaRest);
// refresh view, update (initialize) zoom
long window = 0;
VARIANT_BOOL zoom = VARIANT_FALSE;
res = pSapObject->SapModel->View->RefreshView(window, zoom);
// add load patterns
double SelfWTMultiplier = 1.0;
VARIANT_BOOL AddLoadCase = VARIANT_TRUE;
res = pSapObject->SapModel->LoadPatterns->Add("1", SAP2000v1::eLoadPatternType_Other,
SelfWTMultiplier, AddLoadCase);
SelfWTMultiplier = 0.;
res = pSapObject->SapModel->LoadPatterns->Add("2", SAP2000v1::eLoadPatternType_Other,
SelfWTMultiplier, AddLoadCase);
res = pSapObject->SapModel->LoadPatterns->Add("3", SAP2000v1::eLoadPatternType_Other,
SelfWTMultiplier, AddLoadCase);


res = pSapObject->SapModel->LoadPatterns->Add("4", SAP2000v1::eLoadPatternType_Other,
SelfWTMultiplier, AddLoadCase);
res = pSapObject->SapModel->LoadPatterns->Add("5", SAP2000v1::eLoadPatternType_Other,
SelfWTMultiplier, AddLoadCase);
res = pSapObject->SapModel->LoadPatterns->Add("6", SAP2000v1::eLoadPatternType_Other,
SelfWTMultiplier, AddLoadCase);
res = pSapObject->SapModel->LoadPatterns->Add("7", SAP2000v1::eLoadPatternType_Other,
SelfWTMultiplier, AddLoadCase);
// assign loading for load pattern 2
res = pSapObject->SapModel->FrameObj->GetPoints(FrameName2, &PointName0,
&PointName1);
CComSafeArray<double> saPLoad(6);
for (int i = 0; i < 6; i++)
saPLoad[i] = 0.;
saPLoad[2] = -10.;
bstrCoordSys = L"Global";
LPSAFEARRAY psaPLoad = saPLoad.Detach();
res = pSapObject->SapModel->PointObj->SetLoadForce(PointName0, "2", &psaPLoad,
VARIANT_FALSE, bstrCoordSys, SAP2000v1::eItemType_Objects);
saPLoad.Attach(psaPLoad);
res = pSapObject->SapModel->FrameObj->SetLoadDistributed(FrameName2, "2", 1, 10, 0., 1.,
1.8, 1.8, bstrCoordSys, VARIANT_TRUE, VARIANT_TRUE, SAP2000v1::eItemType_Objects);
// assign loading for load pattern 3
res = pSapObject->SapModel->FrameObj->GetPoints(FrameName2, &PointName0,
&PointName1);
for (int i = 0; i < 6; i++)
saPLoad[i] = 0.;
saPLoad[2] = -17.2;
saPLoad[4] = -54.4;
psaPLoad = saPLoad.Detach();
res = pSapObject->SapModel->PointObj->SetLoadForce(PointName1, "3", &psaPLoad,
VARIANT_FALSE, bstrCoordSys, SAP2000v1::eItemType_Objects);
saPLoad.Attach(psaPLoad);


// assign loading for load pattern 4
res = pSapObject->SapModel->FrameObj->SetLoadDistributed(FrameName1, "4", 1, 10, 0, 1,
1.8, 1.8, bstrCoordSys, VARIANT_TRUE, VARIANT_TRUE, SAP2000v1::eItemType_Objects);
// assign loading for load pattern 5
bstrCoordSys = L"Local";
res = pSapObject->SapModel->FrameObj->SetLoadDistributed(FrameName0, "5", 1, 2, 0, 1, 2, 2,
bstrCoordSys, VARIANT_TRUE, VARIANT_TRUE, SAP2000v1::eItemType_Objects);
res = pSapObject->SapModel->FrameObj->SetLoadDistributed(FrameName1, "5", 1, 2, 0, 1, -2, -
2, bstrCoordSys, VARIANT_TRUE, VARIANT_TRUE, SAP2000v1::eItemType_Objects);
// assign loading for load pattern 6
res = pSapObject->SapModel->FrameObj->SetLoadDistributed(FrameName0, "6", 1, 2, 0, 1,
0.9984, 0.3744, bstrCoordSys, VARIANT_TRUE, VARIANT_TRUE,
SAP2000v1::eItemType_Objects);
res = pSapObject->SapModel->FrameObj->SetLoadDistributed(FrameName1, "6", 1, 2, 0, 1, -
0.3744, 0, bstrCoordSys, VARIANT_TRUE, VARIANT_TRUE,
SAP2000v1::eItemType_Objects);
// assign loading for load pattern 7
res = pSapObject->SapModel->FrameObj->SetLoadPoint(FrameName1, "7", 1, 2, 0.5, -15,
bstrCoordSys, VARIANT_TRUE, VARIANT_TRUE, SAP2000v1::eItemType_Objects);
// switch to k-in units
res = pSapObject->SapModel->SetPresentUnits(SAP2000v1::eUnits_kip_in_F);
// save model
_bstr_t bstrFileName(ModelPath);
res = pSapObject->SapModel->File->Save(bstrFileName);
// run model (this will create the analysis model)
res = pSapObject->SapModel->Analyze->RunAnalysis();
// initialize for SAP2000 results
long NumberResults = 0;
double SapResult[7];
for (int i = 0; i < 7; i++)
SapResult[i] = 0.;
CComSafeArray<BSTR> saResObj(1);


CComSafeArray<BSTR> saResElm(1);
CComSafeArray<BSTR> saResLoadCase(1);
CComSafeArray<BSTR> saResStepType(1);
CComSafeArray<double> saResStepNum(1);
CComSafeArray<double> saResU1(1);
CComSafeArray<double> saResU2(1);
CComSafeArray<double> saResU3(1);
CComSafeArray<double> saResR1(1);
CComSafeArray<double> saResR2(1);
CComSafeArray<double> saResR3(1);
res = pSapObject->SapModel->FrameObj->GetPoints(FrameName1, &PointName0,
&PointName1);
// get SAP2000 results for load cases 1 through 7
for (int i = 0; i < 7; i++) {
res = pSapObject->SapModel->Results->Setup->DeselectAllCasesAndCombosForOutput();
_bstr_t bstrLoadPattern = std::to_string(i + 1).c_str();
res = pSapObject->SapModel->Results->Setup->SetCaseSelectedForOutput(bstrLoadPattern,
VARIANT_TRUE);
PointName = (i <= 3)? PointName1 : PointName0;
// result arrays get reallocated inside the response call so we have to detach first
LPSAFEARRAY psaResObj = saResObj.Detach();
LPSAFEARRAY psaResElm = saResElm.Detach();
LPSAFEARRAY psaResLoadCase = saResLoadCase.Detach();
LPSAFEARRAY psaResStepType = saResStepType.Detach();
LPSAFEARRAY psaResStepNum = saResStepNum.Detach();
LPSAFEARRAY psaResU1 = saResU1.Detach();
LPSAFEARRAY psaResU2 = saResU2.Detach();
LPSAFEARRAY psaResU3 = saResU3.Detach();
LPSAFEARRAY psaResR1 = saResR1.Detach();


LPSAFEARRAY psaResR2 = saResR2.Detach();
LPSAFEARRAY psaResR3 = saResR3.Detach();
res = pSapObject->SapModel->Results->JointDispl(PointName,
SAP2000v1::eItemTypeElm_ObjectElm, &NumberResults,
&psaResObj, &psaResElm, &psaResLoadCase, &psaResStepType, &psaResStepNum,
&psaResU1, &psaResU2, &psaResU3, &psaResR1, &psaResR2, &psaResR3);
//re-attach to the result arrays
saResObj.Attach(psaResObj);
saResElm.Attach(psaResElm);
saResLoadCase.Attach(psaResLoadCase);
saResStepType.Attach(psaResStepType);
saResStepNum.Attach(psaResStepNum);
saResU1.Attach(psaResU1);
saResU2.Attach(psaResU2);
saResU3.Attach(psaResU3);
saResR1.Attach(psaResR1);
saResR2.Attach(psaResR2);
saResR3.Attach(psaResR3);
if (i <= 3)
SapResult[i] = saResU3[0];
else
SapResult[i] = saResU1[0];
}
// close SAP2000 application
res = pSapObject->ApplicationExit(VARIANT_FALSE);
// fill independent results (hand calculated)
double IndResult[7];
IndResult[0] = -0.02639;
IndResult[1] = 0.06296;


IndResult[2] = 0.06296;
IndResult[3] = -0.2963;
IndResult[4] = 0.3125;
IndResult[5] = 0.11556;
IndResult[6] = 0.00651;
// fill percent difference
double PercentDiff[7];
for (int i = 0; i < 7; i++)
PercentDiff[i] = fabs((SapResult[i] / IndResult[i]) - 1);
// print results
stringstream sMsg;
sMsg << fixed << setfill(' ');
sMsg << "LC Sap2000 Independent % Diff" << endl;
for (int i = 0; i < 7; i++)
sMsg << setprecision(5) << showpoint << setiosflags(ios::left)
<< setw(2) << i + 1 << " "
<< setw(11) << IndResult[i] << " "
<< setw(11) << SapResult[i] << " "
<< setprecision(0) << noshowpoint << setiosflags(ios::right)
<< setw(5) << PercentDiff[i] << '%' << endl;
MessageBoxA(0, sMsg.str().c_str(), " Results", MB_SETFOREGROUND);
// uninitialize COM
CoUninitialize();
// we're done!
return (EXIT_SUCCESS);
}
catch (_com_error& ex) {
CheckHRESULT(ex.Error(), ex.ErrorMessage());


// close SAP2000
CComVariant vRes = pSapObject->ApplicationExit(false);
// uninitialize COM
CoUninitialize();
return (-1);
}
}

## Release Notes

Initial release in version 15.0.1
Updated in version 22.1.0.
Updated for version 26.0.0.

# Example 6 (MATLAB)

## Remarks

This example was created and tested using MATLAB R2024a. It is based on the SAP2000
verification problem Example 1-001.
This example creates the example verification problem from scratch, runs the analysis,
extracts results, and compares the results with hand calculated values.
IMPORTANT NOTE: With the release of SAP2000 v26.0.0, the API is now implemented
as a .NET Standard 2.0 library. Due to this change, MATLAB can now use either
the .NET Core or the .NET Framework run-time environment when running API scripts.
Changing the .NET run-time environment affects all open MATLAB sessions and can
only be reset by restarting MATLAB.
This example activates the .NET Core run-time environment but can easily be modified to
use .NET Framework run-time environment. See comments for details.

## Example

1. Create a MATLAB .m file and paste in the following code. Please pay attention to the
    comments in this code block, they contain important information about running the script.
%% clean-up the workspace & command window
clear;
clc;


%% set the following flag to true to select the .NET Core run-time environment,
%% false to select .NET Framework run-time environment.
%% Changing the .NET run-time environment affects all open MATLAB sessions
%% and can only be reset by restarting MATLAB.
UseNETCore = true(); % false(); %
%% select the .NET Core run-time environment
if UseNETCore
ne = dotnetenv("core")
else
ne = dotnetenv("framework")
end
%%set the following flag to true to attach to an existing instance of the program otherwise a new
instance of the program will be started
AttachToInstance = false(); % true(); %
%% set the following flag to true to manually specify the path to SAP2000.exe
%% this allows for a connection to a version of SAP2000 other than the latest installation
%% otherwise the latest installed version of SAP2000 will be launched
SpecifyPath = false(); % true(); %
%% if the above flag is set to true, specify the path to SAP2000 below
ProgramPath = 'C:\Program Files\Computers and Structures\SAP2000 26\SAP2000.exe';
%% full path to API dll
%% set it to the installation folder
APIDLLPath = 'C:\Program Files\Computers and Structures\SAP2000 26\SAP2000v1.dll';
%% full path to the model
%% set it to the desired path of your model
ModelDirectory = 'C:\CSiAPIExample';
if ~exist(ModelDirectory, 'dir')
mkdir(ModelDirectory);
end


ModelName = 'API_1-001.sdb';
ModelPath = strcat(ModelDirectory, filesep, ModelName);
%% create API helper object
a = NET.addAssembly(APIDLLPath);
helper = SAP2000v1.Helper;
helper = NET.explicitCast(helper,'SAP2000v1.cHelper');
if AttachToInstance
%% attach to a running instance of SAP2000
SapObject = helper.GetObject('CSI.SAP2000.API.SapObject');
SapObject = NET.explicitCast(SapObject,'SAP2000v1.cOAPI');
else
if SpecifyPath
%% create an instance of the SapObject from the specified path
SapObject = helper.CreateObject(ProgramPath);
else
%% create an instance of the SapObject from the latest installed SAP2000
SapObject = helper.CreateObjectProgID('CSI.SAP2000.API.SapObject');
end
SapObject = NET.explicitCast(SapObject,'SAP2000v1.cOAPI');
%% start SAP2000 application
SapObject.ApplicationStart;
end
helper = 0;
%% create SapModel object
SapModel = NET.explicitCast(SapObject.SapModel,'SAP2000v1.cSapModel');
%% initialize model
ret = SapModel.InitializeNewModel;
%% create new blank model


File = NET.explicitCast(SapModel.File,'SAP2000v1.cFile');
ret = File.NewBlank;
%% define material property
PropMaterial = NET.explicitCast(SapModel.PropMaterial,'SAP2000v1.cPropMaterial');
ret = PropMaterial.SetMaterial('CONC', SAP2000v1.eMatType.Concrete);
%% assign isotropic mechanical properties to material
ret = PropMaterial.SetMPIsotropic('CONC', 3600, 0.2, 0.0000055);
%% define rectangular frame section property
PropFrame = NET.explicitCast(SapModel.PropFrame,'SAP2000v1.cPropFrame');
ret = PropFrame.SetRectangle('R1', 'CONC', 12, 12);
%% define frame section property modifiers
ModValue = NET.createArray('System.Double',8);
for i = 1 : 8
ModValue(i) = 1;
end
ModValue(1) = 1000;
ModValue(2) = 0;
ModValue(3) = 0;
ret = PropFrame.SetModifiers('R1', ModValue);
%% switch to k-ft units
ret = SapModel.SetPresentUnits(SAP2000v1.eUnits.kip_ft_F);
%% add frame object by coordinates
FrameObj = NET.explicitCast(SapModel.FrameObj,'SAP2000v1.cFrameObj');
FrameName1 = System.String(' ');
FrameName2 = System.String(' ');
FrameName3 = System.String(' ');
[ret, FrameName1] = FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, FrameName1, 'R1', '1', 'Global');
[ret, FrameName2] = FrameObj.AddByCoord(0, 0, 10, 8, 0, 16, FrameName2, 'R1', '2', 'Global');


[ret, FrameName3] = FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10, FrameName3, 'R1', '3', 'Global');
%% assign point object restraint at base
PointObj = NET.explicitCast(SapModel.PointObj,'SAP2000v1.cPointObj');
PointName1 = System.String(' ');
PointName2 = System.String(' ');
Restraint = NET.createArray('System.Boolean',6);
for i = 1 : 4
Restraint(i) = true();
end
for i = 5 : 6
Restraint(i) = false();
end
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName1, PointName1, PointName2);
ret = PointObj.SetRestraint(PointName1, Restraint);
%% assign point object restraint at top
for i = 1 : 2
Restraint(i) = true();
end
for i = 3 : 6
Restraint(i) = false();
end
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName2, PointName1, PointName2);
ret = PointObj.SetRestraint(PointName2, Restraint);
%% refresh view, update (initialize) zoom
View = NET.explicitCast(SapModel.View,'SAP2000v1.cView');
ret = View.RefreshView(0, false());
%% add load patterns
LoadPatterns = NET.explicitCast(SapModel.LoadPatterns,'SAP2000v1.cLoadPatterns');


ret = LoadPatterns.Add('1', SAP2000v1.eLoadPatternType.Other, 1, true());
ret = LoadPatterns.Add('2', SAP2000v1.eLoadPatternType.Other, 0, true());
ret = LoadPatterns.Add('3', SAP2000v1.eLoadPatternType.Other, 0, true());
ret = LoadPatterns.Add('4', SAP2000v1.eLoadPatternType.Other, 0, true());
ret = LoadPatterns.Add('5', SAP2000v1.eLoadPatternType.Other, 0, true());
ret = LoadPatterns.Add('6', SAP2000v1.eLoadPatternType.Other, 0, true());
ret = LoadPatterns.Add('7', SAP2000v1.eLoadPatternType.Other, 0, true());
%% assign loading for load pattern 2
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName3, PointName1, PointName2);
PointLoadValue = NET.createArray('System.Double',6);
for i = 1 : 6
PointLoadValue(i) = 0.0;
end
PointLoadValue(3) = -10;
ret = PointObj.SetLoadForce(PointName1, '2', PointLoadValue);
ret = FrameObj.SetLoadDistributed(FrameName3, '2', 1, 10, 0, 1, 1.8, 1.8);
%% assign loading for load pattern 3
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName3, PointName1, PointName2);
for i = 1 : 6
PointLoadValue(i) = 0.0;
end
PointLoadValue(3) = -17.2;
PointLoadValue(5) = -54.4;
ret = PointObj.SetLoadForce(PointName2, '3', PointLoadValue);
%% assign loading for load pattern 4
ret = FrameObj.SetLoadDistributed(FrameName2, '4', 1, 11, 0, 1, 2, 2);
%% assign loading for load pattern 5
ret = FrameObj.SetLoadDistributed(FrameName1, '5', 1, 2, 0, 1, 2, 2, 'Local');


ret = FrameObj.SetLoadDistributed(FrameName2, '5', 1, 2, 0, 1, -2, -2, 'Local');
%% assign loading for load pattern 6
ret = FrameObj.SetLoadDistributed(FrameName1, '6', 1, 2, 0, 1, 0.9984, 0.3744, 'Local');
ret = FrameObj.SetLoadDistributed(FrameName2, '6', 1, 2, 0, 1, -0.3744, 0, 'Local');
%% assign loading for load pattern 7
ret = FrameObj.SetLoadPoint(FrameName2, '7', 1, 2, 0.5, -15, 'Local');
%% switch to k-in units
ret = SapModel.SetPresentUnits(SAP2000v1.eUnits.kip_in_F);
%% save model
ret = File.Save(ModelPath);
%% run model (this will create the analysis model)
Analyze = NET.explicitCast(SapModel.Analyze,'SAP2000v1.cAnalyze');
ret = Analyze.RunAnalysis();
%% initialize for SAP2000 results
SAP2000Result = zeros(7,1,'double');
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName2, PointName1, PointName2);
%% get SAP2000 results for load cases 1 through 7
AnalysisResults = NET.explicitCast(SapModel.Results,'SAP2000v1.cAnalysisResults');
AnalysisResultsSetup = NET.explicitCast
(AnalysisResults.Setup,'SAP2000v1.cAnalysisResultsSetup');
for i = 1 : 7
NumberResults = 0;
Obj = NET.createArray('System.String',2);
Elm = NET.createArray('System.String',2);
ACase = NET.createArray('System.String',2);
StepType = NET.createArray('System.String',2);
StepNum = NET.createArray('System.Double',2);
U1 = NET.createArray('System.Double',2);
U2 = NET.createArray('System.Double',2);


U3 = NET.createArray('System.Double',2);
R1 = NET.createArray('System.Double',2);
R2 = NET.createArray('System.Double',2);
R3 = NET.createArray('System.Double',2);
ret = AnalysisResultsSetup.DeselectAllCasesAndCombosForOutput;
ret = AnalysisResultsSetup.SetCaseSelectedForOutput(int2str(i));
if i <= 4
[ret, NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2, R3] =
AnalysisResults.JointDispl(PointName2, SAP2000v1.eItemTypeElm.ObjectElm, NumberResults,
Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2, R3);
SAP2000Result(i) = U3(1);
else
[ret, NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2, R3] =
AnalysisResults.JointDispl(PointName1, SAP2000v1.eItemTypeElm.ObjectElm, NumberResults,
Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2, R3);
SAP2000Result(i) = U1(1);
end
end
%% close SAP2000
ret = SapObject.ApplicationExit(false());
File = 0;
PropMaterial = 0;
PropFrame = 0;
FrameObj = 0;
PointObj = 0;
View = 0;
LoadPatterns = 0;
Analyze = 0;
AnalysisResults = 0;
AnalysisResultsSetup = 0;


SapModel = 0;
SapObject = 0;
%% fill independent results
IndResult = zeros(7,1,'double');
IndResult(1) = -0.02639;
IndResult(2) = 0.06296;
IndResult(3) = 0.06296;
IndResult(4) = -0.2963;
IndResult(5) = 0.3125;
IndResult(6) = 0.11556;
IndResult(7) = 0.00651;
%% fill percent difference
PercentDiff = zeros(7,1,'double');
for i = 1 : 7
PercentDiff(i) = (SAP2000Result(i) / IndResult(i)) - 1;
end
%% display results
SAP2000Result
IndResult
PercentDiff

## Release Notes

Initial release in version 15.0.1
Updated for version 26.0.0.

# Example 7 (Python COM)

## Remarks

This example was created using Python 3.9.7. It is based on the SAP2000 verification problem
Example 1-001.


This example creates the example verification problem from scratch, runs the analysis, extracts
results, and compares the results with hand calculated values.

## Example

1. Download and install Python 3.9.7 or higher for Windows. Python is freely available at
https:\\python.org.
2. Install the Python package "comtypes". This example was created using comtypes version 1.4.1.
If you are using Python 3.4 or higher, the easiest way to install this package is by opening a
command prompt with administrative privileges and entering the command:
python -m pip install comtypes
Please note that your computer will need to be connected to the internet for the above command to
work.
3. Create a Python .py file using IDLE or any text editor and paste in the following code. Please
pay attention to the comments in this code block; they contain important information about
running the script.
    import os
    import sys
    import comtypes.client

```
#set the following flag to True to attach to an existing instance of the
program
#otherwise a new instance of the program will be started
AttachToInstance = False
#set the following flag to True to manually specify the path to
SAP2000.exe
#this allows for a connection to a version of SAP2000 other than the
latest installation
#otherwise the latest installed version of SAP2000 will be launched
SpecifyPath = False
#if the above flag is set to True, specify the path to SAP2000 below
ProgramPath = R'C:\Program Files\Computers and Structures\SAP2000 26
\SAP2000.exe'
#full path to the model
#set it to the desired path of your model
```

APIPath = R'C:\CSiAPIExample'
if not os.path.exists(APIPath):
try:
os.makedirs(APIPath)
except OSError:
pass
ModelPath = APIPath + os.sep + 'API_1-001.sdb'
#create API helper object
helper = comtypes.client.CreateObject('SAP2000v1.Helper')
helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)

if AttachToInstance:
#attach to a running instance of SAP2000
try:
#get the active SapObject
mySapObject = helper.GetObject("CSI.SAP2000.API.SapObject")
except (OSError, comtypes.COMError):
print("No running instance of the program found or failed to
attach.")
sys.exit(-1)
else:
if SpecifyPath:
try:
#'create an instance of the SAPObject from the specified path
mySapObject = helper.CreateObject(ProgramPath)
except (OSError, comtypes.COMError):
print("Cannot start a new instance of the program from " +
ProgramPath)
sys.exit(-1)


else:
try:
#create an instance of the SAPObject from the latest
installed SAP2000
mySapObject = helper.CreateObjectProgID
("CSI.SAP2000.API.SapObject")
except (OSError, comtypes.COMError):
print("Cannot start a new instance of the program.")
sys.exit(-1)
#start SAP2000 application
mySapObject.ApplicationStart()

#create SapModel object
SapModel = mySapObject.SapModel

#initialize model
SapModel.InitializeNewModel()

#create new blank model
ret = SapModel.File.NewBlank()

#define material property
MATERIAL_CONCRETE = 2
ret = SapModel.PropMaterial.SetMaterial('CONC', MATERIAL_CONCRETE)

#assign isotropic mechanical properties to material
ret = SapModel.PropMaterial.SetMPIsotropic('CONC', 3600, 0.2, 0.0000055)

#define rectangular frame section property


ret = SapModel.PropFrame.SetRectangle('R1', 'CONC', 12, 12)

#define frame section property modifiers
ModValue = [1000, 0, 0, 1, 1, 1, 1, 1]
ret = SapModel.PropFrame.SetModifiers('R1', ModValue)

#switch to k-ft units
kip_ft_F = 4
ret = SapModel.SetPresentUnits(kip_ft_F)

#add frame object by coordinates
FrameName1 = ' '
FrameName2 = ' '
FrameName3 = ' '
[FrameName1, ret] = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10,
FrameName1, 'R1', '1', 'Global')
[FrameName2, ret] = SapModel.FrameObj.AddByCoord(0, 0, 10, 8, 0, 16,
FrameName2, 'R1', '2', 'Global')
[FrameName3, ret] = SapModel.FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10,
FrameName3, 'R1', '3', 'Global')

#assign point object restraint at base
PointName1 = ' '
PointName2 = ' '
Restraint = [True, True, True, True, False, False]
[PointName1, PointName2, ret] = SapModel.FrameObj.GetPoints(FrameName1,
PointName1, PointName2)
ret = SapModel.PointObj.SetRestraint(PointName1, Restraint)

#assign point object restraint at top


Restraint = [True, True, False, False, False, False]
[PointName1, PointName2, ret] = SapModel.FrameObj.GetPoints(FrameName2,
PointName1, PointName2)
ret = SapModel.PointObj.SetRestraint(PointName2, Restraint)

#refresh view, update (initialize) zoom
ret = SapModel.View.RefreshView(0, False)

#add load patterns
LTYPE_OTHER = 8
ret = SapModel.LoadPatterns.Add('1', LTYPE_OTHER, 1, True)
ret = SapModel.LoadPatterns.Add('2', LTYPE_OTHER, 0, True)
ret = SapModel.LoadPatterns.Add('3', LTYPE_OTHER, 0, True)
ret = SapModel.LoadPatterns.Add('4', LTYPE_OTHER, 0, True)
ret = SapModel.LoadPatterns.Add('5', LTYPE_OTHER, 0, True)
ret = SapModel.LoadPatterns.Add('6', LTYPE_OTHER, 0, True)
ret = SapModel.LoadPatterns.Add('7', LTYPE_OTHER, 0, True)

#assign loading for load pattern 2
[PointName1, PointName2, ret] = SapModel.FrameObj.GetPoints(FrameName3,
PointName1, PointName2)
PointLoadValue = [0,0,-10,0,0,0]
ret = SapModel.PointObj.SetLoadForce(PointName1, '2', PointLoadValue)
ret = SapModel.FrameObj.SetLoadDistributed(FrameName3, '2', 1, 10, 0, 1,
1.8, 1.8)

#assign loading for load pattern 3
[PointName1, PointName2, ret] = SapModel.FrameObj.GetPoints(FrameName3,
PointName1, PointName2)
PointLoadValue = [0,0,-17.2,0,-54.4,0]


ret = SapModel.PointObj.SetLoadForce(PointName2, '3', PointLoadValue)

#assign loading for load pattern 4
ret = SapModel.FrameObj.SetLoadDistributed(FrameName2, '4', 1, 11, 0, 1,
2, 2)

#assign loading for load pattern 5
ret = SapModel.FrameObj.SetLoadDistributed(FrameName1, '5', 1, 2, 0, 1,
2, 2, 'Local')
ret = SapModel.FrameObj.SetLoadDistributed(FrameName2, '5', 1, 2, 0, 1, -
2, -2, 'Local')

#assign loading for load pattern 6
ret = SapModel.FrameObj.SetLoadDistributed(FrameName1, '6', 1, 2, 0, 1,
0.9984, 0.3744, 'Local')
ret = SapModel.FrameObj.SetLoadDistributed(FrameName2, '6', 1, 2, 0, 1, -
0.3744, 0, 'Local')

#assign loading for load pattern 7
ret = SapModel.FrameObj.SetLoadPoint(FrameName2, '7', 1, 2, 0.5, -15,
'Local')

#switch to k-in units
kip_in_F = 3
ret = SapModel.SetPresentUnits(kip_in_F)

#save model
ret = SapModel.File.Save(ModelPath)

#run model (this will create the analysis model)
ret = SapModel.Analyze.RunAnalysis()


#initialize for SAP2000 results
SapResult = [0,0,0,0,0,0,0]
[PointName1, PointName2, ret] = SapModel.FrameObj.GetPoints(FrameName2,
PointName1, PointName2)

#get SAP2000 results for load cases 1 through 7
for i in range(0,7):
NumberResults = 0
Obj = []
Elm = []
ACase = []
StepType = []
StepNum = []
U1 = []
U2 = []
U3 = []
R1 = []
R2 = []
R3 = []
ObjectElm = 0
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput(str(i + 1))
if i <= 3:
[NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3,
R1, R2, R3, ret] = SapModel.Results.JointDispl(PointName2, ObjectElm,
NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2,
R3)
SapResult[i] = U3[0]
else:


[NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3,
R1, R2, R3, ret] = SapModel.Results.JointDispl(PointName1, ObjectElm,
NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2,
R3)
SapResult[i] = U1[0]

#close SAP2000
ret = mySapObject.ApplicationExit(False)
SapModel = None
mySapObject = None
#fill independent results
IndResult = [0,0,0,0,0,0,0]
IndResult[0] = -0.02639
IndResult[1] = 0.06296
IndResult[2] = 0.06296
IndResult[3] = -0.2963
IndResult[4] = 0.3125
IndResult[5] = 0.11556
IndResult[6] = 0.00651

#fill percent difference
PercentDiff = [0,0,0,0,0,0,0]
for i in range(0,7):
PercentDiff[i] = (SapResult[i] / IndResult[i]) - 1

#display results
for i in range(0,7):
print()
print(SapResult[i])
print(IndResult[i])


```
print(PercentDiff[i])
```
## Release Notes

Initial release in version 15.0.1
Updated for version 24.1.0.
Updated for version 26.0.0.

# Example 8 (Python NET)

## Remarks

This example was created using Python 3.9.7. It is based on the SAP2000 verification problem
Example 1-001.
This example creates the example verification problem from scratch, runs the analysis, extracts
results, and compares the results with hand calculated values.

## Example

1. Download and install Python 3.9.7 or higher for Windows. Python is freely available at
python.org.
2. Install the Python package "pythonnet". This example was created using pythonnet version
3.0.3. If you are using Python 3.4 or higher, the easiest way to install this package is by opening a
command prompt with administrative privileges and entering the command:
python -m pip install pythonnet
Please note that your computer will need to be connected to the internet for the above command to
work.
3. Create a Python .py file using IDLE or any text editor and paste in the following code. Please
pay attention to the comments in this code block; they contain important information about
running the script. This example includes an option for executing on a remote computer, however
that functionality has been disabled in SAP2000 v26.0.0. It may be reinstated in a future release.
    import os
    import sys
    # set the following flag to true to select the .NET Core run-time
    environment,
    # false to select .NET Framework run-time environment.
    UseNETCore = True # False #
    if UseNETCore:


from pythonnet import load
load("coreclr")
import clr
else:
import clr
clr.AddReference("System.Runtime.InteropServices")
from System.Runtime.InteropServices import Marshal
from enum import Enum
#set the following path to the installed SAP2000 program directory
clr.AddReference(R'C:\Program Files\Computers and Structures\SAP2000 26
\SAP2000v1.dll')
from SAP2000v1 import *
#set the following flag to True to execute on a remote computer
Remote = False
#if the above flag is True, set the following variable to the hostname of
the remote computer
#remember that the remote computer must have SAP2000 installed and be
running the CSiAPIService.exe
RemoteComputer = "SpareComputer-DT"
#set the following flag to True to attach to an existing instance of the
program
#otherwise a new instance of the program will be started
AttachToInstance = False
#set the following flag to True to manually specify the path to
SAP2000.exe
#this allows for a connection to a version of SAP2000 other than the
latest installation
#otherwise the latest installed version of SAP2000 will be launched
SpecifyPath = False
#if the above flag is set to True, specify the path to SAP2000 below
ProgramPath = R'C:\Program Files\Computers and Structures\SAP2000 26
\SAP2000.exe'


#full path to the model
#set it to the desired path of your model
#if executing remotely, ensure that this folder already exists on the
remote computer
#the below command will only create the folder locally
APIPath = R'C:\CSiAPIExample'
if not os.path.exists(APIPath):
try:
os.makedirs(APIPath)
except OSError:
pass
ModelPath = APIPath + os.sep + R'API_1-001.sdb'
#create API helper object
helper = cHelper(Helper())
if AttachToInstance:
#attach to a running instance of SAP2000
try:
#get the active SapObject
if Remote:
mySapObject = cOAPI(helper.GetObjectHost(RemoteComputer,
"CSI.SAP2000.API.SapObject"))
else:
mySapObject = cOAPI(helper.GetObject
("CSI.SAP2000.API.SapObject"))
except:
print("No running instance of the program found or failed to
attach.")
sys.exit(-1)
else:
if SpecifyPath:


try:
#'create an instance of the SapObject from the specified path
if Remote:
mySapObject = cOAPI(helper.CreateObjectHost
(RemoteComputer, ProgramPath))
else:
mySapObject = cOAPI(helper.CreateObject(ProgramPath))
except :
print("Cannot start a new instance of the program from " +
ProgramPath)
sys.exit(-1)
else:
try:
#create an instance of the SapObject from the latest
installed SAP2000
if Remote:
mySapObject = cOAPI(helper.CreateObjectProgIDHost
(RemoteComputer, "CSI.SAP2000.API.SapObject"))
else:
mySapObject = cOAPI(helper.CreateObjectProgID
("CSI.SAP2000.API.SapObject"))
except:
print("Cannot start a new instance of the program.")
sys.exit(-1)
#start SAP2000 application
mySapObject.ApplicationStart()
#create SapModel object
SapModel = cSapModel(mySapObject.SapModel)
#initialize model
kip_in_F = 3
SapModel.InitializeNewModel(eUnits(kip_in_F))


#create new blank model
File = cFile(SapModel.File)
ret = File.NewBlank()
#define material property
MATERIAL_CONCRETE = 2
PropMaterial = cPropMaterial(SapModel.PropMaterial)
ret = PropMaterial.SetMaterial('CONC', eMatType(MATERIAL_CONCRETE))
#assign isotropic mechanical properties to material
ret = PropMaterial.SetMPIsotropic('CONC', 3600, 0.2, 0.0000055)
#define rectangular frame section property
PropFrame = cPropFrame(SapModel.PropFrame)
ret = PropFrame.SetRectangle('R1', 'CONC', 12, 12)
#define frame section property modifiers
ModValue = [1000, 0, 0, 1, 1, 1, 1, 1]
ret = PropFrame.SetModifiers('R1', ModValue)
#switch to k-ft units
kip_ft_F = 4
ret = SapModel.SetPresentUnits(eUnits(kip_ft_F))
#add frame object by coordinates
FrameObj = cFrameObj(SapModel.FrameObj)
FrameName1 = ' '
FrameName2 = ' '
FrameName3 = ' '
[ret, FrameName1] = FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, FrameName1,
'R1', '1', 'Global')
[ret, FrameName2] = FrameObj.AddByCoord(0, 0, 10, 8, 0, 16, FrameName2,
'R1', '2', 'Global')
[ret, FrameName3] = FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10, FrameName3,
'R1', '3', 'Global')
#assign point object restraint at base


PointObj = cPointObj(SapModel.PointObj)
PointName1 = ' '
PointName2 = ' '
Restraint = [True, True, True, True, False, False]
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName1,
PointName1, PointName2)
ret = PointObj.SetRestraint(PointName1, Restraint)
#assign point object restraint at top
Restraint = [True, True, False, False, False, False]
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName2,
PointName1, PointName2)
ret = PointObj.SetRestraint(PointName2, Restraint)
#refresh view, update (initialize) zoom
View = cView(SapModel.View)
ret = View.RefreshView(0, False)
#add load patterns
LTYPE_OTHER = 8
LoadPatterns = cLoadPatterns(SapModel.LoadPatterns)
ret = LoadPatterns.Add('1', eLoadPatternType(LTYPE_OTHER), 1, True)
ret = LoadPatterns.Add('2', eLoadPatternType(LTYPE_OTHER), 0, True)
ret = LoadPatterns.Add('3', eLoadPatternType(LTYPE_OTHER), 0, True)
ret = LoadPatterns.Add('4', eLoadPatternType(LTYPE_OTHER), 0, True)
ret = LoadPatterns.Add('5', eLoadPatternType(LTYPE_OTHER), 0, True)
ret = LoadPatterns.Add('6', eLoadPatternType(LTYPE_OTHER), 0, True)
ret = LoadPatterns.Add('7', eLoadPatternType(LTYPE_OTHER), 0, True)
#assign loading for load pattern 2
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName3,
PointName1, PointName2)
PointLoadValue = [0,0,-10,0,0,0]
ret = PointObj.SetLoadForce(PointName1, '2', PointLoadValue)


ret = FrameObj.SetLoadDistributed(FrameName3, '2', 1, 10, 0, 1, 1.8, 1.8)
#assign loading for load pattern 3
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName3,
PointName1, PointName2)
PointLoadValue = [0,0,-17.2,0,-54.4,0]
ret = PointObj.SetLoadForce(PointName2, '3', PointLoadValue)
#assign loading for load pattern 4
ret = FrameObj.SetLoadDistributed(FrameName2, '4', 1, 11, 0, 1, 2, 2)
#assign loading for load pattern 5
ret = FrameObj.SetLoadDistributed(FrameName1, '5', 1, 2, 0, 1, 2, 2,
'Local')
ret = FrameObj.SetLoadDistributed(FrameName2, '5', 1, 2, 0, 1, -2, -2,
'Local')
#assign loading for load pattern 6
ret = FrameObj.SetLoadDistributed(FrameName1, '6', 1, 2, 0, 1, 0.9984,
0.3744, 'Local')
ret = FrameObj.SetLoadDistributed(FrameName2, '6', 1, 2, 0, 1, -0.3744,
0, 'Local')
#assign loading for load pattern 7
ret = FrameObj.SetLoadPoint(FrameName2, '7', 1, 2, 0.5, -15, 'Local')
#switch to k-in units
kip_in_F = 3
ret = SapModel.SetPresentUnits(eUnits(kip_in_F))
#save model
File = cFile(SapModel.File)
ret = File.Save(ModelPath)
#run model (this will create the analysis model)
Analyze = cAnalyze(SapModel.Analyze)
ret = Analyze.RunAnalysis()
#initialize for results
ProgramResult = [0,0,0,0,0,0,0]


[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName2,
PointName1, PointName2)
#get results for load cases 1 through 7
Results = cAnalysisResults(SapModel.Results)
Setup = cAnalysisResultsSetup(Results.Setup)
for i in range(0,7):
NumberResults = 0
Obj = []
Elm = []
ACase = []
StepType = []
StepNum = []
U1 = []
U2 = []
U3 = []
R1 = []
R2 = []
R3 = []
ObjectElm = 0
ret = Setup.DeselectAllCasesAndCombosForOutput()
ret = Setup.SetCaseSelectedForOutput(str(i + 1))
if i <= 3:
[ret, NumberResults, Obj, Elm, ACase, StepType, StepNum, U1,
U2, U3, R1, R2, R3] = Results.JointDispl(PointName2, eItemTypeElm
(ObjectElm), NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2,
U3, R1, R2, R3)
ProgramResult[i] = U3[0]
else:
[ret, NumberResults, Obj, Elm, ACase, StepType, StepNum, U1,
U2, U3, R1, R2, R3] = Results.JointDispl(PointName1, eItemTypeElm
(ObjectElm), NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2,
U3, R1, R2, R3)


```
ProgramResult[i] = U1[0]
#close the program
ret = mySapObject.ApplicationExit(False)
SapModel = None
mySapObject = None
#fill independent results
IndResult = [0,0,0,0,0,0,0]
IndResult[0] = -0.02639
IndResult[1] = 0.06296
IndResult[2] = 0.06296
IndResult[3] = -0.2963
IndResult[4] = 0.3125
IndResult[5] = 0.11556
IndResult[6] = 0.00651
#fill percent difference
PercentDiff = [0,0,0,0,0,0,0]
for i in range(0,7):
PercentDiff[i] = (ProgramResult[i] / IndResult[i]) - 1
#display results
for i in range(0,7):
print()
print(ProgramResult[i])
print(IndResult[i])
print(PercentDiff[i])
```
## Release Notes

Initial release in version 15.0.1
Updated for version 24.1.0.
Updated for version 26.0.0.


# Example (IronPython)

## Remarks

This example was created using IronPython 3.4. It is based on the SAP2000 verification problem
Example 1-001.
This example creates the example verification problem from scratch, runs the analysis, extracts
results, and compares the results with hand calculated values.

## Example

1. Either download and install the IronPython interpreter from https:\\ironpython.net or, on a
    command prompt, navigate to your API script folder and install IronPython as a .NET local
    tool by issuing the following commands:
       dotnet new tool-manifest
       dotnet tool install --local IronPython.Console --version 3.4.1
2. Create a Python .py file using your preferred IDE, copy and paste in the Python code
    example below, and save it as IronPythonApplication1.py in your API script folder.
3. When using the IronPython interpreter, open a command prompt, navigate to your API
    script folder and issue the following command to run the API script
       When using the IronPython interpreter, open a command prompt, navigate to your
       API script folder and issue the following command to run the API script:
          ipy IronPythonApplication1.py
       When using the .NET local tool, on the same command prompt, issue the following
       command to run the API script:
       dotnet ipy IronPythonApplication1.py
       Please pay attention to the comments in this code block; they contain important
       information about running the script. This example includes an option for executing
       on a remote computer, however that functionality has been disabled in SAP2000
       v26.0.0. It may be reinstated in a future release.
import os
import sys
import clr
from enum import Enum
clr.AddReference("System")
import System


#set the following path to the installed SAP2000 program directory
clr.AddReferenceToFileAndPath("C:\Program Files\Computers and Structures\SAP2000 26
\SAP2000v1.dll")
from SAP2000v1 import *
#set the following flag to True to execute on a remote computer
Remote = False
#if the above flag is True, set the following variable to the hostname of the remote computer
#remember that the remote computer must have SAP2000 installed and be running the
CSiAPIService.exe
RemoteComputer = "SpareComputer-DT"
#set the following flag to True to attach to an existing instance of the program
#otherwise a new instance of the program will be started
AttachToInstance = False
#set the following flag to True to manually specify the path to SAP2000.exe
#this allows for a connection to a version of SAP2000 other than the latest installation
#otherwise the latest installed version of SAP2000 will be launched
SpecifyPath = False
#if the above flag is set to True, specify the path to SAP2000 below
ProgramPath = "C:\Program Files\Computers and Structures\SAP2000 26\SAP2000.exe"
#full path to the model
#set it to the desired path of your model
#if executing remotely, ensure that this folder already exists on the remote computer
#the below command will only create the folder locally
APIPath = "C:\CSiAPIExample"
if not os.path.exists(APIPath):
try:
os.makedirs(APIPath)
except OSError:
pass


ModelPath = APIPath + os.sep + "API_1-001.sdb"
#create API helper object
helper = Helper()
if AttachToInstance:
#attach to a running instance of SAP2000
try:
#get the active SapObject
if Remote:
mySapObject = helper.GetObjectHost(RemoteComputer, "CSI.SAP2000.API.SapObject")
else:
mySapObject = helper.GetObject("CSI.SAP2000.API.SapObject")
except:
print("No running instance of the program found or failed to attach.")
sys.exit(-1)
else:
if SpecifyPath:
try:
#'create an instance of the SapObject from the specified path
if Remote:
mySapObject = helper.CreateObjectHost(RemoteComputer, ProgramPath)
else:
mySapObject = helper.CreateObject(ProgramPath)
except:
print("Cannot start a new instance of the program from " + ProgramPath)
sys.exit(-1)
else:
try:
#create an instance of the SapObject from the latest installed SAP2000


if Remote:
mySapObject = helper.CreateObjectProgIDHost(RemoteComputer,
"CSI.SAP2000.API.SapObject")
else:
mySapObject = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
except:
print("Cannot start a new instance of the program.")
sys.exit(-1)
#start SAP2000 application
mySapObject.ApplicationStart()
#create SapModel object
SapModel = mySapObject.SapModel
#initialize model
SapModel.InitializeNewModel()
#create new blank model
File = SapModel.File
ret = File.NewBlank()
#define material property
PropMaterial = SapModel.PropMaterial
ret = PropMaterial.SetMaterial('CONC', eMatType.Concrete)
#assign isotropic mechanical properties to material
ret = PropMaterial.SetMPIsotropic('CONC', 3600, 0.2, 0.0000055)
#define rectangular frame section property
PropFrame = SapModel.PropFrame
ret = PropFrame.SetRectangle('R1', 'CONC', 12, 12)
#define frame section property modifiers
ModValue = System.Array[float]([1000, 0, 0, 1, 1, 1, 1, 1])
ret = PropFrame.SetModifiers('R1', ModValue)
#switch to k-ft units


ret = SapModel.SetPresentUnits(eUnits.kip_ft_F)
#add frame object by coordinates
FrameObj = SapModel.FrameObj
FrameName1 = ' '
FrameName2 = ' '
FrameName3 = ' '
[ret, FrameName1] = FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, FrameName1, 'R1', '1', 'Global')
[ret, FrameName2] = FrameObj.AddByCoord(0, 0, 10, 8, 0, 16, FrameName2, 'R1', '2', 'Global')
[ret, FrameName3] = FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10, FrameName3, 'R1', '3', 'Global')
#assign point object restraint at base
PointObj = SapModel.PointObj
PointName1 = ' '
PointName2 = ' '
Restraint = clr.StrongBox[System.Array[bool]](System.Array[bool]([True, True, True, True,
False, False]))
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName1, PointName1, PointName2)
ret = PointObj.SetRestraint(PointName1, Restraint)
#assign point object restraint at top
Restraint = clr.StrongBox[System.Array[bool]](System.Array[bool]([True, True, False, False,
False, False]))
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName2, PointName1, PointName2)
ret = PointObj.SetRestraint(PointName2, Restraint)
#refresh view, update (initialize) zoom
View = SapModel.View
ret = View.RefreshView(0, False)
#add load patterns
LoadPatterns = SapModel.LoadPatterns
ret = LoadPatterns.Add('1', eLoadPatternType.Other, 1, True)
ret = LoadPatterns.Add('2', eLoadPatternType.Other, 0, True)


ret = LoadPatterns.Add('3', eLoadPatternType.Other, 0, True)
ret = LoadPatterns.Add('4', eLoadPatternType.Other, 0, True)
ret = LoadPatterns.Add('5', eLoadPatternType.Other, 0, True)
ret = LoadPatterns.Add('6', eLoadPatternType.Other, 0, True)
ret = LoadPatterns.Add('7', eLoadPatternType.Other, 0, True)
#assign loading for load pattern 2
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName3, PointName1, PointName2)
PointLoadValue = clr.StrongBox[System.Array[float]](System.Array[float]([0,0,-10,0,0,0]))
ret = PointObj.SetLoadForce(PointName1, '2', PointLoadValue)
ret = FrameObj.SetLoadDistributed(FrameName3, '2', 1, 10, 0, 1, 1.8, 1.8)
#assign loading for load pattern 3
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName3, PointName1, PointName2)
PointLoadValue = clr.StrongBox[System.Array[float]](System.Array[float]([0,0,-17.2,0,-54.4,0]))
ret = PointObj.SetLoadForce(PointName2, '3', PointLoadValue)
#assign loading for load pattern 4
ret = FrameObj.SetLoadDistributed(FrameName2, '4', 1, 11, 0, 1, 2, 2)
#assign loading for load pattern 5
ret = FrameObj.SetLoadDistributed(FrameName1, '5', 1, 2, 0, 1, 2, 2, 'Local')
ret = FrameObj.SetLoadDistributed(FrameName2, '5', 1, 2, 0, 1, -2, -2, 'Local')
#assign loading for load pattern 6
ret = FrameObj.SetLoadDistributed(FrameName1, '6', 1, 2, 0, 1, 0.9984, 0.3744, 'Local')
ret = FrameObj.SetLoadDistributed(FrameName2, '6', 1, 2, 0, 1, -0.3744, 0, 'Local')
#assign loading for load pattern 7
ret = FrameObj.SetLoadPoint(FrameName2, '7', 1, 2, 0.5, -15, 'Local')
#switch to k-in units
ret = SapModel.SetPresentUnits(eUnits.kip_in_F)
#save model
File = SapModel.File


ret = File.Save(ModelPath)
#run model (this will create the analysis model)
Analyze = SapModel.Analyze
ret = Analyze.RunAnalysis()
#initialize for results
ProgramResult = System.Array[float]([0,0,0,0,0,0,0])
[ret, PointName1, PointName2] = FrameObj.GetPoints(FrameName2, PointName1, PointName2)
#get results for load cases 1 through 7
Results = SapModel.Results
Setup = Results.Setup
for i in range(0,7):
NumberResults = 0
Obj = System.Array[str]([])
Elm = System.Array[str]([])
ACase = System.Array[str]([])
StepType = System.Array[str]([])
StepNum = System.Array[float]([])
U1 = System.Array[float]([])
U2 = System.Array[float]([])
U3 = System.Array[float]([])
R1 = System.Array[float]([])
R2 = System.Array[float]([])
R3 = System.Array[float]([])
ObjectElm = 0
ret = Setup.DeselectAllCasesAndCombosForOutput()
ret = Setup.SetCaseSelectedForOutput(str(i + 1))
if i <= 3:


[ret, NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2, R3] =
Results.JointDispl(PointName2, eItemTypeElm(ObjectElm), NumberResults, Obj, Elm, ACase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)
ProgramResult[i] = U3[0]
else:
[ret, NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2, R3] =
Results.JointDispl(PointName1, eItemTypeElm(ObjectElm), NumberResults, Obj, Elm, ACase,
StepType, StepNum, U1, U2, U3, R1, R2, R3)
ProgramResult[i] = U1[0]
#close the program
ret = mySapObject.ApplicationExit(False)
SapModel = None
mySapObject = None
#fill independent results
IndResult = [0,0,0,0,0,0,0]
IndResult[0] = -0.02639
IndResult[1] = 0.06296
IndResult[2] = 0.06296
IndResult[3] = -0.2963
IndResult[4] = 0.3125
IndResult[5] = 0.11556
IndResult[6] = 0.00651
#fill percent difference
PercentDiff = [0,0,0,0,0,0,0]
for i in range(0,7):
PercentDiff[i] = (ProgramResult[i] / IndResult[i]) - 1
#display results
for i in range(0,7):
print()
print(ProgramResult[i])


print(IndResult[i])
print(PercentDiff[i])

## Release Notes

Initial Release for version 24.2.0
Updated for version 26.0.0.


