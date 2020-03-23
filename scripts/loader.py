
from os.path import join, exists
from torch.utils.data import Dataset


class CoronavirusCases(Dataset):
  val_states = ['06000']           # California FIPS
  test_states = ['53000']          # Washington State FIPS
  
  def __init__(self, path, split='train', threshold=8):
    """Return dataset entries with county info and estimated beta and gamma.

    :param path: 
    :param split: 
    :param threshold: 
    :returns: 
    :rtype: 

    """
    pass
  
  def __getitem__(self, i):
    pass

  def __len__(self, i):
    pass
