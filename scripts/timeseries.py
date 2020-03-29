import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_timeseries(infections):
  for row in infections.iterrows():
    row = row[1].to_numpy()
    datapoints = row[5:].astype(np.float)
    datapoints = datapoints[~np.isnan(datapoints)]
    # this should not be needed as data is cumulative -> maybe faulty raw data
    datapoints = datapoints[datapoints != 0]
    # at least 15 days into infections
    if datapoints.shape[0] > 15:
        max_cases = np.max(datapoints)
        # at least 100 infections
        if max_cases > 100:
            y = np.expand_dims(datapoints, axis=1)
            y_log = np.log10(y)
            M = np.ones((y.shape[0], 2))
            M[:, 0] = np.arange(y.shape[0])

            M_inv = np.linalg.pinv(M)

            [m, b] = M_inv @ y_log

            plt.subplot(121)
            plt.plot(y, label='Infections')
            plt.title(row[1] + ', ' + row[2])
            plt.xlabel('Days after first case')
            plt.ylabel('Number cases')
            plt.legend()

            plt.subplot(122)
            plt.plot(y_log, label='Infections log')

            x = np.arange(y_log.shape[0])
            y_fit = m * x + b

            plt.plot(y_fit, label='linear fit')

            plt.title(row[1] + ', ' + row[2] + ', m: ' + '{0:.2f}'.format(m[0]))
            plt.xlabel('Days after first case')
            plt.ylabel('Number cases [log]')
            plt.legend()

            plt.show()

if __name__=='__main__':
  infections = pd.read_csv(r'../raw_data/national/USAfacts_infections/covid_confirmed_usafacts_aligned.csv')
  plot_timeseries(infections)

