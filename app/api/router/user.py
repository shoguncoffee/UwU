from .base import *
from . import booking

router = APIRouter(
    prefix="/account",
    tags=["customer"],
)

    
@router.get("{username}/my-account")
async def get_account(username: str):
    account = Airline.accounts.get(username)
    return AccountBody.transform(account)


@router.get("{username}/my-bookings")
async def get_bookings(username: str):
    customer = Airline.accounts.get(username)
    assert isinstance(customer, src.Customer)
    return [
        BookingBody.transform(booking) 
        for booking in customer.bookings
    ]


@router.post("{username}/book")
async def book(username: str,
    journey: list[tuple[list[FlightInstanceBody], TravelClass]],
    contact: ContactInfoBody,
    passengers: list[PassengerBody],
):
    """
    - `creator`: 
        - customer id
        
    - `contact`: `ContactInfoBody`
        - contact information
    """
    customer = Airline.accounts.get(username)
    assert isinstance(customer, src.Customer)
    
    _passengers = PassengerBody.converts(passengers)
    _journey = [
        (
            FlightInstanceBody.converts(itinerary), travel_class
        ) for itinerary, travel_class in journey
    ]
    return Airline.create_booking(
        customer,
        contact.convert(_passengers),
        _passengers,
        _journey,
    )