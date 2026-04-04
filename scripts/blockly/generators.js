// ===========================================================
// SAP2000 Python Generators - Auto-generated
// Generated: 2026-04-04 01:14
// DO NOT EDIT MANUALLY
// ===========================================================

function registerSAP2000Generators(pythonGenerator) {

  // File.NewBlank
  pythonGenerator.forBlock['sap_SapModel_File_NewBlank'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.File.NewBlank()\n';
    code += 'assert ret == 0, "File.NewBlank failed"\n';
    return code;
  };

  // PropMaterial.SetMaterial
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_SetMaterial'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatType = block.getFieldValue('MatType') || '2';
    var code = '';
    code += 'ret = SapModel.PropMaterial.SetMaterial(' + v_Name + ', ' + v_MatType + ')\n';
    code += 'assert ret == 0, "PropMaterial.SetMaterial failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.SetMPIsotropic
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_SetMPIsotropic'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_E = block.getFieldValue('E') || '0';
    var v_U = block.getFieldValue('U') || '0';
    var v_A = "'" + (block.getFieldValue('A') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropMaterial.SetMPIsotropic(' + v_Name + ', ' + v_E + ', ' + v_U + ', ' + v_A + ')\n';
    code += 'assert ret == 0, "PropMaterial.SetMPIsotropic failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.SetWeightAndMass
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_SetWeightAndMass'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MyType = block.getFieldValue('MyType') || '1';
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropMaterial.SetWeightAndMass(' + v_Name + ', ' + v_MyType + ', ' + v_Value + ')\n';
    code += 'assert ret == 0, "PropMaterial.SetWeightAndMass failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetRectangle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetRectangle'] = function(block, generator) {
    var v_Name = block.getFieldValue('Name') || '0';
    var v_MatProp = block.getFieldValue('MatProp') || '0';
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetRectangle(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ')\n';
    code += 'assert ret == 0, "PropFrame.SetRectangle failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetCircle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetCircle'] = function(block, generator) {
    var v_Name = block.getFieldValue('Name') || '0';
    var v_MatProp = block.getFieldValue('MatProp') || '0';
    var v_T3 = block.getFieldValue('T3') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetCircle(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ')\n';
    code += 'assert ret == 0, "PropFrame.SetCircle failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetISection
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetISection'] = function(block, generator) {
    var v_Name = block.getFieldValue('Name') || '0';
    var v_MatProp = block.getFieldValue('MatProp') || '0';
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var v_TF = block.getFieldValue('TF') || '0';
    var v_TW = block.getFieldValue('TW') || '0';
    var v_T2B = block.getFieldValue('T2B') || '0';
    var v_TFB = block.getFieldValue('TFB') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetISection(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ', ' + v_TF + ', ' + v_TW + ', ' + v_T2B + ', ' + v_TFB + ')\n';
    code += 'assert ret == 0, "PropFrame.SetISection failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetTube
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetTube'] = function(block, generator) {
    var v_Name = block.getFieldValue('Name') || '0';
    var v_MatProp = block.getFieldValue('MatProp') || '0';
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var v_TF = block.getFieldValue('TF') || '0';
    var v_TW = block.getFieldValue('TW') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetTube(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ', ' + v_TF + ', ' + v_TW + ')\n';
    code += 'assert ret == 0, "PropFrame.SetTube failed: " + str(ret)\n';
    return code;
  };

  // PointObj.AddCartesian
  pythonGenerator.forBlock['sap_SapModel_PointObj_AddCartesian'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PointObj.AddCartesian()\n';
    code += 'assert ret == 0, "PointObj.AddCartesian failed"\n';
    return code;
  };

  // FrameObj.AddByPoint
  pythonGenerator.forBlock['sap_SapModel_FrameObj_AddByPoint'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.AddByPoint()\n';
    code += 'assert ret == 0, "FrameObj.AddByPoint failed"\n';
    return code;
  };

  // FrameObj.AddByCoord
  pythonGenerator.forBlock['sap_SapModel_FrameObj_AddByCoord'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.AddByCoord()\n';
    code += 'assert ret == 0, "FrameObj.AddByCoord failed"\n';
    return code;
  };

  // FrameObj.SetSection
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetSection'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.SetSection()\n';
    code += 'assert ret == 0, "FrameObj.SetSection failed"\n';
    return code;
  };

  // PropArea.SetShell_1
  pythonGenerator.forBlock['sap_SapModel_PropArea_SetShell_1'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropArea.SetShell_1()\n';
    code += 'assert ret == 0, "PropArea.SetShell_1 failed"\n';
    return code;
  };

  // AreaObj.AddByCoord
  pythonGenerator.forBlock['sap_SapModel_AreaObj_AddByCoord'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.AreaObj.AddByCoord()\n';
    code += 'assert ret == 0, "AreaObj.AddByCoord failed"\n';
    return code;
  };

  // AreaObj.SetSpring
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetSpring'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.AreaObj.SetSpring()\n';
    code += 'assert ret == 0, "AreaObj.SetSpring failed"\n';
    return code;
  };

  // LoadPatterns.Add
  pythonGenerator.forBlock['sap_SapModel_LoadPatterns_Add'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadPatterns.Add()\n';
    code += 'assert ret == 0, "LoadPatterns.Add failed"\n';
    return code;
  };

  // FuncRS.SetUser
  pythonGenerator.forBlock['sap_SapModel_Func_FuncRS_SetUser'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Func.FuncRS.SetUser()\n';
    code += 'assert ret == 0, "FuncRS.SetUser failed"\n';
    return code;
  };

  // ResponseSpectrum.SetLoads
  pythonGenerator.forBlock['sap_SapModel_LoadCases_ResponseSpectrum_SetLoads'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadCases.ResponseSpectrum.SetLoads()\n';
    code += 'assert ret == 0, "ResponseSpectrum.SetLoads failed"\n';
    return code;
  };

  // RespCombo.Add
  pythonGenerator.forBlock['sap_SapModel_RespCombo_Add'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.Add()\n';
    code += 'assert ret == 0, "RespCombo.Add failed"\n';
    return code;
  };

  // RespCombo.SetCaseList
  pythonGenerator.forBlock['sap_SapModel_RespCombo_SetCaseList'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.SetCaseList()\n';
    code += 'assert ret == 0, "RespCombo.SetCaseList failed"\n';
    return code;
  };

  // RespCombo.GetCaseList
  pythonGenerator.forBlock['sap_SapModel_RespCombo_GetCaseList'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.GetCaseList()\n';
    code += 'assert ret == 0, "RespCombo.GetCaseList failed"\n';
    return code;
  };

  // EditArea.Divide
  pythonGenerator.forBlock['sap_SapModel_EditArea_Divide'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.EditArea.Divide()\n';
    code += 'assert ret == 0, "EditArea.Divide failed"\n';
    return code;
  };

  // SelectObj.CoordinateRange
  pythonGenerator.forBlock['sap_SapModel_SelectObj_CoordinateRange'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.SelectObj.CoordinateRange()\n';
    code += 'assert ret == 0, "SelectObj.CoordinateRange failed"\n';
    return code;
  };

  // ConstraintDef.SetBody
  pythonGenerator.forBlock['sap_SapModel_ConstraintDef_SetBody'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.ConstraintDef.SetBody()\n';
    code += 'assert ret == 0, "ConstraintDef.SetBody failed"\n';
    return code;
  };

  // FrameObj.SetTCLimits
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetTCLimits'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.SetTCLimits()\n';
    code += 'assert ret == 0, "FrameObj.SetTCLimits failed"\n';
    return code;
  };

  // PointObj.SetRestraint
  pythonGenerator.forBlock['sap_SapModel_PointObj_SetRestraint'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PointObj.SetRestraint()\n';
    code += 'assert ret == 0, "PointObj.SetRestraint failed"\n';
    return code;
  };

  // FrameObj.SetLoadDistributed
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetLoadDistributed'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.SetLoadDistributed()\n';
    code += 'assert ret == 0, "FrameObj.SetLoadDistributed failed"\n';
    return code;
  };

  // PointObj.SetLoadForce
  pythonGenerator.forBlock['sap_SapModel_PointObj_SetLoadForce'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PointObj.SetLoadForce()\n';
    code += 'assert ret == 0, "PointObj.SetLoadForce failed"\n';
    return code;
  };

  // DatabaseTables.GetAllTables
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetAllTables'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetAllTables()\n';
    code += 'assert ret == 0, "DatabaseTables.GetAllTables failed"\n';
    return code;
  };

  // DatabaseTables.GetAvailableTables
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetAvailableTables'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetAvailableTables()\n';
    code += 'assert ret == 0, "DatabaseTables.GetAvailableTables failed"\n';
    return code;
  };

  // DatabaseTables.GetAllFieldsInTable
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetAllFieldsInTable'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetAllFieldsInTable()\n';
    code += 'assert ret == 0, "DatabaseTables.GetAllFieldsInTable failed"\n';
    return code;
  };

  // DatabaseTables.GetObsoleteTableKeyList
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetObsoleteTableKeyList'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetObsoleteTableKeyList()\n';
    code += 'assert ret == 0, "DatabaseTables.GetObsoleteTableKeyList failed"\n';
    return code;
  };

  // DatabaseTables.GetTableForEditingArray
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForEditingArray'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForEditingArray()\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForEditingArray failed"\n';
    return code;
  };

  // DatabaseTables.CancelTableEditing
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_CancelTableEditing'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.CancelTableEditing()\n';
    code += 'assert ret == 0, "DatabaseTables.CancelTableEditing failed"\n';
    return code;
  };

  // DatabaseTables.SetTableForEditingArray
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetTableForEditingArray'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetTableForEditingArray()\n';
    code += 'assert ret == 0, "DatabaseTables.SetTableForEditingArray failed"\n';
    return code;
  };

  // DatabaseTables.ApplyEditedTables
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_ApplyEditedTables'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.ApplyEditedTables()\n';
    code += 'assert ret == 0, "DatabaseTables.ApplyEditedTables failed"\n';
    return code;
  };

  // DatabaseTables.GetTableForDisplayArray
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForDisplayArray'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForDisplayArray()\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForDisplayArray failed"\n';
    return code;
  };

  // DatabaseTables.GetTableForDisplayCSVFile
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForDisplayCSVFile'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForDisplayCSVFile()\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForDisplayCSVFile failed"\n';
    return code;
  };

  // DatabaseTables.GetTableForDisplayCSVString
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForDisplayCSVString'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForDisplayCSVString()\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForDisplayCSVString failed"\n';
    return code;
  };

  // DatabaseTables.GetTableForDisplayXMLString
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForDisplayXMLString'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForDisplayXMLString()\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForDisplayXMLString failed"\n';
    return code;
  };

  // DatabaseTables.GetTableForEditingCSVFile
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForEditingCSVFile'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForEditingCSVFile()\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForEditingCSVFile failed"\n';
    return code;
  };

  // DatabaseTables.GetTableForEditingCSVString
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForEditingCSVString'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForEditingCSVString()\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForEditingCSVString failed"\n';
    return code;
  };

  // DatabaseTables.SetTableForEditingCSVFile
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetTableForEditingCSVFile'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetTableForEditingCSVFile()\n';
    code += 'assert ret == 0, "DatabaseTables.SetTableForEditingCSVFile failed"\n';
    return code;
  };

  // DatabaseTables.SetTableForEditingCSVString
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetTableForEditingCSVString'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetTableForEditingCSVString()\n';
    code += 'assert ret == 0, "DatabaseTables.SetTableForEditingCSVString failed"\n';
    return code;
  };

  // DatabaseTables.GetLoadCasesSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetLoadCasesSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetLoadCasesSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetLoadCasesSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetLoadCasesSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetLoadCasesSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetLoadCasesSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetLoadCombinationsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetLoadCombinationsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetLoadCombinationsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetLoadCombinationsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetLoadCombinationsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetLoadCombinationsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetLoadCombinationsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetLoadPatternsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetLoadPatternsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetLoadPatternsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetLoadPatternsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetLoadPatternsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetLoadPatternsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetLoadPatternsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetElementVirtualWorkNamedSetsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetElementVirtualWorkNamedSetsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetGeneralizedDisplacementsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetGeneralizedDisplacementsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetJointResponseSpectraNamedSetsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetJointResponseSpectraNamedSetsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetPlotFunctionTracesNamedSetsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetPlotFunctionTracesNamedSetsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetPushoverNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetPushoverNamedSetsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetPushoverNamedSetsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetPushoverNamedSetsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetPushoverNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetPushoverNamedSetsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetPushoverNamedSetsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetPushoverNamedSetsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetSectionCutsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetSectionCutsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetSectionCutsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetSectionCutsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetSectionCutsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetSectionCutsSelectedForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetSectionCutsSelectedForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetSectionCutsSelectedForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.GetTableOutputOptionsForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableOutputOptionsForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableOutputOptionsForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableOutputOptionsForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.SetTableOutputOptionsForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetTableOutputOptionsForDisplay'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetTableOutputOptionsForDisplay()\n';
    code += 'assert ret == 0, "DatabaseTables.SetTableOutputOptionsForDisplay failed"\n';
    return code;
  };

  // DatabaseTables.ShowTablesInExcel
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_ShowTablesInExcel'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DatabaseTables.ShowTablesInExcel()\n';
    code += 'assert ret == 0, "DatabaseTables.ShowTablesInExcel failed"\n';
    return code;
  };

  // FrameObj.GetLoadDistributed
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetLoadDistributed'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.GetLoadDistributed()\n';
    code += 'assert ret == 0, "FrameObj.GetLoadDistributed failed"\n';
    return code;
  };

  // FrameObj.SetLoadPoint
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetLoadPoint'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.SetLoadPoint()\n';
    code += 'assert ret == 0, "FrameObj.SetLoadPoint failed"\n';
    return code;
  };

  // AreaObj.SetLoadUniform
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetLoadUniform'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.AreaObj.SetLoadUniform()\n';
    code += 'assert ret == 0, "AreaObj.SetLoadUniform failed"\n';
    return code;
  };

  // Results.BaseReact
  pythonGenerator.forBlock['sap_SapModel_Results_BaseReact'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Results.BaseReact()\n';
    code += 'assert ret == 0, "Results.BaseReact failed"\n';
    return code;
  };

  // AreaObj.SetLoadGravity
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetLoadGravity'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.AreaObj.SetLoadGravity()\n';
    code += 'assert ret == 0, "AreaObj.SetLoadGravity failed"\n';
    return code;
  };

  // FrameObj.SetReleases
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetReleases'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.SetReleases()\n';
    code += 'assert ret == 0, "FrameObj.SetReleases failed"\n';
    return code;
  };

  // FrameObj.GetReleases
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetReleases'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.GetReleases()\n';
    code += 'assert ret == 0, "FrameObj.GetReleases failed"\n';
    return code;
  };

  // FrameObj.SetInsertionPoint_1
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetInsertionPoint_1'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.SetInsertionPoint_1()\n';
    code += 'assert ret == 0, "FrameObj.SetInsertionPoint_1 failed"\n';
    return code;
  };

  // FrameObj.SetLocalAxes
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetLocalAxes'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.SetLocalAxes()\n';
    code += 'assert ret == 0, "FrameObj.SetLocalAxes failed"\n';
    return code;
  };

  // GroupDef.SetGroup
  pythonGenerator.forBlock['sap_SapModel_GroupDef_SetGroup'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.GroupDef.SetGroup()\n';
    code += 'assert ret == 0, "GroupDef.SetGroup failed"\n';
    return code;
  };

  // GroupDef.GetNameList
  pythonGenerator.forBlock['sap_SapModel_GroupDef_GetNameList'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.GroupDef.GetNameList()\n';
    code += 'assert ret == 0, "GroupDef.GetNameList failed"\n';
    return code;
  };

  // FrameObj.SetGroupAssign
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetGroupAssign'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.SetGroupAssign()\n';
    code += 'assert ret == 0, "FrameObj.SetGroupAssign failed"\n';
    return code;
  };

  // AreaObj.SetGroupAssign
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetGroupAssign'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.AreaObj.SetGroupAssign()\n';
    code += 'assert ret == 0, "AreaObj.SetGroupAssign failed"\n';
    return code;
  };

  // ConstraintDef.SetDiaphragm
  pythonGenerator.forBlock['sap_SapModel_ConstraintDef_SetDiaphragm'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.ConstraintDef.SetDiaphragm()\n';
    code += 'assert ret == 0, "ConstraintDef.SetDiaphragm failed"\n';
    return code;
  };

  // ConstraintDef.GetDiaphragm
  pythonGenerator.forBlock['sap_SapModel_ConstraintDef_GetDiaphragm'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.ConstraintDef.GetDiaphragm()\n';
    code += 'assert ret == 0, "ConstraintDef.GetDiaphragm failed"\n';
    return code;
  };

  // Results.AreaStressShell
  pythonGenerator.forBlock['sap_SapModel_Results_AreaStressShell'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Results.AreaStressShell()\n';
    code += 'assert ret == 0, "Results.AreaStressShell failed"\n';
    return code;
  };

  // Results.ModalPeriod
  pythonGenerator.forBlock['sap_SapModel_Results_ModalPeriod'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Results.ModalPeriod()\n';
    code += 'assert ret == 0, "Results.ModalPeriod failed"\n';
    return code;
  };

  // Results.ModalParticipatingMassRatios
  pythonGenerator.forBlock['sap_SapModel_Results_ModalParticipatingMassRatios'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Results.ModalParticipatingMassRatios()\n';
    code += 'assert ret == 0, "Results.ModalParticipatingMassRatios failed"\n';
    return code;
  };

  // Results.ModeShape
  pythonGenerator.forBlock['sap_SapModel_Results_ModeShape'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Results.ModeShape()\n';
    code += 'assert ret == 0, "Results.ModeShape failed"\n';
    return code;
  };

  // Analyze.SetActiveDOF
  pythonGenerator.forBlock['sap_SapModel_Analyze_SetActiveDOF'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Analyze.SetActiveDOF()\n';
    code += 'assert ret == 0, "Analyze.SetActiveDOF failed"\n';
    return code;
  };

  // Analyze.GetActiveDOF
  pythonGenerator.forBlock['sap_SapModel_Analyze_GetActiveDOF'] = function(block, generator) {
    var code = '';
    code += 'raw = SapModel.Analyze.GetActiveDOF(' + '' + ')\n';
    code += 'dof_ = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "Analyze.GetActiveDOF failed: " + str(ret_code)\n';
    return code;
  };

  // Analyze.GetCaseStatus
  pythonGenerator.forBlock['sap_SapModel_Analyze_GetCaseStatus'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Analyze.GetCaseStatus()\n';
    code += 'assert ret == 0, "Analyze.GetCaseStatus failed"\n';
    return code;
  };

  // File.OpenFile
  pythonGenerator.forBlock['sap_SapModel_File_OpenFile'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.File.OpenFile()\n';
    code += 'assert ret == 0, "File.OpenFile failed"\n';
    return code;
  };

  // PropLink.SetLinear
  pythonGenerator.forBlock['sap_SapModel_PropLink_SetLinear'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropLink.SetLinear()\n';
    code += 'assert ret == 0, "PropLink.SetLinear failed"\n';
    return code;
  };

  // LinkObj.AddByPoint
  pythonGenerator.forBlock['sap_SapModel_LinkObj_AddByPoint'] = function(block, generator) {
    var code = '';
    code += 'raw = SapModel.LinkObj.AddByPoint(' + '' + ')\n';
    code += 'name_assigned = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "LinkObj.AddByPoint failed: " + str(ret_code)\n';
    return code;
  };

  // LinkObj.AddByCoord
  pythonGenerator.forBlock['sap_SapModel_LinkObj_AddByCoord'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LinkObj.AddByCoord()\n';
    code += 'assert ret == 0, "LinkObj.AddByCoord failed"\n';
    return code;
  };

  // AreaObj.SetProperty
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetProperty'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.AreaObj.SetProperty()\n';
    code += 'assert ret == 0, "AreaObj.SetProperty failed"\n';
    return code;
  };

  // PropArea.GetShell_1
  pythonGenerator.forBlock['sap_SapModel_PropArea_GetShell_1'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropArea.GetShell_1()\n';
    code += 'assert ret == 0, "PropArea.GetShell_1 failed"\n';
    return code;
  };

  // PropMaterial.SetOSteel_1
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_SetOSteel_1'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Fy = "'" + (block.getFieldValue('Fy') || '') + "'";
    var v_Fu = "'" + (block.getFieldValue('Fu') || '') + "'";
    var v_EFy = block.getFieldValue('EFy') || '0';
    var v_EFu = block.getFieldValue('EFu') || '0';
    var v_SSType = "'" + (block.getFieldValue('SSType') || '') + "'";
    var v_SSHysType = "'" + (block.getFieldValue('SSHysType') || '') + "'";
    var v_StrainAtHardening = "'" + (block.getFieldValue('StrainAtHardening') || '') + "'";
    var v_StrainAtMaxStress = "'" + (block.getFieldValue('StrainAtMaxStress') || '') + "'";
    var v_StrainAtRupture = "'" + (block.getFieldValue('StrainAtRupture') || '') + "'";
    var v_FinalSlope = "'" + (block.getFieldValue('FinalSlope') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropMaterial.SetOSteel_1(' + v_Name + ', ' + v_Fy + ', ' + v_Fu + ', ' + v_EFy + ', ' + v_EFu + ', ' + v_SSType + ', ' + v_SSHysType + ', ' + v_StrainAtHardening + ', ' + v_StrainAtMaxStress + ', ' + v_StrainAtRupture + ', ' + v_FinalSlope + ')\n';
    code += 'assert ret == 0, "PropMaterial.SetOSteel_1 failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.SetOConcrete_1
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_SetOConcrete_1'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_fc = "'" + (block.getFieldValue('fc') || '') + "'";
    var v_IsLightweight = "'" + (block.getFieldValue('IsLightweight') || '') + "'";
    var v_FcsFactor = "'" + (block.getFieldValue('FcsFactor') || '') + "'";
    var v_SSType = "'" + (block.getFieldValue('SSType') || '') + "'";
    var v_SSHysType = "'" + (block.getFieldValue('SSHysType') || '') + "'";
    var v_StrainAtfc = "'" + (block.getFieldValue('StrainAtfc') || '') + "'";
    var v_StrainUltimate = "'" + (block.getFieldValue('StrainUltimate') || '') + "'";
    var v_FinalSlope = "'" + (block.getFieldValue('FinalSlope') || '') + "'";
    var v_FrictionAngle = "'" + (block.getFieldValue('FrictionAngle') || '') + "'";
    var v_DilatationalAngle = block.getFieldValue('DilatationalAngle') || '0';
    var code = '';
    code += 'ret = SapModel.PropMaterial.SetOConcrete_1(' + v_Name + ', ' + v_fc + ', ' + v_IsLightweight + ', ' + v_FcsFactor + ', ' + v_SSType + ', ' + v_SSHysType + ', ' + v_StrainAtfc + ', ' + v_StrainUltimate + ', ' + v_FinalSlope + ', ' + v_FrictionAngle + ', ' + v_DilatationalAngle + ')\n';
    code += 'assert ret == 0, "PropMaterial.SetOConcrete_1 failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.GetMaterial
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_GetMaterial'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatType = block.getFieldValue('MatType') || '2';
    var code = '';
    code += 'ret = SapModel.PropMaterial.GetMaterial(' + v_Name + ', ' + v_MatType + ')\n';
    code += 'assert ret == 0, "PropMaterial.GetMaterial failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.GetMPIsotropic
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_GetMPIsotropic'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_E = block.getFieldValue('E') || '0';
    var v_U = block.getFieldValue('U') || '0';
    var v_A = "'" + (block.getFieldValue('A') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropMaterial.GetMPIsotropic(' + v_Name + ', ' + v_E + ', ' + v_U + ', ' + v_A + ')\n';
    code += 'assert ret == 0, "PropMaterial.GetMPIsotropic failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetAngle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetAngle'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.SetAngle()\n';
    code += 'assert ret == 0, "PropFrame.SetAngle failed"\n';
    return code;
  };

  // PropFrame.SetChannel
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetChannel'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.SetChannel()\n';
    code += 'assert ret == 0, "PropFrame.SetChannel failed"\n';
    return code;
  };

  // PropFrame.SetPipe
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetPipe'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.SetPipe()\n';
    code += 'assert ret == 0, "PropFrame.SetPipe failed"\n';
    return code;
  };

  // PropFrame.GetRectangle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_GetRectangle'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.GetRectangle()\n';
    code += 'assert ret == 0, "PropFrame.GetRectangle failed"\n';
    return code;
  };

  // PropFrame.GetCircle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_GetCircle'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.GetCircle()\n';
    code += 'assert ret == 0, "PropFrame.GetCircle failed"\n';
    return code;
  };

  // PropFrame.GetISection
  pythonGenerator.forBlock['sap_SapModel_PropFrame_GetISection'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.GetISection()\n';
    code += 'assert ret == 0, "PropFrame.GetISection failed"\n';
    return code;
  };

  // DesignSteel.SetComboStrength
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_SetComboStrength'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignSteel.SetComboStrength()\n';
    code += 'assert ret == 0, "DesignSteel.SetComboStrength failed"\n';
    return code;
  };

  // DesignSteel.GetComboStrength
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_GetComboStrength'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignSteel.GetComboStrength()\n';
    code += 'assert ret == 0, "DesignSteel.GetComboStrength failed"\n';
    return code;
  };

  // DesignSteel.SetComboDeflection
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_SetComboDeflection'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignSteel.SetComboDeflection()\n';
    code += 'assert ret == 0, "DesignSteel.SetComboDeflection failed"\n';
    return code;
  };

  // DesignSteel.GetCode
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_GetCode'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignSteel.GetCode()\n';
    code += 'assert ret == 0, "DesignSteel.GetCode failed"\n';
    return code;
  };

  // DesignSteel.SetCode
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_SetCode'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignSteel.SetCode()\n';
    code += 'assert ret == 0, "DesignSteel.SetCode failed"\n';
    return code;
  };

  // DesignSteel.DeleteResults
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_DeleteResults'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignSteel.DeleteResults()\n';
    code += 'assert ret == 0, "DesignSteel.DeleteResults failed"\n';
    return code;
  };

  // DesignConcrete.SetComboStrength
  pythonGenerator.forBlock['sap_SapModel_DesignConcrete_SetComboStrength'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignConcrete.SetComboStrength()\n';
    code += 'assert ret == 0, "DesignConcrete.SetComboStrength failed"\n';
    return code;
  };

  // DesignConcrete.GetCode
  pythonGenerator.forBlock['sap_SapModel_DesignConcrete_GetCode'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignConcrete.GetCode()\n';
    code += 'assert ret == 0, "DesignConcrete.GetCode failed"\n';
    return code;
  };

  // DesignConcrete.SetCode
  pythonGenerator.forBlock['sap_SapModel_DesignConcrete_SetCode'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.DesignConcrete.SetCode()\n';
    code += 'assert ret == 0, "DesignConcrete.SetCode failed"\n';
    return code;
  };

  // RespCombo.Delete
  pythonGenerator.forBlock['sap_SapModel_RespCombo_Delete'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.Delete()\n';
    code += 'assert ret == 0, "RespCombo.Delete failed"\n';
    return code;
  };

  // RespCombo.ChangeName
  pythonGenerator.forBlock['sap_SapModel_RespCombo_ChangeName'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.ChangeName()\n';
    code += 'assert ret == 0, "RespCombo.ChangeName failed"\n';
    return code;
  };

  // RespCombo.Count
  pythonGenerator.forBlock['sap_SapModel_RespCombo_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.Count()\n';
    code += 'assert ret == 0, "RespCombo.Count failed"\n';
    return code;
  };

  // RespCombo.SetTypeOAPI
  pythonGenerator.forBlock['sap_SapModel_RespCombo_SetTypeOAPI'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.SetTypeOAPI()\n';
    code += 'assert ret == 0, "RespCombo.SetTypeOAPI failed"\n';
    return code;
  };

  // RespCombo.GetTypeOAPI
  pythonGenerator.forBlock['sap_SapModel_RespCombo_GetTypeOAPI'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.GetTypeOAPI()\n';
    code += 'assert ret == 0, "RespCombo.GetTypeOAPI failed"\n';
    return code;
  };

  // RespCombo.DeleteCase
  pythonGenerator.forBlock['sap_SapModel_RespCombo_DeleteCase'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.DeleteCase()\n';
    code += 'assert ret == 0, "RespCombo.DeleteCase failed"\n';
    return code;
  };

  // RespCombo.AddDesignDefaultCombos
  pythonGenerator.forBlock['sap_SapModel_RespCombo_AddDesignDefaultCombos'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.RespCombo.AddDesignDefaultCombos()\n';
    code += 'assert ret == 0, "RespCombo.AddDesignDefaultCombos failed"\n';
    return code;
  };

  // ResponseSpectrum.SetDampConstant
  pythonGenerator.forBlock['sap_SapModel_LoadCases_ResponseSpectrum_SetDampConstant'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant()\n';
    code += 'assert ret == 0, "ResponseSpectrum.SetDampConstant failed"\n';
    return code;
  };

  // LoadCases.Count
  pythonGenerator.forBlock['sap_SapModel_LoadCases_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadCases.Count()\n';
    code += 'assert ret == 0, "LoadCases.Count failed"\n';
    return code;
  };

  // LoadCases.Delete
  pythonGenerator.forBlock['sap_SapModel_LoadCases_Delete'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadCases.Delete()\n';
    code += 'assert ret == 0, "LoadCases.Delete failed"\n';
    return code;
  };

  // LoadCases.ChangeName
  pythonGenerator.forBlock['sap_SapModel_LoadCases_ChangeName'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadCases.ChangeName()\n';
    code += 'assert ret == 0, "LoadCases.ChangeName failed"\n';
    return code;
  };

  // LoadPatterns.Count
  pythonGenerator.forBlock['sap_SapModel_LoadPatterns_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadPatterns.Count()\n';
    code += 'assert ret == 0, "LoadPatterns.Count failed"\n';
    return code;
  };

  // LoadPatterns.Delete
  pythonGenerator.forBlock['sap_SapModel_LoadPatterns_Delete'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadPatterns.Delete()\n';
    code += 'assert ret == 0, "LoadPatterns.Delete failed"\n';
    return code;
  };

  // LoadPatterns.ChangeName
  pythonGenerator.forBlock['sap_SapModel_LoadPatterns_ChangeName'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LoadPatterns.ChangeName()\n';
    code += 'assert ret == 0, "LoadPatterns.ChangeName failed"\n';
    return code;
  };

  // SourceMass.SetMassSource
  pythonGenerator.forBlock['sap_SapModel_SourceMass_SetMassSource'] = function(block, generator) {
    var code = '';
    code += 'raw = SapModel.SourceMass.SetMassSource(' + '' + ')\n';
    code += 'loadpat_ = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "SourceMass.SetMassSource failed: " + str(ret_code)\n';
    return code;
  };

  // SourceMass.Count
  pythonGenerator.forBlock['sap_SapModel_SourceMass_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.SourceMass.Count()\n';
    code += 'assert ret == 0, "SourceMass.Count failed"\n';
    return code;
  };

  // SourceMass.GetMassSource
  pythonGenerator.forBlock['sap_SapModel_SourceMass_GetMassSource'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.SourceMass.GetMassSource()\n';
    code += 'assert ret == 0, "SourceMass.GetMassSource failed"\n';
    return code;
  };

  // SourceMass.GetDefault
  pythonGenerator.forBlock['sap_SapModel_SourceMass_GetDefault'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.SourceMass.GetDefault()\n';
    code += 'assert ret == 0, "SourceMass.GetDefault failed"\n';
    return code;
  };

  // FrameObj.SetModifiers
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetModifiers'] = function(block, generator) {
    var code = '';
    code += 'raw = SapModel.FrameObj.SetModifiers(' + '' + ')\n';
    code += 'value_8 = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "FrameObj.SetModifiers failed: " + str(ret_code)\n';
    return code;
  };

  // FrameObj.GetModifiers
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetModifiers'] = function(block, generator) {
    var code = '';
    code += 'raw = SapModel.FrameObj.GetModifiers(' + '' + ')\n';
    code += 'value_8 = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "FrameObj.GetModifiers failed: " + str(ret_code)\n';
    return code;
  };

  // PropArea.SetModifiers
  pythonGenerator.forBlock['sap_SapModel_PropArea_SetModifiers'] = function(block, generator) {
    var code = '';
    code += 'raw = SapModel.PropArea.SetModifiers(' + '' + ')\n';
    code += 'value_10 = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "PropArea.SetModifiers failed: " + str(ret_code)\n';
    return code;
  };

  // PropArea.GetModifiers
  pythonGenerator.forBlock['sap_SapModel_PropArea_GetModifiers'] = function(block, generator) {
    var code = '';
    code += 'raw = SapModel.PropArea.GetModifiers(' + '' + ')\n';
    code += 'value_10 = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "PropArea.GetModifiers failed: " + str(ret_code)\n';
    return code;
  };

  // PropFrame.ChangeName
  pythonGenerator.forBlock['sap_SapModel_PropFrame_ChangeName'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.ChangeName()\n';
    code += 'assert ret == 0, "PropFrame.ChangeName failed"\n';
    return code;
  };

  // PropFrame.Count
  pythonGenerator.forBlock['sap_SapModel_PropFrame_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.Count()\n';
    code += 'assert ret == 0, "PropFrame.Count failed"\n';
    return code;
  };

  // PropFrame.Delete
  pythonGenerator.forBlock['sap_SapModel_PropFrame_Delete'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropFrame.Delete()\n';
    code += 'assert ret == 0, "PropFrame.Delete failed"\n';
    return code;
  };

  // PropMaterial.ChangeName
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_ChangeName'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropMaterial.ChangeName()\n';
    code += 'assert ret == 0, "PropMaterial.ChangeName failed"\n';
    return code;
  };

  // PropMaterial.Count
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropMaterial.Count()\n';
    code += 'assert ret == 0, "PropMaterial.Count failed"\n';
    return code;
  };

  // PropMaterial.Delete
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_Delete'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropMaterial.Delete()\n';
    code += 'assert ret == 0, "PropMaterial.Delete failed"\n';
    return code;
  };

  // PropLink.SetGap
  pythonGenerator.forBlock['sap_SapModel_PropLink_SetGap'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropLink.SetGap()\n';
    code += 'assert ret == 0, "PropLink.SetGap failed"\n';
    return code;
  };

  console.log('✅ SAP2000 Python generators registered');
}
