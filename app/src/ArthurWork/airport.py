from __future__ import annotations
from ..base import *
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Airport:
    __name: str = name # type: ignore
    __location_code: str = location_code # type: ignore
    __city: str = city # type: ignore
    __country: str = country # type: ignore
    
    @property
    def name(self):
        return self.__name
    
    @property
    def location_code(self):
        return self.__location_code
    
    @property
    def city(self):
        return self.__city
    
    @property
    def country(self):
        return self.__country
