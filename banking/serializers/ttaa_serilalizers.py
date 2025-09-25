from rest_framework import serializers
from banking.models.ttaa_model import TTAA

# Transfer To Another Account Serializers
class TransferToAnotherAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=TTAA
        fields='__all__' 
