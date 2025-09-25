from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from item.models.stock_transfer_model import *
from item.serializers.stock_transfer_serializer import *
from item.models.item_model import Item
from item.models.stock_model import *
import traceback
from django.db.models import Q

class StockTransferView(APIView):

    def get(self,request,pk=None,comp_id=None,branch_id=None):
        if pk:
            obj = StockTransfer.objects.get(st_id=pk)
            serializer = StockTransferSerializer(obj)
            return Response(serializer.data,status=200)
        limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
        offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

        # Build the response links for pagination
        url = str(request.build_absolute_uri()).split("?")[0]
        print(request.user)
        objs = StockTransfer.objects.filter(company_id=comp_id)
        response = {
            'next': url + f"?limit={limit}&offset={offset + limit}",
            'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
            "count": objs.count()
        }

        # Get the company object by comp_id and apply pagination
        objs = objs[offset:offset + limit]

        # Serialize the items and return the paginated response
        response['results'] = StockTransferGetSerializer(objs, many=True).data
        return Response(response,status=200)


    def post(self,request):
        with transaction.atomic():
            try:
                data = request.data
                transactions = data['stock_transactions']
                print(data)
                serializer = StockPostTransferSerializer(data=data)
                if serializer.is_valid():
                    st = serializer.save()

                else:
                    print(serializer.errors)
                    return Response(status=400)
                for trans in transactions:
                    p_branch = Branch.objects.get(branch_id=trans['primary_branch'])
                    s_branch = Branch.objects.get(branch_id=trans['secondary_branch'])
                    item = Item.objects.get(item_id=trans['item_id'])

                    mfg_date = trans['mfg_date']
                    expire_date = trans['expire_date']
                    batches = trans['batches']

                    if not batches:
                        batches = [None]
                        mfg_date = None
                        expire_date = None

                    quantity = float(trans['quantity'])

                    try:
                        stock_quantity = Batch.objects.get(Q(branch_id=trans['primary_branch'],
                                                             expire_date=expire_date,
                                                             mfg_date=mfg_date,
                                                           batch_no=batches[0],
                                                            item_id=trans['item_id'])).stock_quantity
                    except Exception as e:
                        print(e)
                        raise Exception(f"Stock Not available for {item.name}")
                    stock_rate_p = 0
                    if float(stock_quantity) >= float(quantity):

                        stt = StockTransferTransaction.objects.create(
                            stock_transfer=st,
                            primary_branch=p_branch,
                            item_id=item,
                            sec_item_id=item,
                            secondary_branch=s_branch,
                            quantity=quantity,
                            batches=batches,
                            mfg_date=mfg_date,
                            expire_date=expire_date,
                            sec_batches=batches,
                            sec_mfg_date=mfg_date,
                            sec_expire_date=expire_date
                        )
                        Stock.objects.create(
                            item_id=item.item_id,
                            item_name=item.name,
                            branch_id=p_branch,
                            rate=0,
                            amount=0,
                            date=data['trans_date'],
                            company_id=st.company_id,
                            ref_tblname='Stock Transfer',
                            ref_id=st.st_id,
                            stock_out=quantity,
                            quantity=quantity,
                            expire_date=expire_date,
                            mfg_date=mfg_date,
                            batch_no=batches[0],
                            module='Transfer',
                            formname='Stock Transfer',
                            stage='Add Stages'
                        )
                        Stock.objects.create(
                            item_id=item.item_id,
                            item_name=item.name,
                            branch_id=s_branch,
                            date=data['trans_date'],
                            rate=0,
                            amount=0,
                            company_id=st.company_id,
                            ref_tblname='Stock Transfer',
                            ref_id=st.st_id,
                            stock_in=quantity,
                            quantity=quantity,
                            expire_date=expire_date,
                            mfg_date=mfg_date,
                            batch_no=batches[0],
                            module='Transfer',
                            formname='Stock Transfer',
                            stage='Add Stages'
                        )



                    else:
                        raise Exception("Stock Not Available")

                return Response(status=200)
            except Exception as e:
                traceback.print_exc()
                transaction.set_rollback(True)
                return Response({"message": str(e)}, status=400)
