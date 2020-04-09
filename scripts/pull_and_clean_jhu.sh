#!/bin/bash

curl -o ../raw_data/national/JHU_Infections_time_series/time_series_covid19_confirmed_US.csv https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv
curl -o ../raw_data/national/JHU_Infections_time_series/time_series_covid19_deaths_US.csv https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv

python update_timeseries.py
