from rest_framework import serializers
from banking.models.expense_refund_model import ExpenseRefund

class ExpenseRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExpenseRefund
        fields= '__all__'
