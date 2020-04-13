import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import datetime as dt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
# otherwise rotation of x-labels by 90 deg crashes from time to time
ticker.Locator.MAXTICKS = 10000


def plot_rt_europe(simulation_file, interventions_file, country_number, country_name, start_date, num_days=75, save_img=False):
    # read data
    simulation_data = pd.read_csv(simulation_file, delimiter=',', index_col=0)
    interventions, interventions_data = get_interventions_europe(interventions_file)
    interventions_data = interventions_data[interventions_data['Country'] == country_name]
    #time_data = list(pd.date_range(start=start_date, periods=num_days))
    time_data = list(pd.date_range(start=start_date, end='04/07/20'))
    num_days = len(time_data)
    # remove those interventions, that are not considered in the report
    interventions.remove('sport')
    interventions.remove('travel_restrictions')
    interventions.remove('any government intervention')

    start = 'Rt[1,' + str(country_number) + ']'
    end = 'Rt[' + str(num_days) + ',' + str(country_number) + ']'
    Rt_data = simulation_data.loc[start:end]

    plt.figure()
    # plot mean
    #plt.plot(time_data, Rt_data['mean'], drawstyle='steps-post', color='darkgreen')
    # horizontal line at R=1
    plt.hlines(1, time_data[0], time_data[-1])

    # 50% conf interval
    upper = Rt_data['75%'][:num_days]
    lower = Rt_data['25%'][:num_days]
    plt.fill_between(time_data, lower, upper, step='post', alpha=0.4, color='darkgreen', label='50% conf. interval')

    # 95% conf interval
    upper = Rt_data['97.5%'][:num_days]
    lower = Rt_data['2.5%'][:num_days]
    plt.fill_between(time_data, lower, upper, step='post', alpha=0.4, color='lightgreen', label='95% conf. interval')

    init_height = 1.2 * plt.gca().get_ylim()[1]
    plt.ylim([0, init_height])

    # markers used for different kinds of interventions
    marker = ['o', 'v', '^', '<', '>', 's', '*', 'D']
    # neede to make sure marker for several interventions on the same day don't overlap
    adjust_height = []

    # plot vertical lines and markers for each intervention
    # make sure markers for several interventions on the same day are drawn at different positions
    for ind, intervention in enumerate(interventions):
        date = interventions_data[intervention].values[0]
        num = adjust_height.count(date)
        adjust_height.append(date)
        if num == 0:
            # plot vertical line
            plt.axvline(pd.to_datetime(date), drawstyle='steps-pre', color='gray', ls='--')
        # plot marker for this intervention
        plt.plot(pd.to_datetime(date), init_height - (num + 1) * 0.05 * init_height, marker=marker[ind],
                 label=intervention, linestyle='None')

    # legend for interventions
    box = plt.gca().get_position()
    plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
    lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # adjust x axis labels and figure size
    date_form = DateFormatter("%B %d")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.30)
    plt.xlim([time_data[0], time_data[-1]])

    plt.title(country_name)
    plt.xlabel('Days')
    plt.ylabel('Time-dependent Reproduction Number')

    if save_img:
        plt.savefig(r'results\plots\europe_interventions\Rt_{}.png'.format(country_name), bbox_extra_artists=(lgd,), bbox_inches='tight')

    plt.show()


def plot_rt_US(simulation_file, interventions_file, county_number, fips, start_date, state_level, save_img=False):
    # read data
    simulation_data = pd.read_csv(simulation_file, delimiter=',', index_col=0)
    interventions, interventions_data = get_interventions_US(interventions_file, state_level=state_level)
    interventions_data = interventions_data[interventions_data['FIPS'] == fips]
    # time_data = list(pd.date_range(start=start_date, periods=num_days))
    time_data = list(pd.date_range(start=start_date, end='04/07/20'))
    num_days = len(time_data)
    # remove those interventions, that are not considered in the report
    interventions.remove('foreign travel ban')

    start = 'Rt[1,' + str(county_number) + ']'
    end = 'Rt[' + str(num_days) + ',' + str(county_number) + ']'
    Rt_data = simulation_data.loc[start:end]

    plt.figure()
    # plot mean
    #plt.plot(time_data, Rt_data['mean'], drawstyle='steps-post', color='darkgreen')
    # horizontal line at R=1
    plt.hlines(1, time_data[0], time_data[-1])

    # 50% conf interval
    upper = Rt_data['75%'][:num_days]
    lower = Rt_data['25%'][:num_days]
    plt.fill_between(time_data, lower, upper, step='post', alpha=0.4, color='darkgreen', label='50% conf. interval')

    # 95% conf interval
    upper = Rt_data['97.5%'][:num_days]
    lower = Rt_data['2.5%'][:num_days]
    plt.fill_between(time_data, lower, upper, step='post', alpha=0.4, color='lightgreen', label='95% conf. interval')

    init_height = 1.2 * plt.gca().get_ylim()[1]
    plt.ylim([0, init_height])

    # markers used for different kinds of interventions
    marker = ['o', 'v', '^', '<', '>', 's', '*', 'D']
    # neede to make sure marker for several interventions on the same day don't overlap
    adjust_height = []

    # plot vertical lines and markers for each intervention
    # make sure markers for several interventions on the same day are drawn at different positions
    for ind, intervention in enumerate(interventions):
        date = interventions_data[intervention].values[0]
        if not pd.isna(date):
            num = adjust_height.count(date)
            adjust_height.append(date)
            if num == 0:
                # plot vertical line
                plt.axvline(pd.to_datetime(date), drawstyle='steps-pre', color='gray', ls='--')
            # plot marker for this intervention
            plt.plot(pd.to_datetime(date), init_height - (num + 1) * 0.05 * init_height, marker=marker[ind],
                     label=intervention, linestyle='None')

    # legend for interventions
    box = plt.gca().get_position()
    plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
    lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # adjust x axis labels and figure size
    date_form = DateFormatter("%B %d")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.30)
    plt.xlim([time_data[0], time_data[-1]])

    plt.title(interventions_data['AREA_NAME'].values[0])
    plt.xlabel('Days')
    plt.ylabel('Time-dependent Reproduction Number')

    if save_img:
        if state_level:
            plt.savefig(r'results\plots\usa_interventions\Rt_state_{}.png'.format(fips), bbox_extra_artists=(lgd,), bbox_inches='tight')
        else:
            plt.savefig(r'results\plots\usa_interventions\Rt_county_{}.png'.format(fips), bbox_extra_artists=(lgd,),
                            bbox_inches='tight')

    plt.show()


# copied from data_parser
def get_interventions_europe(interventions_file):

    interventions = pd.read_csv(interventions_file, encoding='latin-1')

    mod_interventions = pd.DataFrame(columns=['Country', 'school/uni closures', 'self-isolating if ill',
                                              'banning public events', 'any government intervention',
                                              'complete/partial lockdown', 'social distancing/isolation'])

    mod_interventions['Country'] = interventions.iloc[0:11]['Country']
    mod_interventions['school/uni closures'] = interventions.iloc[0:11]['schools_universities']
    mod_interventions['self-isolating if ill'] = interventions.iloc[0:11]['self_isolating_if_ill']
    mod_interventions['banning public events'] = interventions.iloc[0:11]['public_events']
    mod_interventions['social distancing/isolation'] = interventions.iloc[0:11]['social_distancing_encouraged']
    mod_interventions['complete/partial lockdown'] = interventions.iloc[0:11]['lockdown']
    mod_interventions['any government intervention'] = interventions.iloc[0:11]['lockdown']
    mod_interventions['sport'] = interventions.iloc[0:11]['sport']
    mod_interventions['travel_restrictions'] = interventions.iloc[0:11]['travel_restrictions']

    mod_interventions.sort_values('Country', inplace=True)

    for col in mod_interventions.columns.tolist():
        if col == 'Country' or col == 'complete/partial lockdown':
            continue
        col1 = pd.to_datetime(mod_interventions[col], format='%Y-%m-%d').dt.date
        col2 = pd.to_datetime(mod_interventions['complete/partial lockdown'], format='%Y-%m-%d').dt.date
        col3 = pd.to_datetime(mod_interventions['any government intervention'], format='%Y-%m-%d').dt.date
        mod_interventions[col] = np.where(col1 > col2, col2, col1).astype(str)
        if col != 'self-isolating if ill':
            mod_interventions['any government intervention'] = np.where(col1 < col3, col1, col1).astype(str)

    countries = mod_interventions['Country'].to_list()
    date_cols = [col for col in mod_interventions.columns.tolist() if col != 'Country']

    return date_cols, mod_interventions


# copied from data_parser
def get_interventions_US(interventions_file, state_level=False):

    if state_level:
        interventions = pd.read_csv(interventions_file)

        interventions.fillna(1, inplace=True)
        interventions.drop([0], axis=0, inplace=True)
        beginning_ids_int = np.unique(np.array(interventions['FIPS'] / 1000).astype(np.int))
        id_cols = ['FIPS', 'STATE', 'AREA_NAME', 'Combined_Key']
        int_cols = [col for col in interventions.columns.tolist() if col not in id_cols]
        for col in int_cols:
            interventions[col] = interventions[col].apply(lambda x: dt.date.fromordinal(int(x)))

        state_interventions = pd.DataFrame(columns=int_cols, index=beginning_ids_int * 1000)
        for i in beginning_ids_int:
            county_int = interventions.loc[(interventions['FIPS'] / 1000).astype(int) == i, :]
            ## set the latest date for intervention at any county as the date of intervention for the state
            state_interventions.loc[i * 1000, :] = county_int[int_cols].max(axis=0)

        state_interventions.replace(dt.date.fromordinal(1), np.nan, inplace=True)
        state_interventions.insert(0, 'FIPS', state_interventions.index)
        state_interventions.insert(1, 'STATE', interventions['STATE'][interventions['FIPS'].isin(state_interventions.index)].values)
        state_interventions.insert(2, 'AREA_NAME', interventions['AREA_NAME'][interventions['FIPS'].isin(state_interventions.index)].values)
        interventions = state_interventions

    else:
        interventions = pd.read_csv(interventions_file)
        id_cols = ['FIPS', 'STATE', 'AREA_NAME', 'Combined_Key']
        #id_cols = ['FIPS', 'STATE', 'AREA_NAME']
        int_cols = [col for col in interventions.columns.tolist() if col not in id_cols]
        #interventions.fillna(1, inplace=True)
        for col in int_cols: ### convert date from given format
            interventions[col] = interventions[col].apply(lambda x: dt.date.fromordinal(int(x)) if not pd.isna(x) else x)

    interventions_list = list(interventions.columns.values)[3:]

    return interventions_list, interventions


def get_geo_startdate_data(geo_file, startdate_file):

    geos = pd.read_csv(geo_file)
    start_dates = pd.read_csv(startdate_file)

    fips_list = list(geos.values[0, 1:])
    start_dates = list(start_dates.values[0, 1:])

    return fips_list, start_dates


if __name__ == '__main__':

    ### EUROPE ###
    # simulation_file = r'results\europe_summary.csv'
    # interventions_file = r'data\europe_data\interventions.csv'
    # geo_file = r'results\europe_geocode.csv'
    # startdate_file = r'results\europe_start_dates.csv'
    #
    # country_list, start_dates = get_geo_startdate_data(geo_file, startdate_file)
    #
    # # model output indices start at 1
    # country_numbers = np.arange(1, len(country_list) + 1)
    #
    # for country_ind, country_name, date in zip(country_numbers, country_list, start_dates):
    #     plot_rt_europe(simulation_file, interventions_file, country_ind, country_name, date, save_img=True)

    ### USA counties ###
    simulation_file = r'results\US_county_summary.csv'
    interventions_file = r'data\us_data\interventions.csv'
    geo_file = r'results\us_county_geocode.csv'
    startdate_file = r'results\us_county_start_dates.csv'

    fips_list, start_dates = get_geo_startdate_data(geo_file, startdate_file)

    # model output indices start at 1
    county_numbers = np.arange(1, len(fips_list) + 1)

    for county, fips, date in zip(county_numbers, fips_list, start_dates):
        plot_rt_US(simulation_file, interventions_file, county, fips, date, False, save_img=True)

    ### USA states ###
    simulation_file = r'results\US_state_summary.csv'
    interventions_file = r'data\us_data\interventions.csv'
    geo_file = r'results\us_states_geocode.csv'
    startdate_file = r'results\us_states_start_dates.csv'

    fips_list, start_dates = get_geo_startdate_data(geo_file, startdate_file)

    # model output indices start at 1
    county_numbers = np.arange(1, len(fips_list) + 1)

    for county, fips, date in zip(county_numbers, fips_list, start_dates):
        plot_rt_US(simulation_file, interventions_file, county, fips, date, True, save_img=True)




