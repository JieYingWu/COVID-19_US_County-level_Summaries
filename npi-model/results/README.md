### File descriptions

For each region selection, we provide three files

* <region>_summary.csv - contains the outputs of the model
* <region>_start_dates.csv - this is the first day we use data for our model. We follow MRC Centre's model's choice for 30 days before the first date cumulative deaths > 10 
* <region>_geocode.csv - this maps the index from our model to a FIPS code or country name

### Model output

We're currently predicting for 100 days after the start date. While the model provides many parameters as outputs, we highlight a few below

* prediction[# of days, # of regions] - the model's prediction for the true number of cases for each day
* E_deaths[# of days, # of regions] - the model's prediction for the number of deaths each day 
* Rt[# of days, # of regions] - the estimated time-dependent reproduction number 
