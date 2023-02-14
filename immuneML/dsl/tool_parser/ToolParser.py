from immuneML.tool_interface.InterfaceController import InterfaceController
from immuneML.tool_interface.ToolType import ToolType


class ToolParser:

    @staticmethod
    def parse(workflow_specification: dict):
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
            print("No tool found while parsing tool(s)")

    @staticmethod
    def execute_tool(specs: dict, tool_type: ToolType):
        print(f"execute_tool specs={specs}")

        if "tool_path" and "tool_executable" in specs:
            InterfaceController.interface_controller(tool_type, specs)
        else:
            raise KeyError("tool_path must be specified in yaml file specification")

