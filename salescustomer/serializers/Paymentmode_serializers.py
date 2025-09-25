from rest_framework import serializers

from salescustomer.models.Paymentmode_model import PaymentMode

class paymentmodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = '__all__'