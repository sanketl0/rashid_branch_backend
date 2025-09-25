from rest_framework import serializers
from salescustomer.models.Estimated_item_model import EstimatedItem


class EstimateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimatedItem
        fields = '__all__'
        
        
class EstItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimatedItem
        fields = ['est_id', 'estitem_id', 'item_name','item_id','amount', 'quantity', 'rate', 'tax_name', 'taxamount',
                  'igst_amount', 'cgst_amount', 'sgst_amount','coa_id']





        
        
class EstimatedITEMSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = EstimatedItem
        fields = '__all__'
        

class EstimatedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimatedItem
        fields = '__all__'
        # depth = 1