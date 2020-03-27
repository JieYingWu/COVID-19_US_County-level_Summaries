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


def create_html_page(html_page_name):
  del states["HI"]
  del states["AK"]

  EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

  state_xs = [states[code]["lons"] for code in states]
  state_ys = [states[code]["lats"] for code in states]

  county_xs = [counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
  county_ys = [counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]

  county_names = [counties[code]["name"] for code in counties if counties[code]["state"] not in EXCLUDED]

  data = dict(
    x=county_xs,
    y=county_ys,
    name=county_names
  )

  colors = ['#084594', '#4292c6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff']

  county_colors = []
  for county_id in counties:
    print(county_id)
    if counties[county_id]["state"] in EXCLUDED:
      continue
    try:
      rate = unemployment[county_id]
      idx = int(rate / 6)
      county_colors.append(colors[idx])
    except KeyError:
      county_colors.append("black")

  # color_mapper = LogColorMapper(palette=colors)
  TOOLS = "pan,wheel_zoom,reset,hover,save"
  p = figure(title="US density", toolbar_location="left",
             plot_width=1100, plot_height=700, tools=TOOLS,
             tooltips=[
               ("County", "@name"), ("(Long, Lat)", "($x, $y)")
             ])

  # hide grid and axes
  p.axis.visible = None
  p.xgrid.grid_line_color = None
  p.ygrid.grid_line_color = None
  p.hover.point_policy = "follow_mouse"

  p.patches(county_xs, county_ys,
            fill_color=county_colors, fill_alpha=0.7,
            line_color="white", line_width=0.5)

  p.patches(state_xs, state_ys, fill_alpha=0.0,
            line_color="#884444", line_width=2, line_alpha=0.3)

  output_file(html_page_name, title="Interactive USA density map")
  show(p)


def create_cases_dict(data_dir):
  filename = join(data_dir, 'cases.csv')
  with open(filename, 'r', newline='') as file:
    reader = csv.reader(file, delimiter=',')



def main():
  data_dir = r"D:\JHU\corona\disease_spread\data"
  create_cases_dict(data_dir)
  create_html_page(html_page_name="us_cases.html")


if __name__ == '__main__':
  # python -c "import bokeh.sampledata; bokeh.sampledata.download()"
  main()

