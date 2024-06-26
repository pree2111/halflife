# -*- coding: utf-8 -*-
"""BNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12wVkpSVW7MrXTCl-psc7s9ozxn58kkid
"""

pip install torchbnn

import numpy as np
from sklearn import datasets
import torch
import torch.nn as nn
import torch.optim as optim
import torchbnn as bnn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive', force_remount = True)

df = pd.read_csv('/content/drive/MyDrive/BNN/TensorSetNvsHL.csv')

print(df)

X = df['N']
Y = df['T1/2']

xt = torch.from_numpy(X.values)
yt = torch.from_numpy(Y.values)

pip install pyro-ppl

from torch.optim import Adam

AdamArgs = {'lr': 1e-3}
optimizer = Adam(bayesian_nn.parameters(), **AdamArgs)
scheduler = pyro.optim.ExponentialLR({'optimizer': optimizer, 'optim_args': AdamArgs, 'gamma': 0.996})
svi = SVI(bayesian_nn, bayesian_nn, scheduler, loss=Trace_ELBO())

# Assuming xt is your input data
xt = xt.float()

import torch
import torch.nn as nn
import pyro
import pyro.distributions as dist
from pyro.infer import SVI, Trace_ELBO
from pyro.nn import PyroModule, PyroSample
import pyro.optim as pyro_optim

class BayesianNN(PyroModule):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(BayesianNN, self).__init__()
        self.fc1 = PyroModule[nn.Linear](input_dim, hidden_dim)
        self.fc1.weight = PyroSample(dist.Normal(0., 1.).expand([hidden_dim, input_dim]).to_event(2))
        self.fc1.bias = PyroSample(dist.Normal(0., 1.).expand([hidden_dim]).to_event(1))

        self.fc2 = PyroModule[nn.Linear](hidden_dim, output_dim)
        self.fc2.weight = PyroSample(dist.Normal(0., 1.).expand([output_dim, hidden_dim]).to_event(2))
        self.fc2.bias = PyroSample(dist.Normal(0., 1.).expand([output_dim]).to_event(1))

    def forward(self, x, y=None):
        # Define forward pass
        hidden = torch.relu(self.fc1(x))
        output = self.fc2(hidden)
        # If training, return distribution over output, else return mean prediction
        with pyro.plate("data", x.shape[0]):
            obs = pyro.sample("obs", dist.Normal(output.squeeze(-1), 0.1), obs=y.squeeze(-1))
        return output

# Example usage
input_dim = 1
hidden_dim = 10
output_dim = 1

# Instantiate the model
bayesian_nn = BayesianNN(input_dim, hidden_dim, output_dim)

# Define loss function
loss_fn = Trace_ELBO()

# Define Pyro optimizer
optimizer = pyro_optim.Adam({"lr": 0.01})

# Define SVI (Stochastic Variational Inference) object
svi = SVI(bayesian_nn, pyro.infer.autoguide.AutoDiagonalNormal(bayesian_nn), optimizer, loss=loss_fn)

# Assuming xt and yt are your input and target tensors
xt = torch.randn(100, input_dim)  # Example input tensor
yt = torch.randn(100, output_dim)  # Example target tensor

# Convert target tensor to the appropriate data type
yt = yt.float()

# Training loop
num_epochs = 1000
for epoch in range(num_epochs):
    # Forward pass
    loss = svi.step(xt, yt)
    if epoch % 100 == 0:
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss:.4f}")





