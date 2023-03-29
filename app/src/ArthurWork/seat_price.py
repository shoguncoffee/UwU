from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..constants import PassengerType

@dataclass
class SeatPrice:
    __price: float # type: ignore
    __passenger_type: PassengerType # type: ignore
    
    @property
    def price(self):
        return self.__price

    @property
    def passenger_type(self):
        return self.__passenger_type