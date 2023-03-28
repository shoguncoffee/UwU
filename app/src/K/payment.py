from ..constants import PaymentStatus, PaymentMethod

#CLASS
class Payment():
    
    def __init__(self,transaction_id,payment_time,status) :
        self._transaction_id = transaction_id
        self._payment_time = payment_time
        self._status = status

    def check_balance(self,total_fare,balance) :
        if balance >= total_fare :
            return True
        else :
            return False
    
    def pay(self) :
        pass

class CreditClassPayment(Payment) :
    #def __init__(self, securtity_code):
    #    self.security_code = securtity_code

    def pay(self,total_fare,balance) :
        if self.check_balance(total_fare,balance) == True:
            print("Credit Class Payment : SUCCESS")
            print("TRANSACTION ID :",self._transaction_id)
            print("YOUR BALANCE BEFORE TRANSACTION :",balance)
            balance = balance - total_fare
            print("YOUR BALANCE AFTER TRANSACTION :",balance)
            self._status = PaymentStatus.COMPLETED
        else :
            self._status = PaymentStatus.FAILED
            print("PAYMENT STATUS :",self._status)

class InternetBankingPayment(Payment) :
    def pay(self,total_fare,balance) :
        if self.check_balance(total_fare,balance) == True:
            print("Internet Banking Payment : SUCCESS")
            print("TRANSACTION ID :",self._transaction_id)
            print("YOUR BALANCE BEFORE TRANSACTION :",balance)
            balance = balance - total_fare
            print("YOUR BALANCE AFTER TRANSACTION :",balance)
            self._status = PaymentStatus.COMPLETED
        else :
            self._status = PaymentStatus.FAILED
            print("PAYMENT STATUS :",self._status)

class PaypalPayment(Payment) :
    def pay(self,total_fare,balance) :
        if self.check_balance(total_fare,balance) == True:
            print("Paypal Payment : SUCCESS")
            print("TRANSACTION ID :",self._transaction_id)
            print("YOUR BALANCE BEFORE TRANSACTION :",balance)
            balance = balance - total_fare
            print("YOUR BALANCE AFTER TRANSACTION :",balance)
            self._status = PaymentStatus.COMPLETED
        else :
            self._status = PaymentStatus.FAILED
            print("PAYMENT STATUS :",self._status)