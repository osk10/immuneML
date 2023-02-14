import subprocess

class InterfaceDatasetTool:

    @staticmethod
    def instruction_handler(ml_specs: dict):
        print("------- ----- ---- Broski you are now trying to run an external dataset tool")

        InterfaceDatasetTool.start_sub_process(ml_specs)

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
        print("\n--------Summary of tool output--------")
        print(stdout.decode())

    @staticmethod
    def create_dataset_result():
        print("Creating dataset results")
        default_folder_path = ""

        #  should the program create a folder where the dataset should be stored?

