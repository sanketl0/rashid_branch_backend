import json
import os
from django.http import HttpResponse, FileResponse
import uuid
from rest_framework.response import Response
from rest_framework import viewsets,generics
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.banking_model import Banking
from salescustomer.models.Salescustomer_model import SalesCustomer
from banking.models.dtoa_model import DTOA
from banking.serializers.dtoa_serializers import DTOASerializer
from wsgiref.util import FileWrapper
from audit.models import Audit
from django.db import transaction
class DTOAViewsets(viewsets.ModelViewSet):
    queryset =DTOA.objects.all()
    serializer_class =DTOASerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        DTOAViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            DTOAViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            DTOAViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            DTOAViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        dtoa_data_converte= request.data['data']

        user = request.user
       
        dtoa_data = json.loads(dtoa_data_converte)
        print("Converted Format is",type(dtoa_data))

        dtoa_file_data=request.FILES.get('attach_file')
        print("Dtoa_data",type(dtoa_file_data))

        
        # GET coa_id in Banking and Pass the bank_id Transaction Table
        bank=dtoa_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)

        if(DTOAViewsets.ValidateDefaults(dtoa_data)==False):
            print(" Ooops!!! Error Occured ",DTOAViewsets.logger)
        
        print(dtoa_data)

        #Branch and Company Null Value

        branch_id=dtoa_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=dtoa_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        customer_id=dtoa_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
            
            
        company_year_id=dtoa_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        

        # Creating DTOA
        dtoa_id=DTOA.objects.create(
        status=dtoa_data["status"],
        deposit_to_date=dtoa_data["deposit_to_date"],
        deposit_to_ref_no=dtoa_data["deposit_to_ref_no"],
        description=dtoa_data["description"],
        to_account=dtoa_data["to_account"],
        paid_via=dtoa_data["paid_via"],
        amount=dtoa_data["amount"],
        company_id=company_id,
        branch_id=branch_id,
        attach_file=dtoa_file_data,
        bank_id=From_Bank,
        customer_id=customer_id)    
        dtoa_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=dtoa_data["deposit_to_date"],
            module="Banking",
            sub_module='DTOA',
            data=dtoa_data
        )

# region Of the MasterTransaction of DTOA

        TO_COA = COA.objects.get(coa_id=dtoa_data["to_account"])
        dtoamast=MasterTransaction.objects.create(
        L1detail_id=dtoa_id.dtoa_id,
        L1detailstbl_name='DTOA',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyOut',
        sub_module='DTOA',
        transc_deatils='Deposit to Other Account',
        banking_module_type=dtoa_data["transaction_module"],
        journal_module_type=dtoa_data["transaction_module"],
        trans_date=dtoa_data["deposit_to_date"],
        trans_status=dtoa_data["status"],
        debit=dtoa_data["amount"],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=dtoa_data['amount'],
        from_account=From_Bank.coa_id.coa_id,        
        from_acc_type=From_Bank.coa_id.account_type,
        from_acc_head=From_Bank.coa_id.account_head,
        from_acc_subhead=From_Bank.coa_id.account_subhead,
        from_acc_name=From_Bank.coa_id.account_name,
        company_id=company_id,
        branch_id=branch_id)
        dtoamast.save()
#endregion
        serializer = DTOASerializer(dtoa_id)
        return Response( serializer.data)



# file download section Deposite to other account
class DTOAFileDownloadListAPIView(generics.ListAPIView):
    def get(self, request, dtoa_id, format=None):
        queryset = DTOA.objects.get(dtoa_id=dtoa_id)
        file_handle = queryset.attach_file.path
        if os.path.exists(file_handle):
            document = open(file_handle, 'rb')
            response = HttpResponse(FileWrapper(document), content_type='application/msword')
            response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
        else:
            response=HttpResponse("File Not Found")
        return response
    