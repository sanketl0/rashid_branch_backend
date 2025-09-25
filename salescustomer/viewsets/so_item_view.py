from rest_framework import viewsets,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from salescustomer.models.So_item_model import SoItem
from salescustomer.serializers import SoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

#Sales Order Return The All Sales Order Item
class soitemViewSet(viewsets.ModelViewSet):
    queryset = SoItem.objects.all()
    serializer_class = SoItemSerializer

    

#Sales Order Item Featch the All data
class soitemList(generics.ListAPIView):
    queryset = SoItem.objects.all()
    serializer_class = SoItemSerializer

    
    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def soitemCreation(request):
        soitem = SoItem.objects.all()
        serializer = SoItemSerializer(soitem, many=True)
        return Response(serializer.data)
