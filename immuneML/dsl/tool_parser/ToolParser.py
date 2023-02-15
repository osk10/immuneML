from immuneML.tool_interface.InterfaceController import InterfaceController
from immuneML.tool_interface.ToolType import ToolType


class ToolParser:

    valid_tool_definitions = {
        "ml_tool": [
            "tool_path",
            "tool_executable"
        ],
        "dataset_tool": [
            "tool_path",
            "tool_executable"
        ]
    }

    @staticmethod
    def parse(workflow_specification: dict):
        # First thing that should be done is to check if the parser gets valid data

        if not ToolParser.check_if_valid_tool_definition(workflow_specification):
            print(f"Invalid YAML file. Requirements: {ToolParser.valid_tool_definitions}")
            return
        else:
            specs = workflow_specification["tools"]

        print(f"\nToolparser got specs: {specs}\n")

        if "ml_tool" in specs:
            ml_specs = specs.get("ml_tool")
            ToolParser.execute_tool(ml_specs, ToolType.ML_TOOL)
        if "dataset_tool" in specs:
            print("TOOL PARSER FOUND DATASET TOOL")
            dataset_specs = specs.get("dataset_tool")
            ToolParser.execute_tool(dataset_specs, ToolType.DATASET_TOOL)
        else:
            print("Invalid yaml specification file?")

    @staticmethod
    def check_if_valid_tool_definition(workflow_specification: dict):
        # TODO: implement function
        return True

    @staticmethod
    def execute_tool(specs: dict, tool_type: ToolType):
        print(f"execute_tool specs={specs}")

        if "tool_path" and "tool_executable" in specs:
            InterfaceController.interface_controller(tool_type, specs)
        else:
            raise KeyError("tool_path must be specified in yaml file specification")

