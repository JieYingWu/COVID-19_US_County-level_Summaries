import numpy as np
import pandas as pd
import sys
sys.path.insert(0, 'scripts/')
from formatter import Formatter
import timeseries
import csv
import argparse
from os.path import join, exists


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

## Plot both the infections and deaths
#timeseries.plot_timeseries(infections, fips=fips, label='Infections')
#timeseries.plot_timeseries(deaths, fips=fips, label='Deaths')

## Extract the features from those counties
national_data = formatter.parse_national_data()
king_county_data = national_data[str(fips[1])]
nyc_data = national_data[str(fips[1])]
print(king_county_data)
print(nyc_data)

