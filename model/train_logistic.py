"""
Meant to be run from the 'model' directory as `python3 train_logistic.py`

"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import ReduceLROnPlateau

from time import strftime
import tqdm
import numpy as np
from logistic import Net
from pathlib import Path
from dataset import CumulativeCoronavirusCases


def init_weights(m):
  if type(m) == nn.Linear:
    torch.nn.init.kaiming_uniform_(m.weight, nonlinearity='relu')
    m.bias.data.fill_(0.00)

    
# Device information
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Model parameters
county_dim = 1083 # 732
channels = [2048, 2048, 1024, 1024, 512, 512, 256, 256, 128, 128, 2]
# channels = [1024, 1024, 512, 512]
out_channels = 1
threshold = 8
deaths = False
max_cols = None

# Training parameters
batch_size = 32
lr = 1.0
n_epochs = 1000
validate_each = 5

# Make datasets and dataloaders
data_dir = '../data'
train_dataset = CumulativeCoronavirusCases(data_dir=data_dir, split='train', deaths=deaths, max_cols=max_cols,
                                           threshold=threshold, device=device)
val_dataset = CumulativeCoronavirusCases(data_dir=data_dir, split='val', deaths=deaths, max_cols=max_cols,
                                         threshold=threshold, device=device)
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(dataset=val_dataset, batch_size=batch_size, shuffle=True)

# Checkpoint parameter
root = Path("checkpoints")
timestamp = strftime('%Y-%m-%d-%H-%M-%S')
try:
    model_root = root / f"{timestamp}_models"
    model_root.mkdir(mode=0o777, parents=False)
except OSError:
    print("Model path exists")
use_previous_model = False
epoch_to_use = 0

# Make model, loss, optimizer, and scheduler
model = Net(train_dataset.num_counties, county_dim, channels=channels).to(device)
loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=lr) 
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
    model = model.apply(init_weights)

    
def save(ep, model, model_path, error, optimizer, scheduler):
  torch.save({
    'model': model.state_dict(),
    'epoch': ep,
    'error': error,
    'optimizer': optimizer.state_dict(),
    'scheduler': scheduler.state_dict()
  }, str(model_path))

  
for e in range(epoch, n_epochs):
  model.train()
  epoch_loss = 0.0
  step = 0.0
  tq = tqdm.tqdm(total=(len(train_loader) * batch_size))
  tq.set_description('Epoch {}, lr {}'.format(e, lr))
  
  for i, (x, y) in enumerate(train_loader):
    pred = model(x)
    loss = loss_fn(pred, y)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    epoch_loss += loss.item()
    step += 1
    tq.update(batch_size)
    tq.set_postfix(loss=' loss={:.5f}'.format(loss.item()))

  tq.set_postfix(loss=' loss={:.5f}'.format(epoch_loss / step))
  
  if e % validate_each == 0:
    all_val_loss = []
    
  with torch.no_grad():
    for j, (x, y) in enumerate(val_loader):
      pred = model(x)
      loss = loss_fn(pred, y)
      all_val_loss.append(loss.item())
    
    mean_loss = np.mean(all_val_loss)
    scheduler.step(mean_loss)
    tq.set_postfix(loss='val_loss={:.5f}'.format(mean_loss))

    model_path = model_root / "model_{}.pt".format(e)
    save(e, model, model_path, mean_loss, optimizer, scheduler)
    
  tq.close()
