from rest_framework.decorators import api_view
from rest_framework.response import Response
from salescustomer.models.Customerob_model import CustomerOB
from salescustomer.serializers.Customerob_serializers import CustomerObSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes

# opening balance for customer
@api_view(['PUT'])


def customerobUpdate(request, pk):
    openingbalance = CustomerOB.objects.get(ob_id=pk)
    serializer = CustomerObSerializer(
        instance=openingbalance, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)