"""
Read the raw data and convert it to the machine-readable format.

Meant to be run from the root as `python scripts/format_data.py`.

"""

from os.path import join, exists
import itertools
import numpy as np
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

  def __enter__(self):
    self.files = dict((k, open(v, 'r', newline='')) for k, v in self.filenames.items())
    self.readers = dict((k, csv.reader(file, delimiter=',')) for k, file in self.files.items())
    return self

  def __iter__(self):
    # yields a dictionary mapping the original keys to each row
    iterators = dict((k, iter(reader)) for k, reader in self.readers.items())
    if self.skiprows is not None:
      for k, n in self.skiprows.items():
        for _ in range(n):
          next(iterators[k])
      
    while True:
      rows = {}
      for k, iterator in iterators.items():
        rows[k] = next(iterator, None)
        if rows[k] is None:
          break
      yield rows

  def __exit__(self, exc_type, exc_val, exc_tb):
    for file in self.files.values():
      file.close()


class Formatter():
  def __init__(self, args):
    self.args = args
    for k, v in args.__dict__.items():
      setattr(self, k, v)

    national_data_filenames = {
      'population': join(self.raw_data_dir, 'national', 'Demographics', 'PopulationEstimates.csv'),
      'density': join(self.raw_data_dir, 'national', 'Density', 'housing_area_density_national_2010_census.csv'),
      'education': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'Education.csv'),
      'poverty': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'PovertyEstimates.csv'),
      'unemployment': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'Unemployment.csv')
    }
    national_data_skiprows = {
      'population': 2,
      'density': 1,
      'education': 4,
      'poverty': 4,
      'unemployment': 4
    }
    self.csv_readers = CSVReaders(national_data_filenames, skiprows=national_data_skiprows)
    
  def make_data_for_state(self, state):
    """Make the data for a given state.

    :param state: string abbreviation for the state, e.g. 'NY' for New York State.
    :returns: 
    :rtype: 

    """
    with self.csv_readers as readers:
      for i, rows in enumerate(readers):
        print(i)
        print(rows['population'][1], rows['population'][2])
        print(rows['density'][5], rows['density'][5])
        print(rows['education'][2], rows['education'][2])
        print(rows['poverty'][2], rows['poverty'][2])
        print(rows['unemployment'][2], rows['unemployment'][2])
        if i > 10:
          break
    

def main():
  parser = argparse.ArgumentParser(description='data formatter')

  # file settings
  parser.add_argument('--raw-data-dir', default='./raw_data', help='directory containing raw data')
  parser.add_argument('--data-dir', default='./data', help='directory to write formatted data to')
  parser.add_argument('--states', nargs='+', default=['NY'], help='states to create data for')
  args = parser.parse_args()

  # debug
  Formatter(args).make_data_for_state('NY')
  

if __name__ == '__main__':
  main()
  
