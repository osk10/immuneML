import abc
from pathlib import Path

import numpy as np
import pandas as pd

from pytorch_tabular import TabularModel
from pytorch_tabular.models import CategoryEmbeddingModelConfig
from pytorch_tabular.config import DataConfig, OptimizerConfig, TrainerConfig, ExperimentConfig

from immuneML.data_model.encoded_data.EncodedData import EncodedData
from immuneML.environment.Label import Label
from immuneML.ml_methods.MLMethod import MLMethod
from immuneML.ml_methods.util.Util import Util
from immuneML.util.FilenameHandler import FilenameHandler
from immuneML.util.PathBuilder import PathBuilder

import torch
import math


class PyTorchTabularInterface(MLMethod):

    def __init__(self):
        super(PyTorchTabularInterface, self).__init__()
        self.feature_names = None
        self.class_mapping = None
        self.label = None
        self.input_size = 0
        self.model = None

    def fit(self, encoded_data: EncodedData, label: Label, cores_for_training: int = 2):
        self.label = label
        self.class_mapping = Util.make_class_mapping(encoded_data.labels[self.label.name])
        self.feature_names = encoded_data.feature_names

        numpy_array = encoded_data.examples.toarray()

        # Map from True/False to 1/0
        mapped_y = Util.map_to_new_class_values(encoded_data.labels[self.label.name], self.class_mapping)

        # add mapped_y to array
        data = np.hstack([numpy_array, mapped_y.reshape(-1, 1)])
        # create names for columns
        col_names = [f"feature_{i}" for i in range(data.shape[-1])]
        col_names[-1] = "target"

        # create dataframe with data and column names
        data = pd.DataFrame(data, columns=col_names)

        num_col_names = col_names
        cat_col_names = []
        target_col_name = ['target']

        data_config = DataConfig(
            target=target_col_name,
            continuous_cols=num_col_names,
            categorical_cols=cat_col_names,
        )

        trainer_config, model_config = self._get_config()

        optimizer_config = OptimizerConfig()

        tabular_model = TabularModel(
            data_config=data_config,
            model_config=model_config,
            optimizer_config=optimizer_config,
            trainer_config=trainer_config,
        )
        tabular_model.fit(train=data)
        self.model = tabular_model

    def predict(self, encoded_data: EncodedData, label: Label):
        predictions_proba = self.predict_proba(encoded_data, label)
        return {label.name: [self.class_mapping[val] for val in (predictions_proba[label.name][:, 1] > 0.5).tolist()]}

    def fit_by_cross_validation(self, encoded_data: EncodedData, number_of_splits: int = 5, label: Label = None,
                                cores_for_training: int = -1, optimization_metric=None):
        self.fit(encoded_data, label)

    def store(self, path: Path, feature_names: list = None, details_path: Path = None):
        PathBuilder.build(path)
        file_path = path / f"{self._get_model_filename()}"
        self.model.save_model(file_path)

    def _get_model_filename(self):
        return FilenameHandler.get_filename(self.__class__.__name__, "")

    def load(self, path: Path):
        name = f"{self._get_model_filename()}"
        file_path = str(path / name)
        loaded_model = TabularModel.load_from_checkpoint(file_path)
        self.model = loaded_model

    def check_if_exists(self, path: Path) -> bool:
        return self.model is not None

    def get_classes(self) -> list:
        return self.label.values

    def get_params(self):
        pass

    @abc.abstractmethod
    def _get_config(self):
        pass

    def predict_proba(self, encoded_data: EncodedData, label: Label):
        # prepare data
        # TODO: target column has to be included. Why?
        numpy_array = encoded_data.examples.toarray()
        rows, _ = numpy_array.shape
        target = np.zeros((rows, 1))
        data = np.hstack([numpy_array, target])
        col_names = [f"feature_{i}" for i in range(data.shape[-1])]
        col_names[-1] = "target"
        data = pd.DataFrame(data, columns=col_names)

        # predict
        pred_df = self.model.predict(data)

        return {label.name: np.vstack([pred_df.iloc[:, -3], pred_df.iloc[:, -2]]).T}

    def get_label_name(self) -> str:
        return self.label.name

    def get_package_info(self) -> str:
        return Util.get_immuneML_version()

    def get_feature_names(self) -> list:
        return self.feature_names

    def can_predict_proba(self) -> bool:
        return True

    def get_class_mapping(self) -> dict:
        return self.class_mapping

    def get_compatible_encoders(self):
        from immuneML.encodings.kmer_frequency.KmerFrequencyEncoder import KmerFrequencyEncoder

        return [KmerFrequencyEncoder]
