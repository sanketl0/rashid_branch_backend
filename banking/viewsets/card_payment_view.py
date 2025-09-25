import json
import os
from pathlib import Path

import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.banking_model import Banking
from banking.models.card_payment_model import CardPayment
from banking.serializers.card_payment_serializers import CardPaymentSerializer
from utility import save_attach_file
from audit.models import Audit

#region
from django.db import transaction
class CardPaymentViewsets(viewsets.ModelViewSet):
    queryset = CardPayment.objects.all()
    serializer_class =CardPaymentSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        CardPaymentViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        
        company_year_id=obj.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        
        retValue=True
        if branch_id is None:
            CardPaymentViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            CardPaymentViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            CardPaymentViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
       # card_payment_data = request.data
        user=request.user
        cardpayment_data_converte= request.data['data']
        print(cardpayment_data_converte)
        print("CardPaymentData Format is ",type(cardpayment_data_converte))
        card_payment_data = json.loads(cardpayment_data_converte)
        print("Converted Format is",type(card_payment_data))

        card_payment_file_data=request.FILES.get('attach_file')
        print("cardpayment_data",type(card_payment_file_data))


        # GET coa_id in Banking and Pass the bank_id Transaction Table
        bank=card_payment_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)



        if(CardPaymentViewsets.ValidateDefaults(card_payment_data)==False):
            print(" Ooops!!! Error Occured ",CardPaymentViewsets.logger)
        
        print(card_payment_data)

        # Branch and Company Null Value

        branch_id=card_payment_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=card_payment_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        company_year_id=card_payment_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        #Creating CardPayment
        cardpayments_id=CardPayment.objects.create(
        status=card_payment_data["status"],        
        paid_to=card_payment_data['paid_to'],
        amount=card_payment_data['amount'],
        card_payment_date=card_payment_data["card_payment_date"],
        card_payment_ref_no=card_payment_data["card_payment_ref_no"],
        description=card_payment_data["description"],
        attach_file=card_payment_file_data,
        company_id=company_id,
        bank_id=From_Bank,
        branch_id=branch_id)
        cardpayments_id.save()

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=card_payment_data["card_payment_date"],
            module="Banking",
            sub_module='CardPayment',
            data=card_payment_data
        )
        if card_payment_file_data is not None:
            file_ext = os.path.splitext(card_payment_file_data.name)[1]
            new_file_path = f'media/CardPayment_{cardpayments_id.cardpayment_id}{file_ext}' 
            pth=save_attach_file(card_payment_file_data,new_file_path)
            cardpayments_id.attach_file=pth
            cardpayments_id.save()
 
        print("Card_Payment",cardpayments_id,type(cardpayments_id))

       
# MasterTransaction By Card Payment

         
        TO_COA = COA.objects.get(coa_id=card_payment_data["paid_to"])
        print('""""""""""""',TO_COA)  
        cp_mast=MasterTransaction.objects.create(
        L1detail_id=cardpayments_id.cardpayment_id,
        L1detailstbl_name='CardPayment',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyOut',
        sub_module='CardPayment',
        transc_deatils='Card Payment',
        banking_module_type=card_payment_data["transaction_module"],
        journal_module_type=card_payment_data["transaction_module"],
        trans_date=card_payment_data["card_payment_date"],
        trans_status=card_payment_data["status"],
        debit=card_payment_data["amount"],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=card_payment_data['amount'],
        from_account=From_Bank.coa_id.coa_id,        
        from_acc_type=From_Bank.coa_id.account_type,
        from_acc_head=From_Bank.coa_id.account_head,
        from_acc_subhead=From_Bank.coa_id.account_subhead,
        from_acc_name=From_Bank.coa_id.account_name,
        company_id=company_id,
        branch_id=branch_id)
        cp_mast.save() 
       

        serializer = CardPaymentSerializer(cardpayments_id)
        return Response(serializer.data)

#endregion