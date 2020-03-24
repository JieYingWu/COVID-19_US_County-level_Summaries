
import numpy as np
from os.path import join, exists
from torch.utils.data import Dataset
import torch


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
    counties = np.loadtxt(join(data_dir, 'counties.csv'))
    counties = counties[1:,:]
    cases = np.loadtxt(join(data_dir, 'cases.csv'))  # fips, num infections, beta, gamma

    print(cases.shape)
    print(counties.shape)
    
    # get which rows correspond to this split
    which = []
    
    for i, row in enumerate(counties):
      if row[0][:2] in getattr(self, split + '_states') and int(cases[i, 1]) > threshold:
        which.append(i)

    print(which)
    counties = counties[which].astype(np.float64)
    cases = cases[which].astype(np.float64)
    print(counties[0])
    
    # Remove FIPS, state, and county name columns
    counties = counties[:,3:]
    cases = cases[:,3:]

    # Convert rural-urban continuum code (1-9), 0 means no data
    ruc_category = counties[:,0]
    ruc_category[np.isnan(ruc_category)] = 0
    ruc_category = torch.from_numpy(ruc_category).to(torch.int64)
    ruc_one_hot = F.one_hot(ruc_category, num_classes=10).float()
        
    # Convert urban influence code (1-12), 0 means no data
    ui_category = counties[:,1]
    ui_category[np.isnan(ui_category)] = 0
    ui_category = torch.from_numpy(ui_category).to(torch.int64)
    ui_one_hot = F.one_hot(ui_category, num_classes=13).float()
        
    # Convert economic typology (0-5)
    # To be in line with the other categories, shifting the actual
    # numbers to be +1 so 0 can remain the missing data column
    et_category = counties[:,2]
    et_category = et_category + 1
    et_category[np.isnan(et_category)] = 0
    et_category = torch.from_numpy(et_category).to(torch.int64)
    et_one_hot = F.one_hot(et_category, num_classes=7).float()
        
    # Combine the features
    counties = torch.from_numpy(counties[:,3:]).float()
    counties = torch.cat((ruc_one_hot, ui_one_hot, et_one_hot, counties), axis=1)
        
    self.counties = counties
    self.cases = cases
    
  def _convert_county_input(self, row):
    pass
    
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