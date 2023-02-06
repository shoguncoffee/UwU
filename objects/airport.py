"""
airport
"""
from __future__ import annotations
from base import *
from geopy.distance import distance

@dataclass
class Airport:
    name: str
    code: str
    city: str
    country: str
    coordinates: tuple[float, float]
    
    def __post_init__(self):
        self.code = self.code.upper()
    
    def distance(self, target: Airport):
        """
        distance between airports in km
        """
        coors = (x.coordinates for x in (self, target))
        length = distance(*coors).km
        return round(length)