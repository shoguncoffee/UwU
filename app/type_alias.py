from app.base import *
from app.src import *

__all__ = [
    'journey_param',
    'fares_param'
]


journey_param = Sequence[
    tuple[FlightItinerary, TravelClass]
]
fares_param = Sequence[
    tuple[TravelClass, Fare]
]