import hashlib
from pathlib import Path

from immuneML.dsl.instruction_parsers.LabelHelper import LabelHelper
from immuneML.dsl.symbol_table.SymbolTable import SymbolTable
from immuneML.dsl.symbol_table.SymbolType import SymbolType
from immuneML.environment.EnvironmentSettings import EnvironmentSettings
from immuneML.hyperparameter_optimization.HPSetting import HPSetting
from immuneML.util.ParameterValidator import ParameterValidator
from immuneML.workflows.instructions.MLToolInstruction import MLToolInstruction


class MLToolParser:
    """
    Specification example for the MLTool instruction:

    .. highlight:: yaml
    .. code-block:: yaml

        instruction_name:
            type: MLToolParser
            dataset: d1
            label: CD

    """

    def parse(self, key: str, instruction: dict, symbol_table: SymbolTable, path: Path) -> MLToolInstruction:
        location = MLToolParser.__name__
        ParameterValidator.assert_keys(instruction.keys(), ['type', 'dataset', 'labels', 'settings'],
                                       location, key)
        ParameterValidator.assert_in_valid_list(instruction['dataset'],
                                                symbol_table.get_keys_by_type(SymbolType.DATASET), location,
                                                f"{key}: dataset")

        dataset = symbol_table.get(instruction["dataset"])
        label_config = LabelHelper.create_label_config(instruction["labels"], dataset, location, key)
        path = self._prepare_path(instruction)
        settings = self._parse_settings(instruction, symbol_table)

        instruction = MLToolInstruction(dataset=symbol_table.get(instruction['dataset']),
                                        label_configuration=label_config, path=path, name=key, hp_setting=settings[0])

        return instruction

    def _prepare_path(self, instruction: dict) -> Path:
        if "path" in instruction:
            path = Path(instruction["path"]).absolute()
        else:
            path = EnvironmentSettings.default_analysis_path / hashlib.md5(str(instruction).encode()).hexdigest()

        return path

    def _parse_settings(self, instruction: dict, symbol_table: SymbolTable) -> list:
        try:
            settings = []
            for index, setting in enumerate(instruction["settings"]):
                ParameterValidator.assert_keys(setting.keys(), ["ml_method", "encoding"], MLToolParser.__name__,
                                               f"settings, {index + 1}. entry")

                encoder = symbol_table.get(setting["encoding"]).build_object(symbol_table.get(instruction["dataset"]),
                                                                             **symbol_table.get_config(
                                                                                 setting["encoding"])["encoder_params"]) \
                    .set_context({"dataset": symbol_table.get(instruction['dataset'])})

                # ml_method = symbol_table.get(setting["ml_method"])
                # ml_method.check_encoder_compatibility(encoder)

                s = HPSetting(encoder=encoder,
                              encoder_name=setting["encoding"],
                              encoder_params=symbol_table.get_config(setting["encoding"])["encoder_params"],
                              ml_method=None,
                              ml_method_name=setting["ml_method"],
                              ml_params={},
                              preproc_sequence=[], preproc_sequence_name=None)

                settings.append(s)
            return settings
        except KeyError as key_error:
            raise KeyError(
                f"{MLToolParser.__name__}: parameter {key_error.args[0]} was not defined under settings in MLToolParser instruction.")
