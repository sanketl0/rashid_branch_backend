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
from rest_framework import routers
# from .views import *
# import salescustomer.views
# from . views import InvoiceDownloadPdf,render_to_pdf,download_invoice,generate_invoice_pdf,download_inv,download_cn_data,download_cn,download_est_data,download_est,download_so_data
# from salescustomer import Sales_update
# download_so,generate_dc_pdf,download_dc,generate_pr_pdf,download_pr
# from . import views 
# from wsgiref.util import FileWrapper
# from .Sales_update import (UpdtPaymentRCvViewset,
#                         CustomerUpdtViewset,ShubhamEstimateUpdateViewSet,SalesOrderUpdateViewSet,DeliveryChalanUpdateViewSet)

from salescustomer.viewsets import *
from salescustomer.printing import *
from salescustomer.viewsets.salescustomer_view import  getCustomerDetailsByCustomerName

router = routers.SimpleRouter()
router.register('addcustomer', newcustomerViewSet)
router.register('addcustomerob', customerobViewSet)
#router.register('addestimates', estimateViewSet)
router.register('addestimate', estimateitemsViewSet, basename='addesaddpaymentreceivetimate')
#router.register('addso', soViewSet)
router.register('addsalesorder', salesorderitemsViewSet, basename='addsalesorder')#post for sales order and item
router.register('adddc', dcitemsViewSet)#post for delivery challan and item
router.register('addcreditnote', new3creditnoteitemsViewSet)# post for credit note and item
router.register('addinvoice', new3invoiceitemsViewSet)# post for invoice and item
router.register('addpaymentmode', paymentmodeViewSet)
router.register('addpaymentreceive', new1paymentreceiveViewSet)#post for payment receive and payment transaction
router.register('addpaymentreceivenewfrom', paymentreceivenew_fromViewSet)#post for payment receive and payment transaction

router.register('addpr', demoViewSet)
router.register('addsoitem', soitemViewSet)#so item post url
router.register('addpaymentterm', paymenttermViewSet)#url to post data
router.register('getpaymentterms', paymenttermViewSet)#url to get data
router.register('addemployee', employeeViewSet)
router.register('addtcs', tcsViewSet)
router.register('addnewcustomeradvancebank',SalesCustomerAdvanceViewsets,basename='newformaddcustomeradvancenbank')
router.register('addnewcreditnoterefundbank',SalesCNRefundModelViewSets,basename='creditnoterefund')
# router.register('updateinvoice', InvoiceUpdate4ViewSet)# post for invoice and item
router.register('updatecreditnote', CreditNoteUpdate3ViewSet)

router.register('updateso', SalesOrderUpdateViewSet),
router.register('updatedc', DeliveryChalanUpdateViewSet)
router.register('updateest', ShubhamEstimateUpdateViewSet)
router.register('updatepmr', UpdtPaymentRCvViewset)  #CustomerUpdtViewset
router.register('updatecustomer', CustomerUpdtViewset)
router.register('multipleinvoice', MultipleInvoice_Paid_At_onetime)

urlpatterns = [
    path('update-invoice/<uuid:pk>/',UpdateInvoiceView.as_view()),
    path('update-customer-advance/<uuid:pk>/', CustomerAdvanceUpdateView.as_view()),
    path('addNewEstimate/',EstimatedView.as_view()),
    path('', include(router.urls)),
    path('customer', customerList.as_view()),#remove add from here List will be display
    path('getcustomer', customerList.as_view()),   
    path('getpaymentterms/<uuid:company_id>/<uuid:branch_id>/',PaymentTermView.as_view()),
    #get customer opening balance
    path('getcustomerob', CustomerGenericAPIView.as_view()),#customer opening balance join
    
    #path('getcustomer', views.customerCreation, name='custinvoicerefbycustomeridomer'),
    path('getcustomershort', ShortCustomerDetails, name='customer'),

    #get customer by company id
    path('getcustomershortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', customershortbycompanyid, name='customer'),
    path('getcustomershortpaginationbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', customershortbypaginationcompanyid, name='customer'),
    path('getallcustomershortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', customerallshortbycompanyid, name='customer'),
    path('getallcustomershortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/<str:customer_name>/', customernameallshortbycompanyid, name='customer'),
    #Customer by name   
    path('getcustomerbyname/', customername, name='customer'), 

    # customer by id   
    path('getcustomerbyid/<uuid:pk>/', customerDetail, name='getcustomerbyid'),
    #Update customer opening balance by ob id
    path('updatecustomerobbyid/<uuid:pk>/', customerobUpdate, name='updatecustomerobbyid'),

    #Customer Advanced Refund 
    path('getcajournaltransactionbyca_id/<uuid:ca_id>/', getCARJournalTransaction, name='getCARJournalTransaction'),
    path('carffile_download/<uuid:ca_id>/',CARFFileDownloadListAPIView.as_view()),
    path('Downloadcarf/<str:file_name>',download_carf),
    path('DownloadCAR/<uuid:comp_id>/<uuid:pr_id>/',download_carf_data),
    path('getcarefundshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/',carefundshortbycompanyid, name='carefundshortbycompanyid'),
    path('getsalescaby_id/<uuid:pk>/', CustomerAdvGenericAPIView.as_view()),
    path('getsalescatransactionbyca_id/<uuid:ca_id>/',salescabyid, name='salescabyid'),
    path('carffile_download/<uuid:ca_id>/',CARFFileDownloadListAPIView.as_view()),
    
    #Estimate path    
    path('getestimatebyorder', estimateList.as_view()), #it will show results in order by created date   
    path('getestimateshort', ShortEstimateDetails, name='estimate'),
    #path('getestimatebyid/<uuid:pk>/', views.estimateDetail, name='getestimatebyid'),
    path('updatebyid/<uuid:pk>/', estimateUpdate, name='updatebyid'),
    path('getestimateitem', EstimateGenericAPIView.as_view()),
    path('getestimate', EstimatedItemGenericAPIView.as_view()),#Estimated Item get api url
    path('getestimatebyid/<uuid:pk>/', EstimatedItemGenericAPIView.as_view()),#Estimated Item get api url by id
    path('estimatefile_download/<uuid:estimate_id>/',EstimateFileDownloadListAPIView.as_view()),
    #for view the pdf
    path('estimatepdf/<uuid:estimate_id>/',EstimateGeneratePdf.as_view()),
    # for download the pdf
    path('estimatepdf_download/', EstimateDownloadPdf.as_view(),name='DownloadPdf'),
    path('getestimateshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', getestimateshortbycompanyid, name='estimate'),
     path('Downloadest/<str:file_name>',download_est),
    path('DownloadEST/<uuid:est_id>/',download_est_data),

    ################ Generate pdf for customer advance and download ###################
    path('Downloadca/<str:file_name>',download_ca),
    path('DownloadCA/<uuid:comp_id>/<uuid:ca_id>/',download_customer_advanced_data),



    #Sales Order 
    #Sales Order
    path('getsalesorder', SoItemGenericAPIView.as_view()),#so Item get api url
    path('getsalesorderbyid/<uuid:pk>/', SoItemGenericAPIView.as_view()),
    path('getsalesordershort', ShortSalesOrderDetails, name='getsalesordershort'),
    path('salesorderfile_download/<uuid:salesorder_id>/',SalesorderFileDownloadListAPIView.as_view()),
    #for view the pdf
    path('salesorderpdf/<uuid:salesorder_id>/',SalesorderGeneratePdf.as_view()),
    # for download the pdf
    path('salesorderpdf_download/', SalesorderDownloadPdf.as_view(),name='DownloadPdf'),
    path('getsalesordershortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', getsalesordershortbycompanyid, name='salesorder'),
     path('Downloadso/<str:file_name>',download_so),
    path('DownloadSO/<uuid:so_id>/',download_so_data),
   
   
    #Delivery challan    
    path('getdc', DcItemGenericAPIView.as_view()),#so Item get api url
    path('getdcbyid/<uuid:pk>/', DcItemGenericAPIView.as_view()),
    path('getdcshort', ShortDeliveryChallanDetails, name='getdcshort'),    
    path('getdcshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', dcshortbycompanyid, name='dc'),#get dc by company id
    path('dcfile_download/<uuid:dc_id>/',DelivarychallanFileDownloadListAPIView.as_view()),
    #for view the pdf
    path('dcpdf/<uuid:dc_id>/',DelivaryChallenGeneratePdf.as_view()),
    # for download the pdf
    path('dcpdf_download/', DelivarychallenDownloadPdf.as_view(),name='DownloadPdf'),
    path('DownloadDC/<str:file_name>',download_dc),
    path('DownloadDC/<uuid:dc_id>/',download_dc_data),

    #Credit Note    
    path('getcreditnote', CreditNoteItemGenericAPIView.as_view()),#credit note Item get api url
    path('getcreditnotebyid/<uuid:pk>/', CreditNoteItemGenericAPIView.as_view()), # get full details by id
    path('getcreditnoteshort', ShortCreditNoteDetails, name='getcreditnoteshort'),
    path('getcreditnoteshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', cnshortbycompanyid, name='getcreditnoteshortbycompanyid'), # get credit note by company id
    path('getsalescnreftransactionshortbycn_id/<uuid:form_id>/', salescntransactionshortbycnid, name='salescntransactionshortbycnid'), # get credit note by company id 
    
    # path('getcreditnotejournaltransactionbycnid/<uuid:pk>/', creditnotejournaltransactionDetail, name='gecreditnotejournaltransactionbycnid'), # get credit note journal  transaction by credit note id 
    path('creditnotefile_download/<uuid:creditnote_id>/',CreditnoteFileDownloadListAPIView.as_view()),
    #for view the pdf
    path('creditnotepdf/<uuid:creditnote_id>/',CreditnoteGeneratePdf.as_view()),
    path('Downloadcn/<str:file_name>',download_cn),
    path('DownloadCN/<uuid:cn_id>/',download_cn_data),
    # for download the pdf

    #Invoice
    path('getinvoice', InvoiceItemGenericAPIView.as_view()),#so Item get api url
    path('getinvoicebyid/<uuid:pk>/', InvoiceItemGenericAPIView.as_view()),

    path('getinvoicebyinvoiceid/<uuid:invoice_id>/',getinvoicebyinvoiceid),
    path('get2areports/<uuid:company_id>/',get2Areports),
    

    #path('getinvoicebycustomerid', salescustomer.views.invoiceList.as_view()),
    path('getinvoiceshort', ShortInvoiceDetails, name='getinvoiceshort'),
    path('getAllPeginatedInvoiceDetails/', getAllPeginatedInvoiceDetails),
    path('getinvoiceshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', invoiceshortbycompanyid, name='getinvoiceshortbycompanyid'),
    path('getinvoicebycustomerid/<uuid:pk>/', invoicebycustomerid, name='getinvoicebycustomerid'),#get invoices by customer id
    # path('getinvoicejournaltransaction', invoicejournaltransactionList.as_view()),
    # path('getinvoicejournaltransactionbyinvoiceid/<uuid:pk>/', invoicejournaltransactionDetail, name='getinvoicejournaltransactionbyinvoiceid'), # get invoice journal  transaction by invoice id 
    path('invoicefile_download/<uuid:invoice_id>/',FileDownloadListAPIView.as_view()),
    path('invoicerefbycustomerid/<uuid:pk>/', invoicerefbycustomerid, name='invoicerefbycustomerid'),#get invoices ref by customer id
    #for view the pdf
  #  path('invoicepdf/<uuid:invoice_id>/',InvoiceGeneratePdf.as_view()),
    # for download the pdf
    path('invoicepdf_download/', InvoiceDownloadPdf.as_view(),name='DownloadPdf'),
    # path('invoice/<uuid:invoice_id>/',views.generate_invoice),
    
    path('in/',generate_invoice_pdf),
    path('Downloadinvoice/<str:file_name>',download_invoice),
    path('DownloadINV/<uuid:invoice_id>/',download_inv),

    path('getAllInvoicedetails/',getAllInvoicedetails),




   # Payment mode 
    path('getpaymentmode/<uuid:comp_id>/<uuid:branch_id>/', paymentModeView.as_view()),

    # Payment Receive 

    path('getpaymentreceive', PRGenericAPIView.as_view()),#so Item get api url
    path('getpaymentreceivebyid/<uuid:pk>/', prfullview,name='prfullview'),
    path('getmydata/<uuid:pk>/', prfullview,name='prfullview'),

    path('getprshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', prshortbycompanyid, name='getprshortbycompanyid'),
    
    
   
    path('prfile_download/<uuid:pr_id>/',PRFileDownloadListAPIView.as_view()),
    #for view the pdf
    path('prpdf/<uuid:pr_id>/',PRGeneratePdf.as_view()),
    # for download the pdf
    path('prpdf_download/', PRDownloadPdf.as_view(),name='DownloadPdf'),

    # Employee
    path('getemployee/<uuid:comp_id>/<uuid:branch_id>/', employeeList.as_view()),
    path('getemployeeAll/<uuid:comp_id>/<uuid:branch_id>/', employeeAllList),
    # TCS
    path('gettcs/<uuid:comp_id>/<uuid:branch_id>/', tcsList.as_view()),
    
    path('Downloadpr/<str:file_name>',download_pr),
    path('DownloadPR/<uuid:pr_id>/',download_pr_data),
    #Customer Advanced Refund 
    path('Downloadcarf/<str:file_name>',download_carf),
    path('DownloadCA/<uuid:ca_id>/',download_carf_data),
    path('invoiceupdate/<uuid:invoice_id>/',updateinvoice),
    
    
    
    #This Section Is pagination Of Sales 
    path('getAllPeginatedInvoiceDetails/', getAllPeginatedInvoiceDetails),
    path('getAllPeginatedCustomerDetails/', getAllPeginatedCustomerDetails),
    path('getAllPeginatedCustomername/', getAllPeginatedCustomername),
    path('getPeginatedShortEstimateDetails/', getPeginatedShortEstimateDetails),
    path('getAllPeginatedEstimateDetails/', getAllPeginatedEstimateDetails),
    path('getPeginatedSalesOrderDetails/', getShortPeginatedSalesOrderDetails),
    path('getPeginatedDeliveryChallanDetails/',getShortPeginatedDeliveryChallanDetails),
    path('gePeginatedCreditNoteDetails/', getShortPeginatedCreditNoteDetails),

    
    path('getinvoiceitembyinvoiceid/<uuid:invoice_id>/',getinvoiceitembyinvoiceid),

    path('getestimateitembyest_id/<uuid:est_id>/',getestimateitembyest_id),
    path('getestimatebyest_id/<uuid:est_id>/',getest_byestid),
    path('getcoatransactionsbycustomer_id/<uuid:from_to_id>',getJRNLTransbyCUSTOMERID),
    path('getjrnlbyformid/<uuid:form_id>',getJRNLbyFormID),
    path('getCustomerDetailsByCustomerName/<uuid:company_id>/<uuid:branch_id>/',getCustomerDetailsByCustomerName),
    path('getCustomerDetailsByCustomerMobileNo/<uuid:company_id>/<uuid:branch_id>/',getCustomerDetailsByCustomerMobileNo),
    path('getEsatimateDetailsByEstimateNumber/<uuid:company_id>/<uuid:branch_id>/<str:est_serial>/',getEsatimateDetailsByEstimateNumber),
    path('getSODetailsBySoNumber/<uuid:company_id>/<uuid:branch_id>/<str:so_serial>/',getSODetailsBySoNumber),
    path('getDCDetailsByDC_Serial/<uuid:company_id>/<uuid:branch_id>/<str:dc_serial>/',getDCDetailsByDC_Serial),
    path('getInvoiceDetailsByInvoice_Serial/<uuid:company_id>/<uuid:branch_id>/',getInvoiceDetailsByInvoice_Serial),
    path('getPRDetailsByPR_number/<uuid:company_id>/<uuid:branch_id>/',getPRDetailsByPR_number),
    path('getPRAdvDetailsByPR_number/<uuid:company_id>/<uuid:branch_id>/<str:payment_serial>/',getPRAdvDetailsByPR_number),
    path('getCNDetailsByCN_number/<uuid:company_id>/<uuid:branch_id>/',getCNDetailsByCN_number),
    #getEstimateshortbyCustomer_name
    path('getEstimateshortbyCustomer_name/<uuid:company_id>/<uuid:branch_id>/<str:customer_name>/',getEstimateshortbyCustomer_name),
    path('getCADetailsBypm_serial/<uuid:company_id>/<uuid:branch_id>/<str:payment_serial>/',getCADetailsBypm_serial),
    path('getInvoiceshortbyCustomer_name/<uuid:company_id>/<uuid:branch_id>/',getInvoiceshortbyCustomer_name),
    path('getCNshortbyCustomer_name/<uuid:company_id>/<uuid:branch_id>/',getCNshortbyCustomer_name),
    path('getSOshortbyCustomer_name/<uuid:company_id>/<uuid:branch_id>/<str:customer_name>/',getSOshortbyCustomer_name),
    path('getDCshortbyCustomer_name/<uuid:company_id>/<uuid:branch_id>/<str:customer_name>/',getDCshortbyCustomer_name),
    path('getPRshortbyCustomer_name/<uuid:company_id>/<uuid:branch_id>/',getPRshortbyCustomer_name),
    path('getPRAdvshortbyCustomer_name/<uuid:company_id>/<uuid:branch_id>/<str:customer_name>/',getPRAdvshortbyCustomer_name),
    path('getCAhortbyCustomer_name/<uuid:company_id>/<uuid:branch_id>/<str:customer_name>/',getCAhortbyCustomer_name),
    path('getInvoiceSerial/<uuid:comp_id>/<uuid:branch_id>/',getCurrentInvoiceId)
    ]
