import sys
import time
import socket


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
    def testing_func():
        pass

    """
    The tool should implement functions that must take a certain parameter 
    and return data in a specific format 
    """


ToolTest.main(sys.argv[1])
