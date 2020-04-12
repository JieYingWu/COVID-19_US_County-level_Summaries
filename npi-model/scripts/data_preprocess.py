import numpy as np
import pandas as pd
import datetime as dt
from os.path import join, exists

pd.set_option('mode.chained_assignment', None)

def filter_negative_counts(df_cases, df_deaths, idx):
    """"
    Returns:
        df_cases: Infections time series with no negative values
        df_deaths: Deaths time series with no negative values
    """
    ## drop if daily count negative
    sanity_check = df_cases.iloc[:, idx:].apply(lambda x: np.sum(x < 0), axis=1)
    drop_counties = sanity_check[sanity_check != 0].index
    df_cases = df_cases.drop(drop_counties)

    sanity_check2 = df_deaths.iloc[:, idx:].apply(lambda x: np.sum(x < 0), axis=1)
    drop_counties = sanity_check2[sanity_check2 != 0].index
    df_deaths = df_deaths.drop(drop_counties)

    ## filter only the FIPS that are present in both cases and deaths timeseries
    intersect = list(set(df_cases['FIPS']) & set(df_deaths['FIPS']))
    df_cases = df_cases[df_cases['FIPS'].isin(intersect)]
    df_deaths = df_deaths[df_deaths['FIPS'].isin(intersect)]

    return df_cases, df_deaths

def filtering(df_cases, df_deaths, interventions, num_counties):
    """"
    Returns:
        df_cases: Infections timeseries for top N places
        df_deaths: Death timeseries for top N places
        interventions: Intervention starting dates for top N places
        fips_list: FIPS of top N places
    """

    # Pick top 20 counties with most cases
    headers = df_cases.columns.values
    last_day = headers[-1]
    observed_days = len(headers[2:])

    df_cases = df_cases.sort_values(by=[last_day], ascending=False)
    df_cases = df_cases.iloc[:num_counties].copy()
    df_cases = df_cases.reset_index(drop=True)

    fips_list = df_cases['FIPS'].tolist()

    merge_df = pd.DataFrame({'merge': fips_list})
    df_deaths = df_deaths.loc[df_deaths['FIPS'].isin(fips_list)]
    # Select the 20 counties in the same order from the deaths dataframe by merging
    df_deaths = pd.merge(merge_df, df_deaths, left_on='merge', right_on='FIPS', how='outer')
    df_deaths = df_deaths.reset_index(drop=True)

    interventions = interventions.loc[interventions['FIPS'].isin(fips_list)]
    interventions = pd.merge(merge_df, interventions, left_on='merge', right_on='FIPS', how='outer')
    interventions = interventions.reset_index(drop=True)

    #print("Inside filtering function:", df_cases.shape, df_deaths.shape)
    return df_cases, df_deaths, interventions, fips_list

def check_monotonicity(L):
    is_monotonic = np.sum([x<= y for x, y in zip(L, L[1:])])
    return is_monotonic

def county_monotonicity(df):
    df1 = df.iloc[:, 2:].apply(check_monotonicity, axis=1)
    df1 = df1[df1!=(df.shape[1] - 3)]
    idx_row = {}
    return df.iloc[df1.index]['FIPS']


def simple_impute_data(arr):
    """
    Naive data imputation that does NOT yield a monotonically increasing timeseries

    """

    arr = arr.T
    for county in arr:
        for i, cell in enumerate(county[1:], 1):
            if cell != -1 and county[i + 1] != -1 and cell < county[i - 1]:
                county[i] = interpolate(county[i - 1], county[i + 1])
    arr = arr.T
    return arr


def advanced_impute_data(arr):
    """
    Make array monotonically increasing by linear interpolation
    Returns:
    - Imputed Array

    """

    arr = arr.T
    for county in arr:
        change_list = []
        # get first date of cases/deaths and skip it
        first = np.nonzero(county)[0]
        for i, cell in enumerate(county[1:], 1):
            if i < first[0]:
                continue
            # Special Case where series is decreasing towards the end
            if cell == -1 and len(change_list) != 1:
                first_idx = change_list[0]
                diff = county[first_idx] - county[first_idx - 1]
                new_value = county[first_idx] + diff

                for j, idx in enumerate(change_list[1:], 1):
                    new_value += diff
                    county[idx] = new_value
                break

            if cell != -1 and county[i + 1] != -1 and change_list == []:
                change_list.append(i)

            if i not in change_list:
                change_list.append(i)
            if cell > county[change_list[0]]:
                if len(change_list) >= 3:
                    # cut first and last value of change list
                    first_, *change_list, last_ = change_list
                    county[change_list[0]:change_list[-1] + 1] = interpolate(change_list,
                                                                             county[first_],
                                                                             county[last_])
                    change_list = [last_]
    arr = arr.T
    return arr

def impute(df):
    """
    Impute the dataframe directly via linear interpolation

    Arguments:
    - df : pandas DataFrame

    Returns:
    - imputes pandas DataFrame

    """
    FIPS_EXISTS = False
    COMBINED_KEY_EXISTS = False
    if 'FIPS' in df:
        fips = df['FIPS']
        fips = fips.reset_index(drop=True)
        df = df.drop('FIPS', axis=1)
        FIPS_EXISTS = True
    if 'Combined_Key' in df:
        combined_key = df ['Combined_Key']
        combined_key = combined_key.reset_index(drop=True)
        df = df.drop('Combined_Key', axis=1)
        COMBINED_KEY_EXISTS = True

    header = df.columns.values
    df = df.to_numpy()
    
    for county in df:
        change_list = []
        # get first date of cases/deaths and skip it
        first = np.nonzero(county)[0]
        if len(first) == 0:
            continue
        change_list.append(first[0])
        for i, cell in enumerate(county[1:], 1):
            if i < first[0]:
                continue

            if i not in change_list:
                change_list.append(i)

            # Special Case where series is decreasing towards the end
            if i == (len(county)-1) and len(change_list) > 1:
                first_idx = change_list[0]
                diff = county[first_idx] - county[first_idx - 1]
                new_value = county[first_idx] + diff

                for j, idx in enumerate(change_list[1:], 1):
                    county[idx] = new_value
                    new_value += diff
                break

            if cell > county[change_list[0]]:
                if len(change_list) >= 3:
                    # cut first and last value of change list
                    first_, *change_list, last_ = change_list
                    county[change_list[0]:change_list[-1] + 1] = interpolate(change_list,
                                                                             county[first_],
                                                                             county[last_]) 
                    change_list = [last_]
                else:
                    change_list = [change_list[-1]]
    df = pd.DataFrame(df, columns=header)
    if COMBINED_KEY_EXISTS:
        df = pd.concat([combined_key, df], axis=1)
    if FIPS_EXISTS:
        df = pd.concat([fips, df], axis=1)
    return df

def interpolate(change_list, lower, upper):
    """
    Interpolate values with length ofchange_list between two given values lower and upper

    """

    x = np.arange(1, len(change_list) + 1)
    xp = np.array([0, len(change_list) + 1])
    fp = np.array([lower, upper])
    interpolated_values = np.interp(x, xp, fp)
    return np.ceil(interpolated_values)

def preprocessing_us_data(data_dir):
    """"
    Loads and cleans data
    Returns:
        df_cases: Infections timeseries based on daily count
        df_deaths: Deaths timeseries based on daily count
        interventions: Interventions data with dates converted to date format
    """

    cases_path = join(data_dir, 'us_data/infections_timeseries.csv')
    deaths_path = join(data_dir, 'us_data/deaths_timeseries.csv')
    interventions_path = join(data_dir, 'us_data/interventions.csv')

    df_cases = pd.read_csv(cases_path)
    df_deaths = pd.read_csv(deaths_path)
    interventions = pd.read_csv(interventions_path)

    id_cols = ['FIPS', 'STATE', 'AREA_NAME']
    int_cols = [col for col in interventions.columns.tolist() if col not in id_cols]

    interventions.drop([0], axis=0, inplace=True)
    interventions.fillna(1, inplace=True)

    for col in int_cols: ### convert date from given format
        interventions[col] = interventions[col].apply(lambda x: dt.date.fromordinal(int(x)))

    #issues_cases = county_monotonicity(df_cases)
    #issues_deaths = county_monotonicity(df_deaths)
    def get_daily_counts(L):
        diff = np.array([y - x for x, y in zip(L, L[1:])])
        L[1:] = diff
        return L

    #### get daily counts instead of cumulative
    df_cases.iloc[:, 2:] = df_cases.iloc[:, 2:].apply(get_daily_counts, axis=1)
    df_deaths.iloc[:, 2:] = df_deaths.iloc[:, 2:].apply(get_daily_counts, axis=1)

    return df_cases, df_deaths, interventions
