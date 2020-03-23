The entire set of historical LAUS data for New York State, New York City, 
Balance of State, counties, cities, MSA's, Labor Market Region's and WIB area's are in the
comma-separated-value (CSV) data file(s).

laus_state.txt
laus_counties.txt
laus_cities.txt
laus_msas.txt
laus_regions.txt
laus_wib.txt


COLUMN HEADINGS			DATA DEFINITIONS

AREA				Area Name
YEAR				Year
MONTH				Month of the year, Where zero denotes annual average
LABORFORCE			Civilian Labor Force 
EMP				Civilian Employment 
UNEMP				Civilian Unemployment 
UNEMPRATE			Unemployment Rate


UNEMPLOYMENT RATES AND LABOR FORCE (LAUS) TECHNICAL NOTES

Introduction 
**************
The Local Area Unemployment Statistics (LAUS) program is a federal-state cooperative 
effort in which monthly estimates of total employment and unemployment are prepared 
for approximately 6,800 areas across the United States. In New York State, LAUS data 
are available for the state, labor market regions, metropolitan areas, counties, and 
municipalities of at least 25,000.

Labor force, employment and unemployment data are based on the same concepts and 
definitions as those used for the official national estimates obtained from the Current 
Population Survey (CPS), a sample survey of households that is conducted for the U.S. 
Bureau of Labor Statistics by the U.S. Bureau of the Census.


Cautions When Using These Data 
***************************************
There are a number of caveats to be aware of when using LAUS data. Below is a list of 
the most important ones: 

* The "Employment" which is shown under "Labor Force" is not directly comparable to 
the "Total Nonfarm" employment data from the Current Employment Series (CES) 
survey. See comparing sources of employment data for more information. 

* Sub-state labor force data are not seasonally adjusted. When doing a comparison with 
State and U.S. rates, it is important to use "Not Adjusted for Seasonality" labor force 
data for the State and the nation. 

* The unemployment rate usually gets the most attention, as it is a rough gauge of the 
area's labor market. It is best to consider the unemployment rate over a period of 
several months, or years. The employment and unemployment figures tend to vary from 
month to month for many reasons. Seasonal variation often may not reflect the 
economic conditions in all areas of the county. Seasonal factors may contribute to an 
area's high unemployment rate, but firms in some industries may have difficulty finding 
qualified employees. The labor market can vary greatly in different industries, in 
different occupations, and in different parts of the county. 

* The annual average figures, over time, tend to be a better gauge of the labor force 
trends within the area. 

* Month-to-month labor force data are a useful indicator to show the seasonal changes 
in the area, such as outdoor activities (e.g. construction), holiday hiring, school 
schedules, and agricultural patterns. 

* Changes in the method of estimating substate areas caused breaks in the continuity of 
the data series. These breaks occured during the following periods: March 1988 to April 
1988; October 1989 to November 1989; December 1989 to January 1990; December 1993 to 
January 1994; and December 1999 to January 2000. Because of the changes in methodology, 
data for the period preceding each break are not comparable to data for the period 
following each break.


Area Name (New York State, Labor Market Regions, Metropolitan Areas, and Counties)
****************************************************************************************************
New York State consists of 62 counties. Counties are the building blocks used to 
build progressively larger geographic areas for which labor market statistics 
are reported. These larger areas include Core Based Statistical Areas (CBSAs) 
and labor market regions (LMRs). Each CBSA consists of a county or associated 
counties containing at least one urban area of 10,000 or more population, plus 
adjacent, outlying counties that have a high degree of social and economic 
integration with the core. An outlying county is included in the CBSA if at 
least 25 percent of its employed residents work in the central county (or 
counties) or if not less than 25 percent of the jobs in the outlying county are 
held by residents of the central county (or counties). There are two types of 
CBSAs: Metropolitan Statistical Areas and Micropolitan Statistical Areas.  Each 
Metropolitan Statistical Area must have at least one urban area of 50,000 or 
more inhabitants.  Each Micropolitan Statistical Area must have at least one 
urban area of at least 10,000 but less than 50,000 inhabitants.  New York State 
has eleven Metropolitan Statistical Areas and fifteen Micropolitan Statistical 
Areas. If specified criteria are met, a Metropolitan Statistical Area containing 
a single core with a population of 2.5 million or more may be subdivided to form 
smaller groupings of counties referred to as "Metropolitan Divisions."  New York 
State's portion of the New York-Northern New Jersey-Long Island, NY-NJ-PA 
Metropolitan Statistical Area includes the Nassau-Suffolk Metropolitan Division 
as well as the New York City labor market area and the Putnam-Rockland-
Westchester labor market area. If two adjacent Metropolitan or Micropolitan 
Statistical Areas have a certain degree of employment interchange, for reporting 
purposes they may be combined into a single geographic entity know as a Combined 
Statistical Area (CSA).  New York State has five CSAs entirely within its 
borders and a sixth - the New York-Newark-Bridgeport CSA - which includes 
portions of  Pennsylvania, New Jersey, and Connecticut. 


Metropolitan statistical areas: 
  Albany-Schenectady-Troy: Albany, Rensselaer, Saratoga, Schenectady and Schoharie counties. 
  Binghamton: Broome and Tioga counties. 
  Buffalo-Niagara Falls: Erie and Niagara counties.
  Elmira: Chemung County. 
  Glens Falls: Warren and Washington counties. 
  Ithaca: Tompkins County. 
  Kingston: Ulster County. 
  Nassau-Suffolk Metropolitan Division: Nassau and Suffolk counties. 
  New York City labor market area: Bronx, Kings, New York, Queens and Richmond counties. 
  Poughkeepsie-Newburgh-Middletown: Dutchess and Orange counties. 
  Putnam-Rockland-Westchester labor market area: Putnam, Rockland and Westchester counties. 
  Rochester: Genesee, Livingston, Monroe, Ontario, Orleans and Wayne counties. 
  Syracuse: Cayuga, Madison, Onondaga and Oswego counties. 
  Utica-Rome: Herkimer and Oneida counties. 
 
Micropolitan statistical areas: 
  Amsterdam: Montgomery County
  Auburn: Cayuga County
  Batavia: Genesee County
  Corning: Steuben County
  Cortland: Cortland County
  Gloversville: Fulton County
  Hudson: Columbia County
  Jamestown-Dunkirk-Fredonia: Chautauqua County
  Malone: Franklin County
  Ogdensburg-Massena: St. Lawrence County
  Olean: Cattaraugus County
  Oneonta: Otsego County
  Plattsburgh: Clinton County
  Seneca Falls: Seneca County
  Watertown-Ft. Drum: Jefferson County
 
Combined statistical areas: 
  Albany-Schenectady-Amsterdam: Albany-Schenectady-Troy and Glens Falls Metropolitan Statistical Areas and Amsterdam, Gloversville and Hudson Micropolitan Statistical Areas.
  Buffalo-Niagara-Cattaraugus: Buffalo-Niagara Falls Metropolitan Statistical Area and Olean Micropolitan Statistical Area. 
  Ithaca-Cortland: Ithaca Metropolitan Statistical Area and Cortland Micropolitan Statistical Area.
  Rochester-Batavia-Seneca Falls: Rochester Metropolitan Statistical Area and Batavia and Seneca Falls Micropolitan Statistical Areas. 
  Syracuse-Auburn: Syracuse Metropolitan Statistical Area and Auburn Micropolitan Statistical Area. 
Labor market regions: 
  Capital: Albany, Columbia, Greene, Rensselaer, Saratoga, Schenectady, Warren, and Washington counties. 
  Central New York: Cayuga, Cortland, Madison, Onondaga, and Oswego counties. 
  Finger Lakes: Genesee, Livingston, Monroe, Ontario, Orleans, Seneca, Wayne, Wyoming, and Yates counties. 
  Hudson Valley: Dutchess, Orange, Putnam, Rockland, Sullivan, Ulster and Westchester counties. 
  Long Island: Nassau and Suffolk counties. 
  Mohawk Valley: Fulton, Herkimer, Montgomery, Oneida, Otsego, and Schoharie counties. 
  New York City: Bronx, Kings, New York, Queens and Richmond counties. 
  North Country: Clinton, Essex, Franklin, Hamilton, Jefferson, Lewis, and St. Lawrence counties. 
  Southern Tier: Broome, Chemung, Chenango, Delaware, Schuyler, Steuben, Tioga, and Tompkins counties. 
  Western New York: Allegany, Cattaraugus, Chautauqua, Erie, and Niagara counties. 
 

Civilian Labor Force
***********************
Civilian Labor Force is the sum of civilian employment and civilian unemployment. 
These individuals are civilians (not members of the Armed Services) who are age 16 
years or older, and are not in institutions such as prisons, mental hospitals, or nursing 
homes.


Civilian Employment
***********************
Civilian Employment includes all individuals who worked at least one hour for a wage or 
salary, or were self-employed, or were working at least 15 unpaid hours in a family 
business or on a family farm, during the week including the 12th of the month. Those 
who were on vacation, other kinds of leave, or involved in a labor dispute, were also 
counted as employed.


Civilian Unemployment
**************************
Civilian Unemployment includes those individuals who were not working but were able, 
available, and actively looking for work during the week including the 12th of the month. 
Individuals who were waiting to be recalled from a layoff, and individuals waiting to 
report to a new job within 30 days were also considered to be unemployed.


Unemployment Rate
************************
Unemployment Rate is the number of unemployed as a percentage of the labor force.


