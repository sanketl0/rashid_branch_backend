"""MyAutoCount URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from .import banking_update
from .banking_update import CustomerAdvanceViewset
from banking.viewsets import *
from purchase.viewsets.Expense_Record_view import ExpenseBankModelViewSets
from salescustomer.viewsets.salescustomer_view import getexcessamountpaymentbycustomerid,getpaymentbycustomerid,getcnstatusopenbycustomer,getcreditnotebycustomerid
from purchase.viewsets.Vendor_view import getexcessamountpaymentbyvendorid,getvendorpaymentrefbyvendorid,getdebitnotebyvendorid
from transaction.views import getJRNLBankTransbyCOAID,getJRNLBankTransbyNameCOAID

router=routers.SimpleRouter()
router.register('addbank',BankingViewsets,basename='addbank') 
#TTAA
#add ttaa
router.register('addtransfertobank',TransferToAnotherAccountViewsets,basename='addtransfertobank')
#CardPayment
#add Cardpayment
router.register('addcardpaymentbank',CardPaymentViewsets,basename='addcardpayment')
#DTOA
#Add DTOA
router.register('adddeposittobank',DTOAViewsets,basename='adddeposittobank')
#PaymentRefund
#Add PaymentRefund(Customer Advanced Refund)
router.register('addpaymentrefundbank',PaymentRefundViewsets,basename='addpaymentrefund')
# Customer Advanced
router.register('addcustomeradvancebank',CustomerAdvanceViewsets,basename='addcustomeradvancebank')

#Customer Payment
router.register('addcustomerpaymentbank',CustomerPaymentViewsets,basename='addcustomerpaymentbank')
#DFOA
router.register('adddepositfrombank',DFOAViewsets,basename='adddepositfromtbank')
#Vendor Advanced
#add vendor advanced
router.register('addtvendoradvanedbank',Vendor_AdvancedModelViewSets,basename='vendoradvanced')
#router.register('addtvendoradvanedrefundbank',views.Vendor_AdvancedRefund_newViewSets,basename='vendoradvanced')

#OwnerDrawing
# add owner drawing	
router.register('addownerdrawingsbank',OwnerdrawingModelViewSets,basename='ownerdrawing')
#Credit Note Refund
# add credit note refund
router.register('addcreditnoterefundbank',CNRefundModelViewSets,basename='creditnoterefund')
# OtherIncome
#Add Other Incomeaddpaymentrefundbank
router.register('addotherincomebank',OtherIncomeModelViewSets,basename='otherincome')
#ExpenseRefund
#Add ExpenseRefund
router.register('addexpenserefundbank',ExpRefundModelViewSets,basename='addexpenserefundbank')
# InterestIncome
#Add InterstIncome
router.register('addinterestincomebank',InterestIncomeModelViewSets,basename='interestincome')
#Owners Contribution
#Add Qwners Contribution
router.register('addownerscontributionbank',OwnersContributionModelViewSets,basename='ownerscontribution')
#Debit Note Refund
#Add Debitnote Refund
router.register('adddebitnoterefundbank',DebitNoteRefundModelViewSets,basename='debitnoterefund')
#expense bank
router.register('addexpensebank',ExpenseBankModelViewSets,basename='expensebank')
# tfaa
router.register('addtransferfrombank',TFAAModelViewSets,basename='tfaa')
# Vendor Payment Refund 
# Add Vendor Payment Refund
router.register('addvendorpaymentrefundbank',VendorPaymentRefModelViewSets,basename='addvendorpaymentrefundbank')

#VendorPayment
#Add Vendor Payment
router.register('addvendorpaymentbank',VendorPaymentModelViewSets,basename='addvendorpaymentbank')

#router.register('bankTransactions', bankTransactionsGenericAPIView)
router.register('updateca',CustomerAdvanceViewset)
router.register('updateva',banking_update.UpdateVendorAdvanceViewset)

urlpatterns = [
    path('', include(router.urls)),
    #get all transaction by bank_id
    #path('getalltransactionshortbycoaid/<uuid:pk>/', bankTransactionsGenericAPIView.as_view({'get': 'get'})), 
    path('getalltransactionshortbycoaid/<uuid:from_to_id>/', getJRNLBankTransbyCOAID),
    path('getalltransactionshortbyname/<uuid:from_to_id>/<str:name>/', getJRNLBankTransbyNameCOAID),
    # path('getalltransactionshortbyType/<uuid:from_to_id>/<str:type>/', getJRNLBankTransbyCOAID),
    #Banking
    path('getbankshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/',getbankshortbycompanyid),
    path('getBankById/<uuid:pk>/', getBankByIdView),
    path('getbank/',getallbanks.as_view()),
    
    #TTAA
    #path('gettransfertobankbycoaid/<uuid:pk>/',gettransfertobankbycoaid),
    
    #Cardpayment
    
    
    #DTOA
   # path('getdeposittobankbycoaid/<uuid:pk>/',views.getdeposittobankbycoaid),
    path('dtoafile_download/<uuid:dtoa_id>/',DTOAFileDownloadListAPIView.as_view()),
    #path('getdeposittobankbycoaid/<uuid:pk>/', DtoaItemGenericAPIView.as_view()),
    
    #PaymentRefund
    path('getexcessamountpaymentbycustomerid/<uuid:pk>/',getexcessamountpaymentbycustomerid),
   
    path('getpaymentbycustomerid/<uuid:pk>/',getpaymentbycustomerid),

    
  
    
    
    #CreditNoteRefund
    path('getcnstatusopenbycustomer/<uuid:pk>/',getcnstatusopenbycustomer),
 
    path('getcreditnotebycustomerid/<uuid:pk>/',getcreditnotebycustomerid),
    
   
    	 	  
    # Get DebitNote status open by vendor id	  
    
     # Get DebitNote by vendor id
    path('getdebitnotebyvendorid/<uuid:pk>/',getdebitnotebyvendorid), 
    
 

    #Vendor Payment Refund
    #Get Coa id by Vendor Payment Refund
  
    path('getexcessamountpaymentbyvendorid/<uuid:pk>/',getexcessamountpaymentbyvendorid),
    path('getvendorpaymentrefbyvendorid/<uuid:pk>/',getvendorpaymentrefbyvendorid),
    path('getBKDetailsByaccount_name/<uuid:comp_id>/<uuid:branch_id>/<str:name>/',getBKDetailsByaccount_name),
    path('getBKDetailsByaccount_type/<uuid:comp_id>/<uuid:branch_id>/<str:account_type>/',getBKDetailsByaccount_type),
#region

    #Vendor Payment
    #Get Vendor Paymentby coa id
    
    #Customer Payment
    #Get Customer Paymentby coa id
    # path('getcustomerpaymentbankbycoaid/<uuid:pk>/',getcustomerpaymentbankbycoaid),
    # path('getvendorpaymentbankbycoaid/<uuid:pk>/',getvendorpaymentbankbycoaid),
    # path('getvendorpaymentrefundbankbycoaid/<uuid:pk>/',getvendorpaymentrefundbankbycoaid),
    # path('gettransferfromanotheraccountbycoaid/<uuid:pk>/',gettransferfromanotheraccountbycoaid),
    # path('getexpensebankbycoaid/<uuid:pk>/',getexpensebankbycoaid),
    # path('getdnstatusopenbyvendorid/<uuid:pk>/',getdnstatusopenbyvendorid),
    # path('getdebitnoterefundbankbycoaid/<uuid:pk>/',getdebitnoterefundbankbycoaid), 
    # path('getownerscontributionbankbycoaid/<uuid:pk>/',getownerscontributionbankbycoaid),
    # path('getinterestincomebankbycoaid/<uuid:pk>/',getinterestincomebankbycoaid),
    # path('getexpenserefundbankbycoaid/<uuid:pk>/',getexpenserefundbankbycoaid),
    # path('getotherincomebankbycoaid/<uuid:pk>/',getotherincomebankbycoaid),
    # path('getcreditnoterefundbankbycoaid/<uuid:pk>/',getcreditnoterefundbankbycoaid),
    # path('getcardpaymentbankbycoaid/<uuid:pk>/',getcardpaymentbankbycoaid),
    # path('getpaymentrefundbankbycoaid/<uuid:pk>/',getpaymentrefundbankbycoaid),
    path('getcustomeradvancedbankbycoaid/<uuid:pk>/',getcustomeradvancedbankbycoaid),
    # path('getcustomerpaymentbankbycoaid/<uuid:pk>/',getcustomerpaymentbankbycoaid),
    # path('getdepositfrombankbycoaid/<uuid:pk>/',getdepositfrombankbycoaid),
    path('getvendoradvancedbankbycoaid/<uuid:pk>/',getvendoradvancedbankbycoaid),
    # path('getownerdrawingsbankbycoaid/<uuid:pk>/',get_getownerdrawingsbankbycoaid),
    
#endregion    
]
