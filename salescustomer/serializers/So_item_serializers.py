from rest_framework import serializers

from salescustomer.models.So_item_model import SoItem



class SoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoItem
        fields = '__all__'
        
        
        
        
        
class SOItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoItem
        fields = ['so_id', 'soitem_id', 'item_name', 'amount', 'quantity', 'rate', 'tax_name', 'taxamount',
                  'cgst_amount', 'sgst_amount', 'igst_amount','item_id','coa_id','tax_type','tax_rate']
        
        
class SOITEMSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = SoItem
        fields = '__all__'
        
        
class SOITEMSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = SoItem
        fields = '__all__'