"""
enum constants
"""
from enum import Enum as _Enum

FlightStatus = _Enum(
    'FlightStatus', 'SCHEDULED CANCELLED IN_FLIGHT ARRIVED'
)
PassengerType = _Enum(
    'PassengerType', 'ADULT CHILD INFANT'
)
TravelClass = _Enum(
    'TravelClass', 'ECONOMY BUSINESS FIRST'
)
AccountStatus = _Enum(
    'AccountStatus', 'PENDING ACTIVE SUSPENDED, INACTIVE'
)
BookingStatus = _Enum(
    'BookingStatus', 'FAILED INCOMPLETE PENDING COMPLETED CANCELLED'
)
SeatType = _Enum(
    'SeatType', 'LEGROOM WINDOW AISLE COMMON'
)
GenderType = _Enum(
    'GenderType', 'MALE FEMALE'
)
PaymentStatus = _Enum(
    'PaymentStatus', 'PENDING FAILED COMPLETED'
)
PaymentMethod = _Enum(
    'PaymentMethod', 'PAYPAL INTERNETBANKING CREDITCARD'
)