from __future__ import annotations
from app.base import *

if TYPE_CHECKING:
    from . import Booking


class Payment(ABC):
    def __init__(self, 
        total_price: int,
        transaction_id: Optional[UUID] = None,
    ):
        self._total_price = total_price
        self._transaction_id = transaction_id or uuid4()
        self._datetime = dt.datetime.now()
        self._status = PaymentStatus.PENDING
    
    def __bool__(self):
        return self._status is PaymentStatus.COMPLETED
    
    @property
    def total_price(self):
        return self._total_price
    
    @property
    def transaction_id(self):
        return self._transaction_id
    
    @property
    def datetime(self):
        return self._datetime
    
    @property
    def status(self):
        return self._status

    @classmethod
    def pay(cls, booking: Booking, **data):
        if cls.send_api(**data):
            return cls(booking.get_price())
    
    @classmethod
    @abstractmethod
    def send_api(self, **data): 
        """send api to payment provider"""


class CreditCardPayment(Payment):
    @classmethod
    def send_api(self, **data): ...


class InternetBankingPayment(Payment):
    @classmethod
    def send_api(self, **data): ...


class PaypalPayment(Payment):
    @classmethod
    def send_api(self, **data): ...
        

payment_map: dict[PaymentMethod, Type[Payment]] = {
    PaymentMethod.CREDIT_CARD: 
        CreditCardPayment,
    PaymentMethod.INTERNET_BANKING: 
        InternetBankingPayment,
    PaymentMethod.PAYPAL: 
        PaypalPayment,
}