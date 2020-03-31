import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

## Extract the timeseries from a pandas dataframe by fips
def get_timeseries(infections, deaths, fips, population=None):
    i = infections.loc[infections['countyFIPS'] == fips]
    i = i.values[0][5:].astype(np.float)
    i = i[~np.isnan(i)]
    d = deaths.loc[deaths['countyFIPS'] == fips]
    d = d.values[0][5:].astype(np.float)
    d = d[~np.isnan(d)]
    d = np.pad(d, (len(i) - len(d),0), 'constant', constant_values=(0,0))
    t = np.linspace(1, len(i), num=len(i))

    if population:
        i = i/population
        d = d/population
    return t, i, d

## Fit an exponential model to the timeseries
def fit_exponential(x, a):
    y = np.exp(a*x)
    return y

## Fit an exponential model to the timeseries
def fit_sigmoid(x, a):
    y = 1/(1+np.exp(-a*(x)))
    return y

## Define some error metric
def calc_error(a, b):
    sq_err = ((a-b)**2).mean()
    return np.sqrt(sq_err)

def print_fit(name, param, cov, err):
    print(f"{name}'s growth factor is estimated to be {param} ({cov}) with error {err}")

def plot(gt, pred, label='', county=''):
    plt.figure()
    plt.plot(gt, label='Measured')
    plt.plot(pred, label='Predicted')
    plt.xlabel('Days after first case')
    plt.ylabel('Number of ' + label)
    plt.title(county + ' ' + label)
    plt.legend()
    plt.show()

def fit_timeseries(model, time, data):
    param, param_cov = curve_fit(model, time, data)
    pred = model(time, param[0])
    error = calc_error(data, pred)
    return param, param_cov, pred, error
