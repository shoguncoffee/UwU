from __future__ import annotations
from app.base import *

from ..constants import TravelClass
from .seat_reservation import SeatReservation
from ..flightsystem.flight import FlightInstance

@dataclass
class FlightReservation:
    __class_of_service: TravelClass #type:ignore
    __flight_instance: FlightInstance #type:ignore
    __seat: list[SeatReservation] = field(default_factory=list)#type:ignore

    def get_flight_instance(self):
        return self.__flight_instance

    def get_total_fare(self):
        pass

    def create_flight_reservation(self):
        pass

    #Temp
    def get_travel_class(self):
        return self.__class_of_service
    
    #Temp
    def create_reserved_seat(self, passenger, position):
        reserved_seat = SeatReservation(passenger, position)
        self.__seat.append(reserved_seat)

    def get_all_reserved_seat(self):
        return self.__seat