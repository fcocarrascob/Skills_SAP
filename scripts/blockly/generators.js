// ===========================================================
// SAP2000 Python Generators - Auto-generated
// Generated: 2026-04-04 22:39
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
    var v_A = block.getFieldValue('A') || '0';
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
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetRectangle(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ')\n';
    code += 'assert ret == 0, "PropFrame.SetRectangle failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetCircle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetCircle'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetCircle(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ')\n';
    code += 'assert ret == 0, "PropFrame.SetCircle failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetISection
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetISection'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
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
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var v_TF = block.getFieldValue('TF') || '0';
    var v_TW = block.getFieldValue('TW') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetTube(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ', ' + v_TF + ', ' + v_TW + ')\n';
    code += 'assert ret == 0, "PropFrame.SetTube failed: " + str(ret)\n';
    return code;
  };

  // SapModel.InitializeNewModel
  pythonGenerator.forBlock['sap_SapModel_InitializeNewModel'] = function(block, generator) {
    var v_Units = block.getFieldValue('Units') || '6';
    var code = '';
    code += 'ret = SapModel.InitializeNewModel(' + v_Units + ')\n';
    code += 'assert ret == 0, "SapModel.InitializeNewModel failed: " + str(ret)\n';
    return code;
  };

  // SapModel.SetPresentUnits
  pythonGenerator.forBlock['sap_SapModel_SetPresentUnits'] = function(block, generator) {
    var v_Units = block.getFieldValue('Units') || '6';
    var code = '';
    code += 'ret = SapModel.SetPresentUnits(' + v_Units + ')\n';
    code += 'assert ret == 0, "SapModel.SetPresentUnits failed: " + str(ret)\n';
    return code;
  };

  // PointObj.AddCartesian
  pythonGenerator.forBlock['sap_SapModel_PointObj_AddCartesian'] = function(block, generator) {
    var v_X = block.getFieldValue('X') || '0';
    var v_Y = block.getFieldValue('Y') || '0';
    var v_Z = block.getFieldValue('Z') || '0';
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_UserName = "'" + (block.getFieldValue('UserName') || '') + "'";
    var v_MergeOff = "'" + (block.getFieldValue('MergeOff') || '') + "'";
    var v_MergeNumber = "'" + (block.getFieldValue('MergeNumber') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PointObj.AddCartesian(' + v_X + ', ' + v_Y + ', ' + v_Z + ', ' + v_Name + ', ' + v_UserName + ', ' + v_MergeOff + ', ' + v_MergeNumber + ')\n';
    code += 'assert ret == 0, "PointObj.AddCartesian failed: " + str(ret)\n';
    return code;
  };

  // PointObj.Count
  pythonGenerator.forBlock['sap_SapModel_PointObj_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PointObj.Count()\n';
    code += 'assert ret == 0, "PointObj.Count failed"\n';
    return code;
  };

  // PointObj.GetCoordCartesian
  pythonGenerator.forBlock['sap_SapModel_PointObj_GetCoordCartesian'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_X = block.getFieldValue('X') || '0';
    var v_Y = block.getFieldValue('Y') || '0';
    var v_Z = block.getFieldValue('Z') || '0';
    var code = '';
    code += 'ret = SapModel.PointObj.GetCoordCartesian(' + v_Name + ', ' + v_X + ', ' + v_Y + ', ' + v_Z + ')\n';
    code += 'assert ret == 0, "PointObj.GetCoordCartesian failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.AddByPoint
  pythonGenerator.forBlock['sap_SapModel_FrameObj_AddByPoint'] = function(block, generator) {
    var v_Point1 = "'" + (block.getFieldValue('Point1') || '') + "'";
    var v_Point2 = "'" + (block.getFieldValue('Point2') || '') + "'";
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_UserName = "'" + (block.getFieldValue('UserName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.AddByPoint(' + v_Point1 + ', ' + v_Point2 + ', ' + v_Name + ', ' + v_PropName + ', ' + v_UserName + ')\n';
    code += 'assert ret == 0, "FrameObj.AddByPoint failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.Count
  pythonGenerator.forBlock['sap_SapModel_FrameObj_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.FrameObj.Count()\n';
    code += 'assert ret == 0, "FrameObj.Count failed"\n';
    return code;
  };

  // FrameObj.GetPoints
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetPoints'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Point1 = "'" + (block.getFieldValue('Point1') || '') + "'";
    var v_Point2 = "'" + (block.getFieldValue('Point2') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.GetPoints(' + v_Name + ', ' + v_Point1 + ', ' + v_Point2 + ')\n';
    code += 'assert ret == 0, "FrameObj.GetPoints failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.AddByCoord
  pythonGenerator.forBlock['sap_SapModel_FrameObj_AddByCoord'] = function(block, generator) {
    var v_x1 = block.getFieldValue('x1') || '0';
    var v_y1 = block.getFieldValue('y1') || '0';
    var v_z1 = block.getFieldValue('z1') || '0';
    var v_x2 = block.getFieldValue('x2') || '0';
    var v_y2 = block.getFieldValue('y2') || '0';
    var v_z2 = block.getFieldValue('z2') || '0';
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_UserName = "'" + (block.getFieldValue('UserName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.AddByCoord(' + v_x1 + ', ' + v_y1 + ', ' + v_z1 + ', ' + v_x2 + ', ' + v_y2 + ', ' + v_z2 + ', ' + v_Name + ', ' + v_PropName + ', ' + v_UserName + ')\n';
    code += 'assert ret == 0, "FrameObj.AddByCoord failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetSection
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetSection'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var v_SAuto = "'" + (block.getFieldValue('SAuto') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.SetSection(' + v_Name + ', ' + v_PropName + ', ' + v_ItemType + ', ' + v_SAuto + ')\n';
    code += 'assert ret == 0, "FrameObj.SetSection failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.GetSection
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetSection'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_SAuto = "'" + (block.getFieldValue('SAuto') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.GetSection(' + v_Name + ', ' + v_PropName + ', ' + v_SAuto + ')\n';
    code += 'assert ret == 0, "FrameObj.GetSection failed: " + str(ret)\n';
    return code;
  };

  // PropArea.SetShell_1
  pythonGenerator.forBlock['sap_SapModel_PropArea_SetShell_1'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ShellType = block.getFieldValue('ShellType') || '1';
    var v_IncludeDrillingDOF = "'" + (block.getFieldValue('IncludeDrillingDOF') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_MatAng = "'" + (block.getFieldValue('MatAng') || '') + "'";
    var v_Thickness = "'" + (block.getFieldValue('Thickness') || '') + "'";
    var v_Bending = "'" + (block.getFieldValue('Bending') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropArea.SetShell_1(' + v_Name + ', ' + v_ShellType + ', ' + v_IncludeDrillingDOF + ', ' + v_MatProp + ', ' + v_MatAng + ', ' + v_Thickness + ', ' + v_Bending + ')\n';
    code += 'assert ret == 0, "PropArea.SetShell_1 failed: " + str(ret)\n';
    return code;
  };

  // PropArea.GetNameList
  pythonGenerator.forBlock['sap_SapModel_PropArea_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropArea.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "PropArea.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.AddByCoord
  pythonGenerator.forBlock['sap_SapModel_AreaObj_AddByCoord'] = function(block, generator) {
    var v_NumberPoints = "'" + (block.getFieldValue('NumberPoints') || '') + "'";
    var v_X = block.getFieldValue('X') || '0';
    var v_Y = block.getFieldValue('Y') || '0';
    var v_Z = block.getFieldValue('Z') || '0';
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_UserName = "'" + (block.getFieldValue('UserName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.AreaObj.AddByCoord(' + v_NumberPoints + ', ' + v_X + ', ' + v_Y + ', ' + v_Z + ', ' + v_Name + ', ' + v_PropName + ', ' + v_UserName + ')\n';
    code += 'assert ret == 0, "AreaObj.AddByCoord failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.Count
  pythonGenerator.forBlock['sap_SapModel_AreaObj_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.AreaObj.Count()\n';
    code += 'assert ret == 0, "AreaObj.Count failed"\n';
    return code;
  };

  // AreaObj.SetSpring
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetSpring'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MyType = block.getFieldValue('MyType') || '1';
    var v_S = "'" + (block.getFieldValue('S') || '') + "'";
    var v_SimpleSpringType = "'" + (block.getFieldValue('SimpleSpringType') || '') + "'";
    var v_LinkProp = "'" + (block.getFieldValue('LinkProp') || '') + "'";
    var v_Face = "'" + (block.getFieldValue('Face') || '') + "'";
    var v_SpringLocalOneType = "'" + (block.getFieldValue('SpringLocalOneType') || '') + "'";
    var v_Dir = block.getFieldValue('Dir') || '10';
    var v_Outward = "'" + (block.getFieldValue('Outward') || '') + "'";
    var v_Vec = "'" + (block.getFieldValue('Vec') || '') + "'";
    var v_Ang = "'" + (block.getFieldValue('Ang') || '') + "'";
    var v_Replace = block.getFieldValue('Replace') === 'TRUE' ? 'True' : 'False';
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.AreaObj.SetSpring(' + v_Name + ', ' + v_MyType + ', ' + v_S + ', ' + v_SimpleSpringType + ', ' + v_LinkProp + ', ' + v_Face + ', ' + v_SpringLocalOneType + ', ' + v_Dir + ', ' + v_Outward + ', ' + v_Vec + ', ' + v_Ang + ', ' + v_Replace + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "AreaObj.SetSpring failed: " + str(ret)\n';
    return code;
  };

  // LoadPatterns.Add
  pythonGenerator.forBlock['sap_SapModel_LoadPatterns_Add'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MyType = block.getFieldValue('MyType') || '1';
    var v_SelfWTMultiplier = "'" + (block.getFieldValue('SelfWTMultiplier') || '') + "'";
    var v_AddCase = "'" + (block.getFieldValue('AddCase') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadPatterns.Add(' + v_Name + ', ' + v_MyType + ', ' + v_SelfWTMultiplier + ', ' + v_AddCase + ')\n';
    code += 'assert ret == 0, "LoadPatterns.Add failed: " + str(ret)\n';
    return code;
  };

  // FuncRS.SetUser
  pythonGenerator.forBlock['sap_SapModel_Func_FuncRS_SetUser'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_Period = "'" + (block.getFieldValue('Period') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var v_DampRatio = "'" + (block.getFieldValue('DampRatio') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Func.FuncRS.SetUser(' + v_Name + ', ' + v_NumberItems + ', ' + v_Period + ', ' + v_Value + ', ' + v_DampRatio + ')\n';
    code += 'assert ret == 0, "FuncRS.SetUser failed: " + str(ret)\n';
    return code;
  };

  // FuncRS.GetUser
  pythonGenerator.forBlock['sap_SapModel_Func_FuncRS_GetUser'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_Period = "'" + (block.getFieldValue('Period') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var v_DampRatio = "'" + (block.getFieldValue('DampRatio') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Func.FuncRS.GetUser(' + v_Name + ', ' + v_NumberItems + ', ' + v_Period + ', ' + v_Value + ', ' + v_DampRatio + ')\n';
    code += 'assert ret == 0, "FuncRS.GetUser failed: " + str(ret)\n';
    return code;
  };

  // ResponseSpectrum.SetCase
  pythonGenerator.forBlock['sap_SapModel_LoadCases_ResponseSpectrum_SetCase'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadCases.ResponseSpectrum.SetCase(' + v_Name + ')\n';
    code += 'assert ret == 0, "ResponseSpectrum.SetCase failed: " + str(ret)\n';
    return code;
  };

  // ResponseSpectrum.SetLoads
  pythonGenerator.forBlock['sap_SapModel_LoadCases_ResponseSpectrum_SetLoads'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberLoads = "'" + (block.getFieldValue('NumberLoads') || '') + "'";
    var v_LoadName = "'" + (block.getFieldValue('LoadName') || '') + "'";
    var v_Func = "'" + (block.getFieldValue('Func') || '') + "'";
    var v_SF = "'" + (block.getFieldValue('SF') || '') + "'";
    var v_Ang = "'" + (block.getFieldValue('Ang') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(' + v_Name + ', ' + v_NumberLoads + ', ' + v_LoadName + ', ' + v_Func + ', ' + v_SF + ', ' + v_Ang + ')\n';
    code += 'assert ret == 0, "ResponseSpectrum.SetLoads failed: " + str(ret)\n';
    return code;
  };

  // ResponseSpectrum.GetLoads
  pythonGenerator.forBlock['sap_SapModel_LoadCases_ResponseSpectrum_GetLoads'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_LoadName = "'" + (block.getFieldValue('LoadName') || '') + "'";
    var v_Func = "'" + (block.getFieldValue('Func') || '') + "'";
    var v_SF = "'" + (block.getFieldValue('SF') || '') + "'";
    var v_Ang = "'" + (block.getFieldValue('Ang') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadCases.ResponseSpectrum.GetLoads(' + v_Name + ', ' + v_NumberItems + ', ' + v_LoadName + ', ' + v_Func + ', ' + v_SF + ', ' + v_Ang + ')\n';
    code += 'assert ret == 0, "ResponseSpectrum.GetLoads failed: " + str(ret)\n';
    return code;
  };

  // LoadCases.GetNameList
  pythonGenerator.forBlock['sap_SapModel_LoadCases_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var v_MyType = block.getFieldValue('MyType') || '1';
    var code = '';
    code += 'ret = SapModel.LoadCases.GetNameList(' + v_NumberNames + ', ' + v_MyName + ', ' + v_MyType + ')\n';
    code += 'assert ret == 0, "LoadCases.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.Add
  pythonGenerator.forBlock['sap_SapModel_RespCombo_Add'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ComboType = block.getFieldValue('ComboType') || '0';
    var code = '';
    code += 'ret = SapModel.RespCombo.Add(' + v_Name + ', ' + v_ComboType + ')\n';
    code += 'assert ret == 0, "RespCombo.Add failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.GetNameList
  pythonGenerator.forBlock['sap_SapModel_RespCombo_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.RespCombo.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "RespCombo.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.SetCaseList
  pythonGenerator.forBlock['sap_SapModel_RespCombo_SetCaseList'] = function(block, generator) {
    var v_ComboName = "'" + (block.getFieldValue('ComboName') || '') + "'";
    var v_CaseType = "'" + (block.getFieldValue('CaseType') || '') + "'";
    var v_CaseName = "'" + (block.getFieldValue('CaseName') || '') + "'";
    var v_ScaleFactor = "'" + (block.getFieldValue('ScaleFactor') || '') + "'";
    var code = '';
    code += 'ret = SapModel.RespCombo.SetCaseList(' + v_ComboName + ', ' + v_CaseType + ', ' + v_CaseName + ', ' + v_ScaleFactor + ')\n';
    code += 'assert ret == 0, "RespCombo.SetCaseList failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.GetCaseList
  pythonGenerator.forBlock['sap_SapModel_RespCombo_GetCaseList'] = function(block, generator) {
    var v_ComboName = "'" + (block.getFieldValue('ComboName') || '') + "'";
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_CaseType = "'" + (block.getFieldValue('CaseType') || '') + "'";
    var v_CaseName = "'" + (block.getFieldValue('CaseName') || '') + "'";
    var v_ScaleFactor = "'" + (block.getFieldValue('ScaleFactor') || '') + "'";
    var code = '';
    code += 'ret = SapModel.RespCombo.GetCaseList(' + v_ComboName + ', ' + v_NumberItems + ', ' + v_CaseType + ', ' + v_CaseName + ', ' + v_ScaleFactor + ')\n';
    code += 'assert ret == 0, "RespCombo.GetCaseList failed: " + str(ret)\n';
    return code;
  };

  // EditArea.Divide
  pythonGenerator.forBlock['sap_SapModel_EditArea_Divide'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MeshType = "'" + (block.getFieldValue('MeshType') || '') + "'";
    var v_NumAreas = "'" + (block.getFieldValue('NumAreas') || '') + "'";
    var v_AreaName = "'" + (block.getFieldValue('AreaName') || '') + "'";
    var v_N1 = "'" + (block.getFieldValue('N1') || '') + "'";
    var v_N2 = "'" + (block.getFieldValue('N2') || '') + "'";
    var v_MaxSize1 = "'" + (block.getFieldValue('MaxSize1') || '') + "'";
    var v_MaxSize2 = "'" + (block.getFieldValue('MaxSize2') || '') + "'";
    var v_PointOnEdgeFromLine = "'" + (block.getFieldValue('PointOnEdgeFromLine') || '') + "'";
    var v_PointOnEdgeFromPoint = "'" + (block.getFieldValue('PointOnEdgeFromPoint') || '') + "'";
    var v_ExtendCookieCutLines = "'" + (block.getFieldValue('ExtendCookieCutLines') || '') + "'";
    var v_Rotation = "'" + (block.getFieldValue('Rotation') || '') + "'";
    var v_MaxSizeGeneral = "'" + (block.getFieldValue('MaxSizeGeneral') || '') + "'";
    var v_LocalAxesOnEdge = "'" + (block.getFieldValue('LocalAxesOnEdge') || '') + "'";
    var v_LocalAxesOnFace = "'" + (block.getFieldValue('LocalAxesOnFace') || '') + "'";
    var v_RestraintsOnEdge = "'" + (block.getFieldValue('RestraintsOnEdge') || '') + "'";
    var v_RestraintsOnFace = "'" + (block.getFieldValue('RestraintsOnFace') || '') + "'";
    var v_Group = "'" + (block.getFieldValue('Group') || '') + "'";
    var v_SubMesh = "'" + (block.getFieldValue('SubMesh') || '') + "'";
    var v_SubMeshSize = "'" + (block.getFieldValue('SubMeshSize') || '') + "'";
    var code = '';
    code += 'ret = SapModel.EditArea.Divide(' + v_Name + ', ' + v_MeshType + ', ' + v_NumAreas + ', ' + v_AreaName + ', ' + v_N1 + ', ' + v_N2 + ', ' + v_MaxSize1 + ', ' + v_MaxSize2 + ', ' + v_PointOnEdgeFromLine + ', ' + v_PointOnEdgeFromPoint + ', ' + v_ExtendCookieCutLines + ', ' + v_Rotation + ', ' + v_MaxSizeGeneral + ', ' + v_LocalAxesOnEdge + ', ' + v_LocalAxesOnFace + ', ' + v_RestraintsOnEdge + ', ' + v_RestraintsOnFace + ', ' + v_Group + ', ' + v_SubMesh + ', ' + v_SubMeshSize + ')\n';
    code += 'assert ret == 0, "EditArea.Divide failed: " + str(ret)\n';
    return code;
  };

  // SelectObj.ClearSelection
  pythonGenerator.forBlock['sap_SapModel_SelectObj_ClearSelection'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.SelectObj.ClearSelection()\n';
    code += 'assert ret == 0, "SelectObj.ClearSelection failed"\n';
    return code;
  };

  // SelectObj.CoordinateRange
  pythonGenerator.forBlock['sap_SapModel_SelectObj_CoordinateRange'] = function(block, generator) {
    var v_XMin = block.getFieldValue('XMin') || '0';
    var v_XMax = block.getFieldValue('XMax') || '0';
    var v_YMin = block.getFieldValue('YMin') || '0';
    var v_YMax = block.getFieldValue('YMax') || '0';
    var v_ZMin = block.getFieldValue('ZMin') || '0';
    var v_ZMax = block.getFieldValue('ZMax') || '0';
    var v_Deselect = "'" + (block.getFieldValue('Deselect') || '') + "'";
    var v_IncludeIntersections = "'" + (block.getFieldValue('IncludeIntersections') || '') + "'";
    var v_IncludePoints = "'" + (block.getFieldValue('IncludePoints') || '') + "'";
    var v_IncludeFrames = "'" + (block.getFieldValue('IncludeFrames') || '') + "'";
    var v_IncludeAreas = "'" + (block.getFieldValue('IncludeAreas') || '') + "'";
    var v_IncludeSolids = "'" + (block.getFieldValue('IncludeSolids') || '') + "'";
    var v_IncludeLinks = "'" + (block.getFieldValue('IncludeLinks') || '') + "'";
    var code = '';
    code += 'ret = SapModel.SelectObj.CoordinateRange(' + v_XMin + ', ' + v_XMax + ', ' + v_YMin + ', ' + v_YMax + ', ' + v_ZMin + ', ' + v_ZMax + ', ' + v_Deselect + ', ' + v_IncludeIntersections + ', ' + v_IncludePoints + ', ' + v_IncludeFrames + ', ' + v_IncludeAreas + ', ' + v_IncludeSolids + ', ' + v_IncludeLinks + ')\n';
    code += 'assert ret == 0, "SelectObj.CoordinateRange failed: " + str(ret)\n';
    return code;
  };

  // SelectObj.GetSelected
  pythonGenerator.forBlock['sap_SapModel_SelectObj_GetSelected'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_ObjectType = "'" + (block.getFieldValue('ObjectType') || '') + "'";
    var v_ObjectName = "'" + (block.getFieldValue('ObjectName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.SelectObj.GetSelected(' + v_NumberItems + ', ' + v_ObjectType + ', ' + v_ObjectName + ')\n';
    code += 'assert ret == 0, "SelectObj.GetSelected failed: " + str(ret)\n';
    return code;
  };

  // ConstraintDef.SetBody
  pythonGenerator.forBlock['sap_SapModel_ConstraintDef_SetBody'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var code = '';
    code += 'ret = SapModel.ConstraintDef.SetBody(' + v_Name + ', ' + v_Value + ')\n';
    code += 'assert ret == 0, "ConstraintDef.SetBody failed: " + str(ret)\n';
    return code;
  };

  // PointObj.SetConstraint
  pythonGenerator.forBlock['sap_SapModel_PointObj_SetConstraint'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ConstraintName = "'" + (block.getFieldValue('ConstraintName') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.PointObj.SetConstraint(' + v_Name + ', ' + v_ConstraintName + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "PointObj.SetConstraint failed: " + str(ret)\n';
    return code;
  };

  // ConstraintDef.GetBody
  pythonGenerator.forBlock['sap_SapModel_ConstraintDef_GetBody'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_DOF = "'" + (block.getFieldValue('DOF') || '') + "'";
    var code = '';
    code += 'ret = SapModel.ConstraintDef.GetBody(' + v_Name + ', ' + v_DOF + ')\n';
    code += 'assert ret == 0, "ConstraintDef.GetBody failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetTCLimits
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetTCLimits'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_LimitCompressionExists = "'" + (block.getFieldValue('LimitCompressionExists') || '') + "'";
    var v_LimitCompression = "'" + (block.getFieldValue('LimitCompression') || '') + "'";
    var v_LimitTensionExists = "'" + (block.getFieldValue('LimitTensionExists') || '') + "'";
    var v_LimitTension = "'" + (block.getFieldValue('LimitTension') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.FrameObj.SetTCLimits(' + v_Name + ', ' + v_LimitCompressionExists + ', ' + v_LimitCompression + ', ' + v_LimitTensionExists + ', ' + v_LimitTension + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "FrameObj.SetTCLimits failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.GetTCLimits
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetTCLimits'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_LimitCompressionExists = "'" + (block.getFieldValue('LimitCompressionExists') || '') + "'";
    var v_LimitCompression = "'" + (block.getFieldValue('LimitCompression') || '') + "'";
    var v_LimitTensionExists = "'" + (block.getFieldValue('LimitTensionExists') || '') + "'";
    var v_LimitTension = "'" + (block.getFieldValue('LimitTension') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.GetTCLimits(' + v_Name + ', ' + v_LimitCompressionExists + ', ' + v_LimitCompression + ', ' + v_LimitTensionExists + ', ' + v_LimitTension + ')\n';
    code += 'assert ret == 0, "FrameObj.GetTCLimits failed: " + str(ret)\n';
    return code;
  };

  // PointObj.SetRestraint
  pythonGenerator.forBlock['sap_SapModel_PointObj_SetRestraint'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.PointObj.SetRestraint(' + v_Name + ', ' + v_Value + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "PointObj.SetRestraint failed: " + str(ret)\n';
    return code;
  };

  // LoadPatterns.GetNameList
  pythonGenerator.forBlock['sap_SapModel_LoadPatterns_GetNameList'] = function(block, generator) {
    var v_NumberNames = block.getFieldValue('NumberNames') || '1';
    var v_MyName = block.getFieldValue('MyName') || '1';
    var v_MyType = block.getFieldValue('MyType') || '1';
    var code = '';
    code += 'ret = SapModel.LoadPatterns.GetNameList(' + v_NumberNames + ', ' + v_MyName + ', ' + v_MyType + ')\n';
    code += 'assert ret == 0, "LoadPatterns.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.GetNameList
  pythonGenerator.forBlock['sap_SapModel_PropFrame_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropFrame.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "PropFrame.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetLoadDistributed
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetLoadDistributed'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_LoadPat = "'" + (block.getFieldValue('LoadPat') || '') + "'";
    var v_MyType = block.getFieldValue('MyType') || '1';
    var v_Dir = block.getFieldValue('Dir') || '10';
    var v_Dist1 = "'" + (block.getFieldValue('Dist1') || '') + "'";
    var v_Dist2 = "'" + (block.getFieldValue('Dist2') || '') + "'";
    var v_Val1 = "'" + (block.getFieldValue('Val1') || '') + "'";
    var v_Val2 = "'" + (block.getFieldValue('Val2') || '') + "'";
    var v_RelDist = "'" + (block.getFieldValue('RelDist') || '') + "'";
    var v_Replace = block.getFieldValue('Replace') === 'TRUE' ? 'True' : 'False';
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.FrameObj.SetLoadDistributed(' + v_Name + ', ' + v_LoadPat + ', ' + v_MyType + ', ' + v_Dir + ', ' + v_Dist1 + ', ' + v_Dist2 + ', ' + v_Val1 + ', ' + v_Val2 + ', ' + v_RelDist + ', ' + v_Replace + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "FrameObj.SetLoadDistributed failed: " + str(ret)\n';
    return code;
  };

  // PointObj.SetLoadForce
  pythonGenerator.forBlock['sap_SapModel_PointObj_SetLoadForce'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_LoadPat = "'" + (block.getFieldValue('LoadPat') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var v_Replace = block.getFieldValue('Replace') === 'TRUE' ? 'True' : 'False';
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.PointObj.SetLoadForce(' + v_Name + ', ' + v_LoadPat + ', ' + v_Value + ', ' + v_Replace + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "PointObj.SetLoadForce failed: " + str(ret)\n';
    return code;
  };

  // View.RefreshView
  pythonGenerator.forBlock['sap_SapModel_View_RefreshView'] = function(block, generator) {
    var v_Window = "'" + (block.getFieldValue('Window') || '') + "'";
    var v_Zoom = block.getFieldValue('Zoom') || '0';
    var code = '';
    code += 'ret = SapModel.View.RefreshView(' + v_Window + ', ' + v_Zoom + ')\n';
    code += 'assert ret == 0, "View.RefreshView failed: " + str(ret)\n';
    return code;
  };

  // File.Save
  pythonGenerator.forBlock['sap_SapModel_File_Save'] = function(block, generator) {
    var v_FileName = "'" + (block.getFieldValue('FileName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.File.Save(' + v_FileName + ')\n';
    code += 'assert ret == 0, "File.Save failed: " + str(ret)\n';
    return code;
  };

  // Analyze.RunAnalysis
  pythonGenerator.forBlock['sap_SapModel_Analyze_RunAnalysis'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Analyze.RunAnalysis()\n';
    code += 'assert ret == 0, "Analyze.RunAnalysis failed"\n';
    return code;
  };

  // Setup.DeselectAllCasesAndCombosForOutput
  pythonGenerator.forBlock['sap_SapModel_Results_Setup_DeselectAllCasesAndCombosForOutput'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()\n';
    code += 'assert ret == 0, "Setup.DeselectAllCasesAndCombosForOutput failed"\n';
    return code;
  };

  // Setup.SetCaseSelectedForOutput
  pythonGenerator.forBlock['sap_SapModel_Results_Setup_SetCaseSelectedForOutput'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Selected = "'" + (block.getFieldValue('Selected') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.Setup.SetCaseSelectedForOutput(' + v_Name + ', ' + v_Selected + ')\n';
    code += 'assert ret == 0, "Setup.SetCaseSelectedForOutput failed: " + str(ret)\n';
    return code;
  };

  // Results.JointDispl
  pythonGenerator.forBlock['sap_SapModel_Results_JointDispl'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ItemTypeElm = block.getFieldValue('ItemTypeElm') || '0';
    var v_NumberResults = "'" + (block.getFieldValue('NumberResults') || '') + "'";
    var v_Obj = "'" + (block.getFieldValue('Obj') || '') + "'";
    var v_Elm = "'" + (block.getFieldValue('Elm') || '') + "'";
    var v_LoadCase = "'" + (block.getFieldValue('LoadCase') || '') + "'";
    var v_StepType = "'" + (block.getFieldValue('StepType') || '') + "'";
    var v_StepNum = "'" + (block.getFieldValue('StepNum') || '') + "'";
    var v_U1 = "'" + (block.getFieldValue('U1') || '') + "'";
    var v_U2 = "'" + (block.getFieldValue('U2') || '') + "'";
    var v_U3 = "'" + (block.getFieldValue('U3') || '') + "'";
    var v_R1 = "'" + (block.getFieldValue('R1') || '') + "'";
    var v_R2 = "'" + (block.getFieldValue('R2') || '') + "'";
    var v_R3 = "'" + (block.getFieldValue('R3') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.JointDispl(' + v_Name + ', ' + v_ItemTypeElm + ', ' + v_NumberResults + ', ' + v_Obj + ', ' + v_Elm + ', ' + v_LoadCase + ', ' + v_StepType + ', ' + v_StepNum + ', ' + v_U1 + ', ' + v_U2 + ', ' + v_U3 + ', ' + v_R1 + ', ' + v_R2 + ', ' + v_R3 + ')\n';
    code += 'assert ret == 0, "Results.JointDispl failed: " + str(ret)\n';
    return code;
  };

  // Results.FrameForce
  pythonGenerator.forBlock['sap_SapModel_Results_FrameForce'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ItemTypeElm = block.getFieldValue('ItemTypeElm') || '0';
    var v_NumberResults = "'" + (block.getFieldValue('NumberResults') || '') + "'";
    var v_Obj = "'" + (block.getFieldValue('Obj') || '') + "'";
    var v_ObjSta = "'" + (block.getFieldValue('ObjSta') || '') + "'";
    var v_Elm = "'" + (block.getFieldValue('Elm') || '') + "'";
    var v_ElmSta = "'" + (block.getFieldValue('ElmSta') || '') + "'";
    var v_LoadCase = "'" + (block.getFieldValue('LoadCase') || '') + "'";
    var v_StepType = "'" + (block.getFieldValue('StepType') || '') + "'";
    var v_StepNum = "'" + (block.getFieldValue('StepNum') || '') + "'";
    var v_P = "'" + (block.getFieldValue('P') || '') + "'";
    var v_V2 = "'" + (block.getFieldValue('V2') || '') + "'";
    var v_V3 = "'" + (block.getFieldValue('V3') || '') + "'";
    var v_T = block.getFieldValue('T') || '0';
    var v_M2 = "'" + (block.getFieldValue('M2') || '') + "'";
    var v_M3 = "'" + (block.getFieldValue('M3') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.FrameForce(' + v_Name + ', ' + v_ItemTypeElm + ', ' + v_NumberResults + ', ' + v_Obj + ', ' + v_ObjSta + ', ' + v_Elm + ', ' + v_ElmSta + ', ' + v_LoadCase + ', ' + v_StepType + ', ' + v_StepNum + ', ' + v_P + ', ' + v_V2 + ', ' + v_V3 + ', ' + v_T + ', ' + v_M2 + ', ' + v_M3 + ')\n';
    code += 'assert ret == 0, "Results.FrameForce failed: " + str(ret)\n';
    return code;
  };

  // Results.JointReact
  pythonGenerator.forBlock['sap_SapModel_Results_JointReact'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ItemTypeElm = block.getFieldValue('ItemTypeElm') || '0';
    var v_NumberResults = "'" + (block.getFieldValue('NumberResults') || '') + "'";
    var v_Obj = "'" + (block.getFieldValue('Obj') || '') + "'";
    var v_Elm = "'" + (block.getFieldValue('Elm') || '') + "'";
    var v_LoadCase = "'" + (block.getFieldValue('LoadCase') || '') + "'";
    var v_StepType = "'" + (block.getFieldValue('StepType') || '') + "'";
    var v_StepNum = "'" + (block.getFieldValue('StepNum') || '') + "'";
    var v_F1 = "'" + (block.getFieldValue('F1') || '') + "'";
    var v_F2 = "'" + (block.getFieldValue('F2') || '') + "'";
    var v_F3 = "'" + (block.getFieldValue('F3') || '') + "'";
    var v_M1 = "'" + (block.getFieldValue('M1') || '') + "'";
    var v_M2 = "'" + (block.getFieldValue('M2') || '') + "'";
    var v_M3 = "'" + (block.getFieldValue('M3') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.JointReact(' + v_Name + ', ' + v_ItemTypeElm + ', ' + v_NumberResults + ', ' + v_Obj + ', ' + v_Elm + ', ' + v_LoadCase + ', ' + v_StepType + ', ' + v_StepNum + ', ' + v_F1 + ', ' + v_F2 + ', ' + v_F3 + ', ' + v_M1 + ', ' + v_M2 + ', ' + v_M3 + ')\n';
    code += 'assert ret == 0, "Results.JointReact failed: " + str(ret)\n';
    return code;
  };

  // Setup.SetComboSelectedForOutput
  pythonGenerator.forBlock['sap_SapModel_Results_Setup_SetComboSelectedForOutput'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Selected = "'" + (block.getFieldValue('Selected') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.Setup.SetComboSelectedForOutput(' + v_Name + ', ' + v_Selected + ')\n';
    code += 'assert ret == 0, "Setup.SetComboSelectedForOutput failed: " + str(ret)\n';
    return code;
  };

  // LoadPatterns.SetSelfWTMultiplier
  pythonGenerator.forBlock['sap_SapModel_LoadPatterns_SetSelfWTMultiplier'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_SelfWTMultiplier = "'" + (block.getFieldValue('SelfWTMultiplier') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadPatterns.SetSelfWTMultiplier(' + v_Name + ', ' + v_SelfWTMultiplier + ')\n';
    code += 'assert ret == 0, "LoadPatterns.SetSelfWTMultiplier failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetAllTables
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetAllTables'] = function(block, generator) {
    var v_NumberTables = "'" + (block.getFieldValue('NumberTables') || '') + "'";
    var v_TableKey__ = "'" + (block.getFieldValue('TableKey[]') || '') + "'";
    var v_TableName__ = "'" + (block.getFieldValue('TableName[]') || '') + "'";
    var v_ImportType__ = "'" + (block.getFieldValue('ImportType[]') || '') + "'";
    var v_IsEmpty__ = "'" + (block.getFieldValue('IsEmpty[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetAllTables(' + v_NumberTables + ', ' + v_TableKey__ + ', ' + v_TableName__ + ', ' + v_ImportType__ + ', ' + v_IsEmpty__ + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetAllTables failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetAvailableTables
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetAvailableTables'] = function(block, generator) {
    var v_NumberTables = "'" + (block.getFieldValue('NumberTables') || '') + "'";
    var v_TableKey__ = "'" + (block.getFieldValue('TableKey[]') || '') + "'";
    var v_TableName__ = "'" + (block.getFieldValue('TableName[]') || '') + "'";
    var v_ImportType__ = "'" + (block.getFieldValue('ImportType[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetAvailableTables(' + v_NumberTables + ', ' + v_TableKey__ + ', ' + v_TableName__ + ', ' + v_ImportType__ + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetAvailableTables failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetAllFieldsInTable
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetAllFieldsInTable'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_NumberFields = "'" + (block.getFieldValue('NumberFields') || '') + "'";
    var v_FieldKey__ = "'" + (block.getFieldValue('FieldKey[]') || '') + "'";
    var v_FieldName__ = "'" + (block.getFieldValue('FieldName[]') || '') + "'";
    var v_Description__ = "'" + (block.getFieldValue('Description[]') || '') + "'";
    var v_UnitsString__ = block.getFieldValue('UnitsString[]') || '6';
    var v_IsImportable__ = "'" + (block.getFieldValue('IsImportable[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetAllFieldsInTable(' + v_TableKey + ', ' + v_TableVersion + ', ' + v_NumberFields + ', ' + v_FieldKey__ + ', ' + v_FieldName__ + ', ' + v_Description__ + ', ' + v_UnitsString__ + ', ' + v_IsImportable__ + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetAllFieldsInTable failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetObsoleteTableKeyList
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetObsoleteTableKeyList'] = function(block, generator) {
    var v_NumberTableKeys = "'" + (block.getFieldValue('NumberTableKeys') || '') + "'";
    var v_TableKeyList__ = "'" + (block.getFieldValue('TableKeyList[]') || '') + "'";
    var v_NotesList__ = "'" + (block.getFieldValue('NotesList[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetObsoleteTableKeyList(' + v_NumberTableKeys + ', ' + v_TableKeyList__ + ', ' + v_NotesList__ + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetObsoleteTableKeyList failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetTableForEditingArray
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForEditingArray'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_FieldKeysIncluded__ = "'" + (block.getFieldValue('FieldKeysIncluded[]') || '') + "'";
    var v_NumberRecords = "'" + (block.getFieldValue('NumberRecords') || '') + "'";
    var v_TableData__ = "'" + (block.getFieldValue('TableData[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForEditingArray(' + v_TableKey + ', ' + v_GroupName + ', ' + v_TableVersion + ', ' + v_FieldKeysIncluded__ + ', ' + v_NumberRecords + ', ' + v_TableData__ + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForEditingArray failed: " + str(ret)\n';
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
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_FieldKeysIncluded__ = "'" + (block.getFieldValue('FieldKeysIncluded[]') || '') + "'";
    var v_NumberRecords = "'" + (block.getFieldValue('NumberRecords') || '') + "'";
    var v_TableData__ = "'" + (block.getFieldValue('TableData[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetTableForEditingArray(' + v_TableKey + ', ' + v_TableVersion + ', ' + v_FieldKeysIncluded__ + ', ' + v_NumberRecords + ', ' + v_TableData__ + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetTableForEditingArray failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.ApplyEditedTables
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_ApplyEditedTables'] = function(block, generator) {
    var v_FillImportLog = "'" + (block.getFieldValue('FillImportLog') || '') + "'";
    var v_NumFatalErrors = "'" + (block.getFieldValue('NumFatalErrors') || '') + "'";
    var v_NumErrorMsgs = "'" + (block.getFieldValue('NumErrorMsgs') || '') + "'";
    var v_NumWarnMsgs = "'" + (block.getFieldValue('NumWarnMsgs') || '') + "'";
    var v_NumInfoMsgs = "'" + (block.getFieldValue('NumInfoMsgs') || '') + "'";
    var v_ImportLog = "'" + (block.getFieldValue('ImportLog') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.ApplyEditedTables(' + v_FillImportLog + ', ' + v_NumFatalErrors + ', ' + v_NumErrorMsgs + ', ' + v_NumWarnMsgs + ', ' + v_NumInfoMsgs + ', ' + v_ImportLog + ')\n';
    code += 'assert ret == 0, "DatabaseTables.ApplyEditedTables failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetTableForDisplayArray
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForDisplayArray'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_FieldKeyList__ = "'" + (block.getFieldValue('FieldKeyList[]') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_FieldKeysIncluded__ = "'" + (block.getFieldValue('FieldKeysIncluded[]') || '') + "'";
    var v_NumberRecords = "'" + (block.getFieldValue('NumberRecords') || '') + "'";
    var v_TableData__ = "'" + (block.getFieldValue('TableData[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForDisplayArray(' + v_TableKey + ', ' + v_FieldKeyList__ + ', ' + v_GroupName + ', ' + v_TableVersion + ', ' + v_FieldKeysIncluded__ + ', ' + v_NumberRecords + ', ' + v_TableData__ + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForDisplayArray failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetTableForDisplayCSVFile
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForDisplayCSVFile'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_FieldKeyList__ = "'" + (block.getFieldValue('FieldKeyList[]') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_csvFilePath = "'" + (block.getFieldValue('csvFilePath') || '') + "'";
    var v_sepChar = "'" + (block.getFieldValue('sepChar') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForDisplayCSVFile(' + v_TableKey + ', ' + v_FieldKeyList__ + ', ' + v_GroupName + ', ' + v_TableVersion + ', ' + v_csvFilePath + ', ' + v_sepChar + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForDisplayCSVFile failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetTableForDisplayCSVString
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForDisplayCSVString'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_FieldKeyList__ = "'" + (block.getFieldValue('FieldKeyList[]') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_csvString = "'" + (block.getFieldValue('csvString') || '') + "'";
    var v_sepChar = "'" + (block.getFieldValue('sepChar') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForDisplayCSVString(' + v_TableKey + ', ' + v_FieldKeyList__ + ', ' + v_GroupName + ', ' + v_TableVersion + ', ' + v_csvString + ', ' + v_sepChar + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForDisplayCSVString failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetTableForDisplayXMLString
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForDisplayXMLString'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_FieldKeyList__ = "'" + (block.getFieldValue('FieldKeyList[]') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_IncludeSchema = "'" + (block.getFieldValue('IncludeSchema') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_XMLTableData = block.getFieldValue('XMLTableData') || '0';
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForDisplayXMLString(' + v_TableKey + ', ' + v_FieldKeyList__ + ', ' + v_GroupName + ', ' + v_IncludeSchema + ', ' + v_TableVersion + ', ' + v_XMLTableData + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForDisplayXMLString failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetTableForEditingCSVFile
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForEditingCSVFile'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_csvFilePath = "'" + (block.getFieldValue('csvFilePath') || '') + "'";
    var v_sepChar = "'" + (block.getFieldValue('sepChar') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForEditingCSVFile(' + v_TableKey + ', ' + v_GroupName + ', ' + v_TableVersion + ', ' + v_csvFilePath + ', ' + v_sepChar + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForEditingCSVFile failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetTableForEditingCSVString
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableForEditingCSVString'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_csvString = "'" + (block.getFieldValue('csvString') || '') + "'";
    var v_sepChar = "'" + (block.getFieldValue('sepChar') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableForEditingCSVString(' + v_TableKey + ', ' + v_GroupName + ', ' + v_TableVersion + ', ' + v_csvString + ', ' + v_sepChar + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableForEditingCSVString failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetTableForEditingCSVFile
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetTableForEditingCSVFile'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_csvFilePath = "'" + (block.getFieldValue('csvFilePath') || '') + "'";
    var v_sepChar = "'" + (block.getFieldValue('sepChar') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetTableForEditingCSVFile(' + v_TableKey + ', ' + v_TableVersion + ', ' + v_csvFilePath + ', ' + v_sepChar + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetTableForEditingCSVFile failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetTableForEditingCSVString
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetTableForEditingCSVString'] = function(block, generator) {
    var v_TableKey = "'" + (block.getFieldValue('TableKey') || '') + "'";
    var v_TableVersion = "'" + (block.getFieldValue('TableVersion') || '') + "'";
    var v_csvString = "'" + (block.getFieldValue('csvString') || '') + "'";
    var v_sepChar = "'" + (block.getFieldValue('sepChar') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetTableForEditingCSVString(' + v_TableKey + ', ' + v_TableVersion + ', ' + v_csvString + ', ' + v_sepChar + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetTableForEditingCSVString failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetLoadCasesSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetLoadCasesSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetLoadCasesSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetLoadCasesSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetLoadCasesSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetLoadCasesSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetLoadCasesSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetLoadCombinationsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetLoadCombinationsSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetLoadCombinationsSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetLoadCombinationsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetLoadCombinationsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetLoadCombinationsSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetLoadCombinationsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetLoadPatternsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetLoadPatternsSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetLoadPatternsSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetLoadPatternsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetLoadPatternsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetLoadPatternsSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetLoadPatternsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetElementVirtualWorkNamedSetsSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetElementVirtualWorkNamedSetsSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetGeneralizedDisplacementsSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetGeneralizedDisplacementsSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetJointResponseSpectraNamedSetsSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetJointResponseSpectraNamedSetsSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetPlotFunctionTracesNamedSetsSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetPlotFunctionTracesNamedSetsSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetPushoverNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetPushoverNamedSetsSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetPushoverNamedSetsSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetPushoverNamedSetsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetPushoverNamedSetsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetPushoverNamedSetsSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetPushoverNamedSetsSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetPushoverNamedSetsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetSectionCutsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetSectionCutsSelectedForDisplay'] = function(block, generator) {
    var v_NumberSelected = "'" + (block.getFieldValue('NumberSelected') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetSectionCutsSelectedForDisplay(' + v_NumberSelected + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetSectionCutsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetSectionCutsSelectedForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetSectionCutsSelectedForDisplay'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_NameList = "'" + (block.getFieldValue('NameList') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetSectionCutsSelectedForDisplay(' + v_NumberItems + ', ' + v_NameList + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetSectionCutsSelectedForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.GetTableOutputOptionsForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_GetTableOutputOptionsForDisplay'] = function(block, generator) {
    var v_SortTableData = "'" + (block.getFieldValue('SortTableData') || '') + "'";
    var v_SortConnectyData = "'" + (block.getFieldValue('SortConnectyData') || '') + "'";
    var v_ModeShapeOpt = "'" + (block.getFieldValue('ModeShapeOpt') || '') + "'";
    var v_ModeShapeRef = "'" + (block.getFieldValue('ModeShapeRef') || '') + "'";
    var v_TableGroupOpt = "'" + (block.getFieldValue('TableGroupOpt') || '') + "'";
    var v_TableGroupSingle = "'" + (block.getFieldValue('TableGroupSingle') || '') + "'";
    var v_TwoDFloat = "'" + (block.getFieldValue('TwoDFloat') || '') + "'";
    var v_TwoDFloatFig = "'" + (block.getFieldValue('TwoDFloatFig') || '') + "'";
    var v_TwoDInt = "'" + (block.getFieldValue('TwoDInt') || '') + "'";
    var v_FourDFloat = "'" + (block.getFieldValue('FourDFloat') || '') + "'";
    var v_FourDFloatFig = "'" + (block.getFieldValue('FourDFloatFig') || '') + "'";
    var v_FourDInt = "'" + (block.getFieldValue('FourDInt') || '') + "'";
    var v_EightDFloat = "'" + (block.getFieldValue('EightDFloat') || '') + "'";
    var v_EightDFloatFig = "'" + (block.getFieldValue('EightDFloatFig') || '') + "'";
    var v_EightDInt = "'" + (block.getFieldValue('EightDInt') || '') + "'";
    var v_TwelveDFloat = "'" + (block.getFieldValue('TwelveDFloat') || '') + "'";
    var v_TwelveDFloatFig = "'" + (block.getFieldValue('TwelveDFloatFig') || '') + "'";
    var v_TwelveDInt = "'" + (block.getFieldValue('TwelveDInt') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.GetTableOutputOptionsForDisplay(' + v_SortTableData + ', ' + v_SortConnectyData + ', ' + v_ModeShapeOpt + ', ' + v_ModeShapeRef + ', ' + v_TableGroupOpt + ', ' + v_TableGroupSingle + ', ' + v_TwoDFloat + ', ' + v_TwoDFloatFig + ', ' + v_TwoDInt + ', ' + v_FourDFloat + ', ' + v_FourDFloatFig + ', ' + v_FourDInt + ', ' + v_EightDFloat + ', ' + v_EightDFloatFig + ', ' + v_EightDInt + ', ' + v_TwelveDFloat + ', ' + v_TwelveDFloatFig + ', ' + v_TwelveDInt + ')\n';
    code += 'assert ret == 0, "DatabaseTables.GetTableOutputOptionsForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.SetTableOutputOptionsForDisplay
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_SetTableOutputOptionsForDisplay'] = function(block, generator) {
    var v_SortTableData = "'" + (block.getFieldValue('SortTableData') || '') + "'";
    var v_SortConnectyData = "'" + (block.getFieldValue('SortConnectyData') || '') + "'";
    var v_ModeShapeOpt = "'" + (block.getFieldValue('ModeShapeOpt') || '') + "'";
    var v_ModeShapeRef = "'" + (block.getFieldValue('ModeShapeRef') || '') + "'";
    var v_TableGroupOpt = "'" + (block.getFieldValue('TableGroupOpt') || '') + "'";
    var v_TableGroupSingle = "'" + (block.getFieldValue('TableGroupSingle') || '') + "'";
    var v_TwoDFloat = "'" + (block.getFieldValue('TwoDFloat') || '') + "'";
    var v_TwoDFloatFig = "'" + (block.getFieldValue('TwoDFloatFig') || '') + "'";
    var v_TwoDInt = "'" + (block.getFieldValue('TwoDInt') || '') + "'";
    var v_FourDFloat = "'" + (block.getFieldValue('FourDFloat') || '') + "'";
    var v_FourDFloatFig = "'" + (block.getFieldValue('FourDFloatFig') || '') + "'";
    var v_FourDInt = "'" + (block.getFieldValue('FourDInt') || '') + "'";
    var v_EightDFloat = "'" + (block.getFieldValue('EightDFloat') || '') + "'";
    var v_EightDFloatFig = "'" + (block.getFieldValue('EightDFloatFig') || '') + "'";
    var v_EightDInt = "'" + (block.getFieldValue('EightDInt') || '') + "'";
    var v_TwelveDFloat = "'" + (block.getFieldValue('TwelveDFloat') || '') + "'";
    var v_TwelveDFloatFig = "'" + (block.getFieldValue('TwelveDFloatFig') || '') + "'";
    var v_TwelveDInt = "'" + (block.getFieldValue('TwelveDInt') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.SetTableOutputOptionsForDisplay(' + v_SortTableData + ', ' + v_SortConnectyData + ', ' + v_ModeShapeOpt + ', ' + v_ModeShapeRef + ', ' + v_TableGroupOpt + ', ' + v_TableGroupSingle + ', ' + v_TwoDFloat + ', ' + v_TwoDFloatFig + ', ' + v_TwoDInt + ', ' + v_FourDFloat + ', ' + v_FourDFloatFig + ', ' + v_FourDInt + ', ' + v_EightDFloat + ', ' + v_EightDFloatFig + ', ' + v_EightDInt + ', ' + v_TwelveDFloat + ', ' + v_TwelveDFloatFig + ', ' + v_TwelveDInt + ')\n';
    code += 'assert ret == 0, "DatabaseTables.SetTableOutputOptionsForDisplay failed: " + str(ret)\n';
    return code;
  };

  // DatabaseTables.ShowTablesInExcel
  pythonGenerator.forBlock['sap_SapModel_DatabaseTables_ShowTablesInExcel'] = function(block, generator) {
    var v_TableKeyList__ = "'" + (block.getFieldValue('TableKeyList[]') || '') + "'";
    var v_WindowHandle = "'" + (block.getFieldValue('WindowHandle') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DatabaseTables.ShowTablesInExcel(' + v_TableKeyList__ + ', ' + v_WindowHandle + ')\n';
    code += 'assert ret == 0, "DatabaseTables.ShowTablesInExcel failed: " + str(ret)\n';
    return code;
  };

  // SapModel.GetModelIsLocked
  pythonGenerator.forBlock['sap_SapModel_GetModelIsLocked'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.GetModelIsLocked()\n';
    code += 'assert ret == 0, "SapModel.GetModelIsLocked failed"\n';
    return code;
  };

  // FrameObj.GetLoadDistributed
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetLoadDistributed'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_FrameName = "'" + (block.getFieldValue('FrameName') || '') + "'";
    var v_LoadPat = "'" + (block.getFieldValue('LoadPat') || '') + "'";
    var v_MyType = block.getFieldValue('MyType') || '1';
    var v_Dir = block.getFieldValue('Dir') || '10';
    var v_RD1 = "'" + (block.getFieldValue('RD1') || '') + "'";
    var v_RD2 = "'" + (block.getFieldValue('RD2') || '') + "'";
    var v_Dist1 = "'" + (block.getFieldValue('Dist1') || '') + "'";
    var v_Dist2 = "'" + (block.getFieldValue('Dist2') || '') + "'";
    var v_Val1 = "'" + (block.getFieldValue('Val1') || '') + "'";
    var v_Val2 = "'" + (block.getFieldValue('Val2') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.FrameObj.GetLoadDistributed(' + v_Name + ', ' + v_NumberItems + ', ' + v_FrameName + ', ' + v_LoadPat + ', ' + v_MyType + ', ' + v_Dir + ', ' + v_RD1 + ', ' + v_RD2 + ', ' + v_Dist1 + ', ' + v_Dist2 + ', ' + v_Val1 + ', ' + v_Val2 + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "FrameObj.GetLoadDistributed failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetLoadPoint
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetLoadPoint'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_LoadPat = "'" + (block.getFieldValue('LoadPat') || '') + "'";
    var v_MyType = block.getFieldValue('MyType') || '1';
    var v_Dir = block.getFieldValue('Dir') || '10';
    var v_Dist = "'" + (block.getFieldValue('Dist') || '') + "'";
    var v_Val = "'" + (block.getFieldValue('Val') || '') + "'";
    var v_RelDist = "'" + (block.getFieldValue('RelDist') || '') + "'";
    var v_Replace = block.getFieldValue('Replace') === 'TRUE' ? 'True' : 'False';
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.FrameObj.SetLoadPoint(' + v_Name + ', ' + v_LoadPat + ', ' + v_MyType + ', ' + v_Dir + ', ' + v_Dist + ', ' + v_Val + ', ' + v_RelDist + ', ' + v_Replace + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "FrameObj.SetLoadPoint failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.SetLoadUniform
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetLoadUniform'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_LoadPat = "'" + (block.getFieldValue('LoadPat') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var v_Dir = block.getFieldValue('Dir') || '10';
    var v_Replace = block.getFieldValue('Replace') === 'TRUE' ? 'True' : 'False';
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.AreaObj.SetLoadUniform(' + v_Name + ', ' + v_LoadPat + ', ' + v_Value + ', ' + v_Dir + ', ' + v_Replace + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "AreaObj.SetLoadUniform failed: " + str(ret)\n';
    return code;
  };

  // Results.BaseReact
  pythonGenerator.forBlock['sap_SapModel_Results_BaseReact'] = function(block, generator) {
    var v_NumberResults = "'" + (block.getFieldValue('NumberResults') || '') + "'";
    var v_LoadCase = "'" + (block.getFieldValue('LoadCase') || '') + "'";
    var v_StepType = "'" + (block.getFieldValue('StepType') || '') + "'";
    var v_StepNum = "'" + (block.getFieldValue('StepNum') || '') + "'";
    var v_Fx = "'" + (block.getFieldValue('Fx') || '') + "'";
    var v_Fy = "'" + (block.getFieldValue('Fy') || '') + "'";
    var v_Fz = "'" + (block.getFieldValue('Fz') || '') + "'";
    var v_Mx = "'" + (block.getFieldValue('Mx') || '') + "'";
    var v_My = "'" + (block.getFieldValue('My') || '') + "'";
    var v_Mz = "'" + (block.getFieldValue('Mz') || '') + "'";
    var v_gx = "'" + (block.getFieldValue('gx') || '') + "'";
    var v_gy = "'" + (block.getFieldValue('gy') || '') + "'";
    var v_gz = "'" + (block.getFieldValue('gz') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.BaseReact(' + v_NumberResults + ', ' + v_LoadCase + ', ' + v_StepType + ', ' + v_StepNum + ', ' + v_Fx + ', ' + v_Fy + ', ' + v_Fz + ', ' + v_Mx + ', ' + v_My + ', ' + v_Mz + ', ' + v_gx + ', ' + v_gy + ', ' + v_gz + ')\n';
    code += 'assert ret == 0, "Results.BaseReact failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.SetLoadGravity
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetLoadGravity'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_LoadPat = "'" + (block.getFieldValue('LoadPat') || '') + "'";
    var v_x = block.getFieldValue('x') || '0';
    var v_y = block.getFieldValue('y') || '0';
    var v_z = block.getFieldValue('z') || '0';
    var v_Replace = block.getFieldValue('Replace') === 'TRUE' ? 'True' : 'False';
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.AreaObj.SetLoadGravity(' + v_Name + ', ' + v_LoadPat + ', ' + v_x + ', ' + v_y + ', ' + v_z + ', ' + v_Replace + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "AreaObj.SetLoadGravity failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetReleases
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetReleases'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ii = "'" + (block.getFieldValue('ii') || '') + "'";
    var v_jj = "'" + (block.getFieldValue('jj') || '') + "'";
    var v_StartValue = "'" + (block.getFieldValue('StartValue') || '') + "'";
    var v_EndValue = "'" + (block.getFieldValue('EndValue') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.FrameObj.SetReleases(' + v_Name + ', ' + v_ii + ', ' + v_jj + ', ' + v_StartValue + ', ' + v_EndValue + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "FrameObj.SetReleases failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.GetReleases
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetReleases'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ii = "'" + (block.getFieldValue('ii') || '') + "'";
    var v_jj = "'" + (block.getFieldValue('jj') || '') + "'";
    var v_StartValue = "'" + (block.getFieldValue('StartValue') || '') + "'";
    var v_EndValue = "'" + (block.getFieldValue('EndValue') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.GetReleases(' + v_Name + ', ' + v_ii + ', ' + v_jj + ', ' + v_StartValue + ', ' + v_EndValue + ')\n';
    code += 'assert ret == 0, "FrameObj.GetReleases failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetInsertionPoint_1
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetInsertionPoint_1'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_CardinalPoint = "'" + (block.getFieldValue('CardinalPoint') || '') + "'";
    var v_Mirror2 = "'" + (block.getFieldValue('Mirror2') || '') + "'";
    var v_Mirror3 = "'" + (block.getFieldValue('Mirror3') || '') + "'";
    var v_StiffTransform = "'" + (block.getFieldValue('StiffTransform') || '') + "'";
    var v_Offset1 = "'" + (block.getFieldValue('Offset1') || '') + "'";
    var v_Offset2 = "'" + (block.getFieldValue('Offset2') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'raw = SapModel.FrameObj.SetInsertionPoint_1(' + v_Name + ', ' + v_CardinalPoint + ', ' + v_Mirror2 + ', ' + v_Mirror3 + ', ' + v_StiffTransform + ', ' + v_Offset1 + ', ' + v_Offset2 + ', ' + v_ItemType + ')\n';
    code += 'offset1_ = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "FrameObj.SetInsertionPoint_1 failed: " + str(ret_code)\n';
    return code;
  };

  // FrameObj.GetInsertionPoint_1
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetInsertionPoint_1'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_CardinalPoint = "'" + (block.getFieldValue('CardinalPoint') || '') + "'";
    var v_Mirror2 = "'" + (block.getFieldValue('Mirror2') || '') + "'";
    var v_StiffTransform = "'" + (block.getFieldValue('StiffTransform') || '') + "'";
    var v_Offset1 = "'" + (block.getFieldValue('Offset1') || '') + "'";
    var v_Offset2 = "'" + (block.getFieldValue('Offset2') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.GetInsertionPoint_1(' + v_Name + ', ' + v_CardinalPoint + ', ' + v_Mirror2 + ', ' + v_StiffTransform + ', ' + v_Offset1 + ', ' + v_Offset2 + ')\n';
    code += 'assert ret == 0, "FrameObj.GetInsertionPoint_1 failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetLocalAxes
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetLocalAxes'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Ang = "'" + (block.getFieldValue('Ang') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.FrameObj.SetLocalAxes(' + v_Name + ', ' + v_Ang + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "FrameObj.SetLocalAxes failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.GetLocalAxes
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetLocalAxes'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Ang = "'" + (block.getFieldValue('Ang') || '') + "'";
    var v_Advanced = "'" + (block.getFieldValue('Advanced') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.GetLocalAxes(' + v_Name + ', ' + v_Ang + ', ' + v_Advanced + ')\n';
    code += 'assert ret == 0, "FrameObj.GetLocalAxes failed: " + str(ret)\n';
    return code;
  };

  // GroupDef.SetGroup
  pythonGenerator.forBlock['sap_SapModel_GroupDef_SetGroup'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_SpecifiedForSelection = "'" + (block.getFieldValue('SpecifiedForSelection') || '') + "'";
    var v_SpecifiedForSectionCutDefinition = "'" + (block.getFieldValue('SpecifiedForSectionCutDefinition') || '') + "'";
    var v_SpecifiedForSteelDesign = "'" + (block.getFieldValue('SpecifiedForSteelDesign') || '') + "'";
    var v_SpecifiedForConcreteDesign = "'" + (block.getFieldValue('SpecifiedForConcreteDesign') || '') + "'";
    var v_SpecifiedForAluminumDesign = "'" + (block.getFieldValue('SpecifiedForAluminumDesign') || '') + "'";
    var v_SpecifiedForColdFormedDesign = "'" + (block.getFieldValue('SpecifiedForColdFormedDesign') || '') + "'";
    var v_SpecifiedForStaticNLActiveStage = "'" + (block.getFieldValue('SpecifiedForStaticNLActiveStage') || '') + "'";
    var v_SpecifiedForBridgeResponseOutput = "'" + (block.getFieldValue('SpecifiedForBridgeResponseOutput') || '') + "'";
    var v_SpecifiedForAutoSeismicOutput = "'" + (block.getFieldValue('SpecifiedForAutoSeismicOutput') || '') + "'";
    var v_SpecifiedForAutoWindOutput = "'" + (block.getFieldValue('SpecifiedForAutoWindOutput') || '') + "'";
    var v_SpecifiedForMassAndWeight = "'" + (block.getFieldValue('SpecifiedForMassAndWeight') || '') + "'";
    var code = '';
    code += 'ret = SapModel.GroupDef.SetGroup(' + v_Name + ', ' + v_SpecifiedForSelection + ', ' + v_SpecifiedForSectionCutDefinition + ', ' + v_SpecifiedForSteelDesign + ', ' + v_SpecifiedForConcreteDesign + ', ' + v_SpecifiedForAluminumDesign + ', ' + v_SpecifiedForColdFormedDesign + ', ' + v_SpecifiedForStaticNLActiveStage + ', ' + v_SpecifiedForBridgeResponseOutput + ', ' + v_SpecifiedForAutoSeismicOutput + ', ' + v_SpecifiedForAutoWindOutput + ', ' + v_SpecifiedForMassAndWeight + ')\n';
    code += 'assert ret == 0, "GroupDef.SetGroup failed: " + str(ret)\n';
    return code;
  };

  // GroupDef.GetNameList
  pythonGenerator.forBlock['sap_SapModel_GroupDef_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.GroupDef.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "GroupDef.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetGroupAssign
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetGroupAssign'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_Remove = "'" + (block.getFieldValue('Remove') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.FrameObj.SetGroupAssign(' + v_Name + ', ' + v_GroupName + ', ' + v_Remove + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "FrameObj.SetGroupAssign failed: " + str(ret)\n';
    return code;
  };

  // GroupDef.GetAssignments
  pythonGenerator.forBlock['sap_SapModel_GroupDef_GetAssignments'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_ObjectType = "'" + (block.getFieldValue('ObjectType') || '') + "'";
    var v_ObjectName = "'" + (block.getFieldValue('ObjectName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.GroupDef.GetAssignments(' + v_Name + ', ' + v_NumberItems + ', ' + v_ObjectType + ', ' + v_ObjectName + ')\n';
    code += 'assert ret == 0, "GroupDef.GetAssignments failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.SetGroupAssign
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetGroupAssign'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_GroupName = "'" + (block.getFieldValue('GroupName') || '') + "'";
    var v_Remove = "'" + (block.getFieldValue('Remove') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.AreaObj.SetGroupAssign(' + v_Name + ', ' + v_GroupName + ', ' + v_Remove + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "AreaObj.SetGroupAssign failed: " + str(ret)\n';
    return code;
  };

  // ConstraintDef.SetDiaphragm
  pythonGenerator.forBlock['sap_SapModel_ConstraintDef_SetDiaphragm'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Axis = "'" + (block.getFieldValue('Axis') || '') + "'";
    var code = '';
    code += 'ret = SapModel.ConstraintDef.SetDiaphragm(' + v_Name + ', ' + v_Axis + ')\n';
    code += 'assert ret == 0, "ConstraintDef.SetDiaphragm failed: " + str(ret)\n';
    return code;
  };

  // ConstraintDef.GetDiaphragm
  pythonGenerator.forBlock['sap_SapModel_ConstraintDef_GetDiaphragm'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Axis = "'" + (block.getFieldValue('Axis') || '') + "'";
    var code = '';
    code += 'ret = SapModel.ConstraintDef.GetDiaphragm(' + v_Name + ', ' + v_Axis + ')\n';
    code += 'assert ret == 0, "ConstraintDef.GetDiaphragm failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.GetPoints
  pythonGenerator.forBlock['sap_SapModel_AreaObj_GetPoints'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberPoints = "'" + (block.getFieldValue('NumberPoints') || '') + "'";
    var v_Point = "'" + (block.getFieldValue('Point') || '') + "'";
    var code = '';
    code += 'ret = SapModel.AreaObj.GetPoints(' + v_Name + ', ' + v_NumberPoints + ', ' + v_Point + ')\n';
    code += 'assert ret == 0, "AreaObj.GetPoints failed: " + str(ret)\n';
    return code;
  };

  // Results.AreaStressShell
  pythonGenerator.forBlock['sap_SapModel_Results_AreaStressShell'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ItemTypeElm = block.getFieldValue('ItemTypeElm') || '0';
    var v_NumberResults = "'" + (block.getFieldValue('NumberResults') || '') + "'";
    var v_Obj = "'" + (block.getFieldValue('Obj') || '') + "'";
    var v_Elm = "'" + (block.getFieldValue('Elm') || '') + "'";
    var v_PointElm = "'" + (block.getFieldValue('PointElm') || '') + "'";
    var v_LoadCase = "'" + (block.getFieldValue('LoadCase') || '') + "'";
    var v_StepType = "'" + (block.getFieldValue('StepType') || '') + "'";
    var v_StepNum = "'" + (block.getFieldValue('StepNum') || '') + "'";
    var v_S11Top = "'" + (block.getFieldValue('S11Top') || '') + "'";
    var v_S22Top = "'" + (block.getFieldValue('S22Top') || '') + "'";
    var v_S12Top = "'" + (block.getFieldValue('S12Top') || '') + "'";
    var v_SMaxTop = "'" + (block.getFieldValue('SMaxTop') || '') + "'";
    var v_SMinTop = "'" + (block.getFieldValue('SMinTop') || '') + "'";
    var v_SAngleTop = "'" + (block.getFieldValue('SAngleTop') || '') + "'";
    var v_SVMTop = "'" + (block.getFieldValue('SVMTop') || '') + "'";
    var v_S11Bot = "'" + (block.getFieldValue('S11Bot') || '') + "'";
    var v_S22Bot = "'" + (block.getFieldValue('S22Bot') || '') + "'";
    var v_S12Bot = "'" + (block.getFieldValue('S12Bot') || '') + "'";
    var v_SMaxBot = "'" + (block.getFieldValue('SMaxBot') || '') + "'";
    var v_SMinBot = "'" + (block.getFieldValue('SMinBot') || '') + "'";
    var v_SAngleBot = "'" + (block.getFieldValue('SAngleBot') || '') + "'";
    var v_SVMBot = "'" + (block.getFieldValue('SVMBot') || '') + "'";
    var v_S13Avg = "'" + (block.getFieldValue('S13Avg') || '') + "'";
    var v_S23Avg = "'" + (block.getFieldValue('S23Avg') || '') + "'";
    var v_SMaxAvg = "'" + (block.getFieldValue('SMaxAvg') || '') + "'";
    var v_SAngleAvg = "'" + (block.getFieldValue('SAngleAvg') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.AreaStressShell(' + v_Name + ', ' + v_ItemTypeElm + ', ' + v_NumberResults + ', ' + v_Obj + ', ' + v_Elm + ', ' + v_PointElm + ', ' + v_LoadCase + ', ' + v_StepType + ', ' + v_StepNum + ', ' + v_S11Top + ', ' + v_S22Top + ', ' + v_S12Top + ', ' + v_SMaxTop + ', ' + v_SMinTop + ', ' + v_SAngleTop + ', ' + v_SVMTop + ', ' + v_S11Bot + ', ' + v_S22Bot + ', ' + v_S12Bot + ', ' + v_SMaxBot + ', ' + v_SMinBot + ', ' + v_SAngleBot + ', ' + v_SVMBot + ', ' + v_S13Avg + ', ' + v_S23Avg + ', ' + v_SMaxAvg + ', ' + v_SAngleAvg + ')\n';
    code += 'assert ret == 0, "Results.AreaStressShell failed: " + str(ret)\n';
    return code;
  };

  // PointObj.GetNameList
  pythonGenerator.forBlock['sap_SapModel_PointObj_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PointObj.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "PointObj.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // Results.ModalPeriod
  pythonGenerator.forBlock['sap_SapModel_Results_ModalPeriod'] = function(block, generator) {
    var v_NumberResults = "'" + (block.getFieldValue('NumberResults') || '') + "'";
    var v_LoadCase = "'" + (block.getFieldValue('LoadCase') || '') + "'";
    var v_StepType = "'" + (block.getFieldValue('StepType') || '') + "'";
    var v_StepNum = "'" + (block.getFieldValue('StepNum') || '') + "'";
    var v_Period = "'" + (block.getFieldValue('Period') || '') + "'";
    var v_Frequency = "'" + (block.getFieldValue('Frequency') || '') + "'";
    var v_CircFreq = "'" + (block.getFieldValue('CircFreq') || '') + "'";
    var v_EigenValue = "'" + (block.getFieldValue('EigenValue') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.ModalPeriod(' + v_NumberResults + ', ' + v_LoadCase + ', ' + v_StepType + ', ' + v_StepNum + ', ' + v_Period + ', ' + v_Frequency + ', ' + v_CircFreq + ', ' + v_EigenValue + ')\n';
    code += 'assert ret == 0, "Results.ModalPeriod failed: " + str(ret)\n';
    return code;
  };

  // Results.ModalParticipatingMassRatios
  pythonGenerator.forBlock['sap_SapModel_Results_ModalParticipatingMassRatios'] = function(block, generator) {
    var v_NumberResults = "'" + (block.getFieldValue('NumberResults') || '') + "'";
    var v_LoadCase = "'" + (block.getFieldValue('LoadCase') || '') + "'";
    var v_StepType = "'" + (block.getFieldValue('StepType') || '') + "'";
    var v_StepNum = "'" + (block.getFieldValue('StepNum') || '') + "'";
    var v_Period = "'" + (block.getFieldValue('Period') || '') + "'";
    var v_Ux = "'" + (block.getFieldValue('Ux') || '') + "'";
    var v_Uy = "'" + (block.getFieldValue('Uy') || '') + "'";
    var v_Uz = "'" + (block.getFieldValue('Uz') || '') + "'";
    var v_SumUx = "'" + (block.getFieldValue('SumUx') || '') + "'";
    var v_SumUy = "'" + (block.getFieldValue('SumUy') || '') + "'";
    var v_SumUz = "'" + (block.getFieldValue('SumUz') || '') + "'";
    var v_Rx = "'" + (block.getFieldValue('Rx') || '') + "'";
    var v_Ry = "'" + (block.getFieldValue('Ry') || '') + "'";
    var v_Rz = "'" + (block.getFieldValue('Rz') || '') + "'";
    var v_SumRx = "'" + (block.getFieldValue('SumRx') || '') + "'";
    var v_SumRy = "'" + (block.getFieldValue('SumRy') || '') + "'";
    var v_SumRz = "'" + (block.getFieldValue('SumRz') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.ModalParticipatingMassRatios(' + v_NumberResults + ', ' + v_LoadCase + ', ' + v_StepType + ', ' + v_StepNum + ', ' + v_Period + ', ' + v_Ux + ', ' + v_Uy + ', ' + v_Uz + ', ' + v_SumUx + ', ' + v_SumUy + ', ' + v_SumUz + ', ' + v_Rx + ', ' + v_Ry + ', ' + v_Rz + ', ' + v_SumRx + ', ' + v_SumRy + ', ' + v_SumRz + ')\n';
    code += 'assert ret == 0, "Results.ModalParticipatingMassRatios failed: " + str(ret)\n';
    return code;
  };

  // Results.ModeShape
  pythonGenerator.forBlock['sap_SapModel_Results_ModeShape'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ItemTypeElm = block.getFieldValue('ItemTypeElm') || '0';
    var v_NumberResults = "'" + (block.getFieldValue('NumberResults') || '') + "'";
    var v_Obj = "'" + (block.getFieldValue('Obj') || '') + "'";
    var v_Elm = "'" + (block.getFieldValue('Elm') || '') + "'";
    var v_LoadCase = "'" + (block.getFieldValue('LoadCase') || '') + "'";
    var v_StepType = "'" + (block.getFieldValue('StepType') || '') + "'";
    var v_StepNum = "'" + (block.getFieldValue('StepNum') || '') + "'";
    var v_U1 = "'" + (block.getFieldValue('U1') || '') + "'";
    var v_U2 = "'" + (block.getFieldValue('U2') || '') + "'";
    var v_U3 = "'" + (block.getFieldValue('U3') || '') + "'";
    var v_R1 = "'" + (block.getFieldValue('R1') || '') + "'";
    var v_R2 = "'" + (block.getFieldValue('R2') || '') + "'";
    var v_R3 = "'" + (block.getFieldValue('R3') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Results.ModeShape(' + v_Name + ', ' + v_ItemTypeElm + ', ' + v_NumberResults + ', ' + v_Obj + ', ' + v_Elm + ', ' + v_LoadCase + ', ' + v_StepType + ', ' + v_StepNum + ', ' + v_U1 + ', ' + v_U2 + ', ' + v_U3 + ', ' + v_R1 + ', ' + v_R2 + ', ' + v_R3 + ')\n';
    code += 'assert ret == 0, "Results.ModeShape failed: " + str(ret)\n';
    return code;
  };

  // Analyze.SetActiveDOF
  pythonGenerator.forBlock['sap_SapModel_Analyze_SetActiveDOF'] = function(block, generator) {
    var v_DOF = "'" + (block.getFieldValue('DOF') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Analyze.SetActiveDOF(' + v_DOF + ')\n';
    code += 'assert ret == 0, "Analyze.SetActiveDOF failed: " + str(ret)\n';
    return code;
  };

  // Analyze.GetActiveDOF
  pythonGenerator.forBlock['sap_SapModel_Analyze_GetActiveDOF'] = function(block, generator) {
    var v_DOF = "'" + (block.getFieldValue('DOF') || '') + "'";
    var code = '';
    code += 'raw = SapModel.Analyze.GetActiveDOF(' + v_DOF + ')\n';
    code += 'dof_ = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "Analyze.GetActiveDOF failed: " + str(ret_code)\n';
    return code;
  };

  // Analyze.GetCaseStatus
  pythonGenerator.forBlock['sap_SapModel_Analyze_GetCaseStatus'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_CaseName = "'" + (block.getFieldValue('CaseName') || '') + "'";
    var v_Status = "'" + (block.getFieldValue('Status') || '') + "'";
    var code = '';
    code += 'ret = SapModel.Analyze.GetCaseStatus(' + v_NumberItems + ', ' + v_CaseName + ', ' + v_Status + ')\n';
    code += 'assert ret == 0, "Analyze.GetCaseStatus failed: " + str(ret)\n';
    return code;
  };

  // File.OpenFile
  pythonGenerator.forBlock['sap_SapModel_File_OpenFile'] = function(block, generator) {
    var v_FileName = "'" + (block.getFieldValue('FileName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.File.OpenFile(' + v_FileName + ')\n';
    code += 'assert ret == 0, "File.OpenFile failed: " + str(ret)\n';
    return code;
  };

  // PropLink.SetLinear
  pythonGenerator.forBlock['sap_SapModel_PropLink_SetLinear'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_DOF = "'" + (block.getFieldValue('DOF') || '') + "'";
    var v_Fixed = "'" + (block.getFieldValue('Fixed') || '') + "'";
    var v_Ke = "'" + (block.getFieldValue('Ke') || '') + "'";
    var v_Ce = "'" + (block.getFieldValue('Ce') || '') + "'";
    var v_dj2 = "'" + (block.getFieldValue('dj2') || '') + "'";
    var v_dj3 = "'" + (block.getFieldValue('dj3') || '') + "'";
    var v_KeCoupled = "'" + (block.getFieldValue('KeCoupled') || '') + "'";
    var v_CeCoupled = "'" + (block.getFieldValue('CeCoupled') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropLink.SetLinear(' + v_Name + ', ' + v_DOF + ', ' + v_Fixed + ', ' + v_Ke + ', ' + v_Ce + ', ' + v_dj2 + ', ' + v_dj3 + ', ' + v_KeCoupled + ', ' + v_CeCoupled + ')\n';
    code += 'assert ret == 0, "PropLink.SetLinear failed: " + str(ret)\n';
    return code;
  };

  // PropLink.GetLinear
  pythonGenerator.forBlock['sap_SapModel_PropLink_GetLinear'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_DOF = "'" + (block.getFieldValue('DOF') || '') + "'";
    var v_Fixed = "'" + (block.getFieldValue('Fixed') || '') + "'";
    var v_Ke = "'" + (block.getFieldValue('Ke') || '') + "'";
    var v_Ce = "'" + (block.getFieldValue('Ce') || '') + "'";
    var v_DJ2 = "'" + (block.getFieldValue('DJ2') || '') + "'";
    var v_DJ3 = "'" + (block.getFieldValue('DJ3') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropLink.GetLinear(' + v_Name + ', ' + v_DOF + ', ' + v_Fixed + ', ' + v_Ke + ', ' + v_Ce + ', ' + v_DJ2 + ', ' + v_DJ3 + ')\n';
    code += 'assert ret == 0, "PropLink.GetLinear failed: " + str(ret)\n';
    return code;
  };

  // LinkObj.AddByPoint
  pythonGenerator.forBlock['sap_SapModel_LinkObj_AddByPoint'] = function(block, generator) {
    var v_Point1 = "'" + (block.getFieldValue('Point1') || '') + "'";
    var v_Point2 = "'" + (block.getFieldValue('Point2') || '') + "'";
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_IsSingleJoint = "'" + (block.getFieldValue('IsSingleJoint') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_UserName = "'" + (block.getFieldValue('UserName') || '') + "'";
    var code = '';
    code += 'raw = SapModel.LinkObj.AddByPoint(' + v_Point1 + ', ' + v_Point2 + ', ' + v_Name + ', ' + v_IsSingleJoint + ', ' + v_PropName + ', ' + v_UserName + ')\n';
    code += 'name_assigned = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "LinkObj.AddByPoint failed: " + str(ret_code)\n';
    return code;
  };

  // LinkObj.Count
  pythonGenerator.forBlock['sap_SapModel_LinkObj_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.LinkObj.Count()\n';
    code += 'assert ret == 0, "LinkObj.Count failed"\n';
    return code;
  };

  // LinkObj.AddByCoord
  pythonGenerator.forBlock['sap_SapModel_LinkObj_AddByCoord'] = function(block, generator) {
    var v_xi = block.getFieldValue('xi') || '0';
    var v_yi = block.getFieldValue('yi') || '0';
    var v_zi = block.getFieldValue('zi') || '0';
    var v_xj = block.getFieldValue('xj') || '0';
    var v_yj = block.getFieldValue('yj') || '0';
    var v_zj = block.getFieldValue('zj') || '0';
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_IsSingleJoint = "'" + (block.getFieldValue('IsSingleJoint') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_UserName = "'" + (block.getFieldValue('UserName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LinkObj.AddByCoord(' + v_xi + ', ' + v_yi + ', ' + v_zi + ', ' + v_xj + ', ' + v_yj + ', ' + v_zj + ', ' + v_Name + ', ' + v_IsSingleJoint + ', ' + v_PropName + ', ' + v_UserName + ')\n';
    code += 'assert ret == 0, "LinkObj.AddByCoord failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.GetProperty
  pythonGenerator.forBlock['sap_SapModel_AreaObj_GetProperty'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_SAuto = "'" + (block.getFieldValue('SAuto') || '') + "'";
    var code = '';
    code += 'ret = SapModel.AreaObj.GetProperty(' + v_Name + ', ' + v_PropName + ', ' + v_SAuto + ')\n';
    code += 'assert ret == 0, "AreaObj.GetProperty failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.SetProperty
  pythonGenerator.forBlock['sap_SapModel_AreaObj_SetProperty'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.AreaObj.SetProperty(' + v_Name + ', ' + v_PropName + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "AreaObj.SetProperty failed: " + str(ret)\n';
    return code;
  };

  // PropArea.GetShell_1
  pythonGenerator.forBlock['sap_SapModel_PropArea_GetShell_1'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ShellType = block.getFieldValue('ShellType') || '1';
    var v_IncludeDrillingDOF = "'" + (block.getFieldValue('IncludeDrillingDOF') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_MatAng = "'" + (block.getFieldValue('MatAng') || '') + "'";
    var v_Thickness = "'" + (block.getFieldValue('Thickness') || '') + "'";
    var v_Bending = "'" + (block.getFieldValue('Bending') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropArea.GetShell_1(' + v_Name + ', ' + v_ShellType + ', ' + v_IncludeDrillingDOF + ', ' + v_MatProp + ', ' + v_MatAng + ', ' + v_Thickness + ', ' + v_Bending + ')\n';
    code += 'assert ret == 0, "PropArea.GetShell_1 failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.SetOSteel_1
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_SetOSteel_1'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Fy = "'" + (block.getFieldValue('Fy') || '') + "'";
    var v_Fu = "'" + (block.getFieldValue('Fu') || '') + "'";
    var v_EFy = "'" + (block.getFieldValue('EFy') || '') + "'";
    var v_EFu = "'" + (block.getFieldValue('EFu') || '') + "'";
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
    var v_DilatationalAngle = "'" + (block.getFieldValue('DilatationalAngle') || '') + "'";
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
    var v_A = block.getFieldValue('A') || '0';
    var code = '';
    code += 'ret = SapModel.PropMaterial.GetMPIsotropic(' + v_Name + ', ' + v_E + ', ' + v_U + ', ' + v_A + ')\n';
    code += 'assert ret == 0, "PropMaterial.GetMPIsotropic failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.GetNameList
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropMaterial.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "PropMaterial.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetAngle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetAngle'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var v_TF = block.getFieldValue('TF') || '0';
    var v_TW = block.getFieldValue('TW') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetAngle(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ', ' + v_TF + ', ' + v_TW + ')\n';
    code += 'assert ret == 0, "PropFrame.SetAngle failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetChannel
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetChannel'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var v_TF = block.getFieldValue('TF') || '0';
    var v_TW = block.getFieldValue('TW') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetChannel(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ', ' + v_TF + ', ' + v_TW + ')\n';
    code += 'assert ret == 0, "PropFrame.SetChannel failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.SetPipe
  pythonGenerator.forBlock['sap_SapModel_PropFrame_SetPipe'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_TW = block.getFieldValue('TW') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.SetPipe(' + v_Name + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_TW + ')\n';
    code += 'assert ret == 0, "PropFrame.SetPipe failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.GetRectangle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_GetRectangle'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_FileName = "'" + (block.getFieldValue('FileName') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.GetRectangle(' + v_Name + ', ' + v_FileName + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ')\n';
    code += 'assert ret == 0, "PropFrame.GetRectangle failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.GetCircle
  pythonGenerator.forBlock['sap_SapModel_PropFrame_GetCircle'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_FileName = "'" + (block.getFieldValue('FileName') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.GetCircle(' + v_Name + ', ' + v_FileName + ', ' + v_MatProp + ', ' + v_T3 + ')\n';
    code += 'assert ret == 0, "PropFrame.GetCircle failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.GetISection
  pythonGenerator.forBlock['sap_SapModel_PropFrame_GetISection'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_FileName = "'" + (block.getFieldValue('FileName') || '') + "'";
    var v_MatProp = "'" + (block.getFieldValue('MatProp') || '') + "'";
    var v_T3 = block.getFieldValue('T3') || '0';
    var v_T2 = block.getFieldValue('T2') || '0';
    var v_TF = block.getFieldValue('TF') || '0';
    var v_TW = block.getFieldValue('TW') || '0';
    var v_T2B = block.getFieldValue('T2B') || '0';
    var v_TFB = block.getFieldValue('TFB') || '0';
    var code = '';
    code += 'ret = SapModel.PropFrame.GetISection(' + v_Name + ', ' + v_FileName + ', ' + v_MatProp + ', ' + v_T3 + ', ' + v_T2 + ', ' + v_TF + ', ' + v_TW + ', ' + v_T2B + ', ' + v_TFB + ')\n';
    code += 'assert ret == 0, "PropFrame.GetISection failed: " + str(ret)\n';
    return code;
  };

  // DesignSteel.SetComboStrength
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_SetComboStrength'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Selected = "'" + (block.getFieldValue('Selected') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DesignSteel.SetComboStrength(' + v_Name + ', ' + v_Selected + ')\n';
    code += 'assert ret == 0, "DesignSteel.SetComboStrength failed: " + str(ret)\n';
    return code;
  };

  // DesignSteel.GetComboStrength
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_GetComboStrength'] = function(block, generator) {
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_MyName__ = "'" + (block.getFieldValue('MyName[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DesignSteel.GetComboStrength(' + v_NumberItems + ', ' + v_MyName__ + ')\n';
    code += 'assert ret == 0, "DesignSteel.GetComboStrength failed: " + str(ret)\n';
    return code;
  };

  // DesignSteel.SetComboDeflection
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_SetComboDeflection'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Selected = "'" + (block.getFieldValue('Selected') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DesignSteel.SetComboDeflection(' + v_Name + ', ' + v_Selected + ')\n';
    code += 'assert ret == 0, "DesignSteel.SetComboDeflection failed: " + str(ret)\n';
    return code;
  };

  // DesignSteel.GetCode
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_GetCode'] = function(block, generator) {
    var v_CodeName = "'" + (block.getFieldValue('CodeName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DesignSteel.GetCode(' + v_CodeName + ')\n';
    code += 'assert ret == 0, "DesignSteel.GetCode failed: " + str(ret)\n';
    return code;
  };

  // DesignSteel.SetCode
  pythonGenerator.forBlock['sap_SapModel_DesignSteel_SetCode'] = function(block, generator) {
    var v_CodeName = "'" + (block.getFieldValue('CodeName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DesignSteel.SetCode(' + v_CodeName + ')\n';
    code += 'assert ret == 0, "DesignSteel.SetCode failed: " + str(ret)\n';
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
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Selected = "'" + (block.getFieldValue('Selected') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DesignConcrete.SetComboStrength(' + v_Name + ', ' + v_Selected + ')\n';
    code += 'assert ret == 0, "DesignConcrete.SetComboStrength failed: " + str(ret)\n';
    return code;
  };

  // DesignConcrete.GetCode
  pythonGenerator.forBlock['sap_SapModel_DesignConcrete_GetCode'] = function(block, generator) {
    var v_CodeName = "'" + (block.getFieldValue('CodeName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DesignConcrete.GetCode(' + v_CodeName + ')\n';
    code += 'assert ret == 0, "DesignConcrete.GetCode failed: " + str(ret)\n';
    return code;
  };

  // DesignConcrete.SetCode
  pythonGenerator.forBlock['sap_SapModel_DesignConcrete_SetCode'] = function(block, generator) {
    var v_CodeName = "'" + (block.getFieldValue('CodeName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.DesignConcrete.SetCode(' + v_CodeName + ')\n';
    code += 'assert ret == 0, "DesignConcrete.SetCode failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.Delete
  pythonGenerator.forBlock['sap_SapModel_RespCombo_Delete'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.RespCombo.Delete(' + v_Name + ')\n';
    code += 'assert ret == 0, "RespCombo.Delete failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.ChangeName
  pythonGenerator.forBlock['sap_SapModel_RespCombo_ChangeName'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NewName = "'" + (block.getFieldValue('NewName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.RespCombo.ChangeName(' + v_Name + ', ' + v_NewName + ')\n';
    code += 'assert ret == 0, "RespCombo.ChangeName failed: " + str(ret)\n';
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
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ComboType = block.getFieldValue('ComboType') || '0';
    var code = '';
    code += 'ret = SapModel.RespCombo.SetTypeOAPI(' + v_Name + ', ' + v_ComboType + ')\n';
    code += 'assert ret == 0, "RespCombo.SetTypeOAPI failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.GetTypeOAPI
  pythonGenerator.forBlock['sap_SapModel_RespCombo_GetTypeOAPI'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.RespCombo.GetTypeOAPI(' + v_Name + ')\n';
    code += 'assert ret == 0, "RespCombo.GetTypeOAPI failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.DeleteCase
  pythonGenerator.forBlock['sap_SapModel_RespCombo_DeleteCase'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_CType = "'" + (block.getFieldValue('CType') || '') + "'";
    var v_CName = "'" + (block.getFieldValue('CName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.RespCombo.DeleteCase(' + v_Name + ', ' + v_CType + ', ' + v_CName + ')\n';
    code += 'assert ret == 0, "RespCombo.DeleteCase failed: " + str(ret)\n';
    return code;
  };

  // RespCombo.AddDesignDefaultCombos
  pythonGenerator.forBlock['sap_SapModel_RespCombo_AddDesignDefaultCombos'] = function(block, generator) {
    var v_DesignSteel = "'" + (block.getFieldValue('DesignSteel') || '') + "'";
    var v_DesignConcrete = "'" + (block.getFieldValue('DesignConcrete') || '') + "'";
    var v_DesignAluminum = "'" + (block.getFieldValue('DesignAluminum') || '') + "'";
    var v_DesignColdFormed = "'" + (block.getFieldValue('DesignColdFormed') || '') + "'";
    var code = '';
    code += 'ret = SapModel.RespCombo.AddDesignDefaultCombos(' + v_DesignSteel + ', ' + v_DesignConcrete + ', ' + v_DesignAluminum + ', ' + v_DesignColdFormed + ')\n';
    code += 'assert ret == 0, "RespCombo.AddDesignDefaultCombos failed: " + str(ret)\n';
    return code;
  };

  // File.New2DFrame
  pythonGenerator.forBlock['sap_SapModel_File_New2DFrame'] = function(block, generator) {
    var v_TemplateName = "'" + (block.getFieldValue('TemplateName') || '') + "'";
    var v_NumberStorys = block.getFieldValue('NumberStorys') || '0';
    var v_StoryHeight = block.getFieldValue('StoryHeight') || '0';
    var v_NumberBays = block.getFieldValue('NumberBays') || '0';
    var v_BayWidth = block.getFieldValue('BayWidth') || '0';
    var v_OverWrite = block.getFieldValue('OverWrite') || '0';
    var v_RestraintType = block.getFieldValue('RestraintType') || '0';
    var code = '';
    code += 'ret = SapModel.File.New2DFrame(' + v_TemplateName + ', ' + v_NumberStorys + ', ' + v_StoryHeight + ', ' + v_NumberBays + ', ' + v_BayWidth + ', ' + v_OverWrite + ', ' + v_RestraintType + ')\n';
    code += 'assert ret == 0, "File.New2DFrame failed: " + str(ret)\n';
    return code;
  };

  // SapModel.GetVersion
  pythonGenerator.forBlock['sap_SapModel_GetVersion'] = function(block, generator) {
    var v_Version = "'" + (block.getFieldValue('Version') || '') + "'";
    var code = '';
    code += 'ret = SapModel.GetVersion(' + v_Version + ')\n';
    code += 'assert ret == 0, "SapModel.GetVersion failed: " + str(ret)\n';
    return code;
  };

  // ResponseSpectrum.SetDampConstant
  pythonGenerator.forBlock['sap_SapModel_LoadCases_ResponseSpectrum_SetDampConstant'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Damp = "'" + (block.getFieldValue('Damp') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant(' + v_Name + ', ' + v_Damp + ')\n';
    code += 'assert ret == 0, "ResponseSpectrum.SetDampConstant failed: " + str(ret)\n';
    return code;
  };

  // LoadCases.Count
  pythonGenerator.forBlock['sap_SapModel_LoadCases_Count'] = function(block, generator) {
    var v_CaseType = "'" + (block.getFieldValue('CaseType') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadCases.Count(' + v_CaseType + ')\n';
    code += 'assert ret == 0, "LoadCases.Count failed: " + str(ret)\n';
    return code;
  };

  // LoadCases.Delete
  pythonGenerator.forBlock['sap_SapModel_LoadCases_Delete'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadCases.Delete(' + v_Name + ')\n';
    code += 'assert ret == 0, "LoadCases.Delete failed: " + str(ret)\n';
    return code;
  };

  // LoadCases.ChangeName
  pythonGenerator.forBlock['sap_SapModel_LoadCases_ChangeName'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NewName = "'" + (block.getFieldValue('NewName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadCases.ChangeName(' + v_Name + ', ' + v_NewName + ')\n';
    code += 'assert ret == 0, "LoadCases.ChangeName failed: " + str(ret)\n';
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
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadPatterns.Delete(' + v_Name + ')\n';
    code += 'assert ret == 0, "LoadPatterns.Delete failed: " + str(ret)\n';
    return code;
  };

  // LoadPatterns.ChangeName
  pythonGenerator.forBlock['sap_SapModel_LoadPatterns_ChangeName'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NewName = "'" + (block.getFieldValue('NewName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadPatterns.ChangeName(' + v_Name + ', ' + v_NewName + ')\n';
    code += 'assert ret == 0, "LoadPatterns.ChangeName failed: " + str(ret)\n';
    return code;
  };

  // SourceMass.SetMassSource
  pythonGenerator.forBlock['sap_SapModel_SourceMass_SetMassSource'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MassFromElements = "'" + (block.getFieldValue('MassFromElements') || '') + "'";
    var v_MassFromMasses = "'" + (block.getFieldValue('MassFromMasses') || '') + "'";
    var v_MassFromLoads = "'" + (block.getFieldValue('MassFromLoads') || '') + "'";
    var v_IsDefault = "'" + (block.getFieldValue('IsDefault') || '') + "'";
    var v_NumberLoads = "'" + (block.getFieldValue('NumberLoads') || '') + "'";
    var v_LoadPat__ = "'" + (block.getFieldValue('LoadPat[]') || '') + "'";
    var v_SF__ = "'" + (block.getFieldValue('SF[]') || '') + "'";
    var code = '';
    code += 'raw = SapModel.SourceMass.SetMassSource(' + v_Name + ', ' + v_MassFromElements + ', ' + v_MassFromMasses + ', ' + v_MassFromLoads + ', ' + v_IsDefault + ', ' + v_NumberLoads + ', ' + v_LoadPat__ + ', ' + v_SF__ + ')\n';
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
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MassFromElements = "'" + (block.getFieldValue('MassFromElements') || '') + "'";
    var v_MassFromMasses = "'" + (block.getFieldValue('MassFromMasses') || '') + "'";
    var v_MassFromLoads = "'" + (block.getFieldValue('MassFromLoads') || '') + "'";
    var v_IsDefault = "'" + (block.getFieldValue('IsDefault') || '') + "'";
    var v_NumberLoads = "'" + (block.getFieldValue('NumberLoads') || '') + "'";
    var v_LoadPat__ = "'" + (block.getFieldValue('LoadPat[]') || '') + "'";
    var v_SF__ = "'" + (block.getFieldValue('SF[]') || '') + "'";
    var code = '';
    code += 'ret = SapModel.SourceMass.GetMassSource(' + v_Name + ', ' + v_MassFromElements + ', ' + v_MassFromMasses + ', ' + v_MassFromLoads + ', ' + v_IsDefault + ', ' + v_NumberLoads + ', ' + v_LoadPat__ + ', ' + v_SF__ + ')\n';
    code += 'assert ret == 0, "SourceMass.GetMassSource failed: " + str(ret)\n';
    return code;
  };

  // SourceMass.GetDefault
  pythonGenerator.forBlock['sap_SapModel_SourceMass_GetDefault'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.SourceMass.GetDefault(' + v_Name + ')\n';
    code += 'assert ret == 0, "SourceMass.GetDefault failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.SetModifiers
  pythonGenerator.forBlock['sap_SapModel_FrameObj_SetModifiers'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var code = '';
    code += 'raw = SapModel.FrameObj.SetModifiers(' + v_Name + ', ' + v_Value + ')\n';
    code += 'value_8 = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "FrameObj.SetModifiers failed: " + str(ret_code)\n';
    return code;
  };

  // FrameObj.GetModifiers
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetModifiers'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var code = '';
    code += 'raw = SapModel.FrameObj.GetModifiers(' + v_Name + ', ' + v_Value + ')\n';
    code += 'value_8 = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "FrameObj.GetModifiers failed: " + str(ret_code)\n';
    return code;
  };

  // PropArea.SetModifiers
  pythonGenerator.forBlock['sap_SapModel_PropArea_SetModifiers'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var code = '';
    code += 'raw = SapModel.PropArea.SetModifiers(' + v_Name + ', ' + v_Value + ')\n';
    code += 'value_10 = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "PropArea.SetModifiers failed: " + str(ret_code)\n';
    return code;
  };

  // PropArea.GetModifiers
  pythonGenerator.forBlock['sap_SapModel_PropArea_GetModifiers'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var code = '';
    code += 'raw = SapModel.PropArea.GetModifiers(' + v_Name + ', ' + v_Value + ')\n';
    code += 'value_10 = raw[0]\n';
    code += 'ret_code = raw[-1]\n';
    code += 'assert ret_code == 0, "PropArea.GetModifiers failed: " + str(ret_code)\n';
    return code;
  };

  // PropFrame.ChangeName
  pythonGenerator.forBlock['sap_SapModel_PropFrame_ChangeName'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NewName = "'" + (block.getFieldValue('NewName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropFrame.ChangeName(' + v_Name + ', ' + v_NewName + ')\n';
    code += 'assert ret == 0, "PropFrame.ChangeName failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.Count
  pythonGenerator.forBlock['sap_SapModel_PropFrame_Count'] = function(block, generator) {
    var v_PropType = "'" + (block.getFieldValue('PropType') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropFrame.Count(' + v_PropType + ')\n';
    code += 'assert ret == 0, "PropFrame.Count failed: " + str(ret)\n';
    return code;
  };

  // PropFrame.Delete
  pythonGenerator.forBlock['sap_SapModel_PropFrame_Delete'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropFrame.Delete(' + v_Name + ')\n';
    code += 'assert ret == 0, "PropFrame.Delete failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.ChangeName
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_ChangeName'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NewName = "'" + (block.getFieldValue('NewName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropMaterial.ChangeName(' + v_Name + ', ' + v_NewName + ')\n';
    code += 'assert ret == 0, "PropMaterial.ChangeName failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.Count
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_Count'] = function(block, generator) {
    var v_MatType = block.getFieldValue('MatType') || '2';
    var code = '';
    code += 'ret = SapModel.PropMaterial.Count(' + v_MatType + ')\n';
    code += 'assert ret == 0, "PropMaterial.Count failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.Delete
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_Delete'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropMaterial.Delete(' + v_Name + ')\n';
    code += 'assert ret == 0, "PropMaterial.Delete failed: " + str(ret)\n';
    return code;
  };

  // PropLink.SetGap
  pythonGenerator.forBlock['sap_SapModel_PropLink_SetGap'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_DOF = "'" + (block.getFieldValue('DOF') || '') + "'";
    var v_Fixed = "'" + (block.getFieldValue('Fixed') || '') + "'";
    var v_Ke = "'" + (block.getFieldValue('Ke') || '') + "'";
    var v_Nonlinear = "'" + (block.getFieldValue('Nonlinear') || '') + "'";
    var v_GapOpens = "'" + (block.getFieldValue('GapOpens') || '') + "'";
    var v_Opens = "'" + (block.getFieldValue('Opens') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropLink.SetGap(' + v_Name + ', ' + v_DOF + ', ' + v_Fixed + ', ' + v_Ke + ', ' + v_Nonlinear + ', ' + v_GapOpens + ', ' + v_Opens + ')\n';
    code += 'assert ret == 0, "PropLink.SetGap failed: " + str(ret)\n';
    return code;
  };

  // PropLink.Count
  pythonGenerator.forBlock['sap_SapModel_PropLink_Count'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.PropLink.Count()\n';
    code += 'assert ret == 0, "PropLink.Count failed"\n';
    return code;
  };

  // AreaObj.AddByPoint
  pythonGenerator.forBlock['sap_SapModel_AreaObj_AddByPoint'] = function(block, generator) {
    var v_NumberPoints = "'" + (block.getFieldValue('NumberPoints') || '') + "'";
    var v_Point = "'" + (block.getFieldValue('Point') || '') + "'";
    var v_PropName = "'" + (block.getFieldValue('PropName') || '') + "'";
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_UserName = "'" + (block.getFieldValue('UserName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.AreaObj.AddByPoint(' + v_NumberPoints + ', ' + v_Point + ', ' + v_PropName + ', ' + v_Name + ', ' + v_UserName + ')\n';
    code += 'assert ret == 0, "AreaObj.AddByPoint failed: " + str(ret)\n';
    return code;
  };

  // ConstraintDef.GetNameList
  pythonGenerator.forBlock['sap_SapModel_ConstraintDef_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.ConstraintDef.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "ConstraintDef.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.GetNameList
  pythonGenerator.forBlock['sap_SapModel_AreaObj_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.AreaObj.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "AreaObj.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // SapModel.GetPresentUnits
  pythonGenerator.forBlock['sap_SapModel_GetPresentUnits'] = function(block, generator) {
    var code = '';
    code += 'ret = SapModel.GetPresentUnits()\n';
    code += 'assert ret == 0, "SapModel.GetPresentUnits failed"\n';
    return code;
  };

  // PropMaterial.AddMaterial
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_AddMaterial'] = function(block, generator) {
    var v_Region = "'" + (block.getFieldValue('Region') || '') + "'";
    var v_Standard = "'" + (block.getFieldValue('Standard') || '') + "'";
    var v_Grade = "'" + (block.getFieldValue('Grade') || '') + "'";
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PropMaterial.AddMaterial(' + v_Region + ', ' + v_Standard + ', ' + v_Grade + ', ' + v_Name + ')\n';
    code += 'assert ret == 0, "PropMaterial.AddMaterial failed: " + str(ret)\n';
    return code;
  };

  // PropMaterial.GetTypeOAPI
  pythonGenerator.forBlock['sap_SapModel_PropMaterial_GetTypeOAPI'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_MatType = block.getFieldValue('MatType') || '2';
    var code = '';
    code += 'ret = SapModel.PropMaterial.GetTypeOAPI(' + v_Name + ', ' + v_MatType + ')\n';
    code += 'assert ret == 0, "PropMaterial.GetTypeOAPI failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.GetGroupAssign
  pythonGenerator.forBlock['sap_SapModel_AreaObj_GetGroupAssign'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberGroups = "'" + (block.getFieldValue('NumberGroups') || '') + "'";
    var v_Groups = "'" + (block.getFieldValue('Groups') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.AreaObj.GetGroupAssign(' + v_Name + ', ' + v_NumberGroups + ', ' + v_Groups + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "AreaObj.GetGroupAssign failed: " + str(ret)\n';
    return code;
  };

  // PointObj.GetRestraint
  pythonGenerator.forBlock['sap_SapModel_PointObj_GetRestraint'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.PointObj.GetRestraint(' + v_Name + ', ' + v_Value + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "PointObj.GetRestraint failed: " + str(ret)\n';
    return code;
  };

  // LoadCases.GetTypeOAPI
  pythonGenerator.forBlock['sap_SapModel_LoadCases_GetTypeOAPI'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_CaseType = "'" + (block.getFieldValue('CaseType') || '') + "'";
    var code = '';
    code += 'ret = SapModel.LoadCases.GetTypeOAPI(' + v_Name + ', ' + v_CaseType + ')\n';
    code += 'assert ret == 0, "LoadCases.GetTypeOAPI failed: " + str(ret)\n';
    return code;
  };

  // SapModel.GetModelFilename
  pythonGenerator.forBlock['sap_SapModel_GetModelFilename'] = function(block, generator) {
    var v_IncludePath = "'" + (block.getFieldValue('IncludePath') || '') + "'";
    var code = '';
    code += 'ret = SapModel.GetModelFilename(' + v_IncludePath + ')\n';
    code += 'assert ret == 0, "SapModel.GetModelFilename failed: " + str(ret)\n';
    return code;
  };

  // SapModel.SetModelIsLocked
  pythonGenerator.forBlock['sap_SapModel_SetModelIsLocked'] = function(block, generator) {
    var v_LockIt = "'" + (block.getFieldValue('LockIt') || '') + "'";
    var code = '';
    code += 'ret = SapModel.SetModelIsLocked(' + v_LockIt + ')\n';
    code += 'assert ret == 0, "SapModel.SetModelIsLocked failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.GetNameList
  pythonGenerator.forBlock['sap_SapModel_FrameObj_GetNameList'] = function(block, generator) {
    var v_NumberNames = "'" + (block.getFieldValue('NumberNames') || '') + "'";
    var v_MyName = "'" + (block.getFieldValue('MyName') || '') + "'";
    var code = '';
    code += 'ret = SapModel.FrameObj.GetNameList(' + v_NumberNames + ', ' + v_MyName + ')\n';
    code += 'assert ret == 0, "FrameObj.GetNameList failed: " + str(ret)\n';
    return code;
  };

  // FrameObj.Delete
  pythonGenerator.forBlock['sap_SapModel_FrameObj_Delete'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.FrameObj.Delete(' + v_Name + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "FrameObj.Delete failed: " + str(ret)\n';
    return code;
  };

  // AreaObj.Delete
  pythonGenerator.forBlock['sap_SapModel_AreaObj_Delete'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var code = '';
    code += 'ret = SapModel.AreaObj.Delete(' + v_Name + ', ' + v_ItemType + ')\n';
    code += 'assert ret == 0, "AreaObj.Delete failed: " + str(ret)\n';
    return code;
  };

  // PointObj.GetLoadForce
  pythonGenerator.forBlock['sap_SapModel_PointObj_GetLoadForce'] = function(block, generator) {
    var v_Name = "'" + (block.getFieldValue('Name') || '') + "'";
    var v_NumberItems = "'" + (block.getFieldValue('NumberItems') || '') + "'";
    var v_PatternName = "'" + (block.getFieldValue('PatternName') || '') + "'";
    var v_ItemType = block.getFieldValue('ItemType') || '0';
    var v_DOF = "'" + (block.getFieldValue('DOF') || '') + "'";
    var v_Value = "'" + (block.getFieldValue('Value') || '') + "'";
    var code = '';
    code += 'ret = SapModel.PointObj.GetLoadForce(' + v_Name + ', ' + v_NumberItems + ', ' + v_PatternName + ', ' + v_ItemType + ', ' + v_DOF + ', ' + v_Value + ')\n';
    code += 'assert ret == 0, "PointObj.GetLoadForce failed: " + str(ret)\n';
    return code;
  };

  console.log('✅ SAP2000 Python generators registered');
}
