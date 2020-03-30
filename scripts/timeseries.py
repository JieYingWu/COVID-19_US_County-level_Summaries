import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def filter_counties(data, min_days=20, min_cases=100):
    valid = data.apply(is_valid, args=(min_days, min_cases), axis=1)
    return data[valid]


def is_valid(row, min_days, min_cases):
    datapoints = row[5:]
    if pd.Series.max(datapoints) >= min_cases:
        if pd.Series.count(datapoints) >= min_days:
            return True
    return False


def plot_data(data, min_days=20, min_cases=100, label=''):
    valid_data = filter_counties(data, min_days=min_days, min_cases=min_cases)
    for index, row in valid_data.iterrows():
        row = row.to_numpy()
        datapoints = row[5:].astype(np.float)
        datapoints = datapoints[~np.isnan(datapoints)]
        # this should not be needed as data is cumulative -> maybe faulty raw data
        datapoints = datapoints[datapoints != 0]

        y = np.expand_dims(datapoints, axis=1)
        y_log = np.log10(y)
        M = np.ones((y.shape[0], 2))
        M[:, 0] = np.arange(y.shape[0])

        M_inv = np.linalg.pinv(M)

        [m, b] = M_inv @ y_log

        plt.figure()

        plt.subplot(121)
        plt.plot(y, label=label)
        plt.title(row[1] + ', ' + row[2])
        plt.xlabel('Days after first case')
        plt.ylabel('Number cases')
        plt.legend()

        plt.subplot(122)
        plt.plot(y_log, label= label + ' log')

        x = np.arange(y_log.shape[0])
        y_fit = m * x + b

        plt.plot(y_fit, label='linear fit')

        plt.title(row[1] + ', ' + row[2] + ', m: ' + '{0:.2f}'.format(m[0]))
        plt.xlabel('Days after first case')
        plt.ylabel('Number cases [log]')
        plt.legend()


def plot_timeseries(infections, fips=None, label=''):
    # if no fips list is given: plot all counties which fulfill min days and cases
    if fips is None:
        plot_data(infections)
    # else plot only those counties corresponding to the given fips list
    else:
        fips_rows = infections.loc[infections['countyFIPS'].isin(fips)]
        plot_data(fips_rows, min_days=0, min_cases=1, label=label)

    plt.show()


if __name__=='__main__':
    infections = pd.read_csv(r'../raw_data/national/USAfacts_infections/covid_confirmed_usafacts_aligned.csv')
    #fips = [5113, 6029]
    plot_timeseries(infections)
