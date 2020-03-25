# County-level Socioeconomic Data for Predictive Modeling of Epidemiological Effects

**TL/DR:** We aim to gather a *machine readable* dataset related to socioeconomic factors that may affect the spread and/or consequences of epidemiological outbreaks, particularly the novel coronavirus (COVID-19). This dataset is envisioned to serve the datascience and modeling communities. If you want to contribute, please let us know!

**Overview** 
We have curated a machine readable dataset from multiple governmental sources on the county-level with 332 data columns (and three identifying columns with fips, state, and area name). Detailed description of all fields can be found [here](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/tree/master/data)

## Structure

We accumulated statistics from different sources on a county level granularity.
- [./data](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/tree/master/data) folder contains aggregated machine-readable file counties.csv with demographic, socioeconomic, health care, and education data for each county in the 50 states and Washington DC. Data is organized by FIPS codes - unambiguous identifiers for each county, since the same county name may appear in many states.
-  [./raw_data](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/tree/master/raw_data) contains raw datasets that were used to create *data* folder
- [./model](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/tree/master/model) *under construction*
- [./scripts](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/tree/master/scripts) - scripts for making the raw_data machine-readable

## Instructions for Adding Data

Please create a new directory in [./raw_data](https://github.com/JieYingWu/disease_spread/raw_data)
with a sensible name based on the type of data you are adding.

## Acknowledgements
This project was initiated by the ARCADE Lab at Johns Hopkins University, directed by Mathias Unberath. People contributing are, in no particular order:
* Jie Ying Wu
* Benjamin Killeen
* Kinjal Shah
* Anna Zapaishchykova
* Philipp Nikutta
* Shreya Chakraborty
* Jinchi Wei
* Tiger Gao
* Mareike Thies
