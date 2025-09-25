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
from salescustomer.models.Salescustomer_model import SalesCustomer
from banking.models.other_income_model import OtherIncome
from banking.serializers.other_income_serializers import OtherIncomeSerializer
from django.db import transaction
from audit.models import Audit
class OtherIncomeModelViewSets(viewsets.ModelViewSet):
    queryset=OtherIncome.objects.all()
    serializer_class=OtherIncomeSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        OtherIncomeModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            OtherIncomeModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            OtherIncomeModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            OtherIncomeModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        otherincome_data_converte= request.data['data']

        user = request.user
        otherincome_data = json.loads(otherincome_data_converte)
        print("Converted Format is",type(otherincome_data))

        otherincome_file_data=request.FILES.get('attach_file')
        print("otherincome_data",type(otherincome_file_data))


        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=otherincome_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)


        if(OtherIncomeModelViewSets.ValidateDefaults(otherincome_data)==False):
            print(" Ooops!!! Error Occured ",OtherIncomeModelViewSets.logger)
            
        print(otherincome_data)
            #What if this ID is null , 

        branch_id=otherincome_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=otherincome_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
            
        
        



       
        # create OtherIncome
		
        otherincome_id=OtherIncome.objects.create(
        company_id=company_id,
        branch_id=branch_id,
        bank_id=From_Bank,
        attach_file=otherincome_file_data,
        amount=otherincome_data["amount"],
        status=otherincome_data["status"],
        from_account=otherincome_data["from_account"],
        description=otherincome_data["description"],
        other_income_date=otherincome_data["other_income_date"],
        other_income_ref_no=otherincome_data["other_income_ref_no"], 
        received_via=otherincome_data["received_via"])
        otherincome_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=otherincome_data["other_income_date"],
            module="Banking",
            sub_module='OtherIncome',
            data=otherincome_data
        )

        TO_COA=COA.objects.get(coa_id=otherincome_data["from_account"])
        oimast=MasterTransaction.objects.create(
        L1detail_id=otherincome_id.oi_id,
        L1detailstbl_name='OtherIncome',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyIN',
        sub_module='OtherIncome',
        transc_deatils='OtherIncome',
        banking_module_type=otherincome_data["transaction_module"],
        journal_module_type=otherincome_data["transaction_module"],
        trans_date=otherincome_data["other_income_date"],
        trans_status=otherincome_data["status"],
        debit=otherincome_data["amount"],
        to_account=From_Bank.coa_id.coa_id,
        to_acc_type=From_Bank.coa_id.account_type,
        to_acc_head=From_Bank.coa_id.account_head,
        to_acc_subhead=From_Bank.coa_id.account_subhead,
        to_acc_name=From_Bank.coa_id.account_name,
        credit=otherincome_data['amount'],
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_subhead,
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        branch_id=branch_id)
        oimast.save() 
#endregion
#End of Master Transaction
        serializer=OtherIncomeSerializer(otherincome_id)      
        return Response(serializer.data)
