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
from banking.models.transfer_from_another_account_model import TransferFromAnotherAccount
from banking.serializers.transfer_from_another_account_serializers import TFAASerializer
from audit.models import Audit
from django.db import transaction
class TFAAModelViewSets(viewsets.ModelViewSet):
    queryset=TransferFromAnotherAccount.objects.all()
    serializer_class=TFAASerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        TFAAModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            TFAAModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            TFAAModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            TFAAModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue    
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        tfaa_data_converte= request.data['data']

        user = request.user
        tfaa_data = json.loads(tfaa_data_converte)
        print("Converted Format is",type(tfaa_data))

        tfaa_file_data=request.FILES.get('attach_file')
        print("transafer from_data",type(tfaa_file_data))


        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=tfaa_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)


        if(TFAAModelViewSets.ValidateDefaults(tfaa_data)==False):
            print(" Ooops!!! Error Occured ",TFAAModelViewSets.logger)
            
        print(tfaa_data)
            #What if this ID is null , 
        	
        branch_id=tfaa_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=tfaa_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
            
        company_year_id=tfaa_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        # create Transfer From Another account

        tfaac_id=TransferFromAnotherAccount.objects.create(
        company_id=company_id,
        branch_id=branch_id, 
        bank_id=From_Bank,
        attach_file=tfaa_file_data,      
        from_account=tfaa_data["from_account"],
        amount=tfaa_data["amount"],
        transfer_from_date=tfaa_data["transfer_from_date"],
        transfer_from_ref_no=tfaa_data["transfer_from_ref_no"],
        description=tfaa_data["description"],
        status=tfaa_data["status"])
        tfaac_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=tfaa_data["transfer_from_date"],
            module="Banking",
            sub_module='TFAA',
            data=tfaa_data
        )

         #region  Master Transaction Section

        TO_COA =COA.objects.get(coa_id=tfaa_data["from_account"])
        TFAAmast=MasterTransaction.objects.create(
        L1detail_id=tfaac_id.tfaa_id,
        L1detailstbl_name='TFAA',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyIN',
        sub_module='TFAA',
        transc_deatils='Transfer From Another Account',
        banking_module_type=tfaa_data["transaction_module"],
        journal_module_type=tfaa_data["transaction_module"],
        trans_date=tfaa_data["transfer_from_date"],
        trans_status=tfaa_data["status"],
        debit=tfaa_data["amount"],
        to_account=From_Bank.coa_id.coa_id,
        to_acc_type=From_Bank.coa_id.account_type,
        to_acc_head=From_Bank.coa_id.account_head,
        to_acc_subhead=From_Bank.coa_id.account_subhead,
        to_acc_name=From_Bank.coa_id.account_name,
        credit=tfaa_data['amount'],
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_subhead,
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        branch_id=branch_id)
        TFAAmast.save()      
        
# endregion 
#End Master Transaction Section
        serializer =TFAASerializer(tfaac_id)    
        return Response(serializer.data)

