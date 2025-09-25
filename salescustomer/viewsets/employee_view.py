from rest_framework import viewsets,generics
from rest_framework.decorators import api_view
from salescustomer.models.Employee_model import Employee
from salescustomer.serializers.Employee_serializers import employeeAllSerializer,employeeSerializer
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes


#Employee Model To retruns all Objects
class employeeViewSet(
        viewsets.ModelViewSet):  # provision to add data from API by providing HTML form also we can see posted data
    queryset = Employee.objects.all()
    serializer_class = employeeSerializer

 

#Class Base Function Api To return the Function
class employeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = employeeSerializer

    
    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def employeeCreation(request,comp_id=None):
        employee = Employee.objects.filter(company_id=comp_id)
        serializer = employeeSerializer(employee, many=True)
        return Response(serializer.data)

@api_view(['GET'])

def employeeAllList(request,comp_id,branch_id):
    customer = Employee.objects.filter(company_id=comp_id,branch_id=branch_id)
    serializer = employeeAllSerializer(customer, many=True)
    return Response(serializer.data)