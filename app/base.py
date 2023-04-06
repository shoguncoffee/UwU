"""
fancy variables and functions
"""
from __future__ import annotations
# from .utils.checking import *
from .utils.packages import *
if TYPE_CHECKING:
    T = TypeVar('T')
    U = TypeVar('U')
    
def daterange(days: int, start: Optional[date] = None):
    """
    if start is None, start = date.today()
    
    *include start and end
    """
    start = start or date.today()
    for i in range(days + 1):
        yield start + timedelta(i)
        

def difference_time(start: time, end: time):
    """
    calculate the difference between two time objects,
    if end time is earlier than start time, it will be considered as the next day
    """
    crossday = timedelta(end < start)
    d2 = datetime.combine(date.min + crossday, end)
    d1 = datetime.combine(date.min, start)
    return d2 - d1