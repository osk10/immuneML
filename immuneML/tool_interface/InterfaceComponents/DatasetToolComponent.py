import subprocess
import json


class DatasetToolComponent:

    @staticmethod
    def instruction_handler(ml_specs: dict):
        print("------- ----- ---- Broski you are now trying to run an external dataset tool")
        # The sub_process should return a JSON string
        result: str = DatasetToolComponent.start_sub_process(ml_specs)
        DatasetToolComponent.handle_response_data(result)

    @staticmethod
    def handle_response_data(json_response: str):
        # Handles response from tool
        # For instance in the context of a dataset tool that would be a path and file name?
        """
        {
          path: "",
          file: ""
        }
        """
        path, file, response_object = None, None, None
        try:
            response_object = json.loads(json_response)
        except json.decoder.JSONDecodeError as e:
            print(f"Error: {e.msg}")

        try:
            path = response_object["path"]
            file = response_object["dataset_file"]
        except KeyError as e:
            print(e)
            return None

        print(f"Found path: {path} and file: {file}")

    @staticmethod
    def fetch_dataset(path: str, file: str):
        # Fetch the data from path and filename
        # Search through path file?
        # Or use default path?
        print("Fetching dataset?")

    @staticmethod
    def start_sub_process(ml_specs: dict):
        print("Starting subprocess")

        # must send information to the tool
        # path where the dataset should be stored
        program = ml_specs.get("tool_path") + "/" + ml_specs.get("tool_executable")
        proc = subprocess.Popen([program],
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                shell=True)

        stdout, stderr = proc.communicate()
        return stdout.decode()

    @staticmethod
    def create_dataset_result():
        print("Creating dataset results")
        default_folder_path = ""

        #  should the program create a folder where the dataset should be stored?

