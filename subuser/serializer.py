from registration.models import user,UserAccess
from rest_framework import serializers

class UserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccess
        exclude = ['id','user']

class SubUserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['name','email','role','mobile_no']

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['role_details'] = UserAccessSerializer(instance.user_access.all()[0]).data
        return representation
