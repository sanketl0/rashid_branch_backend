from rest_framework import serializers
from purchase.models.Vendor_contact_model import VendorContact

class VendorContactSerializer(serializers.ModelSerializer):     
    class Meta:   
        model = VendorContact
        fields= '__all__'  