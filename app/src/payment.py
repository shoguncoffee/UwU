from __future__ import annotations
from .base import *

if TYPE_CHECKING:
    from . import *


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
    @abstractmethod
    def pay(cls, booking: Booking):
        return cls(
            booking.get_price()
        )


class CreditCardPayment(Payment):
    #def __init__(self, securtity_code):
    #    self.security_code = securtity_code

    def pay(self, total_fare):
        print("Credit Class Payment : SUCCESS")
        print("TRANSACTION ID :", self._transaction_id)
        print("TOTAL FARE :", total_fare,"THB")
        self._status = PaymentStatus.COMPLETED


class InternetBankingPayment(Payment):
    def pay(self, total_fare):
        print("Internet Banking Payment : SUCCESS")
        print("TRANSACTION ID :", self._transaction_id)
        print("TOTAL FARE :", total_fare,"THB")
        self._status = PaymentStatus.COMPLETED


class PaypalPayment(Payment):
    def pay(self, total_fare):
        print("Paypal Payment : SUCCESS")
        print("TRANSACTION ID :", self._transaction_id)
        print("TOTAL FARE :", total_fare,"THB")
        self._status = PaymentStatus.COMPLETED
        

payment_map: dict[PaymentMethod, Type[Payment]] = {
    PaymentMethod.CREDIT_CARD: 
        CreditCardPayment,
    PaymentMethod.INTERNET_BANKING: 
        InternetBankingPayment,
    PaymentMethod.PAYPAL: 
        PaypalPayment,
}