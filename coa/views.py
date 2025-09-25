
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from .models import COA, OpeningBalance, AccountHead,TransactionDetail,Tax
from .serializers import *

from django.http.response import Http404
from transaction .models import MasterTransaction
from transaction.serializers import MasterTransactionSerializer
import pandas as pd
import json

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db import transaction
from rest_framework.views import APIView
from report.models import AccountBalance
# this Class Used the Featching the all records in coa Table
from django.db.models import Q
from item.viewsets.item_view import get_financial_year_start


class TaxView(APIView):
    def get(self,request,tax_id=None,name=None,company_id=None):
        if name:
            objs = Tax.objects.filter(company_id=company_id,name__icontains=name)[:5]
            serializer = TaxSerializer(objs,many=True)
            return Response(serializer.data,status=200)
        if tax_id:
            obj = Tax.objects.get(tax_id=tax_id)
            serializer = TaxSerializer(obj)
            return Response(serializer.data, status=200)
        if company_id:
            limit = int(request.GET['limit'])
            offset = int(request.GET['offset'])
            url = str(request.build_absolute_uri()).split("?")[0]
            objs  = Tax.objects.filter(company_id=company_id)
            response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                        "count": objs.count()}
            instance = objs[offset:offset + limit]
            response['results'] = TaxSerializer(instance, many=True).data
            return Response(response,status=200)
        return Response(status=400)

    def post(self,request):
        data = request.data
        serializer = TaxSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(serializer.errors,status=400)

    def put(self,request,tax_id):
        obj = Tax.objects.get(tax_id=tax_id)
        serializer = TaxSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(serializer.errors,status=400)

class coaViewSet(viewsets.ModelViewSet):
    queryset = COA.objects.all()
    serializer_class = COASerializer

class CoaSubheadSearchView(APIView):
    def get(self,request,comp_id,acc_name=None,acc_type=None):
        if acc_name:
            objs =  COA.objects.filter(company_id_id=comp_id,
                                       system=False,
                                       isdefault=True,account_name__isnull=False,
                                       account_name__icontains=acc_name)
        if acc_type:
            objs = COA.objects.filter(company_id_id=comp_id, isdefault=True, account_name__isnull=False,
                                      account_type__icontains=acc_type)
        limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
        offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

        # Build the response links for pagination
        url = str(request.build_absolute_uri()).split("?")[0]
        response = {
            'next': url + f"?limit={limit}&offset={offset + limit}",
            'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
            "count": objs.count()
        }
        objs = objs[offset:offset + limit]
        serializer = COASerializerShortbyCompany(objs, many=True)
        response['results'] = serializer.data
        return Response(response)

class CoaWholeView(APIView):

    def get(self, request, comp_id):
        objs = COA.objects.filter(company_id_id=comp_id, isdefault=True, system=False,account_name__isnull=False)
        serializer = COASerializerShortbyCompany(objs, many=True)
        return Response(serializer.data)

class CoaAsyncAssetLiabView(APIView):
    def get(self,request,name,comp_id):
        if name:
            objs = AccountBalance.objects.filter(company_id=comp_id, isdefault=False,
                                                 account_type__in=['Assets','Liabilities'],
                                                 account_name__icontains=name)[:5]
            serializer = accountnameSerializer(objs, many=True)
            return Response(serializer.data)
class CoaAsyncWholeView(APIView):

    def get(self, request, comp_id,name,account_type=None,account_subhead=None,income=None):
        if account_type:
            objs = AccountBalance.objects.filter(company_id=comp_id, isdefault=False,

                                      account_type=account_type,
                                      account_name__icontains=name)[:5]

        elif account_subhead:
            if account_subhead == "Bank":
                objs = AccountBalance.objects.filter(Q(company_id=comp_id, isdefault=False,account_name__icontains=name) &
                                                     (Q(account_subhead=account_subhead) | Q(account_subhead='Cash'))
                                                     )[:5]
                print(objs)
            else:
                objs = AccountBalance.objects.filter(company_id=comp_id, isdefault=False,
                                          account_subhead=account_subhead,
                                          account_name__icontains=name)[:5]
        elif income:
            objs = AccountBalance.objects.filter(Q(company_id=comp_id, isdefault=False, account_name__icontains=name) &
                                                 (
                                                  Q(account_subhead="Other Operating Revenues") |
                                                  Q(account_subhead='Other Financial Services') |
                                                  Q(account_subhead="Other Income")
                                                  )
                                                 )[:5]

        else:
            objs = AccountBalance.objects.filter(company_id=comp_id, isdefault=False,
                                      account_name__icontains=name)[:5]
        print(objs)
        serializer = accountnameSerializer(objs, many=True)

        return Response(serializer.data)

class CoaSubheadView(APIView):


    def get(self,request,comp_id):
        objs = COA.objects.filter(company_id_id=comp_id,
                                  system=False,
                                  isdefault=True,account_name__isnull=False)
        limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
        offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

        # Build the response links for pagination
        url = str(request.build_absolute_uri()).split("?")[0]
        response = {
            'next': url + f"?limit={limit}&offset={offset + limit}",
            'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
            "count": objs.count()
        }
        objs = objs[offset:offset + limit]
        serializer = COASerializerShortbyCompany(objs,many=True)
        response['results'] = serializer.data
        return Response(response)
    @transaction.atomic
    def handle_post(self,data):

        serializer = COASerializer(data=data)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            return Response({"message": "Successfully Created Subhead"}, status=201)
        return Response({"message": "Not Valid"}, status=400)


    def post(self,request):
        data = request.data
        return self.handle_post(data)

    @transaction.atomic
    def handle_update(self,data,pk):

        coa = COA.objects.get(coa_id=pk)
        serializer = COASerializer(coa, data=data)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            return Response({"message": "Successfully Created Coa"}, status=201)
        return Response({"message": "Not Valid"}, status=400)

    def put(self,request,pk):
        data = request.data
        return self.handle_update(data,pk)
#this class is used multiples method is used but our used in only get method
class coaList(generics.ListAPIView):
    queryset = COA.objects.all()
    serializer_class = COASerializer

    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def coaCreation(self, request):
        try:
            coa = COA.objects.all()
            # print("SQL Query:", COA.query)
            serializer = COASerializer(coa, many=True)
            return Response(serializer.data)
        except COA.DoesNotExist:
            return Response(status=404)


# @api_view Allow to define function that match http methods
#Check the Account name is null or not
@api_view(['GET'])
@renderer_classes([JSONRenderer])

def getcoashortpaginationbycompanyid(request, comp_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": AccountBalance.objects.filter(company_id=comp_id,account_name__isnull=False,isdefault=False).count()
    }
    # Get the company object by comp_id and apply pagination
    try:

        coa = AccountBalance.objects.filter(company_id=comp_id, account_name__isnull=False,isdefault=False)[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company Does Not Exist")
    
     # Serialize the items and return the paginated response
    response['results'] =COASerializerShortbyCompany(coa, many=True).data
    print(response['results'])
    return Response(response)

# get coa by account name
#check the Account name  in coa table 

@api_view(['GET'])

def accountname(request):
    try:
        customer = COA.objects.all()
        serializer = accountnameSerializer(customer, many=True)
        return Response(serializer.data)
    except COA.DoesNotExist:
        return Response("COA Does Not Exist")
    except Exception as e:
        return Response(str(e), status=Http404)


# get coa by account name
@api_view(['GET'])

def accountnameshortbycompanyid(request, comp_id):
    try:

        coas = AccountBalance.objects.filter(company_id=comp_id,isdefault=True,account_name__isnull=False
                                             )
        serializer = accountnameSerializer(coas, many=True)
        return Response(serializer.data)
    except Company.DoesNotExist:
        return Response("Account Name Does Not Exist")
    except Exception as e:
        return Response(str(e), status=Http404)

@api_view(['GET'])

def accountnamesdefaulthortbycompanyid(request, comp_id):
    try:

        coas = AccountBalance.objects.filter(company_id=comp_id,isdefault=False,account_name__isnull=False
                                             )
        serializer = accountnameSerializer(coas, many=True)
        return Response(serializer.data)
    except Company.DoesNotExist:
        return Response("Account Name Does Not Exist")
    except Exception as e:
        return Response(str(e), status=Http404)

# get coa by company id
@api_view(['GET'])

def coabycompany(request, comp_id):
    coa = COA.objects.all()
    serializer = accountnameSerializer(coa, many=True)
    return Response(serializer.data)

#Get method and get the coa in coa_id through
@api_view(['GET'])

def coaDetail(request, pk):
    coa = COA.objects.get(coa_id=pk)
    serializer = COASerializer(coa, many=False)
    return Response(serializer.data)

#Post Method in Chart of with respective id
#this is update method in respective id 
@api_view(['POST'])

def coaUpdate(request, pk):
    coa = COA.objects.get(coa_id=pk)
    serializer = COASerializer(instance=coa, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# Account Head
#this code currently not working in futring is used to account heads are seapreted

#region
class accountheadViewSet(viewsets.ModelViewSet):
    queryset = AccountHead.objects.all()
    serializer_class = AccountHeadSerializer

class accountheadList(generics.ListAPIView):
    queryset = AccountHead.objects.all()
    serializer_class = AccountHeadSerializer

    @api_view(['GET'])
    def AccountHeadCreation(self, request):
        accounthead = AccountHead.objects.all()
        serializer = AccountHeadSerializer(accounthead, many=True)
        return Response(serializer.data)


@api_view(['GET'])

def AccountHeadDetail(request, pk):
    accounthead = AccountHead.objects.get(ah_id=pk)
    serializer = AccountHeadSerializer(accounthead, many=False)
    return Response(serializer.data)


@api_view(['PUT'])

def AccountHeadUpdate(request, pk):
    accounthead = AccountHead.objects.get(ah_id=pk)
    serializer = AccountHeadSerializer(instance=accounthead, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
#endregion
# Opening Balance for COA


class openingbalanceViewSet(viewsets.ModelViewSet):
    queryset = OpeningBalance.objects.all()
    serializer_class = OpeningBalanceSerializer


class openingbalanceList(generics.ListAPIView):
    queryset = OpeningBalance.objects.all()
    serializer_class = OpeningBalanceSerializer

    @api_view(['GET'])
    def OpeningBalanceCreation(self, request):
        openingbalance = OpeningBalance.objects.all()
        serializer = OpeningBalanceSerializer(openingbalance, many=True)
        return Response(serializer.data)



class COAGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = COA.objects.all()
    serializer_class = JoinCOASerializer


    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })
        return self.list(request)


#get ob short by company id
@api_view(['GET'])

def obshortbycompanyid(request, comp_id):

    obj = OpeningBalanceView.objects.filter(company_id=comp_id)
    print(obj)
    serializer = JoinCOASerializer(obj, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def OpeningBalanceDetail(request, pk):
    openingbalance = OpeningBalance.objects.get(ob_id=pk)
    serializer = OpeningBalanceSerializer(openingbalance, many=False)
    return Response(serializer.data)

# opening balance for chart of account


@api_view(['PUT'])

def coaobUpdate(request, pk):
    openingbalance = OpeningBalance.objects.get(ob_id=pk)
    serializer = OpeningBalanceSerializer(
        instance=openingbalance, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# opening balance for customer


@api_view(['PUT'])

def customerobUpdate(request, pk):
    openingbalance = OpeningBalance.objects.get(ob_id=pk)
    serializer = OpeningBalanceSerializer(
        instance=openingbalance, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# get all transactions of respective chart of account
#all transaction data get in with respective chart of account
class COATransactionsGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = COA.objects.all()
    serializer_class = transactionsSerializer


    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })
        return self.list(request)

#Master Transaction Full View Get Short By Coa_id related All Transaction 
# By To and From Side
# from_mast=None
# to_mast=None
# from_data=None
# to_data=None




#Journa Trasaction data in Coa 
#Char of Trasaction data which respective chart off account through added in master trasaction
#check the one by one coa to which categories through added in coa

@api_view(['GET'])
def getJRNLTransbyCoaId(self,from_to_id):
    objs = TransactionDetail.objects.filter(account=from_to_id,amount__gt=0).order_by('trans_date','created_date')
    serializer = TransactionDetailSerializer(objs,many=True)
    return Response(serializer.data,status=200)

@api_view(['GET'])
def getJRNLTransbyId(self,from_to_id):
    objs = TransactionDetail.objects.filter(L1detail_id=from_to_id).order_by('trans_date','created_date')
    print(objs)
    serializer = TransactionDetailSerializer(objs,many=True)
    return Response(serializer.data,status=200)

@api_view(['GET'])

def getJRNLTransbyCOAID(self,from_to_id):
    
        #check the from id in mastertrasaction table and filter of data with respective chart of account
        from_mast = MasterTransaction.objects.filter(from_account=from_to_id)

        print('@@@@@@',from_mast)
        #check the to id in mastertrasaction table and filter of data with respective chart of account
        to_mast = MasterTransaction.objects.filter(to_account=from_to_id)
        all_transactions = from_mast | to_mast
        
        # check the from mast length is greter than 0 below code excuted and its used in data frame
        #used pandas dataframe
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
            return Response("Data not found") 
        from_response = json.loads(df_accounts.to_json(orient='records'))
        from_serializer = MasterTransactionSerializer(from_mast, many=True)
        to_serializer= MasterTransactionSerializer(to_mast,many=True)
        
        all_response = {
                'transaction': from_response,

                # 'to_transaction':to_response,
            }
        return Response(all_response) 

# Commenting By Shubham
# region Opening Balance Section
# Post Code For Opening Balance

class Opening_BalanceViewSet(viewsets.ViewSet):

    def create(self,request):
        if request.user.role != 'admin':
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        data = request.data
        return self.handle_post(data)
    @transaction.atomic
    def handle_post(self, data):

        transactions = data['ob_data']
        company_id = data['company_id']
        comp_id = Company.objects.get(company_id=company_id)
        data["ob_date"] = get_financial_year_start(comp_id.financial_year)
        # Remove Opening Balance Adjus as its beign caluclated here

        MasterTransaction.objects.filter(L1detailstbl_name='OpeningBalance',company_id=company_id).delete()
        OpeningBalance.objects.filter(company_id=company_id).delete()

        # Fill this list with created opening balances and master trnsaction
        opening_balances = []
        master_transactions = []
        difference = float(data['difference'])
        # Make one more entry in both tables if available balance is greater than zero
        if difference  > 0:
            adjustment_coa = COA.objects.select_for_update().get(
                account_name='Opening Balance Adjustment', company_id=data['company_id'],system=True)

            adjustment_entry = {
                "coa_id": adjustment_coa.coa_id, 
                "debit": 0, 
                "credit": 0}
            # Check wether that entry will be of debit side or credit side
            if data['sub_total_cr'] < data['sub_total_dr']:
                # Then entry will be of credit side
                adjustment_entry["credit"]= data['difference']
                
            else:
                adjustment_entry["debit"]= data['difference']

            transactions.append(adjustment_entry)

        # Loop through data
        for transaction in transactions:
            # Discard value where debit and credit are null:
            if not (float(transaction['debit']) > 0 or float(transaction['credit']) > 0):
                continue

            # Create opening balance id
            try:
                opening_balance = OpeningBalance.objects.get(coa_id=transaction['coa_id'],
                                                             company_id_id=data['company_id'])
                opening_balance.credit=transaction['credit']
                opening_balance.debit=transaction['debit']
                opening_balance.migration_date=data['ob_date']
                opening_balance.notes=data['notes']
                opening_balance.save()
            except OpeningBalance.DoesNotExist:
                opening_balance = OpeningBalance.objects.create(
                    coa_id_id=transaction['coa_id'],
                    credit=transaction['credit'],
                    debit=transaction['debit'],
                    company_id_id=data['company_id'],
                    migration_date=data['ob_date'],
                    notes=data['notes']
                )
            opening_balances.append(opening_balance)

            # Add common details for master transaction
            master_transaction = MasterTransaction(
                L1detail_id=opening_balance.ob_id,
                L1detailstbl_name='OpeningBalance',
                main_module='COA',
                module='Chart of Account',
                sub_module='OpeningBalance',
                transc_deatils='Opening Balance',
                banking_module_type='Opening Balance',
                journal_module_type='Opening Balance',

                trans_date=data["ob_date"],
                trans_status="Manually Added",
                company_id_id=data["company_id"])
            print('Coa is Herer' ,transaction['coa_id'])
            coa_instance = COA.objects.get(coa_id=transaction['coa_id'])

            # Add either debit or credit values to master transaction
            if float(transaction['debit']) > 0:
                coa_instance.OpenBalance = transaction['debit']
                master_transaction.debit = transaction['debit']
                master_transaction.to_account = coa_instance.coa_id
                master_transaction.to_acc_type = coa_instance.account_type
                master_transaction.to_acc_head = coa_instance.account_head
                master_transaction.to_acc_subhead = coa_instance.account_subhead
                master_transaction.to_acc_name = coa_instance.account_name
            elif float(transaction['credit']) > 0:
                coa_instance.OpenBalance = transaction['credit']
                master_transaction.credit = transaction['credit']
                master_transaction.from_account = coa_instance.coa_id
                master_transaction.from_acc_type = coa_instance.account_type
                master_transaction.from_acc_head = coa_instance.account_head
                master_transaction.from_acc_subhead = coa_instance.account_subhead
                master_transaction.from_acc_name = coa_instance.account_name
            else:
                return Response(f"Both credit and debit are not greater than 0: {transaction}", status=400)
            coa_instance.OpenBalanceDate = data['ob_date']
            coa_instance.save()
            master_transaction.save()
            master_transactions.append(master_transaction)

        # return all modified/created data
        opening_balances_data = OpeningBalanceSerializer(
            opening_balances, many=True).data
        master_transactions_data = MasterTransactionSerializer(
            master_transactions, many=True).data
        return Response({
            'opening_balances': opening_balances_data,
            'master_transactions': master_transactions_data
        })

# endregion
# End Of the Opening Balance Section


# @api_view Allow to define function that match http methods
#Check the Account name is null or not
@api_view(['GET'])

def getcoashortbycompanyid(request, comp_id):
    
    
    
    try:
        company = Company.objects.get(company_id=comp_id)
        coa = COA.objects.filter(company_id=company, account_name__isnull=False ) 
    except Company.DoesNotExist:
        return Response("Company Does Not Exist")
    
     # Serialize the items and return the paginated response
    serializer=COASerializerShortbyCompany(coa, many=True).data
    return Response(serializer)


@api_view(['GET'])
@renderer_classes([JSONRenderer])

def getCOADetailsByaccount_name(request, company_id,name):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    coas = AccountBalance.objects.filter(company_id=company_id,account_name__icontains=name, account_name__isnull=False,
                                         isdefault=False)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": coas.count()
    }
    coa = coas[offset:offset + limit]
    response['results'] = COASerializerShortbyCompany(coa, many=True).data
    print(response['results'])
    return Response(response)


@api_view(['GET'])
@renderer_classes([JSONRenderer])

def getCOADetailsByaccount_type(request, company_id,account_type):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    coas = AccountBalance.objects.filter(company_id=company_id,account_type__icontains=account_type, account_name__isnull=False,
                                         isdefault=False
                                         )
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": coas.count()
    }
    coa = coas[offset:offset + limit]
    response['results'] = COASerializerShortbyCompany(coa, many=True).data
    return Response(response)