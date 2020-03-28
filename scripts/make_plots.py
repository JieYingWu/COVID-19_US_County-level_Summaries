"""
Create beautiful plots
"""

from shutil import copyfile
from os.path import join, exists
import numpy as np
import re
from collections import OrderedDict
import csv
import argparse
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment

from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6

from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer


def create_html_page(html_page_name, infected_cases):
  del states["HI"]
  del states["AK"]

  EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

  state_xs = [states[code]["lons"] for code in states]
  state_ys = [states[code]["lats"] for code in states]

  county_xs = [counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
  county_ys = [counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]

  county_names = [counties[code]["name"] for code in counties if counties[code]["state"] not in EXCLUDED]

  county_rates = []
  for county_id in counties:
    if counties[county_id]["state"] in EXCLUDED:
      continue
    try:
      rate = infected_cases[county_id]
      county_rates.append(infected_cases[county_id])
    except KeyError:
      county_rates.append(0.0)

  data = dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates
  )
  # Define a sequential multi-hue color palette.
  palette = brewer['YlGnBu'][8]

  # Reverse color order so that dark blue is highest obesity.
  palette = palette[::-1]
  color_mapper = LinearColorMapper(palette=palette, low=0, high=40)

  TOOLS = "pan,wheel_zoom,reset,hover,save"
  p = figure(title="US density", toolbar_location="left",
             plot_width=1100, plot_height=700, tools=TOOLS,
             tooltips=[
               ("County", "@name"), ("Infection rate", "@rate"),  ("(Long, Lat)", "($x, $y)")
             ])

  # hide grid and axes
  p.axis.visible = None
  p.xgrid.grid_line_color = None
  p.ygrid.grid_line_color = None
  p.hover.point_policy = "follow_mouse"

  p.patches(county_xs, county_ys,
            #fill_alpha=0.7,
            line_color="white", line_width=0.5)

  p.patches(state_xs, state_ys, fill_alpha=0.0,
            line_color="#884444", line_width=2, line_alpha=0.3)

  p.patches('x', 'y', source=data,
            fill_color={'field': 'rate', 'transform': color_mapper},
            fill_alpha=0.7, line_color="white", line_width=0.5)

  output_file(html_page_name, title="Interactive USA density map")
  show(p)


def create_cases_dict(data_dir):
  cases_dict = {}
  filename = join(data_dir, 'cases.csv')

  with open(filename, 'r', newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for i, line in enumerate(reader):
      if i == 0:
        continue
      state_fips_code = int('{:0d}'.format(int(line[0][0:2])))
      county_fips_code = int('{:0d}'.format(int(line[0][2:])))
      infected = float(line[3])
      cases_dict[(state_fips_code, county_fips_code)] = infected

    return cases_dict


def main():
  data_dir = r"D:\JHU\corona\disease_spread\data"
  html_page_name = "us_cases.html"
  infected_cases = create_cases_dict(data_dir)
  create_html_page(html_page_name, infected_cases)


if __name__ == '__main__':
  # run once python -c "import bokeh.sampledata; bokeh.sampledata.download()"
  main()

