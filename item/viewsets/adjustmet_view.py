import imp
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from item.models.item_model import Item
from transaction .models import MasterTransaction
from coa .models import COA
from company.models import Company,Branch
from item.models.stock_model import Stock,Batch
import os
from pathlib import Path
from django.db.models import Q
from item.models.adjustment_model import Adjustment
from item.serializers.adjustment_serializers import (AdjustmentSerializer,JoinAdjustmentAndAdjustItemSerializer,
                                                     AdjustmentSerializerForShortView)
from item.models.adjustment_item_model import AdjustmentItem
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db import transaction as trans
import traceback
class AdjustmentViewSet(viewsets.ModelViewSet):
    queryset = Adjustment.objects.all()
    serializer_class =AdjustmentSerializer


    def handle_post(self,data):
        with trans.atomic():
            try:
                Adj_data_converte = data


                Adj_data = Adj_data_converte
                Adj_items = Adj_data['ajustment_items']
                print(Adj_items)
                comp_id = Company.objects.get(company_id=Adj_data["company_id"])
                branch_id = Branch.objects.get(branch_id=Adj_data['branch_id'])
                # coa_id = COA.objects.get(coa_id=Adj_data["coa_id"])
                bch_id = Adj_data['branch_id']
                # Adjustment  fields
                # All The Ajustment field to use the Serializers Field
                Adj_serializer = AdjustmentSerializer(data=Adj_data)
                if Adj_serializer.is_valid():
                    Adj_id = Adj_serializer.save()
                    # Adj_id.attach_file = Adj_file_data
                    Adj_id.company_id = comp_id
                    Adj_id.branch_id = branch_id
                    # Adj_id.coa_id = coa_id
                    Adj_id.status = 'Adjusted'
                    Adj_id.save()
                    print("**********************Test******************************")
                    print(Adj_serializer.data)
                else:
                    print(Adj_serializer.errors)
                    return Response(Adj_serializer.errors)

                # Selected Adjsument Item
                for item in Adj_items:
                    item_adj = Item.objects.get(item_id=item["item_id"])
                    batch_no = item['batches']
                    mfg_date = item["mfg_date"]
                    expire_date = item["expire_date"]
                    if not batch_no:
                        batch_no.append(None)
                    if Stock.objects.filter(Q(item_id=item['item_id'], batch_no=batch_no[0],
                                              expire_date=expire_date,
                                              mfg_date=mfg_date,
                                              branch_id=bch_id,
                                              )).exists():
                        stock_item = Stock.objects.filter(Q(item_id=item['item_id'], batch_no=batch_no[0],
                                                            expire_date=expire_date,
                                                            mfg_date=mfg_date,
                                                            branch_id=bch_id,
                                                            )).latest('created_date')
                        stock_rate = stock_item.rate

                    else:
                        stock_rate = item_adj.cost_price
                        print('Stock Rate is Here', stock_rate)
                        stock_in = item["quantity"]
                        stock_out = 0

                    print('AAA', item)
                    adjusted_items = AdjustmentItem.objects.create(adj_id=Adj_id,
                                                                   item_id=item["item_id"],
                                                                   item_name=item["item_name"],
                                                                   changed_value=item["changed_value"],
                                                                   adjusted_value=item["adjusted_value"],
                                                                   rate=stock_rate,
                                                                   batch_no=batch_no,
                                                                   mfg_date=item["mfg_date"],
                                                                   expire_date=item["expire_date"],
                                                                   current_value=item["current_value"],
                                                                   quantity=item['quantity'],
                                                                   stock_quantity=item['stock_quantity'],
                                                                   adjusted_qty=item['adjusted_qty'])
                    adjusted_items.save()

                # User Can Select The Quntity Adjustment This Section Can Execute
                Quantity = Adj_data['adj_type']
                if Quantity == 'Quantity':
                    stock_on_hand = item['stock_on_hand']
                    expire_date = item['expire_date']
                    mfg_date = item['mfg_date']
                    for item in Adj_items:
                        print(item)
                        batch_no = item['batches']
                        if not batch_no:
                            batch_no.append(None)
                            mfg_date = None
                            expire_date = None

                        item_adj = Item.objects.get(Q(item_id=item["item_id"]))
                        if item['adjusted_qty'] < 0:
                            print('stock_hand', stock_on_hand)
                            print('quantity', item['adjusted_qty'])
                            adj_qty = float(stock_on_hand) - float(item['adjusted_qty'])
                            adj_in = float(item['adjusted_qty'])


                        else:
                            print('stock_hand1', stock_on_hand)
                            print('quantity1', item['adjusted_qty'])
                            adj_qty = float(stock_on_hand) + float(item['adjusted_qty'])
                            adj_in = float(item['adjusted_qty'])
                            print('Adj_qunty1', adj_qty)

                        # First Time You Creating the directly Adjustment From
                        # So frist time stock table are empty So this situation item cost price
                        # item are exist so Stock table item reate assign
                        if Stock.objects.filter(Q(item_id=item["item_id"],
                                                  mfg_date=mfg_date,
                                                  expire_date=expire_date,
                                                  branch_id=bch_id,
                                                  batch_no=batch_no[0])).exists():
                            stock_item = Stock.objects.filter(Q(item_id=item['item_id'], batch_no=batch_no[0],
                                                                mfg_date=mfg_date,
                                                                expire_date=expire_date,
                                                                branch_id=bch_id,
                                                                )).latest('created_date')
                            stock_rate = float(stock_item.rate)
                            stock_amount = float(stock_item.amount)
                            print(adj_in)

                            if adj_in < 0:
                                stock_in = 0
                                stock_out = item["adjusted_qty"]
                                amount_out = stock_rate * abs(stock_out)
                                amount = stock_amount - amount_out
                            else:
                                stock_in = abs(adj_in)
                                stock_out = 0

                                amount_in = stock_rate * abs(stock_in)
                                amount = stock_amount + amount_in

                        else:
                            stock_rate = item_adj.cost_price
                            print('Stock Rate is Here', stock_rate)
                            stock_in = float(item["quantity"])
                            stock_out = 0
                            amount = float(stock_in) * abs(float(stock_rate))

                        print(amount, ">>>>>>>>>>>>>")
                        stock_items = Stock.objects.create(
                            item_id=item["item_id"],
                            item_name=item["item_name"],
                            quantity=item["quantity"],
                            rate=stock_rate,
                            stock_out=abs(stock_out),
                            stock_in=stock_in,
                            ref_id=Adj_id.adj_id,
                            company_id=comp_id,
                            branch_id=branch_id,
                            ref_tblname='Adjustment',
                            amount=amount,
                            batch_no=batch_no[0],
                            mfg_date=item["mfg_date"],
                            expire_date=item["expire_date"],
                            module='Inventory',
                            formname='Quantity',
                            stage='Add Stages',
                            adjusted_qty=item['adjusted_qty'],
                            date=Adj_data["adj_date"])
                        stock_items.save()

                        # Items Puchase Account And Inventroy Account
                        purchase_account = Item.objects.get(item_id=item['item_id']).purchase_account
                        inventory_account = Item.objects.get(item_id=item['item_id']).inventory_account

                        FROM_COA = COA.objects.get(company_id=comp_id, coa_id=inventory_account)
                        TO_COA = COA.objects.get(company_id=comp_id, coa_id=purchase_account)
                        stkmast = MasterTransaction.objects.create(
                            L1detail_id=Adj_id.adj_id,
                            L1detailstbl_name='Adjusment',
                            L2detail_id=stock_items.st_id,
                            L2detailstbl_name='Stock',
                            main_module='Inventory',
                            module='Inventory',
                            sub_module='Adjusment',
                            transc_deatils='Adjusment',
                            banking_module_type='Inventory',
                            journal_module_type='Inventory',
                            trans_date=Adj_data["adj_date"],
                            trans_status='Manually Added',
                            debit=amount,
                            to_account=FROM_COA.coa_id,
                            to_acc_type=FROM_COA.account_type,
                            to_acc_head=FROM_COA.account_head,
                            to_acc_subhead=FROM_COA.account_subhead,
                            to_acc_name=FROM_COA.account_name,
                            credit=amount,
                            from_account=TO_COA.coa_id,
                            from_acc_type=TO_COA.account_type,
                            from_acc_head=TO_COA.account_head,
                            from_acc_subhead=TO_COA.account_subhead,
                            from_acc_name=TO_COA.account_name,
                            branch_id=branch_id,
                            company_id=comp_id)
                        stkmast.save()

                # User Can Select the Value AdjustMent This Section Can Excute
                else:
                    print(Adj_items, "*******************************************")
                    for item in Adj_items:
                        if float(item["changed_value"]) > 0:

                            item_obj = Item.objects.get(item_id=item['item_id'])

                            batch_no = item['batches']
                            mfg_date = item["mfg_date"]
                            expire_date = item["expire_date"]
                            if not batch_no:
                                batch_no.append(None)
                                mfg_date = None
                                expire_date = None

                            batch_obj = Batch.objects.get(Q(item_id=item['item_id'],
                                                            batch_no=batch_no[0],
                                                            expire_date=expire_date,
                                                            mfg_date=mfg_date,
                                                            branch_id=bch_id,
                                                            ))

                            rate = float(item["changed_value"]) // batch_obj.stock_quantity
                            item_obj.cost_price = rate
                            item_obj.save()
                            stock_items = Stock.objects.create(
                                item_id=item['item_id'],
                                item_name=item["item_name"],
                                stock_in=item["quantity"],
                                amount=item["changed_value"],
                                rate=rate,
                                batch_no=batch_no[0],
                                mfg_date=mfg_date,
                                expire_date=expire_date,
                                quantity=item["stock_on_hand"],
                                ref_id=Adj_id.adj_id,
                                ref_tblname='Adjustment',
                                module='Adjustment',
                                formname='Value',
                                stage='Add Stages',
                                date=Adj_data["adj_date"],
                                branch_id=branch_id,
                                company_id=comp_id)

                            # =Adj_data.get('adjustment_items')
                            purchase_account = Item.objects.get(item_id=item['item_id']).purchase_account
                            inventory_account = Item.objects.get(item_id=item['item_id']).inventory_account

                            FROM_COA = COA.objects.get(company_id=comp_id, coa_id=inventory_account)
                            TO_COA = COA.objects.get(company_id=comp_id, coa_id=purchase_account)
                            stkmast = MasterTransaction.objects.create(
                                L1detail_id=Adj_id.adj_id,
                                L1detailstbl_name='Adjusment',
                                L2detail_id=stock_items.st_id,
                                L2detailstbl_name='Stock',
                                main_module='Inventory',
                                module='Inventory',
                                sub_module='Adjusment',
                                transc_deatils='Adjusment',
                                banking_module_type='Inventory',
                                journal_module_type='Inventory',
                                trans_date=Adj_data["adj_date"],
                                trans_status='Manually Added',
                                debit=Adj_items[0]["stock_on_hand"],
                                to_account=FROM_COA.coa_id,
                                to_acc_type=FROM_COA.account_type,
                                to_acc_head=FROM_COA.account_head,
                                to_acc_subhead=FROM_COA.account_subhead,
                                to_acc_name=FROM_COA.account_name,
                                credit=Adj_items[0]["stock_on_hand"],
                                from_account=TO_COA.coa_id,
                                from_acc_type=TO_COA.account_type,
                                from_acc_head=TO_COA.account_head,
                                from_acc_subhead=TO_COA.account_subhead,
                                from_acc_name=TO_COA.account_name,
                                company_id=comp_id)
                            stkmast.save()

                serializer = AdjustmentSerializer(Adj_id)
                return Response(serializer.data)
            except Exception as e:
                traceback.print_exc()
                print(e)
                trans.set_rollback(True)
                return Response({"message": 'Stock Not Available'}, status=400)

    def create(self, request):
        data = request.data
        return self.handle_post(data)

class ItemInventoryUpdateView(APIView):

    def handle_update(self, data, pk):
        with trans.atomic():
            try:
                adj = Adjustment.objects.get(adj_id=pk)
                Adj_items = data['ajustment_items']
                print(Adj_items)
                comp_id = Company.objects.get(company_id=data["company_id"])
                branch_id = Branch.objects.get(branch_id=data['branch_id'])
                # coa_id = COA.objects.get(coa_id=data["coa_id"])
                bch_id = data['branch_id']

                Adj_serializer = AdjustmentSerializer(adj,data=data)
                if Adj_serializer.is_valid():
                    Adj_id = Adj_serializer.save()
                    # Adj_id.attach_file = Adj_file_data
                    Adj_id.company_id = comp_id
                    Adj_id.branch_id = branch_id
                    # Adj_id.coa_id = coa_id
                    Adj_id.status = 'Adjusted'
                    Adj_id.save()
                    print("**********************Test******************************")
                    print(Adj_serializer.data)
                else:
                    print(Adj_serializer.errors)
                    return Response(Adj_serializer.errors)
                adj.adj_items.all().delete()
                Stock.objects.filter(ref_id=adj.adj_id).delete()
                MasterTransaction.objects.filter(L1detail_id=adj.adj_id).delete()
                # Selected Adjsument Item
                for item in Adj_items:
                    item_adj = Item.objects.get(item_id=item["item_id"])
                    batch_no = item['batches']
                    mfg_date = item["mfg_date"]
                    expire_date = item["expire_date"]
                    if not batch_no:
                        batch_no.append(None)
                    if Stock.objects.filter(Q(item_id=item['item_id'], batch_no=batch_no[0],
                                              expire_date=expire_date,
                                              mfg_date=mfg_date,
                                              branch_id=bch_id,
                                              )).exists():
                        stock_item = Stock.objects.filter(Q(item_id=item['item_id'], batch_no=batch_no[0],
                                                            expire_date=expire_date,
                                                            mfg_date=mfg_date,
                                                            branch_id=bch_id,
                                                            )).latest('created_date')
                        stock_rate = stock_item.rate
                        # stock_out = stock_item.stock_out - int(item["quantity"])


                    else:
                        stock_rate = item_adj.cost_price
                        print('Stock Rate is Here', stock_rate)
                        stock_in = item["quantity"]
                        stock_out = 0

                    print('AAA', item)
                    adjusted_items = AdjustmentItem.objects.create(adj_id=Adj_id,
                                                                   item_id=item["item_id"],
                                                                   item_name=item["item_name"],
                                                                   changed_value=item["changed_value"],
                                                                   adjusted_value=item["adjusted_value"],
                                                                   rate=stock_rate,
                                                                   batch_no=batch_no,
                                                                   mfg_date=item["mfg_date"],
                                                                   expire_date=item["expire_date"],
                                                                   current_value=item["current_value"],
                                                                   quantity=item['quantity'],
                                                                   stock_quantity=item['stock_quantity'],
                                                                   adjusted_qty=item['adjusted_qty'])
                    adjusted_items.save()

                # User Can Select The Quntity Adjustment This Section Can Execute
                Quantity = data['adj_type']
                if Quantity == 'Quantity':
                    stock_on_hand = item['stock_on_hand']
                    expire_date = item['expire_date']
                    mfg_date = item['mfg_date']
                    for item in Adj_items:
                        print(item)
                        batch_no = item['batches']
                        if not batch_no:
                            batch_no.append(None)
                            mfg_date = None
                            expire_date = None

                        item_adj = Item.objects.get(Q(item_id=item["item_id"]))
                        if item['adjusted_qty'] < 0:
                            print('stock_hand', stock_on_hand)
                            print('quantity', item['adjusted_qty'])
                            adj_qty = float(stock_on_hand) - float(item['adjusted_qty'])
                            adj_in = float(item['adjusted_qty'])

                        else:
                            adj_qty = float(stock_on_hand) + float(item['adjusted_qty'])
                            adj_in = float(item['adjusted_qty'])
                        if Stock.objects.filter(Q(item_id=item["item_id"],
                                                  mfg_date=mfg_date,
                                                  expire_date=expire_date,
                                                  branch_id=bch_id,
                                                  batch_no=batch_no[0])).exists():
                            stock_item = Stock.objects.filter(Q(item_id=item['item_id'], batch_no=batch_no[0],
                                                                mfg_date=mfg_date,
                                                                expire_date=expire_date,
                                                                branch_id=bch_id,
                                                                )).latest('created_date')
                            stock_rate = float(stock_item.rate)
                            stock_amount = float(stock_item.amount)
                            print(adj_in)

                            if adj_in < 0:
                                stock_in = 0
                                stock_out = item["adjusted_qty"]
                                amount_out = stock_rate * abs(stock_out)
                                amount = stock_amount - amount_out
                            else:
                                stock_in = abs(adj_in)
                                stock_out = 0

                                amount_in = stock_rate * abs(stock_in)
                                amount = stock_amount + amount_in

                        else:
                            stock_rate = item_adj.cost_price
                            print('Stock Rate is Here', stock_rate)
                            stock_in = float(item["quantity"])
                            stock_out = 0
                            amount = stock_in * abs(float(stock_rate))

                        print(amount, ">>>>>>>>>>>>>")
                        stock_items = Stock.objects.create(
                            item_id=item["item_id"],
                            item_name=item["item_name"],
                            quantity=item["quantity"],
                            rate=stock_rate,
                            stock_out=abs(stock_out),
                            stock_in=stock_in,
                            ref_id=Adj_id.adj_id,
                            company_id=comp_id,
                            branch_id=branch_id,
                            ref_tblname='Adjustment',
                            amount=amount,
                            batch_no=batch_no[0],
                            mfg_date=item["mfg_date"],
                            expire_date=item["expire_date"],
                            module='Inventory',
                            formname='Quantity',
                            stage='Add Stages',
                            adjusted_qty=item['adjusted_qty'],
                            date=data["adj_date"])
                        stock_items.save()

                        # Items Puchase Account And Inventroy Account
                        purchase_account = Item.objects.get(item_id=item['item_id']).purchase_account
                        inventory_account = Item.objects.get(item_id=item['item_id']).inventory_account

                        FROM_COA = COA.objects.get(company_id=comp_id, coa_id=inventory_account)
                        TO_COA = COA.objects.get(company_id=comp_id, coa_id=purchase_account)
                        stkmast = MasterTransaction.objects.create(
                            L1detail_id=Adj_id.adj_id,
                            L1detailstbl_name='Adjusment',
                            L2detail_id=stock_items.st_id,
                            L2detailstbl_name='Stock',
                            main_module='Inventory',
                            module='Inventory',
                            sub_module='Adjusment',
                            transc_deatils='Adjusment',
                            banking_module_type='Inventory',
                            journal_module_type='Inventory',
                            trans_date=data["adj_date"],
                            trans_status='Manually Added',
                            debit=amount,
                            to_account=FROM_COA.coa_id,
                            to_acc_type=FROM_COA.account_type,
                            to_acc_head=FROM_COA.account_head,
                            to_acc_subhead=FROM_COA.account_subhead,
                            to_acc_name=FROM_COA.account_name,
                            credit=amount,
                            from_account=TO_COA.coa_id,
                            from_acc_type=TO_COA.account_type,
                            from_acc_head=TO_COA.account_head,
                            from_acc_subhead=TO_COA.account_subhead,
                            from_acc_name=TO_COA.account_name,
                            branch_id=branch_id,
                            company_id=comp_id)
                        stkmast.save()

                # User Can Select the Value AdjustMent This Section Can Excute
                else:
                    print(Adj_items, "*******************************************")
                    for item in Adj_items:
                        if float(item["changed_value"]) > 0:

                            item_obj = Item.objects.get(item_id=item['item_id'])

                            batch_no = item['batches']
                            mfg_date = item["mfg_date"]
                            expire_date = item["expire_date"]
                            if not batch_no:
                                batch_no.append(None)
                                mfg_date = None
                                expire_date = None

                            batch_obj = Batch.objects.get(Q(item_id=item['item_id'],
                                                            batch_no=batch_no[0],
                                                            expire_date=expire_date,
                                                            mfg_date=mfg_date,
                                                            branch_id=bch_id,
                                                            ))

                            rate = float(item["changed_value"]) // batch_obj.stock_quantity
                            item_obj.cost_price = rate
                            item_obj.save()
                            stock_items = Stock.objects.create(
                                item_id=item['item_id'],
                                item_name=item["item_name"],
                                stock_in=item["quantity"],
                                amount=item["changed_value"],
                                rate=rate,
                                batch_no=batch_no[0],
                                mfg_date=mfg_date,
                                expire_date=expire_date,
                                quantity=item["stock_on_hand"],
                                ref_id=Adj_id.adj_id,
                                ref_tblname='Adjustment',
                                module='Adjustment',
                                formname='Value',
                                stage='Add Stages',
                                date=data["adj_date"],
                                branch_id=branch_id,
                                company_id=comp_id)

                            # =Adj_data.get('adjustment_items')
                            purchase_account = Item.objects.get(item_id=item['item_id']).purchase_account
                            inventory_account = Item.objects.get(item_id=item['item_id']).inventory_account

                            FROM_COA = COA.objects.get(company_id=comp_id, coa_id=inventory_account)
                            TO_COA = COA.objects.get(company_id=comp_id, coa_id=purchase_account)
                            stkmast = MasterTransaction.objects.create(
                                L1detail_id=Adj_id.adj_id,
                                L1detailstbl_name='Adjusment',
                                L2detail_id=stock_items.st_id,
                                L2detailstbl_name='Stock',
                                main_module='Inventory',
                                module='Inventory',
                                sub_module='Adjusment',
                                transc_deatils='Adjusment',
                                banking_module_type='Inventory',
                                journal_module_type='Inventory',
                                trans_date=data["adj_date"],
                                trans_status='Manually Added',
                                debit=Adj_items[0]["stock_on_hand"],
                                to_account=FROM_COA.coa_id,
                                to_acc_type=FROM_COA.account_type,
                                to_acc_head=FROM_COA.account_head,
                                to_acc_subhead=FROM_COA.account_subhead,
                                to_acc_name=FROM_COA.account_name,
                                credit=Adj_items[0]["stock_on_hand"],
                                from_account=TO_COA.coa_id,
                                from_acc_type=TO_COA.account_type,
                                from_acc_head=TO_COA.account_head,
                                from_acc_subhead=TO_COA.account_subhead,
                                from_acc_name=TO_COA.account_name,
                                company_id=comp_id)
                            stkmast.save()

                serializer = AdjustmentSerializer(Adj_id)
                return Response(serializer.data)
            except Exception as e:
                print(e)
                trans.set_rollback(True)
                return Response({"message": 'Stock Not Available'}, status=400)
    def put(self, request, pk=None):
        data = request.data
        return self.handle_update(data,pk)
# Adjustment Short View
@api_view(['GET'])
@renderer_classes([JSONRenderer])

def adjustmentshortbycompanyid(request, company_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": Adjustment.objects.filter(company_id=company_id,branch_id=branch_id).count()
    }
    
    # Get the company object by comp_id and apply pagination
    try:
        company = Company.objects.get(company_id=company_id)
        adjustments = Adjustment.objects.filter(company_id=company,branch_id=branch_id)[offset:offset + limit]

    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    response['results'] = AdjustmentSerializerForShortView(adjustments, many=True).data  #JoinDebitNoteItemSerializer
    print(response['results'])
    return Response(response)


#Adjustment Full view
@api_view(['GET'])

def addjustmentfullview(request, adj_id):
    #company = Company.objects.get(company_id=company_id)
    ad = Adjustment.objects.get(adj_id=adj_id)
    serializer = JoinAdjustmentAndAdjustItemSerializer(ad)
    return Response(serializer.data)



# Get item details by item type 
@api_view(['GET'])

def getAdjustmentDetailsByItemName(request,company_id, name):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count":Item.objects.filter(name__icontains=name,company_id=company_id).count()}
    
    instance = Item.objects.filter(name__icontains=name,company_id=company_id)[offset:offset + limit]
    serializer = AdjustmentSerializer(instance, many=True)
    
    response['results'] = AdjustmentSerializer(instance, many=True).data
    return Response(response)


# Get item details by item type 
@api_view(['GET'])

def getAdjustmentDetailsBystatus(request, track_inventory):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count":Item.objects.count()}
    
    instance = Item.objects.filter(track_inventory__icontains=track_inventory)[offset:offset + limit]
    serializer = AdjustmentSerializer(instance, many=True)
    
    response['results'] = AdjustmentSerializer(instance, many=True).data
    return Response(response)


@api_view(['GET'])

def getAdjustmentDetailsByReference(request, company_id,reference,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])

    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Adjustment.objects.filter(ref_no__icontains=reference,company_id=company_id,branch_id=branch_id).count()}

    instance = Adjustment.objects.filter(ref_no__icontains=reference,company_id=company_id,branch_id=branch_id)[offset:offset + limit]
    serializer = AdjustmentSerializer(instance, many=True)

    response['results'] = serializer.data

    return Response(response)


@api_view(['GET'])

def getAdjustmentDetailsByType(request, company_id,typ,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])

    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Adjustment.objects.filter(adj_type__icontains=typ,company_id=company_id,branch_id=branch_id).count()}

    instance = Adjustment.objects.filter(adj_type__icontains=typ,company_id=company_id,branch_id=branch_id)[offset:offset + limit]
    serializer = AdjustmentSerializer(instance, many=True)

    response['results'] = serializer.data

    return Response(response)

