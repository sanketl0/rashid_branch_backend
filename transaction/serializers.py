from rest_framework import serializers

from .models import *

class MasterTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTransaction
        fields = '__all__'


class MasterTransactionBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTransaction
        fields = ['L1detail_id','transc_deatils','trans_status','credit','debit','trans_date']
    def __init__(self, *args, **kwargs):
        # Extract and remove the custom argument from kwargs
        self.account = str(kwargs.pop('account', None))
        # Call the parent's __init__ method with the remaining kwargs
        super(MasterTransactionBankSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)

        if self.account == instance.to_account:
            representation['credit'] = 0
        else:
            representation['debit'] = 0

        return representation

"Vendor Payment"
class ChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        fields = '__all__'

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)

        representation['label'] = instance.charge_name
        representation['value'] = instance.chg_id
        return representation



class ChargeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeTransaction
        fields = '__all__'

class CoaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoaCharges
        fields = ['amount','coa_id','coa_name','name','charges_type']