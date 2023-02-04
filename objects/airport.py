"""
airport
"""
from __future__ import annotations
from base import *
from geopy.distance import distance

@dataslots
class Airport:
    name: str
    airport_id: str
    city: str
    country: str
    coordinate: tuple[float, float]
    
    def distance(self, target: Airport):
        """
        distance in km
        """
        coors = (x.coordinate for x in (self, target))
        length = distance(*coors).km
        return round(length)