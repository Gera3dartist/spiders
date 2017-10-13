import csv
import json


with open('output.json') as out:
    data  = json.load(out)

    with open("output.csv", "wt") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data[0].keys())
        for item in data:
             writer.writerow(item.values())
