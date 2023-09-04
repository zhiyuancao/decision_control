import torch.nn as nn


class SINCEEGNet(nn.Module):
    def __init__(self, num_class, l_num=125):
        super(SINCEEGNet, self).__init__()
        self.block1 = nn.Sequential()
        self.block1_conv = nn.Conv2d(
            in_channels=1,
            out_channels=8,
            kernel_size=(1, 64),
            padding=(0, 32),
            bias=False,
        )
        self.block1.add_module("conv1", self.block1_conv)
        self.block1.add_module("norm1", nn.BatchNorm2d(8))

        self.block2 = nn.Sequential()
        self.block2.add_module(
            "conv2",
            nn.Conv2d(
                in_channels=8, out_channels=16, kernel_size=(8, 1), groups=2, bias=False
            ),
        )
        self.block2.add_module("act1", nn.ELU())
        self.block2.add_module("pool1", nn.AvgPool2d(kernel_size=(1, 4)))
        self.block2.add_module("drop1", nn.Dropout(p=0.5))

        self.block3 = nn.Sequential()
        self.block3.add_module(
            "conv3",
            nn.Conv2d(
                in_channels=16,
                out_channels=16,
                kernel_size=(1, 16),
                padding=(0, 8),
                groups=16,
                bias=False,
            ),
        )
        self.block3.add_module(
            "conv4",
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=(1, 1), bias=False),
        )
        self.block3.add_module("norm2", nn.BatchNorm2d(16))
        self.block3.add_module("act2", nn.ELU())
        self.block3.add_module("pool2", nn.AvgPool2d(kernel_size=(1, 8)))
        self.block3.add_module("drop2", nn.Dropout(p=0.5))
        self.classify = nn.Sequential(nn.Linear(16 * l_num, num_class))

    def forward(self, x):
        x = x.view(x.size(0), 1, x.size(1), x.size(2))
        x = self.block1(x)
        x = self.block2(x)
        x = x[:, :, :, range(x.size(3) - 1)]  # 1.5s 749
        x = self.block3(x)
        x = x.view(x.size(0), -1)
        x = self.classify(x)
        return x
