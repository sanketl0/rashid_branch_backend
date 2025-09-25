import json
import os
import datetime
from wsgiref.util import FileWrapper
from django.template.loader import get_template
from django.views.generic import View
from django.http import HttpResponse, FileResponse

from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from purchase.models.Bill_model import Bill,BillView
from company.models import Company,Company_Year,Branch
from company.serializers import CompanySerializer
from purchase.serializers.Bill_serializers import BillItemSerializer,BillSerializer,JoinBillAndBillItemSerializer,billbyvendorSerializer,ForPaginationJoinBillAndBillItemSerializer
from rest_framework.views import APIView
from purchase.models.Vendor_model import Vendor
from purchase.printing.generate_bill import generate_bill_pdf
from item.models.item_model import Item
from item.models.stock_model import Stock
from coa.models import COA
from purchase.models.Tds_model import TDS
from purchase.models.Bill_Item_model import Bill_Item
from salescustomer.models.Tcs_model import TCS
from transaction .models import MasterTransaction,ChargeTransaction,CoaCharges

from utility import render_to_pdf
from purchase.serializers.Bill_Item_serializers import GETBillItemSerializer
from audit.models import Audit
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from purchase.models.Po_model import PO
from django.db import transaction
from registration.models import Feature
from django.db.models import Q

#Bill File Download Section
class BillFileDownloadListAPIView(generics.ListAPIView):
    
    def get(self, request, bill_id, format=None):
        queryset = Bill.objects.get(bill_id=bill_id)
        if queryset.attach_file:
            #Get the Attach file
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
        
        
#Generate the pdf bill
class BillGeneratePdf(View):
    def get(self, request, bill_id, *args, **kwargs):
        bill = Bill.objects.get(bill_id=bill_id)
        # Get The Bill By bill id
        # and Then Serialize the data
        serializer = BillSerializer(bill)
        print(serializer.data)
        # get the Company data In Estimate (company_id) related
        print(bill.company_id.company_id)
        company = Company.objects.get(company_id=bill.company_id.company_id)
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

#Biill Download In Pdf
class BillDownloadPdf(View):
    def get(self, request, *args, **kwargs):

        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "bill_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)

        # rendering the template

        with open(pdf_path, 'r') as f:
            file_data = f.read()

        # sending response
        response = FileResponse(file_data, as_attachment=True,
                                filename='hello.pdf', content_type='application/pdf')
        response['Content-Disposition'] = content
        return response


########################################################################################################################
# Bill and Item join
class BillItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Bill.objects.all()
    serializer_class = JoinBillAndBillItemSerializer

    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data
            return Response({
                'data': return_data
            })
        return self.list(request)


import time

#Get the Bill By Company Id Wise
@api_view(['GET'])

def billshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    start = time.time()
    objs = BillView.objects.filter(company_id=comp_id,branch_id=branch_id)
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": objs.count()
    }


    items = objs[offset:offset + limit]

    # Serialize the items and return the paginated response
    response['results'] = ForPaginationJoinBillAndBillItemSerializer(items, many=True).data
    end = time.time()
    print(f"time take is {end-start}")
    return Response(response)



#Bill By Vendor id wise
#Hown Many Bill Of one vendor
@api_view(['GET'])

def Billrefbyvendorid(request, pk):
    vendor = Vendor.objects.get(vendor_id=pk)
    bills=Bill.objects.filter(vendor_id=vendor)
    print('Bills Is here',bills)
    response_list=[]
    for bill in bills:
        bill_id=bill.bill_id
        bill_serial=bill.bill_serial
        vendor_id=bill.vendor_id.vendor_id
   
        response_dict = {"vendor_id":vendor_id,"bill_id":bill_id,"bill_serial":bill_serial}
        response_list.append(response_dict)  
    return Response(response_list)




import time

# api for get bill by company id and bill id
@api_view(['GET'])

def download_bill_data(request, bill_id):


    bl = Bill.objects.select_related('vendor_id','company_id').prefetch_related('charges').get(bill_id=bill_id)
    serializers = JoinBillAndBillItemSerializer(bl)
    output_pdf=f"Bill_{datetime.datetime.now().timestamp()}.pdf"

    html = generate_bill_pdf(data=serializers.data,output_path=os.path.join("media/purchase/",output_pdf))
    return html
#return Response(response)

def download_bl(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response
################################################################################




# get bill by vendor id(Response for this api is its return all invoices as per respective  vendor)


@api_view(['GET'])

def billbyvendorid(request, pk):
    vendor = Vendor.objects.get(vendor=pk)
    # cust_queryset=Customer.objects.prefetch_related()
    print('cust_queryset', vendor)
    # customer=cust_queryset.objects.filter(customer_id=pk)

    print('vendor', vendor)
    serializer = billbyvendorSerializer(vendor, many=False)
    return Response(serializer.data)





#Bill Creation Section
class BillitemsViewSet(viewsets.ModelViewSet):
    queryset = Bill_Item.objects.all()
    serializer_class = BillItemSerializer


    @transaction.atomic
    def handle_post(self, user,bill_data,bill_file_data):
        TCS_id = bill_data.get("tcs_id")
        if TCS_id is not None:
            TCS_id = TCS.objects.get(tcs_id=TCS_id)

        TDS_id = bill_data.get("tds_id")
        if TDS_id is not None:
            TDS_id = TDS.objects.get(tds_id=TDS_id)

            
        comp_id = bill_data["company_id"]
        if comp_id is not None:
            comp_id = Company.objects.get(company_id=comp_id)  
            
            
            
        ven_id = bill_data["vendor_id"]
        if ven_id is not None:
            ven_id = Vendor.objects.get(vendor_id=ven_id)
      
        bch_id= bill_data["branch_id"]
        branch_id = Branch.objects.get(branch_id=bch_id)
        # if Branch_id is not None:
        #     Branch_id=Branch.objects.get(branch_id=Branch_id)

        bill_items = bill_data["bill_items"]
        bill_data['amount_due'] = bill_data["total"]
        print(bill_data)
        bill_serializer = BillSerializer(data=bill_data)
        if bill_serializer.is_valid():
            bill_id=bill_serializer.save()
            bill_id.attach_file = bill_file_data
            bill_id.save()
        else:
            print(bill_serializer.errors)
            return Response(bill_serializer.errors, 400)
        Audit.objects.create(
            company_id=comp_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=bill_data["bill_date"],
            module="Bill",
            sub_module='Bill',
            data=bill_data
        )
        # Bill Fields

        if bill_id.is_converted == True:
            if bill_id.From_convt_type == "PO to Bill":
                print("*********************", bill_id.is_converted)
                
                # Assign the relevant fields from the estimate object to the invoice object:            
                bill_id.From_convt_id = bill_data['convt_id']
                bill_id.From_convt_ref_no = bill_data['convt_ref_no']
                bill_id.From_convt_serial = bill_data['convt_serial']
                bill_id.From_is_converted = bill_data["is_converted"]
                print("////////////////////////////////////////", bill_id.From_is_converted)
                bill_id.From_convt_type = bill_data['convt_type']
                bill_id.save() 
                
                print("OHHHHHHHHHHHHHHHHH")
                
                # Get estimate by converted id 
                po = PO.objects.get(po_id=bill_data['convt_id'])
                print("estimate Object is Here", bill_data.From_convt_id)
                if not po.To_is_converted:
                    po.To_convt_id = bill_data.From_convt_id
                    po.To_convt_ref_no = bill_data.From_convt_ref_no
                    po.To_convt_serial = bill_data.From_convt_serial
                    po.To_is_converted = bill_data.From_is_converted
                    po.To_convt_type = bill_data.From_convt_type
                    po.save()
                else:
                    return Response("This Estimate Already Converted")
        purchase_account = bill_data.get('purchase_account',None)
        party_account = bill_data.get('party_account',None)
        try:
            account_payable = COA.get_account(party_account)
        except:
            if ven_id:
                account_payable = ven_id.coa_id
            else:
                account_payable = COA.get_account_paybles(comp_id)
        try:
            purchase_account = COA.get_account(purchase_account)
        except:
            purchase_account= None
        for items in bill_data["bill_items"]:
            godown_id = items['godown_id']
            item_obj = Item.objects.get(item_id=items["item_id"])
            billed_items = Bill_Item.objects.create(bill_id=bill_id,
                                                    item_id=item_obj,
                                                    coa_id=COA.objects.get(
                                                        coa_id=items["coa_id"]),
                                                    godown_name=items['godown_name'],
                                                    item_name=items["item_name"],
                                                    rate=items["rate"],
                                                    expire_date=items["expire_date"],
                                                    mfg_date=items["mfg_date"],
                                                    batch_no=items["batches"],
                                                    godown_id_id=godown_id,
                                                    quantity=float(items["quantity"]),
                                                    tax_rate=items["tax_rate"],
                                                    tax_name=items["tax_name"],
                                                    tax_type=items["tax_type"],
                                                    cgst_amount=items["cgst_amount"],
                                                    sgst_amount=items["sgst_amount"],
                                                    igst_amount=items["igst_amount"],
                                                    discount=items["discount"],
                                                    cess_rate=items['cess_rate'],
                                                    cess_amount=items['cess_amount'],
                                                    amount=items["amount"])
            billed_items.save()

            track_inventory= item_obj.track_inventory
            amount= float(items['amount'])
            if track_inventory:
                batch = items["batches"]
                exp_date = items["expire_date"]
                mfg_date = items["mfg_date"]
                if not batch:
                    batch.append(None)
                    exp_date = None
                    mfg_date = None
                Stock.objects.create(
                    item_id=items['item_id'],
                    item_name=items["item_name"],
                    stock_in=items["quantity"],
                    amount=amount,
                    rate= items["rate"],
                    quantity=items["quantity"],
                    flow_type='INWARD',
                    godown_id_id=godown_id,
                    godown_name=items['godown_name'],
                    expire_date=exp_date,
                    mfg_date=mfg_date,
                    batch_no=batch[0],
                    ref_id=bill_id.bill_id,
                    module_date=bill_id.created_date,
                    ref_tblname='Bill',
                    module='Purchase',
                    formname='Bill',
                    stage='Add Stages',
                    date=bill_data["bill_date"],
                    branch_id=branch_id,
                    company_id=comp_id)

            if not purchase_account:
                coa_id = items["coa_id"] if not items["coa_id"] else item_obj.purchase_account
                TO_COA = COA.get_account(coa_id)
            else:
                TO_COA = purchase_account
            billmast = MasterTransaction.objects.create(
                L1detail_id=bill_id.bill_id,
                L1detailstbl_name='Bill',
                main_module='Purchase',
                module='Bill',
                sub_module='Bill',
                transc_deatils='Bill',
                banking_module_type='Bill',
                journal_module_type='Bill',
                trans_date=bill_data["bill_date"],
                trans_status='Manually Added',
                debit=amount,
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=amount,
                from_account=account_payable.coa_id,
                from_acc_type=account_payable.account_type,
                from_acc_head=account_payable.account_head,
                from_acc_subhead=account_payable.account_subhead,
                from_acc_name=account_payable.account_name,
                vendor_id=ven_id,
                branch_id=branch_id,
                company_id=comp_id)
            billmast.save()


        bill_data['tds_amount'] = abs(float(bill_data['tds_amount']))
        transaction_list = [] #This Empty List added the append 

        if float(bill_data['tcs_amount'])>0:
            tcs_account = bill_data.get('tcs_account', None)
            if tcs_account:
                account = COA.objects.get(coa_id=tcs_account)
            else:
                account = COA.get_input_tcs_account(comp_id)
            transaction_list.append([account, "tcs_amount"],)
        if float(bill_data['cess_total']) > 0:
            cess_account = bill_data.get('cess_account', None)
            if cess_account:
                account = COA.objects.get(coa_id=cess_account)
            else:
                account = COA.get_input_cess_account(comp_id)
            transaction_list.append([account, "cess_total"], )
        # if float(bill_data['total_charges']) > 0:
        #     transaction_list.append(["Input Charges", "total_charges"], )
        total_taxes = bill_data.get('total_taxes', [])
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
                    TO_COA_OBJ = account_payable
                    FROM_COA_OBJ = coa
                else:
                    obj.debit = abs(amount)
                    obj.credit = abs(amount)
                    TO_COA_OBJ = coa
                    FROM_COA_OBJ = account_payable
                MasterTransaction.objects.create(
                    L1detail_id=bill_id.bill_id,
                    L1detailstbl_name='Bill',
                    main_module='Purchase',
                    module='Bill',
                    sub_module='Tax Charges',
                    transc_deatils='Bill',
                    banking_module_type='Bill',
                    journal_module_type='Bill',
                    trans_date=bill_data["bill_date"],
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
                    vendor_id=ven_id,
                    branch_id=branch_id,
                    company_id=comp_id)

            obj.bill_id = bill_id
            obj.save()
        charges = bill_data.get('co_charges',[])
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
                amount = float(charge.get('amount',0))
                coa = obj.coa_id
                if amount != 0:

                    if amount < 0:
                        obj.credit = abs(amount)
                        obj.debit = abs(amount)
                        TO_COA_OBJ = account_payable
                        FROM_COA_OBJ = coa
                    else:
                        obj.debit = abs(amount)
                        obj.credit = abs(amount)
                        TO_COA_OBJ = coa
                        FROM_COA_OBJ = account_payable
                    MasterTransaction.objects.create(
                    L1detail_id=bill_id.bill_id,
                    L1detailstbl_name='Bill',
                    main_module='Purchase',
                    module='Bill',
                    sub_module='Bill',
                    transc_deatils='Bill',
                    banking_module_type='Bill',
                    journal_module_type='Bill',
                    trans_date=bill_data["bill_date"],
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
                    vendor_id=ven_id,
                    branch_id=branch_id,
                    company_id=comp_id)

                obj.bill_id = bill_id
                obj.save()

        for transaction in transaction_list:
            TO_COA = transaction[0]
            billmast = MasterTransaction.objects.create(
                L1detail_id=bill_id.bill_id,
                L1detailstbl_name='Bill',
                main_module='Purchase',
                module='Bill',
                sub_module='Bill',
                transc_deatils='Bill',
                banking_module_type='Bill',
                journal_module_type='Bill',
                trans_date=bill_data["bill_date"],
                trans_status='Manually Added',
                debit=bill_data[transaction[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=bill_data[transaction[1]],
                from_account=account_payable.coa_id,
                from_acc_type=account_payable.account_type,
                from_acc_head=account_payable.account_head,
                from_acc_subhead=account_payable.account_subhead,
                from_acc_name=account_payable.account_name,
                vendor_id=ven_id,
                branch_id=branch_id,
                company_id=comp_id)
            billmast.save()

        transaction_list_tds=[]
        #Tds View Section tds diff tcs is to Account and From Account is Diffrance
        if float(bill_data['tds_amount'])>0:
            tds_account = bill_data.get('tds_account', None)
            if tds_account:
                account = COA.objects.get(coa_id=tds_account)
            else:
                account = COA.get_input_tds_account(comp_id)
            transaction_list_tds.append([account, "tds_amount"],)
        for transaction in transaction_list_tds:
            TO_COA = transaction[0]
            billmast = MasterTransaction.objects.create(
                L1detail_id=bill_id.bill_id,
                L1detailstbl_name='Bill',
                main_module='Purchase',
                module='Bill',
                sub_module='Bill',
                transc_deatils='Bill',
                banking_module_type='Bill',
                journal_module_type='Bill',
                trans_date=bill_data["bill_date"],
                trans_status='Manually Added',
                debit=bill_data[transaction[1]],
                to_account=account_payable.coa_id,
                to_acc_type=account_payable.account_type,
                to_acc_head=account_payable.account_head,
                to_acc_subhead=account_payable.account_subhead,
                to_acc_name=account_payable.account_name,
                credit=bill_data[transaction[1]],
                from_account=TO_COA.coa_id,
                from_acc_type=TO_COA.account_type,
                from_acc_head=TO_COA.account_head,
                from_acc_subhead=TO_COA.account_subhead,
                from_acc_name=TO_COA.account_name,
                vendor_id=ven_id,
                branch_id=branch_id,
                company_id=comp_id)
            billmast.save()

        if float(bill_data['discount']) > 0:

            discount_account = bill_data.get('discount_account', None)
            if discount_account:
                disc_acc = COA.objects.select_for_update().get(coa_id=discount_account, company_id=company_id)
            else:
                disc_acc = COA.objects.select_for_update().get(company_id=comp_id,
                                                               account_subhead='Other Income',
                                                               account_head='Other Income',
                                                               isdefault=True,
                                                               account_name="Discount")
            TO_COA = account_payable

            billmast = MasterTransaction.objects.create(
                L1detail_id=bill_id.bill_id,
                L1detailstbl_name='Bill',
                main_module='Purchase',
                module='Bill',
                sub_module='Bill',
                transc_deatils='Bill',
                banking_module_type='Bill',
                journal_module_type='Bill',
                trans_date=bill_data["bill_date"],
                trans_status='Manually Added',
                debit=bill_data['discount'],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=bill_data['discount'],
                from_account=disc_acc.coa_id,
                from_acc_type=disc_acc.account_type,
                from_acc_head=disc_acc.account_head,
                from_acc_subhead=disc_acc.account_subhead,
                from_acc_name=disc_acc.account_name,
                vendor_id=ven_id,
                branch_id=branch_id,
                company_id=comp_id)
            billmast.save()
        serializer = BillSerializer(bill_id)  # browser
        return Response(serializer.data,status=201)


    def create(self, request, *args, **kwargs):
        # count = Feature.objects.get(user_id=request.user.id).bill_remaining
        # print(count, 'Bill')
        # if count <= 0:
        #     return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        bill_file_data = None
        try:
            bill_data_converte = request.data['data']
            bill_data = json.loads(bill_data_converte)

        except:
            bill_data = request.data
        # bill_data=bill_data_converte
        bill_file_data = request.FILES.get('attach_file')
        user = request.user
        return self.handle_post(user,bill_data,bill_file_data)



class BillUpdateView(APIView):

    @transaction.atomic
    def handle_update(self,user,bill_data,bill_file_data,pk):


        bill = Bill.objects.get(bill_id=pk)
        comp_id = bill_data["company_id"]
        branch_id = Branch.objects.get(branch_id=bill_data["branch_id"])

        if comp_id is not None:
            comp_id = Company.objects.get(company_id=comp_id)
        ven_id = bill_data["vendor_id"]
        if ven_id is not None:
            ven_id = Vendor.objects.get(vendor_id=ven_id)

        # delete related data
        bill.bill_items.all().delete()
        CoaCharges.objects.filter(bill_id=bill).delete()
        # Stock.objects.filter(ref_id=bill.bill_id).delete()
        MasterTransaction.objects.filter(L1detail_id=bill.bill_id).delete()
        bill_items = bill_data["bill_items"]
        bill_data['amount_due'] = bill_data["total"]
        bill_serializer = BillSerializer(bill,data=bill_data)
        if bill_serializer.is_valid():
            bill_id = bill_serializer.save()
            if bill_file_data:
                bill_id.attach_file = bill_file_data
            bill_id.save()
        else:
            print(bill_serializer.errors)
            return Response(bill_serializer.errors, 400)
        Audit.objects.create(
            company_id=comp_id,
            branch_id=branch_id,
            modified_by=user,
            audit_modified_date=bill_data["bill_date"],
            module="Bill",
            sub_module='Bill',
            data=bill_data
        )

        purchase_account = bill_data.get('purchase_account', None)
        party_account = bill_data.get('party_account', None)
        try:
            account_payable = COA.get_account(party_account)
        except:
            if ven_id:
                account_payable = ven_id.coa_id
            else:
                account_payable = COA.get_account_paybles(comp_id)
        try:
            purchase_account = COA.get_account(purchase_account)
        except:
            purchase_account = None
        bill_stocks = Stock.objects.filter(
            ref_id=bill_id.bill_id,
            ref_tblname='Bill',
            formname='Bill',
            module='Purchase',
            branch_id=bill_id.branch_id,
            company_id=bill_id.company_id,
            stage='Add Stages'
        )
        prev_stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,float(stock.quantity),stock.godown_id_id): stock for stock in
                         bill_stocks}
        bill_stk_list = {}
        for items in bill_items:
            godown_id = items["godown_id"]

            item_obj = Item.objects.get(item_id=items["item_id"])
            billed_items = Bill_Item.objects.create(bill_id=bill_id,
                                                    item_id=item_obj,
                                                    coa_id=COA.objects.get(
                                                    coa_id=items["coa_id"]),
                                                    expire_date=items["expire_date"],
                                                    mfg_date=items["mfg_date"],
                                                    batch_no=items["batches"],
                                                    godown_id_id=godown_id,
                                                    godown_name=items['godown_name'],
                                                    item_name=items["item_name"],
                                                    rate=items["rate"],
                                                    quantity=items["quantity"],
                                                    tax_rate=items["tax_rate"],
                                                    tax_name=items["tax_name"],
                                                    tax_type=items["tax_type"],
                                                    cgst_amount=items["cgst_amount"],
                                                    sgst_amount=items["sgst_amount"],
                                                    igst_amount=items["igst_amount"],
                                                    discount=items["discount"],
                                                    cess_rate=items['cess_rate'],
                                                    cess_amount=items['cess_amount'],
                                                    amount=items["amount"])
            billed_items.save()
            track_inventory = item_obj.track_inventory

            amount = float(items['amount'])

            if track_inventory:

                batch = items["batches"]
                exp_date = items["expire_date"]
                mfg_date = items["mfg_date"]
                if not batch:
                    batch.append(None)
                    exp_date = None
                    mfg_date = None

                obj_bill, created = Stock.objects.get_or_create(
                    item_id=items['item_id'],
                    ref_id=bill_id.bill_id,
                    ref_tblname='Bill',
                    formname='Bill',
                    godown_id_id=godown_id,
                    batch_no=batch[0],
                    quantity=round(float(items['quantity']),2),
                    mfg_date=mfg_date,
                    expire_date=exp_date,
                    branch_id=bill_id.branch_id,
                    company_id=bill_id.company_id,
                    stage='Add Stages',
                    module="Purchase"
                )
                if created:
                    print("New Stock created")
                else:
                    print("stock updarted")
                obj_bill.godown_name = items['godown_name']
                obj_bill.flow_type = 'INWARD'
                obj_bill.item_name = items["item_name"]
                obj_bill.stock_in = float(items['quantity'])
                obj_bill.stock_out = 0
                obj_bill.amount = amount
                obj_bill.rate = items["rate"]
                obj_bill.module_date = bill_id.created_date
                obj_bill.date = bill_data["bill_date"]
                obj_bill.save()
                bill_stk_list[(obj_bill.item_id, obj_bill.batch_no, obj_bill.expire_date,
                                  obj_bill.mfg_date,float(obj_bill.quantity),obj_bill.godown_id_id)] = obj_bill


            if not purchase_account:
                coa_id = items["coa_id"] if not items["coa_id"] else item_obj.purchase_account
                TO_COA = COA.get_account(coa_id)
            else:
                TO_COA = purchase_account

            MasterTransaction.objects.create(
                L1detail_id=bill_id.bill_id,
                L1detailstbl_name='Bill',
                # L2detail_id=L2detail_id,
                # L2detailstbl_name=L2detailstbl_n
                main_module='Purchase',
                module='Bill',
                sub_module='Bill',
                transc_deatils='Bill',
                banking_module_type='Bill',
                journal_module_type='Bill',
                trans_date=bill_data["bill_date"],
                trans_status='Manually Added',
                debit=amount,
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=amount,
                from_account=account_payable.coa_id,
                from_acc_type=account_payable.account_type,
                from_acc_head=account_payable.account_head,
                from_acc_subhead=account_payable.account_subhead,
                from_acc_name=account_payable.account_name,
                vendor_id=ven_id,
                branch_id=branch_id,
                company_id=comp_id)
        for key, obj in prev_stk_list.items():
            if key not in bill_stk_list:
                print("deleting child")
                obj.delete()
        transaction_list = [] #This Empty List added the append

        if float(bill_data['tcs_amount']) > 0:
            tcs_account = bill_data.get('tcs_account', None)
            if tcs_account:
                account = COA.objects.get(coa_id=tcs_account)
            else:
                account = COA.get_input_tcs_account(comp_id)
            transaction_list.append([account, "tcs_amount"], )
        if float(bill_data['cess_total']) > 0:
            cess_account = bill_data.get('cess_account', None)
            if cess_account:
                account = COA.objects.get(coa_id=cess_account)
            else:
                account = COA.get_input_cess_account(comp_id)
            transaction_list.append([account, "cess_total"], )
        total_taxes = bill_data.get('total_taxes', [])
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
                    TO_COA_OBJ = account_payable
                    FROM_COA_OBJ = coa
                else:
                    obj.debit = abs(amount)
                    obj.credit = abs(amount)
                    TO_COA_OBJ = coa
                    FROM_COA_OBJ = account_payable
                MasterTransaction.objects.create(
                    L1detail_id=bill_id.bill_id,
                    L1detailstbl_name='Bill',
                    main_module='Purchase',
                    module='Bill',
                    sub_module='Tax Charges',
                    transc_deatils='Bill',
                    banking_module_type='Bill',
                    journal_module_type='Bill',
                    trans_date=bill_data["bill_date"],
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
                    vendor_id=ven_id,
                    branch_id=branch_id,
                    company_id=comp_id)

            obj.bill_id = bill_id
            obj.save()
        charges = bill_data.get('co_charges', [])
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
                amount = float(charge.get('amount',0))
                coa = obj.coa_id
                if amount != 0:

                    if amount < 0:
                        obj.credit = abs(amount)
                        obj.debit = abs(amount)
                        TO_COA_OBJ = account_payable
                        FROM_COA_OBJ = coa
                    else:
                        obj.debit = abs(amount)
                        obj.credit = abs(amount)
                        TO_COA_OBJ = coa
                        FROM_COA_OBJ = account_payable
                    # if coa.account_type in ["Assets", "Expense"]:
                    #     if amount < 0:
                    #         obj.credit = abs(amount)
                    #         TO_COA_OBJ = account_payable
                    #         FROM_COA_OBJ = coa
                    #     else:
                    #         obj.debit = abs(amount)
                    #         FROM_COA_OBJ = account_payable
                    #         TO_COA_OBJ = coa
                    # else:
                    #     if amount < 0:
                    #         obj.debit = abs(amount)
                    #         TO_COA_OBJ = coa
                    #         FROM_COA_OBJ = account_payable
                    #     else:
                    #         obj.credit = abs(amount)
                    #         FROM_COA_OBJ = coa
                    #         TO_COA_OBJ = account_payable
                    MasterTransaction.objects.create(
                    L1detail_id=bill_id.bill_id,
                    L1detailstbl_name='Bill',
                    main_module='Purchase',
                    module='Bill',
                    sub_module='Bill',
                    transc_deatils='Bill',
                    banking_module_type='Bill',
                    journal_module_type='Bill',
                    trans_date=bill_data["bill_date"],
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
                    vendor_id=ven_id,
                    branch_id=branch_id,
                    company_id=comp_id)

                obj.bill_id = bill_id
                obj.save()
        for transaction in transaction_list:
            TO_COA = transaction[0]
            MasterTransaction.objects.create(
                L1detail_id=bill_id.bill_id,
                L1detailstbl_name='Bill',
                main_module='Purchase',
                module='Bill',
                sub_module='Bill',
                transc_deatils='Bill',
                banking_module_type='Bill',
                journal_module_type='Bill',
                trans_date=bill_data["bill_date"],
                trans_status='Manually Added',
                debit=bill_data[transaction[1]],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=bill_data[transaction[1]],
                from_account=account_payable.coa_id,
                from_acc_type=account_payable.account_type,
                from_acc_head=account_payable.account_head,
                from_acc_subhead=account_payable.account_subhead,
                from_acc_name=account_payable.account_name,
                vendor_id=ven_id,
                branch_id=branch_id,
                company_id=comp_id)
        transaction_list_tds = []
        if float(bill_data['tds_amount']) > 0:
            tds_account = bill_data.get('tds_account', None)
            if tds_account:
                account = COA.objects.get(coa_id=tds_account)
            else:
                account = COA.get_input_tds_account(comp_id)
            transaction_list_tds.append([account, "tds_amount"] )
        for transaction in transaction_list_tds:
            TO_COA = transaction[0]
            billmast = MasterTransaction.objects.create(
                L1detail_id=bill_id.bill_id,
                L1detailstbl_name='Bill',
                main_module='Purchase',
                module='Bill',
                sub_module='Bill',
                transc_deatils='Bill',
                banking_module_type='Bill',
                journal_module_type='Bill',
                trans_date=bill_data["bill_date"],
                trans_status='Manually Added',
                debit=bill_data[transaction[1]],
                to_account=account_payable.coa_id,
                to_acc_type=account_payable.account_type,
                to_acc_head=account_payable.account_head,
                to_acc_subhead=account_payable.account_subhead,
                to_acc_name=account_payable.account_name,
                credit=bill_data[transaction[1]],
                from_account=TO_COA.coa_id,
                from_acc_type=TO_COA.account_type,
                from_acc_head=TO_COA.account_head,
                from_acc_subhead=TO_COA.account_subhead,
                from_acc_name=TO_COA.account_name,
                vendor_id=ven_id,
                branch_id=branch_id,
                company_id=comp_id)
        if float(bill_data['discount']) > 0:
            discount_account = bill_data.get('discount_account', None)
            if discount_account:
                disc_acc = COA.objects.select_for_update().get(coa_id=discount_account, company_id=company_id)
            else:
                disc_acc = COA.objects.select_for_update().get(company_id=comp_id,
                                                               account_subhead='Other Income',
                                                               account_head='Other Income',
                                                               isdefault=True,
                                                               account_name="Discount")
            TO_COA = account_payable

            print('Discount Account is', discount_account, type(discount_account))
            print('""""""""""""', TO_COA)
            MasterTransaction.objects.create(
                L1detail_id=bill_id.bill_id,
                L1detailstbl_name='Bill',
                main_module='Purchase',
                module='Bill',
                sub_module='Bill',
                transc_deatils='Bill',
                banking_module_type='Bill',
                journal_module_type='Bill',
                trans_date=bill_data["bill_date"],
                trans_status='Manually Added',
                debit=bill_data['discount'],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=bill_data['discount'],
                from_account=disc_acc.coa_id,
                from_acc_type=disc_acc.account_type,
                from_acc_head=disc_acc.account_head,
                from_acc_subhead=disc_acc.account_subhead,
                from_acc_name=disc_acc.account_name,
                vendor_id=ven_id,
                branch_id=branch_id,
                company_id=comp_id)
        return Response(bill_serializer.data,status=201)

    def put(self,request,pk):
        bill_file_data = None
        try:
            bill_data = request.data['data']
            bill_data = json.loads(bill_data)
            bill_file_data = request.FILES.get('attach_file')
        except:
            bill_data = request.data
        user = request.user
        return self.handle_update(user,bill_data,bill_file_data,pk)

#Bill updation Section
class BillUpdate3ViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = Bill


    @transaction.atomic
    def update(self, request, pk, *args, **kwargs):
        bill_file_data = None
        try:
            bill_data=request.data['data']
            bill_data = json.loads(bill_data)
            bill_file_data = request.FILES.get('attach_file')
        except:
            bill_data = request.data

        print(bill_data)
        bill = Bill.objects.select_for_update().get(bill_id=pk)
        comp_id = Company.objects.get(company_id=bill_data["company_id"])
        vend_id = None
        if bill_data['vendor_id']:
            ven_id = Vendor.objects.get(
                vendor_id=bill_data["vendor_id"])
        
        #account receivable varibale are declaret the chart of account of to side from item and taxation Section 
        #and Discount time this chartof Account is From Side
        print(bill_data['bill_items'])
        # Invoice Item Looping
        for bill_item_data in bill_data['bill_items']:
            print(bill_item_data,"??????????????")
           # Item are find Out Section
           
            try:
                try:
                    bill_item = Bill_Item.objects.get(item_id=bill_item_data['item_id'],bill_id=bill)
                    
                except KeyError:
                    bill_item=None
                    
                  
                                
            except Bill_Item.DoesNotExist:
                bill_item=None
            
            # Invoice Item Are Find the update this Code Section   
            if bill_item is not None:
                
                item_serializer=GETBillItemSerializer(bill_item,data=bill_item_data)
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    return Response(item_serializer.errors, status=400)
                   
            else:
                try:
                    # Get The Chart Of Account and item Id Of the Item Related
                    coa=COA.objects.get(coa_id=bill_item_data["coa_id"])
                    item=Item.objects.get(item_id=bill_item_data["item_id"])
                except KeyError:
                    coa=None
                    item=None
                
                try:
                    #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
                    bill_items = Bill_Item.objects.create(bill_id=bill,
                                                        item_id=item,
                                                        coa_id=coa,
                                                          expire_date=bill_item_data["expire_date"],
                                                          mfg_date=bill_item_data["mfg_date"],
                                                          batch_no=bill_item_data["batch_no"],
                                                        item_name=bill_item_data["item_name"],
                                                        rate=bill_item_data["rate"],
                                                        quantity=bill_item_data["quantity"],
                                                        tax_rate=bill_item_data["tax_rate"],
                                                        tax_name=bill_item_data["tax_name"],
                                                        tax_type=bill_item_data["tax_type"],
                                                        sgst_amount=bill_item_data["sgst_amount"],
                                                        cgst_amount=bill_item_data["cgst_amount"],
                                                        igst_amount=bill_item_data["igst_amount"],
                                                        # taxamount=item["taxamount"],
                                                        amount=bill_item_data["amount"])
                    bill_items.save()
                   
                except KeyError:
                    pass                 
                
                    
                
            
        #this Section Is Invoice Data Update Serializer Through
        bill_data['amount_due'] = bill_data["total"]
        serializer = BillSerializer(bill, data=bill_data)

        if serializer.is_valid():

            bill_id=serializer.save()
            if bill_file_data:
                bill_id.attach_file = bill_file_data
            bill_id.save()
            # return Response({"data":serializer.data})
        else:
             return Response(serializer.errors, status=400)
        
        stock_item_list=[]
        stock_transactiom_item_list=[]
        account_payable = COA.objects.get(company_id=comp_id, account_subhead='Account Payables',isdefault=True)

        for bill_item_stock in bill_data['bill_items']:
            print('For Loop Is Excuted')
            stock_item_list.append(bill_item_stock['item_id'])
            try: 
                
                stock_item=Stock.objects.get(item_id=bill_item_stock['item_id'],ref_id=bill.bill_id)
           
                print('okk')     
                item_value=Item.objects.get(item_id=bill_item_stock["item_id"])
                current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
            
                print("updating stock", bill_item_stock['quantity'], bill_item_stock['item_id'])
                stock_item.stock_in=float(bill_item_stock['quantity'])
                stock_item.rate=float(current_assets_last_stock.rate)
                stock_item.amount=float(current_assets_last_stock.rate)*float(bill_item_stock['quantity'])
                stock_item.quantity=float(bill_item_stock['quantity'])
                stock_item.expire_date = bill_item_stock['expire_date']
                stock_item.mfg_date = bill_item_stock['mfg_date']
                stock_item.batch_no = bill_item_stock['batch_no']

                stock_item.save()
                stock_transactiom_item_list.append(stock_item)
                stock_mast=MasterTransaction.objects.get(L2detail_id=stock_item.st_id,L1detail_id=bill_id.bill_id)
                stock_mast.debit=stock_item.rate*stock_item.quantity,
                stock_mast.credit=stock_item.rate*stock_item.quantity,
                print('Updateing Sucessfully')
            except Stock.DoesNotExist:
                    
                items_inventory=bill_data.get('bill_items')
                print('Inventory Tracked item is ',items_inventory)
                track_inventory=bill_item_stock.get('selected_item_name',{}).get('track_inventory')
                print('Inventory Tracked item is ',items_inventory)
                coa=items_inventory[0].get('coa_id')
                amount=items_inventory[0].get('amount')
                item_value=Item.objects.get(item_id=bill_item_stock["item_id"])
                
                try:
                    current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
                    current_stock_amount=current_assets_last_stock.amount
                   
                except Stock.DoesNotExist:
                    current_stock_amount=0
                    
                    
                
                if track_inventory==True:
                    stk_in=Stock.objects.filter(item_id=bill_item_stock["item_id"]).exclude(stock_in=0).order_by('created_date')
                    stk_out=Stock.objects.filter(item_id=bill_item_stock["item_id"]).exclude(stock_out=0).order_by('created_date')        
                    stock_int_items = stk_in
                    
                    
                    stock_items=Stock.objects.create(
                        item_id=bill_item_stock['item_id'],
                        item_name=bill_item_stock["item_name"],
                        stock_in=bill_item_stock["quantity"],
                        expire_date=bill_item_stock["expire_date"],
                        mfg_date=bill_item_stock["mfg_date"],
                        batch_no=bill_item_stock["batch_no"],
                        amount=current_stock_amount+(bill_item_stock["quantity"] * bill_item_stock["rate"]),
                        rate= bill_item_stock["rate"],
                        quantity=bill_item_stock["quantity"],
                        #stock_on_hand=current_stock_on_hand+bill_item_stock["quantity"],
                        ref_id=bill_id.bill_id,
                        module_date=bill_id.created_date,
                        ref_tblname='Bill',
                        module='Purchase',
                        formname='Bill',
                        stage='Add Stages',
                        date=bill_data["bill_date"],

                        company_id=comp_id)
                        
                #This Section Is Stock Journal Transaction 
                #Stock Charetd Account name is Inventory Assets
                    # if track_inventory == True:
                    print('New Item Are Created in Stock',stock_items)    
                    TO_COA = COA.objects.get(company_id=comp_id,account_name='Inventory Assets')
                    print('Stock is Created master Transaction Start')
                    stkmast = MasterTransaction.objects.create(
                        L1detail_id=bill_id.bill_id,
                        L1detailstbl_name='Bill',
                        L2detail_id=stock_items.st_id,
                        L2detailstbl_name='Stock',
                        main_module='Purchase',
                        module='Bill',
                        sub_module='Bill',
                        transc_deatils='Bill',
                        banking_module_type='Bill',
                        journal_module_type='Bill',
                        trans_date=bill_data["bill_date"],
                        trans_status='Manually Added',
                        debit=stock_items.rate*stock_items.quantity,
                        to_account=TO_COA.coa_id,
                        to_acc_type=TO_COA.account_type,
                        to_acc_head=TO_COA.account_head,
                        to_acc_subhead=TO_COA.account_subhead,
                        to_acc_name=TO_COA.account_name,
                        credit=stock_items.rate*stock_items.quantity,
                        from_account=account_payable.coa_id,
                        from_acc_type=account_payable.account_type,
                        from_acc_head=account_payable.account_head,
                        from_acc_subhead=account_payable.account_subhead,
                        from_acc_name=account_payable.account_name,
                        company_id=comp_id,
                        vendor_id=ven_id)
                    stkmast.save()
                   
                else:
                    print('Transaction Completed Start')
                    TO_COA = COA.objects.get(coa_id=coa)
                    #FROM_COA = COA.objects.get(company_id=comp_id,coa_id=purchase_account)
                    billmast = MasterTransaction.objects.create(
                        L1detail_id=bill_id.bill_id,
                        L1detailstbl_name='Bill',
                        # L2detail_id=L2detail_id,
                        # L2detailstbl_name=L2detailstbl_name,
                        main_module='Purchase',
                        module='Bill',
                        sub_module='Bill',
                        transc_deatils='Bill',
                        banking_module_type='Bill',
                        journal_module_type='Bill',
                        trans_date=bill_data["bill_date"],
                        trans_status='Manually Added',
                        debit=amount,
                        to_account=account_payable.coa_id,
                        to_acc_type=account_payable.account_type,
                        to_acc_head=account_payable.account_head,
                        to_acc_subhead=account_payable.account_subhead,
                        to_acc_name=account_payable.account_name,
                        credit=amount,
                        from_account=TO_COA.coa_id,
                        from_acc_type=TO_COA.account_type,
                        from_acc_head=TO_COA.account_head,
                        from_acc_subhead=TO_COA.account_subhead,
                        from_acc_name=TO_COA.account_name,
                        vendor_id=ven_id,
                        company_id=comp_id)
                    billmast.save() 

        
        
       
        try:    
            # 0%GST and 0%IGST Calculation
            #0 % Taxtion Is the UserSelection User Can Select the 0% Tax This 0 is Added the Tax Section
            Zero_tax=bill_data.get('bill_items')
            GST_TAX=None
            if GST_TAX==Zero_tax[0] is not None:
                GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
            else:
                pass
        except AttributeError:
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
        
       
        bill_data['tds_amount']=abs(float(bill_data['tds_amount']))
        transaction_list = [] #This Empty List added the append 
        print("Transaction List is here",)
        if float(bill_data['cgst_total'])>0  or Both_Tax:
            transaction_list.append(["Input CGST", "cgst_total"],)
        if float(bill_data['sgst_total'])>0 or Both_Tax:
            transaction_list.append(["Input SGST", "sgst_total"])
        if float(bill_data['igst_total']) >0 or IGST_0:
            transaction_list.append(["Input IGST", "igst_total"],)            
        if float(bill_data['tcs_amount'])>0:
            transaction_list.append(["TCS Receivable", "tcs_amount"],)
        if float(bill_data['cess_total']) > 0:
            transaction_list.append(["Input CESS", "cess_total"], )
        if float(bill_data['total_charges']) > 0:
            transaction_list.append(["Input Charges", "total_charges"], )
        # if(float(bill_data['tds_amount'])) > 0:
        #     transaction_list.append(["TDS Payable", "tds_amount"] )
        acc_from_list=[]
        acc_to_list=[]
        for transaction in transaction_list:
            for account_transaction in [transaction[0]]:
                acc_to_list.append(account_transaction)
                print('input tax  isisss is herer',account_transaction)
                if account_transaction is not None:
                    try:
                        #this Section is List Addded Charted Of account Updated                
                        account_list=MasterTransaction.objects.get(to_acc_name=account_transaction,L1detail_id=bill_id.bill_id)
                        account_list.updateBalance(bill_data[transaction[1]], bill_data[transaction[1]])
                        account_list.credit=bill_data[transaction[1]]
                        account_list.debit=bill_data[transaction[1]]
                        account_list.save()
                        print('Tax Suessfully updated')
            
                    except MasterTransaction.DoesNotExist:
            
                        print('Tax Transaction Is Created')
            #List Of index added 0 is get Account_name
                        TO_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
                        print('""""""""""""', TO_COA)
                        billmast = MasterTransaction.objects.create(
                            L1detail_id=bill_id.bill_id,
                            L1detailstbl_name='Bill',
                            main_module='Purchase',
                            module='Bill',
                            sub_module='Bill',
                            transc_deatils='Bill',
                            banking_module_type='Bill',
                            journal_module_type='Bill',
                            trans_date=bill_data["bill_date"],
                            trans_status='Manually Added',
                            debit=bill_data[transaction[1]],
                            to_account=TO_COA.coa_id,
                            to_acc_type=TO_COA.account_type,
                            to_acc_head=TO_COA.account_head,
                            to_acc_subhead=TO_COA.account_subhead,
                            to_acc_name=TO_COA.account_name,
                            credit=bill_data[transaction[1]],
                            from_account=account_payable.coa_id,
                            from_acc_type=account_payable.account_type,
                            from_acc_head=account_payable.account_head,
                            from_acc_subhead=account_payable.account_subhead,
                            from_acc_name=account_payable.account_name,
                            vendor_id=ven_id,
                            company_id=comp_id)
                        billmast.save()


          
            #  This Sectio Is Discount 
            # Diffrance in Tax Section And Disscount Section Is Tax Side From Account Is Discount Section To Side
            #and Discount From Side Account is Tax Side is To side
            #Change The Credit and Debit side 

        transaction_list_tds = []
        if float(bill_data['tds_amount']) > 0:
            transaction_list_tds.append(["TDS Payable", "tds_amount"])
            for transaction in transaction_list:
                for account_transaction in [transaction[0]]:
                    acc_to_list.append(account_transaction)
                    print('input tax  isisss is herer', account_transaction)
                    if account_transaction is not None:
                        try:
                            # this Section is List Addded Charted Of account Updated
                            account_list = MasterTransaction.objects.get(to_acc_name=account_transaction,
                                                                         L1detail_id=bill_id.bill_id)
                            account_list.updateBalance(bill_data[transaction[1]], bill_data[transaction[1]])
                            account_list.credit = bill_data[transaction[1]]
                            account_list.debit = bill_data[transaction[1]]
                            account_list.save()
                            print('Tax Suessfully updated')

                        except MasterTransaction.DoesNotExist:

                            print('Tax Transaction Is Created')
                            # List Of index added 0 is get Account_name
                            TO_COA = COA.objects.get(company_id=comp_id, account_name=transaction[0])
                            print('""""""""""""', TO_COA)
                            billmast = MasterTransaction.objects.create(
                                L1detail_id=bill_id.bill_id,
                                L1detailstbl_name='Bill',
                                main_module='Purchase',
                                module='Bill',
                                sub_module='Bill',
                                transc_deatils='Bill',
                                banking_module_type='Bill',
                                journal_module_type='Bill',
                                trans_date=bill_data["bill_date"],
                                trans_status='Manually Added',
                                debit=bill_data[transaction[1]],
                                to_account=account_payable.coa_id,
                                to_acc_type=account_payable.account_type,
                                to_acc_head=account_payable.account_head,
                                to_acc_subhead=account_payable.account_subhead,
                                to_acc_name=account_payable.account_name,
                                credit=bill_data[transaction[1]],
                                from_account=TO_COA.coa_id,
                                from_acc_type=TO_COA.account_type,
                                from_acc_head=TO_COA.account_head,
                                from_acc_subhead=TO_COA.account_subhead,
                                from_acc_name=TO_COA.account_name,
                                vendor_id=ven_id,
                                company_id=comp_id)
                            billmast.save()
        try:
            #This Section is Disscount will Be find to this code will Be Excuted
            discount_account=bill_data['discount_account']
            if discount_account is not None:
                discount_acc =COA.objects.get(company_id=comp_id, coa_id=discount_account)
                discount_acc_name=discount_acc.account_name
                print(f"------------------{discount_acc_name}")
                item_discount_list=MasterTransaction.objects.get(to_acc_name=discount_acc_name,L1detail_id=bill_id)
                item_discount_list.updateBalance(bill_data['discount'], bill_data['discount'])
                item_discount_list.credit=bill_data['discount']
                item_discount_list.debit=bill_data['discount']
                item_discount_list.save()
            
        # This Section List are addded the Disscount Create mastertransaction new entry    
        except Exception as e:
            print(e)
            discount_account = bill_data['discount_account']
            print("discount account not found",COA.objects.get(company_id=comp_id, coa_id=discount_account).account_name)
            if float(bill_data['discount'])>0:
                  
                discount_account=bill_data['discount_account']
                TO_COA = COA.objects.get(coa_id=account_payable.coa_id)
                account_payable = COA.objects.get(company_id=comp_id, coa_id=discount_account)
                print('Discount Account is', account_payable, type(discount_account))

                print('""""""""""""', TO_COA)
                billmast = MasterTransaction.objects.create(
                    L1detail_id=bill_id.bill_id,
                    L1detailstbl_name='Bill',
                    main_module='Purchase',
                    module='Bill',
                    sub_module='Bill',
                    transc_deatils='Bill',
                    banking_module_type='Bill',
                    journal_module_type='Bill',
                    trans_date=bill_data["bill_date"],
                    trans_status='Manually Added',
                    debit=bill_data['discount'],
                    to_account=TO_COA.coa_id,
                    to_acc_type=TO_COA.account_type,
                    to_acc_head=TO_COA.account_head,
                    to_acc_subhead=TO_COA.account_subhead,
                    to_acc_name=TO_COA.account_name,
                    credit=bill_data['discount'],
                    from_account=account_payable.coa_id,
                    from_acc_type=account_payable.account_type,
                    from_acc_head=account_payable.account_head,
                    from_acc_subhead=account_payable.account_subhead,
                    from_acc_name=account_payable.account_name,
                    vendor_id=ven_id,
                    company_id=comp_id)
                billmast.save()
        


        
        
        print('Stock item list is ',stock_item_list,'bill id is',bill_id)
        trans_stock_list= Stock.objects.filter(ref_id=bill_id.bill_id).exclude(item_id__in=stock_item_list)
        print('Start The item Is ready to delete',trans_stock_list)
        for trans_stock in trans_stock_list:
            mast_stock=trans_stock.st_id
            transaction_stock= MasterTransaction.objects.filter(L1detail_id=bill_id.bill_id,L2detail_id=str(mast_stock)).delete()
            print('Deleted Stock Transaction item Name is ',transaction_stock)
        
        del_stock= Stock.objects.filter(ref_id=bill_id.bill_id).exclude(item_id__in=stock_item_list).delete()
        print('Ohhh Stock is deleted',del_stock)
        
     
        
      #this Section Is the Delete the Trnsaction Not Fined is List Mens Remove the Transaction
        #master_stock variable is the remaning of stock item in master transaction
        master_stock_list=[]
        master_stock= MasterTransaction.objects.filter(L1detail_id=bill_id.bill_id,L2detailstbl_name='Stock')
        for stock_trans_mast in master_stock:
            master_stock_list.append(stock_trans_mast.to_acc_name)
        print('acc List Is here',acc_to_list)
        print('master_stock_list is herer',master_stock_list)
        to_and_from=acc_from_list+acc_to_list
        Both_List=to_and_from+master_stock_list
       
        topics = MasterTransaction.objects.filter(L1detail_id=bill_id.bill_id).exclude(to_acc_name__in=Both_List).exclude(from_acc_name__in=Both_List).delete()
        print('Both List Is here',Both_List)
        bill_item_list=Bill_Item.objects.filter(bill_id=bill_id.bill_id).exclude(item_id__in=stock_item_list).delete()

        serializer = BillSerializer(bill_id)    
        return Response(serializer.data)
        
        
@api_view(['GET'])
def getbillitembybillid(request, bill_id):
    object = Bill_Item.objects.filter(bill_id=bill_id)
    serializer = GETBillItemSerializer(object, many=True)
    return Response(serializer.data)  


# Get search details by bill serial number
@api_view(['GET'])

def getBillDetailsBybill_serial(request, company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    bill_serial = request.GET['serial']
    bills = BillView.objects.filter(company_id=company_id,
                                    branch_id=branch_id,bill_serial__icontains=bill_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": bills.count()}
    
    instance = bills[offset:offset + limit]
    serializer = ForPaginationJoinBillAndBillItemSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)


@api_view(['GET'])

def getBillDetailsByvendor_name(request, company_id,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    vendor_name = request.GET['name']
    bills = BillView.objects.filter(company_id=company_id,
                                branch_id=branch_id,
                                vendor_name__icontains=vendor_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": bills.count()}

    instance = bills[offset:offset + limit]
    serializer = ForPaginationJoinBillAndBillItemSerializer(instance, many=True)

    response['results'] = serializer.data
    return Response(response)