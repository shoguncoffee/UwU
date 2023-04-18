"""
fancy variables and functions
"""
from __future__ import annotations

# from .utils.checking import *
from .utils.packages import *
from .constants import *

if TYPE_CHECKING:
    T = TypeVar('T')
    U = TypeVar('U')
    
    
def daterange(days: int, start: Optional[dt.date] = None):
    """
    if start is None, start = dt.date.today()
    
    *include start and end
    """
    start = start or dt.date.today()
    for i in range(days + 1):
        yield start + dt.timedelta(i)
        

def difference_time(start: dt.time, end: dt.time):
    """
    calculate the difference between two time objects,
    if end time is earlier than start time, it will be considered as the next day
    """
    crossday = dt.timedelta(end < start)
    d2 = dt.datetime.combine(dt.date.min + crossday, end)
    d1 = dt.datetime.combine(dt.date.min, start)
    return d2 - d1