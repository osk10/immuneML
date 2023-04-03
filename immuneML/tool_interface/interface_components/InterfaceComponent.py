import json
import os
import socket
import subprocess
import sys
import time
from abc import ABC

import zmq


class InterfaceComponent(ABC):
    def __init__(self, name: str, specs: dict):
        self.name = name
        self.specs = specs
        self.tool_path = specs['path']
        self.port = None
        self.socket = None
        self.process = None
        self.interpreter = None

        self.set_interpreter()

    def set_interpreter(self):
        """ Sets the interpreter necessary for running the tool

        If no extension is found, it returns None and assumes that no interpreter should be added to the subprocess
        module
        """

        # Current valid interpreters
        interpreters = {
            ".py": "python",
            ".class": "java"
        }

        file_extension = os.path.splitext(self.tool_path)[-1]
        if file_extension not in interpreters:
            print(f"Interpreter not found for script: {self.tool_path}")
            print(f"Assuming the file is an executable")  # TODO: We should add a bit more description here
            return None

        self.interpreter = interpreters.get(file_extension)

    def create_json_params(self, specs: dict) -> str:
        """ Creates a json string from tool params specified in YAML
        """
        if 'params' in specs:
            return json.dumps(specs['params'], ensure_ascii=False)
        else:
            return ""

    def set_port(self, start_port: int = 5000, end_port: int = 8000):
        """ Finds an available port on the computer to send to subprocess
        """
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.bind(("", port))
                    self.port = str(port)
                except OSError as e:
                    print(f"Error: {e}")

    def start_subprocess(self):
        self.set_port()
        working_dir = os.path.dirname(self.tool_path)

        # Executable
        if self.interpreter is None:
            subprocess_args = [self.tool_path, self.port]
        else:
            subprocess_args = [self.interpreter, self.tool_path, self.port]

        self.process = subprocess.Popen(subprocess_args, stdin=subprocess.PIPE, cwd=working_dir)

        # Wait for process to start
        while self.process is None:
            pass

    def stop_subprocess(self):

        print("stopping tool process", self.process.pid)
        if self.process is not None:
            # TODO: should we use self.process.kill or terminate
            self.process.kill()
            self.process = None
        print("tool process stopped")

    def open_connection(self):
        # TODO: (important info of how to connect to tool)
        #  - We have to send an ack to make sure that we can communicate with the tool. That means that the tool has
        #    to wait for a message from immuneML the second it starts and send an ack back to immuneML
        #  - Once we have received an ack back, opening the connection is done and immuneML can continue with its
        #    functionality

        print("Connecting to tool…")
        attempts = 0
        context = None

        while True:
            if attempts > 10:
                print(f"Could not establish connection to tool after {attempts} attempts")
                return
            try:
                # Try establishing a connection
                context = zmq.Context()
                self.socket = context.socket(zmq.REQ)
                self.socket.connect("tcp://localhost:" + self.port)
                self.socket.send_string("")
                self.socket.recv()
                # If we reach this point we have been able to create a connection
                break
            except zmq.error.ZMQError:
                # Failed to establish connection, failed as a result of socket not being binded yet
                attempts += 1
                self.socket.close()
                context.term()
            time.sleep(1)  # add a sleep to give some time for the tool to connect

        print("Connected to tool")

    def close_connection(self):
        self.socket.close()

        # TODO: should we use self.context.term() as well?

    def execution_animation(self, process: subprocess):
        """Function creates an animation to give user feedback while process is running
        """

        num_dots = 0

        while process.poll() is None:
            sys.stdout.write('\rRunning subprocess{}   '.format('.' * num_dots))
            sys.stdout.flush()
            num_dots = (num_dots + 1) % 4
            time.sleep(0.5)

        sys.stdout.flush()
        sys.stdout.write("\rSubprocess finished")

    def show_process_output(self, ml_specs: dict):
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
