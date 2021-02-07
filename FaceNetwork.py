import torch
from torch import nn

class FaceNetwork(nn.Module):
    def __init__(self):
        super(FaceNetwork, self).__init__()

        self.cnn_layers = nn.Sequential(
            # Defining a 2D convolution layer
            nn.Conv2d(in_channels = 1, out_channels = 8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(8),
            nn.Sigmoid(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # Defining another 2D convolution layer
            nn.Conv2d(in_channels = 8, out_channels = 16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(16),
            nn.Sigmoid(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Defining another 2D convolution layer
            nn.Conv2d(in_channels = 16, out_channels = 16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(16),
            nn.Sigmoid(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Defining another 2D convolution layer
            nn.Conv2d(in_channels = 16, out_channels = 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(4),
            nn.Sigmoid(),
            # nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.linear_layers = nn.Sequential(
            nn.Linear(in_features = 1024, out_features = 100),
            nn.Linear(in_features = 100, out_features = 5)
        )

    def forward(self, x):
        x = self.cnn_layers(x)
        x = x.reshape(-1, self.num_flat_features(x))
        x = self.linear_layers(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
