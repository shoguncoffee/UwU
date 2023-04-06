from __future__ import annotations
from ..base import *

if TYPE_CHECKING:
    from app.src import FlightInstance


@dataclass(init=False, slots=True)
class FlightItinerary:
    """
    collection of FlightInstance, represent connecting flights,
    provide some useful methods to get information from group of flights,
    intended to be used for summarizing information to user
    """
    __instances: tuple[FlightInstance, ...]
    
    def __init__(self, *flight: FlightInstance):
        self.__instances = flight
    
    @property
    def flights(self):
        return self.__instances
    
    def choice(self, cls: TravelClass):
        return Trip(self, cls)
    
    def bookable(self, pax: int):
        """
        check if this itinerary is bookable by any travel class for pax (number of passenger)
        """
        return all(
            any(
                flight.bookable(travel_class, pax) 
                for travel_class in flight.all_travel_class
            )
            for flight in self.flights
            
        )
        
    def minimal_fare(self):
        return sum(
            instance.base_fare for instance in self.flights
        )


@dataclass(slots=True, frozen=True)
class Trip:
    """
    trip segment, a FlightItinerary with a specific travel class
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
        check if this trip is bookable (specific travel class)
        """
        return all(
            flight.bookable(self.travel_class, pax) 
            for flight in self.flights
        )