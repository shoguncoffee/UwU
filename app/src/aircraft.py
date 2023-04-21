from __future__ import annotations
from .base import *

from string import ascii_uppercase


@dataclass(slots=True, frozen=True)
class Seat:
    __row: int # type: ignore
    __column: int # type: ignore
    __number: str # type: ignore
    __type: SeatType # type: ignore
    __descriptions: list[str] = field(hash=False, default_factory=list) # type: ignore
    
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
    
    @property
    def descriptions(self):
        return self.__descriptions


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
        *layout: tuple[int, Sequence[int]],
    ):
        """
        generate a `Cabin`, for use in spawn.py
        """
        seats = []
        for lenght, column_config in layout:
            aisle_columns = {
                sum(column_config[:column]) - i
                for column in range(1, len(column_config)) 
                for i in range(2)
            }
            width = sum(column_config)
            for row, column in product(
                range(1, lenght + 1), range(1, width + 1)
            ):
                type = SeatType.COMMON
                info = []
                
                if column in aisle_columns:
                    type = SeatType.AISLE
                    info.append('Seat has direct access to the aisle')
                    
                elif column in (1, width):
                    type = SeatType.WINDOW
                    info.append('Seat has access to the window')
                
                if row == 1:
                    type = SeatType.LEGROOM
                    info.append('Seat has more legroom')
                
                absolute_row = initial_row + row
                seats.append(
                    Seat(
                        absolute_row, 
                        column, 
                        ascii_uppercase[column-1] + str(absolute_row), 
                        type, 
                        info
                    )
                )
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
        *cabin_layout: tuple[
            TravelClass, Sequence[tuple[int, Sequence[int]]]
        ]
    ):
        """
        generate a `Desk`, for use in spawn.py
        """
        cabins = []
        row = 1
        for travel_class, layout in cabin_layout:
            cabins.append(
                Cabin.generate(travel_class, row, *layout)
            )
            row += sum(lenght for lenght, _ in layout) 
            
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