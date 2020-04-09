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
