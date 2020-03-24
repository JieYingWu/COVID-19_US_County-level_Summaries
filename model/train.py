# Draws ideas from https://towardsdatascience.com/modelling-the-coronavirus-epidemic-spreading-in-a-city-with-python-babd14d82fa2
# Focus on estimating the parameters based on socio-economics data

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import ReduceLROnPlateau

import tqdm
import numpy as np
from mlp import MLP
from pathlib import Path
from dataset import CoronavirusCases


# Device information
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Model parameters
in_channels = 274
channels = [256, 128, 2]
out_channels = 2

# Training parameters
batch_size = 32
lr = 1.0e-4
n_epochs = 100
momentum = 0.9

# Make datasets and dataloaders
data_dir = '../data'
train_dataset = CoronavirusCases(data_dir, split='train', device=device)
val_dataset = CoronavirusCases(data_dir, split='val', device=device)
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(dataset=val_dataset, batch_size=batch_size, shuffle=False)

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


print("WARNING - using random train set. Should set to a more reasonable split")    
for e in range(epoch, n_epochs):
    model.train()
    epoch_loss = 0.0
    step = 0.0

    tq = tqdm.tqdm(total=(len(train_loader) * batch_size))
    tq.set_description('Epoch {}, lr {}'.format(e, lr))
    
    for i, (counties, cases) in enumerate(train_loader):
        pred = model(counties)
        loss = loss_fn(pred, cases)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        epoch_loss += loss
        step += 1
        tq.update(batch_size)
        tq.set_postfix(loss=' loss={:.5f}'.format(loss))

    tq.set_postfix(loss=' loss={:.5f}'.format(epoch_loss/step))

    if e % validate_each == 0:
        all_vall_loss = []
    
        with torch.no_grad():
            for j, (counties, cases) in enumerate(val_loader):
                pred = model(counties)
                loss = loss_fn(pred, cases)
                all_val_loss.append(loss.item())
                
        mean_loss = np.mean(all_val_loss)
        scheduler.step(mean_loss)
        model_path = model_root/"model_{}.pt".format(e)
        save(e, model, model_path, mean_loss, optiizer, scheduler)
        
