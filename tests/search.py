from rapidfuzz.process import extract
from rapidfuzz.fuzz import *

l = (
    'halloween', 'zxc', 'iop', 'asd',
    'xxx', 'he', 'aaa', 'eee',
    'zzz', 'eee', 'hello', 'qqq',
    'haoo', 'ge', 'saAhelloqwe', 'www',
    'h', 'e', 'l', 'l'
)
w = 'hello'

'''for n, rati in [q for q in globals().items() if 'ratio' in q[0] and 'alignment' not in q[0]]:
    print(n)
    r = extract(
        w, [(x, 0) for x in l], 
        scorer=rati,
        processor=lambda x: x[0],
    )
    print(r, end='\n\n')'''
    
results = [
    partial_ratio_alignment(
        [x], [w], score_cutoff=50,
    ) for x in l
]
results.sort(
    key=lambda x: x.score if x is not None else 0, 
    reverse=True
)
print(*results, sep='\n')