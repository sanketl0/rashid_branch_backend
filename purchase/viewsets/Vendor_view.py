
import datetime
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins

from purchase.models.Vendor_model import Vendor,VendorTds
from company.serializers import CompanySerializer
from purchase.serializers .Vendor_contact_serializers import VendorContactSerializer
from purchase.serializers .Vendor_serializers import  VendorSerializer,allcontactofvendorSerializer,vendornameSerializer,BillbyVendorSerializer,vendorshortbycompanySerializer,VendorExAmountSerializer,VendorpaymenttrefSerializer
from company.models import Company,Branch
from purchase.models.Vendor_contact_model import VendorContact
from purchase.models.Tds_model import TDS
from purchase.serializers.Vendor_serializers import WholeVendorSerializer,WholeVendorJournalSerializer, VendorDebitNoteRefSerializer,ForPaginationvendorshortbycompanySerializer,VendorSerializerUpdate

from rest_framework.decorators import api_view, permission_classes,authentication_classes
from coa.models import COA
from purchase.models.Vendorob_models import VendorOB
from transaction.models import MasterTransaction
import pandas as pd
import json
from transaction.serializers import MasterTransactionSerializer          
from django.db import transaction

from salescustomer.models.Salescustomer_model import CustomerTcs
from salescustomer.serializers.Salescustomer_serializers import WholeCustomerJournalSerializer
#company returns All vendor data
class companyViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = CompanySerializer

# to get the all vendor list


class vendorList(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorContactSerializer




#Class Vendor Details Creation Section
class vendorViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


    @transaction.atomic
    def handle_post(self, vendor_data,vendor_file_data):
        #Convert Str to Dict Code

       # vendor_data = vendor_data_convert

      #  print("vendor_file_data", type(vendor_file_data))
        contact_person = vendor_data.get("contact_person")
        company_id = Company.objects.get(company_id=vendor_data["company_id"])
        branch_id = Branch.objects.get(branch_id=vendor_data["branch_id"])
        tds = None
        try:
            tds = TDS.objects.get(tds_id=vendor_data['tds_id'])
        except:
            pass
        #comp_id = Company.objects.get(company_id=vendor_data["company_id"])
        vendor = Vendor.objects.create(salutation=vendor_data["salutation"],
                                       vendor_name=vendor_data["vendor_name"],
                                       company_name=vendor_data["company_name"],
                                       ext_id=vendor_data.get('ext_id',None),
                                       ext_type='TALLY',
                                       vendor_display_name=vendor_data["vendor_display_name"],
                                       vendor_contact=vendor_data["vendor_contact"],
                                       vendor_mobile=vendor_data["vendor_mobile"],
                                       vendor_email=vendor_data["vendor_email"],
                                       website=vendor_data["website"],
                                       vendor_designation=vendor_data["vendor_designation"],
                                       vendor_department=vendor_data["vendor_department"],
                                       term_name=vendor_data["term_name"],
                                       no_of_days=vendor_data["no_of_days"],
                                       gst_treatment=vendor_data["gst_treatment"],
                                       gstin_number=vendor_data["gstin_number"],
                                       tax_preference=vendor_data["tax_preference"],
                                       source_place=vendor_data["source_place"],
                                       exemption_reason=vendor_data["exemption_reason"],
                                       pan_number=vendor_data["gstin_number"],
                                       b_attention=vendor_data["b_attention"],
                                       bill_address1=vendor_data["bill_address1"],
                                       bill_address2=vendor_data["bill_address2"],
                                       bill_address_city=vendor_data["bill_address_city"],
                                       bill_address_state=vendor_data["bill_address_state"],
                                       bill_address_postal_code=vendor_data["bill_address_postal_code"],
                                       bill_address_country=vendor_data["bill_address_country"],
                                       bill_contact_number=vendor_data["bill_contact_number"],
                                       bill_fax_number=vendor_data["bill_fax_number"],
                                       s_attention=vendor_data["s_attention"],
                                       ship_address1=vendor_data["ship_address1"],
                                       ship_address2=vendor_data["ship_address2"],
                                       ship_address_city=vendor_data["ship_address_city"],
                                       ship_address_state=vendor_data["ship_address_state"],
                                       ship_address_postal_code=vendor_data["ship_address_postal_code"],
                                       ship_address_country=vendor_data["ship_address_country"],
                                       ship_contact_number=vendor_data["ship_contact_number"],
                                       ship_fax_number=vendor_data["ship_fax_number"],
                                       remarks=vendor_data["remarks"],
                                       bill_template=vendor_file_data,
                                       tds_id=tds,
                                       branch_id=branch_id,
                                       company_id=company_id)
        vendor.save()

        contact_person = VendorContact.objects.create(vendor_id=vendor,
                                                      contact_salutation=vendor_data["contact_salutation"],
                                                      contact_name=vendor_data["contact_name"],
                                                      contact_phone=vendor_data["contact_phone"],
                                                      contact_mobile=vendor_data["contact_mobile"],
                                                      contact_email=vendor_data["contact_email"],
                                                      contact_designation=vendor_data["contact_designation"],
                                                      contact_department=vendor_data["contact_department"])
        contact_person.save()
        print("contact_person", contact_person, type(contact_person))

       
            # here vendor is a variable that we taken from above and vendor_id is a

        opening_balance_credit=float(vendor_data.get('credit'))
        opening_balance_debit=float(vendor_data.get('debit'))
        print("************************* opening balance is",opening_balance_credit)         
        if opening_balance_credit > 0:
                print("*************************",opening_balance_credit) 
                vendor.opening_balance = opening_balance_credit
                vendor.save()
                account_rec = COA.objects.get(company_id=vendor_data['company_id'],
                                              account_subhead="Account Payables",isdefault=True)
                print("",account_rec)
                opening_balance_object = VendorOB.objects.create(
                        coa_id_id=account_rec.coa_id,
                        credit=opening_balance_credit,
                        vendor_id_id=vendor.vendor_id,)
                opening_balance_object.save()
                
                print("****************************",opening_balance_object)
                master_transaction = MasterTransaction(

                    L1detail_id=opening_balance_object.Vendorob_id,

                    L1detailstbl_name='Vendor_OpeningBalance',
                    main_module='Vendor',
                    module='Vendor',
                    sub_module='Vendor_OpeningBalance',
                    transc_deatils='Vendor_OpeningBalance',
                    banking_module_type='Vendor_OpeningBalance',
                    journal_module_type='Vendor_OpeningBalance',
                    
                    #trans_date=customer_data['ob_date'],
                    trans_status="Manually Added",
                    branch_id=branch_id,
                    company_id_id=company_id.company_id,
            
                  ##  coa_instance = COA.objects.get(coa_id=customer_data['coa_id']),

            #  Add either debit or credit values to master transaction
                    
                # debit =opening_balance_amount,
                    credit =opening_balance_credit, # this is changed by varsha from debit to credit after discussion with shubham
                    to_account = account_rec.coa_id,
                    to_acc_type = account_rec.account_type,
                    to_acc_head = account_rec.account_head,
                    to_acc_subhead = account_rec.account_subhead,
                    to_acc_name = account_rec.account_name,
                    vendor_id_id=vendor.vendor_id,
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
           
                vendor.opening_balance = opening_balance_debit
                vendor.save()
                account_rec = COA.objects.get(company_id=vendor_data['company_id'],
                                              account_subhead="Account Payables",isdefault=True)
                print("",account_rec)
                opening_balance_object = VendorOB.objects.create(
                        coa_id_id=account_rec.coa_id,
                        credit=opening_balance_credit,
                        vendor_id_id=vendor.vendor_id,)
                opening_balance_object.save()
                
                print("****************************",opening_balance_object)
                master_transaction = MasterTransaction(

                    L1detail_id=opening_balance_object.Vendorob_id,

                    L1detailstbl_name='Vendor_OpeningBalance',
                    main_module='Vendor',
                    module='Vendor',
                    sub_module='Vendor_OpeningBalance',
                    transc_deatils='Vendor_OpeningBalance',
                    banking_module_type='Vendor_OpeningBalance',
                    journal_module_type='Vendor_OpeningBalance',
                    
                    #trans_date=customer_data['ob_date'],
                    trans_status="Manually Added",
                    branch_id=branch_id,
                    company_id_id=company_id.company_id,
            
                  ##  coa_instance = COA.objects.get(coa_id=customer_data['coa_id']),

            #  Add either debit or credit values to master transaction
                    
                # debit =opening_balance_amount,
                    debit =opening_balance_debit, # this is changed by varsha from debit to credit after discussion with shubham
                    to_account = account_rec.coa_id,
                    to_acc_type = account_rec.account_type,
                    to_acc_head = account_rec.account_head,
                    to_acc_subhead = account_rec.account_subhead,
                    to_acc_name = account_rec.account_name,
                    vendor_id_id=vendor.vendor_id,
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
        serializer = VendorSerializer(vendor)  # browser
        return Response(serializer.data,status=201)

    def create(self, request, *args, **kwargs):
        # count = Feature.objects.get(user_id=request.user.id).vendor_remaining
        # print(count,'vendors')
        # if count <= 0:
        #     return Response({"message":"You dont have access to this service please upgrade plan"},status=401)
        vendor_file_data = None
        try:
            vendor_data_convert = request.data['data']
            vendor_data = json.loads(vendor_data_convert)
            vendor_file_data = request.FILES.get('bill_template')
        except:
            vendor_data = request.data
        return self.handle_post(vendor_data,vendor_file_data)

#Vendor 
class VendorAndContactGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Vendor.objects.all()
    serializer_class = allcontactofvendorSerializer


    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })
        return self.list(request)




class vendorList(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


@api_view(['GET'])

def vendorDetail(request, pk):
    vendor = Vendor.objects.get(vendor_id=pk)
    serializer = allcontactofvendorSerializer(vendor, many=False)
    return Response(serializer.data)

# get vendor short by company id


@api_view(['GET'])

def vendorshortbycompanyid(request, comp_id):
    company = Company.objects.get(company_id=comp_id)
    vendor = Vendor.objects.filter(company_id=company)
    serializer = vendorshortbycompanySerializer(vendor, many=True)
    return Response(serializer.data)

@api_view(['GET'])

def vendorallshortbycompanyid(request, comp_id,branch_id):

    vendor = VendorTds.objects.filter(company_id=comp_id,branch_id=branch_id)
    serializer = WholeVendorSerializer(vendor, many=True)
    return Response(serializer.data)

@api_view(['GET'])

def vendornameallshortbycompanyid(request, comp_id,vendor_name,branch_id):


    customer = VendorTds.objects.filter(company_id=comp_id,
                                        branch_id=branch_id,
                                        vendor_name__icontains=vendor_name)[:10]

    serializer = WholeVendorSerializer(customer, many=True)
    return Response(serializer.data)


@api_view(['GET'])

def contactallshortbycompanyid(request, comp_id,name,branch_id):

    vendors = VendorTds.objects.filter(company_id=comp_id,
                                        branch_id=branch_id,
                                        vendor_name__icontains=name)[:5]
    serializer1 = WholeVendorJournalSerializer(vendors, many=True)
    customer = CustomerTcs.objects.filter(company_id=comp_id,
                                          branch_id=branch_id,
                                          customer_name__icontains=name)[:5]

    serializer2 = WholeCustomerJournalSerializer(customer, many=True)
    lst = serializer1.data + serializer2.data
    return Response(lst)

@api_view(['GET'])
#
def getvendorshortpaginationbycompanyid(request, comp_id,branch_id):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": Vendor.objects.filter(branch_id=branch_id,company_id=comp_id).count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        items = Vendor.objects.filter(company_id=comp_id,branch_id=branch_id).order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = ForPaginationvendorshortbycompanySerializer(items, many=True).data
    return Response(response)







# @api_view(['GET'])
#
# def getvendorshortpaginationbycompanyid(request, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     vendor = Vendor.objects.filter(company_id=company)
#     serializer = vendorshortbycompanySerializer(vendor, many=True)
#     return Response(serializer.data)




# getvendorbyname


@api_view(['GET'])

def vendorname(request):
    vendor = Vendor.objects.all()
    serializer = vendornameSerializer(vendor, many=True)
    return Response(serializer.data)


@api_view(['POST'])

def vendorUpdate(request, pk):
    vendor = Vendor.objects.get(vendor_id=pk)
    serializer = VendorSerializer(instance=vendor, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['GET'])

def billbyvendorid(request, pk):
    vendor = Vendor.objects.get(vendor_id=pk)
    print('vendor', vendor)
    serializer = BillbyVendorSerializer(vendor, many=False)
    return Response(serializer.data)

@api_view(['GET'])

def getexcessamountpaymentbyvendorid(request,pk):
   queryset = Vendor.objects.get(pk=pk)
   serializer=VendorExAmountSerializer(queryset)
   return Response(serializer.data)
@api_view(['GET'])

def getvendorpaymentrefbyvendorid(request,pk):
   queryset = Vendor.objects.get(pk=pk)
   serializer=VendorpaymenttrefSerializer(queryset)
   return Response(serializer.data)	  



@api_view(['GET'])

def getdebitnotebyvendorid(request,pk):
   queryset = Vendor.objects.get(pk=pk)
   serializer=VendorDebitNoteRefSerializer(queryset)
   return Response(serializer.data)	


class VendorUpdtViewset(viewsets.ModelViewSet):
    queryset=Vendor.objects.all()
    serializer_class=VendorSerializer


    @transaction.atomic
    def handle_update(self, vendor_data, pk):

        print(" REQUEST DATA",vendor_data)
       

        try:
            vendor = Vendor.objects.select_for_update().get(vendor_id=pk)
        except Vendor.DoesNotExist:
            pass

        vn_serializers = VendorSerializerUpdate(vendor, data=vendor_data)

        if vn_serializers.is_valid():
                vn_serializers.save()
                msg="Details Updated Successfully" 
                return Response(vn_serializers.data,status=200)
        else:
                return Response(vn_serializers.errors, status=400)

    def update(self,request,pk):
        vendor_data = request.data
        return self.handle_update(vendor_data,pk)

from coa.models import TransactionDetailCV
from coa.serializers import TransactionDetailCVSerializer
@api_view(['GET'])
#
def getJRNLTransbyVENDORID(request,from_to_id):
        objs = TransactionDetailCV.objects.filter(vendor_id=from_to_id)
        print(objs)
        serializer = TransactionDetailCVSerializer(objs, many=True)
        return Response(serializer.data, status=200)
        print("from_to_id",from_to_id)
        # Fetch transactions where 'from_acc_subhead' is 'Account Receivables'
        from_mast = MasterTransaction.objects.filter(vendor_id=from_to_id,from_acc_subhead='Account Payables')

        print('@@@@@@',MasterTransaction.customer_id)
        to_mast = MasterTransaction.objects.filter(vendor_id=from_to_id,to_acc_subhead='Account Payables')
        all_transactions = from_mast | to_mast
        if  len(from_mast) > 0 :      
            from_df = pd.DataFrame(from_mast.values('L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                                'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit','transc_deatils','trans_date','trans_status'))
            print("111111111111111111111111111 from df",from_df)
            from_acc = from_df.groupby(['L1detail_id','from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name','transc_deatils','trans_date','trans_status',]).agg(
            {'credit': 'sum'}).reset_index()
            from_acc = from_acc.rename(columns={'L1detail_id':'L1detail_id',
                                    'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name','transc_deatils':'transc_deatils','trans_date':'trans_date','trans_status':'trans_status'}, inplace=False)
            print("***************************************** from_acc",from_acc)
            # Filter only positive credit values
            from_acc = from_acc.loc[from_acc['credit'] > 0]
        else:
            from_acc = None

        if len(to_mast) > 0:
            to_df = pd.DataFrame(to_mast.values('L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                                'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit','transc_deatils','trans_date','trans_status'))
            print("111111111111111111111111111 from df", to_df)
            to_acc = to_df.groupby(['L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name','transc_deatils','trans_date','trans_status',]).agg(
                { 'debit': 'sum'}).reset_index()
            to_acc = to_acc.rename(columns={'L1detail_id':'L1detail_id',
                                    'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name','transc_deatils':'transc_deatils','trans_date':'trans_date','trans_status':'trans_status'}, inplace=False)
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
            return Response("Data not found") 
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
        return Response(all_response) 



# Get search details by customer name 
@api_view(['GET'])

def getVendorDetailsByVendorName(request, vendor_name,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    vendors = Vendor.objects.filter(company_id=company_id,branch_id=branch_id,vendor_name__icontains=vendor_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": vendors.count()}
    
    instance = vendors[offset:offset + limit]
    serializer = VendorSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)


# Get Vendor details by vendor mobile number 
@api_view(['GET'])

def getVendorDetailsByVendorContact(request, vendor_mobile,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    vendors = Vendor.objects.filter(company_id=company_id,
                                    branch_id=branch_id,
                                    vendor_mobile__icontains=vendor_mobile)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Vendor.objects.count()}
    
    instance = vendors[offset:offset + limit]
    serializer = VendorSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)