## Preprocessing

Since the timeseries data obtained from USA on the county level have certain inconsistencies, 
we tried several imputation techniques such as
- Interpolation:
    Our main goal is to keep the daily number of cases and deaths either constant or increasing. 
    There are two cases to consider:
    1. The daily cases7deaths are dropping but at some point in the timeseries there is a point where the number is higher than the last valid count. All the values inbetween them are linearly interpolated.
    Example:
    Original timeseries: `..., 1, 3, 6, 4, 5, 11, ...`
    Interpolated:        `..., 1, 3, 6, 8, 10, 11, ...` (When we encounter decimals, we round up)
    2. The count is dropping until the end of the timeseries. For extrapolation we take the difference between the last two valid counts and use this as the difference between the last valid count and the next invalid count. This countinues until the end of the timeseries.
    Example: 
    Original timeseries: `..., 35, 47, 63, 52, 50, 43`
    Interpolated:        `..., 35, 47, 63, 79, 95, 111` 

If using the original data, we include checks to ensure that daily counts do not drop to 0,
and discard the counties/states for which they do.

The US data is cumulative, so it is converted to daily counts before further preprocessing.
For the state-level analysis, we consider the latest date over associated counties for the interventions, 
and the sum across counties for calculation of infections and deaths.

Following the Imperial College analysis, the start-date for analysis is taken to be one month before
the cumulative sum of deaths exceeds 10. This keeps the windows open to account for the infective phase 
that is known to start at least 14 days earlier.

## To run
To run the data_parser in itself, uncomment lines 581-589 and call `python scripts/data_parser.py` 
from the base directory. To change the time period considered for analysis, change the value of `N2`. Currently,
it is taken to be 75 (for Europe data) and 100 (for US data). You can change the number of counties/states considered
by changing the parameters `num_counties` and `num_states`.

**Note:**
- The FIPS code is known to be the only reliable and consistent identifier, so we do our analysis based on that.
- Since the number of infections/deaths across certain counties/states are low, and the model is known to work mostly
for larger numbers, we consider only places with numbers high enough for our analysis.


