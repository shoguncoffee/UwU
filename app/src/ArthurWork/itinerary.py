from __future__ import annotations
from ..base import *

from ..flightsystem import FlightInstance
from ..booking_related import Pax


class FlightItinerary(tuple[FlightInstance]):
    """
    ### collection of FlightInstance
        - represent a one flight or connecting flights
        - provide some useful methods to get information from group of flights
        - intended to be used for summarizing information to user
    """
    @property
    def all_travel_class(self) -> set[TravelClass]:
        return {
            travel_class for instance in self
            for travel_class in instance.all_travel_class 
        }
    
    def bookable(self, 
        pax: Pax, 
        travel_class: Optional[TravelClass] = None
    ):
        """
        check if this itinerary is bookable by any travel class for pax (number of passenger)
        """
        if travel_class:
            return all(
                flight.bookable(pax, travel_class) for flight in self
            )
        return all(any(
                flight.bookable(pax, cls) for cls in flight.all_travel_class
            ) for flight in self
        )
        
    def lowest_fare(self):
        return self.get_price(
            Pax([(PassengerType.ADULT, 1)]), 
            TravelClass.ECONOMY
        )
        
    def get_price(self, pax: Pax, travel_class: TravelClass):
        prices = []
        for instance in self:
            fare = instance.get_fare(travel_class)
            prices.append(
                fare.pax_price(pax)
            )
        return sum(prices)