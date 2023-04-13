from immuneML.tool_interface.interface_components.InterfaceComponent import InterfaceComponent


class PreprocessingComponent(InterfaceComponent):
    """ Runs an external preprocessing program

    The preprocessing component should return the path to the dataset(?)

    """

    def __init__(self, name: str, specs: dict):
        super().__init__(name, specs)

    def run_preprocessing(self, dataset_path):
        """ Main function running external preprocessing
        """
        print("Running preprocessing component")

        tool_args = self.create_json_params(self.specs)
        test = self.specs["params"]
        test["filename"] = dataset_path  # Add the dataset path to the params list

        # Send parameters to external preprocessor and wait for dataset path in return
        self.socket.send_json(self.specs["params"])
        response = self.socket.recv_json()

        dataset_path = response["dataset"]

        return dataset_path


