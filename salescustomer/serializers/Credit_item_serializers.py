from rest_framework import serializers
from salescustomer.models.Credit_item_model import CreditItem



class CnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditItem
        fields = '__all__'
        
        
class CreditNoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditItem
        fields = ['cn_id', 'cnitem_id', 'item_name', 'amount', 'quantity', 'rate', 'tax_name', 'taxamount', 'coa_id',
                  'cgst_amount', 'sgst_amount', 'igst_amount','item_id']
        depth = 1

class CreditNoteItemSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = CreditItem
        exclude = ['cnitem_id','cn_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        btch = []
        try:
            btch = eval(instance.batches)
        except:
            pass
        representation['batches'] = btch
        return representation
        
class GSTReportsCnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditItem
        fields = '__all__'
        depth=2