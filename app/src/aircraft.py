"""
https://docs.python.org/3/library/enum.html#enum.Flag
https://docs.python.org/3/howto/enum.html#flag
"""
from __future__ import annotations
from app.base import *

from string import ascii_uppercase


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
    def number(self):
        return self.__number
    
    @property
    def column(self):
        return self.__column
    
    @property
    def type(self):
        return self.__type


@dataclass(slots=True, frozen=True)
class Cabin:
    __travel_class: TravelClass # type: ignore
    __seats: frozenset[Seat] = field(repr=False) # type: ignore
    
    @property
    def travel_class(self):
        return self.__travel_class

    @property
    def seats(self):
        return self.__seats
    
    @classmethod
    def generate(cls, 
        travel_class: TravelClass,
        initial_row: int,
        layouts: Sequence[Sequence[int]],
    ):
        """
        generate a `Cabin`, for using in spawn.py
        """
        seats = []
        relative_row = 0
        
        for lenght, *config in layouts:
            width = sum(config)
            gaps = len(config) - 1
            aisle_columns = {
                sum(config[:column+1]) - i
                for column, i in product(range(gaps), range(2)) 
            }
            for row, column in product(range(lenght), range(width)):
                conditions = {
                    SeatType.AISLE: column in aisle_columns,
                    SeatType.WINDOW: column in (0, width-1),
                    SeatType.LEGROOM: relative_row + row == 0,
                }
                type = reduce(
                    operator.or_, 
                    compress(conditions, conditions.values()), 
                    SeatType(0)
                )
                absolute_row = initial_row + relative_row + row
                seat_number = f'{ascii_uppercase[column]}{1 + absolute_row}'
                seats.append(
                    Seat(absolute_row, column, seat_number, type)
                )
            relative_row += lenght
            
        return cls(travel_class, frozenset(seats))


class Desk(tuple[Cabin, ...]):
    def get_cabins_of(self, travel_class: TravelClass):
        """
        get all cabins in this desk that match with a travel class
        """
        for cabin in self :
            if cabin.travel_class is travel_class:
                yield cabin
    
    @classmethod
    def generate(cls,
        cabin_layout: Iterable[tuple[
            TravelClass, Sequence[Sequence[int]]
        ]]
    ):
        """
        generate a `Desk`, for use in spawn.py
        """
        cabins = []
        row = 0
        for travel_class, layout in cabin_layout:
            cabins.append(
                Cabin.generate(travel_class, row, layout)
            )
            row += sum(lenght for lenght, *_ in layout) 
            
        return cls(cabins)
        

@dataclass(slots=True)
class Aircraft:
    __model: str # type: ignore
    __desks: tuple[Desk, ...] # type: ignore
    
    @property
    def model(self):
        return self.__model
    
    @property
    def desks(self):
        return self.__desks
    
    @property
    def all_cabins(self):
        for desk in self.desks:
            yield from desk
    
    @property
    def all_seats(self):
        """
        get all passenger's seat in aircraft
        """
        return {
            seat for cabin in self.all_cabins
            for seat in cabin.seats
        }
        
    def get_cabins_of(self, travel_class: TravelClass):
        """
        get all cabin that match travel_class in this desk
        """
        for cabin in self.all_cabins:
            if cabin.travel_class is travel_class:
                yield cabin
        
    def get_seats_of(self, travel_class: TravelClass):
        """
        get all passenger's seat whch in specifiy travel_class in aircraft
        """
        return {
            seat for cabin in self.get_cabins_of(travel_class)
            for seat in cabin.seats
        }
        
    def get_seat(self, number: str):
        """
        get seat by number (designator)
        """
        for seat in self.all_seats:
            if seat.number == number:
                return seat
            
        raise KeyError