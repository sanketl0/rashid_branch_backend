import json

import uuid
from rest_framework.response import Response
from rest_framework import viewsets

from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.banking_model import Banking
from banking.models.dfoa_model import DFOA
from banking.serializers.dfoa_serializers import DFOASerializer

from salescustomer.models.Salescustomer_model import SalesCustomer
from audit.models import Audit
from django.db import transaction

#Deposit From Other Account 
class DFOAViewsets(viewsets.ModelViewSet):
    queryset =DFOA.objects.all()
    serializer_class =DFOASerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        DFOAViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        customer_id=obj["customer_id"]
        retValue=True
        if branch_id is None:
            DFOAViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        


        if customer_id is None:
            DFOAViewsets.logger.append("Customer iD is Null Please Provide a Customer ID")
            retValue= False  

        if(company_id is  None ):
            DFOAViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False

        if(type(company_id!=uuid)):
            DFOAViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False

        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        dfoa_data_converte= request.data['data']
        user = request.user
        
        dfoa_data = json.loads(dfoa_data_converte)
        print("Converted Format is",type(dfoa_data))

        dfoa_file_data=request.FILES.get('attach_file')
        print("dfoa_data",type(dfoa_file_data))


        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=dfoa_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)



        if(DFOAViewsets.ValidateDefaults(dfoa_data)==False):
            print(" Ooops!!! Error Occured ",DFOAViewsets.logger)
        
        print(dfoa_data)

        branch_id=dfoa_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=dfoa_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        customer_id=dfoa_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
            
        company_year_id=dfoa_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        
        #Creating Customer Payment
        dfoaed_id=DFOA.objects.create(
        company_id=company_id,
        branch_id=branch_id,
        bank_id=From_Bank,
        attach_file=dfoa_file_data,
        customer_id=customer_id,
        amount=dfoa_data["amount"],
        deposit_from_date=dfoa_data["deposit_from_date"] ,
        deposit_from_ref_no=dfoa_data["deposit_from_ref_no"],
        from_account=dfoa_data["from_account"],
        received_via=dfoa_data["received_via"],
        description=dfoa_data["description"],
        status=dfoa_data["status"])
        dfoaed_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=dfoa_data["deposit_from_date"],
            module="Banking",
            sub_module='DFOA',
            data=dfoa_data
        )

#region Master Trasaction Section

        TO_COA= COA.objects.get(coa_id=dfoa_data["from_account"] )
        print('""""""""""""',TO_COA) 
        dfoadebittrans=MasterTransaction.objects.create(
        L1detail_id=dfoaed_id.dfoa_id,
        L1detailstbl_name='DFOA',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenIN',
        sub_module='DFOA',
        transc_deatils='Deposit Form other Account',
        banking_module_type=dfoa_data["transaction_module"],
        journal_module_type=dfoa_data["transaction_module"],
        trans_date=dfoa_data["deposit_from_date"],
        trans_status=dfoa_data["status"],
        debit=dfoa_data["amount"],
        to_account=From_Bank.coa_id.coa_id,
        to_acc_type=From_Bank.coa_id.account_type,
        to_acc_head=From_Bank.coa_id.account_head,
        to_acc_subhead=From_Bank.coa_id.account_subhead,
        to_acc_name=From_Bank.coa_id.account_name,
        credit=dfoa_data['amount'],
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_subhead,
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        customer_id=customer_id,
        branch_id=branch_id)
        dfoadebittrans.save() 
       
#endregion
#End Of Master Trasaction Section
        serializer = DFOASerializer(dfoaed_id)
        return Response(serializer.data)

