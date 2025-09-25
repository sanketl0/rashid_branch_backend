from rest_framework import serializers 
from banking.models.customer_advance_model import CustomerAdvance



class CustomerAdvSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerAdvance
        fields='__all__'
        depth=1
        
        
class CustomerAdvancedSerializer(serializers.ModelSerializer):


    class Meta:
        model=CustomerAdvance
        fields='__all__'
        depth=1
        
        
class UpdateCustomerAdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerAdvance
        fields='__all__'
        
        
class GetCustomerShortBy_CompanyidSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerAdvance
        fields=['customer_advance_date',  'customer_advance_ref_no', 'payment_serial', 'customer_id', 
                'ca_id', 'amount_received', 'balance_amount', 'received_via']
        depth=1