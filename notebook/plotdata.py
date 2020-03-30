import numpy as np
import pandas as pd
import sys
sys.path.insert(0, 'scripts/')
from formatter import Formatter
import timeseries
import csv
import argparse
from os.path import join, exists
from scipy.optimize import curve_fit

## Extract the timeseries from a pandas dataframe by fips
def get_timeseries(infections, deaths, fips):
    i = infections.loc[infections['countyFIPS'] == fips]
    i = i.values[0][5:].astype(np.float)
    i = i[~np.isnan(i)]
    d = deaths.loc[deaths['countyFIPS'] == fips]
    d = d.values[0][5:].astype(np.float)
    d = d[~np.isnan(d)]
    d = np.pad(d, (len(i) - len(d),0), 'constant', constant_values=(0,0))
    t = np.linspace(1, len(i), num=len(i))
    return t, i, d

## Fit an exponential model to the timeseries
def fit_exponential(x, a):
    y = np.exp(a*x)
    return y

## Define some error metric
def error(a, b):
    sq_err = ((a-b)**2).mean()
    return np.sqrt(sq_err)

def print_fit(name, param, cov, err):
    print(f"{name}'s growth factor is estimated to be {param} ({cov}) with error {err}")

## Preprocessing - Make a formatter that contains many counties data 
parser = argparse.ArgumentParser(description='data formatter')

# file settings
parser.add_argument('--raw-data-dir', default='./raw_data', help='directory containing raw data')
parser.add_argument('--data-dir', default='./data', help='directory to write formatted data to')
parser.add_argument('--threshold', default='20', help='threshold for relevant counties')
    
args = parser.parse_args()

# run
formatter = Formatter(args)

## First, we load the data and identify some counties we're interested in
## Let's go with King County, WA (where the first US case was identified), and NYC
infections = pd.read_csv(join(formatter.raw_data_dir, 'national/USAfacts_infections/covid_confirmed_usafacts_aligned.csv'))
deaths = pd.read_csv(join(formatter.raw_data_dir, 'national/USAfacts_infections/covid_deaths_usafacts_aligned.csv'))
fips = [53033, 36061]

## To get a general overview of the data, we can first plot them
#timeseries.plot_timeseries(infections, fips=fips, label='Infections')
#timeseries.plot_timeseries(deaths, fips=fips, label='Deaths')

## Let's take a deeper look at the data and see how the growth in these two counties compare
## Read out the timeseries in each county and we can calculate the growth rate
king_time, king_infections, king_deaths = get_timeseries(infections, deaths, fips[0])
nyc_time, nyc_infections, nyc_deaths = get_timeseries(infections, deaths, fips[1])

king_param, king_param_cov = curve_fit(fit_exponential, king_time, king_infections)
king_error = error(king_infections, fit_exponential(king_time, king_param))

nyc_param, nyc_param_cov = curve_fit(fit_exponential, nyc_time, nyc_infections)
nyc_error = error(nyc_infections, fit_exponential(nyc_time, nyc_param))

print_fit('King County', king_param[0], king_param_cov[0][0], king_error)
print_fit('New York City', nyc_param[0], nyc_param_cov[0][0], nyc_error)
              
## Extract the features from those counties
national_data = formatter.parse_national_data()
king_data = national_data[str(fips[1])]
nyc_data = national_data[str(fips[1])]
#print(king_data)
#print(nyc_data)











