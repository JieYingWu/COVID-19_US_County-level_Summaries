import numpy as np
import pandas as pd
import sys
sys.path.insert(0, 'scripts/')
from formatter import Formatter
import timeseries
import csv
import argparse
from os.path import join, exists
import utils

## Define some parameters
susceptible_factor = 0.8 
model = utils.fit_exponential

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

king_population = int(king_data['population'][6])*susceptible_factor
nyc_population = int(nyc_data['population'][6])*susceptible_factor

## To get a general overview of the data, we can first plot them
#timeseries.plot_timeseries(infections, fips=fips, label='Infections')
#timeseries.plot_timeseries(deaths, fips=fips, label='Deaths')

## Let's take a deeper look at the data and see how the growth in these two counties compare
## Read out the timeseries in each county and we can calculate the growth rate
king_time, king_infections, king_deaths = utils.get_timeseries(infections, deaths, fips[0])
nyc_time, nyc_infections, nyc_deaths = utils.get_timeseries(infections, deaths, fips[1])

king_infections_param, king_infections_param_cov, king_infections_pred, king_infections_error = utils.fit_timeseries(model, king_time, king_infections)
nyc_infections_param, nyc_infections_param_cov, nyc_infections_pred, nyc_infections_error = utils.fit_timeseries(model, nyc_time, nyc_infections)
king_deaths_param, king_deaths_param_cov, king_deaths_pred, king_deaths_error = utils.fit_timeseries(model, king_time, king_deaths)
nyc_deaths_param, nyc_deaths_param_cov, nyc_deaths_pred, nyc_deaths_error = utils.fit_timeseries(model, nyc_time, nyc_deaths)


utils.print_fit('King County infections', king_infections_param, king_infections_param_cov, king_infections_error)
utils.print_fit('New York City infections', nyc_infections_param, nyc_infections_param_cov, nyc_infections_error)
utils.print_fit('King County death', king_deaths_param, king_deaths_param_cov, king_deaths_error)
utils.print_fit('New York City deaths', nyc_deaths_param, nyc_deaths_param_cov, nyc_deaths_error)

utils.plot(king_infections, king_infections_pred, 'Infections')
utils.plot(nyc_infections, nyc_infections_pred, 'Infections')
utils.plot(king_deaths, king_deaths_pred, 'Infections')
utils.plot(nyc_deaths, nyc_deaths_pred, 'Infections')


