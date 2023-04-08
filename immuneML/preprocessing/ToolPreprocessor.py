from abc import ABC
from pathlib import Path


from immuneML.IO.dataset_export.AIRRExporter import AIRRExporter
from immuneML.preprocessing.Preprocessor import Preprocessor
from immuneML.tool_interface import InterfaceController
from immuneML.util.PathBuilder import PathBuilder


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

        params = {"result_path": result_path, "tool_name": self.tool_name}
        print(f"Params to tool: {params}")
        return ToolPreprocessor.process(dataset, params)

    @staticmethod
    def process(dataset, params: dict):
        """ Takes a dataset and returns a new (modified) dataset.
        """

        processed_dataset = dataset.clone()

        # FIRST: export the dataset to AIRR (.tsv) format that the external tool can handle
        path = "/Users/jorgenskimmeland/Documents/aar5/Master/preprocessing test/testingOutput"
        path = PathBuilder.build(path)
        AIRRExporter.export(dataset, path)

        # TODO: get the filepath

        # Start the tool handling the dataset. Returns a path to the dataset
        result = InterfaceController.run_func(params["tool_name"], "run_preprocessing")

        # Get as result the path to the file that has been extended

        #path = "/Users/jorgenskimmeland/Documents/aar5/Master/preprocessing test/testingOutput/merged_file.tsv"
        #result_path = "/Users/jorgenskimmeland/Documents/aar5/Master/preprocessing test/testingOutput/"

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
