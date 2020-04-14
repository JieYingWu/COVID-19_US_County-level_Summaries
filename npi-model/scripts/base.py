from os.path import join
import sys
import numpy as np
from data_parser import get_data_state, get_data_county
from data_parser_europe import get_data_europe
import pystan
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF

assert len(sys.argv) < 5

# Compile the model
data_dir = sys.argv[1]
if sys.argv[2] == 'europe':
    stan_data, regions, start_date, geocode = get_data_europe(data_dir, show=False)
    weighted_fatalities = np.loadtxt(join(data_dir, 'europe_data', 'weighted_fatality.csv'), skiprows=1, delimiter=',', dtype=str)

elif sys.argv[2] == 'US_county':
    M = int(sys.argv[3])
    stan_data, regions, start_date, geocode = get_data_county(M, data_dir, interpolate=True)
    wf_file = join(data_dir, 'us_data', 'weighted_fatality.csv')
    weighted_fatalities = np.loadtxt(wf_file, skiprows=1, delimiter=',', dtype=str)

elif sys.argv[2] == 'US_state':
    M = int(sys.argv[3])
    stan_data, regions, start_date, geocode = get_data_state(M, data_dir, interpolate=True)
    wf_file = join(data_dir, 'us_data', 'state_weighted_fatality.csv')
    weighted_fatalities = np.loadtxt(wf_file, skiprows=1, delimiter=',', dtype=str)

# Build a dictionary of region identifier to weighted fatality rate
ifrs = {}
for i in range(weighted_fatalities.shape[0]):
    ifrs[weighted_fatalities[i,0]] = weighted_fatalities[i,-1]
stan_data['cases'] = stan_data['cases'].astype(np.int)
stan_data['deaths'] = stan_data['deaths'].astype(np.int)

# np.savetxt('cases.csv', stan_data['cases'].astype(int), delimiter=',', fmt='%i')
# np.savetxt('deaths.csv', stan_data['deaths'].astype(int), delimiter=',', fmt='%i')

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

all_f = np.zeros((N2, len(regions)))
for r in range(len(regions)):
    ifr = float(ifrs[str(regions[r])])
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

    all_f[:,r] = s * h

stan_data['f'] = all_f

# Add a shelter-in-place score
if sys.argv[2][0:2] == 'US' and sys.argv[:
    # Train the model and generate samples - returns a StanFit4Model
    sm = pystan.StanModel(file='stan-models/base_us.stan')

elif:
    # Train the model and generate samples - returns a StanFit4Model
    sm = pystan.StanModel(file='stan-models/base_europe.stan')


    
fit = sm.sampling(data=stan_data, iter=200, chains=6, warmup=100, thin=4, control={'adapt_delta':0.9, 'max_treedepth':10})
# fit = sm.sampling(data=stan_data, iter=2000, chains=4, warmup=10, thin=4, seed=101, control={'adapt_delta':0.9, 'max_treedepth':10})

summary_dict = fit.summary()
df = pd.DataFrame(summary_dict['summary'],
                 columns=summary_dict['summary_colnames'],
                 index=summary_dict['summary_rownames'])


df.to_csv('results/' + sys.argv[2] + '_summary.csv', sep=',')

df_sd = pd.DataFrame(start_date, index=[0])
df_geo = pd.DataFrame(geocode, index=[0])
df_sd.to_csv('results/' + sys.argv[2] + '_start_dates.csv', sep=',')
df_geo.to_csv('results/' + sys.argv[2] + '_geocode.csv', sep=',')
