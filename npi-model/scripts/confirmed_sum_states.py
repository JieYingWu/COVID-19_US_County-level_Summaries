from os.path import join, exists
import sys
import numpy as np
import pandas as pd
import math


def compute_sums(filepath_from, filepath_to, selection):
    states_df = pd.read_csv('../data/us_data/states_order.csv', delimiter=';')
    df = pd.read_csv(filepath_from, delimiter=',', dtype={"FIPS": str})
    df['FIPS'] = df['FIPS'].apply(lambda x: str(x).zfill(5))
    fips_list = []

    #append all empty rows
    for index, row in states_df.iterrows():
        fips = str(row[0])
        name = str(row[1])
        fips_list.append([fips,name])

    #compute sums
    for fips, name in fips_list:
        if len(fips) == 5:
            regex_string = fips[:-3]
        else:
            regex_string = "0" + fips[:-3]

        extracted_df = df.loc[df.iloc[:, 0].str.startswith(regex_string)]
        header = [fips, name]
        total = list(extracted_df.sum()[2:])
        new_row = header + total
        state_total_string = pd.Series(new_row, index=df.columns)
        df = df.append(state_total_string, ignore_index=True)
    df.to_csv(filepath_to, index=False, header=True)
    return


def main():

    filepath_from = "../data/us_data/infections_timeseries.csv"
    filepath_to = "../data/us_data/infections_timeseries_w_states.csv"
    compute_sums(filepath_from, filepath_to, 'infection')

    filepath_from = "../data/us_data/deaths_timeseries.csv"
    filepath_to = "../data/us_data/deaths_timeseries_w_states.csv"
    compute_sums(filepath_from, filepath_to,'deaths')


if __name__ == '__main__':
    main()
