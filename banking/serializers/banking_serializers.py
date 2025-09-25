from rest_framework import serializers
from banking.models.banking_model import Banking


class BankingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banking
        fields='__all__'

# GET Short By Company id
class BankCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Banking
        fields=['coa_id','bank_id','bank_name','account_type','account_name','bank_name','account_code','ifsc_code']

