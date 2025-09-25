from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from ocr.models import Document
from ocr.serializer import DocumentSerializer,DocumentQSerializer
from rest_framework.parsers import MultiPartParser,JSONParser
from item.models.item_model import Item
from django.contrib.postgres.search import TrigramSimilarity
from purchase.models.Vendor_model import Vendor
from django.db import transaction
from item.serializers.item_serializers import GstItem,IGstItem,getstock_on_hand
from salescustomer.models.Salescustomer_model import SalesCustomer
from company.models import Company
from registration.models import Feature
from ocr.queueOcr import send_message_to_queue
import os
import json
# Create your views here.
class DocumentNameView(APIView):

    def get(self,request,comp_id=None,name=None,branch_id=None):
        if comp_id and name:
            limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
            offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

            # Build the response links for pagination
            url = str(request.build_absolute_uri()).split("?")[0]
            print(request.user)
            # companies = Company.objects.filter(user=request.user).values_list('company_id', flat=True)
            response = {
                'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Document.objects.filter(filename__icontains=name,
                                                 branch_id=branch_id,
                                                 created=False, company_id=comp_id).count()
            }
            try:

                docs = Document.objects.filter(filename__icontains=name,created=False,
                                               branch_id=branch_id,
                                               company_id=comp_id)[offset:offset + limit]
            except Exception:
                return Response("Company not found.", status=404)

                # Serialize the items and return the paginated response
            response['results'] = DocumentSerializer(docs, many=True).data
            return Response(response)
class DocumentView(APIView):
    parser_classes = [MultiPartParser,JSONParser]

    def get(self,request,comp_id,branch_id):
        limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
        offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

        # Build the response links for pagination
        url = str(request.build_absolute_uri()).split("?")[0]
        print(request.user)
        # companies = Company.objects.filter(user=request.user).values_list('company_id', flat=True)
        response = {
            'next': url + f"?limit={limit}&offset={offset + limit}",
            'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
            "count": Document.objects.filter(created=False,
                                             branch_id=branch_id,
                                             company_id=comp_id).count()
        }
        try:

            docs = Document.objects.filter(created=False,company_id=comp_id, branch_id=branch_id)[offset:offset + limit]
        except Exception:
            return Response("Company not found.", status=404)

            # Serialize the items and return the paginated response
        response['results'] = DocumentSerializer(docs, many=True).data
        return Response(response)

    @transaction.atomic
    def post(self,request):
        count = Feature.objects.get(user_id=request.user.id).doc_remaining
        print(count, 'ocr docs')
        if count <= 0:
            return Response({"message": "You don't have access to this service please upgrade plan"}, status=401)
        files = request.FILES.getlist('files')
        company = request.data.get('company_id')
        branch_id = request.data.get('branch_id')

        if company:
            for file in files:
                filename = file.name
                binary_data = file.read()
                obj = Document.objects.create(filename=filename,
                                        content=binary_data,
                                        company_id=company,
                                        branch_id = branch_id
                                       )

                serializer = DocumentQSerializer(obj)
                message ={"doc_id":serializer.data['doc_id'],"db_name":os.environ.get("DB_NAME")}
                print(message)
                send_message_to_queue(message,obj.doc_id,"ocr")
            return Response(status=201)
        return Response(status=400)



class ResultView(APIView):

    def update_gst(self,row,it):
        gst_rate = row.get('gst_rate',None)
        if gst_rate:
            print(gst_rate,"????????")
            filtered_items = list(filter(lambda x: x['value'] == str(int(gst_rate)), GstItem))
            print(filtered_items)
            if filtered_items:
                item = filtered_items[0]
                tax_rate = item['value']
                tax_type = item['group']
                tax_name = item['label']
                print(tax_name,">>>>>>>>")
                row['tax_name'] = tax_name
                row['tax_rate'] = tax_rate
                row['tax_type'] = tax_type
            filtered_items = list(filter(lambda x: x['value'] == str(int(gst_rate)), IGstItem))
            if filtered_items:
                item = filtered_items[0]
                i_tax_rate = item['value']
                i_tax_type = item['group']
                tax_name = item['label']
                row['i_tax_name'] = tax_name
                row['i_tax_rate'] = i_tax_rate
                row['i_tax_type'] = i_tax_type
            row['stock_quantity'] = getstock_on_hand(it.item_id)
            row['track_inventory'] = it.track_inventory
            return
        inter_rate = it.inter_rate
        intra_rate = it.intra_rate
        tax_rate = None
        tax_type = None
        tax_name = intra_rate
        i_tax_rate = None
        i_tax_type = None
        i_tax_name = inter_rate
        if intra_rate:
            filtered_items = list(filter(lambda x:x['label'] == tax_name,GstItem))
            if filtered_items:
                item = filtered_items[0]
                tax_rate = item['value']
                tax_type = item['group']
        row['tax_name'] = tax_name
        row['tax_rate'] = tax_rate
        row['tax_type'] = tax_type
        if inter_rate:
            filtered_items = list(filter(lambda x:x['label'] == i_tax_name,IGstItem))
            if filtered_items:
                item = filtered_items[0]
                i_tax_rate = item['value']
                i_tax_type = item['group']
        row['i_tax_name'] = i_tax_name
        row['i_tax_rate'] = i_tax_rate
        row['i_tax_type'] = i_tax_type
        row['stock_quantity'] = getstock_on_hand(it.item_id)
        row['track_inventory'] = it.track_inventory

    def get_bill_data(self,result,company_id):
        comp = Company.objects.get(company_id=company_id)
        rows = result['rows']
        place_supply = result.get('place_supply',comp.state)
        bill_serial = result.get('serial','')
        name = result.get('name','')
        gst = result.get('gst_no','')
        date = result.get('date')
        vendor_id = None
        vendor_name = name
        if gst:
            vendors = Vendor.objects.filter(gstin_number=gst)
            if vendors:
                vendor_id = vendors[0].vendor_id
                vendor_name = vendors[0].vendor_name
        if not vendor_id and name:
            vendors = Vendor.objects.annotate(
                distance=TrigramSimilarity('vendor_name', name)
            ).filter(
                distance__gte=0.5,
                company_id=company_id
            ).order_by('distance')
            if vendors:
                vendor_id = vendors[0].vendor_id
                vendor_name = vendors[0].vendor_name
        if vendor_id:
            vend  = Vendor.objects.get(vendor_id=vendor_id)
            if vend.source_place:
                place_supply = vend.source_place
        result['company_id'] = company_id
        result['supply_place'] = place_supply
        print(result['supply_place'],">>>>>>>>>>>>")
        result['bill_serial'] = bill_serial
        result['vendor_id'] = vendor_id
        result['bill_date'] = date
        result['vendor_name'] = vendor_name
        result['batch'] = False
        for row in rows:
            hsn = row.get('hsn',None)
            product = row.get('product',None)
            batch_no = row.get('batch_no',None)
            expiry_date = row.get('expiry_date', None)
            mfg_date = row.get('mfg_date', None)
            if expiry_date and mfg_date and expiry_date < mfg_date:
                expiry_date,mfg_date = mfg_date,expiry_date

            discount_rate = row.get('discount_rate',None)
            row['discount'] = 0
            row['item_name'] = product

            if batch_no:
                row['batches'] = [batch_no]
                row['expire_date'] = expiry_date
                row['mfg_date'] = mfg_date
                if not result['batch']:
                    result['batch'] = True
            else:
                row['batches'] = []
                row['expire_date'] = expiry_date
                row['mfg_date'] = mfg_date
            if discount_rate:
                try:
                    row['discount'] = round((row.get('quantity', 1) * row.get('rate', 0)) / row.get('discount_rate', 1),
                                            2)
                    result['discount_type'] = "Item level"
                except Exception as e:
                    print(e)

            try:
                row['amount'] = round((row.get('quantity',1) * row.get('rate',0)) - row['discount'],2)
            except Exception as e:
                print(e,"error")
                row['amount'] = 0

            row['item_id'] = None
            if hsn:
                items = Item.objects.filter(hsn_code=int(hsn),company_id_id=company_id)
                if items and not len(items) > 1:
                    item = items[0]
                    row['item_id'] = item.item_id
                    row['coa_id'] = item.purchase_account
                    row['item_name'] = item.name
                    self.update_gst(row,item)
            if row['item_id'] is None:
                if product:
                    items = Item.objects.annotate(
                        distance=TrigramSimilarity('name', product)
                    ).filter(
                        distance__gte=0.5,
                        company_id=company_id
                    ).order_by('distance')
                    if items:
                        item = items[0]
                        row['item_id'] = item.item_id
                        row['coa_id'] = item.purchase_account
                        row['item_name'] = item.name
                        self.update_gst(row, item)

    def get_invoice_data(self,result,company_id):
        comp = Company.objects.get(company_id=company_id)
        rows = result['rows']
        place_supply = result.get('place_supply', comp.state)
        invoice_serial = result.get('serial', '')
        name = result.get('name_1', '')
        gst = result.get('gst_no_1', '')

        date = result.get('date')
        customer_id = None
        customer_name = name
        if gst:
            customers = SalesCustomer.objects.filter(gstin_number=gst)
            if customers:
                customer_id = customers[0].customer_id
                customer_name = customers[0].customer_name
        if not customer_id and name:
            customers = SalesCustomer.objects.annotate(
                distance=TrigramSimilarity('customer_name', name)
            ).filter(
                distance__gte=0.5,
                company_id=company_id
            ).order_by('distance')
            if customers:
                customer_id = customers[0].customer_id
                customer_name = customers[0].customer_name
        if customer_id:
            custom  = SalesCustomer.objects.get(customer_id=customer_id)
            if custom.supply_place:
                place_supply = custom.supply_place
        print(place_supply,"???????????????????")
        result['company_id'] = company_id
        result['supply_place'] = place_supply
        result['invoice_serial'] = invoice_serial
        result['customer_id'] = customer_id
        result['invoice_date'] = date
        result['customer_name'] = customer_name
        for row in rows:
            hsn = row.get('hsn', None)
            product = row.get('product', None)
            batch_no = row.get('batch_no', None)
            expiry_date = row.get('expiry_date', None)
            mfg_date = row.get('mfg_date', None)
            discount_rate = row.get('discount_rate', None)
            row['item_name'] = product
            row['discount'] = 0
            if discount_rate:
                try:
                    row['discount'] = round((row.get('quantity', 1) * row.get('rate', 0)) / row.get('discount_rate', 1),
                                            2)
                    result['discount_type']="Item level"
                except Exception as e:
                    print(e)

            try:
                row['amount'] = round((row.get('quantity', 1) * row.get('rate', 0))-row['discount'], 2)
            except Exception as e:
                print(e, "error")
                row['amount'] = 0
            row['item_id'] = None
            if batch_no:
                row['batches'] = [batch_no]
                row['expire_date'] = expiry_date
                row['mfg_date'] = mfg_date
            else:
                row['batches'] = []
                row['expire_date'] = expiry_date
                row['mfg_date'] = mfg_date

            if hsn:
                items = Item.objects.filter(hsn_code=int(hsn), company_id_id=company_id)
                if items and not len(items) > 1:
                    item = items[0]
                    row['item_id'] = item.item_id
                    row['coa_id'] = item.sales_account
                    row['item_name'] = item.name
                    self.update_gst(row, item)
            if row['item_id'] is None:
                if product:
                    items = Item.objects.annotate(
                        distance=TrigramSimilarity('name', product)
                    ).filter(
                        distance__gte=0.5,
                        company_id=company_id
                    ).order_by('distance')
                    if items:
                        item = items[0]
                        row['item_id'] = item.item_id
                        row['coa_id'] = item.sales_account
                        row['item_name'] = item.name
                        self.update_gst(row, item)
            print(row)
    def get(self,request,doc_type=None,doc_id=None):
        if doc_type and doc_id:
            obj = Document.objects.get(doc_id=doc_id)
            result = obj.result
            if result and doc_type == 'BILL':
                self.get_bill_data(result,obj.company_id)
            if result and doc_type == 'INVOICE':
                self.get_invoice_data(result, obj.company_id)
            print(obj.result)
            return Response(obj.result,status=200)

    @transaction.atomic
    def put(self, request, doc_id=None):
        if doc_id:
            doc = Document.objects.get(doc_id=doc_id)
            data = request.data
            print(data)
            created_type = data.get('created_type', None)
            if created_type:
                doc.created = True
                doc.created_type = created_type
                doc.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
 # item_name: null,
 #        quantity: 1,
 #        rate: null,
 #        amount: 0,
 #        discount:0,
 #        cess_rate:0,
 #        cess_amount:0,
 #        item_id:null,
 #        tax_name:null,
 #        tax_rate: null,
 #        tax_type: null,
 #        cgst_amount: 0,
 #        sgst_amount: 0,
 #        igst_amount: 0,
 #        taxamount: 0,
 #        coa_id:null


 # is_bill_generated: true,
 #    bill_status: " Save and Send ",
 #    vendor_id: null,
 #    customer_id: null,
 #    company_id: company_id,
 #    branch_id: null,
 #    payment_status: "unpaid",
 #    bill_serial: "",
 #    order_no: "",
 #    bill_date: getToday(),
 #    due_date: getToday(),
 #    discount_type: "Transaction level",
 #    tax_Type: "",
 #    amount_due: 0,
 #    supply_place: "",
 #    sub_total: 0,
 #    total: 0,
 #    cgst_total:0,
 #    sgst_total:0,
 #    igst_total: 0,
 #    cess:false,
 #    cess_total: 0,
 #    total_charges:0,
 #    tcs_id: null,
 #    notes: "",
 #    tcs_amount: 0,
 #    tcs_rate:0,
 #    tcs_id:null,
 #    select_tax:"TDS",
 #    tds_amount:0,
 #    tds_rate:0,
 #    tds_id:null,
 #    total_quantity: 0,
 #    entered_discount: 0,
 #    discount_account: null,
 #    discount: 0,
 #    paymentterm: null,
 #    terms_condition: "",
 #    term_name: "",
 #    no_of_days: 0,
 #    attach_file: null,
 #    is_converted: false