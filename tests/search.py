from app.utils.search import *
import string, time, dataclasses, random


alphabet = string.ascii_letters

@dataclasses.dataclass(slots=True, frozen=True)
class test:
    name: str
    home: str
    # age: str
    # love: str

s = [*test.__slots__]
size = len(s)
n = 1
times = 2000
lenght = 30

t = time.time()
l = [
    test(
        *[
            ''.join(
                random.choice(alphabet) for _ in range(lenght)
            ) for _ in range(size)
        ]
    ) for _ in range(times)
]
'''l = [
    test(*x) for x in (
        ('halloween', 'zxc',),
        ('hkllo', 'pppp',),
        ('h123o', '675',),
        ('Whelloq', 'sdawq',),
        ('hbsbfsd', 'hi',),
    )
]'''
kw = {'query': 'hello', 'pool': l}

t1 = time.time()
print(t1-t)

for _ in range(n): 
    f1 = list(multi_alignment(*s, **kw))
t2 = time.time()
print((t2-t1)/n)

print('------------------')

for _ in range(n):
    f2 = list(multi(*s, **kw))
t3 = time.time()
print((t3-t2)/n)