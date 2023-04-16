import os.path
import shutil
from pathlib import Path

from immuneML.IO.dataset_export.AIRRExporter import AIRRExporter
from immuneML.IO.dataset_import.GenericImport import GenericImport
from immuneML.preprocessing.Preprocessor import Preprocessor
from immuneML.tool_interface import InterfaceController
from immuneML.util.PathBuilder import PathBuilder


class PreprocessorTool(Preprocessor):
    """This preprocessor runs an external preprocessor

    YAML specification:

    .. indent with spaces
    .. code-block:: yaml

        preprocessing_sequences:
            my_preprocessing:
                - my_filter: PreprocessorTool
    """

    def __init__(self, name: str, result_path: Path = None):
        super().__init__(result_path)
        self.name = name

    def process_dataset(self, dataset, result_path):
        """ Prepares parameters and calls process(dataset, params) internally
        """

        params = {"result_path": result_path, "tool_name": self.name}
        return PreprocessorTool.process(dataset, params)

    @staticmethod
    def process(dataset, params: dict):
        """ Takes a dataset and returns a new (modified) dataset.
        """
        processed_dataset = dataset.clone()

        # Export the dataset to the folder on which the tool script is located
        # TODO: Alternatively a path to the dataset could have been sent as a parameter to the tool
        tool_script_path = InterfaceController.get_tool_path(params["tool_name"])
        path = os.path.dirname(tool_script_path)
        path = PathBuilder.build(path)
        AIRRExporter.export(processed_dataset, path)

        # Start the tool handling the dataset. Returns a path to the dataset
        # batch1.tsv is default name of exported file
        result_path = InterfaceController.run_func(params["tool_name"], "run_preprocessing", "batch1.tsv")

        processed_dataset = PreprocessorTool.run_generic_import(result_path, params["result_path"])
        # Insert the dataset into a folder located inside immuneML to show the results of the preprocessing directly
        PreprocessorTool.insert_dataset_to_immuneML(result_path)

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
    def run_generic_import(path, result_path):
        """ Used for testing the import of the externally preprocessed dataset
        TODO: this import will not include all the sections of the originally exported dataset. Neither will it
            include new columns added. This is because there is no mapping implemented to certain columns
        """

        column_mapping = {
            "sequence_id": "sequence_identifiers",
            "v_call": "v_alleles",
            "j_call": "j_alleles",
            "duplicate_count": "counts",
            "cdr3_aa": "sequence_aas",
        }

        # Generic import used as AIRR import gives errors
        dataset = GenericImport.import_dataset({"is_repertoire": False, "paired": False,
                                                "result_path": result_path, "path": path,
                                                "import_illegal_characters": False,
                                                "region_type": "FULL_SEQUENCE", "separator": "\t",
                                                "import_empty_nt_sequences": True,
                                                "column_mapping": column_mapping, "number_of_processes": 4},
                                               "generic_dataset")
        return dataset

    @staticmethod
    def insert_dataset_to_immuneML(file_path):
        """ Receives a file path, creates a copy of the file and inserts it into external_preprocessed_dataset folder
        This function is only used to show what the result of the preprocessing is. This is not shown when for instance
        exporting.
        """
        destination_folder = "../tool_interface/external_preprocessed_dataset/"

        shutil.copy(file_path, destination_folder)
