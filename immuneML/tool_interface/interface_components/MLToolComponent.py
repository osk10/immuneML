import json
import pickle

from immuneML.tool_interface.interface_components.InterfaceComponent import InterfaceComponent


class MLToolComponent(InterfaceComponent):
    def __init__(self, name: str, specs: dict):
        super().__init__(name, specs)

    def _prepare_data(self, encoded_data):
        if self.interpreter != "python":
            pickle_data = pickle.dumps(encoded_data)
            return pickle_data
        else:
            paths = {
                "metadata": encoded_data.info["metadata_filepath"],
                "dataset": encoded_data.info["dataset_filepath"],
            }
            json_data = json.dumps(paths)
            return json_data

    def run_fit(self, encoded_data):
        data = self._prepare_data(encoded_data)
        """
        if self.interpreter != "python":
            self.socket.send_pyobj(data)
            res = json.loads(self.socket.recv_json())

            if res["data_received"] is True:
                # print("Tool received data")
                pass
            else:
                # TODO: retry sending data?
                pass
        else:
            self.socket.send_json(data)
            result = json.loads(self.socket.recv_json())
            if result["data_received"] is True:
                # print("Tool received data")
                pass
        """
        # run function in tool
        x = {
            'fit':                {"metadata_filepath": encoded_data.info["metadata_filepath"],
                "dataset_filepath": encoded_data.info["dataset_filepath"]+"\\encoding"},
        }
        self.socket.send_json(json.dumps(x))

        # receive results and load pickle data
        res = self.socket.recv_pyobj()
        # print(pickle.loads(res))

    def run_predict(self, encoded_data):
        data = self._prepare_data(encoded_data)
        self.socket.send_pyobj(data)
        result = json.loads(self.socket.recv_json())
        if result["data_received"] is True:
            # print("Tool received data")
            pass
        else:
            # TODO: retry sending data
            pass

        # run function in tool
        x = {
            'predict': 1,
        }
        self.socket.send_json(json.dumps(x))

        # receive results and load pickle data
        res = self.socket.recv_pyobj()
        return pickle.loads(res)

    def run_predict_proba(self, encoded_data):
        data = self._prepare_data(encoded_data)
        self.socket.send_pyobj(data)
        result = json.loads(self.socket.recv_json())
        if result["data_received"] is True:
            # print("Tool received data")
            pass

        # run function in tool
        x = {
            'predict_proba': 1,
        }
        self.socket.send_json(json.dumps(x))

        # receive results and load pickle data
        res = self.socket.recv_pyobj()
        return pickle.loads(res)
