"""
filter some airports from airportRAW.csv
"""
import csv

new_field = 'Code', 'Name', 'Country', 'Latitude', 'Longitude'
with (
    open('Data/airportRAW.csv') as original,
    open('Data/airport.csv', 'w') as file
):
    data = csv.reader(original)
    old_field = next(data)
    writer = csv.writer(file, delimiter=';')
    writer.writerow(new_field)
    
    for line in data:
        seats = line.pop(2)
        if float(seats) > 9_000_000:
            writer.writerow(line)