import pandas as pd
from os.path import join, exists
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from math import isnan

visualizations_dir = 'visualizations'
beds_key = "ICU Beds"
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
  for fips, bs in zip(list(df['FIPS']), list(df[beds_key])):
    if is_county(fips) and bs != 'NA' and bs != '' and not isnan(float(bs)):
      fips_codes.append(fips)
      beds.append(int(bs))
  return fips_codes, beds
  

def plot_counties(fips, values):
  binning_endpoints = [1, 5, 10, 15, 20, 25, 30, 50, 75, 100, 200, 300, 400, 500]
  num_points = len(binning_endpoints) + 2
  colors = [cmap((i+1) / num_points) for i in range(num_points)]
  colorscale = [f'rgb({t[0]}, {t[1]}, {t[2]})' for t in colors]
  fig = ff.create_choropleth(
    fips=fips, values=values,
    binning_endpoints=binning_endpoints,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.05},
    colorscale=colorscale,
    round_legend_values=True,
    title='County-level Number of Intensive Care Unit Beds'
  )
  fig.layout.template = None
  return fig


def main():
  data_dir = 'data'
  filename = join(visualizations_dir, "icu_beds.png")
  fips, beds = read_beds(data_dir)
  fig = plot_counties(fips, beds)
  fig.write_image(filename)
  
    
if __name__ == '__main__':
  main()
