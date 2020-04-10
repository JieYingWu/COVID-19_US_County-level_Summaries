import os 
import sys
import csv
import argparse 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

import formatter

def clean_file(path):
    name = path.split('.')[0]
    clean_name = name + '_clean'
    df = pd.read_csv(path)

    df.dropna(subset=['FIPS'], inplace=True)
    df = df[df['FIPS'].notnull()]
    df = df.reset_index(drop=True)
    
    headers = df.columns.values

    print(df)
    for header in ['UID', 'iso2', 'iso3', 'code3', 'Lat', 'Long_', 'Combined_Key']:
        df = df.drop([header], axis = 1)
    print(headers)
    print(df)
    df.to_csv(clean_name+'.csv', index=False)



if __name__ == '__main__':
    path = '../raw_data/national/JHU_Infections_time_series/'
    os.chdir(path)
    confirmed_path = 'time_series_covid19_confirmed_US.csv'
    deaths_path = 'time_series_covid19_deaths_US.csv'
    clean_file(confirmed_path)
    clean_file(deaths_path)

    os.chdir('../../../')
    parser = argparse.ArgumentParser(description='data formatter')

    # file settings
    parser.add_argument('--raw-data-dir', default='./raw_data', help='directory containing raw data')
    parser.add_argument('--data-dir', default='./data', help='directory to write formatted data to')
    parser.add_argument('--threshold', default='20', help='threshold for relevant counties')
        
    args = parser.parse_args()

    formatter = formatter.Formatter(args)
    formatter.make_cases_data()
    
