import pandas as pd
import numpy as np
from os.path import join


def to_fips(row):
    state = str(int(row['STATE'])).zfill(2)
    county = str(int(row['COUNTY'])).zfill(3)
    return state + county


# used census data can be downloaded from
# https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/counties/asrh/
census_data = pd.read_csv(join('data', 'us_data', 'cc-est2018-alldata.csv'), encoding="ISO-8859-1")
census_data = census_data[census_data['YEAR'] == 11]
ind = ['STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'AGEGRP', 'TOT_POP']
census_data = census_data[ind]

# add rows for state level by aggregating the counties of each state
states = np.unique(census_data['STATE'])
state_names = np.unique(census_data['STNAME'])
for state, state_name in zip(states, state_names):
    # add total population per age group over all counties of that state
    state_data = census_data[census_data['STATE'] == state]
    for age_group in range(19):
        total = state_data[state_data['AGEGRP'] == age_group]['TOT_POP'].sum()
        new_row = pd.Series([state, 0.0, state_name, 'NA', age_group, total], index=ind)
        census_data = census_data.append(new_row, ignore_index=True)
        
census_data['FIPS'] = census_data.apply(to_fips, axis=1)
census_data = census_data.sort_values(by=['FIPS', 'AGEGRP'])
share = census_data.pivot_table(index=['FIPS'], columns=['AGEGRP'], values=['TOT_POP'])
share = share.divide(share[('TOT_POP', 0)], axis=0)

# add two age groups together to match the brackets in Verity et al.
out = pd.DataFrame()
out['0-9'] = share[[('TOT_POP', 1), ('TOT_POP', 2)]].sum(axis=1)
out['10-19'] = share[[('TOT_POP', 3), ('TOT_POP', 4)]].sum(axis=1)
out['20-29'] = share[[('TOT_POP', 5), ('TOT_POP', 6)]].sum(axis=1)
out['30-39'] = share[[('TOT_POP', 7), ('TOT_POP', 8)]].sum(axis=1)
out['40-49'] = share[[('TOT_POP', 9), ('TOT_POP', 10)]].sum(axis=1)
out['50-59'] = share[[('TOT_POP', 11), ('TOT_POP', 12)]].sum(axis=1)
out['60-69'] = share[[('TOT_POP', 13), ('TOT_POP', 14)]].sum(axis=1)
out['70-79'] = share[[('TOT_POP', 15), ('TOT_POP', 16)]].sum(axis=1)
out['80+'] = share[[('TOT_POP', 17), ('TOT_POP', 18)]].sum(axis=1)
out['test'] = out.sum(axis=1)
out.insert(0, 'FIPS', out.index)

# this data is taken from Verity et al. 'Estimates of the severity of coronavirus disease 2019: a model-based analysis'
ifr_unweighted = [0.0000161, 0.0000695, 0.000309, 0.000844, 0.00161, 0.00595, 0.0193, 0.0428, 0.0780]
age_groups = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']

# county level demographics data
out['fatality_rate'] = np.dot(out[age_groups], ifr_unweighted)

out.to_csv(join('data', 'us_data', 'weighted_fatality.csv'), index=False)
