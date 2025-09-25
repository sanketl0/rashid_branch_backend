import imp
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from item.models.item_model import Item
from item.models.stock_model import Stock,Batch,WareHouse
from item.serializers.stock_serializers import StockSerializer,AdjStockSerializer,\
    BatchSerializer,GodownSerializer,GodownGetSerializer
from purchase.models.Bill_model import Bill
from purchase.models.Debitnote_model import DebitNote
from item.models.stock_model import getstock_on_hand

from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.views import APIView
from django.db import transaction

class GodownView(APIView):

    def get(self,request,pk=None,comp_id=None,branch_id=None,name=None):
        if pk:
            instance = WareHouse.objects.get(wh_id=pk)
            serializer = GodownSerializer(instance)
            return Response(serializer.data,status=200)
        if name and branch_id:
            instance = WareHouse.objects.filter(name__icontains=name,branch_id=branch_id)
            serializer = GodownGetSerializer(instance,many=True)
            return Response(serializer.data, status=200)
        objs = WareHouse.objects.filter(company_id=comp_id,branch_id=branch_id)
        serializer = GodownSerializer(objs,many=True)
        return Response(serializer.data, status=200)

    @transaction.atomic
    def post(self,request):
        data = request.data
        serializer = GodownSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)

    @transaction.atomic
    def put(self,request,pk):
        instance = WareHouse.objects.get(wh_id=pk)
        data = request.data
        serializer = GodownSerializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)



@api_view(['GET'])
def getFIFOstock_details(request,item_id):
    items= Stock.objects.filter(item_id=item_id)
    # use exclude for not having item whose stock i 0 
    stk_out=Stock.objects.filter(item_id=item_id).exclude(stock_out=0).order_by('created_date')
    stk_in=Stock.objects.filter(item_id=item_id).exclude(stock_in=0).order_by('created_date')
    print('Stock in value',stk_in)
    st_sum = 0
    # Stock out Sum
    for st_out_item in stk_out:
        st_sum = st_sum + st_out_item.stock_out
    print("Sum Of Stockout", st_sum)
    st_in_sum = 0
    in_qty_sum = 0
    #Stock in sum and claculation 
    for st_in_item in stk_in:
        
        print("Iteration: ", st_in_item.stock_in, st_in_item.rate, st_in_item.amount, st_in_item.created_date)
        st_in = st_sum-st_in_item.stock_in
        print(f"{st_in} = {st_sum}-{st_in_item.stock_in}")
        if st_in > 0:
            print("Ignore this item")
            st_sum = st_in

        else:
            print("Consider this item")
            st_in_sum = st_in_sum+st_in_item.rate*st_in*-1
            in_qty_sum = in_qty_sum + st_in *-1
            st_sum = 0
            date=st_in_item.date,
            in_ref=st_in_item.ref_id
            formname=st_in_item.formname
            print('QQQQ',formname)
            if formname == 'Bill':
                get_in_ref=Bill.objects.filter(bill_id=in_ref)
                print('Bill is here',type(get_in_ref))
            else:
                get_in_ref=DebitNote.objects.filter(dn_id=in_ref)
                print('Debit Note is Herer')
            for get_in_refs in get_in_ref:
                get_in_refs=get_in_refs

           
        print("-----------------")

    print(st_in_sum)
    print('last value',stk_in.last())
    #print('last stock rate', stk_in.last().rate)
    print(f"remining quantity: {in_qty_sum}")
    inserializer = StockSerializer(stk_in, many=True)
    in_data=inserializer.data
    outserializer = StockSerializer(stk_out, many=True)
    out_data=outserializer.data
    adjustment_serializer=AdjStockSerializer(items,many=True)
    
    stk_out
    all_response = {
            'stock_in_data': in_data,
            'stock_out_data': out_data,
            'total':st_in_sum,
            # 'last value':stk_in.last(),
            'last stock rate': stk_in.last().rate,
            'remining quantity': {in_qty_sum},
            'in_date':date,
            'in_ref':get_in_refs.convt_type,
            'adjustment_data':adjustment_serializer.data
            # 'quantity':st_in_item.quantity,
    
            
        }
    return Response(all_response)
#endregion
#End FIFO Section

# Inventory valution LIFO Method
#region
#stk_out is the get the sales side the data  filter item wise
#stk_in is the get the purchase side the data filter item wise
#LIFO methos is the Purchase the last item and remaing the last quantity is multiplication is dec order

@api_view(['GET'])


def getLIFOstock_details(request,item_id):
    items= Stock.objects.filter(item_id=item_id)
    stk_out=Stock.objects.filter(item_id=item_id,).exclude(stock_out=0).order_by('-created_date')
    stk_in=Stock.objects.filter(item_id=item_id,).exclude(stock_in=0).order_by('-created_date')
    print('Stock in value',stk_in)
    st_sum = 0
    # Stock out Sum
    for st_out_item in stk_out:
        st_sum = st_sum + st_out_item.stock_out
    print("Sum Of Stockout", st_sum)
    st_in_sum = 0
    in_qty_sum = 0
    #Stock in sum and claculation 
    for st_in_item in stk_in:
        
        print("Iteration: ", st_in_item.stock_in, st_in_item.rate, st_in_item.amount, st_in_item.created_date)
        st_in = st_sum-st_in_item.stock_in
        print(f"{st_in} = {st_sum}-{st_in_item.stock_in}")
        if st_in > 0:
            print("Ignore this item")
            st_sum = st_in

        else:
            print("Consider this item")
            st_in_sum = st_in_sum+st_in_item.rate*st_in*-1
            in_qty_sum = in_qty_sum + st_in *-1
            st_sum = 0
        print("-----------------")

    print(st_in_sum)
    print('last value',stk_in.last())
    print('last stock rate', stk_in.last().rate)
    print(f"remining quantity: {in_qty_sum}")
    inserializer = StockSerializer(stk_in, many=True)
    in_data=inserializer.data
    outserializer = StockSerializer(stk_out, many=True)
    out_data=outserializer.data
    all_response = {
            'stock_in_data': in_data,
            'stock_out_data': out_data,
            'total':st_in_sum,
            # 'last value':stk_in.last(),
            'last stock rate': stk_in.last().rate,
            'remining quantity': {in_qty_sum}
    
            
        }
    return Response(all_response)
#endregion
#END LIFO Section
 
    
#WAC Cost Section
#region 
@api_view(['GET'])


def getWACstock_details(request,item_id):

    stk_out=Stock.objects.filter(item_id=item_id).exclude(stock_out=0).order_by('created_date')
    stk_in=Stock.objects.filter(item_id=item_id).exclude(stock_in=0).order_by('created_date')
    print('Stock in value',stk_in)
    st_sum = 0
    for st_out_item in stk_out:
        st_sum = st_sum + st_out_item.stock_out
    print("Sum Of Stockout", st_sum)
    st_in_sum = 0
    in_qty_sum = 0
    sum_stock_in=0
    sum_stock_amount=0
    for st_in_item in stk_in:
        
        print("Iteration: ", st_in_item.stock_in, st_in_item.rate, st_in_item.amount, st_in_item.created_date)
        st_in = st_sum-st_in_item.stock_in
        print(f"{st_in} = {st_sum}-{st_in_item.stock_in}")
        if st_in > 0:
            print("Ignore this item")
            st_sum = st_in

        else:
            print("Consider this item")
            st_in_sum = st_in_sum+st_in_item.rate*st_in*-1
            in_qty_sum = in_qty_sum + st_in *-1
            st_sum = 0
            print("-----------------")
    for sum_stockin_item in stk_in:
        sum_stock_in = sum_stock_in + sum_stockin_item.stock_in
        sum_stock_amount = sum_stock_amount + sum_stockin_item.amount
   
        
        
        
    wac_rate=sum_stock_amount/sum_stock_in
    total_wac=wac_rate*in_qty_sum
   
    print("stock in sum",sum_stock_in)
    print("sum of stock in amount",sum_stock_amount)
    print("Sum of Stock in / remaing quantity",wac_rate)
    print(f"remaining quantity: {in_qty_sum}")
    print("remaining qty * wac rate",total_wac)
    inserializer = StockSerializer(stk_in, many=True)
    in_data=inserializer.data
    outserializer = StockSerializer(stk_out, many=True)
    out_data=outserializer.data
    inserializer = StockSerializer(stk_in, many=True)
    in_data=inserializer.data
    outserializer = StockSerializer(stk_out, many=True)
    out_data=outserializer.data
    all_response = {
            'stock_in_data': in_data,
            'stock_out_data': out_data,
            'stock in sum':sum_stock_in,
            'sum of stock in amount':sum_stock_amount,
            'Sum of Stock in / remaing quantity':wac_rate,
            'remaining quantity': {in_qty_sum},
            'remaining qty * wac rate':total_wac
            
        }
    return Response(all_response)
#endregion
#End WAC






#getitemshortbycompanyid
#All the Stock Item Get In Company Id Wise
@api_view(['GET'])

def getstockitemamountvalue(request,item_id,branch_id):
    try:
        stock_item = Stock.objects.filter(item_id=item_id,
                                              branch_id=branch_id,
                                              ).latest('created_date')
    except Stock.DoesNotExist:
        stock_item=None
        #return the This data Becasue Ui Side Calcultation time Some Error Occurs
        return Response([])
    # st_in_hand=getstock_on_hand(item_id)

    try:
        no_batch_stock = Batch.objects.filter(item_id=item_id,batch_no__isnull=True,
                                              mfg_date__isnull=True,
                                              branch_id=branch_id,
                                              expire_date__isnull=True)[0].stock_quantity
    except Exception as e:
        print(e)
        no_batch_stock = 0
    try:
        st_in_hand = Batch.objects.filter(item_id=item_id,
                                              branch_id=branch_id,
                                              )[0].stock_quantity
    except Exception as e:
        print(e)
        st_in_hand = 0
    response_list=[]
    response_dict = {"Item_Name":stock_item.item_name,"Stock_Id":stock_item.st_id,
                     "no_batch_stock":no_batch_stock,
                     "Item_id":stock_item.item_id,"Amount":stock_item.amount,"Stock_on_hand":st_in_hand}
    print(response_dict)
    response_list.append(response_dict)
    return Response(response_list)

#Get The Stock Item By Item Id wise 
#getreportshortbyitemid
@api_view(['GET'])


def getitemstockreport(request,from_date,to_date,comp_id,branch_id):
    item= Item.objects.filter(created_date__date__range=(from_date, to_date),
                              branch_id=branch_id,
                              company_id=comp_id)

    response_list = []
    for items in item:
        item_track=items.track_inventory
        print('items is tracked',)
        if item_track is False:
            continue
        
        item_id=items.item_id
        print('item is here',item_id)
        try:
            stock_item = Stock.objects.filter(item_id=item_id).latest('created_date')
        except Stock.DoesNotExist:
            continue
        

        stk_out=Stock.objects.filter(item_id=item_id,).exclude(stock_out=0).order_by('created_date')
        stk_in=Stock.objects.filter(item_id=item_id,).exclude(stock_in=0).order_by('created_date')
        
        st_out_sum = 0
        for st_out_item in stk_out:
            st_out_sum = st_out_sum + st_out_item.stock_out
        st_in_sum = 0
        for st_in_item in stk_in:
            st_in_sum = st_in_sum + st_in_item.stock_in
            
        st_in_hand=getstock_on_hand(item_id)
        
        serializer = StockSerializer(stock_item)
        n_data=serializer.data
        
        response_dict = {"rate":stock_item.rate,"Amount":stock_item.amount,"Item_id":stock_item.item_id,"Item_Name":stock_item.item_name,"Stock_In":st_in_sum,"Stock_Out":st_out_sum,"Stock_in_Hand":st_in_hand}
        response_list.append(response_dict)
    print(response_list)
    return Response({"data":response_list})

#getitemshortbycompanyid
#All the Stock Item Get In Company Id Wise
@api_view(['GET'])


def getstockiteminventoyvalution(request,item_id,):
    try:
        stock_items = Stock.objects.filter(item_id=item_id)
    except Stock.DoesNotExist:
        stock_item=None
        #return the This data Becasue Ui Side Calcultation time Some Error Occurs
        return Response({'stock_on_hand':0})
    response_list=[]
    for stock_item in stock_items:
        pass
      
        response_dict = {"Item_name":stock_item.item_name,"Date":stock_item.date,"Transaction_Details":stock_item.formname,"Quantity":stock_item.quantity,"Unit_Cost":stock_item.rate,"Stock_on_hand":stock_item.stock_on_hand,"Amount":stock_item.amount}
        response_list.append(response_dict)
    return Response(response_list)


@api_view(['GET'])
def getBatchStockView(request, pk,branch_id):

    stock_items = Batch.objects.filter(item_id=pk,branch_id=branch_id)

    serializer = BatchSerializer(stock_items, many=True)
    print(serializer.data)
    return Response(serializer.data, status=200)
