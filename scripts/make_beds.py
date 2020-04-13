import numpy as np
import pandas as pd
from os.path import join, exists
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from math import isnan

visualizations_dir = 'visualizations'
# beds_key = "ICU Beds"
# beds_name = "Intensive Care Unit Beds"
# beds_key = "Active Physicians per 100000 Population 2018 (AAMC)" 
# beds_name = "Active Physicians per 100000"

plot_name = 'icu_beds.png'

pop_key = "POP_ESTIMATE_2018"
per_what = 10000
cmap = plt.get_cmap('Blues')


def is_county(fips):
  return fips[2:] != '000'


def read_beds(data_dir):
  filename = join(data_dir, 'counties.csv')
  df = pd.read_csv(filename, converters={
    "FIPS": str,
    # beds_key : lambda x : 0. if x == 'NA' else float(x)
  })
  fips_codes = []
  beds = []
  for fips, bs, pop in zip(list(df['FIPS']), list(df[beds_key]), list(df[pop_key])):
    pop = int(pop)
    if is_county(fips) and bs != 'NA' and bs != '' and not isnan(float(bs)):
      fips_codes.append(fips)
      if bool(per_what):
        beds.append(int(bs) / pop * per_what)
      else:
        beds.append(int(bs) / pop)
  return fips_codes, beds
  

def plot_counties(fips, values):
  # binning_endpoints = [1, 5, 10, 15, 20, 25, 30, 50, 75, 100, 200, 300, 400, 500]
  # binning_endpoints = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
  # binning_endpoints = list(np.arange(1.0, 10.0, 1.0)) + [10.0, 20.0, 30.]
  num_points = len(binning_endpoints) + 2
  colors = [cmap((i + 1) / num_points) for i in range(num_points)]
  colorscale = [f'rgb({t[0]}, {t[1]}, {t[2]})' for t in colors]
  fig = ff.create_choropleth(
    fips=fips, values=values,
    binning_endpoints=binning_endpoints,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.05},
    colorscale=colorscale,
    # round_legend_values=True,
    # legend_title=f'Beds per {per_what}',
    title=f'{beds_name} in the United States'
  )
  fig.layout.template = None
  return fig


def main():
  data_dir = 'data'
  filename = join(visualizations_dir, plot_name)
  fips, beds = read_beds(data_dir)
  fig = plot_counties(fips, beds)
  fig.write_image(filename)
  
    
if __name__ == '__main__':
  main()
