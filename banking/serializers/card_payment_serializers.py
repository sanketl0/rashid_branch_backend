from rest_framework import serializers
from banking.models.card_payment_model import CardPayment

#Card payment Serializer
class CardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CardPayment
        fields='__all__'
        depth=1