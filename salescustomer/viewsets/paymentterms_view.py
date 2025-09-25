from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from salescustomer.models.Paymentterms_model import PaymentTerms
from salescustomer.serializers.Paymentterms_serializers import PaymentTermSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

# PAYMENT TERMS
class paymenttermViewSet(
        viewsets.ModelViewSet):  # provision to add data from API by providing HTML form also we can see posted data
    queryset = PaymentTerms.objects.all()
    serializer_class = PaymentTermSerializer

    
    # class paymenttermList(generics.ListAPIView):
    # queryset = PaymentTerms.objects.all()
    # serializer_class = PaymentTermSerializer

    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def paymenttermCreation(self, request,company_id=None):
        if company_id:
            paymentterm = PaymentTerms.objects.filter(company_id=company_id)
            serializer = PaymentTermSerializer(paymentterm, many=True)
            return Response(serializer.data)
        return Response(status=400)

class PaymentTermView(APIView):


    def get(self,request,company_id=None,branch_id=None):
        if company_id:
            paymentterm = PaymentTerms.objects.filter(company_id=company_id,branch_id=branch_id)
            serializer = PaymentTermSerializer(paymentterm, many=True)
            return Response(serializer.data)
        return Response(status=400)