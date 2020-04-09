
from os.path import join
import sys
import numpy as np
from data_parser import get_stan_parameters_europe, get_stan_parameters_by_state_us, get_stan_parameters_by_county_us
import pystan
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF
#from forecast_plots import plot_forecasts

assert len(sys.argv) < 5

# Compile the model
data_dir = sys.argv[1]
if sys.argv[2] == 'europe':
    stan_data, countries = get_stan_parameters_europe(data_dir, show=False)
    weighted_fatalities = np.loadtxt(join(data_dir, 'europe_data', 'weighted_fatality.csv'), skiprows=1, delimiter=',', dtype=str)
    ifrs = {}
    for i in range(weighted_fatalities.shape[0]):
        ifrs[weighted_fatalities[i,1]] = float(weighted_fatalities[i,-2])

elif sys.argv[2] == 'US_county':
    num_of_counties = int(sys.argv[3])
    stan_data, countries, start_date, geocode = get_stan_parameters_by_county_us(num_of_counties, data_dir, show=False)
    weighted_fatalities = np.loadtxt(join(data_dir, 'us_data', 'weighted_fatality.csv'), skiprows=1, delimiter=',', dtype=str)
    ifrs = {}
    for i in range(weighted_fatalities.shape[0]):
        ifrs[str(weighted_fatalities[i,0])] = weighted_fatalities[i,-1]

elif sys.argv[2] == 'US_state':
    num_of_states = int(sys.argv[3])
    stan_data, countries, start_date, geocode = get_stan_parameters_by_state_us(num_of_states, data_dir, show=False)
    weighted_fatalities = np.loadtxt(join(data_dir, 'us_data', 'state_weighted_fatality.csv'), skiprows=1, delimiter=',', dtype=str)
    ifrs = {}
    for i in range(weighted_fatalities.shape[0]):
        ifrs[str(weighted_fatalities[i,0])] = weighted_fatalities[i,-1]

stan_data['cases'] = stan_data['cases'].astype(np.int)
stan_data['deaths'] = stan_data['deaths'].astype(np.int)

# print("**********Preprocessing done**********")
# np.savetxt('cases.csv', stan_data['cases'].astype(int), delimiter=',', fmt='%i')
# np.savetxt('deaths.csv', stan_data['deaths'].astype(int), delimiter=',', fmt='%i')
# print("**********Writing out cases.csv and deaths.csv done**********")


N2 = stan_data['N2']
serial_interval = np.loadtxt(join(data_dir, 'serial_interval.csv'), skiprows=1, delimiter=',')
# Time between primary infector showing symptoms and secondary infected showing symptoms - this is a probability distribution from 1 to 100 days

SI = serial_interval[0:stan_data['N2'],1]
stan_data['SI'] = SI

# infection to onset
mean1 = 5.1
cv1 = 0.86
alpha1 = cv1**-2
beta1 = mean1/alpha1
# onset to death
mean2 = 18.8
cv2 = 0.45
alpha2 = cv2**-2
beta2 = mean2/alpha2

all_f = np.zeros((N2, len(countries)))
for c in range(len(countries)):
    ifr = float(ifrs[str(countries[c])])
    ## assume that IFR is probability of dying given infection
    x1 = np.random.gamma(alpha1, beta1, 5000000) # infection-to-onset -> do all people who are infected get to onset?
    x2 = np.random.gamma(alpha2, beta2, 5000000) # onset-to-death
    f = ECDF(x1+x2)
    def conv(u): # IFR is the country's probability of death
        return ifr * f(u)

    h = np.zeros(N2) # Discrete hazard rate from time t = 1, ..., 100
    h[0] = (conv(1.5) - conv(0.0))

    for i in range(1, N2):
        h[i] = (conv(i+.5) - conv(i-.5)) / (1-conv(i-.5))
    s = np.zeros(N2)
    s[0] = 1
    for i in range(1, N2):
        s[i] = s[i-1]*(1-h[i-1])

    all_f[:,c] = s * h

stan_data['f'] = all_f

# Train the model and generate samples - returns a StanFit4Model
sm = pystan.StanModel(file='stan-models/base.stan')

fit = sm.sampling(data=stan_data, iter=4000, chains=6, warmup=2000, thin=4, control={'adapt_delta':0.9, 'max_treedepth':10})
# fit = sm.sampling(data=stan_data, iter=2000, chains=4, warmup=10, thin=4, seed=101, control={'adapt_delta':0.9, 'max_treedepth':10})

# All the parameters in the stan model
# mu = fit['mu']
# alpha = fit['alpha']
# kappa = fit['kappa']
# y = fit['y']
# phi = fit['phi']
# tau = fit['tau']
# prediction = fit['prediction']
# estimated_deaths = fit['E_deaths']
# estimated_deaths_cf = fit['E_deaths0']
# print(mu, alpha, kappa, y, phi, tau, prediction, estimated_deaths, estimated_deaths_cf)

summary_dict = fit.summary()
df = pd.DataFrame(summary_dict['summary'],
                 columns=summary_dict['summary_colnames'],
                 index=summary_dict['summary_rownames'])


df.to_csv('results/' + sys.argv[2] + '_summary.csv', sep=',')

df_sd = pd.DataFrame(start_dates, index=[0])
df_geo = pd.DataFrame(geocode, index=[0])
df_sd.to_csv('results/' + sys.argv[2] + '_start_dates.csv', sep=',')
df_geo.to_csv('results/' + sys.argv[2] + '_geocode.csv', sep=',')
## TODO: Make pretty plots
# plot_forecasts()
