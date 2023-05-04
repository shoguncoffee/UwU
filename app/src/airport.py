from __future__ import annotations
from app.base import *

from geopy.distance import great_circle


@dataclass(slots=True, frozen=True)
class Airport:
    __name: str # type: ignore
    __code: str # type: ignore
    __country: str # type: ignore
    __coordinates: tuple[float, float] # type: ignore
    
    @property
    def name(self):
        return self.__name
    
    @property
    def code(self):
        return self.__code

    @property
    def country(self):
        return self.__country

    @property
    def coordinates(self):
        return self.__coordinates
    
    def distance(self, other: Self):
        return great_circle(self.coordinates, other.coordinates)