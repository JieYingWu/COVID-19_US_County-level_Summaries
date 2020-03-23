# Draws ideas from https://towardsdatascience.com/modelling-the-coronavirus-epidemic-spreading-in-a-city-with-python-babd14d82fa2
# Focus on estimating the parameters based on socio-economics data

import torch
import numpy as np
from mlp import MLP

# Device information
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Model parameters
in_channels = 5
channels = [10, 10, 10]
out_channels = 2

# Training parameters
batch_size = 32
lr = 1.0e-4
n_epochs = 100
momentum = 0.9

# Checkpoint parameter
root = Path("checkpoints")
try:
    model_root = root / "models"
    model_root.mkdir(mode=0o777, parents=False)
except OSError:
    print("Model path exists")
use_previous_model = False
epoch_to_use = 0

# Make model, loss, optimizer, and scheduler
model = MLP(in_channels, out_channels, channels).to(device)
loss_fn = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum) 
scheduler = ReduceLROnPlateau(optimizer)

# Read existing weights for both G and D models
if use_previous_model:
    model_path = model_root / 'model_{}.pt'.format(epoch_to_use)
    if model_path.exists():
        state = torch.load(str(model_path))
        epoch = state['epoch'] + 1
        model.load_state_dict(state['model'])
        optimizer.load_state_dict(state['optimizer'])
        scheduler.load_state_dict(state['scheduler'])
        best_mean_error = state['error']
        print('Restored model, epoch {}'.format(epoch))
    else:
        print('Failed to restore model')
        exit()
else:
    epoch = 0
    best_mean_error = 0.0
        
save = lambda ep, model, model_path, error, optimizer, scheduler: torch.save({
    'model': model.state_dict(),
    'epoch': ep,
    'error': error,
    'optimizer': optimizer.state_dict(),
    'scheduler': scheduler.state_dict()
}, str(model_path))

    
for e in range(epoch, n_epochs):
    model.train()
