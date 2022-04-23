# based on default transaction code from Authorize.net

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
import sys
 
merchantAuth = apicontractsv1.merchantAuthenticationType()
merchantAuth.name = '2m9Hw5Qg'
merchantAuth.transactionKey = '6hUFVzvJ8Q8q467K'
 
creditCard = apicontractsv1.creditCardType()
creditCard.cardNumber ="4111111111111111"
creditCard.expirationDate ="2022-12"
 
payment = apicontractsv1.paymentType()
payment.creditCard = creditCard
 
transactionrequest = apicontractsv1.transactionRequestType()
transactionrequest.transactionType ="authCaptureTransaction"
try:
       transactionrequest.amount = Decimal(sys.argv[1])
       print('Amount of money passed to Python: ' + sys.argv[1])
except:
       transactionrequest.amount = Decimal('1.00')
transactionrequest.payment = payment
 
 
createtransactionrequest = apicontractsv1.createTransactionRequest()
createtransactionrequest.merchantAuthentication = merchantAuth
createtransactionrequest.refId ="MerchantID-0001"
 
createtransactionrequest.transactionRequest = transactionrequest
createtransactioncontroller = createTransactionController(createtransactionrequest)
createtransactioncontroller.execute()
 
response = createtransactioncontroller.getresponse()
 
if (response.messages.resultCode=="Ok"):
       print('Transaction ID: %s' % response.transactionResponse.transId)
else:
       print('response code: %s' % response.messages.resultCode)