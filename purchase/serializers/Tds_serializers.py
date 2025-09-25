from rest_framework import serializers
from purchase.models.Tds_model import TDS
class tdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TDS
        fields = '__all__'

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = f"{instance.tax_name} {instance.rate}%"
        representation['value'] = instance.tds_id
        return representation