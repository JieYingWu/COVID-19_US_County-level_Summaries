import numpy as np
import pandas as pd
import os


def create_aligned(input_file, output_file, skiprow=False):
    if skiprow:
        infections_data = pd.read_csv(input_file, skiprows=[1176])
    else:
        infections_data = pd.read_csv(input_file)

    day_of_first_case = []
    time_series = []
    headers = infections_data.columns.values.tolist()

    for row in infections_data.iterrows():
        values = row[1].to_numpy()
        inds = np.argwhere(values[4:] > 0)
        if inds.size == 0:
            day_of_first_case.append([np.nan])
            time_series.append([])
        else:
            ind = np.min(inds)
            day_of_first_case.append([headers[ind + 4]])
            time_series.append(values[ind + 4:])

    timeseries_data = pd.DataFrame(time_series)
    start_data = pd.DataFrame(day_of_first_case, columns=['Date of 1st case'])
    unchanged_data = infections_data[['countyFIPS', 'County Name', 'State', 'stateFIPS']]

    aligned_data = pd.concat([unchanged_data, start_data, timeseries_data], axis=1)

    aligned_data.to_csv(output_file, index=False, na_rep='NA')


if __name__ == '__main__':
    # for infections
    input_path = r'../raw_data/national/USAfacts_infections/covid_confirmed_usafacts.csv'
    output_path = os.path.join(os.path.dirname(input_path), 'covid_confirmed_usafacts_aligned.csv')

    create_aligned(input_path, output_path, skiprow=True)

    input_path = r'../raw_data/national/USAfacts_infections/covid_deaths_usafacts.csv'
    output_path = os.path.join(os.path.dirname(input_path), 'covid_deaths_usafacts_aligned.csv')

    create_aligned(input_path, output_path, skiprow=False)

    print('done')
