import json

from immuneML.tool_interface.interface_components.InterfaceComponent import InterfaceComponent


class MLToolComponent(InterfaceComponent):
    def __init__(self, name: str, specs: dict):
        super().__init__(name, specs)

    def run_fit(self, encoded_data):
        x = {
            'fit': {"metadata_filepath": encoded_data.info["metadata_filepath"],
                    "dataset_filepath": encoded_data.info["dataset_filepath"]},
        }
        self.socket.send_json(json.dumps(x))

        res = json.loads(self.socket.recv_json())

    def run_predict(self, encoded_data):
        x = {
            'predict': {"metadata_filepath": encoded_data.info["metadata_filepath"],
                        "dataset_filepath": encoded_data.info["dataset_filepath"]},
        }
        self.socket.send_json(json.dumps(x))

        # receive results and load pickle data
        res = json.loads(self.socket.recv_json())
        return res

    def run_predict_proba(self, encoded_data):
        x = {
            'predict_proba': {"metadata_filepath": encoded_data.info["metadata_filepath"],
                              "dataset_filepath": encoded_data.info["dataset_filepath"]},
        }
        self.socket.send_json(json.dumps(x))

        # receive results and load pickle data
        res = json.loads(self.socket.recv_json())
        return res
