import json
import os
import pandas as pd
import datetime
from pathlib import Path
from wsgiref.util import FileWrapper

from django.template.loader import get_template
from django.views.generic import View
from django.http import HttpResponse, FileResponse
from purchase.printing.generate_dn import generate_dn_pdf

from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import api_view
from purchase.models.Multiple_bill_model import Multiple_Bill_Details
from purchase.models.Vendor_model import Vendor
from coa.models import COA
from transaction.models import MasterTransaction
from purchase.models.Bill_model import Bill
from item.models.item_model import Item
from item.models.stock_model import Stock
from company.models import Company,Company_Year
from company.serializers import CompanySerializer
from purchase.serializers.Multiple_bill_serializers import Multiple_bill_Serializer
from purchase.models.Paymentmade_model import PaymentMade 
from purchase.serializers.Paymentmade_serializers import PaymentmadeSerializer





class MultipleBillViewSet(viewsets.ModelViewSet):
    queryset = Multiple_Bill_Details.objects.all()
    serializer_class = Multiple_bill_Serializer
   
    # here is the entry for dabit note
    def create(self, request, *args, **kwargs):
        mb_data_converte = request.data#['data']
        print("request data is",mb_data_converte)
      
        # Debitnote Convert Str to Dict Code
        mb_data = mb_data_converte#json.loads(mb_data_converte)
      
        vendor_id = mb_data["vendor_id"]
        if vendor_id is not None:
            vendor_id = Vendor.objects.get(vendor_id=vendor_id)  
            
            
        company_id = mb_data["company_id"]
        if company_id is not None:
            company_id = Company.objects.get(company_id=company_id)
            
        company_year_id=mb_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
    
        bill_id=mb_data.get("bill_id")
        if bill_id is not None:
            bill_id=Bill.objects.get(bill_id=bill_id)

        
        pm_serializer = PaymentmadeSerializer(data=mb_data)
        if pm_serializer.is_valid():
            print(pm_serializer.validated_data)
            company_id=company_id.company_id
            payment_id = pm_serializer.save()
            payment_id.save()
        else:
            return Response(pm_serializer.errors)
        
        #chart of account is get the Account Payables
        account_payable =COA.get_account_paybles(company_id)
        
        for bill in mb_data["multiple_bills"]:
            print("bill in multiple bill",bill)
            multiple_bills = Multiple_Bill_Details.objects.create(
                                                         bill_id=Bill.objects.get(
                                                             bill_id=bill["bill_id"]),
                                                         company_id=Company.objects.get(
                                                             company_id=bill["company_id"]),
                                                         vendor_id=Vendor.objects.get(
                                                             vendor_id=bill["vendor_id"]),
                                                         amount=bill["amount"],
                                                         amount_due=bill["amount_due"],
                                                         pm_id=payment_id)
            
            multiple_bills.save()
            print("multiple_bills", multiple_bills, type(multiple_bills))
        return Response(pm_serializer.data)
        
        

