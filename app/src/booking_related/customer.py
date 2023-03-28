from __future__ import annotations
from ..K.account import Account
from app.base import *
if TYPE_CHECKING:
    from src.booking_related.booking import Booking

@dataclass
class Customer(Account):
    _phone: str
    _bookings: list[Booking] = field(default_factory=list)

        
    def select_booking(self, num):
        if (int(num) > len(self._bookings) or int(num) <= 0):
            print("This booking doesn't exist.")
        else:
            return self._bookings[int(num) - 1]
            

    def view_booking(self):
        pass


    def add_booking(self, booking): #Temporary
        self._bookings.append(booking)


    def get_phone(self): #getter
        return self._phone