import torch


class PyTorchMLP(torch.nn.Module):
    def __init__(self, in_features: int):
        super().__init__()
        self.layer = torch.nn.Sequential(
            torch.nn.Linear(in_features, 1, bias=True),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        return self.layer(x)

"""
    def __init__(self, in_features: int):
        super().__init__()
        self.layer = torch.nn.Linear(in_features, 1, bias=True)
        self.activation = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.layer(x)
        # squeeze() function is used when we want to remove single-dimensional entries from the shape of an array.
        # From shape (70,1) to (70,)
        #x = self.activation(x) #.squeeze()
        return x
"""