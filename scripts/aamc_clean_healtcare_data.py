import pandas as pd
import numpy as np
import tabula
import requests
import os

def download_aamc_data(save_folder: str):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    base_url = 'https://www.aamc.org/system/files/2019-12/state-physician-Alabama-2019%5B1%5D.pdf'

    us_states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
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

def main():
    save_folder = './healthcare_pdf'
    download_aamc_data(save_folder = save_folder)

if __name__ == '__main__':
    main()
