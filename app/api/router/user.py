from .base import *

router = APIRouter(
    prefix="/account",
    tags=["customer"],
)

 
@router.get("/{username}/my-account")
async def get_account(username: str):
    if username in system.accounts:
        account = system.accounts.get(username)
        return AccountBody.transform(account)
    else:
        raise HTTPException(status_code=404, detail="Account not found")


@router.get("/{username}/my-bookings")
async def get_bookings(username: str):
    if username in system.accounts:
        customer = system.accounts.get(username)
        
        return [
            BookingBody.transform(booking) for booking in customer.bookings
        ]
    else:
        raise HTTPException(status_code=404, detail="Account not found")


@router.post("/{username}/book")
async def book(username: str,
    data: PreBookingBody,
):
    """
    - `creator`: 
        - customer id
        
    - `contact`: `ContactInfoBody`
        - contact information
    """
    customer = system.accounts.get(username)    
    journey, contact, passengers = data.convert()
    
    return system.create_booking(customer,
        contact,
        passengers,
        journey,
    )