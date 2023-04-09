import json
import pickle
import sys

import numpy as np
import zmq
from sklearn.linear_model import LogisticRegression


class NewLogisticRegression:
    def __init__(self):
        self.model = None
        self.label = None
        self.feature_names = None
        self.class_mapping = {
            0: False,
            1: True
        }

    def fit(self, encoded_data):
        self.feature_names = encoded_data.feature_names
        self.label = "signal_disease"
        mapped_y = self.map_to_new_class_values(encoded_data.labels[self.label], self.class_mapping)

        X = encoded_data.examples
        y = mapped_y

        # TODO: Implement scikit learn logistic regression
        self.model = LogisticRegression()

        # TODO: train model
        self.model.fit(X, y)

    def predict(self, encoded_data):
        predictions = self.model.predict(encoded_data.examples)
        return {self.label: self.map_to_old_class_values(np.array(predictions), self.class_mapping)}

    def predict_proba(self, encoded_data):
        # new version of immuneML. Change when we have updated immuneML
        # probabilities = self.model.predict_proba(encoded_data.examples)
        # class_names = self.map_to_old_class_values(self.model.classes_, self.class_mapping)

        # return {self.label: {class_name: probabilities[:, i] for i, class_name in enumerate(class_names)}}
        predictions = {self.label: self.model.predict_proba(encoded_data.examples)}
        return predictions

    def get_params(self):
        params = self.model.get_params()
        params["coefficients"] = self.model.coef_[0].tolist()
        params["intercept"] = self.model.intercept_.tolist()
        return params

    def get_feature_names(self):
        return self.feature_names

    def can_predict_proba(self):
        return True

    def get_class_mapping(self):
        return self.class_mapping

    def map_to_new_class_values(self, y, class_mapping):
        mapped_y = np.copy(y).astype(object)
        switched_mapping = {value: key for key, value in class_mapping.items()}
        new_class_type = np.array(list(switched_mapping.values())).dtype
        for i in range(mapped_y.shape[0]):
            mapped_y[i] = switched_mapping[y[i]]
        return mapped_y.astype(new_class_type)

    def map_to_old_class_values(self, y, class_mapping):
        old_class_type = np.array(list(class_mapping.values())).dtype
        mapped_y = np.copy(y).astype(object)
        for i in range(mapped_y.shape[0]):
            mapped_y[i] = class_mapping[y[i]]
        return mapped_y.astype(old_class_type)


def main():
    # Program must take the port number as only program input
    port_number = sys.argv[1]

    # Bind to ZeroMQ socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port_number)

    # Wait for a message from immuneML. This will be empty
    socket.recv_string()

    # Send an acknowledgement message back. Must be json format and should be empty
    socket.send_string("")

    # Receive the parameters from immuneML.
    # Sent as json string with parameters defined by the tool developers
    # The parameters must be defined and documented to enable the program to run
    # Example: {"parameter_1": "x", "parameter_2": "y"}
    # program_parameters = socket.recv_json()

    # ------------- Add your functionality here -------------
    my_class = globals()["MyTool"]()
    while True:
        pickle_message = socket.recv_pyobj()
        pickle_message = pickle.loads(pickle_message)
        response = {
            'data_received': True
        }
        socket.send_json(json.dumps(response))
        json_message = socket.recv_json()

        for func_name, value in json.loads(json_message).items():
            my_function = getattr(my_class, func_name)
            result = my_function(pickle_message)
            # result = globals()[func_name](pickle_message)
            socket.send_pyobj(pickle.dumps(result))


if __name__ == "__main__":
    """ Your program receives a port number from immuneML. This is used to establish connection with immuneML
    """
    main()
