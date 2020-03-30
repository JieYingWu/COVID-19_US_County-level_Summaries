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
import utils

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

## Extract the features from those counties
national_data = formatter.parse_national_data()
king_data = national_data[str(fips[0])]
nyc_data = national_data[str(fips[1])]

king_population = int(king_data['population'][6])
nyc_population = int(nyc_data['population'][6])

## To get a general overview of the data, we can first plot them
#timeseries.plot_timeseries(infections, fips=fips, label='Infections')
#timeseries.plot_timeseries(deaths, fips=fips, label='Deaths')

## Let's take a deeper look at the data and see how the growth in these two counties compare
## Read out the timeseries in each county and we can calculate the growth rate
king_time, king_infections, king_deaths = utils.get_timeseries(infections, deaths, fips[0], king_population)
nyc_time, nyc_infections, nyc_deaths = utils.get_timeseries(infections, deaths, fips[1], nyc_population)

king_param, king_param_cov = curve_fit(utils.fit_sigmoid, king_time, king_infections)
king_error = utils.error(king_infections, utils.fit_sigmoid(king_time, king_param[0], king_param[1]))

nyc_param, nyc_param_cov = curve_fit(utils.fit_sigmoid, nyc_time, nyc_infections)
nyc_error = utils.error(nyc_infections, utils.fit_sigmoid(nyc_time, nyc_param[0], nyc_param[1]))

utils.print_fit('King County', king_param, king_param_cov, king_error)
utils.print_fit('New York City', nyc_param, nyc_param_cov, nyc_error)
              
