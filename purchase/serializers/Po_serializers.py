from rest_framework import serializers
from purchase.models.Po_model import PO
from .Poitem_serializers import POItemSerializer,POItemSerializerGet
class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PO
        fields = '__all__'
        depth=1
        
        
class purchaseordershortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PO
        fields = ['po_id','total','expected_delivery_date','po_date','po_ref_no','po_serial','customer_id','po_status','vendor_id']
        depth=1
        
class JoinPoItemSerializer(serializers.ModelSerializer):
    po_items = POItemSerializerGet(many=True)
    class Meta:
        model = PO
        fields = '__all__'
        depth=1



class UpdtPOserializer(serializers.ModelSerializer):
    class Meta:
        model= PO
        fields='__all__'
        
        
class UpdatePOSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = PO
        exclude = ('attach_file', )
