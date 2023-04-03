from typing import Collection, Iterable, Sequence
print(
    *(
        [
            isinstance(obj, q) 
            for q in (Collection, Iterable, Sequence)
        ] 
        for obj in (
            dict(), 
            set(), 
            list(), 
            tuple(), 
            frozenset(), 
            str(), 
            range(10), 
            (q for q in (1,2)),
        )
    ), 
    sep='\n'
)