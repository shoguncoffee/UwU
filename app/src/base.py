from __future__ import annotations
from ..base import *

from .constants import *


class Info(list[str]):
    def __str__(self):
        return '\n'.join(self)


'''
class HasReference(ABC):
    """
    base on uuid4
    """
    # reference: Optional[UUID] = reference or self.generate_reference() # type: ignore
    @abstractmethod
    def get_reference_pool(self) -> Collection:
        pass 
    
    def generate_reference(self) -> UUID: # type: ignore
        pool = self.get_reference_pool()
        while 1:
            if (ref := uuid4()) not in pool:
                return ref
'''