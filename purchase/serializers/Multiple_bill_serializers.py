from rest_framework import serializers
from purchase .models.Multiple_bill_model import Multiple_Bill_Details


class Multiple_bill_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Multiple_Bill_Details
        fields='__all__'
