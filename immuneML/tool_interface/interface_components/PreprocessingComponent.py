from immuneML.tool_interface.interface_components.InterfaceComponent import InterfaceComponent


class PreprocessingComponent(InterfaceComponent):
    """ Runs an external preprocessing program

    The preprocessing component should return the path to the dataset(?)

    """

    def __init__(self, name: str, specs: dict):
        super().__init__(name, specs)

    def run_preprocessing(self, dataset_path):
        print("Running preprocessing component")

        tool_args = self.create_json_params(self.specs)

        test = self.specs["params"]
        # Add the dataset path
        test["filename"] = dataset_path

        self.socket.send_json(self.specs["params"])  # Send input to tool

        response = self.socket.recv_json()

        print(f"Dataset received from program: {response}")

        dataset_path = response["dataset"]

        return dataset_path


