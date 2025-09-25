import imp
import os
import json
# from turtle import pd
from rest_framework import viewsets,generics,mixins
from rest_framework.response import Response
from company.models import Company, Branch
from wsgiref.util import FileWrapper
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.views.generic import View
from salescustomer.printing.generate_cn import generate_credit_note_pdf
from utility import render_to_pdf
from audit.models import Audit
import pandas as pd

from salescustomer.models.Creditnote_model import CreditNote
from salescustomer.serializers.Creditnote_serializers import CreditNoteSerializer,ShortCreditNoteSerializer,JoinCreditNoteItemSerializer,CreditNoteonlyserializer
from company.serializers import CompanySerializer

from transaction.models import MasterTransaction,CoaCharges
from transaction.serializers import MasterTransactionSerializer
from salescustomer.models.Credit_item_model import CreditItem
from salescustomer.serializers.Credit_item_serializers import CreditNoteItemSerializer,CnItemSerializer
from salescustomer.models.Tcs_model import TCS
from salescustomer.models.Invoice_model import Invoice
from salescustomer.models.Salescustomer_model import SalesCustomer
from item.models.item_model import Item
from item.models.stock_model import Stock
from coa.models import COA
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from salescustomer.models.So_model import SO
from django.db import transaction
from django.db.models import Q


#Credit Note File Download Class Section
class CreditnoteFileDownloadListAPIView(generics.ListAPIView):
    
    def get(self, request, creditnote_id, format=None):
        queryset = CreditNote.objects.get(cn_id=creditnote_id)
        #Credit Note id Wise Featch The records
        if queryset.attach_file:
            #Geting the Attach File
            file_handle = queryset.attach_file.path
            if os.path.exists(file_handle):
                document = open(file_handle, 'rb')
                response = HttpResponse(FileWrapper(
                    document), content_type='application/msword')
                response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
                #File is Found 
                return response
            else:
                return HttpResponse("File Not Found")
        else:
            return HttpResponse("No File Found")


#######################################################

#Credit note Generating the PDF File
class CreditnoteGeneratePdf(View):
    def get(self, request, creditnote_id, *args, **kwargs):
        creditnote = CreditNote.objects.get(cn_id=creditnote_id)
        # Get The CreditNote By creditnote id
        # and Then Serialize the data
        serializer = CreditNoteSerializer(creditnote)
        print(serializer.data)
        # get the Company data In CreditNote (company_id) related
        print(creditnote.company_id.company_id)
        company = Company.objects.get(
            company_id=creditnote.company_id.company_id)
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
        # Add the Company and Creditnpte Data in Dictionary (Means Combine the data)
        context.update(dict(serializer.data))
        context.update(dict(company_serializer.data))
        html = template.render(context)

        return HttpResponse(html)


#####################
#credit note Pdf File Download
class CreditnoteDownloadPdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "creditnote_%s.pdf" % ("12341231")
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




#Get ing the All The Credit Note data Featching
@api_view(['GET'])
def creditnoteDetail(request, pk):
    creditnote = CreditNote.objects.get(id=pk)
    serializer = CreditNoteSerializer(creditnote, many=False)
    return Response(serializer.data)

#Function Based Post
@api_view(['POST'])


def creditnoteUpdate(request, pk):
    creditnote = CreditNote.objects.get(id=pk)
    serializer = CreditNoteSerializer(instance=creditnote, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# getshortDetails
@api_view(['GET'])


def ShortCreditNoteDetails(request):
    cn = CreditNote.objects.all()
    serializer = ShortCreditNoteSerializer(cn, many=True)
    return Response(serializer.data)


# cnshortbycompanyid
@api_view(['GET'])


def cnshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    objs = CreditNote.objects.filter(branch_id=branch_id,company_id=comp_id)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": objs.count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        cn = objs.order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = ShortCreditNoteSerializer(cn, many=True).data
    return Response(response)
    
#Sales Credit Note refund



#All Journal Transaction View
#Credit note Journal Transaction data means Credit note related all the 
#transaction get in Master taransaction table
#
n_data=None
@api_view(['GET'])


def salescntransactionshortbycnid(self,form_id):
    form_mast = MasterTransaction.objects.filter(L3detail_id=form_id)
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





# credit note item and credit note join
class CreditNoteItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = CreditNote.objects.all()
    serializer_class = JoinCreditNoteItemSerializer

    
    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data
            print(return_data)
            return Response({
                'data': return_data
            })
        return self.list(request)




# API for Credit Note
@api_view(['GET'])


def creditnoteDetail(request, pk):
    creditnote = CreditNote.objects.get(id=pk)
    serializer = CreditNoteSerializer(creditnote, many=False)
    return Response(serializer.data)


@api_view(['POST'])


def creditnoteUpdate(request, pk):
    creditnote = CreditNote.objects.get(id=pk)
    serializer = CreditNoteSerializer(instance=creditnote, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# api to generate credit note pdf

@api_view(['GET'])


def download_cn_data(request, cn_id):

    cn = CreditNote.objects.select_related('customer_id','company_id').get(
         cn_id=cn_id)

    serializers = JoinCreditNoteItemSerializer(cn)

    html = generate_credit_note_pdf(data=serializers.data)
    return html


def download_cn(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:

    response = FileResponse(open(file_path, 'rb'),as_attachment=True)
    # response = FileResponse(file_data, as_attachment=True,

    return response





#Credit Note Creation Section

class new3creditnoteitemsViewSet(viewsets.ModelViewSet):
    queryset = CreditItem.objects.all()
    serializer_class = CnItemSerializer

    def create(self, request, *args, **kwargs):
        # count = Feature.objects.get(user_id=request.user.id).cn_remaining
        # print(count, 'credit notes')
        # if count <= 0:
        #     return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        try:
            creditnote_data = request.data['data']
            creditnote_data = json.loads(creditnote_data)

        except:
            creditnote_data = request.data
        creditnote_file_data = request.FILES.get('attach_file')
        user = request.user
        return self.handle_post(user,creditnote_data,creditnote_file_data)

    @transaction.atomic
    def handle_post(self,user, creditnote_data,creditnote_file_data):

        # branch_id=creditnote_data["branch_id"]
        # if branch_id is not None:
        #     branch_id=Branch.objects.get(branch_id=branch_id)
        try:    
            tcs_id = creditnote_data["tcs_id"]
            if tcs_id is not None:
                tcs_id = TCS.objects.get(tcs_id=tcs_id)
        except KeyError:
            tcs_id=None
        
        invoice_id=creditnote_data.get("invoice_id")
        if invoice_id is not None:
            invoice_id=Invoice.objects.get(invoice_id=invoice_id)
        else:
            invoice_id = None
            
        ext_id = creditnote_data.get('ext_id',None)
        if not invoice_id:
            inv_serial = 'ext__001'
        else:
            inv_serial=invoice_id.invoice_serial
        
        credit_note_items = creditnote_data["credit_note_items"]
        comp_id = Company.objects.get(company_id=creditnote_data["company_id"])
        branch_id = Branch.objects.get(branch_id=creditnote_data["branch_id"])
        bch_id = creditnote_data["branch_id"]
        # employee_id = Employee.objects.get(emp_id=creditnote_data["emp_id"])
        try:
            cust_id = SalesCustomer.get_account(creditnote_data["customer_id"])
        
        except:
            cust_id = None

        serializer = CreditNoteSerializer(data=creditnote_data)

        if serializer.is_valid():
            creditnote_id = serializer.save()
            print(creditnote_id.total_charges, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            if creditnote_file_data:
                creditnote_id.attach_file = creditnote_file_data
                creditnote_id.save()

            # return Response({"data":serializer.data})
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)

        Audit.objects.create(
            company_id=comp_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=creditnote_data["cn_date"],
            module="CreditNote",
            sub_module='CreditNote',
            data=creditnote_data
        )
        if creditnote_id.is_converted == True:
            print("*********************",creditnote_id. is_converted)
        
          #  Assign the relevant fields from the estimate object to the sales order object:            
            creditnote_id.From_convt_id=creditnote_data['convt_id']
            creditnote_id.From_convt_ref_no=creditnote_data['convt_ref_no']
            creditnote_id.From_convt_serial=creditnote_data['convt_serial']
            creditnote_id.From_is_converted=creditnote_data["is_converted"]
            print("////////////////////////////////////////",creditnote_id.From_is_converted)
            creditnote_id.From_convt_type=creditnote_data['convt_type']
            creditnote_id.save() 
           # salesorder_id.save()
            #get estimate by converted id 
            sales_o= SO.objects.get(so_id=creditnote_data['convt_id'])
            print("sales order Object is Here ",creditnote_data.From_convt_id)
            if sales_o.To_is_converted==False:
                sales_o.To_convt_id=creditnote_data.From_convt_id
                sales_o.To_convt_ref_no=creditnote_data.From_convt_ref_no
                sales_o.To_convt_serial=creditnote_data.From_convt_serial
                sales_o.To_is_converted=creditnote_data.From_is_converted
                sales_o.To_convt_type=creditnote_data.From_convt_type
                sales_o.save()
            else:
                return Response("This Estimate Already Converted")
        #Attached Filed Coe Saving 

        sales_account = creditnote_data.get('sales_account', None)
        party_account = creditnote_data.get('party_account', None)
        try:
            account_receivable = COA.objects.get(coa_id=party_account)
        except:
            if cust_id:
                account_receivable = cust_id.coa_id
            else:
                account_receivable = COA.get_account_recievables(company_id)
        try:
            sales_account = COA.objects.get(coa_id=sales_account)
        except:
            sales_account = None
        #Credit note Item Data Store in Credit Note Items Table
        for item in creditnote_data["credit_note_items"]:
            godown_id = item['godown_id']
            new_credit_note_items = CreditItem.objects.create(cn_id=creditnote_id,
                                                              item_id=Item.objects.get(
                                                                  item_id=item["item_id"]),
                                                              coa_id=COA.objects.get(
                                                                  coa_id=item["coa_id"]),
                                                              item_name=item["item_name"],
                                                              rate=item["rate"],
                                                              godown_id_id=godown_id,
                                                              godown_name=item['godown_name'],
                                                              quantity=item["quantity"],
                                                              tax_rate=item["tax_rate"],
                                                              tax_name=item["tax_name"],
                                                              tax_type=item["tax_type"],
                                                              batches=item['batches'],
                                                            mfg_date = item['mfg_date'],
                                                            expire_date = item['expire_date'],
                                                             # taxamount=item["taxamount"],
                                                              cgst_amount=item['cgst_amount'],
                                                              sgst_amount=item['sgst_amount'],
                                                              igst_amount=item['igst_amount'],
                                                              discount=item["discount"],
                                                              amount=item["amount"])

            new_credit_note_items.save()

            item_obj=Item.objects.get(item_id=item["item_id"])
            # items_inventory=creditnote_data.get('credit_note_items')
            track_inventory=item_obj.track_inventory

            
            #Stock Inventory Management    
            if track_inventory:

                if not item['batches']:
                    batch_no = None
                else:
                    batch_no = item['batches'][0]

                amount = float(item["amount"])

                Stock.objects.create(
                    item_id=item['item_id'],
                    item_name=item["item_name"],
                    stock_out=(-float(item["quantity"])),
                    amount=(-(float(amount))),
                    rate= item["rate"],
                    quantity=float(item["quantity"]),
                    batch_no=batch_no,
                    godown_id_id=godown_id,
                    godown_name=item['godown_name'],
                    flow_type='OUTWARD',
                    expire_date=item['expire_date'],
                    mfg_date=item['mfg_date'],
                    #stock_on_hand=current_stock_on_hand+item["quantity"],
                    ref_id=creditnote_id.cn_id,
                    ref_tblname='CreditNote',
                    module='Sales',
                    formname='Credit Note',
                    stage='Add Stages',
                    date=creditnote_data["cn_date"],
                    module_date=creditnote_id.created_date,
                    branch_id=branch_id,
                    company_id=comp_id)

        

        transaction_list = []
        if float(creditnote_data['tcs_amount']) > 0:
            tcs_account = creditnote_data.get('tcs_account', None)
            if tcs_account:
                account = COA.objects.get(coa_id=tcs_account)
            else:
                account = COA.get_input_tcs_pay_account(comp_id)
            transaction_list.append([account, "tcs_amount"])
        if float(creditnote_data['shipping_charges']) > 0:
            shipping_account = creditnote_data.get('shipping_account', None)
            if shipping_account:
                account = COA.objects.get(coa_id=shipping_account)
            else:
                account = COA.get_shipping_account(comp_id)
            transaction_list.append([account, "shipping_charges"])

        if float(creditnote_data['cess_total']) > 0:
            cess_account = creditnote_data.get('cess_account', None)
            if cess_account:
                account = COA.objects.get(coa_id=cess_account)
            else:
                account = COA.get_out(comp_id)
            transaction_list.append([account, "cess_total"], )
        charges = creditnote_data.get('co_charges', [])
        total_taxes = creditnote_data.get('total_taxes', [])
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
                    coa = COA.get_output_igst_account(comp_id)
                elif "CGST" in name:
                    coa = COA.get_output_cgst_account(comp_id)
                elif "SGST" in name:
                    coa = COA.get_output_sgst_account(comp_id)
            if amount != 0:
                if amount < 0:
                    obj.credit = abs(amount)
                    obj.debit = abs(amount)
                    TO_COA_OBJ = account_receivable
                    FROM_COA_OBJ = coa
                else:
                    obj.debit = abs(amount)
                    obj.credit = abs(amount)
                    TO_COA_OBJ = coa
                    FROM_COA_OBJ = account_receivable
                MasterTransaction.objects.create(
                    L1detail_id=creditnote_id.cn_id,
                    L1detailstbl_name='Credit Note',
                    main_module='Sales',
                    module='Sales',
                    sub_module='Credit Note',
                    transc_deatils='Credit Note',
                    banking_module_type='Credit Note',
                    journal_module_type='Credit Note',
                    trans_date=creditnote_data["cn_date"],
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
                    company_id=comp_id)

            obj.cn_id = creditnote_id
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
                        TO_COA_OBJ = account_receivable
                        FROM_COA_OBJ = coa
                    else:
                        obj.debit = abs(amount)
                        obj.credit = abs(amount)
                        TO_COA_OBJ = coa
                        FROM_COA_OBJ = account_receivable
                    MasterTransaction.objects.create(
                        L1detail_id=creditnote_id.cn_id,
                        L1detailstbl_name='Credit Note',
                        main_module='Sales',
                        module='Sales',
                        sub_module='Credit Note',
                        transc_deatils='Credit Note',
                        banking_module_type='Credit Note',
                        journal_module_type='Credit Note',
                        trans_date=creditnote_data["cn_date"],
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
                        company_id=comp_id)

                obj.cn_id = creditnote_id
                obj.save()
        for transaction in transaction_list:

            #List of index 0 is get the Account name
            TO_COA = transaction[0]
            cnmast = MasterTransaction.objects.create(
                L1detail_id=creditnote_id.cn_id,
                L1detailstbl_name='Credit Note',
                main_module='Sales',
                module='Sales',
                sub_module='Credit Note',
                transc_deatils='Credit Note',
                banking_module_type='Credit Note',
                journal_module_type='Credit Note',
                trans_date=creditnote_data["cn_date"],
                trans_status='Manually added',
                debit=creditnote_data[transaction[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=creditnote_data[transaction[1]],
                from_account=account_receivable.coa_id,
                from_acc_type=account_receivable.account_type,
                from_acc_head=account_receivable.account_head,
                from_acc_subhead=account_receivable.account_subhead,
                from_acc_name=account_receivable.account_name,
                company_id=comp_id,
                branch_id=branch_id,
                customer_id=cust_id)
            cnmast.save()

        # Group By credit note item
        #Multiple item Send the request Group the coa_id 
        # Invoice item Transaction Changes is the Sum of all Item
        #All The Transaction Sum is Store Credit and Debit Side
        coa_amount_dict = {}

        for cn_item in credit_note_items:

            if coa_amount_dict.get(cn_item['coa_id']) is None:
                coa_amount_dict[cn_item['coa_id']
                                ] = float(cn_item['amount'])
            else:
                coa_amount_dict[cn_item['coa_id']
                                ] = float(coa_amount_dict[cn_item['coa_id']]) + float(cn_item['amount'])

        print(coa_amount_dict)
        # Group BY coa_id and sum of all item values
        for coa_id, amount in coa_amount_dict.items():
            if not sales_account:
                sales_account = coa_id
                TO_COA = COA.objects.get(coa_id=sales_account)
            else:
                TO_COA = sales_account

            cnmast = MasterTransaction.objects.create(
                L1detail_id=creditnote_id.cn_id,
                L1detailstbl_name='Credit Note',
                main_module='Sales',
                module='Sales',
                sub_module='Credit Note',
                transc_deatils='Credit Note',
                banking_module_type='Credit Note',
                journal_module_type='Credit Note',
                trans_date=creditnote_data["cn_date"],
                trans_status='Manually added',
                debit=amount,
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=amount,
                from_account=account_receivable.coa_id,
                from_acc_type=account_receivable.account_type,
                from_acc_head=account_receivable.account_head,
                from_acc_subhead=account_receivable.account_subhead,
                from_acc_name=account_receivable.account_name,
                company_id=comp_id,
                branch_id=branch_id,
                customer_id=cust_id)
            cnmast.save()

        #credit note Transaction Discount is Valid to excute this Code
        if float(creditnote_data['discount']) > 0:
            discount_account = creditnote_data.get('discount_account', None)
            if discount_account:
                disc_acc = COA.objects.select_for_update().get(coa_id=discount_account, company_id=comp_id)
            else:
                disc_acc = COA.objects.select_for_update().get(company_id=comp_id,
                                           account_subhead='Other Income',
                                           account_head='Other Income',
                                           isdefault=True,
                                           account_name="Discount")
            cnmast = MasterTransaction.objects.create(
                L1detail_id=creditnote_id.cn_id,
                L1detailstbl_name='Credit Note',
                main_module='Sales',
                module='Sales',
                sub_module='Credit Note',
                transc_deatils='Credit Note',
                banking_module_type='Credit Note',
                journal_module_type='Credit Note',
                trans_date=creditnote_data["cn_date"],
                trans_status='Manually added',
                debit=creditnote_data['discount'],
                to_account=account_receivable.coa_id,
                to_acc_type=account_receivable.account_type,
                to_acc_head=account_receivable.account_head,
                to_acc_subhead=account_receivable.account_subhead,
                to_acc_name=account_receivable.account_name,
                credit=creditnote_data['discount'],
                from_account=disc_acc.coa_id,
                from_acc_type=disc_acc.account_type,
                from_acc_head=disc_acc.account_head,
                from_acc_subhead=disc_acc.account_subhead,
                from_acc_name=disc_acc.account_name,
                company_id=comp_id,
                branch_id=branch_id,
                customer_id=cust_id)
            cnmast.save()

        serializer = CreditNoteSerializer(creditnote_id)
        return Response(serializer.data,status=201)
        



#Pagination Of Credit Note data in extracting Pages
@api_view(['GET'])
def getShortPeginatedCreditNoteDetails(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": CreditNote.objects.count()}

    queryset = CreditNote.objects.all()[offset:offset + limit]
    serializer = ShortCreditNoteSerializer(queryset, many=True)

    response['results'] = ShortCreditNoteSerializer(queryset, many=True).data
    return Response(response)








#Cr edit Note Update Section

class CreditNoteUpdate3ViewSet(viewsets.ModelViewSet):
    queryset = CreditNote.objects.all()
    serializer_class = CreditNoteSerializer


    def update(self, request, pk, *args, **kwargs):
        cn_file_data = None
        try:
            creditnote_data = request.data['data']
            creditnote_data = json.loads(creditnote_data)
            cn_file_data = request.FILES.get('attach_file')
        except:
            creditnote_data = request.data
        user = request.user
        return self.handle_update(user,creditnote_data,cn_file_data,pk)
    @transaction.atomic
    def handle_update(self, user,creditnote_data,cn_file_data, pk):

        creditnote = CreditNote.objects.select_for_update().get(cn_id=pk)
        
        comp_id = Company.objects.get(company_id=creditnote_data["company_id"])
        branch_id = Branch.objects.get(branch_id=creditnote_data["branch_id"])
        bch_id = creditnote_data["branch_id"]
        try:
            cust_id = SalesCustomer.objects.get(
                customer_id=creditnote_data["customer_id"])

        except:
            cust_id = None

        serializer = CreditNoteSerializer(creditnote, data=creditnote_data)

        if serializer.is_valid():
            creditnote_id=serializer.save()

            if cn_file_data:
                creditnote.attach_file = cn_file_data
                creditnote.save()
            
            # return Response({"data":serializer.data})
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        Audit.objects.create(
            company_id=comp_id,
            branch_id=branch_id,
            modified_by=user,
            audit_modified_date=creditnote_data["cn_date"],
            module="CreditNote",
            sub_module='CreditNote',
            data=creditnote_data
        )
        MasterTransaction.objects.select_for_update().filter(L1detail_id=creditnote.cn_id).delete()
        creditnote.credit_note_items.select_for_update().all().delete()
        # Stock.objects.select_for_update().filter(ref_id=creditnote.cn_id).delete()
        # raise Exception("check status")
        sales_account = creditnote_data.get('sales_account', None)
        party_account = creditnote_data.get('party_account', None)
        try:
            account_receivable = COA.get_account(party_account)
        except:
            if cust_id:
                account_receivable = cust_id.coa_id
            else:
                account_receivable = COA.get_account_recievables(comp_id)
        try:
            sales_account = COA.get_account(sales_account)

        except:
            print(sales_account, "here it is ")
            sales_account = None

        credit_stocks = Stock.objects.filter(

            ref_id=creditnote_id.cn_id,
            ref_tblname='CreditNote',
            module='Sales',
            formname='Credit Note',
            stage='Add Stages',
            branch_id=branch_id,
            company_id=comp_id)
        prev_stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,
                          float(stock.quantity),stock.godown_id_id): stock for stock in
                         credit_stocks}
        credit_stk_list = {}
        for item in creditnote_data["credit_note_items"]:
            godown_id = item['godown_id']
            new_credit_note_items = CreditItem.objects.create(cn_id=creditnote_id,
                                                              item_id=Item.objects.get(
                                                                  item_id=item["item_id"]),
                                                              coa_id=COA.objects.get(
                                                                  coa_id=item["coa_id"]),
                                                              item_name=item["item_name"],
                                                              rate=item["rate"],
                                                              batches=item['batches'],
                                                              godown_id_id=godown_id,
                                                              godown_name=item['godown_name'],
                                                              expire_date=item['expire_date'],
                                                              mfg_date=item['mfg_date'],
                                                              quantity=item["quantity"],
                                                              tax_rate=item["tax_rate"],
                                                              tax_name=item["tax_name"],
                                                              tax_type=item["tax_type"],
                                                             # taxamount=item["taxamount"],
                                                              cgst_amount=item['cgst_amount'],
                                                              sgst_amount=item['sgst_amount'],
                                                              igst_amount=item['igst_amount'],
                                                              discount=item["discount"],
                                                              amount=item["amount"])
            item_obj = Item.objects.get(item_id=item["item_id"])
            coa_id = item['coa_id']
            amount = float(item['amount'])

            if sales_account is None:
                TO_COA = COA.get_account(coa_id)
                print(TO_COA, "<<<<<<<<<<<<<<")
            else:
                TO_COA = sales_account
                print(TO_COA, ">>>>>>>>>>>>>>>>>>>>")

            MasterTransaction.objects.create(
                L1detail_id=creditnote_id.cn_id,
                L1detailstbl_name='Credit Note',
                main_module='Sales',
                module='Sales',
                sub_module='Credit Note',
                transc_deatils='Credit Note',
                banking_module_type='Credit Note',
                journal_module_type='Credit Note',
                trans_date=creditnote_data["cn_date"],
                trans_status='Manually added',
                debit=amount,
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=amount,
                from_account=account_receivable.coa_id,
                from_acc_type=account_receivable.account_type,
                from_acc_head=account_receivable.account_head,
                from_acc_subhead=account_receivable.account_subhead,
                from_acc_name=account_receivable.account_name,
                company_id=comp_id,
                branch_id=branch_id,
                customer_id=cust_id)
            track_inventory = item_obj.track_inventory
            if track_inventory:
                if not item['batches']:
                    batch_no = None
                else:
                    batch_no = item['batches'][0]
                credit_obj, created = Stock.objects.get_or_create(
                    item_id=item['item_id'],
                    ref_id=creditnote_id.cn_id,
                    ref_tblname='CreditNote',
                    formname='Credit Note',
                    batch_no=batch_no,
                    godown_id_id=godown_id,
                    mfg_date=item['mfg_date'],
                    expire_date=item['expire_date'],
                    quantity=round(float(item['quantity']),2),
                    branch_id=branch_id,
                    company_id=comp_id,
                    stage='Add Stages',
                    module="Sales"
                )
                credit_obj.godown_name = item['godown_name']
                credit_obj.flow_type = 'OUTWARD'
                credit_obj.item_name = item["item_name"]
                credit_obj.stock_out = (-float(item['quantity']))
                credit_obj.stock_in = 0
                credit_obj.amount = (-(float(amount)))
                credit_obj.rate = item["rate"]
                credit_obj.date = creditnote_data["cn_date"]
                credit_obj.module_date = creditnote_id.created_date
                credit_obj.save()
                credit_stk_list[(credit_obj.item_id, credit_obj.batch_no, credit_obj.expire_date,
                                  credit_obj.mfg_date,float(credit_obj.quantity),credit_obj.godown_id_id)] = credit_obj

        for key, obj in prev_stk_list.items():
            if key not in credit_stk_list:
                print("deleting child")
                obj.delete()

        transaction_list = []
        if float(creditnote_data['tcs_amount']) > 0:
            tcs_account = creditnote_data.get('tcs_account', None)
            if tcs_account:
                account = COA.objects.get(coa_id=tcs_account)
            else:
                account = COA.get_input_tcs_pay_account(comp_id)
            transaction_list.append([account, "tcs_amount"])
        if float(creditnote_data['shipping_charges']) > 0:
            shipping_account = creditnote_data.get('shipping_account', None)
            if shipping_account:
                account = COA.objects.get(coa_id=shipping_account)
            else:
                account = COA.get_shipping_account(comp_id)
            transaction_list.append([account, "shipping_charges"])

        if float(creditnote_data['cess_total']) > 0:
            cess_account = creditnote_data.get('cess_account', None)
            if cess_account:
                account = COA.objects.get(coa_id=cess_account)
            else:
                account = COA.get_out(comp_id)
            transaction_list.append([account, "cess_total"], )
        charges = creditnote_data.get('co_charges', [])
        total_taxes = creditnote_data.get('total_taxes', [])
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
                    coa = COA.get_output_igst_account(comp_id)
                elif "CGST" in name:
                    coa = COA.get_output_cgst_account(comp_id)
                elif "SGST" in name:
                    coa = COA.get_output_sgst_account(comp_id)
            if amount != 0:
                if amount < 0:
                    obj.credit = abs(amount)
                    obj.debit = abs(amount)
                    TO_COA_OBJ = account_receivable
                    FROM_COA_OBJ = coa
                else:
                    obj.debit = abs(amount)
                    obj.credit = abs(amount)
                    TO_COA_OBJ = coa
                    FROM_COA_OBJ = account_receivable
                MasterTransaction.objects.create(
                    L1detail_id=creditnote_id.cn_id,
                    L1detailstbl_name='Credit Note',
                    main_module='Sales',
                    module='Sales',
                    sub_module='Credit Note',
                    transc_deatils='Credit Note',
                    banking_module_type='Credit Note',
                    journal_module_type='Credit Note',
                    trans_date=creditnote_data["cn_date"],
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
                    company_id=comp_id)

            obj.cn_id = creditnote_id
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
                        TO_COA_OBJ = account_receivable
                        FROM_COA_OBJ = coa
                    else:
                        obj.debit = abs(amount)
                        obj.credit = abs(amount)
                        TO_COA_OBJ = coa
                        FROM_COA_OBJ = account_receivable

                    MasterTransaction.objects.create(
                        L1detail_id=creditnote_id.cn_id,
                        L1detailstbl_name='Credit Note',
                        main_module='Sales',
                        module='Credit Note',
                        sub_module='Credit Note',
                        transc_deatils='Credit Note',
                        banking_module_type='Credit Note',
                        journal_module_type='Credit Note',
                        trans_date=creditnote_data["cn_date"],
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
                        company_id=comp_id)

                obj.cn_id = creditnote_id
                obj.save()
        for transaction in transaction_list:
            print(transaction)
            # List of index 0 is get the Account name
            TO_COA = transaction[0]
            cnmast = MasterTransaction.objects.create(
                L1detail_id=creditnote_id.cn_id,
                L1detailstbl_name='Credit Note',
                main_module='Sales',
                module='Sales',
                sub_module='Credit Note',
                transc_deatils='Credit Note',
                banking_module_type='Credit Note',
                journal_module_type='Credit Note',
                trans_date=creditnote_data["cn_date"],
                trans_status='Manually added',
                debit=creditnote_data[transaction[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=creditnote_data[transaction[1]],
                from_account=account_receivable.coa_id,
                from_acc_type=account_receivable.account_type,
                from_acc_head=account_receivable.account_head,
                from_acc_subhead=account_receivable.account_subhead,
                from_acc_name=account_receivable.account_name,
                company_id=comp_id,
                branch_id=branch_id,
                customer_id=cust_id)
            cnmast.save()



        # credit note Transaction Discount is Valid to excute this Code
        if float(creditnote_data['discount']) > 0:
            discount_account = creditnote_data.get('discount_account', None)
            if discount_account:
                disc_acc = COA.objects.select_for_update().get(coa_id=discount_account, company_id=comp_id)
            else:
                disc_acc = COA.objects.select_for_update().get(company_id=comp_id,
                                                               account_subhead='Other Income',
                                                               account_head='Other Income',
                                                               isdefault=True,
                                                               account_name="Discount")
            cnmast = MasterTransaction.objects.create(
                L1detail_id=creditnote_id.cn_id,
                L1detailstbl_name='Credit Note',
                main_module='Sales',
                module='Sales',
                sub_module='Credit Note',
                transc_deatils='Credit Note',
                banking_module_type='Credit Note',
                journal_module_type='Credit Note',
                trans_date=creditnote_data["cn_date"],
                trans_status='Manually added',
                debit=creditnote_data['discount'],
                to_account=account_receivable.coa_id,
                to_acc_type=account_receivable.account_type,
                to_acc_head=account_receivable.account_head,
                to_acc_subhead=account_receivable.account_subhead,
                to_acc_name=account_receivable.account_name,
                credit=creditnote_data['discount'],
                from_account=disc_acc.coa_id,
                from_acc_type=disc_acc.account_type,
                from_acc_head=disc_acc.account_head,
                from_acc_subhead=disc_acc.account_subhead,
                from_acc_name=disc_acc.account_name,
                company_id=comp_id,
                branch_id=branch_id,
                customer_id=cust_id)
            cnmast.save()


        serializer = CreditNoteSerializer(creditnote_id)
        return Response(serializer.data,status=200)

# Get Credit Note details by Credit note serial number  
@api_view(['GET'])


def getCNDetailsByCN_number(request, company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    cn_serial = request.GET['serial']
    credits = CreditNote.objects.filter(company_id=company_id,
                                        branch_id=branch_id,
                                        cn_serial__icontains=cn_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": credits.count()}
    
    instance = credits[offset:offset + limit]
    serializer = ShortCreditNoteSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)




#getitemshortbycompanyid
@api_view(['GET'])


def getCNshortbyCustomer_name(request,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    customer_name = request.GET['name']
    credits = CreditNote.objects.filter(company_id=company_id,
                                        branch_id=branch_id,
                                        customer_id__customer_name__icontains=customer_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": credits.count()}
    
    instance = credits[offset:offset + limit]

    serializer = ShortCreditNoteSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)
