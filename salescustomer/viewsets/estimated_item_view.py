from rest_framework.decorators import api_view
from salescustomer.models.Estimated_item_model import EstimatedItem
from salescustomer.serializers.Estimated_item_serializers import EstItemSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
#Get the estimated Item Details in Est id 
@api_view(['GET'])


def getestimateitembyest_id(request, est_id):
    object = EstimatedItem.objects.filter(est_id=est_id)
    serializer = EstItemSerializer(object, many=True)
    return Response(serializer.data)