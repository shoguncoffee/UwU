from __future__ import annotations
from ..base import *

from ..information import Info


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


@dataclass(slots=True, frozen=True)
class CabinLayout:
    __travel_class: TravelClass # type: ignore
    __seats: frozenset[Seat] # type: ignore
    
    @property
    def travel_class(self):
        return self.__travel_class

    @property
    def seats(self):
        return self.__seats
    

@dataclass(slots=True, frozen=True)
class Seat:
    __row: int # type: ignore
    __column: int # type: ignore
    __type: SeatType # type: ignore
    __description: Info = field(hash=False, default_factory=Info) # type: ignore
    
    @property
    def row(self):
        return self.__row
    
    @property
    def column(self):
        return self.__column
    
    @property
    def type(self):
        return self.__type
    
    @property
    def description(self):
        return self.__description