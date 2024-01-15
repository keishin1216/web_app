import json
import csv

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as json_input:
        data = json.load(json_input)

    if isinstance(data, list):
        # If JSON contains a list of dictionaries
        with open(csv_file, 'w', newline='') as csv_output:
            csv_writer = csv.DictWriter(csv_output, fieldnames=data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data)
    elif isinstance(data, dict):
        # If JSON contains a single dictionary
        with open(csv_file, 'w', newline='') as csv_output:
            csv_writer = csv.DictWriter(csv_output, fieldnames=data.keys())
            csv_writer.writeheader()
            csv_writer.writerow(data)

# 以下のように関数を呼び出します
json_to_csv('大迫.json', '大迫.csv')