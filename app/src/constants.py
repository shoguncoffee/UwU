"""
enum constants
"""
from enum import Enum as _Enum

FlightStatus = _Enum(
    'FlightStatus', 'SCHEDULED CANCELLED DELAYED IN_FLIGHT ARRIVED'
)
PassengerType = _Enum(
    'PassengerType', 'ADULT CHILD INFANT'
)
TravelClass = _Enum(
    'TravelClass', 'Economy Bussiness First'
)
AccountStatus = _Enum(
    'AccountStatus', 'PENDING ACTIVE SUSPENDED'
)
BookingStatus = _Enum(
    'BookingStatus', 'FAILED INCOMPLETE PENDING COMPLETED CANCELLED'
)
SeatType = _Enum(
    'SeatType', 'STANDARD'
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