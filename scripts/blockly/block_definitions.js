// ===========================================================
// SAP2000 Block Definitions - Auto-generated
// Generated: 2026-04-04 22:39
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
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'A');
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
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
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
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
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
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
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
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
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

  // SapModel.InitializeNewModel
  Blockly.Blocks['sap_SapModel_InitializeNewModel'] = {
    init: function() {
      this.setColour(0);
      this.appendDummyInput()
          .appendField('SapModel.InitializeNewModel')
          .appendField(new Blockly.FieldLabel('Units:'))
          .appendField(new Blockly.FieldDropdown([["lb_in_F (1)", "1"], ["lb_ft_F (2)", "2"], ["kip_in_F (3)", "3"], ["kip_ft_F (4)", "4"], ["kN_mm_C (5)", "5"], ["kN_m_C (6)", "6"], ["kgf_mm_C (7)", "7"], ["kgf_m_C (8)", "8"], ["N_mm_C (9)", "9"], ["N_m_C (10)", "10"], ["Ton_mm_C (11)", "11"], ["Ton_m_C (12)", "12"], ["kN_cm_C (13)", "13"], ["kgf_cm_C (14)", "14"], ["N_cm_C (15)", "15"], ["Ton_cm_C (16)", "16"]]), 'Units');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Initialize a new model with specified units');
    }
  };

  // SapModel.SetPresentUnits
  Blockly.Blocks['sap_SapModel_SetPresentUnits'] = {
    init: function() {
      this.setColour(210);
      this.appendDummyInput()
          .appendField('SapModel.SetPresentUnits')
          .appendField(new Blockly.FieldLabel('Units:'))
          .appendField(new Blockly.FieldDropdown([["lb_in_F (1)", "1"], ["lb_ft_F (2)", "2"], ["kip_in_F (3)", "3"], ["kip_ft_F (4)", "4"], ["kN_mm_C (5)", "5"], ["kN_m_C (6)", "6"], ["kgf_mm_C (7)", "7"], ["kgf_m_C (8)", "8"], ["N_mm_C (9)", "9"], ["N_m_C (10)", "10"], ["Ton_mm_C (11)", "11"], ["Ton_m_C (12)", "12"], ["kN_cm_C (13)", "13"], ["kgf_cm_C (14)", "14"], ["N_cm_C (15)", "15"], ["Ton_cm_C (16)", "16"]]), 'Units');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set the current display units for the model');
    }
  };

  // PointObj.AddCartesian
  Blockly.Blocks['sap_SapModel_PointObj_AddCartesian'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.AddCartesian')
          .appendField(new Blockly.FieldLabel('X:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'X');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Y:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Y');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Z:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Z');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('UserName:'))
          .appendField(new Blockly.FieldTextInput(''), 'UserName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MergeOff:'))
          .appendField(new Blockly.FieldTextInput(''), 'MergeOff');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MergeNumber:'))
          .appendField(new Blockly.FieldTextInput(''), 'MergeNumber');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a point object at Cartesian coordinates');
    }
  };

  // PointObj.Count
  Blockly.Blocks['sap_SapModel_PointObj_Count'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the number of point objects in the model');
    }
  };

  // PointObj.GetCoordCartesian
  Blockly.Blocks['sap_SapModel_PointObj_GetCoordCartesian'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.GetCoordCartesian')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('X:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'X');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Y:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Y');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Z:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Z');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get Cartesian coordinates of a point object');
    }
  };

  // FrameObj.AddByPoint
  Blockly.Blocks['sap_SapModel_FrameObj_AddByPoint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.AddByPoint')
          .appendField(new Blockly.FieldLabel('Point1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Point1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Point2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Point2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('UserName:'))
          .appendField(new Blockly.FieldTextInput(''), 'UserName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a frame element between two existing points');
    }
  };

  // FrameObj.Count
  Blockly.Blocks['sap_SapModel_FrameObj_Count'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the number of frame objects in the model');
    }
  };

  // FrameObj.GetPoints
  Blockly.Blocks['sap_SapModel_FrameObj_GetPoints'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetPoints')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Point1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Point1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Point2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Point2');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the two endpoint point names of a frame object');
    }
  };

  // FrameObj.AddByCoord
  Blockly.Blocks['sap_SapModel_FrameObj_AddByCoord'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.AddByCoord')
          .appendField(new Blockly.FieldLabel('x1:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'x1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('y1:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'y1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('z1:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'z1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('x2:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'x2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('y2:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'y2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('z2:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'z2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('UserName:'))
          .appendField(new Blockly.FieldTextInput(''), 'UserName');
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
          .appendField('FrameObj.SetSection')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SAuto:'))
          .appendField(new Blockly.FieldTextInput(''), 'SAuto');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign or change the section property of a frame element');
    }
  };

  // FrameObj.GetSection
  Blockly.Blocks['sap_SapModel_FrameObj_GetSection'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetSection')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SAuto:'))
          .appendField(new Blockly.FieldTextInput(''), 'SAuto');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the section property assigned to a frame object');
    }
  };

  // PropArea.SetShell_1
  Blockly.Blocks['sap_SapModel_PropArea_SetShell_1'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropArea.SetShell_1')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ShellType:'))
          .appendField(new Blockly.FieldDropdown([["ShellThin (1)", "1"], ["ShellThick (2)", "2"], ["Membrane (3)", "3"], ["Plate (4)", "4"]]), 'ShellType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludeDrillingDOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludeDrillingDOF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatAng:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatAng');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Thickness:'))
          .appendField(new Blockly.FieldTextInput(''), 'Thickness');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Bending:'))
          .appendField(new Blockly.FieldTextInput(''), 'Bending');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define una propiedad de área tipo shell. ShellType: 1=thin, 2=thick, 3=plate-thin, 4=plate-thick, 5=membrane, 6=layered.');
    }
  };

  // PropArea.GetNameList
  Blockly.Blocks['sap_SapModel_PropArea_GetNameList'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropArea.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names of all area section properties defined in the model');
    }
  };

  // AreaObj.AddByCoord
  Blockly.Blocks['sap_SapModel_AreaObj_AddByCoord'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.AddByCoord')
          .appendField(new Blockly.FieldLabel('NumberPoints:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberPoints');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('X:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'X');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Y:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Y');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Z:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Z');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('UserName:'))
          .appendField(new Blockly.FieldTextInput(''), 'UserName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Crea un objeto de área (shell) definiendo sus vértices por coordenadas. Acepta triángulos (3 pts) o quads (4 pts). Retor');
    }
  };

  // AreaObj.Count
  Blockly.Blocks['sap_SapModel_AreaObj_Count'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the number of area objects in the model');
    }
  };

  // AreaObj.SetSpring
  Blockly.Blocks['sap_SapModel_AreaObj_SetSpring'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.SetSpring')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyType:'))
          .appendField(new Blockly.FieldNumber(1, -Infinity, Infinity, 1), 'MyType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S:'))
          .appendField(new Blockly.FieldTextInput(''), 'S');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SimpleSpringType:'))
          .appendField(new Blockly.FieldTextInput(''), 'SimpleSpringType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LinkProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'LinkProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Face:'))
          .appendField(new Blockly.FieldTextInput(''), 'Face');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpringLocalOneType:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpringLocalOneType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dir:'))
          .appendField(new Blockly.FieldDropdown([["Local1 (1)", "1"], ["Local2 (2)", "2"], ["Local3 (3)", "3"], ["X (4)", "4"], ["Y (5)", "5"], ["Z (6)", "6"], ["GravityProjected (10)", "10"], ["GravityFull (11)", "11"]]), 'Dir');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Outward:'))
          .appendField(new Blockly.FieldTextInput(''), 'Outward');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Vec:'))
          .appendField(new Blockly.FieldTextInput(''), 'Vec');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ang:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ang');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Replace:'))
          .appendField(new Blockly.FieldCheckbox('TRUE'), 'Replace');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('LoadPatterns.Add')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyType:'))
          .appendField(new Blockly.FieldNumber(1, -Infinity, Infinity, 1), 'MyType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SelfWTMultiplier:'))
          .appendField(new Blockly.FieldTextInput(''), 'SelfWTMultiplier');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('AddCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'AddCase');
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
          .appendField('FuncRS.SetUser')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Period:'))
          .appendField(new Blockly.FieldTextInput(''), 'Period');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DampRatio:'))
          .appendField(new Blockly.FieldTextInput(''), 'DampRatio');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a user-defined response spectrum function from period-value pairs');
    }
  };

  // FuncRS.GetUser
  Blockly.Blocks['sap_SapModel_Func_FuncRS_GetUser'] = {
    init: function() {
      this.setColour(210);
      this.appendDummyInput()
          .appendField('FuncRS.GetUser')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Period:'))
          .appendField(new Blockly.FieldTextInput(''), 'Period');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DampRatio:'))
          .appendField(new Blockly.FieldTextInput(''), 'DampRatio');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the user-defined response spectrum function data');
    }
  };

  // ResponseSpectrum.SetCase
  Blockly.Blocks['sap_SapModel_LoadCases_ResponseSpectrum_SetCase'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('ResponseSpectrum.SetCase')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Initialize a response spectrum load case');
    }
  };

  // ResponseSpectrum.SetLoads
  Blockly.Blocks['sap_SapModel_LoadCases_ResponseSpectrum_SetLoads'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('ResponseSpectrum.SetLoads')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberLoads:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberLoads');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadName:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Func:'))
          .appendField(new Blockly.FieldTextInput(''), 'Func');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SF:'))
          .appendField(new Blockly.FieldTextInput(''), 'SF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ang:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ang');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign directional response spectrum loads to a spectrum load case');
    }
  };

  // ResponseSpectrum.GetLoads
  Blockly.Blocks['sap_SapModel_LoadCases_ResponseSpectrum_GetLoads'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('ResponseSpectrum.GetLoads')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadName:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Func:'))
          .appendField(new Blockly.FieldTextInput(''), 'Func');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SF:'))
          .appendField(new Blockly.FieldTextInput(''), 'SF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ang:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ang');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the load components for a response spectrum load case');
    }
  };

  // LoadCases.GetNameList
  Blockly.Blocks['sap_SapModel_LoadCases_GetNameList'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadCases.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyType:'))
          .appendField(new Blockly.FieldNumber(1, -Infinity, Infinity, 1), 'MyType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names and types of all load cases defined');
    }
  };

  // RespCombo.Add
  Blockly.Blocks['sap_SapModel_RespCombo_Add'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.Add')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ComboType:'))
          .appendField(new Blockly.FieldDropdown([["LinearAdd (0)", "0"], ["Envelope (1)", "1"], ["AbsAdd (2)", "2"], ["SRSS (3)", "3"], ["RangeAdd (4)", "4"]]), 'ComboType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a new response combination (linear, envelope, SRSS, etc.)');
    }
  };

  // RespCombo.GetNameList
  Blockly.Blocks['sap_SapModel_RespCombo_GetNameList'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names of all load combinations defined in the model');
    }
  };

  // RespCombo.SetCaseList
  Blockly.Blocks['sap_SapModel_RespCombo_SetCaseList'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('RespCombo.SetCaseList')
          .appendField(new Blockly.FieldLabel('ComboName:'))
          .appendField(new Blockly.FieldTextInput(''), 'ComboName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CaseType:'))
          .appendField(new Blockly.FieldTextInput(''), 'CaseType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CaseName:'))
          .appendField(new Blockly.FieldTextInput(''), 'CaseName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ScaleFactor:'))
          .appendField(new Blockly.FieldTextInput(''), 'ScaleFactor');
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
          .appendField('RespCombo.GetCaseList')
          .appendField(new Blockly.FieldLabel('ComboName:'))
          .appendField(new Blockly.FieldTextInput(''), 'ComboName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CaseType:'))
          .appendField(new Blockly.FieldTextInput(''), 'CaseType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CaseName:'))
          .appendField(new Blockly.FieldTextInput(''), 'CaseName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ScaleFactor:'))
          .appendField(new Blockly.FieldTextInput(''), 'ScaleFactor');
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
          .appendField('EditArea.Divide')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MeshType:'))
          .appendField(new Blockly.FieldTextInput(''), 'MeshType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumAreas:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumAreas');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('AreaName:'))
          .appendField(new Blockly.FieldTextInput(''), 'AreaName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('N1:'))
          .appendField(new Blockly.FieldTextInput(''), 'N1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('N2:'))
          .appendField(new Blockly.FieldTextInput(''), 'N2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MaxSize1:'))
          .appendField(new Blockly.FieldTextInput(''), 'MaxSize1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MaxSize2:'))
          .appendField(new Blockly.FieldTextInput(''), 'MaxSize2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PointOnEdgeFromLine:'))
          .appendField(new Blockly.FieldTextInput(''), 'PointOnEdgeFromLine');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PointOnEdgeFromPoint:'))
          .appendField(new Blockly.FieldTextInput(''), 'PointOnEdgeFromPoint');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ExtendCookieCutLines:'))
          .appendField(new Blockly.FieldTextInput(''), 'ExtendCookieCutLines');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Rotation:'))
          .appendField(new Blockly.FieldTextInput(''), 'Rotation');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MaxSizeGeneral:'))
          .appendField(new Blockly.FieldTextInput(''), 'MaxSizeGeneral');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LocalAxesOnEdge:'))
          .appendField(new Blockly.FieldTextInput(''), 'LocalAxesOnEdge');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LocalAxesOnFace:'))
          .appendField(new Blockly.FieldTextInput(''), 'LocalAxesOnFace');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('RestraintsOnEdge:'))
          .appendField(new Blockly.FieldTextInput(''), 'RestraintsOnEdge');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('RestraintsOnFace:'))
          .appendField(new Blockly.FieldTextInput(''), 'RestraintsOnFace');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Group:'))
          .appendField(new Blockly.FieldTextInput(''), 'Group');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SubMesh:'))
          .appendField(new Blockly.FieldTextInput(''), 'SubMesh');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SubMeshSize:'))
          .appendField(new Blockly.FieldTextInput(''), 'SubMeshSize');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Divide an area object into a mesh of smaller areas');
    }
  };

  // SelectObj.ClearSelection
  Blockly.Blocks['sap_SapModel_SelectObj_ClearSelection'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('SelectObj.ClearSelection()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Deselect all currently selected objects');
    }
  };

  // SelectObj.CoordinateRange
  Blockly.Blocks['sap_SapModel_SelectObj_CoordinateRange'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('SelectObj.CoordinateRange')
          .appendField(new Blockly.FieldLabel('XMin:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'XMin');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('XMax:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'XMax');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('YMin:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'YMin');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('YMax:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'YMax');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ZMin:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'ZMin');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ZMax:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'ZMax');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Deselect:'))
          .appendField(new Blockly.FieldTextInput(''), 'Deselect');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludeIntersections:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludeIntersections');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludePoints:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludePoints');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludeFrames:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludeFrames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludeAreas:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludeAreas');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludeSolids:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludeSolids');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludeLinks:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludeLinks');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Select objects within a coordinate bounding box');
    }
  };

  // SelectObj.GetSelected
  Blockly.Blocks['sap_SapModel_SelectObj_GetSelected'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('SelectObj.GetSelected')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ObjectType:'))
          .appendField(new Blockly.FieldTextInput(''), 'ObjectType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ObjectName:'))
          .appendField(new Blockly.FieldTextInput(''), 'ObjectName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get all currently selected objects by type and name');
    }
  };

  // ConstraintDef.SetBody
  Blockly.Blocks['sap_SapModel_ConstraintDef_SetBody'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('ConstraintDef.SetBody')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a body constraint (rigid link) for DOF coupling');
    }
  };

  // PointObj.SetConstraint
  Blockly.Blocks['sap_SapModel_PointObj_SetConstraint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.SetConstraint')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ConstraintName:'))
          .appendField(new Blockly.FieldTextInput(''), 'ConstraintName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign a constraint to a point object');
    }
  };

  // ConstraintDef.GetBody
  Blockly.Blocks['sap_SapModel_ConstraintDef_GetBody'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('ConstraintDef.GetBody')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'DOF');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the DOF configuration of a body constraint');
    }
  };

  // FrameObj.SetTCLimits
  Blockly.Blocks['sap_SapModel_FrameObj_SetTCLimits'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetTCLimits')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LimitCompressionExists:'))
          .appendField(new Blockly.FieldTextInput(''), 'LimitCompressionExists');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LimitCompression:'))
          .appendField(new Blockly.FieldTextInput(''), 'LimitCompression');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LimitTensionExists:'))
          .appendField(new Blockly.FieldTextInput(''), 'LimitTensionExists');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LimitTension:'))
          .appendField(new Blockly.FieldTextInput(''), 'LimitTension');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set tension/compression force limits for a frame element');
    }
  };

  // FrameObj.GetTCLimits
  Blockly.Blocks['sap_SapModel_FrameObj_GetTCLimits'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetTCLimits')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LimitCompressionExists:'))
          .appendField(new Blockly.FieldTextInput(''), 'LimitCompressionExists');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LimitCompression:'))
          .appendField(new Blockly.FieldTextInput(''), 'LimitCompression');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LimitTensionExists:'))
          .appendField(new Blockly.FieldTextInput(''), 'LimitTensionExists');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LimitTension:'))
          .appendField(new Blockly.FieldTextInput(''), 'LimitTension');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the tension/compression limits for a frame object');
    }
  };

  // PointObj.SetRestraint
  Blockly.Blocks['sap_SapModel_PointObj_SetRestraint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.SetRestraint')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign translational and rotational restraints to a joint');
    }
  };

  // LoadPatterns.GetNameList
  Blockly.Blocks['sap_SapModel_LoadPatterns_GetNameList'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadPatterns.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldDropdown([["Dead (1)", "1"], ["SuperDead (2)", "2"], ["Live (3)", "3"], ["ReduceLive (4)", "4"], ["Quake (5)", "5"], ["Wind (6)", "6"], ["Snow (7)", "7"], ["Other (8)", "8"], ["Move (9)", "9"], ["Temperature (10)", "10"], ["RoofLive (11)", "11"], ["Notional (12)", "12"]]), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldDropdown([["Dead (1)", "1"], ["SuperDead (2)", "2"], ["Live (3)", "3"], ["ReduceLive (4)", "4"], ["Quake (5)", "5"], ["Wind (6)", "6"], ["Snow (7)", "7"], ["Other (8)", "8"], ["Move (9)", "9"], ["Temperature (10)", "10"], ["RoofLive (11)", "11"], ["Notional (12)", "12"]]), 'MyName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyType:'))
          .appendField(new Blockly.FieldDropdown([["Dead (1)", "1"], ["SuperDead (2)", "2"], ["Live (3)", "3"], ["ReduceLive (4)", "4"], ["Quake (5)", "5"], ["Wind (6)", "6"], ["Snow (7)", "7"], ["Other (8)", "8"], ["Move (9)", "9"], ["Temperature (10)", "10"], ["RoofLive (11)", "11"], ["Notional (12)", "12"]]), 'MyType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names and types of all load patterns defined');
    }
  };

  // PropFrame.GetNameList
  Blockly.Blocks['sap_SapModel_PropFrame_GetNameList'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names of all frame section properties defined in the model');
    }
  };

  // FrameObj.SetLoadDistributed
  Blockly.Blocks['sap_SapModel_FrameObj_SetLoadDistributed'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetLoadDistributed')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadPat:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadPat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyType:'))
          .appendField(new Blockly.FieldNumber(1, -Infinity, Infinity, 1), 'MyType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dir:'))
          .appendField(new Blockly.FieldDropdown([["Local1 (1)", "1"], ["Local2 (2)", "2"], ["Local3 (3)", "3"], ["X (4)", "4"], ["Y (5)", "5"], ["Z (6)", "6"], ["GravityProjected (10)", "10"], ["GravityFull (11)", "11"]]), 'Dir');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dist1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Dist1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dist2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Dist2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Val1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Val1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Val2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Val2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('RelDist:'))
          .appendField(new Blockly.FieldTextInput(''), 'RelDist');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Replace:'))
          .appendField(new Blockly.FieldCheckbox('TRUE'), 'Replace');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('PointObj.SetLoadForce')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadPat:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadPat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Replace:'))
          .appendField(new Blockly.FieldCheckbox('TRUE'), 'Replace');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign point load forces and moments to point objects');
    }
  };

  // View.RefreshView
  Blockly.Blocks['sap_SapModel_View_RefreshView'] = {
    init: function() {
      this.setColour(210);
      this.appendDummyInput()
          .appendField('View.RefreshView')
          .appendField(new Blockly.FieldLabel('Window:'))
          .appendField(new Blockly.FieldTextInput(''), 'Window');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Zoom:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'Zoom');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Redraw and refresh the SAP2000 model view');
    }
  };

  // File.Save
  Blockly.Blocks['sap_SapModel_File_Save'] = {
    init: function() {
      this.setColour(0);
      this.appendDummyInput()
          .appendField('File.Save')
          .appendField(new Blockly.FieldLabel('FileName:'))
          .appendField(new Blockly.FieldTextInput(''), 'FileName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Save the current model to file');
    }
  };

  // Analyze.RunAnalysis
  Blockly.Blocks['sap_SapModel_Analyze_RunAnalysis'] = {
    init: function() {
      this.setColour(230);
      this.appendDummyInput()
          .appendField('Analyze.RunAnalysis()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Run the structural analysis for all active load cases');
    }
  };

  // Setup.DeselectAllCasesAndCombosForOutput
  Blockly.Blocks['sap_SapModel_Results_Setup_DeselectAllCasesAndCombosForOutput'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Setup.DeselectAllCasesAndCombosForOutput()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Clear all load cases and combinations from the output selection');
    }
  };

  // Setup.SetCaseSelectedForOutput
  Blockly.Blocks['sap_SapModel_Results_Setup_SetCaseSelectedForOutput'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Setup.SetCaseSelectedForOutput')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Selected:'))
          .appendField(new Blockly.FieldTextInput(''), 'Selected');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Select or deselect a load case for results output');
    }
  };

  // Results.JointDispl
  Blockly.Blocks['sap_SapModel_Results_JointDispl'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.JointDispl')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemTypeElm:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemTypeElm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberResults:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberResults');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Obj:'))
          .appendField(new Blockly.FieldTextInput(''), 'Obj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Elm:'))
          .appendField(new Blockly.FieldTextInput(''), 'Elm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadCase');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepType:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepNum:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepNum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('U1:'))
          .appendField(new Blockly.FieldTextInput(''), 'U1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('U2:'))
          .appendField(new Blockly.FieldTextInput(''), 'U2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('U3:'))
          .appendField(new Blockly.FieldTextInput(''), 'U3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('R1:'))
          .appendField(new Blockly.FieldTextInput(''), 'R1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('R2:'))
          .appendField(new Blockly.FieldTextInput(''), 'R2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('R3:'))
          .appendField(new Blockly.FieldTextInput(''), 'R3');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract joint displacement results (translations and rotations)');
    }
  };

  // Results.FrameForce
  Blockly.Blocks['sap_SapModel_Results_FrameForce'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.FrameForce')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemTypeElm:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemTypeElm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberResults:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberResults');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Obj:'))
          .appendField(new Blockly.FieldTextInput(''), 'Obj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ObjSta:'))
          .appendField(new Blockly.FieldTextInput(''), 'ObjSta');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Elm:'))
          .appendField(new Blockly.FieldTextInput(''), 'Elm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ElmSta:'))
          .appendField(new Blockly.FieldTextInput(''), 'ElmSta');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadCase');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepType:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepNum:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepNum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('P:'))
          .appendField(new Blockly.FieldTextInput(''), 'P');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('V2:'))
          .appendField(new Blockly.FieldTextInput(''), 'V2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('V3:'))
          .appendField(new Blockly.FieldTextInput(''), 'V3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('M2:'))
          .appendField(new Blockly.FieldTextInput(''), 'M2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('M3:'))
          .appendField(new Blockly.FieldTextInput(''), 'M3');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract frame internal forces (P, V2, V3, T, M2, M3) at stations');
    }
  };

  // Results.JointReact
  Blockly.Blocks['sap_SapModel_Results_JointReact'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.JointReact')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemTypeElm:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemTypeElm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberResults:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberResults');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Obj:'))
          .appendField(new Blockly.FieldTextInput(''), 'Obj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Elm:'))
          .appendField(new Blockly.FieldTextInput(''), 'Elm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadCase');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepType:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepNum:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepNum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('F1:'))
          .appendField(new Blockly.FieldTextInput(''), 'F1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('F2:'))
          .appendField(new Blockly.FieldTextInput(''), 'F2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('F3:'))
          .appendField(new Blockly.FieldTextInput(''), 'F3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('M1:'))
          .appendField(new Blockly.FieldTextInput(''), 'M1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('M2:'))
          .appendField(new Blockly.FieldTextInput(''), 'M2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('M3:'))
          .appendField(new Blockly.FieldTextInput(''), 'M3');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract joint reaction forces at restrained joints');
    }
  };

  // Setup.SetComboSelectedForOutput
  Blockly.Blocks['sap_SapModel_Results_Setup_SetComboSelectedForOutput'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Setup.SetComboSelectedForOutput')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Selected:'))
          .appendField(new Blockly.FieldTextInput(''), 'Selected');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Select or deselect a load combination for results output');
    }
  };

  // LoadPatterns.SetSelfWTMultiplier
  Blockly.Blocks['sap_SapModel_LoadPatterns_SetSelfWTMultiplier'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadPatterns.SetSelfWTMultiplier')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SelfWTMultiplier:'))
          .appendField(new Blockly.FieldTextInput(''), 'SelfWTMultiplier');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Set the self-weight multiplier for a load pattern');
    }
  };

  // DatabaseTables.GetAllTables
  Blockly.Blocks['sap_SapModel_DatabaseTables_GetAllTables'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('DatabaseTables.GetAllTables')
          .appendField(new Blockly.FieldLabel('NumberTables:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberTables');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableKey[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableName[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableName[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ImportType[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'ImportType[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IsEmpty[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'IsEmpty[]');
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
          .appendField('DatabaseTables.GetAvailableTables')
          .appendField(new Blockly.FieldLabel('NumberTables:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberTables');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableKey[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableName[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableName[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ImportType[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'ImportType[]');
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
          .appendField('DatabaseTables.GetAllFieldsInTable')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberFields:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberFields');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldKey[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldKey[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldName[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldName[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Description[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'Description[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('UnitsString[]:'))
          .appendField(new Blockly.FieldDropdown([["lb_in_F (1)", "1"], ["lb_ft_F (2)", "2"], ["kip_in_F (3)", "3"], ["kip_ft_F (4)", "4"], ["kN_mm_C (5)", "5"], ["kN_m_C (6)", "6"], ["kgf_mm_C (7)", "7"], ["kgf_m_C (8)", "8"], ["N_mm_C (9)", "9"], ["N_m_C (10)", "10"], ["Ton_mm_C (11)", "11"], ["Ton_m_C (12)", "12"], ["kN_cm_C (13)", "13"], ["kgf_cm_C (14)", "14"], ["N_cm_C (15)", "15"], ["Ton_cm_C (16)", "16"]]), 'UnitsString[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IsImportable[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'IsImportable[]');
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
          .appendField('DatabaseTables.GetObsoleteTableKeyList')
          .appendField(new Blockly.FieldLabel('NumberTableKeys:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberTableKeys');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableKeyList[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKeyList[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NotesList[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'NotesList[]');
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
          .appendField('DatabaseTables.GetTableForEditingArray')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldKeysIncluded[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldKeysIncluded[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberRecords:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberRecords');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableData[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableData[]');
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
          .appendField('DatabaseTables.SetTableForEditingArray')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldKeysIncluded[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldKeysIncluded[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberRecords:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberRecords');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableData[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableData[]');
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
          .appendField('DatabaseTables.ApplyEditedTables')
          .appendField(new Blockly.FieldLabel('FillImportLog:'))
          .appendField(new Blockly.FieldTextInput(''), 'FillImportLog');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumFatalErrors:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumFatalErrors');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumErrorMsgs:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumErrorMsgs');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumWarnMsgs:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumWarnMsgs');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumInfoMsgs:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumInfoMsgs');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ImportLog:'))
          .appendField(new Blockly.FieldTextInput(''), 'ImportLog');
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
          .appendField('DatabaseTables.GetTableForDisplayArray')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldKeyList[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldKeyList[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldKeysIncluded[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldKeysIncluded[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberRecords:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberRecords');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableData[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableData[]');
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
          .appendField('DatabaseTables.GetTableForDisplayCSVFile')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldKeyList[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldKeyList[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('csvFilePath:'))
          .appendField(new Blockly.FieldTextInput(''), 'csvFilePath');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('sepChar:'))
          .appendField(new Blockly.FieldTextInput(''), 'sepChar');
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
          .appendField('DatabaseTables.GetTableForDisplayCSVString')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldKeyList[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldKeyList[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('csvString:'))
          .appendField(new Blockly.FieldTextInput(''), 'csvString');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('sepChar:'))
          .appendField(new Blockly.FieldTextInput(''), 'sepChar');
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
          .appendField('DatabaseTables.GetTableForDisplayXMLString')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FieldKeyList[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'FieldKeyList[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludeSchema:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludeSchema');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('XMLTableData:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'XMLTableData');
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
          .appendField('DatabaseTables.GetTableForEditingCSVFile')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('csvFilePath:'))
          .appendField(new Blockly.FieldTextInput(''), 'csvFilePath');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('sepChar:'))
          .appendField(new Blockly.FieldTextInput(''), 'sepChar');
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
          .appendField('DatabaseTables.GetTableForEditingCSVString')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('csvString:'))
          .appendField(new Blockly.FieldTextInput(''), 'csvString');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('sepChar:'))
          .appendField(new Blockly.FieldTextInput(''), 'sepChar');
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
          .appendField('DatabaseTables.SetTableForEditingCSVFile')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('csvFilePath:'))
          .appendField(new Blockly.FieldTextInput(''), 'csvFilePath');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('sepChar:'))
          .appendField(new Blockly.FieldTextInput(''), 'sepChar');
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
          .appendField('DatabaseTables.SetTableForEditingCSVString')
          .appendField(new Blockly.FieldLabel('TableKey:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKey');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableVersion:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableVersion');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('csvString:'))
          .appendField(new Blockly.FieldTextInput(''), 'csvString');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('sepChar:'))
          .appendField(new Blockly.FieldTextInput(''), 'sepChar');
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
          .appendField('DatabaseTables.GetLoadCasesSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetLoadCasesSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetLoadCombinationsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetLoadCombinationsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetLoadPatternsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetLoadPatternsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetPushoverNamedSetsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetPushoverNamedSetsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetSectionCutsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberSelected:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberSelected');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.SetSectionCutsSelectedForDisplay')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NameList:'))
          .appendField(new Blockly.FieldTextInput(''), 'NameList');
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
          .appendField('DatabaseTables.GetTableOutputOptionsForDisplay')
          .appendField(new Blockly.FieldLabel('SortTableData:'))
          .appendField(new Blockly.FieldTextInput(''), 'SortTableData');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SortConnectyData:'))
          .appendField(new Blockly.FieldTextInput(''), 'SortConnectyData');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ModeShapeOpt:'))
          .appendField(new Blockly.FieldTextInput(''), 'ModeShapeOpt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ModeShapeRef:'))
          .appendField(new Blockly.FieldTextInput(''), 'ModeShapeRef');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableGroupOpt:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableGroupOpt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableGroupSingle:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableGroupSingle');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwoDFloat:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwoDFloat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwoDFloatFig:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwoDFloatFig');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwoDInt:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwoDInt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FourDFloat:'))
          .appendField(new Blockly.FieldTextInput(''), 'FourDFloat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FourDFloatFig:'))
          .appendField(new Blockly.FieldTextInput(''), 'FourDFloatFig');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FourDInt:'))
          .appendField(new Blockly.FieldTextInput(''), 'FourDInt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EightDFloat:'))
          .appendField(new Blockly.FieldTextInput(''), 'EightDFloat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EightDFloatFig:'))
          .appendField(new Blockly.FieldTextInput(''), 'EightDFloatFig');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EightDInt:'))
          .appendField(new Blockly.FieldTextInput(''), 'EightDInt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwelveDFloat:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwelveDFloat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwelveDFloatFig:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwelveDFloatFig');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwelveDInt:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwelveDInt');
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
          .appendField('DatabaseTables.SetTableOutputOptionsForDisplay')
          .appendField(new Blockly.FieldLabel('SortTableData:'))
          .appendField(new Blockly.FieldTextInput(''), 'SortTableData');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SortConnectyData:'))
          .appendField(new Blockly.FieldTextInput(''), 'SortConnectyData');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ModeShapeOpt:'))
          .appendField(new Blockly.FieldTextInput(''), 'ModeShapeOpt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ModeShapeRef:'))
          .appendField(new Blockly.FieldTextInput(''), 'ModeShapeRef');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableGroupOpt:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableGroupOpt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TableGroupSingle:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableGroupSingle');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwoDFloat:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwoDFloat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwoDFloatFig:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwoDFloatFig');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwoDInt:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwoDInt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FourDFloat:'))
          .appendField(new Blockly.FieldTextInput(''), 'FourDFloat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FourDFloatFig:'))
          .appendField(new Blockly.FieldTextInput(''), 'FourDFloatFig');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FourDInt:'))
          .appendField(new Blockly.FieldTextInput(''), 'FourDInt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EightDFloat:'))
          .appendField(new Blockly.FieldTextInput(''), 'EightDFloat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EightDFloatFig:'))
          .appendField(new Blockly.FieldTextInput(''), 'EightDFloatFig');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EightDInt:'))
          .appendField(new Blockly.FieldTextInput(''), 'EightDInt');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwelveDFloat:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwelveDFloat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwelveDFloatFig:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwelveDFloatFig');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TwelveDInt:'))
          .appendField(new Blockly.FieldTextInput(''), 'TwelveDInt');
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
          .appendField('DatabaseTables.ShowTablesInExcel')
          .appendField(new Blockly.FieldLabel('TableKeyList[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'TableKeyList[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('WindowHandle:'))
          .appendField(new Blockly.FieldTextInput(''), 'WindowHandle');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Export specified tables directly to Excel. Excel must be installed. Returns 0 on success.');
    }
  };

  // SapModel.GetModelIsLocked
  Blockly.Blocks['sap_SapModel_GetModelIsLocked'] = {
    init: function() {
      this.setColour(210);
      this.appendDummyInput()
          .appendField('SapModel.GetModelIsLocked()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Check if the model is currently locked (analysis run)');
    }
  };

  // FrameObj.GetLoadDistributed
  Blockly.Blocks['sap_SapModel_FrameObj_GetLoadDistributed'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetLoadDistributed')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FrameName:'))
          .appendField(new Blockly.FieldTextInput(''), 'FrameName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadPat:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadPat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyType:'))
          .appendField(new Blockly.FieldNumber(1, -Infinity, Infinity, 1), 'MyType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dir:'))
          .appendField(new Blockly.FieldDropdown([["Local1 (1)", "1"], ["Local2 (2)", "2"], ["Local3 (3)", "3"], ["X (4)", "4"], ["Y (5)", "5"], ["Z (6)", "6"], ["GravityProjected (10)", "10"], ["GravityFull (11)", "11"]]), 'Dir');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('RD1:'))
          .appendField(new Blockly.FieldTextInput(''), 'RD1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('RD2:'))
          .appendField(new Blockly.FieldTextInput(''), 'RD2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dist1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Dist1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dist2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Dist2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Val1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Val1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Val2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Val2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('FrameObj.SetLoadPoint')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadPat:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadPat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyType:'))
          .appendField(new Blockly.FieldNumber(1, -Infinity, Infinity, 1), 'MyType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dir:'))
          .appendField(new Blockly.FieldDropdown([["Local1 (1)", "1"], ["Local2 (2)", "2"], ["Local3 (3)", "3"], ["X (4)", "4"], ["Y (5)", "5"], ["Z (6)", "6"], ["GravityProjected (10)", "10"], ["GravityFull (11)", "11"]]), 'Dir');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dist:'))
          .appendField(new Blockly.FieldTextInput(''), 'Dist');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Val:'))
          .appendField(new Blockly.FieldTextInput(''), 'Val');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('RelDist:'))
          .appendField(new Blockly.FieldTextInput(''), 'RelDist');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Replace:'))
          .appendField(new Blockly.FieldCheckbox('TRUE'), 'Replace');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('AreaObj.SetLoadUniform')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadPat:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadPat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Dir:'))
          .appendField(new Blockly.FieldDropdown([["Local1 (1)", "1"], ["Local2 (2)", "2"], ["Local3 (3)", "3"], ["X (4)", "4"], ["Y (5)", "5"], ["Z (6)", "6"], ["GravityProjected (10)", "10"], ["GravityFull (11)", "11"]]), 'Dir');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Replace:'))
          .appendField(new Blockly.FieldCheckbox('TRUE'), 'Replace');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('Results.BaseReact')
          .appendField(new Blockly.FieldLabel('NumberResults:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberResults');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadCase');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepType:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepNum:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepNum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Fx:'))
          .appendField(new Blockly.FieldTextInput(''), 'Fx');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Fy:'))
          .appendField(new Blockly.FieldTextInput(''), 'Fy');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Fz:'))
          .appendField(new Blockly.FieldTextInput(''), 'Fz');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Mx:'))
          .appendField(new Blockly.FieldTextInput(''), 'Mx');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('My:'))
          .appendField(new Blockly.FieldTextInput(''), 'My');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Mz:'))
          .appendField(new Blockly.FieldTextInput(''), 'Mz');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('gx:'))
          .appendField(new Blockly.FieldTextInput(''), 'gx');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('gy:'))
          .appendField(new Blockly.FieldTextInput(''), 'gy');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('gz:'))
          .appendField(new Blockly.FieldTextInput(''), 'gz');
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
          .appendField('AreaObj.SetLoadGravity')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadPat:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadPat');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('x:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'x');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('y:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'y');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('z:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'z');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Replace:'))
          .appendField(new Blockly.FieldCheckbox('TRUE'), 'Replace');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('FrameObj.SetReleases')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ii:'))
          .appendField(new Blockly.FieldTextInput(''), 'ii');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('jj:'))
          .appendField(new Blockly.FieldTextInput(''), 'jj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StartValue:'))
          .appendField(new Blockly.FieldTextInput(''), 'StartValue');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EndValue:'))
          .appendField(new Blockly.FieldTextInput(''), 'EndValue');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('FrameObj.GetReleases')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ii:'))
          .appendField(new Blockly.FieldTextInput(''), 'ii');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('jj:'))
          .appendField(new Blockly.FieldTextInput(''), 'jj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StartValue:'))
          .appendField(new Blockly.FieldTextInput(''), 'StartValue');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EndValue:'))
          .appendField(new Blockly.FieldTextInput(''), 'EndValue');
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
          .appendField('FrameObj.SetInsertionPoint_1')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CardinalPoint:'))
          .appendField(new Blockly.FieldTextInput(''), 'CardinalPoint');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Mirror2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Mirror2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Mirror3:'))
          .appendField(new Blockly.FieldTextInput(''), 'Mirror3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StiffTransform:'))
          .appendField(new Blockly.FieldTextInput(''), 'StiffTransform');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Offset1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Offset1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Offset2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Offset2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign cardinal point and joint offsets to frame objects');
    }
  };

  // FrameObj.GetInsertionPoint_1
  Blockly.Blocks['sap_SapModel_FrameObj_GetInsertionPoint_1'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetInsertionPoint_1')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CardinalPoint:'))
          .appendField(new Blockly.FieldTextInput(''), 'CardinalPoint');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Mirror2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Mirror2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StiffTransform:'))
          .appendField(new Blockly.FieldTextInput(''), 'StiffTransform');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Offset1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Offset1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Offset2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Offset2');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the insertion point (cardinal point and offsets) of a frame');
    }
  };

  // FrameObj.SetLocalAxes
  Blockly.Blocks['sap_SapModel_FrameObj_SetLocalAxes'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.SetLocalAxes')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ang:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ang');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Assign local axis rotation angle to frame objects');
    }
  };

  // FrameObj.GetLocalAxes
  Blockly.Blocks['sap_SapModel_FrameObj_GetLocalAxes'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetLocalAxes')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ang:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ang');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Advanced:'))
          .appendField(new Blockly.FieldTextInput(''), 'Advanced');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the local axes rotation angle for a frame object');
    }
  };

  // GroupDef.SetGroup
  Blockly.Blocks['sap_SapModel_GroupDef_SetGroup'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('GroupDef.SetGroup')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForSelection:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForSelection');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForSectionCutDefinition:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForSectionCutDefinition');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForSteelDesign:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForSteelDesign');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForConcreteDesign:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForConcreteDesign');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForAluminumDesign:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForAluminumDesign');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForColdFormedDesign:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForColdFormedDesign');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForStaticNLActiveStage:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForStaticNLActiveStage');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForBridgeResponseOutput:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForBridgeResponseOutput');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForAutoSeismicOutput:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForAutoSeismicOutput');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForAutoWindOutput:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForAutoWindOutput');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SpecifiedForMassAndWeight:'))
          .appendField(new Blockly.FieldTextInput(''), 'SpecifiedForMassAndWeight');
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
          .appendField('GroupDef.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
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
          .appendField('FrameObj.SetGroupAssign')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Remove:'))
          .appendField(new Blockly.FieldTextInput(''), 'Remove');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add or remove frame objects from a group');
    }
  };

  // GroupDef.GetAssignments
  Blockly.Blocks['sap_SapModel_GroupDef_GetAssignments'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('GroupDef.GetAssignments')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ObjectType:'))
          .appendField(new Blockly.FieldTextInput(''), 'ObjectType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ObjectName:'))
          .appendField(new Blockly.FieldTextInput(''), 'ObjectName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get all objects assigned to a named group');
    }
  };

  // AreaObj.SetGroupAssign
  Blockly.Blocks['sap_SapModel_AreaObj_SetGroupAssign'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.SetGroupAssign')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GroupName:'))
          .appendField(new Blockly.FieldTextInput(''), 'GroupName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Remove:'))
          .appendField(new Blockly.FieldTextInput(''), 'Remove');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('ConstraintDef.SetDiaphragm')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Axis:'))
          .appendField(new Blockly.FieldTextInput(''), 'Axis');
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
          .appendField('ConstraintDef.GetDiaphragm')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Axis:'))
          .appendField(new Blockly.FieldTextInput(''), 'Axis');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve diaphragm constraint definition (axis and coordinate system)');
    }
  };

  // AreaObj.GetPoints
  Blockly.Blocks['sap_SapModel_AreaObj_GetPoints'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.GetPoints')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberPoints:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberPoints');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Point:'))
          .appendField(new Blockly.FieldTextInput(''), 'Point');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the corner point names of an area object');
    }
  };

  // Results.AreaStressShell
  Blockly.Blocks['sap_SapModel_Results_AreaStressShell'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.AreaStressShell')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemTypeElm:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemTypeElm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberResults:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberResults');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Obj:'))
          .appendField(new Blockly.FieldTextInput(''), 'Obj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Elm:'))
          .appendField(new Blockly.FieldTextInput(''), 'Elm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PointElm:'))
          .appendField(new Blockly.FieldTextInput(''), 'PointElm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadCase');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepType:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepNum:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepNum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S11Top:'))
          .appendField(new Blockly.FieldTextInput(''), 'S11Top');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S22Top:'))
          .appendField(new Blockly.FieldTextInput(''), 'S22Top');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S12Top:'))
          .appendField(new Blockly.FieldTextInput(''), 'S12Top');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SMaxTop:'))
          .appendField(new Blockly.FieldTextInput(''), 'SMaxTop');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SMinTop:'))
          .appendField(new Blockly.FieldTextInput(''), 'SMinTop');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SAngleTop:'))
          .appendField(new Blockly.FieldTextInput(''), 'SAngleTop');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SVMTop:'))
          .appendField(new Blockly.FieldTextInput(''), 'SVMTop');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S11Bot:'))
          .appendField(new Blockly.FieldTextInput(''), 'S11Bot');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S22Bot:'))
          .appendField(new Blockly.FieldTextInput(''), 'S22Bot');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S12Bot:'))
          .appendField(new Blockly.FieldTextInput(''), 'S12Bot');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SMaxBot:'))
          .appendField(new Blockly.FieldTextInput(''), 'SMaxBot');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SMinBot:'))
          .appendField(new Blockly.FieldTextInput(''), 'SMinBot');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SAngleBot:'))
          .appendField(new Blockly.FieldTextInput(''), 'SAngleBot');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SVMBot:'))
          .appendField(new Blockly.FieldTextInput(''), 'SVMBot');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S13Avg:'))
          .appendField(new Blockly.FieldTextInput(''), 'S13Avg');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('S23Avg:'))
          .appendField(new Blockly.FieldTextInput(''), 'S23Avg');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SMaxAvg:'))
          .appendField(new Blockly.FieldTextInput(''), 'SMaxAvg');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SAngleAvg:'))
          .appendField(new Blockly.FieldTextInput(''), 'SAngleAvg');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Extract shell element stresses (S11, S22, S12 at top/bottom, principal, Von Mises)');
    }
  };

  // PointObj.GetNameList
  Blockly.Blocks['sap_SapModel_PointObj_GetNameList'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names of all point objects in the model');
    }
  };

  // Results.ModalPeriod
  Blockly.Blocks['sap_SapModel_Results_ModalPeriod'] = {
    init: function() {
      this.setColour(270);
      this.appendDummyInput()
          .appendField('Results.ModalPeriod')
          .appendField(new Blockly.FieldLabel('NumberResults:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberResults');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadCase');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepType:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepNum:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepNum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Period:'))
          .appendField(new Blockly.FieldTextInput(''), 'Period');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Frequency:'))
          .appendField(new Blockly.FieldTextInput(''), 'Frequency');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CircFreq:'))
          .appendField(new Blockly.FieldTextInput(''), 'CircFreq');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EigenValue:'))
          .appendField(new Blockly.FieldTextInput(''), 'EigenValue');
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
          .appendField('Results.ModalParticipatingMassRatios')
          .appendField(new Blockly.FieldLabel('NumberResults:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberResults');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadCase');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepType:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepNum:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepNum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Period:'))
          .appendField(new Blockly.FieldTextInput(''), 'Period');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ux:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ux');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Uy:'))
          .appendField(new Blockly.FieldTextInput(''), 'Uy');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Uz:'))
          .appendField(new Blockly.FieldTextInput(''), 'Uz');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SumUx:'))
          .appendField(new Blockly.FieldTextInput(''), 'SumUx');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SumUy:'))
          .appendField(new Blockly.FieldTextInput(''), 'SumUy');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SumUz:'))
          .appendField(new Blockly.FieldTextInput(''), 'SumUz');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Rx:'))
          .appendField(new Blockly.FieldTextInput(''), 'Rx');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ry:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ry');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Rz:'))
          .appendField(new Blockly.FieldTextInput(''), 'Rz');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SumRx:'))
          .appendField(new Blockly.FieldTextInput(''), 'SumRx');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SumRy:'))
          .appendField(new Blockly.FieldTextInput(''), 'SumRy');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SumRz:'))
          .appendField(new Blockly.FieldTextInput(''), 'SumRz');
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
          .appendField('Results.ModeShape')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemTypeElm:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemTypeElm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberResults:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberResults');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Obj:'))
          .appendField(new Blockly.FieldTextInput(''), 'Obj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Elm:'))
          .appendField(new Blockly.FieldTextInput(''), 'Elm');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadCase:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadCase');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepType:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StepNum:'))
          .appendField(new Blockly.FieldTextInput(''), 'StepNum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('U1:'))
          .appendField(new Blockly.FieldTextInput(''), 'U1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('U2:'))
          .appendField(new Blockly.FieldTextInput(''), 'U2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('U3:'))
          .appendField(new Blockly.FieldTextInput(''), 'U3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('R1:'))
          .appendField(new Blockly.FieldTextInput(''), 'R1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('R2:'))
          .appendField(new Blockly.FieldTextInput(''), 'R2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('R3:'))
          .appendField(new Blockly.FieldTextInput(''), 'R3');
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
          .appendField('Analyze.SetActiveDOF')
          .appendField(new Blockly.FieldLabel('DOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'DOF');
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
          .appendField('Analyze.GetActiveDOF')
          .appendField(new Blockly.FieldLabel('DOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'DOF');
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
          .appendField('Analyze.GetCaseStatus')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CaseName:'))
          .appendField(new Blockly.FieldTextInput(''), 'CaseName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Status:'))
          .appendField(new Blockly.FieldTextInput(''), 'Status');
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
          .appendField('File.OpenFile')
          .appendField(new Blockly.FieldLabel('FileName:'))
          .appendField(new Blockly.FieldTextInput(''), 'FileName');
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
          .appendField('PropLink.SetLinear')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'DOF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Fixed:'))
          .appendField(new Blockly.FieldTextInput(''), 'Fixed');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ke:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ke');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ce:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ce');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('dj2:'))
          .appendField(new Blockly.FieldTextInput(''), 'dj2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('dj3:'))
          .appendField(new Blockly.FieldTextInput(''), 'dj3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('KeCoupled:'))
          .appendField(new Blockly.FieldTextInput(''), 'KeCoupled');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CeCoupled:'))
          .appendField(new Blockly.FieldTextInput(''), 'CeCoupled');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a linear-type link property (stiffness, damping, DOFs)');
    }
  };

  // PropLink.GetLinear
  Blockly.Blocks['sap_SapModel_PropLink_GetLinear'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropLink.GetLinear')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'DOF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Fixed:'))
          .appendField(new Blockly.FieldTextInput(''), 'Fixed');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ke:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ke');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ce:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ce');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DJ2:'))
          .appendField(new Blockly.FieldTextInput(''), 'DJ2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DJ3:'))
          .appendField(new Blockly.FieldTextInput(''), 'DJ3');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get linear link property parameters');
    }
  };

  // LinkObj.AddByPoint
  Blockly.Blocks['sap_SapModel_LinkObj_AddByPoint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('LinkObj.AddByPoint')
          .appendField(new Blockly.FieldLabel('Point1:'))
          .appendField(new Blockly.FieldTextInput(''), 'Point1');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Point2:'))
          .appendField(new Blockly.FieldTextInput(''), 'Point2');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IsSingleJoint:'))
          .appendField(new Blockly.FieldTextInput(''), 'IsSingleJoint');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('UserName:'))
          .appendField(new Blockly.FieldTextInput(''), 'UserName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a two-joint link element between two existing point objects.');
    }
  };

  // LinkObj.Count
  Blockly.Blocks['sap_SapModel_LinkObj_Count'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('LinkObj.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the number of link objects in the model');
    }
  };

  // LinkObj.AddByCoord
  Blockly.Blocks['sap_SapModel_LinkObj_AddByCoord'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('LinkObj.AddByCoord')
          .appendField(new Blockly.FieldLabel('xi:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'xi');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('yi:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'yi');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('zi:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'zi');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('xj:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'xj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('yj:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'yj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('zj:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'zj');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IsSingleJoint:'))
          .appendField(new Blockly.FieldTextInput(''), 'IsSingleJoint');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('UserName:'))
          .appendField(new Blockly.FieldTextInput(''), 'UserName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a link element by specifying I-End and J-End coordinates');
    }
  };

  // AreaObj.GetProperty
  Blockly.Blocks['sap_SapModel_AreaObj_GetProperty'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.GetProperty')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SAuto:'))
          .appendField(new Blockly.FieldTextInput(''), 'SAuto');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the section property assigned to an area object');
    }
  };

  // AreaObj.SetProperty
  Blockly.Blocks['sap_SapModel_AreaObj_SetProperty'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.SetProperty')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
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
          .appendField('PropArea.GetShell_1')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ShellType:'))
          .appendField(new Blockly.FieldDropdown([["ShellThin (1)", "1"], ["ShellThick (2)", "2"], ["Membrane (3)", "3"], ["Plate (4)", "4"]]), 'ShellType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IncludeDrillingDOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludeDrillingDOF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatAng:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatAng');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Thickness:'))
          .appendField(new Blockly.FieldTextInput(''), 'Thickness');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Bending:'))
          .appendField(new Blockly.FieldTextInput(''), 'Bending');
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
          .appendField(new Blockly.FieldTextInput(''), 'EFy');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('EFu:'))
          .appendField(new Blockly.FieldTextInput(''), 'EFu');
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
          .appendField(new Blockly.FieldTextInput(''), 'DilatationalAngle');
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
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'A');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Retrieve isotropic mechanical properties (E, Poisson ratio, thermal expansion coefficient)');
    }
  };

  // PropMaterial.GetNameList
  Blockly.Blocks['sap_SapModel_PropMaterial_GetNameList'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names of all material properties defined in the model');
    }
  };

  // PropFrame.SetAngle
  Blockly.Blocks['sap_SapModel_PropFrame_SetAngle'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetAngle')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
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
      this.setTooltip('Define an angle (L-shape) frame section');
    }
  };

  // PropFrame.SetChannel
  Blockly.Blocks['sap_SapModel_PropFrame_SetChannel'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetChannel')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
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
      this.setTooltip('Define a channel (C-shape) frame section');
    }
  };

  // PropFrame.SetPipe
  Blockly.Blocks['sap_SapModel_PropFrame_SetPipe'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropFrame.SetPipe')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T3:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('TW:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'TW');
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
          .appendField('PropFrame.GetRectangle')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FileName:'))
          .appendField(new Blockly.FieldTextInput(''), 'FileName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T3:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T3');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T2:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T2');
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
          .appendField('PropFrame.GetCircle')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FileName:'))
          .appendField(new Blockly.FieldTextInput(''), 'FileName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('T3:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'T3');
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
          .appendField('PropFrame.GetISection')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('FileName:'))
          .appendField(new Blockly.FieldTextInput(''), 'FileName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatProp:'))
          .appendField(new Blockly.FieldTextInput(''), 'MatProp');
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
      this.setTooltip('Retrieve I-section properties');
    }
  };

  // DesignSteel.SetComboStrength
  Blockly.Blocks['sap_SapModel_DesignSteel_SetComboStrength'] = {
    init: function() {
      this.setColour(300);
      this.appendDummyInput()
          .appendField('DesignSteel.SetComboStrength')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Selected:'))
          .appendField(new Blockly.FieldTextInput(''), 'Selected');
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
          .appendField('DesignSteel.GetComboStrength')
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName[]');
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
          .appendField('DesignSteel.SetComboDeflection')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Selected:'))
          .appendField(new Blockly.FieldTextInput(''), 'Selected');
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
          .appendField('DesignSteel.GetCode')
          .appendField(new Blockly.FieldLabel('CodeName:'))
          .appendField(new Blockly.FieldTextInput(''), 'CodeName');
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
          .appendField('DesignSteel.SetCode')
          .appendField(new Blockly.FieldLabel('CodeName:'))
          .appendField(new Blockly.FieldTextInput(''), 'CodeName');
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
          .appendField('DesignConcrete.SetComboStrength')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Selected:'))
          .appendField(new Blockly.FieldTextInput(''), 'Selected');
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
          .appendField('DesignConcrete.GetCode')
          .appendField(new Blockly.FieldLabel('CodeName:'))
          .appendField(new Blockly.FieldTextInput(''), 'CodeName');
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
          .appendField('DesignConcrete.SetCode')
          .appendField(new Blockly.FieldLabel('CodeName:'))
          .appendField(new Blockly.FieldTextInput(''), 'CodeName');
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
          .appendField('RespCombo.Delete')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
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
          .appendField('RespCombo.ChangeName')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NewName:'))
          .appendField(new Blockly.FieldTextInput(''), 'NewName');
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
          .appendField('RespCombo.SetTypeOAPI')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ComboType:'))
          .appendField(new Blockly.FieldDropdown([["LinearAdd (0)", "0"], ["Envelope (1)", "1"], ["AbsAdd (2)", "2"], ["SRSS (3)", "3"], ["RangeAdd (4)", "4"]]), 'ComboType');
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
          .appendField('RespCombo.GetTypeOAPI')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
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
          .appendField('RespCombo.DeleteCase')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CType:'))
          .appendField(new Blockly.FieldTextInput(''), 'CType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CName:'))
          .appendField(new Blockly.FieldTextInput(''), 'CName');
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
          .appendField('RespCombo.AddDesignDefaultCombos')
          .appendField(new Blockly.FieldLabel('DesignSteel:'))
          .appendField(new Blockly.FieldTextInput(''), 'DesignSteel');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DesignConcrete:'))
          .appendField(new Blockly.FieldTextInput(''), 'DesignConcrete');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DesignAluminum:'))
          .appendField(new Blockly.FieldTextInput(''), 'DesignAluminum');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DesignColdFormed:'))
          .appendField(new Blockly.FieldTextInput(''), 'DesignColdFormed');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add default design combinations by material type');
    }
  };

  // File.New2DFrame
  Blockly.Blocks['sap_SapModel_File_New2DFrame'] = {
    init: function() {
      this.setColour(0);
      this.appendDummyInput()
          .appendField('File.New2DFrame')
          .appendField(new Blockly.FieldLabel('TemplateName:'))
          .appendField(new Blockly.FieldTextInput(''), 'TemplateName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberStorys:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'NumberStorys');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('StoryHeight:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'StoryHeight');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberBays:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'NumberBays');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('BayWidth:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'BayWidth');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('OverWrite:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'OverWrite');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('RestraintType:'))
          .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001), 'RestraintType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Create a new 2D frame model from a built-in template');
    }
  };

  // SapModel.GetVersion
  Blockly.Blocks['sap_SapModel_GetVersion'] = {
    init: function() {
      this.setColour(210);
      this.appendDummyInput()
          .appendField('SapModel.GetVersion')
          .appendField(new Blockly.FieldLabel('Version:'))
          .appendField(new Blockly.FieldTextInput(''), 'Version');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the SAP2000 version number');
    }
  };

  // ResponseSpectrum.SetDampConstant
  Blockly.Blocks['sap_SapModel_LoadCases_ResponseSpectrum_SetDampConstant'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('ResponseSpectrum.SetDampConstant')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Damp:'))
          .appendField(new Blockly.FieldTextInput(''), 'Damp');
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
          .appendField('LoadCases.Count')
          .appendField(new Blockly.FieldLabel('CaseType:'))
          .appendField(new Blockly.FieldTextInput(''), 'CaseType');
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
          .appendField('LoadCases.Delete')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
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
          .appendField('LoadCases.ChangeName')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NewName:'))
          .appendField(new Blockly.FieldTextInput(''), 'NewName');
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
          .appendField('LoadPatterns.Delete')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
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
          .appendField('LoadPatterns.ChangeName')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NewName:'))
          .appendField(new Blockly.FieldTextInput(''), 'NewName');
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
          .appendField('SourceMass.SetMassSource')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MassFromElements:'))
          .appendField(new Blockly.FieldTextInput(''), 'MassFromElements');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MassFromMasses:'))
          .appendField(new Blockly.FieldTextInput(''), 'MassFromMasses');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MassFromLoads:'))
          .appendField(new Blockly.FieldTextInput(''), 'MassFromLoads');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IsDefault:'))
          .appendField(new Blockly.FieldTextInput(''), 'IsDefault');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberLoads:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberLoads');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadPat[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadPat[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SF[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'SF[]');
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
          .appendField('SourceMass.GetMassSource')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MassFromElements:'))
          .appendField(new Blockly.FieldTextInput(''), 'MassFromElements');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MassFromMasses:'))
          .appendField(new Blockly.FieldTextInput(''), 'MassFromMasses');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MassFromLoads:'))
          .appendField(new Blockly.FieldTextInput(''), 'MassFromLoads');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('IsDefault:'))
          .appendField(new Blockly.FieldTextInput(''), 'IsDefault');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberLoads:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberLoads');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('LoadPat[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'LoadPat[]');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('SF[]:'))
          .appendField(new Blockly.FieldTextInput(''), 'SF[]');
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
          .appendField('SourceMass.GetDefault')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
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
          .appendField('FrameObj.SetModifiers')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
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
          .appendField('FrameObj.GetModifiers')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
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
          .appendField('PropArea.SetModifiers')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
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
          .appendField('PropArea.GetModifiers')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
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
          .appendField('PropFrame.ChangeName')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NewName:'))
          .appendField(new Blockly.FieldTextInput(''), 'NewName');
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
          .appendField('PropFrame.Count')
          .appendField(new Blockly.FieldLabel('PropType:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropType');
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
          .appendField('PropFrame.Delete')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
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
          .appendField('PropMaterial.ChangeName')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NewName:'))
          .appendField(new Blockly.FieldTextInput(''), 'NewName');
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
          .appendField('PropMaterial.Count')
          .appendField(new Blockly.FieldLabel('MatType:'))
          .appendField(new Blockly.FieldDropdown([["Steel (1)", "1"], ["Concrete (2)", "2"], ["NoDesign (3)", "3"], ["Aluminum (4)", "4"], ["ColdFormed (5)", "5"], ["Rebar (6)", "6"], ["Tendon (7)", "7"]]), 'MatType');
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
          .appendField('PropMaterial.Delete')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
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
          .appendField('PropLink.SetGap')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'DOF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Fixed:'))
          .appendField(new Blockly.FieldTextInput(''), 'Fixed');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Ke:'))
          .appendField(new Blockly.FieldTextInput(''), 'Ke');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Nonlinear:'))
          .appendField(new Blockly.FieldTextInput(''), 'Nonlinear');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('GapOpens:'))
          .appendField(new Blockly.FieldTextInput(''), 'GapOpens');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Opens:'))
          .appendField(new Blockly.FieldTextInput(''), 'Opens');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Define a Gap-type nonlinear link property (compression-only). DOF arrays size 6.');
    }
  };

  // PropLink.Count
  Blockly.Blocks['sap_SapModel_PropLink_Count'] = {
    init: function() {
      this.setColour(60);
      this.appendDummyInput()
          .appendField('PropLink.Count()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the number of link/support properties defined');
    }
  };

  // AreaObj.AddByPoint
  Blockly.Blocks['sap_SapModel_AreaObj_AddByPoint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.AddByPoint')
          .appendField(new Blockly.FieldLabel('NumberPoints:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberPoints');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Point:'))
          .appendField(new Blockly.FieldTextInput(''), 'Point');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PropName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PropName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('UserName:'))
          .appendField(new Blockly.FieldTextInput(''), 'UserName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add an area object by specifying existing point names');
    }
  };

  // ConstraintDef.GetNameList
  Blockly.Blocks['sap_SapModel_ConstraintDef_GetNameList'] = {
    init: function() {
      this.setColour(160);
      this.appendDummyInput()
          .appendField('ConstraintDef.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names of all constraints defined in the model');
    }
  };

  // AreaObj.GetNameList
  Blockly.Blocks['sap_SapModel_AreaObj_GetNameList'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names of all area objects in the model');
    }
  };

  // SapModel.GetPresentUnits
  Blockly.Blocks['sap_SapModel_GetPresentUnits'] = {
    init: function() {
      this.setColour(210);
      this.appendDummyInput()
          .appendField('SapModel.GetPresentUnits()');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the current display units of the model');
    }
  };

  // PropMaterial.AddMaterial
  Blockly.Blocks['sap_SapModel_PropMaterial_AddMaterial'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.AddMaterial')
          .appendField(new Blockly.FieldLabel('Region:'))
          .appendField(new Blockly.FieldTextInput(''), 'Region');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Standard:'))
          .appendField(new Blockly.FieldTextInput(''), 'Standard');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Grade:'))
          .appendField(new Blockly.FieldTextInput(''), 'Grade');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Add a material from the built-in SAP2000 database');
    }
  };

  // PropMaterial.GetTypeOAPI
  Blockly.Blocks['sap_SapModel_PropMaterial_GetTypeOAPI'] = {
    init: function() {
      this.setColour(30);
      this.appendDummyInput()
          .appendField('PropMaterial.GetTypeOAPI')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MatType:'))
          .appendField(new Blockly.FieldDropdown([["Steel (1)", "1"], ["Concrete (2)", "2"], ["NoDesign (3)", "3"], ["Aluminum (4)", "4"], ["ColdFormed (5)", "5"], ["Rebar (6)", "6"], ["Tendon (7)", "7"]]), 'MatType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the material type (eMatType) for a material property');
    }
  };

  // AreaObj.GetGroupAssign
  Blockly.Blocks['sap_SapModel_AreaObj_GetGroupAssign'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.GetGroupAssign')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberGroups:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberGroups');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Groups:'))
          .appendField(new Blockly.FieldTextInput(''), 'Groups');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get groups assigned to an area object');
    }
  };

  // PointObj.GetRestraint
  Blockly.Blocks['sap_SapModel_PointObj_GetRestraint'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.GetRestraint')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the restraint conditions for a point object');
    }
  };

  // LoadCases.GetTypeOAPI
  Blockly.Blocks['sap_SapModel_LoadCases_GetTypeOAPI'] = {
    init: function() {
      this.setColour(200);
      this.appendDummyInput()
          .appendField('LoadCases.GetTypeOAPI')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('CaseType:'))
          .appendField(new Blockly.FieldTextInput(''), 'CaseType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the load case type for a named load case');
    }
  };

  // SapModel.GetModelFilename
  Blockly.Blocks['sap_SapModel_GetModelFilename'] = {
    init: function() {
      this.setColour(0);
      this.appendDummyInput()
          .appendField('SapModel.GetModelFilename')
          .appendField(new Blockly.FieldLabel('IncludePath:'))
          .appendField(new Blockly.FieldTextInput(''), 'IncludePath');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get the current model file path');
    }
  };

  // SapModel.SetModelIsLocked
  Blockly.Blocks['sap_SapModel_SetModelIsLocked'] = {
    init: function() {
      this.setColour(210);
      this.appendDummyInput()
          .appendField('SapModel.SetModelIsLocked')
          .appendField(new Blockly.FieldLabel('LockIt:'))
          .appendField(new Blockly.FieldTextInput(''), 'LockIt');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Lock or unlock the model');
    }
  };

  // FrameObj.GetNameList
  Blockly.Blocks['sap_SapModel_FrameObj_GetNameList'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.GetNameList')
          .appendField(new Blockly.FieldLabel('NumberNames:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberNames');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('MyName:'))
          .appendField(new Blockly.FieldTextInput(''), 'MyName');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get names of all frame objects in the model');
    }
  };

  // FrameObj.Delete
  Blockly.Blocks['sap_SapModel_FrameObj_Delete'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('FrameObj.Delete')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Delete a frame object from the model');
    }
  };

  // AreaObj.Delete
  Blockly.Blocks['sap_SapModel_AreaObj_Delete'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('AreaObj.Delete')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Delete an area object from the model');
    }
  };

  // PointObj.GetLoadForce
  Blockly.Blocks['sap_SapModel_PointObj_GetLoadForce'] = {
    init: function() {
      this.setColour(120);
      this.appendDummyInput()
          .appendField('PointObj.GetLoadForce')
          .appendField(new Blockly.FieldLabel('Name:'))
          .appendField(new Blockly.FieldTextInput(''), 'Name');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('NumberItems:'))
          .appendField(new Blockly.FieldTextInput(''), 'NumberItems');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('PatternName:'))
          .appendField(new Blockly.FieldTextInput(''), 'PatternName');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('ItemType:'))
          .appendField(new Blockly.FieldDropdown([["Object (0)", "0"], ["Group (1)", "1"], ["SelectedObjects (2)", "2"]]), 'ItemType');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('DOF:'))
          .appendField(new Blockly.FieldTextInput(''), 'DOF');
      this.appendDummyInput()
          .appendField(new Blockly.FieldLabel('Value:'))
          .appendField(new Blockly.FieldTextInput(''), 'Value');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Get point loads assigned to a joint');
    }
  };

  console.log('✅ ' + Object.keys(Blockly.Blocks).filter(k => k.startsWith("sap_")).length + ' SAP2000 blocks registered');
}
