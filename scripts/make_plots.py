"""
Create beautiful plots
"""

from shutil import copyfile
from bokeh.plotting import curdoc
from os.path import join, exists
import numpy as np
import re
import pandas as pd
from collections import OrderedDict
from datetime import datetime
import csv
import argparse
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.us_counties import data as counties
from datetime import timedelta
import math
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.models import Slider, CustomJS, DateSlider
from bokeh.models import LogColorMapper
from bokeh.palettes import Magma256
from bokeh.layouts import widgetbox, row, column

from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.themes import built_in_themes

visualizations_dir = 'visualizations'


def create_dict_forJS(df):
    EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

    col_names = list(df.columns.values)
    len_col = len(col_names)
    county_rates = []

    for county_id in counties:
        if counties[county_id]["state"] in EXCLUDED:
            continue
        fips = str(county_id[0]).zfill(2) + str(county_id[1]).zfill(3)
        # len_col - 1 = its the last day that we have
        rates = np.zeros(len_col - 4)
        for i in range(0, len_col-4):
            rate = df.loc[df['FIPS'] == fips][col_names[i+4]].values
            if len(rate) > 0:
                if math.isnan(rate[0]):
                    rates[i] = 0.0
                else:
                    rates[i] = rate[0]
            else:
                rates[i] = 0.0
        county_rates.append(rates)

    a_dict = {}
    for i in range(0, len_col - 4):
        day_str = col_names[i+4]
        day_key = str(datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S').date())
        a_dict[day_key] = np.array(county_rates)[:, i]

    source_new=ColumnDataSource(data=a_dict)
    print(a_dict)
    return a_dict


def create_colors_forJS(df):
    EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")
    hex_color = rgb_to_hex((255, 255, 255))
    col_names = list(df.columns.values)
    len_col = len(col_names)
    county_rates = []

    for county_id in counties:
        if counties[county_id]["state"] in EXCLUDED:
            continue
        fips = str(county_id[0]).zfill(2) + str(county_id[1]).zfill(3)
        # len_col - 1 = its the last day that we have
        rates = ["" for x in range(len_col - 4)]
        for i in range(0, len_col-4):
            rate = df.loc[df['FIPS'] == fips][col_names[i+4]].values
            if len(rate) > 0:
                if math.isnan(rate[0]):
                    rates[i] = hex_color #0.0
                else:
                    rates[i] = hex_color # rate[0]
            else:
                rates[i] = hex_color # 0.0
        county_rates.append(rates)

    a_dict = {}
    for i in range(0, len_col - 4):
        day_str = col_names[i+4]
        day_key = str(datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S').date())
        a_dict[day_key] = np.array(county_rates)[:, i]

    print(a_dict)
    return a_dict


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def create_html_page(html_page_name, df):
    del states["HI"]
    del states["AK"]

    EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

    state_xs = [states[code]["lons"] for code in states]
    state_ys = [states[code]["lats"] for code in states]

    county_xs = [counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
    county_ys = [counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]

    county_names = [counties[code]["name"] for code in counties if counties[code]["state"] not in EXCLUDED]

    col_names = list(df.columns.values)
    len_col = len(col_names)

    last_day_str = col_names[len_col - 1]
    last_day = datetime.strptime(last_day_str, '%Y-%m-%d %H:%M:%S').date()
    first_day_str = col_names[4]  # first 4 colums contain names etc
    first_day = datetime.strptime(first_day_str, '%Y-%m-%d %H:%M:%S').date()

    a_dict = create_dict_forJS(df)
    source_new = ColumnDataSource(data=a_dict)
    source_visible = ColumnDataSource(data={'x': county_xs, 'y': county_ys,
                                            'name': county_names, 'rate': a_dict[str(last_day)]})
    '''
    c_dict = create_colors_forJS(df)
    hex_color = rgb_to_hex((255, 255, 255))

    source_visible = ColumnDataSource(data={'x': county_xs, 'y': county_ys,
                                            'name': county_names, 'rate': a_dict[str(last_day)],
                                            'color': [hex_color]})
    '''

    # Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][6]
    palette = palette[::-1]

    # TODO: get the high value from median?
    color_mapper = LinearColorMapper(palette=palette, low=0, high=100)
    # TODO: add agenda?
    TOOLS = "pan,zoom_in,zoom_out,wheel_zoom,box_zoom,reset,hover,save"
    p = figure(title="US density", toolbar_location="right", output_backend="webgl",
               plot_width=1100, plot_height=700, tools=TOOLS,
               tooltips=[
                   ("County", "@name"), ("Confirmed cases", "@rate"), ("(Long, Lat)", "($x, $y)")
               ])

    # hide grid and axes
    p.axis.visible = None
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    # p.patches(county_xs, county_ys,
              # fill_alpha=0.7,
    #          line_color="white", line_width=0.5)

    p.patches(state_xs, state_ys, fill_alpha=0.7,
              line_color="white", line_width=2, line_alpha=0.3)

    p.patches('x', 'y', source=source_visible,
              fill_color={'field': 'rate', 'transform': color_mapper},
              #fill_color='color',
              fill_alpha=0.7, line_color="white", line_width=0.2)

    date_slider = DateSlider(title="Date:", start=first_day, end=last_day, value=last_day, step=1)
    callback = CustomJS(args=dict(source=source_new, ts=source_visible), code="""
                            var data=ts.data;
                            var data1=source.data;
                            var f=cb_obj.value; //this is the selection value of slider 
                            var event = new Date(f);
                            var date_selected = event.toISOString().substring(0,10); // converting date from python to JS
                            //ts.data['color'] = '#ffffff' //color_dict.data[date_selected];
                            data['rate']=data1[date_selected];
                            ts.change.emit();
                    """)

    date_slider.js_on_change('value', callback)

    layout = row(column(date_slider), p)
    output_file(html_page_name, title="Interactive USA density map")
    show(layout)


def create_infections_dict(data_dir):
    filename = join(data_dir, 'infections_timeseries.csv')
    df = pd.read_csv(filename, dtype={"FIPS": int})
    df['FIPS'] = df['FIPS'].apply(lambda x: str(x).zfill(5))
    return df


# deprecated
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


def big_palette(size, palette_func):
    if size < 256:
        return palette_func(size)
        p = palette_func(256)
        out = []
    for i in range(size):
        idx = int(i * 256.0 / size)
        out.append(p[idx])
    return out


def main():
    html_page_name = join(visualizations_dir, "us_cases.html")
    infected_cases = create_cases_dict(data_dir)
    df = create_infections_dict(data_dir)
    create_html_page(html_page_name, df)
    


if __name__ == '__main__':
    # run once python -c "import bokeh.sampledata; bokeh.sampledata.download()"
    main()
