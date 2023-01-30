from ToolType import ToolType


class InterfaceController:

    @staticmethod
    def interface_controller(tool_type):
        if tool_type == ToolType.ML_TOOL:
            InterfaceController._ml_tool_caller()
        elif tool_type == ToolType.ENCODING_TOOL:
            InterfaceController._encoding_tool_caller()
        else:
            print(f"Invalid argument: {tool_type}")

    @staticmethod
    def _ml_tool_caller():
        print("ml_tool_caller: looking for ml_method")

    @staticmethod
    def _encoding_tool_caller():
        print("encoding_tool_caller: looking for encoding")
