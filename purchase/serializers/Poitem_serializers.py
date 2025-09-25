from rest_framework import serializers
from purchase.models.PoItem_model import PoItem
class PoItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = PoItem
        fields = '__all__'
        depth=1
        
class POItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = PoItem        
        fields = ['po_id','poitem_id','item_name','item_id','amount','discount','quantity','rate','coa_id','customer_id','cgst_amount','sgst_amount','igst_amount','tax_name']
        depth=1

class POItemSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = PoItem
        fields = ['po_id','poitem_id','item_name','item_id','amount','discount','quantity','rate','coa_id','customer_id','cgst_amount','sgst_amount','igst_amount','tax_name']


class UpdtPOItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = PoItem        
        fields = ['po_id','poitem_id','item_name','amount','discount','quantity','rate','coa_id','customer_id','cgst_amount','sgst_amount','igst_amount','tax_name']
       