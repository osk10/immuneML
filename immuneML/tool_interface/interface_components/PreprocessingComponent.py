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

        # TODO: send the parameters to the tool
        tool_args = self.create_json_params(self.specs)

        # Add the dataset path to it
        #tool_args['file_path'] = dataset_path

        self.socket.send_json(tool_args)  # Send input to tool

        print("Receiving data path from preprocessing")
        response = self.socket.recv_json()

        print(f"Dataset received from program: {response}")

        dataset_path = response["dataset"]

        self.insert_dataset_to_immuneML(dataset_path)


    def insert_dataset_to_immuneML(self, dataset_path: str) -> str:
        """This function uses the dataset path returned from tool to replace the original dataset

        """
        print("Copying data from produced dataset and inserting into immuneML for further use")

        returned_path = dataset_path
        return returned_path
