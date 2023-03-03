import subprocess
import os
import shutil
from immuneML.tool_interface.InterfaceComponents.InterfaceComponent import InterfaceComponent


class DatasetToolComponent(InterfaceComponent):
    # Set the path of where the datasets should be stored and fetched from
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    DEFAULT_DATASET_FOLDER_PATH = os.path.join(parent_directory, "generated_datasets")

    @staticmethod
    def instruction_handler(ml_specs: dict):
        print("\n------- Running DatasetToolComponent-------\n")
        result = DatasetToolComponent.start_sub_process(ml_specs)
        print(f"Result shown in instruction_handler: ({type(result)}) --> {result}")
        print(f"Path to dataset folder: {DatasetToolComponent.DEFAULT_DATASET_FOLDER_PATH}")

    @staticmethod
    def fetch_dataset(process_output: str) -> str:
        process_output: list = process_output.split("\n")
        for line in process_output:
            if "Dataset path:" in line:
                path = line.split(":")[1].strip()
                return path
        return "None"

    @staticmethod
    def change_dataset_folder(dataset_path: str, target_path: str):
        # Get the filename of the dataset from its path
        #target_path = target_path + "/" + os.path.basename(dataset_path)

        shutil.move(dataset_path, target_path)

    @staticmethod
    def start_sub_process(ml_specs: dict, debug_process=False):
        print("Starting subprocess")

        json_data_example = DatasetToolComponent.produce_JSON_object(
            option="repertoire",
            antigen="1FBI",
            filename="miniSetCDR3-TESTING.txt",
            threads=3
        )

        print(f"Produced json string:\n{json_data_example}")

        # json_data_example2 = DatasetToolComponent.produce_JSON_object(
        # dataset_folder=DatasetToolComponent.DEFAULT_DATASET_FOLDER_PATH)
        tool_path = ml_specs.get("tool_path")
        program = tool_path + "/" + ml_specs.get("tool_executable")

        # Define the command to run the subprocess program
        command = [program, json_data_example]

        # Start the new Terminal window and execute the command in it
        # Include 'cwd' to make sure to use the subprocess working directory, not inherit from main process
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=tool_path)

        if process.stdout:
            output_string = ""
            if not InterfaceComponent.show_process_output(ml_specs):
                # animation used for user feedback to avoid it seeming like the subprocess has frozen
                print(f"-------------------- Show animation because show_process_output is False")
                InterfaceComponent.subprocess_animation(process)
            else:
                output_bytes = process.stdout.read()
                output_string = output_bytes.decode("UTF-8")
                print(output_string)
                return_code = process.wait()
                # Get the path of the dataset so we can move it to inside of immuneML
            dataset_path = DatasetToolComponent.fetch_dataset(output_string)
            print(f"Checking if path exists: {os.path.exists(dataset_path)}")
            print(f"Checking if default path exists: {os.path.exists(DatasetToolComponent.DEFAULT_DATASET_FOLDER_PATH)}")
            DatasetToolComponent.change_dataset_folder(dataset_path, DatasetToolComponent.DEFAULT_DATASET_FOLDER_PATH)

        # Important to check for error returned by pipe. Error does not show in stdout
        if process.stderr:
            print(f"Subprocess error: {process.stderr.read().decode('UTF-8')}")

        output, error = process.communicate()
        # print(f"\nProcess output: {output}")

        # This should only be printed under success
        # print(f"Dataset is now available in path: {DatasetToolComponent.DEFAULT_DATASET_FOLDER_PATH}")
        return output
