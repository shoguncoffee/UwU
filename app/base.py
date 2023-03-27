"""
fancy variables and functions
"""
from __future__ import annotations
#from utils.checking import *
from utils.packages import *
if TYPE_CHECKING:
    ...
else:
    dataclass = dataclass(slots=True)

field_set = field(default_factory=set)


class Singleton(ABC):
    def __new__(cls):
        instance = vars(cls).get('_instance')
        cls._instance = instance or super().__new__(cls)
        return cls._instance


class HasReference(ABC):
    """
    base on uuid4
    """
    @abstractmethod
    def get_reference_pool(self) -> Collection:
        pass 
    
    def generate_reference(self) -> UUID: # type: ignore
        pool = self.get_reference_pool()
        while 1:
            if (ref := uuid4()) not in pool:
                return ref


if __name__ == '__main__':
    print()