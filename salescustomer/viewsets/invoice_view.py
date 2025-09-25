import os
import json
from io import BytesIO
import datetime
from rest_framework import viewsets,generics,mixins
from rest_framework.response import Response
from company.models import Company, Branch
from wsgiref.util import FileWrapper
from salescustomer.viewsets.pr_view import new1paymentreceiveViewSet,UpdtPaymentRCvViewset
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.views.generic import View
from salescustomer.printing.generate_invoice import generate_invoice_pdf
from utility import render_to_pdf
from re import template
from xhtml2pdf import pisa
from salescustomer.models.Invoice_model import Invoice
from salescustomer.serializers.Invoice_serializers import JoinInvoiceAndInvoiceItemSerializer,InvoiceAndInvoiceItem2ASerializer,invoiceshortbycompanySerializer,InvoiceSerializer,ShortInvoiceSerializer,reports2AInvoiceItemSerializer
from salescustomer.models.Salescustomer_model import SalesCustomer
from salescustomer.serializers.Salescustomer_serializers import InvoicebyCustomerSerializer
from transaction.models import MasterTransaction,CoaCharges
from transaction.serializers import ChargeTransactionSerializer
from coa.models import COA
from item.models.item_model import Item
from item.models.stock_model import Stock,Batch,get_inventory_value_rate
from salescustomer.models.Employee_model import Employee
from salescustomer.models.Invoice_item_model import InvoiceItem
from salescustomer.models.Tcs_model import TCS
from salescustomer.serializers.Invoice_item_serializers import InvoiceItemSerializer
from django.db import transaction
from audit.models import Audit
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from salescustomer.models.Estimate_model import Estimate
from salescustomer.models.So_model import SO
from salescustomer.models.Dc_model import DC
from salescustomer.models.Creditnote_model import CreditNote
from django.db.models import Q
from salescustomer.models.Pr_model import PR
##############
# get invoice api
import traceback
from autocount.permission import CustomPermission
from registration.models import  Feature
@api_view(['GET'])


def getinvoicebyinvoiceid(request, invoice_id):
    object = Invoice.objects.get(invoice_id=invoice_id)
    serializer = JoinInvoiceAndInvoiceItemSerializer(object, many=False)
    return Response(serializer.data)


#GST 2A Reports
@api_view(['GET'])


def get2Areports(request, company_id):
    object = Invoice.objects.filter(company_id=company_id)
    serializer = InvoiceAndInvoiceItem2ASerializer(object, many=False)
    return Response(serializer.data)

# Dwonload Code Is Creting api By Download
# Download Invoice by id Attach File Download


class FileDownloadListAPIView(generics.ListAPIView):

    def get(self, request, invoice_id, format=None):
        queryset = Invoice.objects.get(invoice_id=invoice_id)
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


############################
# File Convert in  Pdf
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    current_time = datetime.datetime.now().timestamp()
    pdf_path = 'media/mypdf_{}.pdf'.format(current_time)
    with open(pdf_path, 'wb+') as output:
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
    return pdf_path


class InvoiceDownloadPdf(View):
    def get(self, request, *args, **kwargs):
        html = template
        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)

        # rendering the template

        with open(pdf_path, 'r') as f:
            file_data = f.read()

        # sending response
        response = FileResponse(file_data, as_attachment=True,
                                filename='hello.pdf', content_type='application/pdf')
        response['Content-Disposition'] = content
        return response


# 3
# Invoice and Item join
class InvoiceItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Invoice.objects.all()
    serializer_class = JoinInvoiceAndInvoiceItemSerializer

    
    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data

            return Response({
                'data': return_data
            })
        return self.list(request)







# invoiceshortbycompanyid

####################################################
@api_view(['GET'])


def invoiceshortbycompanyid(request, comp_id,branch_id):
    # invoice = Invoice.objects.all().order_by('created_date')
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    objs = Invoice.objects.filter(company_id=comp_id,branch_id=branch_id)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": objs.count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        invoice = objs.order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = invoiceshortbycompanySerializer(invoice, many=True).data
    return Response(response)

#########################################################
@api_view(['GET'])

# 
def download_inv(request, comp_id, invoice_id):
    # invoice = Invoice.objects.all().order_by('created_date')
    company = Company.objects.get(company_id=comp_id)
    inv = Invoice.objects.get(invoice_id=invoice_id)
    invoice = Invoice.objects.filter(
        company_id=comp_id, invoice_id=invoice_id).order_by('created_date')
    print(f"&&&&&&&&&&&&&&&&&&&&&&&&&{invoice}")
    #serializer = invoiceshortbycompanySerializer(invoice, many=True)
    serializers = JoinInvoiceAndInvoiceItemSerializer(invoice, many=True)

    output_pdf = f'INV_{datetime.datetime.now().timestamp()}.pdf'
    html = generate_invoice_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
    return html


def download_invoice(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:

    response = FileResponse(open(file_path, 'rb'),as_attatchment=True)
    # response = FileResponse(file_data, as_attachment=True,

    return response


@api_view(['GET'])


def invoiceDetail(request, pk):
    invoice = Invoice.objects.get(id=pk)
    serializer = InvoiceSerializer(invoice, many=False)
    return Response(serializer.data)








# get invoice by customer id(Response for this api is its return only unpaid invoices as per respective  customer)
@api_view(['GET'])


def invoicebycustomerid(request, pk):
    customer = SalesCustomer.objects.get(customer_id=pk)
    print('customer', customer)
    serializer = InvoicebyCustomerSerializer(customer, many=False)
    return Response(serializer.data)

#this section is use to invoice ref 
@api_view(['GET'])


def invoicerefbycustomerid(request, pk):
    customer = SalesCustomer.objects.get(customer_id=pk)
    invoices=Invoice.objects.filter(customer_id=customer)
    print('Invoces Is here',invoices)
    response_list=[]
    for invoice in invoices:
        invoice_id=invoice.invoice_id
        invoice_serial=invoice.invoice_serial
        customer_id=invoice.customer_id.customer_id
   
        response_dict = {"invoice_id":invoice_id,"invoice_serial":invoice_serial,"customer_id":customer_id,"label":invoice_serial,"value":invoice_id}
        response_list.append(response_dict)  
    return Response(response_list)


@api_view(['POST'])


def invoiceUpdate(request, pk):
    invoice = Invoice.objects.get(id=pk)
    serializer = InvoiceSerializer(instance=invoice, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)






@api_view(['GET'])


def download_inv(request, invoice_id):

    invoice = Invoice.objects.select_related('customer_id','company_id').prefetch_related('charges').get(
        invoice_id=invoice_id)

    #serializer = invoiceshortbycompanySerializer(invoice, many=True)
    serializers = JoinInvoiceAndInvoiceItemSerializer(invoice)
    output_pdf = f"INV_{datetime.datetime.now().timestamp()}.pdf"

    html = generate_invoice_pdf(data=serializers.data,output_path=os.path.join("media", output_pdf))
    return html



def download_invoice(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
    response = FileResponse(open(file_path, 'rb'))
    # response = FileResponse(file_data, as_attachment=True,
    return response





from django.db import transaction as trans
class new3invoiceitemsViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

    
    # here is the entry for invoice

    def handle_post(self, user,invoice_data, invoice_file_data):
        with trans.atomic():
            try:
                all_invoice_items = invoice_data["invoice_items"]
                company_id = Company.objects.get(company_id=invoice_data["company_id"])
                print(invoice_data['branch_id'])
                branch_id = Branch.objects.get(branch_id=invoice_data["branch_id"])
                bch_id = invoice_data["branch_id"]
                ext_id = invoice_data.get('ext_id',None)
                print(f"company ID is HERE ",company_id)
                try:
                    cust_id = SalesCustomer.objects.get(
                    customer_id=invoice_data["customer_id"])
                except:
                    cust_id = None
                employee_id = None
                employee_id = invoice_data["emp_id"]
                if employee_id is not None:
                    employee_id = Employee.objects.get(emp_id=employee_id)
                tcs_id = None
                tcs_id = invoice_data['tcs_id']
                if tcs_id is not None:
                    tcs_id = TCS.objects.get(tcs_id=tcs_id)
                print(tcs_id)
                invoice_data['amount_due'] = invoice_data["total"]
                invoice_serializer = InvoiceSerializer(data=invoice_data)
                if invoice_serializer.is_valid():
                    invoice_id = invoice_serializer.save()
                    invoice_id.tcs_id = tcs_id
                    invoice_id.attach_file = invoice_file_data
                    invoice_id.company_id = company_id
                    invoice_id.branch_id = branch_id
                    invoice_id.emp_id = employee_id
                    invoice_id.customer_id = cust_id
                    invoice_id.save()

                    comp = Company.objects.select_for_update().get(company_id=invoice_data["company_id"])
                    sequence = comp.invoice_sequence
                    invoice_no = sequence
                    invoice_id.invoice_serial = invoice_no
                    invoice_id.save()
                    comp.invoice_sequence = sequence + 1
                    comp.save()
                else:
                    print(invoice_serializer.errors)
                    return Response(invoice_serializer.errors,status=400)
                Audit.objects.create(
                    company_id=company_id,
                    branch_id=branch_id,
                    created_by=user,
                    audit_created_date=invoice_data["invoice_date"],
                    module="Invoice",
                    sub_module='Invoice',
                    data=invoice_data
                )
                print(invoice_serializer.data['tcs_id'])
                # check if the is_convertwd is true

                if invoice_id.is_converted == True:
                    if invoice_id.From_convt_type == "Estimate to Invoice":
                        print("*********************", invoice_id.is_converted)

                        # Assign the relevant fields from the estimate object to the invoice object:
                        invoice_id.From_convt_id = invoice_data['convt_id']
                        invoice_id.From_convt_ref_no = invoice_data['convt_ref_no']
                        invoice_id.From_convt_serial = invoice_data['convt_serial']
                        invoice_id.From_is_converted = invoice_data["is_converted"]
                        print("////////////////////////////////////////", invoice_id.From_is_converted)
                        invoice_id.From_convt_type = invoice_data['convt_type']
                        invoice_id.save()

                        print("OHHHHHHHHHHHHHHHHH")

                        # Get estimate by converted id
                        est = Estimate.objects.get(est_id=invoice_data['convt_id'])
                        print("estimate Object is Here", invoice_id.From_convt_id)
                        if not est.To_is_converted:
                            est.To_convt_id = invoice_id.From_convt_id
                            est.To_convt_ref_no = invoice_id.From_convt_ref_no
                            est.To_convt_serial = invoice_id.From_convt_serial
                            est.To_is_converted = invoice_id.From_is_converted
                            est.To_convt_type = invoice_id.From_convt_type
                            est.save()
                        else:
                            return Response("This Estimate Already Converted")

                    elif invoice_id.From_convt_type == "Sales Order to Invoice":
                        print("*********************", invoice_id.is_converted)

                        # Assign the relevant fields from the sales order object to the invoice object:
                        invoice_id.From_convt_id = invoice_data['convt_id']
                        invoice_id.From_convt_ref_no = invoice_data['convt_ref_no']
                        invoice_id.From_convt_serial = invoice_data['convt_serial']
                        invoice_id.From_is_converted = invoice_data["is_converted"]
                        print("////////////////////////////////////////", invoice_id.From_is_converted)
                        invoice_id.From_convt_type = invoice_data['convt_type']
                        invoice_id.save()

                        print("OHHHHHHHHHHHHHHHHH")

                        # Get sales order by converted id
                        so = SO.objects.get(so_id=invoice_data['convt_id'])
                        print("sales order Object is Here", invoice_id.From_convt_id)
                        if not so.To_is_converted:
                            so.To_convt_id = invoice_id.From_convt_id
                            so.To_convt_ref_no = invoice_id.From_convt_ref_no
                            so.To_convt_serial = invoice_id.From_convt_serial
                            so.To_is_converted = invoice_id.From_is_converted
                            so.To_convt_type = invoice_id.From_convt_type
                            so.save()
                        else:
                            return Response("This Estimate Already Converted")

                    elif invoice_id.From_convt_type == "DC to Invoice":
                        print("*********************", invoice_id.is_converted)

                        # Assign the relevant fields from the estimate object to the invoice object:
                        invoice_id.From_convt_id = invoice_data['convt_id']
                        invoice_id.From_convt_ref_no = invoice_data['convt_ref_no']
                        invoice_id.From_convt_serial = invoice_data['convt_serial']
                        invoice_id.From_is_converted = invoice_data["is_converted"]
                        print("////////////////////////////////////////", invoice_id.From_is_converted)
                        invoice_id.From_convt_type = invoice_data['convt_type']
                        invoice_id.save()

                        print("OHHHHHHHHHHHHHHHHH")

                        # Get estimate by converted id
                        dc = DC.objects.get(dc_id=invoice_data['convt_id'])
                        print("estimate Object is Here", invoice_id.From_convt_id)
                        if not est.To_is_converted:
                            dc.To_convt_id = invoice_id.From_convt_id
                            dc.To_convt_ref_no = invoice_id.From_convt_ref_no
                            dc.To_convt_serial = invoice_id.From_convt_serial
                            dc.To_is_converted = invoice_id.From_is_converted
                            dc.To_convt_type = invoice_id.From_convt_type
                            dc.save()
                        else:
                            return Response("This DC Already Converted")
                    elif invoice_id.From_convt_type == "Invoice to CN":
                        print("*********************", invoice_id.is_converted)

                        # Assign the relevant fields from the estimate object to the invoice object:
                        invoice_id.From_convt_id = invoice_data['convt_id']
                        invoice_id.From_convt_ref_no = invoice_data['convt_ref_no']
                        invoice_id.From_convt_serial = invoice_data['convt_serial']
                        invoice_id.From_is_converted = invoice_data["is_converted"]
                        print("////////////////////////////////////////", invoice_id.From_is_converted)
                        invoice_id.From_convt_type = invoice_data['convt_type']
                        invoice_id.save()

                        print("OHHHHHHHHHHHHHHHHH")

                        # Get estimate by converted id
                        cn = CreditNote.objects.get(cn_id=invoice_data['convt_id'])
                        print("estimate Object is Here", invoice_id.From_convt_id)
                        if not cn.To_is_converted:
                            cn.To_convt_id = invoice_id.From_convt_id
                            cn.To_convt_ref_no = invoice_id.From_convt_ref_no
                            cn.To_convt_serial = invoice_id.From_convt_serial
                            cn.To_is_converted = invoice_id.From_is_converted
                            cn.To_convt_type = invoice_id.From_convt_type
                            cn.save()
                        else:
                            return Response("This CN Already Converted")
                sales_account = invoice_data.get('sales_account', None)
                party_account = invoice_data.get('party_account', None)
                try:
                    account_receivable = COA.get_account(party_account)
                except:
                    if cust_id:
                        account_receivable = cust_id.coa_id
                    else:
                        account_receivable = COA.get_account_recievables(company_id)
                try:
                    sales_account = COA.get_account(sales_account)
                except:
                    sales_account = None

                coa_amount_dict = {}
                for item in all_invoice_items:
                    godown_id = item['godown_id']
                    coa=COA.get_account(item["coa_id"])
                    invoice_items = InvoiceItem.objects.create(invoice_id=invoice_id,
                                                               item_id=Item.objects.get(
                                                                   item_id=item["item_id"]),
                                                               coa_id=coa,
                                                               item_name=item["item_name"],
                                                               rate=item["rate"],
                                                               quantity=item["quantity"],
                                                               tax_rate=float(item["tax_rate"]),
                                                               tax_name=item["tax_name"],
                                                               tax_type=item["tax_type"],
                                                               godown_id_id=godown_id,
                                                               godown_name=item['godown_name'],
                                                               sgst_amount=item["sgst_amount"],
                                                               cgst_amount=item["cgst_amount"],
                                                               igst_amount=item["igst_amount"],
                                                               discount=item["discount"],
                                                               cess_rate=item['cess_rate'],
                                                               cess_amount=item['cess_amount'],
                                                               # taxamount=item["taxamount"],
                                                               amount=item["amount"]
                                                               )
                    invoice_items.save()
                    item_obj=Item.objects.get(item_id=item["item_id"])
                    track_inventory=item_obj.track_inventory
                    if track_inventory:
                        batches = item['batches']
                        mfg_date = item['mfg_date']
                        expire_date = item['expire_date']
                        if len(batches) == 0:
                            batches.append(None)
                            mfg_date = None
                            expire_date = None
                        invoice_items.batches = batches
                        invoice_items.expire_date = expire_date
                        invoice_items.mfg_date = mfg_date
                        invoice_items.save()
                        stk_in = None
                        stk_out = None

                        remaining_to_sell = float(item["quantity"])
                        for index,batch in enumerate(batches):
                            print(remaining_to_sell)
                            if remaining_to_sell > 0:
                                if False:
                                    if batch is None:
                                        batch_total_stk_in = Batch.objects.get(Q(item_id=item["item_id"],
                                                                                 expire_date=item['expire_date'],
                                                                                mfg_date = item['mfg_date'],
                                                                                 branch_id=bch_id,
                                                                                 batch_no__isnull=True))
                                        batch_total_stk_in = float(batch_total_stk_in.stock_quantity)
                                    else:
                                        print(item_obj.item_id,item,batch,item['mfg_date'],item['expire_date'])
                                        batch_total_stk_in = Batch.objects.get(item_id=item_obj.item_id,
                                                                                         expire_date=item['expire_date'],
                                                                                         mfg_date=item['mfg_date'],
                                                                                        branch_id=bch_id,
                                                                                         batch_no=batch)
                                        batch_total_stk_in = float(batch_total_stk_in.stock_quantity)

                                    print(stk_in,stk_out,batch_total_stk_in,batch)
                                    if index == len(batches)-1:
                                        if (batch_total_stk_in - remaining_to_sell) < 0:

                                           raise Exception("Stock Not Available")
                                Stock.objects.create(
                                    item_id=item["item_id"],
                                    item_name=item["item_name"],
                                    godown_id_id=godown_id,
                                    godown_name=item['godown_name'],
                                    flow_type='OUTWARD',
                                    batch_no=batch,
                                    mfg_date=mfg_date,
                                    expire_date=expire_date,
                                    stock_out=item["quantity"],
                                    ref_id=invoice_id.invoice_id,
                                    module_date=invoice_id.created_date,
                                    amount=item["amount"],
                                    rate=item["rate"],
                                    ref_tblname='Invoice',
                                    module='Sales',
                                    quantity=item["quantity"],
                                    formname='Invoice',
                                    stage='Add Stages',
                                    date=invoice_data["invoice_date"],
                                    branch_id=branch_id,
                                    company_id=company_id)

                    if coa_amount_dict.get(item['coa_id']) is None:
                        coa_amount_dict[item['coa_id']] = item['amount']
                    else:
                        coa_amount_dict[item['coa_id']] = float(coa_amount_dict[item['coa_id']]) + float(item['amount'])


                transaction_list = []
                if float(invoice_data['tcs_amount'])>0:
                    tcs_account = invoice_data.get('tcs_account', None)
                    if tcs_account:
                        account = COA.objects.get(coa_id=tcs_account)
                    else:
                        account = COA.get_input_tcs_pay_account(company_id)
                    transaction_list.append([account,"tcs_amount"])
                if float(invoice_data['shipping_charges']) >0:
                    shipping_account = invoice_data.get('shipping_account', None)
                    if shipping_account:
                        account = COA.objects.get(coa_id=shipping_account)
                    else:
                        account = COA.get_shipping_account(company_id)
                    transaction_list.append([account,"shipping_charges"])

                if float(invoice_data['cess_total']) > 0:
                    cess_account = invoice_data.get('cess_account', None)
                    if cess_account:
                        account = COA.objects.get(coa_id=cess_account)
                    else:
                        account = COA.get_out(company_id)
                    transaction_list.append([account, "cess_total"], )
                charges = invoice_data.get('co_charges', [])
                total_taxes = invoice_data.get('total_taxes',[])
                for tax in total_taxes:
                    if tax['coa_id']:
                        tax['coa_id'] = COA.get_account(tax['coa_id'])

                    try:
                        del tax['id']
                    except:
                        pass

                    obj = CoaCharges.objects.create(
                        **tax
                    )
                    amount = float(tax.get('amount', 0))
                    name = tax.get('name',None)
                    coa = obj.coa_id
                    if not coa:
                        if "IGST" in name:
                            coa = COA.get_output_igst_account(company_id)
                        elif "CGST" in name:
                            coa = COA.get_output_cgst_account(company_id)
                        elif "SGST" in name:
                            coa = COA.get_output_sgst_account(company_id)
                    if amount != 0:
                        if amount < 0:
                            obj.credit = abs(amount)
                            obj.debit = abs(amount)
                            TO_COA_OBJ = coa
                            FROM_COA_OBJ = account_receivable
                        else:
                            obj.debit = abs(amount)
                            obj.credit = abs(amount)
                            TO_COA_OBJ = account_receivable
                            FROM_COA_OBJ = coa
                        MasterTransaction.objects.create(
                            L1detail_id=invoice_id.invoice_id,
                            L1detailstbl_name='Invoice',
                            main_module='Sales',
                            module='Invoice',
                            sub_module='Tax Charges',
                            transc_deatils='Invoice',
                            banking_module_type='Invoice',
                            journal_module_type='Invoice',
                            trans_date=invoice_data["invoice_date"],
                            trans_status='Manually Added',
                            debit=abs(amount),
                            to_account=TO_COA_OBJ.coa_id,
                            to_acc_type=TO_COA_OBJ.account_type,
                            to_acc_head=TO_COA_OBJ.account_head,
                            to_acc_subhead=TO_COA_OBJ.account_subhead,
                            to_acc_name=TO_COA_OBJ.account_name,
                            credit=abs(amount),
                            from_account=FROM_COA_OBJ.coa_id,
                            from_acc_type=FROM_COA_OBJ.account_type,
                            from_acc_head=FROM_COA_OBJ.account_head,
                            from_acc_subhead=FROM_COA_OBJ.account_subhead,
                            from_acc_name=FROM_COA_OBJ.account_name,
                            customer_id=cust_id,
                            branch_id=branch_id,
                            company_id=company_id)

                    obj.invoice_id = invoice_id
                    obj.save()
                if charges:
                    for charge in charges:
                        charge['coa_id'] = COA.get_account(charge['coa_id'])
                        try:
                            del charge['id']
                        except:
                            pass
                        print(charge)
                        obj = CoaCharges.objects.create(
                            **charge
                        )
                        amount = float(charge.get('amount', 0))
                        coa = obj.coa_id
                        if amount != 0:

                            if amount < 0:
                                obj.credit = abs(amount)
                                obj.debit = abs(amount)
                                TO_COA_OBJ = coa
                                FROM_COA_OBJ = account_receivable
                            else:
                                obj.debit = abs(amount)
                                obj.credit = abs(amount)
                                TO_COA_OBJ = account_receivable
                                FROM_COA_OBJ = coa
                            MasterTransaction.objects.create(
                                L1detail_id=invoice_id.invoice_id,
                                L1detailstbl_name='Invoice',
                                main_module='Sales',
                                module='Invoice',
                                sub_module='Invoice',
                                transc_deatils='Invoice',
                                banking_module_type='Invoice',
                                journal_module_type='Invoice',
                                trans_date=invoice_data["invoice_date"],
                                trans_status='Manually Added',
                                debit=abs(amount),
                                to_account=TO_COA_OBJ.coa_id,
                                to_acc_type=TO_COA_OBJ.account_type,
                                to_acc_head=TO_COA_OBJ.account_head,
                                to_acc_subhead=TO_COA_OBJ.account_subhead,
                                to_acc_name=TO_COA_OBJ.account_name,
                                credit=abs(amount),
                                from_account=FROM_COA_OBJ.coa_id,
                                from_acc_type=FROM_COA_OBJ.account_type,
                                from_acc_head=FROM_COA_OBJ.account_head,
                                from_acc_subhead=FROM_COA_OBJ.account_subhead,
                                from_acc_name=FROM_COA_OBJ.account_name,
                                customer_id=cust_id,
                                branch_id=branch_id,
                                company_id=company_id)

                        obj.invoice_id = invoice_id
                        obj.save()
                for transaction in transaction_list:

                    #List Of index added 0 is get Account_name
                    TO_COA = transaction[0]
                    invomast = MasterTransaction.objects.create(
                        L1detail_id=invoice_id.invoice_id,
                        L1detailstbl_name='Invoice',
                        main_module='Sales',
                        module='Invoice',
                        sub_module='General Charges',
                        transc_deatils='Invoice',
                        banking_module_type='Invoice',
                        journal_module_type='Invoice',
                        trans_date=invoice_data["invoice_date"],
                        trans_status='Manually Added',
                        debit=invoice_data[transaction[1]],
                        to_account=account_receivable.coa_id,
                        to_acc_type=account_receivable.account_type,
                        to_acc_head=account_receivable.account_head,
                        to_acc_subhead=account_receivable.account_subhead,
                        to_acc_name=account_receivable.account_name,
                        credit=invoice_data[transaction[1]],
                        from_account=TO_COA.coa_id,
                        from_acc_type=TO_COA.account_type,
                        from_acc_head=TO_COA.account_head,
                        from_acc_subhead=TO_COA.account_subhead,
                        from_acc_name=TO_COA.account_name,
                        company_id=company_id,
                        branch_id=branch_id,
                        customer_id=cust_id)
                    invomast.save()


                # Group BY coa_id and sum of all item values
                for coa_id, amount in coa_amount_dict.items():
                    if not sales_account:
                        sales_account = coa_id
                        TO_COA = COA.objects.get(coa_id=sales_account)
                    else:
                        TO_COA = sales_account
                    invomast = MasterTransaction.objects.create(
                        L1detail_id=invoice_id.invoice_id,
                        L1detailstbl_name='Invoice',
                        main_module='Sales',
                        module='Invoice',
                        sub_module='Invoice',
                        transc_deatils='Invoice',
                        banking_module_type='Invoice',
                        journal_module_type='Invoice',
                        trans_date=invoice_data["invoice_date"],
                        trans_status='Manually Added',
                        debit=amount,
                        to_account=account_receivable.coa_id,
                        to_acc_type=account_receivable.account_type,
                        to_acc_head=account_receivable.account_head,
                        to_acc_subhead=account_receivable.account_subhead,
                        to_acc_name=account_receivable.account_name,
                        credit=amount,
                        from_account=TO_COA.coa_id,
                        from_acc_type=TO_COA.account_type,
                        from_acc_head=TO_COA.account_head,
                        from_acc_subhead=TO_COA.account_subhead,
                        from_acc_name=TO_COA.account_name,
                        company_id=company_id,
                        branch_id=branch_id,
                        customer_id=cust_id)
                    invomast.save()

                if float(invoice_data['discount']) > 0:
                    discount_account = invoice_data.get('discount_account',None)
                    if discount_account:
                        disc_acc = COA.objects.select_for_update().get(coa_id=discount_account, company_id=company_id)
                    else:
                        disc_acc = COA.objects.select_for_update().get(company_id=company_id,
                                                          account_subhead='Other Income',
                                                          account_head='Other Income',
                                                          isdefault=True,
                                                          account_name="Discount")
                    invomast = MasterTransaction.objects.create(
                        L1detail_id=invoice_id.invoice_id,
                        L1detailstbl_name='Invoice',
                        main_module='Sales',
                        module='Invoice',
                        sub_module='Invoice',
                        transc_deatils='Invoice',
                        banking_module_type='Invoice',
                        journal_module_type='Invoice',
                        trans_date=invoice_data["invoice_date"],
                        trans_status='Manually Added',
                        debit=invoice_data['discount'],
                        to_account=disc_acc.coa_id,
                        to_acc_type=disc_acc.account_type,
                        to_acc_head=disc_acc.account_head,
                        to_acc_subhead=disc_acc.account_subhead,
                        to_acc_name=disc_acc.account_name,
                        credit=invoice_data['discount'],
                        from_account=account_receivable.coa_id,
                        from_acc_type=account_receivable.account_type,
                        from_acc_head=account_receivable.account_head,
                        from_acc_subhead=account_receivable.account_subhead,
                        from_acc_name=account_receivable.account_name,
                        company_id=company_id,
                        branch_id=branch_id,
                        customer_id=cust_id)
                    invomast.save()
                serializer = InvoiceSerializer(invoice_id)
                payment_data = invoice_data.get('payment_data',None)
                if payment_data:
                    payment_dict = {
                        "invoice_id":str(invoice_id.invoice_id),
                        "payment_serial":invoice_id.invoice_serial,
                         "amount_due":float(invoice_id.amount_due),
                        "invoice_serial":invoice_id.invoice_serial
                    }
                    payment_data.update(payment_dict)
                    view_obj = new1paymentreceiveViewSet()
                    response = view_obj.handle_post(user, payment_data, None)
                    if response.status_code < 300:
                        return Response(serializer.data,status=201)
                return Response(serializer.data,status=201)
            except Exception as e:
                traceback.print_exc()
                trans.set_rollback(True)
                print(e)
                return Response({"message": str(e)}, status=400)


    def create(self, request, *args, **kwargs):
        # count = Feature.objects.get(user_id=request.user.id).invoice_remaining
        # print(count, 'invoices.............................')
        # if count <= 0:
        #     return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        invoice_data = None
        try:
            invoice_data_converte = request.data['data']
            invoice_data = json.loads(invoice_data_converte)

        except:
            invoice_data = request.data
        print(invoice_data)

        invoice_file_data = request.FILES.get('attach_file')
        user = request.user
        return self.handle_post(user,invoice_data,invoice_file_data)

from rest_framework.views import APIView
class UpdateInvoiceView(APIView):

    permission_classes = [IsAuthenticated,CustomPermission]


    def handle_update(self,user, invoice_data,invoice_file_data,pk):
        with trans.atomic():
            try:
                invoice = Invoice.objects.select_for_update().get(invoice_id=pk)
                comp_id = Company.objects.get(company_id=invoice_data["company_id"])
                branch_id = Branch.objects.get(branch_id=invoice_data["branch_id"])
                ext_id = invoice_data.get('ext_id',None)
                bch_id = invoice_data["branch_id"]
                employee_id = None
                employee_id = invoice_data["emp_id"]
                if employee_id is not None:
                    employee_id = Employee.objects.get(emp_id=employee_id)
                tcs_id = None
                tcs_id = invoice_data['tcs_id']
                if tcs_id is not None:
                    tcs_id = TCS.objects.get(tcs_id=tcs_id)
                try:
                    cust_id = SalesCustomer.objects.get(customer_id=invoice_data["customer_id"])
                except:
                    cust_id = None
                invoice.invoice_items.select_for_update().all().delete()
                # Stock.objects.select_for_update().filter(ref_id=invoice.invoice_id).delete()
                CoaCharges.objects.select_for_update().filter(invoice_id=invoice).delete()
                MasterTransaction.objects.select_for_update().filter(L1detail_id=invoice.invoice_id).delete()
                invoice_data['amount_due'] = invoice_data["total"]
                print(invoice_data["customer_id"],">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",invoice_data,"?????????????????")
                serializer = InvoiceSerializer(invoice, data=invoice_data)

                if serializer.is_valid():
                    invoice_id=serializer.save()
                    # invoice_id.tcs_id = tcs_id
                    # invoice_id.emp_id = employee_id
                    if invoice_file_data:
                        invoice_id.attach_file = invoice_file_data
                    invoice_id.customer_id = cust_id
                    invoice_id.save()

                    # return Response(serializer.errors, status=200)
                else:
                     print(serializer.errors)
                     return Response(serializer.errors, status=400)
                Audit.objects.create(
                    company_id=comp_id,
                    branch_id=branch_id,
                    modified_by=user,
                    audit_modified_date=invoice_data["invoice_date"],
                    module="Invoice",
                    sub_module='Invoice',
                    data=invoice_data
                )

                all_invoice_items = invoice_data["invoice_items"]
                company_id = Company.objects.get(company_id=invoice_data["company_id"])
                invoice_stocks = Stock.objects.filter(
                    ref_id=invoice_id.invoice_id,
                    ref_tblname='Invoice',
                    formname='Invoice',
                    module='Sales',
                    branch_id=invoice_id.branch_id,
                    company_id=invoice_id.company_id,
                    stage='Add Stages'
                )
                prev_stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,
                                  float(stock.quantity),stock.godown_id_id): stock for stock in
                                 invoice_stocks}
                invoice_stk_list = {}
                for item in all_invoice_items:
                    godown_id = item['godown_id']
                    coa=COA.get_account(item["coa_id"])
                    invoice_items = InvoiceItem.objects.create(invoice_id=invoice_id,
                                                               item_id=Item.objects.get(
                                                                   item_id=item["item_id"]),
                                                               coa_id=coa,
                                                               godown_id_id=godown_id,
                                                               godown_name=item['godown_name'],
                                                               item_name=item["item_name"],
                                                               rate=item["rate"],
                                                               quantity=item["quantity"],
                                                               tax_rate=item["tax_rate"],
                                                               tax_name=item["tax_name"],
                                                               tax_type=item["tax_type"],
                                                               sgst_amount=item["sgst_amount"],
                                                               cgst_amount=item["cgst_amount"],
                                                               igst_amount=item["igst_amount"],
                                                               discount=item["discount"],
                                                               cess_rate=item['cess_rate'],
                                                               cess_amount=item['cess_amount'],
                                                               # taxamount=item["taxamount"],
                                                               amount=item["amount"]
                                                               )
                    invoice_items.save()

                    item_obj = Item.objects.get(item_id=item["item_id"])
                    track_inventory = item_obj.track_inventory
                    if track_inventory == True:
                        batches = item['batches']
                        mfg_date = item['mfg_date']
                        expire_date = item['expire_date']
                        if len(batches) == 0:
                            batches.append(None)
                            mfg_date = None
                            expire_date = None
                        invoice_items.batches = batches
                        invoice_items.mfg_date = mfg_date
                        invoice_items.expire_date = expire_date
                        invoice_items.save()
                        stk_in = None
                        stk_out = None

                        remaining_to_sell = float(item["quantity"])

                        for index, batch in enumerate(batches):
                            obj_inv, created = Stock.objects.get_or_create(
                                item_id=item["item_id"],
                                ref_id=invoice_id.invoice_id,
                                ref_tblname='Invoice',
                                formname='Invoice',
                                godown_id_id=godown_id,
                                quantity=round(float(item['quantity']),2),
                                batch_no=batch,
                                mfg_date=mfg_date,
                                expire_date=expire_date,
                                branch_id=invoice_id.branch_id,
                                company_id=invoice_id.company_id,
                                stage='Add Stages',
                                module="Sales"
                            )
                            print(remaining_to_sell)
                            if remaining_to_sell > 0:
                                if False:
                                    if batch is None:

                                        batch_total_stk_in = Batch.objects.get(item_id=item["item_id"],
                                                                               mfg_date=item['mfg_date'],
                                                                               branch_id=bch_id,
                                                                             expire_date = item['expire_date'],
                                                                               batch_no__isnull=True)
                                        batch_total_stk_in = float(batch_total_stk_in.stock_quantity)

                                        print(batch_total_stk_in,"batch_total_stk_in")
                                    else:
                                        batch_total_stk_in = Batch.objects.get(item_id=item["item_id"],
                                                                               mfg_date=item['mfg_date'],
                                                                               expire_date=item['expire_date'],
                                                                               branch_id=bch_id,
                                                                               batch_no=batch)
                                        batch_total_stk_in = float(batch_total_stk_in.stock_quantity)
                                    if not created:
                                        batch_total_stk_in += float(obj_inv.quantity)
                                        print("upoated")
                                    if index == len(batches) - 1:
                                        if (batch_total_stk_in - remaining_to_sell) < 0:
                                            # pass
                                            raise Exception("Stock Not Available")
                                obj_inv.godown_name=item['godown_name']
                                obj_inv.flow_type = 'OUTWARD'
                                obj_inv.item_name = item["item_name"]
                                obj_inv.stock_out = item['quantity']
                                obj_inv.stock_in = 0
                                obj_inv.amount = item["amount"]
                                obj_inv.rate = item["rate"]
                                obj_inv.module_date = invoice_id.created_date
                                obj_inv.date = invoice_data["invoice_date"]
                                obj_inv.save()
                                invoice_stk_list[(obj_inv.item_id, obj_inv.batch_no, obj_inv.expire_date,
                                               obj_inv.mfg_date,float(obj_inv.quantity),obj_inv.godown_id_id)] = obj_inv
                for key, obj in prev_stk_list.items():
                    if key not in invoice_stk_list:
                        print("deleting child")
                        obj.delete()

                # Zero_tax = invoice_data.get('invoice_items')
                # GST_TAX = None
                # GST_TAX = Zero_tax[0]
                #
                # if GST_TAX == Zero_tax[0].get('selected_tax_name') is not None:
                #     GST_TAX = Zero_tax[0].get('selected_tax_name', {}).get('tax_name')
                # else:
                #     pass
                #
                # IGST_TAX = GST_TAX
                # if GST_TAX == 'GST0 [0%]':
                #     Both_Tax = GST_TAX
                #
                # else:
                #     Both_Tax = None
                #
                # if IGST_TAX == 'IGST0 [0%]':
                #     IGST_0 = IGST_TAX
                # else:
                #     IGST_0 = None

                transaction_list = []  # This Empty List added the append
                sales_account = invoice_data.get('sales_account', None)
                party_account = invoice_data.get('party_account', None)
                try:
                    account_receivable = COA.get_account(party_account)
                except:
                    if cust_id:
                        account_receivable = cust_id.coa_id
                    else:
                        account_receivable = COA.get_account_recievables(company_id)
                try:
                    sales_account = COA.get_account(sales_account)
                except:
                    sales_account = None
                if float(invoice_data['tcs_amount']) > 0:
                    tcs_account = invoice_data.get('tcs_account', None)
                    if tcs_account:
                        account = COA.objects.get(coa_id=tcs_account)
                    else:
                        account = COA.get_input_tcs_pay_account(company_id)
                    transaction_list.append([account, "tcs_amount"])
                if float(invoice_data['shipping_charges']) > 0:
                    shipping_account = invoice_data.get('shipping_account', None)
                    if shipping_account:
                        account = COA.objects.get(coa_id=shipping_account)
                    else:
                        account = COA.get_shipping_account(company_id)
                    transaction_list.append([account, "shipping_charges"])
                # if float(invoice_data['cgst_total']) > 0 :
                #     cgst_account = invoice_data.get('cgst_account', None)
                #     if cgst_account:
                #         account = COA.objects.get(coa_id=cgst_account)
                #     else:
                #         account = COA.get_output_cgst_account(company_id)
                #     transaction_list.append([account, "cgst_total"], )
                # if float(invoice_data['sgst_total']) > 0 :
                #     sgst_account = invoice_data.get('sgst_account', None)
                #     if sgst_account:
                #         account = COA.objects.get(coa_id=sgst_account)
                #     else:
                #         account = COA.get_output_sgst_account(company_id)
                #     transaction_list.append([account, "sgst_total"])
                # if float(invoice_data['igst_total']) > 0 :
                #     igst_account = invoice_data.get('igst_account', None)
                #     if igst_account:
                #         account = COA.objects.get(coa_id=igst_account)
                #     else:
                #         account = COA.get_output_igst_account(company_id)
                #     transaction_list.append([account, "igst_total"], )
                if float(invoice_data['cess_total']) > 0:
                    cess_account = invoice_data.get('cess_account', None)
                    if cess_account:
                        account = COA.objects.get(coa_id=cess_account)
                    else:
                        account = COA.get_out(company_id)
                    transaction_list.append([account, "cess_total"], )
                charges = invoice_data.get('co_charges', [])
                total_taxes = invoice_data.get('total_taxes', [])
                for tax in total_taxes:
                    if tax['coa_id']:
                        tax['coa_id'] = COA.get_account(tax['coa_id'])

                    try:
                        del tax['id']
                    except:
                        pass

                    obj = CoaCharges.objects.create(
                        **tax
                    )
                    amount = float(tax.get('amount', 0))
                    name = tax.get('name', None)
                    coa = obj.coa_id
                    if not coa:
                        if "IGST" in name:
                            coa = COA.get_output_igst_account(company_id)
                        elif "CGST" in name:
                            coa = COA.get_output_cgst_account(company_id)
                        elif "SGST" in name:
                            coa = COA.get_output_sgst_account(company_id)
                    if amount != 0:
                        if amount < 0:
                            obj.credit = abs(amount)
                            obj.debit = abs(amount)
                            TO_COA_OBJ = coa
                            FROM_COA_OBJ = account_receivable
                        else:
                            obj.debit = abs(amount)
                            obj.credit = abs(amount)
                            TO_COA_OBJ = account_receivable
                            FROM_COA_OBJ = coa
                        MasterTransaction.objects.create(
                            L1detail_id=invoice_id.invoice_id,
                            L1detailstbl_name='Invoice',
                            main_module='Sales',
                            module='Invoice',
                            sub_module='Tax Charges',
                            transc_deatils='Invoice',
                            banking_module_type='Invoice',
                            journal_module_type='Invoice',
                            trans_date=invoice_data["invoice_date"],
                            trans_status='Manually Added',
                            debit=abs(amount),
                            to_account=TO_COA_OBJ.coa_id,
                            to_acc_type=TO_COA_OBJ.account_type,
                            to_acc_head=TO_COA_OBJ.account_head,
                            to_acc_subhead=TO_COA_OBJ.account_subhead,
                            to_acc_name=TO_COA_OBJ.account_name,
                            credit=abs(amount),
                            from_account=FROM_COA_OBJ.coa_id,
                            from_acc_type=FROM_COA_OBJ.account_type,
                            from_acc_head=FROM_COA_OBJ.account_head,
                            from_acc_subhead=FROM_COA_OBJ.account_subhead,
                            from_acc_name=FROM_COA_OBJ.account_name,
                            customer_id=cust_id,
                            branch_id=branch_id,
                            company_id=company_id)

                    obj.invoice_id = invoice_id
                    obj.save()
                if charges:
                    for charge in charges:
                        charge['coa_id'] = COA.objects.get(coa_id=charge['coa_id'])
                        try:
                            del charge['id']
                        except:
                            pass
                        print(charge)
                        obj = CoaCharges.objects.create(
                            **charge
                        )
                        amount = float(charge.get('amount', 0))
                        coa = obj.coa_id
                        if amount != 0:

                            if amount < 0:
                                obj.credit = abs(amount)
                                obj.debit = abs(amount)
                                TO_COA_OBJ = coa
                                FROM_COA_OBJ = account_receivable
                            else:
                                obj.debit = abs(amount)
                                obj.credit = abs(amount)
                                TO_COA_OBJ = account_receivable
                                FROM_COA_OBJ = coa
                            MasterTransaction.objects.create(
                                L1detail_id=invoice_id.invoice_id,
                                L1detailstbl_name='Invoice',
                                main_module='Sales',
                                module='Invoice',
                                sub_module='Invoice',
                                transc_deatils='Invoice',
                                banking_module_type='Invoice',
                                journal_module_type='Invoice',
                                trans_date=invoice_data["invoice_date"],
                                trans_status='Manually Added',
                                debit=abs(amount),
                                to_account=TO_COA_OBJ.coa_id,
                                to_acc_type=TO_COA_OBJ.account_type,
                                to_acc_head=TO_COA_OBJ.account_head,
                                to_acc_subhead=TO_COA_OBJ.account_subhead,
                                to_acc_name=TO_COA_OBJ.account_name,
                                credit=abs(amount),
                                from_account=FROM_COA_OBJ.coa_id,
                                from_acc_type=FROM_COA_OBJ.account_type,
                                from_acc_head=FROM_COA_OBJ.account_head,
                                from_acc_subhead=FROM_COA_OBJ.account_subhead,
                                from_acc_name=FROM_COA_OBJ.account_name,
                                customer_id=cust_id,
                                branch_id=branch_id,
                                company_id=company_id)

                        obj.invoice_id = invoice_id
                        obj.save()
                for transaction in transaction_list:
                    # List Of index added 0 is get Account_name
                    TO_COA =  transaction[0]
                    MasterTransaction.objects.create(
                        L1detail_id=invoice_id.invoice_id,
                        L1detailstbl_name='Invoice',
                        main_module='Sales',
                        module='Invoice',
                        sub_module='Invoice',
                        transc_deatils='Invoice',
                        banking_module_type='Invoice',
                        journal_module_type='Invoice',
                        trans_date=invoice_data["invoice_date"],
                        trans_status='Manually Added',
                        debit=invoice_data[transaction[1]],
                        to_account=account_receivable.coa_id,
                        to_acc_type=account_receivable.account_type,
                        to_acc_head=account_receivable.account_head,
                        to_acc_subhead=account_receivable.account_subhead,
                        to_acc_name=account_receivable.account_name,
                        credit=invoice_data[transaction[1]],
                        from_account=TO_COA.coa_id,
                        from_acc_type=TO_COA.account_type,
                        from_acc_head=TO_COA.account_head,
                        from_acc_subhead=TO_COA.account_subhead,
                        from_acc_name=TO_COA.account_name,
                        company_id=company_id,
                        branch_id=branch_id,
                        customer_id=cust_id)
                coa_amount_dict = {}

                for invoice_item in all_invoice_items:
                    if coa_amount_dict.get(invoice_item['coa_id']) is None:
                        coa_amount_dict[invoice_item['coa_id']] = invoice_item['amount']
                    else:
                        coa_amount_dict[invoice_item['coa_id']] = float(coa_amount_dict[invoice_item['coa_id']]) + float(invoice_item['amount'])
                for coa_id, amount in coa_amount_dict.items():
                    if not sales_account:
                        sales_account = coa_id
                        TO_COA = COA.get_account(sales_account)
                    else:
                        TO_COA = sales_account
                    MasterTransaction.objects.create(
                            L1detail_id=invoice_id.invoice_id,
                            L1detailstbl_name='Invoice',
                            main_module='Sales',
                            module='Invoice',
                            sub_module='Invoice',
                            transc_deatils='Invoice',
                            banking_module_type='Invoice',
                            journal_module_type='Invoice',
                            trans_date=invoice_data["invoice_date"],
                            trans_status='Manually Added',
                            debit=amount,
                            to_account=account_receivable.coa_id,
                            to_acc_type=account_receivable.account_type,
                            to_acc_head=account_receivable.account_head,
                            to_acc_subhead=account_receivable.account_subhead,
                            to_acc_name=account_receivable.account_name,
                            credit=amount,
                            from_account=TO_COA.coa_id,
                            from_acc_type=TO_COA.account_type,
                            from_acc_head=TO_COA.account_head,
                            from_acc_subhead=TO_COA.account_subhead,
                            from_acc_name=TO_COA.account_name,
                            company_id=company_id,
                        branch_id=branch_id,
                            customer_id=cust_id)
                print(invoice_data['discount'], "discouooooooooooooooooooooooooont")
                if float(invoice_data['discount']) > 0:

                    discount_account = invoice_data.get('discount_account', None)
                    if discount_account:
                        disc_acc = COA.get_account(discount_account)
                    else:
                        disc_acc = COA.objects.get(company_id=company_id,
                                                   account_subhead='Other Income',
                                                   account_head='Other Income',
                                                   isdefault=True,
                                                   account_name="Discount")
                    MasterTransaction.objects.create(
                        L1detail_id=invoice_id.invoice_id,
                        L1detailstbl_name='Invoice',
                        main_module='Sales',
                        module='Invoice',
                        sub_module='Invoice',
                        transc_deatils='Invoice',
                        banking_module_type='Invoice',
                        journal_module_type='Invoice',
                        trans_date=invoice_data["invoice_date"],
                        trans_status='Manually Added',
                        debit=invoice_data['discount'],
                        to_account=disc_acc.coa_id,
                        to_acc_type=disc_acc.account_type,
                        to_acc_head=disc_acc.account_head,
                        to_acc_subhead=disc_acc.account_subhead,
                        to_acc_name=disc_acc.account_name,
                        credit=invoice_data['discount'],
                        from_account=account_receivable.coa_id,
                        from_acc_type=account_receivable.account_type,
                        from_acc_head=account_receivable.account_head,
                        from_acc_subhead=account_receivable.account_subhead,
                        from_acc_name=account_receivable.account_name,
                        company_id=company_id,
                        branch_id=branch_id,
                        customer_id=cust_id)
                payment_data = invoice_data.get('payment_data', None)

                if payment_data:
                    pr_id = PR.objects.get(invoice_id=invoice_id)
                    payment_dict = {
                        "invoice_id": str(invoice_id.invoice_id),
                        "payment_serial": invoice_id.invoice_serial,
                        "amount_due": float(invoice_id.amount_due),
                        "invoice_serial": invoice_id.invoice_serial
                    }
                    payment_data.update(payment_dict)
                    view_obj = UpdtPaymentRCvViewset()
                    response = view_obj.handle_update(user,payment_data, None, pr_id.pr_id)
                    if response.status_code < 300:
                        return Response(serializer.data, status=201)
                return Response(serializer.data,status=200)
            except Exception as e:
                traceback.print_exc()
                trans.set_rollback(True)
                print(e)
                return Response({"message": 'Stock Not Available'}, status=400)
    def put(self, request, pk):
        invoice_file_data = None
        try:
            invoice_data = request.data['data']
            invoice_data = json.loads(invoice_data)
            invoice_file_data = request.FILES.get('attach_file')
        except:
            invoice_data = request.data
        user = request.user
        return self.handle_update(user,invoice_data,invoice_file_data,pk)

@api_view(['GET'])
def getAllInvoicedetails(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Invoice.objects.count()}

    queryset = Invoice.objects.all()[offset:offset + limit]
    serializer = InvoiceSerializer(queryset, many=True)

    response['results'] = InvoiceSerializer(queryset, many=True).data
    return Response(response)





@api_view(['GET'])


def ShortInvoiceDetails(request):
    invoice = Invoice.objects.all()
    serializer = ShortInvoiceSerializer(invoice, many=True)
    return Response(serializer.data)

@api_view(['GET'])


def getAllPeginatedInvoiceDetails(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Invoice.objects.count()}

    queryset = Invoice.objects.all()[offset:offset + limit]
    serializer = ShortInvoiceSerializer(queryset, many=True)

    response['results'] = ShortInvoiceSerializer(queryset, many=True).data
    return Response(response)





@api_view(['GET'])


def getinvoiceitembyinvoiceid(request, invoice_id):
    object = InvoiceItem.objects.filter(invoice_id=invoice_id)
    serializer = reports2AInvoiceItemSerializer(object, many=True)
    return Response(serializer.data)





    
    
@api_view(['PUT'])


def updateinvoice(request, invoice_id):
    invoice = Invoice.objects.get(invoice_id=invoice_id)
    serializer=InvoiceSerializer(instance=invoice,data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.invoice_serial=serializer.data[''],
        serializer.save()
        print('Yes')
        
    return Response(serializer.data)



# Get Invoice details by Invoice Number 
@api_view(['GET'])

#
def getInvoiceDetailsByInvoice_Serial(request, company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    invoice_serial = request.GET['serial']
    invs = Invoice.objects.filter(company_id=company_id,branch_id=branch_id,invoice_serial__icontains=invoice_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": invs.count()}
    
    instance = invs[offset:offset + limit]
    serializer = invoiceshortbycompanySerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)




#getitemshortbycompanyid
@api_view(['GET'])


def getInvoiceshortbyCustomer_name(request,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    customer_name = request.GET['name']
    invs = Invoice.objects.filter(company_id=company_id,branch_id=branch_id,customer_id__customer_name__icontains=customer_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": invs.count()}
    
    instance = invs[offset:offset + limit]
    

    instance = invoiceshortbycompanySerializer(instance, many=True)
    
    response['results'] = instance.data
    return Response(response)


@api_view(['GET'])

def getCurrentInvoiceId(request,comp_id,branch_id):
    company  = Company.objects.get(company_id=comp_id)
    return Response({"invoice_serial":company.invoice_sequence},status=200)