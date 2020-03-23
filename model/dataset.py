import torch
from torch.utils.data import Dataset

class CountyDataset(Dataset):
    def __init__(self, source_path, target_path):
        self.source = np.genfromtxt(source_path, delimiter=',')
        self.target = np.genfromtxt(target_path, delimiter=',')
        
        
