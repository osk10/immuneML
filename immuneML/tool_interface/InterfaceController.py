import time
import socket
from multiprocessing.connection import Listener

from immuneML.tool_interface.ToolType import ToolType
from immuneML.tool_interface.InterfaceObject import InterfaceObject
from pathlib import Path
import subprocess


class InterfaceController:

    @staticmethod
    def interface_controller(tool_type: ToolType, ml_specs: dict):
        print(f"interface_controller specs received: {ml_specs}")
        if tool_type == ToolType.ML_TOOL:
            InterfaceController._ml_tool_caller(ml_specs)
        else:
            print(f"Invalid argument: {tool_type}")

    @staticmethod
    def _ml_tool_caller(ml_specs: dict):
        print("ml_tool_caller: looking for ml_method")
        InterfaceController._start_subprocess(ml_specs)

    @staticmethod
    def _start_subprocess(ml_specs: dict):
        #  Specify socket information
        server_socket = socket.socket()
        host = socket.gethostname()
        port = 6000

        #  Bind host and porth number
        server_socket.bind((host, port))

        #  Define and run subprocess (external tool)
        file = ml_specs.get("tool_path") + "/" + ml_specs.get("tool_execution_file")
        json_data_example = InterfaceController._create_JSON_data()
        proc = subprocess.Popen(["python", file, json_data_example], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        #  Listen for connections. Only listen to one client (tool) at a time
        #  Can be increased if we need multiple tools to run at the same time
        #  Tried to do this before starting subprocess, but this created a deadlock
        server_socket.listen(1)
        conn, address = server_socket.accept()

        #  Handle data from connected client (tool)
        while True:
            data = conn.recv(1024).decode()
            print(f"Data received from client: {data}")
            if data == 'EXIT CONNECTION':
                break

        conn.send('Closing connection'.encode())
        conn.close()

    @staticmethod
    def _create_JSON_data():
        # the point of this method is to generate a JSON file that contains information that other tools should be
        # able to understand and base their instructions on
        # that means that an external tool must be able to understand a specific JSON structure and implement that
        # to be able to call the right functions?

        interface_object = InterfaceObject("main")
        json_object = interface_object.getJson()
        return json_object
