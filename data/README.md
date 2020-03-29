# Datasets

* `counties.csv` contains demographic, socioeconomic, health care, education and transit data for
  each county in the 50 states and Washington DC. Note that this also includes analogous data for
  states, as available.
* `counties_only.csv` contains the same columns for counties only.
* `states_only.csv` contains the same columns for the fifty states and DC.
* `infections_timeseries.csv` contains an county-level timeseries of cumulative COVID-19 infections in the US.
* `deaths_timeseries.csv` contains analogous information for COVID-19 related deaths.
* `filtered_cases_and_deaths.csv` contains only counties with a significant number of cases.
* `filtered_cases_and_deaths.csv` contains info on all fifty states and DC.
* `interventions.csv` contains the dates that counties (or states governing them) took measures to
  mitigate the spread by restricting gatherings, measured in days since February 29, 2020.
* `counties_order.csv` contains the FIPS codes and county name for each of these counties. FIPS
  codes are unambiguous identifiers for each county, since the same county name may appear in many
  states. See [this list](https://www.wikiwand.com/en/List_of_the_most_common_U.S._county_names)
  for examples. This is the first three columns of `counties.csv`.
* [list_of_columns.md](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/blob/master/data/list_of_columns.md)
  contains descriptions for each column in `counties.csv`, `counties_only.csv`, etc.
* `recovered_timeseries.csv` is a *limited* timeseries for recovered patients. This data is not
  very well-tracked, but we include it as we are able.

#### Data links
1. [ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/](ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/)
2. [https://data.census.gov/cedsci/table?q=dp02&hidePreview=true&tid=ACSDP1Y2018.DP02&vintage=2018&g=0400000US36.050000&tp=true&y=2018](https://data.census.gov/cedsci/table?q=dp02&hidePreview=true&tid=ACSDP1Y2018.DP02&vintage=2018&g=0400000US36.050000&tp=true&y=2018)
3. [https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/counties/](https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/counties/)
4. [https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk)
5. Johns Hopkins CSSE COVID-19 Tracking: [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)
6. [https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/](https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/)
7. USAfacts: [https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/](https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/)
8. [https://www.kff.org/state-category/providers-service-use/](https://www.kff.org/state-category/providers-service-use/)
9. [https://www.aamc.org/data-reports/workforce/data/2019-state-profiles](https://www.aamc.org/data-reports/workforce/data/2019-state-profiles)
10. [https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/](https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/)
11. [https://alltransit.cnt.org/data-download/](https://alltransit.cnt.org/data-download/)
12.[https://khn.org/news/as-coronavirus-spreads-widely-millions-of-older-americans-live-in-counties-with-no-icu-beds/](https://khn.org/news/as-coronavirus-spreads-widely-millions-of-older-americans-live-in-counties-with-no-icu-beds/)

