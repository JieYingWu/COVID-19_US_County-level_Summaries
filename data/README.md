# Datasets

* `counties.csv` contains demographic, socioeconomic, health care, education and transit data for
  each county in the 50 states and Washington DC. Note that this also includes analogous data for
  states, as available.
* `infections_timeseries.csv` contains an county-level timeseries of cumulative COVID-19 infections
  in the US.
* `deaths_timeseries.csv` contains analogous information for COVID-19 related deaths.  **Note**
  that the first column in the infections and deaths data corresponds to Jan 22, 2020, or **t =
  737446**.
* `Hospitalization_all_locs.csv` contains a timeseries of projected requirements and deficits for hospital beds, ICUs, ventilators, across all US states from 1st March 2020 till 4th August 2020. The projections have been computed by the IHME "Chris Murray" model. The data has been processed to have a format similar to other timeseries in this dataset.
* `interventions.csv` contains the dates that counties (or states governing them) took measures to
  mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the
  date, where January 1 of year 1 has `t = 1`. This convention is chosen for consistency with the
  python `datetime` library. A date in this format can be converted to year, month, date with:
```python
import datetime
date = datetime.date.fromordinal(ordinal_date)
print(date.month, date.day, date.year)
```
  It has now been updated to include intervention rollbacks. Any type of restaurant or gym reopening was taken as the rollback date (ex. the county could have reopened at 25% capacity and only outdoor, all the way to business as usual)
* `counties_order.csv` contains the FIPS codes and county name for each of these counties. FIPS
  codes are unambiguous identifiers for each county, since the same county name may appear in many
  states. See [this list](https://www.wikiwand.com/en/List_of_the_most_common_U.S._county_names)
  for examples. This is the first three columns of `counties.csv`.
* [list_of_columns.md](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/blob/master/data/list_of_columns.md)
  contains descriptions for each column in `counties.csv`, `counties_only.csv`, etc.
* `recovered_timeseries.csv` is a *limited* timeseries for recovered patients. This data is not
  very well-tracked, but we include it as we are able.
* `google_reports` contains six csv files which correspond to the six areas of interest that Goo
   gle is reporting in its mobility reports.For detailed information about the data:(https://www
   .google.com/covid19/mobility/data_documentation.html#about-this-data) 
`
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
14. State-level hospitalization and ICU requirements projections from [IHME](http://www.healthdata.org/covid/data-downloads).
15. Mobility Reports from [Google](https://www.google.com/covid19/mobility/index.html)
16. COVID-19 related interventions data from numerous media sources:
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
17. Rollback of interventions from numerous media sources:
    * https://covid19.alaska.gov/wp-content/uploads/2020/05/05142020-Reopen-Alaska-Plan.pdf
    * https://abc7news.com/sonoma-county-restaurants-napa-newsoms-plan-to-reopen-california-when/6178845/
    * http://www.calaverasenterprise.com/news/coronavirus_information/article_da41af68-9577-11ea-affd-fb8bc483a30b.html
    * http://www.acphd.org/2019-ncov/shelter-in-place.aspx
    * https://abc7news.com/reopening-california-monterey-tourism-shelter-in-place-carmel-by-the-sea/6257886/
    * https://www.latimes.com/california/story/2020-05-12/coronavirus-beaches-reopen-los-angeles-county-move-toward-new-normal
    * https://covid19.lacounty.gov/covid19-news/nail-salons-spas-tattoo-shops-casinos-bars-and-wineries-reopening-with-safeguards/
    * https://sf.gov/step-by-step/reopening-san-francisco
    * https://www.smcgov.org/smc-reopening
    * https://abc7news.com/santa-cruz-beaches-reopen-covid-is-open-coronavirus/6243867/
    * https://www.visaliatimesdelta.com/story/news/2020/05/27/tulare-county-meets-readiness-criteria-can-reopen-pending-state-approval/5263823002/
    * https://portal.ct.gov/-/media/DECD/Covid_Business_Recovery-Phase-2/Amusement_Parks_C3_V1.pdf
    * https://coronavirus.delaware.gov/reopening/phase2/
    * https://coronavirus.dc.gov/phasetwo
    * https://twitter.com/govrondesantis/status/1261369779035623425?lang=en
    * https://floridahealthcovid19.gov/plan-for-floridas-recovery/
    * https://www.11alive.com/article/news/health/coronavirus/georgia-reopening-dates-plan-kemp/85-1df2aa97-48fd-4cf8-a9fd-afbd8c73dfcf
    * https://rebound.idaho.gov/stages-of-reopening/
    * https://www.pantagraph.com/news/state-and-regional/illinois-stay-at-home-order-ends-and-restrictions-lifted-on-churches-as-the-state-advances/article_71393207-40a5-58cf-a658-c580da3d437d.html
    * https://wcfcourier.com/news/local/govt-and-politics/update-watch-now-iowa-to-reopen-restaurants-friday/article_7636be19-9dec-5cb9-8344-29c6aafd0196.html
    * https://www.thegazette.com/subject/news/business/gyms-working-up-a-sweat-to-reopen-friday-20200514
    * https://gov.louisiana.gov/index.cfm/newsroom/detail/2573
    * https://conduitstreet.mdcounties.org/2020/05/15/marylands-reopening-status-by-county/
    * https://www.aacounty.org/coronavirus/road-to-recovery/
    * https://baltimore.cbslocal.com/reopening-maryland-whats-open-whats-closed-county-by-county/
    * https://www.baltimorecountymd.gov/News/BaltimoreCountyNow/baltimore-county-to-fully-enter-stage-one-reopening
    * https://www.charlescountymd.gov/services/health-and-human-services/covid-19
    * https://health.frederickcountymd.gov/621/Recovery
    * https://www.howardcountymd.gov/News/ArticleID/2007/Coronavirus-Updates-Howard-County-Aligns-with-Governor%E2%80%99s-Phase-2-Reopening-Contact-Tracing-Campaign
    * https://www.montgomerycountymd.gov/covid19/news/index.html
    * https://www.princegeorgescountymd.gov/Archive.aspx?AMID=142
    * https://www.mass.gov/info-details/safety-standards-and-checklist-restaurants
    * https://mn.gov/covid19/for-minnesotans/stay-safe-mn/stay-safe-plan.jsp
    * https://governor.mo.gov/show-me-strong-recovery-plan-guidance-and-frequently-asked-questions
    * https://www.nytimes.com/interactive/2020/us/states-reopen-map-coronavirus.html
    * https://www.sos.mo.gov/library/reference/orders/2020/eo12
    * https://stlpartnership.com/details-on-state-stl-county-and-city-of-stl-reopening/
    * https://www.newmexico.gov/2020/05/28/governor-announces-limited-reopening-for-dine-in-restaurants-indoor-malls-gyms-salons-and-more/
    * https://www.usnews.com/news/best-states/new-mexico/articles/2020-05-25/new-mexico-governor-blocks-plans-to-reopen-drive-in-theater
    * https://nymag.com/intelligencer/2020/07/when-will-new-york-reopen-phases-and-full-plan-explained.html
    * https://www1.nyc.gov/nycbusiness/article/nyc-restaurant-reopening-guide
    * https://www.governor.ny.gov/news/governor-cuomo-announces-outdoor-dining-restaurants-will-be-permitted-phase-two-reopening
    * https://www.nbcnewyork.com/news/local/hundreds-of-restaurants-expected-to-reopen-on-long-island-as-phase-ii-begins-cuomo-shifts-metrics-focus/2454500/
    * https://www.dailyfreeman.com/news/local-news/phase-2-starts-tuesday-in-mid-hudson-region-outdoor-dining-at-restaurants-haircuts-in-store/article_afba1bea-a9a4-11ea-bf5a-677d5abe84e2.html
    * https://www.governor.ny.gov/news/governor-cuomo-announces-capital-region-cleared-global-public-health-experts-enter-phase-4
    * https://www.governor.ny.gov/news/governor-cuomo-announces-five-regions-track-enter-phase-iv-reopening-friday
    * https://spectrumlocalnews.com/nys/buffalo/politics/2020/06/29/western-new-york-begins-phase-4-reopening-tuesday-
    * https://www.dailyfreeman.com/news/local-news/mid-hudson-region-starts-phase-4-of-reopening-process-on-tuesday/article_bf23d59c-bf9f-11ea-bd04-979c464b1ebc.html
    * https://www.newsobserver.com/news/coronavirus/article242836711.html
    * https://www.usnews.com/news/best-states/north-dakota/articles/2020-05-01/north-dakota-cafes-other-businesses-reopen-under-new-rules
    * https://coronavirus.ohio.gov/wps/portal/gov/covid-19/resources/news-releases-news-you-can-use/governor-reopen-certain-facilities
    * https://coronavirus.ohio.gov/wps/portal/gov/covid-19/resources/news-releases-news-you-can-use/reopening-restaurants-bars-personal-care-services
    * https://govstatus.egov.com/reopening-oregon#countyStatuses
    * https://www.clackamas.us/coronavirus/updates
    * https://www.co.marion.or.us/HLT/COVID-19/Pages/Reopening.aspx
    * https://www.co.polk.or.us/ph/covid-19-news
    * https://www.oregon.gov/newsroom/Pages/NewsDetail.aspx?newsid=36806
    * https://www.kgw.com/article/news/health/coronavirus/these-oregon-counties-have-been-approved-for-phase-1-of-reopening/283-b24c4243-bb25-43e7-bafa-75e5126a71a0
    * https://www.wgal.com/article/pennsylvania-counties-reopening-coronavirus/32343176#
    * https://www.governor.pa.gov/newsroom/gov-wolf-12-more-counties-to-move-to-yellow-phase-on-may-22/
    * https://www.pahomepage.com/news/wolf-announces-next-counties-to-move-to-yellow-phase/
    * https://www.mcall.com/coronavirus/mc-nws-coronavirus-pa-counties-reopening-20200509-hqwbnzot5bb6tlw3g3j7qalxhq-story.html
    * https://www.ddec.pr.gov/covid19_informaciongeneral/ 
    * https://governor.sc.gov/news/2020-05/gov-henry-mcmaster-restaurants-are-able-open-limited-dine-services-monday-may-11
    * https://governor.sc.gov/news/2020-05/gov-henry-mcmaster-announces-additional-businesses-gyms-pools-are-able-open-monday-may
    * https://www.wsmv.com/news/tennessee-releases-new-guidelines-for-reopening-restaurants-retail-and-large-attractions/article_0f74cd22-9ad3-11ea-9f03-e3784e1e4029.html
    * https://www.knoxnews.com/story/news/health/2020/06/17/knox-county-moves-align-state-coronavirus-reopening-plan/3205652001/
    * https://www.wjhl.com/local-coronavirus-coverage/sullivan-county-health-officials-mirroring-gov-lees-plan-to-reopen-businesses/
    * https://www.wmcactionnews5.com/2020/06/14/shelby-county-begin-phase-reopening-monday/
    * https://www.asafenashville.org/roadmap-for-reopening-nashville/
    * https://coronavirus-download.utah.gov/Governor/Utah_Leads_Together_3.0_May2020_v20.pdf
    * https://www.governor.virginia.gov/media/governorvirginiagov/governor-of-virginia/pdf/Forward-Virginia-Phase-Three-Guidelines.pdf
    * https://www.governor.wa.gov/sites/default/files/SafeStartPhasedReopening.pdf
    * https://mynorthwest.com/1872686/phases-counties-washington-reopen-inslee/?
    * https://governor.wv.gov/Pages/The-Comeback.aspx
    * https://www.wisbank.com/articles/2020/05/wisconsin-county-list-of-safer-at-home-orders/
    * https://www.wyo-wcca.org/index.php/covid-19-resources/emergency-declarations-and-public-building-access/
    * https://drive.google.com/file/d/1yP1IHC60t9pHQMeenAEzyAuVZJSNAvH2/view
