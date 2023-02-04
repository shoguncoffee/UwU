from __future__ import annotations
from base import *
from geopy.distance import distance
from geopy import Point


class Airport():
    name: str
    airport_id: str
    city: str
    country: str
    coordinate: tuple[float, float]
    
    def distance(self, a: Airport):
        """
        distance in km
        """
        length = distance(
            self.coordinate, 
            a.coordinate
        )
        return round(length.km)