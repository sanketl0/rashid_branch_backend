import imp
import os
import json 
import uuid
from pathlib import Path
from io import BytesIO
import datetime
from rest_framework import viewsets,generics,mixins
from rest_framework.response import Response
from company.models import Company, Branch
from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.views.generic import View
from rest_framework.decorators import api_view
from salescustomer.printing.generate_pr import generate_pr_pdf
from utility import render_to_pdf
from re import template
from xhtml2pdf import pisa
import pandas as pd
from banking.models import CustomerAdvance,RefundMaster
from banking.serializers import CustomerAdvancedSerializer,CustomerAdvSerializer,GetCustomerShortBy_CompanyidSerializer
from salescustomer.models.Salescustomer_model import SalesCustomer
from company.models import Company
from coa.models import COA
from transaction.models import MasterTransaction
from item.models.item_model import Item
from item.models.stock_model import Stock
from salescustomer.models.Pr_model import PR
from transaction.serializers import MasterTransactionSerializer
from salescustomer.models.Creditnote_model import CreditNote
from utility import save_attach_file
from salescustomer.printing.generate_ca import generate_customer_advance_pdf
from banking.serializers.refund_master_serializers import Refund_Serializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from salescustomer.serializers.Salescustomer_serializers import SalesCustomerSerializer
from banking.serializers.customer_advance_serializers import UpdateCustomerAdvanceSerializer
from django.db import transaction
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
# New Customer Advanced refund  from
from salescustomer.printing.generate_ca import generate_customer_advance_pdf

class CustomerAdvanceUpdateView(APIView):

    @transaction.atomic
    def put(self,request,pk):
        ca = CustomerAdvance.objects.select_for_update().get(ca_id=pk)
        data = request.data
        serializer = UpdateCustomerAdvanceSerializer(ca,data=data)
        if serializer.is_valid():
            customer_id = data["customer_id"]
            if customer_id is not None:
                customer_id = SalesCustomer.objects.get(customer_id=customer_id)
            # bank_id=ca_data['bank_id'],
            ca.coa_id = COA.objects.get(coa_id=data['deposit_to'])
            ca.ustomer_id = customer_id
            ca.is_customer_advance_generated = data['is_customer_advance_generated']
            ca.customer_advance_date = data['customer_advance_date']
            ca.supply_place = data["supply_place"]
            ca.amount_received = data["amount_received"]
            ca.received_via = data['payment_mode']
            ca.customer_advance_ref_no = data["payment_ref_no"]
            ca.balance_amount = data["amount_received"]
            ca.status = "Manually Added"
            ca.description_supply = data["dec_supply_place"]
            ca.bank_charges = data["bank_charges"]
            ca.payment_serial = data["payment_serial"]
            ca.cgst_amount = data["cgst_amount"]
            ca.sgst_amount = data["sgst_amount"]
            ca.igst_amount = data['igst_amount']
            ca.tax_rate = data["tax_rate"]
            ca.tax_name = data["tax_name"]
            ca.tax_type = data["tax_type"]
            ca.save()
        else:
            return Response(status=400)
        branch_id = data["branch_id"]
        if branch_id is not None:
            branch_id = Branch.objects.get(branch_id=branch_id)

        company_id = data["company_id"]
        if company_id is not None:
            company_id = Company.objects.get(company_id=company_id)



        customer_id = data["customer_id"]
        if customer_id is not None:
            customer_id = SalesCustomer.objects.get(customer_id=customer_id)

        party_account = data.get('party_account', None)
        try:
            account_receivable = COA.objects.get(coa_id=party_account)
        except:
            if customer_id:
                account_receivable = customer_id.coa_id
            else:
                account_receivable = COA.get_account_recievables(company_id)
        MasterTransaction.objects.filter(L1detail_id=pk).delete()
        if data['bank_charges'] is not None and float(data['bank_charges']) > 0:
                # transaction_list.append(["Bank Fees and Charges","bank_charges"])
            TO_COA = account_receivable
            From_Bank = COA.get_bank_fees_account(company_id)
            print('QQQ', From_Bank)
            cabmast = MasterTransaction.objects.create(
                    L1detail_id=pk,
                    L1detailstbl_name='Customer Advance',
                    L2detail_id=From_Bank.coa_id,
                    L2detailstbl_name='BANK',
                    main_module='Sales',
                    module='MonenyIN',
                    trans_status='Manually Added',
                    sub_module='Customer Advanced',
                    transc_deatils='Customer Advanced',
                    banking_module_type=data["transaction_type"],
                    journal_module_type=data["transaction_type"],
                    trans_date=data["customer_advance_date"],
                    credit=data["bank_charges"],
                    to_account=From_Bank.coa_id,
                    to_acc_type=From_Bank.account_type,
                    to_acc_head=From_Bank.account_head,
                    to_acc_subhead=From_Bank.account_subhead,
                    to_acc_name=From_Bank.account_name,
                    debit=data['bank_charges'],
                    from_account=TO_COA.coa_id,
                    from_acc_type=TO_COA.account_type,
                    from_acc_head=TO_COA.account_head,
                    from_acc_subhead=TO_COA.account_head,
                    from_acc_name=TO_COA.account_name,
                    company_id=company_id,
                    customer_id=customer_id,
                    branch_id=branch_id)
            cabmast.save()

            # region MasterTransaction Section

            # In case of with tax =0  so with tax= amount_received
        with_tax = data['with_tax']
        if with_tax == 0:
            with_tax = data['amount_received']

        From_COA = COA.objects.get(company_id=company_id, coa_id=data['deposit_to'])
        TO_COA = account_receivable

        camast = MasterTransaction.objects.create(
            L1detail_id=pk,
            L1detailstbl_name='Customer Advance',
            L2detail_id=From_COA.coa_id,
            L2detailstbl_name='BANK',
            main_module='Banking',
            module='MonenyIN',
            trans_status='Manually Added',
            sub_module='Customer Advanced',
            transc_deatils='Customer Advanced',
            banking_module_type=data["transaction_type"],
            journal_module_type=data["transaction_type"],
            trans_date=data["customer_advance_date"],
            credit=with_tax,
            to_account=From_COA.coa_id,
            to_acc_type=From_COA.account_type,
            to_acc_head=From_COA.account_head,
            to_acc_subhead=From_COA.account_subhead,
            to_acc_name=From_COA.account_name,
            debit=with_tax,
            from_account=TO_COA.coa_id,
            from_acc_type=TO_COA.account_type,
            from_acc_head=TO_COA.account_head,
            from_acc_subhead=TO_COA.account_subhead,  # commited by Shubham 24FEB2023
            from_acc_name=TO_COA.account_name,
            company_id=company_id,
            customer_id=customer_id,
            branch_id=branch_id)
        camast.save()
        #  %0 taxtion Section
        Zero_tax = data
        GST_TAX = None
        GST_TAX = Zero_tax

        if GST_TAX == Zero_tax is not None:
            GST_TAX = Zero_tax.get('tax_name')
        else:
            pass

        IGST_TAX = GST_TAX
        if GST_TAX == 'GST0 [0%]':
            Both_Tax = GST_TAX

        else:
            Both_Tax = None

        if IGST_TAX == 'IGST0 [0%]':
            IGST_0 = IGST_TAX
        else:
            IGST_0 = None

        # User Can the Send the data in request the this data added in this empty list and
        # this list can perform the operation
        # all the values are not equal to zero the added the list
        # list added item to add the master transaction table
        # chnges of this transaction debit credit and to from account
        transaction_list = []  # This Empty List added the append

        if float(data['cgst_amount']) > 0 :
            cgst_account = data.get('cgst_account', None)
            if cgst_account:
                account = COA.objects.get(coa_id=cgst_account)
            else:
                account = COA.get_output_cgst_account(company_id)
            transaction_list.append([account, "cgst_amount"], )
        if float(data['sgst_amount']) > 0 :
            sgst_account = data.get('sgst_account', None)
            if sgst_account:
                account = COA.objects.get(coa_id=sgst_account)
            else:
                account = COA.get_output_sgst_account(company_id)
            transaction_list.append([account, "sgst_amount"])
        if float(data['igst_amount']) > 0 :
            igst_account = data.get('igst_account', None)
            if igst_account:
                account = COA.objects.get(coa_id=igst_account)
            else:
                account = COA.get_output_igst_account(company_id)
            transaction_list.append([account, "igst_amount"], )
        for transaction in transaction_list:
            # List Of index added 0 is get Account_name
            From_COA = transaction[0]
            # Transaction Time to you TO_COA will account Subhead
            TO_COA = COA.objects.get(company_id=company_id, coa_id=data['deposit_to'])

            camast = MasterTransaction.objects.create(
                L1detail_id=pk,
                L1detailstbl_name='Customer Advance',
                L2detail_id=From_COA.coa_id,
                L2detailstbl_name='COA',
                main_module='Sales',
                module='Refund',
                sub_module='Customer Advanced',
                transc_deatils='Customer Advanced',
                banking_module_type=data["transaction_type"],
                journal_module_type=data["transaction_type"],
                trans_date=data["customer_advance_date"],
                trans_status='Manually Added',
                debit=data[transaction[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=data[transaction[1]],
                from_account=From_COA.coa_id,
                from_acc_type=From_COA.account_type,
                from_acc_head=From_COA.account_head,
                from_acc_subhead=From_COA.account_subhead,
                from_acc_name=From_COA.account_name,
                company_id=company_id,
                branch_id=branch_id,
                customer_id=customer_id)
            camast.save()

        # endregion End Master Transaction Section

        return Response(status=200)


class SalesCustomerAdvanceViewsets(viewsets.ModelViewSet):
    queryset =CustomerAdvance.objects.all()
    serializer_class =CustomerAdvancedSerializer

    
    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction


    def ValidateDefaults(obj):
        SalesCustomerAdvanceViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            SalesCustomerAdvanceViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            SalesCustomerAdvanceViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            SalesCustomerAdvanceViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue



    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ca_data_converte= request.data['data']

        print("#################################################")
        print(ca_data_converte)
        print("Customer Format is ",type(ca_data_converte))
        print("#################################################")
        ca_data = json.loads(ca_data_converte)
        #print("Converted Format is",type(ca_data))
        #ca_data=ca_data_converte
        ca_file_data=request.FILES.get('attach_file')
        print("ca_data",type(ca_file_data))

        # GET coa_deposit_toid in Banking and Pass the bank_id Transaction Table and Main Details Table
        # bank=ca_data["deposit_to"]
        # From_Bank=Banking.objects.get(coa_id=bank)


        if(SalesCustomerAdvanceViewsets.ValidateDefaults(ca_data)==False):
            print(" Ooops!!! Error Occured ",SalesCustomerAdvanceViewsets.logger)
        
        print(ca_data)


        #Branch and company null value

        branch_id=ca_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=ca_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        customer_id=ca_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)

        serializer = UpdateCustomerAdvanceSerializer(data=ca_data)
        if serializer.is_valid():
            caed_id = serializer.save()
            caed_id.received_via = ca_data['payment_mode']
            caed_id.save()
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=400)
        #Creating Customer Advance


        party_account = ca_data.get('party_account', None)
        try:
            account_receivable = COA.objects.get(coa_id=party_account)
        except:
            if customer_id:
                account_receivable = customer_id.coa_id
            else:
                account_receivable = COA.get_account_recievables(company_id)
         
        #Bank Chnarges Section
        if ca_data['bank_charges'] is not None and float(ca_data['bank_charges']) >0:
            # transaction_list.append(["Bank Fees and Charges","bank_charges"]) 
            TO_COA= account_receivable
            From_Bank = COA.objects.get(company_id=company_id,account_name="Bank Fees and Charges")
            print('QQQ',From_Bank)
            cabmast=MasterTransaction.objects.create(
            L1detail_id=caed_id.ca_id,
            L1detailstbl_name='Customer Advance',
            L2detail_id=From_Bank.coa_id,
            L2detailstbl_name='BANK',
            main_module='Sales',
            module='MonenyIN',
            trans_status='Manually Added',
            sub_module='Customer Advanced',
            transc_deatils='Customer Advanced',
            banking_module_type=ca_data["transaction_type"],
            journal_module_type=ca_data["transaction_type"],
            trans_date=ca_data["customer_advance_date"],
            credit=ca_data["bank_charges"],
            to_account=From_Bank.coa_id,
            to_acc_type=From_Bank.account_type,
            to_acc_head=From_Bank.account_head,
            to_acc_subhead=From_Bank.account_subhead,
            to_acc_name=From_Bank.account_name,
            debit=ca_data['bank_charges'],
            from_account=TO_COA.coa_id,
            from_acc_type=TO_COA.account_type,
            from_acc_head=TO_COA.account_head,
            from_acc_subhead=TO_COA.account_head,
            from_acc_name=TO_COA.account_name,
            company_id=company_id,
            customer_id=customer_id,
            branch_id=branch_id)
            cabmast.save()


#region MasterTransaction Section
        
        #In case of with tax =0  so with tax= amount_received
        with_tax=ca_data['with_tax']
        if with_tax==0:
            with_tax=ca_data['amount_received']
        
        From_COA= COA.objects.get(company_id=company_id,coa_id=ca_data['deposit_to']) 
        TO_COA= COA.objects.get(company_id=company_id,account_subhead="Account Receivables",isdefault=True)
        camast=MasterTransaction.objects.create(
        L1detail_id=caed_id.ca_id,
        L1detailstbl_name='Customer Advance',
        L2detail_id=From_COA.coa_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyIN',
        trans_status='Manually Added',
        sub_module='Customer Advanced',
        transc_deatils='Customer Advanced',
        banking_module_type=ca_data["transaction_type"],
        journal_module_type=ca_data["transaction_type"],
        trans_date=ca_data["customer_advance_date"],
        credit=with_tax,
        to_account=From_COA.coa_id,
        to_acc_type=From_COA.account_type,
        to_acc_head=From_COA.account_head,
        to_acc_subhead=From_COA.account_subhead,
        to_acc_name=From_COA.account_name,
        debit=with_tax,
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_subhead,#commited by Shubham 24FEB2023
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        customer_id=customer_id,
        branch_id=branch_id)
        camast.save()
       #  %0 taxtion Section
        Zero_tax=ca_data
        GST_TAX=None
        GST_TAX=Zero_tax
        
        if GST_TAX==Zero_tax is not None:
            GST_TAX=Zero_tax.get('tax_name')
        else:
            pass

        IGST_TAX=GST_TAX
        if GST_TAX=='GST0 [0%]':
            Both_Tax=GST_TAX   
            
        else:
            Both_Tax=None
           
        if IGST_TAX=='IGST0 [0%]':
            IGST_0=IGST_TAX
        else:
            IGST_0=None
             
            

        transaction_list = [] #This Empty List added the append

        if float(ca_data['cgst_amount']) > 0:
            cgst_account = ca_data.get('cgst_account', None)
            if cgst_account:
                account = COA.objects.get(coa_id=cgst_account)
            else:
                account = COA.get_output_cgst_account(company_id)
            transaction_list.append([account, "cgst_amount"], )
        if float(ca_data['sgst_amount']) > 0 :
            sgst_account = ca_data.get('sgst_account', None)
            if sgst_account:
                account = COA.objects.get(coa_id=sgst_account)
            else:
                account = COA.get_output_sgst_account(company_id)
            transaction_list.append([account, "sgst_amount"])
        if float(ca_data['igst_amount']) > 0 :
            igst_account = ca_data.get('igst_account', None)
            if igst_account:
                account = COA.objects.get(coa_id=igst_account)
            else:
                account = COA.get_output_igst_account(company_id)
            transaction_list.append([account, "igst_amount"], )
        for transaction in transaction_list:
            
            #List Of index added 0 is get Account_name
            From_COA = transaction[0]
            #Transaction Time to you TO_COA will account Subhead
            TO_COA=COA.objects.get(company_id=company_id,coa_id=ca_data['deposit_to']) 

            camast = MasterTransaction.objects.create(
                L1detail_id=caed_id.ca_id,
                L1detailstbl_name='Customer Advance',
                L2detail_id=From_COA.coa_id,
                L2detailstbl_name='COA',
                main_module='Sales',
                module='Refund',
                sub_module='Customer Advanced',
                transc_deatils='Customer Advanced',
                banking_module_type=ca_data["transaction_type"],
                journal_module_type=ca_data["transaction_type"],
                trans_date=ca_data["customer_advance_date"],
                trans_status='Manually Added',
                debit=ca_data[transaction[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=ca_data[transaction[1]],
                from_account=From_COA.coa_id,
                from_acc_type=From_COA.account_type,
                from_acc_head=From_COA.account_head,
                from_acc_subhead=From_COA.account_subhead,
                from_acc_name=From_COA.account_name,
                company_id=company_id,
                customer_id=customer_id)
            camast.save()
        
        
             
        
#endregion End Master Transaction Section
        serializer = CustomerAdvancedSerializer(caed_id)
        return Response(serializer.data)

#Sales Customer Advanced Refund Journal Transaction

n_data=None
@api_view(['GET'])


def getCARJournalTransaction(self,ca_id):
    form_mast = MasterTransaction.objects.filter(L1detail_id=ca_id)
    df = pd.DataFrame(form_mast.values('to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                        'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit'))
    print(df)
    from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name',]).agg(
        {'credit': 'sum'}).reset_index()
    to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',]).agg(
        { 'debit': 'sum'}).reset_index()
    from_acc = from_acc.rename(columns={
                                'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name'}, inplace=False)
    to_acc = to_acc.rename(columns={
                            'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name'}, inplace=False)


    df_accounts = pd.concat([from_acc, to_acc])
    response = json.loads(df_accounts.to_json(orient='records'))

    serializer = MasterTransactionSerializer(form_mast, many=True)
    n_data=serializer.data
    all_response = {
            # 'original_data': account_type_list,
            'form_data': n_data,
            'transaction': response,
        }
    return Response(all_response)


# api for get bill by company id and bill id
@api_view(['GET'])

def download_carf_data(request, ca_id):
    ca = CustomerAdvance.objects.get(ca_id=ca_id)

    serializers =CustomerAdvancedSerializer(ca)

    output_pdf = f"PR_{datetime.datetime.now().timestamp()}.pdf"
    html = generate_customer_advance_pdf(data=serializers.data)

    return html





def download_carf(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response
class CustomerAdvGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = CustomerAdvance.objects.all()
    serializer_class = CustomerAdvancedSerializer

    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data
            return_data['attach_file'] = 'salescustomer/carffile_download/{}/'.format(
                pk)
            return Response({
                'data': return_data
            })
        return self.list(request)

class CARFFileDownloadListAPIView(generics.ListAPIView):
    
    def get(self, request, ca_id, format=None):
        queryset = CustomerAdvance.objects.get(ca_id=ca_id)
        if queryset.attach_file:
            file_handle = queryset.attach_file.path
            if os.path.exists(file_handle):
                document = open(file_handle, 'rb')
                response = HttpResponse(FileWrapper(
                    document), content_type='application/msword')
                response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
                return response
            else:
                response = HttpResponse("File Not Found")
        else:
            return HttpResponse('File not Found in Model')



#Sales Credit Note refunfd from

class SalesCNRefundModelViewSets(viewsets.ModelViewSet):
    queryset=RefundMaster.objects.all()
    serializer_class=Refund_Serializer

    
    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        SalesCNRefundModelViewSets.logger=[]
        ## Validation Section

        company_id=obj["company_id"]
        customer_id=obj["customer_id"]
        cn_id=obj["cn_id"]
        retValue=True
        if customer_id is None:
            SalesCNRefundModelViewSets.logger.append("Customer iD is Null Please Provide a Customer ID")
            retValue= False        
           
        if(company_id is  None ):
            SalesCNRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            SalesCNRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False
        if(type(cn_id!=uuid)):
            SalesCNRefundModelViewSets.logger.append("creditnote ID is not a Valid UUID Please Provide a valid creditnote ID ")
            retValue= False 

        return retValue

    def create(self, request, *args, **kwargs):
        Cnrefund_data = request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        # bank=Cnrefund_data["coa_id"]
        # From_Bank=Banking.objects.get(coa_id=bank)


        if(SalesCNRefundModelViewSets.ValidateDefaults(Cnrefund_data)==False):
            print(" Ooops!!! Error Occured ",SalesCNRefundModelViewSets.logger)
            
        print(Cnrefund_data)
            #What if this ID is null , 

    
        company_id=Cnrefund_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
        
        customer_id=Cnrefund_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)

        creditnote_id=Cnrefund_data["cn_id"]
        print("cnid",creditnote_id,type(creditnote_id))

        cnrefund_id=RefundMaster.objects.create(
            company_id=company_id,
            bank_id=Cnrefund_data["bank_id"],
            customer_id=customer_id,
            refrence_id=creditnote_id,
            coa_id=COA.objects.get(coa_id=Cnrefund_data["coa_id"]),
            refund_date=Cnrefund_data["refund_on"],
            is_cn_refund_generated=Cnrefund_data["is_cn_refund_generated"],
            status=Cnrefund_data["status"],
            refund_ref_no=Cnrefund_data["refund_ref_no"],
            refund_balance_amount=Cnrefund_data["refund_balance_amount"],
            amount=Cnrefund_data["amount"],
            serial_ref=Cnrefund_data["cn_serial"],
            amount_ref=Cnrefund_data["cn_amount"],
            payment_mode=Cnrefund_data["payment_mode"],
            description=Cnrefund_data["description"])
        cnrefund_id.save()
        print("Cnrefund_created",cnrefund_id,type(cnrefund_id))



        
#region Master Transaction Section

        TO_COA =COA.objects.get(company_id=company_id,account_name="Account Receivables",isdefault=True)
        From_COA=COA.objects.get(company_id=company_id,coa_id=Cnrefund_data["coa_id"])
        print('""""""""""""',TO_COA)  
        CNRmast=MasterTransaction.objects.create(
        L1detail_id=cnrefund_id.rm_id,
        L1detailstbl_name='RefundMaster',
        L2detail_id=From_COA.coa_id,
        L2detailstbl_name='COA',
        L3detail_id=creditnote_id,
        L3detailstbl_name='Credit Note',
        main_module='Sales',
        module='Refund',
        sub_module='CreditNoteRefund',
        transc_deatils='Credit Note Refund',
        banking_module_type=Cnrefund_data["transaction_module"],
        journal_module_type='Refund',
        trans_date=Cnrefund_data["refund_on"],
        trans_status=Cnrefund_data["status"],
        debit=Cnrefund_data["entered_amount"],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=Cnrefund_data['amount'],
        from_account=From_COA.coa_id,        
        from_acc_type=From_COA.account_type,
        from_acc_head=From_COA.account_head,
        from_acc_subhead=From_COA.account_subhead,
        from_acc_name=From_COA.account_name,
        company_id=company_id,
        customer_id=customer_id)
        
        CNRmast.save() 

#endregion

#End Master Transaction Section Credit Note refund

        cn_id=Cnrefund_data["cn_id"]
        if cn_id is not None:
            cn_id=CreditNote.objects.get(cn_id=cn_id)

            balance_amount=Cnrefund_data["refund_balance_amount"]
            print("Amount values are",balance_amount,type(balance_amount))
            if balance_amount == 0:
            # cn_id =cn_id      
                print('cn_id', cn_id)              
                cn_id.status='Closed'
                cn_id.cn_status='Closed'
                cn_id.balance_amount= Cnrefund_data["refund_balance_amount"]
                cn_id.save()
                print('creditnote status updated to ', cn_id.status)
           
            elif balance_amount >= 0:
            # cn_id = cn_id
                print('credit note id of else', cn_id)
                cn_id.balance_amount= Cnrefund_data["refund_balance_amount"]            
                cn_id.save()       
                print('credinote amount due updated to ', cn_id.balance_amount)
            else:
            # cn_id =cn_id      
                print('cn_id', cn_id)              
                cn_id.status='open'
                cn_id.save()
                print('creditnote status updated to ', cn_id.status)
        
        
        serializer =Refund_Serializer(cnrefund_id)
        return Response(serializer.data)
 
 
        
############# GENERATE CUSTOMER ADVANCED PDF AND DOWNLOAD ##############################
@api_view(['GET'])

   
def download_customer_advanced_data(request, comp_id,ca_id):
    company = Company.objects.get(company_id=comp_id)
    ca = CustomerAdvance.objects.get(ca_id=ca_id)
    # here filter the object of bill id and company id
    carecieved = CustomerAdvance.objects.filter(
        company_id=comp_id,ca_id=ca_id).order_by('customer_advance_date')
    
    serializers =CustomerAdvancedSerializer(carecieved, many=True)


    html = generate_customer_advance_pdf(data=serializers.data)
    
    return html

def download_ca(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'), as_attachment=True)
   # response = FileResponse(open(file_path, 'rb'), as_attachment=True)   
    #response = FileResponse(file_data, as_attachment=True,                              
    return response
################################################################################
@api_view(['GET'])


def getPRAdvDetailsByPR_number(request, payment_serial, company_id,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    cas = CustomerAdvance.objects.filter(company_id=company_id,
                                         branch_id=branch_id,
                                         payment_serial__icontains=payment_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": cas.count()}

    instance = cas[offset:offset + limit]
    serializer = GetCustomerShortBy_CompanyidSerializer(instance, many=True)

    response['results'] = serializer.data
    return Response(response)


@api_view(['GET'])


def getPRAdvshortbyCustomer_name(request, customer_name, company_id,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    cas = CustomerAdvance.objects.filter(company_id=company_id,
                                         branch_id=branch_id,
                                         customer_id__customer_name__icontains=customer_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": cas.count()}

    instance = cas[offset:offset + limit]

    serializer = GetCustomerShortBy_CompanyidSerializer(instance, many=True)

    response['results'] = serializer.data
    return Response(response)
#Sales Customer Advanced refund
@api_view(['GET'])


def carefundshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": CustomerAdvance.objects.filter(company_id=comp_id,branch_id=branch_id).count()
    }

    # Get the company object by comp_id and apply pagination
    try:
        company = Company.objects.get(company_id=comp_id)
        items = CustomerAdvance.objects.filter(company_id=company,branch_id=branch_id)[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = GetCustomerShortBy_CompanyidSerializer(items, many=True).data
    return Response(response)
    
#Customer Advanced By Ca Id Wise
@api_view(['GET'])


def salescabyid(request, ca_id):
    ca = CustomerAdvance.objects.filter(ca_id=ca_id)
    serializer = CustomerAdvSerializer(ca, many=True)
    return Response(serializer.data)



# Get search details by payment serial
@api_view(['GET'])

#
def getCADetailsBypm_serial(request, payment_serial):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": CustomerAdvance.objects.count()}
    
    instance = CustomerAdvance.objects.filter(payment_serial__icontains=payment_serial)[offset:offset + limit]
    serializer = CustomerAdvancedSerializer(instance, many=True)
    
    response['results'] = CustomerAdvancedSerializer(instance, many=True).data
    return Response(response)




#getitemshortbycompanyid
@api_view(['GET'])

#
def getCAhortbyCustomer_name(request,customer_name,company_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    credits = CreditNote.objects.filter(company_id=company_id,customer_id__customer_name__icontains=customer_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": SalesCustomer.objects.count()}
    
    instance = credits[offset:offset + limit]
    
    serializer = SalesCustomerSerializer(instance, many=True)
   # return Response(serializer.data)

    if serializer.data:
        customer_id = serializer.data[0].get('customer_id')
        print("Estimate data is **********************", customer_id)
        coa = CustomerAdvance.objects.filter(customer_id=customer_id)
    else:
        # Handle the case where there are no instances in the list
        coa = None  # You may want to handle this differently based on your use case
    serializer = CustomerAdvancedSerializer(coa, many=True)
    
    response['results'] = CustomerAdvancedSerializer(coa, many=True).data
    return Response(response)