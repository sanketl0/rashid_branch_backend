from rest_framework import serializers

from salescustomer.models.Dc_model import DC
from .Dc_item_serializers import DcItemSerializer
from .Dc_item_serializers import DcItemSerializer
class DCSerializer(serializers.ModelSerializer):
    dc_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = DC
        fields = '__all__'
        depth=1
        
        
        
class ShortDeliveryChallanSerializer(serializers.ModelSerializer):
    dc_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = DC
        fields = ['dc_id', 'total', 'dc_date', 'dc_ref_no', 'dc_serial', 'customer_id', 'dc_status', 'company_id',
                  'branch_id']
        depth = 1
        
class dcshortbycompanySerializer(serializers.ModelSerializer):
    dc_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = DC
        exclude = ['attach_file']
        depth = 1
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['dc_items'] = DcItemSerializer(instance.dc_items.all(),many=True).data
        return representation

class JoinDcItemSerializer(serializers.ModelSerializer):
    dc_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    dc_items = DcItemSerializer(many=True)

    class Meta:
        model = DC
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)


        return representation



class UpdtDcItemSerializer(serializers.ModelSerializer):
    dc_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    dc_items = DcItemSerializer(many=True)

    class Meta:
        model = DC
        fields = '__all__'
        
        
class DeliveryChalanSerializerUpdate(serializers.ModelSerializer):
    dc_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = DC
        exclude = ['attach_file']