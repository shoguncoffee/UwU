from rapidfuzz import process

my_list = ['apple', 'banana', 'orange', 'kiwi', 'grape']

query = input("Enter your search : ")

matches = process.extract(query, my_list)

print([item for item, score, _ in matches if score > 70])
