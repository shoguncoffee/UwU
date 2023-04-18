from __future__ import annotations
from .base import *

from string import ascii_uppercase


@dataclass(slots=True, frozen=True)
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
        return {
            cabin for desk in self.desks
            for cabin in desk.cabins
        }
        
    @property
    def all_seats(self):
        """
        get all passenger's seat in aircraft
        """
        return {
            seat for desk in self.desks
            for seat in desk.get_seats()
        }
        
    def get_seats_of(self, travel_class: TravelClass):
        """
        get all passenger's seat that match travel_class in aircraft
        """
        return {
            seat for desk in self.desks
            for seat in desk.get_seats_of(travel_class)
        }
        
    def get_seat(self, number: str):
        """
        get seat by row and column
        """
        for seat in self.all_seats:
            if seat.number == number:
                return seat
        raise KeyError
        

@dataclass(slots=True, frozen=True)
class Desk:
    __cabins: tuple[CabinLayout, ...] # type: ignore
    
    @property
    def cabins(self):
        return self.__cabins

    def get_seats(self):
        """
        get all passenger's seat in this desk
        """
        return {
            seat for cabin in self.cabins
            for seat in cabin.seats
        }
    
    def get_cabins_of(self, travel_class: TravelClass):
        """
        get all cabin that match travel_class in this desk
        """
        return {
            cabin for cabin in self.cabins 
            if cabin.travel_class == travel_class
        }
    
    def get_seats_of(self, travel_class: TravelClass):
        """
        get all passenger's seat that match travel_class in this desk
        """
        return {
            seat for cabin in self.get_cabins_of(travel_class)
            for seat in cabin.seats
        }
        
    @classmethod
    def generate(cls,
        *layouts: tuple[
            TravelClass, 
            Sequence[
                tuple[int, Sequence[int]]
            ]              
        ]
    ):
        return cls(tuple(
            CabinLayout.generate(
                travel_class, *layout, 
                initial_row=sum(
                    sum(q[0] for q in k[1]) for k in layouts[:i]
                )
            ) for i, (travel_class, layout) in enumerate(layouts)
        ))
        

@dataclass(slots=True, frozen=True)
class CabinLayout:
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
        *layout: tuple[int, Sequence[int]],
        initial_row: int = 1,
    ):
        """
        generate a CabinLayout
        """
        l = []
        for lenght, config in layout:
            width = sum(config)
            aisle = {
                sum(config[:i]) - k
                for i in range(1, len(config)) 
                for k in range(2)
            }
            for row, column in product(
                range(1, lenght+1), range(1, width+1)
            ):
                type = SeatType.COMMON
                info = []
                
                if row == 1:
                    type = SeatType.LEGROOM
                    info.append('Seat has more legroom')
                
                if column in aisle:
                    info.append('Seat has direct access to the aisle')
                    
                if column in (1, width):
                    info.append('Seat has access to the window')
                
                letter = ascii_uppercase[column-1]                
                l.append(Seat(
                    initial_row + row, 
                    column, 
                    letter, 
                    type, 
                    info
                    )
                )
        return cls(travel_class, frozenset(l))


@dataclass(slots=True, frozen=True)
class Seat:
    __row: int # type: ignore
    __column: int # type: ignore
    __letter: str # type: ignore number?
    __type: SeatType # type: ignore
    __description: list[str] = field(hash=False, default_factory=list) # type: ignore
    
    @property
    def row(self):
        return self.__row
    
    @property
    def letter(self):
        return self.__letter
    
    @property
    def column(self):
        return self.__column
    
    @property
    def type(self):
        return self.__type
    
    @property
    def description(self):
        return self.__description
    
    @property
    def number(self):
        return str(self.row) + self.letter