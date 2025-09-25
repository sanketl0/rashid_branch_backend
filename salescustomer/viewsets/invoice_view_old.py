
import os
import json 

from io import BytesIO
import datetime
from rest_framework import viewsets,generics,mixins
from rest_framework.response import Response
from company.models import Company
from wsgiref.util import FileWrapper

from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.views.generic import View
from salescustomer.printing.generate_invoice import generate_invoice_pdf
from utility import render_to_pdf
from re import template
from operator import itemgetter
from xhtml2pdf import pisa
from salescustomer.models.Invoice_model import Invoice
from salescustomer.serializers.Invoice_serializers import JoinInvoiceAndInvoiceItemSerializer,InvoiceAndInvoiceItem2ASerializer,invoiceshortbycompanySerializer,InvoiceSerializer,ShortInvoiceSerializer,reports2AInvoiceItemSerializer
from salescustomer.models.Salescustomer_model import SalesCustomer
from salescustomer.serializers.Salescustomer_serializers import InvoicebyCustomerSerializer
from transaction.models import MasterTransaction
from coa.models import COA
from item.models.item_model import Item
from item.models.stock_model import Stock
from salescustomer.models.Employee_model import Employee
from salescustomer.models.Invoice_item_model import InvoiceItem
from salescustomer.serializers.Invoice_item_serializers import InvoiceItemSerializer
from utility import save_attach_file

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
##############
# get invoice api


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

#Invoice Pdf Download Function 
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
            return_data['attach_file'] = 'salescustomer/invoicefile_download/{}/'.format(
                pk)
            return Response({
                'data': return_data
            })
        return self.list(request)







# invoiceshortbycompanyid

####################################################
@api_view(['GET'])


def invoiceshortbycompanyid(request, comp_id):
    # invoice = Invoice.objects.all().order_by('created_date')

    company = Company.objects.get(company_id=comp_id)
    invoice = Invoice.objects.filter(
        company_id=company).order_by('created_date')
    serializer = invoiceshortbycompanySerializer(invoice, many=True)

    return Response(serializer.data)

#########################################################
@api_view(['GET'])


def download_inv(request, comp_id, invoice_id):
    # invoice = Invoice.objects.all().order_by('created_date')
    company = Company.objects.get(company_id=comp_id)
    inv = Invoice.objects.get(invoice_id=invoice_id)
    invoice = Invoice.objects.filter(
        company_id=comp_id, invoice_id=invoice_id).order_by('created_date')
    #serializer = invoiceshortbycompanySerializer(invoice, many=True)
    serializers = JoinInvoiceAndInvoiceItemSerializer(invoice, many=True)
    output_pdf = f'INV_{datetime.datetime.now().timestamp()}.pdf'
    generate_invoice_pdf(data=serializers.data,output_path=os.path.join("media",output_pdf))
    
    
    if output_pdf:
        http = 'https' if request.is_secure() else 'http'
        pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadinvoice/{output_pdf}'
    else:
        pdf_url = 'File Not found'
     # give pdf url to download path
    response = pdf_url
# return Response(response)
    return Response(response)


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
   
        response_dict = {"invoice_id":invoice_id,"invoice_serial":invoice_serial,"customer_id":customer_id}
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


def download_inv(request, comp_id, invoice_id):
    # invoice = Invoice.objects.all().order_by('created_date')
    company = Company.objects.get(company_id=comp_id)
    inv = Invoice.objects.get(invoice_id=invoice_id)
    invoice = Invoice.objects.filter(
        company_id=comp_id, invoice_id=invoice_id).order_by('created_date')
    #serializer = invoiceshortbycompanySerializer(invoice, many=True)
    serializers = JoinInvoiceAndInvoiceItemSerializer(invoice, many=True)
    output_pdf = f"INV_{datetime.datetime.now().timestamp()}.pdf"
    generate_invoice_pdf(data=serializers.data,output_path=os.path.join("media", output_pdf))
    
## here we use if function to check where whether the file is exist on media file or not
## here we give full output path (os.path.join("media", output_pdf))
    if os.path.exists(os.path.join("media", output_pdf)):
        http = 'https' if request.is_secure() else 'http'
        pdf_url = f'{http}://{request.get_host()}/salescustomer/Downloadinvoice/{output_pdf}'
    else:
        pdf_url = 'File Not found'
     # give pdf url to download path
    response = pdf_url
# return Response(response)
    return Response(response)


def download_invoice(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:
    response = FileResponse(open(file_path, 'rb'))
    # response = FileResponse(file_data, as_attachment=True,
    return response





# Inoice Creation Section
class new3invoiceitemsViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

    permission_classes=[IsAuthenticated]
    # here is the entry for invoice
    def create(self, request, *args, **kwargs):
        invoice_data_converte = request.data['data']
        user=request.user
        print('HIIIIIIII USER DATA',user,)
        
        """_summary_

        Returns:
            _type_: _description_
        """
        # Invoice Convert Str to Dict Code
        invoice_data = json.loads(invoice_data_converte)
        # invoice_data = request.data['data']

        invoice_file_data = request.FILES.get('attach_file')
        print("  //////////////////////////// invoice_file_data", type(invoice_file_data))
       

        # Branch_id=invoice_data["branch_id"]
        # if Branch_id is not None:
        #     Branch_id=Branch.objects.get(branch_id=Branch_id)

        all_invoice_items = invoice_data["invoice_items"]
        company_id = Company.objects.get(company_id=invoice_data["company_id"])
        cust_id = SalesCustomer.objects.get(
        customer_id=invoice_data["customer_id"])
        employee_id = invoice_data["emp_id"]
        if employee_id is not None:
            employee_id = Employee.objects.get(emp_id=employee_id)
        # Invoice fields
        # global invoice_id
        # Creating the invoice And Save the Invoice salescustomer_invoice table
        invoice_data['amount_due'] = invoice_data["total"]
        invoice_serializer = InvoiceSerializer(data=invoice_data)
        if invoice_serializer.is_valid():
            invoice_id = invoice_serializer.save()
            invoice_id.attach_file = invoice_file_data
            invoice_id.save()
        else:
            return Response(invoice_serializer.errors)

        # File Rename Code The File is Save By Invoice id
        if invoice_file_data is not None:
            file_ext = os.path.splitext(invoice_file_data.name)[1]
            new_file_path = f'media/Invoice_{invoice_id.invoice_id}{file_ext}'
            pth=save_attach_file(invoice_file_data,new_file_path)
            invoice_id.attach_file = pth
            invoice_id.save()
        items = sorted(all_invoice_items, key=itemgetter('coa_id'))
        print('@@@@@',items)
        
        # Display data grouped by 'coa_id'
        account_receivable = COA.objects.get(company_id=company_id, account_subhead="Account Receivables")
        for item in items:
            print('item is here$$$$$$$',item["coa_id"])
            coa=COA.objects.get(coa_id=item["coa_id"])
            print('coa_type',type(coa))

            # Created the debitnote items entries. for one debitnote many items to be created.
            invoice_items = InvoiceItem.objects.create(invoice_id=invoice_id,
                                                       item_id=Item.objects.get(
                                                           item_id=item["item_id"]),
                                                       coa_id=coa,
                                                       item_name=item["item_name"],
                                                       rate=item["rate"],
                                                       quantity=item["quantity"],
                                                       tax_rate=item["tax_rate"],
                                                       tax_name=item["tax_name"],
                                                       tax_type=item["tax_type"],
                                                       sgst_amount=item["sgst_amount"],
                                                       cgst_amount=item["cgst_amount"],
                                                       igst_amount=item["igst_amount"],
                                                       # taxamount=item["taxamount"],
                                                       amount=item["amount"])
            invoice_items.save()
            
            
            
            
        #This Section is Stock Main Section 
        #All The Value Save In Stock Table Section
        #The Sales Stock Value To Be Decrease means Stock Out field be updated
            #Stock out last rate invoice stock journal all the claculation
            #depends on FIFO Method last rate 
            item_value=Item.objects.get(item_id=item["item_id"])
            items_inventory=invoice_data.get('invoice_items')
            track_inventory=items_inventory[0].get('selected_item_name',{}).get('track_inventory')
            print('inventory',track_inventory)
            if track_inventory==True:
                stk_in=Stock.objects.filter(item_id=item["item_id"]).exclude(stock_in=0).order_by('created_date')
                stk_out=Stock.objects.filter(item_id=item["item_id"]).exclude(stock_out=0).order_by('created_date')        
              
                print(stk_out)
                stock_int_items = stk_in
                already_stock_out_items =stk_out
                item_to_sell = item["quantity"]

                # -------------------------------------------------

                # Check if the stock is available
                sum_of_stock_in = sum([_.stock_in for _ in stock_int_items])
                sum_of_stock_in_amount = sum([_.amount for _ in stock_int_items])
                print("sum_of_stock_in_amount", sum_of_stock_in_amount)

                sum_of_already_stock_out = sum([_.stock_out for _ in already_stock_out_items])
                print("sum_of_already_stock_out", sum_of_already_stock_out)

                if sum_of_stock_in - (sum_of_already_stock_out + item_to_sell) < 0:
                    print("Stock not available")
                    return Response('Stock is not Avilable')

                print("Stock available")
                current_stock=sum_of_stock_in-sum_of_already_stock_out
                print('item is herer',item_value.item_id)        
                current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
                print("current Assets_vlaue",current_assets_last_stock.amount)
                future_stock_outs = []
                for stock_in_item in stock_int_items:
                    print(stock_in_item)
                    if item_to_sell==0:
                        break
                    if sum_of_already_stock_out - stock_in_item.stock_in >= 0:
                        print("\tItem fully sold")
                        sum_of_already_stock_out = sum_of_already_stock_out - stock_in_item.stock_in
                        print("\tRemaining already sold items: ", sum_of_already_stock_out)
                        continue

                    if sum_of_already_stock_out > 0:
                        print("\tItem partially unsold")
                        remaining_unsold_items = stock_in_item.stock_in - sum_of_already_stock_out
                        print("\tRemaining unsold items", remaining_unsold_items)
                        sum_of_already_stock_out = 0
                    else:
                        print("\tItem fully unsold")
                        remaining_unsold_items = stock_in_item.stock_in
                    
                    if item_to_sell > remaining_unsold_items:
                        print("\tMore items need to be sold")
                        print(f"\tSelling {remaining_unsold_items} items")
                        
                        future_stock_outs=Stock.objects.create(
                        item_id=item["item_id"],
                        item_name=item["item_name"],
                        stock_out=remaining_unsold_items,
                        ref_id=invoice_id.invoice_id,
                        amount=current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate,
                        rate=current_assets_last_stock.rate,
                        ref_tblname='Invoice',
                        quantity=remaining_unsold_items,
                        #stock_on_hand=current_stock-remaining_unsold_items,
                        formname='Invoice',
                        stage='Add Stages',
                        date=invoice_data["invoice_date"],                
                        company_id=company_id)
                        current_assets_last_stock.amount = current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate
                        current_stock = current_stock-remaining_unsold_items
                        
                            
                        #Stock(0, remaining_unsold_items, stock_in_item.rate)
                        item_to_sell = item_to_sell - remaining_unsold_items
                        print(f"\t{item_to_sell} still needed by the buyer")
                    else:
                        print(f"\tSelling {item_to_sell} items")
                        future_stock_outs=Stock.objects.create(
                        item_id=item["item_id"],
                        item_name=item["item_name"],
                        stock_out=item_to_sell,
                        ref_id=invoice_id.invoice_id,
                        amount=current_assets_last_stock.amount- item_to_sell*stock_in_item.rate,
                        rate=current_assets_last_stock.rate,
                        quantity=item_to_sell,
                        ref_tblname='Invoice',
                        #stock_on_hand=current_stock-item_to_sell,
                        module='Sales',
                        formname='Invoice',
                        stage='Add Stages',
                        date=invoice_data["invoice_date"],                
                        company_id=company_id)
                        
                        #append(Stock(0, item_to_sell, stock_in_item.rate))
                        item_to_sell = 0
                        

                    print("------------")
               
            #This Section Is Stock Journal Transaction 
            #Stock Charetd Account name is Inventory Assets
            #item select time has three chart of account must be
            #Sales Account,Purchase Account ,Inventory Accounts
            
                    inv_item=invoice_data.get('invoice_items')
                    purchase_account=inv_item[0].get('selected_item_name').get('purchase_account')
                    inventory_account=inv_item[0].get('selected_item_name').get('inventory_account')
                    if purchase_account is not None:           
                        TO_COA = COA.objects.get(company_id=company_id,coa_id=purchase_account)
                    else:
                        print("No Chart of Account Found")
                    if inventory_account is not None:
                        FROM_COA=COA.objects.get(company_id=company_id,coa_id=inventory_account)
                    else:
                        print("No Chart of Account Found")
                        
                    print('item rate',future_stock_outs.rate)
                    print('item quantity',future_stock_outs.quantity)
                    stkmast = MasterTransaction.objects.create(
                        L1detail_id=invoice_id.invoice_id,
                        L1detailstbl_name='Invoice',
                        L2detail_id=future_stock_outs.st_id,
                        L2detailstbl_name='Stock',
                        main_module='Sales',
                        module='Invoice',
                        sub_module='Invoice',
                        transc_deatils='Invoice',
                        banking_module_type='Invoice',
                        journal_module_type='Invoice',
                        trans_date=invoice_data["invoice_date"],
                        trans_status='Manually Added',
                        debit=future_stock_outs.rate*future_stock_outs.quantity,
                        to_account=TO_COA.coa_id,
                        to_acc_type=TO_COA.account_type,
                        to_acc_head=TO_COA.account_head,
                        to_acc_subhead=TO_COA.account_subhead,
                        to_acc_name=TO_COA.account_name,
                        credit=future_stock_outs.rate*future_stock_outs.quantity,
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        company_id=company_id,
                        customer_id=cust_id)
                    stkmast.save()
                        
        # 0%GST and 0%IGST Calculation
        Zero_tax=invoice_data.get('invoice_items')
        GST_TAX=None
        GST_TAX=Zero_tax[0]
        
        if GST_TAX==Zero_tax[0].get('selected_tax_name') is not None:
            GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
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

        if float(invoice_data['tcs_amount'])>0:
            transaction_list.append(["TCS Payable","tcs_amount"])
        if float(invoice_data['shipping_charges']) >0:
            transaction_list.append(["Shipping Charges","shipping_charges"])
        if float(invoice_data['cgst_total']) >0 or Both_Tax:
            transaction_list.append(["Output CGST", "cgst_total"],)
        if float(invoice_data['sgst_total'] )>0 or Both_Tax:
            transaction_list.append(["Output SGST", "sgst_total"])
        if float(invoice_data['igst_total']) >0 or IGST_0:
            transaction_list.append(["Output IGST", "igst_total"],)
        for transaction in transaction_list:
            
            #List Of index added 0 is get Account_name
            TO_COA = COA.objects.get(company_id=company_id,account_name=transaction[0])
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
                customer_id=cust_id)
            invomast.save()
            
        # Group By Invoice item
        #Multiple item Send the request Group the coa_id 
        # Invoice item Transaction Changes is the Sum of all Item
        #All The Transaction Sum is Store Credit and Debit Side
        coa_amount_dict = {}
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',type(invoice_items))
        for invoice_item in all_invoice_items:

            print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
            print(type(invoice_item))
            if coa_amount_dict.get(invoice_item['coa_id']) is None:
                coa_amount_dict[invoice_item['coa_id']
                                ] = invoice_item['amount']
            else:
                coa_amount_dict[invoice_item['coa_id']
                                ] = coa_amount_dict[invoice_item['coa_id']] + invoice_item['amount']

        print('''''''',coa_amount_dict)
        # Group BY coa_id and sum of all item values
        for coa_id, amount in coa_amount_dict.items():
            
            TO_COA = COA.objects.get(coa_id=coa_id)
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
                customer_id=cust_id)
            invomast.save()
            
        #Invoice Transaction Discount is Valid to excute this Code
        if invoice_data['discount']!=0:  
            TO_COA = COA.objects.get(company_id=company_id, account_subhead="Account Receivables")
            account_receivable = COA.objects.get(company_id=company_id, account_name="Discount")
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
                to_account=account_receivable.coa_id,
                to_acc_type=account_receivable.account_type,
                to_acc_head=account_receivable.account_head,
                to_acc_subhead=account_receivable.account_subhead,
                to_acc_name=account_receivable.account_name,
                credit=invoice_data['discount'],
                from_account=TO_COA.coa_id,
                from_acc_type=TO_COA.account_type,
                from_acc_head=TO_COA.account_head,
                from_acc_subhead=TO_COA.account_subhead,
                from_acc_name=TO_COA.account_name,
                company_id=company_id,
                customer_id=cust_id)
            invomast.save()
        serializer = InvoiceSerializer(invoice_id)    
        return Response(serializer.data)



#Invoice Pagination Section
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




#This Funaction Are Return All the inovice data
@api_view(['GET'])


def ShortInvoiceDetails(request):
    invoice = Invoice.objects.all()
    serializer = ShortInvoiceSerializer(invoice, many=True)
    return Response(serializer.data)

#Get the Pagination Details
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




#Featching the invoice items Are Invoice id Wise
@api_view(['GET'])


def getinvoiceitembyinvoiceid(request, invoice_id):
    object = InvoiceItem.objects.filter(invoice_id=invoice_id)
    serializer = reports2AInvoiceItemSerializer(object, many=True)
    return Response(serializer.data)



#Invoice Update Section
class InvoiceUpdate4ViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    permission_classes=[IsAuthenticated]
    def update(self, request, pk, *args, **kwargs):
        #dxfxfddfc
        invoice_data=request.data
        invoice = Invoice.objects.get(invoice_id=pk)
        comp_id = Company.objects.get(company_id=invoice_data["company_id"])
        cust_id = SalesCustomer.objects.get(
            customer_id=invoice_data["customer_id"])
        
        #account receivable varibale are declaret the chart of account of to side from item and taxation Section 
        #and Discount time this chartof Account is From Side
        account_receivable = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
        # Invoice Item Looping
        invoice_item_list=[]
        for invoice_item_data in invoice_data['invoice_items']:
            invoice_item_list.append(invoice_item_data['item_id'])
           # Item are find Out Section
            print(invoice_item_data['item_name'])
            try:
                try:
                    invoice_item = InvoiceItem.objects.get(item_id=invoice_item_data['item_id'],invoice_id=invoice.invoice_id)
                    
                except KeyError:
                    invoice_item=None
                    
                  
                                
            except InvoiceItem.DoesNotExist:
                invoice_item=None
            
            # Invoice Item Are Find the update this Code Section   
            if invoice_item is not None:
                item_serializer=InvoiceItemSerializer(invoice_item,data=invoice_item_data)
                if item_serializer.is_valid():
                    item_serializer.save()
                   
            else:
                try:
                    # Get The Chart Of Account and item Id Of the Item Related
                    coa=COA.objects.get(coa_id=invoice_item_data["coa_id"])
                    item=Item.objects.get(item_id=invoice_item_data["item_id"])
                except KeyError:
                    coa=None
                    item=None
                
                try:
                    #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
                    invoice_items = InvoiceItem.objects.create(invoice_id=invoice,
                                                        item_id=item.item_id, 
                                                        coa_id=coa,
                                                        item_name=invoice_item_data["item_name"],
                                                        rate=invoice_item_data["rate"],
                                                        quantity=invoice_item_data["quantity"],
                                                        tax_rate=invoice_item_data["tax_rate"],
                                                        tax_name=invoice_item_data["tax_name"],
                                                        tax_type=invoice_item_data["tax_type"],
                                                        sgst_amount=invoice_item_data["sgst_amount"],
                                                        cgst_amount=invoice_item_data["cgst_amount"],
                                                        igst_amount=invoice_item_data["igst_amount"],
                                                        # taxamount=item["taxamount"],
                                                        amount=invoice_item_data["amount"])
                    invoice_items.save()
                   
                except KeyError:
                    pass                 
                
                    
        print('Not deleted invoice item',invoice_item_list)        
        del_item = InvoiceItem.objects.filter(invoice_id=invoice.invoice_id).exclude(item_id__in=invoice_item_list).delete()  
        #this Section Is Invoice Data Update Serializer Through
        serializer = InvoiceSerializer(invoice, data=invoice_data)

        if serializer.is_valid():
            invoice_id=serializer.save()
            
            # return Response({"data":serializer.data})
        else:
             return Response(serializer.errors, status=400)
        
        stock_item_list=[]
        stock_transactiom_item_list=[]
      
        for invoice_item_stock in invoice_data['invoice_items']:
            stock_item_list.append(invoice_item_stock['item_name'])
            try:
                stock_item=Stock.objects.get(item_id=invoice_item_stock['item_id'],ref_id=invoice)
                item_value=Item.objects.get(item_id=invoice_item_stock["item_id"])
                current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
                # stock_serializer=StockSerializer(stock_item,data=invoice_item_data)
                print("updating stock", invoice_item_stock['quantity'], invoice_item_stock['item_id'])
                stock_item.stock_out=float (invoice_item_stock['quantity'])
                stock_item.rate=float (current_assets_last_stock.rate)
                stock_item.amount=float(current_assets_last_stock.rate) * float(invoice_item_stock['quantity'])
                stock_item.quantity=float (invoice_item_stock['quantity'])
                stock_item.save()
                stock_transactiom_item_list.append(stock_item)
            except Stock.DoesNotExist:
                item_value=Item.objects.get(item_id=invoice_item_stock["item_id"])
                
                
                track_inventory=invoice_item_stock.get('selected_item_name',{}).get('track_inventory')
                print('inventory',track_inventory)
                if track_inventory==True:
                    stk_in=Stock.objects.filter(item_id=invoice_item_stock["item_id"]).exclude(stock_in=0).order_by('created_date')
                    stk_out=Stock.objects.filter(item_id=invoice_item_stock["item_id"]).exclude(stock_out=0).order_by('created_date')        
                
                    print(stk_out)
                    stock_int_items = stk_in
                    already_stock_out_items =stk_out
                    item_to_sell = invoice_item_stock["quantity"]

                    # -------------------------------------------------

                    # Check if the stock is available
                    sum_of_stock_in = sum([_.stock_in for _ in stock_int_items])
                    sum_of_stock_in_amount = sum([_.amount for _ in stock_int_items])
                    print("sum_of_stock_in_amount", sum_of_stock_in_amount)

                    sum_of_already_stock_out = sum([_.stock_out for _ in already_stock_out_items])
                    print("sum_of_already_stock_out", sum_of_already_stock_out)
                    print('sum_of_stock_in',type(sum_of_stock_in),sum_of_stock_in)
                    print('sum_of_already_stock_out',type(sum_of_already_stock_out),sum_of_already_stock_out)
                    print('item_to_sell',type(item_to_sell),item_to_sell)
                    if sum_of_stock_in - (float (sum_of_already_stock_out) +  (item_to_sell)) < 0:
                        print("Stock not available")
                        return Response('Stock is not Avilable')

                    print("Stock available")
                    current_stock=sum_of_stock_in-sum_of_already_stock_out
                    print('item is herer',item_value.item_id)        
                    current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
                    print("current Assets_vlaue",current_assets_last_stock.amount)
                    future_stock_outs = []
                    for stock_in_item in stock_int_items:
                        print(stock_in_item)
                        if item_to_sell==0:
                            break
                        if sum_of_already_stock_out - stock_in_item.stock_in >= 0:
                            print("\tItem fully sold")
                            sum_of_already_stock_out = sum_of_already_stock_out - stock_in_item.stock_in
                            print("\tRemaining already sold items: ", sum_of_already_stock_out)
                            continue

                        if sum_of_already_stock_out > 0:
                            print("\tItem partially unsold")
                            remaining_unsold_items = stock_in_item.stock_in - sum_of_already_stock_out
                            print("\tRemaining unsold items", remaining_unsold_items)
                            sum_of_already_stock_out = 0
                        else:
                            print("\tItem fully unsold")
                            remaining_unsold_items = stock_in_item.stock_in
                        
                        if item_to_sell > remaining_unsold_items:
                            print("\tMore items need to be sold")
                            print(f"\tSelling {remaining_unsold_items} items")
                            
                            future_stock_outs=Stock.objects.create(
                            item_id=invoice_item_stock["item_id"],
                            item_name=invoice_item_stock["item_name"],
                            stock_out=remaining_unsold_items,
                            ref_id=invoice_id,
                            amount=current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate,
                            rate=current_assets_last_stock.rate,
                            ref_tblname='Invoice',
                            quantity=remaining_unsold_items,
                            #stock_on_hand=current_stock-remaining_unsold_items,
                            formname='Invoice',
                            stage='Add Stages',
                            date=invoice_data["invoice_date"],                
                            company_id=comp_id)
                            current_assets_last_stock.amount = current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate
                            current_stock = current_stock-remaining_unsold_items
                            
                                
                        
                            item_to_sell = item_to_sell - remaining_unsold_items
                            print(f"\t{item_to_sell} still needed by the buyer")
                        else:
                            print(f"\tSelling {item_to_sell} items")
                            future_stock_outs=Stock.objects.create(
                            item_id=invoice_item_stock["item_id"],
                            item_name=invoice_item_stock["item_name"],
                            stock_out=item_to_sell,
                            ref_id=invoice_id,
                            amount=current_assets_last_stock.amount- item_to_sell*stock_in_item.rate,
                            rate=current_assets_last_stock.rate,
                            quantity=item_to_sell,
                            ref_tblname='Invoice',
                            #stock_on_hand=current_stock-item_to_sell,
                            module='Sales',
                            formname='Invoice',
                            stage='Add Stages',
                            date=invoice_data["invoice_date"],                
                            company_id=comp_id)
                            
                            
                            item_to_sell = 0
                        

                        print("------------")
                


                            

                        
                    
            
            
                #This Section Is Stock Journal Transaction 
                #Stock Charetd Account name is Inventory Assets
                #item select time has three chart of account must be
                #Sales Account,Purchase Account ,Inventory Accounts
                
                        # inv_item=invoice_data.get('invoice_items')
                        purchase_account=invoice_item_stock.get('selected_item_name').get('purchase_account')
                        inventory_account=invoice_item_stock.get('selected_item_name').get('inventory_account')
                        if purchase_account is not None:           
                            TO_COA = COA.objects.get(company_id=comp_id,coa_id=purchase_account)
                        else:
                            print("No Chart of Account Found")
                        if inventory_account is not None:
                            FROM_COA=COA.objects.get(company_id=comp_id,coa_id=inventory_account)
                        else:
                            print("No Chart of Account Found")
                            
                        print('item rate',future_stock_outs.rate)
                        print('item quantity',future_stock_outs.quantity)
                        stkmast = MasterTransaction.objects.create(
                            L1detail_id=invoice_id.invoice_id,
                            L1detailstbl_name='Invoice',
                            L2detail_id=future_stock_outs.st_id,
                            L2detailstbl_name='Stock',
                            main_module='Sales',
                            module='Invoice',
                            sub_module='Invoice',
                            transc_deatils='Invoice',
                            banking_module_type='Invoice',
                            journal_module_type='Invoice',
                            trans_date=invoice_data["invoice_date"],
                            trans_status='Manually Added',
                            debit=future_stock_outs.rate*future_stock_outs.quantity,
                            to_account=TO_COA.coa_id,
                            to_acc_type=TO_COA.account_type,
                            to_acc_head=TO_COA.account_head,
                            to_acc_subhead=TO_COA.account_subhead,
                            to_acc_name=TO_COA.account_name,
                            credit=future_stock_outs.rate*future_stock_outs.quantity,
                            from_account=FROM_COA.coa_id,
                            from_acc_type=FROM_COA.account_type,
                            from_acc_head=FROM_COA.account_head,
                            from_acc_subhead=FROM_COA.account_subhead,
                            from_acc_name=FROM_COA.account_name,
                            company_id=comp_id,
                            customer_id=cust_id)
                        stkmast.save()
                        print('Sucessfully Added Transaction')
      
       
       
       
       
        # Zero tax Calculation Section
        Zero_tax=invoice_data.get('invoice_items')
        GST_TAX=None
        GST_TAX=Zero_tax[0]
        
        if GST_TAX==Zero_tax[0].get('selected_tax_name') is not None:
            GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
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
            
        #This Section Is The Tax and Shiping Charges ,And tcs Amount is Find the add the
        #transaction_list
        
        transaction_list = [] #This Empty List added the append
        print('Checkit',type(invoice_data['tcs_amount']))
        print('checkit2',invoice_data['tcs_amount'])
        if float(invoice_data['tcs_amount'])>0:
            transaction_list.append(["TCS Payable","tcs_amount"])
        if float(invoice_data['shipping_charges']) >0:
            transaction_list.append(["Shipping Charges","shipping_charges"])
        if float(invoice_data['cgst_total']) >0 or Both_Tax:
            transaction_list.append(["Output CGST", "cgst_total"],)
        if float(invoice_data['sgst_total'] )>0 or Both_Tax:
            transaction_list.append(["Output SGST", "sgst_total"])
        if float(invoice_data['igst_total']) >0 or IGST_0:
            transaction_list.append(["Output IGST", "igst_total"],)
        acc_from_list=[]
        acc_to_list=[]
        #Looping the Added Transaction List Chrat of Account 
        # and this Credit and debit value 
        #this list type is list of list eg: [[Chart of account ,invoicedata[igst_total]]]
        for transaction in transaction_list:
            
            for account_transaction in [transaction[0]]:
                acc_from_list.append(account_transaction)
                if account_transaction is not None:
                    try:
                        #this Section is List Addded Charted Of account Updated                
                        account_list=MasterTransaction.objects.get(from_acc_name=account_transaction,L1detail_id=invoice_id)
                        account_list.credit=invoice_data[transaction[1]]
                        account_list.debit=invoice_data[transaction[1]]
                        account_list.save()
                       
                        
                    except MasterTransaction.DoesNotExist:
                        #List Are Addded New Chart of Account this Code Will be ecxecuted 
                        #Menas New transaction Are Created in Master Transaction Section
                            
                        TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
                        account_receivable = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
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
                            company_id=comp_id,
                            customer_id=cust_id)
                        invomast.save()
                    
        
          
            #  This Sectio Is Discount 
            # Diffrance in Tax Section And Disscount Section Is Tax Side From Account Is Discount Section To Side
            #and Discount From Side Account is Tax Side is To side
            #Change The Credit and Debit side 
            
        print('YYYYYYY code excuted')
        print(invoice_data['discount'])
        try:
            #This Section is Disscount will Be find to this code will Be Excuted
            item_discount_list=MasterTransaction.objects.get(to_acc_name='Discount',L1detail_id=invoice_id)
           
            item_discount_list.credit=invoice_data['discount']
            item_discount_list.debit=invoice_data['discount']
            item_discount_list.save()
            
        
        # This Section List are addded the Disscount Create mastertransaction new entry    
        except MasterTransaction.DoesNotExist:
            if float(invoice_data['discount'])>0:
                acc_to_list.append('Discount') 
                print('ohhhhh Discount Code excuted') 
                TO_COA = COA.objects.get(company_id=comp_id, account_subhead="Account Receivables")
                account_receivable = COA.objects.get(company_id=comp_id, account_name="Discount")
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
                    to_account=account_receivable.coa_id,
                    to_acc_type=account_receivable.account_type,
                    to_acc_head=account_receivable.account_head,
                    to_acc_subhead=account_receivable.account_subhead,
                    to_acc_name=account_receivable.account_name,
                    credit=invoice_data['discount'],
                    from_account=TO_COA.coa_id,
                    from_acc_type=TO_COA.account_type,
                    from_acc_head=TO_COA.account_head,
                    from_acc_subhead=TO_COA.account_subhead,
                    from_acc_name=TO_COA.account_name,
                    company_id=comp_id,
                    customer_id=cust_id)
                invomast.save()
                
    
    
        
       #This Section is Item Transaction The Item transaction Can't Created Is only updated 
       #this only Chnage the Credit and debit Side values 
       #Other can;t Change
    
    
    
    
        #This Section is Item chart of account and amount group by section
        coa_list = []
        coa_amount_dict = {}       
        for invoice_item in invoice_data['invoice_items']:
            
            if coa_amount_dict.get(invoice_item['coa_id']) is None:
                coa_amount_dict[invoice_item['coa_id']
                                ] = invoice_item['amount']
            else:
                coa_amount_dict[invoice_item['coa_id']
                                ] = coa_amount_dict[invoice_item['coa_id']] + invoice_item['amount']
            
        print('coa_amount_dict', coa_amount_dict)
        item_transaction_list = []
        for coa_id, amount in coa_amount_dict.items():
            print('MMMM',coa_id)
            print('@@',invoice_id.invoice_id)
            coa_mast=MasterTransaction.objects.filter(from_account=coa_id,L1detail_id=invoice_id.invoice_id)
            print('WWWWWW',coa_mast)
            for coa in coa_mast:
                
                coa_acc=coa.from_acc_name
                item_transaction_list.append(coa_acc)
                acc_from_list.append(coa_acc)  
                   
        #this Section Is Mastertransction item related 
        # item_transaction_list = [coa_acc]
        
        
        for item_transaction in item_transaction_list:
                      
            item_account_list=MasterTransaction.objects.get(from_acc_name=item_transaction,L1detail_id=invoice_id.invoice_id)
            item_account_list.credit=amount
            item_account_list.debit=amount
            item_account_list.save()
        
        
        
        trans_stock_list= Stock.objects.filter(ref_id=invoice_id).exclude(item_name__in=stock_item_list)
        for trans_stock in trans_stock_list:
            mast_stock=trans_stock.st_id
            transaction_stock= MasterTransaction.objects.filter(L1detail_id=invoice_id,L2detail_id=str(mast_stock)).delete()
            print(transaction_stock)
        del_stock= Stock.objects.filter(ref_id=invoice_id).exclude(item_name__in=stock_item_list).delete()
        
        
     
        
      #this Section Is the Delete the Trnsaction Not Fined is List Mens Remove the Transaction
        #master_stock variable is the remaning of stock item in master transaction
        master_stock_list=[]
        master_stock= MasterTransaction.objects.filter(L1detail_id=invoice_id,L2detailstbl_name='Stock')
        print('account From List')
        for stock_trans_mast in master_stock:
            master_stock_list.append(stock_trans_mast.from_acc_name)
        print('@@@@@@@@@@@@@@@@@@@@',acc_to_list)
        to_and_from=acc_from_list+acc_to_list
        Both_List=to_and_from+master_stock_list
       
        topics = MasterTransaction.objects.filter(L1detail_id=invoice_id).exclude(from_acc_name__in=Both_List).exclude(to_acc_name__in=Both_List).delete()
        print('Both List Is here',Both_List)
        invoice_item_list= InvoiceItem.objects.filter(invoice_id=invoice_id.invoice_id).exclude(item_name__in=stock_item_list).delete()
        serializer = InvoiceSerializer(invoice_id)    
        return Response(serializer.data)
    
#Function base Invoice Update section   
@api_view(['PUT'])


def updateinvoice(request, invoice_id):
    invoice = Invoice.objects.get(invoice_id=invoice_id)
    serializer=InvoiceSerializer(instance=invoice,data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.invoice_serial=serializer.data[''],
        serializer.save()
        print('Yes')
        
    return Response(serializer.data)