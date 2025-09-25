import json
import os
from pathlib import Path
from utility import save_attach_file
import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.banking_model import Banking
from banking.models.owner_drawing_model import OwnerDrawing
from banking.serializers.owner_drawing_serializers import OwnerDrawingSerializer
from django.db import transaction
from audit.models import Audit
class OwnerdrawingModelViewSets(viewsets.ModelViewSet):
    queryset=OwnerDrawing.objects.all()
    serializer_class=OwnerDrawingSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        OwnerdrawingModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            OwnerdrawingModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            OwnerdrawingModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            OwnerdrawingModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        #ownerdrawing_data = request.data

        od_data_converte= request.data['data']

        user = request.user
        ownerdrawing_data = json.loads(od_data_converte)
        print("Converted Format is",type(ownerdrawing_data))

        od_file_data=request.FILES.get('attach_file')
        print("ownerdrawing_data",type(od_file_data))


        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=ownerdrawing_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)

        if(OwnerdrawingModelViewSets.ValidateDefaults(ownerdrawing_data)==False):
            print(" Ooops!!! Error Occured ",OwnerdrawingModelViewSets.logger)
        
        print(ownerdrawing_data)
        #What if this ID is null , 

        branch_id=ownerdrawing_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=ownerdrawing_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
            
        company_year_id=ownerdrawing_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        #Create Ownerdrawing	
        ownerdrawing_id=OwnerDrawing.objects.create(
        company_id=company_id,
        branch_id=branch_id,
        bank_id=From_Bank,
        status=ownerdrawing_data["status"],
        to_account=ownerdrawing_data["to_account"],
        amount=ownerdrawing_data["amount"],
        attach_file=od_file_data,      
        owners_drawing_date=ownerdrawing_data["owners_drawing_date"],
        owners_drawing_ref_no=ownerdrawing_data["owners_drawing_ref_no"],
        description=ownerdrawing_data["description"])
        ownerdrawing_id.save()
        print("ownerdrawing_created",ownerdrawing_id)

        if od_file_data is not None:
            file_ext = os.path.splitext(od_file_data.name)[1]
            new_file_path = f'media/OwnerDrawing{ownerdrawing_id.ownerdrawing_id}{file_ext}' 
            pth=save_attach_file(od_file_data,new_file_path)
            ownerdrawing_id.attach_file=pth
            ownerdrawing_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=ownerdrawing_data["owners_drawing_date"],
            module="Banking",
            sub_module='OwnerDrawing',
            data=ownerdrawing_data
        )
       
#region Master Transaction Section  Ownwer Drawing
        TO_COA = COA.objects.get(coa_id=ownerdrawing_data["to_account"])
        print('""""""""""""',TO_COA)  
        odcreditTransaction=MasterTransaction.objects.create(
        L1detail_id=ownerdrawing_id.ownerdrawing_id,
        L1detailstbl_name='OwnerDrawing',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyOut',
        sub_module='OwnerDrawing',
        transc_deatils='Owner Drawing',
        banking_module_type=ownerdrawing_data["transaction_module"],
        journal_module_type=ownerdrawing_data["transaction_module"],
        trans_date=ownerdrawing_data["owners_drawing_date"],
        trans_status=ownerdrawing_data["status"],
        debit=ownerdrawing_data["amount"],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=ownerdrawing_data['amount'],
        from_account=From_Bank.coa_id.coa_id,        
        from_acc_type=From_Bank.coa_id.account_type,
        from_acc_head=From_Bank.coa_id.account_head,
        from_acc_subhead=From_Bank.coa_id.account_subhead,
        from_acc_name=From_Bank.coa_id.account_name,
        company_id=company_id,
        branch_id=branch_id)
        odcreditTransaction.save() 
        
#endregion
#END Master Transaction Section Ownere Drawing

        serializer =OwnerDrawingSerializer(ownerdrawing_id)         
        return Response(serializer.data)
