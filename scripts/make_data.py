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


class CSVReaders():
  def __init__(self, filenames, skiprows=None):
    """Reader for multiple csv files, maintaining a dict convention

    Usage: below is an example concatenating the two csv files along dimension 1, and printing the lines.

    ```
    filenames = {'population': 'path/to/population.csv',
                 'density': 'path/to/density.csv'}
    with CSVReaders(filenames) as readers:
      for rows in readers:
        print(','.join(rows['population'] + rows['density']))
    ```

    TODO: allow lists of filenames

    :param filenames: dictionary of keys to filenames
    :param skiprows: dictionary with the same keys mapping to integers, so that the CSVs line up.
    :returns: 
    :rtype: 

    """
    self.skiprows = skiprows
    self.filenames = filenames
    self._iterators = None

  def __enter__(self):
    self.files = dict((k, open(v, 'r', newline='')) for k, v in self.filenames.items())
    self.readers = dict((k, csv.reader(file, delimiter=',')) for k, file in self.files.items())
    return self

  def __iter__(self):
    # yields a dictionary mapping the original keys to each row
    self._iterators = dict((k, iter(reader)) for k, reader in self.readers.items())
    if self.skiprows is not None:
      for k, n in self.skiprows.items():
        for _ in range(n):
          next(self._iterators[k])
      
    while True:
      rows = {}
      for k, iterator in self._iterators.items():
        rows[k] = next(iterator, None)
        if rows[k] is None or all(map(lambda x: x == '', rows[k])):
          break
      yield rows

  def next(self, k):
    """Get the next row for key `k`.

    :param k: 
    :returns: 
    :rtype: 

    """
    assert self._iterators is not None
    return next(self._iterators[k])

  def __exit__(self, exc_type, exc_val, exc_tb):
    for file in self.files.values():
      file.close()


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
    'density']             # TODO: add density
  
  national_data_skiprows = {
    'population': 2,
    'education': 4,
    'poverty': 4,
    'unemployment': 4,
    'density': 1}

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
  i = 0
  for k in keys:
    national_data_column_mapping[k] = {}
    for idx in national_data_which_columns[k]:
      national_data_column_mapping[k][idx] = i
      i += 1
  
  def __init__(self, args):
    self.args = args
    for k, v in args.__dict__.items():
      setattr(self, k, v)

    national_data_filenames = {
      'population': join(self.raw_data_dir, 'national', 'Demographics', 'PopulationEstimates.csv'),
      'education': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'Education.csv'),
      'poverty': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'PovertyEstimates.csv'),
      'unemployment': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'Unemployment.csv'),
      'density': join(self.raw_data_dir, 'national', 'Density', 'housing_area_density_national_2010_census.csv')
    }
    
    self.csv_readers = CSVReaders(national_data_filenames, skiprows=self.national_data_skiprows)

    self.fips_codes = {}        # mapping from fips code to canonical area name
    self.areas = {}             # mapping from (STATE, canonical area name) tuple to fips code
    self._make_reference()

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

  def _set_area(self, fips, state, area):
    """Make the dictionary of fips codes.

    :param state: 
    :param county: 
    :param fips: 
    :returns: 
    :rtype: 

    """
    self.fips_codes[fips] = area
    area = self._get_key(area)
    state = self._get_state(state)
    self.areas[(state, area)] = fips
    if area in self.states:
      self.areas[area] = fips
      self.areas[state] = fips

  def _make_reference(self):
    with self.csv_readers as readers:
      rows = iter(readers.readers['population'])
      for _ in range(readers.skiprows['population']):
        next(rows)
      
      for i, row in enumerate(rows):
        if i == 0:
          continue
        if all(map(lambda x: x == '', row)):
          break
        fips = row[0]
        state = self._get_state(row[1])
        area = row[2]
        self._set_area(fips, state, area)

  def _get_fips(self, x):
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

    if x in self.fips_codes:
      return x
    elif x in self.areas:
      return self.areas[x]
    elif isinstance(x, int):
      return str(x).zfill(5)
    elif x[7:9] == 'US':
      fips = x[9:]
      return fips + ''.join(['0'] * (5 - len(fips)))
    else:
      raise ValueError(f'unrecognized area: {x}')
    
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
    file = open(join(self.data_dir, 'counties.csv'), 'w', newline='')
    writer = csv.writer(file, delimiter=',')
    
    with self.csv_readers as readers:
      for i, rows in enumerate(readers):
        if i == 0:
          # prints all the labels and their column index
          # print(*['\n'.join(map(lambda t: f'      {t[0]},                      # {t[1]}',
          #                       enumerate(rows[k]))) for k in self.keys], sep='\n')
          labels = sum([[rows[k][j].replace(',', '') for j in self.national_data_which_columns[k]] for k in self.keys], [])
          writer.writerow(labels)
        else:

          # make sure the rows are all corresponding
          if not (self._get_fips(rows['population'][0])
                  == self._get_fips(rows['education'][0])
                  == self._get_fips(rows['poverty'][0])
                  == self._get_fips(rows['unemployment'][0])
                  == self._get_fips(rows['density'][3])):
            print(rows['population'][2],
                  rows['education'][2],
                  rows['poverty'][2],
                  rows['unemployment'][2],
                  rows['density'][5], sep=', ')
            print(rows['population'][0],
                  self._get_fips(rows['education'][0]),
                  self._get_fips(rows['poverty'][0]),
                  self._get_fips(rows['unemployment'][0]),
                  self._get_fips(rows['density'][3]), sep=', ')
            continue
          
          values = sum([[rows[k][j].replace(',', '') for j in self.national_data_which_columns[k]] for k in self.keys], [])
          print(values[0])
          
          if not self._is_state(values[self.national_data_column_mapping['population'][1]]):
            continue

          # the density data includes r values in the same columns, remove these
          for j in self.national_data_column_mapping['density'].values():
            values[j] = re.sub(r'\(r\d+\)', '', values[j])

          writer.writerow(values)
          
          # print(*values, sep='\n')
          # fix some rows
          # values[self.column]
          
        # state = self._get_state(rows[k][1])
        # fips = rows[k][0]
        # print(fips)
        # area = rows[k][2].lower().strip()
        # print(area)
        # # self._set_county()
    

def main():
  parser = argparse.ArgumentParser(description='data formatter')

  # file settings
  parser.add_argument('--raw-data-dir', default='./raw_data', help='directory containing raw data')
  parser.add_argument('--data-dir', default='./data', help='directory to write formatted data to')
  args = parser.parse_args()

  # debug
  Formatter(args).make_national_data()
  

if __name__ == '__main__':
  main()
  
