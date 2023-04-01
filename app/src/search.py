from __future__ import annotations
from .base import *

from rapidfuzz.process import extract
from rapidfuzz.fuzz import *

scorer = partial_ratio
limit = 30
score_cutoff = 50

def _search(
    key: str,
    query: str,
    pool: Iterable,
    scorer: Callable,
    limit: int,
    score_cutoff: int,
):
    choices: list[str] = [
        getattr(item, key) for item in pool
    ]
    yield from extract(
        query, choices, 
        scorer=scorer, 
        limit=limit, 
        score_cutoff=score_cutoff
    )


def simple(
    key: str,
    query: str,
    pool: Iterable[T],
    scorer: Callable = scorer,
    limit: int = limit,
    score_cutoff: int = score_cutoff,
):
    sequence: Sequence[T] = pool if isinstance(pool, Sequence) else list(pool)
    result = _search(
        key, query, sequence, 
        scorer, limit, score_cutoff
    )
    for value, score, index in result:
        yield sequence[index] 
    
    
def _filter(
    sequence: Sequence,
    result: list[tuple[str, Any, int]],
    limit: int,
    size: int
):
    temp = set()
    tick = iter(range(limit-1))
    for value, score, index in result:
        obj = sequence[index//size]
        if (ID := id(obj)) not in temp:
            try: 
                yield obj
                next(tick)
                temp.add(ID)
            except StopIteration:
                break
    
    
def multi(
    *keys: str,
    query: str,
    pool: Iterable[T],
    scorer: Callable = scorer,
    limit: int = limit,
    score_cutoff: int = score_cutoff,
):
    sequence: Sequence[T] = pool if isinstance(pool, Sequence) else list(pool)
    result = []
    for key in keys:
        result.extend(
            _search(
                key, query, sequence, 
                scorer, limit, score_cutoff
            )
        )
    result.sort(reverse=True, key=lambda x: x[1])
    print('normal', result)
    yield from _filter(sequence, result, limit, len(keys))
    
    
def multi_opt(
    *keys: str,
    query: str,
    pool: Iterable[T],
    scorer: Callable = scorer,
    limit: int = limit,
    score_cutoff: int = score_cutoff,
):  
    sequence: Sequence[T] = pool if isinstance(pool, Sequence) else list(pool)
    choices: list[str] = [
        getattr(obj, key) 
        for obj in sequence 
        for key in keys
    ]
    n = len(keys)
    result = extract(
        query, choices, 
        scorer=scorer, 
        limit=limit * n, 
        score_cutoff=score_cutoff
    )
    print('opt', result)
    yield from _filter(sequence, result, limit, n)
            
            
if __name__ == '__main__':
    import string, time
    alphabet = string.ascii_letters
    
    @dataclass(slots=True)
    class test:
        name: str
        hello: str
        home: str
        xxx: str
    
    s = [*test.__slots__]
    size = len(s)
    n = 10
    times = 20_000
    lenght = 15
    
    t = time.time()
    '''l = [
        test(
            *[
                ''.join(
                    random.choice(alphabet) for _ in range(lenght)
                )*2 for _ in range(size)
            ]
        ) for _ in range(times)
    ]'''
    l = [
        test(*x) for x in (
            ('halloween', 'zxc', 'iop', 'asd'),
            ('362', 'he', '135', '96'),
            ('741', '675', 'hello', '14'),
            ('haoo', 'ge', 'saA3hello0qwe', 'ol'),
            ('h', 'e', 'l', 'l'),
        )
    ]
    kw = {'query': 'hello', 'pool': l}
    
    t1 = time.time()
    print(t1-t)
    
    for _ in range(n):
        f1 = list(multi_opt(*s, **kw))
    t2 = time.time()
    print((t2-t1)/n)
    
    for _ in range(n):
        f2 = list(multi(*s, **kw))
    t3 = time.time()
    print((t3-t2)/n)