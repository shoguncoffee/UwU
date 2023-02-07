"""
Deprecation
"""
from __future__ import annotations
from base import *

Type = Enum(
    'Food Type',
    'BEVERAGE MEAL'
)

@dataclass
class Food:
    name: str
    price: int
    