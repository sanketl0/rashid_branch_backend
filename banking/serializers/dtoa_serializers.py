from rest_framework import serializers
from banking.models.dtoa_model import DTOA

#DTOA Serializer
class DTOASerializer(serializers.ModelSerializer):
    class Meta:
        model=DTOA
        fields='__all__'