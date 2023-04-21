from .airport import Airport
from .itinerary import FlightItinerary
from .fare import Fare
from .booking import Booking
from .schedule import (
    FlightPlan, 
    Deviation,
)
from .reservation import (
    SeatReservation, 
    FlightReservation,
)
from .account import (
    Account, 
    Customer, 
    Admin,
)
from .passenger import (
    PassengerDetails, 
    Pax, 
    ContactInformation,
)
from .flight import (
    Flight, 
    FlightInstance, 
    FlightClass,
)
from .aircraft import (
    Aircraft, 
    Desk, 
    Cabin, 
    Seat,
)
from .payment import (
    Payment, 
    CreditCardPayment, 
    InternetBankingPayment, 
    PaypalPayment,
    payment_map,
)

from .base import *

journey_param = Sequence[
    tuple[FlightItinerary, TravelClass]
]
fares_param = Sequence[
    tuple[TravelClass, Fare]
]