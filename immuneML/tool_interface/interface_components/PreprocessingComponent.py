from immuneML.tool_interface.interface_components.InterfaceComponent import InterfaceComponent


class PreprocessingComponent(InterfaceComponent):
    """ Runs an external preprocessing tool
    """

    def __init__(self, name: str, specs: dict):
        super().__init__(name, specs)

    def run_preprocessing(self, dataset_path):
        """ Main function running external preprocessing

        Returns the path to the preprocessed dataset
        """
        print("Running preprocessing component")

        # Get specified tool parameters
        tool_args = self.specs["params"]
        # Add the dataset path (to be preprocessed) to the params list
        tool_args["filename"] = dataset_path

        # Send parameters to external preprocessor and wait for dataset path in return
        self.socket.send_json(self.specs["params"])
        response = self.socket.recv_json()

        # Set dataset path to the response path retrieved by tool
        dataset_path = response["dataset"]

        return dataset_path


