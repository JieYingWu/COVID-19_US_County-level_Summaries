import pandas as pd
from os.path import join, exists
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly as pl


def plot_states(df, date):
    fig = go.Figure(data=go.Choropleth(
        locations=df['Combined_Key'],  # Spatial coordinates
        z=df[date].astype(float),  # Data to be color-coded
        zmin=0.0,
        zmax=4.0,
        locationmode='USA-states',  # set of locations match entries in `locations`
        colorscale='blues',
        marker_line_color='white'
    ))

    fig.update_layout(
        title_text='Per State Reproduction Number R_t over time ' + str(date),
        geo_scope='usa',  # limite map scope to USA
    )
    return fig


def main():
    visualizations_dir = '../results/plots/states_r/'
    df = pd.read_csv('../data/us_data/Rt_data_states.csv', delimiter=',')
    col_names = list(df.columns.values)[2:]
    for date in col_names:
        fig = plot_states(df, date)
        filename = visualizations_dir + date.replace("/", "") + '.png'
        fig.write_image(filename)


if __name__ == '__main__':
    main()
