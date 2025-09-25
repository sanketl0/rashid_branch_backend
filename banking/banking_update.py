from rest_framework.response import Response
from rest_framework import views, viewsets
from banking.models import CustomerAdvance,VendorAdvanced
from .serializers import UpdateCustomerAdvanceSerializer,UpdateVendorAdvanceSerializer
from salescustomer.models.Salescustomer_model import SalesCustomer
from purchase.models import Vendor
from company.models import Company
from transaction.models import MasterTransaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class CustomerAdvanceViewset(viewsets.ModelViewSet):
    queryset = CustomerAdvance.objects.all()
    serializer_class=UpdateCustomerAdvanceSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def update(self, request, pk, *args, **kwargs):
        ca_data = request.data

        ca = CustomerAdvance.objects.get(ca_id=pk)
        customer_id=SalesCustomer.objects.get(customer_id=ca_data["customer_id"])
        company_id=Company.objects.get(company_id=ca_data['company_id'])


        serializer = UpdateCustomerAdvanceSerializer(ca, data=ca_data)

        if serializer.is_valid():
            serializer.save()
            msg="Details Updated Successfully"
            
        else:
                return Response(serializer.errors, status=400)    

        account_list=MasterTransaction.objects.get(L1detail_id=ca.ca_id)
        account_list.credit=float(ca_data['amount_received'])
        account_list.debit=float(ca_data['amount_received'])
        account_list.save()

        return Response(serializer.data)

        
from django.db import transaction
##############################################################################
class UpdateVendorAdvanceViewset(viewsets.ModelViewSet):
    queryset = VendorAdvanced.objects.all()
    serializer_class=UpdateVendorAdvanceSerializer

    @transaction.atomic
    def update(self, request, pk, *args, **kwargs):
        va_data = request.data
        print("THIS API IS HEATING")
        va = VendorAdvanced.objects.get(va_id=pk)
        print("VA ID",va)
        vendor_id=Vendor.objects.get(vendor_id=va_data["vendor_id"])
        company_id=Company.objects.get(company_id=va_data['company_id'])


        serializer = UpdateVendorAdvanceSerializer(va, data=va_data)
      
        if serializer.is_valid():
            
            serializer.save()
            msg="Details Updated Successfully"
            
        else:
                return Response(serializer.errors, status=400)    

        account_list=MasterTransaction.objects.get(L1detail_id=va.va_id)
        print("account_list",account_list)
        account_list.credit=float(va_data['amount'])
        account_list.debit=float(va_data['amount'])
        account_list.save()

        return Response(serializer.data)

        
############################################################################

