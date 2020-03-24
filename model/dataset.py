
import numpy as np
from os.path import join, exists
from torch.utils.data import Dataset
import torch
import torch.nn.functional as F


class CoronavirusCases(Dataset):

    
  def __init__(self, data_dir, split='train', threshold=8, device='cuda'):
    """Return dataset entries with county info and estimated beta and gamma.

    :param path: 
    :param split: 
    :param threshold: 
    :returns: 
    :rtype: 

    """
    val_states = {'06'}           # California FIPS
    test_states = {'53'}          # Washington State FIPS
    train_states = set(str(i).zfill(2) for i in range(1, 100)
                     if str(i).zfill(2) not in val_states
                     and str(i).zfill(2) not in test_states)

    self.device = device
    self.threshold = threshold
    self.split = split
    
    counties = np.genfromtxt(join(data_dir, 'counties.csv'), delimiter=',')
    counties = counties[1:,:]
    cases = np.genfromtxt(join(data_dir, 'cases.csv'), delimiter=',')
    cases = cases[1:,:]
                        
    print(cases.shape)
    print(counties.shape)
    
    # get which rows correspond to this split
    which = []
    for i, (row, case_row) in enumerate(zip(counties, cases)):
      if row[0][:2] in getattr(self, split + '_states') and float(cases[i, 1]) > threshold and float(case_row[1]) > threshold:
        which.append(i)
    
    self.counties = counties[which]
    self.cases = cases[which]
    
  def format_input(self, row):
    # Convert rural-urban continuum code (1-9), 0 means no data
    # Convert urban influence code (1-12), 0 means no data
    x = []
    for idx, num_classes in [(3, 10), (4, 13)]:
      x.append(np.eye(num_classes)[0] if row[idx] == 'NA' else np.eye(num_classes)[int(row[idx])])

    # Convert economic typology (0-5), offsetting by 1
    idx = 5
    num_classes = 7
    x.append(np.eye(num_classes)[0] if row[idx] == 'NA' else np.eye(num_classes)[int(row[idx]) + 1])

    id2 = np.eye(2)
    for idx in range(6, len(row)):
      if row[idx] == 'NA':
        x.append(id2[0])        # class 0 means data not available
        x.append([0])
      else:
        x.append(id2[0])        # class 1 means data available
        x.append([float(row[idx])])

    x = np.concatenate(x, axis=0).astype(np.float32)
    return x

  def format_output(self, row):
    y = row[2:4].astype(np.float32)
    return y
  
  def __getitem__(self, i):
    county = self.format_input(self.counties[i])
    case = self.format_output(self.cases[i])
    
    county = torch.from_numpy(county).float().to(self.device)
    case = torch.from_numpy(case).float().to(self.device)

    return county, case
    
  def __len__(self):
    return len(self.counties)


if __name__ == '__main__':
  cases = CoronavirusCases()
