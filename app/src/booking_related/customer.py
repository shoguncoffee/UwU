from __future__ import annotations
from ..base import *
if TYPE_CHECKING:
    from ..ArthurWork.flight_itinerary import Trip
    from .booking import Booking
    from .passenger_detail import PassengerDetails
    from .contact_information import ContactInformation
from ..K import Account

@dataclass(slots=True)
class Customer(Account):
    __bookings: set[Booking] = field(init=False, default_factory=set) # type: ignore
    
    @property
    def bookings(self):
        return self.__bookings


    def request_booking(self,
        journey: list[Trip],
        contact: ContactInformation,
        *passenger: PassengerDetails,
    ):
        from ..airline import Airline
        booking = Airline.create_booking(
            self, journey, contact, *passenger, 
        )

    def add_booking(self, booking: Booking):
        self.__bookings.add(booking)            
    
    def selected_booking(self, num):
        ...
            
    def view_booking(self):
        ...