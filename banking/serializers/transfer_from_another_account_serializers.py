from rest_framework import serializers
from banking.models.transfer_from_another_account_model import TransferFromAnotherAccount



class TFAASerializer(serializers.ModelSerializer):
    class Meta:
        model=TransferFromAnotherAccount
        fields='__all__'