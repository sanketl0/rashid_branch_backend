from rest_framework import serializers
from banking.models.customer_payment_model import CustomerPayment

class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerPayment
        fields='__all__'