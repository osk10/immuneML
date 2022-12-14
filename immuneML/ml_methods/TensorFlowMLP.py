import tensorflow

from immuneML.ml_methods.MLMethod import MLMethod
from pathlib import Path

from sklearn.exceptions import NotFittedError

from immuneML.data_model.encoded_data.EncodedData import EncodedData
from immuneML.environment import Label
from immuneML.ml_methods.util.Util import Util
from immuneML.util.PathBuilder import PathBuilder

import tensorflow as tf
import keras
from keras import layers
from keras.layers import Dense


class TensorFlowMLP(MLMethod):

    def __init__(self, result_path: Path = None):
        super().__init__()
        self.feature_names = None
        self.class_mapping = None
        self.label = None
        self.result_path = result_path
        self.input_size = 0
        self.mlp = None
        self.random_seed = None
        self.model = None
        self.epochs = 100 # testing




    def fit(self, encoded_data: EncodedData, label: Label, cores_for_training: int = 2):
        self.feature_names = encoded_data.feature_names
        self.label = label
        self.class_mapping = Util.make_class_mapping(encoded_data.labels[self.label.name])
        self.feature_names = encoded_data.feature_names
        mapped_y = Util.map_to_new_class_values(encoded_data.labels[self.label.name], self.class_mapping)

        # Create a Sequential model
        self.model = keras.models.Sequential()

        # We have to define the input (which is 70 values), and we define 10 as the amount of neurons in the layer
        self.model.add(Dense(10, input_shape=(70,), activation="sigmoid"))

        # Compile the model with default optimizer (sgd = stochastic gradient descent)
        self.model.compile(optimizer='sgd', loss='mse', metrics=['accuracy'])

        self.model.fit(mapped_y, epochs=self.epochs)


    def predict(self, encoded_data: EncodedData, label: Label):
        predictions_proba = self.predict_proba(encoded_data, label)
        return {label.name: [self.class_mapping[val] for val in (predictions_proba[label.name][:, 1] > 0.5).tolist()]}

    def fit_by_cross_validation(self, encoded_data: EncodedData, number_of_splits: int = 5, label: Label = None,
                                cores_for_training: int = -1,
                                optimization_metric=None):
        self.fit(encoded_data, label)

    def store(self, path: Path, feature_names: list = None, details_path: Path = None):
        PathBuilder.build(path)

    def load(self, path: Path):
        pass

    def check_if_exists(self, path: Path) -> bool:
        return self.mlp is not None

    def get_classes(self) -> list:
        return self.label.values

    def get_params(self):
        pass

    def predict_proba(self, encoded_data: EncodedData, label: Label):
        if self.can_predict_proba():
            predictions = {label.name: self.model.predict_proba(encoded_data.examples)}
            return predictions
        else:
            return None

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
