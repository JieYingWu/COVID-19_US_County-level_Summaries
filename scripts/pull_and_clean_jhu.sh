#!/bin/bash

curl -o ../raw_data/national/JHU_Infections/cases.csv https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases.csv
python update_timeseries.py
rm ../raw_data/national/JHU_Infections/cases.csv
