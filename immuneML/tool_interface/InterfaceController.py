import psutil

from immuneML.tool_interface.ToolTable import ToolTable
from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.interface_components.MLToolComponent import MLToolComponent
from immuneML.tool_interface.interface_components.PreprocessingComponent import PreprocessingComponent

toolTable = ToolTable()


class InterfaceController:

    @staticmethod
    def get_tool_path(name: str):
        """ Returns the tool path defined in the YAML specification file
        """
        return toolTable.get(name).tool_path

    @staticmethod
    def create_component(tool_type: ToolType, name: str, specs: dict):
        """ Creates a component depending on tool type specified, and adds it to the ToolTable
        """
        if tool_type == ToolType.ML_TOOL:
            new_component = MLToolComponent(name, specs)
            toolTable.add(name, new_component)
        elif tool_type == ToolType.PREPROCESSOR_TOOL:
            new_component = PreprocessingComponent(name, specs)
            toolTable.add(name, new_component)

    @staticmethod
    def run_func(name: str, func: str, params=None):
        # Get tool from toolTable
        tool = toolTable.get(name)

        # Check if tool is running. If not, start subprocess and open connection
        if not InterfaceController.check_running(name):
            tool.start_subprocess()
            tool.open_connection()

        # Run function in tool component
        if not params:
            result = getattr(tool, func)()
        else:
            result = getattr(tool, func)(params)

        return result

    @staticmethod
    def check_running(name: str) -> bool:
        # Check if component has process running

        # Get tool from toolTable
        tool = toolTable.get(name)

        if tool.process is not None:
            if psutil.pid_exists(tool.process.pid):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def stop_tool(name: str):
        tool = toolTable.get(name)
        tool.close_connection()
        tool.stop_subprocess()

    @staticmethod
    def stop_all_tools():
        for tool in toolTable.items:
            InterfaceController.stop_tool(tool)
