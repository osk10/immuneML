import os
import pickle
from dataclasses import dataclass
from pathlib import Path

from immuneML.data_model.dataset.Dataset import Dataset
from immuneML.dsl.ToolControllerML import ToolControllerML
from immuneML.environment.LabelConfiguration import LabelConfiguration
from immuneML.hyperparameter_optimization.HPSetting import HPSetting
from immuneML.hyperparameter_optimization.core.HPUtil import HPUtil
from immuneML.workflows.instructions.Instruction import Instruction


@dataclass
class MLToolState:
    dataset: Dataset
    label_configuration: LabelConfiguration
    hp_setting: HPSetting
    name: str = None
    path: Path = None


class MLToolInstruction(Instruction):

    def __init__(self, dataset, label_configuration: LabelConfiguration, hp_setting: HPSetting, path: Path = None,
                 name: str = None):
        self.state = MLToolState(dataset, label_configuration, hp_setting, name, path)

    def run(self, result_path: Path):
        self.state.path = result_path
        absolute_path = os.path.abspath(result_path)

        # encode data
        encoded_data = HPUtil.encode_dataset(self.state.dataset, self.state.hp_setting,
                                             self.state.path / "encoded_datasets",
                                             learn_model=True,
                                             context={}, number_of_processes=1,
                                             label_configuration=self.state.label_configuration)

        # start subprocess
        tool = ToolControllerML(
            tool_path="/Users/oskar/Documents/Skole/Master/immuneml_forked/ML_tool/PytorchTabular_tool2.py")
        tool.start_subprocess()

        # open communication
        tool.open_connection()

        # start training
        encoded_data_pickle = pickle.dumps(encoded_data.encoded_data)
        tool.run_entire_process(encoded_data_pickle, absolute_path,
                                self.state.label_configuration.get_labels_by_name()[0])

        tool.stop_subprocess()

        return self.state
