from rest_framework import serializers
from item.models.adjustment_item_model import AdjustmentItem


#Adjustment Item means item Quntity an And Value Adjust mented are used Item Adjustment Section
class AdjustmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjustmentItem
        fields = '__all__'

    def to_representation(self,instance):
        representation = super().to_representation(instance)

        btch = []
        try:
            btch = eval(instance.batch_no)
        except:
            pass
        representation['batches'] = btch
        return representation