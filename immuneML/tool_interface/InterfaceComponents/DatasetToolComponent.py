import subprocess
import json
from pathlib import Path
from immuneML.tool_interface.InterfaceComponents.InterfaceComponent import InterfaceComponent


class DatasetToolComponent(InterfaceComponent):

    @staticmethod
    def instruction_handler(ml_specs: dict):
        print("Running DatasetToolComponent")
        # The sub_process should return a JSON string
        result = DatasetToolComponent.start_sub_process(ml_specs)
        print(f"Result shown in instruction_handler: ({type(result)}) --> {result}")
        DatasetToolComponent.handle_response_data(result)

    @staticmethod
    def handle_response_data(json_response):
        # Handles response from tool
        path, file, response_object = None, None, None
        try:
            response_object = json.loads(json_response)
        except Exception as e:
            print(f"Error: {e}")

        print(f"Received data from subprocess: {response_object}")

        try:
            path = response_object["path"]
            file = response_object["dataset_file"]
        except KeyError as e:
            print(e)
            return None

        print(f"Found path: {path} and file: {file}")
        DatasetToolComponent.fetch_dataset(path, file)

    @staticmethod
    def fetch_dataset(path: str, filename: str):
        print(f"""Fetching dataset with information 
            - Path:     {path}
            - Filename: {filename}""")

        path = Path(path)
        # TODO: continue handling the dataset?

    @staticmethod
    def start_sub_process(ml_specs: dict, debug_process=False):
        print("Starting subprocess")

        json_data_example = DatasetToolComponent.produce_JSON_object(path="test",
                                                                     dataset_file="test")
        program = ml_specs.get("tool_path") + "/" + ml_specs.get("tool_executable")

        # Define the command to run the subprocess program
        command = [program, json_data_example]

        # Start the new Terminal window and execute the command in it
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()

        print(f"Process output: {output}")
        return output

