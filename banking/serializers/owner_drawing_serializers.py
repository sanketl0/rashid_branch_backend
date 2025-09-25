from rest_framework import serializers 
from banking.models.owner_drawing_model import OwnerDrawing


class OwnerDrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnerDrawing
        fields= '__all__'