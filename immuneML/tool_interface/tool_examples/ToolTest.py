import sys
import time
import socket
from multiprocessing.connection import Client


class ToolTest:

    @staticmethod
    def main(json_data):
        host = socket.gethostname()
        port = 6000

        client_socket = socket.socket()

        attempts = 10

        try:
            client_socket.connect((host, port))
        except ConnectionRefusedError:
            print("could not connect")
            return
        else:
            print("Successfully connected")

        for i in range(0, 5):
            packet_data = f'Data packet {i}'
            client_socket.send(packet_data.encode())
            time.sleep(1)

        client_socket.send('stop connection'.encode())
        client_socket.close()

    @staticmethod
    def main2(json_data):
        print(f"Data in tool: {json_data}")

        # Start waiting for communication
        # Tool will send a request through localhost when it is started by immuneML

        active_connection = Client(('localhost', 6000), authkey=b'123')

        test_counter = 0
        test_counter_limit = 10
        running = True
        while running:
            print(f"Running tool iteration {test_counter}")
            active_connection.send('test')
            time.sleep(1)
            test_counter += 1
            if test_counter >= test_counter_limit:
                running = False

        active_connection.send("close connection")
        active_connection.close()

    @staticmethod
    def testing_func():
        pass

    """
    The tool should implement functions that must take a certain parameter 
    and return data in a specific format 
    """


ToolTest.main(sys.argv[1])
