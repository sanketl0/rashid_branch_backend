import imp
from rest_framework import serializers
from item.models.adjustment_model import Adjustment
from item.serializers.adjustment_item_serializers import AdjustmentItemSerializer


class JoinAdjustmentAndAdjustItemSerializer(serializers.ModelSerializer):
    adj_items = AdjustmentItemSerializer(many=True)

    class Meta:
        model = Adjustment
        fields = '__all__'


class AdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjustment
        fields = '__all__'
        depth=1
        


class AdjustmentSerializerForShortView(serializers.ModelSerializer):
    class Meta:
        model = Adjustment
        fields = ['adj_date', 'adj_type', 'reason', 'status','ref_no','rate', 'adj_id']