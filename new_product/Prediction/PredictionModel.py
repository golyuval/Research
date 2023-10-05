import torch
from torch import nn
from torch import optim

# Define a neural network for profit prediction
class ProfitPredictionModel(nn.Module):

    def __init__(self, input_size):
        super(ProfitPredictionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, in_):
        out_ = self.relu(self.fc1(in_))
        out_ = self.relu(self.fc2(out_))
        out_ = self.fc3(out_)
        return out_


def init_Model(df, loss=nn.MSELoss()):

    input_size = df.shape[1] - 1  # Number of input features
    model = ProfitPredictionModel(input_size)
    criterion = loss
    optimizer = optim.Adam(model.parameters(), lr=0.06)

    return input_size, model, criterion, optimizer