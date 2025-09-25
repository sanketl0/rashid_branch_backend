import json
from audit.models import Audit
import uuid
from rest_framework.response import Response
from rest_framework import viewsets

from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.banking_model import Banking
from salescustomer.models.Salescustomer_model import SalesCustomer
from banking.models.customer_advance_model import CustomerAdvance
from banking.serializers.customer_advance_serializers import CustomerAdvancedSerializer,UpdateCustomerAdvanceSerializer
from rest_framework.decorators import api_view, permission_classes

from django.db import transaction
from banking.models.vendor_advanced_model import VendorAdvanced
from banking.serializers.vendor_advanced_serializers import VendorPaymentGETSerializer


class CustomerAdvanceViewsets(viewsets.ModelViewSet):
    queryset =CustomerAdvance.objects.all()
    serializer_class =CustomerAdvancedSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        CustomerAdvanceViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            CustomerAdvanceViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            CustomerAdvanceViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            CustomerAdvanceViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue



    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ca_data_converte= request.data['data']
        user = request.user
        print("#################################################")
        print(ca_data_converte)
        print("Customer Format is ",type(ca_data_converte))
        print("#################################################")
        ca_data = json.loads(ca_data_converte)
        print("Converted Format is",type(ca_data))
        ca_file_data=request.FILES.get('attach_file')
        print("ca_data",type(ca_file_data))

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=ca_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)


        if(CustomerAdvanceViewsets.ValidateDefaults(ca_data)==False):
            print(" Ooops!!! Error Occured ",CustomerAdvanceViewsets.logger)
        
        print(ca_data)


        #Branch and company null value

        branch_id=ca_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=ca_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
            
        company_year_id=ca_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        customer_id=ca_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
        is_bank_transaction="True"
        print("Bank Transaction", is_bank_transaction)
        if is_bank_transaction=="True": 

        #Creating Customer Advance
            caed_id=CustomerAdvance.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            bank_id=From_Bank,
            coa_id=COA.objects.get(coa_id=ca_data['coa_id']),
            customer_id=customer_id,
            attach_file=ca_file_data,
            is_bank_transaction=True,
            gst_treatment=ca_data["gst_treatment"],
            is_customer_advance_generated=ca_data['is_customer_advance_generated'],
            gstin_no=ca_data["gstin_no"],
            supply_place=ca_data["supply_place"],
            amount_received=ca_data["amount_received"],
            balance_amount=ca_data["balance_amount"],
            customer_advance_date=ca_data["customer_advance_date"],
            customer_advance_ref_no=ca_data["customer_advance_ref_no"],
            received_via=ca_data["received_via"],
            status=ca_data["status"],
            description=ca_data["description"],
            description_supply=ca_data["description_supply"],
            bank_charges=ca_data["bank_charges"],
            payment_serial=ca_data["payment_serial"],
            tax_rate=ca_data["tax_rate"],
            tax_name=ca_data["tax_name"],
            tax_type=ca_data["tax_type"],
            tax_amount=ca_data["tax_amount"])
            caed_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=ca_data["customer_advance_date"],
            module="Banking",
            sub_module='Customer Advanced',
            data=ca_data
        )

#region MasterTransaction Section
        TO_COA= COA.objects.get(company_id=company_id,account_subhead="Account Receivables",isdefault=True)
        print('""""""""""""',TO_COA)  
        camast=MasterTransaction.objects.create(
        L1detail_id=caed_id.ca_id,
        L1detailstbl_name='Customer Advance',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyIN',
        sub_module='Customer Advanced',
        transc_deatils='Customer Advanced',
        banking_module_type=ca_data["transaction_module"],
        journal_module_type=ca_data["transaction_module"],
        trans_date=ca_data["customer_advance_date"],
        trans_status=ca_data["status"],
        debit=ca_data["amount_received"],
        to_account=From_Bank.coa_id.coa_id,
        to_acc_type=From_Bank.coa_id.account_type,
        to_acc_head=From_Bank.coa_id.account_head,
        to_acc_subhead=From_Bank.coa_id.account_subhead,
        to_acc_name=From_Bank.coa_id.account_name,
        credit=ca_data['amount_received'],
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_head,
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        customer_id=customer_id,
        branch_id=branch_id)
        camast.save()      
        
#endregion End Master Transaction Section
        serializer = CustomerAdvancedSerializer(caed_id)
        return Response(serializer.data)



#Customer Advanced Updating the Section 


@api_view(['GET'])
def getcustomeradvancedbankbycoaid(request,pk):
    ca = CustomerAdvance.objects.get(ca_id=pk)
    serializer = CustomerAdvancedSerializer(ca)
    return Response(serializer.data,status=200)


@api_view(['GET'])
def getvendoradvancedbankbycoaid(request,pk):
    va = VendorAdvanced.objects.get(va_id=pk)
    serializer = VendorPaymentGETSerializer(va)
    return Response(serializer.data,status=200)
