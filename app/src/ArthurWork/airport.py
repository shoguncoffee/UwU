from __future__ import annotations
from ..base import *

@dataclass(slots=True, frozen=True)
class Airport:
    __name: str # type: ignore
    __location_code: str # type: ignore
    __city: str # type: ignore
    __country: str # type: ignore
    
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
