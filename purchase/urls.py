"""api URL Configuration

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
from django.urls import include, path
from .import views
from .views import * # import List and Viewset of app from views
from rest_framework import routers
from purchase.viewsets import *
from banking.viewsets.refund_master_view import NewVendor_debitRefundModelViewSets
from transaction.views import getDNRJournalTransaction
router = routers.SimpleRouter()
#Add Vendor
router.register('addvendor', vendorViewset)
#Creating the Bill
router.register('addbill', BillitemsViewSet)# post for invoice and item and journal transaction\
#Add Tcs
router.register('addtds', tdsViewSet)
#Creating the Expense
router.register('addexpense', new3expenserecordViewSet)
#Add Payment Made
router.register('addpaymentmade',PaymentmadeJournalViewsets, basename='addpaymentmade') #  Add PaymentMade
router.register('addpurchaseorder', purchaseorderitemsViewSet)
router.register('adddebitnote',DebitnoteItemViewSet,basename='adddebitnote')# add debit note
router.register('vendordebitrefund',NewVendor_debitRefundModelViewSets,basename='vendordebitrefund')# add debit note
router.register('vendoradvancerefund',Vendor_AdvancedRefundModelViewSets,basename='vendoradvancerefund')# add debit note
router.register('updatebill', BillUpdate3ViewSet)
router.register('updatedebitnote',DebitnoteUpdate3ViewSet)


router.register('updatepo', PurchaseOrderUpdateViewSet)
# router.register('updatepm', UpdtPaymentMadeViewset)
router.register('updatevendor', VendorUpdtViewset)
router.register('updateer', ExpenseUpdateViewset)


# router.register('addmultiplebill', MultipleBill_Paid_At_onetime)
router.register('multiplebill',MultipleBill_Paid_At_onetime)
urlpatterns = [
    path('update-bill/<uuid:pk>/',BillUpdateView.as_view()),
    path('update-vendor-advance/<uuid:pk>/',VendorAdvanceUpdateView.as_view()),
    path('', include(router.urls)),
    path('updatepm/<uuid:pk>',UpdtPaymentMadeViewset.as_view()),
    path('getvendor/', VendorAndContactGenericAPIView.as_view()),#Vendor and contact get api url   
    path('getvendorbyid/<uuid:pk>/', vendorDetail, name='getvendorbyid'),
    path('getvendorbyname/', vendorname, name='vendor'), #it will return all vendor list
    path('getvendorshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', vendorshortbycompanyid, name='vendorbycompany'),  #get vendor by company id
    path('getvendorshortpaginationbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', getvendorshortpaginationbycompanyid, name='vendorbycompany'),
    path('getallvendorshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/',vendorallshortbycompanyid),
    path('getallvendorshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/<str:vendor_name>/',vendornameallshortbycompanyid),
    path('getcontactallshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/<str:name>/',contactallshortbycompanyid),
    path('UpdateById/<int:pk>/', vendorUpdate, name='UpdateById'),


    #Billupdatepm
    path('getbill/', BillItemGenericAPIView.as_view()),#so Item get api urlupdatevendor
    path('getbillbyid/<uuid:pk>/', BillItemGenericAPIView.as_view()),
    #path('getinvoicebycustomerid', sales.views.invoiceList.as_view()),
    #path('invoicestatus', sales.views.invoiceListView.as_view()),
    path('getbillshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', billshortbycompanyid, name='getbillshortbycompanyid'),
    # path('getbillbyvendorid/<uuid:pk>/', billbyvendorid, name='getbillbyvendorid'),#get invoices by customer id
    # path('getbilljournaltransaction', billjournaltransactionList.as_view()),
    # path('getbilljournaltransactionbybillid/<uuid:pk>/', billjournaltransactionDetail, name='getbilljournaltransactionbybillid'), # get bill journal  transaction by bill id
    path('getbillbyvendorid/<uuid:pk>/', billbyvendorid, name='getbillbyvendorid'),#get bills by vendor id
    path('billfile_download/<uuid:bill_id>/',BillFileDownloadListAPIView.as_view()),
    path('billfile_download/<uuid:bill_id>/',BillFileDownloadListAPIView.as_view()),
    #for view the pdf
    path('billpdf/<uuid:bill_id>/',BillGeneratePdf.as_view()),
    # for download  the pdf
    path('billpdf_download/', BillDownloadPdf.as_view(),name='DownloadPdf'),
    path('Downloadbill/<str:file_name>',download_bl),
    path('DownloadBL/<uuid:bill_id>/',download_bill_data),
    #billrefbyvendorid
    path('billrefbyvendorid/<uuid:pk>/', Billrefbyvendorid, name='billrefbyvendorid'),
    
    ################ Generate pdf for vendor  advance and download ###################
    path('Downloadva/<str:file_name>',download_va),
    path('DownloadVA/<uuid:va_id>/',download_vendor_advanced_data),

   # Get TDS
    path('gettds/<uuid:comp_id>/<uuid:branch_id>/', tdsList.as_view()),


    # Expense Record 
    path('getexpense', expenserecordList.as_view()),    
    path('getexpensebyid/<uuid:pk>/', expenserecordList.as_view()),
    path('getexpenseshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', ershortbycompanyid, name='getexpenseshortbycompanyid'),
    #path('getexpensejournaltransaction', expensejournaltransactionList.as_view()),
    #path('getexpensejournaltransactionbyerid/<uuid:pk>/', expensejournaltransactionDetail, name='getexpensejournaltransactionbyerid'), # get expense journal  transaction by er id 
    path('expensefile_download/<uuid:er_id>/',ExpenseFileDownloadListAPIView.as_view()),
    path('Downloadexp/<str:file_name>',download_exp),
    path('DownloadEXP/<uuid:er_id>/',download_exp_data),

    # Payment Made
    path('getpaymentmade', paymentmadedList.as_view()),
    path('getpaymentmadebyid/<uuid:pk>/',getpaymentmade),# GET Paymentmade 
    #path('getpaymentmadejournaltransactionbypmid/<uuid:pk>/',getpaymentmadejournaltrasctionbyid),#getpaymentmadejournaltrasctionbyid
    path('getpaymentmadeshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/',getpaymentmadeshortbycompanyid),#getshortbycompanyid
    path('Downloadpm/<str:file_name>',download_pm),
    path('DownloadPM/<uuid:pm_id>/',download_pm_data),


   #Purchase order
    path('getpurchaseorder', PoItemGenericAPIView.as_view()),#po Item get api url
    path('getpurchaseorderbyid/<uuid:pk>/', PoItemGenericAPIView.as_view()),
    #getshortbycompanyid
    path('getpurchaseordershortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', getpurchaseordershortbycompanyid),
    path('getpoitem', PoItemGenericAPIView.as_view()),#po Item get api url
    path('purchaseorderfile_download/<uuid:purchaseorder_id>/',POFileDownloadListAPIView.as_view()),
    #for view the pdf
    path('purchaseorderpdf/<uuid:purchaseorder_id>/',POGeneratePdf.as_view()),
    # for download the pdf
    path('purchaseorderpdf_download/', PODownloadPdf.as_view(),name='DownloadPdf'),
    path('Downloadpo/<str:file_name>',download_po),
    path('DownloadPO/<uuid:po_id>/',download_po_data),


    #Debit Note    
    path('getdebitnote', DebitNoteItemGenericAPIView.as_view()),#credit note Item get api url
    path('getdebitnotebyid/<uuid:pk>/', DebitNoteItemGenericAPIView.as_view()), # get full details by id
    path('getdebitnoteshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', dnshortbycompanyid, name='getdebitnoteshortbycompanyid'), # get details by company id
    #path('gedebitnotejournaltransactionbydnid/<uuid:pk>/', debitnotejournaltransactionDetail, name='getdebitnotejournaltransactionbydnid'), # get debit note journal  transaction by debit note id 
    path('debitnotefile_download/<uuid:debitnote_id>/',DebitnoteFileDownloadListAPIView.as_view()),
    #for view the pdf
    path('debitnotepdf/<uuid:debitnote_id>/',DebitnoteGeneratePdf.as_view()),
    # for download the pdf
    path('debitnotepdf_download/', DebitnoteDownloadPdf.as_view(),name='DownloadPdf'),
    path('Downloaddn/<str:file_name>',download_dn),
    path('DownloadDN/<uuid:dn_id>/',download_dn_data),
    path('getdnjournaltransactionbydn_id/<uuid:dn_id>/', getDNRJournalTransaction, name='getDNRJournalTransaction'),
   
    #vendor Advanced Refund
    path('getvajournaltransactionbyva_id/<uuid:va_id>/', getVARJournalTransaction, name='getVARJournalTransaction'),
    path('getvendoradvrefshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', varshortbycompanyid, name='getvendoradvrefshortbycompanyid'), # get details by company id
    path('getpurchasevaby_id/<uuid:pk>/', VendorAdvGenericAPIView.as_view()),
    path('varffile_download/<uuid:va_id>/',VARFFileDownloadListAPIView.as_view()),


    path('getbillitembybillid/<uuid:bill_id>/',getbillitembybillid),
    path('getdebitnotebydn_id/<uuid:dn_id>/',getdebitnoteitembydn_id),
    path('getcoatransactionsbyvendor_id/<uuid:from_to_id>',getJRNLTransbyVENDORID),
    path('getVendorDetailsByVendorName/<uuid:company_id>/<uuid:branch_id>/<str:vendor_name>/',getVendorDetailsByVendorName),
    path('getPODetailsByPo_serial/<uuid:company_id>/<uuid:branch_id>/<str:po_serial>/',getPODetailsByPo_serial),
    path('getBillDetailsBybill_serial/<uuid:company_id>/<uuid:branch_id>/',getBillDetailsBybill_serial),
    path('getDNDetailsBydn_serial/<uuid:company_id>/<uuid:branch_id>/',getDNDetailsBydn_serial),
    path('getExpenseRecordDetailsByexpense_serial/<uuid:company_id>/<uuid:branch_id>/<str:expense_serial>/',getExpenseRecordDetailsByexpense_serial),
    path('getVADetailsBypm_serial/<uuid:comp_id>/<uuid:branch_id>/<str:payment_serial>/',getVADetailsBypm_serial),
    path('getPMDetailsBypm_serial/<uuid:company_id>/<uuid:branch_id>/<str:payment_serial>/',getPMDetailsBypm_serial),

    path('getVendorDetailsByVendorContact/<uuid:company_id>/<uuid:branch_id>/<str:vendor_mobile>/',getVendorDetailsByVendorContact),
    path('getExpenseRecordDetailsByvendor_name/<uuid:company_id>/<uuid:branch_id>/<str:vendor_name>/',getExpenseRecordDetailsByvendor_name),
    path('getPODetailsByvendor_name/<uuid:company_id>/<uuid:branch_id>/<str:vendor_name>/',getPODetailsByvendor_name),
    path('getBillDetailsByvendor_name/<uuid:company_id>/<uuid:branch_id>/',getBillDetailsByvendor_name),
    path('getPMDetailsByvendor_name/<uuid:company_id>/<uuid:branch_id>/<str:vendor_name>/',getPMDetailsByvendor_name),
    path('getDNDetailsByvendor_name/<uuid:company_id>/<uuid:branch_id>/',getDNDetailsByvendor_name),
    path('getPMAdvshortbyVendor_name/<uuid:company_id>/<uuid:branch_id>/<str:vendor_name>/',getPMAdvshortbyVendor_name)
]
