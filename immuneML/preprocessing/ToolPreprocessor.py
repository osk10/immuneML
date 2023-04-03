from abc import ABC
from pathlib import Path
import pandas as pd
import os

from immuneML.IO.dataset_export.AIRRExporter import AIRRExporter

from immuneML.preprocessing.Preprocessor import Preprocessor
from immuneML.tool_interface import InterfaceController


class ToolPreprocessor(Preprocessor, ABC):
    """This preprocessor runs an external preprocessor

    YAML specification:

    # TODO: do changes here!!
    .. indent with spaces
    .. code-block:: yaml

        preprocessing_sequences:
            my_preprocessing:
                - my_filter:
                    NewClonesPerRepertoireFilter:
                        lower_limit: 100
                        upper_limit: 100000
    """

    def __init__(self, tool_name: str, result_path: Path = None):
        super().__init__(result_path)
        self.tool_name = tool_name

    def process_dataset(self, dataset, result_path):
        """ Prepares parameters and calls process(dataset, params) internally
        """
        print("Running PreprocessingTool process_dataset()")

        params = {"result_path": result_path, "tool_name": self.tool_name}
        print(f"Params to tool: {params}")
        return ToolPreprocessor.process(dataset, params)





    @staticmethod
    def process(dataset, params: dict):
        """ Takes a dataset and returns a new (modified) dataset.
        """
        # Todo: IMPORTANT: this example generally gives an example where we are sending a SequenceDataset. We need to adapt this

        print("Running PreprocessingTool process()")
        # clone dataset
        processed_dataset = dataset.clone()
        print("Dataset type: ", type(processed_dataset))
        processed_dataset_path = processed_dataset.get_filenames()[0].resolve()
        print(f"filenames: {processed_dataset_path}")

        # TODO: try export them, then import it back???
        test_folder = processed_dataset.get_filenames()[0] / "exported"

        # FIRST: export the dataset to AIRR (.tsv) format that the external tool can handle
        #AIRRExporter.export(dataset, test_folder)

        # Run the interface 
        InterfaceController.run_func(params["tool_name"], "run_preprocessing", processed_dataset)

        # SECOND: import the dataset from AIRR (.tsv) format that the external tool has created

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
