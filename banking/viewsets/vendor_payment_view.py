
import json
from operator import imod
import os
from pathlib import Path

import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.vendor_payment_model import VendorPayment
from banking.serializers.vendor_payment_serializers import VendorPaymentSerializer
from banking.models.banking_model import Banking
from purchase.models.Paymentmade_model import PaymentMade
from purchase.models.Bill_model import Bill
from purchase.models.Vendor_model import Vendor
from audit.models import Audit

from django.db import transaction
class VendorPaymentModelViewSets(viewsets.ModelViewSet):
    queryset=VendorPayment.objects.all()
    serializer_class=VendorPaymentSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        VendorPaymentModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            VendorPaymentModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            VendorPaymentModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            VendorPaymentModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue  
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        vp_data = request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=vp_data["paid_through"]
        print("bank", bank)
        From_Bank=Banking.objects.get(coa_id=bank)

        if(VendorPaymentModelViewSets.ValidateDefaults(vp_data)==False):
            print(" Ooops!!! Error Occured ",VendorPaymentModelViewSets.logger)
            
        print(vp_data)
            
            #What if this ID is null , 
        	
        branch_id=vp_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=vp_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
        
        
        company_year_id=vp_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        
        bill_id=Bill.objects.get(bill_id=vp_data["bill_id"])
        user = request.user
        is_bank_transaction="True"

        if is_bank_transaction=="True":                        

            vped_id=PaymentMade.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            bank_id=From_Bank,
            vendor_id=Vendor.objects.get(vendor_id=vp_data["vendor_id"]),
            paid_through=vp_data["paid_through"],
            status=vp_data["status"],
            is_bank_transaction=True,
            payment_ref_no=vp_data["payment_ref_no"],
            payment_mode=vp_data["payment_mode"],
            amount_payable=vp_data["amount_payable"],
            payment_date=vp_data["payment_date"],
            bill_id=bill_id,
            bill_date=vp_data["bill_date"],
            bill_serial=vp_data["bill_serial"],
            amount_due=vp_data["amount_due"],
            bill_amount=vp_data["bill_amount"],
            balance_amount=vp_data["balance_amount"],
            payment_serial=vp_data["payment_serial"],
            amount_excess=vp_data["amount_excess"],
            note=vp_data["note"],
            form_type="Vendor Payment")
            vped_id.save()
            print("entry for payment made",vp_data,type(vp_data))

            Audit.objects.create(
                company_id=company_id,
                branch_id=branch_id,
                created_by=user,
                audit_created_date=vp_data["payment_date"],
                module="Banking",
                sub_module='VendorPayment',
                data=vp_data
            )
            #2 Financial Transaction Prerequisites 
            ## Credit Transaction 
            ## SHould be added the amount TO_COA_ID 


            FROM_COA =COA.objects.get(coa_id=vp_data["paid_through"])

         

          


            vendor_id=Vendor.objects.get(vendor_id=vp_data["vendor_id"]),        
            TO_COA =COA.objects.get(company_id=company_id,account_subhead='Account Payables',isdefault=True)
            print('""""""""""""',TO_COA)  
            vpmast=MasterTransaction.objects.create(
            L1detail_id=vped_id.pm_id,
            L1detailstbl_name='Payment Made',
            L2detail_id=From_Bank.bank_id,
            L2detailstbl_name='BANK',
            L3detail_id=bill_id.bill_id,
            L3detailstbl_name='Bill',
            main_module='Banking',
            module='MonenyOut',
            sub_module='VendorPayment',
            transc_deatils='Vendor Payment',
            banking_module_type=vp_data["transaction_module"],
            journal_module_type='Payment Made',
            trans_date=vp_data["payment_date"],
            trans_status=vp_data["status"],
            debit=vp_data["amount_payable"],
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=vp_data['amount_payable'],
            from_account=From_Bank.coa_id.coa_id,        
            from_acc_type=From_Bank.coa_id.account_type,
            from_acc_head=From_Bank.coa_id.account_head,
            from_acc_subhead=From_Bank.coa_id.account_subhead,
            from_acc_name=From_Bank.coa_id.account_name,
            company_id=company_id,
            vendor_id=Vendor.objects.get(vendor_id=vp_data["vendor_id"]),
            branch_id=branch_id)
            vpmast.save()
            
            #If payment is full then payment status will change unpaid to paid in Bill
            balance_amount=vp_data["balance_amount"]
            amount_excess=vp_data["amount_excess"]
            #if bill_amount == balance_amount:
            if balance_amount == 0:
                bill_id = Bill.objects.get(bill_id=vp_data["unpaindBill"]["bill_id"])       
                print('bill_id', bill_id)              
                bill_id.payment_status='paid'
                bill_id.save()
                print('bill status updated to ', bill_id.payment_status)

            if amount_excess < 0:
                bill_id = Bill.objects.get(bill_id=vp_data["unpaindBill"]["bill_id"])
                print('bill id of else', bill_id)
                bill_id.amount_due = vp_data["balance_amount"]            
                bill_id.save()       
                print('bill amount due updated to ', bill_id.amount_due)

            else:
                bill_id = Bill.objects.get(bill_id=vp_data["unpaindBill"]["bill_id"])
                print('bill id of else', bill_id)
                bill_id.amount_due = vp_data["balance_amount"]            
                bill_id.save()       
                print('bill amount due updated to ', bill_id.amount_due)
        serializer =VendorPaymentSerializer(vped_id)         
        return Response(serializer.data)
