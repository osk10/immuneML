// This file contains a clear instruction on how a python script should communicate with immuneML
// It shows an example of how it could be written. The importance of this file is to show:
//   1. Handling the input data from immuneML
//   2. Handling socket connection with immuneML

#include <iostream>
#include <zmq.hpp>

using namespace std;

int main(int argc, char *argv[]) {

    // Program must take the port number as only program input
    std::string port_number = argv[1],

    // Bind to ZeroMQ socket
    zmq::context_t context{1};
    zmq::socket_t socket{context, zmq::socket_type::rep};
    std::string port_string = "tcp://*:" + port_number;
    socket.bind(port_string);

    // Wait for a message from immuneML. This will be empty
    zmq::message_t message;
    socket.recv(&message);

    // Send an acknowledgement message back. Should be empty
    zmq::message response;
    socket.send(response);


    // Receive the parameters from immuneML.
    // Sent as json string with parameters defined by the tool developers
    // The parameters must be defined and documented to enable the program to run
    // Example: {"parameter_1": "x", "parameter_2": "y"}

    zmq::message_t message;
    socket.recv(&message);

    std::string json_string(static_cast<char*>(message.data()), message.size());

    // ------------- Add your functionality here -------------

    // Use the parameters to run your functionality.
    // All response back to immuneML must be in json format - use socket.send_json()
}