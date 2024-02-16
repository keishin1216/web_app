import os
import pandas as pd
import json

def json_to_csv(json_file, csv_file):
    

    with open(json_file, 'r') as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    df.to_csv(csv_file, index=False)

def convert_folder_to_csv(folder_path):
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            json_file = os.path.join(folder_path, filename)
            csv_file = os.path.splitext(json_file)[0] + '.csv'
            json_to_csv(json_file, csv_file)
            print(f'Converted {json_file} to {csv_file}')


folder_path = '卒論'


convert_folder_to_csv(folder_path)