import numpy as np


## Extract the timeseries from a pandas dataframe by fips
def get_timeseries(infections, deaths, fips, population):
    i = infections.loc[infections['countyFIPS'] == fips]
    i = i.values[0][5:].astype(np.float)
    i = i[~np.isnan(i)]
    d = deaths.loc[deaths['countyFIPS'] == fips]
    d = d.values[0][5:].astype(np.float)
    d = d[~np.isnan(d)]
    d = np.pad(d, (len(i) - len(d),0), 'constant', constant_values=(0,0))
    t = np.linspace(1, len(i), num=len(i))
    return t, i/population, d/population

## Fit an exponential model to the timeseries
def fit_exponential(x, a):
    y = np.exp(a*x)
    return y

## Fit an exponential model to the timeseries
def fit_sigmoid(x, a, b):
    y = 1/(1+np.exp(-a*x-b))
    return y

## Define some error metric
def error(a, b):
    sq_err = ((a-b)**2).mean()
    return np.sqrt(sq_err)

def print_fit(name, param, cov, err):
    print(f"{name}'s growth factor is estimated to be {param} ({cov}) with error {err}")
