import argparse
import numpy as np
import string
import seaborn as sns


def get_timeseries_figure(
    timeseries,
    counties,
    timeseries_type='infections',
    mode='Date',
    interventions=['stay at home'],
    scale='Linear',
    per_capita=False):
  """FIXME! briefly describe function

  :param data: 
  :param timeseries_type: 
  :param mode: Either 'Analysis' or 'Raw'
  :returns: 
  :rtype: 

  """
  
  # get top 10 counties by default
  assert timeseries_type in ['infections', 'deaths']
  timeseries = timeseries.loc[timeseries['FIPS'].isin(counties)]

  color_palette = sns.color_palette('Set1', n_colors=len(data.selected_counties))
  color_palette = [f'#{int(255*t[0]):02x}{int(255*t[1]):02x}{int(255*t[2]):02x}' for t in color_palette]

  if per_capita:
    raise NotImplementedError
    # value_func = lambda x, fips: x / data.fips_to_population[fips] * data.per_what
  else:
    value_func = lambda x, fips: x
  
  if mode == 'Date':
    xtitle = 'Date'
    start = data.timeseries_start_index
    xfunc = lambda row, idx: data.timeseries_dates[start:]
    yfunc = lambda row, idx: value_func(row[start + 1:], row[0])
  elif mode == 'Threshold':
    xtitle = f'Days since {threshold} Confirmed {string.capwords(timeseries_type)}'
    xfunc = lambda row, idx: list(range(len(row) - data.infections_start_indices[idx] - 1))
    yfunc = lambda row, idx: value_func(row[1:][data.infections_start_indices[idx]:], row[0])
    
  fig_data = [
    dict(
      x=xfunc(row, idx),
      y=yfunc(row, idx),
      mode='lines',
      name=data.fips_to_county_name.get(row[0], 'NA'),
      text=data.fips_to_county_name.get(row[0], 'NA'),
      hoverinfo='text+x+y',
      line=dict(color=color_palette[i]), shape='spline' if gradient else 'linear', smoothing=2)
    for i, (idx, row) in enumerate(timeseries.iterrows())]

  title = f'{string.capwords(timeseries_type)}'
  if gradient:
    title += ' per Day (smoothed)'
  if per_capita:
    title += f', per {data.per_what:,d}'
  
  layout = dict(
    title=title,
    # showlegend=False,
    yaxis={'type': 'log' if scale == 'Log' else 'linear'},
    xaxis={'title': xtitle},
    hovermode='closest',
    annotations=[])

  # add annotations
  annotations = getattr(data, ('threshold_' if mode == 'Threshold' else '') + f'{timeseries_type}_annotations')
  for i, (idx, row) in enumerate(timeseries.iterrows()):
    fips = row['FIPS']
    if annotations.get((fips, intervention)) is None:
      continue
    # if mode == 'Threshold' and annotations[fips, intervention]['x'] > len(fig_data[i]['x']):
    #   continue
    annotation = annotations[fips, intervention].copy()
    annotation['arrowcolor'] = color_palette[i]
    annotation['textfont'] = dict(size=8, color=color_palette[i])
    annotation['y'] = value_func(row[annotation['xidx']], fips)
    if scale == 'Log':
      annotation['y'] = np.log10(annotation['y'])
    layout['annotations'].append(annotation)
    
  return dict(data=fig_data, layout=layout)


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('--counties', nargs='+', default=['06037'], type=str, help='counties to include, by fips code')
  


if __name__ == '__main__':
  main()

