from __future__ import annotations
from base import *

@dataclass
class Food:
    price: int
    
class Berverage(Food):
    ...
    
class Meal(Food):
    ...