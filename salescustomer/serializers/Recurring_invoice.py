from rest_framework import serializers
from salescustomer.models.Recurringinvoice_model import RI


class RISerializer(serializers.ModelSerializer):
    class Meta:
        model = RI
        fields = '__all__'