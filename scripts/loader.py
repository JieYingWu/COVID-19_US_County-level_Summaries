
import numpy as np
from os.path import join, exists
from torch.utils.data import Dataset
import torch


class CoronavirusCases(Dataset):
  val_states = {'06'}           # California FIPS
  test_states = {'53'}          # Washington State FIPS
  train_states = set(str(i).zfill(2) for i in range(1, 100)
                     if str(i).zfill(2) not in val_states
                     and str(i).zfill(2) not in test_states)

  def __init__(self, data_dir, split='train', threshold=8, device='cuda'):
    """Return dataset entries with county info and estimated beta and gamma.

    :param path: 
    :param split: 
    :param threshold: 
    :returns: 
    :rtype: 

    """
    self.device = device
    self.threshold = threshold
    self.split = split
    counties = np.loadtxt(join(data_dir, 'counties.csv'))
    cases = np.loadtxt(join(data_dir, 'cases.csv'))  # fips, num infections, beta, gamma

    # get which rows correspond to this split
    which = []
    
    for i, row in enumerate(counties):
      if row[0][:2] in getattr(self, split + '_states') and int(cases[i, 1]) > threshold:
        which.append(i)

    self.counties = counties[which]
    self.cases = cases[which]

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
