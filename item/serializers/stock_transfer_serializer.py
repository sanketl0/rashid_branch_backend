from rest_framework import serializers
from item.models.stock_transfer_model import StockTransfer,StockTransferTransaction

class StockTransferTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransferTransaction
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        representation['primary_branch_name'] = instance.primary_branch.branch_name
        representation['secondary_branch_name'] = instance.secondary_branch.branch_name
        representation['item_name'] = instance.item_id.name
        representation['batches'] = eval(instance.batches)
        representation['sec_batches'] = eval(instance.sec_batches)
        return representation


class StockTransferSerializer(serializers.ModelSerializer):
    stock_transactions = StockTransferTransactionSerializer(many=True)

    class Meta:
        model = StockTransfer
        fields = '__all__'

class StockPostTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockTransfer
        fields = '__all__'


class StockTransferGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockTransfer
        fields = '__all__'
