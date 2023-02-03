import csv

d = [
    {'Aircraft': 'Airbus A380', 'Capacity': 300}, 
    {'Aircraft': 'Boeing A380', 'Capacity': 200}
]
field = [
    'Aircraft', 
    'Capacity', 
    'Modifly',
    'First',
    'Business',
    'Economy'
    'Description'
]

with open('DATA/qwe.csv', 'w') as f:
    writer = csv.DictWriter(f, field, delimiter=';')
    writer.writeheader()
    writer.writerows(d)
    