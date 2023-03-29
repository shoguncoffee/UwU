from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..flightsystem import FlightInstance

@dataclass(init=False, slots=True, unsafe_hash=True)
class FlightItinerary:
    """
    collection of flight
    """
    __flights: tuple[FlightInstance, ...] # type: ignore
    
    def __init__(self, *flight: FlightInstance):
        self.__flights = flight
    
    @property
    def flights(self):
        return self.__flights
    
    def choice(self, cls: TravelClass):
        return Trip(self, cls)


@dataclass(slots=True, frozen=True)
class Trip:
    """
    trip segment, just a 
    """
    __itinerary: FlightItinerary # type: ignore
    __travel_class: TravelClass # type: ignore
    
    @property
    def itinerary(self):
        return self.__itinerary
    
    @property
    def travel_class(self):
        return self.__travel_class