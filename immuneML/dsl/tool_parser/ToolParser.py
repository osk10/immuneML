from immuneML.tool_interface.InterfaceController import InterfaceController
from immuneML.tool_interface.ToolType import ToolType


class ToolParser:

    @staticmethod
    def parse(workflow_specification: dict):
        specs = workflow_specification["tools"]

        if "ml_tool" in specs:
            ml_specs  = specs.get("ml_tool")
            ToolParser.execute_tool(ml_specs)

    @staticmethod
    def execute_tool(ml_specs: dict):
        print(f"execute_tool ml_specs={ml_specs}")
        tool_path = None

        if "tool_path" in ml_specs:
            tool_path = ml_specs.get("tool_path")
            print(f"tool_path: {tool_path}")
            InterfaceController.interface_controller(ToolType.ML_TOOL)
        else:
            raise KeyError("tool_path must be specified in yaml file specification")

