"""
no idea
"""
from __future__ import annotations
from base import *

Status = Enum()

@dataclass
class Payment:
    transaction_id: str
    