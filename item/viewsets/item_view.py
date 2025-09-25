

from rest_framework import viewsets, generics

from item.models.item_model import Item,ItemGroup,ItemView
from item.serializers.item_serializers import (ShortItemAllSerializer,
                                               ItemSearchSerializer,ItemSerializer,ItemSerializer_v1,ItemGroupSerializer)
from transaction .models import MasterTransaction
from coa .models import COA
from company.models import Company,Branch
from company.serializers import CompanySerializer ,ShortItemSerializer
from item.models.stock_model import Stock,WareHouse

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from item.models.stock_model import ItemAvgTransaction
from item.serializers.stock_serializers import ItemAvgTransactionSerializer
from django.db import transaction
from autocount.constant import convert_to_datetime_with_current_time
from autocount.constant import check_access
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# creating the item to added item table values




def get_financial_year_start(financial_year):
    # Split the input financial year to get the start year
    start_year = financial_year.split("-")[0]

    # Format the start date as "YYYY-04-01"
    start_date = f"{start_year}-04-01"

    return start_date

class ItemGroupView(APIView):

    def handle_post(self,data):

        serializer = ItemGroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(serializer.errors,status=400)

    def post(self,request):
        data = request.data
        return self.handle_post(data)


    def put(self,request,pk):
        data = request.data

        return self.handle_update(data,pk)

    def handle_update(self,data,pk):
        print(data)
        if pk:
            obj = ItemGroup.objects.get(item_grp_id=pk)
            serializer = ItemGroupSerializer(obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response(serializer.errors, status=400)
        return Response(status=400)

class itemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @transaction.atomic
    def handle_post(self,item_data):
        print("item_data", item_data)

        comp_id = Company.objects.get(company_id=item_data["company_id"])
        branch_id = Branch.objects.get(branch_id=item_data["branch_id"])
        serializer = ItemSerializer_v1(data=item_data)
        if serializer.is_valid():
            it = serializer.save()
            it.date = get_financial_year_start(comp_id.financial_year)
            it.save()
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        item = Item.objects.get(item_id=data['item_id'])
        batches = item_data['batches']

        for each in batches:
            if float(each['opening_stock'])> 0:
                if each.get('opening_stock_amount',None):
                    total = each['opening_stock_amount']
                else:
                    total = float(each['opening_stock']) * float(each['opening_stock_rate'])

                flow_type = 'INWARD' if total > 0 else 'OUTWARD'
                godown_id = each['godown_id']
                if godown_id:
                    godown_id = WareHouse.objects.get(wh_id=godown_id)
                Stock.objects.create(
                    item_id=item.item_id,
                    item_name=item.name,
                    branch_id=item.branch_id,
                    rate=each['opening_stock_rate'],
                    amount=total,
                    company_id=comp_id,
                    ref_tblname='Item',
                    date=item.date,
                    module_date=item.created_date,
                    ref_id=item.item_id,
                    stock_in=each['opening_stock'],
                    quantity=each['opening_stock'],
                    batch_no=each['batch_no'],
                    flow_type=flow_type,
                    godown_id=godown_id,
                    godown_name=each['godown_name'],
                    expire_date=each['expire_date'],
                    mfg_date=each['mfg_date'],
                    module='Inventory',
                    formname='Opening Stock',
                    stage='Add Stages')
                TO_COA = COA.get_opening_account(comp_id)
                FROM_COA = COA.objects.get(company_id=comp_id, account_name='Opening Balance Adjustment',
                                           isdefault=True, account_subhead='Other Current Liabilities')
                MasterTransaction.objects.create(
                        L1detail_id=data['item_id'],
                        L1detailstbl_name='Item',
                        main_module='Item',
                        module='Item',
                        sub_module='Item',
                        transc_deatils='Item',
                        banking_module_type='Item',
                        journal_module_type='Item',
                        trans_date=item_data['created_date'],
                        trans_status='Manually Added',
                        debit=total,
                        to_account=TO_COA.coa_id,
                        to_acc_type=TO_COA.account_type,
                        to_acc_head=TO_COA.account_head,
                        to_acc_subhead=TO_COA.account_subhead,
                        to_acc_name=TO_COA.account_name,
                        credit=total,
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        branch_id=branch_id,
                        company_id=comp_id)


        return Response(data,status=201)


    def create(self, request, *args, **kwargs):
        item_data = request.data
        return self.handle_post(item_data)



class ItemUpdateView(APIView):
    @transaction.atomic
    def handle_update(self,data,pk):
        item = Item.objects.select_for_update().get(item_id=pk)
        serialzier = ItemSerializer_v1(item, data=data)
        comp_id = Company.objects.get(company_id=data["company_id"])
        if serialzier.is_valid():
            it = serialzier.save()
            it.date = get_financial_year_start(comp_id.financial_year)
            it.save()
        else:
            print(serialzier.errors)
            return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)



        branch_id = Branch.objects.get(branch_id=data["branch_id"])
        MasterTransaction.objects.select_for_update().filter(L1detail_id=pk).delete()
        batches = data['batches']
        item = Item.objects.select_for_update().get(item_id=pk)
        queryset = Stock.objects.select_for_update().filter(ref_id=pk)
        batch_list = {(item.batch_no, item.expire_date, item.mfg_date,float(item.quantity),item.godown_id_id):item for item in queryset}
        batch_list1 = []
        if item.track_inventory:
            for each in batches:
                temp = (each['batch_no'],each['expire_date'], each['mfg_date'],float(each['opening_stock']),each['godown_id'])
                batch_list1.append(temp)
                if float(each['opening_stock']) > 0:
                    if each.get('opening_stock_amount', None):
                        total = each['opening_stock_amount']
                    else:
                        total = float(each['opening_stock']) * float(each['opening_stock_rate'])
                    flow_type = 'INWARD' if total > 0 else 'OUTWARD'
                    godown_id = each['godown_id']

                    print(temp,batch_list)
                    if temp in batch_list:
                        print("updating stock")
                        obj = Stock.objects.select_for_update().get(
                            ref_id=item.item_id,
                            batch_no=each['batch_no'],
                            expire_date=each['expire_date'],
                            mfg_date=each['mfg_date'],
                            godown_id_id=each['godown_id'],
                            quantity=round(float(each['opening_stock']),2)
                        )
                        obj.godown_name = each['godown_name']
                        obj.rate = each['opening_stock_rate']
                        obj.stock_in = each['opening_stock']
                        obj.date=item.date
                        obj.module_date=item.created_date
                        obj.save()
                    else:
                        print("creating stock")
                        Stock.objects.create(
                            item_id=item.item_id,
                            item_name=item.name,
                            branch_id=item.branch_id,
                            rate=each['opening_stock_rate'],
                            amount=total,
                            company_id=comp_id,
                            ref_tblname='Item',
                            date=item.date,
                            module_date=item.created_date,
                            ref_id=item.item_id,
                            stock_in=each['opening_stock'],
                            quantity=each['opening_stock'],
                            batch_no=each['batch_no'],
                            flow_type=flow_type,
                            godown_id_id=godown_id,
                            godown_name=each['godown_name'],
                            expire_date=each['expire_date'],
                            mfg_date=each['mfg_date'],
                            module='Inventory',
                            formname='Opening Stock',
                            stage='Add Stages')

                    TO_COA = COA.get_opening_account(comp_id)
                    FROM_COA = COA.objects.get(company_id=comp_id,account_name='Opening Balance Adjustment',
                                               isdefault=True,account_subhead='Other Current Liabilities')
                    MasterTransaction.objects.create(
                        L1detail_id=item.item_id,
                        L1detailstbl_name='Item',
                        main_module='Item',
                        module='Item',
                        sub_module='Item',
                        transc_deatils='Item',
                        banking_module_type='Item',
                        journal_module_type='Item',
                        trans_date=item.date,
                        trans_status='Manually Added',
                        debit=total,
                        to_account=TO_COA.coa_id,
                        to_acc_type=TO_COA.account_type,
                        to_acc_head=TO_COA.account_head,
                        to_acc_subhead=TO_COA.account_subhead,
                        to_acc_name=TO_COA.account_name,
                        credit=total,
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        branch_id=branch_id,
                        company_id=comp_id)
        for key, child in batch_list.items():
            print(key in batch_list)
            if key not in batch_list1:
                child.delete()
        return Response(status=200)
    def put(self, request, pk=None):
        data = request.data
        return self.handle_update(data,pk)



#End Item
class itemList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    
    @api_view(['GET']) #@api_view Allow to define function that match http methods
    def itemCreation(self, request):
        item = Item.objects.all()    
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)
from itertools import groupby
from operator import itemgetter

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getitemtransaction(request, item_id):
    objs = ItemAvgTransaction.objects.filter(item_id=item_id)
    data = ItemAvgTransactionSerializer(objs,many=True).data
    grouped_data = []
    count =0
    result = {}

    for each in data:
        temp = (each['batch_no'] , each['expire_date'] ,each['mfg_date'],each['godown_name'])
        if temp in result:
            result[temp].append(each)
        else:
            result[temp] = [each]
    for key,value in result.items():
        if key[0]:
            grouped_data.append({'batch_no':f"{key[0]} => {key[3]}",'items':value})
        else:
            grouped_data.append({'batch_no':f"No Batch => {key[3]}",'items': value})
    # grouped_data = [{f'{each["batch_no"] => {each["godown_name"]}':result[each]} for each in result]
    # for batch_no, items in groupby(data, key=itemgetter('batch_no','expire_date','mfg_date','godown_name')):
    #     print(list(items))
    #     print("***************")
    #     if not batch_no[0]:
    #         batch_no = f"No Batch  {batch_no[3]}"
    #     else:
    #         batch_no =  f"{batch_no[0]} {batch_no[3]}"
    #     print("append")
    #     grouped_data.append({
    #         'batch_no': batch_no,
    #         'items': list(items)
    #     })
    print(grouped_data)
    return Response(grouped_data ,status=200)

#getitemshortbycompanyid
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getitemshortpaginationbycompanyid(request, comp_id,branch_id):

    if not check_access(request.user,'item'):
        return Response({"message":"You dont have access to this service"},status=400)

    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    print(request.user)
    # companies = Company.objects.filter(user=request.user).values_list('company_id', flat=True)
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": ItemView.objects.filter(company_id=comp_id).count()
    }

    # Get the company object by comp_id and apply pagination
    try:
        items = ItemView.objects.filter(company_id=comp_id)[offset:offset + limit]
        print(items)
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = ShortItemSerializer(items, many=True).data
    return Response(response)

@api_view(['GET'])

@renderer_classes([JSONRenderer])
def getitemshortbycompanyid(request, comp_id):

    
    try:
        # companies = Company.objects.filter(user=request.user).values_list('company_id', flat=True)
        # print(companies)
        items = Item.objects.filter(company_id=comp_id)
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)



@api_view(['GET'])


def ShortItemAll(request,comp_id,branch_id):
    # companies = Company.objects.filter(user=request.user).values_list('company_id', flat=True)
    item = Item.objects.filter(company_id=comp_id,branch_id=branch_id)
    serializer = ShortItemAllSerializer(item, many=True,branch_id=branch_id)
    return Response(serializer.data)

@api_view(['GET'])
def ShortAsyncItemAll(request,comp_id,branch_id,name):
    # companies = Company.objects.filter(user=request.user).values_list('company_id', flat=True)
    item = Item.objects.filter(company_id=comp_id,name__icontains=name)[:5]
    if item:
        serializer = ShortItemAllSerializer(item,many=True,branch_id=branch_id)
        print(serializer.data)
        return Response(serializer.data)
    return Response([],status=200)

@api_view(['GET'])
def ShortAsyncFullItemAll(request,comp_id,branch_id,name):
    # companies = Company.objects.filter(user=request.user).values_list('company_id', flat=True)
    item = Item.objects.filter(company_id=comp_id,
                               full_inventory=True,
                               branch_id=branch_id,name__icontains=name)[:5]
    if item:
        serializer = ShortItemAllSerializer(item,many=True,branch_id=branch_id)
        print(serializer.data)
        return Response(serializer.data)
    return Response([],status=200)




#getshortDetails
@api_view(['GET'])


def ShortItemDetails(request): 
    item = Item.objects.all()   
    serializer = ShortItemSerializer(item, many=True)
    return Response(serializer.data)

#get item short by company id
@api_view(['GET'])


def itemshortbycompanyid(request, pk):
    customer = Company.objects.get(company_id=pk)
    serializer = CompanySerializer(customer, many=False)
    return Response(serializer.data)

@api_view(['GET'])


def itemDetail(request, pk):
    item = Item.objects.get(item_id=pk)
    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data)

@api_view(['POST'])


def itemUpdate(request, pk):
    item = Item.objects.get(item_id=pk)
    serializer = ItemSerializer(instance=item, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



# Item Update Section 
#User can Upadte the item to do But Cuurently no any feature are implemented in item updation
class ItemUpdateViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = Item

    
    def update(self, request, pk, *args, **kwargs):
            
        item_data=request.data
        item = Item.objects.get(item_id=pk)
        #get the item object with respective id
        total=float(item_data['opening_stock']) * float(item_data['opening_stock_rate'])
        print('@@@@@@',type(total))
        comp_id = Company.objects.get(company_id=item_data["company_id"])
        inv_id = item_data.get("inventory_account")
          
        if inv_id is not None:
            inv_id =COA.objects.get(coa_id=inv_id)
            inventory_account = inv_id.coa_id
        else:
            inv_id=None
            inventory_account = None
        
        pur_id = item_data.get("purchase_account")
            
        if pur_id is not None:
            pur_id =COA.objects.get(coa_id=pur_id)
            purchase_account = pur_id.coa_id
        else:
            pur_id=None
            purchase_account = None
        #user Selected sales account featching in item table   
        sal_id = item_data.get("sales_account")
            
        if sal_id is not None:
            sal_id =COA.objects.get(coa_id=sal_id)
            sales_account = sal_id.coa_id
        else:
            sal_id=None
            sales_account = None
            
            
            
        serializer = ItemSerializer(item, data=item_data)

        if serializer.is_valid():
            item_id=serializer.save()
        
        
                   
        else:
             return Response(serializer.errors, status=400)
        
        serializer = ItemSerializer(item_id)    
        return Response(serializer.data) 
    
import  time
# Get item details by item name 
@api_view(['GET'])
def getItemDetailsByItemName(request,company_id, branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    name = request.GET['name']
    objs = ItemView.objects.filter(name__icontains=name,company_id=company_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count":objs.count()}
    
    instance = objs[offset:offset + limit]

    start = time.time()
    response['results'] = ShortItemSerializer(instance, many=True).data
    end = time.time()
    print(f"{end-start} query time")
    return Response(response)





# Get item details by item type 
@api_view(['GET'])


def getItemDetailsByItemCatagory(request, company_id,branch_id):

    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    item_category = request.GET['category']
    objs = Item.objects.filter(item_category__icontains=item_category,company_id=company_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count":objs.count()}
    
    instance = objs[offset:offset + limit]

    
    response['results'] = ShortItemSerializer(instance, many=True).data
    return Response(response)
