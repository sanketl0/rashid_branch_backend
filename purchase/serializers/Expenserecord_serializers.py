from rest_framework import serializers
from purchase.models.Expense_Record_model import ExpenseRecord
from coa.models import COA
from report.models import AccountBalance
class ExpenseRecordSerializer(serializers.ModelSerializer):
    expense_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = ExpenseRecord
        fields = '__all__'
        depth=1
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)

        # representation['expense_date'] = instance.expense_date.date()
        representation['paid_through_name'] = AccountBalance.objects.get(coa_id=instance.paid_through).label
        representation['balance'] = AccountBalance.objects.get(coa_id=instance.paid_through).balance
        return representation

class ExpenseRecordSerializerDownload(serializers.ModelSerializer):
    expense_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = ExpenseRecord
        fields = '__all__'
        depth=1
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)

        # representation['expense_date'] = instance.expense_date.date()
        representation['paid_through'] = COA.objects.get(coa_id=instance.paid_through).account_name
        return representation
        
class ershortbycompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseRecord
        fields = ['er_id', 'company_id', 'expense_date', 'coa_id', 'vendor_id', 'paid_through', 'customer_id', 'expense_serial','expense_status', 'amount']
        depth = 1

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)

        return representation
        

class UpdTExpenseRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseRecord
        exclude = ['attach_file']
        
        
        
        
#ExpenseBank serializer
class ExpbankSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExpenseRecord
        fields='__all__'
        
        
class ForPaginationExpenseRecordSerializer(serializers.ModelSerializer):
    expense_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = ExpenseRecord
        fields =['er_id', 'expense_date', 'expense_ref_no', 'expense_serial', 'expense_status', 'expense_total', 'expense_type', 
                 'amount', 'vendor_id', 'customer_id', 'is_converted']
        depth=1

