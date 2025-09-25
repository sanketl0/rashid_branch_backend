from rest_framework import serializers

from salescustomer.models.Estimate_model import Estimate
from .Estimated_item_serializers import EstimateItemSerializer,EstItemSerializer


class EstimateNewSerializer(serializers.ModelSerializer):
    estimate_items = EstimateItemSerializer(many=True)
    class Meta:
        model = Estimate
        fields = '__all__'

    def create(self,validated_data):
        print(validated_data['estimated_items'])




class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = '__all__'
        depth=1

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['estimated_items'] = EstimateItemSerializer(instance.estimate_items.all(),many=True).data
        return representation





class ShortEstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = ['est_date', 'est_ref_no', 'est_serial', 'customer_id', 'est_status', 'total', 'amount', 'tcs_amount',
                  'est_id', 'company_id', 'branch_id']
        depth = 1
        
        
        
class JoinItemSerializer(serializers.ModelSerializer):
    estimate_items = EstimateItemSerializer(many=True)

    class Meta:
        model = Estimate
        fields = '__all__'
        # fields = ['est_id','est_no','estimate_items']


class EstimateSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = '__all__'

class EstimateSerializerUpdateGet(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        exclude = ['attach_file']
        
class UpDtEstimateSerializer(serializers.ModelSerializer):
    estimate_items = EstItemSerializer(many=True)
    class Meta:
        model = Estimate
        fields = '__all__'
        
class JoinEstimateItemSerializer(serializers.ModelSerializer):
    estimate_items = EstItemSerializer(many=True)

    class Meta:
        model = Estimate
        fields = '__all__'
        depth = 1
        
        
class GetestimateShortbycompany_idEstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = ['est_date', 'est_ref_no', 'est_serial', 'customer_name', 'est_status', 'total', 
                  'est_id', 'is_converted']
        
        #est_date, est_ref_no, est_serial, customer_name, est_status, is_converted, total, est_id
from salescustomer.models.Salescustomer_model import SalesCustomer 
from salescustomer.serializers.Salescustomer_serializers import SalesCustomerSerializer    
class PropertyDetailSerializer(serializers.ModelSerializer):
    comapny=SalesCustomerSerializer()
    class Meta:
        model = Estimate
        fields = '__all__'