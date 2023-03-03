// Main program compiled into an executable that the immuneML tool interface can connect with
// Must be run inside the Absolut src folder
#include <iostream>
#include <unistd.h>
#include <cstdlib>
#include <cstdio>
#include <fstream>
#include <nlohmann/json.hpp>

/* JSON format required
{
    "option": "repertoire",
    "antigen": "1FBI",
    "filename": ""
    "threads":

}*/

using namespace std;
namespace fs = std::filesystem;

using json = nlohmann::json;

// Struct containing the data received from immuneML
struct InputData {
    std::string target_directory;
    std::string option;
    std::string antigen;
    std::string filename;
    std::string threads;
};


// Handles the input data received from immuneML by filling in an InputData struct
InputData getJSON(std::string jsonString) {
    // Parse the JSON string
    json j = json::parse(jsonString);

    std::cout << j << std::endl;

    // Get the values
    InputData inputData;
    inputData.option = j["option"].get<std::string>();
    inputData.antigen = j["antigen"].get<std::string>();
    inputData.filename = j["filename"].get<std::string>();
    inputData.threads = std::to_string(j["threads"].get<int>());

    std::cout << "Printing values received from immuneML in Absolut" << std::endl;
    std::cout << "  - Option: " << inputData.option << std::endl;
    std::cout << "  - Antigen: " << inputData.antigen << std::endl;
    std::cout << "  - Filename: " << inputData.filename << std::endl;
    std::cout << "  - Threads: " << inputData.threads << std::endl;

    return inputData;
}

std::string getDatasetPath(std::string antigen) {
    fs::path cwd = fs::current_path();
    std::string dir_path = cwd.string();
    std::string filenameSubstring = "FinalBindings_Process_";

    // Look through the files in the directory
    for (const auto& entry : fs::directory_iterator(dir_path)) {
        // Check if the filename constains the substring and the antigen substring
        if (entry.path().filename().string().find(filenameSubstring) != std::string::npos &&
        entry.path().filename().string().find(antigen) != std::string::npos) {
            std::string curr_path = entry.path().string();
            return curr_path;
        }
    }
    return "Could not find file and move to different directory";
}

int main(int argc, char* argv[]) {
    std::cout << "Running program" << std::endl;

    // Check for valid input from immuneML
    if (argc != 2) {
        std::cout << "Arg length: " << argc << std::endl;
        std::cout << "{Failed: Require JSON string of specified format}" << std::endl;
        return 1;
    }

    InputData inputData = getJSON(argv[1]);

    // ----- Testing new code, running the new program as a subprocess -----
    const char* command2 = "../src/AbsolutNoLib repertoire 1FBI miniSetCDR3-TESTING.txt 3";

    // Concatenates the strings
    std::string concatenatedData = "../src/AbsolutNoLib " + inputData.option + " " + inputData.antigen + " " + inputData.filename + " " + inputData.threads;
    std::cout << "Concatenated string command: " << concatenatedData << std::endl;

    const char* command_from_input = concatenatedData.c_str();
    FILE* pipe = popen(command_from_input, "r");
    if (!pipe) {
        std::cerr << "Error: popen failed" << std::endl;
        return 1;
    }

    std::cout << "Trying to read from process execution in c++ program" << std::endl;
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
        std::cout << buffer;
    }
    pclose(pipe);

    //Get the path of the dataset produced
    std::string dataset_path = getDatasetPath(inputData.antigen);
    std::cout << "Dataset path: " << dataset_path << std::endl;
    return 0;
}