// New executable version
// This version uses the source code from Absolut

#include <iostream>
#include <fstream>
#include <dirent.h>
#include <cstring>
#include <unistd.h>
#include <zmq.hpp>
#include <nlohmann/json.hpp>
#include <experimental/filesystem>

#include "standalone_main_functions.h"

using namespace std;
namespace fs = std::experimental::filesystem;
using json = nlohmann::json;

struct InputData {
    std::string option;
    std::string antigen;
    std::string filename;
    int threads;
};

// Handles the input data received from immuneML by filling in an InputData struct
InputData getInputData(const std::string& jsonString) {
     // Parse the JSON string
    json j = json::parse(jsonString);

    std::cout << "j: " << j << std::endl;

    // Get the values
    InputData inputData;
    inputData.option = j["option"].get<std::string>();
    inputData.antigen = j["antigen"].get<std::string>();
    inputData.filename = j["filename"].get<std::string>();
    inputData.threads = j["threads"].get<int>();

    std::cout << "Printing values received from immuneML in Absolut" << std::endl;
    std::cout << "  - Option: " << inputData.option << std::endl;
    std::cout << "  - Antigen: " << inputData.antigen << std::endl;
    std::cout << "  - Filename: " << inputData.filename << std::endl;
    std::cout << "  - Threads: " << inputData.threads << std::endl;

    return inputData;
}

// This is not the most optimal solution, but because option2 does not return the name of the produced filed
// this is a temporary solution
std::string getDatasetPath(std::string antigen) {
    // Get the directory we are currently in
    std::string currDirPath = "";
    char buffer[PATH_MAX];
    if (getcwd(buffer, PATH_MAX) != nullptr) {
        currDirPath = buffer;
    }

    const char* dirPath = currDirPath.c_str();
    std::string filePath = "";
    DIR* dir = opendir(dirPath);

    if (dir) {
        dirent* file;

        // Substrings used to identify the dataset file produced
        const char* filenameSubstring = "FinalBindings_Process_";
        const char* antigenSubstring = antigen.c_str();

        // Search for file based on substrings
        while ((file = readdir(dir)) != nullptr) {
            if ((strstr(file->d_name, filenameSubstring) != nullptr) &&
                (strstr(file->d_name, antigenSubstring) != nullptr)) {
                filePath = std::string(dirPath) + "/" + std::string(file->d_name);
                std::cout << "FOUND THE FILEPATH: " << filePath << std::endl;
            }
        }
        closedir(dir);
    }

    return filePath;
}

int main(int argc, char* argv[]) {
    std::cout << "Running exectuable V2 for Absolut" << std::endl;

    // First, get the port number
    std::string port_number = argv[1];

    // Bind to the socket
    zmq::context_t context{1};
    zmq::socket_t socket{context, zmq::socket_type::rep};
    std::string port_string = "tcp://*:" + port_number;
    socket.bind(port_string);

    // Wait for a message from immuneML
    zmq::message_t request_1;
    (void) socket.recv(request_1, zmq::recv_flags::none);

    // Send an ack message back to immuneML
    std::string response_content = "{}";
    zmq::message_t response_1{response_content.size()};
    memcpy(response_1.data(), response_content.data(), response_content.size());
    socket.send(response_1, zmq::send_flags::none);

    // Receive the parameters from immuneML
    zmq::message_t request_2;
    (void) socket.recv(request_2, zmq::recv_flags::none);

    // ------- insert your code here -------

    // Get the parameters
    std::string json_string(static_cast<char*>(request_2.data()), request_2.size());
    InputData inputData = getInputData(json_string);

    // Using the filename, copy the file and insert it into currenty folder
    //std::string copied_file_from_input = tsv_dataset_to_absolut_file("cdr3_aa", inputData.filename, "absolut_ready_file.txt");

    // Turn tsv input file into an Absolut friendly txt file
    std::string tsv_to_absolut_file = tsv_dataset_to_absolut_file("cdr3_aa", inputData.filename, "absolut_ready_file.txt");

    // Call for the Absolut function
    option2(inputData.antigen, tsv_to_absolut_file, inputData.threads);

    std::string absolut_dataset = getDatasetPath(inputData.antigen);
    std::string absolut_dataset_to_tsv = txt_to_tsv(absolut_dataset, "absolut_results.tsv");

    // Filter dataset
    std::string filtered_dataset = filter_out_worse(absolut_dataset_to_tsv, "filtered_dataset.tsv");

    // Add new columns from absolut
    std::vector<std::string> columns_to_add = {"Slide", "Energy", "Structure"};
    std::string extended_dataset = add_columns_to_dataset(inputData.filename, filtered_dataset, columns_to_add, "extended_dataset.tsv");


    // Get the full path of the resulting dataset
    fs::path current_file_path = fs::canonical(__FILE__);
    fs::path current_dir = current_file_path.parent_path();
    std::string current_dir_str = current_dir.string();
    // Return the path to the produced dataset
    std::string dataset_path = current_dir_str + "/" + extended_dataset;

    std::cout << "Dataset path in c++ program: " << dataset_path << std::endl;

    json j;
    j["dataset"] = dataset_path;
    std::string dataset_path_reply = j.dump();
    zmq::message_t dataset_path_reply_msg(dataset_path_reply.size());
    memcpy(dataset_path_reply_msg.data(), dataset_path_reply.data(), dataset_path_reply.size());
    socket.send(dataset_path_reply_msg);


    return 0;
}
