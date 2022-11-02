import torch


class PyTorchLogisticRegression(torch.nn.Module):

    def __init__(self, in_features: int, zero_abundance_weight_init: bool):
        super().__init__()

        # input and output features. in = 21
        # Number of output = 1, sick or not sick? Or hidden layer? Check TODO
        self.linear = torch.nn.Linear(in_features, 1, bias=True)

        # Disabling gradient calculation is useful for inference, when you are sure that you will not call
        # Tensor.backward(). It will reduce memory consumption for computations that would otherwise have
        # requires_grad=True.
        with torch.no_grad():
            self.linear.bias.zero_()
            self.linear.weight.normal_(mean=0, std=1/in_features)
            if zero_abundance_weight_init:
                self.linear.weight[:, -1].fill_(0.0)

    def forward(self, x):
        return self.linear(x).squeeze()
