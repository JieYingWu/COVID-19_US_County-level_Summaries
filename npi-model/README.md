![](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/blob/master/npi-model/results/plots/states.gif)
## This Weeks Predications

| Washington State | 05/07/20 | 05/08/20 | 05/09/20 | 05/10/20 | 05/11/20 | 05/12/20 | 05/13/20 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cases |  228121  |  238986  |  250405  |  262406  |  275020  |  288282  |  291  |
| Deaths |  799  |  835  |  872  |  911  |  952  |  995  |  0  |

| New York State | 05/07/20 | 05/08/20 | 05/09/20 | 05/10/20 | 05/11/20 | 05/12/20 | 05/13/20 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cases |  130627254  |  151216998  |  175070684  |  202708629  |  234734556  |  271849031  |  314865087  |
| Deaths |  77309  |  89339  |  103252  |  119344  |  137959  |  159495  |  184411  |

| Maryland | 05/07/20 | 05/08/20 | 05/09/20 | 05/10/20 | 05/11/20 | 05/12/20 | 05/13/20 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cases |  12650  |  12978  |  13318  |  13670  |  14034  |  14411  |  14802  |
| Deaths |  84  |  86  |  88  |  90  |  92  |  94  |  96  |

| California | 05/07/20 | 05/08/20 | 05/09/20 | 05/10/20 | 05/11/20 | 05/12/20 | 05/13/20 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cases |  66759  |  70048  |  73507  |  77146  |  80975  |  85005  |  89245  |
| Deaths |  225  |  236  |  247  |  259  |  271  |  284  |  297  |

This repository is a Python port of the model proposed by report 13 from the MRC Centre for Global Infectious Disease Analysis, Imperial College London. The original code in R is available at: https://github.com/ImperialCollegeLondon/covid19model. Since we started the project, they have also added Python support and a notebook. We keep our code for its additional visualizations in Python and integration with our US county-level dataset. We also use their data here to validate our model, that we can reproduce their results. 

We provide...
* Support to run this model on the US state and county level
* Code to visualize the model fit with confidence intervales
* Plotting tools of how US interventions have affected modeled Rt

![](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/blob/master/npi-model/results/plots/usa/deaths53000.jpg)
![](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/blob/master/npi-model/results/plots/usa/infections53000.jpg)
![](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/blob/master/npi-model/results/plots/usa_interventions/Rt_state_53000.png)


Words of warning: We have noticed that the time series of the reported cases and deaths are of inconsistent quality; for example, our cumulative time series of cases and death counts are not monotonically increasing (so, checks have been implemented for the same). For days where the case or death count is negative, we interpolate neighbouring days for that value.

Additionally, fits to the US-county level data is less certain than the European Countries considered by the original model as there are fewer cases in most counties than any of the European countries. We also provide state-level analysis for more similar comparison. 

## Dependencies
* pystan (this requires Cython compiler - https://pystan.readthedocs.io/en/latest/installation_beginner.html)
Pystan is only partially supported on Windows: https://pystan.readthedocs.io/en/latest/windows.html **(Tip: Use Anaconda!!)**
* Python 3

## To Run
For US data, call `python scripts/base.py data <europe/US_state/US_county> <num of regions>` in the base directory and it will save the summary over runs in the results folder.
