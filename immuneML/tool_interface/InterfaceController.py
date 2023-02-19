from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.InterfaceComponents.DatasetToolComponent import DatasetToolComponent
from immuneML.tool_interface.InterfaceComponents.MLToolComponent import MLToolComponent


class InterfaceController:

    @staticmethod
    def interface_controller(tool_type: ToolType, specs: dict):
        print(f"interface_controller specs received: {specs}")
        if tool_type == ToolType.ML_TOOL:
            MLToolComponent.instruction_handler(specs)
        elif tool_type == ToolType.DATASET_TOOL:
            DatasetToolComponent.instruction_handler(specs)
        else:
            print(f"Invalid argument: {tool_type}. No such tool exists")
