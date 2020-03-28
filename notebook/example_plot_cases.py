import numpy as np


## First, we load the data



## Generate some plots to study to trajectory of different counties


parser = argparse.ArgumentParser(description='data formatter')

# file settings
parser.add_argument('--raw-data-dir', default='./raw_data', help='directory containing raw data')
parser.add_argument('--data-dir', default='./data', help='directory to write formatted data to')
parser.add_argument('--threshold', default='20', help='threshold for relevant counties')

args = parser.parse_args()
  
# run
formatter = Formatter(args)

