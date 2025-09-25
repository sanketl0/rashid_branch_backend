
import datetime
from rest_framework import viewsets,generics,mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from salescustomer.models.Tcs_model import *
from salescustomer.models.Customerob_model import CustomerOB
from coa.models import COA
import pandas as pd
import json
from transaction.serializers import MasterTransactionSerializer
from transaction.models import MasterTransaction
from salescustomer.models.Salescustomer_model import SalesCustomer,CustomerTcs
from salescustomer.serializers.Salescustomer_serializers import WholeCustomerSerializer,NewSalesCustomerSerializer, SalesCustomerSerializer,PaginationcustomershortbycompanySerializer,SalesCustomerSerializerUpdate
from salescustomer.serializers.Salescustomer_serializers import ShortCustomerSerializer,customernameSerializer,customershortbycompanySerializer,JoinCustomerSerializer
from salescustomer.serializers.Salescustomer_serializers import PRCustomerSerializer,CustomerPaymentRefundSerializer,GETCreditNoteCustomerSerializer,CNStatusCustomerSerializer
from rest_framework.parsers import MultiPartParser,JSONParser
from django.db import transaction
from registration.models import  Feature
from salescustomer.serializers.Customerob_serializers import CustomerObSerializer
from coa.views import CoaSubheadView

@api_view(['GET'])
def getpaymentbycustomerid(request, pk):
    instance =SalesCustomer.objects.get(pk=pk)
    serializer =CustomerPaymentRefundSerializer(instance)
    return Response(serializer.data) 


#class Base Return The all Customer
class customerList(generics.ListAPIView):
    queryset = SalesCustomer.objects.all()
    serializer_class = SalesCustomerSerializer

    @api_view(['GET'])
    def customerCreation(self, request):
        customer = SalesCustomer.objects.all()
        serializer = SalesCustomerSerializer(customer, many=True)
        return Response(serializer.data)


# customer and opening balance join
class CustomerGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = SalesCustomer.objects.all()
    serializer_class = JoinCustomerSerializer

    
    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })
        return self.list(request)

    # post for customer opening balance(addcustomerob)


class customerobViewSet(viewsets.ModelViewSet):
    queryset = SalesCustomer.objects.all()
    serializer_class = CustomerObSerializer

    
    @api_view(['POST'])
    def customerob(request):
        customer = SalesCustomer.objects.all()
        serializer = SalesCustomerSerializer(
            instance=customer, data=request.data)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


# getshortDetails
@api_view(['GET'])


def ShortCustomerDetails(request):
    customer = SalesCustomer.objects.all()
    serializer = ShortCustomerSerializer(customer, many=True)
    return Response(serializer.data)


# getcustomerbyname
@api_view(['GET'])


def customername(request):
    customer = SalesCustomer.objects.all()
    serializer = customernameSerializer(customer, many=True)
    return Response(serializer.data)


# #getcustomershortbycompanyid()
# @api_view(['GET'])
# def customershortbycompanyid(request, comp_id):
#     customer = SalesCustomer.objects.get(company_id=comp_id)
#     serializer = customershortbycompanySerializer(customer, many=False)
#     return Response(serializer.data)

# getcustomershortbycompanyid(demo currently live)
@api_view(['GET'])


def customernameallshortbycompanyid(request, comp_id,customer_name,branch_id):


    customer = CustomerTcs.objects.filter(company_id=comp_id,
                                          branch_id=branch_id,
                                          customer_name__icontains=customer_name)[:10]

    serializer = WholeCustomerSerializer(customer, many=True)
    return Response(serializer.data)

@api_view(['GET'])


def customershortbycompanyid(request, comp_id):
    comapny = Company.objects.get(company_id=comp_id)
    customer = SalesCustomer.objects.filter(company_id=comapny)
    serializer = customershortbycompanySerializer(customer, many=True)
    return Response(serializer.data)

@api_view(['GET'])


def customerallshortbycompanyid(request, comp_id,branch_id):

    customer = CustomerTcs.objects.filter(company_id=comp_id,branch_id=branch_id)
    serializer = WholeCustomerSerializer(customer, many=True)
    return Response(serializer.data)

@api_view(['GET'])

def customershortbypaginationcompanyid(request, comp_id,branch_id):
    all = request.GET.get('all',False)
    if all:
        customers = SalesCustomer.objects.filter(company_id=comp_id,branch_id=branch_id)

    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": SalesCustomer.objects.filter(company_id=comp_id,branch_id=branch_id).count()
    }

    # Get the company object by comp_id and apply pagination
    try:
        company = Company.objects.get(company_id=comp_id)
        items = SalesCustomer.objects.filter(company_id=company,branch_id=branch_id).order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = PaginationcustomershortbycompanySerializer(items, many=True).data
    print("stage 1")
    return Response(response)



# getcustomerbyid
@api_view(['GET'])


def customerDetail(request, pk):
    customer = SalesCustomer.objects.get(customer_id=pk)
    serializer = SalesCustomerSerializer(customer, many=False)
    return Response(serializer.data)


# update customer
@api_view(['POST'])


def customerUpdate(request, pk):
    customer = SalesCustomer.objects.get(customer_id=pk)
    serializer = SalesCustomerSerializer(instance=customer, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#Customer Pagination section
@api_view(['GET'])


def getAllPeginatedCustomerDetails(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": SalesCustomer.objects.count()}

    queryset = SalesCustomer.objects.all()[offset:offset + limit]
    serializer = ShortCustomerSerializer(queryset, many=True)

    response['results'] = ShortCustomerSerializer(queryset, many=True).data
    return Response(response)

# getcust

@api_view(['GET'])


def getAllPeginatedCustomername(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": SalesCustomer.objects.count()}

    queryset = SalesCustomer.objects.all()[offset:offset + limit]
    serializer = customernameSerializer(queryset, many=True)

    response['results'] = customernameSerializer(queryset, many=True).data
    return Response(response)





#Customer Update Section
class CustomerUpdtViewset(viewsets.ModelViewSet):
    queryset=SalesCustomer.objects.all()
    serializer_class=SalesCustomerSerializer

    def update(self,request,pk):
        customer_data = request.data
        return self.handle_update(customer_data,pk)

    @transaction.atomic
    def handle_update(self, customer_data, pk):


        cust = SalesCustomer.objects.select_for_update().get(customer_id=pk)

        cust_serializers = SalesCustomerSerializerUpdate(cust, data=customer_data)

        if cust_serializers.is_valid():
            cust_serializers.save()
            msg="Details Updated Successfully"

            return Response(cust_serializers.data,status=200)
        else:
            print(cust_serializers.errors)
            return Response(cust_serializers.errors, status=400)


@api_view(['GET'])
def getexcessamountpaymentbycustomerid(request, pk):
    instance =SalesCustomer.objects.get(pk=pk)
    serializer =PRCustomerSerializer(instance)
    return Response(serializer.data) 







# GET CreditNote by Customer Id
@api_view(['GET'])


def getcreditnotebycustomerid(request, pk):
    instance =SalesCustomer.objects.get(pk=pk)
    serializer =GETCreditNoteCustomerSerializer(instance)
    return Response(serializer.data) 

# GET CreditNote CN_Status by Customer Id
@api_view(['GET'])


def getcnstatusopenbycustomer(request, pk):
    instance =SalesCustomer.objects.get(pk=pk)
    serializer =CNStatusCustomerSerializer(instance)
    return Response(serializer.data)


#Customer Creation and Customer Opening Balnce adding Section 
class newcustomerViewSet(viewsets.ModelViewSet):
    queryset = SalesCustomer.objects.all()
    serializer_class = SalesCustomerSerializer

    parser_classes = [MultiPartParser,JSONParser]
    
    def create(self,request):
        try:
            estimate_data_converte = request.data['data']
            customer_data = json.loads(estimate_data_converte)
        except:
            customer_data = request.data
        print(request.FILES)
        customer_file_data = request.FILES.get('invoice_template')
        return self.handle_post(customer_data,customer_file_data)

    @transaction.atomic
    def handle_post(self, customer_data, customer_file_data):
        # count = Feature.objects.get(user_id=request.user.id).customer_remaining
        # print(count, 'customers')
        # if count <= 0:
        #     return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)



        print("customer_file_data", type(customer_file_data))
        comp_id = Company.objects.get(company_id=customer_data["company_id"])
        branch =  Branch.objects.get(branch_id=customer_data["branch_id"])
      
        cust_serializer = NewSalesCustomerSerializer(data=customer_data)
        if cust_serializer.is_valid():
            customer_id = cust_serializer.save()
            customer_id.invoice_template = customer_file_data
            customer_id.save()


        else:
            return Response(cust_serializer.errors)
        opening_balance_credit=float(customer_data.get('credit',0))
        opening_balance_debit=float(customer_data.get('debit',0))
        print("************************* opening balance is",opening_balance_credit)         
        if opening_balance_credit > 0:
                print("*************************",opening_balance_credit) 
                customer_id.opening_balance = opening_balance_credit
                customer_id.save()
                account_rec = COA.objects.get(company_id=customer_data['company_id'], account_subhead="Account Receivables",isdefault=True)
                print("",account_rec)
                opening_balance_object = CustomerOB.objects.create(
                        coa_id_id=account_rec.coa_id,
                        credit=opening_balance_credit,
                        customer_id_id=customer_id.customer_id,
                    
                        
                    )
                opening_balance_object.save()
                
                print("****************************",opening_balance_object)
                master_transaction = MasterTransaction(

                    L1detail_id=opening_balance_object.ob_id,

                    L1detailstbl_name='Customer_OpeningBalance',
                    main_module='Customer',
                    module='Customer',
                    sub_module='Customer_OpeningBalance',
                    transc_deatils='Customer_OpeningBalance',
                    banking_module_type='Customer_OpeningBalance',
                    journal_module_type='Customer_OpeningBalance',
                    
                    #trans_date=customer_data['ob_date'],
                    trans_status="Manually Added",
                    company_id_id=comp_id.company_id,
                    branch_id=branch,
            
                  ##  coa_instance = COA.objects.get(coa_id=customer_data['coa_id']),

            #  Add either debit or credit values to master transaction
                    
                # debit =opening_balance_amount,
                    credit =opening_balance_credit, # this is changed by varsha from debit to credit after discussion with shubham
                    to_account = account_rec.coa_id,
                    to_acc_type = account_rec.account_type,
                    to_acc_head = account_rec.account_head,
                    to_acc_subhead = account_rec.account_subhead,
                    to_acc_name = account_rec.account_name,
                    customer_id_id=customer_id.customer_id,
                    from_account=account_rec.coa_id,
                   # to_account=account_rec.coa_id,
                    #from_account = account_rec.coa_id,
                    from_acc_type = account_rec.account_type,
                    from_acc_head = account_rec.account_head,
                    from_acc_subhead = account_rec.account_subhead,
                    from_acc_name = account_rec.account_name,
                    trans_date=datetime.date.today()
                )
                
                master_transaction.save()
        if  opening_balance_debit > 0:
           
                customer_id.opening_balance = opening_balance_debit
                customer_id.save()
                account_rec = COA.objects.get(company_id=customer_data['company_id'], account_subhead="Account Receivables",isdefault=True)
                print("",account_rec)
                opening_balance_object = CustomerOB.objects.create(
                        coa_id_id=account_rec.coa_id,
                        credit=opening_balance_credit,
                        debit=opening_balance_debit,
                        customer_id_id=customer_id.customer_id,
                    
                        
                    )
                opening_balance_object.save()
                
                print("****************************",opening_balance_object)
                master_transaction = MasterTransaction(

                    L1detail_id=opening_balance_object.ob_id,

                    L1detailstbl_name='Customer_OpeningBalance',
                    main_module='Customer',
                    module='Customer',
                    sub_module='Customer_OpeningBalance',
                    transc_deatils='Customer_OpeningBalance',
                    banking_module_type='Customer_OpeningBalance',
                    journal_module_type='Customer_OpeningBalance',
                    
                    #trans_date=customer_data['ob_date'],
                    trans_status="Manually Added",
                    company_id_id=comp_id.company_id,
                    branch_id=branch,
                  ##  coa_instance = COA.objects.get(coa_id=customer_data['coa_id']),

            #  Add either debit or credit values to master transaction
                    
                # debit =opening_balance_amount,
                    debit =opening_balance_debit, # this is changed by varsha from debit to credit after discussion with shubham
                    to_account = account_rec.coa_id,
                    to_acc_type = account_rec.account_type,
                    to_acc_head = account_rec.account_head,
                    to_acc_subhead = account_rec.account_subhead,
                    to_acc_name = account_rec.account_name,
                    customer_id_id=customer_id.customer_id,
                    from_account=account_rec.coa_id,
                   # to_account=account_rec.coa_id,
                    #from_account = account_rec.coa_id,
                    from_acc_type = account_rec.account_type,
                    from_acc_head = account_rec.account_head,
                    from_acc_subhead = account_rec.account_subhead,
                    from_acc_name = account_rec.account_name,
                    trans_date=datetime.date.today()
                )
                
                master_transaction.save()
                
        serializer = NewSalesCustomerSerializer(customer_id)  # browser
        print(" output serializer data",serializer.data)
        return Response({"data":serializer.data,"status":200},status=201)

#With Respective Customer related All Transaction in Below Section 
#Means Master Trasaction table How many trasction in With respective customer Related To Return In Report Formating

from coa.models import TransactionDetailCV
from coa.serializers import TransactionDetailCVSerializer
@api_view(['GET'])
def getJRNLTransbyCUSTOMERID(request,from_to_id):
        objs = TransactionDetailCV.objects.filter(customer_id=from_to_id)
        print(objs)
        serializer = TransactionDetailCVSerializer(objs, many=True)
        return Response(serializer.data, status=200)
        # Fetch transactions where 'from_acc_subhead' is 'Account Receivables'
        from_mast = MasterTransaction.objects.filter(customer_id=from_to_id,from_acc_subhead='Account Receivables')
        
        
        print('@@@@@@',MasterTransaction.customer_id)
        
        to_mast = MasterTransaction.objects.filter(customer_id=from_to_id,to_acc_subhead='Account Receivables')
        
        all_transactions = from_mast | to_mast

        if  len(from_mast) > 0 :      
            from_df = pd.DataFrame(from_mast.values('L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                                'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 
                                'credit','transc_deatils','trans_date','trans_status','created_date',))
           
            from_acc = from_df.groupby(['L1detail_id','from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name',
                                        'transc_deatils','trans_date','trans_status','created_date']).agg(
            {'credit': 'sum'}).reset_index()
            from_acc = from_acc.rename(columns={'L1detail_id':'L1detail_id',
                                    'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead',
                                    'from_acc_name':'account_name','transc_deatils':'transc_deatils','trans_date':'trans_date',
                                    'trans_status':'trans_status','created_date':'created_date'}, inplace=False)
            # Filter only positive credit values
            from_acc = from_acc.loc[from_acc['credit'] > 0]
            
        else:
            from_acc = None

        if len(to_mast) > 0:
            to_df = pd.DataFrame(to_mast.values('L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                                'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit','transc_deatils','trans_date','trans_status'))
           
            to_acc = to_df.groupby(['L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name','transc_deatils','trans_date','trans_status',]).agg(
                { 'debit': 'sum'}).reset_index()
            to_acc = to_acc.rename(columns={'L1detail_id':'L1detail_id',
                                    'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name','transc_deatils':'transc_deatils','trans_date':'trans_date','trans_status':'trans_status','created_date':'created_date'}, inplace=False)
            # Filter only positive debit values
            to_acc = to_acc.loc[to_acc['debit'] > 0]
        else:
            to_acc = None
        
        if from_acc is not None and to_acc is not None:
            
            df_accounts = pd.concat([from_acc, to_acc])
        elif from_acc is not None:
            df_accounts = from_acc
        elif to_acc is not None:
            df_accounts = to_acc
            
        else:
            print(from_mast,to_mast)
            return Response("Data not found",status=200)
        df_accounts = df_accounts.sort_values(by='trans_date',ascending=True)
        from_response = json.loads(df_accounts.to_json(orient='records'))
        from_serializer = MasterTransactionSerializer(from_mast, many=True)
        to_serializer= MasterTransactionSerializer(to_mast,many=True)
        from_data=from_serializer.data
        to_data=to_serializer.data
        all_response = {
                'from_data': from_data,
                'to_data':to_data,
                'transaction': from_response,

                # 'to_transaction':to_response,
            }
        print(all_response)
        return Response(all_response)


@api_view(['GET'])

def getJRNLbyFormID(request, form_id):
    form_mast = MasterTransaction.objects.filter(L1detail_id=form_id)
    df = pd.DataFrame(form_mast.values('to_acc_type', 'to_acc_head', 'to_acc_subhead', 'to_acc_name',
                                       'from_acc_type', 'from_acc_subhead', 'from_acc_head', 'from_acc_name', 'debit',
                                       'credit'))

    # Define the columns to check
    columns_to_check = ['from_acc_type', 'from_acc_head', 'from_acc_subhead', 'from_acc_name', 'debit', 'credit',
                        'to_acc_type', 'to_acc_head', 'to_acc_subhead', 'to_acc_name']

    # Check if the columns exist and replace missing values with None
    for col in columns_to_check:
        if col not in df.columns:
            df[col] = None

    print("coming columns in dataframe", df.columns)

    # Check if 'credit' and 'debit' columns exist before aggregation
    if 'credit' in df.columns:
        from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead', 'from_acc_name']).agg(
            {'credit': 'sum'}).reset_index()
    else:
        from_acc = pd.DataFrame(
            columns=['from_acc_type', 'from_acc_head', 'from_acc_subhead', 'from_acc_name', 'credit'])

    if 'debit' in df.columns:
        to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead', 'to_acc_name']).agg(
            {'debit': 'sum'}).reset_index()
    else:
        to_acc = pd.DataFrame(columns=['to_acc_type', 'to_acc_head', 'to_acc_subhead', 'to_acc_name', 'debit'])

    from_acc = from_acc.rename(columns={
        'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead',
        'from_acc_name': 'account_name'}, inplace=False)
    to_acc = to_acc.rename(columns={
        'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead',
        'to_acc_name': 'account_name'}, inplace=False)

    print("FROM ACCOUNT DATA", from_acc)
    print("TO ACCOUNT DATA", to_acc)
    df_accounts = pd.concat([from_acc, to_acc])

    response = json.loads(df_accounts.to_json(orient='records'))

    serializer = MasterTransactionSerializer(form_mast, many=True)
    n_data = serializer.data
    all_response = {
        # 'original_data': account_type_list,
        'form_data': n_data,
        'transaction': response,
    }
    return Response(all_response)

# Get search details by customer name 
@api_view(['GET'])


def getCustomerDetailsByCustomerName(request, company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    customer_name = request.GET['name']
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": SalesCustomer.objects.filter(company_id=company_id,customer_name__icontains=customer_name,branch_id=branch_id).count()}
    
    instance = SalesCustomer.objects.filter(company_id=company_id,customer_name__icontains=customer_name,branch_id=branch_id)[offset:offset + limit]
    print(instance)
    serializer = customernameSerializer(instance, many=True)
    
    response['results'] = ShortCustomerSerializer(instance, many=True).data
    return Response(response)



# Get search details by customer contact number 
@api_view(['GET'])

#
def getCustomerDetailsByCustomerMobileNo(request, company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    customer_mobile = request.GET['mobile']
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": SalesCustomer.objects.filter(company_id=company_id,
                                                      branch_id=branch_id,
                                                      customer_mobile__icontains=customer_mobile).count()}
    
    instance = SalesCustomer.objects.filter(company_id=company_id,
                                            branch_id=branch_id,
                                            customer_mobile__icontains=customer_mobile)[offset:offset + limit]
    serializer = customernameSerializer(instance, many=True)
    
    response['results'] = ShortCustomerSerializer(instance, many=True).data
    return Response(response)