import json
import os
import uuid
from pathlib import Path
from django.views.generic import View
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import api_view
from banking.models import VendorAdvanced
from banking.serializers import VendorAdvancedSerializer,ForPaginationVendorAdvancedSerializer,UpdateVendorAdvanceSerializer
from company.models import Company,Branch
from purchase.models.Tds_model import TDS
from purchase.models.Vendor_model import Vendor
from coa.models import COA
from transaction.models import MasterTransaction
import pandas as pd
import datetime
from wsgiref.util import FileWrapper
from django.http import HttpResponse, FileResponse
from purchase.printing.generate_va import generate_vendor_advance_pdf
from transaction.serializers import MasterTransactionSerializer
from audit.models import Audit
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.db import transaction
from rest_framework.views import APIView
#Vendor Advanced Refund Transaction Section 
#region  
class Vendor_AdvancedRefundModelViewSets(viewsets.ModelViewSet):
    queryset=VendorAdvanced.objects.all()
    serializer_class=VendorAdvancedSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        Vendor_AdvancedRefundModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            Vendor_AdvancedRefundModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            Vendor_AdvancedRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            Vendor_AdvancedRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        vendor_advanced_data = request.data['data']
        vendor_advanced_data = json.loads(vendor_advanced_data)
        user= request.user

        va_file_data=request.FILES.get('attach_file')
        if(Vendor_AdvancedRefundModelViewSets.ValidateDefaults(vendor_advanced_data)==False):
            print(" Ooops!!! Error Occured ",Vendor_AdvancedRefundModelViewSets.logger)
        
        print(vendor_advanced_data)
        va_file_data = request.FILES.get('attach_file')
        branch_id=vendor_advanced_data["branch_id"]
        branch_id = Branch.objects.get(branch_id=branch_id)


        company_id=vendor_advanced_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
        
        vendor_id=vendor_advanced_data["vendor_id"]
        if vendor_id is not None:
            vendor_id=Vendor.objects.get(vendor_id=vendor_id)
            

        SAL_TAX=None   
        Zero_tax=vendor_advanced_data.get('tax_name')
        if Zero_tax is not None:
            SAL_TAX=Zero_tax
        serializer =  UpdateVendorAdvanceSerializer(data=vendor_advanced_data)
        if serializer.is_valid():
            va_id = serializer.save()
            if va_file_data:
                va_id.attach_file = va_file_data
            va_id.amount = vendor_advanced_data.get('amount_payable',0)
            va_id.save()
        else:
            print(serializer.erros)
            return Response(serializer.errors,status=400)


        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=vendor_advanced_data["vendor_advance_date"],
            module="VendorAdvanced",
            sub_module='VendorAdvanced',
            data=vendor_advanced_data
        )
        party_account = vendor_advanced_data.get('party_account', None)
        try:
            account_payables = COA.objects.get(coa_id=party_account)
        except:
            if vendor_id:
                account_payables = vendor_id.coa_id
            else:
                account_payables = COA.get_account_paybles(company_id)

        TO_COA= account_payables
        From_COA=COA.objects.get(company_id=company_id,coa_id=vendor_advanced_data["deposit_to"])

        vamast=MasterTransaction.objects.create(
        L1detail_id=va_id.va_id,
        L1detailstbl_name='VendorAdvanced',
        L2detail_id=From_COA.coa_id,
        L2detailstbl_name='COA',
        main_module='Purchase',
        module='Refund',
        sub_module='VendorAdvanced',
        transc_deatils='Vendor Advanced',
        banking_module_type=vendor_advanced_data["transaction_module"],
        journal_module_type=vendor_advanced_data["transaction_module"],
        trans_date=vendor_advanced_data["vendor_advance_date"],
        trans_status=vendor_advanced_data["status"],
        debit=vendor_advanced_data['amount_payable'],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=vendor_advanced_data['amount_payable'],
        from_account=From_COA.coa_id,        
        from_acc_type=From_COA.account_type,
        from_acc_head=From_COA.account_head,
        from_acc_subhead=From_COA.account_subhead,
        from_acc_name=From_COA.account_name,
        company_id=company_id,
        vendor_id=vendor_id,
        branch_id=branch_id)
        vamast.save()
        print('@@@@@@',vamast)
        
        Zero_tax=vendor_advanced_data
        GST_TAX=vendor_advanced_data['tax_name']
        
        if GST_TAX is not None:
            GST_TAX=GST_TAX
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
             
            
        
        # User Can the Send the data in request the this data added in this empty list and 
        #this list can perform the operation 
        # all the values are not equal to zero the added the list
        #list added item to add the master transaction table
        #chnges of this transaction debit credit and to from account
        transaction_list = [] #This Empty List added the append
        
        if float(vendor_advanced_data['tds_amount'])>0:
            tds_account = vendor_advanced_data.get('tds_account', None)
            if tds_account:
                account = COA.objects.get(coa_id=tds_account)
            else:
                account = COA.get_input_tcs_pay_account(company_id)
            transaction_list.append([account,"tds_amount"])
        
        for transaction in transaction_list :
            FORM_COA = transaction[0]
            TO_COA= account_payables

            MasterTransaction.objects.create(
            L1detail_id=va_id.va_id,
            L1detailstbl_name='VendorAdvanced',
            main_module='Purchase',
            module='Refund',
            sub_module='VendorAdvanced',
            transc_deatils='Vendor Advanced',
            banking_module_type=vendor_advanced_data["transaction_module"],
            journal_module_type=vendor_advanced_data["transaction_module"],
            trans_date=vendor_advanced_data["vendor_advance_date"],
            trans_status=vendor_advanced_data["status"],
            debit=vendor_advanced_data[transaction[1]],
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=vendor_advanced_data[transaction[1]],
            from_account=FORM_COA.coa_id,        
            from_acc_type=FORM_COA.account_type,
            from_acc_head=FORM_COA.account_head,
            from_acc_subhead=FORM_COA.account_subhead,
            from_acc_name=FORM_COA.account_name,
            company_id=company_id,
            vendor_id=vendor_id,
            branch_id=branch_id)

        # UI side to select the reverse charge to implement     
        if vendor_advanced_data['reverse_charge'] == True:
            tax_transaction_list=[]
        else:
            tax_transaction_list=[]
                
        # taxtion Section 
        if float(vendor_advanced_data['cgst_amount']) > 0:
            cgst_account = vendor_advanced_data.get('cgst_account', None)
            if cgst_account:
                account = COA.objects.get(coa_id=cgst_account)
            else:
                account = COA.get_output_cgst_account(company_id)
            transaction_list.append([account, "cgst_amount"], )
        if float(vendor_advanced_data['sgst_amount']) > 0:
            sgst_account = vendor_advanced_data.get('sgst_account', None)
            if sgst_account:
                account = COA.objects.get(coa_id=sgst_account)
            else:
                account = COA.get_output_sgst_account(company_id)
            transaction_list.append([account, "sgst_amount"])
        if float(vendor_advanced_data['igst_amount']) > 0:
            igst_account = vendor_advanced_data.get('igst_account', None)
            if igst_account:
                account = COA.objects.get(coa_id=igst_account)
            else:
                account = COA.get_output_igst_account(company_id)
            transaction_list.append([account, "igst_amount"], )
        for transaction_tax in tax_transaction_list :   
            FORM_COA = transaction_tax[0]
            TO_COA= COA.objects.get(company_id=company_id,account_name= 'Tax Paid Expense',system=True)

            MasterTransaction.objects.create(
            L1detail_id=va_id.va_id,
            L1detailstbl_name='VendorAdvanced',
            main_module='Purchase',
            module='Refund',
            sub_module='VendorAdvanced',
            transc_deatils='Vendor Advanced',
            banking_module_type=vendor_advanced_data["transaction_module"],
            journal_module_type=vendor_advanced_data["transaction_module"],
            trans_date=vendor_advanced_data["vendor_advance_date"],
            trans_status=vendor_advanced_data["status"],
            debit=vendor_advanced_data[transaction_tax[1]],
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=vendor_advanced_data[transaction_tax[1]],
            from_account=FORM_COA.coa_id,        
            from_acc_type=FORM_COA.account_type,
            from_acc_head=FORM_COA.account_head,
            from_acc_subhead=FORM_COA.account_subhead,
            from_acc_name=FORM_COA.account_name,
            company_id=company_id,
            vendor_id=vendor_id,
            branch_id=branch_id)
            vamast.save()



        serializer =VendorAdvancedSerializer(va_id)         
        return Response(serializer.data)

class VendorAdvanceUpdateView(APIView):

    @transaction.atomic
    def put(self,request,pk):
        va = VendorAdvanced.objects.select_for_update().get(va_id
                                                            =pk)
        user = request.user
        vendor_advanced_data = request.data
        print(type(vendor_advanced_data['is_vendor_advance_generated']),"boolean")
        serializer = UpdateVendorAdvanceSerializer(va,data=vendor_advanced_data)
        branch_id = vendor_advanced_data["branch_id"]
        branch_id = Branch.objects.get(branch_id=branch_id)
        company_id = vendor_advanced_data["company_id"]
        if company_id is not None:
            company_id = Company.objects.get(company_id=company_id)
        vendor_id = vendor_advanced_data["vendor_id"]
        if vendor_id is not None:
            vendor_id = Vendor.objects.get(vendor_id=vendor_id)
        # coa_id = vendor_advanced_data["deposit_to"]
        # if coa_id is not None:
        #     coa_id = COA.objects.get(coa_id=coa_id)
        # tds_id = vendor_advanced_data.get("tds_id")
        # if tds_id is not None:
        #     tds_id = TDS.objects.get(tds_id=tds_id)
        SAL_TAX = None
        Zero_tax = vendor_advanced_data.get('tax_name')
        if Zero_tax is not None:
            SAL_TAX = Zero_tax
        if serializer.is_valid():
           va = serializer.save()
           va.amount = vendor_advanced_data.get('amount_payable', 0)
           va.save()
        else:
            return Response(status=400)

        party_account = vendor_advanced_data.get('party_account', None)
        try:
            account_payables = COA.objects.get(coa_id=party_account)
        except:
            if vendor_id:
                account_payables = vendor_id.coa_id
            else:
                account_payables = COA.get_account_paybles(company_id)

        TO_COA = account_payables
        From_COA = COA.objects.get(company_id=company_id, coa_id=vendor_advanced_data["deposit_to"])

        MasterTransaction.objects.select_for_update().filter(L1detail_id=pk).delete()
        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            modified_by=user,
            audit_modified_date=vendor_advanced_data["vendor_advance_date"],
            module="VendorAdvanced",
            sub_module='VendorAdvanced',
            data=vendor_advanced_data
        )
        vamast = MasterTransaction.objects.create(
            L1detail_id=va.va_id,
            L1detailstbl_name='VendorAdvanced',
            L2detail_id=From_COA.coa_id,
            L2detailstbl_name='COA',
            main_module='Purchase',
            module='Refund',
            sub_module='VendorAdvanced',
            transc_deatils='Vendor Advanced',
            banking_module_type=vendor_advanced_data["transaction_module"],
            journal_module_type=vendor_advanced_data["transaction_module"],
            trans_date=vendor_advanced_data["vendor_advance_date"],
            trans_status=vendor_advanced_data["status"],
            debit=vendor_advanced_data['amount_payable'],
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=vendor_advanced_data['amount_payable'],
            from_account=From_COA.coa_id,
            from_acc_type=From_COA.account_type,
            from_acc_head=From_COA.account_head,
            from_acc_subhead=From_COA.account_subhead,
            from_acc_name=From_COA.account_name,
            company_id=company_id,
            vendor_id=vendor_id,
            branch_id=branch_id)
        vamast.save()
        print('@@@@@@', vamast)
        Zero_tax = vendor_advanced_data
        GST_TAX = vendor_advanced_data['tax_name']
        if GST_TAX is not None:
            GST_TAX = GST_TAX
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
        transaction_list = []  # This Empty List added the append

        if float(vendor_advanced_data['tds_amount']) > 0:
            tds_account = vendor_advanced_data.get('tds_account', None)
            if tds_account:
                account = COA.objects.get(coa_id=tds_account)
            else:
                account = COA.get_input_tcs_pay_account(company_id)
            transaction_list.append([account, "tds_amount"])

        for transaction in transaction_list:
            FORM_COA = transaction[0]
            TO_COA = account_payables

            MasterTransaction.objects.create(
                L1detail_id=va.va_id,
                L1detailstbl_name='VendorAdvanced',
                main_module='Purchase',
                module='Refund',
                sub_module='VendorAdvanced',
                transc_deatils='Vendor Advanced',
                banking_module_type=vendor_advanced_data["transaction_module"],
                journal_module_type=vendor_advanced_data["transaction_module"],
                trans_date=vendor_advanced_data["vendor_advance_date"],
                trans_status=vendor_advanced_data["status"],
                debit=vendor_advanced_data[transaction[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=vendor_advanced_data[transaction[1]],
                from_account=FORM_COA.coa_id,
                from_acc_type=FORM_COA.account_type,
                from_acc_head=FORM_COA.account_head,
                from_acc_subhead=FORM_COA.account_subhead,
                from_acc_name=FORM_COA.account_name,
                company_id=company_id,
                vendor_id=vendor_id,
                branch_id=branch_id)
        if vendor_advanced_data['reverse_charge'] == True:
            tax_transaction_list = []
        else:
            tax_transaction_list = []

        # taxtion Section
        if float(vendor_advanced_data['cgst_amount']) > 0:
            cgst_account = vendor_advanced_data.get('cgst_account', None)
            if cgst_account:
                account = COA.objects.get(coa_id=cgst_account)
            else:
                account = COA.get_output_cgst_account(company_id)
            transaction_list.append([account, "cgst_amount"], )
        if float(vendor_advanced_data['sgst_amount']) > 0:
            sgst_account = vendor_advanced_data.get('sgst_account', None)
            if sgst_account:
                account = COA.objects.get(coa_id=sgst_account)
            else:
                account = COA.get_output_sgst_account(company_id)
            transaction_list.append([account, "sgst_amount"])
        if float(vendor_advanced_data['igst_amount']) > 0:
            igst_account = vendor_advanced_data.get('igst_account', None)
            if igst_account:
                account = COA.objects.get(coa_id=igst_account)
            else:
                account = COA.get_output_igst_account(company_id)
            transaction_list.append([account, "igst_amount"], )
        for transaction_tax in tax_transaction_list:
            FORM_COA = transaction_tax[0]
            TO_COA = COA.objects.get(company_id=company_id, account_name='Tax Paid Expense', system=True)

            MasterTransaction.objects.create(
                L1detail_id=va.va_id,
                L1detailstbl_name='VendorAdvanced',
                main_module='Purchase',
                module='Refund',
                sub_module='VendorAdvanced',
                transc_deatils='Vendor Advanced',
                banking_module_type=vendor_advanced_data["transaction_module"],
                journal_module_type=vendor_advanced_data["transaction_module"],
                trans_date=vendor_advanced_data["vendor_advance_date"],
                trans_status=vendor_advanced_data["status"],
                debit=vendor_advanced_data[transaction_tax[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=vendor_advanced_data[transaction_tax[1]],
                from_account=FORM_COA.coa_id,
                from_acc_type=FORM_COA.account_type,
                from_acc_head=FORM_COA.account_head,
                from_acc_subhead=FORM_COA.account_subhead,
                from_acc_name=FORM_COA.account_name,
                company_id=company_id,
                vendor_id=vendor_id,
                branch_id=branch_id)
            vamast.save()

        serializer = VendorAdvancedSerializer(va)
        return Response(serializer.data)
#endregion
#End Vendor Advance Refund 


# Vendor Advanced Journal Transaction Section
#region
#va_id through the fethch the data
n_data=None
@api_view(['GET'])

def getVARJournalTransaction(self,va_id):
    form_mast = MasterTransaction.objects.filter(L1detail_id=va_id)
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
    
#endregion
# Vendor Advanced refund Journal Transactions 

@api_view(['GET'])
#
def varshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    objs = VendorAdvanced.objects.filter(company_id=comp_id,branch_id=branch_id)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": objs.count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        items = objs.order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = ForPaginationVendorAdvancedSerializer(items, many=True).data
    return Response(response)
 

@api_view(['GET'])

def purchasevabyid(request, va_id):
    va = VendorAdvanced.objects.filter(va_id=va_id)
    serializer = VendorAdvancedSerializer(va, many=True)
    return Response(serializer.data)




class VendorAdvGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = VendorAdvanced.objects.all()
    serializer_class = VendorAdvancedSerializer


    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data

            return Response({
                'data': return_data
            })
        return self.list(request)
    
#Vendor Advance Refund file Download    
class VARFFileDownloadListAPIView(generics.ListAPIView):
    
    def get(self, request, va_id, format=None):
        queryset = VendorAdvanced.objects.get(va_id=va_id)
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
                return response
        else:
            return HttpResponse('File not Found in Model')



############# GENERATE VENDOR ADVANCED PDF AND DOWNLOAD ##############################
@api_view(['GET'])

def download_vendor_advanced_data(request, va_id):

    # here filter the object of bill id and company id
    varecieved = VendorAdvanced.objects.get(va_id=va_id)
    
    serializers =VendorAdvancedSerializer(varecieved)

    output_pdf = f"PR_{datetime.datetime.now().timestamp()}.pdf"
    html = generate_vendor_advance_pdf(data=serializers.data,output_path=os.path.join("media", output_pdf))
    
    return html


def download_va(request, file_name):
    file_path = f"media/{file_name}"           
    response = FileResponse(open(file_path,'rb'), as_attachment=True)                              
    return response
################################################################################

# Get search details by payment serial
@api_view(['GET'])

def getVADetailsBypm_serial(request, payment_serial,comp_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    objs = VendorAdvanced.objects.filter(payment_serial__icontains=payment_serial,
                                             company_id=comp_id,branch_id=branch_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": objs.count()}
    
    instance = objs[offset:offset + limit]
    response['results'] = VendorAdvancedSerializer(instance, many=True).data
    return Response(response)


@api_view(['GET'])

def getPMAdvshortbyVendor_name(request, vendor_name, company_id,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    cas = VendorAdvanced.objects.filter(company_id=company_id,
                                        branch_id=branch_id,
                                        vendor_id__vendor_name__icontains=vendor_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": cas.count()}

    instance = cas[offset:offset + limit]

    serializer = VendorAdvancedSerializer(instance, many=True)

    response['results'] = serializer.data
    return Response(response)