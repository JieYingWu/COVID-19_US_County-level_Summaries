import os 
import sys
import csv 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

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
    
