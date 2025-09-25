import imp
import os
import json
from rest_framework import viewsets,generics,mixins
from rest_framework.response import Response
from company.models import Company, Branch ,Company_Year
from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.views.generic import View
from salescustomer.printing.generate_pr import generate_pr_pdf
from utility import render_to_pdf
from audit.models import Audit
from salescustomer.models.Pr_model import PR,PrView
from salescustomer.serializers.Pr_serializers import PRMSerializer,PRSerializer,prshortbycompanySerializer,updtPRMSerializer,GetPRshortbycompany_IDSerializer
from salescustomer.models.Invoice_model import Invoice
from salescustomer.serializers.Invoice_serializers import InvoiceSerializer
from company.serializers import CompanySerializer
from salescustomer.models.Salescustomer_model import SalesCustomer
from coa.models import COA
from transaction.models import MasterTransaction
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from salescustomer.models.Multiple_invoice_model import Multiple_Invoice_Details
from django.db import transaction
class PRFileDownloadListAPIView(generics.ListAPIView):
    
    def get(self, request, pr_id, format=None):
        queryset = PR.objects.get(pr_id=pr_id)
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
            return HttpResponse('No File Found')


#######################################################

#Payment Recived Generate pdf
class PRGeneratePdf(View):
    def get(self, request, pr_id, *args, **kwargs):
        paymentrecive = PR.objects.get(pr_id=pr_id)
        # Get The Payment Recive By  pr_id
        # and Then Serialize the data
        serializer = PRSerializer(paymentrecive)
        print(serializer.data)
        # get the Company data In PR (company_id) related
        print(paymentrecive.company_id.company_id)
        company = Company.objects.get(
            company_id=paymentrecive.company_id.company_id)
        # Serialize the data in Comapny
        company_serializer = CompanySerializer(company)
        print("##################################")
        print(serializer.data)
        print("##################################")
        print("Company Data", company_serializer.data)
        print("##################################")
        template = get_template('invoice.html')
        # Create the empty Dictionary in
        context = dict()
        # Add the Company and Invoice Data in Dictionary (Means Combine the data)
        context.update(dict(serializer.data))
        context.update(dict(company_serializer.data))
        html = template.render(context)

        return HttpResponse(html)


#####################
class PRDownloadPdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        pdf_path = render_to_pdf('base.html')

        filename = "pr_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)

        # rendering the template

        with open(pdf_path, 'r') as f:
            file_data = f.read()

        # sending response
        response = FileResponse(file_data, as_attachment=True,
                                filename='hello.pdf', content_type='application/pdf')
        response['Content-Disposition'] = content
        return response


#############################################################


class demoViewSet(viewsets.ModelViewSet):
    queryset = PR.objects.all()
    serializer_class = PRSerializer

    
    def create(self, request, *args, **kwargs):
        pr_data = request.data
        print("pr_data", pr_data)
        invoice_id = pr_data["invoice_id"]
        invoice = Invoice.objects.get(invoice_id=pr_data["invoice_id"])
        print("invoice.payment_status", invoice.payment_status)
        invoice.payment_status = pr_data["payment_status"]

        invoice.save()
        print('invoice_updated', invoice)

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)


# get all payment receive list
class paymentreceiveList(generics.ListAPIView):
    queryset = PR.objects.all()
    serializer_class = PRSerializer

    

class PRGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = PR.objects.all()
    serializer_class = PRSerializer

    
    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data
            return_data['attach_file'] = 'salescustomer/prfile_download/{}/'.format(
                pk)
            return Response({
                'data': return_data
            })
        return self.list(request)

# get payment recivied Full View by pr id
@api_view(['GET'])
@transaction.atomic
def prfullview(request, pk):
    prfullview = PR.objects.select_for_update().get(pr_id=pk)
    serializer = PRMSerializer(prfullview)
    return Response(serializer.data)

# get payment receive byid
@api_view(['GET'])


def prDetail(request, pk):
    pr = PR.objects.get(pr_id=pk)
    serializer = PRSerializer(pr, many=False)
    return Response(serializer.data)






# payment receive short by company id
@api_view(['GET'])


def prshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    objs = PrView.objects.filter(company_id=comp_id,branch_id=branch_id)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": objs.count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        items = objs[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = GetPRshortbycompany_IDSerializer(items, many=True).data
    return Response(response)
    
# api for get bill by company id and bill id
@api_view(['GET'])


def download_pr_data(request,pr_id):

    # here filter the object of bill id and company id
    precieved = PR.objects.select_related('company_id','customer_id').get(
        pr_id=pr_id)
    serializers =prshortbycompanySerializer(precieved)

    html = generate_pr_pdf(data=serializers.data)
    return html

def download_pr(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response
################################################################################

#Payment Recived Function based Upadting section
@api_view(['POST'])


def prUpdate(request, pk):
    pr = PR.objects.get(id=pk)
    serializer = PRSerializer(instance=pr, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)




# payment recieve abdulrashid sales customer
class new1paymentreceiveViewSet(viewsets.ModelViewSet):
    queryset = PR.objects.all()
    serializer_class = PRSerializer

    def create(self, request, *args, **kwargs):
        try:
            pr_data = json.loads(request.data['data'])

        except:
            pr_data = request.data

        pr_file_data = request.FILES.get('attach_file')
        user = request.user
        return self.handle_post(user,pr_data,pr_file_data)

    @transaction.atomic
    def handle_post(self,user, pr_data, pr_file_data):
        # count = Feature.objects.get(user_id=request.user.id).pr_remaining
        # print(count, 'payment received')
        # if count <= 0:
        #     return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)

        company_id=pr_data["company_id"]
        company_id=Company.objects.get(company_id=company_id)
        branch_id = Branch.objects.get(branch_id=pr_data["branch_id"])
        
        customer_id=pr_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
            
        print(pr_data)
        invoice_id=pr_data["invoice_id"]
        if invoice_id is not None:
            invoice_id=Invoice.objects.get(invoice_id=invoice_id)
        serializer = updtPRMSerializer(data=pr_data)
        if serializer.is_valid():
            pr_id = serializer.save()
            pr_id.attach_file = pr_file_data
            pr_id.save()
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=pr_data["payment_date"],
            module="PaymentRecv",
            sub_module='PaymentRecv',
            data=pr_data
        )
        party_account = pr_data.get('party_account', None)
        try:
            account_receivable = COA.objects.get(coa_id=party_account)
        except:
            if customer_id:
                account_receivable = customer_id.coa_id
            else:
                account_receivable = COA.get_account_recievables(company_id)
        if pr_data['bank_charges'] is not None and float(pr_data['bank_charges']) >0:
            # transaction_list.append(["Bank Fees and Charges","bank_charges"]) 
            From_Bank = COA.get_bank_fees_account(company_id)
            prmast = MasterTransaction.objects.create(
                L1detail_id=pr_id.pr_id,
                L1detailstbl_name='PR',
                L3detail_id=invoice_id.invoice_id,
                L3detailstbl_name='invoice',
                main_module='Sales',
                module='Payment Recived',
                sub_module='PR',
                transc_deatils='Payment Recived',
                trans_date=pr_data["payment_date"],
                banking_module_type='Customer Payment',
                journal_module_type='Invoice Payment',
                trans_status='Manually Added',
                debit=pr_data["bank_charges"],
                to_account=From_Bank.coa_id,
                to_acc_type=From_Bank.account_type,
                to_acc_head=From_Bank.account_head,
                to_acc_subhead=From_Bank.account_subhead,
                to_acc_name=From_Bank.account_name,
                credit=pr_data["bank_charges"],
                from_account=account_receivable.coa_id,
                from_acc_type=account_receivable.account_type,
                from_acc_head=account_receivable.account_head,
                from_acc_subhead=account_receivable.account_subhead,
                from_acc_name=account_receivable.account_name,
                customer_id=customer_id,
                branch_id=branch_id,
                company_id=company_id)
            prmast.save()
            
            
        To_Bank = COA.objects.get(coa_id=pr_data["coa_id"])
        prmast = MasterTransaction.objects.create(
            L1detail_id=pr_id.pr_id,
            L1detailstbl_name='PR',
            L3detail_id=invoice_id.invoice_id,
            L3detailstbl_name='invoice',
            main_module='Sales',
            module='Payment Recived',
            sub_module='PR',
            transc_deatils='Payment Recived',
            trans_date=pr_data["payment_date"],
            banking_module_type='Customer Payment',
            journal_module_type='Invoice Payment',
            trans_status='Manually Added',
            debit=pr_data["amount_received"],
            to_account=To_Bank.coa_id,
            to_acc_type=To_Bank.account_type,
            to_acc_head=To_Bank.account_head,
            to_acc_subhead=To_Bank.account_subhead,
            to_acc_name=To_Bank.account_name,
            credit=pr_data['amount_received'],
            from_account=account_receivable.coa_id,
            from_acc_type=account_receivable.account_type,
            from_acc_head=account_receivable.account_head,
            from_acc_subhead=account_receivable.account_subhead,
            from_acc_name=account_receivable.account_name,
            customer_id=customer_id,
            branch_id=branch_id,
            company_id=company_id)
        prmast.save()


        # Update the status in invoice table for payment_status
        # Update the status if update invoice status in Invoice model if amount_due==amount_received which means payment received is full
        amount_due = pr_data["amount_due"]
        amount_received = pr_data["amount_received"]
        # If payment is full then payment status will change unpaid to paid in invoice
        balance_amount = float(pr_data["balance_amount"])
        # if amount_due == amount_received:
        if balance_amount <= 0:
            invoice_id = Invoice.objects.select_for_update().get(invoice_id=pr_data["invoice_id"])
            print('invoice_id', invoice_id)
            invoice_id.payment_status = 'paid'
            invoice_id.amount_due = pr_data["balance_amount"]
            invoice_id.save()
            print('invoice status updated to ', invoice_id.payment_status)
        else:
            invoice_id = Invoice.objects.select_for_update().get(invoice_id=pr_data["invoice_id"])
            print('invoice id of else', invoice_id)
            invoice_id.amount_due = pr_data["balance_amount"]
            invoice_id.save()
            print('invoice amount due updated to ', invoice_id.amount_due)


        serializer = PRSerializer(pr_id)  # browser
        print(serializer.data)
        return Response(serializer.data)




#Payment Recived creting t
class paymentreceivenew_fromViewSet(viewsets.ModelViewSet):
    queryset = PR.objects.all()
    serializer_class = PRSerializer

    
    def create(self, request, *args, **kwargs):
        pr_data_converte = request.data['data']
        # PR Convert Str to Dict Code
        #pr_data = json.loads(pr_data_converte)
        pr_data=pr_data_converte
        pr_file_data = request.FILES.get('attach_file')
        
        company_id=pr_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        
        customer_id=pr_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
            
        
        invoice_id=pr_data["invoice_id"]
        if invoice_id is not None:
            invoice_id=Invoice.objects.get(invoice_id=invoice_id)


        # Payment Receive fields
        pr_id = PR.objects.create(
            # withholding_tax=pr_data["withholding_tax"],
            # customer_note=pr_data["customer_note"],
            notes=pr_data["notes"],
            amount_due=pr_data["amount_due"],
            invoice_amount=pr_data["invoice_amount"],
            invoice_date=pr_data["invoice_date"],
            invoice_serial=pr_data["invoice_serial"],
            payment_date=pr_data["payment_date"],
            tds_tax_account=pr_data["tds_tax_account"],
            tax_deducted=pr_data["tax_deducted"],
            bank_charges=pr_data["bank_charges"],
            amount_received=pr_data["amount_received"],
            balance_amount=pr_data["balance_amount"],
            amount_excess=pr_data["amount_excess"],
            payment_mode=pr_data["payment_mode"],
            deposit_to=pr_data["deposit_to"],
            payment_ref_no=pr_data["payment_ref_no"],
            payment_serial=pr_data["payment_serial"],
            ext_id=pr_data["ext_id"],
            ext_type=pr_data["ext_type"],
            attach_file=pr_file_data,
            customer_id=customer_id,
            invoice_id=invoice_id,
            company_id=company_id)

        # coa_id = COA.objects.get(coa_id=pr_data["coa_id"]))
        pr_id.save()


            
        account_receivable = COA.objects.get(company_id=company_id, account_subhead="Account Receivables",isdefault=True)
        # transaction_list = []
        if pr_data['bank_charges'] is not None and float(pr_data['bank_charges']) >0:
            # transaction_list.append(["Bank Fees and Charges","bank_charges"]) 
            From_Bank = COA.objects.get(company_id=company_id,account_name="Bank Fees and Charges",isdefault=True)
            prmast = MasterTransaction.objects.create(
                L1detail_id=pr_id.pr_id,
                L1detailstbl_name='PR',
                L3detail_id=invoice_id.invoice_id,
                L3detailstbl_name='invoice',
                main_module='Sales',
                module='Payment Received',
                sub_module='PR',
                transc_deatils='Payment Received',
                trans_date=pr_data["payment_date"],
                banking_module_type='Customer Payment',
                journal_module_type='Invoice Payment',
                trans_status='Manually Added',
                debit=pr_data["bank_charges"],
                to_account=From_Bank.coa_id,
                to_acc_type=From_Bank.account_type,
                to_acc_head=From_Bank.account_head,
                to_acc_subhead=From_Bank.account_subhead,
                to_acc_name=From_Bank.account_name,
                credit=pr_data["bank_charges"],
                from_account=account_receivable.coa_id,
                from_acc_type=account_receivable.account_type,
                from_acc_head=account_receivable.account_head,
                from_acc_subhead=account_receivable.account_subhead,
                from_acc_name=account_receivable.account_name,
                customer_id=customer_id,
                company_id=company_id)
            prmast.save()
            
            
        From_Bank = COA.objects.get(coa_id=pr_data["coa_id"])
        prmast = MasterTransaction.objects.create(
            L1detail_id=pr_id.pr_id,
            L1detailstbl_name='PR',
            L3detail_id=invoice_id.invoice_id,
            L3detailstbl_name='invoice',
            main_module='Sales',
            module='Payment Recived',
            sub_module='PR',
            transc_deatils='Payment Recived',
            trans_date=pr_data["payment_date"],
            banking_module_type='Customer Payment',
            journal_module_type='Invoice Payment',
            trans_status='Manually Added',
            debit=pr_data["amount_received"],
            to_account=From_Bank.coa_id,
            to_acc_type=From_Bank.account_type,
            to_acc_head=From_Bank.account_head,
            to_acc_subhead=From_Bank.account_subhead,
            to_acc_name=From_Bank.account_name,
            credit=pr_data['amount_received'],
            from_account=account_receivable.coa_id,
            from_acc_type=account_receivable.account_type,
            from_acc_head=account_receivable.account_head,
            from_acc_subhead=account_receivable.account_subhead,
            from_acc_name=account_receivable.account_name,
            customer_id=customer_id,
            company_id=company_id)
        prmast.save()


        # Update the status in invoice table for payment_status
        # Update the status if update invoice status in Invoice model if amount_due==amount_received which means payment received is full
        amount_due = pr_data["amount_due"]
        print("amount_due", amount_due, type(amount_due))
        amount_received = pr_data["amount_received"]
        print("amount_received", amount_received, type(amount_received))
        # If payment is full then payment status will change unpaid to paid in invoice
        balance_amount = float(pr_data["balance_amount"])
        # if amount_due == amount_received:
        if balance_amount <= 0:
            invoice_id = Invoice.objects.get(invoice_id=pr_data["invoice_id"])
            print('invoice_id', invoice_id)
            invoice_id.payment_status = 'paid'
            invoice_id.amount_due = pr_data["balance_amount"]
            invoice_id.save()
            print('invoice status updated to ', invoice_id.payment_status)
        else:
            invoice_id = Invoice.objects.get(invoice_id=pr_data["invoice_id"])
            print('invoice id of else', invoice_id)
            invoice_id.amount_due = pr_data["balance_amount"]
            invoice_id.save()
            print('invoice amount due updated to ', invoice_id.amount_due)
        serializer = PRSerializer(pr_id)  # browser
        return Response(serializer.data,status=200)

from django.db.models import Q

#Updating the Payment Recived 
class UpdtPaymentRCvViewset(viewsets.ModelViewSet):
    queryset = PR.objects.all()
    serializer_class=updtPRMSerializer

    
    def update(self, request, pk, *args, **kwargs):
        pr_file_data = None
        try:
            pr_data = json.loads(request.data['data'])
            pr_file_data = request.FILES.get('attach_file')
            del pr_data['attach_file']
        except:
            pr_data = request.data
        user = request.user
        return self.handle_update(user,pr_data,pr_file_data,pk)
    @transaction.atomic
    def handle_update(self, user,pr_data,pr_file_data, pk):


        print(pr_data)
        #Cehck the Pr id in pr tabel
        pr = PR.objects.select_for_update().get(pr_id=pk)
        MasterTransaction.objects.select_for_update().filter(L1detail_id=pr.pr_id).delete()
        serializer = updtPRMSerializer(pr, data=pr_data)
        company_id = pr.company_id
        branch_id = pr.branch_id
        customer_id = pr_data["customer_id"]
        if customer_id is not None:
            customer_id = SalesCustomer.objects.get(customer_id=customer_id)
        invoice_id = pr_data["invoice_id"]
        if invoice_id is not None:
            invoice_id = Invoice.objects.get(invoice_id=invoice_id)
        if serializer.is_valid():
            if pr_file_data is not None:
                pr.attach_file  = pr_file_data
                pr.save()
            serializer.save()
            msg="Details Updated Successfully"
            
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            modified_by=user,
            audit_modified_date=pr_data["payment_date"],
            module="PaymentRecv",
            sub_module='PaymentRecv',
            data=pr_data
        )
        party_account = pr_data.get('party_account', None)
        try:
            account_receivable = COA.objects.get(coa_id=party_account)
        except:
            if customer_id:
                account_receivable = customer_id.coa_id
            else:
                account_receivable = COA.get_account_recievables(company_id)
        if pr_data['bank_charges'] is not None and float(pr_data['bank_charges']) > 0:
            # transaction_list.append(["Bank Fees and C harges","bank_charges"])
            From_Bank = COA.get_bank_fees_account(company_id)
            prmast = MasterTransaction.objects.create(
                L1detail_id=pr.pr_id,
                L1detailstbl_name='PR',
                L3detail_id=invoice_id.invoice_id,
                L3detailstbl_name='invoice',
                main_module='Sales',
                module='Payment Recived',
                sub_module='PR',
                transc_deatils='Payment Recived',
                trans_date=pr_data["payment_date"],
                banking_module_type='Customer Payment',
                journal_module_type='Invoice Payment',
                trans_status='Manually Added',
                debit=pr_data["bank_charges"],
                to_account=From_Bank.coa_id,
                to_acc_type=From_Bank.account_type,
                to_acc_head=From_Bank.account_head,
                to_acc_subhead=From_Bank.account_subhead,
                to_acc_name=From_Bank.account_name,
                credit=pr_data["bank_charges"],
                from_account=account_receivable.coa_id,
                from_acc_type=account_receivable.account_type,
                from_acc_head=account_receivable.account_head,
                from_acc_subhead=account_receivable.account_subhead,
                from_acc_name=account_receivable.account_name,
                customer_id=customer_id,
                branch_id=branch_id,
                company_id=company_id)
            prmast.save()

        To_Bank = COA.objects.get(coa_id=pr_data["coa_id"])
        prmast = MasterTransaction.objects.create(
            L1detail_id=pr.pr_id,
            L1detailstbl_name='PR',
            L3detail_id=invoice_id.invoice_id,
            L3detailstbl_name='invoice',
            main_module='Sales',
            module='Payment Recived',
            sub_module='PR',
            transc_deatils='Payment Recived',
            trans_date=pr_data["payment_date"],
            banking_module_type='Customer Payment',
            journal_module_type='Invoice Payment',
            trans_status='Manually Added',
            debit=pr_data["amount_received"],
            to_account=To_Bank.coa_id,
            to_acc_type=To_Bank.account_type,
            to_acc_head=To_Bank.account_head,
            to_acc_subhead=To_Bank.account_subhead,
            to_acc_name=To_Bank.account_name,
            credit=pr_data['amount_received'],
            from_account=account_receivable.coa_id,
            from_acc_type=account_receivable.account_type,
            from_acc_head=account_receivable.account_head,
            from_acc_subhead=account_receivable.account_subhead,
            from_acc_name=account_receivable.account_name,
            customer_id=customer_id,
            branch_id=branch_id,
            company_id=company_id)
        prmast.save()
        amount_due = pr_data["amount_due"]
        amount_received = pr_data["amount_received"]

        balance_amount = float(pr_data["balance_amount"])
        if balance_amount <= 0:
            invoice_id = Invoice.objects.select_for_update().get(invoice_id=pr_data["invoice_id"])
            print('invoice_id', invoice_id)
            invoice_id.payment_status = 'paid'
            invoice_id.amount_due = pr_data["balance_amount"]
            invoice_id.save()
            print('invoice status updated to ', invoice_id.payment_status)
        else:
            invoice_id = Invoice.objects.select_for_update().get(invoice_id=pr_data["invoice_id"])
            invoice_id.payment_status = "unpaid"
            invoice_id.amount_due = pr_data["balance_amount"]
            invoice_id.save()
            print('invoice amount due updated to ', invoice_id.amount_due)

        return Response(serializer.data,status=200)



#Logic for paid multiple invoices. at a time 
class MultipleInvoice_Paid_At_onetime(viewsets.ModelViewSet):
    queryset = PR.objects.all()  # get the Paymentmade Model Data
    serializer_class = PRSerializer
    
    # payment recieve field
    def create(self, request, *args, **kwargs):
        pr_data = request.data
        print("request.dats",pr_data)
      
       
        customer=pr_data["customer_id"]
        if customer is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer)
            
        company_id = pr_data["company_id"]
        if company_id is not None:
            company_id = Company.objects.get(company_id=company_id)
            
        company_year_id=pr_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
    
        invoice_id=pr_data.get("invoice_id")
        if invoice_id is not None:
            invoice_id=Invoice.objects.get(invoice_id=invoice_id)
        
        
        
        
        
        # Payment recieve field
        pm_serializer = PRSerializer(data=pr_data)
        if pm_serializer.is_valid():
            pr_id = pm_serializer.save()
            pr_id.save()
        else:
            return Response(pm_serializer.errors)

        account_recievable =COA.get_account_recievables(company_id)

        for invoice in pr_data["multiple_invoices"]:
            print("bill in multiple bill",invoice)
            multiple_invoices = Multiple_Invoice_Details.objects.create(
                                                         invoice_id=Invoice.objects.get(
                                                             invoice_id=invoice["invoice_id"]),
                                                         company_id=Company.objects.get(
                                                             company_id=invoice["company_id"]),
                                                         customer_id=SalesCustomer.objects.get(
                                                             customer_id=invoice["customer_id"]),
                                                        
                                                         amount=invoice["amount"],
                                                         amount_due=invoice["amount_due"],
                                                        
                                                         pr_id=pr_id)
            
            multiple_invoices.save()
           
        invoice_id = multiple_invoices.invoice_id
        print(invoice)
        invoice_main_amount=multiple_invoices.amount
        print('bill main amount',invoice_main_amount)
                
        invoice_id.payment_status = 'paid'
        print("////////////////",invoice_id)
        invoice_id.save()
            
        remaing_amount=int(invoice_main_amount.split('.')[0])-int(invoice_main_amount.split('.')[0])
        print('remaing',remaing_amount)
        total_amount=remaing_amount
           
                
                
        comp_id=Company.objects.get(company_id=pr_data["company_id"])
        account_recievable = COA.get_account_recievables(comp_id)
        print('Account PAybale is her @@@@@@@@@@@@',account_recievable)
        print('Account  @@@@@@@@@@@@',account_recievable.coa_id)
        customer_id = SalesCustomer.objects.get(customer_id=pr_data["customer_id"])
            
        

        company_year_id=pr_data.get("company_year_id")
        if company_year_id is not None:
                    company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        company_id = Company.objects.get(
                    company_id=pr_data["company_id"])
            #From_Bank = COA.objects.get(coa_id=paymentmade_data["paid_through"])
        From_Bank = COA.objects.get(company_id=company_id, account_subhead='Bank',isdefault=True)
        pmmast = MasterTransaction.objects.create(
                    L1detail_id=pr_id.pr_id,
                    L1detailstbl_name='PR',
                # L3detail_id=multiple_bills.bill_id,
                    L3detailstbl_name='Invoice',
                    main_module='Salescustomer',
                    module='Salescustomer',
                    sub_module='PR',
                    transc_deatils='PR',
                    banking_module_type='Vendor Payment',
                    journal_module_type='Payment Recieve',
                    trans_date=pr_data["invoice_date"],
                    trans_status='Maually Added',
                    debit=invoice_main_amount,
                    to_account=account_recievable.coa_id,
                    to_acc_type=account_recievable.account_type,
                    to_acc_head=account_recievable.account_head,
                    to_acc_subhead=account_recievable.account_subhead,
                    to_acc_name=account_recievable.account_name,
                    credit=invoice_main_amount,
                    from_account=From_Bank.coa_id,
                    from_acc_type=From_Bank.account_type,
                    from_acc_head=From_Bank.account_head,
                    from_acc_subhead=From_Bank.account_subhead,
                    from_acc_name=From_Bank.account_name,
                    customer_id=customer_id,
                    company_id=company_id)
        pmmast.save()   
                                       
        serializer =InvoiceSerializer(invoice_id)
        return Response(serializer.data)


# Get PR details by pr number
@api_view(['GET'])


def getPRDetailsByPR_number(request, company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    payment_serial = request.GET['serial']
    prs = PrView.objects.filter(company_id=company_id,
                            branch_id=branch_id,
                            payment_serial__icontains=payment_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": prs.count()}
    
    instance = prs[offset:offset + limit]
    serializer = GetPRshortbycompany_IDSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)




@api_view(['GET'])


def getPRshortbyCustomer_name(request,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    customer_name = request.GET['name']
    prs = PrView.objects.filter(company_id=company_id,
                            branch_id=branch_id,
                            customer_name__icontains=customer_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": prs.count()}
    
    instance = prs[offset:offset + limit]
    

    serializer = GetPRshortbycompany_IDSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)