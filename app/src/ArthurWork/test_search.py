from rapidfuzz import process
from ..airport import Airport

airports = [
    Airport("Suvarnabhumi Airport", "BKK", "Bangkok", "Thailand"),
    Airport("Shogun Airport", "SHO", "Shogunus", "Shogunium"),
    Airport("Arthur Airport", "ATA", "Chiba", "Japan"),
    Airport("Shonen Airport", "SHA", "Sapporo", "Japan")
]
airport_attr = {
    attr: {getattr(airport, attr): airport for airport in airports} 
    for attr in ('name', 'location_code', 'city', 'country')
}
#print(*airport_attr, sep='\n')
query = input("Enter your search : ")

matches = {
    attr: process.extract(query, value.keys()) for attr, value in airport_attr.items()
}

for paramiter, value in matches.items():
    print(paramiter, {item: airport_attr[paramiter][item] for item, score, _ in value if score > 60}, sep='\n', end='\n\n')
