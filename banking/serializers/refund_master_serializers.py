from rest_framework import serializers 
from banking.models.refund_master_model import RefundMaster



# credit note refund transaction
class Refund_Serializer(serializers.ModelSerializer):
    class Meta:
        model=RefundMaster
        fields= '__all__'

