from abc import ABC, abstractmethod
import subprocess
import time
import sys
import json


class InterfaceComponent(ABC):
    # The other components should inherit from this
    # Should contain functions that can be reused, overwritten or new functions added (?)

    @staticmethod
    def start_sub_process(ml_specs: dict):
        # Should have a standard way of starting a subprocess that can be overwritten
        pass

    @staticmethod
    def produce_JSON_object(**input_data):
        # The communication of instructions to a subprocess should be through a JSON string message
        # **input_data = dictionary of keyword arguments
        #print("Printing input sent to function produce_JSON_object")
        #for key, value in input_data.items():
        #print(f"Key: {key}, value: {value}")
        print("Producing JSON object")

        try:
            json_bytes = json.dumps(input_data)
        except Exception as e:
            print(f"Error: {e}")
            return None

        return json_bytes

    @staticmethod
    def check_executable_language(filename: str):
        # I don't know if this is necessary, but we might have to know which language that we are supposed to run?
        # Alternatively we can simply ask the user to write language of executable into the YAML file, but this might
        # introduce a confusing element for the user as they then would have to know the language of the executable
        pass

    @staticmethod
    def subprocess_animation(process: subprocess):
        # Animation only meant for giving user feedback in terminal
        # Subprocesses can take a long time, so it's important for the user to know the program is not frozen
        num_dots = 0

        while process.poll() is None:
            sys.stdout.write('\rRunning subprocess{}   '.format('.' * num_dots))
            sys.stdout.flush()
            num_dots = (num_dots + 1) % 4
            time.sleep(0.5)

        # Clear the output
        sys.stdout.flush()
        sys.stdout.write("\rSubprocess finished")

    @staticmethod
    def show_process_output(ml_specs: dict):
        # Checks for the parameter "show_process_output"
        # If this parameter is not defined in YAML file, output will not be shown, but rather a process status
        show_output = False
        value = ml_specs.get("show_process_output")
        if value is not None:
            if value == "True":
                show_output = True
            elif value != "False":
                print("show_process_output must have parameter 'True' or 'False")
        else:
            print("Not showing process output. If you want too see process output, insert show_process_output: 'True' "
                  "into YAML specification file")
        return show_output
