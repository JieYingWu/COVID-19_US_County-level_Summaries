import pandas as pd
import os
from tqdm import tqdm

def convert_ihms_to_timeseries(input_path: str = './Hospitalization_all_locs.csv', output_path: str = './ihms_timeseries.csv') -> None:
    df = pd.read_csv(input_path)

    us_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
                 "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
                 "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
                 "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
                 "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
                 "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
                 "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
                 "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    df = df.set_index('location_name')
    df = df.loc[us_states]
    df = df.reset_index()
    df['date'] = df.date.apply(
        lambda x: '{}/{}/{}'.format(x.split('-')[1], x.split('-')[2], x.split('-')[0][2:]))

    relevant_columns = ['allbed_mean', 'allbed_lower',
                        'allbed_upper', 'ICUbed_mean', 'ICUbed_lower', 'ICUbed_upper',
                        'InvVen_mean', 'InvVen_lower', 'InvVen_upper', 'deaths_mean',
                        'deaths_lower', 'deaths_upper', 'admis_mean', 'admis_lower',
                        'admis_upper', 'newICU_mean', 'newICU_lower', 'newICU_upper',
                        'totdea_mean', 'totdea_lower', 'totdea_upper', 'bedover_mean',
                        'bedover_lower', 'bedover_upper', 'icuover_mean', 'icuover_lower',
                        'icuover_upper']

    states_list = [st for st in us_states for _ in range(
        len(relevant_columns))]
    attributes_list = [at for _ in range(
        len(us_states)) for at in relevant_columns]

    out = pd.DataFrame({'State': states_list, 'Attribute': attributes_list})
    for date in df.date.values.tolist():
        out[date] = 0.0

    out = out.set_index(['State', 'Attribute'])

    for idx in tqdm(range(len(df))):
        row = df.iloc[idx]
        for col in relevant_columns:
            out.loc[row['location_name'], col][row['date']] = row[col].item()

    out.to_csv(output_path)

def main():
    input_path = '/Users/aniruddha/Downloads/2020_04_12.02/Hospitalization_all_locs.csv'
    output_path = '/Users/aniruddha/Downloads/2020_04_12.02/ihme_timeseries.csv'
    convert_ihms_to_timeseries(input_path=input_path, output_path=output_path)

if __name__ == '__main__':
    main()
