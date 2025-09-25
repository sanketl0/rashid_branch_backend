from rest_framework import serializers

from salescustomer.models.Paymentterms_model import PaymentTerms

class PaymentTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTerms
        fields = '__all__'
