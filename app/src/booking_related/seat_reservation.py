from __future__ import annotations
from app.base import *

from .passenger_detail import PassengerDetail
from ..ArthurWork.seat import Seat

@dataclass
class SeatReservation:
    __passenger_detail: PassengerDetail #type:ignore
    __seat: Seat | None #type:ignore

    def create_seat_reservation(self):
        pass

    def get_seat_pos(self):
        if self.__seat != None:
            return self.__seat
        else:
            return 'Not Selected'

    def get_owner_name(self):
        return self.__passenger_detail.get_passenger_fullname()