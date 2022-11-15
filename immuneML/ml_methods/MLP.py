import copy
import random
from pathlib import Path

import numpy as np
import torch
import yaml

from immuneML.data_model.encoded_data.EncodedData import EncodedData
from immuneML.environment.Label import Label
from immuneML.ml_methods.MLMethod import MLMethod
from immuneML.ml_methods.pytorch_implementations.PyTorchMLP import PyTorchMLP
from immuneML.ml_methods.util.Util import Util
from immuneML.util.PathBuilder import PathBuilder
import time



class MLP(MLMethod):
    def __init__(self, result_path: Path = None):
        super().__init__()
        self.feature_names = None
        self.class_mapping = None
        self.label = None
        self.result_path = result_path
        self.input_size = 0

        self.mlp = None
        self.epochs = 10000
        self.learning_rate = 0.0001
        self.threshold = 0.00001
        self.pytorch_device_name = None
        self.number_of_threads = 8
        self.random_seed = None

    def _make_mlp(self):
        return PyTorchMLP(in_features=self.input_size)

    def fit(self, encoded_data: EncodedData, label: Label, cores_for_training: int = 2):
        # Variables needed for training. Used in SklearnMethod.py and AtchletKmerMILClassifier.py
        self.label = label
        self.class_mapping = Util.make_class_mapping(encoded_data.labels[self.label.name])
        self.feature_names = encoded_data.feature_names
        mapped_y = Util.map_to_new_class_values(encoded_data.labels[self.label.name], self.class_mapping)

        # Clear model for training
        self.mlp = None

        # --- Initialization ---,
        random.seed(self.random_seed)
        random_seed = random.randint(1, 100000)

        # Setup pytorch: torch.set_num_threads() and torch.manual_seed()
        #self.pytorch_device_name = torch.device("mps")

        Util.setup_pytorch(self.number_of_threads, random_seed, self.pytorch_device_name)
        self.input_size = encoded_data.examples.shape[1]

        # Create instance of MLP
        _mlp = self._make_mlp()

        # Set loss to infinity, first loss will always be better
        loss = np.inf

        # Define the optimization:
        # Binary cross-entropy loss as loss function
        loss_func = torch.nn.BCELoss()
        # Stochastic gradient descent as optimizer
        optimizer = torch.optim.SGD(_mlp.parameters(), lr=self.learning_rate)
        start_time = time.time()
        for epoch in range(self.epochs):
            """
            Each update to the model involves the same general pattern comprised of:
            - Clearing the last error gradient.
            - A forward pass of the input through the model.
            - Calculating the loss for the model output.
            - Backpropagating the error through the model.
            - Update the model in an effort to reduce loss.
            https://machinelearningmastery.com/pytorch-tutorial-develop-deep-learning-models/
            """
            # clear the last gradients
            optimizer.zero_grad()

            # convert from csr_matrix to numpy array, to Tensor
            numpy_array = encoded_data.examples.toarray()
            inputs = torch.from_numpy(numpy_array).float()

            # compute model output. Forward pass
            output = _mlp(inputs)
            target = torch.tensor(mapped_y).float()
            target = target.reshape(-1, 1)

            # calculate the loss. loss_func(model_ouput, targets)
            loss = loss_func(output, target)

            # backpropagating and update the model
            loss.backward()
            optimizer.step()

            # stop training when loss reaches threshold
            if loss < self.threshold:
                break

            #print("epoch: ", epoch, " - loss: ", loss)

        # set trained model to self.mlp
        self.mlp = _mlp
        print("--- %s seconds ---" % (time.time() - start_time))

        # just for testing and debugging
        #pred = self.predict(encoded_data, label)

    def predict(self, encoded_data: EncodedData, label: Label):
        predictions_proba = self.predict_proba(encoded_data, label)
        return {label.name: [self.class_mapping[val] for val in (predictions_proba[label.name][:, 1] > 0.5).tolist()]}

    def fit_by_cross_validation(self, encoded_data: EncodedData, number_of_splits: int = 5, label: Label = None,
                                cores_for_training: int = -1, optimization_metric=None):
        self.fit(encoded_data, label)

    def store(self, path: Path, feature_names: list = None, details_path: Path = None):
        PathBuilder.build(path)
        torch.save(copy.deepcopy(self.mlp).state_dict(), str(path / "mlp.pt"))
        custom_vars = copy.deepcopy(vars(self))

        # coefficients_df = pd.DataFrame(custom_vars["mlp"].layer.detach().numpy(), columns=feature_names)
        # coefficients_df["bias"] = custom_vars["mlp"].linear.bias.detach().numpy()
        # coefficients_df.to_csv(path / "coefficients.csv", index=False)

        del custom_vars["result_path"]
        del custom_vars["mlp"]
        del custom_vars["label"]

        if self.label:
            custom_vars["label"] = vars(self.label)

        params_path = path / "custom_params.yaml"
        with params_path.open('w') as file:
            yaml.dump(custom_vars, file)

    def load(self, path: Path):
        params_path = path / "custom_params.yaml"
        with params_path.open("r") as file:
            custom_params = yaml.load(file, Loader=yaml.SafeLoader)

        for param, value in custom_params.items():
            if hasattr(self, param):
                if param == "label":
                    setattr(self, "label", Label(**value))
                else:
                    setattr(self, param, value)

        self.mlp = self._make_mlp()
        self.mlp.load_state_dict(torch.load(str(path / "mlp.pt")))

    def check_if_exists(self, path: Path) -> bool:
        return self.mlp is not None

    def get_classes(self) -> list:
        return self.label.values

    def get_params(self):
        params = copy.deepcopy(vars(self))
        params["mlp"] = copy.deepcopy(self.mlp).state_dict()
        return params

    def predict_proba(self, encoded_data: EncodedData, label: Label):
        self.mlp.eval()
        numpy_array = encoded_data.examples.toarray()

        with torch.no_grad():
            data = torch.from_numpy(numpy_array).float()
            # output from Torch to numpy, then squeeze to get array
            predictions = self.mlp(data).numpy().squeeze()

            # TODO: is sigmoid needed when it is used in the PyTorchMLP forward pass??
            #predictions = torch.sigmoid(self.mlp(data)).numpy()

        return {label.name: np.vstack([1 - np.array(predictions), predictions]).T}

    def get_label_name(self) -> str:
        return self.label.name

    def get_package_info(self) -> str:
        return Util.get_immuneML_version()

    def get_feature_names(self) -> list:
        return self.feature_names

    def can_predict_proba(self) -> bool:
        return True

    def get_class_mapping(self) -> dict:
        """Returns a dictionary containing the mapping between label values and values internally used in the classifier"""
        return self.class_mapping

    def get_compatible_encoders(self):
        from immuneML.encodings.kmer_frequency.KmerFrequencyEncoder import KmerFrequencyEncoder

        return [KmerFrequencyEncoder]
