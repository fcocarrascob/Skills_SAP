# Accessing SAP2000 From An External

# Application

This page contains an outline for connecting to the SAP2000 API, with VBA code examples. For
specific instructions for supported programming languages, please refer to the Example Code
section.
The first step in using the CSI API from an external application is to reference SAP2000v1.dll or
SAP2000v1.tlb from your application. If using Excel VBA, reference SAP2000v1.TLB by
opening the VBA editor, clicking the **Tools menu > References** command and selecting
SAP2000v1.TLB from the program installation folder.
Next, within your application, you will create a variable of interface type cOAPI, and an instance
of the SAP2000 object which implements cOAPI. In VBA this could be accomplished as:
Dim mySapObject As SAP2000v1.cOAPI
Dim myHelper As SAP2000v1.cHelper
Set myHelper = New SAP2000v1.Helper
Set mySapObject = myHelper.CreateObject(ProgramPath)

The first line creates the interface variable, the second and third lines create a helper class, and the
fourth line creates the instance of the SAP2000 object which implements the interface by passing
in the path to where the SAP2000.exe program is located. Now that an instance of the SAP 2000
object has been created in your application, start SAP2000 using the following VBA command:
SapObject.ApplicationStart

At this point you can open an existing model, or create a new one and perform whatever actions
are required. In general, the API commands are accessed through SapObject.SapModel.
It may be helpful to define a SapModel variable so that the API commands are accessed through
SapModel instead of SapObject.SapModel. In VBA this could be accomplished as:
Dim mySapModel As cSapModel
Set mySapModel= mySapObject.SapModel

When finished with a model, you may want to close the SAP2000 application. This can be
accomplished using the following VBA command:
SapObject.ApplicationExit True

As a last step, the SapModel and SapObject variables should always be set to Nothing. In VBA
this is accomplished as:


Set SapModel= Nothing
Set SapObject= Nothing

Setting the variables to Nothing is a very important step. It breaks the connection between your
application and SAP2000 and frees up system resources. If the variables are not set to Nothing, the
SAP2000 application may not completely close (you may still see it running in your Windows
Task Manager).
Putting all the steps previously described into a single example, a VBA program might consist of
the following:
Sub MyProgram
'dimension variables
Dim mySapObject As SAP2000v1.cOAPI
Dim myHelper As SAP2000v1.cHelper
Dim mySapModel As cSapModel
Dim ret As Long
'create an instance of the SAP2000 object
Set myHelper= New SAP2000v1.Helper
Set mySapObject= myHelper.CreateObject("C:\Program Files (x86)\Computers and
Structures\SAP2000 21\sap2000.exe")
'start the SAP2000 application
mySapObject.ApplicationStart

'create the SapModel object
Set mySapModel= mySapObject.SapModel

'initialize model
ret = mySapModel.InitializeNewModel
'call SAP2000 API functions here to perform desired tasks
'in this example a new 2D frame is created from template
ret = mySapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'close the SAP2000 application, if desired
mySapObject.ApplicationExit False

'set the objects to Nothing
'at the end of your program ALWAYS terminate the objects in this manner
Set mySapModel= Nothing
Set mySapObject= Nothing
End Sub

**See Also**
Introduction


```
Function Documentation Conventions
Function Return Values
Units Abbreviations
Visual Basic Concepts Used in the CSI API
```
# Function Documentation Conventions

The documentation of each function in the API has the following sections:
Syntax
This section provides the syntax of the command as including any parameters you would call it from an external application without

VB6 Procedure
The VB6 procedure shows the function as defined in type of each parameter, which parameters are optionSAP2000. This function definition shows the variablal, and which optional parameters have built-in default e
values.
See apply to the CSI API.Visual Basic Concepts Used in the CSI API for more information about Visual Basic definitions that

Parameters
The Parameters used in the function are briefly desthem are followed by a units abbreviation in square brackets, such as [F], indicating the uncribed. Parameters that have units associated with its type for the
item.
Remarks
The Remarks describe what the function does and proexplained in the Parameters. See Function Return Valuesvides additional information, if any, that was not for more information.

VBA Example
The VBA example uses the considered function. The examples are written for use in Microsoft Excel VBA.
Release Notes
The release information specific to the considered function is provided.
See Also
Functions that are related to the considered function, if any, are listed in this area.
**See Also**
Introduction
Accessing SAP2000 From An External Application
Function Return Values


```
Units Abbreviations
Visual Basic Concepts Used in the CSI API
```
# Function Return Values

Almost all CSI API functions return a Long (32 bit signed integer) value indicating if the function
executed successfully.
A return value of 0 indicates that SAP2000 successfully executed the function.
Any nonzero return value indicates that the function was not successfully executed.
**See Also**
Introduction
Accessing SAP2000 From An External Application
Function Documentation Conventions
Units Abbreviations
Visual Basic Concepts Used in the CSI API

# Units Abbreviations

In the documentation of each CSI API function, parameters that have units associated with them
are followed by one of the following abbreviations, to indicate the units for those parameters.
**[L]** = Length
**[F]** = Force, [F] = [ML/s^2 ]
**[M]** = Mass
**[s]** = Time, seconds
**[T]** = Temperature
**[cyc]** = Cycles
**[rad]** = Radians (angle measurement)
**[deg]** = Degrees (angle measurement)
Combinations of these abbreviations are used in many cases. For example, moments are indicated
as **[FL]** and stresses are indicated as **[F/L**^2 **]**.
**See Also**
Introduction


```
Accessing SAP2000 From An External Application
Function Documentation Conventions
Function Return Values
Visual Basic Concepts Used in the CSI API
```
# Visual Basic Concepts Used in the CSI API

Some of the Visual Basic concepts and definitions that apply to the CSI API are explained herein.
Option Base
Visual Basic 6 allows the default lower bound for arrays to be specified as 0 (the default), or 1.
SAP2000 uses a lower bound of 0 for all arrays. Any program that accesses SAP2000 through the
API should also use a lower bound of 0 for its arrays.
Fixed-Size and Dynamic Arrays
Arrays can be used to refer to a series of variables by the same name and to use a number (an
index) to distinguish them. Visual Basic has two types of arrays: fixed-size and dynamic. A fixed-
size array always remains the same size. A dynamic array can change its size while the program is
running.
A fixed-size array is declared with the size indicated. For example, the following line declares
MyFixedArray dimensioned to 2.
Dim MyFixedArray(2)as Double

Dimensioning the array to 2 means that it holds three data items:
MyFixedArray(0) = first data item
MyFixedArray(1) = second data item
MyFixedArray(2) = third data item
Dynamic arrays are declared with no size indicated as shown here:
Dim MyDynamicArray()as Double

Dynamic arrays are dimensioned sometime after they are declared using a statement such as the
following:
ReDim MyDynamicArray(2)

Any array that is dimensioned inside SAP2000 must be declared as a dynamic array so that
SAP2000 can redimension it. It is probably a good idea to declare all arrays as dynamic arrays for
simplicity. As an example, the analysis results obtained through the CSI API are stored in arrays
that are defined as dynamic arrays by the user and then dimensioned and filled inside of SAP2000.


Variable Types
Most of the data in the CSI API is one of the following variable types.
◾ **Boolean** : A variable stored as a 16-bit (2-byte) number, but it can only be True or False.
When boolean values are converted to other data types, False becomes 0 and True becomes
–1.
◾ **Long** : A variable stored as a 32-bit (4-byte) number ranging in value from -2,147,483,
to 2,147,483,647. Note that other programming languages may refer to this data type
differently; for example, they may refer to this as an Integer.
◾ **Double** : A double-precision floating-point variable stored as an IEEE 64-bit (8-byte)
floating-point number ranging in value from -1.79769313486231E308 to -
4.94065645841247E-324 for negative values and from 4.94065645841247E-324 to
1.79769313486232E308 for positive values.
◾ **String** : A variable length string.
Optional Arguments
Some of the CSI API functions have optional arguments. For example, the CountLoadDispl
function has two optional arguments: Name and LoadPat. It is not necessary to include the
optional arguments when calling this function. All four of the following calls are valid.
ret = SapModel.PointObj.CountLoadDispl(Count)
ret = SapModel.PointObj.CountLoadDispl(Count, Name)

ret = SapModel.PointObj.CountLoadDispl(Count, , LoadPat)

ret = SapModel.PointObj.CountLoadDispl(Count, Name, LoadPat)

Note in the third example, the first optional item is not included and the second optional item is
included. In that case, commas must be included to denote the missing arguments.
Comments
In Visual Basic the Rem statement followed by a space indicates that all of the data on the line to
the right of the Rem statement is a comment (or a remark). The Rem statement can be abbreviated
using an apostrophe, '. The apostrophe is used in all of the VBA examples in the CSI API
documentation to denote a comment.
ByVal and ByRef
Variables are passed to the \ using the ByRef or the ByVal keyword.
◾ **ByVal** means that the variable is passed by value. This allows the CSI API to access a copy
of the variable but not the original variable. This means the value of the variable in another
application can not be changed by the API.
◾ **ByRef** , which is the default in VB6 and VBA, means the argument is passed by reference.
This passes the address of the variable to the CSI API instead of passing a copy of the value.


It allows the CSI API to access the actual variable, and, as a result, allows SAP2000 to
change the variable's actual value in an application.
Variables are passed ByRef when data needs to be returned in them from SAP2000 to your
application. In addition, Visual Basic requires that all arrays be passed ByRef.
Release Notes
Changed nomenclature from Load Cases, Analysis Cases and Response Combinations to Load
Patterns, Load Cases and Load Combinations, respectively, in version 12.00.
**See Also**
Introduction
Accessing SAP2000 From An External Application
Function Documentation Conventions
Function Return Values
Units Abbreviations

# Using the Cross-Product API Library

Starting with Version 21 of SAP2000, API developers have access to a powerful new tool to
create API client applications that can work with multiple CSI programs.
New releases of SAP2000, CSiBridge, ETABS, and SAFE all contain a new API library,
CSiAPIv1.dll. This library is compatible with all four programs.
Developers can now create API client applications that reference CSiAPIv1.dll , and connect to
either SAP2000, CSiBridge, ETABS, or SAFE, without any code changes required.
For more information and examples of how to use CSiAPIv1.dll , please see: CSI Knowledge
Base Cross Product API Examples

# Remote API

The SAP2000 API can be used to start and/or connect to a running instance of SAP2000 on a
remote computer that is running the API Service. This can be particularly useful if you need to run
a large number of load cases (e.g., earthquakes for performance-based design, moving load cases
for bridge design, etc.), and there are multiple machines available for running analyses
simultaneously.
Simultaneous runs can be started on multiple Remote Computers using an API script or plug-in,
and results can be merged to the Main Computer programmatically, without user intervention, as
they become available. Other applications could include using distributed processing to run a large
parameter study or Monte Carlo simulation.
Terminology


**Main Computer** : Your primary computer.
**Remote Computer** : Any other computer that you have access to (physically or over the
network) and that is available for running analyses and/or API scripts.
**API Service** : “CSiAPIService.exe” command line utility running on a remote computer that
enables Remote API.
**TCP Port** : A TCP (Transmission Control Protocol) port is an integer between 0 to 65535
used to identify which service is to receive a packet/message sent to a Remote Computer.
Requirements & Limitations
Depending on the type of firewall installed on a Remote Computer, you may have to create
a firewall exception on that Remote Computer to allow the API Service to communicate on
your network. This is done automatically for Windows Firewall during the installation of
SAP2000, but it may have to be manually done for other firewalls and will require
administrative privileges. This is typically a one-time operation.
The API Service has two modes:
Product-Specific:
◦ Listens to connections made from SAP2000v1.dll at default TCP port 11650. (For
CSiBridge1.dll , the port is 11649 )
◦ This is the default mode and can be started using the following command:
“CSiAPIService.exe” or “CSiAPIService.exe --api A”
Cross-Product:
◦ Listens to connections made from CSiAPIv1.dll at default TCP port 11646.
◦ This can be started using the following command:
“CSiAPIService.exe --api C”
Multiple API Service instances can be run simultaneously on a Remote Computer as long as they
do not use the same TCP port. In case of TCP port conflicts with other programs, it is possible to
assign a specific TCP port to each API Service instance using the following command:
“CSiAPIService.exe --port [portNumber]”
where [portNumber] is between 1024 and 49151.
It is also possible to override the default TCP port for Product-Specific and Cross-Product API
modes using the following Windows environment variables:
Product-Specific: “SAP2000v1_cOAPI_DEFAULT_PORT” (For CSiBridge, use
“CSiBridge1_cOAPI_DEFAULT_PORT”)
Cross-Product: “CSiAPIv1_cOAPI_DEFAULT_PORT”
Procedure
Install the SAP2000 on the Main and Remote Computers.


On each Remote Computer, open a command prompt and run “CSiAPIService.exe”, located in the
SAP2000 installation folder, to start the API Service.
**Tip** : Type “CSiAPIService.exe --help” to view a detailed list of options where you can set
◦ The TCP port to use.
◦ API mode: Product-specific or Cross-product.
**Tip** : You can set the API Service to run automatically when your computer starts (see Change
which apps run automatically at startup in Windows 10 for details).
On your Main Computer, run a script, program, or SAP2000 Plug-in that uses one of the following
API calls to start (CreateObject...) or connect to (GetObject...) an instance of SAP2000 on a
Remote Computer:
cHelper.CreateObjectHost(
ByVal hostName As String,
ByVal fullPath As String)
cHelper.CreateObjectHostPort(
ByVal hostName As String,
ByVal portNumber As Integer,
ByVal fullPath As String)
cHelper.CreateObjectProgIDHost(
ByVal hostName As String,
ByVal progID As String)
cHelper.CreateObjectProgIDHostPort(
ByVal hostName As String,
ByVal portNumber As Integer,
ByVal progID As String)
cHelper.GetObjectHost(
ByVal hostName As String,
ByVal progID As String)
cHelper.GetObjectHostPort(
ByVal hostName As String,
ByVal portNumber As Integer,


ByVal progID As String)
The above API calls receive the name of the Remote Computer (e.g. hostName = “myserver”),
and optionally a TCP port number, in addition to the arguments of the regular
cHelper.CreateObject() or GetObject() API calls. Upon successful instantiation at a Remote
Computer, subsequent calls to the returned cOAPI object will execute on the Remote Computer.
API calls can be used to open models, modify them, run analysis and design, extract results,
and/or merge results back to identical models on the Main Computer.

## Release Notes

Initial release in version 22.1.


