from rest_framework import serializers
from integration.models import *
import uuid

class TaskSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self,instance):
        ret = super().to_representation(instance)
        if instance.branch_id:
            ret['branch_name'] = f"{instance.company_id.company_name} => {instance.branch_id.branch_name}"
        return ret


class TaskLogSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = TaskLogs
        fields = '__all__'

class ItemBatchSerializer(serializers.Serializer):
    item_id = serializers.UUIDField( required=True)  # UUID field, required
    batch_no = serializers.CharField(max_length=100, required=True)  # Batch number, required
    expire_date = serializers.DateField(required=True)  # Expiry date, required
    mfg_date = serializers.DateField(required=True)  # Manufacturing date, required
    branch_id = serializers.UUIDField(required=True)
    company_id = serializers.UUIDField( required=True)



class VersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = VersionHelper
        fields = ['version','file']
