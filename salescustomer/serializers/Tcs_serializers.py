from rest_framework import serializers
from salescustomer.models.Tcs_model import TCS


class tcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCS
        fields = '__all__'

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = f"{instance.tax_name} {instance.rate}%"
        representation['value'] = instance.tcs_id
        return representation