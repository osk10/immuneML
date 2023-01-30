from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.InterfaceObject import InterfaceObject
from pathlib import Path
import subprocess

class InterfaceController:

    @staticmethod
    def interface_controller(tool_type: ToolType, ml_specs: dict):
        print(f"interface_controller specs received: {ml_specs}")
        if tool_type == ToolType.ML_TOOL:
            InterfaceController._ml_tool_caller(ml_specs)
        else:
            print(f"Invalid argument: {tool_type}")

    @staticmethod
    def _ml_tool_caller(ml_specs: dict):
        print("ml_tool_caller: looking for ml_method")
        InterfaceController._start_subprocess(ml_specs)

    @staticmethod
    def _start_subprocess(ml_specs: dict):
        tool_path = Path(ml_specs.get("tool_path"))
        print(f"_start_subprocess tool path: {tool_path}")

        try:
            file = ml_specs.get("tool_path") + "/" + ml_specs.get("tool_execution_file")
            result = subprocess.run(["python", file], capture_output=True)
            print(f"Result from running subprocess: {result}")
        except PermissionError as e:
            print(e)
            print("Make sure to give right permissions to file")
            return

    @staticmethod
    def _create_JSON_file():
        # the point of this method is to generate a JSON file that contains information that other tools should be
        # able to understand and base their instructions on
        # that means that an external tool must be able to understand a specific JSON structure and imlpement that
        # to be able to call the right functions?

        interfaceObject = InterfaceObject("main")
        jsonObject = interfaceObject.toJson()
        print(jsonObject)

