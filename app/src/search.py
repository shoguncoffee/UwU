"""
amazing search functions, Wow!
"""
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
    pool: Iterable[T],
    scorer: Callable = partial_ratio,
    limit: int = limit,
    score_cutoff: int = score_cutoff,
):
    """
    supported object-attr search for rapidfuzz.process.extract()
    """
    choices: list[tuple[str, T]] = [
       (getattr(obj, key), obj) for obj in pool
    ]
    results = extract(
        query, choices, 
        scorer=scorer, 
        limit=limit, 
        processor=lambda x: x[0],
        score_cutoff=score_cutoff
    )
    for (choice, obj), score, index in results:
        yield score, obj


def simple(
    key: str,
    query: str,
    pool: Iterable[T],
    scorer: Callable = scorer,
    limit: int = limit,
    score_cutoff: int = score_cutoff,
):
    """
    one key search
    """
    results = _search(
        key, query, pool, scorer, limit, score_cutoff
    )
    for score, obj in results:
        yield obj


def _filter(results: Iterable[T], limit: int):
    """
    filter duplicate object for `limit` times 
    """
    temp = set()
    tick = iter(range(limit-1))
    for obj in results: 
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
    """
    chain from _search()
    """
    results = []
    if TYPE_CHECKING:
        results = [*_search('', '', pool)]
        
    for key in keys:
        results.extend(
            _search(key, query, pool, scorer, limit, score_cutoff)
        )
    results.sort(reverse=True)    
    yield from _filter(
        (obj for score, obj in results), limit
    )
    
    
def multi_opt(
    *keys: str,
    query: str,
    pool: Iterable[T],
    scorer: Callable = scorer,
    limit: int = limit,
    score_cutoff: int = score_cutoff,
):  
    """
    more low level optimization, a bit faster
    """
    sequence: Sequence[T] = pool if isinstance(pool, Sequence) else list(pool)
    choices: list[str] = [
        getattr(obj, key) 
        for obj in sequence 
        for key in keys
    ]
    n = len(keys)
    results = extract(
        query, choices, 
        scorer=scorer, 
        limit=limit * n, 
        score_cutoff=score_cutoff
    )
    yield from _filter(
        (sequence[index//size] for value, score, index in results), limit
    )
    
    
def alignment(
    key: str,
    query: str,
    pool: Iterable[T],
    limit: int = limit,
    score_cutoff: int = score_cutoff,
):
    """
    alignment search with more information
    """
    choices: list[tuple[str, T]] = [
        (
            getattr(obj, key), obj
        ) for obj in pool
    ]
    results = [
        (ratio, obj) for choice, obj in choices
        if (
            ratio := partial_ratio_alignment(
                choice, query, score_cutoff=score_cutoff,
            )
        ) is not None
    ]
    results.sort(
        key=lambda i: i[0].score, 
        reverse=True
    )
    yield from results
    

def multi_alignment(
    *keys: str,
    query: str,
    pool: Iterable[T],
    limit: int,
    score_cutoff: int,
):
    """
    multi alignment search
    """
    choices: list[tuple[list[str], T]] = [
        (
            [getattr(obj, key) for key in keys], obj
        ) for obj in pool
    ]
    results = [
        (
            [
                ratio for choice in attrs
                if (
                    ratio := partial_ratio_alignment(
                        choice, query, score_cutoff=score_cutoff,
                    )
                ) is not None
            ], 
            obj
        ) for attrs, obj in choices 
    ]
    results.sort(
        key=lambda i: max(r.score for r in i[0]), 
        reverse=True
    )
    yield from results
    
    
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