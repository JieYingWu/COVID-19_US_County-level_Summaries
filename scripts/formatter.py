"""
Read the raw data and convert it to the machine-readable format.

Meant to be run from the root as `python scripts/make_data.py`.

"""

from shutil import copyfile
from os.path import join, exists
import numpy as np
import re
from collections import OrderedDict
import csv
import argparse
import json
import datetime


class Formatter():
  states = {
    'alabama': 'AL',
    'alaska': 'AK',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'district of columbia': 'DC',
    'florida': 'FL',
    'georgia': 'GA',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'nebraska': 'NE',
    'nevada': 'NV',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'new york': 'NY',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'puerto rico': 'PR',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'united states': 'US',
    'utah': 'UT',
    'vermont': 'VT',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY'}
  abbreviations = dict((v, k) for k, v in states.items())

  keys = [
    'population',
    'education',
    'poverty',
    'unemployment',
    'climate',
    'density',
    'demographics',
    'health',
    'transit',
    'crime'
  ]
  
  national_data_skiprows = {
    'population': 2,
    'education': 4,
    'poverty': 4,
    'unemployment': 4,
    'climate': 0,
    'density': 1,
    'demographics': 0,
    'health': 0,
    'transit': 0,
    'crime': 0
  }

  # which column has the fips code in each table
  fips_columns = {
    'population': 0,
    'education': 0,
    'poverty': 0,
    'unemployment': 0,
    'climate': 0,
    'density': 3,
    'demographics': 0,
    'health': 0,
    'transit': 1,
    'crime': 1
  }

  national_data_delimiters = {'demographics': ';',
                              'transit': ';',
                              'crime': ';'}
  
  national_data_which_columns = OrderedDict([
    ('population', [
      0,                        # FIPS
      1,                        # State
      2,                        # Area_Name
      4,                        # Rural-urban_Continuum Code_2013
      6,                        # Urban_Influence_Code_2013
      7,                        # Economic_typology_2015
      18,                       # POP_ESTIMATE_2018
      27,                       # N_POP_CHG_2018
      36,                       # Births_2018
      45,                       # Deaths_2018
      54,                       # NATURAL_INC_2018
      63,                       # INTERNATIONAL_MIG_2018
      72,                       # DOMESTIC_MIG_2018
      81,                       # NET_MIG_2018
      90,                       # RESIDUAL_2018
      100,                      # GQ_ESTIMATES_2018
      108,                      # R_birth_2018
      116,                      # R_death_2018
      124,                      # R_NATURAL_INC_2018
      132,                      # R_INTERNATIONAL_MIG_2018
      140,                      # R_DOMESTIC_MIG_2018
      148                       # R_NET_MIG_2018
    ]),
    
    ('education', [
      39,                       # Less than a high school diploma, 2014-18
      40,                       # High school diploma only, 2014-18
      41,                       # Some college or associate's degree, 2014-18
      42,                       # Bachelor's degree or higher, 2014-18
      43,                       # Percent of adults with less than a high school diploma, 2014-18
      44,                       # Percent of adults with a high school diploma only, 2014-18
      45,                       # Percent of adults completing some college or associate's degree, 2014-18
      46                        # Percent of adults with a bachelor's degree or higher, 2014-18
    ]),
    
    ('poverty', [
      7,                        # POVALL_2018
      8,                        # CI90LBAll_2018
      9,                        # CI90UBALL_2018
      10,                       # PCTPOVALL_2018
      11,                       # CI90LBALLP_2018
      12,                       # CI90UBALLP_2018
      13,                       # POV017_2018
      14,                       # CI90LB017_2018
      15,                       # CI90UB017_2018
      16,                       # PCTPOV017_2018
      17,                       # CI90LB017P_2018
      18,                       # CI90UB017P_2018
      19,                       # POV517_2018
      20,                       # CI90LB517_2018
      21,                       # CI90UB517_2018
      22,                       # PCTPOV517_2018
      23,                       # CI90LB517P_2018
      24,                       # CI90UB517P_2018
      25,                       # MEDHHINC_2018
      26,                       # CI90LBINC_2018
      27                        # CI90UBINC_2018
    ]),
    
    ('unemployment', [
      50,                      # Civilian_labor_force_2018
      51,                      # Employed_2018
      52,                      # Unemployed_2018
      53,                      # Unemployment_rate_2018
      54,                      # Median_Household_Income_2018
      55                       # Med_HH_Income_Percent_of_State_Total_2018
    ]),
    
    ('climate', [
      1,                        # Jan Precipitation / inch
      2,                        # Feb Precipitation / inch
      3,                        # Mar Precipitation / inch
      4,                        # Apr Precipitation / inch
      5,                        # May Precipitation / inch
      6,                        # Jun Precipitation / inch
      7,                        # Jul Precipitation / inch
      8,                        # Aug Precipitation / inch
      9,                        # Sep Precipitation / inch
      10,                       # Oct Precipitation / inch
      11,                       # Nov Precipitation / inch
      12,                       # Dec Precipitation / inch
      13,                       # Jan Temp AVG / F
      14,                       # Feb Temp AVG / F
      15,                       # Mar Temp AVG / F
      16,                       # Apr Temp AVG / F
      17,                       # May Temp AVG / F
      18,                       # Jun Temp AVG / F
      19,                       # Jul Temp AVG / F
      20,                       # Aug Temp AVG / F
      21,                       # Sep Temp AVG / F
      22,                       # Oct Temp AVG / F
      23,                       # Nov Temp AVG / F
      24,                       # Dec Temp AVG / F
      25,                       # Jan Temp Min / F
      26,                       # Feb Temp Min / F
      27,                       # Mar Temp Min / F
      28,                       # Apr Temp Min / F
      29,                       # May Temp Min / F
      30,                       # Jun Temp Min / F
      31,                       # Jul Temp Min / F
      32,                       # Aug Temp Min / F
      33,                       # Sep Temp Min / F
      34,                       # Oct Temp Min / F
      35,                       # Nov Temp Min / F
      36,                       # Dec Temp Min / F
      37,                       # Jan Temp Max / F
      38,                       # Feb Temp Max / F
      39,                       # Mar Temp Max / F
      40,                       # Apr Temp Max / F
      41,                       # May Temp Max / F
      42,                       # Jun Temp Max / F
      43,                       # Jul Temp Max / F
      44,                       # Aug Temp Max / F
      45,                       # Sep Temp Max / F
      46,                       # Oct Temp Max / F
      47,                       # Nov Temp Max / F
      48                        # Dec Temp Max / F
    ]),
    
    ('density', [
      8,                        # Housing units
      9,                        # Area in square miles - Total area
      10,                       # Area in square miles - Water area
      11,                       # Area in square miles - Land area
      12,                       # Density per square mile of land area - Population
      13                        # Density per square mile of land area - Housing units
    ]),
    
    ('demographics', [
      3,                      #  Total_Male
      4,                      #  Total_Female
      5,                      # Total_age0to17
      6,                      # Male_age0to17
      7,                      # Female_age0to17
      8,                      # Total_age18to64
      9,                      # Male_age18to64
      10,                      # Female_age18to64
      11,                      # Total_age65plus
      12,                      # Male_age65plus
      13,                      # Female_age65plus
      14,                      # Total_age85plusr
      15,                      # Male_age85plusr
      16,                      # Female_age85plusr
      18,                      # Total households
      19,                      # Total households!!Family households (families)
      20,                      # Total households!!Family households (families)!!With own children of the householder under 18 years
      21,                      # Total households!!Family households (families)!!Married-couple family
      22,                      # Total households!!Family households (families)!!Married-couple family!!With own children of the householder under 18 years
      23,                      # Total households!!Family households (families)!!Male householder, no wife present, family
      24,                      # HOUSEHOLDS BY TYPE!!
      25,                      # Total households!!Family households (families)!!Female householder, no husband present, family
      26,                      # Total households!!Family households (families)!!Female householder, no husband present, family!!With own children of the householder under 18 years
      27,                      # Total households!!Nonfamily households
      28,                      # Total households!!Nonfamily households!!Householder living alone
      29,                      # Total households!!Nonfamily households!!Householder living alone!!65 years and over
      30,                      # Total households!!Households with one or more people under 18 years
      31,                      # Total households!!Households with one or more people 65 years and over
      32,                      # Total households!!Average household size
      33,                      # Total households!!Average family size
      34,                      # RELATIONSHIP!!Population in households
      35,                      # RELATIONSHIP!!Population in households!!Householder
      36,                      # RELATIONSHIP!!Population in households!!Spouse
      37,                      # RELATIONSHIP!!Population in households!!Child
      38,                      # RELATIONSHIP!!Population in households!!Other relatives
      39,                      # RELATIONSHIP!!Population in households!!Nonrelatives
      40,                      # RELATIONSHIP!!Population in households!!Nonrelatives!!Unmarried partner
      41,                      # MARITAL STATUS!!Males 15 years and over
      42,                      # MARITAL STATUS!!Males 15 years and over!!Never married
      43,                      # MARITAL STATUS!!Males 15 years and over!!Now married, except separated
      44,                      # MARITAL STATUS!!Males 15 years and over!!Separated
      45,                      # MARITAL STATUS!!Males 15 years and over!!Widowed
      46,                      # MARITAL STATUS!!Males 15 years and over!!Divorced
      47,                      # MARITAL STATUS!!Females 15 years and over
      48,                      # MARITAL STATUS!!Females 15 years and over!!Never married
      49,                      # MARITAL STATUS!!Females 15 years and over!!Now married, except separated
      50,                      # MARITAL STATUS!!Females 15 years and over!!Separated
      51,                      # MARITAL STATUS!!Females 15 years and over!!Widowed
      52,                      # MARITAL STATUS!!Females 15 years and over!!Divorced
      53,                      # SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school
      54,                      # SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Nursery school, preschool
      55,                      # SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Kindergarten
      56,                      # SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!Elementary school (grades 1-8)
      57,                      # SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!High school (grades 9-12)
      58,                      # SCHOOL ENROLLMENT!!Population 3 years and over enrolled in school!!College or graduate school
      69,                      # VETERAN STATUS!!Civilian population 18 years and over
      70,                      # VETERAN STATUS!!Civilian population 18 years and over!!Civilian veterans
      71,                      # DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population
      72,                      # DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Total Civilian Noninstitutionalized Population!!With a disability
      73,                      # DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years
      74,                      # DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!Under 18 years!!With a disability
      75,                      # DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years
      76,                      # DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!18 to 64 years!!With a disability
      77,                      # DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over
      78,                      # DISABILITY STATUS OF THE CIVILIAN NONINSTITUTIONALIZED POPULATION!!65 years and over!!With a disability
      80,                      # TOT_MALE
      81,                      # TOT_FEMALE
      82,                      # WA_MALE
      83,                      # WA_FEMALE
      84,                      # BA_MALE
      85,                      # BA_FEMALE
      86,                      # IA_MALE
      87,                      # IA_FEMALE
      88,                      # AA_MALE
      89,                      # AA_FEMALE
      90,                      # NA_MALE
      91,                      # NA_FEMALE
      92,                      # TOM_MALE
      93,                      # TOM_FEMALE
      94,                      # WAC_MALE
      95,                      # WAC_FEMALE
      96,                      # BAC_MALE
      97,                      # BAC_FEMALE
      98,                      # IAC_MALE
      99,                      # IAC_FEMALE
      100,                      # AAC_MALE
      101,                      # AAC_FEMALE
      102,                      # NAC_MALE
      103,                      # NAC_FEMALE
      104,                      # NH_MALE
      105,                      # NH_FEMALE
      106,                      # NHWA_MALE
      107,                      # NHWA_FEMALE
      108,                      # NHBA_MALE
      109,                      # NHBA_FEMALE
      110,                      # NHIA_MALE
      111,                      # NHIA_FEMALE
      112,                      # NHAA_MALE
      113,                      # NHAA_FEMALE
      114,                      # NHNA_MALE
      115,                      # NHNA_FEMALE
      116,                      # NHTOM_MALE
      117,                      # NHTOM_FEMALE
      118,                      # NHWAC_MALE
      119,                      # NHWAC_FEMALE
      120,                      # NHBAC_MALE
      121,                      # NHBAC_FEMALE
      122,                      # NHIAC_MALE
      123,                      # NHIAC_FEMALE
      124,                      # NHAAC_MALE
      125,                      # NHAAC_FEMALE
      126,                      # NHNAC_MALE
      127,                      # NHNAC_FEMALE
      128,                      # H_MALE
      129,                      # H_FEMALE
      130,                      # HWA_MALE
      131,                      # HWA_FEMALE
      132,                      # HBA_MALE
      133,                      # HBA_FEMALE
      134,                      # HIA_MALE
      135,                      # HIA_FEMALE
      136,                      # HAA_MALE
      137,                      # HAA_FEMALE
      138,                      # HNA_MALE
      139,                      # HNA_FEMALE
      140,                      # HTOM_MALE
      141,                      # HTOM_FEMALE
      142,                      # HWAC_MALE
      143,                      # HWAC_FEMALE
      144,                      # HBAC_MALE
      145,                      # HBAC_FEMALE
      146,                      # HIAC_MALE
      147,                      # HIAC_FEMALE
      148,                      # HAAC_MALE
      149,                      # HAAC_FEMALE
      150,                      # HNAC_MALE
      151                       # HNAC_FEMALE
    ]),

    ('health', [
      5,                      # Active Physicians per 100,000 Population, 2018 (AAMC)
      6,                      # Total Active Patient Care Physicians per 100,000 Population, 2018 (AAMC)
      7,                      # Active Primary Care Physicians per 100,000 Population, 2018 (AAMC)
      8,                      # Active Patient Care Primary Care Physicians per 100,000 Population, 2018 (AAMC)
      9,                      # Active General Surgeons per 100,000 Population, 2018 (AAMC)
      10,                      # Active Patient Care General Surgeons per 100,000 Population, 2018 (AAMC)
      11,                      # Percentage of Active Physicians Who Are Female, 2018 (AAMC)
      12,                      # Percentage of Active Physicians Who Are International Medical Graduates (IMGs), 2018 (AAMC)
      13,                      # Percentage of Active Physicians Who Are Age 60 or Older, 2018 (AAMC)
      14,                      # MD and DO Student Enrollment per 100,000 Population, AY 2018-2019 (AAMC)
      15,                      # Student Enrollment at Public MD and DO Schools per 100,000 Population, AY 2018-2019 (AAMC)
      16,                      # Percentage Change in Student Enrollment at MD and DO Schools, 2008-2018 (AAMC)
      17,                      # Percentage of MD Students Matriculating In-State, AY 2018-2019 (AAMC)
      18,                      # Total Residents/Fellows in ACGME Programs per 100,000 Population as of December 31, 2018 (AAMC)
      19,                      # Total Residents/Fellows in Primary Care ACGME Programs per 100,000 Population as of Dec. 31, 2018 (AAMC)
      20,                      # Percentage of Residents in ACGME Programs Who Are IMGs as of December 31, 2018 (AAMC)
      21,                      # Ratio of Residents and Fellows (GME) to Medical Students (UME), AY 2017-2018 (AAMC)
      22,                      # Percent Change in Residents and Fellows in ACGME-Accredited Programs, 2008-2018 (AAMC)
      23,                      # Percentage of Physicians Retained in State from Undergraduate Medical Education (UME), 2018 (AAMC)
      24,                      # All Specialties (AAMC)
      25,                      # Allergy & Immunology (AAMC)
      26,                      # Anatomic/Clinical Pathology (AAMC)
      27,                      # Anesthesiology (AAMC)
      28,                      # Cardiovascular Disease (AAMC)
      29,                      # Child & Adolescent Psychiatry** (AAMC)
      30,                      # Critical Care Medicine (AAMC)
      31,                      # Dermatology (AAMC)
      32,                      # Emergency Medicine (AAMC)
      33,                      # Endocrinology, Diabetes & Metabolism (AAMC)
      34,                      # Family Medicine/General Practice (AAMC)
      35,                      # Gastroenterology (AAMC)
      36,                      # General Surgery (AAMC)
      37,                      # Geriatric Medicine*** (AAMC)
      38,                      # Hematology & Oncology (AAMC)
      39,                      # Infectious Disease (AAMC)
      40,                      # Internal Medicine (AAMC)
      41,                      # Internal Medicine/Pediatrics (AAMC)
      42,                      # Interventional Cardiology (AAMC)
      43,                      # Neonatal-Perinatal Medicine (AAMC)
      44,                      # Nephrology (AAMC)
      45,                      # Neurological Surgery (AAMC)
      46,                      # Neurology (AAMC)
      47,                      # Neuroradiology (AAMC)
      48,                      # Obstetrics & Gynecology (AAMC)
      49,                      # Ophthalmology (AAMC)
      50,                      # Orthopedic Surgery (AAMC)
      51,                      # Otolaryngology (AAMC)
      52,                      # Pain Medicine & Pain Management (AAMC)
      53,                      # Pediatrics** (AAMC)
      54,                      # Physical Medicine & Rehabilitation (AAMC)
      55,                      # Plastic Surgery (AAMC)
      56,                      # Preventive Medicine (AAMC)
      57,                      # Psychiatry (AAMC)
      58,                      # Pulmonary Disease (AAMC)
      59,                      # Radiation Oncology (AAMC)
      60,                      # Radiology & Diagnostic Radiology (AAMC)
      61,                      # Rheumatology (AAMC)
      62,                      # Sports Medicine (AAMC)
      63,                      # Thoracic Surgery (AAMC)
      64,                      # Urology (AAMC)
      65,                      # Vascular & Interventional Radiology (AAMC)
      66,                      # Vascular Surgery (AAMC)
      # 67,                      # State/Local Government hospital beds per 1000 people (2019)
      # 68,                      # Non-profit hospital beds per 1000 people (2019)
      # 69,                      # For-profit hospital beds per 1000 people (2019)
      # 70,                      # Total hospital beds per 1000 people (2019)
      71,                      # Total nurse practitioners (2019)
      72,                      # Total physician assistants (2019)
      73,                      # Total Hospitals (2019)
      74,                      # Internal Medicine Primary Care (2019)
      75,                      # Family Medicine/General Practice Primary Care (2019)
      76,                      # Pediatrics Primary Care (2019)
      77,                      # Obstetrics & Gynecology Primary Care (2019)
      78,                      # Geriatrics Primary Care (2019)
      79,                      # Total Primary Care Physicians (2019)
      80,                      # Psychiatry specialists (2019)
      81,                      # Surgery specialists (2019)
      82,                      # Anesthesiology specialists (2019)
      83,                      # Emergency Medicine specialists (2019)
      84,                      # Radiology specialists (2019)
      85,                      # Cardiology specialists (2019)
      86,                      # Oncology (Cancer) specialists (2019)
      87,                      # Endocrinology, Diabetes, and Metabolism specialists (2019)
      88,                      # All Other Specialties specialists (2019)
      89,                      # Total Specialist Physicians (2019)
      90                       # ICU Beds
    ]),

    ('transit', [
      2                      # transit_scores - population weighted averages aggregated from town/city level to county
    ]),
    ('crime', [
      2,                      # crime_rate_per_100000
      3,                      # COUNTY POPULATION-AGENCIES REPORT ARRESTS
      4,                      # COUNTY POPULATION-AGENCIES REPORT CRIMES
      5,                      # NUMBER OF AGENCIES IN COUNTY REPORT ARRESTS
      6,                      # NUMBER OF AGENCIES IN COUNTY REPORT CRIMES
      7,                      # COVERAGE INDICATOR
      8,                      # Total number of UCR (Uniform Crime Report) Index crimes, excluding arson.
      9,                      # Total number of UCR (Uniform Crime Report) index crimes reported, including arson
      10,                      # MURDER
      11,                      # RAPE
      12,                      # ROBBERY
      13,                      # Number of AGGRAVATED ASSAULTS
      14,                      # BURGLRY
      15,                      # LARCENY
      16,                      # MOTOR VEHICLE THEFTS
      17,                      # ARSON
    ])
  ])

  # map the old columns to the new columns
  national_data_column_mapping = {}
  for k in keys:
    national_data_column_mapping[k] = {}
    i = 0
    for idx in national_data_which_columns[k]:
      national_data_column_mapping[k][idx] = i
      i += 1
  
  def __init__(self, args):
    self.args = args
    for k, v in args.__dict__.items():
      setattr(self, k, v)

    self.national_data_filenames = {
      'population': join(self.raw_data_dir, 'national', 'Demographics', 'PopulationEstimates.csv'),
      'education': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'Education.csv'),
      'poverty': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'PovertyEstimates.csv'),
      'unemployment': join(self.raw_data_dir, 'national', 'Socioeconomic_status', 'Unemployment.csv'),
      # 'climate': join(self.raw_data_dir, 'national', 'Climate', 'FIPS_2019_precipitation_tempAvg_tempMin_tempMax.csv'),
      'climate': join(self.raw_data_dir, 'national', 'Climate', 'unified_climate.csv'),
      'density': join(self.raw_data_dir, 'national', 'Density', 'housing_area_density_national_2010_census.csv'),
      'demographics': join(self.raw_data_dir, 'national', 'Demographics', 'demographics_by_county.csv'),
      'health': join(self.raw_data_dir, 'national', 'healthcare_services_per_county.csv'),
      'transit': join(self.raw_data_dir, 'national', 'transit_scores.csv'),
      'crime': join(self.raw_data_dir, 'national', 'crime_data.csv')
    }
    
    self._make_reference()
    # self._write_reference()

  def _get_key(self, key):
    return key.lower().strip()
    
  def _get_state(self, x):
    """Get the standard state abbreviation.

    :param state: String identifying state.
    :returns: 
    :rtype: 

    """
    if x in self.abbreviations:
      return x
    elif x in self.fips_codes:
      return self.fips_to_state[x]
    elif self._get_key(x) in self.states:
      return self.states[self._get_key(x)]
    else:
      raise ValueError(f'unrecognized state: {repr(state)}')

  def _make_reference(self):
    self.fips_codes = OrderedDict()  # mapping from fips code to canonical area name
    self.fips_order = []            # list of fips codes
    self.fips_indices = OrderedDict()  # mapping from fips code to index
    self.areas = {}                  # mapping from (STATE, canonical area name) tuple to fips code
    self.populations = {}
    self.fips_to_state = {}
    self.state_to_fips_codes = {}  # mapping from state XX to list of fips codes in that state

    with open(self.national_data_filenames['population'], 'r', newline='') as file:
      rows = iter(csv.reader(file, delimiter=','))
      for _ in range(self.national_data_skiprows['population'] + 1):
        next(rows)
      
      for i, row in enumerate(rows):
        if all(map(lambda x: x == '', row)):
          break
        fips = row[0]
        state = self._get_state(row[1])
        area = self._get_key(row[2])
        
        self.fips_codes[fips] = area
        self.fips_order.append(fips)
        self.fips_indices[fips] = i
        self.areas[(state, area)] = fips
        if area in self.states:
          self.areas[area] = fips
          self.areas[state] = fips
        self.fips_to_state[fips] = state
        if self._is_county(fips):
          self.state_to_fips_codes[state] = self.state_to_fips_codes.get(state, []) + [fips]
          self.state_to_fips_codes['US'] = self.state_to_fips_codes.get('US', []) + [fips]
        self.populations[fips] = int(row[18].replace(',', '')) # POP_ESTIMATE_2018
          
  def _write_reference(self):
    with open(join(self.data_dir, 'counties_order.csv'), 'w', newline='') as file:
      writer = csv.writer(file, delimiter=',')
      for fips, area in self.fips_codes.items():
        state = self.fips_to_state[fips]
        writer.writerow([fips, area, state])
        
  def _get_fips(self, x, key=None, default=None):
    """Get the 5 digit FIPS string from x, which could be a couple things.

    The possible values for x are:
    - the Fips itself, as a string
    - the GCT_STUB.target-geo-id, e.g. 0500000US01001, the last five digits of which are the FIPS
    - FIPS as an int
    - a (state, county name) pair

    :param x: the value
    :returns: 
    :rtype: 

    """

    if isinstance(x, list) and key is not None:
      # assume fips in first column unless otherwise noted
      return self._get_fips(x[self.fips_columns.get(key, 0)])  
    elif isinstance(x, dict) and key is not None:
      if x.get(key, None) is None:
        return default
      return self._get_fips(x[key][self.fips_columns[key]])
    elif x in self.fips_codes:
      return x
    elif type(x) is str and re.match(r'^\d+(?:\.\d+)$', x) is not None:
      return self._get_fips(str(int(float(x))).zfill(5))
    elif type(x) is str and re.match(r'^\d+$', x) is not None and len(x) < 5:
      return self._get_fips(x.zfill(5))
    elif x in self.areas:
      return self.areas[x]
    elif isinstance(x, int):
      return self._get_fips(str(x).zfill(5))
    elif x[7:9] == 'US':
      fips = x[9:]
      return self._get_fips(fips + ''.join(['0'] * (5 - len(fips))))
    else:
      return default
    
  def _is_county(self, x):
    """Tell whether the area x is a county equivalent.

    :param x: an area identifier, e.g. fips string
    :returns: 
    :rtype: 

    """
    fips = self._get_fips(x)
    assert len(fips) == 5
    return fips[2:] != '000'

  def _is_state(self, x):
    """

    :param x: an fips code
    :returns: 
    :rtype: 

    """
    fips = self._get_fips(x)
    return fips[-1] == '0' and fips[-2] == '0' and fips[-3] == '0'

  def unify_climate_data(self):
    # requires datafiles downloaded from ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/
    filenames = [join(self.raw_data_dir, 'national', 'Climate', 'climdiv-pcpncy-v1.0.0-20200304'),
                 join(self.raw_data_dir, 'national', 'Climate', 'climdiv-tmpccy-v1.0.0-20200304'),
                 join(self.raw_data_dir, 'national', 'Climate', 'climdiv-tmaxcy-v1.0.0-20200304'),
                 join(self.raw_data_dir, 'national', 'Climate', 'climdiv-tmincy-v1.0.0-20200304')]
    labels = ['Precipitation / inch', 'Temp AVG / F', 'Temp Min / F', 'Temp Max / F']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    out = OrderedDict()  # fips to row
    for filename, label in zip(filenames, labels):
      with open(filename, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=' ')
        for row in reader:
          fips = row[0][:5]
          if out.get(fips, None) is None:
            out[fips] = {}
          year = int(row[0][7:11])
          if year != 2019:
            continue
          out[fips][label] = [x for x in row[1:] if x != '']

    # collect data from each state
    state_averages = {}
    for fips in out:
      state = fips[:2]
      if state_averages.get(state) is None:
        state_averages[state] = dict((label, []) for label in labels)
      for label in labels:
        x = np.array([float(elem) for elem in out[fips][label]])
        state_averages[state][label].append(x)

    # reduce by mean
    for state in state_averages:
      for label in state_averages[state]:
        state_averages[state][label] = [f'{x:.02f}' for x in np.mean(np.array(state_averages[state][label]), 0)]

    # write to the file
    fname = join(self.raw_data_dir, 'national', 'Climate', 'unified_climate.csv')
    imputed = OrderedDict([(fips, False) for fips in self.fips_codes])
    with open(fname, 'w', newline='') as file:
      writer = csv.writer(file, delimiter=',')
      writer.writerow(['FIPS'] + [f'{month} {label}' for label in labels for month in months])
      counties_na = 0
      for fips in self.fips_codes:
        if out.get(fips) is None:
          if state_averages.get(fips[:2]) is None:
            continue
          # impute with state average
          counties_na += 1
          imputed[fips] = True
          writer.writerow([fips] + sum([state_averages[fips[:2]][label] for label in labels], []))
        else:
          writer.writerow([fips] + sum([out[fips][label] for label in labels], []))

    with open(join(self.data_dir, 'imputed_climate_data.json'), 'w') as file:
      json.dump(imputed, file)
    imputed = np.array([imputed[fips] for fips in imputed])
    print(f'imputed {np.sum(imputed)} / {imputed.shape[0]} ({np.mean(imputed)}) climate values')

  def parse_national_data(self):
    """Parse multiple csv files into one national data file."""

        # parse the incoming data by fips, creating a mapping from fips to a dict mapping datatype keys
    # to data for that row, ready to by joined.
    national_data = dict(
      (fips, dict(
        (k, ['NA'] * len(self.national_data_which_columns[k])) for k in self.keys))
      for fips in self.fips_codes)
    national_data['labels'] = dict(
      (k, ['NA'] * len(self.national_data_which_columns[k])) for k in self.keys)

    # parse the data into national_data
    for k in self.keys:
      with open(self.national_data_filenames[k], 'r', newline='') as file:
        delimiter = self.national_data_delimiters.get(k, ',')
        reader = csv.reader(file, delimiter=delimiter)
        for i, row in enumerate(reader):
          if i < self.national_data_skiprows[k]:            
            continue

          if i == self.national_data_skiprows[k]:
#            print(k)
#            print(*list(map(lambda t: f'      {t[0]},                      # {t[1]}', enumerate(row))), sep='\n')
            if k == 'health':
              national_data['labels'][k] = [row[j].strip().replace(',', '').replace('Percentage', 'Fraction')
                                                 for j in self.national_data_which_columns[k]]
            else:
              national_data['labels'][k] = [row[j].strip().replace(',', '')
                                                 for j in self.national_data_which_columns[k]]
            continue

          fips = self._get_fips(row, k)
          if fips is None:
            # county not in canonical list skip it
            continue

          values = [row[j].replace(',', '') for j in self.national_data_which_columns[k]]
          # the density data includes r values in the same columns, remove these
          if k == 'density':
            # get rid of r values
            for j in range(len(values)):
              values[j] = re.sub(r'\(r\d+\)', '', values[j])
          
          if k == 'unemployment':
            # fix the median household income dollar sign
            values[self.national_data_column_mapping[k][54]] = values[
              self.national_data_column_mapping[k][54]].replace('$', '')

          if k == 'health':
            for j in range(len(values)):
              if '%' in values[j]:
                values[j] = '{:.03f}'.format(float(values[j].replace('%', '')) / 100.)

          for j in range(len(values)):
            if values[j] == '':
              values[j] = 'NA'

          national_data[fips][k] = values

    return national_data
    
  def make_national_data(self):
    """Make the national data.

    :returns: 
    :rtype: 

    """

    self.national_data = self.parse_national_data()
    
    # write to csv
    with open(join(self.data_dir, 'counties_only.csv'), 'w', newline='') as counties_file, \
         open(join(self.data_dir, 'states_only.csv'), 'w', newline='') as states_file, \
         open(join(self.data_dir, 'counties.csv'), 'w', newline='') as file:
      counties_writer = csv.writer(counties_file, delimiter=',')
      states_writer = csv.writer(states_file, delimiter=',')
      writer = csv.writer(file, delimiter=',')
      labels = sum([self.national_data['labels'][k] for k in self.keys], [])
      na_counties = OrderedDict([(label, 0) for label in labels])

      counties_writer.writerow(labels)
      states_writer.writerow(labels)
      writer.writerow(labels)

      num_counties = 0
      num_states = 0
      for i, fips in enumerate(self.fips_codes):
        row = sum([self.national_data[fips][k] for k in self.keys], [])

        # write to both files
        writer.writerow(row)
        
        # write the row to counties or states (which includes the US)
        if self._is_county(fips):
          num_counties += 1
          counties_writer.writerow(row)
          
          # record availability data
          for j, label in enumerate(na_counties):
            if row[j] == 'NA':
              na_counties[label] += 1
              
        elif self._is_state(fips):
          num_states += 1
          states_writer.writerow(row)
        else:
          raise RuntimeError(f'neither state nor county: {row[:3]}')
          
      num_columns = len(row)
      print(f'wrote {num_columns} data columns for {num_counties} counties, {num_states} states')

    with open(join(self.data_dir, 'availability.csv'), 'w', newline='') as file:
      writer = csv.writer(file, delimiter=',')
      writer.writerow(['COLUMN_LABEL',
                       'COUNTIES_AVAILABLE', 'COUNTIES_NA', 'FRACTION_COUNTIES_AVAILABLE', 'FRACTION_COUNTIES_NA'])
      for label in labels:
        counties_available = num_counties - na_counties[label]
        writer.writerow([
          label,
          counties_available,
          na_counties[label],
          f'{counties_available / num_counties:.04f}',
          f'{na_counties[label] / num_counties:.04f}'])
      
      print(f'wrote availability data')
      
  def _read_cases_data(self, infections_filename, deaths_filename, recovered_filename):
    def load(filename):
      data = {}
      with open(filename, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        length = None
        for i, row in enumerate(reader):
          if i == 0:
            continue
          fips = self._get_fips(row[0])
          if fips is None:
            continue
          data[fips] = np.array(list(map(lambda x: 0 if x == '' else float(x), row[4:])))
          if length is None:
            length = data[fips].shape[0]

        # fix the state data, which is just a sum of the counties
        for state in self.abbreviations:
          # print(state, len(self.state_to_fips_codes[state]))
          x = np.zeros(length)
          for fips in self.state_to_fips_codes[state]:
            # print(state, self.fips_codes[fips], data.get(fips, np.zeros_like(x)))
            x += data.get(fips, np.zeros_like(x))
          data[self._get_fips(state)] = x
      return data
      
    # mapping from fips to numpy array giving timeseries for each.
    infections = load(infections_filename)
    deaths = load(deaths_filename)
    recovered = load(recovered_filename)

    return infections, deaths, recovered

  def copy_cases_data(self, src_filename, dst_filename):
    """Copy the case timeseries data.

    cases start at j = 11, 5-digit fips is row[0][-5:], e.g. Weston County, Wyoming has entry 84056045.

    The cases also includes full designation in row[10].

    Some rows are not for  counties, e.g. Diamond Princess. We do not copy these over.

    :param src_filename: 
    :param dst_filename: 
    :returns: 
    :rtype: 

    """
    with open(src_filename, 'r', newline='') as src_file, \
         open(dst_filename, 'w', newline='') as dst_file:
      reader = csv.reader(src_file, delimiter=',')
      writer = csv.writer(dst_file, delimiter=',')
      for i, row in enumerate(reader):
        if i == 0:
          writer.writerow(['FIPS'] + row[10:])
          
        if all(map(lambda x : x == '', row)):
          continue
        if len(row[0]) != 8 or row[0][:3] != '840':
          continue

        fips = row[0][-5:]
        if fips not in self.fips_codes:
          continue
        
        row = [fips] + [row[10].replace(',', ' -')] + row[11:]
        writer.writerow(row)
        
  
  def make_cases_data(self):
    """Solve for beta and gamma for each county.

    based on https://towardsdatascience.com/infection-modeling-part-1-87e74645568a

    rows are:

    FIPS, beta, gamma

    :returns: 
    :rtype: 

    """
    # mapping from fips to numpy array giving timeseries for each, starting from the first day with
    # nonzero infections
    infections_filename = join(self.raw_data_dir, 'national', 'JHU_Infections_time_series',
                               'time_series_covid19_confirmed_US.csv')
    deaths_filename = join(self.raw_data_dir, 'national', 'JHU_Infections_time_series',
                           'time_series_covid19_deaths_US.csv')
        
    self.copy_cases_data(infections_filename, join(self.data_dir, 'infections_timeseries.csv'))
    self.copy_cases_data(deaths_filename, join(self.data_dir, 'deaths_timeseries.csv'))

  def copy_traffic_file(self, src_filename, dst_filename):
    with open(src_filename, 'r', newline='') as src_file, \
         open(dst_filename, 'w', newline='') as dst_file:
      reader = csv.reader(src_file, delimiter=',')
      writer = csv.writer(dst_file, delimiter=',')
      
      for i, row in enumerate(reader):
        if all(map(lambda x : x == '', row)):
          continue

        if i == 0:
          # write teh labels
          d0 = datetime.date(2020, 3, 1).toordinal()  # Mar 1, 2020
          dates = [datetime.date.fromordinal(d0 + d) for d in range(len(row[1:]))]
          writer.writerow(['FIPS'] + [f'{d.month} / {d.day} / {d.year}' for d in dates])

        row[0] = row[0].zfill(5)
        writer.writerow(row)

  def make_foot_traffic_data(self):
    src_filenames = [
      join(self.raw_data_dir, 'national', 'SafeGraph', 'Grocery_cty_visits.csv'),
      join(self.raw_data_dir, 'national', 'SafeGraph', 'Healthcare_cty_visits.csv'),
      join(self.raw_data_dir, 'national', 'SafeGraph', 'Hospitals_cty_visits.csv'),
      join(self.raw_data_dir, 'national', 'SafeGraph', 'cty_visits.csv')]
    dst_filenames = [
      join(self.data_dir, 'foot_traffic', 'grocery_visits.csv'),
      join(self.data_dir, 'foot_traffic', 'healthcare_visits.csv'),
      join(self.data_dir, 'foot_traffic', 'hospital_visits.csv'),
      join(self.data_dir, 'foot_traffic', 'poi_visits.csv')]
    for src, dst in zip(src_filenames, dst_filenames):
      self.copy_traffic_file(src, dst)

  def filter_data(self):
    """Filter out counties that have few cases

    """
    # mapping from fips to numpy array giving timeseries for each, starting from the first day with
    # nonzero infections
    infections_filename = join(self.raw_data_dir, 'national', 'JHU_Infections', 'cases_time_series_JHU.csv')
    deaths_filename = join(self.raw_data_dir, 'national', 'JHU_Infections', 'deaths_time_series_JHU.csv')
    recovered_filename = join(self.raw_data_dir, 'national', 'JHU_Infections', 'recovered_time_series_JHU.csv')
    
    infections, deaths, recovered = self._read_cases_data(infections_filename, deaths_filename, recovered_filename)

    filename = join(self.data_dir, 'filtered_cases_and_deaths.csv')
    with open(filename, 'w', newline='') as file:
      writer = csv.writer(file, delimiter=',')
      # writer.writerow(['FIPS', 'STATE', 'AREA_NAME', 'infected', 'beta', 'gamma'])
      
      for fips in self.fips_codes:
        area = self.fips_codes.get(fips, 'NA')
        state = self.fips_to_state.get(fips, 'NA')
        if not (fips in infections and fips in deaths and fips in recovered) or np.all(infections[fips] == 0):
#          writer.writerow([fips, state, area, '0', 'NA'])
          continue

        if fips not in self.fips_codes:
#          writer.writerow([fips, state, area, infections[fips][-1], 'NA'])
          continue

        if infections[fips][-1] < int(self.threshold) or infections[fips][0] == 0:
          continue

        to_write = [fips, state, area]
        I = infections[fips]
        I = I/I[0]
        to_write.extend(I)
        to_write.extend(deaths[fips])
        writer.writerow(to_write)
#        print(f'wrote {fips}')

  def filter_data_states(self):
    """Filter out counties that have few cases

    """
    # mapping from fips to numpy array giving timeseries for each, starting from the first day with
    # nonzero infections
    infections_filename = join(self.raw_data_dir, 'national', 'JHU_Infections', 'cases_time_series_JHU.csv')
    deaths_filename = join(self.raw_data_dir, 'national', 'JHU_Infections', 'deaths_time_series_JHU.csv')
    recovered_filename = join(self.raw_data_dir, 'national', 'JHU_Infections', 'recovered_time_series_JHU.csv')
    
    infections, deaths, recovered = self._read_cases_data(infections_filename, deaths_filename, recovered_filename)

    filename = join(self.data_dir, 'filtered_cases_and_deaths_states.csv')
    with open(filename, 'w', newline='') as file:
      writer = csv.writer(file, delimiter=',')
#      writer.writerow(['FIPS', 'STATE', 'AREA_NAME', 'infected', 'beta', 'gamma'])
      
      for fips in self.fips_codes:
        area = self.fips_codes.get(fips, 'NA')
        state = self.fips_to_state.get(fips, 'NA')
        if not (fips in infections and fips in deaths and fips in recovered) or np.all(infections[fips] == 0):
         # writer.writerow([fips, state, area, '0', 'NA'])
          continue

        if fips not in self.fips_codes:
#          writer.writerow([fips, state, area, infections[fips][-1], 'NA'])
          continue

        to_write = [fips, state, area]
        I = infections[fips]
        to_write.extend(I)
        to_write.extend(deaths[fips])
        if self._is_state(fips):
          writer.writerow(to_write)
          
  def intervention_to_ordinal(self):
    # t0 = datetime.date(2020, 2, 29).toordinal()

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    months = dict(zip(months, range(1, len(months) + 1)))
    
    def date_to_ordinal(x):
      x = x.split('-')
      month = months[x[1]]
      day = int(x[0])
      return datetime.date(2020, month, day).toordinal()
      # if month == 'Mar':
      #   return day
      # elif month == 'Apr':
      #   return str(int(day) + 31)
      # else:
      #   print('Invalid month')
      #   exit()
    
    interventions_filename = join(self.raw_data_dir, 'national', 'public_implementations_fips.csv')
    data = {}
    with open(interventions_filename, 'r', newline='') as file:
      reader = csv.reader(file, delimiter=',')
      for i, row in enumerate(reader):
        if i == 0:
          continue
        fips = self._get_fips(row[0])
        if fips is None:
          continue
        data[fips] = np.array(list(map(lambda x: 'NA' if x.strip() == '' else date_to_ordinal(x), row[3:])))

    filename = join(self.data_dir, 'interventions.csv')
    with open(filename, 'w', newline='') as file:
      writer = csv.writer(file, delimiter=',')
      labels = ['FIPS', 'STATE', 'AREA_NAME', 'stay at home', '>50 gatherings', '>500 gatherings', 'public schools', 'restaurant dine-in', 'entertainment/gym', 'federal guidelines', 'foreign travel ban']
      writer.writerow(labels)
      
      for fips in self.fips_codes:
        area = self.fips_codes.get(fips, 'NA')
        state = self.fips_to_state.get(fips, 'NA')
        if not (fips in data):
          writer.writerow([fips, state, area] + ['NA'] * (len(labels) - 3))
          continue

        writer.writerow([fips, state, area] + [f'{x}' for x in data[fips]])
        print(f'wrote {fips}: {data[fips]}')

    return data

          
def main():
  parser = argparse.ArgumentParser(description='data formatter')

  # file settings
  parser.add_argument('--raw-data-dir', default='./raw_data', help='directory containing raw data')
  parser.add_argument('--data-dir', default='./data', help='directory to write formatted data to')
  parser.add_argument('--threshold', default='20', help='threshold for relevant counties')
    
  args = parser.parse_args()

  # run
  formatter = Formatter(args)
  # formatter.unify_climate_data() # only run if data files present, see function for which files
  formatter.make_national_data()
  # formatter.make_cases_data()
  # formatter.filter_data()
  # formatter.filter_data_states()
  # formatter.intervention_to_ordinal()
  # formatter.make_foot_traffic_data()

  
if __name__ == '__main__':
  main()
  
