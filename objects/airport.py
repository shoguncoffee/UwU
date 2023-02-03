from __future__ import annotations
from base import *

@dataclass
class Airport:
    name: str
    airport_id: str
    city: str
    country: str
    #location: tuple(float, float)