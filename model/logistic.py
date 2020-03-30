
"""

Learn county-dependent parameters a, b, c such that the cumulative number of cases (or deaths) can be modeled as:

Qt = a / (1 + exp(b - c(t - t0)))

where t is the current time-step and t_0 is the timestep of the first case or death.

"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from mlp import MLP


class LogisticModel(nn.Module):
  def forward(self, x):
    t = x[:, 0]
    t0 = x[:, 1]
    a = x[:, 2]
    b = x[:, 3]
    c = x[:, 4]
    out = a / (1 + torch.exp(b - c * (t - t0)))
    return out.view(-1, 1)

  
class BertalanffyModel(nn.Module):
  def forward(self, x):
    t = x[:, 0]
    t0 = x[:, 1]
    a = x[:, 2]
    b = x[:, 3]
    c = x[:, 4]
    out = a * torch.pow(1 - torch.exp(- b * (t - t0)), c)
    return out.view(-1, 1)

  
class Net(nn.Module):
  def __init__(self, num_counties, in_channels, channels=[1024, 1024]):
    super().__init__()
    self.num_counties = num_counties
    # self.county_mlp = MLP(in_channels=in_channels - 2, out_channels=3, channels=channels, use_bn=True)
    self.county_mlp = MLP(in_channels=in_channels - 1, out_channels=1, channels=channels, use_bn=True)
    self.t0_table = nn.Parameter(data=21 * torch.ones(num_counties), requires_grad=True)
    self.logistic = LogisticModel()

  def forward(self, x):
    t = x[:, 0:1]                   # current timestep
    county_index = x[:, 1].long()  # for getting t0 for this county
    county_index_one_hot = F.one_hot(county_index, num_classes=self.num_counties)
    county = x[:, 2:]                # rest of the data on this county

    t0 = torch.sum(self.t0_table.view(1, -1) * county_index_one_hot, dim=1, keepdim=True)
    t = t - t0
    inputs = torch.cat([t, county], dim=1)
    q = self.county_mlp(inputs)
    # abc = self.county_mlp(county)
    # lparams = torch.cat([t, t0, abc], dim=1)
    # print(lparams)
    # q = self.logistic(lparams)
    # print('abc', abc, abc.shape)
    # print('t0', t0, t0.shape)
    # print('q', q, q.shape)
    return q

