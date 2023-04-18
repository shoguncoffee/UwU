import timeit
from random import randint

q = [
    [randint(0, 100) for _ in range(10)] for _ in range(30_000)
]

def extend_method():
    lst = []
    for i in q:
        lst.extend(i)
    return lst

def list_comprehension():
    return [n for i in q for n in i]

print(timeit.timeit("extend_method()", globals=globals(), number=100))
print(timeit.timeit("list_comprehension()", globals=globals(), number=100))