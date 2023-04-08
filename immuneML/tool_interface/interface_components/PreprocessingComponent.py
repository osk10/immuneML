from immuneML.tool_interface.interface_components.InterfaceComponent import InterfaceComponent


class PreprocessingComponent(InterfaceComponent):
    """ Runs an external preprocessing program

    The preprocessing component should return the path to the dataset(?)

    """

    def __init__(self, name: str, specs: dict):
        super().__init__(name, specs)

    def run_preprocessing(self, dataset_path):
        print("Running preprocessing component")

        print("Sending parameters to preprocessing program")

        tool_args = self.create_json_params(self.specs)

        # Add into tool_args the path to the dataset that is to be processed
        tool_args = self.add_value_to_json_string(tool_args, "dataset_path", dataset_path)

        self.socket.send_json(tool_args)  # Send input to tool

        print("Receiving data path from preprocessing")
        response = self.socket.recv_json()

        print(f"Dataset received from program: {response}")

        dataset_path = response["dataset"]

        return dataset_path


