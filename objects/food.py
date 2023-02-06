"""
Deprecation
"""
from __future__ import annotations
from base import *

@dataclass
class Food:
    name: str
    price: int

@dataclass
class Berverage(Food):
    ...
    
@dataclass
class Meal(Food):
    ...
    