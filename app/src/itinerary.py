from __future__ import annotations
from .base import *

from .flight import FlightInstance
from .passenger import Pax


class FlightItinerary(tuple[FlightInstance]):
    """
    ### collection of FlightInstance
        - represent a one flight or connecting flights
        - provide some useful methods to get information from group of flights
        - intended to be used for summarizing information to user
    """
    @property
    def all_travel_class(self):
        classes = set(TravelClass)
        for instance in self:
            classes.intersection_update(
                instance.all_travel_class
            )
        return classes
   
    
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
            TravelClass.ECONOMY
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