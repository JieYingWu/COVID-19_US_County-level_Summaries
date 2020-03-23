"""
Read the raw data and convert it to the machine-readable format.

Meant to be run from the root as `python scripts/format_data.py`.

"""

from os.path import join, exists
import itertools
import numpy as np
import re
from collections import OrderedDict
import csv
import argparse


class Formatter():
  states = {
    'alabama': 'AL',
    'alaska': 'AK',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'district of columbia': 'DC',
    'florida': 'FL',
    'georgia': 'GA',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'nebraska': 'NE',
    'nevada': 'NV',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'new york': 'NY',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'puerto rico': 'PR',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'united states': 'US',
    'utah': 'UT',
    'vermont': 'VT',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY'}
  abbreviations = dict((v, k) for k, v in states.items())

  keys = [
    'population',
    'education',
    'poverty',
    'unemployment',
    'climate',
    'density'
  ]             # TODO: add density
  
  national_data_skiprows = {
    'population': 2,
    'education': 4,
    'poverty': 4,
    'unemployment': 4,
    'climate': 0,
    'density': 1}

  # which column has the fips code in each table
  fips_columns = {
    'population': 0,
    'education': 0,
    'poverty': 0,
    'unemployment': 0,
    'climate': 0,
    'density': 3}
  
  national_data_which_columns = OrderedDict([
    ('population', [
      0,                        # FIPS
      1,                        # State
      2,                        # Area_Name
      4,                        # Rural-urban_Continuum Code_2013
      6,                        # Urban_Influence_Code_2013
      7,                        # Economic_typology_2015
      18,                       # POP_ESTIMATE_2018
      27,                       # N_POP_CHG_2018
      36,                       # Births_2018
      45,                       # Deaths_2018
      54,                       # NATURAL_INC_2018
      63,                       # INTERNATIONAL_MIG_2018
      72,                       # DOMESTIC_MIG_2018
      81,                       # NET_MIG_2018
      90,                       # RESIDUAL_2018
      100,                      # GQ_ESTIMATES_2018
      108,                      # R_birth_2018
      116,                      # R_death_2018
      124,                      # R_NATURAL_INC_2018
      132,                      # R_INTERNATIONAL_MIG_2018
      140,                      # R_DOMESTIC_MIG_2018
      148                       # R_NET_MIG_2018
    ]),
    
    ('education', [
      39,                       # Less than a high school diploma, 2014-18
      40,                       # High school diploma only, 2014-18
      41,                       # Some college or associate's degree, 2014-18
      42,                       # Bachelor's degree or higher, 2014-18
      43,                       # Percent of adults with less than a high school diploma, 2014-18
      44,                       # Percent of adults with a high school diploma only, 2014-18
      45,                       # Percent of adults completing some college or associate's degree, 2014-18
      46                        # Percent of adults with a bachelor's degree or higher, 2014-18
    ]),
    
    ('poverty', [
      7,                        # POVALL_2018
      8,                      # CI90LBAll_2018
      9,                      # CI90UBALL_2018
      10,                      # PCTPOVALL_2018
      11,                      # CI90LBALLP_2018
      12,                      # CI90UBALLP_2018
      13,                      # POV017_2018
      14,                      # CI90LB017_2018
      15,                      # CI90UB017_2018
      16,                      # PCTPOV017_2018
      17,                      # CI90LB017P_2018
      18,                      # CI90UB017P_2018
      19,                      # POV517_2018
      20,                      # CI90LB517_2018
      21,                      # CI90UB517_2018
      22,                      # PCTPOV517_2018
      23,                      # CI90LB517P_2018
      24,                      # CI90UB517P_2018
      25,                      # MEDHHINC_2018
      26,                      # CI90LBINC_2018
      27                       # CI90UBINC_2018
    ]),
    
    ('unemployment', [
      50,                      # Civilian_labor_force_2018
      51,                      # Employed_2018
      52,                      # Unemployed_2018
      53,                      # Unemployment_rate_2018
      54,                      # Median_Household_Income_2018
      55                       # Med_HH_Income_Percent_of_State_Total_2018
    ]),
    
    ('climate', [
      1,                        # Jan Precipitation / inch
      2,                        # Feb Precipitation / inch
      3,                        # Mar Precipitation / inch
      4,                        # Apr Precipitation / inch
      5,                        # May Precipitation / inch
      6,                        # Jun Precipitation / inch
      7,                        # Jul Precipitation / inch
      8,                        # Aug Precipitation / inch
      9,                        # Sep Precipitation / inch
      10,                       # Oct Precipitation / inch
      11,                       # Nov Precipitation / inch
      12,                       # Dec Precipitation / inch
      13,                       # Jan Temp AVG / F
      14,                       # Feb Temp AVG / F
      15,                       # Mar Temp AVG / F
      16,                       # Apr Temp AVG / F
      17,                       # May Temp AVG / F
      18,                       # Jun Temp AVG / F
      19,                       # Jul Temp AVG / F
      20,                       # Aug Temp AVG / F
      21,                       # Sep Temp AVG / F
      22,                       # Oct Temp AVG / F
      23,                       # Nov Temp AVG / F
      24,                       # Dec Temp AVG / F
      25,                       # Jan Temp Min / F
      26,                       # Feb Temp Min / F
      27,                       # Mar Temp Min / F
      28,                       # Apr Temp Min / F
      29,                       # May Temp Min / F
      30,                       # Jun Temp Min / F
      31,                       # Jul Temp Min / F
      32,                       # Aug Temp Min / F
      33,                       # Sep Temp Min / F
      34,                       # Oct Temp Min / F
      35,                       # Nov Temp Min / F
      36,                       # Dec Temp Min / F
      37,                       # Jan Temp Max / F
      38,                       # Feb Temp Max / F
      39,                       # Mar Temp Max / F
      40,                       # Apr Temp Max / F
      41,                       # May Temp Max / F
      42,                       # Jun Temp Max / F
      43,                       # Jul Temp Max / F
      44,                       # Aug Temp Max / F
      45,                       # Sep Temp Max / F
      46,                       # Oct Temp Max / F
      47,                       # Nov Temp Max / F
      48                        # Dec Temp Max / F
    ]),
    
    ('density', [
      8,                        # Housing units
      9,                        # Area in square miles - Total area
      10,                       # Area in square miles - Water area
      11,                       # Area in square miles - Land area
      12,                       # Density per square mile of land area - Population
      13                        # Density per square mile of land area - Housing units
    ])
  ])

  # map the old columns to the new columns
  national_data_column_mapping = {}
  for k in keys:
    national_data_column_mapping[k] = {}
    i = 0
    for idx in national_data_which_columns[k]:
      national_data_column_mapping[k][idx] = i
      i += 1
  
  def __init__(self, args):
    self.args = args
    for k, v in args.__dict__.items():
      setattr(self, k, v)

    self.national_data_filenames = {
      'population': join(self.raw_data_dir, 'national', 'Demographics', 'PopulationEstimates.csv'),
      'education': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'Education.csv'),
      'poverty': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'PovertyEstimates.csv'),
      'unemployment': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'Unemployment.csv'),
      'climate': join(self.raw_data_dir, 'national', 'Climate', 'FIPS_2019_precipitation_tempAvg_tempMin_tempMax.csv'),
      'density': join(self.raw_data_dir, 'national', 'Density', 'housing_area_density_national_2010_census.csv')
    }
    
    self._make_reference()
    self._write_reference()

  def _get_key(self, key):
    return key.lower().strip()
    
  def _get_state(self, state):
    """Get the standard state abbreviation.

    :param state: String identifying state.
    :returns: 
    :rtype: 

    """
    if state in self.abbreviations:
      return state
    elif self._get_key(state) in self.states:
      return self.states[self._get_key(state)]
    else:
      raise ValueError(f'unrecognized state: {repr(state)}')

  def _make_reference(self):
    self.fips_codes = OrderedDict()  # mapping from fips code to canonical area name
    self.fips_order = []            # list of fips codes
    self.fips_indices = OrderedDict()  # mapping from fips code to index
    self.areas = {}                  # mapping from (STATE, canonical area name) tuple to fips code
    self.populations = {}

    with open(self.national_data_filenames['population'], 'r', newline='') as file:
      rows = iter(csv.reader(file, delimiter=','))
      for _ in range(self.national_data_skiprows['population'] + 1):
        next(rows)
      
      for i, row in enumerate(rows):
        if all(map(lambda x: x == '', row)):
          break
        fips = row[0]
        state = self._get_state(row[1])
        area = self._get_key(row[2])
        
        self.fips_codes[fips] = area
        self.fips_order.append(fips)
        self.fips_indices[fips] = i
        self.areas[(state, area)] = fips
        if area in self.states:
          self.areas[area] = fips
          self.areas[state] = fips

        self.populations[fips] = row[18]  # POP_ESTIMATE_2018
        
          
  def _write_reference(self):
    with open(join(self.data_dir, 'counties_order.csv'), 'w', newline='') as file:
      writer = csv.writer(file, delimiter=',')
      for fips, area in self.fips_codes.items():
        writer.writerow([fips, area])
        
  def _get_fips(self, x, key=None, default=None):
    """Get the 5 digit FIPS string from x, which could be a couple things.

    The possible values for x are:
    - the Fips itself, as a string
    - the GCT_STUB.target-geo-id, e.g. 0500000US01001, the last five digits of which are the FIPS
    - FIPS as an int
    - a (state, county name) pair

    :param x: the value
    :returns: 
    :rtype: 

    """

    if isinstance(x, list) and key is not None:
      # assume fips in first column unless otherwise noted
      return self._get_fips(x[self.fips_columns.get(key, 0)])  
    elif isinstance(x, dict) and key is not None:
      if x.get(key, None) is None:
        return default
      return self._get_fips(x[key][self.fips_columns[key]])
    elif x in self.fips_codes:
      return x
    elif x in self.areas:
      return self.areas[x]
    elif isinstance(x, int):
      return self._get_fips(str(x).zfill(5))
    elif x[7:9] == 'US':
      fips = x[9:]
      return self._get_fips(fips + ''.join(['0'] * (5 - len(fips))))
    else:
      return default
    
  def _is_county(self, x):
    """Tell whether the area x is a county.

    :param x: an area identifier, e.g. fips string
    :returns: 
    :rtype: 

    """
    fips = self._get_fips(x)
    return fips[-1] != '0'

  def _is_state(self, x):
    """

    :param x: an fips code
    :returns: 
    :rtype: 

    """
    fips = self._get_fips(x)
    return fips[1] == '1' and fips[4] == '0'

  def make_national_data(self):
    """Make the national data.

    :returns: 
    :rtype: 

    """

    # parse the incoming data by fips, creating a mapping from fips to a dict mapping datatype keys
    # to data for that row, ready to by joined.
    self.national_data = dict(
      (fips, dict(
        (k, ['NA'] * len(self.national_data_which_columns[k])) for k in self.keys))
      for fips in self.fips_codes)
    self.national_data['labels'] = dict(
      (k, ['NA'] * len(self.national_data_which_columns[k])) for k in self.keys)

    for k in self.keys:
      with open(self.national_data_filenames[k], 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        
        for i, row in enumerate(reader):
          if i < self.national_data_skiprows[k]:
            continue

          if i == self.national_data_skiprows[k]:
            self.national_data['labels'][k] = [row[j].replace(',', '') for j in self.national_data_which_columns[k]]
            continue

          fips = self._get_fips(row, k)
          if fips is None:
            # county not in canonical list skip it
            continue

          values = [row[j] for j in self.national_data_which_columns[k]]
          # the density data includes r values in the same columns, remove these
          if k == 'density':
            # get rid of r values
            for j in range(len(values)):
              values[j] = re.sub(r'\(r\d+\)', '', values[j])
          
          if k == 'unemployment':
            # fix the median household income dollar sign
            values[self.national_data_column_mapping[k][54]] = values[
              self.national_data_column_mapping[k][54]].replace('$', '')

          for j in range(len(values)):
            if values[j] == '':
              values[j] = 'NA'

          self.national_data[fips][k] = values
          
    with open(join(self.data_dir, 'counties.csv'), 'w', newline='') as file:
      writer = csv.writer(file, delimiter=',')
      writer.writerow(sum([self.national_data['labels'][k] for k in self.keys], []))

      for fips in self.fips_codes:
        writer.writerow(sum([self.national_data[fips][k] for k in self.keys], []))

  def _read_cases_data(self):
    infections_filename = join(self.raw_data_dir, 'national', )
    deaths_filename = join(self.raw_data_dir, 'national', '')

    # mapping from fips to numpy array giving timeseries for each.
    infections = {}
    deaths = {}
    recovered = {}
    
    return infections, deaths, recovered
        
  def make_cases_data(self):
    """Solve for beta and gamma for each county.

    based on https://towardsdatascience.com/infection-modeling-part-1-87e74645568a

    rows are:

    FIPS, beta, gamma

    :returns: 
    :rtype: 

    """
    # mapping from fips to numpy array giving timeseries for each, starting from the first day with
    # nonzero infections
    infections, deaths, recovered = self._read_cases_data()

    filename = join(self.data_dir, 'beta_gamma.csv')
    file = open(filename, 'w', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['FIPS', 'beta', 'gamma'])

    for fips in self.fips_codes:
      if not (fips in infections and fips in deaths and fips in recovered):
        writer.writerow([fips, 'NA', 'NA'])
        continue

      # Total population, N.
      N = self.populations[fips]

      # number of infected people
      X = infections[fips] / N
      
      # fraction removed (recovered or dead)
      R = (recovered[fips] + deaths[fips]) / N

      # fraction of population susceptible
      S = 1 - X - R

      # integrate with trapezoidal method
      beta = - (S[-1] - S[0]) / np.trapz(S - X, x=None, dx=1)
      gamma = R / np.trapz()
      
      writer.writerow([fips, f'{beta}', f'{gamma}'])
      print(f'wrote {fips}: beta = {beta:.04f}, gamma = {gamma:.04f}')
    file.close()

        
def main():
  parser = argparse.ArgumentParser(description='data formatter')

  # file settings
  parser.add_argument('--raw-data-dir', default='./raw_data', help='directory containing raw data')
  parser.add_argument('--data-dir', default='./data', help='directory to write formatted data to')
  args = parser.parse_args()

  # debug
  formatter = Formatter(args)
  formatter.make_national_data()
  # formatter.make_cases_data()

if __name__ == '__main__':
  main()
  
