from abc import ABC
from pathlib import Path

from immuneML.preprocessing.Preprocessor import Preprocessor


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

    def __init__(self, test: str, result_path: Path = None):
        super().__init__(result_path)
        self.test = test

    def process_dataset(self, dataset, result_path):
        """ which typically prepares parameters and calls process(dataset, params) internally
        """
        print("Running PreprocessingTool process_dataset()")
        params = {"result_path": result_path}
        return ToolPreprocessor.process(dataset, params)

    @staticmethod
    def process(dataset, params: dict):
        """ Takes a dataset and returns a new (modified) dataset.
        """
        print("Running PreprocessingTool process()")
        return dataset  # TODO: make changes so that the dataset is processed before it is returned

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
