import json

from django.http import HttpResponse, FileResponse

from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from purchase.models.Paymentmade_model import PaymentMade
from purchase.serializers .Paymentmade_serializers import PaymentmadeSerializerPost
from company.models import Company,Company_Year,Branch
from purchase.models.Vendor_model import Vendor
from coa .models import COA
from transaction .models import MasterTransaction
from purchase.models.Bill_model import Bill
from purchase.serializers.Paymentmade_serializers import PaymentmadeSerializer,paymentmadeshortbycompanySerializer,UpdtPaymentmadeSerializer,ForPaginationpaymentmadeshortbycompanySerializer
from purchase.printing.generate_pm import generate_payment_made_pdf
from audit.models import Audit
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from purchase.models.Multiple_bill_model import Multiple_Bill_Details
from django.db import transaction

class PaymentmadeJournalViewsets(viewsets.ModelViewSet):
    queryset = PaymentMade.objects.all()  # get the Paymentmade Model Data
    serializer_class = PaymentmadeSerializer

    # payment made field
    def create(self, request, *args, **kwargs):
        paymentmade_data = request.data
        user = request.user
        return self.handle_post(user,paymentmade_data)

    @transaction.atomic
    def handle_post(self, user,paymentmade_data):
        # count = Feature.objects.get(user_id=request.user.id).pm_remaining
        # print(count, 'payment made')
        # if count <= 0:
        #     return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)

        print('paymentmade_data', paymentmade_data)
        bill_id = paymentmade_data["bill_id"]
        bill_amount = paymentmade_data["bill_amount"]
        print("bill_amount", bill_amount)
        # bill_id=paymentmade_data["unpainBill"]["bill_id"]
        print("bill_id", bill_id, type(bill_id))
        company_id = Company.objects.get(
            company_id=paymentmade_data["company_id"])
        branch_id =  Branch.objects.get(
            branch_id=paymentmade_data["branch_id"])
        print('@@@',paymentmade_data)
        vendor_id = paymentmade_data["vendor_id"]
        if vendor_id:
            vendor_id = Vendor.objects.get(vendor_id=vendor_id)
        # Payment made field
        pm_serializer = PaymentmadeSerializerPost(data=paymentmade_data)
        if pm_serializer.is_valid():
            print(pm_serializer.validated_data)

            payment_id = pm_serializer.save()

            payment_id.save()
        else:
            print(pm_serializer.errors)
            return Response(pm_serializer.errors,status=400)
        print(pm_serializer.data)
        party_account = paymentmade_data.get('party_account', None)
        try:
            account_payable = COA.objects.get(coa_id=party_account)
        except:
            if vendor_id:
                account_payable = vendor_id.coa_id
            else:
                account_payable = COA.get_account_paybles(company_id)
        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=paymentmade_data["payment_date"],
            module="PaymentMade",
            sub_module='PaymentMade',
            data=paymentmade_data
        )

        From_Bank = COA.objects.get(coa_id=paymentmade_data["paid_through"])
        pmmast = MasterTransaction.objects.create(
            L1detail_id=payment_id.pm_id,
            L1detailstbl_name='Payment Made',
            L3detail_id=bill_id,
            L3detailstbl_name='Bill',
            main_module='Purchase',
            module='Purchase',
            sub_module='Payment Made',
            transc_deatils='Payment Made',
            banking_module_type='Vendor Payment',
            journal_module_type='Payment Made',
            trans_date=paymentmade_data["payment_date"],
            trans_status='Maually Added',
            debit=paymentmade_data["amount_payable"],
            to_account=account_payable.coa_id,
            to_acc_type=account_payable.account_type,
            to_acc_head=account_payable.account_head,
            to_acc_subhead=account_payable.account_subhead,
            to_acc_name=account_payable.account_name,
            credit=paymentmade_data['amount_payable'],
            from_account=From_Bank.coa_id,
            from_acc_type=From_Bank.account_type,
            from_acc_head=From_Bank.account_head,
            from_acc_subhead=From_Bank.account_subhead,
            from_acc_name=From_Bank.account_name,
            vendor_id=vendor_id,
            branch_id=branch_id,
            company_id=company_id)
        pmmast.save()

# endregion

        # for full payment
        bill_amount = paymentmade_data["bill_amount"]
        print("bill_amount", bill_amount, type(bill_amount))
        amount_payable = paymentmade_data["amount_payable"]
        print("amount_payable", amount_payable, type(amount_payable))

        # If payment is full then payment status will change unpaid to paid in Bill
        balance_amount = float(paymentmade_data["balance_amount"])
        # if bill_amount == balance_amount:
        print(paymentmade_data['bill_id'])
        bill_id = Bill.objects.get(
            bill_id=paymentmade_data["bill_id"])
        bill_id.amount_due = balance_amount
        if balance_amount <= 0:
            bill_id.payment_status = 'paid'
        bill_id.save()

        serializer = PaymentmadeSerializer(payment_id)
        return Response(serializer.data,status=201)







class PaymentmadeViewstes(viewsets.ModelViewSet):
    queryset = PaymentMade.objects.all()
    serializer_class = PaymentmadeSerializer

# get all payment made list


class paymentmadedList(generics.ListAPIView):
    queryset = PaymentMade.objects.all()
    serializer_class = PaymentmadeSerializer

# get Paymentmadebyid


@api_view(['GET'])

def getpaymentmade(request, pk):
    instance = PaymentMade.objects.get(pk=pk)
    serializer = PaymentmadeSerializer(instance)
    return Response(serializer.data)




# get payment made short by company id


@api_view(['GET'])
#
def getpaymentmadeshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    objs = PaymentMade.objects.filter(company_id=comp_id,branch_id=branch_id)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": objs.count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        items = objs.order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = ForPaginationpaymentmadeshortbycompanySerializer(items, many=True).data
    return Response(response)
    
    

# get bill by vendor id(Response for this api is its return all bill as per respective  vendor)

###############################################################3##########################



# api for get bill by company id and bill id
@api_view(['GET'])

def download_pm_data(request,pm_id):

    paymt = PaymentMade.objects.select_related('vendor_id','company_id').get(pm_id=pm_id)
    serializers = paymentmadeshortbycompanySerializer(paymt)

    html = generate_payment_made_pdf(data=serializers.data)
    return html

def download_pm(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response





#Update the Payment Made Data
from rest_framework.views import APIView
from django.db.models import Q
class UpdtPaymentMadeViewset(APIView):
    # queryset = PaymentMade.objects.all()
    # serializer_class=UpdtPaymentmadeSerializer

    def put(self, request, pk, *args, **kwargs):
        pm_data = request.data
        user = request.user
        return self.handle_update(user,pm_data,pk)

    @transaction.atomic
    def handle_update(self,user, pm_data, pk):

        pm = PaymentMade.objects.select_for_update().get(pm_id=pk)
        MasterTransaction.objects.select_for_update().filter(L1detail_id=pk).delete()
        vendor_id = None
        if pm_data["vendor_id"]:
            vendor_id=Vendor.objects.select_for_update().get(vendor_id=pm_data["vendor_id"])
        company_id = Company.objects.get(
            company_id=pm_data["company_id"])
        branch_id = Branch.objects.get(
            branch_id=pm_data["branch_id"])
        serializer = UpdtPaymentmadeSerializer(pm, data=pm_data)
        if serializer.is_valid():
            pm_id = serializer.save()
            msg="Details Updated Successfully"           
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        Audit.objects.create(
            company_id=pm.company_id,
            branch_id=pm.branch_id,
            modified_by=user,
            audit_modified_date=pm_data["payment_date"],
            module="PaymentMade",
            sub_module='PaymentMade',
            data=pm_data
        )
        party_account = pm_data.get('party_account', None)
        try:
            account_payable = COA.objects.get(coa_id=party_account)
        except:
            if vendor_id:
                account_payable = vendor_id.coa_id
            else:
                account_payable = COA.get_account_paybles(company_id)
        From_Bank = COA.objects.get(coa_id=pm_data["paid_through"])
        bill_id = pm_data["bill_id"]
        pmmast = MasterTransaction.objects.create(
            L1detail_id=pm_id.pm_id,
            L1detailstbl_name='Payment Made',
            L3detail_id=bill_id,
            L3detailstbl_name='Bill',
            main_module='Purchase',
            module='Purchase',
            sub_module='Payment Made',
            transc_deatils='Payment Made',
            banking_module_type='Vendor Payment',
            journal_module_type='Payment Made',
            trans_date=pm_data["payment_date"],
            trans_status='Maually Added',
            debit=pm_data["amount_payable"],
            to_account=account_payable.coa_id,
            to_acc_type=account_payable.account_type,
            to_acc_head=account_payable.account_head,
            to_acc_subhead=account_payable.account_subhead,
            to_acc_name=account_payable.account_name,
            credit=pm_data['amount_payable'],
            from_account=From_Bank.coa_id,
            from_acc_type=From_Bank.account_type,
            from_acc_head=From_Bank.account_head,
            from_acc_subhead=From_Bank.account_subhead,
            from_acc_name=From_Bank.account_name,
            vendor_id=vendor_id,
            branch_id=branch_id,
            company_id=company_id)
        pmmast.save()
        bill_id = Bill.objects.select_for_update().get(
            bill_id=pm_data["bill_id"])
        balance_amount = float(pm_data["balance_amount"])
        bill_id.amount_due = balance_amount
        if balance_amount <= 0:
            bill_id.payment_status = 'paid'
        else:
            bill_id.payment_status = 'unpaid'
        bill_id.save()
        return Response(serializer.data)

# Multiple Bill Paid at one time update Amount value

# class PaymentmadeJournalViewsets(viewsets.ModelViewSet):
#     queryset = PaymentMade.objects.all()  # get the Paymentmade Model Data
#     serializer_class = PaymentmadeSerializer
    
#     # payment made field
#     def create(self, request, *args, **kwargs):
#         paymentmade_data = request.data
       
#         unpaid_bill = paymentmade_data["unpaidBill"]
#         # Payment made field
#         pm_serializer = PaymentmadeSerializer(data=paymentmade_data)
#         if pm_serializer.is_valid():
#             payment_id = pm_serializer.save()
#             payment_id.save()
#         else:
#             return Response(pm_serializer.errors)
  
  
#         total_amount = paymentmade_data["bill_amount"]
      
#         for i in unpaid_bill:
#             bill = Bill.objects.get(
#                 bill=i)
#             bill.amount=
            
            
            
#             #bill_id.amount_due = paymentmade_data["balance_amount"]
#             if balance_amount == 0:
#                 bill.payment_status = 'paid'
#             billsave()

#         serializer = PaymentmadeSerializer(payment_id)
#         return Response(serializer.data)


           
from purchase.serializers.Bill_serializers import BillItemSerializer,BillSerializer ,BillSerializer1   
class MultipleBill_Paid_At_onetime(viewsets.ModelViewSet):
    queryset = PaymentMade.objects.all()  # get the Paymentmade Model Data
    serializer_class = PaymentmadeSerializer
    
    # payment made field
    def create(self, request, *args, **kwargs):
        paymentmade_data = request.data
        print("request.dats",paymentmade_data)
       # unpaid_bill = paymentmade_data["unpaidBill"]
       
        vendor=paymentmade_data["vendor_id"]
        if vendor is not None:
            vendor=Vendor.objects.get(vendor_id=vendor)
            
        company_id = paymentmade_data["company_id"]
        if company_id is not None:
            company_id = Company.objects.get(company_id=company_id)
            
        company_year_id=paymentmade_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
    
        bill_id=paymentmade_data.get("bill_id")
        if bill_id is not None:
            bill_id=Bill.objects.get(bill_id=bill_id)
        
        
        
        
        
        # Payment made field
        pm_serializer = PaymentmadeSerializer(data=paymentmade_data)
        if pm_serializer.is_valid():
            payment_id = pm_serializer.save()
            payment_id.save()
        else:
            return Response(pm_serializer.errors)

        account_payable =COA.get_account_paybles(company_id)

        for bill in paymentmade_data["multiple_bills"]:
            print("bill in multiple bill",bill)
            multiple_bills = Multiple_Bill_Details.objects.create(
                                                         bill_id=Bill.objects.get(
                                                             bill_id=bill["bill_id"]),
                                                         company_id=Company.objects.get(
                                                             company_id=bill["company_id"]),
                                                         vendor_id=Vendor.objects.get(
                                                             vendor_id=bill["vendor_id"]),
                                                        
                                                         amount=bill["amount"],
                                                         amount_due=bill["amount_due"],
                                                        
                                                         pm_id=payment_id)
            
            multiple_bills.save()
        
       # bill_amount = paymentmade_data["bill_amount"]
        #print("total_amount",bill_main_amount)
      
        bill_id = multiple_bills.bill_id
        print(bill)
        bill_main_amount=multiple_bills.amount
        print('bill main amount',bill_main_amount)
        
        #  bill_id.amount_due = paymentmade_data["balance_amount"]
            
            #if bill_main_amount<bill_main_amount:
        bill_id.payment_status = 'paid'
        print("////////////////",bill_id)
        bill_id.save()
            
        remaing_amount=int(bill_main_amount.split('.')[0])-int(bill_main_amount.split('.')[0])
        print('remaing',remaing_amount)
        total_amount=remaing_amount
            # else:
            #         balance_amount=bill_main_amount-total_amount
            #         bill.amount_due=balance_amount
            #         print('amount_due is here',bill.amount_due)
            #         bill.save()
                
                
        comp_id=Company.objects.get(company_id=paymentmade_data["company_id"])
        account_payable = COA.get_account_paybles(comp_id)
        print('Account PAybale is her @@@@@@@@@@@@',account_payable)
        print('Account  @@@@@@@@@@@@',account_payable.coa_id)
        vendor_id = Vendor.objects.get(vendor_id=paymentmade_data["vendor_id"])
            
        

        company_year_id=paymentmade_data.get("company_year_id")
        if company_year_id is not None:
                    company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        company_id = Company.objects.get(
                    company_id=paymentmade_data["company_id"])
            #From_Bank = COA.objects.get(coa_id=paymentmade_data["paid_through"])
        From_Bank = COA.objects.filter(company_id=company_id, account_subhead='Bank')[0]
        pmmast = MasterTransaction.objects.create(
                    L1detail_id=payment_id.pm_id,
                    L1detailstbl_name='Payment Made',
                # L3detail_id=multiple_bills.bill_id,
                    L3detailstbl_name='Bill',
                    main_module='Purchase',
                    module='Purchase',
                    sub_module='Payment Made',
                    transc_deatils='Payment Made',
                    banking_module_type='Vendor Payment',
                    journal_module_type='Payment Made',
                    trans_date=paymentmade_data["bill_date"],
                    trans_status='Maually Added',
                    debit=bill_main_amount,
                    to_account=account_payable.coa_id,
                    to_acc_type=account_payable.account_type,
                    to_acc_head=account_payable.account_head,
                    to_acc_subhead=account_payable.account_subhead,
                    to_acc_name=account_payable.account_name,
                    credit=bill_main_amount,
                    from_account=From_Bank.coa_id,
                    from_acc_type=From_Bank.account_type,
                    from_acc_head=From_Bank.account_head,
                    from_acc_subhead=From_Bank.account_subhead,
                    from_acc_name=From_Bank.account_name,
                    vendor_id=vendor_id,
                    company_id=company_id)
        pmmast.save()   
                    
                
                    
                    
        serializer =BillSerializer1(bill_id)
        return Response(serializer.data)

           
# Get search details by payment serial
@api_view(['GET'])

def getPMDetailsBypm_serial(request, payment_serial,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    pms = PaymentMade.objects.filter(company_id=company_id,
                                     branch_id=branch_id,
                                     payment_serial__icontains=payment_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": pms.count()}
    
    instance = pms[offset:offset + limit]
    serializer = paymentmadeshortbycompanySerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)


@api_view(['GET'])

def getPMDetailsByvendor_name(request, company_id,vendor_name,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    pms = PaymentMade.objects.filter(company_id=company_id,
                                     branch_id=branch_id,
                                     vendor_id__vendor_name__icontains=vendor_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": pms.count()}

    instance = pms[offset:offset + limit]
    serializer = paymentmadeshortbycompanySerializer(instance, many=True)

    response['results'] = serializer.data
    return Response(response)