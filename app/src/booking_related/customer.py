from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..ArthurWork.flight_itinerary import Trip
    from .booking import Booking
    from .passenger_detail import PassengerDetails
    from .contact_information import ContactInformation
from ..K import Account

@dataclass
class Customer(Account):
    __phone: str # type: ignore
    __bookings: set[Booking] = field(default_factory=set) # type: ignore
    
    @property
    def bookings(self):
        return self.__bookings


    def request_booking(self,
        journey: list[Trip],
        passenger: list[PassengerDetails],
        contact: ContactInformation
    ):
        from ..airline import Airline
        booking = Airline.create_booking(
            self, 
            journey, 
            passenger, 
            contact
        )

    def add_booking(self, booking: Booking):
        self.__bookings.add(booking)            
    
    def selected_booking(self, num):
        while num > len(self.bookings):
            print("This booking doesn't exist currently.")
        else:
            ...
            return self.__bookings
            
    def view_booking(self):
        pass
