import shutil
from unittest import TestCase

import numpy as np

from source.data_model.dataset.RepertoireDataset import RepertoireDataset
from source.environment.EnvironmentSettings import EnvironmentSettings
from source.pairwise_repertoire_comparison.PairwiseRepertoireComparison import PairwiseRepertoireComparison
from source.util.PathBuilder import PathBuilder
from source.util.RepertoireBuilder import RepertoireBuilder


class TestPairwiseRepertoireComparison(TestCase):

    def create_dataset(self, path: str) -> RepertoireDataset:
        filenames, metadata = RepertoireBuilder.build([["A", "B"], ["B", "C"], ["D"], ["E", "F"]], path)
        dataset = RepertoireDataset(filenames=filenames, metadata_file=metadata)
        return dataset

    def test_compare_repertoires(self):

        path = EnvironmentSettings.tmp_test_path + "pairwise_comparison_reps/"
        PathBuilder.build(path)

        dataset = self.create_dataset(path)

        extraction_fn = lambda repertoire: [{"sequence": seq.amino_acid_sequence} for seq in repertoire.sequences]
        comparison = PairwiseRepertoireComparison(["sequence"], ["sequence"], path, 4, extraction_fn)

        comparison_fn = lambda rep1, rep2: np.sum(np.logical_and(rep1, rep2)) / np.sum(np.logical_or(rep1, rep2))

        result = comparison.compare_repertoires(dataset, comparison_fn)

        self.assertTrue(np.array_equal(result, np.array([[1., 0.3333333333333333, 0., 0.], [0.3333333333333333, 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])))

        shutil.rmtree(path)