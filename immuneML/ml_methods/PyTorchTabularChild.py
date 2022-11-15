from pytorch_tabular.config import TrainerConfig
from pytorch_tabular.models import CategoryEmbeddingModelConfig

from immuneML.ml_methods.PyTorchTabularInterface import PyTorchTabularInterface


class PyTorchTabularChild(PyTorchTabularInterface):

    def __init__(self):
        super(PyTorchTabularChild, self).__init__()

    def _get_config(self):
        trainer_config = TrainerConfig(
            auto_lr_find=False,  # Runs the LRFinder to automatically derive a learning rate if set to True
            batch_size=32,
            max_epochs=100,
            gpus=None,  # index of the GPU to use. None means CPU
        )

        model_config = CategoryEmbeddingModelConfig(
            task="classification",
            layers="4096-4096-512",  # Number of nodes in each layer
            activation="LeakyReLU",  # Activation between each layers
            learning_rate=1e-3
        )

        return trainer_config, model_config
