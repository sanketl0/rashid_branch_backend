from rest_framework import serializers
from statement.models import *


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = instance.name
        representation['value'] = instance.bank_id
        return representation

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['bank_id'] = {"bank_name":instance.bank_id.name}
        representation['date'] = instance.created_date.date()
        status = "COMPLETED"

        if instance.parse and instance.error:
            pass
        elif instance.parse == False and instance.error == False:
            status = "In Progress"
        elif instance.parse == False and instance.error == True:
            status = "FAILED"
        elif instance.parse == True and instance.error == False:
            pass
        representation['status'] = status

        return representation

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = '__all__'