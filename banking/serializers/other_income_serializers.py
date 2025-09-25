from rest_framework import serializers
from banking.models.other_income_model import OtherIncome

# Other Income Serializer
class OtherIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=OtherIncome
        fields= '__all__'
