from rest_framework import viewsets,generics
from rest_framework.decorators import api_view
from salescustomer.models.Tcs_model import TCS
from salescustomer.serializers.Tcs_serializers import tcsSerializer
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView


#provision to add data from API by providing HTML form also we can see posted data
class tcsViewSet(
        viewsets.ModelViewSet):  
    queryset = TCS.objects.all()
    serializer_class = tcsSerializer

    

class tcsList(APIView):



    def get(self,request,comp_id,branch_id):
        tcs = TCS.objects.filter(company_id=comp_id,branch_id=branch_id)

        serializer = tcsSerializer(tcs, many=True)
        return Response(serializer.data)

