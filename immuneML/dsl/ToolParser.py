from pathlib import Path

from immuneML.dsl.symbol_table.SymbolTable import SymbolTable
from immuneML.dsl.symbol_table.SymbolType import SymbolType
from immuneML.tool_interface import InterfaceController
from immuneML.tool_interface.ToolType import ToolType
from immuneML.util.ParameterValidator import ParameterValidator


class ToolParser:
    keyword = "tools"

    @staticmethod
    def parse(specification, symbol_table):
        # loop keys in tool section of YAML-file. Key is user defined name of tool
        # parse tool specification and add to symbol_table
        if ToolParser.keyword in specification:
            for key in specification[ToolParser.keyword]:
                symbol_table = ToolParser._parse_tool(key, specification[ToolParser.keyword][key], symbol_table)
        else:
            specification[ToolParser.keyword] = {}

        return symbol_table, specification

    @staticmethod
    def _parse_tool(key: str, tool_item: dict, symbol_table: SymbolTable):
        # check that all keys are valid
        ParameterValidator.assert_all_in_valid_list(list(tool_item.keys()), ["type", "path", "params"],
                                                    ToolParser.__name__, key)

        # check that all required parameters are present
        ParameterValidator.assert_keys_present(list(tool_item.keys()), ["type", "path"], ToolParser.__name__,
                                               key)

        # change from string to Path
        tool_item["path"] = Path(tool_item["path"])
        ParameterValidator.assert_type_and_value(tool_item["path"], Path, ToolParser.__name__, "path")

        # check that the value of type is valid
        valid_types = ["MLMethodTool", "PreprocessorTool"]
        ParameterValidator.assert_in_valid_list(tool_item["type"], valid_types, "ToolParser", "type")
        tool_specification = {**tool_item}

        ToolParser.create_component_instance(tool_specification, key)

        symbol_table.add(key, SymbolType.TOOL, tool_specification)

        return symbol_table

    @staticmethod
    def get_tool_type(tool_specifications: dict) -> ToolType:
        """ Returns the type of tool
        """
        type_str = tool_specifications['type']

        if type_str == "MLMethodTool":
            return ToolType.ML_TOOL
        elif type_str == "PreprocessorTool":
            return ToolType.PREPROCESSOR_TOOL
        else:
            raise KeyError("Could not identify tool type. YAML file requires 'type' to be defined")

    @staticmethod
    def create_component_instance(tool_specifications: dict, name: str):
        tool_type = ToolParser.get_tool_type(tool_specifications)
        InterfaceController.create_component(tool_type, name, tool_specifications)
