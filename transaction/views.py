
import json 
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from .models import MasterTransaction,Charges,ChargeTransaction
from .serializers import MasterTransactionSerializer,ChargesSerializer,MasterTransactionBankSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.db.models import Q
#get all transaction for banking in Master Transaction
#Group By All Transaction Fields
@api_view(['GET'])


def getChargesBycompany(request,company_id,branch_id):
    chgs = Charges.objects.filter(company_id=company_id,branch_id=branch_id)
    serializer = ChargesSerializer(chgs,many=True)
    return Response(serializer.data,status=200)

@api_view(['POST'])


def postChargesBycompany(request):
    data = request.data
    print(data)
    serializer = ChargesSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    print(serializer.data)
    return Response(serializer.data,status=201)

@api_view(['GET'])
def getJRNLBankTransbyNameCOAID(request,from_to_id,name):

        limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
        offset = int(request.GET.get('offset', 0))
        transactions = MasterTransaction.objects.filter(Q(from_account=from_to_id,transc_deatils__icontains=name) |
                                                        Q(to_account=from_to_id,transc_deatils__icontains=name))
        url = str(request.build_absolute_uri()).split("?")[0]
        response = {
            'next': url + f"?limit={limit}&offset={offset + limit}",
            'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
            "count": transactions.count()
        }
        objs = transactions[offset:offset + limit]
        serializer = MasterTransactionBankSerializer(objs, many=True, account=from_to_id)
        response['results'] = serializer.data
        return Response(response)

@api_view(['GET'])
def getJRNLBankTransbyCOAID(request,from_to_id):

        limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
        offset = int(request.GET.get('offset', 0))
        transactions = MasterTransaction.objects.filter(Q(from_account=from_to_id) | Q(to_account=from_to_id))
        url = str(request.build_absolute_uri()).split("?")[0]
        response = {
            'next': url + f"?limit={limit}&offset={offset + limit}",
            'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
            "count": transactions.count()
        }
        objs = transactions[offset:offset + limit]
        serializer = MasterTransactionBankSerializer(objs, many=True, account=from_to_id)
        response['results'] = serializer.data
        return Response(response)



        from_mast = MasterTransaction.objects.filter(from_account=from_to_id)

        print('@@@@@@',from_mast)
        to_mast = MasterTransaction.objects.filter(to_account=from_to_id)
        all_transactions = from_mast | to_mast
        if  len(from_mast) > 0 :      
            from_df = pd.DataFrame(from_mast.values('L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                                'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit','transc_deatils','trans_date','trans_status'))
            print(from_df)
            from_acc = from_df.groupby(['L1detail_id','from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name','transc_deatils','trans_date','trans_status',]).agg(
            {'credit': 'sum'}).reset_index()
            from_acc = from_acc.rename(columns={'L1detail_id':'L1detail_id',
                                    'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name','transc_deatils':'transc_deatils','trans_date':'trans_date','trans_status':'trans_status'}, inplace=False)
        
        else:
            from_acc = None

        if len(to_mast) > 0:
            to_df = pd.DataFrame(to_mast.values('L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                                'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit','transc_deatils','trans_date','trans_status'))
            print(to_df)
            to_acc = to_df.groupby(['L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name','transc_deatils','trans_date','trans_status',]).agg(
                { 'debit': 'sum'}).reset_index()
            to_acc = to_acc.rename(columns={'L1detail_id':'L1detail_id',
                                    'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name','transc_deatils':'transc_deatils','trans_date':'trans_date','trans_status':'trans_status'}, inplace=False)
        else:
            to_acc = None
        if from_acc is not None and to_acc is not None:
            df_accounts = pd.concat([from_acc, to_acc])
        elif from_acc is not None:
            df_accounts = from_acc
        elif to_acc is not None:
            df_accounts = to_acc
        else:
            return Response("Data not found", status=200)
        from_response = json.loads(df_accounts.to_json(orient='records',date_format='iso'))
        #chnages the responce beacuse ui date sorting issue 19 jan 2023
        change_from_responce=[]
        for i in from_response:
            a=i['trans_date']
            i['trans_date']=a[:10]
            print(a[:10])
            change_from_responce.append(i)
        
       
        all_response = {
           
                'transaction': change_from_responce,
                # 'to_transaction':to_response,
            }
        return Response(all_response) 





n_data=None
@api_view(['GET'])


def getDNRJournalTransaction(self,dn_id):
    form_mast = MasterTransaction.objects.filter(L3detail_id=dn_id)
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