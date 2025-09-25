from rest_framework import viewsets,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from salescustomer.models.Paymentmode_model import PaymentMode
from salescustomer.serializers.Paymentmode_serializers import paymentmodeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
# Payment mode retun the All opbject in in Tabel
class paymentmodeViewSet(viewsets.ModelViewSet):
    queryset = PaymentMode.objects.all()
    serializer_class = paymentmodeSerializer

    

class paymentmodeList(generics.ListAPIView):
    queryset = PaymentMode.objects.all()
    serializer_class = paymentmodeSerializer

    
    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def paymentmodeCreation(self,request,comp_id=None):
        paymentmode = PaymentMode.objects.filter(company_id=comp_id)
        print(paymentmode,comp_id)
        serializer = paymentmodeSerializer(paymentmode, many=True)
        return Response(serializer.data)

class paymentModeView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self,request,comp_id=None,branch_id=None):
        paymentmode = PaymentMode.objects.filter(company_id=comp_id,branch_id=branch_id)
        print(paymentmode, comp_id)
        serializer = paymentmodeSerializer(paymentmode, many=True)
        return Response(serializer.data)