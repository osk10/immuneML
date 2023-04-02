from immuneML.tool_interface.interface_components.InterfaceComponent import InterfaceComponent


class PreprocessingComponent(InterfaceComponent):
    """ Runs an external preprocessing program

    The preprocessing component should return the path to the dataset(?)

    """

    def __init__(self, name: str, specs: dict):
        super().__init__(name, specs)

    def run_preprocessing(self, dataset_file):
        print("Running preprocessing component")

        print("Sending parameters to preprocessing program")

        print("Receiving data path from preprocessing")

        print("Returning preprocessing dataset")
        pass

    def insert_dataset_to_immuneML(self, dataset_path: str) -> str:
        print("Copying data from produced dataset and inserting into immuneML for further use")

        returned_path = dataset_path
        return returned_path
