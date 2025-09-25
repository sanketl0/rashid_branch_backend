import json
import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.banking_model import Banking
from salescustomer.models.Salescustomer_model import SalesCustomer
from banking.models.customer_payment_model import CustomerPayment
from banking.serializers.customer_payment_serializers import CustomerPaymentSerializer
from salescustomer.models.Pr_model import PR
from salescustomer.models.Invoice_model import Invoice
from audit.models import Audit
from django.db import transaction

class CustomerPaymentViewsets(viewsets.ModelViewSet):
    queryset =CustomerPayment.objects.all()
    serializer_class =CustomerPaymentSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        CustomerPaymentViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]

        retValue=True
        if branch_id is None:
            CustomerPaymentViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            CustomerPaymentViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            CustomerPaymentViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cp_data_converte= request.data['data']
        user = request.user
        print("#################################################")
        print(cp_data_converte)
        print("Customer Payment Data Format is ",type(cp_data_converte))
        print("#################################################")
        # PR Convert Str to Dict Code
        cp_data = json.loads(cp_data_converte)
        print("Converted Format is",type(cp_data))

        cp_file_data=request.FILES.get('attach_file')
        print("cp_data",type(cp_file_data))

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=cp_data["deposit_to"]
        print("bank", bank)
        From_Bank=Banking.objects.get(coa_id=bank)

        if(CustomerPaymentViewsets.ValidateDefaults(cp_data)==False):
            print(" Ooops!!! Error Occured ",CustomerPaymentViewsets.logger)
        
        print(cp_data)
        #Branch And Company Null Code
        branch_id=cp_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=cp_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        customer_id=cp_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)

        
        company_year_id=cp_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        #Creating Customer Payment
        # transaction_module=cp_data["transaction_module"]
        # print("transaction module", transaction_module)
        # if transaction_module=="Customer Payment":  
        ## If bank transaction is true then this entry will go to the payment receive table
        is_bank_transaction="True"
        print("Bank Transaction", is_bank_transaction)
        if is_bank_transaction=="True": 

            cped_id=PR.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            bank_id=From_Bank,
            customer_id=customer_id,
            pay_status=cp_data["pay_status"],
            payment_serial=cp_data["payment_serial"],
            payment_ref_no=cp_data["payment_ref_no"],
            payment_mode=cp_data["payment_mode"],
            deposit_to=cp_data["deposit_to"],
            status=cp_data["status"],
            is_bank_transaction=True,
            amount_received=cp_data["amount_received"],
            bank_charges=cp_data["bank_charges"],
            payment_date=cp_data["payment_date"],
            tax_deducted=cp_data["tax_deducted"],
            tds_tax_account=cp_data["tds_tax_account"],
            balance_amount=cp_data["balance_amount"],
            amount_excess=cp_data["amount_excess"],
            invoice_date=cp_data["invoice_date"],
            invoice_serial=cp_data["invoice_serial"],
            invoice_amount=cp_data["invoice_amount"],
            invoice_id=Invoice.objects.get(invoice_id=cp_data["invoice_id"]),
            #coa_id=Banking.objects.get(coa_id=cp_data["deposit_to"]),
            #sub_total=cp_data["sub_total"],
            amount_due=cp_data["amount_due"],
            form_type="Customer Payment",
            attach_file=cp_file_data,
            notes=cp_data["notes"]) 
            cped_id.save()


            #2 Financial Transaction Prerequisites 
            ## Credit Transaction 
            ## SHould be added the amount TO_COA_ID 
            # Refer the Excel coa_id refers  Bank COA it depends on the Form whether it is To_COA or From_COA


            # Get The COA Table  Account Name is Account Receivables and Pass The coa_id id Customer Payment Transaction Table 

            FROM_COA =COA.objects.get(company_id=company_id,account_name="Account Receivables",isdefault=True)
            invoice=Invoice.objects.get(invoice_id=cp_data["invoice_id"])

            Audit.objects.create(
                company_id=company_id,
                branch_id=branch_id,
                created_by=user,
                audit_created_date=cp_data["payment_date"],
                module="Banking",
                sub_module='Customer Payment',
                data=cp_data
            )


            TO_COA= COA.objects.get(company_id=company_id,account_name="Account Receivables",isdefault=True)
            camast=MasterTransaction.objects.create(
            L1detail_id=cped_id.pr_id,
            L1detailstbl_name='salescustomer_pr',
            L2detail_id=From_Bank.bank_id,
            L2detailstbl_name='BANK',
            L3detail_id=invoice.invoice_id,
            L3detailstbl_name='Invoice',
            main_module='Banking',
            module='MoneayIN',
            sub_module='Customer Payment',
            transc_deatils='Customer Payment',
            banking_module_type=cp_data["transaction_module"],
            journal_module_type='Invoice_Payment',
            trans_date=cp_data["payment_date"],
            trans_status=cp_data["status"],
            debit=cp_data["amount_received"],
            to_account=From_Bank.coa_id.coa_id,
            to_acc_type=From_Bank.coa_id.account_type,
            to_acc_head=From_Bank.coa_id.account_head,
            to_acc_subhead=From_Bank.coa_id.account_subhead,
            to_acc_name=From_Bank.coa_id.account_name,
            credit=cp_data['amount_received'],
            from_account=TO_COA.coa_id,
            from_acc_type=TO_COA.account_type,
            from_acc_head=TO_COA.account_head,
            from_acc_subhead=TO_COA.account_subhead,
            from_acc_name=TO_COA.account_name,
            company_id=company_id,
            customer_id=customer_id,
            branch_id=branch_id)
            camast.save()      
            
#endregion

#End MasterTrasaction

            #If payment is full then payment status will change unpaid to paid in invoice
            balance_amount=float(cp_data["balance_amount"])
            amount_excess=float(cp_data["amount_excess"])
            #if amount_due == amount_received:
            if balance_amount <= 0:
                invoice_id = Invoice.objects.get(invoice_id=cp_data["invoice_id"])       
                print('invoice_id', invoice_id)              
                invoice_id.payment_status='paid'
                invoice_id.save()
                print('invoice status updated to ', invoice_id.payment_status)

            if amount_excess < 0:
                invoice_id = Invoice.objects.get(invoice_id=cp_data["invoice_id"])       
                print('invoice_id', invoice_id)              
                invoice_id.amount_due = cp_data["balance_amount"]            
                invoice_id.save()       
                print('invoice amount due updated to ', invoice_id.amount_due)

            else:
                invoice_id = Invoice.objects.get(invoice_id=cp_data["invoice_id"])
                print('invoice id of else', invoice_id)
                invoice_id.amount_due = cp_data["balance_amount"]            
                invoice_id.save()       
                print('invoice amount due updated to ', invoice_id.amount_due)
            serializer = CustomerPaymentSerializer(cped_id)
            return Response(serializer.data)
