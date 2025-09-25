from rest_framework import serializers
from banking.models.interest_income_model import InterestIncome

#Interest Income Serializer
class InterestIncomeSerialiser(serializers.ModelSerializer):
    class Meta:
        model=InterestIncome
        fields= '__all__'