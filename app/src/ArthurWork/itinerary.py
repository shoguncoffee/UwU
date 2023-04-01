from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from app.src import *

@dataclass(init=False, slots=True, unsafe_hash=True)
class FlightItinerary:
    """
    collection of flight
    """
    __flights: tuple[FlightInstance, ...]
    
    def __init__(self, *flight: FlightInstance):
        self.__flights = flight
    
    @property
    def flights(self):
        return self.__flights
    
    def choice(self, cls: TravelClass):
        return Trip(self, cls)
    
    def bookable(self, pax: int):
        """
        check if this itinerary is bookable by any travel class
        """
        return all(
            flight.bookable(travel_class, pax) 
            for flight in self.flights
            for travel_class in flight.all_travel_class
        )


@dataclass(slots=True, frozen=True)
class Trip:
    """
    trip segment, just a ...
    """
    __itinerary: FlightItinerary # type: ignore
    __travel_class: TravelClass # type: ignore
    
    @property
    def flights(self):
        return self.__itinerary.flights
    
    @property
    def travel_class(self):
        return self.__travel_class
    
    def bookable(self, pax: int):
        """
        check if this trip is bookable
        """
        return all(
            flight.bookable(self.travel_class, pax) 
            for flight in self.flights
        )