from .base import *

router = APIRouter(
    prefix='/account',
    tags=["booking"],
)


@router.get("/{username}/{booking_id}")
async def view_booking(username: str, booking_id: UUID):
    customer = system.accounts.get(username)    
    booking = customer.get_booking(booking_id)
    
    return BookingInfoBody.transform(booking)


@router.post("/{username}/{booking_id}/select-seat")
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
    customer = system.accounts.get(username)    
    booking = customer.get_booking(booking_id)
    
    assert len(booking.passengers) == len(selected)
    
    reservation = booking.reservations[segment_index][reservation_index]
    aircraft = reservation.provider.host.aircraft
    return system.select_seats(
        reservation, [
            (passenger, aircraft.get_seat(seat_number)) 
            for passenger, seat_number in zip(booking.passengers, selected)
        ]
    )


@router.post("/{username}/{booking_id}/payment")
async def pay(username: str,
    booking_id: UUID,
    data: dict
):
    customer = system.accounts.get(username)
    booking = customer.get_booking(booking_id)
    
    return system.pay(booking, data)


@router.put("/{username}/{booking_id}/pend")
async def pending(username: str, booking_id: UUID):
    customer = system.accounts.get(username)
    booking = customer.get_booking(booking_id)
    
    return system.pending_booking(booking)


@router.delete("/{username}/{booking_id}/temp")
async def temping(username: str, booking_id: UUID):
    customer = system.accounts.get(username)
    booking = customer.get_booking(booking_id)
    
    return system.cancel_booking(booking)