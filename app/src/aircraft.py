"""
https://docs.python.org/3/library/enum.html#enum.Flag
https://docs.python.org/3/howto/enum.html#flag
"""
from __future__ import annotations
from collections.abc import Iterator
from app.base import *


@dataclass(slots=True, frozen=True)
class Seat:
    __row: int # type: ignore
    __column: int # type: ignore
    __number: str # type: ignore
    __type: SeatType = SeatType(0) # type: ignore
    
    def __lt__(self, other: Self):
        return (self.row, self.column) < (other.row, other.column)
    
    @property
    def row(self):
        return self.__row
    
    @property
    def column(self):
        return self.__column
    
    @property
    def number(self):
        return self.__number

    @property
    def type(self):
        return self.__type


class Cabin:
    def __init__(self, travel_class: TravelClass, seats: Iterable[Seat]):
        self.__travel_class = travel_class
        self.__seats = frozenset(seats)

    def __iter__(self):
        yield from self.__seats
    
    @property
    def travel_class(self):
        return self.__travel_class

    @property
    def seats(self):
        return self.__seats


class Deck:
    def __init__(self, cabins: Sequence[Cabin]):
        self.__cabins = tuple(cabins)

    def __iter__(self):
        yield from self.__cabins
    
    def get_cabins_of(self, travel_class: TravelClass):
        """
            get all cabins in this deck that match with a travel class
        """
        for cabin in self:
            if cabin.travel_class is travel_class:
                yield cabin


class Aircraft:
    def __init__(self, model: str, decks: Sequence[Deck]):
        self.__model = model
        self.__decks = tuple(decks)
    
    @property
    def model(self):
        return self.__model
    
    @property
    def decks(self):
        return self.__decks
    
    @property
    def all_cabins(self):
        for deck in self.decks:
            yield from deck
    
    @property
    def all_seats(self):
        """
            get all passenger's seat in aircraft
        """
        return {
            seat for cabin in self.all_cabins for seat in cabin
        }
        
    def get_cabins_of(self, travel_class: TravelClass):
        """
            get all cabin that match travel_class in this aircraft
        """
        for deck in self.decks:
            yield from deck.get_cabins_of(travel_class)
        
    def get_seats_of(self, travel_class: TravelClass):
        """
            get all passenger's seat whch in specifiy travel_class in aircraft
        """
        return {
            seat for cabin in self.get_cabins_of(travel_class)
            for seat in cabin
        }
        
    def get_seat(self, number: str):
        """
            get seat by number (designator)
        """
        for seat in self.all_seats:
            if seat.number == number:
                return seat
            
        raise KeyError