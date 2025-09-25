# import json
# import os
# import pandas as pd
# import datetime
# from pathlib import Path
# from wsgiref.util import FileWrapper

# from django.template.loader import get_template
# from django.views.generic import View
# from django.http import HttpResponse, FileResponse

# from rest_framework.response import Response
# from rest_framework import viewsets, generics, mixins
# from rest_framework.decorators import api_view

# from . serializers import *
# from .models import *
# from transaction .models import MasterTransaction
# from salescustomer.models import SalesCustomer, TCS
# from transaction .serializers import MasterTransactionSerializer
# from salescustomer .views import render_to_pdf
# from banking .models import VendorAdvanced,Banking,RefundMaster
# from banking .serializers import VendorAdvancedSerializer,DebitNoteRefundSerializer
# from item .models import Stock,Adjustment

# from .generate_bill import generate_bill_pdf
# from .generate_po import generate_po_pdf
# from .generate_dn import generate_dn_pdf
# from .generate_pm import generate_payment_made_pdf
# from .generate_exp import generate_expense_pdf
# from .generate_va import generate_vendor_advance_pdf
# # Vendor
# class companyViewset(viewsets.ModelViewSet):
#     queryset = Vendor.objects.all()
#     serializer_class = CompanySerializer

# # to get the all vendor list


# class vendorList(generics.ListAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorContactSerializer

# # API for Vendor
# # POST


# class vendorViewset(viewsets.ModelViewSet):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer

#     def create(self, request, *args, **kwargs):
#         vendor_data_convert = request.data ['data']
#         print("vendor_data", vendor_data_convert)
        

#         #Convert Str to Dict Code
#         vendor_data = json.loads(vendor_data_convert)
#        # vendor_data = vendor_data_convert
#         vendor_file_data = request.FILES.get('bill_template')
#       #  print("vendor_file_data", type(vendor_file_data))
#         contact_person = vendor_data.get("contact_person")
#         # Vendor fields
#         #comp_id = Company.objects.get(company_id=vendor_data["company_id"])
#         vendor = Vendor.objects.create(salutation=vendor_data["salutation"],
#                                        vendor_name=vendor_data["vendor_name"],
#                                        company_name=vendor_data["company_name"],
#                                        vendor_display_name=vendor_data["vendor_display_name"],
#                                        vendor_contact=vendor_data["vendor_contact"],
#                                        vendor_mobile=vendor_data["vendor_mobile"],
#                                        vendor_email=vendor_data["vendor_email"],
#                                        website=vendor_data["website"],
#                                        vendor_designation=vendor_data["vendor_designation"],
#                                        vendor_department=vendor_data["vendor_department"],
#                                        term_name=vendor_data["term_name"],
#                                        no_of_days=vendor_data["no_of_days"],
#                                        set_credit_limit=vendor_data["set_credit_limit"],
#                                        gst_treatment=vendor_data["gst_treatment"],
#                                        gstin_number=vendor_data["gstin_number"],
#                                        tax_preference=vendor_data["tax_preference"],
#                                        source_place=vendor_data["source_place"],
#                                        exemption_reason=vendor_data["exemption_reason"],
#                                        pan_number=vendor_data["gstin_number"],
#                                        b_attention=vendor_data["b_attention"],
#                                        bill_address1=vendor_data["bill_address1"],
#                                        bill_address2=vendor_data["bill_address2"],
#                                        bill_address_city=vendor_data["bill_address_city"],
#                                        bill_address_state=vendor_data["bill_address_state"],
#                                        bill_address_postal_code=vendor_data["bill_address_postal_code"],
#                                        bill_address_country=vendor_data["bill_address_country"],
#                                        bill_contact_number=vendor_data["bill_contact_number"],
#                                        bill_fax_number=vendor_data["bill_fax_number"],
#                                        s_attention=vendor_data["s_attention"],
#                                        ship_address1=vendor_data["ship_address1"],
#                                        ship_address2=vendor_data["ship_address2"],
#                                        ship_address_city=vendor_data["ship_address_city"],
#                                        ship_address_state=vendor_data["ship_address_state"],
#                                        ship_address_postal_code=vendor_data["ship_address_postal_code"],
#                                        ship_address_country=vendor_data["ship_address_country"],
#                                        ship_contact_number=vendor_data["ship_contact_number"],
#                                        ship_fax_number=vendor_data["ship_fax_number"],
#                                        remarks=vendor_data["remarks"],
#                                        bill_template=vendor_file_data,
                                       
#                                        company_id=Company.objects.get(company_id=vendor_data["company_id"]))
#         vendor.save()
#         print("vendor_added", vendor, type(vendor))
#         if vendor_file_data is not None:
#             file_ext = os.path.splitext(vendor_file_data.name)[1]
#             new_file_path = f'media/Bill_{vendor.vendor_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in vendor_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             vendor.attach_file = pth
#             vendor.save()

       
#             # here vendor is a variable that we taken from above and vendor_id is a
#             contact_person = VendorContact.objects.create(vendor_id=vendor,
#                                                           contact_salutation=vendor_data["contact_salutation"],
#                                                           contact_name=vendor_data["contact_name"],
#                                                           contact_phone=vendor_data["contact_phone"],
#                                                           contact_mobile=vendor_data["contact_mobile"],
#                                                           contact_email=vendor_data["contact_email"],
#                                                           contact_designation=vendor_data["contact_designation"],
#                                                           contact_department=vendor_data["contact_department"])
#             contact_person.save()
#             print("contact_person", contact_person, type(contact_person))

#         serializer = VendorSerializer(vendor)  # browser
#         return Response(serializer.data)

# # Vendor and Contact person join(It will get all records of vendor with contact object)


# class VendorAndContactGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = Vendor.objects.all()
#     serializer_class = allcontactofvendorSerializer

#     def get(self, request, pk=None):
#         if pk:
#             return Response({
#                 'data': self.retrieve(request, pk).data
#             })
#         return self.list(request)

# # to get the all vendor list


# class vendorList(generics.ListAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer

# # get vendor by id


# @api_view(['GET'])
# def vendorDetail(request, pk):
#     vendor = Vendor.objects.get(vendor_id=pk)
#     serializer = allcontactofvendorSerializer(vendor, many=False)
#     return Response(serializer.data)

# # get vendor short by company id


# @api_view(['GET'])
# def vendorshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     vendor = Vendor.objects.filter(company_id=company)
#     serializer = vendorshortbycompanySerializer(vendor, many=True)
#     return Response(serializer.data)

# # getvendorbyname


# @api_view(['GET'])
# def vendorname(request):
#     vendor = Vendor.objects.all()
#     serializer = vendornameSerializer(vendor, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# def vendorUpdate(request, pk):
#     vendor = Vendor.objects.get(vendor_id=pk)
#     serializer = VendorSerializer(instance=vendor, data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['POST'])
# def vendorUpdate(request, pk):
#     vendor = Vendor.objects.get(vendor_id=pk)
#     serializer = VendorSerializer(instance=vendor, data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# ##################################################
# # Dwonload Code Is Creting api By Download
# # Download Bill by id





# class BillGeneratePdf(View):
#     def get(self, request, bill_id, *args, **kwargs):
#         bill = Bill.objects.get(bill_id=bill_id)
#         # Get The Bill By bill id
#         # and Then Serialize the data
#         serializer = BillSerializer(bill)
#         print(serializer.data)
#         # get the Company data In Estimate (company_id) related
#         print(bill.company_id.company_id)
#         company = Company.objects.get(company_id=bill.company_id.company_id)
#         # Serialize the data in Comapny
#         company_serializer = CompanySerializer(company)
#         print("##################################")
#         print(serializer.data)
#         print("##################################")
#         print("Company Data", company_serializer.data)
#         print("##################################")
#         template = get_template('invoice.html')
#         # Create the empty Dictionary in
#         context = dict()
#         # Add the Company and Invoice Data in Dictionary (Means Combine the data)
#         context.update(dict(serializer.data))
#         context.update(dict(company_serializer.data))
#         html = template.render(context)

#         return HttpResponse(html)

# #####################


# class BillDownloadPdf(View):
#     def get(self, request, *args, **kwargs):

#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')

#         filename = "bill_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)

#         # rendering the template

#         with open(pdf_path, 'r') as f:
#             file_data = f.read()

#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response


# ########################################################################################################################
# # Bill and Item join
# class BillItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = Bill.objects.all()
#     serializer_class = JoinBillAndBillItemSerializer

#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'purchase/billfile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)

# # get all bill journal transaction


# class billjournaltransactionList(generics.ListAPIView):
#     queryset = BillJournalTransaction.objects.all()
#     serializer_class = BillJTSerializer

# # get bill journal transaction by bill id


# @api_view(['GET'])  # get details by id
# def billjournaltransactionDetail(request, pk):
#     billjournaltransaction = Bill.objects.get(bill_id=pk)
#     serializer = BilltransactionsSerializer(billjournaltransaction, many=False)
#     return Response(serializer.data)

# # billhortbycompanyid


# @api_view(['GET'])
# def billshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     billshort = Bill.objects.filter(company_id=company)
#  #   serializer = billshortbycompanySerializer(billshort, many=True)
#     serializer = JoinBillAndBillItemSerializer(billshort, many=True)

#     return Response(serializer.data)

# ###############################################################3##########################
# #This Section Is Bill Ref 
 
# @api_view(['GET'])
# def Billrefbyvendorid(request, pk):
#     vendor = Vendor.objects.get(vendor_id=pk)
#     bills=Bill.objects.filter(vendor_id=vendor)
#     print('Bills Is here',bills)
#     response_list=[]
#     for bill in bills:
#         bill_id=bill.bill_id
#         bill_serial=bill.bill_serial
#         vendor_id=bill.vendor_id.vendor_id
   
#         response_dict = {"vendor_id":vendor_id,"bill_id":bill_id,"bill_serial":bill_serial}
#         response_list.append(response_dict)  
#     return Response(response_list)


# # api for get bill by company id and bill id
# @api_view(['GET'])   
# def download_bill_data(request, comp_id,bill_id):
#     company = Company.objects.get(company_id=comp_id)
#     bill = Bill.objects.get(bill_id=bill_id)
#     # here filter the object of bill id and company id
#     bl = Bill.objects.filter(
#         company_id=comp_id,bill_id=bill_id).order_by('created_date')
#     serializers = JoinBillAndBillItemSerializer(bl, many=True)
#     output_pdf=f"Bill_{datetime.datetime.now().timestamp()}.pdf"
#     generate_bill_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/purchase/Downloadbill/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)

# def download_bl(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,                              
#     return response
# ################################################################################




# # get bill by vendor id(Response for this api is its return all invoices as per respective  vendor)


# @api_view(['GET'])
# def billbyvendorid(request, pk):
#     vendor = Vendor.objects.get(vendor=pk)
#     # cust_queryset=Customer.objects.prefetch_related()
#     print('cust_queryset', vendor)
#     # customer=cust_queryset.objects.filter(customer_id=pk)

#     print('vendor', vendor)
#     serializer = billbyvendorSerializer(vendor, many=False)
#     return Response(serializer.data)

# # TDS


# # provision to add data from API by providing HTML form also we can see posted data
# class tdsViewSet(viewsets.ModelViewSet):
#     queryset = TDS.objects.all()
#     serializer_class = tdsSerializer


# class tdsList(generics.ListAPIView):
#     queryset = TDS.objects.all()
#     serializer_class = tdsSerializer

#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def tdsCreation(request):
#         tds = TDS.objects.all()
#         serializer = tdsSerializer(tds, many=True)
#         return Response(serializer.data)


# class PaymentmadeJournalViewsets(viewsets.ModelViewSet):
#     queryset = PaymentMade.objects.all()  # get the Paymentmade Model Data
#     serializer_class = PaymentmadeSerializer

#     # payment made field
#     def create(self, request, *args, **kwargs):
#         paymentmade_data = request.data
#         print('paymentmade_data', paymentmade_data)
#         bill_id = paymentmade_data["unpaindBill"]["bill_id"]
#         bill_amount = paymentmade_data["bill_amount"]
#         print("bill_amount", bill_amount)
#         # bill_id=paymentmade_data["unpainBill"]["bill_id"]
#         print("bill_id", bill_id, type(bill_id))
#         company_id = Company.objects.get(
#             company_id=paymentmade_data["company_id"])
        
        

#         # Payment made field
#         payment_id = PaymentMade.objects.create(payment_date=paymentmade_data["payment_date"],
#                                                 payment_serial=paymentmade_data["payment_serial"],
#                                                 payment_mode=paymentmade_data["payment_mode"],
#                                                 payment_ref_no=paymentmade_data["payment_ref_no"],
#                                                 paid_through=paymentmade_data["paid_through"],
#                                                 amount_payable=paymentmade_data["amount_payable"],
#                                                 bill_date=paymentmade_data["bill_date"],
#                                                 bill_serial=paymentmade_data["bill_serial"],
#                                                 bill_amount=paymentmade_data["bill_amount"],
#                                                 amount_due=paymentmade_data['amount_due'],
#                                                 balance_amount=paymentmade_data['balance_amount'],
#                                                 amount_excess=paymentmade_data['amount_excess'],
#                                                 note=paymentmade_data['note'],
#                                                 vendor_id=Vendor.objects.get(
#             vendor_id=paymentmade_data["vendor_id"]),
#             company_id=Company.objects.get(company_id=paymentmade_data["company_id"]))
#         payment_id.save()
#         print("paymentmade_created", payment_id, type(payment_id))

#         # all the debit entries for payment made as per associated chart of accounts should be added into payment transaction
#         # here account_payable is the the account that already created in chart of account table.
#         #account_payable = COA.objects.get(coa_id='4d6c3ad4-459b-4b7e-9196-394637098b3a')
#         account_payable = COA.objects.get(
#             company_id=company_id, account_subhead='Account Payables')
#         vendor_id = Vendor.objects.get(vendor_id=paymentmade_data["vendor_id"])

# # Commenting By Shubham
# # region This a transaction without Master Transaction
# # This Region is the Credit And Debit Transaction the vlaues are Two rows Added in Database

#         paymentdebittrans = PaymentmadeJournalTransaction.objects.create(pm_id=payment_id,
#                                                                          # here coa_id is coa instance but selected by user as a paid_through account
#                                                                          coa_id=account_payable,
#                                                                          company_id=Company.objects.get(
#                                                                              company_id=paymentmade_data["company_id"]),
#                                                                          debit=paymentmade_data["amount_payable"],
#                                                                          type="Itemized")
#         paymentdebittrans.save()
#         print("paymentmade_data2", paymentdebittrans, type(paymentdebittrans))

#         # here we are going to add a credit entry for accounts payable hence the coa_id for account payable = "c9319c27-b82f-48d9-8033-742bf4ac2fda"
#         # we are using this COA.objects.get method so that we can get the instance of the respective coa as we need to pass instance of the respective coa
#         # account_payable = COA.objects.get(coa_id='4d6c3ad4-459b-4b7e-9196-394637098b3a')
#         account_payable = COA.objects.get(
#             company_id=company_id, account_subhead='Account Payables')
#         paymentmadecredittrans = PaymentmadeJournalTransaction.objects.create(pm_id=payment_id,
#                                                                               company_id=Company.objects.get(
#                                                                                   company_id=paymentmade_data["company_id"]),
#                                                                               coa_id=COA.objects.get(
#                                                                                   coa_id=paymentmade_data["paid_through"]),
#                                                                               credit=paymentmade_data["amount_payable"],
#                                                                               type="Consolidated")
#         paymentmadecredittrans.save()
#         print("paymentmade_items3", paymentmadecredittrans,
#               type(paymentmadecredittrans))
# # endregion
# # region Master Transaction Section
#         company_year_id=paymentmade_data.get("company_year_id")
#         if company_year_id is not None:
#             company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
#         company_id = Company.objects.get(
#             company_id=paymentmade_data["company_id"])
#         From_Bank = COA.objects.get(coa_id=paymentmade_data["paid_through"])
#         pmmast = MasterTransaction.objects.create(
#             L1detail_id=payment_id.pm_id,
#             L1detailstbl_name='Payment Made',
#             L3detail_id=bill_id,
#             L3detailstbl_name='Bill',
#             main_module='Purchase',
#             module='Purchase',
#             sub_module='Payment Made',
#             transc_deatils='Payment Made',
#             banking_module_type='Vendor Payment',
#             journal_module_type='Payment Made',
#             trans_date=paymentmade_data["bill_date"],
#             trans_status='Maually Added',
#             debit=paymentmade_data["amount_payable"],
#             to_account=account_payable.coa_id,
#             to_acc_type=account_payable.account_type,
#             to_acc_head=account_payable.account_head,
#             to_acc_subhead=account_payable.account_subhead,
#             to_acc_name=account_payable.account_name,
#             credit=paymentmade_data['amount_payable'],
#             from_account=From_Bank.coa_id,
#             from_acc_type=From_Bank.account_type,
#             from_acc_head=From_Bank.account_head,
#             from_acc_subhead=From_Bank.account_subhead,
#             from_acc_name=From_Bank.account_name,
#             vendor_id=vendor_id,
#             company_id=company_id)
#         pmmast.save()

# # endregion

#         # for full payment
#         bill_amount = paymentmade_data["bill_amount"]
#         print("bill_amount", bill_amount, type(bill_amount))
#         amount_payable = paymentmade_data["amount_payable"]
#         print("amount_payable", amount_payable, type(amount_payable))

#         # If payment is full then payment status will change unpaid to paid in Bill
#         balance_amount = paymentmade_data["balance_amount"]
#         # if bill_amount == balance_amount:

#         bill_id = Bill.objects.get(
#             bill_id=paymentmade_data["unpaindBill"]["bill_id"])
#         bill_id.amount_due = paymentmade_data["balance_amount"]
#         if balance_amount == 0:
#             bill_id.payment_status = 'paid'
#         bill_id.save()

#         serializer = PaymentmadeSerializer(payment_id)
#         return Response(serializer.data)



# class ExpenseFileDownloadListAPIView(generics.ListAPIView):

#     def get(self, request, er_id, format=None):
#         queryset = ExpenseRecord.objects.get(er_id=er_id)
#         if queryset.attach_file:
#             file_handle = queryset.attach_file.path
#             if os.path.exists(file_handle):
#                 document = open(file_handle, 'rb')
#                 response = HttpResponse(FileWrapper(
#                     document), content_type='application/msword')
#                 response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
#                 return response
#             else:
#                 return HttpResponse("File Not Found")
#         else:
#             return HttpResponse("No File Found")
# #######################################################

# #####################


# class EstimateDownloadPdf(View):
#     def get(self, request, *args, **kwargs):

#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')

#         filename = "estimate_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)

#         # rendering the template

#         with open(pdf_path, 'r') as f:
#             file_data = f.read()

#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response

# #############################################################


# # get all expense record list
# class expenserecordList(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = ExpenseRecord.objects.all()
#     serializer_class = ExpenseRecordSerializer

#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'purchase/expensefile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)

# # get all expense journal transaction


# class expensejournaltransactionList(generics.ListAPIView):
#     queryset = ExpenseRecord.objects.all()
#     serializer_class = ExpenseTransactionSerializer

# # get expense transaction by pr id


# @api_view(['GET'])  # get details by id
# def expensejournaltransactionDetail(request, pk):
#     expensejournaltransaction = ExpenseRecord.objects.get(er_id=pk)
#     serializer = ExpenseTransactionSerializer(
#         expensejournaltransaction, many=False)
#     return Response(serializer.data)

# # expense record short by company id


# @api_view(['GET'])
# def ershortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     expenserecord = ExpenseRecord.objects.filter(company_id=company)
#     serializer =ExpenseRecordSerializer (expenserecord, many=True) # ershortbycompanySerializer
#     return Response(serializer.data)



# # api for get bill by company id and bill id
# @api_view(['GET'])   
# def download_exp_data(request, comp_id,er_id):
#     company = Company.objects.get(company_id=comp_id)
#     expr = ExpenseRecord.objects.get(er_id=er_id)
#     # here filter the object of bill id and company id
#     er = ExpenseRecord.objects.filter(
#         company_id=comp_id,er_id=er_id)
#     serializers = ExpenseTransactionSerializer(er, many=True)#############
#     output_pdf=f"EXP_{datetime.datetime.now().timestamp()}.pdf"
#     generate_expense_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/purchase/Downloadexp/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)

# def download_exp(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,                              
#     return response
# ################################################################################

# @api_view(['GET'])
# def erDetail(request, pk):
#     er = ExpenseRecord.objects.get(er_id=pk)
#     serializer = ExpenseRecordSerializer(er, many=False)

#     return Response(serializer.data)






# class PaymentmadeViewstes(viewsets.ModelViewSet):
#     queryset = PaymentMade.objects.all()
#     serializer_class = PaymentmadeSerializer

# # get all payment made list


# class paymentmadedList(generics.ListAPIView):
#     queryset = PaymentMade.objects.all()
#     serializer_class = PaymentmadeSerializer

# # get Paymentmadebyid


# @api_view(['GET'])
# def getpaymentmade(request, pk):
#     instance = PaymentMade.objects.get(pk=pk)
#     serializer = PaymentmadeSerializer(instance)
#     return Response(serializer.data)

# # get PaymentmadebyJournaltrasctionbyid


# @api_view(['GET'])
# def getpaymentmadejournaltrasctionbyid(request, pk):
#     instance = PaymentMade.objects.get(pk=pk)
#     serializer = PaymentmadeAllSerializer(instance)
#     return Response(serializer.data)

# # get payment made short by company id


# @api_view(['GET'])
# def getpaymentmadeshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     # here if we use wrong object(company) then it will shows null values for all fields
#     paymentmade = PaymentMade.objects.filter(company_id=company)
#     serializer = paymentmadeshortbycompanySerializer(paymentmade, many=True)
#     return Response(serializer.data)

# # get bill by vendor id(Response for this api is its return all bill as per respective  vendor)

# ###############################################################3##########################



# # api for get bill by company id and bill id
# @api_view(['GET'])   
# def download_pm_data(request, comp_id,pm_id):
#     company = Company.objects.get(company_id=comp_id)
#     pay= PaymentMade.objects.get(pm_id=pm_id)
#     # here filter the object of bill id and company id
#     paymt = PaymentMade.objects.filter(
#         company_id=comp_id,pm_id=pm_id).order_by('created_date')
#     serializers = paymentmadeshortbycompanySerializer(paymt, many=True)
#     output_pdf=f"PM_{datetime.datetime.now().timestamp()}.pdf"
#     generate_payment_made_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/purchase/Downloadpm/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)

# def download_pm(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,                              
#     return response
# ################################################################################

# @api_view(['GET'])
# def billbyvendorid(request, pk):
#     vendor = Vendor.objects.get(vendor_id=pk)
#     print('vendor', vendor)
#     serializer = BillbyVendorSerializer(vendor, many=False)
#     return Response(serializer.data)

# # POST Purchase Order Item


# class purchaseorderitemsViewSet(viewsets.ModelViewSet):
#     queryset = PoItem.objects.all()
#     serializer_class = PoItemSerializer

#     def create(self, request, *args, **kwargs):
#         po_data_converte = request.data['data']

#         print("#################################################")
#         print(po_data_converte)
#         print("Purchase order Data Format is ", type(po_data_converte))
#         print("#################################################")
#         # Purchase Convert Str to Dict Code
#         po_data = json.loads(po_data_converte)
#         print("Converted Format is", type(po_data))

#         po_file_data = request.FILES.get('attach_file')
#         print("purchaseorder_data", type(po_file_data))

#         # cust_id=po_data["customer_id"]
#         # if cust_id is not None:
#         #     cust_id=SalesCustomer.objects.get(customer_id=cust_id)

#         Branch_id = po_data["branch_id"]
#         if Branch_id is not None:
#             Branch_id = Branch.objects.get(branch_id=Branch_id)

#         vn_id = po_data["vendor_id"]
#         if vn_id is not None:
#             vn_id = Vendor.objects.get(vendor_id=vn_id)

        
#         company_year_id=po_data.get("company_year_id")
#         if company_year_id is not None:
#             company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        
#         try:    
#             tcs_id = po_data["tcs_id"]
#             if tcs_id is not None:
#                 tcs_id = TCS.objects.get(tcs_id=tcs_id)
#         except KeyError:
#             tcs_id=None

#         po_items = po_data["po_items"]
#         comp_id = Company.objects.get(company_id=po_data["company_id"])
#         #branch_id = Branch.objects.get(branch_id=estimate_data["branch_id"])
#         #cust_id = Customer.objects.get(customer_id=po_data["customer_id"])

#         # Purchaseorder Fields
#         po_id = PO.objects.create(po_date=po_data["po_date"],
#                                   po_status=po_data["po_status"],
#                                   po_serial=po_data["po_serial"],
#                                   po_ref_no=po_data["po_ref_no"],
#                                   is_po_generated=po_data["is_po_generated"],
#                                   # bill_status=po_data["bill_status"],
#                                   # po_amount=po_data["po_amount"],
#                                   tcs_amount=po_data["tcs_amount"],
#                                   supply_place=po_data["supply_place"],
#                                   destination_place=po_data["destination_place"],
#                                   term_name=po_data["term_name"],
#                                   no_of_days=po_data["no_of_days"],
#                                   shipment_preference=po_data["shipment_preference"],
#                                   discount_type=po_data["discount_type"],
#                                   sub_total=po_data["sub_total"],
#                                   total=po_data["total"],
#                                   sgst_total=po_data["sgst_total"],
#                                   cgst_total=po_data["cgst_total"],
#                                   igst_total=po_data["igst_total"],
#                                   discount=po_data["discount"],
#                                   entered_discount=po_data["entered_discount"],
#                                   customer_note=po_data["customer_note"],
#                                   terms_condition=po_data["terms_condition"],
#                                   # vendor_id=Vendor.objects.get(vendor_id=po_data["vendor_id"]),
#                                   # branch_id=Branch.objects.get(branch_id=po_data["branch_id"]),
#                                   # tcs_id=TCS.objects.get(tcs_id=po_data["tcs_id"]),
#                                   # customer_id=Customer.objects.get(customer=po_data["customer_id"]),
#                                   # company_id=Company.objects.get(company_id=po_data["company_id"]),
#                                   expected_delivery_date=po_data["expected_delivery_date"],
#                                   # customer_id=cust_id,
#                                   company_id=comp_id,
#                                   branch_id=Branch_id,
#                                   vendor_id=vn_id,
#                                   attach_file=po_file_data,
#                                   tcs_id=tcs_id)
#         po_id.save()
#         if po_file_data is not None:
#             file_ext = os.path.splitext(po_file_data.name)[1]
#             new_file_path = f'media/PO_{po_id.po_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in po_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             po_id.attach_file = pth
#             po_id.save()
#         print("po_created", po_id, type(po_id))

#         for i in range(len(po_items)):
#             purchase_items = PoItem.objects.create(po_id=po_id,
#                                                    item_id=Item.objects.get(
#                                                        item_id=po_items[i]["item_id"]),
#                                                    coa_id=COA.objects.get(
#                                                        coa_id=po_items[i]["coa_id"]),
#                                                    # customer_id=SalesCustomer.objects.get(customer_id=po_items[i]["customer_id"]),
#                                                    item_name=po_items[i]["item_name"],
#                                                    rate=po_items[i]["rate"],
#                                                    quantity=po_items[i]["quantity"],
#                                                    tax_rate=po_items[i]["tax_rate"],
#                                                    tax_name=po_items[i]["tax_name"],
#                                                    tax_type=po_items[i]["tax_type"],
#                                                    taxamount=po_items[i]["taxamount"],
#                                                    discount=po_items[i]["discount"],
#                                                    sgst_amount=po_items[i]["sgst_amount"],
#                                                    igst_amount=po_items[i]["igst_amount"],
#                                                    cgst_amount=po_items[i]["cgst_amount"],
#                                                    amount=po_items[i]["amount"])
#             purchase_items.save()
#             print("purchase_items", purchase_items, type(purchase_items))
#         serializer = PoItemSerializer(po_id)  # browser
#         return Response(serializer.data)


# ##################################################
# # Dwonload Code Is Creting api By Download
# # Download Purchase Order by id

# class POFileDownloadListAPIView(generics.ListAPIView):

#     def get(self, request, purchaseorder_id, format=None):
#         queryset = PO.objects.get(po_id=purchaseorder_id)
#         if queryset.attach_file:
#             file_handle = queryset.attach_file.path
#             if os.path.exists(file_handle):
#                 document = open(file_handle, 'rb')
#                 response = HttpResponse(FileWrapper(
#                     document), content_type='application/msword')
#                 response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
#                 return response
#             else:
#                 return HttpResponse("File Not Found")
#         else:
#             return HttpResponse("No File Found")
# #######################################################


# class POGeneratePdf(View):
#     def get(self, request, purchaseoreder_id, *args, **kwargs):
#         purchaseorder = PO.objects.get(po_id=purchaseoreder_id)
#         # Get The Purchase Order By purchaseoreder_id
#         # and Then Serialize the data
#         serializer = POSerializer(purchaseorder)
#         print(serializer.data)
#         # get the Company data In Purchaser Oreder (company_id) related
#         print(purchaseorder.company_id.company_id)
#         company = Company.objects.get(
#             company_id=purchaseorder.company_id.company_id)
#         # Serialize the data in Comapny
#         company_serializer = CompanySerializer(company)
#         print("##################################")
#         print(serializer.data)
#         print("##################################")
#         print("Company Data", company_serializer.data)
#         print("##################################")
#         template = get_template('invoice.html')
#         # Create the empty Dictionary in
#         context = dict()
#         # Add the Company and Invoice Data in Dictionary (Means Combine the data)
#         context.update(dict(serializer.data))
#         context.update(dict(company_serializer.data))
#         html = template.render(context)

#         return HttpResponse(html)

# #####################


# class PODownloadPdf(View):
#     def get(self, request, *args, **kwargs):

#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')

#         filename = "po_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)

#         # rendering the template

#         with open(pdf_path, 'r') as f:
#             file_data = f.read()

#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response


# ##########################################################################################################
# class poViewSet(viewsets.ModelViewSet):
#     queryset = PO.objects.all()
#     serializer_class = POSerializer


# class poList(generics.ListAPIView):
#     queryset = PO.objects.all()
#     serializer_class = POSerializer

#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def poCreation(request):
#         po = PO.objects.all()
#         serializer = POSerializer(po, many=True)
#         return Response(serializer.data)

# # #getshortDetails
# # @api_view(['GET'])
# # def ShortPurchaseOrderDetails(request):
# #     po = PO.objects.all()
# #     serializer = ShortPurchaseOrderSerializer(po, many=True)
# #     return Response(serializer.data)


# @api_view(['GET'])
# def getpurchaseordershortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     # here if we use wrong object(company) then it will shows null values for all fields
#     po = PO.objects.filter(company_id=company)
#     serializer = purchaseordershortbycompanySerializer(po, many=True) # 
#     return Response(serializer.data)


# # api for get bill by company id and bill id
# @api_view(['GET'])   
# def download_po_data(request, comp_id,po_id):
#     company = Company.objects.get(company_id=comp_id)
#     po = PO.objects.get(po_id=po_id)
#     # here filter the object of bill id and company id
#     purchaseo = PO.objects.filter(
#         company_id=comp_id,po_id=po_id).order_by('created_date')
#     serializers = JoinPoItemSerializer(purchaseo, many=True)
#     output_pdf=f"PO_{datetime.datetime.now().timestamp()}.pdf"
#     generate_po_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/purchase/Downloadpo/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)

# def download_po(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,                              
#     return response
# ################################################################################


# class poitemViewSet(viewsets.ModelViewSet):
#     queryset = PoItem.objects.all()
#     serializer_class = PoItemSerializer


# class poitemList(generics.ListAPIView):
#     queryset = PoItem.objects.all()
#     serializer_class = PoItemSerializer

#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def poitemCreation(request):
#         poitem = PoItem.objects.all()
#         serializer = PoItemSerializer(poitem, many=True)
#         return Response(serializer.data)

# # Poitem and PO join


# class PoItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = PO.objects.all()
#     serializer_class = JoinPoItemSerializer

#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'purchase/purchaseorderfile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)

# ##################################################
# # Dwonload Code Is Creting api By Download
# # Download Debitnote by id


# class DebitnoteFileDownloadListAPIView(generics.ListAPIView):

#     def get(self, request, debitnote_id, format=None):
#         queryset = DebitNote.objects.get(dn_id=debitnote_id)
#         if queryset.attach_file:
#             file_handle = queryset.attach_file.path
#             if os.path.exists(file_handle):
#                 document = open(file_handle, 'rb')
#                 response = HttpResponse(FileWrapper(
#                     document), content_type='application/msword')
#                 response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
#                 return response
#             else:
#                 return HttpResponse("File Not Found")
#         else:
#             return HttpResponse("No File Found")

# #######################################################


# class DebitnoteGeneratePdf(View):
#     def get(self, request, debitnote_id, *args, **kwargs):
#         debitnote = DebitNote.objects.get(dn_id=debitnote_id)
#         # Get The Debitnote By debitnote id
#         # and Then Serialize the data
#         serializer = DebitnoteSerializer(debitnote)
#         print(serializer.data)
#         # get the Company data In Debitnote (company_id) related
#         print(debitnote.company_id.company_id)
#         company = Company.objects.get(
#             company_id=debitnote.company_id.company_id)
#         # Serialize the data in Comapny
#         company_serializer = CompanySerializer(company)
#         print("##################################")
#         print(serializer.data)
#         print("##################################")
#         print("Company Data", company_serializer.data)
#         print("##################################")
#         template = get_template('invoice.html')
#         # Create the empty Dictionary in
#         context = dict()
#         # Add the Company and Invoice Data in Dictionary (Means Combine the data)
#         context.update(dict(serializer.data))
#         context.update(dict(company_serializer.data))
#         html = template.render(context)

#         return HttpResponse(html)

# #####################


# class DebitnoteDownloadPdf(View):
#     def get(self, request, *args, **kwargs):

#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')

#         filename = "debitnote_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)

#         # rendering the template

#         with open(pdf_path, 'r') as f:
#             file_data = f.read()

#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response

# #############################################################

# # get credit note journal transaction details by cn id


# @api_view(['GET'])
# def debitnotejournaltransactionDetail(request, pk):
#     debitnotejournaltransaction = DebitNote.objects.get(dn_id=pk)
#     serializer = dntransactionsSerializer(
#         debitnotejournaltransaction, many=False)
#     return Response(serializer.data)


# @api_view(['GET'])
# def debitnoteDetail(request, pk):
#     debitnote = DebitNote.objects.get(id=pk)
#     serializer = DebitnoteSerializer(debitnote, many=False)
#     return Response(serializer.data)


# @api_view(['POST'])
# def debitnoteUpdate(request, pk):
#     debitnote = DebitNote.objects.get(dn_id=pk)
#     serializer = DebitnoteSerializer(instance=debitnote, data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# # dnshortbycompanyid


# @api_view(['GET'])
# def dnshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     dn = DebitNote.objects.filter(company_id=company)
#     serializer = ShortDebitNoteSerializer(dn, many=True)  #JoinDebitNoteItemSerializer  
#     return Response(serializer.data)




# # api for get bill by company id and bill id
# @api_view(['GET'])   
# def download_dn_data(request, comp_id,dn_id):
#     company = Company.objects.get(company_id=comp_id)
#     dn = DebitNote.objects.get(dn_id=dn_id)
#     # here filter the object of bill id and company id
#     dnnote = DebitNote.objects.filter(
#         company_id=comp_id,dn_id=dn_id).order_by('created_date')
#     output_pdf=f"DN_{datetime.datetime.now().timestamp()}.pdf"
#     serializers = JoinDebitNoteItemSerializer(dnnote, many=True)
#     print("**************************",serializers.data)
#     generate_dn_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/purchase/Downloaddn/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)

# def download_dn(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,                              
#     return response
# ################################################################################


# class DebitNoteItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = DebitNote.objects.all()
#     serializer_class = JoinDebitNoteItemSerializer

#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'purchase/debitnotefile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)




# #Bill Post Section 
# #region
# #Creating the Bill Section There Are 3 to 4 Section Main Bill ,Bill Item ,Stock
# #Mastertransaction

# class new3billitemsViewSet(viewsets.ModelViewSet):
#     queryset = Bill_Item.objects.all()
#     serializer_class = BillItemSerializer

#     def create(self, request, *args, **kwargs):
#         bill_data_converte = request.data['data']

      
       
#         # Bill Convert Str to Dict Code
#         bill_data = json.loads(bill_data_converte)
#         #bill_data=bill_data_converte
#         bill_file_data = request.FILES.get('attach_file')
       

     
#         TCS_id = bill_data.get("tcs_id")
#         if TCS_id is not None:
#             TCS_id = TCS.objects.get(tcs_id=TCS_id)

#         TDS_id = bill_data.get("tds_id")
#         if TDS_id is not None:
#             TDS_id = TDS.objects.get(tds_id=TDS_id)
            
#         company_year_id=bill_data.get("company_year_id")
#         if company_year_id is not None:
#             company_year_id=Company_Year.objects.get(company_year_id=company_year_id)    
            
#         comp_id = bill_data["company_id"]
#         if comp_id is not None:
#             comp_id = Company.objects.get(company_id=comp_id)  
            
            
            
#         ven_id = bill_data["vendor_id"]
#         if ven_id is not None:
#             ven_id = Vendor.objects.get(vendor_id=ven_id)
      
#         # Branch_id=invoice_data["branch_id"]
#         # if Branch_id is not None:
#         #     Branch_id=Branch.objects.get(branch_id=Branch_id)

#         bill_items = bill_data["bill_items"]

#         # Bill Fields
#         bill_id = Bill.objects.create(bill_date=bill_data["bill_date"],
#                                       bill_status=bill_data["bill_status"],
#                                       bill_serial=bill_data["bill_serial"],
#                                       is_bill_generate=bill_data["is_bill_generated"],
#                                       order_no=bill_data["order_no"],
#                                       due_date=bill_data["due_date"],
#                                       discount=bill_data["discount"],
#                                       discount_type=bill_data["discount_type"],
#                                       tax_Type=bill_data["tax_Type"],
#                                       amount_due=bill_data["total"],
#                                       attach_file=bill_file_data,
#                                       supply_place=bill_data["supply_place"],
#                                       payment_status=bill_data["payment_status"],
#                                       sub_total=bill_data["sub_total"],
#                                       total=bill_data["total"],
#                                       notes=bill_data['notes'],
#                                       tcs_amount=bill_data["tcs_amount"],
#                                       tds_amount=bill_data["tds_amount"],
#                                       cgst_total=bill_data["cgst_total"],
#                                       sgst_total=bill_data["sgst_total"],
#                                       igst_total=bill_data["igst_total"],
#                                       total_quantity=bill_data["total_quantity"],
#                                       entered_discount=bill_data["entered_discount"],
#                                       discount_account=bill_data["discount_account"],
#                                       term_name=bill_data["term_name"],
#                                       tcs_id=TCS_id,
#                                       tds_id=TDS_id,
#                                       no_of_days=bill_data["no_of_days"],
#                                       company_id=comp_id,
#                                       vendor_id=ven_id)
#         bill_id.save()
#         if bill_file_data is not None:
#             file_ext = os.path.splitext(bill_file_data.name)[1]
#             new_file_path = f'media/Bill_{bill_id.bill_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in bill_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             bill_id.attach_file = pth
#             bill_id.save()
#         account_payable = COA.objects.get(company_id=comp_id, account_subhead='Account Payables')
#         for items in bill_data["bill_items"]:
#             # Created the bill items entries.for one bill many items to be created.
#             billed_items = Bill_Item.objects.create(bill_id=bill_id,
#                                                     item_id=Item.objects.get(
#                                                         item_id=items["item_id"]),
#                                                     coa_id=COA.objects.get(
#                                                         coa_id=items["coa_id"]),
#                                                     #customer_id = SalesCustomer.objects.get(customer_id=bill_items[i]["customer_id"]),
#                                                     item_name=items["item_name"],
#                                                     rate=items["rate"],
#                                                     quantity=items["quantity"],
#                                                     tax_rate=items["tax_rate"],
#                                                     tax_name=items["tax_name"],
#                                                     tax_type=items["tax_type"],
#                                                     cgst_amount=items["cgst_amount"],
#                                                     sgst_amount=items["sgst_amount"],
#                                                     igst_amount=items["igst_amount"],
#                                                     discount=items["discount"],
#                                                     amount=items["amount"])
#             billed_items.save()
#             print("bill_items1", billed_items, type(billed_items))
            
#             #This Section is Stock Main Section 
#             #All The Value Save In Stock Table Section
#             #The Sales Stock Value To Be Decrease means Stock Out field be 
#             items_inventory=bill_data.get('bill_items')
#             track_inventory=items_inventory[0].get('selected_item_name',{}).get('track_inventory')
#             coa=items_inventory[0].get('coa_id')
#             amount=items_inventory[0].get('amount')
#             item_value=Item.objects.get(item_id=items["item_id"])
#             print('Item is herer',item_value)
#             try:
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                 current_stock_amount=current_assets_last_stock.amount
                
#             except Stock.DoesNotExist:
#                 current_stock_amount=0
                
                
#             print('inventory',coa)
#             if track_inventory==True:
                
               
                
#                 stock_items=Stock.objects.create(
#                     item_id=items['item_id'],
#                     item_name=items["item_name"],
#                     stock_in=items["quantity"],
#                     amount=current_stock_amount+(items["quantity"] * items["rate"]),
#                     rate= items["rate"],
#                     quantity=items["quantity"],
                   
#                     ref_id=bill_id.bill_id,
#                     ref_tblname='Bill',
#                     module='Purchase',
#                     formname='Bill',
#                     stage='Add Stages',
#                     date=bill_data["bill_date"],               
#                     company_id=comp_id)
    
#             #This Section Is Stock Journal Transaction 
#             #Stock Charetd Account name is Inventory Assets
#                 # if track_inventory == True:    
#                 TO_COA = COA.objects.get(company_id=comp_id,account_name='Inventory Assets')
#                 print('item rate',stock_items.rate)
#                 print('item quantity',stock_items.quantity)
#                 stkmast = MasterTransaction.objects.create(
#                     L1detail_id=bill_id.bill_id,
#                     L1detailstbl_name='Bill',
#                     L2detail_id=stock_items.st_id,
#                     L2detailstbl_name='Stock',
#                     main_module='Purchase',
#                     module='Bill',
#                     sub_module='Bill',
#                     transc_deatils='Bill',
#                     banking_module_type='Bill',
#                     journal_module_type='Bill',
#                     trans_date=bill_data["bill_date"],
#                     trans_status='Manually Added',
#                     debit=stock_items.rate*stock_items.quantity,
#                     to_account=TO_COA.coa_id,
#                     to_acc_type=TO_COA.account_type,
#                     to_acc_head=TO_COA.account_head,
#                     to_acc_subhead=TO_COA.account_subhead,
#                     to_acc_name=TO_COA.account_name,
#                     credit=stock_items.rate*stock_items.quantity,
#                     from_account=account_payable.coa_id,
#                     from_acc_type=account_payable.account_type,
#                     from_acc_head=account_payable.account_head,
#                     from_acc_subhead=account_payable.account_subhead,
#                     from_acc_name=account_payable.account_name,
#                     company_id=comp_id,
#                     vendor_id=ven_id)
#                 stkmast.save()

#             else:
            
#                 TO_COA = COA.objects.get(coa_id=coa)
#                 #FROM_COA = COA.objects.get(company_id=comp_id,coa_id=purchase_account)
#                 billmast = MasterTransaction.objects.create(
#                     L1detail_id=bill_id.bill_id,
#                     L1detailstbl_name='Bill',
#                     # L2detail_id=L2detail_id,
#                     # L2detailstbl_name=L2detailstbl_name,
#                     main_module='Purchase',
#                     module='Bill',
#                     sub_module='Bill',
#                     transc_deatils='Bill',
#                     banking_module_type='Bill',
#                     journal_module_type='Bill',
#                     trans_date=bill_data["bill_date"],
#                     trans_status='Manually Added',
#                     debit=amount,
#                     to_account=account_payable.coa_id,
#                     to_acc_type=account_payable.account_type,
#                     to_acc_head=account_payable.account_head,
#                     to_acc_subhead=account_payable.account_subhead,
#                     to_acc_name=account_payable.account_name,
#                     credit=amount,
#                     from_account=TO_COA.coa_id,
#                     from_acc_type=TO_COA.account_type,
#                     from_acc_head=TO_COA.account_head,
#                     from_acc_subhead=TO_COA.account_subhead,
#                     from_acc_name=TO_COA.account_name,
#                     vendor_id=ven_id,
#                     company_id=comp_id)
#                 billmast.save() 
                
#         try:    
#             # 0%GST and 0%IGST Calculation
#             #0 % Taxtion Is the UserSelection User Can Select the 0% Tax This 0 is Added the Tax Section
#             Zero_tax=bill_data.get('bill_items')
#             GST_TAX=None
#             if GST_TAX==Zero_tax[0] is not None:
#                 GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
#             else:
#                 pass
#         except:AttributeError
        
            
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX   
#         else:
#             Both_Tax=None
           
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
#             print('no')
#         # User Can the Send the data in request the this data added in this empty list and 
#         #this list can perform the operation 
#         # all the values are not equal to zero the added the list
#         #list added item to add the master transaction table
#         #chnges of this transaction debit credit and to from account
        
       
#         bill_data['tds_amount']=abs(float(bill_data['tds_amount']))
#         transaction_list = [] #This Empty List added the append 
#         if float(bill_data['cgst_total'])>0  or Both_Tax:
#             transaction_list.append(["Input CGST", "cgst_total"],)
#         if float(bill_data['sgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Input SGST", "sgst_total"])
#         if float(bill_data['igst_total']) >0 or IGST_0:
#             transaction_list.append(["Input IGST", "igst_total"],)            
#         if float(bill_data['tcs_amount'])>0:
#             transaction_list.append(["TCS Receivable", "tcs_amount"],)     
#         for transaction in transaction_list:
#             print(transaction)
#             #List Of index added 0 is get Account_name
#             TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#             print('""""""""""""', TO_COA)
#             billmast = MasterTransaction.objects.create(
#                 L1detail_id=bill_id.bill_id,
#                 L1detailstbl_name='Bill',
#                 main_module='Purchase',
#                 module='Bill',
#                 sub_module='Bill',
#                 transc_deatils='Bill',
#                 banking_module_type='Bill',
#                 journal_module_type='Bill',
#                 trans_date=bill_data["bill_date"],
#                 trans_status='Manually Added',
#                 debit=bill_data[transaction[1]],
#                 to_account=TO_COA.coa_id,
#                 to_acc_type=TO_COA.account_type,
#                 to_acc_head=TO_COA.account_head,
#                 to_acc_subhead=TO_COA.account_subhead,
#                 to_acc_name=TO_COA.account_name,
#                 credit=bill_data[transaction[1]],
#                 from_account=account_payable.coa_id,
#                 from_acc_type=account_payable.account_type,
#                 from_acc_head=account_payable.account_head,
#                 from_acc_subhead=account_payable.account_subhead,
#                 from_acc_name=account_payable.account_name,
#                 vendor_id=ven_id,
#                 company_id=comp_id)
#             billmast.save()

#         # This TDS Section
#         transaction_list_tds=[]
#         #Tds View Section tds diff tcs is to Account and From Account is Diffrance
#         if float(bill_data['tds_amount'])>0:
#             transaction_list_tds.append(["TDS Payable", "tds_amount"],)
#         for transaction in transaction_list_tds:
#             print(transaction)
#             #List Of index added 0 is get Account_name
#             TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#             print('""""""""""""', TO_COA)
#             billmast = MasterTransaction.objects.create(
#                 L1detail_id=bill_id.bill_id,
#                 L1detailstbl_name='Bill',
#                 main_module='Purchase',
#                 module='Bill',
#                 sub_module='Bill',
#                 transc_deatils='Bill',
#                 banking_module_type='Bill',
#                 journal_module_type='Bill',
#                 trans_date=bill_data["bill_date"],
#                 trans_status='Manually Added',
#                 debit=bill_data[transaction[1]],
#                 to_account=account_payable.coa_id,
#                 to_acc_type=account_payable.account_type,
#                 to_acc_head=account_payable.account_head,
#                 to_acc_subhead=account_payable.account_subhead,
#                 to_acc_name=account_payable.account_name,
#                 credit=bill_data[transaction[1]],
#                 from_account=TO_COA.coa_id,
#                 from_acc_type=TO_COA.account_type,
#                 from_acc_head=TO_COA.account_head,
#                 from_acc_subhead=TO_COA.account_subhead,
#                 from_acc_name=TO_COA.account_name,
#                 vendor_id=ven_id,
#                 company_id=comp_id)
#             billmast.save()


            
#         # Group By Bill item
#         #Multiple item Send the request Group the coa_id 
#         # Bill item Transaction Changes is the Sum of all Item
#         #All The Transaction Sum is Store Credit and Debit Side
        
#         coa_amount_dict = {}
#         for bill_item in bill_items:
            
#             print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
#             print(type(bill_item))
#             if coa_amount_dict.get(bill_item['coa_id']) is None:
#                 coa_amount_dict[bill_item['coa_id']
#                                 ] = bill_item['amount']
#             else:
#                 coa_amount_dict[bill_item['coa_id']] = coa_amount_dict[bill_item['coa_id']] + bill_item['amount']

#         # Loop through each unique coa_id
#         for coa_id, amount in coa_amount_dict.items():
#             # Stock Journal Transaction
#             #The Stock Is Enable To replace the chart off Account Inventory
#             #the Sotck is Disable the no any account has replace to main section
            
            
#             stkbill_item=bill_data.get('bill_items')
#             purchase_account=stkbill_item[0].get('selected_item_name').get('purchase_account')
                        
#         #user selected discount this code will be executed
#         #get the COA Table discount Account 
#         if bill_data['discount']>0:  
#             discount_account=bill_data['discount_account']
#             TO_COA = COA.objects.get(coa_id=account_payable.coa_id)
#             account_payable =COA.objects.get(company_id=comp_id, coa_id=discount_account)
#             print('Discount Account is',discount_account,type(discount_account))
            

#             print('""""""""""""', TO_COA)
#             billmast = MasterTransaction.objects.create(
#                 L1detail_id=bill_id.bill_id,
#                 L1detailstbl_name='Bill',
#                 main_module='Purchase',
#                 module='Bill',
#                 sub_module='Bill',
#                 transc_deatils='Bill',
#                 banking_module_type='Bill',
#                 journal_module_type='Bill',
#                 trans_date=bill_data["bill_date"],
#                 trans_status='Manually Added',
#                 debit=bill_data['discount'],
#                 to_account=TO_COA.coa_id,
#                 to_acc_type=TO_COA.account_type,
#                 to_acc_head=TO_COA.account_head,
#                 to_acc_subhead=TO_COA.account_subhead,
#                 to_acc_name=TO_COA.account_name,
#                 credit=bill_data['discount'],
#                 from_account=account_payable.coa_id,
#                 from_acc_type=account_payable.account_type,
#                 from_acc_head=account_payable.account_head,
#                 from_acc_subhead=account_payable.account_subhead,
#                 from_acc_name=account_payable.account_name,
#                 vendor_id=ven_id,
#                 company_id=comp_id)
#             billmast.save()
#         serializer = BillSerializer(bill_id)  # browser
#         return Response(serializer.data)
        
# #endregion
# #End Bill Section        



# #Debit Note Section
# #region

# class new3DebitnoteItemViewSet(viewsets.ModelViewSet):
#     queryset = DebitNote.objects.all()
#     serializer_class = DebitnoteSerializer

#     # here is the entry for dabit note
#     def create(self, request, *args, **kwargs):
#         dn_data_converte = request.data['data']

      
#         # Debitnote Convert Str to Dict Code
#         debitnote_data = json.loads(dn_data_converte)
#        # debitnote_data=dn_data_converte
#         debit_note_items = debitnote_data["debit_note_items"]
#         print("Hjerrrrrrrrrrrrrrrrrrrrrrrrr",debit_note_items)
        
#         vendor_id = debitnote_data["vendor_id"]
#         if vendor_id is not None:
#             vendor_id = Vendor.objects.get(vendor_id=vendor_id)  
            
            
#         comp_id = debitnote_data["company_id"]
#         if comp_id is not None:
#             comp_id = Company.objects.get(company_id=comp_id)
            
#         company_year_id=debitnote_data.get("company_year_id")
#         if company_year_id is not None:
#             company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
    
#         bill_id=debitnote_data.get("bill_id")
#         if bill_id is not None:
#             bill_id=Bill.objects.get(bill_id=bill_id)

#         # debit note fields
#         debitnote_id = DebitNote.objects.create(dn_date=debitnote_data["dn_date"],
#                                                 dn_serial=debitnote_data["dn_serial"],
#                                                 is_dn_generated=debitnote_data["is_dn_generated"],
#                                                 bill_serial=bill_id.bill_serial,
#                                                 bill_id=bill_id,
#                                                 order_no=debitnote_data["order_no"],
#                                                 bill_type=debitnote_data["bill_type"],
#                                                 dn_status=debitnote_data["dn_status"],
#                                                 status=debitnote_data["status"],
#                                                 vendor_id=vendor_id,
#                                                 source_place=debitnote_data["source_place"],
#                                                 supply_destination=debitnote_data["supply_destination"],
#                                                 sub_total=debitnote_data["sub_total"],
#                                                 total=debitnote_data["total"],
#                                                 cgst_total=debitnote_data["cgst_total"],
#                                                 igst_total=debitnote_data["igst_total"],
#                                                 sgst_total=debitnote_data["sgst_total"],
#                                                 balance_amount=debitnote_data["total"],
#                                                 entered_discount=debitnote_data["entered_discount"],
#                                                 discount=debitnote_data["discount"],
#                                                 discount_account=debitnote_data['discount_account'],
#                                                 company_id=comp_id,
#                                                 note=debitnote_data["note"])
#         # debitnote_id.save()

#         # Save files
        
#         dn_file_data = request.FILES.get('attach_file')
#         print("debitnote_data", type(dn_file_data))

#         if dn_file_data is not None:
#             file_ext = os.path.splitext(dn_file_data.name)[1]
#             new_file_path = f'media/Debitnote_{debitnote_id.dn_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in dn_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             debitnote_id.attach_file = pth
#             debitnote_id.save()
#         print("debitnote_created", debitnote_id, type(debitnote_id))
#         #chart of account is get the Account Payables
#         account_payable = COA.objects.get(company_id=comp_id, account_subhead='Account Payables')
        
#         for item in debitnote_data['debit_note_items']:
#             # Created the debitnote items entries. for one debitnote many items to be created.
#             debitnoteed_items = DebitItem.objects.create(dn_id=debitnote_id,
#                                                          item_id=Item.objects.get(
#                                                              item_id=item["item_id"]),
#                                                          coa_id=COA.objects.get(
#                                                              coa_id=item["coa_id"]),
#                                                          item_name=item["item_name"],
#                                                          rate=item["rate"],
#                                                          quantity=item["quantity"],
#                                                          tax_rate=item["tax_rate"],
#                                                          tax_name=item["tax_name"],
#                                                          tax_type=item["tax_type"],
#                                                          taxamount=item["taxamount"],
#                                                          igst_amount=item['igst_amount'],
#                                                          cgst_amount=item['cgst_amount'],
#                                                          sgst_amount=item['sgst_amount'],
#                                                          amount=item["amount"])
            
            
            
            
#             # Find all the unique coa_id and calculate their sum of amounts
                    
            
            
            
            
#             #This Section is Stock Main Section 
#             #All The Value Save In Stock Table Section
#             #The Sales Stock Value To Be Decrease means Stock Out field be
#             item_value=Item.objects.get(item_id=item["item_id"])
#             items_inventory=debitnote_data.get('debit_note_items')
#             track_inventory=items_inventory[0].get('selected_item_name',{}).get('track_inventory')
#             inv_item_coa=items_inventory[0].get('selected_item_name',{}).get('inventory_account')
            
#             print('inventory item coa',inv_item_coa)
                    
#             if track_inventory==True:
                
       
#                 stk_in=Stock.objects.filter(item_id=item["item_id"]).exclude(stock_in=0).order_by('created_date')
#                 stk_out=Stock.objects.filter(item_id=item["item_id"]).exclude(stock_out=0).order_by('created_date')        
              
#                 print(stk_out)
#                 stock_int_items = stk_in
#                 already_stock_out_items =stk_out
#                 item_to_sell = item["quantity"]
#                 print('item_to_sell',item_to_sell)

#                 # -------------------------------------------------

#                 # Check if the stock is available
#                 sum_of_stock_in = sum([_.stock_in for _ in stock_int_items])
#                 print('sum of stock in',sum_of_stock_in)
#                 sum_of_stock_in_amount = sum([_.amount for _ in stock_int_items])
#                 print("sum_of_stock_in_amount", sum_of_stock_in_amount)

#                 sum_of_already_stock_out = sum([_.stock_out for _ in already_stock_out_items])
#                 print("sum_of_already_stock_out", sum_of_already_stock_out)

#                 if sum_of_stock_in - (sum_of_already_stock_out + item_to_sell) < 0:
#                     print("Stock not available")
#                     return Response('Stock Not Avilable')

#                 print("Stock available")
#                 current_stock=sum_of_stock_in-sum_of_already_stock_out
#                 print('item is herer',item_value.item_id)        
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                 print("current Assets_vlaue",current_assets_last_stock.amount)
#                 future_stock_outs = []
#                 for stock_in_item in stock_int_items:
#                     print(stock_in_item)
                    
#                     if item_to_sell==0:
#                         print('Item Are not selled')
#                         break
#                     else:
#                         if sum_of_already_stock_out - stock_in_item.stock_in >= 0:
#                             print("\tItem fully sold")
#                             sum_of_already_stock_out = sum_of_already_stock_out - stock_in_item.stock_in
#                             print("\tRemaining already sold items: ", sum_of_already_stock_out)
#                             continue

#                         if sum_of_already_stock_out > 0:
#                             print("\tItem partially unsold")
#                             remaining_unsold_items = stock_in_item.stock_in - sum_of_already_stock_out
#                             print("\tRemaining unsold items", remaining_unsold_items)
#                             sum_of_already_stock_out = 0
#                         else:
#                             print("\tItem fully unsold")
#                             remaining_unsold_items = stock_in_item.stock_in
                        
#                         if item_to_sell > remaining_unsold_items:
#                             print("\tMore items need to be sold")
#                             print(f"\tSelling {remaining_unsold_items} items")
                            
#                             future_stock_outs=Stock.objects.create(
#                             item_id=item["item_id"],
#                             item_name=item["item_name"],
#                             stock_out=remaining_unsold_items,
#                             ref_id=debitnote_id.dn_id,
#                             amount=current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate,
#                             rate=stock_in_item.rate,
#                             ref_tblname='Debit Note',
#                             quantity=remaining_unsold_items,
#                             #stock_on_hand=current_stock-remaining_unsold_items,
#                             formname='Debit Note',
#                             module='Purchase',
#                             stage='Add Stages',
#                             date=debitnote_data["dn_date"],                
#                             company_id=comp_id)
#                             current_assets_last_stock.amount = current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate
#                             current_stock = current_stock-remaining_unsold_items
                            
                                
#                             #Stock(0, remaining_unsold_items, stock_in_item.rate)
#                             item_to_sell = item_to_sell - remaining_unsold_items
#                             print(f"\t{item_to_sell} still needed by the buyer")
#                         else:
#                             print(f"\tSelling {item_to_sell} items")
#                             future_stock_outs=Stock.objects.create(
#                             item_id=item["item_id"],
#                             item_name=item["item_name"],
#                             stock_out=item_to_sell,
#                             ref_id=debitnote_id.dn_id,
#                             amount=current_assets_last_stock.amount- item_to_sell*stock_in_item.rate,
#                             rate=stock_in_item.rate,
#                             quantity=item_to_sell,
#                             ref_tblname='DebitNote',
#                             #stock_on_hand=current_stock-item_to_sell,
#                             module='Purchase',
#                             formname='Debit Note',
#                             stage='Add Stages',
#                             date=debitnote_data["dn_date"],                
#                             company_id=comp_id)
                            
#                             #append(Stock(0, item_to_sell, stock_in_item.rate))
#                             item_to_sell = 0
                            


#         #This Section Is Stock Journal Transaction 
#         #Stock Charetd Account name is Inventory Assets
#                     # print('item rate',future_stock_outs.rate)
#                     # print('item quantity',future_stock_outs.quantity)
                    
#                         print('Journa created starts')
#                         account_payable =  COA.objects.get(company_id=comp_id,coa_id=inv_item_coa)
#                         TO_COA = COA.objects.get(company_id=comp_id, coa_id=item['coa_id'])
#                         stkmast = MasterTransaction.objects.create(
#                             L1detail_id=debitnote_id.dn_id,
#                             L1detailstbl_name='DebitNote',
#                             L2detail_id=future_stock_outs.st_id,
#                             L2detailstbl_name='Stock',
#                             main_module='Purchase',
#                             module='DebitNote',
#                             sub_module='DebitNote',
#                             transc_deatils='DebitNote',
#                             banking_module_type='DebitNote',
#                             journal_module_type='DebitNote',
#                             trans_date=debitnote_data["dn_date"],
#                             trans_status='Manually Added',
#                             debit=future_stock_outs.rate*future_stock_outs.quantity,
#                             to_account=TO_COA.coa_id,
#                             to_acc_type=TO_COA.account_type,
#                             to_acc_head=TO_COA.account_head,
#                             to_acc_subhead=TO_COA.account_subhead,
#                             to_acc_name=TO_COA.account_name,
#                             credit=future_stock_outs.rate*future_stock_outs.quantity,
#                             from_account=account_payable.coa_id,
#                             from_acc_type=account_payable.account_type,
#                             from_acc_head=account_payable.account_head,
#                             from_acc_subhead=account_payable.account_subhead,
#                             from_acc_name=account_payable.account_name,
#                             company_id=comp_id,
#                             vendor_id=vendor_id)
#                         stkmast.save()
#                         print(stkmast.from_acc_type)
            
#         # 0%GST and 0%IGST Calculation
#         #0% Tax Is User Select
#         Zero_tax=debitnote_data
#         TAX_name=Zero_tax['debit_note_items'][0]
#         GST_TAX=None
#         GST_TAX=TAX_name['selected_tax_name']
        
#         if GST_TAX is not None:
#             GST_TAX=TAX_name['selected_tax_name']['tax_name']
#         else:
#             pass
    

#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX   
            
#         else:
#             Both_Tax=None
           
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
        
#         transaction_list = [] #This Empty List added the append 
#         if float(debitnote_data['cgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Input CGST", "cgst_total"],)
#         if float(debitnote_data['sgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Input SGST", "sgst_total"])
#         if float(debitnote_data['igst_total'])>0 or IGST_0:
#             transaction_list.append(["Input SGST", "igst_total"],)       
        
#         for transaction in transaction_list:
#             FROM_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#             #transaction list of index is 0
#             dnmast = MasterTransaction.objects.create(
#                 L1detail_id=debitnote_id.dn_id,
#                 L1detailstbl_name='Debit Note',
#                 main_module='Purchase',
#                 module='Purchase',
#                 sub_module='DebitNote',
#                 transc_deatils='Debit Note Transaction',
#                 banking_module_type='Debit Note',
#                 journal_module_type='Debit Note',
#                 trans_date=debitnote_data["dn_date"],
#                 trans_status='Manually Added',
#                 debit=debitnote_data[transaction[1]],
#                 to_account=account_payable.coa_id,
#                 to_acc_type=account_payable.account_type,
#                 to_acc_head=account_payable.account_head,
#                 to_acc_subhead=account_payable.account_subhead,
#                 to_acc_name=account_payable.account_name,
#                 credit=debitnote_data[transaction[1]],
#                 from_account=FROM_COA.coa_id,
#                 from_acc_type=FROM_COA.account_type,
#                 from_acc_head=FROM_COA.account_head,
#                 from_acc_subhead=FROM_COA.account_subhead,
#                 from_acc_name=FROM_COA.account_name,
#                 company_id=comp_id,
#                 vendor_id=vendor_id)
#             dnmast.save()
                                                         

# # Commenting By Shubham
# # region This a transaction without Master Transaction
# # This Region is the Credit And Debit Transaction the vlaues are Two rows Added in Database

        

#         print("Ohhhhhh Transaction Has Started")    
#         account_payable = COA.objects.get(company_id=comp_id, account_subhead='Account Payables')
#         # Loop through each unique coa_id
        
#         for debit_note_item in debit_note_items:
            
#             FROM_COA = COA.objects.get(company_id=comp_id,coa_id=debit_note_item['coa_id'])
#             dnmast = MasterTransaction.objects.create(
#                 L1detail_id=debitnote_id.dn_id,
#                 L1detailstbl_name='Debit Note',
#                 main_module='Purchase',
#                 module='Purchase',
#                 sub_module='DebitNote',
#                 transc_deatils='Debit Note Transaction',
#                 banking_module_type='Debit Note',
#                 journal_module_type='Debit Note',
#                 trans_date=debitnote_data["dn_date"],
#                 trans_status='Manually Added',
#                 debit=debit_note_item['amount'],
#                 to_account=account_payable.coa_id,
#                 to_acc_type=account_payable.account_type,
#                 to_acc_head=account_payable.account_head,
#                 to_acc_subhead=account_payable.account_subhead,
#                 to_acc_name=account_payable.account_name,
#                 credit=debit_note_item['amount'],
#                 from_account=FROM_COA.coa_id,
#                 from_acc_type=FROM_COA.account_type,
#                 from_acc_head=FROM_COA.account_head,
#                 from_acc_subhead=FROM_COA.account_subhead,
#                 from_acc_name=FROM_COA.account_name,
#                 company_id=comp_id,
#                 vendor_id=vendor_id)
#             dnmast.save()
#             print('Sucessfully complted')
        
#         #     #amount is debit and credit side
            

#         #user can select the Discount this block will be excuted
#         if debitnote_data['discount']>0:
#             discount_account=debitnote_data['discount_account']
#             TO_COA =COA.objects.get(company_id=comp_id, coa_id=discount_account)
#             FROM_COA =COA.objects.get(coa_id=account_payable.coa_id)
#             dnmast = MasterTransaction.objects.create(
#                 L1detail_id=debitnote_id.dn_id,
#                 L1detailstbl_name='Debit Note',
#                 main_module='Purchase',
#                 module='Purchase',
#                 sub_module='DebitNote',
#                 transc_deatils='Debit Note Transaction',
#                 banking_module_type='Debit Note',
#                 journal_module_type='Debit Note',
#                 trans_date=debitnote_data["dn_date"],
#                 trans_status='Manually Added',
#                 debit=debitnote_data['discount'],
#                 to_account=TO_COA.coa_id,
#                 to_acc_type=TO_COA.account_type,
#                 to_acc_head=TO_COA.account_head,
#                 to_acc_subhead=TO_COA.account_subhead,
#                 to_acc_name=TO_COA.account_name,
#                 credit=debitnote_data['discount'],
#                 from_account=FROM_COA.coa_id,
#                 from_acc_type=FROM_COA.account_type,
#                 from_acc_head=FROM_COA.account_head,
#                 from_acc_subhead=FROM_COA.account_subhead,
#                 from_acc_name=FROM_COA.account_name,
#                 company_id=comp_id,
#                 vendor_id=vendor_id)
#             dnmast.save()
#         serializer = DebitnoteSerializer(debitnote_id)  # browser
#         return Response(serializer.data)
            
# #endregion
# #End Debit Note Section        
        
# #This Section is Expense Post
# #region
# #Expense form For using master transaction
# class new3expenserecordViewSet(viewsets.ModelViewSet):
#     queryset = ExpenseRecord.objects.all()
#     serializer_class = ExpenseRecordSerializer

#     def create(self, request, *args, **kwargs):
       
#         er_data_converte = request.data['data']
#         # =er_data_converte
#         # Expense Convert Str to Dict Code
#         er_data = json.loads(er_data_converte)

#         er_file_data = request.FILES.get('attach_file')
        
#         vn_id = er_data["vendor_id"]
#         if vn_id is not None:
#             vn_id = Vendor.objects.get(vendor_id=vn_id)

#         cust_id = er_data["customer_id"]
#         if cust_id is not None:
#             cust_id = SalesCustomer.objects.get(customer_id=cust_id)

#         selected_tax_name = er_data['selected_tax_name']
#         if selected_tax_name is not None:
#             tax_percentage = selected_tax_name['tax_percentage']
#         else:
#             tax_percentage = None

#         comp_id = Company.objects.get(company_id=er_data["company_id"])
#         # Expense Record fields
#         er_id = ExpenseRecord.objects.create(
#             expense_date=er_data["expense_date"],
#             # expense_account=er_data["expense_account"],
#             coa_id=COA.objects.get(coa_id=er_data["coa_id"]),
#             expense_type=er_data["expense_type"],
#             amount=er_data["amount"],
#             paid_through=er_data["paid_through"],
#             invoice_serial=er_data["invoice_serial"],
#             expense_serial=er_data["expense_serial"],
#             expense_total=er_data["expense_total"],
#             sac=er_data["sac"],
#             hsn_code=er_data["hsn_code"],
#             gst_treatment=er_data["gst_treatment"],
#             supply_place=er_data["supply_place"],
#             destination_place=er_data["destination_place"],
#             tax=er_data["tax"],
#             is_expense_generated=er_data["is_expense_generated"],
#             expense_status=er_data["expense_status"],
#             notes=er_data["notes"],
#             vendor_gstin=er_data['vendor_gstin'],
#             tax_rate=er_data['tax_rate'],
#             tax_type=er_data['tax_type'],
#             tax_name=er_data['tax_name'],
#             tax_percentage=tax_percentage,
#             cgst_amount=er_data['cgst_amount'],
#             sgst_amount=er_data['sgst_amount'],
#             igst_amount=er_data['igst_amount'],
#             vendor_id=vn_id,
#             attach_file=er_file_data,
#             customer_id=cust_id,
#             company_id=comp_id)
#         er_id.save()
#         if er_file_data is not None:
#             file_ext = os.path.splitext(er_file_data.name)[1]
#             new_file_path = f'media/PRExpense_{er_id.er_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in er_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             er_id.attach_file = pth
#             er_id.save()
            
#         # 0% taxtion
#         Zero_tax=er_data
#         GST_TAX=None
#         GST_TAX=Zero_tax['selected_tax_name']
#         if GST_TAX is not None:
            
#             GST_TAX=Zero_tax['selected_tax_name']['tax_name']
#         else:
#             pass
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX   
            
#         else:
#             Both_Tax=None
           
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
#         print('GOD',GST_TAX)
        
#         #Exp tax Section   
#         FROM_COA = COA.objects.get(coa_id=er_data["paid_through"])
#         transaction_list = [] #This Empty List added the append 
#         if float(er_data['sgst_amount'])>0 or Both_Tax:
#             transaction_list.append(["Input CGST", "sgst_amount"],)
#         if float(er_data['cgst_amount'])>0 or Both_Tax:
#             transaction_list.append(["Input SGST", "cgst_amount"])
#         if float(er_data['igst_amount'])>0 or IGST_0:
#             transaction_list.append(["Input IGST", "igst_amount"],)       
        
#         for transaction in transaction_list:
#             TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#             #transaction list of index is 0
#             expmast = MasterTransaction.objects.create(
#             L1detail_id=er_id.er_id,
#             L1detailstbl_name='Expense Record',
#             main_module='Purchase',
#             module='Expense Record',
#             sub_module='Expense Record',
#             transc_deatils='Expanese Transaction',
#             banking_module_type='Expense',
#             journal_module_type='Expense Account Selection',
#             trans_date=er_data["expense_date"],
#             trans_status='Expense',
#             debit=er_data[transaction[1]],
#             to_account=TO_COA.coa_id,
#             to_acc_type=TO_COA.account_type,
#             to_acc_head=TO_COA.account_head,
#             to_acc_subhead=TO_COA.account_subhead,
#             to_acc_name=TO_COA.account_name,
#             credit=er_data[transaction[1]],
#             from_account=FROM_COA.coa_id,
#             from_acc_type=FROM_COA.account_type,
#             from_acc_head=FROM_COA.account_head,
#             from_acc_subhead=FROM_COA.account_subhead,
#             from_acc_name=FROM_COA.account_name,
#             customer_id=cust_id,
#             company_id=comp_id,
#             vendor_id=vn_id)
#             expmast.save()

#         #Expense main transaction Section Menas item Section
#         FROM_COA = COA.objects.get(coa_id=er_data["paid_through"])
#         TO_COA = COA.objects.get(coa_id=er_data["coa_id"])
#         expmast = MasterTransaction.objects.create(
#         L1detail_id=er_id.er_id,
#         L1detailstbl_name='Expense Record',
#         main_module='Purchase',
#         module='Expense Record',
#         sub_module='Expense Record',
#         transc_deatils='Expanese Transaction',
#         banking_module_type='Expense',
#         journal_module_type='Expense Account Selection',
#         trans_date=er_data["expense_date"],
#         trans_status='Expense',
#         debit=er_data["amount"],
#         to_account=TO_COA.coa_id,
#         to_acc_type=TO_COA.account_type,
#         to_acc_head=TO_COA.account_head,
#         to_acc_subhead=TO_COA.account_subhead,
#         to_acc_name=TO_COA.account_name,
#         credit=er_data["expense_total"],
#         from_account=FROM_COA.coa_id,
#         from_acc_type=FROM_COA.account_type,
#         from_acc_head=FROM_COA.account_head,
#         from_acc_subhead=FROM_COA.account_subhead,
#         from_acc_name=FROM_COA.account_name,
#         customer_id=cust_id,
#         company_id=comp_id,
#         vendor_id=vn_id)
#         expmast.save()

#         serializer = ExpenseRecordSerializer(er_id)  # browser
#         return Response(serializer.data)


# #endregion
# #End The Mastertransaction 




#  #Debit Note Refund Section
#  #region
# class NewVendor_debitRefundModelViewSets(viewsets.ModelViewSet):
#     queryset=RefundMaster.objects.all()
#     serializer_class=DebitNoteRefundSerializer

#     logger=[]
#     # Forone API are going to make three append append namely for Two Main Sections
#       #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
#       #  2: Financial Transaction: 
#         #2.1 Credit Transation
#         #2.2 Debit Transaaction
#     def ValidateDefaults(obj):
#         NewVendor_debitRefundModelViewSets.logger=[]
#         ## Validation Section
#         branch_id=obj["branch_id"]
#         company_id=obj["company_id"]
#         vendor_id=obj["vendor_id"]
#         retValue=True
#         if vendor_id is None:
#             NewVendor_debitRefundModelViewSets.logger.append("Vendor  iD is Null Please Provide a Vendor ID")
#             retValue= False  
#         if branch_id is None:
#             NewVendor_debitRefundModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
#             retValue= False        
#         if(company_id is  None ):
#             NewVendor_debitRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
#             retValue= False            
#         if(type(company_id!=uuid)):
#             NewVendor_debitRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
#             retValue= False      
#         return retValue

#     def create(self, request, *args, **kwargs):
#         debitnote_data = request.data
        

#         # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
#         # bank=debitnote_data["coa_id"]
#         # From_Bank=Banking.objects.get(coa_id=bank)

#         if(NewVendor_debitRefundModelViewSets.ValidateDefaults(debitnote_data)==False):
#             print(" Ooops!!! Error Occured ",NewVendor_debitRefundModelViewSets.logger)
            
#         print(debitnote_data)
#             #What if this ID is null , 
        	
#         branch_id=debitnote_data["branch_id"]
#         if branch_id is not None:
#             branch_id=Branch.objects.get(branch_id=branch_id)

#         company_id=debitnote_data["company_id"]
#         if company_id is not None:
#             company_id=Company.objects.get(company_id=company_id)

#         vendor_id=debitnote_data["vendor_id"]
#         if vendor_id is not None:
#             vendor_id=Vendor.objects.get(vendor_id=vendor_id)


#         debitnote_id=debitnote_data["dn_id"]
#         print("debit note id is ",debitnote_id,type(debitnote_id))

#         # Create DebitNoteRefund

#         debit_id=RefundMaster.objects.create(
#         company_id=company_id,
#         branch_id=branch_id,
#         bank_id=debitnote_data["bank_id"],
#         vendor_id=vendor_id,
#         refrence_id=debitnote_id,
#         coa_id=COA.objects.get(coa_id=debitnote_data["coa_id"]),
#         is_dn_refund_generated=debitnote_data["is_dn_refund_generated"],
#         refund_date=debitnote_data["refunded_on"],
#         status=debitnote_data["status"],
#         refund_balance_amount=debitnote_data["refund_balance_amount"],
#         refund_ref_no=debitnote_data["refund_ref_no"],
#         amount=debitnote_data["amount"],
#         payment_mode=debitnote_data["payment_mode"],
#         serial_ref=debitnote_data["dn_serial"],
#         amount_ref=debitnote_data["dn_amount"],
#         description=debitnote_data["description"])
#         debit_id.save()
#         print("Debit Note Refund",debit_id,type(debit_id))




        
#         #2 Financial Transaction Prerequisites 
#         ## Credit Transaction 
#         ## SHould be added the amount TO_COA_ID 
#         # Refer the Excel coa_id refers  Bank COA it depends on the Form whether it is To_COA or From_COA

      
#          # Get The COA Table  Account Name is Account Payables and Pass The coa_id in Debit Note Refund Transaction Table 

        
# #Commenting By Shubham
# # This Region is the Credit And Debit Transaction the vlaues are Two rows Added in Database


       
#         TO_COA = COA.objects.get(company_id=company_id,account_name="Account Payables")
#         From_COA=COA.objects.get(company_id=company_id,coa_id=debitnote_data["coa_id"])
#         print('""""""""""""',TO_COA)  
#         dnrmast=MasterTransaction.objects.create(
#         L1detail_id=debit_id.rm_id,
#         L1detailstbl_name='RefundMaster',
#         L2detail_id=From_COA.coa_id,
#         L2detailstbl_name='COA',
#         L3detail_id=debitnote_id,
#         L3detailstbl_name='Debit Note',
#         main_module='Banking',
#         module='MonenyIN',
#         sub_module='DebitNote Refund',
#         transc_deatils='Debit Note Refund',
#         banking_module_type=debitnote_data["transaction_module"],
#         journal_module_type=debitnote_data["transaction_module"],
#         trans_date=debitnote_data["refunded_on"],
#         trans_status=debitnote_data["status"],
#         debit=debitnote_data["amount"],
#         to_account=From_COA.coa_id,
#         to_acc_type=From_COA.account_type,
#         to_acc_head=From_COA.account_head,
#         to_acc_subhead=From_COA.account_subhead,
#         to_acc_name=From_COA.account_name,
#         credit=debitnote_data['entered_amount'],
#         from_account=TO_COA.coa_id,
#         from_acc_type=TO_COA.account_type,
#         from_acc_head=TO_COA.account_head,
#         from_acc_subhead=TO_COA.account_subhead,
#         from_acc_name=TO_COA.account_name,
#         company_id=company_id,
#         vendor_id=vendor_id,
#         branch_id=branch_id)
#         dnrmast.save() 

# #Balance Amount Update section
# # refund time Update the status and dn_status or balance_amount
#         dn_id=debitnote_data["dn_id"]
#         if dn_id is not None:
#             dn_id=DebitNote.objects.get(dn_id=dn_id)

#             balance_amount=debitnote_data["refund_balance_amount"]
#             print("Amount values are",balance_amount,type(balance_amount))
#             if balance_amount == 0:
#                 print('dn_id', dn_id)
#                 dn_id.balance_amount= debitnote_data["refund_balance_amount"]           
#                 dn_id.status='Closed'
#                 dn_id.dn_status='Closed'
#                 dn_id.save()
#                 print('Debit status updated to ', dn_id.status)
           
#             elif balance_amount >= 0:
#                 print('debit note id of else', dn_id)
#                 dn_id.balance_amount= debitnote_data["refund_balance_amount"]            
#                 dn_id.save()       
#                 print('Debit note amount due updated to ', dn_id.balance_amount)
#             else:
#                 print('dn_id', dn_id)              
#                 dn_id.status='open'
#                 dn_id.save()
#                 print('Debit note status updated to ', dn_id.status)
#         serializer =DebitNoteRefundSerializer(debit_id)         
#         return Response(serializer.data)
# #endregion
# #End Debit Note refund Section  
    
# # Debit Note refund Journal Transaction Section
# #region
# #dn_id through the fethch the data
# n_data=None
# @api_view(['GET'])
# def getDNRJournalTransaction(self,dn_id):
#     form_mast = MasterTransaction.objects.filter(L3detail_id=dn_id)
#     df = pd.DataFrame(form_mast.values('to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
#                         'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit'))
#     print(df)
#     from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name',]).agg(
#         {'credit': 'sum'}).reset_index()
#     to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',]).agg(
#         { 'debit': 'sum'}).reset_index()
#     from_acc = from_acc.rename(columns={
#                                 'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name'}, inplace=False)
#     to_acc = to_acc.rename(columns={
#                             'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name'}, inplace=False)


#     df_accounts = pd.concat([from_acc, to_acc])
#     response = json.loads(df_accounts.to_json(orient='records'))

#     serializer = MasterTransactionSerializer(form_mast, many=True)
#     n_data=serializer.data
#     all_response = {
#             # 'original_data': account_type_list,
#             'form_data': n_data,
#             'transaction': response,
#         }
#     return Response(all_response)
    
# #endregion
# #Debit Note Journal Transactions 
    
 
# #Vendor Advanced Refund Transaction Section 
# #region  
# class Vendor_AdvancedRefundModelViewSets(viewsets.ModelViewSet):
#     queryset=VendorAdvanced.objects.all()
#     serializer_class=VendorAdvancedSerializer
#     logger=[]
#     # Forone API are going to make three append append namely for Two Main Sections
#       #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
#       #  2: Financial Transaction: 
#         #2.1 Credit Transation
#         #2.2 Debit Transaaction

#     def ValidateDefaults(obj):
#         Vendor_AdvancedRefundModelViewSets.logger=[]
#         ## Validation Section
#         branch_id=obj["branch_id"]
#         company_id=obj["company_id"]
#         retValue=True
#         if branch_id is None:
#             Vendor_AdvancedRefundModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
#             retValue= False        
#         if(company_id is  None ):
#             Vendor_AdvancedRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
#             retValue= False            
#         if(type(company_id!=uuid)):
#             Vendor_AdvancedRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
#             retValue= False      
#         return retValue

#     def create(self, request, *args, **kwargs):
#         vendor_advanced_data = request.data['data']
#         vendor_advanced_data = json.loads(vendor_advanced_data)
#         # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
#         # bank=vendor_advanced_data["coa_id"]
#         # From_Bank=Banking.objects.get(coa_id=bank)

#         va_file_data=request.FILES.get('attach_file')
#         if(Vendor_AdvancedRefundModelViewSets.ValidateDefaults(vendor_advanced_data)==False):
#             print(" Ooops!!! Error Occured ",Vendor_AdvancedRefundModelViewSets.logger)
        
#         print(vendor_advanced_data)

#         branch_id=vendor_advanced_data["branch_id"]
#         if branch_id is not None:
#             branch_id=Branch.objects.get(branch_id=branch_id)

#         company_id=vendor_advanced_data["company_id"]
#         if company_id is not None:
#             company_id=Company.objects.get(company_id=company_id)
        
#         vendor_id=vendor_advanced_data["vendor_id"]
#         if vendor_id is not None:
#             vendor_id=Vendor.objects.get(vendor_id=vendor_id)
            
#         coa_id=vendor_advanced_data["paid_through"]
#         if coa_id is not None:
#             coa_id=COA.objects.get(coa_id=coa_id)
            
#         tds_id = vendor_advanced_data.get("tds_id")
#         if tds_id is not None:
#             tds_id = TDS.objects.get(tds_id=tds_id)
#         SAL_TAX=None   
#         Zero_tax=vendor_advanced_data["selected_tax_name"]  
#         if Zero_tax is not None:
#             SAL_TAX=Zero_tax.get('tax_name')
       
      
      	
# 		# Create Vendor Advanced
		
#         va_id=VendorAdvanced.objects.create(
#         is_vendor_advance_generated=vendor_advanced_data["is_vendor_advance_generated"],
#         company_id=company_id,
#         bank_id=vendor_advanced_data['bank_id'],    
#         branch_id=branch_id,
#         vendor_id=vendor_id,
#         status=vendor_advanced_data["status"],
#         coa_id=coa_id,
#         tds_id=tds_id,     
#         destination_place=vendor_advanced_data["destination_place"],
#         amount=vendor_advanced_data["amount_payable"],
#         payment_serial=vendor_advanced_data["payment_serial"],
#         balance_amount=vendor_advanced_data['balance_amount'],
#         vendor_advance_ref_no=vendor_advanced_data["payment_ref_no"],
#         vendor_advance_date=vendor_advanced_data["payment_date"],
#         paid_via=vendor_advanced_data["payment_mode"],
#         source_place=vendor_advanced_data["supply_place"],
#         description_supply=vendor_advanced_data["dec_supply_place"],
#         cgst_amount=vendor_advanced_data["cgst_amount"],
#         sgst_amount=vendor_advanced_data["sgst_amount"],
#         igst_amount=vendor_advanced_data['igst_amount'],
#         tds_amount=vendor_advanced_data['tds_amount'],
#         #tax_rate=vendor_advanced_data["tax_rate"],
#         tax_name=SAL_TAX,  
#         tax_type=vendor_advanced_data["tax_type"],
#         #tax_amount=vendor_advanced_data["tax_amount"], 
#         reverse_charge=vendor_advanced_data["reverse_charge"])
#         va_id.save()
#         if va_file_data is not None:
#             file_ext = os.path.splitext(va_file_data.name)[1]
#             new_file_path = f'media/VARF_{va_id.va_id}{file_ext}' 
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in va_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here',pth)
#             va_id.attach_file=pth
#             va_id.save()

       

#         TO_COA= COA.objects.get(company_id=company_id,account_subhead="Account Payables")   
#         From_COA=COA.objects.get(company_id=company_id,coa_id=vendor_advanced_data["paid_through"])     
#         print('TTTTTT',TO_COA)
#         print('TTTTT',From_COA)  
#         vamast=MasterTransaction.objects.create(
#         L1detail_id=va_id.va_id,
#         L1detailstbl_name='VendorAdvanced',
#         L2detail_id=From_COA.coa_id,
#         L2detailstbl_name='COA',
#         main_module='Purchase',
#         module='Refund',
#         sub_module='VendorAdvanced',
#         transc_deatils='Vendor Advanced',
#         banking_module_type=vendor_advanced_data["transaction_module"],
#         journal_module_type=vendor_advanced_data["transaction_module"],
#         trans_date=vendor_advanced_data["payment_date"],
#         trans_status=vendor_advanced_data["status"],
#         debit=vendor_advanced_data['amount_payable'],
#         to_account=TO_COA.coa_id,
#         to_acc_type=TO_COA.account_type,
#         to_acc_head=TO_COA.account_head,
#         to_acc_subhead=TO_COA.account_subhead,
#         to_acc_name=TO_COA.account_name,
#         credit=vendor_advanced_data['amount_payable'],
#         from_account=From_COA.coa_id,        
#         from_acc_type=From_COA.account_type,
#         from_acc_head=From_COA.account_head,
#         from_acc_subhead=From_COA.account_subhead,
#         from_acc_name=From_COA.account_name,
#         company_id=company_id,
#         vendor_id=vendor_id,
#         branch_id=branch_id)
#         vamast.save()
#         print('@@@@@@',vamast)
        
#         Zero_tax=vendor_advanced_data
#         TAX_name=Zero_tax
#         GST_TAX=None
#         GST_TAX=TAX_name['selected_tax_name']
        
#         if GST_TAX is not None:
#             GST_TAX=TAX_name['selected_tax_name']['tax_name']
#         else:
#             pass
    

#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX   
            
#         else:
#             Both_Tax=None
           
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
             
            
        
#         # User Can the Send the data in request the this data added in this empty list and 
#         #this list can perform the operation 
#         # all the values are not equal to zero the added the list
#         #list added item to add the master transaction table
#         #chnges of this transaction debit credit and to from account
#         transaction_list = [] #This Empty List added the append
        
#         if float(vendor_advanced_data['tds_amount'])>0:
#             transaction_list.append(["TDS Payable","tds_amount"])
        
#         for transaction in transaction_list :
            
#             #List Of index added 0 is get Account_name
#             FORM_COA = COA.objects.get(company_id=company_id,account_name=transaction[0])
#             print('@@@@@@@@@',From_COA)
#             #Transaction Time to you TO_COA will account Subhead
#             TO_COA= COA.objects.get(company_id=company_id,account_subhead="Account Payables")   
#             print('""""""""""""',TO_COA)  
#             vamast=MasterTransaction.objects.create(
#             L1detail_id=va_id.va_id,
#             L1detailstbl_name='VendorAdvanced',
#             main_module='Purchase',
#             module='Refund',
#             sub_module='VendorAdvanced',
#             transc_deatils='Vendor Advanced',
#             banking_module_type=vendor_advanced_data["transaction_module"],
#             journal_module_type=vendor_advanced_data["transaction_module"],
#             trans_date=vendor_advanced_data["payment_date"],
#             trans_status=vendor_advanced_data["status"],
#             debit=vendor_advanced_data[transaction[1]],
#             to_account=TO_COA.coa_id,
#             to_acc_type=TO_COA.account_type,
#             to_acc_head=TO_COA.account_head,
#             to_acc_subhead=TO_COA.account_subhead,
#             to_acc_name=TO_COA.account_name,
#             credit=vendor_advanced_data[transaction[1]],
#             from_account=FORM_COA.coa_id,        
#             from_acc_type=FORM_COA.account_type,
#             from_acc_head=FORM_COA.account_head,
#             from_acc_subhead=FORM_COA.account_subhead,
#             from_acc_name=FORM_COA.account_name,
#             company_id=company_id,
#             vendor_id=vendor_id,
#             branch_id=branch_id)
#             vamast.save()
#         # UI side to select the reverse charge to implement     
#         if vendor_advanced_data['reverse_charge'] == True:
#             tax_transaction_list=[]
#         else:
#             tax_transaction_list=[]
                
#         # taxtion Section 
#         if float(vendor_advanced_data['cgst_amount']) >0 or Both_Tax:
#             tax_transaction_list.append(["Output CGST", "cgst_amount"],)
#         if float(vendor_advanced_data['sgst_amount'] )>0 or Both_Tax:
#             tax_transaction_list.append(["Output SGST", "sgst_amount"])
#         if float(vendor_advanced_data['igst_amount']) >0 or IGST_0:
#             tax_transaction_list.append(["Output IGST", "igst_amount"],)
#         for transaction_tax in tax_transaction_list :   
#             FORM_COA = COA.objects.get(company_id=company_id,account_name=transaction_tax[0])
#             print('@@@@@@@@@',From_COA)
#             #Transaction Time to you TO_COA will account name
#             TO_COA= COA.objects.get(company_id=company_id,account_name= 'Tax Paid Expense')   
#             print('""""""""""""',TO_COA)  
#             vamast=MasterTransaction.objects.create(
#             L1detail_id=va_id.va_id,
#             L1detailstbl_name='VendorAdvanced',
#             main_module='Purchase',
#             module='Refund',
#             sub_module='VendorAdvanced',
#             transc_deatils='Vendor Advanced',
#             banking_module_type=vendor_advanced_data["transaction_module"],
#             journal_module_type=vendor_advanced_data["transaction_module"],
#             trans_date=vendor_advanced_data["payment_date"],
#             trans_status=vendor_advanced_data["status"],
#             debit=vendor_advanced_data[transaction_tax[1]],
#             to_account=TO_COA.coa_id,
#             to_acc_type=TO_COA.account_type,
#             to_acc_head=TO_COA.account_head,
#             to_acc_subhead=TO_COA.account_subhead,
#             to_acc_name=TO_COA.account_name,
#             credit=vendor_advanced_data[transaction_tax[1]],
#             from_account=FORM_COA.coa_id,        
#             from_acc_type=FORM_COA.account_type,
#             from_acc_head=FORM_COA.account_head,
#             from_acc_subhead=FORM_COA.account_subhead,
#             from_acc_name=FORM_COA.account_name,
#             company_id=company_id,
#             vendor_id=vendor_id,
#             branch_id=branch_id)
#             vamast.save()



#         serializer =VendorAdvancedSerializer(va_id)         
#         return Response(serializer.data)


# #endregion
# #End Vendor Advance Refund 



# # Vendor Advanced Journal Transaction Section
# #region
# #va_id through the fethch the data
# n_data=None
# @api_view(['GET'])
# def getVARJournalTransaction(self,va_id):
#     form_mast = MasterTransaction.objects.filter(L1detail_id=va_id)
#     df = pd.DataFrame(form_mast.values('to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
#                         'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit'))
#     print(df)
#     from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name',]).agg(
#         {'credit': 'sum'}).reset_index()
#     to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',]).agg(
#         { 'debit': 'sum'}).reset_index()
#     from_acc = from_acc.rename(columns={
#                                 'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name'}, inplace=False)
#     to_acc = to_acc.rename(columns={
#                             'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name'}, inplace=False)


#     df_accounts = pd.concat([from_acc, to_acc])
#     response = json.loads(df_accounts.to_json(orient='records'))

#     serializer = MasterTransactionSerializer(form_mast, many=True)
#     n_data=serializer.data
#     all_response = {
#             # 'original_data': account_type_list,
#             'form_data': n_data,
#             'transaction': response,
#         }
#     return Response(all_response)
    
# #endregion
# # Vendor Advanced refund Journal Transactions 

# @api_view(['GET'])
# def varshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     var = VendorAdvanced.objects.filter(company_id=company)
#     serializer = VendorAdvancedSerializer(var, many=True)   
#     return Response(serializer.data)

# @api_view(['GET'])
# def purchasevabyid(request, va_id):
#     va = VendorAdvanced.objects.filter(va_id=va_id)
#     serializer = VendorAdvancedSerializer(va, many=True)
#     return Response(serializer.data)




# class VendorAdvGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = VendorAdvanced.objects.all()
#     serializer_class = VendorAdvancedSerializer

#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'purchase/varffile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)
    
# #Vendor Advance Refund file Download    
# class VARFFileDownloadListAPIView(generics.ListAPIView):
    
#     def get(self, request, va_id, format=None):
#         queryset = VendorAdvanced.objects.get(va_id=va_id)
#         if queryset.attach_file:
#             file_handle = queryset.attach_file.path
#             if os.path.exists(file_handle):
#                 document = open(file_handle, 'rb')
#                 response = HttpResponse(FileWrapper(
#                     document), content_type='application/msword')
#                 response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
#                 return response
#             else:
#                 response = HttpResponse("File Not Found")
#                 return response
#         else:
#             return HttpResponse('File not Found in Model')



# ############# GENERATE VENDOR ADVANCED PDF AND DOWNLOAD ##############################
# @api_view(['GET'])   
# def download_vendor_advanced_data(request, comp_id,va_id):
#     company = Company.objects.get(company_id=comp_id)
#     va = VendorAdvanced.objects.get(ca_id=va_id)
#     # here filter the object of bill id and company id
#     varecieved = VendorAdvanced.objects.filter(
#         company_id=comp_id,ca_id=va_id).order_by('created_date')
    
#     serializers =VendorAdvancedSerializer(varecieved, many=True)
#     print("```````````````````````````````````````````````33333333",serializers.data)
#     output_pdf = f"PR_{datetime.datetime.now().timestamp()}.pdf"
#     generate_vendor_advance_pdf(data=serializers.data,output_path=os.path.join("media", output_pdf))
    
#     if os.path.exists(os.path.join("media", output_pdf)):
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadpr/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)

# def download_va(request, file_name):
#     file_path = f"media/{file_name}"           
#     response = FileResponse(open(file_path,'rb'), as_attachment=True)                              
#     return response
# ################################################################################









# class BillUpdate3ViewSet(viewsets.ModelViewSet):
#     queryset = Bill.objects.all()
#     serializer_class = Bill
#     def update(self, request, pk, *args, **kwargs):
#         #dxfxfddfc
#         bill_data=request.data
#         bill = Bill.objects.get(bill_id=pk)
#         comp_id = Company.objects.get(company_id=bill_data["company_id"])
#         ven_id = Vendor.objects.get(
#             vendor_id=bill_data["vendor_id"])
        
#         #account receivable varibale are declaret the chart of account of to side from item and taxation Section 
#         #and Discount time this chartof Account is From Side
       
#         # Invoice Item Looping
#         for bill_item_data in bill_data['bill_items']:
#            # Item are find Out Section
           
#             try:
#                 try:
#                     bill_item = Bill_Item.objects.get(item_id=bill_item_data['item_id'],bill_id=bill)
                    
#                 except KeyError:
#                     bill_item=None
                    
                  
                                
#             except Bill_Item.DoesNotExist:
#                 bill_item=None
            
#             # Invoice Item Are Find the update this Code Section   
#             if bill_item is not None:
                
#                 item_serializer=GETBillItemSerializer(bill_item,data=bill_item_data)
#                 if item_serializer.is_valid():
#                     item_serializer.save()
#                 else:
#                     return Response(item_serializer.errors, status=400)
                   
#             else:
#                 try:
#                     # Get The Chart Of Account and item Id Of the Item Related
#                     coa=COA.objects.get(coa_id=bill_item_data["coa_id"])
#                     item=Item.objects.get(item_id=bill_item_data["item_id"])
#                 except KeyError:
#                     coa=None
#                     item=None
                
#                 try:
#                     #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
#                     bill_items = Bill_Item.objects.create(bill_id=bill,
#                                                         item_id=item, 
#                                                         coa_id=coa,
#                                                         item_name=bill_item_data["item_name"],
#                                                         rate=bill_item_data["rate"],
#                                                         quantity=bill_item_data["quantity"],
#                                                         tax_rate=bill_item_data["tax_rate"],
#                                                         tax_name=bill_item_data["tax_name"],
#                                                         tax_type=bill_item_data["tax_type"],
#                                                         sgst_amount=bill_item_data["sgst_amount"],
#                                                         cgst_amount=bill_item_data["cgst_amount"],
#                                                         igst_amount=bill_item_data["igst_amount"],
#                                                         # taxamount=item["taxamount"],
#                                                         amount=bill_item_data["amount"])
#                     bill_items.save()
                   
#                 except KeyError:
#                     pass                 
                
                    
                
            
#         #this Section Is Invoice Data Update Serializer Through
#         serializer = BillSerializer(bill, data=bill_data)

#         if serializer.is_valid():
#             bill_id=serializer.save()
            
#             # return Response({"data":serializer.data})
#         else:
#              return Response(serializer.errors, status=400)
        
#         stock_item_list=[]
#         stock_transactiom_item_list=[]
#         account_payable = COA.objects.get(company_id=comp_id, account_subhead='Account Payables')
        
#         for bill_item_stock in bill_data['bill_items']:
#             print('For Loop Is Excuted')
#             stock_item_list.append(bill_item_stock['item_id'])
#             try: 
                
#                 stock_item=Stock.objects.get(item_id=bill_item_stock['item_id'],ref_id=bill.bill_id)
           
#                 print('okk')     
#                 item_value=Item.objects.get(item_id=bill_item_stock["item_id"])
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
            
#                 print("updating stock", bill_item_stock['quantity'], bill_item_stock['item_id'])
#                 stock_item.stock_in=float(bill_item_stock['quantity'])
#                 stock_item.rate=float(current_assets_last_stock.rate)
#                 stock_item.amount=float(current_assets_last_stock.rate)*float(bill_item_stock['quantity'])
#                 stock_item.quantity=float(bill_item_stock['quantity'])
#                 stock_item.save()
#                 stock_transactiom_item_list.append(stock_item)
#                 stock_mast=MasterTransaction.objects.get(L2detail_id=stock_item.st_id,L1detail_id=bill_id.bill_id)
#                 stock_mast.debit=stock_item.rate*stock_item.quantity,
#                 stock_mast.credit=stock_item.rate*stock_item.quantity,
#                 print('Updateing Sucessfully')
#             except Stock.DoesNotExist:
                    
#                 items_inventory=bill_data.get('bill_items')
#                 print('Inventory Tracked item is ',items_inventory)
#                 track_inventory=bill_item_stock.get('selected_item_name',{}).get('track_inventory')
#                 print('Inventory Tracked item is ',items_inventory)
#                 coa=items_inventory[0].get('coa_id')
#                 amount=items_inventory[0].get('amount')
#                 item_value=Item.objects.get(item_id=bill_item_stock["item_id"])
                
#                 try:
#                     current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                     current_stock_amount=current_assets_last_stock.amount
                   
#                 except Stock.DoesNotExist:
#                     current_stock_amount=0
                    
                    
                
#                 if track_inventory==True:
#                     stk_in=Stock.objects.filter(item_id=bill_item_stock["item_id"]).exclude(stock_in=0).order_by('created_date')
#                     stk_out=Stock.objects.filter(item_id=bill_item_stock["item_id"]).exclude(stock_out=0).order_by('created_date')        
#                     stock_int_items = stk_in
                    
                    
#                     stock_items=Stock.objects.create(
#                         item_id=bill_item_stock['item_id'],
#                         item_name=bill_item_stock["item_name"],
#                         stock_in=bill_item_stock["quantity"],
#                         amount=current_stock_amount+(bill_item_stock["quantity"] * bill_item_stock["rate"]),
#                         rate= bill_item_stock["rate"],
#                         quantity=bill_item_stock["quantity"],
#                         #stock_on_hand=current_stock_on_hand+bill_item_stock["quantity"],
#                         ref_id=bill_id.bill_id,
#                         ref_tblname='Bill',
#                         module='Purchase',
#                         formname='Bill',
#                         stage='Add Stages',
#                         date=bill_data["bill_date"],               
#                         company_id=comp_id)
                        
#                 #This Section Is Stock Journal Transaction 
#                 #Stock Charetd Account name is Inventory Assets
#                     # if track_inventory == True:
#                     print('New Item Are Created in Stock',stock_items)    
#                     TO_COA = COA.objects.get(company_id=comp_id,account_name='Inventory Assets')
#                     print('Stock is Created master Transaction Start')
#                     stkmast = MasterTransaction.objects.create(
#                         L1detail_id=bill_id.bill_id,
#                         L1detailstbl_name='Bill',
#                         L2detail_id=stock_items.st_id,
#                         L2detailstbl_name='Stock',
#                         main_module='Purchase',
#                         module='Bill',
#                         sub_module='Bill',
#                         transc_deatils='Bill',
#                         banking_module_type='Bill',
#                         journal_module_type='Bill',
#                         trans_date=bill_data["bill_date"],
#                         trans_status='Manually Added',
#                         debit=stock_items.rate*stock_items.quantity,
#                         to_account=TO_COA.coa_id,
#                         to_acc_type=TO_COA.account_type,
#                         to_acc_head=TO_COA.account_head,
#                         to_acc_subhead=TO_COA.account_subhead,
#                         to_acc_name=TO_COA.account_name,
#                         credit=stock_items.rate*stock_items.quantity,
#                         from_account=account_payable.coa_id,
#                         from_acc_type=account_payable.account_type,
#                         from_acc_head=account_payable.account_head,
#                         from_acc_subhead=account_payable.account_subhead,
#                         from_acc_name=account_payable.account_name,
#                         company_id=comp_id,
#                         vendor_id=ven_id)
#                     stkmast.save()
                   
#                 else:
#                     print('Transaction Completed Start')
#                     TO_COA = COA.objects.get(coa_id=coa)
#                     #FROM_COA = COA.objects.get(company_id=comp_id,coa_id=purchase_account)
#                     billmast = MasterTransaction.objects.create(
#                         L1detail_id=bill_id.bill_id,
#                         L1detailstbl_name='Bill',
#                         # L2detail_id=L2detail_id,
#                         # L2detailstbl_name=L2detailstbl_name,
#                         main_module='Purchase',
#                         module='Bill',
#                         sub_module='Bill',
#                         transc_deatils='Bill',
#                         banking_module_type='Bill',
#                         journal_module_type='Bill',
#                         trans_date=bill_data["bill_date"],
#                         trans_status='Manually Added',
#                         debit=amount,
#                         to_account=account_payable.coa_id,
#                         to_acc_type=account_payable.account_type,
#                         to_acc_head=account_payable.account_head,
#                         to_acc_subhead=account_payable.account_subhead,
#                         to_acc_name=account_payable.account_name,
#                         credit=amount,
#                         from_account=TO_COA.coa_id,
#                         from_acc_type=TO_COA.account_type,
#                         from_acc_head=TO_COA.account_head,
#                         from_acc_subhead=TO_COA.account_subhead,
#                         from_acc_name=TO_COA.account_name,
#                         vendor_id=ven_id,
#                         company_id=comp_id)
#                     billmast.save() 

        
        
       
#         try:    
#             # 0%GST and 0%IGST Calculation
#             #0 % Taxtion Is the UserSelection User Can Select the 0% Tax This 0 is Added the Tax Section
#             Zero_tax=bill_data.get('bill_items')
#             GST_TAX=None
#             if GST_TAX==Zero_tax[0] is not None:
#                 GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
#             else:
#                 pass
#         except:AttributeError
        
            
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX   
#         else:
#             Both_Tax=None
           
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
            
#         # User Can the Send the data in request the this data added in this empty list and 
#         #this list can perform the operation 
#         # all the values are not equal to zero the added the list
#         #list added item to add the master transaction table
#         #chnges of this transaction debit credit and to from account
        
       
#         bill_data['tds_amount']=abs(float(bill_data['tds_amount']))
#         transaction_list = [] #This Empty List added the append 
#         print("Transaction List is here",)
#         if float(bill_data['cgst_total'])>0  or Both_Tax:
#             transaction_list.append(["Input CGST", "cgst_total"],)
#         if float(bill_data['sgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Input SGST", "sgst_total"])
#         if float(bill_data['igst_total']) >0 or IGST_0:
#             transaction_list.append(["Input IGST", "igst_total"],)            
#         if float(bill_data['tcs_amount'])>0:
#             transaction_list.append(["TCS Receivable", "tcs_amount"],)     
        
#         acc_from_list=[]
#         acc_to_list=[]
#         for transaction in transaction_list:
#             for account_transaction in [transaction[0]]:
#                 acc_to_list.append(account_transaction)
#                 print('input tax  isisss is herer',account_transaction)
#                 if account_transaction is not None:
#                     try:
#                         #this Section is List Addded Charted Of account Updated                
#                         account_list=MasterTransaction.objects.get(to_acc_name=account_transaction,L1detail_id=bill_id.bill_id)
#                         account_list.credit=bill_data[transaction[1]]
#                         account_list.debit=bill_data[transaction[1]]
#                         account_list.save()
#                         print('Tax Suessfully updated')
            
#                     except MasterTransaction.DoesNotExist:
            
#                         print('Tax Transaction Is Created')
#             #List Of index added 0 is get Account_name
#                         TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#                         print('""""""""""""', TO_COA)
#                         billmast = MasterTransaction.objects.create(
#                             L1detail_id=bill_id.bill_id,
#                             L1detailstbl_name='Bill',
#                             main_module='Purchase',
#                             module='Bill',
#                             sub_module='Bill',
#                             transc_deatils='Bill',
#                             banking_module_type='Bill',
#                             journal_module_type='Bill',
#                             trans_date=bill_data["bill_date"],
#                             trans_status='Manually Added',
#                             debit=bill_data[transaction[1]],
#                             to_account=TO_COA.coa_id,
#                             to_acc_type=TO_COA.account_type,
#                             to_acc_head=TO_COA.account_head,
#                             to_acc_subhead=TO_COA.account_subhead,
#                             to_acc_name=TO_COA.account_name,
#                             credit=bill_data[transaction[1]],
#                             from_account=account_payable.coa_id,
#                             from_acc_type=account_payable.account_type,
#                             from_acc_head=account_payable.account_head,
#                             from_acc_subhead=account_payable.account_subhead,
#                             from_acc_name=account_payable.account_name,
#                             vendor_id=ven_id,
#                             company_id=comp_id)
#                         billmast.save()
                        
            
          
#             #  This Sectio Is Discount 
#             # Diffrance in Tax Section And Disscount Section Is Tax Side From Account Is Discount Section To Side
#             #and Discount From Side Account is Tax Side is To side
#             #Change The Credit and Debit side 
#         try:
#             #This Section is Disscount will Be find to this code will Be Excuted
#             discount_account=bill_data['discount_account']
#             if discount_account is not None:
#                 account_payable =COA.objects.get(company_id=comp_id, coa_id=discount_account)
#                 discount_acc_name=account_payable.account_name 
#                 item_discount_list=MasterTransaction.objects.get(to_acc_name=discount_acc_name,L1detail_id=bill_id)
            
#                 item_discount_list.credit=bill_data['discount']
#                 item_discount_list.debit=bill_data['discount']
#                 item_discount_list.save()
            
#         # This Section List are addded the Disscount Create mastertransaction new entry    
#         except MasterTransaction.DoesNotExist:
#             if float(bill_data['discount'])>0:
                  
#                 discount_account=bill_data['discount_account']
#                 TO_COA = COA.objects.get(coa_id=account_payable.coa_id)
#                 account_payable =COA.objects.get(company_id=comp_id, coa_id=discount_account)
#                 discount_acc_name=account_payable.account_name 
#                 acc_from_list.append(discount_acc_name)
#                 print('Discount Account is',discount_acc_name)
                

#                 print('""""""""""""', TO_COA)
#                 billmast = MasterTransaction.objects.create(
#                     L1detail_id=bill_id.bill_id,
#                     L1detailstbl_name='Bill',
#                     main_module='Purchase',
#                     module='Bill',
#                     sub_module='Bill',
#                     transc_deatils='Bill',
#                     banking_module_type='Bill',
#                     journal_module_type='Bill',
#                     trans_date=bill_data["bill_date"],
#                     trans_status='Manually Added',
#                     debit=bill_data['discount'],
#                     to_account=TO_COA.coa_id,
#                     to_acc_type=TO_COA.account_type,
#                     to_acc_head=TO_COA.account_head,
#                     to_acc_subhead=TO_COA.account_subhead,
#                     to_acc_name=TO_COA.account_name,
#                     credit=bill_data['discount'],
#                     from_account=account_payable.coa_id,
#                     from_acc_type=account_payable.account_type,
#                     from_acc_head=account_payable.account_head,
#                     from_acc_subhead=account_payable.account_subhead,
#                     from_acc_name=account_payable.account_name,
#                     vendor_id=ven_id,
#                     company_id=comp_id)
#                 billmast.save()
        
#             transaction_list_tds=[]
#             if float(bill_data['tds_amount'])>0:
#                 transaction_list_tds.append(["TDS Payable", "tds_amount"],)
#                 for transaction in transaction_list_tds:
#                     print(transaction)
#                     #List Of index added 0 is get Account_name
#                     TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#                     print('""""""""""""', TO_COA)
#                     billmast = MasterTransaction.objects.create(
#                         L1detail_id=bill_id.bill_id,
#                         L1detailstbl_name='Bill',
#                         main_module='Purchase',
#                         module='Bill',
#                         sub_module='Bill',
#                         transc_deatils='Bill',
#                         banking_module_type='Bill',
#                         journal_module_type='Bill',
#                         trans_date=bill_data["bill_date"],
#                         trans_status='Manually Added',
#                         debit=bill_data[transaction[1]],
#                         to_account=account_payable.coa_id,
#                         to_acc_type=account_payable.account_type,
#                         to_acc_head=account_payable.account_head,
#                         to_acc_subhead=account_payable.account_subhead,
#                         to_acc_name=account_payable.account_name,
#                         credit=bill_data[transaction[1]],
#                         from_account=TO_COA.coa_id,
#                         from_acc_type=TO_COA.account_type,
#                         from_acc_head=TO_COA.account_head,
#                         from_acc_subhead=TO_COA.account_subhead,
#                         from_acc_name=TO_COA.account_name,
#                         vendor_id=ven_id,
#                         company_id=comp_id)
#                     billmast.save()

    
        
#        #This Section is Item Transaction The Item transaction Can't Created Is only updated 
#        #this only Chnage the Credit and debit Side values 
#        #Other can;t Change
    
    
    
    
#         #This Section is Item chart of account and amount group by section
       
                   
#         #this Section Is Mastertransction item related 
        
        
#         print('Stock item list is ',stock_item_list,'bill id is',bill_id)
#         trans_stock_list= Stock.objects.filter(ref_id=bill_id.bill_id).exclude(item_id__in=stock_item_list)
#         print('Start The item Is ready to delete',trans_stock_list)
#         for trans_stock in trans_stock_list:
#             mast_stock=trans_stock.st_id
#             transaction_stock= MasterTransaction.objects.filter(L1detail_id=bill_id.bill_id,L2detail_id=str(mast_stock)).delete()
#             print('Deleted Stock Transaction item Name is ',transaction_stock)
        
#         del_stock= Stock.objects.filter(ref_id=bill_id.bill_id).exclude(item_id__in=stock_item_list).delete()
#         print('Ohhh Stock is deleted',del_stock)
        
     
        
#       #this Section Is the Delete the Trnsaction Not Fined is List Mens Remove the Transaction
#         #master_stock variable is the remaning of stock item in master transaction
#         master_stock_list=[]
#         master_stock= MasterTransaction.objects.filter(L1detail_id=bill_id.bill_id,L2detailstbl_name='Stock')
#         for stock_trans_mast in master_stock:
#             master_stock_list.append(stock_trans_mast.to_acc_name)
#         print('acc List Is here',acc_to_list)
#         print('master_stock_list is herer',master_stock_list)
#         to_and_from=acc_from_list+acc_to_list
#         Both_List=to_and_from+master_stock_list
       
#         topics = MasterTransaction.objects.filter(L1detail_id=bill_id.bill_id).exclude(to_acc_name__in=Both_List).exclude(from_acc_name__in=Both_List).delete()
#         print('Both List Is here',Both_List)
#         bill_item_list=Bill_Item.objects.filter(bill_id=bill_id.bill_id).exclude(item_id__in=stock_item_list).delete()

#         serializer = BillSerializer(bill_id)    
#         return Response(serializer.data)
        
        
# @api_view(['GET'])
# def getbillitembybillid(request, bill_id):
#     object = Bill_Item.objects.filter(bill_id=bill_id)
#     serializer = GETBillItemSerializer(object, many=True)
#     return Response(serializer.data)  

# @api_view(['GET'])
# def getdebitnoteitembydn_id(request, dn_id):
#     object = DebitItem.objects.filter(dn_id=dn_id)
#     serializer = UpdatesDebitnoteItemSerializer(object, many=True)
#     return Response(serializer.data)        





# class DebitnoteUpdate3ViewSet(viewsets.ModelViewSet):
#     queryset = DebitNote.objects.all()
#     serializer_class = DebitnoteSerializer
#     def update(self, request, pk, *args, **kwargs):
#         debitnote_data=request.data
#         debitnote = DebitNote.objects.get(dn_id=pk)
#         comp_id = Company.objects.get(company_id=debitnote_data["company_id"])
#         ven_id = Vendor.objects.get(
#             vendor_id=debitnote_data["vendor_id"])
        
#         #account receivable varibale are declaret the chart of account of to side from item and taxation Section 
#         #and Discount time this chartof Account is From Side
       
#         # Invoice Item Looping
#         debitnote_item_list=[]
#         for debitnote_item_data in debitnote_data['debit_note_items']:
#            # Item are find Out Section
#             debitnote_item_list.append(debitnote_item_data['item_id'])
          
#             try:
#                 try:
#                     debitnote_item = DebitItem.objects.get(item_id=debitnote_item_data['item_id'],dn_id=debitnote.dn_id)
                    
#                 except KeyError:
#                     debitnote_item=None
                    
                  
                        
#             except DebitItem.DoesNotExist:
#                 debitnote_item=None
            
#             # Invoice Item Are Find the update this Code Section   
#             if debitnote_item is not None:
                
#                 item_serializer=DebitNoteItemSerializer(debitnote_item,data=debitnote_item_data)
#                 if item_serializer.is_valid():
#                     item_serializer.save()
#                 else:
#                     return Response(item_serializer.errors, status=400)
                   
#             else:
#                 try:
#                     # Get The Chart Of Account and item Id Of the Item Related
#                     coa=COA.objects.get(coa_id=debitnote_item_data["coa_id"])
#                     item=Item.objects.get(item_id=debitnote_item_data["item_id"])
#                 except KeyError:
#                     coa=None
#                     item=None
                
#                 try:
#                     #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
#                    debitnoteed_items = DebitItem.objects.create(dn_id=debitnote,
#                                                          item_id=Item.objects.get(
#                                                              item_id=debitnote_item_data["item_id"]),
#                                                          coa_id=COA.objects.get(
#                                                              coa_id=debitnote_item_data["coa_id"]),
#                                                          item_name=debitnote_item_data["item_name"],
#                                                          rate=debitnote_item_data["rate"],
#                                                          quantity=debitnote_item_data["quantity"],
#                                                          tax_rate=debitnote_item_data["tax_rate"],
#                                                          tax_name=debitnote_item_data["tax_name"],
#                                                          tax_type=debitnote_item_data["tax_type"],
#                                                          taxamount=debitnote_item_data["taxamount"],
#                                                          igst_amount=debitnote_item_data['igst_amount'],
#                                                          cgst_amount=debitnote_item_data['cgst_amount'],
#                                                          sgst_amount=debitnote_item_data['sgst_amount'],
#                                                          amount=debitnote_item_data["amount"])
#                 except KeyError:
#                     pass                 
                
                    
                
#         del_item = DebitItem.objects.filter(dn_id=debitnote.dn_id).exclude(item_id__in=debitnote_item_list).delete()      
#         #this Section Is Invoice Data Update Serializer Through
#         serializer = DebitnoteSerializer(debitnote, data=debitnote_data)

#         if serializer.is_valid():
#             debitnote_id=serializer.save()
            
#             # return Response({"data":serializer.data})
#         else:
#              return Response(serializer.errors, status=400)
         
         
#         stock_item_list=[]
#         stock_transactiom_item_list=[]
      
#         for debitnote_item_stock in debitnote_data['debit_note_items']:
#             stock_item_list.append(debitnote_item_stock['item_id'])
#             try:
#                 stock_item=Stock.objects.get(item_id=debitnote_item_stock['item_id'],ref_id=debitnote.dn_id)
#                 item_value=Item.objects.get(item_id=debitnote_item_stock["item_id"])
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                 # stock_serializer=StockSerializer(stock_item,data=invoice_item_data)
#                 print("updating stock", debitnote_item_stock['quantity'], debitnote_item_stock['item_id'])
#                 stock_item.stock_out=float (debitnote_item_stock['quantity'])
#                 stock_item.rate=float (current_assets_last_stock.rate)
#                 stock_item.amount=float(current_assets_last_stock.rate) * float(debitnote_item_stock['quantity'])
#                 stock_item.quantity=float (debitnote_item_stock['quantity'])
#                 stock_item.save()
#                 stock_transactiom_item_list.append(stock_item)
#             except Stock.DoesNotExist:
            
            
#                 item_value=Item.objects.get(item_id=debitnote_item_stock["item_id"])
#                 items_inventory=debitnote_data.get('debit_note_items')
#                 track_inventory=items_inventory[0].get('selected_item_name',{}).get('track_inventory')
#                 inv_item_coa=items_inventory[0].get('selected_item_name',{}).get('inventory_account')
                
#                 print('inventory item coa',inv_item_coa)
                        
#                 if track_inventory==True:
                    
        
#                     stk_in=Stock.objects.filter(item_id=debitnote_item_stock["item_id"]).exclude(stock_in=0).order_by('created_date')
#                     stk_out=Stock.objects.filter(item_id=debitnote_item_stock["item_id"]).exclude(stock_out=0).order_by('created_date')        
                
#                     print(stk_out)
#                     stock_int_items = stk_in
#                     already_stock_out_items =stk_out
#                     item_to_sell = debitnote_item_stock["quantity"]
#                     print('item_to_sell',item_to_sell)

#                     # -------------------------------------------------

#                     # Check if the stock is available
#                     sum_of_stock_in = sum([_.stock_in for _ in stock_int_items])
#                     print('sum of stock in',sum_of_stock_in)
#                     sum_of_stock_in_amount = sum([_.amount for _ in stock_int_items])
#                     print("sum_of_stock_in_amount", sum_of_stock_in_amount)

#                     sum_of_already_stock_out = sum([_.stock_out for _ in already_stock_out_items])
#                     print("sum_of_already_stock_out", sum_of_already_stock_out)

#                     if sum_of_stock_in - (sum_of_already_stock_out + item_to_sell) < 0:
#                         print("Stock not available")
#                         return Response('Stock Not Avilable')

#                     print("Stock available")
#                     current_stock=sum_of_stock_in-sum_of_already_stock_out
#                     print('item is herer',item_value.item_id)        
#                     current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                     print("current Assets_vlaue",current_assets_last_stock.amount)
#                     future_stock_outs = []
#                     for stock_in_item in stock_int_items:
#                         print(stock_in_item)
                        
#                         if item_to_sell==0:
#                             print('Item Are not selled')
#                             break
#                         else:
#                             if sum_of_already_stock_out - stock_in_item.stock_in >= 0:
#                                 print("\tItem fully sold")
#                                 sum_of_already_stock_out = sum_of_already_stock_out - stock_in_item.stock_in
#                                 print("\tRemaining already sold items: ", sum_of_already_stock_out)
#                                 continue

#                             if sum_of_already_stock_out > 0:
#                                 print("\tItem partially unsold")
#                                 remaining_unsold_items = stock_in_item.stock_in - sum_of_already_stock_out
#                                 print("\tRemaining unsold items", remaining_unsold_items)
#                                 sum_of_already_stock_out = 0
#                             else:
#                                 print("\tItem fully unsold")
#                                 remaining_unsold_items = stock_in_item.stock_in
                            
#                             if item_to_sell > remaining_unsold_items:
#                                 print("\tMore items need to be sold")
#                                 print(f"\tSelling {remaining_unsold_items} items")
                                
#                                 future_stock_outs=Stock.objects.create(
#                                 item_id=debitnote_item_stock["item_id"],
#                                 item_name=debitnote_item_stock["item_name"],
#                                 stock_out=remaining_unsold_items,
#                                 ref_id=debitnote_id.dn_id,
#                                 amount=current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate,
#                                 rate=stock_in_item.rate,
#                                 ref_tblname='Debit Note',
#                                 quantity=remaining_unsold_items,
#                                 #stock_on_hand=current_stock-remaining_unsold_items,
#                                 formname='Debit Note',
#                                 module='Purchase',
#                                 stage='Add Stages',
#                                 date=debitnote_data["dn_date"],                
#                                 company_id=comp_id)
#                                 current_assets_last_stock.amount = current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate
#                                 current_stock = current_stock-remaining_unsold_items
                                
                                    
#                                 #Stock(0, remaining_unsold_items, stock_in_item.rate)
#                                 item_to_sell = item_to_sell - remaining_unsold_items
#                                 print(f"\t{item_to_sell} still needed by the buyer")
#                             else:
#                                 print(f"\tSelling {item_to_sell} items")
#                                 future_stock_outs=Stock.objects.create(
#                                 item_id=debitnote_item_stock["item_id"],
#                                 item_name=debitnote_item_stock["item_name"],
#                                 stock_out=item_to_sell,
#                                 ref_id=debitnote_id.dn_id,
#                                 amount=current_assets_last_stock.amount- item_to_sell*stock_in_item.rate,
#                                 rate=stock_in_item.rate,
#                                 quantity=item_to_sell,
#                                 ref_tblname='DebitNote',
#                                 #stock_on_hand=current_stock-item_to_sell,
#                                 module='Purchase',
#                                 formname='Debit Note',
#                                 stage='Add Stages',
#                                 date=debitnote_data["dn_date"],                
#                                 company_id=comp_id)
                                
#                                 #append(Stock(0, item_to_sell, stock_in_item.rate))
#                                 item_to_sell = 0
                                


#             #This Section Is Stock Journal Transaction 
#             #Stock Charetd Account name is Inventory Assets
#                         # print('item rate',future_stock_outs.rate)
#                         # print('item quantity',future_stock_outs.quantity)
                        
#                             print('Journa created starts')
#                             account_payable =  COA.objects.get(company_id=comp_id,coa_id=inv_item_coa)
#                             TO_COA = COA.objects.get(company_id=comp_id, coa_id=debitnote_item_stock['coa_id'])
#                             stkmast = MasterTransaction.objects.create(
#                                 L1detail_id=debitnote_id.dn_id,
#                                 L1detailstbl_name='DebitNote',
#                                 L2detail_id=future_stock_outs.st_id,
#                                 L2detailstbl_name='Stock',
#                                 main_module='Purchase',
#                                 module='DebitNote',
#                                 sub_module='DebitNote',
#                                 transc_deatils='DebitNote',
#                                 banking_module_type='DebitNote',
#                                 journal_module_type='DebitNote',
#                                 trans_date=debitnote_data["dn_date"],
#                                 trans_status='Manually Added',
#                                 debit=future_stock_outs.rate*future_stock_outs.quantity,
#                                 to_account=TO_COA.coa_id,
#                                 to_acc_type=TO_COA.account_type,
#                                 to_acc_head=TO_COA.account_head,
#                                 to_acc_subhead=TO_COA.account_subhead,
#                                 to_acc_name=TO_COA.account_name,
#                                 credit=future_stock_outs.rate*future_stock_outs.quantity,
#                                 from_account=account_payable.coa_id,
#                                 from_acc_type=account_payable.account_type,
#                                 from_acc_head=account_payable.account_head,
#                                 from_acc_subhead=account_payable.account_subhead,
#                                 from_acc_name=account_payable.account_name,
#                                 company_id=comp_id,
#                                 vendor_id=ven_id)
#                             stkmast.save()
#                             print(stkmast.from_acc_type)
        
        
        
        
#         # 0%GST and 0%IGST Calculation
#         #0% Tax Is User Select
#         Zero_tax=debitnote_data.get('debit_note_items')
#         GST_TAX=None
#         if GST_TAX==Zero_tax[0]is not None:
#             GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
        
        
            
#         else:
#             pass
    

#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX   
            
#         else:
#             Both_Tax=None
           
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None

#         transaction_list = [] #This Empty List added the append 
#         if float(debitnote_data['cgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Input CGST", "cgst_total"],)
#         if float(debitnote_data['sgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Input SGST", "sgst_total"])
#         if float(debitnote_data['igst_total'])>0 or IGST_0:
#             transaction_list.append(["Input SGST", "igst_total"],)       
        
        
#         acc_from_list=[]
#         acc_to_list=[]
#         account_payable = COA.objects.get(company_id=comp_id, account_subhead='Account Payables')

#         for transaction in transaction_list:
               
#             for account_transaction in [transaction[0]]:
#                 acc_to_list.append(account_transaction)
#                 if account_transaction is not None:
#                     try:
#                         #this Section is List Addded Charted Of account Updated                
#                         account_list=MasterTransaction.objects.get(from_acc_name=account_transaction,L1detail_id=debitnote.dn_id)
#                         account_list.credit=debitnote_data[transaction[1]]
#                         account_list.debit=debitnote_data[transaction[1]]
#                         account_list.save()   
                   
#                     except MasterTransaction.DoesNotExist:
#                         FROM_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#                         dnmast = MasterTransaction.objects.create(
#                         L1detail_id=debitnote_id.dn_id,
#                         L1detailstbl_name='Debit Note',
#                         main_module='Purchase',
#                         module='Purchase',
#                         sub_module='DebitNote',
#                         transc_deatils='Debit Note Transaction',
#                         banking_module_type='Debit Note',
#                         journal_module_type='Debit Note',
#                         trans_date=debitnote_data["dn_date"],
#                         trans_status='Manually Added',
#                         debit=debitnote_data[transaction[1]],
#                         to_account=account_payable.coa_id,
#                         to_acc_type=account_payable.account_type,
#                         to_acc_head=account_payable.account_head,
#                         to_acc_subhead=account_payable.account_subhead,
#                         to_acc_name=account_payable.account_name,
#                         credit=debitnote_data[transaction[1]],
#                         from_account=FROM_COA.coa_id,
#                         from_acc_type=FROM_COA.account_type,
#                         from_acc_head=FROM_COA.account_head,
#                         from_acc_subhead=FROM_COA.account_subhead,
#                         from_acc_name=FROM_COA.account_name,
#                         company_id=comp_id,
#                         vendor_id=ven_id)
#                         dnmast.save()
            
                      
#         try:
#             #This Section is Disscount will Be find to this code will Be Excuted
#             try:
#                 discount_account=debitnote_data['discount_account']
#                 account_discount =COA.objects.get(company_id=comp_id, coa_id=discount_account)
#                 discount_acc_name=account_discount.account_name  
#                 item_discount_list=MasterTransaction.objects.get(to_acc_name=discount_acc_name,L1detail_id=debitnote.dn_id)
#                 print('discount list',item_discount_list)
#                 item_discount_list.credit=debitnote_data['discount']
#                 item_discount_list.debit=debitnote_data['discount']
#                 item_discount_list.save()
#                 print('discount Section is Updated Suessfully')
#             except:
#                 pass    
#         except MasterTransaction.DoesNotExist:
#             if float(debitnote_data['discount'])>0:
#                 discount_account=debitnote_data['discount_account']
#                 TO_COA =COA.objects.get(company_id=comp_id, coa_id=discount_account)
#                 discount_acc_name=TO_COA.account_name   
#                 acc_from_list.append(discount_acc_name)
#                 FROM_COA =COA.objects.get(coa_id=account_payable.coa_id)
#                 dnmast = MasterTransaction.objects.create(
#                     L1detail_id=debitnote_id.dn_id,
#                     L1detailstbl_name='Debit Note',
#                     main_module='Purchase',
#                     module='Purchase',
#                     sub_module='DebitNote',
#                     transc_deatils='Debit Note Transaction',
#                     banking_module_type='Debit Note',
#                     journal_module_type='Debit Note',
#                     trans_date=debitnote_data["dn_date"],
#                     trans_status='Manually Added',
#                     debit=debitnote_data['discount'],
#                     to_account=TO_COA.coa_id,
#                     to_acc_type=TO_COA.account_type,
#                     to_acc_head=TO_COA.account_head,
#                     to_acc_subhead=TO_COA.account_subhead,
#                     to_acc_name=TO_COA.account_name,
#                     credit=debitnote_data['discount'],
#                     from_account=FROM_COA.coa_id,
#                     from_acc_type=FROM_COA.account_type,
#                     from_acc_head=FROM_COA.account_head,
#                     from_acc_subhead=FROM_COA.account_subhead,
#                     from_acc_name=FROM_COA.account_name,
#                     company_id=comp_id,
#                     vendor_id=ven_id)
#                 dnmast.save()
#     #This Section is Item Transaction The Item transaction Can't Created Is only updated 
#     #this only Chnage the Credit and debit Side values 
#     #Other can;t Change



    
#         #This Section is Item chart of account and amount group by section
#         coa_amount_dict = {}       
#         for debit_item in debitnote_data['debit_note_items']:
#             if coa_amount_dict.get(debit_item['coa_id']) is None:
#                 coa_amount_dict[debit_item['coa_id']
#                                 ] = debit_item['amount']
#             else:
#                 coa_amount_dict[debit_item['coa_id']
#                                 ] = coa_amount_dict[debit_item['coa_id']] + debit_item['amount']
            
#             for coa_id, amount in coa_amount_dict.items():
              
#                 coa_mast=MasterTransaction.objects.filter(from_account=coa_id,L1detail_id=debitnote.dn_id)
#                 for coa in coa_mast:
                    
#                     coa_acc=coa.from_acc_name
                   
                   
      
#         trans_stock_list= Stock.objects.filter(ref_id=debitnote_id.dn_id).exclude(item_id__in=stock_item_list)
#         print('Start The item Is ready to delete',trans_stock_list)
#         for trans_stock in trans_stock_list:
#             mast_stock=trans_stock.st_id
#             transaction_stock= MasterTransaction.objects.filter(L1detail_id=debitnote_id.dn_id,L2detail_id=str(mast_stock)).delete()
#             print('Deleted Stock Transaction item Name is ',transaction_stock)
        
#         del_stock= Stock.objects.filter(ref_id=debitnote_id.dn_id).exclude(item_id__in=stock_item_list).delete()
#         print('Ohhh Stock is deleted',del_stock)
        
     
        
#       #this Section Is the Delete the Trnsaction Not Fined is List Mens Remove the Transaction
#         #master_stock variable is the remaning of stock item in master transaction
#         master_stock_list=[]
#         master_stock= MasterTransaction.objects.filter(L1detail_id=debitnote_id.dn_id,L2detailstbl_name='Stock')
#         for stock_trans_mast in master_stock:
#             master_stock_list.append(stock_trans_mast.to_acc_name)
#         print('acc toList Is here',acc_to_list)
#         print('acc fromList Is here',acc_from_list)
#         print('master_stock_list is herer',master_stock_list)
#         to_and_from=acc_from_list+acc_to_list
#         Both_List=to_and_from+master_stock_list
#         print('to_and_From is herer',to_and_from)
#         topics = MasterTransaction.objects.filter(L1detail_id=debitnote_id.dn_id,).exclude(to_acc_name__in=Both_List).exclude(from_acc_name__in=Both_List).delete()
#         print('Both List Is here',Both_List)
#         dn_item_list=DebitItem.objects.filter(dn_id=debitnote_id.dn_id,).exclude(item_id__in=stock_item_list).delete()

          
#         serializer = DebitnoteSerializer(debitnote_id)  # browser
#         return Response(serializer.data)
    
    
    