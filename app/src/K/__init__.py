from .account import Account
from .payment import Payment
from .admin import Admin
from .creditcardpayment import CreditClassPayment
from .internetbankingpayment import InternetBankingPayment
from .paypalpayment import PaypalPayment
from .schedulecatalog import ScheduleCatalog
from .scheduledate import ScheduleDate
#from constants import *

'''
RUN TEST
k = Payment(transaction_id="123456",payment_time="100",status=PaymentStatus.PENDING)
k.create_payment(total_fare=1000,payment_method=PaymentMethod.PAYPAL,balance=5000)
'''