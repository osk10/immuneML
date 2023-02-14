from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.InterfaceObject import InterfaceObject
from immuneML.tool_interface.InterfaceDatasetTool import InterfaceDatasetTool
import subprocess


class InterfaceController:

    @staticmethod
    def interface_controller(tool_type: ToolType, ml_specs: dict):
        print(f"interface_controller specs received: {ml_specs}")
        if tool_type == ToolType.ML_TOOL:
            print("Found ML_TOOL, but skipping program execution")
            # InterfaceController._ml_tool_caller(ml_specs)
        elif tool_type == ToolType.DATASET_TOOL:
            print("Found DATASET_TOOL. Running interface")
            InterfaceDatasetTool.instruction_handler(ml_specs)
        else:
            print(f"Invalid argument: {tool_type}. No such tool exists")

    @staticmethod
    def _ml_tool_caller(ml_specs: dict):
        print("ml_tool_caller: looking for ml_method")
        InterfaceController._start_subprocess(ml_specs)

    @staticmethod
    def _start_subprocess(ml_specs: dict):
        #  Define and run subprocess (external tool)

        program = ml_specs.get("tool_path") + "/" + ml_specs.get("tool_execution_file")
        json_data_example = InterfaceController._create_JSON_data()
        proc = subprocess.Popen([program],
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
