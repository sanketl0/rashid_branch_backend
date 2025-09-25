from rest_framework import serializers
from salescustomer.models.Employee_model import Employee

class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'



class employeeAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = []
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = instance.emp_name
        representation['value'] = instance.emp_id
        return representation