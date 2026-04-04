// ===========================================================
// SAP2000 Block Definitions - Auto-generated
// Generated: 2026-04-04 01:14
// DO NOT EDIT MANUALLY - run blockly_generator.py to regenerate
// ===========================================================

function registerSAP2000Blocks() {

  // File.NewBlank
  Blockly.Blocks['sap_SapModel_File_NewBlank'] = {
    init: function() {
      this.setColour(0);
      this.appendDummyInput()
          .appendField('File.NewBlank()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Initialize a new blank model');
    }
  };

  // PropMaterial.SetMaterial
  Blockly.Blocks['sap_SapModel_PropMaterial_SetMaterial'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.SetMaterial')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatType:'))
          .appendField(new Blockly.FieldDropdown([["Steel (1)", "1"], ["Concrete (2)", "2"], ["NoDesign (3)", "3"], ["Aluminum (4)", "4"], ["ColdFormed (5)", "5"], ["Rebar (6)", "6"], ["Tendon (7)", "7"]]), 'MatType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define or modify a material by name and type');
    }
  };

  // PropMaterial.SetMPIsotropic
  Blockly.Blocks['sap_SapModel_PropMaterial_SetMPIsotropic'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.SetMPIsotropic')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('E:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'E');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('U:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'U');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('A:'))
          .appendField(new Blockly.FieldTextInput(''), 'A');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set isotropic mechanical properties (E, Poisson, thermal coeff)');
    }
  };

  // PropMaterial.SetWeightAndMass
  Blockly.Blocks['sap_SapModel_PropMaterial_SetWeightAndMass'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.SetWeightAndMass')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyType:'))
          .appendField(new Blockly.FieldNumber(1, -Infinity, Infinity, 1), 'MyType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set weight per unit volume and mass per unit volume');
    }
  };

  // PropFrame.SetRectangle
  Blockly.Blocks['sap_SapModel_PropFrame_SetRectangle'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetRectangle')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T3:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T2:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T2');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a rectangular (solid) frame section');
    }
  };

  // PropFrame.SetCircle
  Blockly.Blocks['sap_SapModel_PropFrame_SetCircle'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetCircle')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T3:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T3');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a solid circular frame section');
    }
  };

  // PropFrame.SetISection
  Blockly.Blocks['sap_SapModel_PropFrame_SetISection'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetISection')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T3:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T2:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TF:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'TF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TW:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'TW');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T2B:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T2B');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TFB:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'TFB');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a general I-section (W-shape / H-beam)');
    }
  };

  // PropFrame.SetTube
  Blockly.Blocks['sap_SapModel_PropFrame_SetTube'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetTube')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T3:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T2:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TF:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'TF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TW:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'TW');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a rectangular tube (HSS) frame section');
    }
  };

  // PointObj.AddCartesian
  Blockly.Blocks['sap_SapModel_PointObj_AddCartesian'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.AddCartesian()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a point object at Cartesian coordinates');
    }
  };

  // FrameObj.AddByPoint
  Blockly.Blocks['sap_SapModel_FrameObj_AddByPoint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.AddByPoint()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a frame element between two existing points');
    }
  };

  // FrameObj.AddByCoord
  Blockly.Blocks['sap_SapModel_FrameObj_AddByCoord'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.AddByCoord()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add a frame element defined by endpoint coordinates');
    }
  };

  // FrameObj.SetSection
  Blockly.Blocks['sap_SapModel_FrameObj_SetSection'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetSection()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign or change the section property of a frame element');
    }
  };

  // PropArea.SetShell_1
  Blockly.Blocks['sap_SapModel_PropArea_SetShell_1'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropArea.SetShell_1()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define una propiedad de área tipo shell. ShellType: 1=thin, 2=thick, 3=plate-thin, 4=plate-thick, 5=membrane, 6=layered.');
    }
  };

  // AreaObj.AddByCoord
  Blockly.Blocks['sap_SapModel_AreaObj_AddByCoord'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.AddByCoord()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Crea un objeto de área (shell) definiendo sus vértices por coordenadas. Acepta triángulos (3 pts) o quads (4 pts). Retor');
    }
  };

  // AreaObj.SetSpring
  Blockly.Blocks['sap_SapModel_AreaObj_SetSpring'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.SetSpring()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign area springs (Winkler foundation) to an area element');
    }
  };

  // LoadPatterns.Add
  Blockly.Blocks['sap_SapModel_LoadPatterns_Add'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadPatterns.Add()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add a new load pattern to the model');
    }
  };

  // FuncRS.SetUser
  Blockly.Blocks['sap_SapModel_Func_FuncRS_SetUser'] = {
    init: function() {
      this.setColour(210);
      this.appendDummyInput()
          .appendField('FuncRS.SetUser()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a user-defined response spectrum function from period-value pairs');
    }
  };

  // ResponseSpectrum.SetLoads
  Blockly.Blocks['sap_SapModel_LoadCases_ResponseSpectrum_SetLoads'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('ResponseSpectrum.SetLoads()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign directional response spectrum loads to a spectrum load case');
    }
  };

  // RespCombo.Add
  Blockly.Blocks['sap_SapModel_RespCombo_Add'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.Add()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a new response combination (linear, envelope, SRSS, etc.)');
    }
  };

  // RespCombo.SetCaseList
  Blockly.Blocks['sap_SapModel_RespCombo_SetCaseList'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.SetCaseList()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add a load case to a response combination with scale factor');
    }
  };

  // RespCombo.GetCaseList
  Blockly.Blocks['sap_SapModel_RespCombo_GetCaseList'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.GetCaseList()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Query the load cases and scale factors in a combination');
    }
  };

  // EditArea.Divide
  Blockly.Blocks['sap_SapModel_EditArea_Divide'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('EditArea.Divide()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Divide an area object into a mesh of smaller areas');
    }
  };

  // SelectObj.CoordinateRange
  Blockly.Blocks['sap_SapModel_SelectObj_CoordinateRange'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('SelectObj.CoordinateRange()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Select objects within a coordinate bounding box');
    }
  };

  // ConstraintDef.SetBody
  Blockly.Blocks['sap_SapModel_ConstraintDef_SetBody'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('ConstraintDef.SetBody()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a body constraint (rigid link) for DOF coupling');
    }
  };

  // FrameObj.SetTCLimits
  Blockly.Blocks['sap_SapModel_FrameObj_SetTCLimits'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetTCLimits()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set tension/compression force limits for a frame element');
    }
  };

  // PointObj.SetRestraint
  Blockly.Blocks['sap_SapModel_PointObj_SetRestraint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.SetRestraint()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign translational and rotational restraints to a joint');
    }
  };

  // FrameObj.SetLoadDistributed
  Blockly.Blocks['sap_SapModel_FrameObj_SetLoadDistributed'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetLoadDistributed()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign distributed loads (force/moment per unit length) to frame objects');
    }
  };

  // PointObj.SetLoadForce
  Blockly.Blocks['sap_SapModel_PointObj_SetLoadForce'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.SetLoadForce()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign point load forces and moments to point objects');
    }
  };

  // DatabaseTables.GetAllTables
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetAllTables'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetAllTables()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns all tables with import type and empty status');
    }
  };

  // DatabaseTables.GetAvailableTables
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetAvailableTables'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetAvailableTables()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns available (non-empty) tables with their import type — lighter query than GetAllTables');
    }
  };

  // DatabaseTables.GetAllFieldsInTable
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetAllFieldsInTable'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetAllFieldsInTable()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns all fields (columns) metadata for a specific table');
    }
  };

  // DatabaseTables.GetObsoleteTableKeyList
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetObsoleteTableKeyList'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetObsoleteTableKeyList()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns list of obsolete table keys and associated version notes');
    }
  };

  // DatabaseTables.GetTableForEditingArray
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetTableForEditingArray'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetTableForEditingArray()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Read a table as flat array for interactive editing. Returns TableVersion, FieldKeysIncluded[], NumberRecords, TableData[');
    }
  };

  // DatabaseTables.CancelTableEditing
  Blockly.Blocks['sap_SapModel_DatabaseTables_CancelTableEditing'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.CancelTableEditing()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Cancel all pending table edits without applying them. Acts as a rollback of SetTableForEditing* calls.');
    }
  };

  // DatabaseTables.SetTableForEditingArray
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetTableForEditingArray'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetTableForEditingArray()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Write edited table data (flat array) back for import via ApplyEditedTables. COM echoes back TableVersion, FieldKeysInclu');
    }
  };

  // DatabaseTables.ApplyEditedTables
  Blockly.Blocks['sap_SapModel_DatabaseTables_ApplyEditedTables'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.ApplyEditedTables()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Apply all pending table edits to the model. Returns NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog.');
    }
  };

  // DatabaseTables.GetTableForDisplayArray
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetTableForDisplayArray'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetTableForDisplayArray()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Read table data for display (read-only) as flat array. Allows specifying subset of fields via FieldKeyList.');
    }
  };

  // DatabaseTables.GetTableForDisplayCSVFile
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetTableForDisplayCSVFile'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetTableForDisplayCSVFile()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Export table display data to a CSV file');
    }
  };

  // DatabaseTables.GetTableForDisplayCSVString
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetTableForDisplayCSVString'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetTableForDisplayCSVString()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Export table display data as a CSV string');
    }
  };

  // DatabaseTables.GetTableForDisplayXMLString
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetTableForDisplayXMLString'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetTableForDisplayXMLString()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Export table display data as an XML string');
    }
  };

  // DatabaseTables.GetTableForEditingCSVFile
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetTableForEditingCSVFile'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetTableForEditingCSVFile()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Export editable table data to a CSV file');
    }
  };

  // DatabaseTables.GetTableForEditingCSVString
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetTableForEditingCSVString'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetTableForEditingCSVString()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Export editable table data as a CSV string');
    }
  };

  // DatabaseTables.SetTableForEditingCSVFile
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetTableForEditingCSVFile'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetTableForEditingCSVFile()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Import table data from a CSV file for editing');
    }
  };

  // DatabaseTables.SetTableForEditingCSVString
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetTableForEditingCSVString'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetTableForEditingCSVString()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Import table data from a CSV string for editing');
    }
  };

  // DatabaseTables.GetLoadCasesSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetLoadCasesSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetLoadCasesSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the load cases currently selected for display in database tables');
    }
  };

  // DatabaseTables.SetLoadCasesSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetLoadCasesSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetLoadCasesSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the load cases selected for display in database tables');
    }
  };

  // DatabaseTables.GetLoadCombinationsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetLoadCombinationsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetLoadCombinationsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the load combinations currently selected for display in database tables');
    }
  };

  // DatabaseTables.SetLoadCombinationsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetLoadCombinationsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetLoadCombinationsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the load combinations selected for display in database tables');
    }
  };

  // DatabaseTables.GetLoadPatternsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetLoadPatternsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetLoadPatternsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the load patterns currently selected for display in database tables');
    }
  };

  // DatabaseTables.SetLoadPatternsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetLoadPatternsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetLoadPatternsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the load patterns selected for display in database tables');
    }
  };

  // DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetElementVirtualWorkNamedSetsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the element virtual work named sets currently selected for display');
    }
  };

  // DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetElementVirtualWorkNamedSetsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the element virtual work named sets selected for display');
    }
  };

  // DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetGeneralizedDisplacementsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the generalized displacements currently selected for display');
    }
  };

  // DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetGeneralizedDisplacementsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the generalized displacements selected for display');
    }
  };

  // DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetJointResponseSpectraNamedSetsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the joint response spectra named sets currently selected for display');
    }
  };

  // DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetJointResponseSpectraNamedSetsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the joint response spectra named sets selected for display');
    }
  };

  // DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetPlotFunctionTracesNamedSetsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the plot function traces named sets currently selected for display');
    }
  };

  // DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetPlotFunctionTracesNamedSetsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the plot function traces named sets selected for display');
    }
  };

  // DatabaseTables.GetPushoverNamedSetsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetPushoverNamedSetsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetPushoverNamedSetsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the pushover named sets currently selected for display');
    }
  };

  // DatabaseTables.SetPushoverNamedSetsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetPushoverNamedSetsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetPushoverNamedSetsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the pushover named sets selected for display');
    }
  };

  // DatabaseTables.GetSectionCutsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetSectionCutsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetSectionCutsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns the section cuts currently selected for display');
    }
  };

  // DatabaseTables.SetSectionCutsSelectedForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetSectionCutsSelectedForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetSectionCutsSelectedForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets the section cuts selected for display');
    }
  };

  // DatabaseTables.GetTableOutputOptionsForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetTableOutputOptionsForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetTableOutputOptionsForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Returns table output display options (18 ByRef params: BaseReaction coords, mode ranges, history options)');
    }
  };

  // DatabaseTables.SetTableOutputOptionsForDisplay
  Blockly.Blocks['sap_SapModel_DatabaseTables_SetTableOutputOptionsForDisplay'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.SetTableOutputOptionsForDisplay()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Sets table output display options (18 params: BaseReaction coords, mode ranges, history options)');
    }
  };

  // DatabaseTables.ShowTablesInExcel
  Blockly.Blocks['sap_SapModel_DatabaseTables_ShowTablesInExcel'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.ShowTablesInExcel()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Export specified tables directly to Excel. Excel must be installed. Returns 0 on success.');
    }
  };

  // FrameObj.GetLoadDistributed
  Blockly.Blocks['sap_SapModel_FrameObj_GetLoadDistributed'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetLoadDistributed()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve distributed load assignments from frame objects');
    }
  };

  // FrameObj.SetLoadPoint
  Blockly.Blocks['sap_SapModel_FrameObj_SetLoadPoint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetLoadPoint()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign point loads (force/moment) to frame objects at specified distance');
    }
  };

  // AreaObj.SetLoadUniform
  Blockly.Blocks['sap_SapModel_AreaObj_SetLoadUniform'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.SetLoadUniform()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign uniform distributed loads [F/L²] to area objects');
    }
  };

  // Results.BaseReact
  Blockly.Blocks['sap_SapModel_Results_BaseReact'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.BaseReact()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract total base reactions (forces and moments at reporting point)');
    }
  };

  // AreaObj.SetLoadGravity
  Blockly.Blocks['sap_SapModel_AreaObj_SetLoadGravity'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.SetLoadGravity()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign gravity load multipliers to area objects');
    }
  };

  // FrameObj.SetReleases
  Blockly.Blocks['sap_SapModel_FrameObj_SetReleases'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetReleases()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign end releases (hinges/partial fixity) to frame objects');
    }
  };

  // FrameObj.GetReleases
  Blockly.Blocks['sap_SapModel_FrameObj_GetReleases'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetReleases()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve end release and partial fixity assignments from frame objects');
    }
  };

  // FrameObj.SetInsertionPoint_1
  Blockly.Blocks['sap_SapModel_FrameObj_SetInsertionPoint_1'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetInsertionPoint_1()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign cardinal point and joint offsets to frame objects');
    }
  };

  // FrameObj.SetLocalAxes
  Blockly.Blocks['sap_SapModel_FrameObj_SetLocalAxes'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetLocalAxes()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign local axis rotation angle to frame objects');
    }
  };

  // GroupDef.SetGroup
  Blockly.Blocks['sap_SapModel_GroupDef_SetGroup'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('GroupDef.SetGroup()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create or modify a group definition with properties');
    }
  };

  // GroupDef.GetNameList
  Blockly.Blocks['sap_SapModel_GroupDef_GetNameList'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('GroupDef.GetNameList()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve names of all defined groups');
    }
  };

  // FrameObj.SetGroupAssign
  Blockly.Blocks['sap_SapModel_FrameObj_SetGroupAssign'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetGroupAssign()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add or remove frame objects from a group');
    }
  };

  // AreaObj.SetGroupAssign
  Blockly.Blocks['sap_SapModel_AreaObj_SetGroupAssign'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.SetGroupAssign()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add or remove area objects from a group');
    }
  };

  // ConstraintDef.SetDiaphragm
  Blockly.Blocks['sap_SapModel_ConstraintDef_SetDiaphragm'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('ConstraintDef.SetDiaphragm()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a diaphragm constraint (rigid floor)');
    }
  };

  // ConstraintDef.GetDiaphragm
  Blockly.Blocks['sap_SapModel_ConstraintDef_GetDiaphragm'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('ConstraintDef.GetDiaphragm()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve diaphragm constraint definition (axis and coordinate system)');
    }
  };

  // Results.AreaStressShell
  Blockly.Blocks['sap_SapModel_Results_AreaStressShell'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.AreaStressShell()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract shell element stresses (S11, S22, S12 at top/bottom, principal, Von Mises)');
    }
  };

  // Results.ModalPeriod
  Blockly.Blocks['sap_SapModel_Results_ModalPeriod'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.ModalPeriod()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract modal periods, frequencies, circular frequencies, and eigenvalues');
    }
  };

  // Results.ModalParticipatingMassRatios
  Blockly.Blocks['sap_SapModel_Results_ModalParticipatingMassRatios'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.ModalParticipatingMassRatios()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract modal participating mass ratios (individual and cumulative per DOF)');
    }
  };

  // Results.ModeShape
  Blockly.Blocks['sap_SapModel_Results_ModeShape'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.ModeShape()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract modal displacements (mode shapes) at point elements');
    }
  };

  // Analyze.SetActiveDOF
  Blockly.Blocks['sap_SapModel_Analyze_SetActiveDOF'] = {
    init: function() {
      this.setColour(230);
      this.appendDummyInput()
          .appendField('Analyze.SetActiveDOF()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set active/inactive global degrees of freedom for analysis model');
    }
  };

  // Analyze.GetActiveDOF
  Blockly.Blocks['sap_SapModel_Analyze_GetActiveDOF'] = {
    init: function() {
      this.setColour(230);
      this.appendDummyInput()
          .appendField('Analyze.GetActiveDOF()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve active global degrees of freedom for analysis model');
    }
  };

  // Analyze.GetCaseStatus
  Blockly.Blocks['sap_SapModel_Analyze_GetCaseStatus'] = {
    init: function() {
      this.setColour(230);
      this.appendDummyInput()
          .appendField('Analyze.GetCaseStatus()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve run status for all load cases (1=Not run, 4=Finished)');
    }
  };

  // File.OpenFile
  Blockly.Blocks['sap_SapModel_File_OpenFile'] = {
    init: function() {
      this.setColour(0);
      this.appendDummyInput()
          .appendField('File.OpenFile()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Open an existing SAP2000 model file (.sdb)');
    }
  };

  // PropLink.SetLinear
  Blockly.Blocks['sap_SapModel_PropLink_SetLinear'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropLink.SetLinear()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a linear-type link property (stiffness, damping, DOFs)');
    }
  };

  // LinkObj.AddByPoint
  Blockly.Blocks['sap_SapModel_LinkObj_AddByPoint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('LinkObj.AddByPoint()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a two-joint link element between two existing point objects.');
    }
  };

  // LinkObj.AddByCoord
  Blockly.Blocks['sap_SapModel_LinkObj_AddByCoord'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('LinkObj.AddByCoord()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a link element by specifying I-End and J-End coordinates');
    }
  };

  // AreaObj.SetProperty
  Blockly.Blocks['sap_SapModel_AreaObj_SetProperty'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.SetProperty()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign or change area section property on an area object');
    }
  };

  // PropArea.GetShell_1
  Blockly.Blocks['sap_SapModel_PropArea_GetShell_1'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropArea.GetShell_1()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve shell-type area section properties (type, material, thicknesses)');
    }
  };

  // PropMaterial.SetOSteel_1
  Blockly.Blocks['sap_SapModel_PropMaterial_SetOSteel_1'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.SetOSteel_1')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Fy:'))
          .appendField(new Blockly.FieldTextInput(''), 'Fy');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Fu:'))
          .appendField(new Blockly.FieldTextInput(''), 'Fu');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EFy:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'EFy');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EFu:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'EFu');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SSType:'))
          .appendField(new Blockly.FieldTextInput(''), 'SSType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SSHysType:'))
          .appendField(new Blockly.FieldTextInput(''), 'SSHysType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StrainAtHardening:'))
          .appendField(new Blockly.FieldTextInput(''), 'StrainAtHardening');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StrainAtMaxStress:'))
          .appendField(new Blockly.FieldTextInput(''), 'StrainAtMaxStress');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StrainAtRupture:'))
          .appendField(new Blockly.FieldTextInput(''), 'StrainAtRupture');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FinalSlope:'))
          .appendField(new Blockly.FieldTextInput(''), 'FinalSlope');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set steel design properties (yield/ultimate strengths, stress-strain model)');
    }
  };

  // PropMaterial.SetOConcrete_1
  Blockly.Blocks['sap_SapModel_PropMaterial_SetOConcrete_1'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.SetOConcrete_1')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('fc:'))
          .appendField(new Blockly.FieldTextInput(''), 'fc');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IsLightweight:'))
          .appendField(new Blockly.FieldTextInput(''), 'IsLightweight');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FcsFactor:'))
          .appendField(new Blockly.FieldTextInput(''), 'FcsFactor');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SSType:'))
          .appendField(new Blockly.FieldTextInput(''), 'SSType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SSHysType:'))
          .appendField(new Blockly.FieldTextInput(''), 'SSHysType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StrainAtfc:'))
          .appendField(new Blockly.FieldTextInput(''), 'StrainAtfc');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StrainUltimate:'))
          .appendField(new Blockly.FieldTextInput(''), 'StrainUltimate');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FinalSlope:'))
          .appendField(new Blockly.FieldTextInput(''), 'FinalSlope');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FrictionAngle:'))
          .appendField(new Blockly.FieldTextInput(''), 'FrictionAngle');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DilatationalAngle:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'DilatationalAngle');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set concrete design properties (fc, lightweight flag, stress-strain model)');
    }
  };

  // PropMaterial.GetMaterial
  Blockly.Blocks['sap_SapModel_PropMaterial_GetMaterial'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.GetMaterial')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatType:'))
          .appendField(new Blockly.FieldDropdown([["Steel (1)", "1"], ["Concrete (2)", "2"], ["NoDesign (3)", "3"], ["Aluminum (4)", "4"], ["ColdFormed (5)", "5"], ["Rebar (6)", "6"], ["Tendon (7)", "7"]]), 'MatType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get material type and metadata (MatType, Color, Notes, GUID) for an existing material');
    }
  };

  // PropMaterial.GetMPIsotropic
  Blockly.Blocks['sap_SapModel_PropMaterial_GetMPIsotropic'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.GetMPIsotropic')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('E:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'E');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('U:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'U');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('A:'))
          .appendField(new Blockly.FieldTextInput(''), 'A');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve isotropic mechanical properties (E, Poisson ratio, thermal expansion coefficient)');
    }
  };

  // PropFrame.SetAngle
  Blockly.Blocks['sap_SapModel_PropFrame_SetAngle'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetAngle()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define an angle (L-shape) frame section');
    }
  };

  // PropFrame.SetChannel
  Blockly.Blocks['sap_SapModel_PropFrame_SetChannel'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetChannel()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a channel (C-shape) frame section');
    }
  };

  // PropFrame.SetPipe
  Blockly.Blocks['sap_SapModel_PropFrame_SetPipe'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetPipe()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a circular pipe (hollow) frame section');
    }
  };

  // PropFrame.GetRectangle
  Blockly.Blocks['sap_SapModel_PropFrame_GetRectangle'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.GetRectangle()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve rectangular section properties');
    }
  };

  // PropFrame.GetCircle
  Blockly.Blocks['sap_SapModel_PropFrame_GetCircle'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.GetCircle()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve circular (solid) section properties');
    }
  };

  // PropFrame.GetISection
  Blockly.Blocks['sap_SapModel_PropFrame_GetISection'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.GetISection()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve I-section properties');
    }
  };

  // DesignSteel.SetComboStrength
  Blockly.Blocks['sap_SapModel_DesignSteel_SetComboStrength'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignSteel.SetComboStrength()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Select/deselect a combo for steel strength design');
    }
  };

  // DesignSteel.GetComboStrength
  Blockly.Blocks['sap_SapModel_DesignSteel_GetComboStrength'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignSteel.GetComboStrength()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve combos selected for steel strength design');
    }
  };

  // DesignSteel.SetComboDeflection
  Blockly.Blocks['sap_SapModel_DesignSteel_SetComboDeflection'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignSteel.SetComboDeflection()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Select/deselect a combo for steel deflection design (serviceability)');
    }
  };

  // DesignSteel.GetCode
  Blockly.Blocks['sap_SapModel_DesignSteel_GetCode'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignSteel.GetCode()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve current steel design code');
    }
  };

  // DesignSteel.SetCode
  Blockly.Blocks['sap_SapModel_DesignSteel_SetCode'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignSteel.SetCode()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set the steel design code');
    }
  };

  // DesignSteel.DeleteResults
  Blockly.Blocks['sap_SapModel_DesignSteel_DeleteResults'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignSteel.DeleteResults()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Delete all steel frame design results');
    }
  };

  // DesignConcrete.SetComboStrength
  Blockly.Blocks['sap_SapModel_DesignConcrete_SetComboStrength'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignConcrete.SetComboStrength()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Select/deselect a combo for concrete strength design');
    }
  };

  // DesignConcrete.GetCode
  Blockly.Blocks['sap_SapModel_DesignConcrete_GetCode'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignConcrete.GetCode()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve current concrete design code');
    }
  };

  // DesignConcrete.SetCode
  Blockly.Blocks['sap_SapModel_DesignConcrete_SetCode'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignConcrete.SetCode()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set the concrete design code');
    }
  };

  // RespCombo.Delete
  Blockly.Blocks['sap_SapModel_RespCombo_Delete'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.Delete()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Delete an existing load combination');
    }
  };

  // RespCombo.ChangeName
  Blockly.Blocks['sap_SapModel_RespCombo_ChangeName'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.ChangeName()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Rename an existing load combination');
    }
  };

  // RespCombo.Count
  Blockly.Blocks['sap_SapModel_RespCombo_Count'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get total number of load combinations');
    }
  };

  // RespCombo.SetTypeOAPI
  Blockly.Blocks['sap_SapModel_RespCombo_SetTypeOAPI'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.SetTypeOAPI()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set the type of a load combination');
    }
  };

  // RespCombo.GetTypeOAPI
  Blockly.Blocks['sap_SapModel_RespCombo_GetTypeOAPI'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.GetTypeOAPI()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the type of a load combination');
    }
  };

  // RespCombo.DeleteCase
  Blockly.Blocks['sap_SapModel_RespCombo_DeleteCase'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.DeleteCase()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Remove a load case or combo from a combination');
    }
  };

  // RespCombo.AddDesignDefaultCombos
  Blockly.Blocks['sap_SapModel_RespCombo_AddDesignDefaultCombos'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.AddDesignDefaultCombos()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add default design combinations by material type');
    }
  };

  // ResponseSpectrum.SetDampConstant
  Blockly.Blocks['sap_SapModel_LoadCases_ResponseSpectrum_SetDampConstant'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('ResponseSpectrum.SetDampConstant()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set constant damping for a response spectrum case');
    }
  };

  // LoadCases.Count
  Blockly.Blocks['sap_SapModel_LoadCases_Count'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadCases.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get total number of load cases (optionally by type)');
    }
  };

  // LoadCases.Delete
  Blockly.Blocks['sap_SapModel_LoadCases_Delete'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadCases.Delete()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Delete a load case');
    }
  };

  // LoadCases.ChangeName
  Blockly.Blocks['sap_SapModel_LoadCases_ChangeName'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadCases.ChangeName()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Rename a load case');
    }
  };

  // LoadPatterns.Count
  Blockly.Blocks['sap_SapModel_LoadPatterns_Count'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadPatterns.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get total number of load patterns');
    }
  };

  // LoadPatterns.Delete
  Blockly.Blocks['sap_SapModel_LoadPatterns_Delete'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadPatterns.Delete()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Delete a load pattern');
    }
  };

  // LoadPatterns.ChangeName
  Blockly.Blocks['sap_SapModel_LoadPatterns_ChangeName'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadPatterns.ChangeName()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Rename a load pattern');
    }
  };

  // SourceMass.SetMassSource
  Blockly.Blocks['sap_SapModel_SourceMass_SetMassSource'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('SourceMass.SetMassSource()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add or reinitialize a mass source definition specifying which elements and load patterns contribute to model mass. Essen');
    }
  };

  // SourceMass.Count
  Blockly.Blocks['sap_SapModel_SourceMass_Count'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('SourceMass.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get total number of mass sources defined in the model. Returns integer directly (not ByRef).');
    }
  };

  // SourceMass.GetMassSource
  Blockly.Blocks['sap_SapModel_SourceMass_GetMassSource'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('SourceMass.GetMassSource()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve mass source configuration including element/load contributions and scale factors. Returns ByRef layout with all');
    }
  };

  // SourceMass.GetDefault
  Blockly.Blocks['sap_SapModel_SourceMass_GetDefault'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('SourceMass.GetDefault()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve the name of the default mass source currently set in the model.');
    }
  };

  // FrameObj.SetModifiers
  Blockly.Blocks['sap_SapModel_FrameObj_SetModifiers'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetModifiers()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set stiffness modification factors for a frame object (cracked section analysis)');
    }
  };

  // FrameObj.GetModifiers
  Blockly.Blocks['sap_SapModel_FrameObj_GetModifiers'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetModifiers()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve stiffness modification factors for a frame object');
    }
  };

  // PropArea.SetModifiers
  Blockly.Blocks['sap_SapModel_PropArea_SetModifiers'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropArea.SetModifiers()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set stiffness modification factors for an area property (shell/slab/wall)');
    }
  };

  // PropArea.GetModifiers
  Blockly.Blocks['sap_SapModel_PropArea_GetModifiers'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropArea.GetModifiers()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve stiffness modification factors for an area property');
    }
  };

  // PropFrame.ChangeName
  Blockly.Blocks['sap_SapModel_PropFrame_ChangeName'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.ChangeName()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Rename a frame section property');
    }
  };

  // PropFrame.Count
  Blockly.Blocks['sap_SapModel_PropFrame_Count'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get total number of frame section properties (optionally filtered by type)');
    }
  };

  // PropFrame.Delete
  Blockly.Blocks['sap_SapModel_PropFrame_Delete'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.Delete()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Delete a frame section property (must not be in use by any element)');
    }
  };

  // PropMaterial.ChangeName
  Blockly.Blocks['sap_SapModel_PropMaterial_ChangeName'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.ChangeName()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Rename a material property');
    }
  };

  // PropMaterial.Count
  Blockly.Blocks['sap_SapModel_PropMaterial_Count'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get total number of material properties (optionally filtered by material type)');
    }
  };

  // PropMaterial.Delete
  Blockly.Blocks['sap_SapModel_PropMaterial_Delete'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.Delete()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Delete a material property (must not be in use by any section)');
    }
  };

  // PropLink.SetGap
  Blockly.Blocks['sap_SapModel_PropLink_SetGap'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropLink.SetGap()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a Gap-type nonlinear link property (compression-only). DOF arrays size 6.');
    }
  };

  console.log('✅ ' + Object.keys(Blockly.Blocks).filter(k => k.startsWith("sap_")).length + ' SAP2000 blocks registered');
}
