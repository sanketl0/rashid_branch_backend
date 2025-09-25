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
from banking.models.interest_income_model import InterestIncome
from banking.serializers.interest_income_serializers import InterestIncomeSerialiser
from utility import save_attach_file
from django.db import transaction
from audit.models import Audit
#InterstIncome

class InterestIncomeModelViewSets(viewsets.ModelViewSet):
    queryset=InterestIncome.objects.all()
    serializer_class=InterestIncomeSerialiser

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        InterestIncomeModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            InterestIncomeModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            InterestIncomeModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            InterestIncomeModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False 
        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        intrestincome_data_converte= request.data['data']

        user = request.user
        interestincome_data = json.loads(intrestincome_data_converte)
        print("Converted Format is",type(interestincome_data))

        intrestincome_file_data=request.FILES.get('attach_file')
        print("IntrestIncome_data",type(intrestincome_file_data))

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=interestincome_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)

        if(InterestIncomeModelViewSets.ValidateDefaults(interestincome_data)==False):
            print(" Ooops!!! Error Occured ",InterestIncomeModelViewSets.logger)
            
        print(interestincome_data)
            #What if this ID is null , 
        	
        branch_id=interestincome_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=interestincome_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
        
        
        # create Interest income

        iiad_id=InterestIncome.objects.create(
        company_id=company_id,
        branch_id=branch_id,
        bank_id=From_Bank,
        attach_file=intrestincome_file_data,
        status=interestincome_data["status"],
        interest_income_date=interestincome_data["interest_income_date"],
        interest_income_ref_no=interestincome_data["interest_income_ref_no"],
        description=interestincome_data["description"],
        received_via=interestincome_data["received_via"],
        amount=interestincome_data["amount"],
        from_account=COA.objects.get(coa_id=interestincome_data["coa_id"]))
        iiad_id.save()
        if intrestincome_file_data is not None:

            file_ext = os.path.splitext(intrestincome_file_data.name)[1]
            new_file_path = f'INTREST/Intrest_{iiad_id.ii_id}{file_ext}' 
            pth=save_attach_file(intrestincome_file_data,new_file_path)
            iiad_id.attach_file=pth
            iiad_id.save()
            print("income_interest_created",iiad_id,type(iiad_id))

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=interestincome_data["interest_income_date"],
            module="Banking",
            sub_module='IntrestIncome',
            data=interestincome_data
        )

        TO_COA =COA.objects.get(company_id=company_id,account_name="Interest Income",isdefault=True)
        iimast=MasterTransaction.objects.create(
        L1detail_id=iiad_id.ii_id,
        L1detailstbl_name='IntrestIncome',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyIN',
        sub_module='IntrestIncome',
        transc_deatils='Intrest Income',
        banking_module_type=interestincome_data["transaction_module"],
        journal_module_type=interestincome_data["transaction_module"],
        trans_date=interestincome_data["interest_income_date"],
        trans_status=interestincome_data["status"],
        debit=interestincome_data["amount"],
        to_account=From_Bank.coa_id.coa_id,
        to_acc_type=From_Bank.coa_id.account_type,
        to_acc_head=From_Bank.coa_id.account_head,
        to_acc_subhead=From_Bank.coa_id.account_subhead,
        to_acc_name=From_Bank.coa_id.account_name,
        credit=interestincome_data['amount'],
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_subhead,
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        branch_id=branch_id)
        iimast.save() 
#endregion
# End Master Transaction Section     
        
        serializer =InterestIncomeSerialiser(iiad_id)        
        return Response(serializer.data)
		
