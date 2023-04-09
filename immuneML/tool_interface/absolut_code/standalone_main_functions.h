#ifndef STANDALONE_MAIN_FUNCTIONS
#define STANDALONE_MAIN_FUNCTIONS

#include <iostream>
using namespace std;

//This requires the change of the function definition in the new file with where the default should be removed
void option2(string ID_antigen, string repertoireFile, int nThreads = 1, string prefix = string(""), int startingLine = 0, int endingLine = 1000000000);

std::string txt_to_tsv(std::string input_file, std::string output_file);
std::string add_columns_to_dataset(const std::string& first_file, const std::string& second_file, const std::vector<std::string>& columns_to_add, const std::string& output_file);
std::string tsv_dataset_to_absolut_file(string target_header, std::string input_file, std::string output_file);
std::string filter_out_worse(std::string input_file, std::string output_file);

#endif