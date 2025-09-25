from django.urls import include, path
from .import views
from .views import * # import List and Viewset of app from views


urlpatterns = [        
    #get payment receive by company id 
    path('getpaymentreceivedreportbycompanyid/<uuid:comp_id>/', views.prshortbycompanyid, name='getpaymentreceivedreportbycompanyid'),
    #get credit note by company id 
    path('getcreditnotereportbycompanyid/<uuid:comp_id>/', views.cnshortbycompanyid, name='getcreditnotereportbycompanyid'),   
    # get invoice by company id
    path('getinvoicedetailsbycompanyid/<uuid:comp_id>/', views.invoiceshortbycompanyid, name='getinvoiceshortbycompanyid'),
    # get sales order short by company idBillExcelReport
    path('getsalesorderdetailsbycompanyid/<uuid:comp_id>/', views.ShortSalesOrderDetails, name='getsalesorderdetailsbycompanyid'),
    # get delivery challan short by company id
    path('getdeliverychallandetailsbycompanyid/<uuid:comp_id>/', views.dcshortbycompanyid, name='getdeliverychallandetailsbycompanyid'),
    # get estimate short by company id
    path('getestimatedetailsbycompanyid/<uuid:comp_id>/', views.ShortEstimateDetails, name='getestimatedetailsbycompanyid'),
    # get bill short by company id
    path('getbilldetailsbycompanyid/<uuid:comp_id>/', views.billshortbycompanyid, name='getbilldetailsbycompanyid'),
    # get debit note by company id
    path('getdebitnotedetailsbycompanyid/<uuid:comp_id>/', views.dnshortbycompanyid, name='getdebitnotedetailsbycompanyid'),
    # get payment made short by company id
    path('getpaymentsmadebycompanyid/<uuid:comp_id>/',views.getpaymentmadeshortbycompanyid, name='getpaymentsmadebycompanyid'),
    # get purchase order short by company id
    path('getpurchaseorderdetailsbycompanyid/<uuid:comp_id>/', views.getpurchaseordershortbycompanyid),
    # get payable summary
    #path('getpayablesummarybycompanyid/<uuid:comp_id>/', views.getpayablesummarybycompanyid, name='getpayablesummarybycompanyid'),
    #get expense details
    path('getexpensedetailsbycompanyid/<uuid:comp_id>/', views.ershortbycompanyid, name='getexpensedetailsbycompanyid'),
    #Balance Sheat  Deatils
    path('getbalancesheat_to_from_date/<from_date>/<to_date>/<uuid:comp_id>/',views.getbalancesheat_to_from_date),
    path('getbalancesheat_range_date/<from_date>/<to_date>/<uuid:comp_id>/',BalanceSheetView.as_view()),
    path('getbalancesheet/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/',BalanceSheetReportView.as_view()),
    path('getbalancesheet/<from_date>/<to_date>/<uuid:comp_id>/',BalanceSheetReportView.as_view()),

    path('getprofit_and_loss_to_from_date/<from_date>/<to_date>/<uuid:comp_id>/',views.getprofit_loss_to_from_date),
    path('getprofit_and_loss/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/',ProfitLossReportView.as_view()),
    path('getprofit_and_loss/<from_date>/<to_date>/<uuid:comp_id>/',ProfitLossReportView.as_view()),

    path('DownloadReport/<report_file>', views.download_a_report),
 
#All Transaction Details Journal TransacInvoiceExcelReporttion
    path('getjrnlbyformid/<uuid:form_id>',views.getJRNLbyFormID),
    #path('getjrnlbyformid/',views.getJRNLbyFormID)


#GST Report
#this Report Description Added in View File check first domain Konwladge
    path('getsalesgstreport/<from_date>/<to_date>/<uuid:comp_id>/',views.getsales_gstreport_bycompanyid),
    path('getsalesgst/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/',views.getsales_gst_bycompanyid),
    path('getpurchasegstreport/<from_date>/<to_date>/<uuid:comp_id>/',views.getpurchase_gstreport_bycompanyid),
    path('getpurchasegst/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/',views.getpurchase_gst_bycompanyid),
    path('get3Breportscompanyid/<from_date>/<to_date>/<uuid:comp_id>/', views.get3Bs_gstreport_bycompanyid, name='get3B_gstreport_bycompanyid'),
    path('get3Breport/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/', views.getGSTR3bBydate),
    path('get2Areport/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/', views.getGSTR2aBydate),
    path('get2Breport/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/', views.getGSTR2bBydate),
    path('get2Areportscompanyid/<from_date>/<to_date>/<uuid:comp_id>/', views.get2A_gstreport_bycompanyid, name='get3B_gstreport_bycompanyid'),
    path('get2Breportscompanyid/<from_date>/<to_date>/<uuid:comp_id>/', views.get2B_gstreport_bycompanyid, name='get3B_gstreport_bycompanyid'),
    path('get-audit-logs/<str:start_date>/<str:end_date>/<uuid:company_id>/<uuid:branch_id>/', AuditView.as_view()),
    
    #Cash Book report Api Expolre Cash Book Report Domain Knowladge and the check the 
    #code and implemented report 
    path('daybookreport/<uuid:comp_id>/<uuid:branch_id>/<date>/',views.getDayBookReportLbydate),
    path('cashbookreport/<uuid:comp_id>/<from_date>/<to_date>/',views.getCashBookReportLbydate),
    path('cashbook/<uuid:comp_id>/<uuid:branch_id>/<from_date>/<to_date>/',views.getCashBookBydate),
    path('bankbookreport/<uuid:comp_id>/<from_date>/<to_date>/',views.getBankBookReportLbydate),
    path('bankbook/<uuid:comp_id>/<uuid:branch_id>/<from_date>/<to_date>/',views.getBankBookBydate),
    
    #Excel Report  and Download excel report 
    
    #Invoice Excel Report creating and Download this excel
    path('InvoiceExcelReport/<uuid:comp_id>/<uuid:branch_id>/<from_date>/<to_date>/',views.InvoiceExcelReport),
    path('Downloadexcel/<str:file_name>',views.download_Inv_Report_Excel),
    #Payment Recived Excel Report creating and Download this excel
    path('PRExcelReport/<uuid:comp_id>/<uuid:branch_id>/<from_date>/<to_date>/',views.PMRecieveExcelReport),
    path('DownloadPRexcel/<str:file_name>',views.download_PR_Report_Excel),
    #Bill Excel Report creating and Download this excel
    path('BillExcelReport/<uuid:comp_id>/<uuid:branch_id>/<from_date>/<to_date>/',views.BillExcelReport),
    path('DownloadBLexcel/<str:file_name>',views.download_Bill_Report_Excel),
    #Payment Made Excel Report creating and Download this excel
    path('PMExcelReport/<uuid:comp_id>/<uuid:branch_id>/<from_date>/<to_date>/',views.PMExcelReport),
    path('DownloadPMexcel/<str:file_name>',views.download_PM_Report_Excel),
    path('dashboard-report/<uuid:company_id>/',DashboardReportView.as_view()),
    path('getitemstockreport/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/', StockValuationReportView.as_view(), name='getitemstockreport'),
]