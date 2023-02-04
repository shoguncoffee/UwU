"""
Deprecation
"""
from __future__ import annotations
from base import *

@dataslots
class Food:
    price: int

@dataslots
class Berverage(Food):
    ...
    
@dataslots
class Meal(Food):
    ...
    