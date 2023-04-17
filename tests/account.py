import pickle
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class A:
    a: int

d = A(0)
b = pickle.dumps(d)
q = pickle.loads(b)


class _repr:
    def __repr__(self) -> str:
        return super().__repr__().replace(', ', '\n')[1:-1]

class qwe(_repr, set):
    ...
      
w = qwe(zip(range(5), range(5)))