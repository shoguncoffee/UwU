from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..flightsystem import FlightInstance

@dataclass
class FlightItinerary:
    """
    collection of flight, 
    """
    __flights: list[FlightInstance] # type: ignore
    
    @property
    def flights(self):
        return self.__flights
    
    def choice(self, cls: TravelClass):
        return Trip(self.flights, cls)


@dataclass    
class Trip(FlightItinerary):
    """
    trip segment
    """
    __travel_class: TravelClass # type: ignore
    
    @property
    def travel_class(self):
        return self.__travel_class