from .payment import *

#RUN TEST


processorpayment1 = PaypalPayment(transaction_id="123456",payment_time="100",status=PaymentStatus.PENDING)
processorpayment1.pay(total_fare=199522)

