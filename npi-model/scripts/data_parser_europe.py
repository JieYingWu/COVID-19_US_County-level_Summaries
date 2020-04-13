import numpy as np
import pandas as pd
import datetime as dt

from future.backports import datetime
from os.path import join, exists

pd.set_option('mode.chained_assignment', None)

def get_data_europe(data_dir, show):
    """
    Returns in a dict:
    M; // number of countries
    N0; // number of days for which to impute infections
    N[M]; // days of observed data for country m. each entry must be <= N2
    N2; // days of observed data + # of days to forecast
    x[N2]; // index of days (starting at 1)
    cases[N2,M]; // reported cases
    deaths[N2, M]; // reported deaths -- the rows with i > N contain -1 and should be ignored
    EpidemicStart[M];
    p; //intervention dates
    covariate1, ...., covariate7 //covariate variables

    """
    imp_covid_dir = join(data_dir, 'europe_data/COVID-19-up-to-date.csv')
    imp_interventions_dir = join(data_dir, 'europe_data/interventions.csv')

    interventions = pd.read_csv(imp_interventions_dir, encoding='latin-1')
    covid_up_to_date = pd.read_csv(imp_covid_dir, encoding='latin-1')

    mod_interventions = interventions.iloc[0:11, 0:8] ##only meaningful data for interventions

    mod_interventions.sort_values('Country', inplace=True)

    ### if intervention dates are after lockdown, set them to lockdown date
    for col in mod_interventions.columns.tolist():
        if col == 'Country' or col == 'lockdown':
            continue
        col1 = pd.to_datetime(mod_interventions[col], format='%Y-%m-%d').dt.date
        col2 = pd.to_datetime(mod_interventions['lockdown'], format='%Y-%m-%d').dt.date
        mod_interventions[col] = np.where(col1 > col2, col2, col1).astype(str)

    countries = mod_interventions['Country'].to_list()
    date_cols = [col for col in mod_interventions.columns.tolist() if col != 'Country']

    ###Initialize variables
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
    start_dates = []

    dict_of_start_dates = {}
    dict_of_geo = {}

    for country in countries:
        d1 = covid_up_to_date.loc[covid_up_to_date['countriesAndTerritories'] == country, :]
        covariates1 = mod_interventions.loc[mod_interventions['Country'] == country, date_cols]
        df_date = pd.to_datetime(d1['dateRep'], format='%d/%m/%Y').dt.date
        d1.loc[:, 'Date'] = df_date

        d1 = d1.sort_values(by=['Date']) ##sort by dates
        d1.reset_index(drop=True, inplace=True)

        ## get first day with number of cases >0
        index = (d1['cases'] > 0).idxmax()
        ## get first day with cumulative sum of deaths >=10
        index1 = (d1['deaths'].cumsum() >= 10).argmax()
        ## consider one month before
        index2 = index1 - 30
        idx = countries.index(country)
        dict_of_geo[idx] = country
        dict_of_start_dates[idx] = dt.datetime.strftime(d1['Date'][index2], format='%m-%d-%Y')
        start_dates.append(index1 + 1 - index2)

        d1 = d1.loc[index2:]
        case = d1['cases'].to_numpy()
        death = d1['deaths'].to_numpy()
        if show:
            print("{Country} has {num} days of data".format(Country=country, num=len(d1['cases'])))
            print("Start date for {Country}: ".format(Country=country), dict_of_start_dates[idx])

        ### check if interventions were in place from start date onwards
        for col in date_cols:
            covid_date = pd.to_datetime(d1['dateRep'], format='%d/%m/%Y').dt.date
            int_data = datetime.datetime.strptime(covariates1[col].to_string(index=False).strip(), '%Y-%m-%d')
            # int_date = pd.to_datetime(covariates1[col], format='%Y-%m-%d').dt.date
            d1[col] = np.where(covid_date.apply(lambda x: x >= int_data.date()), 1, 0)

        N = len(d1['cases'])
        N_arr.append(N)
        N2 = 75  ##from paper (number of days needed for prediction)
        forecast = N2 - N

        if forecast < 0:
            print("Country: ", country, " N: ", N)
            print("Error!!!! N is greater than N2!")
            N2 = N
            forecast = N2 - N

        covariates2 = d1[date_cols]
        covariates2.reset_index(drop=True, inplace=True)
        covariates2 = covariates2.to_numpy()
        addlst = [covariates2[N - 1]] * (forecast) ##padding
        add_1 = [-1] * forecast

        covariates2 = np.append(covariates2, addlst, axis=0)
        case = np.append(case, add_1, axis=0)
        death = np.append(death, add_1, axis=0)
        cases.append(case)
        deaths.append(death)

        covariate1.append(covariates2[:, 0])  # schools_universities
        covariate2.append(covariates2[:, 1])  # travel_restrictions
        covariate3.append(covariates2[:, 2])  # public_events
        covariate4.append(covariates2[:, 3])  # sports
        covariate5.append(covariates2[:, 4])  # lockdwon
        covariate6.append(covariates2[:, 5])  # social_distancing
        covariate7.append(covariates2[:, 6])  # self-isolating if ill

    covariate1 = np.array(covariate1).T
    covariate2 = np.array(covariate2).T
    covariate3 = np.array(covariate3).T
    covariate4 = np.array(covariate4).T
    covariate5 = np.array(covariate5).T
    covariate6 = np.array(covariate6).T
    covariate7 = np.array(covariate7).T
    cases = np.array(cases).T
    deaths = np.array(deaths).T

    #covariate2 = 0 * covariate2  # remove travel ban
    #covariate5 = 0 * covariate5  # remove sports
    covariate2 = covariate7  # self-isolating if ill
    covariate4 = np.where(covariate1 + covariate3 + covariate5 + covariate6 + covariate7 >= 1, 1, 0)  # any intervention

    covariate7 = 0  # models should take only one covariate

    final_dict = {}

    final_dict['M'] = len(countries)
    final_dict['N0'] = 6
    final_dict['N'] = np.asarray(N_arr).astype(np.int)
    final_dict['N2'] = N2
    final_dict['x'] = np.arange(1, N2+1)
    final_dict['cases'] = cases
    final_dict['deaths'] = deaths
    final_dict['EpidemicStart'] = np.asarray(start_dates)
    final_dict['p'] = len(mod_interventions.columns) - 1
    final_dict['covariate1'] = covariate1
    final_dict['covariate2'] = covariate2
    final_dict['covariate3'] = covariate3
    final_dict['covariate4'] = covariate4
    final_dict['covariate5'] = covariate5
    final_dict['covariate6'] = covariate6
    final_dict['covariate7'] = covariate7

    return final_dict, countries, dict_of_start_dates, dict_of_geo
