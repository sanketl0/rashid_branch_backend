
import json
import os
from pathlib import Path

import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.ttaa_model import TTAA
from banking.serializers.ttaa_serilalizers import TransferToAnotherAccountSerializer
from banking.models.banking_model import Banking
from audit.models import Audit
from django.db import transaction
class TransferToAnotherAccountViewsets(viewsets.ModelViewSet):
    queryset = TTAA.objects.all()
    serializer_class =TransferToAnotherAccountSerializer

    logger=[]

        # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        TransferToAnotherAccountViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        
        
        
        retValue=True
        if branch_id is None:
            TransferToAnotherAccountViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            TransferToAnotherAccountViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            TransferToAnotherAccountViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue

    @transaction.atomic
    def create(self, request, *args, **kwargs):
       # ttaa_data = request.data
        ttaa_data_converte= request.data['data']
        ttaa_data = json.loads(ttaa_data_converte)
        print("Converted Format is",type(ttaa_data))

        ttaa_file_data=request.FILES.get('attach_file')
        user = request.user
        bank=ttaa_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)

        branch_id=ttaa_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=ttaa_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
        
        
        company_year_id=ttaa_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        # Creating the Transfer To another accounting
        ttaaed_id=TTAA.objects.create(
        status=ttaa_data["status"],
        #What if this ID is null , 
        to_account=ttaa_data['to_account'],
        amount=ttaa_data['amount'],
        transfer_to_date=ttaa_data["transfer_to_date"],
        transfer_to_ref_no=ttaa_data["transfer_to_ref_no"],
        description=ttaa_data["description"],
        branch_id=branch_id,
        attach_file=ttaa_file_data,
        bank_id=From_Bank,
        company_id=company_id)
        ttaaed_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=ttaa_data["transfer_to_date"],
            module="Banking",
            sub_module='TTAA',
            data=ttaa_data
        )


#region MasterTransaction By Transfer to Another Account

        TO_COA = COA.objects.get(coa_id=ttaa_data["to_account"])
        print('""""""""""""',TO_COA)  
        TTAAmast=MasterTransaction.objects.create(
        L1detail_id=ttaaed_id.ttaa_id,
        L1detailstbl_name='TTAA',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyOut',
        sub_module='TTAA',
        transc_deatils='Transfer to Another Account',
        banking_module_type=ttaa_data["transaction_module"],
        journal_module_type=ttaa_data["transaction_module"],
        trans_date=ttaa_data["transfer_to_date"],
        trans_status=ttaa_data["status"],
        debit=ttaa_data["amount"],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=ttaa_data['amount'],
        from_account=From_Bank.coa_id.coa_id,        
        from_acc_type=From_Bank.coa_id.account_type,
        from_acc_head=From_Bank.coa_id.account_head,
        from_acc_subhead=From_Bank.coa_id.account_subhead,
        from_acc_name=From_Bank.coa_id.account_name,
        company_id=company_id,
        branch_id=branch_id)
        TTAAmast.save() 
#endregion Master Transaction

        serializer = TransferToAnotherAccountSerializer(ttaaed_id)
        return Response(serializer.data)

