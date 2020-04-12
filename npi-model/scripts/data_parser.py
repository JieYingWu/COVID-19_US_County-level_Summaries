import numpy as np
import pandas as pd
import datetime as dt

from future.backports import datetime
from os.path import join, exists
from data_preprocess import *

pd.set_option('mode.chained_assignment', None)

def get_stan_parameters_by_county_us(num_counties, data_dir, show, interpolate=False, filter=False):

    df_cases, df_deaths, interventions = preprocessing_us_data(data_dir)

    ## select counties
    interventions = interventions[interventions['FIPS'] % 1000 != 0]

    if interpolate:
        df_cases = impute(df_cases)
        df_deaths = impute(df_deaths)

    if filter:
        df_cases, df_deaths = filter_negative_counts(df_cases, df_deaths, idx=2)

    df_cases, df_deaths, interventions, fips_list = filtering(df_cases, df_deaths, interventions, num_counties)

    dict_of_geo = {} ## map geocode
    for i in range(len(fips_list)):
        # comb_key = df_cases.loc[df_cases['FIPS'] == fips_list[i], 'Combined_Key'].to_string(index=False)
        dict_of_geo[i] = fips_list[i]

    #### drop non-numeric columns

    df_cases = df_cases.drop(['FIPS', 'Combined_Key'], axis=1)
    df_cases = df_cases.T  ### Dates are now row-wise
    df_cases_dates = np.array(df_cases.index)
    df_cases = df_cases.to_numpy()

    df_deaths = df_deaths.drop(['merge', 'FIPS', 'Combined_Key'], axis=1)
    df_deaths = df_deaths.T
    df_deaths = df_deaths.to_numpy()

    interventions.drop(['merge', 'FIPS', 'STATE', 'AREA_NAME'], axis=1, inplace=True)
    interventions_colnames = interventions.columns.values
    covariates1 = interventions.to_numpy()

    dict_of_start_dates, final_dict = primary_calculations(df_cases, df_deaths, covariates1, df_cases_dates, fips_list)

    final_dict['M'] = num_counties
    final_dict['p'] = len(interventions_colnames) - 1

    if show:
        for i in range(len(fips_list)):
            #print("County with FIPS {fips} has {num} days of data".format(fips=fips_list[i], num=final_dict['case']))
            print("County with FIPS {fips} has start date: ".format(fips=fips_list[i]), dict_of_start_dates[i])

    return final_dict, fips_list, dict_of_start_dates, dict_of_geo

def get_stan_parameters_by_state_us(num_states, data_dir, show, interpolate=False, filter=False):

    df_cases, df_deaths, interventions = preprocessing_us_data(data_dir)

    ## select states
    beginning_ids_int = np.unique(np.array(interventions['FIPS'] / 1000).astype(np.int))
    id_cols = ['FIPS', 'STATE', 'AREA_NAME', 'Combined_Key']
    int_cols = [col for col in interventions.columns.tolist() if col not in id_cols]
    int_cases_col = [col for col in df_cases.columns.tolist() if col not in id_cols]

    state_interventions = pd.DataFrame(columns=int_cols, index=beginning_ids_int * 1000)
    for i in beginning_ids_int:
        county_int = interventions.loc[(interventions['FIPS'] / 1000).astype(int) == i, :]
        ## set the latest date for intervention at any county as the date of intervention for the state
        state_interventions.loc[i * 1000, :] = county_int[int_cols].max(axis=0)
    state_interventions.insert(0, 'FIPS', state_interventions.index)

    beginning_ids_cases = np.unique(np.array(df_cases['FIPS'] / 1000).astype(np.int))
    cases_dates_cols = [col for col in df_cases.columns.tolist() if col not in id_cols]
    deaths_dates_cols = [col for col in df_deaths.columns.tolist() if col not in id_cols]
    state_cases = pd.DataFrame(columns=cases_dates_cols, index=beginning_ids_cases * 1000)
    state_deaths = pd.DataFrame(columns=deaths_dates_cols, index=beginning_ids_cases * 1000)

    ### get daily counts over states
    for i in beginning_ids_cases:
        county_case_int = df_cases.loc[(df_cases['FIPS'] / 1000).astype(int) == i, cases_dates_cols]
        county_death_int = df_deaths.loc[(df_deaths['FIPS'] / 1000).astype(int) == i, deaths_dates_cols]
        state_cases.loc[i * 1000, :] = county_case_int.sum(axis=0)
        state_deaths.loc[i * 1000, :] = county_death_int.sum(axis=0)
    state_cases.insert(0, 'FIPS', state_cases.index)
    state_deaths.insert(0, 'FIPS', state_deaths.index)

    if interpolate:
        state_cases = impute(state_cases)
        state_deaths = impute(state_deaths)

    if filter:
        state_cases, state_deaths = filter_negative_counts(state_cases, state_deaths, idx=1)

    state_cases, state_deaths, state_interventions, fips_list \
        = filtering(state_cases, state_deaths, state_interventions, num_states)

    dict_of_geo = {}
    for i in range(len(fips_list)):
        # comb_key = df_cases.loc[df_cases['FIPS'] == fips_list[i], 'Combined_Key'].to_string(index=False)
        dict_of_geo[i] = fips_list[i]

    ### Drop non-numeric columns
    state_cases = state_cases.drop(['FIPS'], axis=1)
    state_cases = state_cases.T  ### Dates are now row-wise
    state_cases_dates = np.array(state_cases.index)
    state_cases = state_cases.to_numpy()

    state_deaths = state_deaths.drop(['merge', 'FIPS'], axis=1)
    state_deaths = state_deaths.T
    state_deaths = state_deaths.to_numpy()

    state_interventions.drop(['merge', 'FIPS'], axis=1, inplace=True)
    state_interventions_colnames = state_interventions.columns.values
    covariates1 = state_interventions.to_numpy()

    dict_of_start_dates, final_dict = primary_calculations(state_cases, state_deaths,
                                                           covariates1, state_cases_dates, fips_list)

    final_dict['M'] = num_states
    final_dict['p'] = len(state_interventions_colnames) - 1

    if show:
        for i in range(len(fips_list)):
            print("State with FIPS {fips} has start date: ".format(fips=fips_list[i]), dict_of_start_dates[i])


    return final_dict, fips_list, dict_of_start_dates, dict_of_geo

def primary_calculations(df_cases, df_deaths, covariates1, df_cases_dates, fips_list, interpolate=True):
    """"
    Returns:
        final_dict: Stan_data used to feed main sampler
        dict_of_start_dates: Starting dates considered for calculations for the top N places
    """

    index = np.argmax(df_cases > 0)
    cum_sum = np.cumsum(df_deaths, axis=0) >= 10
    index1 = np.where(np.argmax(cum_sum, axis=0) != 0, np.argmax(cum_sum, axis=0), cum_sum.shape[0])
    index2 = index1 - 30
    start_dates = index1 + 1 - index2
    dict_of_start_dates = {}

    covariate1 = []
    covariate2 = []
    covariate3 = []
    covariate4 = []
    covariate5 = []
    covariate6 = []
    covariate7 = []

    cases = []
    deaths = []
    N_arr = []

    for i in range(len(fips_list)):
        i2 = index2[i]
        dict_of_start_dates[i] = df_cases_dates[i2]
        case = df_cases[i2:, i]
        death = df_deaths[i2:, i]
        assert len(case) == len(death)

        req_dates = df_cases_dates[i2:]
        covariates2 = []
        req_dates = np.array([dt.datetime.strptime(x, '%m/%d/%y').date() for x in req_dates])

        ### check if interventions were in place start date onwards
        for col in range(covariates1.shape[1]):
            covariates2.append(np.where(req_dates >= covariates1[i, col], 1, 0))
        covariates2 = np.array(covariates2).T

        N = len(case)
        N_arr.append(N)
        N2 = 100

        forecast = N2 - N

        if forecast < 0:
            print("FIPS: ", fips_list[i], " N: ", N)
            print("Error!!!! N is greater than N2!")
            N2 = N
        addlst = [covariates2[N - 1]] * (forecast)
        add_1 = [-1] * forecast ### padding

        case = np.append(case, add_1, axis=0)
        death = np.append(death, add_1, axis=0)
        cases.append(case)
        deaths.append(death)

        covariates2 = np.append(covariates2, addlst, axis=0)
        covariate1.append(covariates2[:, 0])  # stay at home
        covariate2.append(covariates2[:, 1])  # >50 gatherings
        covariate3.append(covariates2[:, 2])  # >500 gatherings
        covariate4.append(covariates2[:, 3])  # public scools
        covariate5.append(covariates2[:, 4])  # restaurant dine-in
        covariate6.append(covariates2[:, 5])  # entertainment/gym
        covariate7.append(covariates2[:, 6])  # federal guidelines

    covariate1 = np.array(covariate1).T
    covariate2 = np.array(covariate2).T
    covariate3 = np.array(covariate3).T
    covariate4 = np.array(covariate4).T
    covariate5 = np.array(covariate5).T
    covariate6 = np.array(covariate6).T
    covariate7 = np.array(covariate7).T
    cases = np.array(cases).T
    deaths = np.array(deaths).T
    #print(np.sum(cases<-1))
    #print(np.sum(deaths<-1))


    final_dict = {}
    final_dict['N0'] = 6
    final_dict['N'] = np.asarray(N_arr, dtype=np.int)
    final_dict['N2'] = N2
    final_dict['x'] = np.arange(1, N2+1)
    final_dict['cases'] = cases
    final_dict['deaths'] = deaths
    final_dict['EpidemicStart'] = np.asarray(start_dates).astype(np.int)
    final_dict['covariate1'] = covariate1
    final_dict['covariate2'] = covariate2
    final_dict['covariate3'] = covariate3
    final_dict['covariate4'] = covariate4
    final_dict['covariate5'] = covariate5
    final_dict['covariate6'] = covariate6
    final_dict['covariate7'] = covariate7

    return dict_of_start_dates, final_dict


# if __name__ == '__main__':
#     data_dir = 'data'
#     ## Europe data
#     get_stan_parameters_europe(data_dir, show=True)
#     print("***********************")
#     ## US data
#     get_stan_parameters_by_state_us(data_dir=data_dir, show=True, interpolate=True, filter = False, num_states = 5)
#     print("***********************")
#     get_stan_parameters_by_county_us(data_dir=data_dir, show=True, interpolate=True, filter = False, num_counties = 5)


