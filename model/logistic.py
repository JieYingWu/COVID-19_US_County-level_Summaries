
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
    t0 = x[:, 0:1]
    a = x[:, 1:2]
    b = x[:, 2:3]
    c = x[:, 3:4]
    ts = x[:, 4:]
    out = a / (1 + torch.exp(b - c * (ts - t0)))
    # print(out.shape)
    return out

  
class Net(nn.Module):
  def __init__(self, num_counties, county_dim, channels=[1024, 1024]):
    super().__init__()
    self.num_counties = num_counties
    self.county_dim = county_dim
    self.county_mlp = MLP(in_channels=county_dim, out_channels=3, channels=channels, use_bn=True)
    # self.county_mlp = MLP(in_channels=county_dim, out_channels=1, channels=channels, use_bn=True)
    self.t0_table = nn.Parameter(data=1 * torch.ones(num_counties), requires_grad=True)
    self.logistic = LogisticModel()

  def forward(self, x):
    # county_index = x[:, 0].long()  # for getting t0 for this county
    # county_index_one_hot = F.one_hot(county_index, num_classes=self.num_counties)
    # t0 = torch.sum(self.t0_table.view(1, -1) * county_index_one_hot, dim=1, keepdim=True)

    # county = x[:, 1:1 + self.county_dim]                # rest of the data on this county
    county = x
    # ts = x[:, 1 + self.county_dim:]

    # inputs = torch.cat([county], dim=1)
    # qs = self.county_mlp(inputs)
    
    abc = self.county_mlp(county)
    return abc
    # lparams = torch.cat([t0, abc, ts], dim=1)
    # print(lparams)
    # qs = self.logistic(lparams)
    # print('abc', abc, abc.shape)
    # print('t0', t0, t0.shape)
    # print('q', q, q.shape)
    # return qs

