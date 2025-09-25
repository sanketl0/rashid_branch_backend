import json
import os
from pathlib import Path

import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.banking_model import Banking
from banking.models.refund_master_model import RefundMaster
from banking.serializers.refund_master_serializers import Refund_Serializer
from salescustomer.models import SalesCustomer
from banking.models.customer_advance_model import CustomerAdvance
from audit.models import Audit
#Payment Refund
class PaymentRefundViewsets(viewsets.ModelViewSet):
    queryset =RefundMaster.objects.all()
    serializer_class =Refund_Serializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        PaymentRefundViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
       
        retValue=True
        if branch_id is None:
            PaymentRefundViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            PaymentRefundViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            PaymentRefundViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False
             
        return retValue

    def create(self, request, *args, **kwargs):
        paymentrefund_data= request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=paymentrefund_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)
        user = request.user

        if(PaymentRefundViewsets.ValidateDefaults(paymentrefund_data)==False):
            print(" Ooops!!! Error Occured ",PaymentRefundViewsets.logger)
        
        print(paymentrefund_data)

       # Branch and Company Null value

        branch_id=paymentrefund_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=paymentrefund_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        customer_id=paymentrefund_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
            
        company_year_id=paymentrefund_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        Customeradvanced_id=paymentrefund_data["ca_id"]
        print("Customer Advanced id is ",Customeradvanced_id,type(Customeradvanced_id))

        is_bank_transaction="True"
        if is_bank_transaction == "True":
            
            
            #Creat Payment Refund
            paymentrefund_id=RefundMaster.objects.create(
            company_id=company_id,
            customer_id=customer_id,
            branch_id=branch_id,
            bank_id=From_Bank,
            is_bank_transaction=True,
            refrence_id=Customeradvanced_id,
            coa_id=COA.objects.get(coa_id=paymentrefund_data["coa_id"]),
            refund_date=paymentrefund_data["payment_refund_date"],
            is_cust_advance_refund_generated=paymentrefund_data["is_payment_refund_generated"],
            refund_ref_no=paymentrefund_data["payment_refund_ref_no"],
            payment_mode=paymentrefund_data["paid_via"],
        # form_type=paymentrefund_data["form_type"],
            status=paymentrefund_data  ["status"],
            serial_ref=paymentrefund_data["payment_serial"],
            description=paymentrefund_data["description"],
            balance_amount_ref=paymentrefund_data["amount_excess"],
            amount_ref=paymentrefund_data["amount_received"])
            paymentrefund_id.save()
            print(paymentrefund_id)

            Audit.objects.create(
                company_id=company_id,
                branch_id=branch_id,
                created_by=user,
                audit_created_date=paymentrefund_data["payment_refund_date"],
                module="Banking",
                sub_module='Customer Advanced Refund',
                data=paymentrefund_data
            )
            custadv=CustomerAdvance.objects.get(ca_id=paymentrefund_data['ca_id'])
            TO_COA= COA.objects.get(company_id=company_id,account_name="Account Receivables",isdefault=True)
            print('""""""""""""',TO_COA)  
            paymnetmast=MasterTransaction.objects.create(
            L1detail_id=paymentrefund_id.rm_id,
            L1detailstbl_name='Refund Master',
            L2detail_id=From_Bank.bank_id,
            L2detailstbl_name='BANK',
            L3detail_id=custadv.ca_id,
            L3detailstbl_name='Customer Advanced',
            main_module='Banking',
            module='MonenyOut',
            sub_module='Customer Advanced Refund',
            transc_deatils='Customer Advanced refund',
            banking_module_type=paymentrefund_data["transaction_module"],
            journal_module_type=paymentrefund_data["transaction_module"],
            trans_date=paymentrefund_data["payment_refund_date"],
            trans_status=paymentrefund_data["status"],
            debit=paymentrefund_data["amount"],
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=paymentrefund_data['amount'],
            from_account=From_Bank.coa_id.coa_id,        
            from_acc_type=From_Bank.coa_id.account_type,
            from_acc_head=From_Bank.coa_id.account_head,
            from_acc_subhead=From_Bank.coa_id.account_subhead,
            from_acc_name=From_Bank.coa_id.account_name,
            company_id=company_id,
            customer_id=customer_id,
            branch_id=branch_id)
            paymnetmast.save() 
            
            # Test Balnce Amount Customer Advance balnce Amount Trasaction Check
            # the payment Of Custmer to pull or partiallz then update balance amount
            ca_id=paymentrefund_data["ca_id"]
            if ca_id is not None:
                ca_id=CustomerAdvance.objects.get(ca_id=ca_id)

                balance_amount=paymentrefund_data["amount_excess"]
                
                print("Amount values are",balance_amount,type(balance_amount))
                if balance_amount >=0:
                    print('Customer Advanced id of else', ca_id)
                    ca_id.balance_amount= paymentrefund_data["amount_excess"]            
                    ca_id.save()       
                    print('Customer Advanced amount updated to ', ca_id.balance_amount)
                else:     
                    print('ca_id', ca_id)              
                    print('Customer Advanced status is Not updated ')
                
            else:
                print("Balance Amount is Low")

            serializer = Refund_Serializer(paymentrefund_id)
            return Response(serializer.data)

