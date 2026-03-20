# ChangeName

## Syntax

SapObject.SapModel.GroupDef.ChangeName

## VB6 Procedure

Function ChangeName(ByVal Name As String, ByVal NewName As String) As Long

## Parameters

Name

The existing name of a defined group.

NewName

The new name for the group.

## Remarks

The function returns zero if the new name is successfully applied, otherwise it returns a nonzero
value.

Changing the name of group ALL will fail and return an error.

## VBA Example

Sub ChangeGroupName()
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

'define new group
ret = SapModel.GroupDef.SetGroup("Group1")

'change name of group
ret = SapModel.GroupDef.ChangeName("Group1", "MyGroup")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# Clear

## Syntax

SapObject.SapModel.GroupDef.Clear

## VB6 Procedure

Function Clear(ByVal Name As String) As Long

## Parameters

Name

The name of an existing group.

## Remarks

This function clears (removes) all assignments from the specified group.

The function returns zero if the group assignment is successfully cleared, otherwise it returns a
nonzero value.

## VBA Example

Sub ClearGroup()
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

'define new group
ret = SapModel.GroupDef.SetGroup("Group1")

'add frame objects to group
ret = SapModel.FrameObj.SetGroupAssign("8", "Group1")
ret = SapModel.FrameObj.SetGroupAssign("10", "Group1")

'clear group
ret = SapModel.GroupDef.Clear("Group1")

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

SapObject.SapModel.GroupDef.Count

## VB6 Procedure


Function Count() As Long

## Parameters

None

## Remarks

The function returns the number of defined groups.

## VBA Example

Sub CountGroups()
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

'return number of defined groups
ret = SapModel.GroupDef.Count

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

SapObject.SapModel.GroupDef.Delete

## VB6 Procedure

Function Delete(ByVal Name As String) As Long

## Parameters

Name

The name of an existing group.

## Remarks

The function deletes the specified group. It will return an error if an attempt is made to delete the
Group named ALL.

The function returns zero if the group is successfully deleted, otherwise it returns a nonzero value.

## VBA Example

Sub DeleteGroup()
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

'define new group
ret = SapModel.GroupDef.SetGroup("Group1")


'delete group
ret = SapModel.GroupDef.Delete("Group1")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

SetGroup

# GetAssignments

## Syntax

SapObject.SapModel.GroupDef.GetAssignments

## VB6 Procedure

Function GetAssignments(ByVal Name As String, ByRef NumberItems As Long, ByRef
ObjectType() As Long, ByRef ObjectName() As String) As Long

## Parameters

Name

The name of an existing group.

NumberItems

The number of assignments made to the specified group.

ObjectType

This is an array that includes the object type of each item in the group.

```
1 = Point object
2 = Frame object
3 = Cable object
4 = Tendon object
5 = Area object
6 = Solid object
7 = Link object
```

ObjectName

This is an array that includes the name of each item in the group.

## Remarks

This function retrieves the assignments to a specified group.

The function returns zero if the group assignment is successfully retrieved, otherwise it returns a
nonzero value.

## VBA Example

Sub GetGroupAssignments()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String
Dim NumberItems As Long
Dim ObjectType() As Long
Dim ObjectName() As String

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

'add cable object by points
ret = SapModel.CableObj.AddByPoint("1", "5", Name)

'set cable data
ret = SapModel.CableObj.SetCableData(Name, 7, 1, 0, 0, 24)

'define new group
ret = SapModel.GroupDef.SetGroup("Group1")

'add point objects to group
ret = SapModel.PointObj.SetGroupAssign("3", "Group1")
ret = SapModel.PointObj.SetGroupAssign("6", "Group1")
ret = SapModel.PointObj.SetGroupAssign("9", "Group1")


'add frame objects to group
ret = SapModel.FrameObj.SetGroupAssign("8", "Group1")
ret = SapModel.FrameObj.SetGroupAssign("10", "Group1")

'add cable object to group
ret = SapModel.CableObj.SetGroupAssign(Name, "Group1")

'get group assignments
ret = SapModel.GroupDef.GetAssignments("Group1", NumberItems, ObjectType,
ObjectName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# GetGroup

## Syntax

SapObject.SapModel.GroupDef.GetGroup

## VB6 Procedure

Function GetGroup(ByVal Name As String, ByRef color As Long, ByRef SpecifiedForSelection
As Boolean,ByRef SpecifiedForSectionCutDefinition As Boolean, ByRef
SpecifiedForSteelDesign As Boolean, ByRef SpecifiedForConcreteDesign As Boolean, ByRef
SpecifiedForAluminumDesign As Boolean, ByRef SpecifiedForColdFormedDesign As Boolean,
ByRef SpecifiedForStaticNLActiveStage As Boolean, ByRef SpecifiedForBridgeResponseOutput
As Boolean, ByRef SpecifiedForAutoSeismicOutput As Boolean, ByRef
SpecifiedForAutoWindOutput As Boolean, ByRef SpecifiedForMassAndWeight As Boolean) As
Long

## Parameters

Name

The name of an existing group.

color

The display color for the group specified as a Long.


SpecifiedForSelection

This item is True if the group is specified to be used for selection; otherwise it is False.

SpecifiedForSectionCutDefinition

This item is True if the group is specified to be used for defining section cuts; otherwise it is False.

SpecifiedForSteelDesign

This item is True if the group is specified to be used for defining steel frame design groups;
otherwise it is False.

SpecifiedForConcreteDesign

This item is True if the group is specified to be used for defining concrete frame design groups;
otherwise it is False.

SpecifiedForAluminumDesign

This item is True if the group is specified to be used for defining aluminum frame design groups;
otherwise it is False.

SpecifiedForColdFormedDesign

This item is True if the group is specified to be used for defining cold formed frame design
groups; otherwise it is False.

SpecifiedForStaticNLActiveStage

This item is True if the group is specified to be used for defining stages for nonlinear static
analysis; otherwise it is False.

SpecifiedForBridgeResponseOutput

This item is True if the group is specified to be used for reporting bridge response output;
otherwise it is False.

SpecifiedForAutoSeismicOutput

This item is True if the group is specified to be used for reporting auto seismic loads; otherwise it
is False.

SpecifiedForAutoWindOutput

This item is True if the group is specified to be used for reporting auto wind loads; otherwise it is
False.

SpecifiedForMassAndWeight

This item is True if the group is specified to be used for reporting group masses and weight;
otherwise it is False.

## Remarks


The function returns zero if the group data is successfully retrieved, otherwise it returns a nonzero
value.

## VBA Example

Sub GetGroupData()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret as Long
Dim Color as long
Dim SpecifiedForSelection as Boolean
Dim SpecifiedForSectionCutDefinition as Boolean
Dim SpecifiedForSteelDesign as Boolean
Dim SpecifiedForConcreteDesign as Boolean
Dim SpecifiedForAluminumDesign as Boolean
Dim SpecifiedForColdFormedDesign as Boolean
Dim SpecifiedForStaticNLActiveStage as Boolean
Dim SpecifiedForBridgeResponseOutput as Boolean
Dim SpecifiedForAutoSeismicOutput as Boolean
Dim SpecifiedForAutoWindOutput as Boolean
Dim SpecifiedForMassAndWeight as Boolean

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

'get group data
ret = SapModel.GroupDef.GetGroup("ALL", Color, SpecifiedForSelection,
SpecifiedForSectionCutDefinition, SpecifiedForSteelDesign, SpecifiedForConcreteDesign,
SpecifiedForAluminumDesign, SpecifiedForColdFormedDesign,
SpecifiedForStaticNLActiveStage, SpecifiedForBridgeResponseOutput,
SpecifiedForAutoSeismicOutput, SpecifiedForAutoWindOutput, SpecifiedForMassAndWeight)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.00.

## See Also

SetGroup

# GetNameList

## Syntax

SapObject.SapModel.GroupDef.GetNameList

## VB6 Procedure

Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

## Parameters

NumberNames

The number of group names retrieved by the program.

MyName

This is a one-dimensional array of group names. The MyName array is created as a dynamic, zero-
based, array by the API user:

Dim MyName() as String

The array is dimensioned to (NumberNames – 1) inside the Sap2000 program, filled with the
names, and returned to the API user.

## Remarks

This function retrieves the names of all defined groups.

The function returns zero if the names are successfully retrieved, otherwise it returns nonzero.

## VBA Example

Sub GetGroupNames()
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

'get group names
ret = SapModel.GroupDef.GetNameList(NumberNames, MyName)

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

## See Also

# SetGroup

## Syntax

SapObject.SapModel.GroupDef.SetGroup

## VB6 Procedure

Function SetGroup(ByVal Name As String, Optional ByVal color As Long = -1, Optional ByVal
SpecifiedForSelection As Boolean = True, Optional ByVal SpecifiedForSectionCutDefinition As
Boolean = True, Optional ByVal SpecifiedForSteelDesign As Boolean = True, Optional ByVal
SpecifiedForConcreteDesign As Boolean = True, Optional ByVal SpecifiedForAluminumDesign
As Boolean = True, Optional ByVal SpecifiedForColdFormedDesign As Boolean = True,
Optional ByVal SpecifiedForStaticNLActiveStage As Boolean = True, Optional ByVal


SpecifiedForBridgeResponseOutput As Boolean = True, Optional ByVal
SpecifiedForAutoSeismicOutput As Boolean = False, Optional ByVal
SpecifiedForAutoWindOutput As Boolean = False, Optional ByVal SpecifiedForMassAndWeight
As Boolean = True) As Long

## Parameters

Name

This is the name of a group. If this is the name of an existing group, that group is modified,
otherwise a new group is added.

color

The display color for the group specified as a Long. If this value is input as –1, the program
automatically selects a display color for the group.

SpecifiedForSelection

This item is True if the group is specified to be used for selection; otherwise it is False.

SpecifiedForSectionCutDefinition

This item is True if the group is specified to be used for defining section cuts; otherwise it is False.

SpecifiedForSteelDesign

This item is True if the group is specified to be used for defining steel frame design groups;
otherwise it is False.

SpecifiedForConcreteDesign

This item is True if the group is specified to be used for defining concrete frame design groups;
otherwise it is False.

SpecifiedForAluminumDesign

This item is True if the group is specified to be used for defining aluminum frame design groups;
otherwise it is False.

SpecifiedForColdFormedDesign

This item is True if the group is specified to be used for defining cold formed frame design
groups; otherwise it is False.

SpecifiedForStaticNLActiveStage

This item is True if the group is specified to be used for defining stages for nonlinear static
analysis; otherwise it is False.

SpecifiedForBridgeResponseOutput

This item is True if the group is specified to be used for reporting bridge response output;
otherwise it is False.


SpecifiedForAutoSeismicOutput

This item is True if the group is specified to be used for reporting auto seismic loads; otherwise it
is False.

SpecifiedForAutoWindOutput

This item is True if the group is specified to be used for reporting auto wind loads; otherwise it is
False.

SpecifiedForMassAndWeight

This item is True if the group is specified to be used for reporting group masses and weight;
otherwise it is False.

## Remarks

The function returns zero if the group data is successfully set, otherwise it returns a nonzero value.

## VBA Example

Sub SetGroupData()
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

'define new group
ret = SapModel.GroupDef.SetGroup("Group1")

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub


## Release Notes

Initial release in version 11.00.

## See Also

GetGroup


