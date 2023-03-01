// Main program compiled into an executable that the immuneML tool interface can connect with
// Must be run inside the Absolut src folder
#include <iostream>
#include <unistd.h>
#include <cstdlib>
#include <cstdio>
#include <fstream>

using namespace std;

int main(int argc, char* argv[]) {
    /*
    if (argc != 1) {
    std::cout << "{Failed}" << std::endl;
    return 1;
    }
    */
    std::cout << "Running program" << std::endl;

    std::string exec = "../src/AbsolutNoLib";
    std::string arg = "repertoire";
    std::string antigen = "1FBI";
    std::string filename = "miniSetCDR3-TESTING.txt";
    std::string threads = "3";
    std::string command = exec + " " + arg + " " + antigen + " " + filename + " " + threads;


    // ----- Testing new code, running the new program as a subprocess -----
    const char* command2 = "../src/AbsolutNoLib repertoire 1FBI miniSetCDR3-TESTING.txt 3";
    FILE* pipe = popen(command2, "r");
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

    // Testing function call
    //option2("1FBI", "miniSetCDR3-TESTING.txt", 3);
    //option2("1FBI", "miniSetCDR3-TESTING.txt", 1, "", 0, 1000000000);

    return 0;
}