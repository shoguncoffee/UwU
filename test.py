from geopy import Point
from dataclasses import dataclass

@dataclass
class airport(Point):
    name: str
    id: str
    city: str
    
print(airport('', '', '').name)
print(Point())
