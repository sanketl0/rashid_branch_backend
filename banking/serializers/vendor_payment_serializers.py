from rest_framework import serializers
from banking.models.vendor_payment_model import VendorPayment


class VendorPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorPayment
        fields= '__all__'
