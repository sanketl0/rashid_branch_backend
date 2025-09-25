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
from banking.models.expense_refund_model import ExpenseRefund
from banking.serializers.expense_refund_serializers import ExpenseRefundSerializer
from purchase.models.Vendor_model import Vendor
from audit.models import Audit
from django.db import transaction
# ExpenseRefund
class ExpRefundModelViewSets(viewsets.ModelViewSet):
    queryset=ExpenseRefund.objects.all()
    serializer_class=ExpenseRefundSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        ExpRefundModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            ExpRefundModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            ExpRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            ExpRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False 
        if(type(branch_id!=uuid)):
            ExpRefundModelViewSets.logger.append("branch ID is not a Valid UUID Please Provide a valid branch ID ")
            retValue= False      
        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        exp_data_converte= request.data['data']

        user = request.user
        
        exp_data = json.loads(exp_data_converte)
        print("Converted Format is",type(exp_data))

        exp_file_data=request.FILES.get('attach_file')
        print("exp_data",type(exp_file_data))


        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=exp_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)

        if(ExpRefundModelViewSets.ValidateDefaults(exp_data)==False):
            print(" Ooops!!! Error Occured ",ExpRefundModelViewSets.logger)
            
        print(exp_data)
            #What if this ID is null , 
        	
        branch_id=exp_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=exp_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        vendor_id=exp_data["vendor_id"]
        if vendor_id is not None:
            vendor_id=Vendor.objects.get(vendor_id=vendor_id)
        
        # Create Expense Refund
        exped_id=ExpenseRefund.objects.create(
        company_id=company_id,
        branch_id=branch_id,
        bank_id=From_Bank,
        vendor_id=vendor_id,
        is_expense_refund_generated=exp_data["is_expense_refund_generated"],
        status=exp_data["status"],
        from_account=exp_data["from_account"],
        expense_type=exp_data["expense_type"],
        gst_treatment=exp_data["gst_treatment"],
        source_place=exp_data["source_place"],
        destination_place=exp_data["destination_place"],
        associated_expense=exp_data["associated_expense"],
        hsn_code=exp_data["hsn_code"],
        expense_refund_date=exp_data["expense_refund_date"],
        sac=exp_data["sac"],
        amount=exp_data["amount"],
        attach_file=exp_file_data,
        expense_refund_ref_no=exp_data["expense_refund_ref_no"],
        description=exp_data["description"],
        tax_rate=exp_data["tax_rate"],
        tax_name=exp_data["tax_name"],
        tax_type=exp_data["tax_type"],
        tax_amount=exp_data["tax_amount"],
        expense_total=exp_data["expense_total"],
        received_via=exp_data["received_via"])
        exped_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=exp_data["expense_refund_date"],
            module="Banking",
            sub_module='ExpenseRefund',
            data=exp_data
        )

#region Master Transaction Section
        TO_COA =COA.objects.get(coa_id=exp_data["from_account"])
        expmast=MasterTransaction.objects.create(
        L1detail_id=exped_id.exp_id,
        L1detailstbl_name='RefundMaster',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyIN',
        sub_module='ExpenseRefund',
        transc_deatils='Expense Refund',
        banking_module_type=exp_data["transaction_module"],
        journal_module_type=exp_data["transaction_module"],
        trans_date=exp_data["expense_refund_date"],
        trans_status=exp_data["status"],
        debit=exp_data["amount"],
        to_account=From_Bank.coa_id.coa_id,
        to_acc_type=From_Bank.coa_id.account_type,
        to_acc_head=From_Bank.coa_id.account_head,
        to_acc_subhead=From_Bank.coa_id.account_subhead,
        to_acc_name=From_Bank.coa_id.account_name,
        credit=exp_data['amount'],
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_subhead,
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        vendor_id=vendor_id,
        branch_id=branch_id)
        expmast.save()
#endregion
#End Master Transaction     
        serializer = ExpenseRefundSerializer(exped_id)
        return Response(serializer.data)

