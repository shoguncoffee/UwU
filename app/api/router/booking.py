from .base import *
from ..body_template import BookingBody

router = APIRouter(
    prefix='/account',
    tags=["booking"],
)


@router.get("{username}/{booking_id}/price")
async def view_booking(username: str, booking_id: UUID): # vs get_bookings?
    customer = Airline.accounts.get(username)
    assert isinstance(customer, src.Customer)
    
    booking = customer.get_booking(booking_id)
    return booking.get_price()


@router.post("{username}/{booking_id}/select-seat")
async def select_seat(username: str,
    booking_id: UUID,
    segment_index: int,
    reservation_index: int,
    selected: list[str],
):
    """
    - `reservation_index`: `int`
        - index of reservation (or flight) in booking

    - `segment_index: `int`
        - index of flights (connecting flights) in booking
        
    - `selected`: `list[str]`
        - list of seat number e.g. ['C12', 'K13']
        - sequence corresponds to index of passenger in booking
    """
    customer = Airline.accounts.get(username)
    assert isinstance(customer, src.Customer)
    
    booking = customer.get_booking(booking_id)
    assert len(booking.passengers) == len(selected)
    
    reservation = booking.reservations[segment_index][reservation_index]
    aircraft = reservation.provider.host.aircraft
    return Airline.select_seats(
        reservation, [
            (passenger, aircraft.get_seat(seat_number)) 
            for passenger, seat_number in zip(booking.passengers, selected)
        ]
    )


@router.post("/{username}/{booking_id}/payment")
async def pay(username: str,
    booking_id: UUID,
    method: PaymentMethod,
    data: dict
):
    customer = Airline.accounts.get(username)
    assert isinstance(customer, src.Customer)

    booking = customer.get_booking(booking_id)
    return Airline.pay(booking, method, data)