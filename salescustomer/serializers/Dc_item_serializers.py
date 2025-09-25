from rest_framework import serializers
from salescustomer.models.Dc_item_model import DcItem

class DcItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcItem
        fields = '__all__'
        
# class DCItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DcItem
#         fields = ['dc_id', 'dcitem_id', 'item_name', 'taxamount', 'amount', 'quantity', 'rate', 'tax_name',
#                   'cgst_amount', 'sgst_amount', 'igst_amount','item_id']
       
       
       
class DCItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcItem
        fields = ['dc_id', 'dcitem_id', 'item_name', 'taxamount', 'amount', 'quantity', 'rate', 'tax_name',
                  'cgst_amount', 'sgst_amount', 'igst_amount','item_id'] 
        
        
class DCITEMSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = DcItem
        fields = '__all__'       
