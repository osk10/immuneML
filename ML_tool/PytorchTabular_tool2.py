import json
import pickle

import numpy as np
import pandas as pd
import zmq
from pytorch_tabular import TabularModel
from pytorch_tabular.config import DataConfig, OptimizerConfig, TrainerConfig
from pytorch_tabular.models import CategoryEmbeddingModelConfig


def make_binary_class_mapping(y) -> dict:
    """
    Creates binary class mapping from a list of classes which can be strings, numbers or boolean values
    Arguments:
        y: list of classes per example, as supplied to fit() method of the classifier; it should include all classes that will appear in the data
    Returns:
         mapping dictionary where 0 and 1 are always the keys and the values are original class names which were mapped for these values
    """
    unique_values = sorted(set(y))
    assert len(unique_values) == 2, f"MLMethod: there has two be exactly two classes to use this classifier," \
                                    f" instead got {str(unique_values)[1:-1]}. For multi-class classification, " \
                                    f"consider some of the other classifiers."
    return {0: unique_values[0], 1: unique_values[1]}


def make_class_mapping(y) -> dict:
    """Creates a class mapping from a list of classes which can be strings, numbers of booleans; maps to same name in multi-class settings"""
    classes = np.unique(y)
    if classes.shape[0] == 2:
        return make_binary_class_mapping(y)
    else:
        return {cls: cls for cls in classes}


def map_to_new_class_values(y, class_mapping: dict):
    try:
        mapped_y = np.copy(y).astype(object)
        switched_mapping = {value: key for key, value in class_mapping.items()}
        new_class_type = np.array(list(switched_mapping.values())).dtype
        for i in range(mapped_y.shape[0]):
            mapped_y[i] = switched_mapping[y[i]]
        return mapped_y.astype(new_class_type)
    except Exception as e:
        print(f"MLMethod util: error occurred when fitting the model due to mismatch of class types.\n"
              f"Classes: {y}\nMapping:{class_mapping}")
        raise e


def train_model(encoded_data, path, label):
    print(encoded_data)
    # print(encoded_data.encoding)
    print("TOOL: running fit. Data: ", encoded_data)

    label_name = label

    class_mapping = make_class_mapping(encoded_data.labels[label_name])

    numpy_array = encoded_data.examples.toarray()

    # Map from True/False to 1/0
    mapped_y = map_to_new_class_values(
        encoded_data.labels[label_name], class_mapping)

    # add mapped_y to array
    data = np.hstack([numpy_array, mapped_y.reshape(-1, 1)])
    # create names for columns
    col_names = [f"feature_{i}" for i in range(data.shape[-1])]
    col_names[-1] = "target"

    # create dataframe with data and column names
    data = pd.DataFrame(data, columns=col_names)
    test_idx = data.sample(int(0.2 * len(data)), random_state=42).index
    test = data[data.index.isin(test_idx)]
    train = data[~data.index.isin(test_idx)]

    num_col_names = col_names
    cat_col_names = []
    target_col_name = ['target']

    data_config = DataConfig(
        target=target_col_name,
        continuous_cols=num_col_names,
        categorical_cols=cat_col_names,
    )

    trainer_config = TrainerConfig(
        auto_lr_find=False,  # Runs the LRFinder to automatically derive a learning rate
        batch_size=32,
        max_epochs=100,
        gpus=None,  # index of the GPU to use. None means CPU
    )

    optimizer_config = OptimizerConfig()

    model_config = CategoryEmbeddingModelConfig(
        task="classification",
        layers="4096-4096-512",  # Number of nodes in each layer
        activation="LeakyReLU",  # Activation between each layers
        learning_rate=1e-3
    )

    tabular_model = TabularModel(
        data_config=data_config,
        model_config=model_config,
        optimizer_config=optimizer_config,
        trainer_config=trainer_config,
    )
    tabular_model.fit(train=train)
    global model
    model = tabular_model

    result = tabular_model.evaluate(test)
    pred_df = tabular_model.predict(test)
    print(pred_df.head())
    print(pred_df["prediction"])
    print(result)

    # tabular_model.save_model(path)

    result2 = {
        'fit_finished': True
    }
    return json.dumps(result2)


# COMMUNICATION WITH CORE
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:

    pickle_message = socket.recv_pyobj()
    pickle_message = pickle.loads(pickle_message)
    result = {
        'data_received': True
    }
    socket.send_json(json.dumps(result))
    json_message = socket.recv_json()

    for func_name, value in json.loads(json_message).items():
        print(func_name)
        print(value)
        print(type(value))
        result = globals()[func_name](pickle_message, value["path"], value["label"])
        socket.send_json(json.dumps(result))
