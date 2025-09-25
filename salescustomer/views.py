# from re import template
# import re
# from sre_constants import IN
# from tkinter import E, NO
# from urllib import response
# from uuid import uuid4
# import pandas as pd
# from django.db.models import Sum
# from django.shortcuts import render
# from numpy import True_, not_equal
# from rest_framework import views, viewsets, generics, mixins
# from rest_framework.response import Response
# from company.models import Company, Branch
# from transaction .models import MasterTransaction
# from transaction .serializers import MasterTransactionSerializer
# from coa.models import COA
# from .models_old import *
# from .serializers import *  # SalesCustomerSerializer,ShortCustomerSerializer, ShortEstimateSerializer, EstimateSerializer, SOSerializer, InvoiceSerializer, DCSerializer, PRSerializer, RISerializer, CreditNoteSerializer
# from rest_framework.decorators import api_view, action
# from rest_framework.generics import ListAPIView
# import itertools
# from company.serializers import *
# from operator import itemgetter
# from abc import abstractmethod
# from django.shortcuts import render
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from django.views.generic import View
# import json
# from wsgiref.util import FileWrapper
# import os
# from pathlib import Path
# from io import BytesIO
#
# import datetime
# from django.http import HttpResponse, FileResponse
# from .generate_invoice import generate_invoice_pdf
# from .generate_cn import generate_credit_note_pdf
# from django.shortcuts import render
# from .generate_est import generate_estimate_pdf
# from .generate_so import generate_so_pdf
# from .generate_dc import generate_dc_pdf
# from .generate_pr import generate_pr_pdf
# from banking .models import *
# from banking .serializers import *
# import pdfkit
# from .generate_ca import generate_customer_advance_pdf
# # Create your views here.
# # POST Estimate Items
#
#
# class estimateitemsViewSet(viewsets.ModelViewSet):
#     queryset = EstimatedItem.objects.all()
#     serializer_class = EstimatedItemSerializer
#
#     def create(self, request, *args, **kwargs):
#         estimate_data_converte = request.data['data']
#
#
#         # PR Convert Str to Dict Code
#         estimate_data = json.loads(estimate_data_converte)
#         #estimate_data=estimate_data_converte
#         print("Converted Format is", type(estimate_data))
#
#         estimate_file_data = request.FILES.get('attach_file')
#         print("estimate_data", type(estimate_file_data))
#
#         employee_id = estimate_data["emp_id"]
#         if employee_id is not None:
#             employee_id = Employee.objects.get(emp_id=employee_id)
#
#         try:
#             tcs_id = estimate_data["tcs_id"]
#             if tcs_id is not None:
#                 tcs_id = TCS.objects.get(tcs_id=tcs_id)
#         except KeyError:
#             tcs_id=None
#
#         Branch_id = estimate_data["branch_id"]
#         if Branch_id is not None:
#             Branch_id = Branch.objects.get(branch_id=Branch_id)
#
#         estimate_items = estimate_data["estimate_items"]
#         comp_id = Company.objects.get(company_id=estimate_data["company_id"])
#         cust_id = SalesCustomer.objects.get(
#             customer_id=estimate_data["customer_id"])
#
#         # Estimate fields
#         estimate_id = Estimate.objects.create(est_ref_no=estimate_data["est_ref_no"],
#                                               est_date=estimate_data["est_date"],
#                                               est_status=estimate_data["est_status"],
#                                               est_serial=estimate_data["est_serial"],
#                                               # notes=estimate_data["notes"],
#                                               # journal_type=estimate_data["journal_type"],
#                                               is_estimate_generated=estimate_data["is_estimate_generated"],
#                                               # attach_file=estimate_data["attach_file"],
#                                               customer_note=estimate_data["customer_note"],
#                                               discount=estimate_data["discount"],
#                                               entered_discount=estimate_data["entered_discount"],
#                                               entered_shipping_charges=estimate_data["entered_shipping_charges"],
#                                               shipping_charges=estimate_data["shipping_charges"],
#                                               shipping_tax_name=estimate_data["shipping_tax_name"],
#                                               shipping_tax_rate=estimate_data["shipping_tax_rate"],
#                                               subject=estimate_data["subject"],
#                                               supply_place=estimate_data["supply_place"],
#                                               terms_condition=estimate_data["terms_condition"],
#                                               total_gst=estimate_data["total_gst"],
#                                               # total_quantity=estimate_data["total_quantity"],
#                                               expiry_date=estimate_data["expiry_date"],
#                                               tcs_amount=estimate_data["tcs_amount"],
#                                               sub_total=estimate_data["sub_total"],
#                                               total=estimate_data["total"],
#                                               # amount=estimate_data["amount"],
#                                               cgst_total=estimate_data['cgst_total'],
#                                               sgst_total=estimate_data['sgst_total'],
#                                               igst_total=estimate_data['igst_total'],
#                                               attach_file=estimate_file_data,
#                                               company_id=comp_id,
#                                               branch_id=Branch_id,
#                                               customer_id=cust_id,
#                                               tcs_id=tcs_id,
#                                               emp_id=employee_id)
#         estimate_id.save()
#
#         if estimate_file_data is not None:
#             file_ext = os.path.splitext(estimate_file_data.name)[1]
#             new_file_path = f'media/Estimate_{estimate_id.est_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in estimate_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             estimate_id.attach_file = pth
#             estimate_id.save()
#
#         print("estimate_items", estimate_items, type(estimate_items))
#
#         for i in range(len(estimate_items)):
#             new_estimate = EstimatedItem.objects.create(est_id=estimate_id,
#                                                         item_id=Item.objects.get(
#                                                             item_id=estimate_items[i]["item_id"]),
#                                                         # customer_id = SalesCustomer.objects.get(customer_id=estimate_items[i]["customer_id"],
#                                                         # company_id = comp_id,
#                                                         item_name=estimate_items[i]["item_name"],
#                                                         rate=estimate_items[i]["rate"],
#                                                         quantity=estimate_items[i]["quantity"],
#                                                         # tax=estimate_items[i]["tax"],
#                                                         tax_rate=estimate_items[i]["tax_rate"],
#                                                         tax_name=estimate_items[i]["tax_name"],
#                                                         tax_type=estimate_items[i]["tax_type"],
#                                                         taxamount=estimate_items[i]["taxamount"],
#                                                         cgst_amount=estimate_items[i]['cgst_amount'],
#                                                         sgst_amount=estimate_items[i]['sgst_amount'],
#                                                         igst_amount=estimate_items[i]['igst_amount'],
#                                                         amount=estimate_items[i]["amount"])
#             new_estimate.save()
#             print(i, "estimate_items")
#         serializer = EstimatedItemSerializer(new_estimate)  # browser
#         return Response(serializer.data)
#
#
# ##################################################
# # Dwonload Code Is Creting api By Download
# # Download Estimet by id
#
# class EstimateFileDownloadListAPIView(generics.ListAPIView):
#
#     def get(self, request, estimate_id, format=None):
#         queryset = Estimate.objects.get(est_id=estimate_id)
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
#
#
# #######################################################
#
#
# class EstimateGeneratePdf(View):
#     def get(self, request, estimate_id, *args, **kwargs):
#         estimate = Estimate.objects.get(est_id=estimate_id)
#         # Get The Estimate By estimate id
#         # and Then Serialize the data
#         serializer = EstimateSerializer(estimate)
#         print(serializer.data)
#         # get the Company data In Estimate (company_id) related
#         print(estimate.company_id.company_id)
#         company = Company.objects.get(
#             company_id=estimate.company_id.company_id)
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
#
#         return HttpResponse(html)
#
#
# #####################
# class EstimateDownloadPdf(View):
#     def get(self, request, *args, **kwargs):
#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')
#
#         filename = "estimate_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#
#         # rendering the template
#
#         with open(pdf_path, 'r') as f:
#             file_data = f.read()
#
#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response
#
#
# #############################################################
# ###############################################################3##########################
#
# # api for get bill by company id and bill id
# @api_view(['GET'])
# def download_est_data(request, comp_id,est_id):
#     company = Company.objects.get(company_id=comp_id)
#     est = Estimate.objects.get(est_id=est_id)
#     # here filter the object of bill id and company id
#     estimate = Estimate.objects.filter(
#         company_id=comp_id,est_id=est_id).order_by('created_date')
#     serializers =JoinEstimateItemSerializer(estimate, many=True)
#     print("8888888888888",serializers.data)
#     output_pdf = f"EST_{datetime.datetime.now().timestamp()}.pdf"
#     generate_estimate_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadest/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)
#
# def download_est(request, file_name):
#    # file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#     file_path = f"media/{file_name}"
#   #  print("""""""""""""''---------------------------------------------------------------------",output_path)
#     response = FileResponse(open( file_path,'rb'))
#   #  return FileResponse(open(output_path, 'rb'), as_attachment=True)
#
#     #response = FileResponse(file_data, as_attachment=True,
#     return response
# ################################################################################
#
#
#
# # POST Sales Order Item
# class salesorderitemsViewSet(viewsets.ModelViewSet):
#     queryset = SoItem.objects.all()
#     serializer_class = SoItemSerializer
#
#     def create(self, request, *args, **kwargs):
#         so_data_converte = request.data['data']
#         print("#################################################")
#         print(so_data_converte)
#         print("salesorderData Format is ", type(so_data_converte))
#         print("#################################################")
#         # Salesorder Convert Str to Dict Code
#         saleorder_data = json.loads(so_data_converte)
#         print("Converted Format is", type(saleorder_data))
#
#         so_file_data = request.FILES.get('attach_file')
#         print("saleorder_data", type(so_file_data))
#
#         employee_id = saleorder_data["emp_id"]
#         if employee_id is not None:
#             employee_id = Employee.objects.get(emp_id=employee_id)
#
#         # pay_id=saleorder_data["payment_id"]
#         # if pay_id is not None:
#         #     pay_id=PaymentTerms.objects.get(payment_id=pay_id)
#
#         try:
#             tcs_id = saleorder_data["tcs_id"]
#             if tcs_id is not None:
#                 tcs_id = TCS.objects.get(tcs_id=tcs_id)
#         except KeyError:
#             tcs_id=None
#
#         branch_id = saleorder_data["branch_id"]
#         if branch_id is not None:
#             branch_id = Branch.objects.get(branch_id=branch_id)
#
#         so_items = saleorder_data["so_items"]
#         comp_id = Company.objects.get(company_id=saleorder_data["company_id"])
#         # branch_id = Branch.objects.get(branch_id=estimate_data["branch_id"])
#         cust_id = SalesCustomer.objects.get(
#             customer_id=saleorder_data["customer_id"])
#
#         # Sales order fields
#         salesorder_id = SO.objects.create(so_ref_no=saleorder_data["so_ref_no"],
#                                           so_date=saleorder_data["so_date"],
#                                           so_status=saleorder_data["so_status"],
#                                           so_serial=saleorder_data["so_serial"],
#                                           is_so_generated=saleorder_data["is_so_generated"],
#                                           attach_file=so_file_data,
#                                           customer_note=saleorder_data["customer_note"],
#                                           discount=saleorder_data["discount"],
#                                           no_of_days=saleorder_data["no_of_days"],
#                                           entered_discount=saleorder_data["entered_discount"],
#                                           entered_shipping_charges=saleorder_data["entered_shipping_charges"],
#                                           shipping_charges=saleorder_data["shipping_charges"],
#                                           shipping_tax_name=saleorder_data["shipping_tax_name"],
#                                           # subject=saleorder_data["subject"],
#                                           supply_place=saleorder_data["supply_place"],
#                                           terms_condition=saleorder_data["terms_condition"],
#                                           total_gst=saleorder_data["total_gst"],
#                                           term_name=saleorder_data["term_name"],
#                                           expected_shipment_date=saleorder_data["expected_shipment_date"],
#                                           sub_total=saleorder_data["sub_total"],
#                                           total=saleorder_data["total"],
#                                           cgst_total=saleorder_data['cgst_total'],
#                                           sgst_total=saleorder_data['sgst_total'],
#                                           igst_total=saleorder_data['igst_total'],
#                                           company_id=comp_id,
#                                           branch_id=branch_id,
#                                           customer_id=cust_id,
#                                           tcs_id=tcs_id,
#                                           # payment_id = pay_id,
#                                           emp_id=employee_id)
#         salesorder_id.save()
#         if so_file_data is not None:
#             file_ext = os.path.splitext(so_file_data.name)[1]
#             new_file_path = f'media/Salesorder_{salesorder_id.so_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in so_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             salesorder_id.attach_file = pth
#             salesorder_id.save()
#
#         for i in range(len(so_items)):
#             new_soitem = SoItem.objects.create(so_id=salesorder_id,
#                                                item_id=Item.objects.get(
#                                                    item_id=so_items[i]["item_id"]),
#                                                # customer_id = SalesCustomer.objects.get(customer_id=estimate_items[i]["customer_id"],
#                                                item_name=so_items[i]["item_name"],
#                                                rate=so_items[i]["rate"],
#                                                quantity=so_items[i]["quantity"],
#                                                tax_rate=so_items[i]["tax_rate"],
#                                                tax_name=so_items[i]["tax_name"],
#                                                tax_type=so_items[i]["tax_type"],
#                                                taxamount=so_items[i]["taxamount"],
#                                                cgst_amount=so_items[i]['cgst_amount'],
#                                                sgst_amount=so_items[i]['sgst_amount'],
#                                                igst_amount=so_items[i]['igst_amount'],
#                                                amount=so_items[i]["amount"])
#             new_soitem.save()
#             print(i, "so_items")
#
#         serializer = SoItemSerializer(new_soitem)  # browser
#         return Response(serializer.data)
#
#
# ########################################################
#
# # Dwonload Code Is Creting api By Download
# # Download salesorder by id
#
#
#
#
# class SalesorderFileDownloadListAPIView(generics.ListAPIView):
#
#     def get(self, request, salesorder_id, format=None):
#         queryset = SO.objects.get(so_id=salesorder_id)
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
#             return HttpResponse('No File Found')
#
#
# ###################################################
#
#
# class SalesorderGeneratePdf(View):
#     def get(self, request, salesorder_id, *args, **kwargs):
#         so = SO.objects.get(so_id=salesorder_id)
#         # Get The Estimate By estimate id
#         # and Then Serialize the data
#         serializer = SOSerializer(so)
#         print(serializer.data)
#         # get the Company data In Estimate (company_id) related
#         print(so.company_id.company_id)
#         company = Company.objects.get(company_id=so.company_id.company_id)
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
#
#         return HttpResponse(html)
#
#
# #####################
# class SalesorderDownloadPdf(View):
#     def get(self, request, *args, **kwargs):
#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')
#
#         filename = "salesorder_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#
#         # rendering the template
#
#         with open(pdf_path, 'r') as f:
#             file_data = f.read()
#
#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response
#
#
# #############################################################
# #############################################################
# ###############################################################3##########################
#
#
# # api for get bill by company id and bill id
# @api_view(['GET'])
# def download_so_data(request, comp_id,so_id):
#     company = Company.objects.get(company_id=comp_id)
#     so = SO.objects.get(so_id=so_id)
#     # here filter the object of bill id and company id
#     sls = SO.objects.filter(
#         company_id=comp_id,so_id=so_id).order_by('created_date')
#     serializers = JoinSoItemSerializer(sls, many=True)
#     output_pdf=f"SO_{datetime.datetime.now().timestamp()}.pdf"
#     generate_so_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadso/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)
#
# def download_so(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,
#     return response
# ################################################################################
#
# class customerViewSet(viewsets.ModelViewSet):
#     queryset = SalesCustomer.objects.all()
#     serializer_class = SalesCustomerSerializer
#
#     def create(self, request, *args, **kwargs):
#         print("/////",request.data)
#         customer_data_converte = request.data['data']
#         #Convert Str to Dict Code
#         customer_data = json.loads(customer_data_converte)
#
#         customer_file_data = request.FILES.get('invoice_template')
#         print("customer_file_data", type(customer_file_data))
#         comp_id = Company.objects.get(company_id=customer_data["company_id"])
#
#
#         cust_serializer = NewSalesCustomerSerializer(data=customer_data)
#         if cust_serializer.is_valid():
#             customer_id = cust_serializer.save()
#             customer_id.invoice_template = customer_file_data
#             customer_id.save()
#
#
#         else:
#             return Response(cust_serializer.errors)
#
#         if customer_file_data is not None:
#             print("********************* customer_file_data ",customer_file_data)
#             file_ext = os.path.splitext(customer_file_data.name)[1]
#             new_file_path = f'media/Invoice_{customer_id.customer_id}{file_ext}'
#             print("------------------------------, new_file_path", new_file_path)
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in customer_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             customer_id.invoice_template = pth
#             customer_id.save()
#
#         serializer = NewSalesCustomerSerializer(customer_id)  # browser
#         print(" output serializer data",serializer.data)
#         return Response({"data":serializer.data,"status":200})
#
#
#
#
# class customerList(generics.ListAPIView):
#     queryset = SalesCustomer.objects.all()
#     serializer_class = SalesCustomerSerializer
#
#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def customerCreation(self, request):
#         customer = SalesCustomer.objects.all()
#         serializer = SalesCustomerSerializer(customer, many=True)
#         return Response(serializer.data)
#
#
# # customer and opening balance join
# class CustomerGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = SalesCustomer.objects.all()
#     serializer_class = JoinCustomerSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return Response({
#                 'data': self.retrieve(request, pk).data
#             })
#         return self.list(request)
#
#     # post for customer opening balance(addcustomerob)
#
#
# class customerobViewSet(viewsets.ModelViewSet):
#     queryset = SalesCustomer.objects.all()
#     serializer_class = CustomerObSerializer
#
#     @api_view(['POST'])
#     def customerob(request):
#         customer = SalesCustomer.objects.all()
#         serializer = SalesCustomerSerializer(
#             instance=customer, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#
#
# # getshortDetails
# @api_view(['GET'])
# def ShortCustomerDetails(request):
#     customer = SalesCustomer.objects.all()
#     serializer = ShortCustomerSerializer(customer, many=True)
#     return Response(serializer.data)
#
#
# # getcustomerbyname
# @api_view(['GET'])
# def customername(request):
#     customer = SalesCustomer.objects.all()
#     serializer = customernameSerializer(customer, many=True)
#     return Response(serializer.data)
#
#
# # #getcustomershortbycompanyid()
# # @api_view(['GET'])
# # def customershortbycompanyid(request, comp_id):
# #     customer = SalesCustomer.objects.get(company_id=comp_id)
# #     serializer = customershortbycompanySerializer(customer, many=False)
# #     return Response(serializer.data)
#
# # getcustomershortbycompanyid(demo currently live)
# @api_view(['GET'])
# def customershortbycompanyid(request, comp_id):
#     comapny = Company.objects.get(company_id=comp_id)
#     customer = SalesCustomer.objects.filter(company_id=comapny)
#     serializer = customershortbycompanySerializer(customer, many=True)
#     return Response(serializer.data)
#
#
# # getcustomerbyid
# @api_view(['GET'])
# def customerDetail(request, pk):
#     customer = SalesCustomer.objects.get(customer_id=pk)
#     serializer = SalesCustomerSerializer(customer, many=False)
#     return Response(serializer.data)
#
#
# # update customer
# @api_view(['POST'])
# def customerUpdate(request, pk):
#     customer = SalesCustomer.objects.get(customer_id=pk)
#     serializer = SalesCustomerSerializer(instance=customer, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# # opening balance for customer
# @api_view(['PUT'])
# def customerobUpdate(request, pk):
#     openingbalance = CustomerOB.objects.get(ob_id=pk)
#     serializer = CustomerObSerializer(
#         instance=openingbalance, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# # PAYMENT TERMS
# class paymenttermViewSet(
#         viewsets.ModelViewSet):  # provision to add data from API by providing HTML form also we can see posted data
#     queryset = PaymentTerms.objects.all()
#     serializer_class = PaymentTermSerializer
#
#     # class paymenttermList(generics.ListAPIView):
#     # queryset = PaymentTerms.objects.all()
#     # serializer_class = PaymentTermSerializer
#
#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def paymenttermCreation(self, request):
#         paymentterm = PaymentTerms.objects.all()
#         serializer = PaymentTermSerializer(paymentterm, many=True)
#         return Response(serializer.data)
#
#
# # Employee
# class employeeViewSet(
#         viewsets.ModelViewSet):  # provision to add data from API by providing HTML form also we can see posted data
#     queryset = Employee.objects.all()
#     serializer_class = employeeSerializer
#
#
# class employeeList(generics.ListAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = employeeSerializer
#
#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def employeeCreation(request):
#         employee = Employee.objects.all()
#         serializer = employeeSerializer(employee, many=True)
#         return Response(serializer.data)
#
#
# # TCS
# class tcsViewSet(
#         viewsets.ModelViewSet):  # provision to add data from API by providing HTML form also we can see posted data
#     queryset = TCS.objects.all()
#     serializer_class = tcsSerializer
#
#
# class tcsList(generics.ListAPIView):
#     queryset = TCS.objects.all()
#     serializer_class = tcsSerializer
#
#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def tcsCreation(request):
#         tcs = TCS.objects.all()
#         serializer = tcsSerializer(tcs, many=True)
#         return Response(serializer.data)
#
#
# # ESTIMATE
# class estimateViewSet(viewsets.ModelViewSet):
#     queryset = Estimate.objects.all()
#     serializer_class = EstimateSerializer
#
#
# class estimateList(generics.ListAPIView):
#     queryset = Estimate.objects.order_by('created_date')
#     serializer_class = EstimateSerializer
#
#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def estimateCreation(self, request):
#         estimate = Estimate.objects.all()
#         serializer = EstimateSerializer(estimate, many=True)
#         return Response(serializer.data)
#
#
# # estimateshortbycompanyid
# @api_view(['GET'])
# def getestimateshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     estimate = Estimate.objects.filter(company_id=company)
#     serializer = EstimateSerializer(estimate, many=True)
#    # serializer = JoinItemSerializer(estimate, many=True)
#     return Response(serializer.data)
#
#
# # getshortDetails
# @api_view(['GET'])
# def ShortEstimateDetails(request):
#     estimate = Estimate.objects.all()
#     serializer = ShortEstimateSerializer(estimate, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def estimateDetail(request, pk):
#     estimate = Estimate.objects.get(est_id=pk)
#     serializer = EstimateSerializer(estimate, many=False)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# def estimateUpdate(request, pk):
#     estimate = Estimate.objects.get(est_id=pk)
#     serializer = EstimateSerializer(instance=estimate, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# # Estimate and Item join
# class EstimateGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = Estimate.objects.all()
#     serializer_class = JoinItemSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return Response({
#                 'data': self.retrieve(request, pk).data
#             })
#         return self.list(request)
#
#     # Estimateditem and Estimate join
#
#
# class EstimatedItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = Estimate.objects.all()
#     serializer_class = JoinEstimateItemSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'salescustomer/estimatefile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)
#
#     # API for Sales Order
#
#
# class soViewSet(viewsets.ModelViewSet):
#     queryset = SO.objects.all()
#     serializer_class = SOSerializer
#
#
# class soList(generics.ListAPIView):
#     queryset = SO.objects.all()
#     serializer_class = SOSerializer
#
#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def soCreation(request):
#         so = SO.objects.all()
#         serializer = SOSerializer(so, many=True)
#         return Response(serializer.data)
#
#
# # salesordershortbycompanyid
# @api_view(['GET'])
# def getsalesordershortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     salesorder = SO.objects.filter(company_id=company)
#     serializer =SOSerializer(salesorder, many=True) #
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def soDetail(request, pk):
#     so = SO.objects.get(id=pk)
#     serializer = SOSerializer(so, many=False)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# def soUpdate(request, pk):
#     so = SO.objects.get(id=pk)
#     serializer = SOSerializer(instance=so, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# # getshortDetails
# @api_view(['GET'])
# def ShortSalesOrderDetails(request):
#     so = SO.objects.all()
#     serializer = ShortSalesOrderSerializer(so, many=True)
#     return Response(serializer.data)
#
#
# # API POST for soitem
# class soitemViewSet(viewsets.ModelViewSet):
#     queryset = SoItem.objects.all()
#     serializer_class = SoItemSerializer
#
#
# class soitemList(generics.ListAPIView):
#     queryset = SoItem.objects.all()
#     serializer_class = SoItemSerializer
#
#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def soitemCreation(request):
#         soitem = SoItem.objects.all()
#         serializer = SoItemSerializer(soitem, many=True)
#         return Response(serializer.data)
#
#
# # Soitem and SO join
# class SoItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = SO.objects.all()
#     serializer_class = JoinSoItemSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'salescustomer/salesorderfile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)
#
#     #########################################################################################
#
#
# # Invoice journal transaction
# # API for Invoice
# # POST Invoice Items
#
#
#
#
#
#
#
# ##############
# # get invoice api
#
#
# @api_view(['GET'])
# def getinvoicebyinvoiceid(request, invoice_id):
#     object = Invoice.objects.get(invoice_id=invoice_id)
#     serializer = JoinInvoiceAndInvoiceItemSerializer(object, many=False)
#     return Response(serializer.data)
#
#
# #GST 2A Reports
# @api_view(['GET'])
# def get2Areports(request, company_id):
#     object = Invoice.objects.filter(company_id=company_id)
#     serializer = InvoiceAndInvoiceItem2ASerializer(object, many=False)
#     return Response(serializer.data)
#
# # Dwonload Code Is Creting api By Download
# # Download Invoice by id Attach File Download
#
#
# class FileDownloadListAPIView(generics.ListAPIView):
#
#     def get(self, request, invoice_id, format=None):
#         queryset = Invoice.objects.get(invoice_id=invoice_id)
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
#         else:
#             return HttpResponse('File not Found in Model')
#
#
# ############################
# # File Convert in  Pdf
# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     current_time = datetime.datetime.now().timestamp()
#     pdf_path = 'media/mypdf_{}.pdf'.format(current_time)
#     with open(pdf_path, 'wb+') as output:
#         pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
#     return pdf_path
#
#
# class InvoiceDownloadPdf(View):
#     def get(self, request, *args, **kwargs):
#         html = template
#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')
#
#         filename = "Invoice_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#
#         # rendering the template
#
#         with open(pdf_path, 'r') as f:
#             file_data = f.read()
#
#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response
#
#
# # 3
# # Invoice and Item join
# class InvoiceItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = Invoice.objects.all()
#     serializer_class = JoinInvoiceAndInvoiceItemSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'salescustomer/invoicefile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)
#
#
# # get all invoice journal transaction
# class invoicejournaltransactionList(generics.ListAPIView):
#     queryset = InvoiceJournalTransaction.objects.all()
#     serializer_class = InvoiceJTSerializer
#
#
#
#
#
# class invoiceList(generics.ListAPIView):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoicetransactionsSerializer
#
#
# @api_view(['GET'])  # get details by id
# def invoicejournaltransactionDetail(request, pk):
#     invoicejournaltransaction = Invoice.objects.get(invoice_id=pk)
#     serializer = InvoicetransactionsSerializer(
#         invoicejournaltransaction, many=False)
#     return Response(serializer.data)
#
#
#
# # invoiceshortbycompanyid
#
# ####################################################
# @api_view(['GET'])
# def invoiceshortbycompanyid(request, comp_id):
#     # invoice = Invoice.objects.all().order_by('created_date')
#
#     company = Company.objects.get(company_id=comp_id)
#     invoice = Invoice.objects.filter(
#         company_id=company).order_by('created_date')
#     serializer = invoiceshortbycompanySerializer(invoice, many=True)
#
#     return Response(serializer.data)
#
# #########################################################
# @api_view(['GET'])
# def download_inv(request, comp_id, invoice_id):
#     # invoice = Invoice.objects.all().order_by('created_date')
#     company = Company.objects.get(company_id=comp_id)
#     inv = Invoice.objects.get(invoice_id=invoice_id)
#     invoice = Invoice.objects.filter(
#         company_id=comp_id, invoice_id=invoice_id).order_by('created_date')
#     #serializer = invoiceshortbycompanySerializer(invoice, many=True)
#     serializers = JoinInvoiceAndInvoiceItemSerializer(invoice, many=True)
#     output_pdf = f'INV_{datetime.datetime.now().timestamp()}.pdf'
#     generate_invoice_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#
#
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadinvoice/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# # return Response(response)
#     return Response(response)
#
#
# def download_invoice(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#
#     response = FileResponse(open(file_path, 'rb'),as_attatchment=True)
#     # response = FileResponse(file_data, as_attachment=True,
#
#     return response
#
#
# @api_view(['GET'])
# def invoiceDetail(request, pk):
#     invoice = Invoice.objects.get(id=pk)
#     serializer = InvoiceSerializer(invoice, many=False)
#     return Response(serializer.data)
#
#
# # get invoice by customer id(Response for this api is its return only unpaid invoices as per respective  customer)
# @api_view(['GET'])
# def invoicebycustomerid(request, pk):
#     customer = SalesCustomer.objects.get(customer_id=pk)
#     print('customer', customer)
#     serializer = InvoicebyCustomerSerializer(customer, many=False)
#     return Response(serializer.data)
#
# #this section is use to invoice ref
# @api_view(['GET'])
# def invoicerefbycustomerid(request, pk):
#     customer = SalesCustomer.objects.get(customer_id=pk)
#     invoices=Invoice.objects.filter(customer_id=customer)
#     print('Invoces Is here',invoices)
#     response_list=[]
#     for invoice in invoices:
#         invoice_id=invoice.invoice_id
#         invoice_serial=invoice.invoice_serial
#         customer_id=invoice.customer_id.customer_id
#
#         response_dict = {"invoice_id":invoice_id,"invoice_serial":invoice_serial,"customer_id":customer_id}
#         response_list.append(response_dict)
#     return Response(response_list)
#
#
# @api_view(['POST'])
# def invoiceUpdate(request, pk):
#     invoice = Invoice.objects.get(id=pk)
#     serializer = InvoiceSerializer(instance=invoice, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
#
#
# ##################################################
# # Dwonload Code Is Creting api By Download
# # Download by id
#
# class PRFileDownloadListAPIView(generics.ListAPIView):
#
#     def get(self, request, pr_id, format=None):
#         queryset = PR.objects.get(pr_id=pr_id)
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
#             return HttpResponse('No File Found')
#
#
# #######################################################
#
#
# class PRGeneratePdf(View):
#     def get(self, request, pr_id, *args, **kwargs):
#         paymentrecive = PR.objects.get(pr_id=pr_id)
#         # Get The Payment Recive By  pr_id
#         # and Then Serialize the data
#         serializer = PRSerializer(paymentrecive)
#         print(serializer.data)
#         # get the Company data In PR (company_id) related
#         print(paymentrecive.company_id.company_id)
#         company = Company.objects.get(
#             company_id=paymentrecive.company_id.company_id)
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
#
#         return HttpResponse(html)
#
#
# #####################
# class PRDownloadPdf(View):
#     def get(self, request, *args, **kwargs):
#         # getting the template
#         pdf_path = render_to_pdf('base.html')
#
#         filename = "pr_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#
#         # rendering the template
#
#         with open(pdf_path, 'r') as f:
#             file_data = f.read()
#
#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response
#
#
# #############################################################
#
#
# class demoViewSet(viewsets.ModelViewSet):
#     queryset = PR.objects.all()
#     serializer_class = PRSerializer
#
#     def create(self, request, *args, **kwargs):
#         pr_data = request.data
#         print("pr_data", pr_data)
#         invoice_id = pr_data["invoice_id"]
#         invoice = Invoice.objects.get(invoice_id=pr_data["invoice_id"])
#         print("invoice.payment_status", invoice.payment_status)
#         invoice.payment_status = pr_data["payment_status"]
#
#         invoice.save()
#         print('invoice_updated', invoice)
#
#         serializer = InvoiceSerializer(invoice)
#         return Response(serializer.data)
#
#
# # get all payment receive list
# class paymentreceiveList(generics.ListAPIView):
#     queryset = PR.objects.all()
#     serializer_class = PRSerializer
#
#
# class PRGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = PR.objects.all()
#     serializer_class = PRSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'salescustomer/prfile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)
#
# # get payment recivied Full View by pr id
# @api_view(['GET'])
# def prfullview(request, pk):
#     prfullview = PR.objects.get(pr_id=pk)
#     serializer = PRMSerializer(prfullview)
#     return Response(serializer.data)
#
# # get payment receive byid
# @api_view(['GET'])
# def prDetail(request, pk):
#     pr = PR.objects.get(pr_id=pk)
#     serializer = PRSerializer(pr, many=False)
#     return Response(serializer.data)
#
#
# # get all payment journal transaction
# class paymentjournaltransactionList(generics.ListAPIView):
#     queryset = PR.objects.all()
#     serializer_class = PaymentTransactionSerializer
#
#
# # get all customer payment journal transaction
# class customerpaymentjournaltransactionList(generics.ListAPIView):
#     queryset = PR.objects.filter(bank_id__isnull=False)
#     serializer_class = PaymentTransactionSerializer
#
#
# # get payment transaction by pr id
# @api_view(['GET'])
# def paymentjournaltransactionDetail(request, pk):
#     paymentjournaltransaction = PR.objects.get(pr_id=pk)
#     serializer = PaymentTransactionSerializer(
#         paymentjournaltransaction, many=False)
#     return Response(serializer.data)
#
#
# # payment receive short by company id
# @api_view(['GET'])
# def prshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     paymentreceive = PR.objects.filter(company_id=company)
#     serializer = prshortbycompanySerializer(paymentreceive, many=True)
#     return Response(serializer.data)
#
# #Sales Customer Advanced refund
# @api_view(['GET'])
# def carefundshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     ca = CustomerAdvance.objects.filter(company_id=company)
#     serializer = CustomerAdvSerializer(ca, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def salescabyid(request, ca_id):
#     ca = CustomerAdvance.objects.filter(ca_id=ca_id)
#     serializer = CustomerAdvSerializer(ca, many=True)
#     return Response(serializer.data)
#
#
# #############################################################
# ###############################################################3##########################
#
#
#
# # api for get bill by company id and bill id
# @api_view(['GET'])
# def download_pr_data(request, comp_id,pr_id):
#     company = Company.objects.get(company_id=comp_id)
#     pr = PR.objects.get(pr_id=pr_id)
#     # here filter the object of bill id and company id
#     precieved = PR.objects.filter(
#         company_id=comp_id,pr_id=pr_id).order_by('created_date')
#     serializers =prshortbycompanySerializer(precieved, many=True)
#     output_pdf=f"PR_{datetime.datetime.now().timestamp()}.pdf"
#     generate_pr_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadpr/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)
#
# def download_pr(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,
#     return response
# ################################################################################
#
#
#
#
#
# # Payment mode
# class paymentmodeViewSet(viewsets.ModelViewSet):
#     queryset = PaymentMode.objects.all()
#     serializer_class = paymentmodeSerializer
#
#
# class paymentmodeList(generics.ListAPIView):
#     queryset = PaymentMode.objects.all()
#     serializer_class = paymentmodeSerializer
#
#     # @api_view Allow to define function that match http methods
#     @api_view(['GET'])
#     def paymentmodeCreation(request):
#         paymentmode = PaymentMode.objects.all()
#         serializer = paymentmodeSerializer(paymentmode, many=True)
#         return Response(serializer.data)
#
#
# ##################################################
# # API for Delivery Challan
# # POST
# class dcitemsViewSet(viewsets.ModelViewSet):
#     queryset = DcItem.objects.all()
#     serializer_class = DcItemSerializer
#
#     def create(self, request, *args, **kwargs):
#
#         dc_data_converte = request.data['data']
#         print("#################################################")
#         print(dc_data_converte)
#         print("Delivary Challan Data Format is ", type(dc_data_converte))
#         print("#################################################")
#         # Delivary Challan Convert Str to Dict Code
#         dc_data = json.loads(dc_data_converte)
#         print("Converted Format is", type(dc_data))
#
#         dc_file_data = request.FILES.get('attach_file')
#         print("dc_data", type(dc_file_data))
#
#
#
#         try:
#             tcs_id = dc_data["tcs_id"]
#             if tcs_id is not None:
#                 tcs_id = TCS.objects.get(tcs_id=tcs_id)
#         except KeyError:
#             tcs_id=None
#         dc_items = dc_data["dc_items"]
#         comp_id = Company.objects.get(company_id=dc_data["company_id"])
#         # branch_id = Branch.objects.get(branch_id=estimate_data["branch_id"])
#         cust_id = SalesCustomer.objects.get(customer_id=dc_data["customer_id"])
#
#         # Delivery Challan fields
#         deliverychallan_id = DC.objects.create(dc_ref_no=dc_data["dc_ref_no"],
#                                                dc_date=dc_data["dc_date"],
#                                                dc_status=dc_data["dc_status"],
#                                                dc_serial=dc_data["dc_serial"],
#                                                is_dc_generated=dc_data["is_dc_generated"],
#                                                customer_note=dc_data["customer_note"],
#                                                discount=dc_data["discount"],
#                                                entered_discount=dc_data["entered_discount"],
#                                                entered_shipping_charges=dc_data["entered_shipping_charges"],
#                                                shipping_charges=dc_data["shipping_charges"],
#                                                shipping_tax_name=dc_data["shipping_tax_name"],
#                                                # shipping_tax_rate=dc_data["shipping_tax_rate"],
#                                                dc_type=dc_data["dc_type"],
#                                                supply_place=dc_data["supply_place"],
#                                                terms_condition=dc_data["terms_condition"],
#                                                total_gst=dc_data["total_gst"],
#                                                cgst_total=dc_data['cgst_total'],
#                                                sgst_total=dc_data['sgst_total'],
#                                                igst_total=dc_data['igst_total'],
#                                                # expiry_date=dc_data["expiry_date"],
#                                                # tcs_amount=dc_data["tcs_amount"],
#                                                sub_total=dc_data["sub_total"],
#                                                total=dc_data["total"],
#                                                tcs_id=tcs_id,
#                                                # payment_id = pay_id,
#                                                # emp_id = employee_id,
#                                                company_id=comp_id,
#                                                attach_file=dc_file_data,
#                                                # branch_id = branch_id,
#                                                customer_id=cust_id)
#
#         deliverychallan_id.save()
#         if dc_file_data is not None:
#             file_ext = os.path.splitext(dc_file_data.name)[1]
#             new_file_path = f'media/DC_{deliverychallan_id.dc_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in dc_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             deliverychallan_id.attach_file = pth
#             deliverychallan_id.save()
#
#         print("so_items", dc_items, type(dc_items))
#
#         for i in range(len(dc_items)):
#             new_dcitem = DcItem.objects.create(dc_id=deliverychallan_id,
#                                                item_id=Item.objects.get(
#                                                    item_id=dc_items[i]["item_id"]),
#                                                item_name=dc_items[i]["item_name"],
#                                                rate=dc_items[i]["rate"],
#                                                quantity=dc_items[i]["quantity"],
#                                                tax_rate=dc_items[i]["tax_rate"],
#                                                tax_name=dc_items[i]["tax_name"],
#                                                tax_type=dc_items[i]["tax_type"],
#                                                taxamount=dc_items[i]["taxamount"],
#                                                cgst_amount=dc_items[i]['cgst_amount'],
#                                                sgst_amount=dc_items[i]['sgst_amount'],
#                                                igst_amount=dc_items[i]['igst_amount'],
#                                                amount=dc_items[i]["amount"])
#
#             new_dcitem.save()
#             print(i, "dc_items")
#
#         serializer = DcItemSerializer(new_dcitem)  # browser
#         return Response(serializer.data)
#
#
# ##################################################
# # Dwonload Code Is Creting api By Download
# # Download Delivary Challan by id
#
# class DelivarychallanFileDownloadListAPIView(generics.ListAPIView):
#
#     def get(self, request, dc_id, format=None):
#         queryset = DC.objects.get(dc_id=dc_id)
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
#
#
# #######################################################
#
#
# class DelivaryChallenGeneratePdf(View):
#     def get(self, request, dc_id, *args, **kwargs):
#         dc = DC.objects.get(dc_id=dc_id)
#         # Get The Estimate By estimate id
#         # and Then Serialize the data
#         serializer = DCSerializer(dc)
#         print(serializer.data)
#         # get the Company data In Estimate (company_id) related
#         print(dc.company_id.company_id)
#         company = Company.objects.get(company_id=dc.company_id.company_id)
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
#
#         return HttpResponse(html)
#
#
# #####################
# class DelivarychallenDownloadPdf(View):
#     def get(self, request, *args, **kwargs):
#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')
#
#         filename = "delivary_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#
#         # rendering the template
#
#         with open(pdf_path, 'r') as f:
#             file_data = f.read()
#
#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response
#
#
# #############################################################
#
#
# @api_view(['GET'])
# def dcDetail(request, pk):
#     dc = DC.objects.get(id=pk)
#     serializer = DCSerializer(dc, many=False)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# def dcUpdate(request, pk):
#     dc = DC.objects.get(id=pk)
#     serializer = DCSerializer(instance=dc, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# # getshortDetails
# @api_view(['GET'])
# def ShortDeliveryChallanDetails(request):
#     dc = DC.objects.all()
#     serializer = ShortDeliveryChallanSerializer(dc, many=True)
#     return Response(serializer.data)
#
#
# # dcshortbycompanyid
# @api_view(['GET'])
# def dcshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     dc = DC.objects.filter(company_id=company)
#     serializer = dcshortbycompanySerializer(dc, many=True)#
#     return Response(serializer.data)
#
# #############################################################
# ###############################################################3##########################
#
#
#
# # api for get bill by company id and bill id
# @api_view(['GET'])
# def download_dc_data(request, comp_id,dc_id):
#     company = Company.objects.get(company_id=comp_id)
#     dc = DC.objects.get(dc_id=dc_id)
#     # here filter the object of bill id and company id
#     dec = DC.objects.filter(
#         company_id=comp_id,dc_id=dc_id).order_by('created_date')
#     serializers =JoinDcItemSerializer(dec, many=True)
#     output_pdf=f'DC_{datetime.datetime.now().timestamp()}.pdf'
#     generate_dc_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/DownloadDC/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)
#
# def download_dc(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,
#     return response
# ################################################################################
#
# # Dcitem and DC join
# class DcItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = DC.objects.all()
#     serializer_class = JoinDcItemSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'salescustomer/dcfile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)
#
#     # API for Credit Note
#
# ################################################################################################################################
#
# # Dwonload Code Is Creting api By Download
# # Download Creditnote by id
#
# class CreditnoteFileDownloadListAPIView(generics.ListAPIView):
#
#     def get(self, request, creditnote_id, format=None):
#         queryset = CreditNote.objects.get(cn_id=creditnote_id)
#         print('''''''', [queryset.attach_file])
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
#
#
# #######################################################
#
#
# class CreditnoteGeneratePdf(View):
#     def get(self, request, creditnote_id, *args, **kwargs):
#         creditnote = CreditNote.objects.get(cn_id=creditnote_id)
#         # Get The CreditNote By creditnote id
#         # and Then Serialize the data
#         serializer = CreditNoteSerializer(creditnote)
#         print(serializer.data)
#         # get the Company data In CreditNote (company_id) related
#         print(creditnote.company_id.company_id)
#         company = Company.objects.get(
#             company_id=creditnote.company_id.company_id)
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
#         # Add the Company and Creditnpte Data in Dictionary (Means Combine the data)
#         context.update(dict(serializer.data))
#         context.update(dict(company_serializer.data))
#         html = template.render(context)
#
#         return HttpResponse(html)
#
#
# #####################
# class CreditnoteDownloadPdf(View):
#     def get(self, request, *args, **kwargs):
#         # getting the template
#         pdf_path = render_to_pdf('invoice.html')
#
#         filename = "creditnote_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#
#         # rendering the template
#
#         with open(pdf_path, 'r') as f:
#             file_data = f.read()
#
#         # sending response
#         response = FileResponse(file_data, as_attachment=True,
#                                 filename='hello.pdf', content_type='application/pdf')
#         response['Content-Disposition'] = content
#         return response
#
#
# #############################################################
#
#
# # get credit note journal transaction details by cn id
# @api_view(['GET'])
# def creditnotejournaltransactionDetail(request, pk):
#     creditnotejournaltransaction = CreditNote.objects.get(cn_id=pk)
#     serializer = cntransactionsSerializer(
#         creditnotejournaltransaction, many=False)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def creditnoteDetail(request, pk):
#     creditnote = CreditNote.objects.get(id=pk)
#     serializer = CreditNoteSerializer(creditnote, many=False)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# def creditnoteUpdate(request, pk):
#     creditnote = CreditNote.objects.get(id=pk)
#     serializer = CreditNoteSerializer(instance=creditnote, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# # getshortDetails
# @api_view(['GET'])
# def ShortCreditNoteDetails(request):
#     cn = CreditNote.objects.all()
#     serializer = ShortCreditNoteSerializer(cn, many=True)
#     return Response(serializer.data)
#
#
# # cnshortbycompanyid
# @api_view(['GET'])
# def cnshortbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     cn = CreditNote.objects.filter(company_id=company)
#     serializer = ShortCreditNoteSerializer(cn, many=True)
#     #serializer =JoinCreditNoteItemSerializer(cn, many=True)
#
#     return Response(serializer.data)
# #Sales Credit Note refund
#
#
#
# #All Journal Transaction View
# n_data=None
# @api_view(['GET'])
# def salescntransactionshortbycnid(self,form_id):
#     form_mast = MasterTransaction.objects.filter(L3detail_id=form_id)
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
#
#
#     df_accounts = pd.concat([from_acc, to_acc])
#     response = json.loads(df_accounts.to_json(orient='records'))
#
#     serializer = MasterTransactionSerializer(form_mast, many=True)
#     n_data=serializer.data
#     all_response = {
#             # 'original_data': account_type_list,
#             'form_data': n_data,
#             'transaction': response,
#         }
#     return Response(all_response)
#
# @api_view(['GET'])
# def download_inv(request, comp_id, invoice_id):
#     # invoice = Invoice.objects.all().order_by('created_date')
#     company = Company.objects.get(company_id=comp_id)
#     inv = Invoice.objects.get(invoice_id=invoice_id)
#     invoice = Invoice.objects.filter(
#         company_id=comp_id, invoice_id=invoice_id).order_by('created_date')
#     #serializer = invoiceshortbycompanySerializer(invoice, many=True)
#     serializers = JoinInvoiceAndInvoiceItemSerializer(invoice, many=True)
#     output_pdf = f"INV_{datetime.datetime.now().timestamp()}.pdf"
#     generate_invoice_pdf(data=serializers.data,output_path=os.path.join("media", output_pdf))
#
# ## here we use if function to check where whether the file is exist on media file or not
# ## here we give full output path (os.path.join("media", output_pdf))
#     if os.path.exists(os.path.join("media", output_pdf)):
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadinvoice/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# # return Response(response)
#     return Response(response)
#
#
# def download_invoice(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#     response = FileResponse(open(file_path, 'rb'))
#     # response = FileResponse(file_data, as_attachment=True,
#     return response
#
#
# # credit note item and credit note join
# class CreditNoteItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = CreditNote.objects.all()
#     serializer_class = JoinCreditNoteItemSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'salescustomer/creditnotefile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)
#
#     # API for Payment Received
#
#
# @api_view(['POST'])
# def prUpdate(request, pk):
#     pr = PR.objects.get(id=pk)
#     serializer = PRSerializer(instance=pr, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# # API for Recurring Invoice
# @api_view(['GET'])
# def riCreation(request):
#     ri = RI.objects.all()
#     serializer = RISerializer(ri, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def riDetail(request, pk):
#     ri = RI.objects.get(id=pk)
#     serializer = RISerializer(ri, many=False)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# def riUpdate(request, pk):
#     ri = RI.objects.get(id=pk)
#     serializer = RISerializer(instance=ri, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# # API for Credit Note
# @api_view(['GET'])
# def creditnoteDetail(request, pk):
#     creditnote = CreditNote.objects.get(id=pk)
#     serializer = CreditNoteSerializer(creditnote, many=False)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# def creditnoteUpdate(request, pk):
#     creditnote = CreditNote.objects.get(id=pk)
#     serializer = CreditNoteSerializer(instance=creditnote, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
# # api to generate credit note pdf
#
#
#
#
#
# @api_view(['GET'])
# def download_cn_data(request, comp_id, cn_id):
#     # invoice = Invoice.objects.all().order_by('created_date')
#     company = Company.objects.get(company_id=comp_id)
#     inv = CreditNote.objects.get(cn_id=cn_id)
#     cn = CreditNote.objects.filter(
#         company_id=comp_id, cn_id=cn_id).order_by('created_date')
#     #serializer = invoiceshortbycompanySerializer(invoice, many=True)
#     serializers = JoinCreditNoteItemSerializer(cn, many=True)
#     output_pdf=f"CN_{datetime.datetime.now().timestamp()}.pdf"
#     generate_credit_note_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadcn/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# # return Response(response)
#     return Response(response)
#
#
# def download_cn(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#
#     response = FileResponse(open(file_path, 'rb'),as_attachment=True)
#     # response = FileResponse(file_data, as_attachment=True,
#
#     return response
#
# class new3invoiceitemsViewSet(viewsets.ModelViewSet):
#     queryset = InvoiceItem.objects.all()
#     serializer_class = InvoiceItemSerializer
#     # here is the entry for invoice
#     def create(self, request, *args, **kwargs):
#         invoice_data_converte = request.data['data']
#         user=request.user
#         print('HIIIIIIII USER DATA',user,)
#
#         """_summary_
#
#         Returns:
#             _type_: _description_
#         """
#         # Invoice Convert Str to Dict Code
#         invoice_data = json.loads(invoice_data_converte)
#         # invoice_data = request.data['data']
#
#         invoice_file_data = request.FILES.get('attach_file')
#         print("  //////////////////////////// invoice_file_data", type(invoice_file_data))
#
#
#         # Branch_id=invoice_data["branch_id"]
#         # if Branch_id is not None:
#         #     Branch_id=Branch.objects.get(branch_id=Branch_id)
#
#         all_invoice_items = invoice_data["invoice_items"]
#         company_id = Company.objects.get(company_id=invoice_data["company_id"])
#         cust_id = SalesCustomer.objects.get(
#         customer_id=invoice_data["customer_id"])
#         employee_id = invoice_data["emp_id"]
#         if employee_id is not None:
#             employee_id = Employee.objects.get(emp_id=employee_id)
#         # Invoice fields
#         # global invoice_id
#         # Creating the invoice And Save the Invoice salescustomer_invoice table
#         invoice_data['amount_due'] = invoice_data["total"]
#         invoice_serializer = InvoiceSerializer(data=invoice_data)
#         if invoice_serializer.is_valid():
#             invoice_id = invoice_serializer.save()
#             invoice_id.attach_file = invoice_file_data
#             invoice_id.save()
#         else:
#             return Response(invoice_serializer.errors)
#
#         # File Rename Code The File is Save By Invoice id
#         if invoice_file_data is not None:
#             file_ext = os.path.splitext(invoice_file_data.name)[1]
#             new_file_path = f'media/Invoice_{invoice_id.invoice_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in invoice_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             invoice_id.attach_file = pth
#             invoice_id.save()
#         items = sorted(all_invoice_items, key=itemgetter('coa_id'))
#         print('@@@@@',items)
#
#         # Display data grouped by 'coa_id'
#         account_receivable = COA.objects.get(company_id=company_id, account_subhead="Account Receivables")
#         for item in items:
#             print('item is here',item)
#             coa=COA.objects.get(coa_id=item["coa_id"])
#             print('coa_type',type(coa))
#
#             # Created the debitnote items entries. for one debitnote many items to be created.
#             invoice_items = InvoiceItem.objects.create(invoice_id=invoice_id,
#                                                        item_id=Item.objects.get(
#                                                            item_id=item["item_id"]),
#                                                        coa_id=coa,
#                                                        item_name=item["item_name"],
#                                                        rate=item["rate"],
#                                                        quantity=item["quantity"],
#                                                        tax_rate=item["tax_rate"],
#                                                        tax_name=item["tax_name"],
#                                                        tax_type=item["tax_type"],
#                                                        sgst_amount=item["sgst_amount"],
#                                                        cgst_amount=item["cgst_amount"],
#                                                        igst_amount=item["igst_amount"],
#                                                        # taxamount=item["taxamount"],
#                                                        amount=item["amount"])
#             invoice_items.save()
#
#
#
#
#         #This Section is Stock Main Section
#         #All The Value Save In Stock Table Section
#         #The Sales Stock Value To Be Decrease means Stock Out field be updated
#             #Stock out last rate invoice stock journal all the claculation
#             #depends on FIFO Method last rate
#             item_value=Item.objects.get(item_id=item["item_id"])
#             items_inventory=invoice_data.get('invoice_items')
#             track_inventory=items_inventory[0].get('selected_item_name',{}).get('track_inventory')
#             print('inventory',track_inventory)
#             if track_inventory==True:
#                 stk_in=Stock.objects.filter(item_id=item["item_id"]).exclude(stock_in=0).order_by('created_date')
#                 stk_out=Stock.objects.filter(item_id=item["item_id"]).exclude(stock_out=0).order_by('created_date')
#
#                 print(stk_out)
#                 stock_int_items = stk_in
#                 already_stock_out_items =stk_out
#                 item_to_sell = item["quantity"]
#
#                 # -------------------------------------------------
#
#                 # Check if the stock is available
#                 sum_of_stock_in = sum([_.stock_in for _ in stock_int_items])
#                 sum_of_stock_in_amount = sum([_.amount for _ in stock_int_items])
#                 print("sum_of_stock_in_amount", sum_of_stock_in_amount)
#
#                 sum_of_already_stock_out = sum([_.stock_out for _ in already_stock_out_items])
#                 print("sum_of_already_stock_out", sum_of_already_stock_out)
#
#                 if sum_of_stock_in - (sum_of_already_stock_out + item_to_sell) < 0:
#                     print("Stock not available")
#                     return Response('Stock is not Avilable')
#
#                 print("Stock available")
#                 current_stock=sum_of_stock_in-sum_of_already_stock_out
#                 print('item is herer',item_value.item_id)
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                 print("current Assets_vlaue",current_assets_last_stock.amount)
#                 future_stock_outs = []
#                 for stock_in_item in stock_int_items:
#                     print(stock_in_item)
#                     if item_to_sell==0:
#                         break
#                     if sum_of_already_stock_out - stock_in_item.stock_in >= 0:
#                         print("\tItem fully sold")
#                         sum_of_already_stock_out = sum_of_already_stock_out - stock_in_item.stock_in
#                         print("\tRemaining already sold items: ", sum_of_already_stock_out)
#                         continue
#
#                     if sum_of_already_stock_out > 0:
#                         print("\tItem partially unsold")
#                         remaining_unsold_items = stock_in_item.stock_in - sum_of_already_stock_out
#                         print("\tRemaining unsold items", remaining_unsold_items)
#                         sum_of_already_stock_out = 0
#                     else:
#                         print("\tItem fully unsold")
#                         remaining_unsold_items = stock_in_item.stock_in
#
#                     if item_to_sell > remaining_unsold_items:
#                         print("\tMore items need to be sold")
#                         print(f"\tSelling {remaining_unsold_items} items")
#
#                         future_stock_outs=Stock.objects.create(
#                         item_id=item["item_id"],
#                         item_name=item["item_name"],
#                         stock_out=remaining_unsold_items,
#                         ref_id=invoice_id.invoice_id,
#                         amount=current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate,
#                         rate=current_assets_last_stock.rate,
#                         ref_tblname='Invoice',
#                         quantity=remaining_unsold_items,
#                         #stock_on_hand=current_stock-remaining_unsold_items,
#                         formname='Invoice',
#                         stage='Add Stages',
#                         date=invoice_data["invoice_date"],
#                         company_id=company_id)
#                         current_assets_last_stock.amount = current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate
#                         current_stock = current_stock-remaining_unsold_items
#
#
#                         #Stock(0, remaining_unsold_items, stock_in_item.rate)
#                         item_to_sell = item_to_sell - remaining_unsold_items
#                         print(f"\t{item_to_sell} still needed by the buyer")
#                     else:
#                         print(f"\tSelling {item_to_sell} items")
#                         future_stock_outs=Stock.objects.create(
#                         item_id=item["item_id"],
#                         item_name=item["item_name"],
#                         stock_out=item_to_sell,
#                         ref_id=invoice_id.invoice_id,
#                         amount=current_assets_last_stock.amount- item_to_sell*stock_in_item.rate,
#                         rate=current_assets_last_stock.rate,
#                         quantity=item_to_sell,
#                         ref_tblname='Invoice',
#                         #stock_on_hand=current_stock-item_to_sell,
#                         module='Sales',
#                         formname='Invoice',
#                         stage='Add Stages',
#                         date=invoice_data["invoice_date"],
#                         company_id=company_id)
#
#                         #append(Stock(0, item_to_sell, stock_in_item.rate))
#                         item_to_sell = 0
#
#
#                     print("------------")
#
#             #This Section Is Stock Journal Transaction
#             #Stock Charetd Account name is Inventory Assets
#             #item select time has three chart of account must be
#             #Sales Account,Purchase Account ,Inventory Accounts
#
#                     inv_item=invoice_data.get('invoice_items')
#                     purchase_account=inv_item[0].get('selected_item_name').get('purchase_account')
#                     inventory_account=inv_item[0].get('selected_item_name').get('inventory_account')
#                     if purchase_account is not None:
#                         TO_COA = COA.objects.get(company_id=company_id,coa_id=purchase_account)
#                     else:
#                         print("No Chart of Account Found")
#                     if inventory_account is not None:
#                         FROM_COA=COA.objects.get(company_id=company_id,coa_id=inventory_account)
#                     else:
#                         print("No Chart of Account Found")
#
#                     print('item rate',future_stock_outs.rate)
#                     print('item quantity',future_stock_outs.quantity)
#                     stkmast = MasterTransaction.objects.create(
#                         L1detail_id=invoice_id.invoice_id,
#                         L1detailstbl_name='Invoice',
#                         L2detail_id=future_stock_outs.st_id,
#                         L2detailstbl_name='Stock',
#                         main_module='Sales',
#                         module='Invoice',
#                         sub_module='Invoice',
#                         transc_deatils='Invoice',
#                         banking_module_type='Invoice',
#                         journal_module_type='Invoice',
#                         trans_date=invoice_data["invoice_date"],
#                         trans_status='Manually Added',
#                         debit=future_stock_outs.rate*future_stock_outs.quantity,
#                         to_account=TO_COA.coa_id,
#                         to_acc_type=TO_COA.account_type,
#                         to_acc_head=TO_COA.account_head,
#                         to_acc_subhead=TO_COA.account_subhead,
#                         to_acc_name=TO_COA.account_name,
#                         credit=future_stock_outs.rate*future_stock_outs.quantity,
#                         from_account=FROM_COA.coa_id,
#                         from_acc_type=FROM_COA.account_type,
#                         from_acc_head=FROM_COA.account_head,
#                         from_acc_subhead=FROM_COA.account_subhead,
#                         from_acc_name=FROM_COA.account_name,
#                         company_id=company_id,
#                         customer_id=cust_id)
#                     stkmast.save()
#
#         # 0%GST and 0%IGST Calculation
#         Zero_tax=invoice_data.get('invoice_items')
#         GST_TAX=None
#         GST_TAX=Zero_tax[0]
#
#         if GST_TAX==Zero_tax[0].get('selected_tax_name') is not None:
#             GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
#         else:
#             pass
#
#
#
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX
#
#         else:
#             Both_Tax=None
#
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
#
#
#
#
#         # User Can the Send the data in request the this data added in this empty list and
#         #this list can perform the operation
#         # all the values are not equal to zero the added the list
#         #list added item to add the master transaction table
#         #chnges of this transaction debit credit and to from account
#         transaction_list = [] #This Empty List added the append
#
#         if float(invoice_data['tcs_amount'])>0:
#             transaction_list.append(["TCS Payable","tcs_amount"])
#         if float(invoice_data['shipping_charges']) >0:
#             transaction_list.append(["Shipping Charges","shipping_charges"])
#         if float(invoice_data['cgst_total']) >0 or Both_Tax:
#             transaction_list.append(["Output CGST", "cgst_total"],)
#         if float(invoice_data['sgst_total'] )>0 or Both_Tax:
#             transaction_list.append(["Output SGST", "sgst_total"])
#         if float(invoice_data['igst_total']) >0 or IGST_0:
#             transaction_list.append(["Output IGST", "igst_total"],)
#         for transaction in transaction_list:
#
#             #List Of index added 0 is get Account_name
#             TO_COA = COA.objects.get(company_id=company_id,account_name=transaction[0])
#             invomast = MasterTransaction.objects.create(
#                 L1detail_id=invoice_id.invoice_id,
#                 L1detailstbl_name='Invoice',
#                 main_module='Sales',
#                 module='Invoice',
#                 sub_module='Invoice',
#                 transc_deatils='Invoice',
#                 banking_module_type='Invoice',
#                 journal_module_type='Invoice',
#                 trans_date=invoice_data["invoice_date"],
#                 trans_status='Manually Added',
#                 debit=invoice_data[transaction[1]],
#                 to_account=account_receivable.coa_id,
#                 to_acc_type=account_receivable.account_type,
#                 to_acc_head=account_receivable.account_head,
#                 to_acc_subhead=account_receivable.account_subhead,
#                 to_acc_name=account_receivable.account_name,
#                 credit=invoice_data[transaction[1]],
#                 from_account=TO_COA.coa_id,
#                 from_acc_type=TO_COA.account_type,
#                 from_acc_head=TO_COA.account_head,
#                 from_acc_subhead=TO_COA.account_subhead,
#                 from_acc_name=TO_COA.account_name,
#                 company_id=company_id,
#                 customer_id=cust_id)
#             invomast.save()
#
#         # Group By Invoice item
#         #Multiple item Send the request Group the coa_id
#         # Invoice item Transaction Changes is the Sum of all Item
#         #All The Transaction Sum is Store Credit and Debit Side
#         coa_amount_dict = {}
#         print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',type(invoice_items))
#         for invoice_item in all_invoice_items:
#
#             print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
#             print(type(invoice_item))
#             if coa_amount_dict.get(invoice_item['coa_id']) is None:
#                 coa_amount_dict[invoice_item['coa_id']
#                                 ] = invoice_item['amount']
#             else:
#                 coa_amount_dict[invoice_item['coa_id']
#                                 ] = coa_amount_dict[invoice_item['coa_id']] + invoice_item['amount']
#
#         print('''''''',coa_amount_dict)
#         # Group BY coa_id and sum of all item values
#         for coa_id, amount in coa_amount_dict.items():
#
#             TO_COA = COA.objects.get(coa_id=coa_id)
#             invomast = MasterTransaction.objects.create(
#                 L1detail_id=invoice_id.invoice_id,
#                 L1detailstbl_name='Invoice',
#                 main_module='Sales',
#                 module='Invoice',
#                 sub_module='Invoice',
#                 transc_deatils='Invoice',
#                 banking_module_type='Invoice',
#                 journal_module_type='Invoice',
#                 trans_date=invoice_data["invoice_date"],
#                 trans_status='Manually Added',
#                 debit=amount,
#                 to_account=account_receivable.coa_id,
#                 to_acc_type=account_receivable.account_type,
#                 to_acc_head=account_receivable.account_head,
#                 to_acc_subhead=account_receivable.account_subhead,
#                 to_acc_name=account_receivable.account_name,
#                 credit=amount,
#                 from_account=TO_COA.coa_id,
#                 from_acc_type=TO_COA.account_type,
#                 from_acc_head=TO_COA.account_head,
#                 from_acc_subhead=TO_COA.account_subhead,
#                 from_acc_name=TO_COA.account_name,
#                 company_id=company_id,
#                 customer_id=cust_id)
#             invomast.save()
#
#         #Invoice Transaction Discount is Valid to excute this Code
#         if invoice_data['discount']!=0:
#             TO_COA = COA.objects.get(company_id=company_id, account_subhead="Account Receivables")
#             account_receivable = COA.objects.get(company_id=company_id, account_name="Discount")
#             invomast = MasterTransaction.objects.create(
#                 L1detail_id=invoice_id.invoice_id,
#                 L1detailstbl_name='Invoice',
#                 main_module='Sales',
#                 module='Invoice',
#                 sub_module='Invoice',
#                 transc_deatils='Invoice',
#                 banking_module_type='Invoice',
#                 journal_module_type='Invoice',
#                 trans_date=invoice_data["invoice_date"],
#                 trans_status='Manually Added',
#                 debit=invoice_data['discount'],
#                 to_account=account_receivable.coa_id,
#                 to_acc_type=account_receivable.account_type,
#                 to_acc_head=account_receivable.account_head,
#                 to_acc_subhead=account_receivable.account_subhead,
#                 to_acc_name=account_receivable.account_name,
#                 credit=invoice_data['discount'],
#                 from_account=TO_COA.coa_id,
#                 from_acc_type=TO_COA.account_type,
#                 from_acc_head=TO_COA.account_head,
#                 from_acc_subhead=TO_COA.account_subhead,
#                 from_acc_name=TO_COA.account_name,
#                 company_id=company_id,
#                 customer_id=cust_id)
#             invomast.save()
#         serializer = InvoiceSerializer(invoice_id)
#         return Response(serializer.data)
#
#
# class new3creditnoteitemsViewSet(viewsets.ModelViewSet):
#     queryset = CreditItem.objects.all()
#     serializer_class = CnItemSerializer
#
#     def create(self, request, *args, **kwargs):
#         print( " GETTING REQUEST ",request.data)
#         creditnote_data_converte = request.data['data']
#
#         print("#################################################")
#         print("#################################################")
#         #Credit Note Convert Str to Dict Code
#         creditnote_data = json.loads(creditnote_data_converte)
#         #creditnote_data = request.data['data']
#         print("Converted Format is", type(creditnote_data))
#
#         creditnote_file_data = request.FILES.get('attach_file')
#         print("Credit Note_data", type(creditnote_file_data))
#
#         print("creditnote_data", creditnote_data)
#
#         # branch_id=creditnote_data["branch_id"]
#         # if branch_id is not None:
#         #     branch_id=Branch.objects.get(branch_id=branch_id)
#         try:
#             tcs_id = creditnote_data["tcs_id"]
#             if tcs_id is not None:
#                 tcs_id = TCS.objects.get(tcs_id=tcs_id)
#         except KeyError:
#             tcs_id=None
#
#         invoice_id=creditnote_data.get("invoice_id")
#         if invoice_id is not None:
#             invoice_id=Invoice.objects.get(invoice_id=invoice_id)
#
#
#         inv_serial=invoice_id.invoice_serial
#
#         credit_note_items = creditnote_data["credit_note_items"]
#         comp_id = Company.objects.get(company_id=creditnote_data["company_id"])
#         # employee_id = Employee.objects.get(emp_id=creditnote_data["emp_id"])
#         cust_id = SalesCustomer.objects.get(
#             customer_id=creditnote_data["customer_id"])
#
#
#
#
#         #creating the  credit note  and Save the Credit Note in salescustomer_creditnote table
#         # Credit Note fields
#         creditnote_id = CreditNote.objects.create(cn_ref_no=creditnote_data["cn_ref_no"],
#                                                   cn_date=creditnote_data["cn_date"],
#                                                   cn_status=creditnote_data["cn_status"],
#                                                   cn_serial=creditnote_data["cn_serial"],
#                                                   invoice_serial=inv_serial,
#                                                   invoice_id=invoice_id,
#                                                   is_cn_generated=creditnote_data["is_cn_generated"],
#                                                   customer_note=creditnote_data["customer_note"],
#                                                   discount=creditnote_data["discount"],
#                                                   reason=creditnote_data["reason"],
#                                                   entered_discount=creditnote_data["entered_discount"],
#                                                   entered_shipping_charges=creditnote_data[
#                                                       "entered_shipping_charges"],
#                                                   shipping_charges=creditnote_data["shipping_charges"],
#                                                   shipping_tax_name=creditnote_data["shipping_tax_name"],
#                                                   shipping_tax_rate=creditnote_data["shipping_tax_rate"],
#                                                   subject=creditnote_data["subject"],
#                                                   supply_place=creditnote_data["supply_place"],
#                                                   terms_condition=creditnote_data["terms_condition"],
#                                                   total_gst=creditnote_data["total_gst"],
#                                                   tcs_amount=creditnote_data["tcs_amount"],
#                                                   sub_total=creditnote_data["sub_total"],
#                                                   balance_amount=creditnote_data["total"],
#                                                   total=creditnote_data["total"],
#                                                   cgst_total=creditnote_data['cgst_total'],
#                                                   sgst_total=creditnote_data['sgst_total'],
#                                                   igst_total=creditnote_data['igst_total'],
#
#
#                                                   attach_file=creditnote_file_data,
#                                                   company_id=comp_id,
#                                                   tcs_id=tcs_id,
#                                                   # branch_id = branch_id,
#                                                   # payment_id = pay_id,
#
#                                                   customer_id=cust_id)
#
#         creditnote_id.save()
#         if creditnote_file_data is not None:
#             file_ext = os.path.splitext(creditnote_file_data.name)[1]
#             new_file_path = f'media/CreditNote_{creditnote_id.cn_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in creditnote_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             creditnote_id.attach_file = pth
#             creditnote_id.save()
#
#         account_receivable = COA.objects.get(
#             company_id=comp_id, account_subhead="Account Receivables")
#
#         for item in creditnote_data["credit_note_items"]:
#             new_credit_note_items = CreditItem.objects.create(cn_id=creditnote_id,
#                                                               item_id=Item.objects.get(
#                                                                   item_id=item["item_id"]),
#                                                               coa_id=COA.objects.get(
#                                                                   coa_id=item["coa_id"]),
#                                                               item_name=item["item_name"],
#                                                               rate=item["rate"],
#                                                               quantity=item["quantity"],
#                                                               tax_rate=item["tax_rate"],
#                                                               tax_name=item["tax_name"],
#                                                               tax_type=item["tax_type"],
#                                                               taxamount=item["taxamount"],
#                                                               cgst_amount=item['cgst_amount'],
#                                                               sgst_amount=item['sgst_amount'],
#                                                               igst_amount=item['igst_amount'],
#                                                               amount=item["amount"])
#
#             new_credit_note_items.save()
#
#
#             print(new_credit_note_items)
#             #This Section is Stock Main Section
#             #All The Value Save In Stock Table Section
#             #The Sales Stock Value To Be Decrease means Stock Out field be updated
#             item_value=Item.objects.get(item_id=item["item_id"])
#             items_inventory=creditnote_data.get('credit_note_items')
#             track_inventory=items_inventory[0].get('selected_item_name',{}).get('track_inventory')
#             print('inventory',track_inventory)
#
#             item_value=Item.objects.get(item_id=item["item_id"])
#             print('Item is herer',item_value)
#
#
#             if track_inventory==True:
#
#
#                 try:
#                     current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                     current_stock_amount=current_assets_last_stock.amount
#
#                     current_invoice_rate=Stock.objects.filter(item_id=item_value.item_id,formname='Invoice').latest('created_date')
#                     stock_invoice_rate=current_invoice_rate.rate
#                 except Stock.DoesNotExist:
#                     stock_invoice_rate=0
#                     current_invoice_rate=0
#                     current_stock_amount=0
#
#                     stk_in=Stock.objects.filter(item_id=item["item_id"]).exclude(stock_in=0).order_by('created_date')
#                     stk_out=Stock.objects.filter(item_id=item["item_id"]).exclude(stock_out=0).order_by('created_date')
#                     stock_int_items = stk_in
#
#                 print("Stock Invoice rate@@@@@@",stock_invoice_rate)
#                 stock_items=Stock.objects.create(
#                     item_id=item['item_id'],
#                     item_name=item["item_name"],
#                     stock_in=item["quantity"],
#                     amount=current_stock_amount+(item["quantity"] * item["rate"]),
#                     rate= stock_invoice_rate,
#                     quantity=item["quantity"],
#                     #stock_on_hand=current_stock_on_hand+item["quantity"],
#                     ref_id=creditnote_id.cn_id,
#                     ref_tblname='CreditNote',
#                     module='Sales',
#                     formname='Credit Note',
#                     stage='Add Stages',
#                     date=creditnote_data["cn_date"],
#                     company_id=comp_id)
#
#
#
#
#         #This Section Is Stock Journal Transaction
#         #Stock Charetd Account name is Inventory Assets
#         #item select time has three chart of account must be
#         #Sales Account,Purchase Account ,Inventory Accounts
#
#                 cr_item=creditnote_data.get('credit_note_items')
#                 purchase_account=cr_item[0].get('selected_item_name').get('purchase_account')
#                 inventory_account=cr_item[0].get('selected_item_name').get('inventory_account')
#                 if purchase_account is not None:
#                     FROM_COA = COA.objects.get(company_id=comp_id,coa_id=purchase_account)
#                 else:
#                     print("No Chart of Account Found")
#                 if inventory_account is not None:
#                     TO_COA=COA.objects.get(company_id=comp_id,coa_id=inventory_account)
#                 else:
#                     print("No Chart of Account Found")
#
#                 #TO_COA = COA.objects.get(company_id=comp_id,account_name='Inventory Assets')
#                 print('item rate',stock_items.rate)
#                 print('item quantity',stock_items.quantity)
#                 stkmast = MasterTransaction.objects.create(
#                     L1detail_id=creditnote_id.cn_id,
#                     L1detailstbl_name='CreditNote',
#                     L2detail_id=stock_items.st_id,
#                     L2detailstbl_name='Stock',
#                     main_module='Sales',
#                     module='CreditNote',
#                     sub_module='CreditNote',
#                     transc_deatils='CreditNote',
#                     banking_module_type='CreditNote',
#                     journal_module_type='CreditNote',
#                     trans_date=creditnote_data["cn_date"],
#                     trans_status='Manually Added',
#                     debit=stock_items.rate*stock_items.quantity,
#                     to_account=TO_COA.coa_id,
#                     to_acc_type=TO_COA.account_type,
#                     to_acc_head=TO_COA.account_head,
#                     to_acc_subhead=TO_COA.account_subhead,
#                     to_acc_name=TO_COA.account_name,
#                     credit=stock_items.rate*stock_items.quantity,
#                     from_account=FROM_COA.coa_id,
#                     from_acc_type=FROM_COA.account_type,
#                     from_acc_head=FROM_COA.account_head,
#                     from_acc_subhead=FROM_COA.account_subhead,
#                     from_acc_name=FROM_COA.account_name,
#                     company_id=comp_id,
#                     customer_id=cust_id)
#                 stkmast.save()
#
#
#
#
#         # 0%GST and 0%IGST Calculation
#         #The User are Select the 0% Tax The value be Store in table is 0
#         #creditnote_data is dictionary .to get the dictionary credit_note_items
#         Zero_tax=creditnote_data
#         TAX_name=Zero_tax['credit_note_items'][0]
#         GST_TAX=None
#         GST_TAX=TAX_name['selected_tax_name']
#
#         if GST_TAX is not None:
#             GST_TAX=TAX_name['selected_tax_name']['tax_name']
#         else:
#             pass
#
#
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX
#
#         else:
#             Both_Tax=None
#
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
#
#
#          # User Can the Send the data in request the this data added in this empty list and
#         #this list can perform the operation
#         # all the values are not equal to zero the added the list
#         #list added item to add the master transaction table
#         #chnges of this transaction debit credit and to from account
#         transaction_list = []
#         if float(creditnote_data['tcs_amount'])>0:
#             transaction_list.append(["TCS Payable","tcs_amount"])
#         if float(creditnote_data['shipping_charges'])>0:
#             transaction_list.append(["Shipping Charges","shipping_charges"])
#         if float(creditnote_data['cgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Output CGST", "cgst_total"],)
#         if float(creditnote_data['sgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Output SGST", "sgst_total"])
#         if float(creditnote_data['igst_total']) >0 or IGST_0:
#             transaction_list.append(["Output IGST", "igst_total"],)
#         for transaction in transaction_list:
#             print(transaction)
#             #List of index 0 is get the Account name
#             TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#             cnmast = MasterTransaction.objects.create(
#                 L1detail_id=creditnote_id.cn_id,
#                 L1detailstbl_name='Credit Note',
#                 main_module='Sales',
#                 module='Sales',
#                 sub_module='Credit Note',
#                 transc_deatils='Credit Note',
#                 banking_module_type='Credit Note',
#                 journal_module_type='Credit Note',
#                 trans_date=creditnote_data["cn_date"],
#                 trans_status='Manually added',
#                 debit=creditnote_data[transaction[1]],
#                 to_account=TO_COA.coa_id,
#                 to_acc_type=TO_COA.account_type,
#                 to_acc_head=TO_COA.account_head,
#                 to_acc_subhead=TO_COA.account_subhead,
#                 to_acc_name=TO_COA.account_name,
#                 credit=creditnote_data[transaction[1]],
#                 from_account=account_receivable.coa_id,
#                 from_acc_type=account_receivable.account_type,
#                 from_acc_head=account_receivable.account_head,
#                 from_acc_subhead=account_receivable.account_subhead,
#                 from_acc_name=account_receivable.account_name,
#                 company_id=comp_id,
#                 customer_id=cust_id)
#             cnmast.save()
#
#         # Group By credit note item
#         #Multiple item Send the request Group the coa_id
#         # Invoice item Transaction Changes is the Sum of all Item
#         #All The Transaction Sum is Store Credit and Debit Side
#         coa_amount_dict = {}
#         print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',type(credit_note_items))
#         for cn_item in credit_note_items:
#
#             print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
#             print(type(cn_item))
#             if coa_amount_dict.get(cn_item['coa_id']) is None:
#                 coa_amount_dict[cn_item['coa_id']
#                                 ] = cn_item['amount']
#             else:
#                 coa_amount_dict[cn_item['coa_id']
#                                 ] = coa_amount_dict[cn_item['coa_id']] + cn_item['amount']
#
#         print('''''''',coa_amount_dict)
#         # Group BY coa_id and sum of all item values
#         for coa_id, amount in coa_amount_dict.items():
#
#             TO_COA = COA.objects.get(coa_id=coa_id)
#             cnmast = MasterTransaction.objects.create(
#                 L1detail_id=creditnote_id.cn_id,
#                 L1detailstbl_name='Credit Note',
#                 main_module='Sales',
#                 module='Sales',
#                 sub_module='Credit Note',
#                 transc_deatils='Credit Note',
#                 banking_module_type='Credit Note',
#                 journal_module_type='Credit Note',
#                 trans_date=creditnote_data["cn_date"],
#                 trans_status='Manually added',
#                 debit=amount,
#                 to_account=TO_COA.coa_id,
#                 to_acc_type=TO_COA.account_type,
#                 to_acc_head=TO_COA.account_head,
#                 to_acc_subhead=TO_COA.account_subhead,
#                 to_acc_name=TO_COA.account_name,
#                 credit=amount,
#                 from_account=account_receivable.coa_id,
#                 from_acc_type=account_receivable.account_type,
#                 from_acc_head=account_receivable.account_head,
#                 from_acc_subhead=account_receivable.account_subhead,
#                 from_acc_name=account_receivable.account_name,
#                 company_id=comp_id,
#                 customer_id=cust_id)
#             cnmast.save()
#
#         #credit note Transaction Discount is Valid to excute this Code
#         if creditnote_data['discount']!=0:
#             TO_COA = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#             account_receivable = COA.objects.get(company_id=comp_id, account_name="Discount")
#             cnmast = MasterTransaction.objects.create(
#                 L1detail_id=creditnote_id.cn_id,
#                 L1detailstbl_name='Credit Note',
#                 main_module='Sales',
#                 module='Sales',
#                 sub_module='Credit Note',
#                 transc_deatils='Credit Note',
#                 banking_module_type='Credit Note',
#                 journal_module_type='Credit Note',
#                 trans_date=creditnote_data["cn_date"],
#                 trans_status='Manually added',
#                 debit=creditnote_data['discount'],
#                 to_account=TO_COA.coa_id,
#                 to_acc_type=TO_COA.account_type,
#                 to_acc_head=TO_COA.account_head,
#                 to_acc_subhead=TO_COA.account_subhead,
#                 to_acc_name=TO_COA.account_name,
#                 credit=creditnote_data['discount'],
#                 from_account=account_receivable.coa_id,
#                 from_acc_type=account_receivable.account_type,
#                 from_acc_head=account_receivable.account_head,
#                 from_acc_subhead=account_receivable.account_subhead,
#                 from_acc_name=account_receivable.account_name,
#                 company_id=comp_id,
#                 customer_id=cust_id)
#             cnmast.save()
#
#         serializer = CreditNoteItemSerializer(new_credit_note_items)
#         return Response(serializer.data)
#
#
#
#
#
#
#
#
# class new1paymentreceiveViewSet(viewsets.ModelViewSet):
#     queryset = PR.objects.all()
#     serializer_class = PRSerializer
#
#     def create(self, request, *args, **kwargs):
#         pr_data_converte = request.data['data']
#         # user=request.user.userid
#         # print('HIIIIIIII USER DATA',user,)
#         # PR Convert Str to Dict Code
#         pr_data = json.loads(pr_data_converte)
#         #pr_data=pr_data_converte
#         pr_file_data = request.FILES.get('attach_file')
#
#         company_id=pr_data["company_id"]
#         if company_id is not None:
#             company_id=Company.objects.get(company_id=company_id)
#
#
#         customer_id=pr_data["customer_id"]
#         if customer_id is not None:
#             customer_id=SalesCustomer.objects.get(customer_id=customer_id)
#
#
#         invoice_id=pr_data["invoice_id"]
#         if invoice_id is not None:
#             invoice_id=Invoice.objects.get(invoice_id=invoice_id)
#
#
#         pr_id = PR.objects.create(
#             # withholding_tax=pr_data["withholding_tax"],
#             # customer_note=pr_data["customer_note"],
#             notes=pr_data["notes"],
#             amount_due=pr_data["amount_due"],
#             invoice_amount=pr_data["invoice_amount"],
#             invoice_date=pr_data["invoice_date"],
#             invoice_serial=pr_data["invoice_serial"],
#             payment_date=pr_data["payment_date"],
#             tds_tax_account=pr_data["tds_tax_account"],
#             tax_deducted=pr_data["tax_deducted"],
#             bank_charges=pr_data["bank_charges"],
#             amount_received=pr_data["amount_received"],
#             balance_amount=pr_data["balance_amount"],
#             amount_excess=pr_data["amount_excess"],
#             payment_mode=pr_data["payment_mode"],
#             deposit_to=pr_data["deposit_to"],
#             payment_ref_no=pr_data["payment_ref_no"],
#             payment_serial=pr_data["payment_serial"],
#             attach_file=pr_file_data,
#             customer_id=customer_id,
#             invoice_id=invoice_id,
#             company_id=company_id)
#
#         # coa_id = COA.objects.get(coa_id=pr_data["coa_id"]))
#         pr_id.save()
#
#         if pr_file_data is not None:
#
#             file_ext = os.path.splitext(pr_file_data.name)[1]
#             new_file_path = f'media/PR_{pr_id.pr_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in pr_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             pr_id.attach_file = pth
#             pr_id.save()
#
#         account_receivable = COA.objects.get(company_id=company_id, account_subhead="Account Receivables")
#         # transaction_list = []
#         if pr_data['bank_charges'] is not None and float(pr_data['bank_charges']) >0:
#             # transaction_list.append(["Bank Fees and Charges","bank_charges"])
#             From_Bank = COA.objects.get(company_id=company_id,account_name="Bank Fees and Charges")
#             prmast = MasterTransaction.objects.create(
#                 L1detail_id=pr_id.pr_id,
#                 L1detailstbl_name='PR',
#                 L3detail_id=invoice_id.invoice_id,
#                 L3detailstbl_name='invoice',
#                 main_module='Sales',
#                 module='Payment Recived',
#                 sub_module='PR',
#                 transc_deatils='Payment Recived',
#                 trans_date=pr_data["payment_date"],
#                 banking_module_type='Customer Payment',
#                 journal_module_type='Invoice Payment',
#                 trans_status='Manually Added',
#                 debit=pr_data["bank_charges"],
#                 to_account=From_Bank.coa_id,
#                 to_acc_type=From_Bank.account_type,
#                 to_acc_head=From_Bank.account_head,
#                 to_acc_subhead=From_Bank.account_subhead,
#                 to_acc_name=From_Bank.account_name,
#                 credit=pr_data["bank_charges"],
#                 from_account=account_receivable.coa_id,
#                 from_acc_type=account_receivable.account_type,
#                 from_acc_head=account_receivable.account_head,
#                 from_acc_subhead=account_receivable.account_subhead,
#                 from_acc_name=account_receivable.account_name,
#                 customer_id=customer_id,
#                 company_id=company_id)
#             prmast.save()
#
#
#         From_Bank = COA.objects.get(coa_id=pr_data["coa_id"])
#         prmast = MasterTransaction.objects.create(
#             L1detail_id=pr_id.pr_id,
#             L1detailstbl_name='PR',
#             L3detail_id=invoice_id.invoice_id,
#             L3detailstbl_name='invoice',
#             main_module='Sales',
#             module='Payment Recived',
#             sub_module='PR',
#             transc_deatils='Payment Recived',
#             trans_date=pr_data["payment_date"],
#             banking_module_type='Customer Payment',
#             journal_module_type='Invoice Payment',
#             trans_status='Manually Added',
#             debit=pr_data["amount_received"],
#             to_account=From_Bank.coa_id,
#             to_acc_type=From_Bank.account_type,
#             to_acc_head=From_Bank.account_head,
#             to_acc_subhead=From_Bank.account_subhead,
#             to_acc_name=From_Bank.account_name,
#             credit=pr_data['amount_received'],
#             from_account=account_receivable.coa_id,
#             from_acc_type=account_receivable.account_type,
#             from_acc_head=account_receivable.account_head,
#             from_acc_subhead=account_receivable.account_subhead,
#             from_acc_name=account_receivable.account_name,
#             customer_id=customer_id,
#             company_id=company_id)
#         prmast.save()
#
#
#         # Update the status in invoice table for payment_status
#         # Update the status if update invoice status in Invoice model if amount_due==amount_received which means payment received is full
#         amount_due = pr_data["amount_due"]
#         print("amount_due", amount_due, type(amount_due))
#         amount_received = pr_data["amount_received"]
#         print("amount_received", amount_received, type(amount_received))
#         # If payment is full then payment status will change unpaid to paid in invoice
#         balance_amount = pr_data["balance_amount"]
#         # if amount_due == amount_received:
#         if balance_amount == 0:
#             invoice_id = Invoice.objects.get(invoice_id=pr_data["invoice_id"])
#             print('invoice_id', invoice_id)
#             invoice_id.payment_status = 'paid'
#             invoice_id.amount_due = pr_data["balance_amount"]
#             invoice_id.save()
#             print('invoice status updated to ', invoice_id.payment_status)
#         else:
#             invoice_id = Invoice.objects.get(invoice_id=pr_data["invoice_id"])
#             print('invoice id of else', invoice_id)
#             invoice_id.amount_due = pr_data["balance_amount"]
#             invoice_id.save()
#             print('invoice amount due updated to ', invoice_id.amount_due)
# # endregion
#
#         serializer = PRSerializer(pr_id)  # browser
#         return Response(serializer.data)
#
#
#
# def geeks_view(request):
#     # return response
#     a =  render(request, "core/ho_ba_sheet.html")
#     print(a.content.decode())
#     # convert all the data to string and pass this to the function
#     html=pdfkit.from_string(a.content.decode(),"newinvoice.pdf")
#     return a
#
# # Payment Recived New From
#
# class paymentreceivenew_fromViewSet(viewsets.ModelViewSet):
#     queryset = PR.objects.all()
#     serializer_class = PRSerializer
#
#     def create(self, request, *args, **kwargs):
#         pr_data_converte = request.data['data']
#         # PR Convert Str to Dict Code
#         #pr_data = json.loads(pr_data_converte)
#         pr_data=pr_data_converte
#         pr_file_data = request.FILES.get('attach_file')
#
#         company_id=pr_data["company_id"]
#         if company_id is not None:
#             company_id=Company.objects.get(company_id=company_id)
#
#
#         customer_id=pr_data["customer_id"]
#         if customer_id is not None:
#             customer_id=SalesCustomer.objects.get(customer_id=customer_id)
#
#
#         invoice_id=pr_data["invoice_id"]
#         if invoice_id is not None:
#             invoice_id=Invoice.objects.get(invoice_id=invoice_id)
#
#
#         # Payment Receive fields
#         pr_id = PR.objects.create(
#             # withholding_tax=pr_data["withholding_tax"],
#             # customer_note=pr_data["customer_note"],
#             notes=pr_data["notes"],
#             amount_due=pr_data["amount_due"],
#             invoice_amount=pr_data["invoice_amount"],
#             invoice_date=pr_data["invoice_date"],
#             invoice_serial=pr_data["invoice_serial"],
#             payment_date=pr_data["payment_date"],
#             tds_tax_account=pr_data["tds_tax_account"],
#             tax_deducted=pr_data["tax_deducted"],
#             bank_charges=pr_data["bank_charges"],
#             amount_received=pr_data["amount_received"],
#             balance_amount=pr_data["balance_amount"],
#             amount_excess=pr_data["amount_excess"],
#             payment_mode=pr_data["payment_mode"],
#             deposit_to=pr_data["deposit_to"],
#             payment_ref_no=pr_data["payment_ref_no"],
#             payment_serial=pr_data["payment_serial"],
#             attach_file=pr_file_data,
#             customer_id=customer_id,
#             invoice_id=invoice_id,
#             company_id=company_id)
#
#         # coa_id = COA.objects.get(coa_id=pr_data["coa_id"]))
#         pr_id.save()
#
#         if pr_file_data is not None:
#
#             file_ext = os.path.splitext(pr_file_data.name)[1]
#             new_file_path = f'media/PR_{pr_id.pr_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in pr_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here', pth)
#             pr_id.attach_file = pth
#             pr_id.save()
#
#         account_receivable = COA.objects.get(company_id=company_id, account_subhead="Account Receivables")
#         # transaction_list = []
#         if pr_data['bank_charges'] is not None and float(pr_data['bank_charges']) >0:
#             # transaction_list.append(["Bank Fees and Charges","bank_charges"])
#             From_Bank = COA.objects.get(company_id=company_id,account_name="Bank Fees and Charges")
#             prmast = MasterTransaction.objects.create(
#                 L1detail_id=pr_id.pr_id,
#                 L1detailstbl_name='PR',
#                 L3detail_id=invoice_id.invoice_id,
#                 L3detailstbl_name='invoice',
#                 main_module='Sales',
#                 module='Payment Recived',
#                 sub_module='PR',
#                 transc_deatils='Payment Recived',
#                 trans_date=pr_data["payment_date"],
#                 banking_module_type='Customer Payment',
#                 journal_module_type='Invoice Payment',
#                 trans_status='Manually Added',
#                 debit=pr_data["bank_charges"],
#                 to_account=From_Bank.coa_id,
#                 to_acc_type=From_Bank.account_type,
#                 to_acc_head=From_Bank.account_head,
#                 to_acc_subhead=From_Bank.account_subhead,
#                 to_acc_name=From_Bank.account_name,
#                 credit=pr_data["bank_charges"],
#                 from_account=account_receivable.coa_id,
#                 from_acc_type=account_receivable.account_type,
#                 from_acc_head=account_receivable.account_head,
#                 from_acc_subhead=account_receivable.account_subhead,
#                 from_acc_name=account_receivable.account_name,
#                 customer_id=customer_id,
#                 company_id=company_id)
#             prmast.save()
#
#
#         From_Bank = COA.objects.get(coa_id=pr_data["coa_id"])
#         prmast = MasterTransaction.objects.create(
#             L1detail_id=pr_id.pr_id,
#             L1detailstbl_name='PR',
#             L3detail_id=invoice_id.invoice_id,
#             L3detailstbl_name='invoice',
#             main_module='Sales',
#             module='Payment Recived',
#             sub_module='PR',
#             transc_deatils='Payment Recived',
#             trans_date=pr_data["payment_date"],
#             banking_module_type='Customer Payment',
#             journal_module_type='Invoice Payment',
#             trans_status='Manually Added',
#             debit=pr_data["amount_received"],
#             to_account=From_Bank.coa_id,
#             to_acc_type=From_Bank.account_type,
#             to_acc_head=From_Bank.account_head,
#             to_acc_subhead=From_Bank.account_subhead,
#             to_acc_name=From_Bank.account_name,
#             credit=pr_data['amount_received'],
#             from_account=account_receivable.coa_id,
#             from_acc_type=account_receivable.account_type,
#             from_acc_head=account_receivable.account_head,
#             from_acc_subhead=account_receivable.account_subhead,
#             from_acc_name=account_receivable.account_name,
#             customer_id=customer_id,
#             company_id=company_id)
#         prmast.save()
#
#
#         # Update the status in invoice table for payment_status
#         # Update the status if update invoice status in Invoice model if amount_due==amount_received which means payment received is full
#         amount_due = pr_data["amount_due"]
#         print("amount_due", amount_due, type(amount_due))
#         amount_received = pr_data["amount_received"]
#         print("amount_received", amount_received, type(amount_received))
#         # If payment is full then payment status will change unpaid to paid in invoice
#         balance_amount = pr_data["balance_amount"]
#         # if amount_due == amount_received:
#         if balance_amount == 0:
#             invoice_id = Invoice.objects.get(invoice_id=pr_data["invoice_id"])
#             print('invoice_id', invoice_id)
#             invoice_id.payment_status = 'paid'
#             invoice_id.amount_due = pr_data["balance_amount"]
#             invoice_id.save()
#             print('invoice status updated to ', invoice_id.payment_status)
#         else:
#             invoice_id = Invoice.objects.get(invoice_id=pr_data["invoice_id"])
#             print('invoice id of else', invoice_id)
#             invoice_id.amount_due = pr_data["balance_amount"]
#             invoice_id.save()
#             print('invoice amount due updated to ', invoice_id.amount_due)
# # endregion
#
#         serializer = PRSerializer(pr_id)  # browser
#         return Response(serializer.data)
#
#
#
#
#
# # New Customer Advanced refund  from
# class SalesCustomerAdvanceViewsets(viewsets.ModelViewSet):
#     queryset =CustomerAdvance.objects.all()
#     serializer_class =CustomerAdvancedSerializer
#     logger=[]
#     # Forone API are going to make three append append namely for Two Main Sections
#       #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
#       #  2: Financial Transaction:
#         #2.1 Credit Transation
#         #2.2 Debit Transaaction
#
#     def ValidateDefaults(obj):
#         SalesCustomerAdvanceViewsets.logger=[]
#         ## Validation Section
#         branch_id=obj["branch_id"]
#         company_id=obj["company_id"]
#         retValue=True
#         if branch_id is None:
#             SalesCustomerAdvanceViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
#             retValue= False
#         if(company_id is  None ):
#             SalesCustomerAdvanceViewsets.logger.append("company ID is Null Please Provide a company ID")
#             retValue= False
#         if(type(company_id!=uuid)):
#             SalesCustomerAdvanceViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
#             retValue= False
#         return retValue
#
#
#
#
#     def create(self, request, *args, **kwargs):
#         ca_data_converte= request.data['data']
#
#         print("#################################################")
#         print(ca_data_converte)
#         print("Customer Format is ",type(ca_data_converte))
#         print("#################################################")
#         ca_data = json.loads(ca_data_converte)
#         #print("Converted Format is",type(ca_data))
#         #ca_data=ca_data_converte
#         ca_file_data=request.FILES.get('attach_file')
#         print("ca_data",type(ca_file_data))
#
#         # GET coa_deposit_toid in Banking and Pass the bank_id Transaction Table and Main Details Table
#         # bank=ca_data["deposit_to"]
#         # From_Bank=Banking.objects.get(coa_id=bank)
#
#
#         if(SalesCustomerAdvanceViewsets.ValidateDefaults(ca_data)==False):
#             print(" Ooops!!! Error Occured ",SalesCustomerAdvanceViewsets.logger)
#
#         print(ca_data)
#
#
#         #Branch and company null value
#
#         branch_id=ca_data["branch_id"]
#         if branch_id is not None:
#             branch_id=Branch.objects.get(branch_id=branch_id)
#
#         company_id=ca_data["company_id"]
#         if company_id is not None:
#             company_id=Company.objects.get(company_id=company_id)
#
#         customer_id=ca_data["customer_id"]
#         if customer_id is not None:
#             customer_id=SalesCustomer.objects.get(customer_id=customer_id)
#
#
#         #Creating Customer Advance
#         caed_id=CustomerAdvance.objects.create(
#         company_id=company_id,
#         branch_id=branch_id,
#         #bank_id=ca_data['bank_id'],
#         coa_id=COA.objects.get(coa_id=ca_data['deposit_to']),
#         customer_id=customer_id,
#         attach_file=ca_file_data,
#         is_customer_advance_generated=ca_data['is_customer_advance_generated'],
#         supply_place=ca_data["supply_place"],
#         amount_received=ca_data["amount_received"],
#         customer_advance_date=ca_data["payment_date"],
#         received_via=ca_data['payment_mode'],
#         customer_advance_ref_no=ca_data["payment_ref_no"],
#         balance_amount=ca_data["amount_received"],
#         status="Manually Added",
#         description_supply=ca_data["dec_supply_place"],
#         bank_charges=ca_data["bank_charges"],
#         payment_serial=ca_data["payment_serial"],
#         cgst_amount=ca_data["cgst_amount"],
#         sgst_amount=ca_data["sgst_amount"],
#         igst_amount=ca_data['igst_amount'],
#         tax_rate=ca_data["tax_rate"],
#         tax_name=ca_data["tax_name"],
#         tax_type=ca_data["tax_type"])
#         caed_id.save()
#         if ca_file_data is not None:
#             file_ext = os.path.splitext(ca_file_data.name)[1]
#             new_file_path = f'media/CA_{caed_id.ca_id}{file_ext}'
#             with open(new_file_path, 'wb+') as destination:
#                 for chunk in ca_file_data.chunks():
#                     destination.write(chunk)
#             pth = os.path.join(Path(__file__).parent.parent, new_file_path)
#             print('file is here',pth)
#             caed_id.attach_file=pth
#             caed_id.save()
#             print(caed_id)
#
#
#         #Bank Chnarges Section
#         if ca_data['bank_charges'] is not None and float(ca_data['bank_charges']) >0:
#             # transaction_list.append(["Bank Fees and Charges","bank_charges"])
#             TO_COA= COA.objects.get(company_id=company_id,account_subhead="Account Receivables")
#             From_Bank = COA.objects.get(company_id=company_id,account_name="Test Bank")
#             print('QQQ',From_Bank)
#             cabmast=MasterTransaction.objects.create(
#             L1detail_id=caed_id.ca_id,
#             L1detailstbl_name='Customer Advance',
#             L2detail_id=From_Bank.coa_id,
#             L2detailstbl_name='BANK',
#             main_module='Sales',
#             module='MonenyIN',
#             trans_status='Manually Added',
#             sub_module='Customer Advanced',
#             transc_deatils='Customer Advanced',
#             banking_module_type=ca_data["transaction_type"],
#             journal_module_type=ca_data["transaction_type"],
#             trans_date=ca_data["payment_date"],
#             credit=ca_data["bank_charges"],
#             to_account=From_Bank.coa_id,
#             to_acc_type=From_Bank.account_type,
#             to_acc_head=From_Bank.account_head,
#             to_acc_subhead=From_Bank.account_subhead,
#             to_acc_name=From_Bank.account_name,
#             debit=ca_data['bank_charges'],
#             from_account=TO_COA.coa_id,
#             from_acc_type=TO_COA.account_type,
#             from_acc_head=TO_COA.account_head,
#             from_acc_subhead=TO_COA.account_head,
#             from_acc_name=TO_COA.account_name,
#             company_id=company_id,
#             customer_id=customer_id,
#             branch_id=branch_id)
#             cabmast.save()
#
#
# #region MasterTransaction Section
#
#         #In case of with tax =0  so with tax= amount_received
#         with_tax=ca_data['with_tax']
#         if with_tax==0:
#             with_tax=ca_data['amount_received']
#
#         From_COA= COA.objects.get(company_id=company_id,coa_id=ca_data['deposit_to'])
#         TO_COA= COA.objects.get(company_id=company_id,account_subhead="Account Receivables")
#         camast=MasterTransaction.objects.create(
#         L1detail_id=caed_id.ca_id,
#         L1detailstbl_name='Customer Advance',
#         L2detail_id=From_COA.coa_id,
#         L2detailstbl_name='BANK',
#         main_module='Banking',
#         module='MonenyIN',
#         trans_status='Manually Added',
#         sub_module='Customer Advanced',
#         transc_deatils='Customer Advanced',
#         banking_module_type=ca_data["transaction_type"],
#         journal_module_type=ca_data["transaction_type"],
#         trans_date=ca_data["payment_date"],
#         credit=with_tax,
#         to_account=From_COA.coa_id,
#         to_acc_type=From_COA.account_type,
#         to_acc_head=From_COA.account_head,
#         to_acc_subhead=From_COA.account_subhead,
#         to_acc_name=From_COA.account_name,
#         debit=with_tax,
#         from_account=TO_COA.coa_id,
#         from_acc_type=TO_COA.account_type,
#         from_acc_head=TO_COA.account_head,
#         from_acc_subhead=TO_COA.account_head,
#         from_acc_name=TO_COA.account_name,
#         company_id=company_id,
#         customer_id=customer_id,
#         branch_id=branch_id)
#         camast.save()
#        #  %0 taxtion Section
#         Zero_tax=ca_data
#         GST_TAX=None
#         GST_TAX=Zero_tax
#
#         if GST_TAX==Zero_tax is not None:
#             GST_TAX=Zero_tax.get('tax_name')
#         else:
#             pass
#
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX
#
#         else:
#             Both_Tax=None
#
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
#
#
#
#         # User Can the Send the data in request the this data added in this empty list and
#         #this list can perform the operation
#         # all the values are not equal to zero the added the list
#         #list added item to add the master transaction table
#         #chnges of this transaction debit credit and to from account
#         transaction_list = [] #This Empty List added the append
#
#         if float(ca_data['cgst_amount']) >0 or Both_Tax:
#             transaction_list.append(["Output CGST", "cgst_amount"],)
#         if float(ca_data['sgst_amount'] )>0 or Both_Tax:
#             transaction_list.append(["Output SGST", "sgst_amount"])
#         if float(ca_data['igst_amount']) >0 or IGST_0:
#             transaction_list.append(["Output IGST", "igst_amount"],)
#         for transaction in transaction_list:
#
#             #List Of index added 0 is get Account_name
#             From_COA = COA.objects.get(company_id=company_id,account_name=transaction[0])
#             #Transaction Time to you TO_COA will account Subhead
#             TO_COA=COA.objects.get(company_id=company_id,coa_id=ca_data['deposit_to'])
#
#             camast = MasterTransaction.objects.create(
#                 L1detail_id=caed_id.ca_id,
#                 L1detailstbl_name='Customer Advance',
#                 L2detail_id=From_COA.coa_id,
#                 L2detailstbl_name='COA',
#                 main_module='Sales',
#                 module='Refund',
#                 sub_module='Customer Advanced',
#                 transc_deatils='Customer Advanced',
#                 banking_module_type=ca_data["transaction_type"],
#                 journal_module_type=ca_data["transaction_type"],
#                 trans_date=ca_data["payment_date"],
#                 trans_status='Manually Added',
#                 debit=ca_data[transaction[1]],
#                 to_account=TO_COA.coa_id,
#                 to_acc_type=TO_COA.account_type,
#                 to_acc_head=TO_COA.account_head,
#                 to_acc_subhead=TO_COA.account_subhead,
#                 to_acc_name=TO_COA.account_name,
#                 credit=ca_data[transaction[1]],
#                 from_account=From_COA.coa_id,
#                 from_acc_type=From_COA.account_type,
#                 from_acc_head=From_COA.account_head,
#                 from_acc_subhead=From_COA.account_subhead,
#                 from_acc_name=From_COA.account_name,
#                 company_id=company_id,
#                 customer_id=customer_id)
#             camast.save()
#
#
#
#
# #endregion End Master Transaction Section
#         serializer = CustomerAdvancedSerializer(caed_id)
#         return Response(serializer.data)
#
# #Sales Customer Advanced Refund Journal Transaction
#
# n_data=None
# @api_view(['GET'])
# def getCARJournalTransaction(self,ca_id):
#     form_mast = MasterTransaction.objects.filter(L1detail_id=ca_id)
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
#
#
#     df_accounts = pd.concat([from_acc, to_acc])
#     response = json.loads(df_accounts.to_json(orient='records'))
#
#     serializer = MasterTransactionSerializer(form_mast, many=True)
#     n_data=serializer.data
#     all_response = {
#             # 'original_data': account_type_list,
#             'form_data': n_data,
#             'transaction': response,
#         }
#     return Response(all_response)
#
#
# # api for get bill by company id and bill id
# @api_view(['GET'])
# def download_carf_data(request, comp_id,ca_id):
#     company = Company.objects.get(company_id=comp_id)
#     ca = CustomerAdvance.objects.get(ca_id=ca_id)
#     # here filter the object of bill id and company id
#     precieved = PR.objects.filter(
#         company_id=comp_id,ca_id=ca_id).order_by('created_date')
#     serializers =CustomerAdvancedSerializer(precieved, many=True)
#     output_pdf=f"CARF_{datetime.datetime.now().timestamp()}.pdf"
#     generate_pr_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
#     if output_pdf:
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadcarf/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)
#
# def download_carf(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#     response = FileResponse(open(file_path,'rb'),as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,
#     return response
# class CustomerAdvGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = CustomerAdvance.objects.all()
#     serializer_class = CustomerAdvancedSerializer
#
#     def get(self, request, pk=None):
#         if pk:
#             return_data = self.retrieve(request, pk).data
#             return_data['attach_file'] = 'salescustomer/carffile_download/{}/'.format(
#                 pk)
#             return Response({
#                 'data': return_data
#             })
#         return self.list(request)
#
# class CARFFileDownloadListAPIView(generics.ListAPIView):
#
#     def get(self, request, ca_id, format=None):
#         queryset = CustomerAdvance.objects.get(ca_id=ca_id)
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
#         else:
#             return HttpResponse('File not Found in Model')
#
#
#
# #Sales Credit Note refunfd from
#
# class SalesCNRefundModelViewSets(viewsets.ModelViewSet):
#     queryset=RefundMaster.objects.all()
#     serializer_class=CreditNoteRefundSerialiser
#     logger=[]
#     # Forone API are going to make three append append namely for Two Main Sections
#       #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
#       #  2: Financial Transaction:
#         #2.1 Credit Transation
#         #2.2 Debit Transaaction
#     def ValidateDefaults(obj):
#         SalesCNRefundModelViewSets.logger=[]
#         ## Validation Section
#
#         company_id=obj["company_id"]
#         customer_id=obj["customer_id"]
#         cn_id=obj["cn_id"]
#         retValue=True
#         if customer_id is None:
#             SalesCNRefundModelViewSets.logger.append("Customer iD is Null Please Provide a Customer ID")
#             retValue= False
#
#         if(company_id is  None ):
#             SalesCNRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
#             retValue= False
#         if(type(company_id!=uuid)):
#             SalesCNRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
#             retValue= False
#         if(type(cn_id!=uuid)):
#             SalesCNRefundModelViewSets.logger.append("creditnote ID is not a Valid UUID Please Provide a valid creditnote ID ")
#             retValue= False
#
#         return retValue
#
#     def create(self, request, *args, **kwargs):
#         Cnrefund_data = request.data
#
#         # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
#         # bank=Cnrefund_data["coa_id"]
#         # From_Bank=Banking.objects.get(coa_id=bank)
#
#
#         if(SalesCNRefundModelViewSets.ValidateDefaults(Cnrefund_data)==False):
#             print(" Ooops!!! Error Occured ",SalesCNRefundModelViewSets.logger)
#
#         print(Cnrefund_data)
#             #What if this ID is null ,
#
#
#         company_id=Cnrefund_data["company_id"]
#         if company_id is not None:
#             company_id=Company.objects.get(company_id=company_id)
#
#         customer_id=Cnrefund_data["customer_id"]
#         if customer_id is not None:
#             customer_id=SalesCustomer.objects.get(customer_id=customer_id)
#
#         creditnote_id=Cnrefund_data["cn_id"]
#         print("cnid",creditnote_id,type(creditnote_id))
#
#         cnrefund_id=RefundMaster.objects.create(
#             company_id=company_id,
#             bank_id=Cnrefund_data["bank_id"],
#             customer_id=customer_id,
#             refrence_id=creditnote_id,
#             coa_id=COA.objects.get(coa_id=Cnrefund_data["coa_id"]),
#             refund_date=Cnrefund_data["refund_on"],
#             is_cn_refund_generated=Cnrefund_data["is_cn_refund_generated"],
#             status=Cnrefund_data["status"],
#             refund_ref_no=Cnrefund_data["refund_ref_no"],
#             refund_balance_amount=Cnrefund_data["refund_balance_amount"],
#             amount=Cnrefund_data["amount"],
#             serial_ref=Cnrefund_data["cn_serial"],
#             amount_ref=Cnrefund_data["cn_amount"],
#             payment_mode=Cnrefund_data["payment_mode"],
#             description=Cnrefund_data["description"])
#         cnrefund_id.save()
#         print("Cnrefund_created",cnrefund_id,type(cnrefund_id))
#
#
#
#
# #region Master Transaction Section
#
#         TO_COA =COA.objects.get(company_id=company_id,account_name="Account Receivables")
#         From_COA=COA.objects.get(company_id=company_id,coa_id=Cnrefund_data["coa_id"])
#         print('""""""""""""',TO_COA)
#         CNRmast=MasterTransaction.objects.create(
#         L1detail_id=cnrefund_id.rm_id,
#         L1detailstbl_name='RefundMaster',
#         L2detail_id=From_COA.coa_id,
#         L2detailstbl_name='COA',
#         L3detail_id=creditnote_id,
#         L3detailstbl_name='Credit Note',
#         main_module='Sales',
#         module='Refund',
#         sub_module='CreditNoteRefund',
#         transc_deatils='Credit Note Refund',
#         banking_module_type=Cnrefund_data["transaction_module"],
#         journal_module_type='Refund',
#         trans_date=Cnrefund_data["refund_on"],
#         trans_status=Cnrefund_data["status"],
#         debit=Cnrefund_data["entered_amount"],
#         to_account=TO_COA.coa_id,
#         to_acc_type=TO_COA.account_type,
#         to_acc_head=TO_COA.account_head,
#         to_acc_subhead=TO_COA.account_subhead,
#         to_acc_name=TO_COA.account_name,
#         credit=Cnrefund_data['amount'],
#         from_account=From_COA.coa_id,
#         from_acc_type=From_COA.account_type,
#         from_acc_head=From_COA.account_head,
#         from_acc_subhead=From_COA.account_subhead,
#         from_acc_name=From_COA.account_name,
#         company_id=company_id,
#         customer_id=customer_id)
#
#         CNRmast.save()
#
# #endregion
#
# #End Master Transaction Section Credit Note refund
#
#         cn_id=Cnrefund_data["cn_id"]
#         if cn_id is not None:
#             cn_id=CreditNote.objects.get(cn_id=cn_id)
#
#             balance_amount=Cnrefund_data["refund_balance_amount"]
#             print("Amount values are",balance_amount,type(balance_amount))
#             if balance_amount == 0:
#             # cn_id =cn_id
#                 print('cn_id', cn_id)
#                 cn_id.status='Closed'
#                 cn_id.cn_status='Closed'
#                 cn_id.balance_amount= Cnrefund_data["refund_balance_amount"]
#                 cn_id.save()
#                 print('creditnote status updated to ', cn_id.status)
#
#             elif balance_amount >= 0:
#             # cn_id = cn_id
#                 print('credit note id of else', cn_id)
#                 cn_id.balance_amount= Cnrefund_data["refund_balance_amount"]
#                 cn_id.save()
#                 print('credinote amount due updated to ', cn_id.balance_amount)
#             else:
#             # cn_id =cn_id
#                 print('cn_id', cn_id)
#                 cn_id.status='open'
#                 cn_id.save()
#                 print('creditnote status updated to ', cn_id.status)
#
#
#         serializer =CreditNoteRefundSerialiser(cnrefund_id)
#         return Response(serializer.data)
#
#
#
#
#
#
#
# @api_view(['PUT'])
# def updateinvoice(request, invoice_id):
#     invoice = Invoice.objects.get(invoice_id=invoice_id)
#     serializer=InvoiceSerializer(instance=invoice,data=request.data)
#     print(serializer)
#     if serializer.is_valid():
#         serializer.invoice_serial=serializer.data[''],
#         serializer.save()
#         print('Yes')
#
#     return Response(serializer.data)
#
#
#
#
#
#
#
#
#
# class InvoiceUpdateViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer
#
#     def update(self, request, pk, *args, **kwargs):
#         #dxfxfddfc
#         invoice_data=request.data
#         invoice = Invoice.objects.get(invoice_id=pk)
#
#         for invoice_item_data in invoice_data['invoice_items']:
#             invoice_item = InvoiceItem.objects.get(item_id=invoice_item_data['item_id'])
#
#             item_serializer=InvoiceItemSerializer(invoice_item,data=invoice_item_data)
#             if item_serializer.is_valid():
#                 item_serializer.save()
#                 #  Response({"data":item_serializer.data})
#             else:
#                 return Response(item_serializer.errors, status=400)
#
#
#
#         serializer = InvoiceSerializer(invoice, data=invoice_data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"data":serializer.data})
#         else:
#             return Response(serializer.errors, status=400)
#
#
# ############# GENERATE CUSTOMER ADVANCED PDF AND DOWNLOAD ##############################
# @api_view(['GET'])
# def download_customer_advanced_data(request, comp_id,ca_id):
#     company = Company.objects.get(company_id=comp_id)
#     ca = CustomerAdvance.objects.get(ca_id=ca_id)
#     # here filter the object of bill id and company id
#     carecieved = CustomerAdvance.objects.filter(
#         company_id=comp_id,ca_id=ca_id).order_by('created_date')
#
#     serializers =CustomerAdvancedSerializer(carecieved, many=True)
#     print("```````````````````````````````````````````````33333333",serializers.data)
#     output_pdf = f"PR_{datetime.datetime.now().timestamp()}.pdf"
#     generate_customer_advance_pdf(data=serializers.data,output_path=os.path.join("media", output_pdf))
#
#     if os.path.exists(os.path.join("media", output_pdf)):
#         http = 'https' if request.is_secure() else 'http'
#         pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadpr/{output_pdf}'
#     else:
#         pdf_url = 'File Not found'
#      # give pdf url to download path
#     response = pdf_url
# #return Response(response)
#     return Response(response)
#
# def download_ca(request, file_name):
#     file_path = f"media/{file_name}"
#    # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
#     response = FileResponse(open(file_path,'rb'), as_attachment=True)
#    # response = FileResponse(open(file_path, 'rb'), as_attachment=True)
#     #response = FileResponse(file_data, as_attachment=True,
#     return response
# ################################################################################
#
#
#
#
# class InvoiceUpdate2ViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer
#     def update(self, request, pk, *args, **kwargs):
#         #dxfxfddfc
#         invoice_data=request.data
#         invoice = Invoice.objects.get(invoice_id=pk)
#
#         for invoice_item_data in invoice_data['invoice_items']:
#
#             try:
#                 try:
#                     invoice_item = InvoiceItem.objects.get(item_id=invoice_item_data['item_id'],invoice_id=invoice)
#                 except KeyError:
#                     invoice_item=None
#
#
#             except InvoiceItem.DoesNotExist:
#                 invoice_item=None
#
#             #print(invoice_item)
#             if invoice_item is not None:
#                 item_serializer=InvoiceItemSerializer(invoice_item,data=invoice_item_data)
#                 if item_serializer.is_valid():
#                     item_serializer.save()
#                     #  Response({"data":item_serializer.data})
#                 # else:
#                 #     return Response(item_serializer.errors, status=400)
#             else:
#                 try:
#                     coa=COA.objects.get(coa_id=invoice_item_data["coa_id"])
#                     item=Item.objects.get(item_id=invoice_item_data["item_id"])
#                 except KeyError:
#                     coa=None
#                     item=None
#                 #print(invoice_item)
#                 try:
#                     invoice_items = InvoiceItem.objects.create(invoice_id=invoice,
#                                                         item_id=item,
#                                                         coa_id=coa,
#                                                         item_name=invoice_item_data["item_name"],
#                                                         rate=invoice_item_data["rate"],
#                                                         quantity=invoice_item_data["quantity"],
#                                                         tax_rate=invoice_item_data["tax_rate"],
#                                                         tax_name=invoice_item_data["tax_name"],
#                                                         tax_type=invoice_item_data["tax_type"],
#                                                         sgst_amount=invoice_item_data["sgst_amount"],
#                                                         cgst_amount=invoice_item_data["cgst_amount"],
#                                                         igst_amount=invoice_item_data["igst_amount"],
#                                                         # taxamount=item["taxamount"],
#                                                         amount=invoice_item_data["amount"])
#                     invoice_items.save()
#
#                 except KeyError:
#                     pass
#
#
#         serializer = InvoiceSerializer(invoice, data=invoice_data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"data":serializer.data})
#         else:
#             return Response(serializer.errors, status=400)
#
#
#
#
#
# class InvoiceUpdate3ViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer
#     def update(self, request, pk, *args, **kwargs):
#         #dxfxfddfc
#         invoice_data=request.data
#         invoice = Invoice.objects.get(invoice_id=pk)
#         comp_id = Company.objects.get(company_id=invoice_data["company_id"])
#         cust_id = SalesCustomer.objects.get(
#             customer_id=invoice_data["customer_id"])
#
#         #account receivable varibale are declaret the chart of account of to side from item and taxation Section
#         #and Discount time this chartof Account is From Side
#         account_receivable = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#         # Invoice Item Looping
#         for invoice_item_data in invoice_data['invoice_items']:
#         # Item are find Out Section
#             print(invoice_item_data['item_name'])
#             try:
#                 try:
#                     invoice_item = InvoiceItem.objects.get(item_id=invoice_item_data['item_id'],invoice_id=invoice)
#
#                 except KeyError:
#                     invoice_item=None
#
#
#
#             except InvoiceItem.DoesNotExist:
#                 invoice_item=None
#
#             # Invoice Item Are Find the update this Code Section
#             if invoice_item is not None:
#                 item_serializer=InvoiceItemSerializer(invoice_item,data=invoice_item_data)
#                 if item_serializer.is_valid():
#                     item_serializer.save()
#
#             else:
#                 try:
#                     # Get The Chart Of Account and item Id Of the Item Related
#                     coa=COA.objects.get(coa_id=invoice_item_data["coa_id"])
#                     item=Item.objects.get(item_id=invoice_item_data["item_id"])
#                 except KeyError:
#                     coa=None
#                     item=None
#
#                 try:
#                     #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
#                     invoice_items = InvoiceItem.objects.create(invoice_id=invoice,
#                                                         item_id=item,
#                                                         coa_id=coa,
#                                                         item_name=invoice_item_data["item_name"],
#                                                         rate=invoice_item_data["rate"],
#                                                         quantity=invoice_item_data["quantity"],
#                                                         tax_rate=invoice_item_data["tax_rate"],
#                                                         tax_name=invoice_item_data["tax_name"],
#                                                         tax_type=invoice_item_data["tax_type"],
#                                                         sgst_amount=invoice_item_data["sgst_amount"],
#                                                         cgst_amount=invoice_item_data["cgst_amount"],
#                                                         igst_amount=invoice_item_data["igst_amount"],
#                                                         # taxamount=item["taxamount"],
#                                                         amount=invoice_item_data["amount"])
#                     invoice_items.save()
#
#                 except KeyError:
#                     pass
#
#
#
#
#         #this Section Is Invoice Data Update Serializer Through
#         serializer = InvoiceSerializer(invoice, data=invoice_data)
#
#         if serializer.is_valid():
#             invoice_id=serializer.save()
#
#             # return Response({"data":serializer.data})
#         else:
#             return Response(serializer.errors, status=400)
#
#         stock_item_list=[]
#         stock_transactiom_item_list=[]
#
#         for invoice_item_stock in invoice_data['invoice_items']:
#             stock_item_list.append(invoice_item_stock['item_name'])
#             try:
#                 stock_item=Stock.objects.get(item_id=invoice_item_stock['item_id'],ref_id=invoice)
#                 item_value=Item.objects.get(item_id=invoice_item_stock["item_id"])
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                 # stock_serializer=StockSerializer(stock_item,data=invoice_item_data)
#                 print("updating stock", invoice_item_stock['quantity'], invoice_item_stock['item_id'])
#                 stock_item.stock_out=invoice_item_stock['quantity']
#                 stock_item.rate=current_assets_last_stock.rate
#                 stock_item.amount=current_assets_last_stock.rate*int(invoice_item_stock['quantity'])
#                 stock_item.quantity=invoice_item_stock['quantity']
#                 stock_item.save()
#                 stock_transactiom_item_list.append(stock_item)
#             except Stock.DoesNotExist:
#                 item_value=Item.objects.get(item_id=invoice_item_stock["item_id"])
#
#
#                 track_inventory=invoice_item_stock.get('selected_item_name',{}).get('track_inventory')
#                 print('inventory',track_inventory)
#                 if track_inventory==True:
#                     stk_in=Stock.objects.filter(item_id=invoice_item_stock["item_id"]).exclude(stock_in=0).order_by('created_date')
#                     stk_out=Stock.objects.filter(item_id=invoice_item_stock["item_id"]).exclude(stock_out=0).order_by('created_date')
#
#                     print(stk_out)
#                     stock_int_items = stk_in
#                     already_stock_out_items =stk_out
#                     item_to_sell = invoice_item_stock["quantity"]
#
#                     # -------------------------------------------------
#
#                     # Check if the stock is available
#                     sum_of_stock_in = sum([_.stock_in for _ in stock_int_items])
#                     sum_of_stock_in_amount = sum([_.amount for _ in stock_int_items])
#                     print("sum_of_stock_in_amount", sum_of_stock_in_amount)
#
#                     sum_of_already_stock_out = sum([_.stock_out for _ in already_stock_out_items])
#                     print("sum_of_already_stock_out", sum_of_already_stock_out)
#
#                     if sum_of_stock_in - (sum_of_already_stock_out + item_to_sell) < 0:
#                         print("Stock not available")
#                         return Response('Stock is not Avilable')
#
#                     print("Stock available")
#                     current_stock=sum_of_stock_in-sum_of_already_stock_out
#                     print('item is herer',item_value.item_id)
#                     current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                     print("current Assets_vlaue",current_assets_last_stock.amount)
#                     future_stock_outs = []
#                     for stock_in_item in stock_int_items:
#                         print(stock_in_item)
#                         if item_to_sell==0:
#                             break
#                         if sum_of_already_stock_out - stock_in_item.stock_in >= 0:
#                             print("\tItem fully sold")
#                             sum_of_already_stock_out = sum_of_already_stock_out - stock_in_item.stock_in
#                             print("\tRemaining already sold items: ", sum_of_already_stock_out)
#                             continue
#
#                         if sum_of_already_stock_out > 0:
#                             print("\tItem partially unsold")
#                             remaining_unsold_items = stock_in_item.stock_in - sum_of_already_stock_out
#                             print("\tRemaining unsold items", remaining_unsold_items)
#                             sum_of_already_stock_out = 0
#                         else:
#                             print("\tItem fully unsold")
#                             remaining_unsold_items = stock_in_item.stock_in
#
#                         if item_to_sell > remaining_unsold_items:
#                             print("\tMore items need to be sold")
#                             print(f"\tSelling {remaining_unsold_items} items")
#
#                             future_stock_outs=Stock.objects.create(
#                             item_id=invoice_item_stock["item_id"],
#                             item_name=invoice_item_stock["item_name"],
#                             stock_out=remaining_unsold_items,
#                             ref_id=invoice_id,
#                             amount=current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate,
#                             rate=current_assets_last_stock.rate,
#                             ref_tblname='Invoice',
#                             quantity=remaining_unsold_items,
#                             #stock_on_hand=current_stock-remaining_unsold_items,
#                             formname='Invoice',
#                             stage='Add Stages',
#                             date=invoice_data["invoice_date"],
#                             company_id=comp_id)
#                             current_assets_last_stock.amount = current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate
#                             current_stock = current_stock-remaining_unsold_items
#
#
#
#                             item_to_sell = item_to_sell - remaining_unsold_items
#                             print(f"\t{item_to_sell} still needed by the buyer")
#                         else:
#                             print(f"\tSelling {item_to_sell} items")
#                             future_stock_outs=Stock.objects.create(
#                             item_id=invoice_item_stock["item_id"],
#                             item_name=invoice_item_stock["item_name"],
#                             stock_out=item_to_sell,
#                             ref_id=invoice_id,
#                             amount=current_assets_last_stock.amount- item_to_sell*stock_in_item.rate,
#                             rate=current_assets_last_stock.rate,
#                             quantity=item_to_sell,
#                             ref_tblname='Invoice',
#                             #stock_on_hand=current_stock-item_to_sell,
#                             module='Sales',
#                             formname='Invoice',
#                             stage='Add Stages',
#                             date=invoice_data["invoice_date"],
#                             company_id=comp_id)
#
#
#                             item_to_sell = 0
#
#
#                         print("------------")
#
#
#
#
#
#
#
#
#
#                 #This Section Is Stock Journal Transaction
#                 #Stock Charetd Account name is Inventory Assets
#                 #item select time has three chart of account must be
#                 #Sales Account,Purchase Account ,Inventory Accounts
#
#                         # inv_item=invoice_data.get('invoice_items')
#                         purchase_account=invoice_item_stock.get('selected_item_name').get('purchase_account')
#                         inventory_account=invoice_item_stock.get('selected_item_name').get('inventory_account')
#                         if purchase_account is not None:
#                             TO_COA = COA.objects.get(company_id=comp_id,coa_id=purchase_account)
#                         else:
#                             print("No Chart of Account Found")
#                         if inventory_account is not None:
#                             FROM_COA=COA.objects.get(company_id=comp_id,coa_id=inventory_account)
#                         else:
#                             print("No Chart of Account Found")
#
#                         print('item rate',future_stock_outs.rate)
#                         print('item quantity',future_stock_outs.quantity)
#                         stkmast = MasterTransaction.objects.create(
#                             L1detail_id=invoice_id.invoice_id,
#                             L1detailstbl_name='Invoice',
#                             L2detail_id=future_stock_outs.st_id,
#                             L2detailstbl_name='Stock',
#                             main_module='Sales',
#                             module='Invoice',
#                             sub_module='Invoice',
#                             transc_deatils='Invoice',
#                             banking_module_type='Invoice',
#                             journal_module_type='Invoice',
#                             trans_date=invoice_data["invoice_date"],
#                             trans_status='Manually Added',
#                             debit=future_stock_outs.rate*future_stock_outs.quantity,
#                             to_account=TO_COA.coa_id,
#                             to_acc_type=TO_COA.account_type,
#                             to_acc_head=TO_COA.account_head,
#                             to_acc_subhead=TO_COA.account_subhead,
#                             to_acc_name=TO_COA.account_name,
#                             credit=future_stock_outs.rate*future_stock_outs.quantity,
#                             from_account=FROM_COA.coa_id,
#                             from_acc_type=FROM_COA.account_type,
#                             from_acc_head=FROM_COA.account_head,
#                             from_acc_subhead=FROM_COA.account_subhead,
#                             from_acc_name=FROM_COA.account_name,
#                             company_id=comp_id,
#                             customer_id=cust_id)
#                         stkmast.save()
#                         print('Sucessfully Added Transaction')
#
#
#
#
#
#         # Zero tax Calculation Section
#         Zero_tax=invoice_data.get('invoice_items')
#         GST_TAX=None
#         GST_TAX=Zero_tax[0]
#
#         if GST_TAX==Zero_tax[0].get('selected_tax_name') is not None:
#             GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
#         else:
#             pass
#
#
#
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX
#
#         else:
#             Both_Tax=None
#
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
#
#         #This Section Is The Tax and Shiping Charges ,And tcs Amount is Find the add the
#         #transaction_list
#
#         transaction_list = [] #This Empty List added the append
#         if float(invoice_data['tcs_amount'])>0:
#             transaction_list.append(["TCS Payable","tcs_amount"])
#         if float(invoice_data['shipping_charges']) >0:
#             transaction_list.append(["Shipping Charges","shipping_charges"])
#         if float(invoice_data['cgst_total']) >0 or Both_Tax:
#             transaction_list.append(["Output CGST", "cgst_total"],)
#         if float(invoice_data['sgst_total'] )>0 or Both_Tax:
#             transaction_list.append(["Output SGST", "sgst_total"])
#         if float(invoice_data['igst_total']) >0 or IGST_0:
#             transaction_list.append(["Output IGST", "igst_total"],)
#         acc_from_list=[]
#         acc_to_list=[]
#         #Looping the Added Transaction List Chrat of Account
#         # and this Credit and debit value
#         #this list type is list of list eg: [[Chart of account ,invoicedata[igst_total]]]
#         for transaction in transaction_list:
#
#             for account_transaction in [transaction[0]]:
#                 acc_from_list.append(account_transaction)
#                 if account_transaction is not None:
#                     try:
#                         #this Section is List Addded Charted Of account Updated
#                         account_list=MasterTransaction.objects.get(from_acc_name=account_transaction,L1detail_id=invoice_id)
#                         account_list.credit=invoice_data[transaction[1]]
#                         account_list.debit=invoice_data[transaction[1]]
#                         account_list.save()
#
#
#                     except MasterTransaction.DoesNotExist:
#                         #List Are Addded New Chart of Account this Code Will be ecxecuted
#                         #Menas New transaction Are Created in Master Transaction Section
#
#                         TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#                         account_receivable = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#                         invomast = MasterTransaction.objects.create(
#                             L1detail_id=invoice_id.invoice_id,
#                             L1detailstbl_name='Invoice',
#                             main_module='Sales',
#                             module='Invoice',
#                             sub_module='Invoice',
#                             transc_deatils='Invoice',
#                             banking_module_type='Invoice',
#                             journal_module_type='Invoice',
#                             trans_date=invoice_data["invoice_date"],
#                             trans_status='Manually Added',
#                             debit=invoice_data[transaction[1]],
#                             to_account=account_receivable.coa_id,
#                             to_acc_type=account_receivable.account_type,
#                             to_acc_head=account_receivable.account_head,
#                             to_acc_subhead=account_receivable.account_subhead,
#                             to_acc_name=account_receivable.account_name,
#                             credit=invoice_data[transaction[1]],
#                             from_account=TO_COA.coa_id,
#                             from_acc_type=TO_COA.account_type,
#                             from_acc_head=TO_COA.account_head,
#                             from_acc_subhead=TO_COA.account_subhead,
#                             from_acc_name=TO_COA.account_name,
#                             company_id=comp_id,
#                             customer_id=cust_id)
#                         invomast.save()
#
#
#
#             #  This Sectio Is Discount
#             # Diffrance in Tax Section And Disscount Section Is Tax Side From Account Is Discount Section To Side
#             #and Discount From Side Account is Tax Side is To side
#             #Change The Credit and Debit side
#             try:
#                 #This Section is Disscount will Be find to this code will Be Excuted
#                 item_discount_list=MasterTransaction.objects.get(to_acc_name='Discount',L1detail_id=invoice_id)
#
#                 item_discount_list.credit=invoice_data['discount']
#                 item_discount_list.debit=invoice_data['discount']
#                 item_discount_list.save()
#                 acc_to_list.append('Discount')
#             # This Section List are addded the Disscount Create mastertransaction new entry
#             except MasterTransaction.DoesNotExist:
#                 if int(invoice_data['discount'])>0:
#                     TO_COA = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#                     account_receivable = COA.objects.get(company_id=comp_id, account_name="Discount")
#                     invomast = MasterTransaction.objects.create(
#                         L1detail_id=invoice_id.invoice_id,
#                         L1detailstbl_name='Invoice',
#                         main_module='Sales',
#                         module='Invoice',
#                         sub_module='Invoice',
#                         transc_deatils='Invoice',
#                         banking_module_type='Invoice',
#                         journal_module_type='Invoice',
#                         trans_date=invoice_data["invoice_date"],
#                         trans_status='Manually Added',
#                         debit=invoice_data['discount'],
#                         to_account=account_receivable.coa_id,
#                         to_acc_type=account_receivable.account_type,
#                         to_acc_head=account_receivable.account_head,
#                         to_acc_subhead=account_receivable.account_subhead,
#                         to_acc_name=account_receivable.account_name,
#                         credit=invoice_data['discount'],
#                         from_account=TO_COA.coa_id,
#                         from_acc_type=TO_COA.account_type,
#                         from_acc_head=TO_COA.account_head,
#                         from_acc_subhead=TO_COA.account_subhead,
#                         from_acc_name=TO_COA.account_name,
#                         company_id=comp_id,
#                         customer_id=cust_id)
#                     invomast.save()
#                     acc_to_list.append('Discount')
#
#
#
#     #This Section is Item Transaction The Item transaction Can't Created Is only updated
#     #this only Chnage the Credit and debit Side values
#     #Other can;t Change
#
#
#
#
#         #This Section is Item chart of account and amount group by section
#         coa_amount_dict = {}
#         for invoice_item in invoice_data['invoice_items']:
#             if coa_amount_dict.get(invoice_item['coa_id']) is None:
#                 coa_amount_dict[invoice_item['coa_id']
#                                 ] = invoice_item['amount']
#             else:
#                 coa_amount_dict[invoice_item['coa_id']
#                                 ] = coa_amount_dict[invoice_item['coa_id']] + invoice_item['amount']
#
#             for coa_id, amount in coa_amount_dict.items():
#
#                 coa_mast=MasterTransaction.objects.filter(from_account=coa_id,L1detail_id=invoice_id)
#                 for coa in coa_mast:
#
#                     coa_acc=coa.from_acc_name
#
#
#         #this Section Is Mastertransction item related
#         item_transaction_list = [coa_acc]
#         acc_from_list.append(coa_acc)
#
#         for item_transaction in item_transaction_list:
#
#             item_account_list=MasterTransaction.objects.get(from_acc_name=item_transaction,L1detail_id=invoice_id)
#             item_account_list.credit=amount
#             item_account_list.debit=amount
#             item_account_list.save()
#
#
#
#         trans_stock_list= Stock.objects.filter(ref_id=invoice_id).exclude(item_name__in=stock_item_list)
#         for trans_stock in trans_stock_list:
#             mast_stock=trans_stock.st_id
#             transaction_stock= MasterTransaction.objects.filter(L1detail_id=invoice_id,L2detail_id=str(mast_stock)).delete()
#
#         del_stock= Stock.objects.filter(ref_id=invoice_id).exclude(item_name__in=stock_item_list).delete()
#
#
#
#     #this Section Is the Delete the Trnsaction Not Fined is List Mens Remove the Transaction
#         #master_stock variable is the remaning of stock item in master transaction
#         master_stock_list=[]
#         master_stock= MasterTransaction.objects.filter(L1detail_id=invoice_id,L2detailstbl_name='Stock')
#         for stock_trans_mast in master_stock:
#             master_stock_list.append(stock_trans_mast.from_acc_name)
#         Both_List=acc_from_list+master_stock_list
#
#         topics = MasterTransaction.objects.filter(L1detail_id=invoice_id).exclude(from_acc_name__in=Both_List).exclude(to_acc_name__in=Both_List).delete()
#         print('Both List Is here',Both_List)
#
#         serializer = InvoiceSerializer(invoice_id)
#         return Response(serializer.data)
#
#
#
#
# @api_view(['GET'])
# def getAllInvoicedetails(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": Invoice.objects.count()}
#
#     queryset = Invoice.objects.all()[offset:offset + limit]
#     serializer = InvoiceSerializer(queryset, many=True)
#
#     response['results'] = InvoiceSerializer(queryset, many=True).data
#     return Response(response)
#
# #     invoice = Invoice.objects.all()
# #     serializer = InvoiceSerializer(invoice, many=True)
# #    # serializer = JoinItemSerializer(estimate, many=True)
# #     return Response(serializer.data)
# # getshortDetails
# @api_view(['GET'])
# def ShortInvoiceDetails(request):
#     invoice = Invoice.objects.all()
#     serializer = ShortInvoiceSerializer(invoice, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def getAllPeginatedInvoiceDetails(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": Invoice.objects.count()}
#
#     queryset = Invoice.objects.all()[offset:offset + limit]
#     serializer = ShortInvoiceSerializer(queryset, many=True)
#
#     response['results'] = ShortInvoiceSerializer(queryset, many=True).data
#     return Response(response)
#
#
#
# @api_view(['GET'])
# def getAllPeginatedCustomerDetails(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": SalesCustomer.objects.count()}
#
#     queryset = SalesCustomer.objects.all()[offset:offset + limit]
#     serializer = ShortCustomerSerializer(queryset, many=True)
#
#     response['results'] = ShortCustomerSerializer(queryset, many=True).data
#     return Response(response)
#
# # getcust
#
# @api_view(['GET'])
# def getAllPeginatedCustomername(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": SalesCustomer.objects.count()}
#
#     queryset = SalesCustomer.objects.all()[offset:offset + limit]
#     serializer = customernameSerializer(queryset, many=True)
#
#     response['results'] = customernameSerializer(queryset, many=True).data
#     return Response(response)
#
#
#
# @api_view(['GET'])
# def getPeginatedShortEstimateDetails(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": Estimate.objects.count()}
#
#     queryset = Estimate.objects.all()[offset:offset + limit]
#     serializer = ShortEstimateSerializer(queryset, many=True)
#
#     response['results'] = ShortEstimateSerializer(queryset, many=True).data
#     return Response(response)
#
#
# @api_view(['GET'])
# def getAllPeginatedEstimateDetails(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": Estimate.objects.count()}
#
#     queryset = Estimate.objects.all()[offset:offset + limit]
#     serializer = EstimateSerializer(queryset, many=True)
#
#     response['results'] = EstimateSerializer(queryset, many=True).data
#     return Response(response)
#
#
#
# @api_view(['GET'])
# def getShortPeginatedSalesOrderDetails(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": SO.objects.count()}
#
#     queryset = SO.objects.all()[offset:offset + limit]
#     serializer = ShortSalesOrderSerializer(queryset, many=True)
#
#     response['results'] = ShortSalesOrderSerializer(queryset, many=True).data
#     return Response(response)
#
#
#
# @api_view(['GET'])
# def getShortPeginatedDeliveryChallanDetails(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": DC.objects.count()}
#
#     queryset = DC.objects.all()[offset:offset + limit]
#     serializer = ShortDeliveryChallanSerializer(queryset, many=True)
#
#     response['results'] = ShortDeliveryChallanSerializer(queryset, many=True).data
#     return Response(response)
#
# # getshortDetails
#
#
# @api_view(['GET'])
# def getShortPeginatedCreditNoteDetails(request):
#
#     limit = int(request.GET['limit'])
#     offset = int(request.GET['offset'])
#
#     url = str(request.build_absolute_uri()).split("?")[0]
#     response = {'next': url + f"?limit={limit}&offset={offset + limit}",
#                 'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
#                 "count": CreditNote.objects.count()}
#
#     queryset = CreditNote.objects.all()[offset:offset + limit]
#     serializer = ShortCreditNoteSerializer(queryset, many=True)
#
#     response['results'] = ShortCreditNoteSerializer(queryset, many=True).data
#     return Response(response)
#
#
#
#
#
# class InvoiceUpdate4ViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer
#     def update(self, request, pk, *args, **kwargs):
#         #dxfxfddfc
#         invoice_data=request.data
#         invoice = Invoice.objects.get(invoice_id=pk)
#         comp_id = Company.objects.get(company_id=invoice_data["company_id"])
#         cust_id = SalesCustomer.objects.get(
#             customer_id=invoice_data["customer_id"])
#
#         #account receivable varibale are declaret the chart of account of to side from item and taxation Section
#         #and Discount time this chartof Account is From Side
#         account_receivable = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#         # Invoice Item Looping
#         invoice_item_list=[]
#         for invoice_item_data in invoice_data['invoice_items']:
#             invoice_item_list.append(invoice_item_data['item_id'])
#            # Item are find Out Section
#             print(invoice_item_data['item_name'])
#             try:
#                 try:
#                     invoice_item = InvoiceItem.objects.get(item_id=invoice_item_data['item_id'],invoice_id=invoice.invoice_id)
#
#                 except KeyError:
#                     invoice_item=None
#
#
#
#             except InvoiceItem.DoesNotExist:
#                 invoice_item=None
#
#             # Invoice Item Are Find the update this Code Section
#             if invoice_item is not None:
#                 item_serializer=InvoiceItemSerializer(invoice_item,data=invoice_item_data)
#                 if item_serializer.is_valid():
#                     item_serializer.save()
#
#             else:
#                 try:
#                     # Get The Chart Of Account and item Id Of the Item Related
#                     coa=COA.objects.get(coa_id=invoice_item_data["coa_id"])
#                     item=Item.objects.get(item_id=invoice_item_data["item_id"])
#                 except KeyError:
#                     coa=None
#                     item=None
#
#                 try:
#                     #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
#                     invoice_items = InvoiceItem.objects.create(invoice_id=invoice,
#                                                         item_id=item.item_id,
#                                                         coa_id=coa,
#                                                         item_name=invoice_item_data["item_name"],
#                                                         rate=invoice_item_data["rate"],
#                                                         quantity=invoice_item_data["quantity"],
#                                                         tax_rate=invoice_item_data["tax_rate"],
#                                                         tax_name=invoice_item_data["tax_name"],
#                                                         tax_type=invoice_item_data["tax_type"],
#                                                         sgst_amount=invoice_item_data["sgst_amount"],
#                                                         cgst_amount=invoice_item_data["cgst_amount"],
#                                                         igst_amount=invoice_item_data["igst_amount"],
#                                                         # taxamount=item["taxamount"],
#                                                         amount=invoice_item_data["amount"])
#                     invoice_items.save()
#
#                 except KeyError:
#                     pass
#
#
#         print('Not deleted invoice item',invoice_item_list)
#         del_item = InvoiceItem.objects.filter(invoice_id=invoice.invoice_id).exclude(item_id__in=invoice_item_list).delete()
#         #this Section Is Invoice Data Update Serializer Through
#         serializer = InvoiceSerializer(invoice, data=invoice_data)
#
#         if serializer.is_valid():
#             invoice_id=serializer.save()
#
#             # return Response({"data":serializer.data})
#         else:
#              return Response(serializer.errors, status=400)
#
#         stock_item_list=[]
#         stock_transactiom_item_list=[]
#
#         for invoice_item_stock in invoice_data['invoice_items']:
#             stock_item_list.append(invoice_item_stock['item_name'])
#             try:
#                 stock_item=Stock.objects.get(item_id=invoice_item_stock['item_id'],ref_id=invoice)
#                 item_value=Item.objects.get(item_id=invoice_item_stock["item_id"])
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                 # stock_serializer=StockSerializer(stock_item,data=invoice_item_data)
#                 print("updating stock", invoice_item_stock['quantity'], invoice_item_stock['item_id'])
#                 stock_item.stock_out=float (invoice_item_stock['quantity'])
#                 stock_item.rate=float (current_assets_last_stock.rate)
#                 stock_item.amount=float(current_assets_last_stock.rate) * float(invoice_item_stock['quantity'])
#                 stock_item.quantity=float (invoice_item_stock['quantity'])
#                 stock_item.save()
#                 stock_transactiom_item_list.append(stock_item)
#             except Stock.DoesNotExist:
#                 item_value=Item.objects.get(item_id=invoice_item_stock["item_id"])
#
#
#                 track_inventory=invoice_item_stock.get('selected_item_name',{}).get('track_inventory')
#                 print('inventory',track_inventory)
#                 if track_inventory==True:
#                     stk_in=Stock.objects.filter(item_id=invoice_item_stock["item_id"]).exclude(stock_in=0).order_by('created_date')
#                     stk_out=Stock.objects.filter(item_id=invoice_item_stock["item_id"]).exclude(stock_out=0).order_by('created_date')
#
#                     print(stk_out)
#                     stock_int_items = stk_in
#                     already_stock_out_items =stk_out
#                     item_to_sell = invoice_item_stock["quantity"]
#
#                     # -------------------------------------------------
#
#                     # Check if the stock is available
#                     sum_of_stock_in = sum([_.stock_in for _ in stock_int_items])
#                     sum_of_stock_in_amount = sum([_.amount for _ in stock_int_items])
#                     print("sum_of_stock_in_amount", sum_of_stock_in_amount)
#
#                     sum_of_already_stock_out = sum([_.stock_out for _ in already_stock_out_items])
#                     print("sum_of_already_stock_out", sum_of_already_stock_out)
#                     print('sum_of_stock_in',type(sum_of_stock_in),sum_of_stock_in)
#                     print('sum_of_already_stock_out',type(sum_of_already_stock_out),sum_of_already_stock_out)
#                     print('item_to_sell',type(item_to_sell),item_to_sell)
#                     if sum_of_stock_in - (float (sum_of_already_stock_out) +  (item_to_sell)) < 0:
#                         print("Stock not available")
#                         return Response('Stock is not Avilable')
#
#                     print("Stock available")
#                     current_stock=sum_of_stock_in-sum_of_already_stock_out
#                     print('item is herer',item_value.item_id)
#                     current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                     print("current Assets_vlaue",current_assets_last_stock.amount)
#                     future_stock_outs = []
#                     for stock_in_item in stock_int_items:
#                         print(stock_in_item)
#                         if item_to_sell==0:
#                             break
#                         if sum_of_already_stock_out - stock_in_item.stock_in >= 0:
#                             print("\tItem fully sold")
#                             sum_of_already_stock_out = sum_of_already_stock_out - stock_in_item.stock_in
#                             print("\tRemaining already sold items: ", sum_of_already_stock_out)
#                             continue
#
#                         if sum_of_already_stock_out > 0:
#                             print("\tItem partially unsold")
#                             remaining_unsold_items = stock_in_item.stock_in - sum_of_already_stock_out
#                             print("\tRemaining unsold items", remaining_unsold_items)
#                             sum_of_already_stock_out = 0
#                         else:
#                             print("\tItem fully unsold")
#                             remaining_unsold_items = stock_in_item.stock_in
#
#                         if item_to_sell > remaining_unsold_items:
#                             print("\tMore items need to be sold")
#                             print(f"\tSelling {remaining_unsold_items} items")
#
#                             future_stock_outs=Stock.objects.create(
#                             item_id=invoice_item_stock["item_id"],
#                             item_name=invoice_item_stock["item_name"],
#                             stock_out=remaining_unsold_items,
#                             ref_id=invoice_id,
#                             amount=current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate,
#                             rate=current_assets_last_stock.rate,
#                             ref_tblname='Invoice',
#                             quantity=remaining_unsold_items,
#                             #stock_on_hand=current_stock-remaining_unsold_items,
#                             formname='Invoice',
#                             stage='Add Stages',
#                             date=invoice_data["invoice_date"],
#                             company_id=comp_id)
#                             current_assets_last_stock.amount = current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate
#                             current_stock = current_stock-remaining_unsold_items
#
#
#
#                             item_to_sell = item_to_sell - remaining_unsold_items
#                             print(f"\t{item_to_sell} still needed by the buyer")
#                         else:
#                             print(f"\tSelling {item_to_sell} items")
#                             future_stock_outs=Stock.objects.create(
#                             item_id=invoice_item_stock["item_id"],
#                             item_name=invoice_item_stock["item_name"],
#                             stock_out=item_to_sell,
#                             ref_id=invoice_id,
#                             amount=current_assets_last_stock.amount- item_to_sell*stock_in_item.rate,
#                             rate=current_assets_last_stock.rate,
#                             quantity=item_to_sell,
#                             ref_tblname='Invoice',
#                             #stock_on_hand=current_stock-item_to_sell,
#                             module='Sales',
#                             formname='Invoice',
#                             stage='Add Stages',
#                             date=invoice_data["invoice_date"],
#                             company_id=comp_id)
#
#
#                             item_to_sell = 0
#
#
#                         print("------------")
#
#
#
#
#
#
#
#
#
#                 #This Section Is Stock Journal Transaction
#                 #Stock Charetd Account name is Inventory Assets
#                 #item select time has three chart of account must be
#                 #Sales Account,Purchase Account ,Inventory Accounts
#
#                         # inv_item=invoice_data.get('invoice_items')
#                         purchase_account=invoice_item_stock.get('selected_item_name').get('purchase_account')
#                         inventory_account=invoice_item_stock.get('selected_item_name').get('inventory_account')
#                         if purchase_account is not None:
#                             TO_COA = COA.objects.get(company_id=comp_id,coa_id=purchase_account)
#                         else:
#                             print("No Chart of Account Found")
#                         if inventory_account is not None:
#                             FROM_COA=COA.objects.get(company_id=comp_id,coa_id=inventory_account)
#                         else:
#                             print("No Chart of Account Found")
#
#                         print('item rate',future_stock_outs.rate)
#                         print('item quantity',future_stock_outs.quantity)
#                         stkmast = MasterTransaction.objects.create(
#                             L1detail_id=invoice_id.invoice_id,
#                             L1detailstbl_name='Invoice',
#                             L2detail_id=future_stock_outs.st_id,
#                             L2detailstbl_name='Stock',
#                             main_module='Sales',
#                             module='Invoice',
#                             sub_module='Invoice',
#                             transc_deatils='Invoice',
#                             banking_module_type='Invoice',
#                             journal_module_type='Invoice',
#                             trans_date=invoice_data["invoice_date"],
#                             trans_status='Manually Added',
#                             debit=future_stock_outs.rate*future_stock_outs.quantity,
#                             to_account=TO_COA.coa_id,
#                             to_acc_type=TO_COA.account_type,
#                             to_acc_head=TO_COA.account_head,
#                             to_acc_subhead=TO_COA.account_subhead,
#                             to_acc_name=TO_COA.account_name,
#                             credit=future_stock_outs.rate*future_stock_outs.quantity,
#                             from_account=FROM_COA.coa_id,
#                             from_acc_type=FROM_COA.account_type,
#                             from_acc_head=FROM_COA.account_head,
#                             from_acc_subhead=FROM_COA.account_subhead,
#                             from_acc_name=FROM_COA.account_name,
#                             company_id=comp_id,
#                             customer_id=cust_id)
#                         stkmast.save()
#                         print('Sucessfully Added Transaction')
#
#
#
#
#
#         # Zero tax Calculation Section
#         Zero_tax=invoice_data.get('invoice_items')
#         GST_TAX=None
#         GST_TAX=Zero_tax[0]
#
#         if GST_TAX==Zero_tax[0].get('selected_tax_name') is not None:
#             GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
#         else:
#             pass
#
#
#
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX
#
#         else:
#             Both_Tax=None
#
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
#
#         #This Section Is The Tax and Shiping Charges ,And tcs Amount is Find the add the
#         #transaction_list
#
#         transaction_list = [] #This Empty List added the append
#         print('Checkit',type(invoice_data['tcs_amount']))
#         print('checkit2',invoice_data['tcs_amount'])
#         if float(invoice_data['tcs_amount'])>0:
#             transaction_list.append(["TCS Payable","tcs_amount"])
#         if float(invoice_data['shipping_charges']) >0:
#             transaction_list.append(["Shipping Charges","shipping_charges"])
#         if float(invoice_data['cgst_total']) >0 or Both_Tax:
#             transaction_list.append(["Output CGST", "cgst_total"],)
#         if float(invoice_data['sgst_total'] )>0 or Both_Tax:
#             transaction_list.append(["Output SGST", "sgst_total"])
#         if float(invoice_data['igst_total']) >0 or IGST_0:
#             transaction_list.append(["Output IGST", "igst_total"],)
#         acc_from_list=[]
#         acc_to_list=[]
#         #Looping the Added Transaction List Chrat of Account
#         # and this Credit and debit value
#         #this list type is list of list eg: [[Chart of account ,invoicedata[igst_total]]]
#         for transaction in transaction_list:
#
#             for account_transaction in [transaction[0]]:
#                 acc_from_list.append(account_transaction)
#                 if account_transaction is not None:
#                     try:
#                         #this Section is List Addded Charted Of account Updated
#                         account_list=MasterTransaction.objects.get(from_acc_name=account_transaction,L1detail_id=invoice_id)
#                         account_list.credit=invoice_data[transaction[1]]
#                         account_list.debit=invoice_data[transaction[1]]
#                         account_list.save()
#
#
#                     except MasterTransaction.DoesNotExist:
#                         #List Are Addded New Chart of Account this Code Will be ecxecuted
#                         #Menas New transaction Are Created in Master Transaction Section
#
#                         TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#                         account_receivable = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#                         invomast = MasterTransaction.objects.create(
#                             L1detail_id=invoice_id.invoice_id,
#                             L1detailstbl_name='Invoice',
#                             main_module='Sales',
#                             module='Invoice',
#                             sub_module='Invoice',
#                             transc_deatils='Invoice',
#                             banking_module_type='Invoice',
#                             journal_module_type='Invoice',
#                             trans_date=invoice_data["invoice_date"],
#                             trans_status='Manually Added',
#                             debit=invoice_data[transaction[1]],
#                             to_account=account_receivable.coa_id,
#                             to_acc_type=account_receivable.account_type,
#                             to_acc_head=account_receivable.account_head,
#                             to_acc_subhead=account_receivable.account_subhead,
#                             to_acc_name=account_receivable.account_name,
#                             credit=invoice_data[transaction[1]],
#                             from_account=TO_COA.coa_id,
#                             from_acc_type=TO_COA.account_type,
#                             from_acc_head=TO_COA.account_head,
#                             from_acc_subhead=TO_COA.account_subhead,
#                             from_acc_name=TO_COA.account_name,
#                             company_id=comp_id,
#                             customer_id=cust_id)
#                         invomast.save()
#
#
#
#             #  This Sectio Is Discount
#             # Diffrance in Tax Section And Disscount Section Is Tax Side From Account Is Discount Section To Side
#             #and Discount From Side Account is Tax Side is To side
#             #Change The Credit and Debit side
#
#         print('YYYYYYY code excuted')
#         print(invoice_data['discount'])
#         try:
#             #This Section is Disscount will Be find to this code will Be Excuted
#             item_discount_list=MasterTransaction.objects.get(to_acc_name='Discount',L1detail_id=invoice_id)
#
#             item_discount_list.credit=invoice_data['discount']
#             item_discount_list.debit=invoice_data['discount']
#             item_discount_list.save()
#
#
#         # This Section List are addded the Disscount Create mastertransaction new entry
#         except MasterTransaction.DoesNotExist:
#             if float(invoice_data['discount'])>0:
#                 acc_to_list.append('Discount')
#                 print('ohhhhh Discount Code excuted')
#                 TO_COA = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#                 account_receivable = COA.objects.get(company_id=comp_id, account_name="Discount")
#                 invomast = MasterTransaction.objects.create(
#                     L1detail_id=invoice_id.invoice_id,
#                     L1detailstbl_name='Invoice',
#                     main_module='Sales',
#                     module='Invoice',
#                     sub_module='Invoice',
#                     transc_deatils='Invoice',
#                     banking_module_type='Invoice',
#                     journal_module_type='Invoice',
#                     trans_date=invoice_data["invoice_date"],
#                     trans_status='Manually Added',
#                     debit=invoice_data['discount'],
#                     to_account=account_receivable.coa_id,
#                     to_acc_type=account_receivable.account_type,
#                     to_acc_head=account_receivable.account_head,
#                     to_acc_subhead=account_receivable.account_subhead,
#                     to_acc_name=account_receivable.account_name,
#                     credit=invoice_data['discount'],
#                     from_account=TO_COA.coa_id,
#                     from_acc_type=TO_COA.account_type,
#                     from_acc_head=TO_COA.account_head,
#                     from_acc_subhead=TO_COA.account_subhead,
#                     from_acc_name=TO_COA.account_name,
#                     company_id=comp_id,
#                     customer_id=cust_id)
#                 invomast.save()
#
#
#
#
#        #This Section is Item Transaction The Item transaction Can't Created Is only updated
#        #this only Chnage the Credit and debit Side values
#        #Other can;t Change
#
#
#
#
#         #This Section is Item chart of account and amount group by section
#         coa_list = []
#         coa_amount_dict = {}
#         for invoice_item in invoice_data['invoice_items']:
#
#             if coa_amount_dict.get(invoice_item['coa_id']) is None:
#                 coa_amount_dict[invoice_item['coa_id']
#                                 ] = invoice_item['amount']
#             else:
#                 coa_amount_dict[invoice_item['coa_id']
#                                 ] = coa_amount_dict[invoice_item['coa_id']] + invoice_item['amount']
#
#         print('coa_amount_dict', coa_amount_dict)
#         item_transaction_list = []
#         for coa_id, amount in coa_amount_dict.items():
#             print('MMMM',coa_id)
#             print('@@',invoice_id.invoice_id)
#             coa_mast=MasterTransaction.objects.filter(from_account=coa_id,L1detail_id=invoice_id.invoice_id)
#             print('WWWWWW',coa_mast)
#             for coa in coa_mast:
#
#                 coa_acc=coa.from_acc_name
#                 item_transaction_list.append(coa_acc)
#                 acc_from_list.append(coa_acc)
#
#         #this Section Is Mastertransction item related
#         # item_transaction_list = [coa_acc]
#
#
#         for item_transaction in item_transaction_list:
#
#             item_account_list=MasterTransaction.objects.get(from_acc_name=item_transaction,L1detail_id=invoice_id.invoice_id)
#             item_account_list.credit=amount
#             item_account_list.debit=amount
#             item_account_list.save()
#
#
#
#         trans_stock_list= Stock.objects.filter(ref_id=invoice_id).exclude(item_name__in=stock_item_list)
#         for trans_stock in trans_stock_list:
#             mast_stock=trans_stock.st_id
#             transaction_stock= MasterTransaction.objects.filter(L1detail_id=invoice_id,L2detail_id=str(mast_stock)).delete()
#             print(transaction_stock)
#         del_stock= Stock.objects.filter(ref_id=invoice_id).exclude(item_name__in=stock_item_list).delete()
#
#
#
#
#       #this Section Is the Delete the Trnsaction Not Fined is List Mens Remove the Transaction
#         #master_stock variable is the remaning of stock item in master transaction
#         master_stock_list=[]
#         master_stock= MasterTransaction.objects.filter(L1detail_id=invoice_id,L2detailstbl_name='Stock')
#         print('account From List')
#         for stock_trans_mast in master_stock:
#             master_stock_list.append(stock_trans_mast.from_acc_name)
#         print('@@@@@@@@@@@@@@@@@@@@',acc_to_list)
#         to_and_from=acc_from_list+acc_to_list
#         Both_List=to_and_from+master_stock_list
#
#         topics = MasterTransaction.objects.filter(L1detail_id=invoice_id).exclude(from_acc_name__in=Both_List).exclude(to_acc_name__in=Both_List).delete()
#         print('Both List Is here',Both_List)
#         invoice_item_list= InvoiceItem.objects.filter(invoice_id=invoice_id.invoice_id).exclude(item_name__in=stock_item_list).delete()
#         serializer = InvoiceSerializer(invoice_id)
#         return Response(serializer.data)
#
#
# @api_view(['GET'])
# def getinvoiceitembyinvoiceid(request, invoice_id):
#     object = InvoiceItem.objects.filter(invoice_id=invoice_id)
#     serializer = reports2AInvoiceItemSerializer(object, many=True)
#     return Response(serializer.data)
#
#
#
#
#
# class CreditNoteUpdate3ViewSet(viewsets.ModelViewSet):
#     queryset = CreditNote.objects.all()
#     serializer_class = CreditNoteSerializer
#     def update(self, request, pk, *args, **kwargs):
#             #dxfxfddfc
#         creditnote_data=request.data
#         creditnote = CreditNote.objects.get(cn_id=pk)
#
#         comp_id = Company.objects.get(company_id=creditnote_data["company_id"])
#         cust_id = SalesCustomer.objects.get(
#             customer_id=creditnote_data["customer_id"])
#
#         #account receivable varibale are declaret the chart of account of to side from item and taxation Section
#         #and Discount time this chartof Account is From Side
#         account_receivable = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#         print('DATA IS Here',creditnote_data['credit_note_items'])
#         # Invoice Item Looping
#         for cn_item_data in creditnote_data['credit_note_items']:
#            # Item are find Out Section
#
#             try:
#                 try:
#                     cn_item = CreditItem.objects.get(item_id=cn_item_data['item_id'],cn_id=creditnote.cn_id)
#
#                 except KeyError:
#                     cn_item=None
#
#
#
#             except CreditItem.DoesNotExist:
#                 cn_item=None
#
#             # Invoice Item Are Find the update this Code Section
#             if cn_item is not None:
#                 item_serializer=CreditNoteItemSerializer(cn_item,data=cn_item_data)
#                 if item_serializer.is_valid():
#                     item_serializer.save()
#
#             else:
#                 try:
#                     # Get The Chart Of Account and item Id Of the Item Related
#                     coa=COA.objects.get(coa_id=cn_item_data["coa_id"])
#                     item=Item.objects.get(item_id=cn_item_data["item_id"])
#                 except KeyError:
#                     coa=None
#                     item=None
#
#                 try:
#                     #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
#                     new_credit_note_items = CreditItem.objects.create(cn_id=creditnote,
#                                                               item_id=Item.objects.get(
#                                                                   item_id=cn_item_data["item_id"]),
#                                                               coa_id=COA.objects.get(
#                                                                   coa_id=cn_item_data["coa_id"]),
#                                                               item_name=cn_item_data["item_name"],
#                                                               rate=cn_item_data["rate"],
#                                                               quantity=cn_item_data["quantity"],
#                                                               tax_rate=cn_item_data["tax_rate"],
#                                                               tax_name=cn_item_data["tax_name"],
#                                                               tax_type=cn_item_data["tax_type"],
#                                                               taxamount=cn_item_data["taxamount"],
#                                                               cgst_amount=cn_item_data['cgst_amount'],
#                                                               sgst_amount=cn_item_data['sgst_amount'],
#                                                               igst_amount=cn_item_data['igst_amount'],
#                                                               amount=cn_item_data["amount"])
#
#                     new_credit_note_items.save()
#
#                 except KeyError:
#                     pass
#
#
#
#
#         #this Section Is Invoice Data Update Serializer Through
#         print('OHHHH',creditnote_data['discount'])
#         serializer = CreditNoteSerializer(creditnote, data=creditnote_data)
#
#         if serializer.is_valid():
#             creditnote_id=serializer.save()
#
#             # return Response({"data":serializer.data})
#         else:
#
#              return Response(serializer.errors, status=400)
#
#
#         stock_item_list=[]
#         stock_transactiom_item_list=[]
#         account_payable = COA.objects.get(company_id=comp_id, account_subhead='Account Payables')
#
#         for cn_item_stock in creditnote_data['credit_note_items']:
#             print('For Loop Is Excuted')
#             stock_item_list.append(cn_item_stock['item_id'])
#             try:
#
#                 stock_item=Stock.objects.get(item_id=cn_item_stock['item_id'],ref_id=creditnote_id.cn_id)
#
#                 print('okk')
#                 item_value=Item.objects.get(item_id=cn_item_stock["item_id"])
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#
#                 print("updating stock", cn_item_stock['quantity'], cn_item_stock['item_id'])
#                 stock_item.stock_in=float(cn_item_stock['quantity'])
#                 stock_item.rate=float(current_assets_last_stock.rate)
#                 stock_item.amount=float(current_assets_last_stock.rate)*float(cn_item_stock['quantity'])
#                 stock_item.quantity=float(cn_item_stock['quantity'])
#                 stock_item.save()
#                 stock_transactiom_item_list.append(stock_item)
#                 stock_mast=MasterTransaction.objects.get(L2detail_id=stock_item.st_id,L1detail_id=creditnote_id.cn_id)
#                 print('@',stock_item.rate)
#                 print('$',stock_item.quantity)
#                 stock_mast.debit=int(stock_item.rate)*stock_item.quantity,
#                 stock_mast.credit=int(stock_item.rate)*stock_item.quantity,
#                 print('Updateing Sucessfully')
#             except Stock.DoesNotExist:
#
#                 item_value=Item.objects.get(item_id=cn_item_stock["item_id"])
#                 items_inventory=creditnote_data.get('credit_note_items')
#                 track_inventory=items_inventory[0].get('selected_item_name',{}).get('track_inventory')
#                 print('inventory',track_inventory)
#
#                 item_value=Item.objects.get(item_id=cn_item_stock["item_id"])
#                 print('Item is herer',item_value)
#
#
#                 if track_inventory==True:
#
#                     current_invoice_rate=Stock.objects.filter(item_id=item_value.item_id,formname='Invoice').latest('created_date')
#                     stock_invoice_rate=current_invoice_rate.rate
#                     try:
#                         current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                         current_stock_amount=current_assets_last_stock.amount
#
#
#                     except Stock.DoesNotExist:
#                         current_stock_amount=0
#
#                         stk_in=Stock.objects.filter(item_id=cn_item_stock["item_id"]).exclude(stock_in=0).order_by('created_date')
#                         stk_out=Stock.objects.filter(item_id=cn_item_stock["item_id"]).exclude(stock_out=0).order_by('created_date')
#                         stock_int_items = stk_in
#
#                     print("Stock Invoice rate@@@@@@",stock_invoice_rate)
#                     stock_items=Stock.objects.create(
#                         item_id=cn_item_stock['item_id'],
#                         item_name=cn_item_stock["item_name"],
#                         stock_in=cn_item_stock["quantity"],
#                         amount=current_stock_amount+(cn_item_stock["quantity"] * cn_item_stock["rate"]),
#                         rate= stock_invoice_rate,
#                         quantity=cn_item_stock["quantity"],
#                         #stock_on_hand=current_stock_on_hand+cn_item_stock["quantity"],
#                         ref_id=creditnote_id.cn_id,
#                         ref_tblname='CreditNote',
#                         module='Sales',
#                         formname='Credit Note',
#                         stage='Add Stages',
#                         date=creditnote_data["cn_date"],
#                         company_id=comp_id)
#
#
#
#
#             #This Section Is Stock Journal Transaction
#             #Stock Charetd Account name is Inventory Assets
#             #item select time has three chart of account must be
#             #Sales Account,Purchase Account ,Inventory Accounts
#
#                     cr_item=creditnote_data.get('credit_note_items')
#                     purchase_account=cr_item[0].get('selected_item_name').get('purchase_account')
#                     inventory_account=cr_item[0].get('selected_item_name').get('inventory_account')
#                     if purchase_account is not None:
#                         FROM_COA = COA.objects.get(company_id=comp_id,coa_id=purchase_account)
#                     else:
#                         print("No Chart of Account Found")
#                     if inventory_account is not None:
#                         TO_COA=COA.objects.get(company_id=comp_id,coa_id=inventory_account)
#                     else:
#                         print("No Chart of Account Found")
#
#                     #TO_COA = COA.objects.get(company_id=comp_id,account_name='Inventory Assets')
#                     print('item rate',stock_items.rate)
#                     print('item quantity',stock_items.quantity)
#                     stkmast = MasterTransaction.objects.create(
#                         L1detail_id=creditnote_id.cn_id,
#                         L1detailstbl_name='CreditNote',
#                         L2detail_id=stock_items.st_id,
#                         L2detailstbl_name='Stock',
#                         main_module='Sales',
#                         module='CreditNote',
#                         sub_module='CreditNote',
#                         transc_deatils='CreditNote',
#                         banking_module_type='CreditNote',
#                         journal_module_type='CreditNote',
#                         trans_date=creditnote_data["cn_date"],
#                         trans_status='Manually Added',
#                         debit=stock_items.rate*stock_items.quantity,
#                         to_account=TO_COA.coa_id,
#                         to_acc_type=TO_COA.account_type,
#                         to_acc_head=TO_COA.account_head,
#                         to_acc_subhead=TO_COA.account_subhead,
#                         to_acc_name=TO_COA.account_name,
#                         credit=stock_items.rate*stock_items.quantity,
#                         from_account=FROM_COA.coa_id,
#                         from_acc_type=FROM_COA.account_type,
#                         from_acc_head=FROM_COA.account_head,
#                         from_acc_subhead=FROM_COA.account_subhead,
#                         from_acc_name=FROM_COA.account_name,
#                         company_id=comp_id,
#                         customer_id=cust_id)
#                     stkmast.save()
#
#         print('Stock Item List is Here',stock_item_list)
#         Zero_tax=creditnote_data.get('credit_note_item')
#         GST_TAX=None
#         GST_TAX=Zero_tax
#         if GST_TAX is not None:
#             if GST_TAX==Zero_tax.get('selected_tax_name') is not None:
#                 GST_TAX=Zero_tax.get('selected_tax_name',{}).get('tax_name')
#             else:
#                 pass
#
#
#
#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX
#
#         else:
#             Both_Tax=None
#
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None
#
#
#
#         transaction_list = []
#         if float(creditnote_data['tcs_amount'])>0:
#             transaction_list.append(["TCS Payable","tcs_amount"])
#         if float(creditnote_data['shipping_charges'])>0:
#             transaction_list.append(["Shipping Charges","shipping_charges"])
#         if float(creditnote_data['cgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Output CGST", "cgst_total"],)
#         if float(creditnote_data['sgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Output SGST", "sgst_total"])
#         if float(creditnote_data['igst_total']) >0 or IGST_0:
#             transaction_list.append(["Output IGST", "igst_total"],)
#         acc_from_list=[]
#         acc_to_list=[]
#         #Looping the Added Transaction List Chrat of Account
#         # and this Credit and debit value
#         #this list type is list of list eg: [[Chart of account ,invoicedata[igst_total]]]
#         for transaction in transaction_list:
#
#             for account_transaction in [transaction[0]]:
#                 acc_from_list.append(account_transaction)
#                 if account_transaction is not None:
#                     try:
#                         #this Section is List Addded Charted Of account Updated
#                         account_list=MasterTransaction.objects.get(from_acc_name=account_transaction,L1detail_id=creditnote_id.cn_id)
#                         account_list.credit=creditnote_data[transaction[1]]
#                         account_list.debit=creditnote_data[transaction[1]]
#                         account_list.save()
#
#
#                     except MasterTransaction.DoesNotExist:
#                         #List Are Addded New Chart of Account this Code Will be ecxecuted
#                         #Menas New transaction Are Created in Master Transaction Section
#
#
#                         account_receivable = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#                         TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#                         cnmast = MasterTransaction.objects.create(
#                             L1detail_id=creditnote_id.cn_id,
#                             L1detailstbl_name='Credit Note',
#                             main_module='Sales',
#                             module='Sales',
#                             sub_module='Credit Note',
#                             transc_deatils='Credit Note',
#                             banking_module_type='Credit Note',
#                             journal_module_type='Credit Note',
#                             trans_date=creditnote_data["cn_date"],
#                             trans_status='Manually added',
#                             debit=creditnote_data[transaction[1]],
#                             to_account=TO_COA.coa_id,
#                             to_acc_type=TO_COA.account_type,
#                             to_acc_head=TO_COA.account_head,
#                             to_acc_subhead=TO_COA.account_subhead,
#                             to_acc_name=TO_COA.account_name,
#                             credit=creditnote_data[transaction[1]],
#                             from_account=account_receivable.coa_id,
#                             from_acc_type=account_receivable.account_type,
#                             from_acc_head=account_receivable.account_head,
#                             from_acc_subhead=account_receivable.account_subhead,
#                             from_acc_name=account_receivable.account_name,
#                             company_id=comp_id,
#                             customer_id=cust_id)
#             cnmast.save()
#
#         try:
#             #This Section is Disscount will Be find to this code will Be Excuted
#             item_discount_list=MasterTransaction.objects.get(to_acc_name='Discount',L1detail_id=creditnote_id.cn_id)
#
#             item_discount_list.credit=creditnote_data['discount']
#             item_discount_list.debit=creditnote_data['discount']
#             item_discount_list.save()
#
#         # This Section List are addded the Disscount Create mastertransaction new entry
#         except MasterTransaction.DoesNotExist:
#             print('QQQQ Discount',creditnote_data['discount'])
#             if float(creditnote_data['discount'])>0:
#                 acc_to_list.append('Discount')
#                 TO_COA = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
#                 account_receivable = COA.objects.get(company_id=comp_id, account_name="Discount")
#                 cnmast = MasterTransaction.objects.create(
#                 L1detail_id=creditnote_id.cn_id,
#                 L1detailstbl_name='Credit Note',
#                 main_module='Sales',
#                 module='Sales',
#                 sub_module='Credit Note',
#                 transc_deatils='Credit Note',
#                 banking_module_type='Credit Note',
#                 journal_module_type='Credit Note',
#                 trans_date=creditnote_data["cn_date"],
#                 trans_status='Manually added',
#                 debit=creditnote_data['discount'],
#                 to_account=TO_COA.coa_id,
#                 to_acc_type=TO_COA.account_type,
#                 to_acc_head=TO_COA.account_head,
#                 to_acc_subhead=TO_COA.account_subhead,
#                 to_acc_name=TO_COA.account_name,
#                 credit=creditnote_data['discount'],
#                 from_account=account_receivable.coa_id,
#                 from_acc_type=account_receivable.account_type,
#                 from_acc_head=account_receivable.account_head,
#                 from_acc_subhead=account_receivable.account_subhead,
#                 from_acc_name=account_receivable.account_name,
#                 company_id=comp_id,
#                 customer_id=cust_id)
#                 cnmast.save()
#
#
#
#
#         #This Section is Item chart of account and amount group by section
#         coa_amount_dict = {}
#         for creditnote_items in creditnote_data['credit_note_items']:
#             if coa_amount_dict.get(creditnote_items['coa_id']) is None:
#                 coa_amount_dict[creditnote_items['coa_id']
#                                 ] = creditnote_items['amount']
#             else:
#                 coa_amount_dict[creditnote_items['coa_id']
#                                 ] = coa_amount_dict[creditnote_items['coa_id']] + creditnote_items['amount']
#
#             for coa_id, amount in coa_amount_dict.items():
#                 print('status ok',coa_id)
#                 coa_mast=MasterTransaction.objects.filter(to_account=coa_id,L1detail_id=creditnote_id.cn_id)
#                 print('Status All Ok')
#                 for coa in coa_mast:
#
#                     coa_acc=coa.to_acc_name
#
#
#         #this Section Is Mastertransction item related
#         item_transaction_list = [coa_acc]
#         acc_from_list.append(coa_acc)
#
#         for item_transaction in item_transaction_list:
#
#             item_account_list=MasterTransaction.objects.get(to_acc_name=item_transaction,L1detail_id=creditnote_id.cn_id)
#             item_account_list.credit=amount
#             item_account_list.debit=amount
#             item_account_list.save()
#
#
#         print('To_Acc_list is Here',acc_to_list)
#         print('From Acc_list is Here',acc_from_list)
#         print('Stock Transaction list',stock_transactiom_item_list)
#         trans_stock_list= Stock.objects.filter(ref_id=creditnote_id.cn_id).exclude(item_id__in=stock_item_list)
#         for trans_stock in trans_stock_list:
#             mast_stock=trans_stock.st_id
#             transaction_stock= MasterTransaction.objects.filter(L1detail_id=creditnote_id.cn_id,L2detail_id=str(mast_stock)).delete()
#             print('KKKK++++',transaction_stock)
#
#         del_stock= Stock.objects.filter(ref_id=creditnote_id.cn_id).exclude(item_id__in=stock_item_list).delete()
#
#         master_stock_list=[]
#         master_stock= MasterTransaction.objects.filter(L1detail_id=creditnote_id.cn_id,L2detailstbl_name='Stock')
#         for stock_trans_mast in master_stock:
#             master_stock_list.append(stock_trans_mast.from_acc_name)
#         print('@@@@@@@@@@@@@@@@@@@@',acc_to_list)
#         to_and_from=acc_from_list+acc_to_list
#         Both_List=to_and_from+master_stock_list
#
#         topics = MasterTransaction.objects.filter(L1detail_id=creditnote_id.cn_id).exclude(from_acc_name__in=Both_List).exclude(to_acc_name__in=Both_List).delete()
#         print('Both List Is here',Both_List)
#         cn_item_list= CreditItem.objects.filter(cn_id=creditnote_id.cn_id).exclude(item_id__in=stock_item_list).delete()
#         print('cn_item_list is here',cn_item_list)
#
#
#
#         serializer = CreditNoteonlyserializer(creditnote_id)
#         return Response(serializer.data)
#
