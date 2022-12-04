# Handling time and unix timestamp
import os

import json

import pandas as pd

def json_to_csv():
    path_ws = os.path.dirname(os.path.abspath(__file__))

    all_data = []

    directory = os.path.join(path_ws, '..', 'data', 'ext')

    files = sorted(os.listdir(directory))

    for filename in files:
        full_path = os.path.join(directory, filename)

        if os.path.isfile(full_path):
            f = open(full_path)
            hist = json.load(f)
            all_data += hist

    df = pd.DataFrame(all_data)
    df.to_csv( os.path.join(directory, 'full_history.csv') , index = None)

    print(all_data[0])
    print(len(all_data))

    
def load():
    # If something went wrong, write into new logfile
    try:
        json_to_csv()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    load()