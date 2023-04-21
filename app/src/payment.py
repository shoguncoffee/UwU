from .base import *

class Payment(ABC):
    def __init__(self, 
        total_price: int,
        transaction_id: Optional[UUID] = None,
    ):
        self._total_price = total_price
        self._transaction_id = transaction_id or uuid4()
        self._datetime = dt.datetime.now()
        self._status = PaymentStatus.PENDING
    
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
    
    @abstractmethod
    def pay(self) :
        pass


class CreditClassPayment(Payment) :
    #def __init__(self, securtity_code):
    #    self.security_code = securtity_code

    def pay(self,total_fare) :
        print("Credit Class Payment : SUCCESS")
        print("TRANSACTION ID :",self._transaction_id)
        print("TOTAL FARE :",total_fare,"THB")
        self._status = PaymentStatus.COMPLETED


class InternetBankingPayment(Payment) :
    def pay(self,total_fare) :
        print("Internet Banking Payment : SUCCESS")
        print("TRANSACTION ID :",self._transaction_id)
        print("TOTAL FARE :",total_fare,"THB")
        self._status = PaymentStatus.COMPLETED


class PaypalPayment(Payment) :
    def pay(self,total_fare) :
        print("Paypal Payment : SUCCESS")
        print("TRANSACTION ID :",self._transaction_id)
        print("TOTAL FARE :",total_fare,"THB")
        self._status = PaymentStatus.COMPLETED