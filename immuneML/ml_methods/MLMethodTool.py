from pathlib import Path

from immuneML.data_model.encoded_data.EncodedData import EncodedData
from immuneML.environment.Label import Label
from immuneML.ml_methods.MLMethod import MLMethod
from immuneML.tool_interface import InterfaceController


class MLMethodTool(MLMethod):
    def __init__(self):
        super().__init__()

    def fit(self, encoded_data: EncodedData, label: Label, cores_for_training: int = 2):
        InterfaceController.run_func(self.name, "run_fit", encoded_data)

    def predict(self, encoded_data: EncodedData, label: Label):
        result = InterfaceController.run_func(self.name, "run_predict", encoded_data)
        return result

    def fit_by_cross_validation(self, encoded_data: EncodedData, number_of_splits: int = 5, label: Label = None,
                                cores_for_training: int = -1, optimization_metric=None):
        pass

    def store(self, path: Path, feature_names: list = None, details_path: Path = None):
        # TODO: subprocess call store
        # store(path, feature_names, details_path)
        pass

    def load(self, path: Path):
        pass

    def check_if_exists(self, path: Path) -> bool:
        return False

    def get_classes(self) -> list:
        return [False, True]

    def get_params(self):
        pass

    def predict_proba(self, encoded_data: EncodedData, Label: Label):
        result = InterfaceController.run_func(self.name, "run_predict_proba", encoded_data)
        return result

    def get_label_name(self) -> str:
        pass

    def get_package_info(self) -> str:
        pass

    def get_feature_names(self) -> list:
        pass

    def can_predict_proba(self) -> bool:
        pass

    def get_class_mapping(self) -> dict:
        pass

    def get_compatible_encoders(self):
        from immuneML.encodings.kmer_frequency.KmerFrequencyEncoder import KmerFrequencyEncoder

        return [KmerFrequencyEncoder]

    def get_positive_class(self):
        return True
