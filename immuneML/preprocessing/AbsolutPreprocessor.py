from pathlib import Path
import pandas as pd
import csv

from immuneML.preprocessing.Preprocessor import Preprocessor
from immuneML.data_model.dataset.RepertoireDataset import RepertoireDataset


class AbsolutPreprocessor(Preprocessor):
    """ TODO: this processor should be removed and fully replaced by a ToolPreprocessor that only calls for tool

    """
    def __init__(self, result_path: Path = None):
        super().__init__(result_path)

    def process_dataset(self, dataset: RepertoireDataset, result_path: Path) -> RepertoireDataset:
        pass

    def keeps_example_count(self) -> bool:
        pass

    def txt_to_tsv(self, file_path: str) -> str:
        # Read the text file with pandas
        df = pd.read_csv(file_path, sep='\t', skiprows=[0])

        # Write the DataFrame to a TSV file without the header
        df.to_csv('example.tsv', sep='\t', index=False)

        return ""

    def add_column_to_dataset(self, column_id: str, original_file: str, file_with_column: str):
        """ Extracts the column wanted from the absolut dataset and inserts data into immuneML dataset
        This expects both files to be files in tsv format

        original_file: the original file without column
        file_with_column: the file containing the column we want to extract
        """
        dataframe1 = pd.read_csv(original_file, sep='\t')
        dataframe2 = pd.read_csv(file_with_column, sep='\t')
        column_to_add = dataframe2[column_id]

        result = pd.concat([dataframe1, column_to_add], axis=1)
        result.to_csv('result.tsv', sep='\t', index=False)  # TODO: the name of the file should be the originals

    # TODO: rewrite this to use pandas - simplifies it alot
    def tsv_dataset_to_absolut_file(self, column_id: str, input_file: str, output_file: str) -> str:
        """ Extracts the column of CDR3 data in a dataset and creates a new file in txt format

        Returns the path of the new data file
        """

        # TODO: give the file a name that fits better
        with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:

            tsv_reader = csv.reader(in_file, delimiter='\t')
            header = next(tsv_reader)
            column_index = header.index(column_id)

            row_index = 1
            for row in tsv_reader:
                out_file.write('{}\t{}\n'.format(row_index, row[column_index]))
                row_index += 1

        # TODO: find the path of this file
        return ""

    def filter_out_worse(self, input_file: str):
        dataframe = pd.read_csv(input_file, sep='\t')

        # Remove rows where the condition is false, aka not the best
        dataframe = dataframe[dataframe['Best'] == True]

        # Write modified dataframe back to tsv file
        dataframe.to_csv("example-kopi-2.tsv", sep='\t', index=False)
