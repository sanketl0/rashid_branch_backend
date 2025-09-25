import imp
import json
import os
from wsgiref.util import FileWrapper
import uuid
from django.views.generic import View
from django.http import HttpResponse, FileResponse
from utility import render_to_pdf
from urllib import response
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from purchase.serializers.Expenserecord_serializers import ExpenseRecordSerializer,\
    ExpbankSerializer,UpdTExpenseRecordSerializer,ForPaginationExpenseRecordSerializer,ExpenseRecordSerializerDownload
from salescustomer.models.Salescustomer_model import SalesCustomer
from purchase.models.Expense_Record_model import ExpenseRecord
from purchase.printing.generate_exp import generate_expense_pdf
from company.models import Company,Company_Year,Branch
from purchase.models.Vendor_model import Vendor
from banking.models.banking_model import Banking
from coa.models import COA
from transaction.models import MasterTransaction
from audit.models import Audit
from rest_framework.decorators import api_view, permission_classes,authentication_classes

from rest_framework.parsers import MultiPartParser
from django.db import transaction
from registration.models import Feature
#Expense File Downloaded Section
class ExpenseFileDownloadListAPIView(generics.ListAPIView):
    
    def get(self, request, er_id, format=None):
        queryset = ExpenseRecord.objects.get(er_id=er_id)
        if queryset.attach_file:
            file_handle = queryset.attach_file.path
            if os.path.exists(file_handle):
                document = open(file_handle, 'rb')
                response = HttpResponse(FileWrapper(
                    document), content_type='application/msword')
                response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
                return response
            else:
                return HttpResponse("File Not Found")
        else:
            return HttpResponse("No File Found")


#Estimated Downloaded Pdf path
class EstimateDownloadPdf(View):
    def get(self, request, *args, **kwargs):

        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "estimate_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)

        # rendering the template

        with open(pdf_path, 'r') as f:
            file_data = f.read()

        # sending response
        response = FileResponse(file_data, as_attachment=True,
                                filename='hello.pdf', content_type='application/pdf')
        response['Content-Disposition'] = content
        return response



#Return the Expense Downloaded path
#Class is return the 
class expenserecordList(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = ExpenseRecord.objects.all()
    serializer_class = ExpenseRecordSerializer

    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data
            return Response({
                'data': return_data
            })
        return self.list(request)



#Expense Record Filter by Company id 

@api_view(['GET'])
#
def ershortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": ExpenseRecord.objects.filter(company_id=comp_id,branch_id=branch_id).count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        items = ExpenseRecord.objects.filter(company_id=comp_id,branch_id=branch_id)[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = ForPaginationExpenseRecordSerializer(items, many=True).data
    return Response(response)
       
#This Section is Expense Post

#Expense form For using master transaction
class new3expenserecordViewSet(viewsets.ModelViewSet):
    queryset = ExpenseRecord.objects.all()
    serializer_class = ExpenseRecordSerializer

    parser_classes = [MultiPartParser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        count = Feature.objects.get(user_id=request.user.id).expense_remaining
        user = request.user
        print(count, 'expenses')
        if count <= 0:
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        er_data_converte = request.data['data']
        # =er_data_converte
        # Expense Convert Str to Dict Code
        er_data = json.loads(er_data_converte)

        er_file_data = request.FILES.get('attach_file')
        
        vn_id = er_data["vendor_id"]
        if vn_id is not None:
            vn_id = Vendor.objects.get(vendor_id=vn_id)

        cust_id = er_data["customer_id"]
        if cust_id is not None:
            cust_id = SalesCustomer.objects.get(customer_id=cust_id)



        comp_id = Company.objects.get(company_id=er_data["company_id"])
        branch_id = Branch.objects.get(branch_id=er_data["branch_id"])
        # Expense Record fields
        er_id = ExpenseRecord.objects.create(
            expense_date=er_data["expense_date"],
            # expense_account=er_data["expense_account"],
            coa_id=COA.objects.get(coa_id=er_data["coa_id"]),
            expense_type=er_data["expense_type"],
            amount=er_data["amount"],
            paid_through=er_data["paid_through"],
            invoice_serial=er_data["invoice_serial"],
            expense_serial=er_data["expense_serial"],
            expense_total=er_data["expense_total"],
            sac=er_data["sac"],
            hsn_code=er_data["hsn_code"],
            gst_treatment=er_data["gst_treatment"],
            supply_place=er_data["supply_place"],
            destination_place=er_data["destination_place"],
            tax=er_data["tax"],
            is_expense_generated=er_data["is_expense_generated"],
            expense_status=er_data["expense_status"],
            notes=er_data["notes"],
            vendor_gstin=er_data['vendor_gstin'],
            tax_rate=er_data['tax_rate'],
            tax_type=er_data['tax_type'],
            tax_name=er_data['tax_name'],
            tax_percentage=er_data['tax_rate'],
            cgst_amount=er_data['cgst_amount'],
            sgst_amount=er_data['sgst_amount'],
            igst_amount=er_data['igst_amount'],
            vendor_id=vn_id,
            attach_file=er_file_data,
            customer_id=cust_id,
            branch_id=branch_id,
            company_id=comp_id)
        er_id.save()
        Audit.objects.create(
            company_id=comp_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=er_data["expense_date"],
            module="Expense",
            sub_module='Expense',
            data=er_data
        )
            
        # 0% taxtion
        Zero_tax=er_data
        GST_TAX=None
        GST_TAX=Zero_tax['tax_name']
        if GST_TAX is not None:
            
            GST_TAX=Zero_tax['tax_name']
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
        print('GOD',GST_TAX)
        
        #Exp tax Section   
        FROM_COA = COA.objects.get(coa_id=er_data["paid_through"])
        transaction_list = [] #This Empty List added the append 
        if float(er_data['sgst_amount'])>0 or Both_Tax:
            transaction_list.append(["Input CGST", "sgst_amount"],)
        if float(er_data['cgst_amount'])>0 or Both_Tax:
            transaction_list.append(["Input SGST", "cgst_amount"])
        if float(er_data['igst_amount'])>0 or IGST_0:
            transaction_list.append(["Input IGST", "igst_amount"],)       
        
        for transaction in transaction_list:
            TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
            #transaction list of index is 0
            expmast = MasterTransaction.objects.create(
            L1detail_id=er_id.er_id,
            L1detailstbl_name='Expense Record',
            main_module='Purchase',
            module='Expense Record',
            sub_module='Expense Record',
            transc_deatils='Expanese Transaction',
            banking_module_type='Expense',
            journal_module_type='Expense Account Selection',
            trans_date=er_data["expense_date"],
            trans_status='Expense',
            debit=er_data[transaction[1]],
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=er_data[transaction[1]],
            from_account=FROM_COA.coa_id,
            from_acc_type=FROM_COA.account_type,
            from_acc_head=FROM_COA.account_head,
            from_acc_subhead=FROM_COA.account_subhead,
            from_acc_name=FROM_COA.account_name,
            customer_id=cust_id,
                branch_id=branch_id,
            company_id=comp_id,
            vendor_id=vn_id)
            expmast.save()

        print(er_data["expense_total"])
        #Expense main transaction Section Menas item Section
        FROM_COA = COA.objects.get(coa_id=er_data["paid_through"])
        TO_COA = COA.objects.get(coa_id=er_data["coa_id"])
        expmast = MasterTransaction.objects.create(
        L1detail_id=er_id.er_id,
        L1detailstbl_name='Expense Record',
        main_module='Purchase',
        module='Expense Record',
        sub_module='Expense Record',
        transc_deatils='Expanese Transaction',
        banking_module_type='Expense',
        journal_module_type='Expense Account Selection',
        trans_date=er_data["expense_date"],
        trans_status='Expense',
        debit=er_data["amount"], #
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=er_data["amount"],
        from_account=FROM_COA.coa_id,
        from_acc_type=FROM_COA.account_type,
        from_acc_head=FROM_COA.account_head,
        from_acc_subhead=FROM_COA.account_subhead,
        from_acc_name=FROM_COA.account_name,
        customer_id=cust_id,
            branch_id=branch_id,
        company_id=comp_id,
        vendor_id=vn_id)
        expmast.save()

        serializer = ExpenseRecordSerializer(er_id)  # browser
        return Response(serializer.data)


def download_exp(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response



# api for get bill by company id and bill id
@api_view(['GET'])

def download_exp_data(request,er_id):


    # here filter the object of bill id and company id
    er = ExpenseRecord.objects.select_related('vendor_id','company_id').get(
        er_id=er_id)
    serializers = ExpenseRecordSerializerDownload(er)#############

    html = generate_expense_pdf(data=serializers.data)
    return html

from django.db import transaction

#Creating the Expense
class ExpenseBankModelViewSets(viewsets.ModelViewSet):
    queryset=ExpenseRecord.objects.all()
    serializer_class=ExpbankSerializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        ExpenseBankModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        retValue=True
        if branch_id is None:
            ExpenseBankModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            ExpenseBankModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            ExpenseBankModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue    
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        expbank_data_converte= request.data['data']
       # expbank_data = request.data
        expbank_data = json.loads(expbank_data_converte)
        print("Converted Format is",type(expbank_data))
        try:
            expbank_file_data=request.FILES.get('attach_file')
        except KeyError:
            return response("file not uploaded")
        print("expbank_data",type(expbank_file_data))

        print('""""""""""""',expbank_data)

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=expbank_data["paid_through"]
        From_Bank=Banking.objects.get(coa_id=bank)

        if(ExpenseBankModelViewSets.ValidateDefaults(expbank_data)==False):
            print(" Ooops!!! Error Occured ",ExpenseBankModelViewSets.logger)
            
        print(expbank_data)
           
            #What if this ID is null , 
        # Branch Id Null	
        branch_id=expbank_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        #Company ID Null
        company_id=expbank_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        #Vendor ID Null
        vendor_id=expbank_data["vendor_id"]
        if vendor_id is not None:
            vendor_id=Vendor.objects.get(vendor_id=vendor_id)

        #Customer Id Null    
        customer_id=expbank_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
            
        company_year_id=expbank_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        # Create ExpenseBank

        expensebank_id=ExpenseRecord.objects.create(
        company_id=company_id,
        customer_id=customer_id,
        bank_id=From_Bank,
        vendor_id=vendor_id,
        is_expense_generated=expbank_data["is_expense_generated"],
        paid_through=expbank_data["paid_through"],
        status=expbank_data["status"],
        expense_date=expbank_data["expense_date"],
        expense_serial=expbank_data["expense_serial"],        
        expense_status=expbank_data["expense_status"],
        expense_type=expbank_data["expense_type"],
        hsn_code=expbank_data["hsn_code"],
        sac=expbank_data["sac"],
        invoice_serial=expbank_data["invoice_serial"],
        amount=expbank_data["amount"],
        notes=expbank_data["notes"],
        tax_rate=expbank_data["tax_rate"],
        tax_name=expbank_data["tax_name"],
       # tax_type=expbank_data["tax_type"],
       # tax_amount=expbank_data["tax_amount"],
       # reverse_charge=expbank_data["reverse_charge"],
        expense_total=expbank_data["expense_total"],
        attach_file=expbank_file_data)
        expensebank_id.save()



        
#region Master Transaction Section 
        TO_COA = COA.objects.get(coa_id=expbank_data["coa_id"])
        print('""""""""""""',TO_COA)  
        expmast=MasterTransaction.objects.create(
        L1detail_id=expensebank_id.er_id,
        L1detailstbl_name='ExpenseRecord',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        main_module='Banking',
        module='MonenyOut',
        sub_module='ExpenseBank',
        transc_deatils='Expense Bank',
        banking_module_type=expbank_data["transaction_module"],
        journal_module_type=expbank_data["transaction_module"],
        trans_date=expbank_data["expense_date"],
        trans_status=expbank_data["status"],
        debit=expbank_data["amount"],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=expbank_data['amount'],
        from_account=From_Bank.coa_id.coa_id,        
        from_acc_type=From_Bank.coa_id.account_type,
        from_acc_head=From_Bank.coa_id.account_head,
        from_acc_subhead=From_Bank.coa_id.account_subhead,
        from_acc_name=From_Bank.coa_id.account_name,
        company_id=company_id,
        customer_id=customer_id,
        vendor_id=vendor_id,
        branch_id=branch_id)
        expmast.save() 
#endregion
#End Of Master Transaction Section

        serializer =ExpbankSerializer(expensebank_id)
        print(serializer.data) 
        return Response(serializer.data)




#Expense Updating the Section
class ExpenseUpdateViewset(viewsets.ModelViewSet):
    queryset = ExpenseRecord.objects.all()
    serializer_class=UpdTExpenseRecordSerializer


    @transaction.atomic
    def update(self, request, pk, *args, **kwargs):
        file_data = None
        user = request.user
        try:
            exps_data = request.data['data']
            exps_data = json.loads(exps_data)
            file_data = request.FILES.get('attach_file')
        except:
            exps_data = request.data

        exp_id = ExpenseRecord.objects.select_for_update().get(er_id=pk)


        serializer = UpdTExpenseRecordSerializer(exp_id, data=exps_data)

        MasterTransaction.objects.filter(L1detail_id=pk).delete()
        if serializer.is_valid():
            serializer.save()
            if file_data:
                exp_id.attach_file = file_data
                exp_id.save()
            # msg="Details Updated Successfully"
            # return Response({"message":msg,"data":serializer.data,"status":200})
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        Audit.objects.create(
            company_id=exp_id.company_id,
            branch_id=exp_id.branch_id,
            modified_by=user,
            audit_modified_date=exps_data["expense_date"],
            module="Expense",
            sub_module='Expense',
            data=exps_data
        )
        er_data = exps_data
        vn_id = er_data["vendor_id"]
        if vn_id is not None:
            vn_id = Vendor.objects.get(vendor_id=vn_id)

        cust_id = er_data["customer_id"]
        if cust_id is not None:
            cust_id = SalesCustomer.objects.get(customer_id=cust_id)
        Zero_tax = er_data
        GST_TAX = None
        GST_TAX = Zero_tax['tax_name']
        if GST_TAX is not None:

            GST_TAX = Zero_tax['tax_name']
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
        print('GOD', GST_TAX)

        # Exp tax Section
        FROM_COA = COA.objects.get(coa_id=er_data["paid_through"])
        transaction_list = []  # This Empty List added the append
        if float(er_data['sgst_amount']) > 0 or Both_Tax:
            transaction_list.append(["Input CGST", "sgst_amount"], )
        if float(er_data['cgst_amount']) > 0 or Both_Tax:
            transaction_list.append(["Input SGST", "cgst_amount"])
        if float(er_data['igst_amount']) > 0 or IGST_0:
            transaction_list.append(["Input IGST", "igst_amount"], )

        for transaction in transaction_list:
            TO_COA = COA.objects.get(company_id=exp_id.company_id, account_name=transaction[0])
            # transaction list of index is 0
            expmast = MasterTransaction.objects.create(
                L1detail_id=pk,
                L1detailstbl_name='Expense Record',
                main_module='Purchase',
                module='Expense Record',
                sub_module='Expense Record',
                transc_deatils='Expanese Transaction',
                banking_module_type='Expense',
                journal_module_type='Expense Account Selection',
                trans_date=er_data["expense_date"],
                trans_status='Expense',
                debit=er_data[transaction[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=er_data[transaction[1]],
                from_account=FROM_COA.coa_id,
                from_acc_type=FROM_COA.account_type,
                from_acc_head=FROM_COA.account_head,
                from_acc_subhead=FROM_COA.account_subhead,
                from_acc_name=FROM_COA.account_name,
                customer_id=cust_id,
                branch_id=exp_id.branch_id,
                company_id=exp_id.company_id,
                vendor_id=vn_id)
            expmast.save()

        print(er_data["expense_total"])
        # Expense main transaction Section Menas item Section
        FROM_COA = COA.objects.get(coa_id=er_data["paid_through"])
        TO_COA = COA.objects.get(coa_id=er_data["coa_id"])
        expmast = MasterTransaction.objects.create(
            L1detail_id=pk,
            L1detailstbl_name='Expense Record',
            main_module='Purchase',
            module='Expense Record',
            sub_module='Expense Record',
            transc_deatils='Expanese Transaction',
            banking_module_type='Expense',
            journal_module_type='Expense Account Selection',
            trans_date=er_data["expense_date"],
            trans_status='Expense',
            debit=er_data["amount"],  #
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=er_data["amount"],
            from_account=FROM_COA.coa_id,
            from_acc_type=FROM_COA.account_type,
            from_acc_head=FROM_COA.account_head,
            from_acc_subhead=FROM_COA.account_subhead,
            from_acc_name=FROM_COA.account_name,
            customer_id=cust_id,
            branch_id=exp_id.branch_id,
            company_id=exp_id.company_id,
            vendor_id=vn_id)
        expmast.save()
        # serializer = ExpenseRecordSerializer(serializer)  # browser
        return Response(status=201)

# Get search details by expense_serial
@api_view(['GET'])

def getExpenseRecordDetailsByexpense_serial(request, expense_serial,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    exps = ExpenseRecord.objects.filter(company_id=company_id,
                                        branch_id=branch_id,
                                        expense_serial__icontains=expense_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": exps.count()}
    
    instance = exps[offset:offset + limit]
    serializer = ExpenseRecordSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)


@api_view(['GET'])

def getExpenseRecordDetailsByvendor_name(request, vendor_name, company_id,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    exps = ExpenseRecord.objects.filter(company_id=company_id,
                                        branch_id=branch_id,
                                        vendor_id__vendor_name__icontains=vendor_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": exps.count()}

    instance = exps[offset:offset + limit]
    serializer = ExpenseRecordSerializer(instance, many=True)

    response['results'] = serializer.data
    return Response(response)