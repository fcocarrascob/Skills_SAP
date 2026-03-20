# RefreshView

## Syntax

SapObject.SapModel.View.RefreshView

## VB6 Procedure

Function RefreshView(Optional ByVal Window As Long = 0, Optional ByVal Zoom As Boolean
= True) As Long

## Parameters

Window

This is 0 meaning all windows or an existing window number. It indicates the window(s) to have
its view refreshed.

Zoom

If this item is True, the window zoom is maintained when the view is refreshed. If it is False, the
zoom returns to a default zoom.

## Remarks

This function refreshes the view for the specified window(s). It returns zero if the window views
are successfully refreshed, otherwise it returns a nonzero value.

See RefreshWindow and RefreshView for more information.

## VBA Example

Sub RefreshAllViews()
'dimension variables
Dim SapObject as cOAPI
Dim SapModel As cSapModel
Dim ret As Long
Dim Name As String

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

'add a frame object
ret = SapModel.FrameObj.AddByPoint("1", "6", Name)

'refresh view for all windows
ret = SapModel.View.RefreshView

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.

Modified optional argument Zoom to be ByVal in version 12.0.1.

## See Also

RefreshWindow

# RefreshWindow

## Syntax

SapObject.SapModel.View.RefreshWindow

## VB6 Procedure

Function RefreshWindow(Optional ByVal Window As Long = 0) As Long

## Parameters

Window

This is 0 meaning all windows or an existing window number. It indicates the window(s) to be
refreshed.

## Remarks


This function refreshes the specified window(s). It returns zero if the windows are successfully
refreshed, otherwise it returns a nonzero value.

See RefreshWindow and RefreshView for more information.

## VBA Example

Sub RefreshAllWindows()
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
ret = SapModel.File.New2DFrame(PortalFrame, 3, 124, 3, 200)

'add joint restraint
Redim Value(5)
For i = 0 to 5
Value(i) = True
Next i
ret = SapModel.PointObj.SetRestraint("1", Value)

'refresh all windows
ret = SapModel.View.RefreshWindow

'close Sap
SapObject.ApplicationExit False
Set SapModel = Nothing
Set SapObject = Nothing
End Sub

## Release Notes

Initial release in version 11.00.


## See Also

RefreshView


