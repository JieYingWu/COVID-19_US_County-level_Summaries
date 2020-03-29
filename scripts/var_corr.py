# -*- coding: utf-8 -*-
"""
Finds the feature that correlates the most with the number of deaths across each state

//run it from the root as python scripts/var_corr.py

author: @shreya
"""

import pandas as pd
import numpy as np
import argparse
import os
import csv
from collections import OrderedDict


def preprocessing(df, excluded):
    df.dropna(thresh=df.shape[0] * 0.9, how='all', axis=1, inplace=True)
    data_cols = [col for col in df.columns.tolist() if col not in excluded]
    df[data_cols] = df[data_cols].astype('float')
    df['FIPS'] = df['FIPS'].astype(int)
    return df


def map_abbr_to_state(cases_data):
    cases_data['FIPS'] = cases_data['FIPS'].astype(int)
    df_ = cases_data.loc[(cases_data['FIPS'] % 1000 == 0) & (cases_data['FIPS'] != 0)]
    df_ = df_[['FIPS', 'STATE', 'AREA_NAME', 'infected']]
    df_.reset_index(drop=True, inplace=True)
    return df_


def main():
    parser = argparse.ArgumentParser(description='Check correlation')

    # file settings
    parser.add_argument('--data-dir', default='./data', help='data directory')
    parser.add_argument('--output-dir', default='./data', help='output directory')
    parser.add_argument('--threshold', default='10', help='threshold for infected cases across counties')

    args = parser.parse_args()
    if os.path.isdir(args.data_dir):
        counties_path = os.path.join(args.data_dir, 'counties.csv')
        cases_path = os.path.join(args.data_dir, 'cases.csv')
        
    if os.path.isdir(args.output_dir):
        output_path = os.path.join(args.output_dir, 'variable_correlation.csv')

    counties_data = pd.read_csv(counties_path)
    cases_data = pd.read_csv(cases_path)

    excluded = ['FIPS', 'Area_Name', 'State', 'Rural-urban_Continuum Code_2013', 'Urban_Influence_Code_2013',
                'Economic_typology_2015']

    counties_data = preprocessing(counties_data, excluded)
    # cases_data = preprocessing(cases_data, excluded)
    infected_by_county = cases_data[['FIPS', 'infected']]

    ### impute counties data with average value
    list_of_cols = [col for col in counties_data.columns.tolist() if col not in excluded]
    counties_data[list_of_cols] = counties_data[list_of_cols].apply(lambda x: x.fillna(x.mean()), axis=0)
    ### impute cases data with 0
    infected_by_county.fillna(0, inplace=True)

    ### Merging with infected data
    df_infect = pd.merge(counties_data, infected_by_county, how="inner", left_on='FIPS', right_on='FIPS')

    states = np.unique(df_infect['State'])

    corr_var = OrderedDict()

    for state in states:
        state_data = df_infect.loc[
            (df_infect['State'] == state) & (df_infect['FIPS'] % 1000 != 0)]  # excludes state data

        if state_data.shape[0] < 2:
            continue
        if state_data['infected'].sum() < int(args.threshold):
            continue
        state_data.drop(excluded, axis=1, inplace=True)
        var = state_data.corrwith(state_data['infected'])[:-1]
        corr_var[state] = var.idxmax()

    df_ = pd.DataFrame.from_dict(corr_var, orient='index',
                                 columns=['Most correlated variable'])
    df_['STATE'] = df_.index
    # print(df_.shape)

    final_ = map_abbr_to_state(cases_data)
    # print(final_.shape)

    df_final = pd.merge(final_, df_, how='right', left_on='STATE', right_on='STATE')
    # print(df_final_.shape)

    df_final.to_csv(output_path, index=False)


if __name__ == '__main__':
    main()