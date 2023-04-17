from ..base import *

class Payment(ABC):
    
    def __init__(self,transaction_id,payment_time,status) :
        self._transaction_id = transaction_id
        self._payment_time = payment_time
        self._status = status
        
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