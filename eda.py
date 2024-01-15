from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import csv
import os
avro_file_path = "観光行動設計-Site 1-775-1-1-00_2023-12-20_eda.avro"
output_dir = "<insert the path to a directory where to save csv files >"
## Read Avro file
reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())
schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
data= next(reader)
## Print the Avro schema
print(schema)
print(" ")
## Export sensors data to csv files
## Eda
eda = data["rawData"]["eda"]
timestamp = [round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
 for i in range(len(eda["values"]))]
with open(os.path.join(output_dir, 'eda.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["unix_timestamp", "eda"])
 writer.writerows([[ts, eda] for ts, eda in zip(timestamp, eda["values"])])
