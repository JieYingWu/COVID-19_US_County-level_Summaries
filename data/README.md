# Datasets

* `counties.csv` contains demographic, socioeconomic, health care, education and transit data for
  each county in the 50 states and Washington DC. Note that this also includes analogous data for
  states, as available.
* `counties_only.csv` contains the same columns for counties only.
* `states_only.csv` contains the same columns for the fifty states and DC.
* `infections_timeseries.csv` contains an county-level timeseries of cumulative COVID-19 infections
  in the US.
* `deaths_timeseries.csv` contains analogous information for COVID-19 related deaths.  **Note**
  that the first column in the infections and deaths data corresponds to Jan 22, 2020, or **t =
  737446**.
* `interventions.csv` contains the dates that counties (or states governing them) took measures to
  mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the
  date, where January 1 of year 1 has `t = 1`. This convention is chosen for consistency with the
  python `datetime` library. A date in this format can be converted to year, month, date with:
```python
import datetime
date = datetime.date.fromordinal(ordinal_date)
print(date.month, date.day, date.year)
```
* `counties_order.csv` contains the FIPS codes and county name for each of these counties. FIPS
  codes are unambiguous identifiers for each county, since the same county name may appear in many
  states. See [this list](https://www.wikiwand.com/en/List_of_the_most_common_U.S._county_names)
  for examples. This is the first three columns of `counties.csv`.
* [list_of_columns.md](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/blob/master/data/list_of_columns.md)
  contains descriptions for each column in `counties.csv`, `counties_only.csv`, etc.
* `recovered_timeseries.csv` is a *limited* timeseries for recovered patients. This data is not
  very well-tracked, but we include it as we are able.

#### Data links

1. Our COVID-19 infections and deaths data come from the Johns Hopkins University [CSSE COVID-19
   Tracking Project](https://github.com/CSSEGISandData/COVID-19) and
   [Dashboard](https://coronavirus.jhu.edu/map.html).
2. Our climate data comes from the [NOAA](ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/)
3. Our county-level demographic data is primarily sourced from the United States Census Bureau
    * https://data.census.gov/cedsci/table?q=dp02&hidePreview=true&tid=ACSDP1Y2018.DP02&vintage=2018&g=0400000US36.050000&tp=true&y=2018
    * https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/counties/
    * https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk
4. Additional county-level data from the [USDA](https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/)
5. Additional COVID-19 Case information from [USAfacts](https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/)
6. Healthcare capacity related information comes primarily from [Kaiser Family Foundation](https://www.kff.org/state-category/providers-service-use/).
7. [https://www.aamc.org/data-reports/workforce/data/2019-state-profiles](https://www.aamc.org/data-reports/workforce/data/2019-state-profiles)
11. Traffic score information from the [Center for Neighborhood Technology](https://alltransit.cnt.org/data-download/)
12. ICU Bed information from [KHN](https://khn.org/news/as-coronavirus-spreads-widely-millions-of-older-americans-live-in-counties-with-no-icu-beds/)
13. Foot traffic data from [SafeGraph](https://shop.safegraph.com/).
14. COVID-19 related Interventions data from numerous media sources:
    * https://www.edweek.org/ew/section/multimedia/map-coronavirus-and-school-closures.html
    * https://www.nytimes.com/interactive/2020/us/coronavirus-stay-at-home-order.html
    * https://www.cnn.com/2020/03/23/us/coronavirus-which-states-stay-at-home-order-trnd/index.html
    * https://www.today.com/food/which-states-have-closed-restaurants-bars-due-coronavirus-t176039
  https://www.eater.com/2020/3/15/21180761/coronavirus-restaurants-bars-closed-new-york-la-chicago
    * https://www.heraldtribune.com/news/20200320/coronavirus-florida-governor-closes-all-restaurants-and-gyms
    * https://www.usnews.com/news/national-news/articles/2020-03-27/alabama-gov-kay-ivey-closes-nonessential-businesses-as-coronavirus-spreads
    * https://www.peninsulaclarion.com/news/local-bars-resaurants-gyms-theaters-react-to-coronavirus/
    * https://www.alaskapublic.org/2020/03/17/state-bans-restaurant-dining-as-alaskas-confirmed-coronavirus-cases-grow-to-6/
    * https://www.fox10phoenix.com/news/phoenix-tucson-order-closures-of-bars-restaurants1
    * https://www.livescience.com/coronavirus-arkansas.html
    * https://katv.com/news/local/coronavirus-cases-rise-to-46-in-arkansas
    * https://dc.eater.com/2020/3/15/21180673/dc-mayor-muriel-bowser-coronavirus-response-elminate-bar-seats-limit-table-size
    * https://www.heraldtribune.com/news/20200320/coronavirus-florida-governor-closes-all-restaurants-and-gyms
    * https://www.forsythnews.com/news/health-care/heres-latest-coronavirus-georgia/
    * https://www.hawaiinewsnow.com/2020/03/18/list-bar-closures-cruise-ship-screening-here-are-all-iges-covid-directives/
    * https://www.kcci.com/article/gov-reynolds-issues-state-of-public-health-disaster/31700874
    * https://www.kansascity.com/news/coronavirus/article241494536.html
    * https://www.courier-journal.com/story/news/2020/03/16/coronavirus-kentucky-beshear-orders-restaurants-bars-close/5057062002/
    * https://wgme.com/news/coronavirus/gov-mills-mandates-maine-bars-restaurants-close-to-dine-in-customers
    * https://mississippitoday.org/2020/03/25/mayors-scramble-to-know-does-gov-reeves-coronavirus-declaration-clash-with-local-orders/
    * https://ktvo.com/news/local/in-missouri-no-dining-in-at-restaurants-groups-of-10-or-more-banned-amid-coronavirus
    * https://www.usnews.com/news/best-states/montana/articles/2020-03-22/evidence-of-community-spread-in-montanas-gallatin-county
    * https://www.ketv.com/article/coronavirus-covid19-nebraska-omaha-latest/31213658
    * https://www.latimes.com/world-nation/story/2020-03-17/las-vegas-to-close-all-casinos-at-midnight
    * https://whdh.com/news/new-hampshire-bans-dine-in-restaurant-meals-until-april-7/
    * https://www.cnbc.com/2020/03/16/new-york-new-jersey-and-connecticut-agree-to-close-restaurants-limit-events-to-less-than-50-people.html
    * https://www.krqe.com/health/coronavirus-new-mexico/new-restrictions-for-new-mexico-restaurants-and-bars-in-to-begin-monday/
    * https://www.ny1.com/nyc/all-boroughs/coronavirus/2020/03/16/bars-restaurants-gyms-movie-theaters-casinos-new-york-state
    * https://www.newsobserver.com/news/coronavirus/article241284781.html
    * https://www.grandforksherald.com/news/education/5007393-Burgum-closes-bars-restaurants-amid-coronavirus-concerns-schools-to-stay-closed-indefinitely
    * https://www.axios.com/ohio-governor-bars-restaurants-coronavirus-26e4b6e3-7f65-4f6a-abf9-f3940220cc6f.html
    * https://patch.com/rhode-island/newport/coronavirus-ri-dine-restaurants-closed-2-weeks
    * https://www.tennessean.com/story/news/health/2020/03/22/tennessee-governor-restaurants-bars-closed-takeout-and-delivery/2892481001/
    * https://www.texastribune.org/2020/03/19/texas-restaurants-bars-closed-greg-abbott/
    * https://www.sltrib.com/news/2020/03/18/utah-orders-restaurants/
    * https://www.burlingtonfreepress.com/story/news/2020/03/16/coronavirus-vermont-burlington-mayor-orders-24-hour-restaurant-bar-closure/5062491002/
    * https://www.washingtonian.com/2020/03/23/virginia-restaurants-and-bars-close-for-dine-in-service-to-help-curb-coronavirus/
    * https://trib.com/news/state-and-regional/health/wyoming-governor-announces-statewide-business-closures-in-response-to-coronavirus/article_fd9b3090-536e-5e55-902e-0585322740a2.html
    * https://www.nytimes.com/2020/03/12/world/europe/trump-travel-ban-coronavirus.html
