from os.path import join, exists

import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

class CountyDataset(Dataset):
    def __init__(self, source_path, target_path, device):
        # Read in source and target csv and make sure they correspond
        source = np.genfromtxt(source_path, delimiter=',')
        target = np.genfromtxt(target_path, delimiter=',')
        assert(source.shape[0] == target.shape[0])

        # Remove FIPS, state, and county name columns
        source = source[:,3:]
        target = target[:,3:]

        # Convert rural-urban continuum code (1-9), 0 means no data
        ruc_category = source[:,0]
        ruc_category[np.isnan(ruc_category)] = 0
        ruc_category = torch.from_numpy(ruc_category).to(torch.int64)
        ruc_one_hot = F.one_hot(ruc_category, num_classes=10).float()
        
        # Convert urban influence code (1-12), 0 means no data
        ui_category = source[:,1]
        ui_category[np.isnan(ui_category)] = 0
        ui_category = torch.from_numpy(ui_category).to(torch.int64)
        ui_one_hot = F.one_hot(ui_category, num_classes=13).float()
        
        # Convert economic typology (0-5)
        # To be in line with the other categories, shifting the actual
        # numbers to be +1 so 0 can remain the missing data column
        et_category = source[:,2]
        et_category = et_category + 1
        et_category[np.isnan(et_category)] = 0
        et_category = torch.from_numpy(et_category).to(torch.int64)
        et_one_hot = F.one_hot(et_category, num_classes=7).float()
        
        # Combine the features
        source = torch.from_numpy(source[:,3:]).float()
        source = torch.cat((ruc_one_hot, ui_one_hot, et_one_hot, source), axis=1)
        
        self.source = source.to(device)
        self.target = torch.from_numpy(target).float().to(device)
        
    def __getitem__(self, i):
        return source[i,:],  target[i,:]

    def __len__(self, i):
        return source.size()[0]
