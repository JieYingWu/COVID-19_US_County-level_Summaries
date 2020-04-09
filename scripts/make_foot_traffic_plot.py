import numpy as np
from os.path import join
import matplotlib.pyplot as plt
import csv
import seaborn as sns


colors = sns.color_palette('muted')


def plot(*fnames,
         which_counties=['53033', '06037', '17031'],
         county_names=['King County, WA', 'Los Angeles, CA', 'Cook County, IL']):
  fig, axes = plt.subplots(len(fnames), 1, figsize=(10, 8), sharex=True)

  for ax, fname in zip(axes, fnames):
    data = {}
    with open(fname, 'r', newline='') as file:
      reader = csv.reader(file, delimiter=',')
      for i, row in enumerate(reader):
        if i == 0:
          continue
        fips = row[0]
        if fips not in which_counties:
          continue
        data[county_names[which_counties.index(fips)]] = np.array(list(map(float, row[1:])))

    for i, (label, traffic) in enumerate(data.items()):
      ax.plot(list(range(len(traffic))), traffic, color=colors[i], label=label)

  axes[0].set_title('All Points of Interest')
  axes[1].set_title('Hospital Visits')
  axes[2].set_title('Grocery Store Visits')
  axes[0].legend()
  axes[2].set_xlabel('Days since March 1, 2020')
  # axes[0].set_ylabel('Number of Visits')
  axes[1].set_ylabel('Number of Visits')
  # axes[1].set_ylabel('Number of Visits')
  plt.xticks([0, 7, 14])
  plt.savefig(join('visualizations', 'foot_traffic.png'))


if __name__ == '__main__':
  plot(join('data', 'foot_traffic', 'poi_visits.csv'),
       join('data', 'foot_traffic', 'hospital_visits.csv'),
       join('data', 'foot_traffic', 'grocery_visits.csv'))
