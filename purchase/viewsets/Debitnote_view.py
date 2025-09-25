import json
import os
from wsgiref.util import FileWrapper

from django.template.loader import get_template
from django.views.generic import View
from django.http import HttpResponse, FileResponse
from purchase.printing.generate_dn import generate_dn_pdf

from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from purchase.serializers.Vendor_serializers import VendordDNSerializer
from purchase.models.Debitnote_model import DebitNote,DebitNoteView
from company.models import Company,Company_Year,Branch
from company.serializers import CompanySerializer
from purchase.serializers.Debitnote_serializers import DebitnoteSerializer,ShortDebitNoteSerializer,JoinDebitNoteItemSerializer,FoRPaginationShortDebitNoteSerializer
from purchase.models import DebitItem
from utility import render_to_pdf
from purchase.models.Vendor_model import Vendor
from coa.models import COA
from transaction.models import MasterTransaction,CoaCharges
from purchase.models.Bill_model import Bill
from item.models.item_model import Item
from item.models.stock_model import Stock,Batch,get_inventory_value_rate
from purchase.serializers.DebitItem_serializers import UpdatesDebitnoteItemSerializer
from rest_framework.decorators import api_view
from django.db.models import Q
from audit.models import Audit
import traceback
#Debit note File Download Section
class DebitnoteFileDownloadListAPIView(generics.ListAPIView):

    def get(self, request, debitnote_id, format=None):
        queryset = DebitNote.objects.get(dn_id=debitnote_id)
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

#######################################################

#Debit note Generating the Pdf
class DebitnoteGeneratePdf(View):
    def get(self, request, debitnote_id, *args, **kwargs):
        debitnote = DebitNote.objects.get(dn_id=debitnote_id)
        # Get The Debitnote By debitnote id
        # and Then Serialize the data
        serializer = DebitnoteSerializer(debitnote)
        print(serializer.data)
        # get the Company data In Debitnote (company_id) related
        print(debitnote.company_id.company_id)
        company = Company.objects.get(
            company_id=debitnote.company_id.company_id)
        # Serialize the data in Comapny
        company_serializer = CompanySerializer(company)

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

#Debit Note Download the pdf
class DebitnoteDownloadPdf(View):
    def get(self, request, *args, **kwargs):

        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "debitnote_%s.pdf" % ("12341231")
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

# get credit note journal transaction details by cn id





@api_view(['GET'])

def debitnoteDetail(request, pk):
    debitnote = DebitNote.objects.get(id=pk)
    serializer = DebitnoteSerializer(debitnote, many=False)
    return Response(serializer.data)

#Debit Function Based Post Api
@api_view(['POST'])

def debitnoteUpdate(request, pk):
    debitnote = DebitNote.objects.get(dn_id=pk)
    serializer = DebitnoteSerializer(instance=debitnote, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# dnshortbycompanyid


@api_view(['GET'])
#
def dnshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    objs = DebitNoteView.objects.filter(company_id=comp_id,branch_id=branch_id)
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
    response['results'] = FoRPaginationShortDebitNoteSerializer(items, many=True).data
    return Response(response)

    





# api for get bill by company id and bill id
@api_view(['GET'])

def download_dn_data(request,dn_id):

    dnnote = DebitNote.objects.select_related('vendor_id','company_id').get(
        dn_id=dn_id)
    serializers = JoinDebitNoteItemSerializer(dnnote)
    html = generate_dn_pdf(data=serializers.data)
    return html

def download_dn(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response
################################################################################

#Debit note item All The APi View is use and Attache file dowmloade path retuen in This Class
class DebitNoteItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = DebitNote.objects.all()
    serializer_class = JoinDebitNoteItemSerializer

    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data
            print(return_data['dn_date'])
            return Response({
                'data': return_data
            })
        return self.list(request)


from django.db import transaction as trans
#Debit note Class Serializer
class DebitnoteItemViewSet(viewsets.ModelViewSet):
    queryset = DebitNote.objects.all()
    serializer_class = DebitnoteSerializer

    # here is the entry for dabit note
    def create(self, request, *args, **kwargs):
        try:
            debitnote_data = request.data['data']
            debitnote_data = json.loads(debitnote_data)

        except:
            debitnote_data = request.data
            # debitnote_data=dn_data_converte

        dn_file_data = request.FILES.get('attach_file')
        user = request.user
        return self.handle_post(user,debitnote_data,dn_file_data)

    def handle_post(self,user, debitnote_data, dn_file_data):

        with trans.atomic():
            try:
                debit_note_items = debitnote_data["debit_note_items"]
                vendor_id = debitnote_data["vendor_id"]
                if vendor_id is not None:
                    vendor_id = Vendor.objects.get(vendor_id=vendor_id)

                ext_id = debitnote_data.get('ext_id',None)
                comp_id = debitnote_data["company_id"]

                branch_id = Branch.objects.get(branch_id=debitnote_data['branch_id'])
                if comp_id is not None:
                    comp_id = Company.objects.get(company_id=comp_id)

                company_year_id=debitnote_data.get("company_year_id")
                if company_year_id is not None:
                    company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

                bill_id=debitnote_data.get("bill_id")
                if bill_id is not None:
                    bill_id=Bill.objects.get(bill_id=bill_id)

                # debit note fields
                dn_serializer = DebitnoteSerializer(data=debitnote_data)
                if dn_serializer.is_valid():
                    debitnote_id = dn_serializer.save()
                    debitnote_id.attach_file = dn_file_data
                    debitnote_id.save()
                else:
                    return Response(dn_serializer.errors)
                Audit.objects.create(
                    company_id=comp_id,
                    branch_id=branch_id,
                    created_by=user,
                    audit_created_date=debitnote_data["dn_date"],
                    module="DebitNote",
                    sub_module='DebitNote',
                    data=debitnote_data
                )
                # check if the is_convertwd is true
                if debitnote_id.is_converted == True:
                    if debitnote_id.From_convt_type == "Estimate to Invoice":


                        # Assign the relevant fields from the estimate object to the invoice object:
                        debitnote_id.From_convt_id = debitnote_data['convt_id']
                        debitnote_id.From_convt_ref_no = debitnote_data['convt_ref_no']
                        debitnote_id.From_convt_serial = debitnote_data['convt_serial']
                        debitnote_id.From_is_converted = debitnote_data["is_converted"]
                        print("////////////////////////////////////////", debitnote_id.From_is_converted)
                        debitnote_id.From_convt_type = debitnote_data['convt_type']
                        debitnote_id.save()

                        print("OHHHHHHHHHHHHHHHHH")

                        # Get estimate by converted id
                        est = Bill.objects.get(est_id=debitnote_data['convt_id'])
                        print("estimate Object is Here", debitnote_id.From_convt_id)
                        if not est.To_is_converted:
                            est.To_convt_id = debitnote_data.From_convt_id
                            est.To_convt_ref_no = debitnote_data.From_convt_ref_no
                            est.To_convt_serial = debitnote_data.From_convt_serial
                            est.To_is_converted = debitnote_data.From_is_converted
                            est.To_convt_type = debitnote_data.From_convt_type
                            est.save()
                        else:
                            return Response("This Estimate Already Converted")

                purchase_account = debitnote_data.get('purchase_account', None)
                party_account = debitnote_data.get('party_account', None)
                try:
                    account_payable = COA.get_account(party_account)
                except:
                    if vendor_id:
                        account_payable = vendor_id.coa_id
                    else:
                        account_payable = COA.get_account_paybles(comp_id)
                try:
                    purchase_account = COA.get_account(purchase_account)
                except:
                    purchase_account = None

                for item in debitnote_data['debit_note_items']:
                    godown_id = item['godown_id']
                    # Created the debitnote items entries. for one debitnote many items to be created.
                    debitnoteed_items = DebitItem.objects.create(dn_id=debitnote_id,
                                                                 item_id=Item.objects.get(
                                                                     item_id=item["item_id"]),
                                                                 coa_id=COA.objects.get(
                                                                     coa_id=item["coa_id"]),
                                                                 item_name=item["item_name"],
                                                                 rate=item["rate"],
                                                                 godown_id_id=godown_id,
                                                                 godown_name=item['godown_name'],
                                                                 expire_date=item["expire_date"],
                                                                 mfg_date=item["mfg_date"],
                                                                 batch_no=item["batches"],
                                                                 quantity=item["quantity"],
                                                                 tax_rate=item["tax_rate"],
                                                                 tax_name=item["tax_name"],
                                                                 tax_type=item["tax_type"],
                                                                # taxamount=item["taxamount"],
                                                                 igst_amount=item['igst_amount'],
                                                                 cgst_amount=item['cgst_amount'],
                                                                 sgst_amount=item['sgst_amount'],
                                                                 discount=item['discount'],
                                                                 amount=item["amount"])

                    item_obj=Item.objects.get(item_id=item["item_id"])
                    track_inventory=item_obj.track_inventory
                    inv_item_coa=item_obj.inventory_account
                    if track_inventory:
                        batches = item['batches']
                        mfg_date = item['mfg_date']
                        expire_date = item['expire_date']
                        if len(batches) == 0:
                            batches.append(None)
                            mfg_date = None
                            expire_date = None
                        remaining_to_sell = float(item["quantity"])
                        for index, batch in enumerate(batches):
                            if remaining_to_sell > 0:
                                if False:
                                    if batch is None:
                                        try:
                                            batch_total_stk_in = Batch.objects.get(Q(item_id=item_obj.item_id,
                                                                                     expire_date=expire_date,
                                                                                     mfg_date=mfg_date,
                                                                                     branch_id=debitnote_data['branch_id'],
                                                                                     batch_no__isnull=True))
                                        except Exception as e:
                                            print(f"name => {item['item_name']} , "
                                                  f"item_id => {item_obj.item_id}, "
                                                  f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                                  f"qty => {item['quantity']}")
                                            raise Exception("Batch Item not available")
                                        batch_total_stk_in = float(batch_total_stk_in.stock_quantity)

                                    else:

                                        try:
                                            batch_total_stk_in = Batch.objects.get(item_id=item_obj.item_id,
                                                                                   expire_date=expire_date,
                                                                                   mfg_date=mfg_date,
                                                                                   branch_id=debitnote_data['branch_id'],
                                                                                   batch_no=batch)
                                            batch_total_stk_in = float(batch_total_stk_in.stock_quantity)
                                        except Exception as e:
                                            print(e, "error")
                                            print(f"name => {item['item_name']} , "
                                                  f"item_id => {item_obj.item_id}, branch_id => {branch_id} {expire_date} => {mfg_date}"
                                                  f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                                  f"qty => {item['quantity']},"
                                                  )
                                            raise Exception("Batch Item not available")


                                    if index == len(batches) - 1:
                                        if (batch_total_stk_in - remaining_to_sell) < 0:
                                            print(f"name => {item['item_name']} , "
                                                  f"item_id => {item_obj.item_id}, "
                                                  f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                                  f"qty => {item['quantity']},"
                                                  f"batch_qty => {batch_total_stk_in}")
                                            raise Exception("Stock Not Available")
                                amount = float(item['amount'])
                                Stock.objects.create(
                                    item_id=item["item_id"],
                                    item_name=item["item_name"],
                                    stock_in=(-(float(item['quantity']))),
                                    ref_id=debitnote_id.dn_id,
                                    expire_date=expire_date,
                                    mfg_date=mfg_date,
                                    batch_no=batch,
                                    flow_type='INWARD',
                                    godown_id_id=godown_id,
                                    godown_name=item['godown_name'],
                                    amount=(-(float(amount))),
                                    rate=item["rate"],
                                    ref_tblname='Debit Note',
                                    quantity=item['quantity'],
                                    formname='Debit Note',
                                    module='Purchase',
                                    stage='Add Stages',
                                    date=debitnote_data["dn_date"],
                                    module_date=debitnote_id.created_date,
                                    branch_id=branch_id,
                                    company_id=comp_id)


                transaction_list = [] #This Empty List added the append

                if float(debitnote_data['tcs_amount']) > 0:
                    tcs_account = debitnote_data.get('tcs_account', None)
                    if tcs_account:
                        account = COA.objects.get(coa_id=tcs_account)
                    else:
                        account = COA.get_input_tcs_account(comp_id)
                    transaction_list.append([account, "tcs_amount"], )

                for transaction in transaction_list:
                    FROM_COA = transaction[0]

                    dnmast = MasterTransaction.objects.create(
                        L1detail_id=debitnote_id.dn_id,
                        L1detailstbl_name='Debit Note',
                        main_module='Purchase',
                        module='Purchase',
                        sub_module='DebitNote',
                        transc_deatils='Debit Note Transaction',
                        banking_module_type='Debit Note',
                        journal_module_type='Debit Note',
                        trans_date=debitnote_data["dn_date"],
                        trans_status='Manually Added',
                        debit=debitnote_data[transaction[1]],
                        to_account=account_payable.coa_id,
                        to_acc_type=account_payable.account_type,
                        to_acc_head=account_payable.account_head,
                        to_acc_subhead=account_payable.account_subhead,
                        to_acc_name=account_payable.account_name,
                        credit=debitnote_data[transaction[1]],
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        company_id=comp_id,
                        branch_id=branch_id,
                        vendor_id=vendor_id)
                    dnmast.save()
                total_taxes = debitnote_data.get('total_taxes', [])
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
                            TO_COA_OBJ = coa
                            FROM_COA_OBJ = account_payable
                        else:
                            obj.debit = abs(amount)
                            obj.credit = abs(amount)
                            TO_COA_OBJ = account_payable
                            FROM_COA_OBJ = coa
                        MasterTransaction.objects.create(
                            L1detail_id=debitnote_id.dn_id,
                            L1detailstbl_name='Debit Note',
                            main_module='Purchase',
                            module='Debit Note',
                            sub_module='Debit Note',
                            transc_deatils='Debit Note',
                            banking_module_type='Debit Note',
                            journal_module_type='Debit Note',
                            trans_date=debitnote_data["dn_date"],
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
                            vendor_id=vendor_id,
                            branch_id=branch_id,
                            company_id=comp_id)

                    obj.dn_id = debitnote_id
                    obj.save()
                charges = debitnote_data.get('co_charges', [])
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
                                FROM_COA_OBJ = account_payable
                            else:
                                obj.debit = abs(amount)
                                obj.credit = abs(amount)
                                TO_COA_OBJ = account_payable
                                FROM_COA_OBJ = coa
                            MasterTransaction.objects.create(
                                L1detail_id=debitnote_id.dn_id,
                                L1detailstbl_name='Debit Note',
                                main_module='Purchase',
                                module='Debit Note',
                                sub_module='Debit Note',
                                transc_deatils='Debit Note',
                                banking_module_type='Debit Note',
                                journal_module_type='Debit Note',
                                trans_date=debitnote_data["dn_date"],
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
                                vendor_id=vendor_id,
                                branch_id=branch_id,
                                company_id=comp_id)

                        obj.dn_id = debitnote_id
                        obj.save()

                for debit_note_item in debit_note_items:
                    if not purchase_account:
                        coa_id = debit_note_item["coa_id"] if not debit_note_item["coa_id"] else item_obj.purchase_account
                        TO_COA = COA.get_account(coa_id)
                    else:
                        TO_COA = purchase_account
                    FROM_COA = TO_COA
                    dnmast = MasterTransaction.objects.create(
                        L1detail_id=debitnote_id.dn_id,
                        L1detailstbl_name='Debit Note',
                        main_module='Purchase',
                        module='Purchase',
                        sub_module='Tax Charges',
                        transc_deatils='Debit Note Transaction',
                        banking_module_type='Debit Note',
                        journal_module_type='Debit Note',
                        trans_date=debitnote_data["dn_date"],
                        trans_status='Manually Added',
                        debit=debit_note_item['amount'],
                        to_account=account_payable.coa_id,
                        to_acc_type=account_payable.account_type,
                        to_acc_head=account_payable.account_head,
                        to_acc_subhead=account_payable.account_subhead,
                        to_acc_name=account_payable.account_name,
                        credit=debit_note_item['amount'],
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        company_id=comp_id,
                        branch_id=branch_id,
                        vendor_id=vendor_id)
                    dnmast.save()
                    print('Sucessfully complted')
                transaction_list_tds = []
                #     #amount is debit and credit side
                if float(debitnote_data['tds_amount']) > 0:
                    tds_account = debitnote_data.get('tds_account', None)
                    if tds_account:
                        account = COA.objects.get(coa_id=tds_account)
                    else:
                        account = COA.get_input_tds_account(comp_id)
                    transaction_list_tds.append([account, "tds_amount"], )
                for transaction in transaction_list_tds:
                    print(transaction)

                    TO_COA = transaction[0]
                    billmast = MasterTransaction.objects.create(
                        L1detail_id=bill_id.bill_id,
                        L1detailstbl_name='Debit Note',
                        main_module='Purchase',
                        module='Debit Note',
                        sub_module='General Charges',
                        transc_deatils='Debit Note',
                        banking_module_type='Debit Note',
                        journal_module_type='Debit Note',
                        trans_date=debitnote_data["dn_date"],
                        trans_status='Manually Added',
                        debit=debitnote_data[transaction[1]],
                        to_account=TO_COA.coa_id,
                        to_acc_type=TO_COA.account_type,
                        to_acc_head=TO_COA.account_head,
                        to_acc_subhead=TO_COA.account_subhead,
                        to_acc_name=TO_COA.account_name,
                        credit=debitnote_data[transaction[1]],
                        from_account=account_payable.coa_id,
                        from_acc_type=account_payable.account_type,
                        from_acc_head=account_payable.account_head,
                        from_acc_subhead=account_payable.account_subhead,
                        from_acc_name=account_payable.account_name,
                        vendor_id=vendor_id,
                        branch_id=branch_id,
                        company_id=comp_id)
                    billmast.save()

                #user can select the Discount this block will be excuted
                if float(debitnote_data['discount']) > 0:
                    discount_account = debitnote_data.get('discount_account', None)
                    if discount_account:
                        disc_acc = COA.objects.select_for_update().get(coa_id=discount_account, company_id=comp_id)
                    else:
                        disc_acc = COA.objects.select_for_update().get(company_id=comp_id,
                                                                       account_subhead='Other Income',
                                                                       account_head='Other Income',
                                                                       isdefault=True,
                                                                       account_name="Discount")

                    FROM_COA = account_payable

                    TO_COA = disc_acc
                    dnmast = MasterTransaction.objects.create(
                        L1detail_id=debitnote_id.dn_id,
                        L1detailstbl_name='Debit Note',
                        main_module='Purchase',
                        module='Purchase',
                        sub_module='DebitNote',
                        transc_deatils='Debit Note Transaction',
                        banking_module_type='Debit Note',
                        journal_module_type='Debit Note',
                        trans_date=debitnote_data["dn_date"],
                        trans_status='Manually Added',
                        debit=debitnote_data['discount'],
                        to_account=TO_COA.coa_id,
                        to_acc_type=TO_COA.account_type,
                        to_acc_head=TO_COA.account_head,
                        to_acc_subhead=TO_COA.account_subhead,
                        to_acc_name=TO_COA.account_name,
                        credit=debitnote_data['discount'],
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        branch_id=branch_id,
                        company_id=comp_id,
                        vendor_id=vendor_id)
                    dnmast.save()
                serializer = DebitnoteSerializer(debitnote_id)  # browser

                return Response(serializer.data,status=201)
            except Exception as e:
                print(e)
                traceback.print_exc()
                trans.set_rollback(True)
                return Response({"message": 'Stock Not Available'}, status=400)
#endregion
#End Debit Note Section        




#get the debit note status by vendor id
@api_view(['GET'])

def getdnstatusopenbyvendorid(request,pk):
   queryset = Vendor.objects.get(pk=pk)
   serializer=VendordDNSerializer(queryset)
   return Response(serializer.data)






#Debit note item by dn id through featch the data
@api_view(['GET'])

def getdebitnoteitembydn_id(request, dn_id):
    object = DebitItem.objects.filter(dn_id=dn_id)
    serializer = UpdatesDebitnoteItemSerializer(object, many=True)
    return Response(serializer.data)        



from django.db import transaction as trans
#Debit note update Section
class DebitnoteUpdate3ViewSet(viewsets.ModelViewSet):
    queryset = DebitNote.objects.all()
    serializer_class = DebitnoteSerializer

    def update(self, request, pk, *args, **kwargs):
        dn_file_data = None
        debitnote_data = None
        try:
            debitnote_data = request.data['data']
            debitnote_data = json.loads(debitnote_data)
            dn_file_data = request.FILES.get('attach_file')
        except:
            debitnote_data = request.data
        user = request.user
        return self.handle_update(user,debitnote_data,dn_file_data,pk)

    def handle_update(self, user,debitnote_data,dn_file_data, pk):
        with trans.atomic():
            try:
                debitnote = DebitNote.objects.get(dn_id=pk)
                comp_id = Company.objects.get(company_id=debitnote_data["company_id"])

                branch_id = Branch.objects.get(branch_id=debitnote_data["branch_id"])
                ext_id = debitnote_data.get('ext_id',None)
                try:
                    vendor_id = Vendor.objects.get(
                        vendor_id=debitnote_data["vendor_id"])
                except:
                    vendor_id = None
                debitnote.debit_note_items.all().delete()
                # Stock.objects.filter(ref_id=debitnote.dn_id).delete()

                MasterTransaction.objects.filter(L1detail_id=debitnote.dn_id).delete()

                serializer = DebitnoteSerializer(debitnote, data=debitnote_data)

                if serializer.is_valid():
                    debitnote_id=serializer.save()
                    if dn_file_data:
                        debitnote.attach_file = dn_file_data
                        debitnote.save()

                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=400)

                Audit.objects.create(
                    company_id=comp_id,
                    branch_id=branch_id,
                    modified_by=user,
                    audit_modified_date=debitnote_data["dn_date"],
                    module="DebitNote",
                    sub_module='DebitNote',
                    data=debitnote_data
                )
                purchase_account = debitnote_data.get('purchase_account', None)
                party_account = debitnote_data.get('party_account', None)
                try:
                    account_payable = COA.get_account(party_account)
                except:
                    if vendor_id:
                        account_payable = vendor_id.coa_id
                    else:
                        account_payable = COA.get_account_paybles(comp_id)
                try:
                    purchase_account = COA.get_account(purchase_account)
                except:
                    purchase_account = None
                debit_stocks = Stock.objects.filter(
                    ref_id=debitnote_id.dn_id,
                    ref_tblname='Debit Note',
                    formname='Debit Note',
                    module='Purchase',
                    branch_id=branch_id,
                    company_id=comp_id,
                    stage='Add Stages'
                )
                prev_stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,
                                  float(stock.quantity),stock.godown_id_id): stock for stock in
                                 debit_stocks}
                debit_stk_list = {}
                for item in debitnote_data['debit_note_items']:
                    godown_id = item['godown_id']
                    # Created the debitnote items entries. for one debitnote many items to be created.
                    debitnoteed_items = DebitItem.objects.create(dn_id=debitnote_id,
                                                                 item_id=Item.objects.get(
                                                                     item_id=item["item_id"]),
                                                                 coa_id=COA.objects.get(
                                                                     coa_id=item["coa_id"]),
                                                                 item_name=item["item_name"],
                                                                 rate=item["rate"],
                                                                 expire_date=item["expire_date"],
                                                                 mfg_date=item["mfg_date"],
                                                                 batch_no=item["batches"],
                                                                 godown_id_id=godown_id,
                                                                 godown_name=item['godown_name'],
                                                                 quantity=item["quantity"],
                                                                 tax_rate=item["tax_rate"],
                                                                 tax_name=item["tax_name"],
                                                                 tax_type=item["tax_type"],
                                                                 # taxamount=item["taxamount"],
                                                                 igst_amount=item['igst_amount'],
                                                                 cgst_amount=item['cgst_amount'],
                                                                 sgst_amount=item['sgst_amount'],
                                                                 discount=item['discount'],
                                                                 amount=item["amount"])

                    item_obj = Item.objects.get(item_id=item["item_id"])
                    track_inventory = item_obj.track_inventory
                    if track_inventory:
                        batches = item['batches']
                        mfg_date = item['mfg_date']
                        expire_date = item['expire_date']
                        if len(batches) == 0:
                            batches.append(None)
                            mfg_date = None
                            expire_date = None
                        remaining_to_sell = float(item["quantity"])
                        for index, batch in enumerate(batches):
                            obj_debit, created = Stock.objects.get_or_create(
                                item_id=item['item_id'],
                                ref_id=debitnote_id.dn_id,
                                ref_tblname='Debit Note',
                                formname='Debit Note',
                                godown_id_id=godown_id,
                                quantity=round(float(item['quantity']),2),
                                batch_no=batch,
                                mfg_date=mfg_date,
                                expire_date=expire_date,
                                branch_id=branch_id,
                                company_id=comp_id,
                                stage='Add Stages',
                                module="Purchase"
                            )
                            if remaining_to_sell > 0:
                                if False:
                                    if batch is None:
                                        try:
                                            batch_total_stk_in = Batch.objects.get(Q(item_id=item_obj.item_id,
                                                                                     expire_date=expire_date,
                                                                                     mfg_date=mfg_date,
                                                                                     branch_id=debitnote_data['branch_id'],
                                                                                     batch_no__isnull=True))
                                        except Exception as e:
                                            print(f"name => {item['item_name']} , "
                                                  f"item_id => {item_obj.item_id}, "
                                                  f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                                  f"qty => {item['quantity']}")
                                            raise Exception("Batch Item not available")
                                        batch_total_stk_in = float(batch_total_stk_in.stock_quantity)

                                    else:

                                        try:
                                            batch_total_stk_in = Batch.objects.get(item_id=item_obj.item_id,
                                                                                   expire_date=expire_date,
                                                                                   mfg_date=mfg_date,
                                                                                   branch_id=debitnote_data['branch_id'],
                                                                                   batch_no=batch)
                                            batch_total_stk_in = float(batch_total_stk_in.stock_quantity)
                                        except Exception as e:
                                            print(e, "error")
                                            print(f"name => {item['item_name']} , "
                                                  f"item_id => {item_obj.item_id}, branch_id => {branch_id} {expire_date} => {mfg_date}"
                                                  f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                                  f"qty => {item['quantity']},"
                                                  )
                                            raise Exception("Batch Item not available")
                                    if not created:
                                        batch_total_stk_in += float(obj_debit.quantity)
                                    if index == len(batches) - 1:
                                        if (batch_total_stk_in - remaining_to_sell) < 0:
                                            print(f"name => {item['item_name']} , "
                                                  f"item_id => {item_obj.item_id}, "
                                                  f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                                  f"qty => {item['quantity']},"
                                                  f"batch_qty => {batch_total_stk_in}")
                                            raise Exception("Stock Not Available")

                                amount = float(item["rate"]) * float(item['quantity'])
                                obj_debit.godown_name = item['godown_name']
                                obj_debit.flow_type = 'INWARD'
                                obj_debit.item_name = item["item_name"]
                                obj_debit.stock_in = (-(float(item['quantity'])))
                                obj_debit.stock_out = 0
                                obj_debit.amount = (-(float(item['amount'])))
                                obj_debit.rate = item["rate"]
                                obj_debit.quantity = float(item['quantity'])
                                obj_debit.date = debitnote_data["dn_date"]
                                obj_debit.module_date=debitnote_id.created_date
                                obj_debit.save()
                                debit_stk_list[(obj_debit.item_id, obj_debit.batch_no, obj_debit.expire_date,
                                               obj_debit.mfg_date, float(item['quantity']),obj_debit.godown_id_id)] = obj_debit

                for key, obj in prev_stk_list.items():
                    print(key,debit_stk_list,"*************")
                    if key not in debit_stk_list:
                        print("deleting child")
                        obj.delete()

                transaction_list = []  # This Empty List added the append
                transaction_list = []  # This Empty List added the append

                if float(debitnote_data['tcs_amount']) > 0:
                    tcs_account = debitnote_data.get('tcs_account', None)
                    if tcs_account:
                        account = COA.objects.get(coa_id=tcs_account)
                    else:
                        account = COA.get_input_tcs_account(comp_id)
                    transaction_list.append([account, "tcs_amount"], )
                for transaction in transaction_list:
                    FROM_COA = transaction[0]
                    # transaction list of index is 0
                    dnmast = MasterTransaction.objects.create(
                        L1detail_id=debitnote_id.dn_id,
                        L1detailstbl_name='Debit Note',
                        main_module='Purchase',
                        module='Purchase',
                        sub_module='DebitNote',
                        transc_deatils='Debit Note Transaction',
                        banking_module_type='Debit Note',
                        journal_module_type='Debit Note',
                        trans_date=debitnote_data["dn_date"],
                        trans_status='Manually Added',
                        debit=debitnote_data[transaction[1]],
                        to_account=account_payable.coa_id,
                        to_acc_type=account_payable.account_type,
                        to_acc_head=account_payable.account_head,
                        to_acc_subhead=account_payable.account_subhead,
                        to_acc_name=account_payable.account_name,
                        credit=debitnote_data[transaction[1]],
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        company_id=comp_id,
                        branch_id=branch_id,
                        vendor_id=vendor_id)
                total_taxes = debitnote_data.get('total_taxes', [])
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
                            TO_COA_OBJ = coa
                            FROM_COA_OBJ = account_payable
                        else:
                            obj.debit = abs(amount)
                            obj.credit = abs(amount)
                            TO_COA_OBJ = account_payable
                            FROM_COA_OBJ = coa
                        MasterTransaction.objects.create(
                            L1detail_id=debitnote_id.dn_id,
                            L1detailstbl_name='Debit Note',
                            main_module='Purchase',
                            module='Debit Note',
                            sub_module='Tax Charges',
                            transc_deatils='Debit Note',
                            banking_module_type='Debit Note',
                            journal_module_type='Debit Note',
                            trans_date=debitnote_data["dn_date"],
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
                            vendor_id=vendor_id,
                            branch_id=branch_id,
                            company_id=comp_id)

                    obj.dn_id = debitnote_id
                    obj.save()
                charges = debitnote_data.get('co_charges', [])
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
                                FROM_COA_OBJ = account_payable
                            else:
                                obj.debit = abs(amount)
                                obj.credit = abs(amount)
                                TO_COA_OBJ = account_payable
                                FROM_COA_OBJ = coa
                            MasterTransaction.objects.create(
                                L1detail_id=debitnote_id.dn_id,
                                L1detailstbl_name='Debit Note',
                                main_module='Purchase',
                                module='Debit Note',
                                sub_module='General Charges',
                                transc_deatils='Debit Note',
                                banking_module_type='Debit Note',
                                journal_module_type='Debit Note',
                                trans_date=debitnote_data["dn_date"],
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
                                vendor_id=vendor_id,
                                branch_id=branch_id,
                                company_id=comp_id)

                        obj.dn_id = debitnote_id
                        obj.save()
                for debit_note_item in debitnote_data['debit_note_items']:
                    if not purchase_account:
                        purchase_account = debit_note_item["coa_id"] if not debit_note_item[
                            "coa_id"] else item_obj.purchase_account
                        TO_COA = COA.objects.get(coa_id=purchase_account)
                    else:
                        TO_COA = purchase_account
                    FROM_COA = TO_COA
                    dnmast = MasterTransaction.objects.create(
                        L1detail_id=debitnote_id.dn_id,
                        L1detailstbl_name='Debit Note',
                        main_module='Purchase',
                        module='Purchase',
                        sub_module='DebitNote',
                        transc_deatils='Debit Note Transaction',
                        banking_module_type='Debit Note',
                        journal_module_type='Debit Note',
                        trans_date=debitnote_data["dn_date"],
                        trans_status='Manually Added',
                        debit=debit_note_item['amount'],
                        to_account=account_payable.coa_id,
                        to_acc_type=account_payable.account_type,
                        to_acc_head=account_payable.account_head,
                        to_acc_subhead=account_payable.account_subhead,
                        to_acc_name=account_payable.account_name,
                        credit=debit_note_item['amount'],
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        company_id=comp_id,
                        branch_id=branch_id,
                        vendor_id=vendor_id)
                    dnmast.save()
                transaction_list_tds = []
                if float(debitnote_data['tds_amount']) > 0:
                    tds_account = debitnote_data.get('tds_account', None)
                    if tds_account:
                        account = COA.objects.get(coa_id=tds_account)
                    else:
                        account = COA.get_input_tds_account(comp_id)
                    transaction_list_tds.append([account, "tds_amount"], )
                    for transaction in transaction_list_tds:
                        print(transaction)

                        TO_COA = transaction[0]
                        billmast = MasterTransaction.objects.create(
                            L1detail_id=bill_id.bill_id,
                            L1detailstbl_name='Debit Note',
                            main_module='Purchase',
                            module='Debit Note',
                            sub_module='Debit Note',
                            transc_deatils='Debit Note',
                            banking_module_type='Debit Note',
                            journal_module_type='Debit Note',
                            trans_date=debitnote_data["dn_date"],
                            trans_status='Manually Added',
                            debit=debitnote_data[transaction[1]],
                            to_account=TO_COA.coa_id,
                            to_acc_type=TO_COA.account_type,
                            to_acc_head=TO_COA.account_head,
                            to_acc_subhead=TO_COA.account_subhead,
                            to_acc_name=TO_COA.account_name,
                            credit=debitnote_data[transaction[1]],
                            from_account=account_payable.coa_id,
                            from_acc_type=account_payable.account_type,
                            from_acc_head=account_payable.account_head,
                            from_acc_subhead=account_payable.account_subhead,
                            from_acc_name=account_payable.account_name,
                            vendor_id=vendor_id,
                            branch_id=branch_id,
                            company_id=comp_id)
                        billmast.save()
                if float(debitnote_data['discount']) > 0:
                    discount_account = debitnote_data.get('discount_account', None)
                    if discount_account:
                        disc_acc = COA.objects.select_for_update().get(coa_id=discount_account, company_id=comp_id)
                    else:
                        disc_acc = COA.objects.select_for_update().get(company_id=comp_id,
                                                                       account_subhead='Other Income',
                                                                       account_head='Other Income',
                                                                       isdefault=True,
                                                                       account_name="Discount")

                    FROM_COA = account_payable

                    TO_COA = disc_acc
                    MasterTransaction.objects.create(
                        L1detail_id=debitnote_id.dn_id,
                        L1detailstbl_name='Debit Note',
                        main_module='Purchase',
                        module='Purchase',
                        sub_module='DebitNote',
                        transc_deatils='Debit Note Transaction',
                        banking_module_type='Debit Note',
                        journal_module_type='Debit Note',
                        trans_date=debitnote_data["dn_date"],
                        trans_status='Manually Added',
                        debit=debitnote_data['discount'],
                        to_account=TO_COA.coa_id,
                        to_acc_type=TO_COA.account_type,
                        to_acc_head=TO_COA.account_head,
                        to_acc_subhead=TO_COA.account_subhead,
                        to_acc_name=TO_COA.account_name,
                        credit=debitnote_data['discount'],
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        company_id=comp_id,
                        branch_id=branch_id,
                        vendor_id=vendor_id)


                serializer = DebitnoteSerializer(debitnote_id)  # browser
                return Response(serializer.data)
            except:
                traceback.print_exc()
                trans.set_rollback(True)
                return Response({"message": 'Stock Not Available'}, status=400)
    
    
# Get search details by po serial number
@api_view(['GET'])

def getDNDetailsBydn_serial(request, company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    dn_serial = request.GET['serial']
    dns = DebitNoteView.objects.filter(company_id=company_id,
                                   branch_id=branch_id,
                                   dn_serial__icontains=dn_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": dns.count()}
    
    instance = dns[offset:offset + limit]
    serializer = FoRPaginationShortDebitNoteSerializer(instance, many=True)
    response['results'] =serializer.data
    return Response(response)


@api_view(['GET'])

def getDNDetailsByvendor_name(request, company_id,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    vendor_name = request.GET['name']
    dns = DebitNoteView.objects.filter(company_id=company_id,
                                   branch_id=branch_id,
                                   vendor_id__vendor_name__icontains=vendor_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": dns.count()}

    instance = dns[offset:offset + limit]
    serializer = FoRPaginationShortDebitNoteSerializer(instance, many=True)
    response['results'] = serializer.data
    return Response(response)