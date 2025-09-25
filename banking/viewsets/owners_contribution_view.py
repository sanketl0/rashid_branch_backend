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
from banking.models.owners_contribution_model import OwnersContribution
from banking.serializers.owners_contribution_serializers import OwnersContributionSerializer
from utility import save_attach_file
from audit.models import Audit
from django.db import transaction
# Owners Contribution
class OwnersContributionModelViewSets(viewsets.ModelViewSet):
    queryset=OwnersContribution.objects.all()
    serializer_class=OwnersContributionSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        OwnersContributionModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            OwnersContributionModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            OwnersContributionModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            OwnersContributionModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        #ownerscontribution_data = request.data
        oc_data_converte= request.data['data']
        user = request.user
        ownerscontribution_data = json.loads(oc_data_converte)
        print("Converted Format is",type(ownerscontribution_data))

        oc_file_data=request.FILES.get('attach_file')
        print("ownerscontribution_data",type(oc_file_data))


        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=ownerscontribution_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)
            
        branch_id=ownerscontribution_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=ownerscontribution_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

       

        # Create OwnersContribution

        ococ_id=OwnersContribution.objects.create(
        company_id=company_id,
        branch_id=branch_id,
        bank_id=From_Bank,
        transaction_module=ownerscontribution_data["transaction_module"],
        status=ownerscontribution_data["status"],
        transaction_type=ownerscontribution_data["transaction_type"],
        from_account=ownerscontribution_data["from_account"],
        owners_cont_date=ownerscontribution_data["owners_cont_date"],
        owners_cont_ref_no=ownerscontribution_data["owners_cont_ref_no"],
        amount=ownerscontribution_data["amount"],
        attach_file=oc_file_data,
        description=ownerscontribution_data["description"])
        ococ_id.save()
        if oc_file_data is not None:
            file_ext = os.path.splitext(oc_file_data.name)[1]
            new_file_path = f'media/OwnersContribution_{ococ_id.oc_id}{file_ext}' 
            pth=save_attach_file(oc_file_data,new_file_path)
            ococ_id.attach_file=pth
            ococ_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=ownerscontribution_data["owners_cont_date"],
            module="Banking",
            sub_module='OwnerContribution',
            data=ownerscontribution_data
        )
        
#region Master Transaction Section

        TO_COA =COA.objects.get(coa_id=ownerscontribution_data["from_account"])
        print('""""""""""""',TO_COA)  
        ocmast=MasterTransaction.objects.create(
        L1detail_id=ococ_id.oc_id,
        L1detailstbl_name='OwnerContribution',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyIN',
        sub_module='OwnerContribution',
        transc_deatils='Owner Contribution',
        banking_module_type=ownerscontribution_data["transaction_module"],
        journal_module_type=ownerscontribution_data["transaction_module"],
        trans_date=ownerscontribution_data["owners_cont_date"],
        trans_status=ownerscontribution_data["status"],
        debit=ownerscontribution_data["amount"],
        to_account=From_Bank.coa_id.coa_id,
        to_acc_type=From_Bank.coa_id.account_type,
        to_acc_head=From_Bank.coa_id.account_head,
        to_acc_subhead=From_Bank.coa_id.account_subhead,
        to_acc_name=From_Bank.coa_id.account_name,
        credit=ownerscontribution_data['amount'],
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_subhead,
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        branch_id=branch_id)
        ocmast.save()      
       
#endregion 

#End Master Transaction Section

        serializer=OwnersContributionSerializer(ococ_id)      
        return Response(serializer.data)

