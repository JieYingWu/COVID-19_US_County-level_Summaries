import torch
import torch.nn as nn


class MLP(nn.Module):
    def __init__(self, in_channels=5, out_channels=2, channels=[10, 10], use_bn=False):
        super(MLP, self).__init__()
        layers = []

        # Make an arbitrary number of layers depending on the input
        if len(channels) < 1:
            layers.append(nn.Linear(in_channels, out_channels))
        else:
            layers.append(nn.Linear(in_channels, channels[0]))
            if use_bn:
                layers.append(nn.BatchNorm1d(channels[0]))
            layers.append(nn.ReLU())
            for i in range(len(channels)-1):
                layers.append(nn.Linear(channels[i], channels[i+1]))
                if use_bn:
                    layers.append(nn.BatchNorm1d(channels[i+1]))
                layers.append(nn.ReLU())
            layers.append(nn.Linear(channels[-1], out_channels))
        self.layers = nn.Sequential(*layers)
                               
    def forward(self, x):
        return self.layers(x)

    
# Test various layers initialization
if __name__ == "__main__":
    x = torch.tensor([1,2]).float().unsqueeze(0)
    print(x.size())
    model = MLP(2,3,[10,10,5,2])
    y = model(x)
    print(y)
                          
