import json
import os
import shutil
import socket
import subprocess
import sys
import time
from abc import ABC

import zmq

tool_process = None


class InterfaceComponent(ABC):
    def __init__(self, name: str, specs: dict):
        self.name = name
        self.specs = specs
        self.tool_path = specs['path']
        self.port = self.find_available_port()
        self.socket = None
        self.pid = None
        self.interpreter = self.get_interpreter(self.tool_path)

    interpreters = {
        ".py": "python",
        ".class": "java"
    }

    @classmethod
    def _get_interpreters(cls):
        """ Returns the dictionary of interpreters. Not accessible by child classes
        """
        return cls.interpreters

    def get_interpreter(self, path: str):
        """ Returns the correct interpreter for executable input. If no extension is found, it returns None and
        assumes that no interpreter should be added to the subprocess module
        """
        interpreters = self._get_interpreters()
        file_extension = os.path.splitext(path)[-1]
        if file_extension not in interpreters:
            print(f"Interpreter not found for executable: {path}")
            return None

        interpreter = interpreters.get(file_extension)

        return interpreter

    def create_json_params(self, specs: dict) -> str:
        """ Creates a json string from tool params specified in YAML
        """
        if 'params' in specs:
            return json.dumps(specs['params'])
        else:
            return ""

    @staticmethod
    def find_available_port(start_port=5000, end_port=8000):
        """ Finds an available port on the computer to send to subprocess
        """
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.bind(("", port))
                    return port
                except OSError:
                    pass

        return None

    def start_subprocess(self):
        # TODO: get interpreter

        # TODO: find available interpreter

        global tool_process
        tool_process = subprocess.Popen(
            ["python", self.tool_path, self.port],
            stdin=subprocess.PIPE)
        self.pid = tool_process.pid

    def stop_subprocess(self):
        global tool_process
        print("stopping tool process", self.pid)
        if tool_process is not None and (self.pid is None or self.pid == self.pid):
            tool_process.kill()
            tool_process = None
        print("tool process stopped")

    def open_connection(self):
        context = zmq.Context()

        #  Socket to talk to server
        print("Connecting to tool…")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:" + self.port)
        print("Connected to tool")

    def close_connection(self):
        self.socket.close()

    @staticmethod
    def execution_animation(process: subprocess):
        """Function creates an animation to give user feedback while process in running
        """

        num_dots = 0

        while process.poll() is None:
            sys.stdout.write('\rRunning subprocess{}   '.format('.' * num_dots))
            sys.stdout.flush()
            num_dots = (num_dots + 1) % 4
            time.sleep(0.5)

        sys.stdout.flush()
        sys.stdout.write("\rSubprocess finished")

    @staticmethod
    def show_process_output(ml_specs: dict):
        """ Returns true or false for showing process output based on YAML spec file
        """

        show_output = False
        value = ml_specs.get("show_process_output")

        if value is not None:
            if value.lower() == "true":
                show_output = True
            elif value.lower() != "false":
                print(f"Show_process_output must have parameter 'true' or 'false'. Parameter given: {value}")
            else:
                print("""Process output not showing. Include 'Show_process_output: true' in the YAML spec file to 
                see process output""")

        return show_output
