
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from salescustomer.models import RI
from salescustomer.serializers.Recurring_invoice import RISerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes




# API for Recurring Invoice
@api_view(['GET'])


def riCreation(request):
    ri = RI.objects.all()
    serializer = RISerializer(ri, many=True)
    return Response(serializer.data)


@api_view(['GET'])


def riDetail(request, pk):
    ri = RI.objects.get(id=pk)
    serializer = RISerializer(ri, many=False)
    return Response(serializer.data)


@api_view(['POST'])


def riUpdate(request, pk):
    ri = RI.objects.get(id=pk)
    serializer = RISerializer(instance=ri, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

