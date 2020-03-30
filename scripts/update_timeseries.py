import os 
import sys
import csv 

import pandas as pd 
import numpy as np


def merge(cleaned_file):
    p1 = cleaned_file
    pc = 'cases_time_series_JHU.csv'
    pd_ = 'deaths_time_series_JHU.csv'

    d1 = pd.read_csv(p1)
    dc = pd.read_csv(pc)
    dd = pd.read_csv(pd_)


    headers = d1.columns.values

    key = d1[headers[4]][1]
    new = {key: d1['Confirmed']}
    new_2 = {key:d1['Deaths']}

    d_new = pd.DataFrame(data=new)
    d_new_2 = pd.DataFrame(data=new_2)

    cases_new = pd.concat([dc, d_new], axis=1)
    deaths_new = pd.concat([dd, d_new_2], axis=1)

    cases_new.to_csv(pc, index=False)
    deaths_new.to_csv(pd_, index=False)


def clean_file(path):
    p1 = path 
    name = p1.split('.')[0]
    
    pc = 'cases_time_series_JHU.csv'
    pd_ = 'deaths_time_series_JHU.csv'

    d1 = pd.read_csv(p1)
    d1_org = d1.copy()
    dc = pd.read_csv(pc)
    dd = pd.read_csv(pd_)

    # only consider us counties
    d1 = d1.sort_values('FIPS')
    d1.dropna(subset=['FIPS'], inplace=True)
    d1 = d1[d1['FIPS'].notnull()]
    d1 = d1.reset_index(drop=True)
    
    headers = d1.columns.values

    for header in ['Lat', 'Long_', 'Combined_Key']:
        d1 = d1.drop([header], axis = 1)

    offset = []
    for i in range(len(dc)):
        if dc.loc[i, 'FIPS'] != d1.loc[i, 'FIPS']:
            d1 = insert_row(d1, i, dc.loc[i, 'FIPS'], dc.loc[i, 'Admin2'], dc.loc[i, 'Province_State'])

    date = d1.loc[2,'Last_Update'][5:10].split('-')
    date = '_'.join(reversed(date))
    name = name +'_'
    p1_save_clean = '.'.join([name + date + '_clean', 'csv'])
    p1_save = '.'.join([name + date, 'csv'])
    d1_org.to_csv(p1_save, index=False)
    d1.to_csv(p1_save_clean, index=False)
    return p1_save



def insert_row(df, index, fips, admin, state):
    df1 = df[0:index]
    df2 = df[index:]  
    df1.loc[index] = ([fips, admin, state, 'US','NA','NA','NA','NA','NA']) 
   
    # Concat the two dataframes 
    df_result = pd.concat([df1, df2]) 
   
    # Reassign the index labels 
    df_result.index = [*range(df_result.shape[0])] 
   
    # Return the updated dataframe 
    return df_result

if __name__ == '__main__':
    os.chdir('../raw_data/national/JHU_Infections/')
    
    #file_path = 'cases.csv'
    #clean_file_path = clean_file(file_path)
    clean_file_path = 'cases_29_03_clean.csv'
    merge(clean_file_path)
