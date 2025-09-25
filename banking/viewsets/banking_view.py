
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import api_view
from company.models import Company,Branch
from coa.models import COA
from banking.models.banking_model import Banking
from ..serializers.banking_serializers import BankingSerializer,BankCompanySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.db import transaction
from registration.models import Feature
from report.models import AccountBalance
from report.serializers import AccountBalanceSerializer
#region
class getallbanks(generics.ListAPIView):
    queryset = Banking.objects.all()
    serializer_class =  BankingSerializer

    # # permission_classes=[IsAuthenticated]





class BankingViewsets(viewsets.ModelViewSet):
    queryset = Banking.objects.all()
    serializer_class = BankingSerializer


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        count = Feature.objects.get(user_id=request.user.id).bank_remaining
        print(count, 'banks')
        if count <= 0:
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)

        bank_data = request.data

        #Branch ID request Are Null
        branch_id=bank_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)
        #Creating Banking
        comp_id=Company.objects.get(company_id=bank_data["company_id"])
        account_type=bank_data["account_type"]
        global coa_id #Global Declaration Variable For using Outside if elif
        
        ## Creat the COA ID first so that we can add theCOA id in to the bank table
        if(account_type =="Bank"):
            bankcoa =COA.objects.create(
            #coa_id=bank_id,
            account_name=bank_data["account_name"],
            account_code=bank_data["account_code"],
            account_head="Current Assets",
            account_subhead="Bank",
            company_id=comp_id,
            account_type="Assets")
            bankcoa.save() 
            coa_id= bankcoa.coa_id
            
            # Select The Credit Card Option to Call this Section
        elif(account_type =="Credit Card"):
            bankcoa =COA.objects.create(
            
            account_name=bank_data["account_name"],
            account_code=bank_data["account_code"],
            account_type="Liabilities",
            account_head="Current Liabilities",
            account_subhead="Credit Card",
            company_id=comp_id)
            
            bankcoa.save() 
            #chatrted Account Addded
            coa_id= bankcoa.coa_id

            
        
        bank_id=Banking.objects.create(
        account_code=bank_data["account_code"],
        account_name=bank_data["account_name"],
        account_number=bank_data["account_number"],
        account_type=bank_data["account_type"],
        bank_name=bank_data["bank_name"],
        #status=bank_data["status"],
        branch_id=branch_id,
        company_id=comp_id,
        description=bank_data["description"],
        ifsc_code=bank_data["ifsc_code"],        
        coa_id=COA.objects.get(coa_id=coa_id))
        
        bank_id.save()  
       #Bank Created
        
        serializer = BankingSerializer(bank_id)
        return Response(serializer.data)
  


# get bankshortbycompanyid
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getbankshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    objs = Banking.objects.filter(company_id=comp_id,branch_id=branch_id)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": objs.count()
    }
    
    try:

        bank = objs.order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company Does Not Exist")
    response['results'] = BankCompanySerializer(bank, many=True).data
    return Response(response)


@api_view(['GET'])

def getBankByIdView(request, pk=None):
    # Get the 'limit' and 'offset' parameters from the query string
    if pk:
        obj = AccountBalance.objects.get(coa_id=pk)
        response = AccountBalanceSerializer(obj).data
    return Response(response,status=200)

@api_view(['GET'])
@renderer_classes([JSONRenderer])

def getBKDetailsByaccount_name(request, comp_id,name,branch_id):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    banks = Banking.objects.filter(company_id=comp_id,
                                   branch_id=branch_id,
                                   account_name__icontains=name)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": banks.count()
    }
    bank = banks[offset:offset + limit]
    response['results'] = BankCompanySerializer(bank, many=True).data
    return Response(response)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getBKDetailsByaccount_type(request, comp_id,account_type,branch_id):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    banks = Banking.objects.filter(company_id=comp_id,
                                   branch_id=branch_id,
                                   account_type__icontains=account_type)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": Banking.objects.count()
    }
    bank = banks[offset:offset + limit]
    response['results'] = BankCompanySerializer(bank, many=True).data
    return Response(response)
###################################################
#endregion