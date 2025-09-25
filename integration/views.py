from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from integration.serializers import *
from integration.models import *
from salescustomer.viewsets.creditnote_view import new3creditnoteitemsViewSet,CreditNoteUpdate3ViewSet
from company.views import *
from django.db import transaction
from item.models.adjustment_model import Adjustment
from coa.models import COA
from item.models.item_model import Item,ItemGroup
from item.models.manufacturing_journal import ManufacturingJournal,StockJournal
from item.viewsets.manufacture_view import ManufactureView,StockJournalView
from purchase.viewsets.Vendor_view import VendorUpdtViewset,vendorViewset
from item.viewsets.item_view import ItemUpdateView,itemViewSet,ItemGroupView
from purchase.viewsets.Paymentmade_view import PaymentmadeJournalViewsets,UpdtPaymentMadeViewset
from salescustomer.viewsets.pr_view import new1paymentreceiveViewSet,UpdtPaymentRCvViewset
from purchase.viewsets.Debitnote_view import DebitnoteItemViewSet,DebitnoteUpdate3ViewSet
from salescustomer.viewsets.invoice_view import new3invoiceitemsViewSet,UpdateInvoiceView
from salescustomer.serializers.Tcs_serializers import tcsSerializer
from salescustomer.viewsets.salescustomer_view import CustomerUpdtViewset,newcustomerViewSet
from purchase.serializers.Tds_serializers import tdsSerializer
from purchase.viewsets.Bill_view import BillUpdateView,BillitemsViewSet
from salescustomer.models.Tcs_model import TCS
from purchase.models.Tds_model import TDS
from salescustomer.models.Salescustomer_model import SalesCustomer
from purchase.models.Vendor_model import Vendor
from purchase.models.Bill_model import Bill
from salescustomer.models.Invoice_model import Invoice
from salescustomer.models.Pr_model import PR
from purchase.models.Paymentmade_model import PaymentMade
from salescustomer.models.Creditnote_model import CreditNote
from purchase.models.Debitnote_model import DebitNote
from accounting.models import ManualJournal
from accounting.views import new1journalViewSet,UpdateJournalView
from coa.views import CoaSubheadView,Opening_BalanceViewSet
from django.db.models import Q
from item.models.stock_model import Batch,WareHouse
from item.serializers.stock_serializers import GodownSerializer
from item.viewsets.adjustmet_view import AdjustmentViewSet,ItemInventoryUpdateView

# Create your views here.


class VersionView(APIView):

    def get(self,request,name):

        try:
            obj = VersionHelper.objects.get(name=name)

            return Response({"version":obj.version,"path":obj.file.url},status=200)
        except:
            pass


class StockView(APIView):
    def get(self,request,db_item_id=None):
        if db_item_id:
            batch_no = request.GET['batch_no']
            expire_date = request.GET['expire_date']
            mfg_date = request.GET['mfg_date']
            if not expire_date:
                expire_date = None
            if not mfg_date:
                mfg_date = None
            obj = Batch.objects.filter(item_id=db_item_id,
                                       batch_no=batch_no,
                                       mfg_date=mfg_date,
                                       expire_date=expire_date)
            if obj.exists():
                obj = obj[0]
                return Response({"stock_quantity": obj.stock_quantity}, status=200)
            return Response({"stock_quantity": 0}, status=200)

# @method_decorator(cache_page(60 * 180, cache="default"), name='dispatch')
class IdViews(APIView):


    def get(self,request,item_id=None,
            bill_id=None,invoice_id=None,item_grp_id=None,wh_id=None,gst_no=None,
            tcs_id=None,tds_id=None,coa_id=None, company_id=None,customer_id=None,vendor_id=None,branch_id=None):
        if gst_no and company_id:
            obj = Branch.objects.filter(gstin=gst_no, company_id=company_id)
            if obj.exists():
                obj = obj[0]
                return Response({"branch_id": obj.branch_id}, status=200)
            obj = Branch.objects.filter(main_branch=True, company_id=company_id)
            return Response({"branch_id": obj[0].branch_id}, status=200)
        if wh_id and branch_id:
            obj = WareHouse.objects.filter(ext_id=wh_id,branch_id=branch_id)
            if obj.exists():
                obj = obj[0]
                return Response({"wh_id":obj.wh_id},status=200)
            return Response({"wh_id": None}, status=200)
        if item_id and branch_id:
            obj = Item.objects.filter(ext_id=item_id,branch_id=branch_id)
            if obj.exists():
                obj = obj[0]
                return Response({"item_id":obj.item_id},status=200)
            return Response({"item_id": None}, status=200)

        elif item_grp_id and branch_id:
            obj = ItemGroup.objects.filter(ext_id=item_grp_id,branch_id=branch_id)
            if obj.exists():
                obj = obj[0]
                return Response({"item_grp_id":obj.item_grp_id},status=200)
            return Response({"item_grp_id": None}, status=200)
        elif tcs_id and branch_id:
            obj = TCS.objects.filter(ext_id=tcs_id,branch_id=branch_id)
            if obj.exists():
                obj = obj[0]
                return Response({"tcs_id": obj.tcs_id}, status=200)
            return Response({"tcs_id": None}, status=200)
        elif tds_id and branch_id:
            obj = TDS.objects.filter(ext_id=tds_id,branch_id=branch_id)
            if obj.exists():
                obj = obj[0]
                return Response({"tds_id": obj.tds_id}, status=200)
            return Response({"tds_id": None}, status=200)
        elif coa_id and company_id:
            obj = COA.objects.filter(ext_id=coa_id,company_id=company_id)
            if obj.exists():
                obj = obj[0]
                return Response({"coa_id": obj.coa_id,"account_type":obj.account_type}, status=200)
            return Response({"coa_id": None}, status=200)
        elif company_id:
            inventory = COA.objects.filter(company_id=company_id,account_subhead='Stock',
                                           account_name='Inventory Assets',isdefault=True)
            purchase = COA.objects.filter(company_id=company_id, account_subhead='Purchase Expense',
                                          isdefault=True,
                                           account_name='Purchase')
            sales = COA.objects.filter(company_id=company_id, account_subhead='Income Customer',
                                           account_name='Sales',isdefault=True)
            result = {}
            if inventory.exists():
                obj = inventory[0]
                result["inventory_account"] = obj.coa_id
                result["inventory_account_name"] = obj.account_name
            else:
                result["inventory_account"] = None
                result["inventory_account_name"] = None
            if purchase.exists():
                obj = purchase[0]
                result["purchase_account"] = obj.coa_id
                result["purchase_account_name"] = obj.account_name
            else:
                result["purchase_account"] = None
                result["purchase_account_name"] = None
            if sales.exists():
                obj = sales[0]
                result["sales_account"] = obj.coa_id
                result["sales_account_name"] = obj.account_name
            else:
                result["sales_account"] = None
                result["sales_account_name"] = None
            print(result)
            return Response(result, status=200)
        elif customer_id:
            obj = SalesCustomer.objects.filter(ext_id=customer_id)
            if obj.exists():
                obj = obj[0]
                return Response({"customer_id": obj.customer_id}, status=200)
            return Response({"customer_id": None}, status=200)
        elif vendor_id:
            obj = Vendor.objects.filter(ext_id=vendor_id,branch_id=branch_id)

            if obj.exists():
                obj = obj[0]
                return Response({"vendor_id": obj.vendor_id}, status=200)
            return Response({"vendor_id": None}, status=200)
        elif bill_id:
            obj = Bill.objects.filter(ext_id=bill_id,branch_id=branch_id)

            if obj.exists():
                obj = obj[0]
                return Response({"bill_id": obj.bill_id}, status=200)
            return Response({"bill_id": None}, status=200)
        elif invoice_id:
            obj = Invoice.objects.filter(ext_id=invoice_id,branch_id=branch_id)
            print(obj)
            if obj.exists():
                obj = obj[0]
                return Response({"invoice_id": obj.invoice_id}, status=200)
            return Response({"invoice_id": None}, status=200)
        else:
            return Response(status=400)

    def post(self,request):
        data = request.data
        serializer = ItemBatchSerializer(data=data)
        if serializer.is_valid():
            qty = 0
            try:
                batch = Batch.objects.get(Q(item_id=data['item_id'],
                                            branch_id=data['branch_id'],
                                            expire_date=data['expire_date'],
                                            mfg_date=data['mfg_date'],
                                            batch_no=data['batch_no'] ))
                qty = batch.stock_quantity
            except:
                pass
            return Response({"stock_quantity":qty},status=200)
        return Response(serializer.errors,status=400)


class TcsManyView(APIView):
    @transaction.atomic
    def post(self,request):
        data = request.data
        for tcs in data:
            print(tcs)
            ext_id = tcs.get('ext_id')
            branch_id = tcs.get('branch_id')
            obj = TCS.objects.filter(ext_id=ext_id,branch_id=branch_id)
            if obj.exists():
                obj = obj[0]
                serializer = tcsSerializer(obj,data=tcs)
                if serializer.is_valid():
                    serializer.save()
                    print("updated")
                else:
                    return Response(status=400)
            else:
                serializer = tcsSerializer(data=tcs)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(status=400)
        else:
            return Response(status=200)

class GodownManyView(APIView):
    @transaction.atomic
    def post(self,request):
        data = request.data
        for ware in data:
            print(ware)
            ext_id = ware.get('ext_id')
            branch_id = ware.get('branch_id')
            obj = WareHouse.objects.filter(ext_id=ext_id,branch_id=branch_id)
            if obj.exists():
                obj = obj[0]
                serializer = GodownSerializer(obj,data=ware)
                if serializer.is_valid():
                    serializer.save()
                    print("updated")
                else:
                    return Response(status=400)
            else:
                serializer = GodownSerializer(data=ware)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(status=400)
        else:
            return Response(status=200)

class TdsManyView(APIView):

    @transaction.atomic
    def post(self,request):
        data = request.data
        for tds in data:
            print(tds)
            ext_id = tds.get('ext_id')
            branch_id = tds.get('branch_id')
            obj = TDS.objects.filter(ext_id=ext_id,branch_id=branch_id)
            if obj.exists():
                obj = obj[0]
                serializer = tdsSerializer(obj, data=tds)
                if serializer.is_valid():
                    serializer.save()
                    print("updated")
                else:
                    print(serializer.errors)
                    return Response(serializer.errors,status=400)
            else:
                serializer = tdsSerializer(data=tds)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    return Response(serializer.errors,status=400)
        else:
            return Response(status=200)



class TaskView(APIView):

    def get(self,request,pk=None,company_id=None,branch_id=None):
        if pk:
            obj = Task.objects.get(task_id=pk)
            serializer = TaskSerializer(obj)
            return Response(serializer.data,status=200)
        if company_id and branch_id:

            limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
            offset = int(request.GET.get('offset', 0))
            objs = Task.objects.filter(company_id=company_id,branch_id=branch_id)
            url = str(request.build_absolute_uri()).split("?")[0]
            response = {
                'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": objs.count()
            }
            objs = objs[offset:offset + limit]
            serializer = TaskSerializer(objs,many=True)
            response['results'] = serializer.data
            return Response(response,status=200)

    def post(self,request):
        data = request.data
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            print(serializer.errors)
            return Response(status=400)

    def patch(self, request, pk):
        obj = Task.objects.get(task_id=pk)

        serializer = TaskSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyManyView(APIView):
    pass


class OpeningBalanceView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        ob_data = data.get('data', [])
        task_id = data.get('task_id', [])
        task = Task.objects.select_for_update().get(task_id=task_id)
        view_obj = Opening_BalanceViewSet()
        response = view_obj.handle_post(ob_data)
        return response

class BranchManyView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        branch_data = data.get('data', [])
        company_id = data.get('company_id')
        if branch_data:
            for obj in branch_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    branch_obj = Branch.objects.filter(ext_id=ext_id, company_id=company_id)

                    if branch_obj.exists():
                        branch_obj = branch_obj[0]
                        view_obj = branchViewSet()
                        response = view_obj.handle_put(obj, branch_obj.branch_id)
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = branchViewSet()
                        response = view_obj.handle_post(obj,request.user)

                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)

    @transaction.atomic
    def put(self,request,branch_id):
        data = request.data
        branch_data = data.get('data',[])
        task_id = data.get('task_id',[])
        task = Task.objects.select_for_update().get(task_id=task_id)
        task.status = "PROCESSING"
        task.error_message = ''
        task.message = ''
        task.save()

        if branch_data:
            branch = branchViewSet()
            return branch.handle_put(branch_data,branch_id)
        print(branch_data,"test_2")
        return Response({"message":"No Data Send"},status=400)

class CoaManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        coa_data = data.get('data', [])
        company_id = data.get('company_id')
        if coa_data:
            for obj in coa_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    coa_obj = COA.objects.filter(ext_id=ext_id,company_id=company_id)

                    if coa_obj.exists():
                        coa_obj = coa_obj[0]
                        view_obj = CoaSubheadView()
                        response = view_obj.handle_update(obj,coa_obj.coa_id)
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = CoaSubheadView()
                        response = view_obj.handle_post(obj)

                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)


class ItemGroupManyView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        item_grp_data = data.get('data', [])
        branch_id = data.get('branch_id')
        if item_grp_data:
            for obj in item_grp_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    item_grp_obj = ItemGroup.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if item_grp_obj.exists():
                        item_grp_obj = item_grp_obj[0]
                        view_obj = ItemGroupView()
                        response = view_obj.handle_update(obj, item_grp_obj.item_grp_id)
                        if response.status_code < 300:
                            continue
                        else:
                            return response
                    else:
                        view_obj = ItemGroupView()
                        response = view_obj.handle_post(obj)

                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)


class ItemInventoryManyView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        inventory_data = data.get('data', [])
        branch_id = data.get('branch_id')
        print(inventory_data,"inventory")
        if inventory_data:
            for obj in inventory_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    adj_obj = Adjustment.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if adj_obj.exists():
                        adj_obj = adj_obj[0]
                        view_obj = ItemInventoryUpdateView()
                        response = view_obj.handle_update(obj, adj_obj.adj_id)

                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = AdjustmentViewSet()
                        response = view_obj.handle_post(obj)

                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)

class ItemManyView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        item_data = data.get('data', [])
        branch_id = data.get('branch_id')
        print(item_data,"items")
        if item_data:
            for obj in item_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    item_obj = Item.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if item_obj.exists():
                        item_obj = item_obj[0]
                        view_obj = ItemUpdateView()
                        response = view_obj.handle_update(obj, item_obj.item_id)

                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = itemViewSet()
                        response = view_obj.handle_post(obj)

                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)

    def patch(self,request,pk=None):
        try:
            data = request.data
            print(data)
            full_inventory = data.get('full_inventory',None)
            obj = Item.objects.get(item_id=pk)
            print(obj)
            obj.full_inventory = full_inventory
            obj.save()
            return Response(status=200)
        except Exception as e:
            print(e)
            return Response(status=400)

class OpeningStockView(APIView):
    pass




class MfgManyView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        mfg_data = data.get('data', [])
        branch_id = data.get('branch_id')

        if mfg_data:
            for obj in mfg_data:
                print(obj)
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    mfg_obj = ManufacturingJournal.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if mfg_obj.exists():
                        mfg_obj = mfg_obj[0]
                        print("updating",ext_id)
                        view_obj = ManufactureView()
                        response = view_obj.handle_update(user,obj,mfg_obj.mfg_id)

                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            continue
                            return response
                    else:
                        print("creating", ext_id)
                        view_obj = ManufactureView()
                        response = view_obj.handle_post(user,obj)

                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            continue
                            return response
            else:
                return Response(status=200)

        return Response(status=400)

class StockJournalManyView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        stk_data = data.get('data', [])
        branch_id = data.get('branch_id')
        if stk_data:
            for obj in stk_data:
                print(obj)
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    stk_obj = StockJournal.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if stk_obj.exists():
                        stk_obj = stk_obj[0]
                        print("updating",ext_id)
                        view_obj = StockJournalView()
                        response = view_obj.handle_update(user,obj,stk_obj.sj_id)
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            continue
                            return response
                    else:
                        print("creating", ext_id)
                        view_obj = StockJournalView()
                        response = view_obj.handle_post(user,obj)

                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            continue
                            return response
            else:

                return Response(status=200)

        return Response(status=400)

class BillManyView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        bill_data = data.get('data', [])
        branch_id = data.get('branch_id')

        if bill_data:
            for obj in bill_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    bill_obj = Bill.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if bill_obj.exists():
                        bill_obj = bill_obj[0]

                        view_obj = BillUpdateView()
                        try:
                            response = view_obj.handle_update(user,obj, None,bill_obj.bill_id)
                        except:
                            continue
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:

                            return response
                    else:
                        view_obj = BillitemsViewSet()
                        response = view_obj.handle_post(user,obj,None)

                        if response.status_code < 300:
                            print("created")
                            continue
                        else:

                            return response
            else:

                return Response(status=200)

        return Response(status=400)

class VendorManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data

        vendor_data = data.get('data', [])
        branch_id = data.get('branch_id')

        if vendor_data:
            for obj in vendor_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    vendor_obj = Vendor.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if vendor_obj.exists():
                        vendor_obj = vendor_obj[0]
                        view_obj = VendorUpdtViewset()
                        response = view_obj.handle_update(obj,  vendor_obj.vendor_id)

                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = vendorViewset()
                        response = view_obj.handle_post(obj,None)
                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)


class ExpenseManyView(APIView):
    pass


class PurchaseOrderManyView(APIView):
    pass


class PaymentMadeManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        pm_data = data.get('data', [])
        branch_id = data.get('branch_id')

        if pm_data:
            for obj in pm_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    print(ext_id,">>>>>>>>>>>>>",obj['payment_serial'])
                    pm_obj = PaymentMade.objects.filter(ext_id=ext_id,branch_id=branch_id,bill_id_id=obj['bill_id'])
                    if pm_obj.exists():
                        pm_obj = pm_obj[0]
                        view_obj = UpdtPaymentMadeViewset()
                        response = view_obj.handle_update(user,obj, pm_obj.pm_id)

                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = PaymentmadeJournalViewsets()
                        response = view_obj.handle_post(user,obj)
                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)


class DebitNoteManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        dn_data = data.get('data', [])
        branch_id = data.get('branch_id')
        user = request.user
        if dn_data:
            for obj in dn_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    dn_obj = DebitNote.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if dn_obj.exists():
                        dn_obj = dn_obj[0]

                        view_obj = DebitnoteUpdate3ViewSet()
                        response = view_obj.handle_update(user,obj, None,dn_obj.dn_id)
                        print(response, obj)
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = DebitnoteItemViewSet()
                        response = view_obj.handle_post(user,obj,None)
                        print(response,obj)
                        if response.status_code < 300:
                            print("created")
                            continue
                        else:

                            return response
            else:

                return Response(status=200)

        return Response(status=400)


class CustomerManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data

        vendor_data = data.get('data', [])
        branch_id = data.get('branch_id')

        if vendor_data:
            for obj in vendor_data:
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    customer_obj = SalesCustomer.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if customer_obj.exists():
                        customer_obj = customer_obj[0]

                        view_obj = CustomerUpdtViewset()
                        response = view_obj.handle_update(obj, customer_obj.customer_id)

                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = newcustomerViewSet()
                        response = view_obj.handle_post(obj,None)
                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:

                return Response(status=200)
        return Response(status=400)


class EstimateManyView(APIView):
    pass


class SalesOrderManyView(APIView):
    pass


class DeliverChallanManyView(APIView):
    pass


class InvoiceManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        invoice_data = data.get('data', [])
        branch_id = data.get('branch_id')

        if invoice_data:
            for index,obj in enumerate(invoice_data):
                print(f"count is {index+1} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    inv_obj = Invoice.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if inv_obj.exists():
                        inv_obj = inv_obj[0]
                        view_obj = UpdateInvoiceView()
                        response = view_obj.handle_update(user,obj,None, inv_obj.invoice_id)
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:

                            return response
                    else:
                        view_obj = new3invoiceitemsViewSet()
                        response = view_obj.handle_post(user,obj, None)
                        if response.status_code < 300:
                            print("created")
                            continue
                        else:

                            return response
            else:
                return Response(status=200)
        return Response(status=400)


class PaymentReceivedManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        pm_data = data.get('data', [])
        branch_id = data.get('branch_id')

        if pm_data:
            for obj in pm_data:
                ext_id = obj.get('ext_id', None)
                if obj['payment_serial'] == '281':
                    print(obj,"28881111111111111111")
                if ext_id:
                    pr_obj = PR.objects.filter(ext_id=ext_id,branch_id=branch_id,invoice_id_id=obj['invoice_id'])
                    if pr_obj.exists():
                        pr_obj = pr_obj[0]
                        view_obj = UpdtPaymentRCvViewset()
                        response = view_obj.handle_update(user,obj, None, pr_obj.pr_id)
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = new1paymentreceiveViewSet()
                        response = view_obj.handle_post(user,obj, None)
                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)


class CreditNoteManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data

        cn_data = data.get('data', [])
        branch_id = data.get('branch_id')
        user = request.user
        if cn_data:
            for obj in cn_data:
                print(obj)
                ext_id = obj.get('ext_id', None)
                if ext_id:
                    cn_obj = CreditNote.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if cn_obj.exists():
                        cn_obj = cn_obj[0]

                        view_obj = CreditNoteUpdate3ViewSet()
                        response = view_obj.handle_update(user,obj, None, cn_obj.cn_id)
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            return response
                    else:
                        view_obj = new3creditnoteitemsViewSet()
                        response = view_obj.handle_post(user,obj, None)
                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            return response
            else:
                return Response(status=200)
        return Response(status=400)


class VoucherManyView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        vch_data = data.get('data', [])
        branch_id = data.get('branch_id')

        if vch_data:
            for obj in vch_data:
                # print(obj)
                ext_id = obj.get('ext_id', None)
                print(obj)
                if ext_id:
                    vch_obj = ManualJournal.objects.filter(ext_id=ext_id,branch_id=branch_id)
                    if vch_obj.exists():
                        vch_obj = vch_obj[0]
                        view_obj = UpdateJournalView()
                        response = view_obj.handle_update(user,obj, vch_obj.mj_id)
                        if response.status_code < 300:
                            print("updated")
                            continue
                        else:
                            print(response)
                            return response
                    else:
                        view_obj = new1journalViewSet()
                        response = view_obj.handle_post(user,obj)
                        if response.status_code < 300:
                            print("created")
                            continue
                        else:
                            print(response)
                            return response
            else:
                return Response(status=200)

        return Response(status=400)


class GeneralVoucherType(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        gen_vch_data = data.get('data', [])
        branch_id = data.get('branch_id')
        if gen_vch_data:
            for gen_obj in gen_vch_data:

                ext_id = gen_obj.get('ext_id', None)
                module = gen_obj.get('voucher_type', None)
                print(gen_obj,module)
                if not module:
                    return Response({"message":"No module Found"},status=400)
                if ext_id:
                    if module == "Bill":

                        bill_obj = Bill.objects.filter(ext_id=ext_id, branch_id=branch_id)
                        if bill_obj.exists():
                            bill_obj = bill_obj[0]

                            view_obj = BillUpdateView()
                            try:
                                response = view_obj.handle_update(user, gen_obj, None, bill_obj.bill_id)
                            except:
                                continue
                            if response.status_code < 300:
                                print("updated")
                                continue
                            else:

                                return response
                        else:
                            view_obj = BillitemsViewSet()
                            response = view_obj.handle_post(user, gen_obj, None)

                            if response.status_code < 300:
                                print("created")
                                continue
                            else:

                                return response
                    elif module == "Invoice":

                        inv_obj = Invoice.objects.filter(ext_id=ext_id, branch_id=branch_id)
                        if inv_obj.exists():
                            inv_obj = inv_obj[0]
                            view_obj = UpdateInvoiceView()
                            response = view_obj.handle_update(user, gen_obj, None, inv_obj.invoice_id)
                            if response.status_code < 300:
                                print("updated")
                                continue
                            else:
                                return response
                        else:
                            view_obj = new3invoiceitemsViewSet()
                            response = view_obj.handle_post(user, gen_obj, None)
                            if response.status_code < 300:
                                print("created")
                                continue
                            else:
                                return response
                    elif module == "DebitNote":
                        dn_obj = DebitNote.objects.filter(ext_id=ext_id, branch_id=branch_id)
                        if dn_obj.exists():
                            dn_obj = dn_obj[0]
                            view_obj = DebitnoteUpdate3ViewSet()
                            response = view_obj.handle_update(user, gen_obj, None, dn_obj.dn_id)
                            if response.status_code < 300:
                                print("updated")
                                continue
                            else:
                                return response
                        else:
                            view_obj = DebitnoteItemViewSet()
                            response = view_obj.handle_post(user, gen_obj, None)
                            if response.status_code < 300:
                                print("created")
                                continue
                            else:
                                return response
                    elif module == "MfgJournal":

                        mfg_obj = ManufacturingJournal.objects.filter(ext_id=ext_id, branch_id=branch_id)
                        if mfg_obj.exists():
                            mfg_obj = mfg_obj[0]
                            print("updating", ext_id)
                            view_obj = ManufactureView()
                            response = view_obj.handle_update(user, gen_obj, mfg_obj.mfg_id)

                            if response.status_code < 300:
                                print("updated")
                                continue
                            else:

                                return response
                        else:
                            print("creating", ext_id)
                            view_obj = ManufactureView()
                            response = view_obj.handle_post(user, gen_obj)

                            if response.status_code < 300:
                                print("created")
                                continue
                            else:

                                return response
                    elif module == "StockJournal":

                        stk_obj = StockJournal.objects.filter(ext_id=ext_id, branch_id=branch_id)
                        if stk_obj.exists():
                            stk_obj = stk_obj[0]
                            print("updating", ext_id)
                            view_obj = StockJournalView()
                            response = view_obj.handle_update(user, gen_obj, stk_obj.sj_id)
                            if response.status_code < 300:
                                print("updated")
                                continue
                            else:

                                return response
                        else:
                            print("creating", ext_id)
                            view_obj = StockJournalView()
                            response = view_obj.handle_post(user, gen_obj)

                            if response.status_code < 300:
                                print("created")
                                continue
                            else:
                                return response
                    elif module == "CreditNote":
                        obj = CreditNote.objects.filter(ext_id=ext_id, branch_id=branch_id)
                        if obj.exists():
                            obj = obj[0]
                            view_obj = CreditNoteUpdate3ViewSet()
                            response = view_obj.handle_update(user, gen_obj, None, obj.cn_id)
                            if response.status_code < 300:
                                print("updated")
                                continue
                            else:
                                return response
                        else:
                            view_obj = new3creditnoteitemsViewSet()
                            response = view_obj.handle_post(user,gen_obj, None)
                            if response.status_code < 300:
                                print("created")
                                continue
                            else:
                                return response
            else:
                return Response(status=200)
        return Response(status=400)


class LogsView(APIView):

    def get(self,request,task_id):
        logs = TaskLogs.objects.filter(task_id=task_id)
        serializer = TaskLogSerializer(logs,many=True)
        return Response(serializer.data,status=200)

    @transaction.atomic
    def post(self,request):
        data = request.data
        print(data)
        serializer = TaskLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(serializer.errors,status=400)