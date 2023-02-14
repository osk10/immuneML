from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.InterfaceObject import InterfaceObject
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
        #  Define and run subprocess (external tool)
        file = ml_specs.get("tool_path") + "/" + ml_specs.get("tool_execution_file")
        json_data_example = InterfaceController._create_JSON_data()
        proc = subprocess.Popen(["python", file, json_data_example],
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE)

        #  Printing the output that the tool gives while running on its own side
        output_list = proc.communicate()[0].decode('UTF-8')
        print("\n--------Summary of tool output--------")
        print(output_list)

    @staticmethod
    def _create_JSON_data():
        # the point of this method is to generate a JSON file that contains information that other tools should be
        # able to understand and base their instructions on
        # that means that an external tool must be able to understand a specific JSON structure and implement that
        # to be able to call the right functions?

        interface_object = InterfaceObject("main")
        json_object = interface_object.getJson()
        return json_object
