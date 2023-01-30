from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.InterfaceObject import InterfaceObject

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
        InterfaceController._create_JSON_file()

    @staticmethod
    def _encoding_tool_caller():
        print("encoding_tool_caller: looking for encoding")

    @staticmethod
    def _create_JSON_file():
        # the point of this method is to generate a JSON file that contains information that other tools should be
        # able to understand and base their instructions on
        # that means that an external tool must be able to understand a specific JSON structure and imlpement that
        # to be able to call the right functions?

        interfaceObject = InterfaceObject("main")
        jsonObject = interfaceObject.toJson()

        print(jsonObject)

        #print(f"JSON string from object: {jsonObject}")

