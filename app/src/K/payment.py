#from constants import PaymentStatus,PaymentMethod
#from creditcardpayment import CreditClassPayment
#from paypalpayment import PaypalPayment
#from internetbankingpayment import InternetBankingPayment


#ENUM
class PaymentStatus(enumerate) :
    PENDING = 'PENDING'
    FAILED = 'FAILED'
    COMPLETED = 'COMPLETED'
class PaymentMethod(enumerate) :
    PAYPAL = 'PAYPAL'
    INTERNETBANKING = 'INTERNETBANKING'
    CREDITCARD = 'CREDITCARD'


#CLASS
class Payment:
    def __init__(self,transaction_id,payment_time,status) :
        self._transaction_id = transaction_id
        self._payment_time = payment_time
        self._status = status

    def create_payment(self,total_fare,payment_method,balance) :
        if self.check_balance(total_fare,balance) == True:
            if payment_method == PaymentMethod.PAYPAL :
                self.pay(total_fare,balance)    #PayPalPayment
            elif payment_method == PaymentMethod.INTERNETBANKING :
                self.pay(total_fare,balance)    #InternetBankingPayment
            elif payment_method == PaymentMethod.CREDITCARD :
                self.pay(total_fare,balance)    #CreditCardPayment 
        else :
            self._status = PaymentStatus.FAILED
            print("PAYMENT STATUS :",self._status)

    def check_balance(self,total_fare,balance) :
        if balance >= total_fare :
            return True
        else :
            return False
        
    def pay(self,total_fare,balance) :
        balance = balance - total_fare
        self._status = PaymentStatus.COMPLETED
        print("TRANSACTION ID :",self._transaction_id)
        print("YOUR BALANCE :",balance)
        print("PAYMENT STATUS :",self._status)
