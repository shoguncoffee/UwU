from __future__ import annotations
from app.base import *

if TYPE_CHECKING:
    from . import *


@dataclass(slots=True, frozen=True)
class Fare:
    __passenger_fare: list[tuple[PassengerType, int]] # type: ignore
    __seat_fare: list[tuple[SeatType, int]] # type: ignore
    
    def get_passenger_price(self, passenger_type: PassengerType):
        for type, price in self.__passenger_fare:
            if type is passenger_type:
                return price
            
        raise KeyError
    
    def set_passenger_price(self, passenger_type: PassengerType, price: int):
        for i, (type, _) in enumerate(self.__passenger_fare):
            if type is passenger_type:
                self.__passenger_fare[i] = (type, price)
                break
        else:
            self.__passenger_fare.append(
                (passenger_type, price)
            )

    def get_seat_price(self, seat_type: Optional[SeatType]):
        if seat_type is None:
            return 0
        
        for type, price in self.__seat_fare:
            if type is seat_type:
                return price
            
        raise KeyError
    
    def set_seat_price(self, seat_type: SeatType, price: int):
        for i, (type, _) in enumerate(self.__seat_fare):
            if type is seat_type:
                self.__seat_fare[i] = (type, price)
                break
        else:
            self.__seat_fare.append(
                (seat_type, price)
            )
            
    def get_price(self, 
        passenger_type: PassengerType, 
        seat_type: Optional[SeatType] = None
    ):
        """
        if seat_type is None, assume that passenger is not assigned a seat (can be any seat)
        so a fee for choosing a seat is not included
        """
        return self.get_passenger_price(passenger_type) + self.get_seat_price(seat_type)
        
        
    def pax_price(self, pax: Pax):
        """
        not include seat's selection price
        """
        return sum(
            number * self.get_price(passenger_type)
            for passenger_type, number in pax
        )