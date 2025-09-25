import json
import os
from pathlib import Path

import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.vendor_advanced_model import VendorAdvanced
from banking.models.banking_model import Banking
from banking.serializers.vendor_advanced_serializers import VendorAdvancedSerializer,UpdateVendorAdvanceSerializer
from purchase.models.Vendor_model import  Vendor
from audit.models import Audit
from django.db import transaction


######################################################################
# Vendor Advance Views

class Vendor_AdvancedModelViewSets(viewsets.ModelViewSet):
    queryset=VendorAdvanced.objects.all()
    serializer_class=VendorAdvancedSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        Vendor_AdvancedModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            Vendor_AdvancedModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            Vendor_AdvancedModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            Vendor_AdvancedModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        vendor_advanced_data = request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=vendor_advanced_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)

        user = request.user
        if(Vendor_AdvancedModelViewSets.ValidateDefaults(vendor_advanced_data)==False):
            print(" Ooops!!! Error Occured ",Vendor_AdvancedModelViewSets.logger)
        
        print(vendor_advanced_data)

        branch_id=vendor_advanced_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=vendor_advanced_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
        
        vendor_id=vendor_advanced_data["vendor_id"]
        if vendor_id is not None:
            vendor_id=Vendor.objects.get(vendor_id=vendor_id)
            
        company_year_id=vendor_advanced_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        	
            # Create Vendor Advanced
            
        is_bank_transaction="True"
        print("Bank Transaction", is_bank_transaction)
        if is_bank_transaction == 'True':
            
         # Create Vendor Advanced    
            va_id=VendorAdvanced.objects.create(
            is_vendor_advance_generated=vendor_advanced_data["is_vendor_advance_generated"],
            company_id=company_id,
            bank_id=From_Bank,      
            branch_id=branch_id,
            vendor_id=vendor_id,
            is_bank_transaction=True,
            status=vendor_advanced_data["status"],
        #  deposit_to=vendor_advanced_data["deposit_to"],            
            gst_treatment=vendor_advanced_data["gst_treatment"],
            vendor_gstin=vendor_advanced_data["vendor_gstin"],
            source_place=vendor_advanced_data["source_place"],
            destination_place=vendor_advanced_data["destination_place"],
            amount=vendor_advanced_data["amount"],
            payment_serial=vendor_advanced_data["payment_serial"],
            balance_amount=vendor_advanced_data['amount'],
            vendor_advance_ref_no=vendor_advanced_data["vendor_advance_ref_no"],
            vendor_advance_date=vendor_advanced_data["vendor_advance_date"],
            paid_via=vendor_advanced_data["paid_via"],
            description=vendor_advanced_data["description"],
            description_supply=vendor_advanced_data["description_supply"],
            tax_rate=vendor_advanced_data["tax_rate"],
            tax_name=vendor_advanced_data["tax_name"],  
            tax_type=vendor_advanced_data["tax_type"],
            tax_amount=vendor_advanced_data["tax_amount"], 
            reverse_charge=vendor_advanced_data["reverse_charge"])
            va_id.save()
            print("vendor_advanced_created",va_id,type(va_id))


            Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=vendor_advanced_data["vendor_advance_date"],
            module="Banking",
            sub_module='VendorAdvanced',
            data=vendor_advanced_data
        )

            TO_COA= COA.objects.get(company_id=company_id,
                                    account_subhead='Account Payables',isdefault=True)
            print('""""""""""""',TO_COA)  
            vamast=MasterTransaction.objects.create(
            L1detail_id=va_id.va_id,
            L1detailstbl_name='VendorAdvanced',
            L2detail_id=From_Bank.bank_id,
            L2detailstbl_name='BANK',
            main_module='Banking',
            module='MonenyOut',
            sub_module='VendorAdvanced',
            transc_deatils='Vendor Advanced',
            banking_module_type=vendor_advanced_data["transaction_module"],
            journal_module_type=vendor_advanced_data["transaction_module"],
            trans_date=vendor_advanced_data["vendor_advance_date"],
            trans_status=vendor_advanced_data["status"],
            debit=vendor_advanced_data["amount"],
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=vendor_advanced_data['amount'],
            from_account=From_Bank.coa_id.coa_id,        
            from_acc_type=From_Bank.coa_id.account_type,
            from_acc_head=From_Bank.coa_id.account_head,
            from_acc_subhead=From_Bank.coa_id.account_subhead,
            from_acc_name=From_Bank.coa_id.account_name,
            company_id=company_id,
            vendor_id=vendor_id,
            branch_id=branch_id)
            vamast.save() 
        
    #endregion
    #End Master Transaction Section

            serializer =VendorAdvancedSerializer(va_id)         
            return Response(serializer.data)
    
 #Vendoe Advanced Refund New from
 
class Vendor_AdvancedRefund_newViewSets(viewsets.ModelViewSet):
    queryset=VendorAdvanced.objects.all()
    serializer_class=VendorAdvancedSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        Vendor_AdvancedModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            Vendor_AdvancedModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            Vendor_AdvancedModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            Vendor_AdvancedModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue

    def create(self, request, *args, **kwargs):
        vendor_advanced_data = request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=vendor_advanced_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)


        if(Vendor_AdvancedModelViewSets.ValidateDefaults(vendor_advanced_data)==False):
            print(" Ooops!!! Error Occured ",Vendor_AdvancedModelViewSets.logger)
        
        print(vendor_advanced_data)

        branch_id=vendor_advanced_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=vendor_advanced_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
        
        vendor_id=vendor_advanced_data["vendor_id"]
        if vendor_id is not None:
            vendor_id=Vendor.objects.get(vendor_id=vendor_id)
            
        company_year_id=vendor_advanced_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
       
			
		# Create Vendor Advanced
		
        va_id=VendorAdvanced.objects.create(
        is_vendor_advance_generated=vendor_advanced_data["is_vendor_advance_generated"],
        company_id=company_id,
        bank_id=From_Bank,      
        branch_id=branch_id,
        vendor_id=vendor_id,
        status=vendor_advanced_data["status"],
      #  deposit_to=vendor_advanced_data["deposit_to"],            
        gst_treatment=vendor_advanced_data["gst_treatment"],
        vendor_gstin=vendor_advanced_data["vendor_gstin"],
        source_place=vendor_advanced_data["source_place"],
        destination_place=vendor_advanced_data["destination_place"],
        amount=vendor_advanced_data["amount"],
        payment_serial=vendor_advanced_data["payment_serial"],
        balance_amount=vendor_advanced_data['amount'],
        vendor_advance_ref_no=vendor_advanced_data["vendor_advance_ref_no"],
        vendor_advance_date=vendor_advanced_data["vendor_advance_date"],
        paid_via=vendor_advanced_data["paid_via"],
        description=vendor_advanced_data["description"],
        description_supply=vendor_advanced_data["description_supply"],
        tax_rate=vendor_advanced_data["tax_rate"],
        tax_name=vendor_advanced_data["tax_name"],  
        tax_type=vendor_advanced_data["tax_type"],
        tax_amount=vendor_advanced_data["tax_amount"], 
        reverse_charge=vendor_advanced_data["reverse_charge"])
        va_id.save()
        print("vendor_advanced_created",va_id,type(va_id))
        
#region Master Transaction Section

        TO_COA= COA.objects.get(company_id=company_id,account_name="Account Payables",isdefault=True)
        print('""""""""""""',TO_COA)  
        vamast=MasterTransaction.objects.create(
        L1detail_id=va_id.va_id,
        L1detailstbl_name='VendorAdvanced',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyOut',
        sub_module='VendorAdvanced',
        transc_deatils='Vendor Advanced',
        banking_module_type=vendor_advanced_data["transaction_module"],
        journal_module_type=vendor_advanced_data["transaction_module"],
        trans_date=vendor_advanced_data["vendor_advance_date"],
        trans_status=vendor_advanced_data["status"],
        debit=vendor_advanced_data["amount"],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        credit=vendor_advanced_data['amount'],
        from_account=From_Bank.coa_id.coa_id,        
        from_acc_type=From_Bank.coa_id.account_type,
        from_acc_head=From_Bank.coa_id.account_head,
        from_acc_subhead=From_Bank.coa_id.account_subhead,
        company_id=company_id,
        vendor_id=vendor_id,
        branch_id=branch_id)
        vamast.save() 
       
#endregion
#End Master Transaction Section

        serializer =VendorAdvancedSerializer(va_id)         
        return Response(serializer.data)
        
           
           
#Updating the vendor Advance  Section 
# Check the vedor advanced id in vendor advance table if exist the updated 
#other wise Does Not Exist
class UpdateVendorAdvanceViewset(viewsets.ModelViewSet):
    queryset = VendorAdvanced.objects.all()
    serializer_class=UpdateVendorAdvanceSerializer



    def update(self, request, pk, *args, **kwargs):
        va_data = request.data
        print("THIS API IS HEATING")
        va = VendorAdvanced.objects.get(va_id=pk)
        print("VA ID",va)
        vendor_id=Vendor.objects.get(vendor_id=va_data["vendor_id"])
        company_id=Company.objects.get(company_id=va_data['company_id'])


        serializer = UpdateVendorAdvanceSerializer(va, data=va_data)
      
        if serializer.is_valid():
            
            serializer.save()
            msg="Details Updated Successfully"
            
        else:
                return Response(serializer.errors, status=400)    

        account_list=MasterTransaction.objects.get(L1detail_id=va.va_id)
        print("account_list",account_list)
        account_list.credit=float(va_data['amount'])
        account_list.debit=float(va_data['amount'])
        account_list.save()

        return Response(serializer.data)

