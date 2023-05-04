"""
filter some airports from airportRAW.csv
"""
import csv

new_field = 'Code', 'Name', 'Country', 'Latitude', 'Longitude'
with (
    open('data/airportRAW-sort.csv') as original,
    open('data/airport.csv', 'w', newline='') as file
):
    data = csv.reader(original)
    old_field = next(data)
    writer = csv.writer(file, delimiter=';')
    writer.writerow(new_field)
    
    for line in data:
        traffic = line.pop(2)
        if float(traffic) > 2_000_000:
            writer.writerow(line)