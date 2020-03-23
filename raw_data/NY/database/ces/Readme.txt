The entire set of historical NAICS-based CES data (1990 to present) for the state, metropolitan areas and counties outside of metropolitan
areas is in the comma-separated-value (CSV) data files; ces_naics.txt, ces_minor.txt, ces_hours.txt, ces_earnings, ces_hourearn.
The data elements contained in that data file and their definitions are listed below.
The MSA geographies are those defined by BLS for 2005.

File: ces_naics.txt -- Monthly and annual employment for NYS and MSA's.
DATA ELEMENTS AND DEFINITIONS 

Data Element	Definition
SERIESCODE	    CES published line code
INDTITLE	    CES published line name
AREATYPE	    Area type (01=state, 21=MSA, 23=MD)
AREA		    Numeric metro area "FIPS" code assigned by the U.S. Office of Management & Budget
AREANAME	    Name of metro area
PERIODYEAR	    Year
JAN		    January employment
FEB		    February employment
MAR		    March employment
APR		    April employment
MAY		    May employment
JUN		    June employment
JUL		    July employment
AUG		    August employment
SEP		    September employment
OCT		    October employment
NOV		    November employment
DEC		    December employment
ANNUAL		    Summed monthly employment divided by 12 


File: ces_minor.txt -- Monthly and annual employment for counties outside metropolitan areas
DATA ELEMENTS AND DEFINITIONS 

Data Element	Definition
SERIESCODE	    CES published line code
INDTITLE	    CES published line name
AREATYPE	    Area type (04=county)
AREA		    Numeric area "FIPS" code assigned by the U.S. Office of Management & Budget
AREANAME	    Name of area
PERIODYEAR	    Year
JAN		    January employment
FEB		    February employment
MAR		    March employment
APR		    April employment
MAY		    May employment
JUN		    June employment
JUL		    July employment
AUG		    August employment
SEP		    September employment
OCT		    October employment
NOV		    November employment
DEC		    December employment
ANNUAL		    Summed monthly employment divided by 12 


File: ces_hours.txt -- Average weekly hours worked (where available --> New York State)
DATA ELEMENTS AND DEFINITIONS 

Data Element	Definition
SERIESCODE	    CES published line code
INDTITLE	    CES published line name
WORKER_TYPE	    Production workers or All workers
AREATYPE	    Area type (01=state)
AREA		    Numeric state "FIPS" code assigned by the U.S. Office of Management & Budget
AREANAME	    Name of state
YEAR	            Year
JAN		    January hours
FEB		    February hours
MAR		    March hours
APR		    April hours
MAY		    May hours
JUN		    June hours
JUL		    July hours
AUG		    August hours
SEP		    September hours
OCT		    October hours
NOV		    November hours
DEC		    December hours
ANNUAL		    Summed monthly hours divided by 12

Note:  All workers series are designated experimental because of the limited experience to date
with the editing and review of the estimates.  


File: ces_earnings.txt -- Average weekly earnings (where available --> New York State)
DATA ELEMENTS AND DEFINITIONS 

Data Element	Definition
SERIESCODE	    CES published line code
INDTITLE	    CES published line name
WORKER_TYPE	    Production workers or All workers
AREATYPE	    Area type (01=state)
AREA		    Numeric state "FIPS" code assigned by the U.S. Office of Management & Budget
AREANAME	    Name of state
YEAR	            Year
JAN		    January earnings
FEB		    February earnings
MAR		    March earnings
APR		    April earnings
MAY		    May earnings
JUN		    June earnings
JUL		    July earnings
AUG		    August earnings
SEP		    September earnings
OCT		    October earnings
NOV		    November earnings
DEC		    December earnings
ANNUAL		    Summed monthly earnings divided by 12

Note:  All workers series are designated experimental because of the limited experience to date
with the editing and review of the estimates.  


File: ces_hourearn.txt -- Average hourly earnings (where available --> New York State)
DATA ELEMENTS AND DEFINITIONS 

Data Element	Definition
SERIESCODE	    CES published line code
INDTITLE	    CES published line name
WORKER_TYPE	    Production workers or All workers
AREATYPE	    Area type (01=state)
AREA		    Numeric state "FIPS" code assigned by the U.S. Office of Management & Budget
AREANAME	    Name of state
YEAR	            Year
JAN		    January hourearn
FEB		    February hourearn
MAR		    March hourearn
APR		    April hourearn
MAY		    May hourearn
JUN		    June hourearn
JUL		    July hourearn
AUG		    August hourearn
SEP		    September hourearn
OCT		    October hourearn
NOV		    November hourearn
DEC		    December hourearn
ANNUAL		    Summed monthly hourearn divided by 12

Note:  All workers series are designated experimental because of the limited experience to date
with the editing and review of the estimates.  
