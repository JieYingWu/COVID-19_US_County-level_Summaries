import pandas as pd
import numpy as np
import tabula
import requests
import os

def download_aamc_data(save_folder: str) -> None:
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    base_url = 'https://www.aamc.org/system/files/2019-12/state-physician-Alabama-2019%5B1%5D.pdf'

    us_states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","District_of_Columbia","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New_Hampshire","New_Jersey","New_Mexico","New_York",
  "North_Carolina","North_Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode_Island","South_Carolina","South_Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West_Virginia","Wisconsin","Wyoming"]

    for state in us_states:
        print('Processing {}'.format(state))
        if state != 'Indiana':
            curr_url = base_url.replace('Alabama', state)
        else:
            curr_url = 'https://www.aamc.org/system/files/2019-12/state-physician-Indiana-2019_0.pdf'
        response = requests.get(curr_url)
        save_path = os.path.join(save_folder, state + '.pdf')
        with open(save_path, 'wb') as f:
            f.write(response.content)
        f.close()

def clean_page_single_file(file_path: str) -> pd.DataFrame:
    state_abbr_dict = {'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT','District_of_Columbia': 'DC','Delaware': 'DE','Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV',
    'New_Hampshire': 'NH','New_Jersey': 'NJ','New_Mexico': 'NM', 'New_York': 'NY','North_Carolina': 'NC','North_Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Rhode_Island': 'RI','South_Carolina': 'SC','South_Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA','Washington': 'WA','West_Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}
    state_name = file_path.split('/')[-1].split('.')[0]
    state_code = state_abbr_dict[state_name]
    
    df = tabula.read_pdf(file_path, pages = 'all')
    p1 = df[0]
    p2 = df[1]

    p1.columns = list('abcde')
    p1 = p1.iloc[2:]
    p1['a'] = p1['b']
    p1 = p1[['a', 'c']]
    p1 = p1.iloc[:19]
    
    p1 = p1.transpose()
    new_header = p1.iloc[0]
    p1 = p1.iloc[1:]
    p1.columns = new_header
    p1.insert(0, 'State', [state_code])
    p1 = p1.reset_index()
    del p1['index']
    p1.columns.name = None
    p1 = p1.replace('---', 'NA')
    
    p2_columns = ['Speciality', 'Physicians', 'People per Physicians', 'Total female Physicians', 'Percent Female Physicians', 'Total Physicians > Age 60', 'Percent Physicians > Age 60']
    p2.columns = p2_columns
    p2 = p2.replace('*', 'NA')
    p2 = p2[['Speciality', 'Physicians']]
    p2 = p2.transpose()
    
    new_header = p2.iloc[0]
    p2 = p2.iloc[1:]
    p2.columns = new_header
    del p2['SpecialtyPhysiciansPeople Per PhysicianNumberPercentNumberPercent']
    p2.insert(0, 'State', [state_code])
    p2 = p2.reset_index()
    del p2['index']
    p2.columns.name = None
    
    p1 = p1.join(p2, rsuffix = '_p2')
    del p1['State_p2']
    
    return(p1)

def clean_all_documents(folder_path: str, save_path: str) -> pd.DataFrame:
    assert os.path.exists(folder_path)
    
    pdf_list = os.listdir(folder_path)
    pdf_list = list(filter(lambda x: '.DS_Store' not in x, pdf_list))
    pdf_list.sort()
    print('Processing file {}'.format(pdf_list[0]))
    master_df = clean_page_single_file(os.path.join(folder_path, pdf_list[0]))

    for pdf in pdf_list[1:]:
        print('Processing file {}'.format(pdf))
        curr_path = os.path.join(folder_path, pdf)
        curr_df = clean_page_single_file(curr_path)
        master_df = master_df.append(curr_df)
    
    print('Saving csv to disk.')
    master_df.to_csv(save_path)
    master_df = master_df.reset_index()
    del master_df['index']
    return(master_df)

def main():
    print('Downloading data.')
    save_folder = './healthcare_pdf'
    download_aamc_data(save_folder = save_folder)

    print('Processing pdfs.')
    folder_path = save_folder
    save_path = './national_physicians.csv'
    clean_all_documents(folder_path= folder_path, save_path=save_path)

if __name__ == '__main__':
    main()
