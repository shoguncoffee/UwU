"""
amazing search functions, Wow!
"""
from __future__ import annotations
from .base import *

from rapidfuzz.process import extract as _extract
from rapidfuzz.fuzz import *

_scorer = partial_ratio
_limit = 30
_score_cutoff = 50


def basic(
    key: str,
    pool: Collection[str],
    scorer: Callable = _scorer,
    limit: Optional[int] = _limit,
    score_cutoff: Optional[int] = _score_cutoff,
):
    for choice, score, index in _extract(
        key, pool, 
        scorer = scorer, 
        limit = limit, 
        score_cutoff = score_cutoff
    ):
        yield choice


def _search(
    key: str,
    query: str,
    pool: Sequence[T],
    scorer: Callable = _scorer,
    limit: Optional[int] = _limit,
    score_cutoff: Optional[int] = _score_cutoff,
):
    """
    supported object-attr search for rapidfuzz.process._extract()
    """
    choices: list[str] = [
       getattr(obj, key) for obj in pool
    ]
    results = _extract(
        query, choices, 
        scorer = scorer, 
        limit = limit, 
        score_cutoff = score_cutoff
    )
    for choice, score, index in results:
        yield score, pool[index]


def simple(
    key: str,
    query: str,
    pool: Iterable[T],
    scorer: Callable = _scorer,
    limit: Optional[int] = _limit,
    score_cutoff: Optional[int] = _score_cutoff,
):
    """
    one key search
    """
    sequence = pool if isinstance(pool, Sequence) else [*pool]
    results = _search(
        key, query, sequence, scorer, limit, score_cutoff
    )
    for score, obj in results:
        yield obj


def _filter(results: Iterable[T], limit: Optional[int]):
    """
    filter duplicate object for `limit` times 
    """
    temp = set()
    tick = iter(range(limit-1) if limit else repeat(None))
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
    scorer: Callable = _scorer,
    limit: Optional[int] = _limit,
    score_cutoff: Optional[int] = _score_cutoff,
):
    """
    chain from _search()
    """
    sequence = pool if isinstance(pool, Sequence) else [*pool]
    results = [] if not TYPE_CHECKING else [*_search('', '', sequence)] 
    for key in keys:
        results.extend(
            _search(key, query, sequence, scorer, limit, score_cutoff)
        )
    results.sort(
        key = lambda i: i[0], 
        reverse = True
    )
    yield from _filter(
        (obj for score, obj in results), limit
    )
    
    
def multi_opt(
    *keys: str,
    query: str,
    pool: Iterable[T],
    scorer: Callable = _scorer,
    limit: Optional[int] = _limit,
    score_cutoff: Optional[int] = _score_cutoff,
):  
    """
    more low-level optimizations
    """
    sequence: Sequence[T] = pool if isinstance(pool, Sequence) else [*pool]
    choices: list[str] = [
        getattr(obj, key) 
        for obj in sequence 
        for key in keys
    ]
    results = _extract(
        query, choices, 
        scorer = scorer, 
        limit = limit and limit * len(keys), 
        score_cutoff = score_cutoff
    )
    yield from _filter(
        (sequence[index//size] for value, score, index in results), limit
    )
    
    
def alignment(
    key: str,
    query: str,
    pool: Iterable[T],
    limit: Optional[int] = _limit,
    score_cutoff: Optional[int] = _score_cutoff,
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
    yield from results[:limit]
    

def multi_alignment(
    *keys: str,
    query: str,
    pool: Iterable[T],
    limit: Optional[int] = _limit,
    score_cutoff: Optional[int] = _score_cutoff,
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
                ratio for choice in attrs if (
                    ratio := partial_ratio_alignment(
                        choice, query, score_cutoff=score_cutoff,
                    )
                ) is not None
            ], obj
        ) for attrs, obj in choices 
    ]
    results.sort(
        key=lambda i: max(r.score for r in i[0]) if i[0] else 0, 
        reverse=True
    )
    yield from results[:limit]
    
    
if __name__ == '__main__':
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