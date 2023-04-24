from __future__ import annotations

# from .utils.checking import *
from app.utils.packages import *
from app.constants import *

if TYPE_CHECKING:
    T = TypeVar('T')
    U = TypeVar('U')
    
    from .src import FlightItinerary, Fare
    journey_param = Sequence[
        tuple[FlightItinerary, TravelClass]
    ]
    fares_param = Sequence[
        tuple[TravelClass, Fare]
    ]
    
    
def daterange(days: int, start: Optional[dt.date] = None):
    """
    if start is None, start = dt.date.today()
    
    *include start and end
    """
    start = start or dt.date.today()
    for i in range(days + 1):
        yield start + dt.timedelta(i)