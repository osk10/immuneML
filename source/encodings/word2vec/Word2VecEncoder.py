# quality: gold
import abc
import hashlib
import os

import pandas as pd
from gensim.models import Word2Vec

from source.IO.dataset_export.PickleExporter import PickleExporter
from source.caching.CacheHandler import CacheHandler
from source.data_model.dataset.Dataset import Dataset
from source.data_model.encoded_data.EncodedData import EncodedData
from source.encodings.DatasetEncoder import DatasetEncoder
from source.encodings.EncoderParams import EncoderParams
from source.encodings.preprocessing.FeatureScaler import FeatureScaler
from source.encodings.word2vec.model_creator.KmerPairModelCreator import KmerPairModelCreator
from source.encodings.word2vec.model_creator.ModelType import ModelType
from source.encodings.word2vec.model_creator.SequenceModelCreator import SequenceModelCreator
from source.util.FilenameHandler import FilenameHandler
from source.util.ParameterValidator import ParameterValidator
from source.util.ReflectionHandler import ReflectionHandler


class Word2VecEncoder(DatasetEncoder):
    """

    Word2VecEncoder learns the vector representations of k-mers in the sequences in a repertoire from the
    context the k-mers appear in.
    It relies on gensim's implementation of Word2Vec and KmerHelper for k-mer extraction.

    Arguments:
        vector_size (int): The size of the vector to be learnt.
        model_type (:py:obj:`~source.encodings.word2vec.model_creator.ModelType.ModelType`):  The context which will be
            used to infer the representation of the sequence.
            If :py:obj:`~source.encodings.word2vec.model_creator.ModelType.ModelType.SEQUENCE` is used, the context of
            a k-mer is defined by the sequence it occurs in (e.g. if the sequence is CASTTY and k-mer is AST,
            then its context consists of k-mers CAS, STT, TTY)
            If :py:obj:`~source.encodings.word2vec.model_creator.ModelType.ModelType.KMER_PAIR` is used, the context for
            the k-mer is defined as all the k-mers that within one edit distance (e.g. for k-mer CAS, the context
            includes CAA, CAC, CAD etc.).
        k (int): The length of the k-mers used for the encoding.

    Specification:

    .. highlight:: yaml
    .. code-block:: yaml

        Word2Vec:
            vector_size: 16
            k: 3
            model_type: SEQUENCE

    """

    DESCRIPTION_REPERTOIRES = "repertoires"
    DESCRIPTION_LABELS = "labels"

    dataset_mapping = {
        "RepertoireDataset": "W2VRepertoireEncoder"
    }

    def __init__(self, vector_size: int, k: int, model_type: ModelType):
        self.vector_size = vector_size
        self.k = k
        self.model_type = model_type

    @staticmethod
    def _prepare_parameters(vector_size: int, k: int, model_type: str):
        location = "Word2VecEncoder"
        ParameterValidator.assert_type_and_value(vector_size, int, location, "vector_size", min_inclusive=1)
        ParameterValidator.assert_type_and_value(k, int, location, "k", min_inclusive=1)
        ParameterValidator.assert_in_valid_list(model_type.upper(), [item.name for item in ModelType], location, "model_type")
        return {"vector_size": vector_size, "k": k, "model_type": ModelType[model_type.upper()]}

    @staticmethod
    def build_object(dataset=None, **params):
        try:
            prepared_params = Word2VecEncoder._prepare_parameters(**params)
            encoder = ReflectionHandler.get_class_by_name(
                Word2VecEncoder.dataset_mapping[dataset.__class__.__name__], "word2vec/")(**prepared_params)
        except ValueError:
            raise ValueError("{} is not defined for dataset of type {}.".format(Word2VecEncoder.__name__,
                                                                                dataset.__class__.__name__))
        return encoder

    def encode(self, dataset, params: EncoderParams):
        encoded_dataset = CacheHandler.memo_by_params(self._prepare_caching_params(dataset, params),
                                                      lambda: self._encode_new_dataset(dataset, params))

        return encoded_dataset

    def _prepare_caching_params(self, dataset, params, vectors=None, description: str = ""):
        return (("dataset_id", dataset.identifier),
                ("dataset_filenames", tuple(dataset.get_example_ids())),
                ("dataset_metadata", dataset.metadata_file),
                ("dataset_type", dataset.__class__.__name__),
                ("labels", tuple(params["label_configuration"].get_labels_by_name())),
                ("vectors", hashlib.sha256(str(vectors).encode("utf-8")).hexdigest()),
                ("description", description),
                ("encoding", Word2VecEncoder.__name__),
                ("learn_model", params["learn_model"]),
                ("encoding_params", tuple([(key, params["model"][key]) for key in params["model"].keys()])), )

    def _encode_new_dataset(self, dataset, params):
        if params["learn_model"] is True and not self._exists_model(params):
            model = self._create_model(dataset=dataset, params=params)
        else:
            model = self._load_model(params)

        vectors = model.wv
        del model

        encoded_dataset = self._encode_by_model(dataset, params, vectors)

        self.store(encoded_dataset, params)

        return encoded_dataset

    @abc.abstractmethod
    def _encode_labels(self, dataset, params: EncoderParams):
        pass

    def _encode_by_model(self, dataset, params: EncoderParams, vectors):
        examples = CacheHandler.memo_by_params(self._prepare_caching_params(dataset, params, vectors,
                                                                            Word2VecEncoder.DESCRIPTION_REPERTOIRES),
                                               lambda: self._encode_examples(dataset, vectors, params))

        labels = CacheHandler.memo_by_params(self._prepare_caching_params(dataset, params, vectors, Word2VecEncoder.DESCRIPTION_LABELS),
                                             lambda: self._encode_labels(dataset, params))

        scaler_filename = params["result_path"] + FilenameHandler.get_filename("standard_scaling", "pkl")
        scaled_examples = FeatureScaler.standard_scale(scaler_filename, examples)

        encoded_dataset = self._build_encoded_dataset(dataset, scaled_examples, labels, params)
        return encoded_dataset

    def _build_encoded_dataset(self, dataset: Dataset, scaled_examples, labels, params: EncoderParams):

        encoded_dataset = dataset.clone()

        label_names = params["label_configuration"].get_labels_by_name()
        feature_names = [str(i) for i in range(scaled_examples.shape[1])]
        feature_annotations = pd.DataFrame({"feature": feature_names})

        encoded_data = EncodedData(examples=scaled_examples,
                                   labels={label: labels[i] for i, label in enumerate(label_names)},
                                   example_ids=[example.identifier for example in encoded_dataset.get_data()],
                                   feature_names=feature_names,
                                   feature_annotations=feature_annotations,
                                   encoding=Word2VecEncoder.__name__)

        encoded_dataset.add_encoded_data(encoded_data)
        return encoded_dataset

    @abc.abstractmethod
    def _encode_examples(self, encoded_dataset, vectors, params):
        pass

    def _load_model(self, params):
        model_path = self._create_model_path(params)
        model = Word2Vec.load(model_path)
        return model

    def _create_model(self, dataset, params):

        if self.model_type == ModelType.SEQUENCE:
            model_creator = SequenceModelCreator()
        else:
            model_creator = KmerPairModelCreator()

        model = model_creator.create_model(dataset=dataset,
                                           k=self.k,
                                           vector_size=self.vector_size,
                                           batch_size=params["batch_size"],
                                           model_path=self._create_model_path(params))

        return model

    def store(self, encoded_dataset, params: EncoderParams):
        PickleExporter.export(encoded_dataset, params["result_path"], params["filename"])

    def _exists_model(self, params: EncoderParams) -> bool:
        return os.path.isfile(self._create_model_path(params))

    def _create_model_path(self, params: EncoderParams):
        return params["result_path"] + "W2V.model"
