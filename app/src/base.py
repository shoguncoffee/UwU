from __future__ import annotations
from app.base import *

if TYPE_CHECKING:
    from . import *
    
    journey_param = Sequence[
        tuple[FlightItinerary, TravelClass]
    ]
    fares_param = Sequence[
        tuple[TravelClass, Fare]
    ]
    
    
'''
class Reference(UUID):
    storage 
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)
'''