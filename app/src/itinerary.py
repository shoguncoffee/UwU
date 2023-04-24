from __future__ import annotations
from .base import *

from .flight import FlightInstance
from .passenger import Pax


class FlightItinerary(tuple[FlightInstance, ...]):
    """
    ### collection of FlightInstance
        - represent a one flight or connecting flights
        - provide some useful methods to get information from group of flights
        - intended to be used for summarizing information to user
    """
    def __lt__(self, other: Self):
        return self.lowest_fare() < other.lowest_fare()
    
    @property
    def all_travel_class(self):
        classes = set(TravelClass)
        for instance in self:
            classes.intersection_update(
                instance.all_travel_class
            )
        return classes

    @property
    def departure(self):
        return self[0].departure
    
    @property
    def origin(self):
        return self[0].flight.origin
   
    @property
    def arrival(self):
        return self[-1].arrival
    
    @property
    def destination(self):
        return self[-1].flight.destination
   
    @property
    def duration(self):
        return self.flight_time() + self.transit_time()
    
    def transit_time(self: Sequence[FlightInstance]):
        return sum(
            [prev.transit_time(next) for prev, next in pairwise(self)], 
            dt.timedelta()
        )
    
    def flight_time(self: Sequence[FlightInstance]):
        return sum(
            [instance.duration for instance in self], 
            dt.timedelta()
        )
    
    def bookable(self, pax: Pax, travel_class: Optional[TravelClass] = None):
        """
        check if this itinerary is bookable by any (or specified) travel class for pax
        """ 
        if travel_class:
            return all(
                instance.get_class(travel_class).bookable(pax) 
                for instance in self
            )
        return all(
            any(
                instance.get_class(cls).bookable(pax) 
                for cls in instance.all_travel_class
            ) for instance in self
        )
        
    def lowest_fare(self):
        return self.get_price(
            Pax.minimum(), 
            min(self.all_travel_class)
        )
        
    def get_seats_left(self, travel_class: TravelClass):
        return min(
            instance.get_class(travel_class).get_seats_left()
            for instance in self
        )
        
    def get_price(self, pax: Pax, travel_class: TravelClass):
        return sum(
            instance.get_class(travel_class).fare.pax_price(pax)
            for instance in self
        )