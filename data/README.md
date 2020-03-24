# Datasets

* `counties.csv` contains demographic, socioeconomic, health care, and education data for each
  county in the 50 states and Washington DC.
* `counties_order.csv` contains the FIPS codes and county name for each of these counties. FIPS
  codes are unambiguous identifiers for each county, since the same county name may appear in many
  states. See [this list](https://www.wikiwand.com/en/List_of_the_most_common_U.S._county_names)
  for examples.

## List of columns (currently)
 ### Identifying variables
| Data variable     | Description |
| ---   | --- |
|FIPS| State-County FIPS Code |
|State| State Abbreviation |
|Area_Name| Area name (State/County) |

### Data variables

 #### Population Estimates
| Data variable     | Description |
| ---   | --- |
|Rural-urban_Continuum Code_2013| Rural-urban Continuum Code, 2013 |
|Urban_Influence_Code_2013| Urban Influence Code, 2013|
|Economic_typology_2015| County economic types, 2015 edition|
|POP_ESTIMATE_2018| 7/1/2018 resident total population estimate |
|N_POP_CHG_2018| Numeric Change in resident total population 7/1/2017 to 7/1/2018|
|Births_2018|Births in period 7/1/2017 to 6/30/2018|
|Deaths_2018| Deaths in period 7/1/2017 to 6/30/2018|
|NATURAL_INC_2018| Natural increase in period 7/1/2017 to 6/30/2018|
|INTERNATIONAL_MIG_2018| Net international migration in period 7/1/2017 to 6/30/2018|
|DOMESTIC_MIG_2018| Net domestic migration in period 7/1/2017 to 6/30/2018|
|NET_MIG_2018| Net migration in period 7/1/2017 to 6/30/2018|
|RESIDUAL_2018| Residual for period 7/1/2017 to 6/30/2018|
|GQ_ESTIMATES_2018| 7/1/2018 Group Quarters total population estimate|
|R_birth_2018| Birth rate in period 7/1/2017 to 6/30/2018|
|R_death_2018| Death rate in period 7/1/2017 to 6/30/2018
|R_NATURAL_INC_2018| Natural increase rate in period 7/1/2016 to 6/30/2017|
|R_INTERNATIONAL_MIG_2018| Net international migration rate in period 7/1/2017 to 6/30/2018|
|R_DOMESTIC_MIG_2018| Net domestic migration rate in period 7/1/2017 to 6/30/2018|
|R_NET_MIG_2018| Net migration rate in period 7/1/2017 to 6/30/2018|

 ####Education
| Data variable     | Description |
| ---   | --- |
|Less than a high school diploma 2014-18	|	Number of adults who do not have a high school diploma|
|High school diploma only 2014-18	| Number of adults who just have a high school diploma|
|Some college or associate's degree 2014-18	| Number of adults with a college degree below bachelor's|
|Bachelor's degree or higher 2014-18|	Number of adults who have at least a bachelor's degree|
|Percent of adults with less than a high school diploma 2014-18|		Percentage of adults who do not have a high school diploma|
|Percent of adults with a high school diploma only 2014-18|	Percentage of adults who just have a high school diploma|
|Percent of adults completing some college or associate's degree 2014-18|		Percentage of adults with a college degree below bachelor's|
|Percent of adults with a bachelor's degree or higher 2014-18|	Percentage of adults who have at least a bachelor's degree|
|POVALL_2018|	Estimate of people of all ages in poverty 2018|
|CI90LBAll_2018|	90% confidence interval lower bound of estimate of people of all ages in poverty 2018|
|CI90UBALL_2018|	90% confidence interval upper bound of estimate of people of all ages in poverty 2018|
|PCTPOVALL_2018|	Estimated percent of people of all ages in poverty 2018|
|CI90LBALLP_2018|	90% confidence interval lower bound of estimate of percent of people of all ages in poverty 2018|
|CI90UBALLP_2018|	90% confidence interval upper bound of estimate of percent of people of all ages in poverty 2018|
|POV017_2018|	Estimate of people age 0-17 in poverty 2018|
|CI90LB017_2018|	90% confidence interval lower bound of estimate of people age 0-17 in poverty 2018|
|CI90UB017_2018|	90% confidence interval upper bound of estimate of people age 0-17 in poverty 2018|
|PCTPOV017_2018|	Estimated percent of people age 0-17 in poverty 2018|
|CI90LB017P_2018|	90% confidence interval lower bound of estimate of percent of people age 0-17 in poverty 2018|
|CI90UB017P_2018|	90% confidence interval upper bound of estimate of percent of people age 0-17 in poverty 2018|
|POV517_2018|	Estimate of related children age 5-17 in families in poverty 2018|
|CI90LB517_2018|	90% confidence interval lower bound of estimate of related children age 5-17 in families in poverty 2018|
|CI90UB517_2018|	90% confidence interval upper bound of estimate of related children age 5-17 in families in poverty 2018|
|PCTPOV517_2018|	Estimated percent of related children age 5-17 in families in poverty 2018|
|CI90LB517P_2018|	90% confidence interval lower bound of estimate of percent of related children age 5-17 in families in poverty 2018|
|CI90UB517P_2018|	90% confidence interval upper bound of estimate of percent of related children age 5-17 in families in poverty 2018|
|MEDHHINC_2018|	Estimate of median household income 2018|
|CI90LBINC_2018|	90% confidence interval lower bound of estimate of median household income 2018|
|CI90UBINC_2018|	90% confidence interval upper bound of estimate of median household income 2018|

#### Employment and median household income
| Data variable     | Description |
| ---   | --- |
|Civilian_labor_force_2018 | Civilian labor force annual average|
|Employed_2018 |	Number employed annual average |
|Unemployed_2018 |	Number unemployed annual average |
|Unemployment_rate_2018 |	Unemployment rate |
|Median_Household_Income_2018 |	Estimate of Median household Income, 2018 |
|Med_HH_Income_Percent_of_State_Total_2018 |	County Household Median Income as a percent of the State Total Median Household Income, 2018 |

#### Climate
| Data variable     | Description |
| ---   | --- |
|Jan Precipitation / inch| Precipitation/inch in the month of Jan for 2019 |
|Feb Precipitation / inch| Precipitation/inch in the month of Feb for 2019 |
|Mar Precipitation / inch| Precipitation/inch in the month of Mar for 2019 |
|Apr Precipitation / inch| Precipitation/inch in the month of Apr for 2019 |
|May Precipitation / inch| Precipitation/inch in the month of May for 2019 |
|Jun Precipitation / inch| Precipitation/inch in the month of Jun for 2019 |
|Jul Precipitation / inch| Precipitation/inch in the month of Jul for 2019 |
|Aug Precipitation / inch| Precipitation/inch in the month of Aug for 2019 |
|Sep Precipitation / inch| Precipitation/inch in the month of Sep for 2019 |
|Oct Precipitation / inch| Precipitation/inch in the month of Oct for 2019 |
|Nov Precipitation / inch| Precipitation/inch in the month of Nov for 2019 |
|Dec Precipitation / inch| Precipitation/inch in the month of Dec for 2019 |
|Jan Temp AVG / F| Average temperature in Jan, 2019 in Fahrenheit |
|Feb Temp AVG / F| Average temperature in Feb, 2019 in Fahrenheit |
|Mar Temp AVG / F| Average temperature in Mar, 2019 in Fahrenheit |
|Apr Temp AVG / F| Average temperature in Apr, 2019 in Fahrenheit |
|May Temp AVG / F| Average temperature in May, 2019 in Fahrenheit |
|Jun Temp AVG / F| Average temperature in Jun, 2019 in Fahrenheit |
|Jul Temp AVG / F| Average temperature in Jul, 2019 in Fahrenheit |
|Aug Temp AVG / F| Average temperature in Aug, 2019 in Fahrenheit |
|Sep Temp AVG / F| Average temperature in Sep, 2019 in Fahrenheit |
|Oct Temp AVG / F| Average temperature in Oct, 2019 in Fahrenheit |
|Nov Temp AVG / F| Average temperature in Nov, 2019 in Fahrenheit |
|Dec Temp AVG / F| Average temperature in Dec, 2019 in Fahrenheit |
|Jan Temp Min / F| Minimum temperature in Jan, 2019 in Fahrenheit |
|Feb Temp Min / F| Minimum temperature in Feb, 2019 in Fahrenheit |
|Mar Temp Min / F| Minimum temperature in Mar, 2019 in Fahrenheit |
|Apr Temp Min / F| Minimum temperature in Apr, 2019 in Fahrenheit |
|May Temp Min / F| Minimum temperature in May, 2019 in Fahrenheit |
|Jun Temp Min / F| Minimum temperature in Jun, 2019 in Fahrenheit |
|Jul Temp Min / F| Minimum temperature in Jul, 2019 in Fahrenheit |
|Aug Temp Min / F| Minimum temperature in Aug, 2019 in Fahrenheit |
|Sep Temp Min / F| Minimum temperature in Sep, 2019 in Fahrenheit |
|Oct Temp Min / F| Minimum temperature in Oct, 2019 in Fahrenheit |
|Nov Temp Min / F| Minimum temperature in Nov, 2019 in Fahrenheit |
|Dec Temp Min / F| Minimum temperature in Dec, 2019 in Fahrenheit |
|Jan Temp Max / F| Maximum temperature in Jan, 2019 in Fahrenheit |
|Feb Temp Max / F| Maximum temperature in Feb, 2019 in Fahrenheit |
|Mar Temp Max / F| Maximum temperature in Mar, 2019 in Fahrenheit |
|Apr Temp Max / F| Maximum temperature in Apr, 2019 in Fahrenheit |
|May Temp Max / F| Maximum temperature in May, 2019 in Fahrenheit |
|Jun Temp Max / F| Maximum temperature in Jun, 2019 in Fahrenheit |
|Jul Temp Max / F| Maximum temperature in Jul, 2019 in Fahrenheit |
|Aug Temp Max / F| Maximum temperature in Aug, 2019 in Fahrenheit |
|Sep Temp Max / F| Maximum temperature in Sep, 2019 in Fahrenheit |
|Oct Temp Max / F| Maximum temperature in Oct, 2019 in Fahrenheit |
|Nov Temp Max / F| Maximum temperature in Nov, 2019 in Fahrenheit |
|Dec Temp Max / F| Maximum temperature in Dec, 2019 in Fahrenheit |

####Housing 
| Data variable     | Description |
| ---   | --- |
|Housing units| Number of housing units as per 2010 census|
|Area in square miles - Total area| Total area in sq. miles as per 2010 census| 
|Area in square miles - Water area| Total water area in sq. miles as per 2010 census|
|Area in square miles - Land area| Total land area in sq. miles as per 2010 census|
|Density per square mile of land area - Population| Land area density for population as per 2010 census|
|Density per square mile of land area - Housing units| Land area density for housing units as per 2010 census|

#### Demographics
| Data variable     | Description |
| ---   | --- |
|Total_Male| Total number of males|
|Total_Female| Total number of females|
|Total_age0to17|Total number of people between ages 0 to 17|
|Male_age0to17|Total number of males between ages 0 to 17|
|Female_age0to17|Total number of females between ages 0 to 17|
|Total_age18to64|Total number of people between ages 18 to 64|
|Male_age18to64|Total number of males between ages 18 to 64|
|Female_age18to64|Total number of females between ages 18 to 64|
|Total_age65plus|Total number of people with age >65|
|Male_age65plus|Total number of males with age >65|
|Female_age65plus|Total number of females with age >65|
|Total_age85plusr|Total number of people with age >85|
|Male_age85plusr|Total number of males with age >85|
|Female_age85plusr|Total number of females with age >85|
|pop_density| Population density as of 2018|
|Total households|Total number of households|
|Total households!!Family households (families)|Total households!!Family households (families)|
|Total households!!Family households (families)!!With own children of the householder under 18 years|Total households!!Family households (families)!!With own children of the householder under 18 years|
|Total households!!Family households (families)!!Married-couple family|Total households!!Family households (families)!!Married-couple family|
|Total households!!Family households (families)!!Married-couple family!!With own children of the householder under 18 years|Total households!!Family households (families)!!Married-couple family!!With own children of the householder under 18 years|
|Total households!!Family households (families)!!Male householder, no wife present, family|Total households!!Family households (families)!!Male householder, no wife present, family|
|HOUSEHOLDS BY TYPE!!|HOUSEHOLDS BY TYPE!!|
|Total households!!Family households (families)!!Female householder, no husband present, family|Total households!!Family households (families)!!Female householder, no husband present, family|
|Total households!!Family households (families)!!Female householder, no husband present, family!!With own children of the householder under 18 years|Total households!!Family households (families)!!Female householder, no husband present, family!!With own children of the householder under 18 years|
|Total households!!Nonfamily households|Total households!!Nonfamily households|
|Total households!!Nonfamily households!!Householder living alone|Total households!!Nonfamily households!!Householder living alone|
|Total households!!Nonfamily households!!Householder living alone!!65 years and over|Total households!!Nonfamily households!!Householder living alone!!65 years and over|
|Total households!!Households with one or more people under 18 years|Total households!!Households with one or more people under 18 years|
|Total households!!Households with one or more people 65 years and over|Total households!!Households with one or more people 65 years and over|
|Total households!!Average household size|Total households!!Average household size|
|Total households!!Average family size|Total households!!Average family size|
|RELATIONSHIP!!Population in households|RELATIONSHIP!!Population in households|
|RELATIONSHIP!!Population in households!!Householder|RELATIONSHIP!!Population in households!!Householder|
|RELATIONSHIP!!Population in households!!Spouse|RELATIONSHIP!!Population in households!!Spouse|
|RELATIONSHIP!!Population in households!!Child|RELATIONSHIP!!Population in households!!Child|
|RELATIONSHIP!!Population in households!!Other relatives|RELATIONSHIP!!Population in households!!Other relatives|
|RELATIONSHIP!!Population in households!!Nonrelatives|RELATIONSHIP!!Population in households!!Nonrelatives|
|RELATIONSHIP!!Population in households!!Nonrelatives!!Unmarried partner|RELATIONSHIP!!Population in households!!Nonrelatives!!Unmarried partner|
|MARITAL STATUS!!Males 15 years and over|MARITAL STATUS!!Males 15 years and over|
|MARITAL STATUS!!Males 15 years and over!!Never married|MARITAL STATUS!!Males 15 years and over!!Never married|
|MARITAL STATUS!!Males 15 years and over!!Now married, except separated|MARITAL STATUS!!Males 15 years and over!!Now married, except separated|
|MARITAL STATUS!!Males 15 years and over!!Separated|MARITAL STATUS!!Males 15 years and over!!Separated|
|MARITAL STATUS!!Males 15 years and over!!Widowed|MARITAL STATUS!!Males 15 years and over!!Widowed|
|MARITAL STATUS!!Males 15 years and over!!Divorced|MARITAL STATUS!!Males 15 years and over!!Divorced|
|MARITAL STATUS!!Females 15 years and over|MARITAL STATUS!!Females 15 years and over|
|MARITAL STATUS!!Females 15 years and over!!Never married|MARITAL STATUS!!Females 15 years and over!!Never married|
|MARITAL STATUS!!Females 15 years and over!!Now married, except separated|MARITAL STATUS!!Females 15 years and over!!Now married, except separated|
|MARITAL STATUS!!Females 15 years and over!!Separated|MARITAL STATUS!!Females 15 years and over!!Separated|
|MARITAL STATUS!!Females 15 years and over!!Widowed|MARITAL STATUS!!Females 15 years and over!!Widowed|
|MARITAL STATUS!!Females 15 years and over!!Divorced|MARITAL STATUS!!Females 15 years and over!!Divorced|
|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school|
|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Nursery school, preschool|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Nursery school, preschool|
|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Kindergarten|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Kindergarten|
|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Elementary school (grades 1-8)|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Elementary school (grades 1-8)|
|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!High school (grades 9-12)|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!High school (grades 9-12)|
|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!College or graduate school|SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!College or graduate school|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over|EDUCATIONAL ATTAINMENT!!Population 25 years and over|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Less than 9th grade|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Less than 9th grade|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!9th to 12th grade, no diploma|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!9th to 12th grade, no diploma|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate (includes equivalency)|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate (includes equivalency)|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Some college, no degree|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Some college, no degree|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Associate's degree|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Associate's degree|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher|
|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree or higher|EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree or higher|
|VETERAN STATUS!!Civilian population 18 years and over|VETERAN STATUS!!Civilian population 18 years and over|
|VETERAN STATUS!!Civilian population 18 years and over!!Civilian veterans|VETERAN STATUS!!Civilian population 18 years and over!!Civilian veterans|
|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population|
|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population!!With a disability|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population!!With a disability|
|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years|
|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years!!With a disability|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years!!With a disability|
|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years|
|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years!!With a disability|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years!!With a disability|
|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over|
|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over!!With a disability|DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over!!With a disability|
|TOT_POP| Total population|
|TOT_MALE| Total male population|
|TOT_FEMALE| Total female population|
|WA_MALE| White alone male population|
|WA_FEMALE| White alone female population|
|BA_MALE| Black or African American alone male population |
|BA_FEMALE| Black or African American alone female population|
|IA_MALE| American Indian and Alaska Native alone male population|
|IA_FEMALE| American Indian and Alaska Native alone female population|
|AA_MALE| Asian alone male population |
|AA_FEMALE| Asian alone female population|
|NA_MALE| Native Hawaiian and Other Pacific Islander alone male population|
|NA_FEMALE| Native Hawaiian and Other Pacific Islander alone female population
|TOM_MALE| Two or More Races male population|
|TOM_FEMALE| Two or More Races female population
|WAC_MALE| White alone or in combination male population|
|WAC_FEMALE| White alone or in combination female population|
|BAC_MALE| Black or African American alone or in combination male population|
|BAC_FEMALE| Black or African American alone or in combination female population
|IAC_MALE| American Indian and Alaska Native alone or in combination male population |
|IAC_FEMALE| American Indian and Alaska Native alone or in combination male population|
|AAC_MALE| Asian alone or in combination male population|
|AAC_FEMALE| Asian alone or in combination female population|
|NAC_MALE| Native Hawaiian and Other Pacific Islander alone or in combination male population|
|NAC_FEMALE| Native Hawaiian and Other Pacific Islander alone or in combination female population|
|NH_MALE| Not Hispanic male population|
|NH_FEMALE| Not Hispanic female population|
|NHWA_MALE| Not Hispanic, White alone male population|
|NHWA_FEMALE| Not Hispanic, White alone female population|
|NHBA_MALE| Not Hispanic, Black or African American alone male population|
|NHBA_FEMALE| Not Hispanic, Black or African American alone female population|
|NHIA_MALE| Not Hispanic, American Indian and Alaska Native alone male population|
|NHIA_FEMALE| Not Hispanic, American Indian and Alaska Native alone female population|
|NHAA_MALE| Not Hispanic, Asian alone male population|
|NHAA_FEMALE| Not Hispanic, Asian alone female population|
|NHNA_MALE| Not Hispanic, Native Hawaiian and Other Pacific Islander alone male population|
|NHNA_FEMALE| Not Hispanic, Native Hawaiian and Other Pacific Islander alone female population|
|NHTOM_MALE| Not Hispanic, Two or More Races male population|
|NHTOM_FEMALE| Not Hispanic, Two or More Races female population|
|NHWAC_MALE| Not Hispanic, White alone or in combination male population|
|NHWAC_FEMALE| Not Hispanic, White alone or in combination female population|
|NHBAC_MALE| Not Hispanic, Black or African American alone or in combination male population|
|NHBAC_FEMALE| Not Hispanic, Black or African American alone or in combination female population|
|NHIAC_MALE| Not Hispanic, American Indian and Alaska Native alone or in combination male population|
|NHIAC_FEMALE| Not Hispanic, American Indian and Alaska Native alone or in combination female population|
|NHAAC_MALE| Not Hispanic, Asian alone or in combination male population|
|NHAAC_FEMALE| Not Hispanic, Asian alone or in combination female population|
|NHNAC_MALE| Not Hispanic, Native Hawaiian and Other Pacific Islander alone or in combination male population|
|NHNAC_FEMALE| Not Hispanic, Native Hawaiian and Other Pacific Islander alone or in combination female population|
|H_MALE| Hispanic male population|
|H_FEMALE| Hispanic female population|
|HWA_MALE| Hispanic, White alone male population|
|HWA_FEMALE| Hispanic, White alone female population|
|HBA_MALE| Hispanic, Black or African American alone male population|
|HBA_FEMALE| Hispanic, Black or African American alone female population|
|HIA_MALE| Hispanic, American Indian and Alaska Native alone male population|
|HIA_FEMALE| Hispanic, American Indian and Alaska Native alone female population|
|HAA_MALE| Hispanic, Asian alone male population|
|HAA_FEMALE| Hispanic, Asian alone female population|
|HNA_MALE| Hispanic, Native Hawaiian and Other Pacific Islander alone male population|
|HNA_FEMALE| Hispanic, Native Hawaiian and Other Pacific Islander alone female population|
|HTOM_MALE| Hispanic, Two or More Races male population|
|HTOM_FEMALE| Hispanic, Two or More Races female population|
|HWAC_MALE| Hispanic, White alone or in combination male population|
|HWAC_FEMALE| Hispanic, White alone or in combination female population|
|HBAC_MALE| Hispanic, Black or African American alone or in combination male population|
|HBAC_FEMALE| Hispanic, Black or African American alone or in combination female population|
|HIAC_MALE| Hispanic, American Indian and Alaska Native alone or in combination male population|
|HIAC_FEMALE| Hispanic, American Indian and Alaska Native alone or in combination female population|
|HAAC_MALE| Hispanic, Asian alone or in combination male population|
|HAAC_FEMALE| Hispanic, Asian alone or in combination female population|
|HNAC_MALE| Hispanic, Native Hawaiian and Other Pacific Islander alone or in combination male population|
|HNAC_FEMALE| Hispanic, Native Hawaiian and Other Pacific Islander alone or in combination female population|

####Healthcare
| Data variable     | Description |
| ---   | --- |
|Active Physicians per 100,000 Population, 2018 (AAMC)|Active Physicians per 100,000 Population, 2018 |
|Total Active Patient Care Physicians per 100,000 Population, 2018 (AAMC)|Total Active Patient Care Physicians per 100,000 Population, 2018 |
|Active Primary Care Physicians per 100,000 Population, 2018 (AAMC)|Active Primary Care Physicians per 100,000 Population, 2018 |
|Active Patient Care Primary Care Physicians per 100,000 Population, 2018 (AAMC)|Active Patient Care Primary Care Physicians per 100,000 Population, 2018 |
|Active General Surgeons per 100,000 Population, 2018 (AAMC)|Active General Surgeons per 100,000 Population, 2018 |
|Active Patient Care General Surgeons per 100,000 Population, 2018 (AAMC)|Active Patient Care General Surgeons per 100,000 Population, 2018 |
|Percentage of Active Physicians Who Are Female, 2018 (AAMC)|Percentage of Active Physicians Who Are Female, 2018 |
|Percentage of Active Physicians Who Are International Medical Graduates (IMGs), 2018 (AAMC)|Percentage of Active Physicians Who Are International Medical Graduates (IMGs), 2018 |
|Percentage of Active Physicians Who Are Age 60 or Older, 2018 (AAMC)|Percentage of Active Physicians Who Are Age 60 or Older, 2018 |
|MD and DO Student Enrollment per 100,000 Population, AY 2018-2019 (AAMC)|MD and DO Student Enrollment per 100,000 Population, AY 2018-2019 |
|Student Enrollment at Public MD and DO Schools per 100,000 Population, AY 2018-2019 (AAMC)|Student Enrollment at Public MD and DO Schools per 100,000 Population, AY 2018-2019 |
|Percentage Change in Student Enrollment at MD and DO Schools, 2008-2018 (AAMC)|Percentage Change in Student Enrollment at MD and DO Schools, 2008-2018 |
|Percentage of MD Students Matriculating In-State, AY 2018-2019 (AAMC)|Percentage of MD Students Matriculating In-State, AY 2018-2019 |
|Total Residents/Fellows in ACGME Programs per 100,000 Population as of December 31, 2018 (AAMC)|Total Residents/Fellows in ACGME Programs per 100,000 Population as of December 31, 2018 |
|Total Residents/Fellows in Primary Care ACGME Programs per 100,000 Population as of Dec. 31, 2018 (AAMC)|Total Residents/Fellows in Primary Care ACGME Programs per 100,000 Population as of Dec. 31, 2018 |
|Percentage of Residents in ACGME Programs Who Are IMGs as of December 31, 2018 (AAMC)|Percentage of Residents in ACGME Programs Who Are IMGs as of December 31, 2018 |
|Ratio of Residents and Fellows (GME) to Medical Students (UME), AY 2017-2018 (AAMC)|Ratio of Residents and Fellows (GME) to Medical Students (UME), AY 2017-2018 |
|Percent Change in Residents and Fellows in ACGME-Accredited Programs, 2008-2018 (AAMC)|Percent Change in Residents and Fellows in ACGME-Accredited Programs, 2008-2018 |
|Percentage of Physicians Retained in State from Undergraduate Medical Education (UME), 2018 (AAMC)|Percentage of Physicians Retained in State from Undergraduate Medical Education (UME), 2018 |
|All Specialties (AAMC)|All Specialties |
|Allergy & Immunology (AAMC)|Allergy & Immunology |
|Anatomic/Clinical Pathology (AAMC)|Anatomic/Clinical Pathology |
|Anesthesiology (AAMC)|Anesthesiology |
|Cardiovascular Disease (AAMC)|Cardiovascular Disease |
|Child & Adolescent Psychiatry** (AAMC)|Child & Adolescent Psychiatry** |
|Critical Care Medicine (AAMC)|Critical Care Medicine |
|Dermatology (AAMC)|Dermatology |
|Emergency Medicine (AAMC)|Emergency Medicine |
|Endocrinology, Diabetes & Metabolism (AAMC)|Endocrinology, Diabetes & Metabolism |
|Family Medicine/General Practice (AAMC)|Family Medicine/General Practice |
|Gastroenterology (AAMC)|Gastroenterology |
|General Surgery (AAMC)|General Surgery |
|Geriatric Medicine*** (AAMC)|Geriatric Medicine*** |
|Hematology & Oncology (AAMC)|Hematology & Oncology |
|Infectious Disease (AAMC)|Infectious Disease |
|Internal Medicine (AAMC)|Internal Medicine |
|Internal Medicine/Pediatrics (AAMC)|Internal Medicine/Pediatrics |
|Interventional Cardiology (AAMC)|Interventional Cardiology |
|Neonatal-Perinatal Medicine (AAMC)|Neonatal-Perinatal Medicine |
|Nephrology (AAMC)|Nephrology |
|Neurological Surgery (AAMC)|Neurological Surgery |
|Neurology (AAMC)|Neurology |
|Neuroradiology (AAMC)|Neuroradiology |
|Obstetrics & Gynecology (AAMC)|Obstetrics & Gynecology |
|Ophthalmology (AAMC)|Ophthalmology |
|Orthopedic Surgery (AAMC)|Orthopedic Surgery |
|Otolaryngology (AAMC)|Otolaryngology |
|Pain Medicine & Pain Management (AAMC)|Pain Medicine & Pain Management |
|Pediatrics** (AAMC)|Pediatrics** |
|Physical Medicine & Rehabilitation (AAMC)|Physical Medicine & Rehabilitation |
|Plastic Surgery (AAMC)|Plastic Surgery |
|Preventive Medicine (AAMC)|Preventive Medicine |
|Psychiatry (AAMC)|Psychiatry |
|Pulmonary Disease (AAMC)|Pulmonary Disease |
|Radiation Oncology (AAMC)|Radiation Oncology |
|Radiology & Diagnostic Radiology (AAMC)|Radiology & Diagnostic Radiology |
|Rheumatology (AAMC)|Rheumatology |
|Sports Medicine (AAMC)|Sports Medicine |
|Thoracic Surgery (AAMC)|Thoracic Surgery |
|Urology (AAMC)|Urology |
|Vascular & Interventional Radiology (AAMC)|Vascular & Interventional Radiology |
|Vascular Surgery (AAMC)|Vascular Surgery |
|State/Local Government hospital beds per 1000 people (2019)|State/Local Government hospital beds per 1000 people (2019)|
|Non-profit hospital beds per 1000 people (2019)|Non-profit hospital beds per 1000 people (2019)|
|For-profit hospital beds per 1000 people (2019)|For-profit hospital beds per 1000 people (2019)|
|Total hospital beds per 1000 people (2019)|Total hospital beds per 1000 people (2019)|
|Total nurses (2019)|Total nurses (2019)|
|Total physical assistants (2019)|Total physical assistants (2019)|
|Total Hospitals (2019)|Total Hospitals (2019)|
|Internal Medicine specialists (2019)|Internal Medicine specialists (2019)|
|Family Medicine/General Practice specialists (2019)|Family Medicine/General Practice specialists (2019)|
|Pediatrics specialists (2019)|Pediatrics specialists (2019)|
|Obstetrics & Gynecology specialists (2019)|Obstetrics & Gynecology specialists (2019)|
|Geriatrics specialists (2019)|Geriatrics specialists (2019)|
|Total Primary Care specialists (2019)|Total Primary Care specialists (2019)|
|Psychiatry specialists (2019)|Psychiatry specialists (2019)|
|Surgery specialists (2019)|Surgery specialists (2019)|
|Anesthesiology specialists (2019)|Anesthesiology specialists (2019)|
|Emergency Medicine specialists (2019)|Emergency Medicine specialists (2019)|
|Radiology specialists (2019)|Radiology specialists (2019)|
|Cardiology specialists (2019)|Cardiology specialists (2019)|
|Oncology (Cancer) specialists (2019)|Oncology (Cancer) specialists (2019)|
|Endocrinology, Diabetes, and Metabolism specialists (2019)|Endocrinology, Diabetes, and Metabolism specialists (2019)|
|All Other Specialties specialists (2019)|All Other Specialties specialists (2019)|
|Total specialists (2019)|Total specialists (2019)|
