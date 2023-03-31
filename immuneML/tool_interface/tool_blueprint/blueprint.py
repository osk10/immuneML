# This file contains a clear instruction on how a python script should communicate with immuneML
# It shows an example of how it could be written. The importance of this file is to show:
#   1. Handling the input data from immuneML
#   2. Handling socket connection with immuneML

import zmq
import sys


def main():
    # Program must take the port number as only program input
    port_number = sys.argv[1]

    # Bind to ZeroMQ socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*" + port_number)

    # Wait for a message from immuneML. This will be empty
    socket.recv_json()

    # Send an acknowledgement message back. Must be json format and should be empty
    socket.send_json("")

    # Receive the parameters from immuneML.
    # Sent as json string with parameters defined by the tool developers
    # The parameters must be defined and documented to enable the program to run
    # Example: {"parameter_1": "x", "parameter_2": "y"}
    program_parameters = socket.recv_json()

    # ------------- Add your functionality here -------------

    # Use the parameters to run your functionality.
    # All response back to immuneML must be in json format - use socket.send_json()


if __name__ == "__main__":
    """ Your program receives a port number from immuneML. This is used to establish connection with immuneML
    """
    main()
