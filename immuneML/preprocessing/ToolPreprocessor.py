import os.path
import shutil
from abc import ABC
from pathlib import Path

from immuneML.IO.dataset_export.AIRRExporter import AIRRExporter
from immuneML.preprocessing.Preprocessor import Preprocessor
from immuneML.tool_interface import InterfaceController
from immuneML.util.PathBuilder import PathBuilder


class ToolPreprocessor(Preprocessor, ABC):
    """This preprocessor runs an external preprocessor

    YAML specification:

    .. indent with spaces
    .. code-block:: yaml

        preprocessing_sequences:
            my_preprocessing:
                - my_filter:
                    ToolPreprocessor:
                        tool_name: my_preprocessing_tool
    """

    def __init__(self, tool_name: str, result_path: Path = None):
        super().__init__(result_path)
        self.tool_name = tool_name

    def process_dataset(self, dataset, result_path):
        """ Prepares parameters and calls process(dataset, params) internally
        """

        params = {"result_path": result_path, "tool_name": self.tool_name}
        return ToolPreprocessor.process(dataset, params)

    @staticmethod
    def process(dataset, params: dict):
        """ Takes a dataset and returns a new (modified) dataset.
        """
        processed_dataset = dataset.clone()

        # Export the dataset to the folder on which the tool script is located
        tool_script_path = InterfaceController.get_tool_path(params["tool_name"])
        path = os.path.dirname(tool_script_path)
        path = PathBuilder.build(path)
        AIRRExporter.export(dataset, path)

        # Start the tool handling the dataset. Returns a path to the dataset
        result = InterfaceController.run_func(params["tool_name"], "run_preprocessing",
                                              "batch1.tsv")  # batch1.tsv is a default name

        # Insert the dataset into a folder located inside immuneML that can be further used - only used for showing the results
        ToolPreprocessor.insert_dataset_to_immuneML(result)

        # TODO: the original dataset is returned. Should be the preprocessed dataset

        return processed_dataset

    def check_dataset_type(self, dataset, valid_dataset_types: list, location: str):
        assert type(
            dataset) in valid_dataset_types, f"{location}: this preprocessing can only be applied to datasets of type: " \
                                             f"{', '.join([dataset_type.__name__ for dataset_type in valid_dataset_types])}. " \
                                             f"Your dataset is a {type(dataset).__name__}. " \
                                             f"Please use a different preprocessing, or omit the preprocessing for this dataset."

    def keeps_example_count(self) -> bool:
        """
        Defines if the preprocessing can be run with TrainMLModel instruction; to be able to run with it, the preprocessing cannot change the
        number of examples in the dataset
        """
        return True

    @staticmethod
    def insert_dataset_to_immuneML(file_path):
        """ Receives a file path, creates a copy of the file and inserts it into generated_datasets folder
        """
        destination_folder = "../tool_interface/generated_datasets/"

        shutil.copy(file_path, destination_folder)
