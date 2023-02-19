#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>
#include <unistd.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;
namespace fs = std::filesystem;

// Make sure to compile with: g++ -std=c++17 main.cpp -o main
// This is because we want to rundt c++ version 17 to make sure that the program works

std::string createJsonString() {  
    // The interface needs to have documentation on how the data needs to be returned 
    json j;
    j["path"] = "/Users/jorgenskimmeland/Documents/aar5/Master/ToolTest/dataset_directory";
    j["dataset_file"] = "dataset_example.txt";

    return j.dump();
}


int main(int argc, char* argv[]) {
    // Handle input 
    if (argc != 2) {
       std::cerr << "Usage: " << argv[0] << " <json_string>" << std::endl;
       return 1; 
    }

    // Parse the JSON string from the command-line argument 
    std::string json_str(argv[1]);
    json data = json::parse(json_str);

    //std::cout << data.dump();
    std::cout << createJsonString();

    // Create directory 
    /*std::string directory_name = "dataset_directory";
    
    if (fs::exists(directory_name) != true) {
        fs::create_directory(directory_name);
    }

    std::string jsonString = createJsonString();
    std::cout << jsonString << std::endl; */

    return 0;
}

