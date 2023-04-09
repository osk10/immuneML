import psutil

from immuneML.tool_interface.ToolTable import ToolTable
from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.interface_components.DatasetToolComponent import DatasetToolComponent
from immuneML.tool_interface.interface_components.MLToolComponent import MLToolComponent
from immuneML.tool_interface.interface_components.PreprocessingComponent import PreprocessingComponent

toolTable = ToolTable()


def get_tool_path(name: str):
    """ Returns the tool path defined in the YAML specification file
    """
    return toolTable.get(name).tool_path


def create_component(tool_type: ToolType, name: str, specs: dict):
    if tool_type == ToolType.ML_TOOL:
        new_component = MLToolComponent(name, specs)
        toolTable.add(name, new_component)
    elif tool_type == ToolType.DATASET_TOOL:
        new_component = DatasetToolComponent(name, specs)
        toolTable.add(name, new_component)
    elif tool_type == ToolType.PREPROCESSING_TOOL:
        new_component = PreprocessingComponent(name, specs)
        toolTable.add(name, new_component)


def run_func(name: str, func: str, params=None):
    # Get tool from toolTable
    tool = toolTable.get(name)

    # Check if tool is running. If not, start subprocess and open connection
    if not check_running(name):
        tool.start_subprocess()
        tool.open_connection()

    # Run function in tool component
    if not params:
        result = getattr(tool, func)()
    else:
        result = getattr(tool, func)(params)

    return result


def check_running(name: str) -> bool:
    # Check if component has process running

    # Get tool from toolTable
    tool = toolTable.get(name)

    if tool.process is not None:
        if psutil.pid_exists(tool.process.pid):
            print("Process is running")
            return True
        else:
            print("Process stopped...")
            return False
    else:
        return False


def stop_tool(name: str):
    tool = toolTable.get(name)
    tool.close_connection()
    tool.stop_subprocess()
