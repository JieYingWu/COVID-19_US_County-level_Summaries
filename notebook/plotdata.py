import numpy as np
import pandas as pd
import sys
sys.path.insert(0, 'scripts/')
from formatter import Formatter
import csv
import argparse
from os.path import join, exists


## First, we load the data
parser = argparse.ArgumentParser(description='data formatter')
raw_data_dir = './raw_data'

# file settings
parser.add_argument('--raw-data-dir', default='./raw_data', help='directory containing raw data')
parser.add_argument('--data-dir', default='./data', help='directory to write formatted data to')
parser.add_argument('--threshold', default='20', help='threshold for relevant counties')

args = parser.parse_args()
formatter = Formatter(args)

# nonzero infections
infections_filename = join(Formatter.raw_data_dir, 'national', 'JHU_Infections', 'cases_time_series_JHU.csv')
deaths_filename = join(Formatter.raw_data_dir, 'national', 'JHU_Infections', 'deaths_time_series_JHU.csv')
recovered_filename = join(Formatter.raw_data_dir, 'national', 'JHU_Infections', 'recovered_time_series_JHU.csv')
    
infections, deaths, recovered = Formatter._read_cases_data(infections_filename, deaths_filename, recovered_filename)

infections = pd.read_csv(r'../raw_data/national/USAfacts_infections/covid_confirmed_usafacts_aligned.csv')
