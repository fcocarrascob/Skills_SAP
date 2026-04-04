// Auto-generado — Generadores Python para cada bloque

python['sap_File_NewBlank'] = function(block) {
  return 'SapModel.File.NewBlank()\n';
};

python['sap_PropMaterial_SetMaterial'] = function(block) {
  var name = Blockly.Python.valueToCode(block, 'Name', Blockly.Python.ORDER_MEMBER);
  var mat_type = Blockly.Python.valueToCode(block, 'MatType', Blockly.Python.ORDER_MEMBER);
  return `SapModel.PropMaterial.SetMaterial(${name}, ${mat_type})\n`;
};

python['sap_FrameObj_AddByCoord'] = function(block) {
  var x1 = Blockly.Python.valueToCode(block, 'X1', Blockly.Python.ORDER_MEMBER);
  var y1 = Blockly.Python.valueToCode(block, 'Y1', Blockly.Python.ORDER_MEMBER);
  var z1 = Blockly.Python.valueToCode(block, 'Z1', Blockly.Python.ORDER_MEMBER);
  var x2 = Blockly.Python.valueToCode(block, 'X2', Blockly.Python.ORDER_MEMBER);
  var y2 = Blockly.Python.valueToCode(block, 'Y2', Blockly.Python.ORDER_MEMBER);
  var z2 = Blockly.Python.valueToCode(block, 'Z2', Blockly.Python.ORDER_MEMBER);
  var prop = Blockly.Python.valueToCode(block, 'Prop', Blockly.Python.ORDER_MEMBER);
  var group = Blockly.Python.valueToCode(block, 'Group', Blockly.Python.ORDER_MEMBER);
  var code = `raw = SapModel.FrameObj.AddByCoord(${x1}, ${y1}, ${z1}, ${x2}, ${y2}, ${z2}, '', ${prop}, ${group})\n`;
  code += `frame_name = raw[0]\n`;
  code += `assert raw[-1] == 0, f'AddByCoord failed: {raw[-1]}'\n`;
  return code;
};

