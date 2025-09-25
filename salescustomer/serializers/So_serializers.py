from rest_framework import serializers

from salescustomer.models.So_model import SO

from .So_item_serializers import SOItemSerializer

class SOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SO
        fields = '__all__'
        depth=1



class ShortSalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SO
        fields = ['so_id', 'total', 'so_date', 'so_ref_no', 'so_serial', 'customer_id', 'so_status', 'company_id',
                  'branch_id']
        depth = 1



class JoinSoItemSerializer(serializers.ModelSerializer):
    so_items = SOItemSerializer(many=True)

    class Meta:
        model = SO
        fields = '__all__'
        depth = 1




class SOUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=SO
        fields='__all__'
        
        
class UpdtJoinSoItemSerializer(serializers.ModelSerializer):
    so_items = SOItemSerializer(many=True)

    class Meta:
        model = SO
        fields = '__all__'


class SalesOrderSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = SO
        exclude = ['attach_file']
        
        
class SalesOrderShortByCompany_idSerializer(serializers.ModelSerializer):
    class Meta:
        model = SO
        exclude = ['attach_file']
        depth=1

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['so_items'] = SOItemSerializer(instance.so_items.all(),many=True).data
        return representation