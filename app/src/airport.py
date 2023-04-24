from __future__ import annotations
from .base import *

from geopy.distance import great_circle


@dataclass(slots=True, frozen=True)
class Airport:
    __name: str # type: ignore
    __location_code: str # type: ignore
    __country: str # type: ignore
    __coordinates: tuple[float, float] # type: ignore
    
    @property
    def name(self):
        return self.__name
    
    @property
    def location_code(self):
        return self.__location_code

    @property
    def country(self):
        return self.__country

    @property
    def coordinates(self):
        return self.__coordinates
    
    def distance(self, other: Self):
        return great_circle(self.coordinates, other.coordinates)