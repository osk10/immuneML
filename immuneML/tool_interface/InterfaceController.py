from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.InterfaceObject import InterfaceObject
from immuneML.tool_interface.InterfaceComponents.DatasetToolComponent import DatasetToolComponent
from immuneML.tool_interface.InterfaceComponents.MLToolComponent import MLToolComponent
import subprocess


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
