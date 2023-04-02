from __future__ import annotations
from ..base import *

from .constants import *


class HasReference(ABC):
    """
    base on uuid4
    """
    # reference: Optional[UUID]
    @abstractmethod
    def get_reference_pool(self) -> Collection:
        pass 
    
    def generate_reference(self) -> UUID: # type: ignore
        pool = self.get_reference_pool()
        while 1:
            if (ref := uuid4()) not in pool:
                return ref

def daterange(days: int, start: Optional[date] = None):
    """
    if start is None, start = date.today()
    
    *include start and end
    """
    start = start or date.today()
    for i in range(days + 1):
        yield start + timedelta(i)