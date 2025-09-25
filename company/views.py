from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics
from .models import Company, Branch,Defaults
from .serializers import CompanySerializer, \
    BranchSerializerV1,CompanySerializerUpdate, ShortBranchSerializer, BranchSerializer,DefaultSerializer,CompanyGetSerializer

from coa .models import *
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated,SAFE_METHODS
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework import permissions
from django.db import connection
from django.http import JsonResponse
from salescustomer.models.Paymentmode_model import PaymentMode
from item.models.item_model import Item
from item.models.stock_model import Stock
from salescustomer.models.Salescustomer_model import SalesCustomer
from purchase.models.Vendor_model import Vendor
from salescustomer.models.Tcs_model import TCS
from purchase.models.Tds_model import TDS
from salescustomer.models.Employee_model import Employee
from transaction.models import Charges
from registration.models import Subscribe,UserAccess
from salescustomer.models.Paymentterms_model import PaymentTerms
from django.db import connections
import copy
from django.db import transaction
from datetime import date
from report.models import AccountBalance
from transaction.models import MasterTransaction
from registration.models import  Feature
from registration.serializers import FeatureSerializer
from django.db.models import Q
from rest_framework.views import APIView
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000

class DefautlView(APIView):
    def get(self,request,comp_id=None,branch_id=None):
        objs = Defaults.objects.filter(company_id=comp_id,branch_id=branch_id)

        if objs:
            obj = objs[0]
            serialiazer = DefaultSerializer(obj)
            return Response(serialiazer.data,status=200)
        return Response({"message":"No Default Found"},status=400)
    def post(self,request,branch_id,comp_id):
        data = request.data
        objs = Defaults.objects.filter(company_id=comp_id, branch_id=branch_id)
        if objs:
            obj = objs[0]
            serialiazer = DefaultSerializer(obj,data=data)
            if serialiazer.is_valid():
                serialiazer.save()
                return Response(status=200)
        serialiazer = DefaultSerializer(data=data)
        if serialiazer.is_valid():
            serialiazer.save()
            return Response(status=201)
        print(serialiazer.errors)
        return Response({"message":"Not Valid Data"},status=400)

class companyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = StandardResultsSetPagination

    # 


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # if Company.objects.filter(user=request.user).count() > 0:
        #     return Response({"message":"Company Already created"},status=400)# company Data Serialize

        is_copied_coa = request.data.get("is_copied_coa", False)  # Use get() to handle missing key gracefully
        company_id = request.data.get("company_id",None)
        is_new_company = request.data.get('is_new_company',True)



        financial_year = request.data.get('financial_year',None)

        if company_id:

            if Company.objects.filter(user=request.user,financial_year=financial_year).exists():
                return Response({"message":"Financial Year Company already Exist"},status=400)

        data = request.data
        print(data)
        if company_id:
            data._mutable=True
            del data['company_id']
            data['logo_image'] = None

        serializer = CompanySerializer(data=data)

        if serializer.is_valid():

            company = serializer.save(user=request.user)

            company.save()
            sub = Subscribe.objects.get(
                user_id=request.user
            )
            sub.company_id.add(company)

            if company_id:
                obj = Company.objects.get(company_id=company_id)
                company.logo_image = obj.logo_image
                company.save()
                print("Company Created")


            else:
                Base_COAS = BaseCOA.objects.all()
                for basecoa in Base_COAS:
                    COA.objects.create(
                        account_head=basecoa.account_head,
                        account_subhead=basecoa.account_subhead,
                        account_name=basecoa.account_name,
                        account_type=basecoa.account_type,
                        isdefault=True,
                        system=basecoa.system,
                        company_id=company
                    )
            # for each in ["Card", "Cash", "Online"]:
            #     PaymentMode.objects.create(
            #         payment_mode=each,
            #         company_id=company
            #     )
            if company_id:  # No need for comparison with True
                rows = COA.objects.filter(company_id=company_id)
                items = Item.objects.filter(company_id=company_id)
                customers = SalesCustomer.objects.filter(company_id=company_id)
                vendors = Vendor.objects.filter(company_id=company_id)
                terms = PaymentTerms.objects.filter(company_id=company_id)
                tds = TDS.objects.filter(company_id=company_id)
                tcs = TCS.objects.filter(company_id=company_id)
                charges = Charges.objects.filter(company_id=company_id)
                employees = Employee.objects.filter(company_id=company_id)
                modes = PaymentMode.objects.filter(company_id=company_id)
                branches = Branch.objects.filter(company_id=company_id)
                users = request.user.sub_users.all()

                b_dict = {}
                for branch in branches.order_by('created_date'):
                    print(branch)
                    new_branch = Branch.objects.create(
                        company_name=company.company_name,
                        company_id=company,
                        branch_name=branch.branch_name,
                        address=branch.address,
                        city=branch.city,
                        email=branch.email,
                        phone=branch.phone,
                        pincode=branch.pincode,
                        primary_contact=branch.primary_contact,
                        state=branch.state,
                        website=branch.website,
                        gstin=branch.gstin,
                        main_branch=branch.main_branch
                    )
                    b_dict[branch] = new_branch
                print("Branch Created",users)
                for usr in users:
                    access = UserAccess.objects.get(user=usr)
                    temp = []
                    bchs = access.branches.all()
                    print(bchs)
                    for branch in bchs:
                        new_branch = b_dict[branch]
                        temp.append(new_branch)

                    access.branches.add(*temp)
                print("Users Updated Branches")
                for row in rows:
                    COA.objects.create(
                        account_head=row.account_head,
                        account_subhead=row.account_subhead,
                        account_name=row.account_name,
                        account_type=row.account_type,
                        isdefault=row.isdefault,
                        company_id=company
                    )
                print("Coa Created")
                for item in items:
                    purchase_account = COA.objects.get(coa_id=item.purchase_account)
                    sales_account = COA.objects.get(coa_id=item.sales_account)
                    coa_inventory = None
                    if item.track_inventory:
                        inventory = COA.objects.get(coa_id=item.inventory_account)
                        coa_inventory,_ = COA.objects.get_or_create(
                            company_id=company,
                            # branch_id
                            account_type=inventory.account_type,
                            account_head=inventory.account_head,
                            account_subhead=inventory.account_subhead,
                            account_name=inventory.account_name,
                            isdefault=False
                        )
                    id = copy.deepcopy(item.item_id)
                    coa_purchase,_ = COA.objects.get_or_create(
                        company_id=company,
                        account_type=purchase_account.account_type,
                        account_head=purchase_account.account_head,
                        account_subhead=purchase_account.account_subhead,
                        account_name=purchase_account.account_name,
                        isdefault=False
                    )
                    coa_sales,_ = COA.objects.get_or_create(
                        company_id=company,
                        account_type=sales_account.account_type,
                        account_head=sales_account.account_head,
                        account_subhead=sales_account.account_subhead,
                        account_name=sales_account.account_name,
                        isdefault=False
                    )
                    item.purchase_account = coa_purchase.coa_id
                    item.sales_account = coa_sales.coa_id
                    item.inventory_account = coa_inventory.coa_id if coa_inventory else None
                    item.item_id = None
                    item.company_id = company
                    item.branch_id = b_dict[item.branch_id]
                    item.save()
                    if item.track_inventory:
                        stocks = Stock.objects.filter(item_id=id)
                        for stock in stocks:
                            stock.st_id = None
                            stock.company_id = company
                            stock.branch_id = item.branch_id
                            stock.item_id = item.item_id
                            stock.save()
                print("Items Created")
                for customer in customers:
                    customer.customer_id = None
                    customer.company_id = company
                    customer.branch_id = b_dict.get(customer.branch_id,None)
                    customer.save()
                print("Customer Created")
                for vendor in vendors:
                    vendor.vendor_id = None
                    vendor.company_id = company
                    vendor.branch_id = b_dict.get(vendor.branch_id,None)
                    vendor.save()
                print("Vendors Created")
                for term in terms:
                    term.payment_id = None
                    term.company_id = company
                    term.branch_id = b_dict.get(term.branch_id,None)
                    term.save()
                print("Terms Created")
                for td in tds:
                    td.tds_id = None
                    td.company_id = company
                    td.branch_id = b_dict.get(td.branch_id,None)
                    td.save()
                print("Tds Created")
                for md in modes:
                    md.payment_id = None
                    md.company_id = company
                    md.branch_id = b_dict.get(md.branch_id,None)
                    md.save()
                print("Payment Mode Created")
                for tc in tcs:
                    tc.tcs_id = None
                    tc.company_id = company
                    tc.branch_id = b_dict.get(tc.branch_id,None)
                    tc.save()
                print("Tcs Created")
                for charge in charges:
                    charge.chg_id = None
                    charge.company_id = company
                    charge.branch_id = b_dict.get(charge.branch_id,None)
                    charge.save()
                print("Charges Created")
                for employee in employees:
                    employee.emp_id = None
                    employee.company_id = company
                    employee.branch_id =b_dict.get(employee.branch_id,None)
                    employee.save()
                print("Employee Created")

                coas_balance = AccountBalance.objects.filter(company_id=company_id,isdefault=False)
                for each in coas_balance:
                    coa_id = each.coa_id
                    account_n = each.account_name
                    account_h = each.account_head
                    account_s = each.account_subhead
                    account_t = each.account_type
                    account_balance = each.balance
                    debit,credit = 0,0
                    if account_t in ["Assets", "Expenses"] and account_balance >= 0:
                        debit = account_balance
                    if account_t in ["Assets", "Expenses"] and account_balance < 0:
                        credit = abs(account_balance)
                    if account_t not in ["Assets", "Expenses"] and account_balance >= 0:
                        credit = account_balance
                    if account_t not in ["Assets", "Expenses"] and account_balance < 0:
                        debit = abs(account_balance)
                    try:
                        if debit > 0 or credit > 0:
                            print(account_n,account_t,account_s,account_h)
                            obj = COA.objects.get(
                                account_name=account_n,
                                account_head=account_h,
                                account_subhead=account_s,
                                account_type=account_t,
                                isdefault=False,
                                company_id=company)
                            obj.OpenBalance = account_balance
                            obj.save()

                            ob = OpeningBalance.objects.create(
                                coa_id=obj,
                                credit=credit,
                                debit=debit,
                                company_id=company,
                                migration_date=company.books_start_date,
                                notes='new company transfer'
                            )
                            mt = MasterTransaction.objects.create(
                                L1detail_id=ob.ob_id,

                                L1detailstbl_name='OpeningBalance',
                                main_module='COA',
                                module='Chart of Account',
                                sub_module='OpeningBalance',
                                transc_deatils='Opening Balance',
                                banking_module_type='Opening Balance',
                                journal_module_type='Opening Balance',

                                trans_date=company.books_start_date,
                                trans_status="Manually Added",
                                company_id=company)
                            if debit > 0:

                                mt.debit = debit
                                mt.to_account = obj.coa_id
                                mt.to_acc_type = obj.account_type
                                mt.to_acc_head = obj.account_head
                                mt.to_acc_subhead = obj.account_subhead
                                mt.to_acc_name = obj.account_name
                            elif credit > 0:

                                mt.credit = credit
                                mt.from_account = obj.coa_id
                                mt.from_acc_type = obj.account_type
                                mt.from_acc_head = obj.account_head
                                mt.from_acc_subhead = obj.account_subhead
                                mt.from_acc_name = obj.account_name
                            mt.save()

                    except Exception as e:
                        raise Exception("Test")
                        print(e)
                print("Opening balance Transfered")
            # raise Exception("Test")
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
  

#endregion Commenting by Sk comapny creation default COA

#this Section Code is Class return all the company data
class companyList(APIView):
  # Add order_by here
    def get_queryset(self):
        return Company.objects.filter(user=self.request.user).order_by('-created_date')

    def get(self,request):
        serializer = CompanyGetSerializer(self.get_queryset(),many=True)
        return Response(serializer.data,status=200)

    
    
#Get the Specific Company Relted Data Return to Company Id Wise
@api_view(['GET'])

#@permission_classes(( IsAuthenticated,))
def companyDetail(request, pk):
    company = Company.objects.get(company_id=pk)
    serializer = CompanySerializer(company, many=False)
    return Response(serializer.data)

#getallcompanyname


@api_view(['GET'])

@permission_classes(( IsAuthenticated,))
def AllCompanyNameDetails(request):
    # Get the company queryset and order it by the 'created_date' field in descending order

    company = Company.objects.filter(Q(user=request.user) |Q(user=request.user.sub_users.all()[0])).order_by('-created_date')

    serializer = CompanySerializer(company, many=True,user=request.user)
    return Response(serializer.data)


@api_view(['GET'])

@permission_classes(( IsAuthenticated,))
def planFeatureView(request):
    # Get the company queryset and order it by the 'created_date' field in descending order

    return Response(FeatureSerializer(Feature.objects.get(user_id=request.user.id)).data)
#geting the company_id and this company id will be updated

@api_view(['POST'])
def companyUpdate(request, pk):
    company = Company.objects.get(company_id=pk)
    serializer = CompanySerializer(instance=company, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
#Baranch Code Section and this section currently not working 
#client say to active to use this code
#region
#Branch



class branchViewSet(APIView):

    def handle_post(self,data,user):
        count = Feature.objects.get(user_id=user.id).branch_remaining
        print(count)
        # if count <= 0 and user.role == "admin":
        #     return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        serializer = BranchSerializer(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.company_name = obj.company_id.company_name
            obj.main_branch = False
            obj.save()
            access = user.user_access.all()[0]
            access.branches.add(obj)
            return Response(status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.handle_post(request.data,request.user)

    @transaction.atomic
    def handle_put(self,data,pk=None):
        branch = Branch.objects.select_for_update().get(branch_id=pk)
        print(data)
        serializer = BranchSerializerV1(branch, data=data)
        if serializer.is_valid():
            obj = serializer.save()
            print(serializer.data)
            obj.main_branch = False
            return Response({"message": "Successfully Updated Branch"}, status=201)
        print(serializer.errors)
        return Response({"message": "Errors in Serializing Branch"}, status=400)


    def put(self,request,pk=None):
        return self.handle_put(request.data,pk)


class branchList(APIView):



    def get(self,request,comp_id=None):
        branch = Branch.objects.filter(company_id_id=comp_id).order_by('created_date')

        serializer = BranchSerializer(branch, many=True)
        return Response(serializer.data)

#getshortDetails
@api_view(['GET'])


def ShortBranchDetails(request):
    branch = Branch.objects.all()   
    serializer = ShortBranchSerializer(branch, many=True)
    return Response(serializer.data)

@api_view(['GET'])


def branchDetail(request, pk):
    branch = Branch.objects.get(branch_id=pk)
    serializer = BranchSerializer(branch, many=False)
    return Response(serializer.data)

@api_view(['POST'])


def branchUpdate(request, pk):
    branch = Branch.objects.get(branch_id=pk)
    serializer = BranchSerializer(instance=branch, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


#endregion
import json
################ UPDATE COMPANY API ##############################
class CompanyUpdateViewset(viewsets.ModelViewSet):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer

    

    @transaction.atomic
    def update(self, request, pk, *args, **kwargs):
        company_data = request.data
        file_data = request.FILES.get('logo_image')

        company= Company.objects.select_for_update().get(company_id=pk)

        print(file_data)
        cust_serializers = CompanySerializerUpdate(company, data=company_data,user=request.user)

        if cust_serializers.is_valid():

            cust_serializers.save()
            if file_data:
                company.logo_image = file_data
                company.save()
            msg="Details Updated Successfully"
            return Response(cust_serializers.data)
        else:
            print(cust_serializers.errors)
            return Response(cust_serializers.errors, status=400)

#endregion


import subprocess

def create_database_backup(username, database_name, backup_file):
    try:
        subprocess.run(['pg_dump', '-U', username, '-Fc', database_name, '>', backup_file], shell=True, check=True)
        print("Backup created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")




import subprocess

def create_database_backup(username, database_name, backup_file):
    try:
        subprocess.run(['pg_dump', '-U', username, '-Fc', database_name, '>', backup_file], shell=True, check=True)
        print("Backup created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")

# Example usage
#create_database_backup('[username]', '[database_name]', '[backup_file].dump')


def group_by_company(data,comp_id):
    company_id= comp_id
    grouped_data = {}
    print("API IS HEATING")
    data = Company.objects.filter(company_id=company_id).values('company_name', 'financial_year','company_id','alias_name',
                                                                'address','pincode','city','state','company_type','pan_number',
                                                               'gstin','cin' )
    print("API IS HEATING**")
    for entry in data:
        company_name = entry['company_name']
        financial_year = entry['financial_year']
        company_id=entry['company_id']
        alias_name=entry['alias_name']
        address = entry['address']
        pincode = entry['pincode']
        city=entry['city']
        state=entry['state']
        company_type = entry['company_type']
        pan_number = entry['pan_number']
        gstin=entry['gstin']
        cin=entry['cin']
        print("API IS HEATING****")
        if company_name not in grouped_data:
            grouped_data[company_name] = []
            print("**************************API IS HEATING")
        grouped_data[company_name].append(financial_year)
        grouped_data[company_name].append(company_id)
        grouped_data[company_name].append(alias_name)
        grouped_data[company_name].append(address)
        grouped_data[company_name].append(pincode)
        grouped_data[company_name].append(city)
        grouped_data[company_name].append(state)
        grouped_data[company_name].append(company_type)
        grouped_data[company_name].append(pan_number)
        grouped_data[company_name].append(gstin)
        grouped_data[company_name].append(cin)
    print("///////////////////////////",grouped_data)
    return JsonResponse(grouped_data)




@api_view(['GET'])

def GetAllCompanyDetails(request):
    company = Company.objects.all()   
    serializer = CompanySerializer(company, many=True)
    return Response(serializer.data)



# Get search details by customer name 
@api_view(['GET'])


def getCompanyDetailsByCompanyrName(request, company_name):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count":  Company.objects.filter(user=request.user).count()}
    
    instance = Company.objects.filter(company_name__icontains=company_name,user=request.user)[offset:offset + limit]
    serializer = CompanySerializer(instance, many=True)
    
    response['results'] = CompanySerializer(instance, many=True).data
    return Response(response)



@api_view(['GET'])


def getCompanyDetailsByCompanyType(request, company_type):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count":  Company.objects.filter(user=request.user).count()}
    
    instance = Company.objects.filter(company_type__icontains=company_type,user=request.user)[offset:offset + limit]
    serializer = CompanySerializer(instance, many=True)
    
    response['results'] = CompanySerializer(instance, many=True).data
    return Response(response)