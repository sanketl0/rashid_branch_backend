from rest_framework import serializers
from banking.models.dfoa_model import DFOA


class DFOASerializer(serializers.ModelSerializer):
    class Meta:
        model=DFOA
        fields='__all__'
