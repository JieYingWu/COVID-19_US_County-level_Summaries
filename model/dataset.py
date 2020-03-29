
import numpy as np
from os.path import join, exists
from torch.utils.data import Dataset
import torch
import torch.nn.functional as F
import re

class CoronavirusCases(Dataset):
  def __init__(self, data_dir='data', split='train', threshold=8, device='cpu'):
    """Return dataset entries with county beta, gamma, cases

    :param path: 
    :param split: 
    :param threshold: 
    :returns: 
    :rtype: 
    """
    self.val_states = {'53'}           # Washington State FIPS
    self.test_states = {'06'}          # California FIPS
    self.train_states = set(str(i).zfill(2) for i in range(1, 100)
                            if str(i).zfill(2) not in self.val_states
                            and str(i).zfill(2) not in self.test_states)

    self.device = device
    self.threshold = threshold
    self.split = split
    
    counties = np.genfromtxt(join(data_dir, 'counties.csv'), delimiter=',', skip_header=1, dtype=str)
    counties = counties[1:, :]
    
    cases = np.genfromtxt(join(data_dir, 'cases.csv'), delimiter=',', skip_header=1, dtype=str)
    cases = cases[1:, :]
    
    # get which rows correspond to this split
    which = []
    for i, (row, case_row) in enumerate(zip(counties, cases)):
      if (row[0][:2] in getattr(self, split + '_states')
          and float(cases[i, 1]) > threshold
          and float(case_row[1]) > threshold):
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
    y = row[4:6].astype(np.float32)
    return y
  
  def __getitem__(self, i):
    county = self.format_input(self.counties[i])
    case = self.format_output(self.cases[i])
    
    county = torch.from_numpy(county).float().to(self.device)
    case = torch.from_numpy(case).float().to(self.device)

    return county, case
  
  def __len__(self):
    return len(self.counties)


class CumulativeCoronavirusCases(Dataset):
  def __init__(self, data_dir='data', split='train', deaths=False, min_t=21, max_cols=None, threshold=8, device='cpu'):
    """Return dataset entries.

    Entry inputs consist of `county_vector`, used to predict parameters a, b, c; `county_index`,
    which is the index of the county in data/counties.csv, used to predict county dependent t0);
    and timestep `t`, passed to the predictive model layer, e.g. LogisticModel.

    The output ground truth is a 2-vector containing:
    number of infections at `t`, number of deaths at timestep `t`.

    This requires some preprocessing to index into properly, since the number of elements in the
    dataset is a combinatorial combination of the number of counties, and the number of non-zero
    timesteps in each individual county. We create an array `self.entries` which contains rows
    [county_index, t, num_cases at time t], where counties[county_index] is the county row,
    infections[case_index] is the timeseries of infections row, which t indexes into, and similarly
    for deaths.

    :param data_dir: 
    :param split: 
    :param deaths: whether to model deaths instead of infections
    :param min_t: what t is for the first column 
    :param max_cols: maximum column to load from infections/deaths data. If none, use all.
    :param threshold: 
    :param device: 'cpu' or 'cuda', etc

    """
    self.device = device
    self.threshold = threshold
    self.min_t = min_t
    self.split = split
    
    self.counties = np.genfromtxt(join(data_dir, 'counties.csv'), delimiter=',', skip_header=1, dtype=str)
    self.num_counties = self.counties.shape[0]
    self.interventions = np.genfromtxt(join(data_dir, 'interventions.csv'), delimiter=',',
                                       skip_header=1, dtype=str, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))

    if max_cols is None:
      usecols = None
    else:
      usecols = tuple(range(max_cols))
      
    if deaths:
      cases = np.genfromtxt(join(data_dir, 'deaths_timeseries.csv'), delimiter=',',
                            skip_header=1, dtype=str, usecols=usecols)
    else:
      cases = np.genfromtxt(join(data_dir, 'infections_timeseries.csv'), delimiter=',',
                            skip_header=1, dtype=str, usecols=usecols)

    self.cases = self.process_cases(cases)

    # build the entries table, int64
    entries = []
    for county_index, row in enumerate(self.counties):
      fips = self._get_fips(row[0])

      if self.cases.get(fips) is None or self.cases[fips][1][-1] < self.threshold:
        continue

      # train on the first n - 1 days, test on the last day
      ts, qs = self.cases[fips]
      if split == 'val' or split == 'test':
        entries.append([county_index, ts[-1], qs[-1]])
      else:
        for t, q in zip(ts[:-1], qs[:-1]):
          if q == 0:
            continue
          entries.append([county_index, t, q])
    self.entries = np.array(entries, dtype=np.int64)

  def _get_fips(self, x, default=None):
    if isinstance(x, str) and re.match(r'^\d{1,5}$', x) is not None:
      return x.zfill(5)
    elif type(x) is str and re.match(r'^\d{1,5}(?:\.\d+)$', x) is not None:
      return str(int(float(x))).zfill(5)
    elif isinstance(x, int):
      return str(x).zfill(5)
    else:
      return default

  def _is_county(self, x):
    """Tell whether the area x is a county equivalent.

    :param x: an area identifier, e.g. fips string
    :returns: 
    :rtype: 

    """
    fips = self._get_fips(x)
    assert len(fips) == 5
    return fips[2:] != '000'
    
  def process_cases(self, cases):
    """Process infections or deaths cases into a lookup table.
    
    :param cases: numpy array of strings
    :returns: dictionary from 5-digit fips to numpy float array of timeseries.
    :rtype: 

    """
    out = {}
    for row in cases:
      fips = self._get_fips(row[0])
      if fips is None or not self._is_county(fips):
        # print(f'skipping {row[:3]}')
        continue

      try:
        values = np.array([float(x) for x in row[4:]])
      except ValueError:
        continue
      
      timesteps = np.arange(self.min_t, self.min_t + values.shape[0])
      out[fips] = (timesteps, values)
    return out
    
  def format_county(self, row):
    # Convert rural-urban continuum code (1-9), 0 means no data
    # Convert urban influence code (1-12), 0 means no data
    x = []
    for idx, num_classes in [(3, 10), (4, 13)]:
      x.append(np.eye(num_classes)[0] if row[idx] == 'NA' else np.eye(num_classes)[int(row[idx])])

    # Convert economic typology (0-5), offsetting by 1
    idx = 5
    num_classes = 7
    x.append(np.eye(num_classes)[0] if row[idx] == 'NA' else np.eye(num_classes)[int(row[idx]) + 1])

    p = []                      # float variables present, 1 if present, 0 if NA
    i2 = np.eye(2)
    for idx in range(6, len(row)):
      if row[idx] == 'NA':
        p.append(i2[0])        # class 0 means data not available
        x.append([0])
      else:
        p.append(i2[1])        # class 1 means data available
        x.append([float(row[idx])])

    x = np.concatenate(x, axis=0)
    p = np.concatenate(p, axis=0)
    x = np.concatenate([x, p], axis=0)
    return x.astype(np.float32)

  def format_intervention(self, row):
    x = []
    p = []                      # 1 if present, 0 if NA

    i2 = np.eye(2)
    for idx in range(3, len(row)):
      if row[idx] == 'NA':
        p.append(i2[0])
        x.append([0])
      else:
        p.append(i2[1])
        x.append([float(row[idx])])

    x = np.concatenate(x, axis=0)
    p = np.concatenate(p, axis=0)
    x = np.concatenate([x, p], axis=0)
    return x.astype(np.float32)

  def format_output(self, row):
    y = row[4:6].astype(np.float32)
    return y
  
  def __getitem__(self, i):
    county_index, t, q = self.entries[i]
    
    county = self.format_county(self.counties[county_index])
    intervention = self.format_intervention(self.interventions[county_index])

    # county_index_one_hot = np.zeros(self.num_counties, np.float32)
    # county_index_one_hot[county_index] = 1

    # input to model is [t, [one hot county index], [interventions], [county_data]]
    # county and intervention have 732 features between them
    x = np.concatenate([[t], [county_index], county, intervention], axis=0)
    y = np.array([q])
        
    x = torch.from_numpy(x).float().to(self.device)
    y = torch.from_numpy(y).float().to(self.device)

    return x, y
  
  def __len__(self):
    return self.entries.shape[0]

  
if __name__ == '__main__':
  data = CumulativeCoronavirusCases('data', split='val', max_cols=10)
  print(f'num_counties: {data.num_counties}')
  for i in range(len(data)):
    print(f'{i}: y={data[i][1]}, x={data[i][0].shape}')
  # print(f'{i}: y={data[i][1]}, {data[i][0][1 + data.num_counties:].shape}')
