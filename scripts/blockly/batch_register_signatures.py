"""
Batch Register Signatures — Rellena el campo 'signature' (y category/description)
en el registry.json para las funciones que les falta, habilitando su generacion
en Blockly como bloques con inputs/params.

Fuentes de datos (por prioridad):
  1. Wrappers: extrae "API Signature:" del docstring de cada wrapper
  2. Tabla hardcodeada: para funciones sin wrapper (InitializeNewModel, Count, etc.)

Uso:
    python scripts/blockly/batch_register_signatures.py [--dry-run]
"""

import json
import re
import sys
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = REPO_ROOT / "scripts" / "registry.json"
WRAPPERS_PATH = REPO_ROOT / "scripts" / "wrappers"

DRY_RUN = "--dry-run" in sys.argv

# ── Hardcoded data para funciones sin wrapper ─────────────────────────────────
# Formato: "SapModel.X.Y": {"category": ..., "description": ..., "signature": ...}

HARDCODED: dict[str, dict] = {
    "SapModel.InitializeNewModel": {
        "category": "File",
        "description": "Initialize a new model with specified units",
        "signature": "(Units) -> ret_code",
        "parameter_notes": "Units: int — eUnits enum (e.g. 6=kN_m_C)",
        "notes": "Returns ret_code directly (0=success). Call before File.NewBlank. Units: 1=lb_in, 2=lb_ft, 3=kip_in, 4=kip_ft, 5=kN_mm, 6=kN_m.",
    },
    "SapModel.SetPresentUnits": {
        "category": "General_Functions",
        "description": "Set the current display units for the model",
        "signature": "(Units) -> ret_code",
        "parameter_notes": "Units: int — eUnits enum (e.g. 6=kN_m_C)",
        "notes": "Returns ret_code directly (0=success). Does not convert existing geometry.",
    },
    "SapModel.GetPresentUnits": {
        "category": "General_Functions",
        "description": "Get the current display units of the model",
        "signature": "() -> Units",
        "parameter_notes": "No input parameters. Returns units enum integer.",
        "notes": "Returns integer directly (eUnits value). Not a list.",
    },
    "SapModel.GetVersion": {
        "category": "General_Functions",
        "description": "Get the SAP2000 version number",
        "signature": "(Version) -> ret_code",
        "parameter_notes": "Version: str — (ByRef out) version string e.g. '22.0.0'",
        "notes": "ByRef output: [Version, ret_code]. Version is a string.",
    },
    "SapModel.GetModelIsLocked": {
        "category": "General_Functions",
        "description": "Check if the model is currently locked (analysis run)",
        "signature": "() -> IsLocked",
        "parameter_notes": "No inputs. Returns bool directly: True=locked, False=unlocked.",
        "notes": "Returns bool directly (not a list). True after RunAnalysis.",
    },
    "SapModel.SetModelIsLocked": {
        "category": "General_Functions",
        "description": "Lock or unlock the model",
        "signature": "(LockIt) -> ret_code",
        "parameter_notes": "LockIt: bool — True=lock, False=unlock",
        "notes": "Returns ret_code directly (0=success). Unlocking deletes analysis results.",
    },
    "SapModel.GetModelFilename": {
        "category": "File",
        "description": "Get the current model file path",
        "signature": "(IncludePath) -> FileName",
        "parameter_notes": "IncludePath: bool — True=full path, False=filename only",
        "notes": "Returns string directly (not a list). Empty string if model unsaved.",
    },
    # ── PointObj ──────────────────────────────────────────────────────────────
    "SapModel.PointObj.Count": {
        "category": "Object_Model",
        "description": "Get the number of point objects in the model",
        "signature": "() -> count",
        "parameter_notes": "No inputs. Returns integer count directly.",
        "notes": "Returns integer directly (not a list).",
    },
    "SapModel.PointObj.GetCoordCartesian": {
        "category": "Object_Model",
        "description": "Get Cartesian coordinates of a point object",
        "signature": "(Name, X, Y, Z, CSys) -> ret_code",
        "parameter_notes": "Name: str — point name; X/Y/Z: float — (ByRef out) coordinates; CSys: str — coordinate system (default 'Global')",
        "notes": "ByRef layout: [X, Y, Z, CSys, ret_code]. Pass 0.0, 0.0, 0.0, '' as placeholders.",
    },
    "SapModel.PointObj.GetNameList": {
        "category": "Object_Model",
        "description": "Get names of all point objects in the model",
        "signature": "(NumberNames, MyName) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) array of names",
        "notes": "ByRef layout: [NumberNames, MyName[], ret_code]. Pass 0, [] as placeholders.",
    },
    "SapModel.PointObj.SetConstraint": {
        "category": "Object_Model",
        "description": "Assign a constraint to a point object",
        "signature": "(Name, ConstraintName, ItemType) -> ret_code",
        "parameter_notes": "Name: str — point name; ConstraintName: str — constraint name; ItemType: int — 0=Object, 1=Group, 2=Selection",
        "notes": "Returns ret_code directly. Prerequisite: constraint must exist via ConstraintDef.SetBody.",
    },
    "SapModel.PointObj.GetRestraint": {
        "category": "Object_Model",
        "description": "Get the restraint conditions for a point object",
        "signature": "(Name, Value, ItemType) -> ret_code",
        "parameter_notes": "Name: str — point name; Value: bool[6] — (ByRef out) [UX,UY,UZ,RX,RY,RZ]; ItemType: int — 0=Object",
        "notes": "ByRef layout: [Value[6], ret_code]. Pass [False]*6 as placeholder.",
    },
    "SapModel.PointObj.GetLoadForce": {
        "category": "Object_Model",
        "description": "Get point loads assigned to a joint",
        "signature": "(Name, NumberItems, PatternName, ItemType, DOF, Value, CSys) -> ret_code",
        "parameter_notes": "Name: str — joint name or 'All'; NumberItems: int — (ByRef out) count; PatternName: str[] — (ByRef out); ItemType: int — 0=Object",
        "notes": "ByRef layout: [NumberItems, PatternName[], ItemType[], DOF[], Value[], CSys[], ret_code].",
    },
    # ── FrameObj ──────────────────────────────────────────────────────────────
    "SapModel.FrameObj.Count": {
        "category": "Object_Model",
        "description": "Get the number of frame objects in the model",
        "signature": "() -> count",
        "parameter_notes": "No inputs. Returns integer count directly.",
        "notes": "Returns integer directly (not a list).",
    },
    "SapModel.FrameObj.GetPoints": {
        "category": "Object_Model",
        "description": "Get the two endpoint point names of a frame object",
        "signature": "(Name, Point1, Point2) -> ret_code",
        "parameter_notes": "Name: str — frame name; Point1: str — (ByRef out) I-end point; Point2: str — (ByRef out) J-end point",
        "notes": "ByRef layout: [Point1, Point2, ret_code]. Pass '', '' as placeholders.",
    },
    "SapModel.FrameObj.GetSection": {
        "category": "Object_Model",
        "description": "Get the section property assigned to a frame object",
        "signature": "(Name, PropName, SAuto) -> ret_code",
        "parameter_notes": "Name: str — frame name; PropName: str — (ByRef out) property name; SAuto: str — (ByRef out) auto-select list",
        "notes": "ByRef layout: [PropName, SAuto, ret_code]. Pass '', '' as placeholders.",
    },
    "SapModel.FrameObj.GetNameList": {
        "category": "Object_Model",
        "description": "Get names of all frame objects in the model",
        "signature": "(NumberNames, MyName) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) names array",
        "notes": "ByRef layout: [NumberNames, MyName[], ret_code]. Pass 0, [] as placeholders.",
    },
    "SapModel.FrameObj.Delete": {
        "category": "Object_Model",
        "description": "Delete a frame object from the model",
        "signature": "(Name, ItemType) -> ret_code",
        "parameter_notes": "Name: str — frame name or group; ItemType: int — 0=Object, 1=Group, 2=Selection",
        "notes": "Returns ret_code directly. Also deletes loads assigned to the frame.",
    },
    "SapModel.FrameObj.GetInsertionPoint_1": {
        "category": "Object_Model",
        "description": "Get the insertion point (cardinal point and offsets) of a frame",
        "signature": "(Name, CardinalPoint, Mirror2, StiffTransform, Offset1, Offset2, CSys) -> ret_code",
        "parameter_notes": "Name: str — frame name; CardinalPoint: int — (ByRef out) 1-11; Mirror2: bool — (ByRef out); StiffTransform: bool — (ByRef out); Offset1/2: float[3] — (ByRef out)",
        "notes": "ByRef layout: [CardinalPoint, Mirror2, StiffTransform, Offset1[3], Offset2[3], CSys, ret_code].",
    },
    "SapModel.FrameObj.GetLocalAxes": {
        "category": "Object_Model",
        "description": "Get the local axes rotation angle for a frame object",
        "signature": "(Name, Ang, Advanced) -> ret_code",
        "parameter_notes": "Name: str — frame name; Ang: float — (ByRef out) local axis angle [deg]; Advanced: bool — (ByRef out) advanced axis definition",
        "notes": "ByRef layout: [Ang, Advanced, ret_code]. Pass 0.0, False as placeholders.",
    },
    "SapModel.FrameObj.GetTCLimits": {
        "category": "Object_Model",
        "description": "Get the tension/compression limits for a frame object",
        "signature": "(Name, LimitCompressionExists, LimitCompression, LimitTensionExists, LimitTension) -> ret_code",
        "parameter_notes": "Name: str — frame name; LimitCompressionExists: bool — (ByRef out); LimitCompression: float — (ByRef out); LimitTensionExists: bool — (ByRef out); LimitTension: float — (ByRef out)",
        "notes": "ByRef layout: [LimitCompressionExists, LimitCompression, LimitTensionExists, LimitTension, ret_code].",
    },
    # ── AreaObj ───────────────────────────────────────────────────────────────
    "SapModel.AreaObj.Count": {
        "category": "Object_Model",
        "description": "Get the number of area objects in the model",
        "signature": "() -> count",
        "parameter_notes": "No inputs. Returns integer count directly.",
        "notes": "Returns integer directly (not a list).",
    },
    "SapModel.AreaObj.GetPoints": {
        "category": "Object_Model",
        "description": "Get the corner point names of an area object",
        "signature": "(Name, NumberPoints, Point) -> ret_code",
        "parameter_notes": "Name: str — area name; NumberPoints: int — (ByRef out) number of corners; Point: str[] — (ByRef out) corner point names",
        "notes": "ByRef layout: [NumberPoints, Point[], ret_code]. Pass 0, [] as placeholders.",
    },
    "SapModel.AreaObj.GetNameList": {
        "category": "Object_Model",
        "description": "Get names of all area objects in the model",
        "signature": "(NumberNames, MyName) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) names array",
        "notes": "ByRef layout: [NumberNames, MyName[], ret_code]. Pass 0, [] as placeholders.",
    },
    "SapModel.AreaObj.GetProperty": {
        "category": "Object_Model",
        "description": "Get the section property assigned to an area object",
        "signature": "(Name, PropName, SAuto) -> ret_code",
        "parameter_notes": "Name: str — area name; PropName: str — (ByRef out) property name; SAuto: str — (ByRef out)",
        "notes": "ByRef layout: [PropName, SAuto, ret_code]. Pass '', '' as placeholders.",
    },
    "SapModel.AreaObj.GetGroupAssign": {
        "category": "Object_Model",
        "description": "Get groups assigned to an area object",
        "signature": "(Name, NumberGroups, Groups, ItemType) -> ret_code",
        "parameter_notes": "Name: str — area name; NumberGroups: int — (ByRef out) group count; Groups: str[] — (ByRef out) group names; ItemType: int — 0=Object",
        "notes": "ByRef layout: [NumberGroups, Groups[], ret_code].",
    },
    "SapModel.AreaObj.Delete": {
        "category": "Object_Model",
        "description": "Delete an area object from the model",
        "signature": "(Name, ItemType) -> ret_code",
        "parameter_notes": "Name: str — area name or group; ItemType: int — 0=Object, 1=Group, 2=Selection",
        "notes": "Returns ret_code directly. Also deletes loads assigned to the area.",
    },
    "SapModel.AreaObj.AddByPoint": {
        "category": "Object_Model",
        "description": "Add an area object by specifying existing point names",
        "signature": "(NumberPoints, Point, PropName, Name, UserName, CSys) -> ret_code",
        "parameter_notes": "NumberPoints: int — number of vertices; Point: str[] — corner point names; PropName: str — section property; Name: str — (ByRef out) assigned name; UserName: str — optional user name",
        "notes": "ByRef layout: [Name, ret_code]. Pass '' for Name. Points must exist.",
    },
    # ── PropArea ──────────────────────────────────────────────────────────────
    "SapModel.PropArea.GetNameList": {
        "category": "Properties",
        "description": "Get names of all area section properties defined in the model",
        "signature": "(NumberNames, MyName) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) names",
        "notes": "ByRef layout: [NumberNames, MyName[], ret_code]. Pass 0, [] as placeholders.",
    },
    # ── PropFrame ─────────────────────────────────────────────────────────────
    "SapModel.PropFrame.GetNameList": {
        "category": "Properties",
        "description": "Get names of all frame section properties defined in the model",
        "signature": "(NumberNames, MyName) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) names",
        "notes": "ByRef layout: [NumberNames, MyName[], ret_code]. Pass 0, [] as placeholders.",
    },
    # ── PropMaterial ──────────────────────────────────────────────────────────
    "SapModel.PropMaterial.GetNameList": {
        "category": "PropMaterial",
        "description": "Get names of all material properties defined in the model",
        "signature": "(NumberNames, MyName) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) names",
        "notes": "ByRef layout: [NumberNames, MyName[], ret_code]. Pass 0, [] as placeholders.",
    },
    "SapModel.PropMaterial.AddMaterial": {
        "category": "PropMaterial",
        "description": "Add a material from the built-in SAP2000 database",
        "signature": "(Region, Standard, Grade, Name) -> ret_code",
        "parameter_notes": "Region: str — region code (e.g. 'United States'); Standard: str — standard (e.g. 'ASTM'); Grade: str — grade (e.g. 'A992'); Name: str — (ByRef out) assigned name",
        "notes": "ByRef layout: [Name, ret_code]. Pass '' for Name. Use for steel grades from library.",
    },
    "SapModel.PropMaterial.GetTypeOAPI": {
        "category": "PropMaterial",
        "description": "Get the material type (eMatType) for a material property",
        "signature": "(Name, MatType) -> ret_code",
        "parameter_notes": "Name: str — material name; MatType: int — (ByRef out) material type (1=Steel, 2=Concrete, etc.)",
        "notes": "ByRef layout: [MatType, ret_code]. Pass 0 as placeholder.",
    },
    # ── PropLink ──────────────────────────────────────────────────────────────
    "SapModel.PropLink.Count": {
        "category": "Properties",
        "description": "Get the number of link/support properties defined",
        "signature": "() -> count",
        "parameter_notes": "No inputs. Returns integer count directly.",
        "notes": "Returns integer directly (not a list).",
    },
    "SapModel.PropLink.GetLinear": {
        "category": "Properties",
        "description": "Get linear link property parameters",
        "signature": "(Name, DOF, Fixed, Ke, Ce, DJ2, DJ3, Notes, GUID) -> ret_code",
        "parameter_notes": "Name: str — link property name; DOF: bool[6] — (ByRef out) active DOFs; Fixed: bool[6] — (ByRef out); Ke: float[6] — (ByRef out) stiffness; Ce: float[6] — (ByRef out) damping; DJ2/DJ3: float — (ByRef out) distances",
        "notes": "ByRef layout: [DOF[6], Fixed[6], Ke[6], Ce[6], DJ2, DJ3, Notes, GUID, ret_code].",
    },
    # ── LinkObj ───────────────────────────────────────────────────────────────
    "SapModel.LinkObj.Count": {
        "category": "Object_Model",
        "description": "Get the number of link objects in the model",
        "signature": "() -> count",
        "parameter_notes": "No inputs. Returns integer count directly.",
        "notes": "Returns integer directly (not a list).",
    },
    # ── LoadPatterns ──────────────────────────────────────────────────────────
    "SapModel.LoadPatterns.GetNameList": {
        "category": "Load_Patterns",
        "description": "Get names and types of all load patterns defined",
        "signature": "(NumberNames, MyName, MyType) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) names; MyType: int[] — (ByRef out) eLoadPatternType values",
        "notes": "ByRef layout: [NumberNames, MyName[], MyType[], ret_code].",
    },
    "SapModel.LoadPatterns.SetSelfWTMultiplier": {
        "category": "Load_Patterns",
        "description": "Set the self-weight multiplier for a load pattern",
        "signature": "(Name, SelfWTMultiplier) -> ret_code",
        "parameter_notes": "Name: str — load pattern name; SelfWTMultiplier: float — multiplier (1.0=full self weight, 0=none)",
        "notes": "Returns ret_code directly (0=success). Common: DEAD=1.0, LIVE=0.0.",
    },
    # ── LoadCases ─────────────────────────────────────────────────────────────
    "SapModel.LoadCases.GetNameList": {
        "category": "Load_Cases",
        "description": "Get names and types of all load cases defined",
        "signature": "(NumberNames, MyName, MyType) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) case names; MyType: int[] — (ByRef out) case type values",
        "notes": "ByRef layout: [NumberNames, MyName[], MyType[], ret_code].",
    },
    "SapModel.LoadCases.GetTypeOAPI": {
        "category": "Load_Cases",
        "description": "Get the load case type for a named load case",
        "signature": "(Name, CaseType) -> ret_code",
        "parameter_notes": "Name: str — load case name; CaseType: int — (ByRef out) eLoadCaseType value",
        "notes": "ByRef layout: [CaseType, ret_code]. Pass 0 as placeholder.",
    },
    "SapModel.LoadCases.ResponseSpectrum.SetCase": {
        "category": "Load_Cases",
        "description": "Initialize a response spectrum load case",
        "signature": "(Name) -> ret_code",
        "parameter_notes": "Name: str — name of the response spectrum load case to initialize",
        "notes": "Returns ret_code directly (0=success). Creates the RS load case if it does not exist.",
    },
    "SapModel.LoadCases.ResponseSpectrum.GetLoads": {
        "category": "Load_Cases",
        "description": "Get the load components for a response spectrum load case",
        "signature": "(Name, NumberItems, LoadName, Func, SF, CSys, Ang) -> ret_code",
        "parameter_notes": "Name: str — RS case name; NumberItems: int — (ByRef out) count; LoadName: str[] — (ByRef out); Func: str[] — (ByRef out) RS function names; SF: float[] — (ByRef out) scale factors; CSys: str[] — (ByRef out); Ang: float[] — (ByRef out)",
        "notes": "ByRef layout: [NumberItems, LoadName[], Func[], SF[], CSys[], Ang[], ret_code].",
    },
    # ── RespCombo ─────────────────────────────────────────────────────────────
    "SapModel.RespCombo.GetNameList": {
        "category": "RespCombo",
        "description": "Get names of all load combinations defined in the model",
        "signature": "(NumberNames, MyName) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) combination names",
        "notes": "ByRef layout: [NumberNames, MyName[], ret_code]. Pass 0, [] as placeholders.",
    },
    # ── Func ─────────────────────────────────────────────────────────────────
    "SapModel.Func.FuncRS.GetUser": {
        "category": "Functions",
        "description": "Get the user-defined response spectrum function data",
        "signature": "(Name, NumberItems, Period, Value, DampRatio) -> ret_code",
        "parameter_notes": "Name: str — function name; NumberItems: int — (ByRef out) number of data points; Period: float[] — (ByRef out); Value: float[] — (ByRef out) spectral accelerations; DampRatio: float — (ByRef out) damping ratio",
        "notes": "ByRef layout: [NumberItems, Period[], Value[], DampRatio, ret_code].",
    },
    # ── SelectObj ─────────────────────────────────────────────────────────────
    "SapModel.SelectObj.ClearSelection": {
        "category": "Select",
        "description": "Deselect all currently selected objects",
        "signature": "() -> ret_code",
        "parameter_notes": "No inputs. Returns ret_code directly.",
        "notes": "Returns ret_code directly (0=success).",
    },
    "SapModel.SelectObj.GetSelected": {
        "category": "Select",
        "description": "Get all currently selected objects by type and name",
        "signature": "(NumberItems, ObjectType, ObjectName) -> ret_code",
        "parameter_notes": "NumberItems: int — (ByRef out) count; ObjectType: int[] — (ByRef out) object types; ObjectName: str[] — (ByRef out) object names",
        "notes": "ByRef layout: [NumberItems, ObjectType[], ObjectName[], ret_code]. ObjectType: 1=Point, 2=Frame, 3=Cable, 5=Area, 6=Link.",
    },
    # ── ConstraintDef ─────────────────────────────────────────────────────────
    "SapModel.ConstraintDef.GetBody": {
        "category": "Constraints",
        "description": "Get the DOF configuration of a body constraint",
        "signature": "(Name, DOF) -> ret_code",
        "parameter_notes": "Name: str — constraint name; DOF: bool[6] — (ByRef out) active DOFs [UX,UY,UZ,RX,RY,RZ]",
        "notes": "ByRef layout: [DOF[6], ret_code]. Pass [False]*6 as placeholder.",
    },
    "SapModel.ConstraintDef.GetNameList": {
        "category": "Constraints",
        "description": "Get names of all constraints defined in the model",
        "signature": "(NumberNames, MyName) -> ret_code",
        "parameter_notes": "NumberNames: int — (ByRef out) count; MyName: str[] — (ByRef out) constraint names",
        "notes": "ByRef layout: [NumberNames, MyName[], ret_code].",
    },
    # ── GroupDef ──────────────────────────────────────────────────────────────
    "SapModel.GroupDef.GetAssignments": {
        "category": "Groups",
        "description": "Get all objects assigned to a named group",
        "signature": "(Name, NumberItems, ObjectType, ObjectName) -> ret_code",
        "parameter_notes": "Name: str — group name; NumberItems: int — (ByRef out); ObjectType: int[] — (ByRef out) 1=Point, 2=Frame, 5=Area; ObjectName: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberItems, ObjectType[], ObjectName[], ret_code].",
    },
    # ── View ──────────────────────────────────────────────────────────────────
    "SapModel.View.RefreshView": {
        "category": "View",
        "description": "Redraw and refresh the SAP2000 model view",
        "signature": "(Window, Zoom) -> ret_code",
        "parameter_notes": "Window: int — window number (0=all); Zoom: bool — True=zoom to fit",
        "notes": "Returns ret_code directly (0=success). Call after model changes.",
    },
    # ── File ───────────────────────────────────────────────────────────────────
    "SapModel.File.Save": {
        "category": "File",
        "description": "Save the current model to file",
        "signature": "(FileName) -> ret_code",
        "parameter_notes": "FileName: str — full path for save; pass '' to save to existing path",
        "notes": "Returns ret_code directly (0=success). Creates .sdb file. Pass '' to overwrite current file.",
    },
    "SapModel.File.New2DFrame": {
        "category": "File",
        "description": "Create a new 2D frame model from a built-in template",
        "signature": "(TemplateName, NumberStorys, StoryHeight, NumberBays, BayWidth, OverWrite, RestraintType) -> ret_code",
        "parameter_notes": "TemplateName: int — 0=PortalFrame, 1=ConcentricBrace, 2=EccentricBrace; NumberStorys: int; StoryHeight: float; NumberBays: int; BayWidth: float; OverWrite: bool; RestraintType: int — 1=Fixed, 2=Pinned",
        "notes": "Returns ret_code directly. Creates a basic 2D frame directly.",
    },
    # ── Analyze ───────────────────────────────────────────────────────────────
    "SapModel.Analyze.RunAnalysis": {
        "category": "Analyze",
        "description": "Run the structural analysis for all active load cases",
        "signature": "() -> ret_code",
        "parameter_notes": "No inputs. Runs all active load cases.",
        "notes": "Returns ret_code directly (0=success). Locks model after completion.",
    },
    # ── Results.Setup ─────────────────────────────────────────────────────────
    "SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput": {
        "category": "Analysis_Results",
        "description": "Clear all load cases and combinations from the output selection",
        "signature": "() -> ret_code",
        "parameter_notes": "No inputs. Call before selecting specific cases for results output.",
        "notes": "Returns ret_code directly (0=success). Use before SetCaseSelectedForOutput.",
    },
    "SapModel.Results.Setup.SetCaseSelectedForOutput": {
        "category": "Analysis_Results",
        "description": "Select or deselect a load case for results output",
        "signature": "(Name, Selected) -> ret_code",
        "parameter_notes": "Name: str — load case name; Selected: bool — True=select for output",
        "notes": "Returns ret_code directly (0=success).",
    },
    "SapModel.Results.Setup.SetComboSelectedForOutput": {
        "category": "Analysis_Results",
        "description": "Select or deselect a load combination for results output",
        "signature": "(Name, Selected) -> ret_code",
        "parameter_notes": "Name: str — combination name; Selected: bool — True=select for output",
        "notes": "Returns ret_code directly (0=success).",
    },
    # ── Results ───────────────────────────────────────────────────────────────
    "SapModel.Results.JointDispl": {
        "category": "Analysis_Results",
        "description": "Extract joint displacement results (translations and rotations)",
        "signature": "(Name, ItemTypeElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3) -> ret_code",
        "parameter_notes": "Name: str — joint name or 'All'; ItemTypeElm: int — 0=Object, 1=Element; all others are ByRef outputs",
        "notes": "ByRef layout: [NumberResults, Obj[], Elm[], LoadCase[], StepType[], StepNum[], U1[], U2[], U3[], R1[], R2[], R3[], ret_code].",
    },
    "SapModel.Results.FrameForce": {
        "category": "Analysis_Results",
        "description": "Extract frame internal forces (P, V2, V3, T, M2, M3) at stations",
        "signature": "(Name, ItemTypeElm, NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3) -> ret_code",
        "parameter_notes": "Name: str — frame name or 'All'; ItemTypeElm: int — 0=Object; all others are ByRef outputs",
        "notes": "ByRef layout: [NumberResults, Obj[], ObjSta[], Elm[], ElmSta[], LoadCase[], StepType[], StepNum[], P[], V2[], V3[], T[], M2[], M3[], ret_code].",
    },
    "SapModel.Results.JointReact": {
        "category": "Analysis_Results",
        "description": "Extract joint reaction forces at restrained joints",
        "signature": "(Name, ItemTypeElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3) -> ret_code",
        "parameter_notes": "Name: str — joint name or 'All'; ItemTypeElm: int — 0=Object; all others are ByRef outputs",
        "notes": "ByRef layout: [NumberResults, Obj[], Elm[], LoadCase[], StepType[], StepNum[], F1[], F2[], F3[], M1[], M2[], M3[], ret_code].",
    },
    # ── PropLink ──────────────────────────────────────────────────────────────
    "SapModel.PropLink.SetGap": {
        "category": "Properties",
        "description": "Define a gap (compression-only) link property",
        "signature": "(Name, DOF, Fixed, Ke, Nonlinear, GapOpens, Opens, Notes, GUID) -> ret_code",
        "parameter_notes": "Name: str — link property name; DOF: bool[6] — active DOFs; Fixed: bool[6] — fixed DOFs; Ke: float[6] — stiffness; Nonlinear: bool[6] — nonlinear flags; GapOpens: float[6] — initial gap; Opens: bool[6] — compression vs tension opens",
        "notes": "Returns ret_code directly (0=success).",
    },
    # ── FrameObj.SetInsertionPoint_1 (wrapper name differs) ──────────────────
    "SapModel.FrameObj.SetInsertionPoint_1": {
        "category": "Object_Model",
        "description": "Assign cardinal point and joint offsets to frame objects",
        "signature": "(Name, CardinalPoint, Mirror2, Mirror3, StiffTransform, Offset1, Offset2, CSys, ItemType) -> ret_code",
        "parameter_notes": "Name: str — frame name; CardinalPoint: int — 1-9=corners 10=Centroid 11=ShearCenter; Mirror2/Mirror3: bool; StiffTransform: bool; Offset1/Offset2: float[3] — I/J end offsets in CSys; ItemType: int — 0=Object",
        "notes": "Returns [Offset1[], Offset2[], ret_code] — extract raw[-1] for ret_code.",
    },
    # ── DatabaseTables Display Selection (20 Get/Set pairs) ───────────────────
    "SapModel.DatabaseTables.GetLoadCasesSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get load cases currently selected for table display output",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out) count; NameList: str[] — (ByRef out) selected case names",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set load cases to select for table display output",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[] — load case names to select",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetLoadCombinationsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get load combinations currently selected for table display output",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out); NameList: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set load combinations to select for table display output",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[]",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetLoadPatternsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get load patterns currently selected for table display output",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out); NameList: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set load patterns to select for table display output",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[]",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get element virtual work named sets selected for display",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out); NameList: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set element virtual work named sets selected for display",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[]",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get generalized displacements selected for display",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out); NameList: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set generalized displacements selected for display",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[]",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get joint response spectra named sets selected for display",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out); NameList: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set joint response spectra named sets selected for display",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[]",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get plot function traces named sets selected for display",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out); NameList: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set plot function traces named sets selected for display",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[]",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetPushoverNamedSetsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get pushover named sets selected for display",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out); NameList: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetPushoverNamedSetsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set pushover named sets selected for display",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[]",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetSectionCutsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Get section cuts selected for display",
        "signature": "(NumberSelected, NameList) -> ret_code",
        "parameter_notes": "NumberSelected: int — (ByRef out); NameList: str[] — (ByRef out)",
        "notes": "ByRef layout: [NumberSelected, NameList[], ret_code].",
    },
    "SapModel.DatabaseTables.SetSectionCutsSelectedForDisplay": {
        "category": "Database_Tables",
        "description": "Set section cuts selected for display",
        "signature": "(NumberItems, NameList) -> ret_code",
        "parameter_notes": "NumberItems: int; NameList: str[]",
        "notes": "Returns ret_code via raw[-1] — use isinstance check.",
    },
    "SapModel.DatabaseTables.GetTableOutputOptionsForDisplay": {
        "category": "Database_Tables",
        "description": "Get the 18 table output display options",
        "signature": "(SortTableData, SortConnectyData, ModeShapeOpt, ModeShapeRef, TableGroupOpt, TableGroupSingle, TwoDFloat, TwoDFloatFig, TwoDInt, FourDFloat, FourDFloatFig, FourDInt, EightDFloat, EightDFloatFig, EightDInt, TwelveDFloat, TwelveDFloatFig, TwelveDInt) -> ret_code",
        "parameter_notes": "All 18 parameters are ByRef outputs — pass 0/False placeholders",
        "notes": "18 ByRef output params. Returns tuple with all option values + ret_code last.",
    },
    "SapModel.DatabaseTables.SetTableOutputOptionsForDisplay": {
        "category": "Database_Tables",
        "description": "Set the 18 table output display options",
        "signature": "(SortTableData, SortConnectyData, ModeShapeOpt, ModeShapeRef, TableGroupOpt, TableGroupSingle, TwoDFloat, TwoDFloatFig, TwoDInt, FourDFloat, FourDFloatFig, FourDInt, EightDFloat, EightDFloatFig, EightDInt, TwelveDFloat, TwelveDFloatFig, TwelveDInt) -> ret_code",
        "parameter_notes": "SortTableData: bool; SortConnectyData: bool; ModeShapeOpt: int; ModeShapeRef: int; TableGroupOpt: int; TableGroupSingle: bool; plus 12 numeric format specifiers",
        "notes": "Returns int or (int,) — use: ret if isinstance(ret, int) else ret[-1].",
    },
}

# ── Signature extractor from wrapper docstrings ──────────────────────────────

# Matches both "API Signature:" and "API Signature (VBA):"
_SIG_HEADER_RE = re.compile(r"API Signature\s*(?:\([^)]*\))?\s*:\s*\n", re.IGNORECASE)


def extract_sig_from_wrapper(wrapper_path: Path) -> str:
    """Extract signature from wrapper docstring after 'API Signature:' header.

    Handles:
      - Single-line:  SapModel.X.Y(a, b) -> ret_code
      - Multi-line:   SapModel.X.Y(a, b,\n      c, d) -> ret_code
      - VBA format:   API Signature (VBA): SapModel.X.Y(a, b(), c())
    """
    text = wrapper_path.read_text(encoding="utf-8", errors="ignore")
    m = _SIG_HEADER_RE.search(text)
    if not m:
        return ""

    # Collect lines after the header until a blank line or "ByRef"
    rest = text[m.end():]
    lines = rest.splitlines()
    collected = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("ByRef") or stripped.startswith("Parameters"):
            break
        collected.append(stripped)

    full = " ".join(collected)

    # Strip "SapModel.X.Y" prefix → keep only "(params...)"
    paren = full.find("(")
    if paren < 0:
        return ""

    raw_sig = full[paren:]

    # Normalize VBA array notation "TableKey()" → "TableKey[]"
    raw_sig = re.sub(r"\(\)", "[]", raw_sig)
    # Collapse extra whitespace
    raw_sig = re.sub(r"\s+", " ", raw_sig).strip()
    return raw_sig


def func_path_to_wrapper_name(func_path: str) -> str:
    """Convert 'SapModel.FrameObj.AddByCoord' → 'func_FrameObj_AddByCoord'."""
    parts = func_path.split(".")
    if parts[0] == "SapModel":
        parts = parts[1:]
    return "func_" + "_".join(parts)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not REGISTRY_PATH.exists():
        print(f"ERROR: Registry not found at {REGISTRY_PATH}")
        return

    with open(REGISTRY_PATH, encoding="utf-8") as f:
        registry = json.load(f)

    funcs = registry["functions"]
    updated = []
    skipped_no_data = []

    for func_path, entry in funcs.items():
        if entry.get("signature", ""):
            continue  # Already has signature — skip

        new_data = {}

        # 1. Check hardcoded data first
        if func_path in HARDCODED:
            hc = HARDCODED[func_path]
            new_data["signature"] = hc.get("signature", "")
            if hc.get("description") and not entry.get("description", ""):
                new_data["description"] = hc["description"]
            if hc.get("category") and not entry.get("category", ""):
                new_data["category"] = hc["category"]
            if hc.get("notes") and not entry.get("notes", ""):
                new_data["notes"] = hc["notes"]
            if hc.get("parameter_notes") and not entry.get("parameter_notes", ""):
                new_data["parameter_notes"] = hc["parameter_notes"]

        # 2. Try to extract from wrapper file
        if not new_data.get("signature"):
            wrapper_name = func_path_to_wrapper_name(func_path)
            wrapper_file = WRAPPERS_PATH / (wrapper_name + ".py")
            if wrapper_file.exists():
                sig = extract_sig_from_wrapper(wrapper_file)
                if sig:
                    new_data["signature"] = sig

        # 3. Apply updates if we found something
        if new_data.get("signature"):
            for key, val in new_data.items():
                entry[key] = val
            updated.append(func_path)
        else:
            skipped_no_data.append(func_path)

    # Save
    mode = "DRY RUN -- no changes written" if DRY_RUN else "SAVED"
    print(f"\n{'='*60}")
    print(f"Batch Register Signatures -- {mode}")
    print(f"{'='*60}")
    print(f"Total funciones en registry: {len(funcs)}")
    print(f"Actualizadas con signature:  {len(updated)}")
    print(f"Sin datos suficientes:       {len(skipped_no_data)}")

    if updated:
        print("\nActualizadas:")
        for fp in updated:
            sig = funcs[fp].get("signature", "")
            print(f"  + {fp}  ->  {sig}")

    if skipped_no_data:
        print("\nSin datos suficientes (registro manual requerido):")
        for fp in skipped_no_data:
            print(f"  - {fp}")

    if not DRY_RUN:
        # Update summary
        registry["summary"] = {
            "total_registered": len(funcs),
            "total_verified": sum(1 for f in funcs.values() if f.get("verified")),
        }
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False, default=str)
        print(f"\nRegistry guardado en {REGISTRY_PATH}")
    else:
        print("\n(Dry run — ejecutar sin --dry-run para aplicar cambios)")


if __name__ == "__main__":
    main()
