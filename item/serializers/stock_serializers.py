from rest_framework import serializers
from item.models.stock_model import Stock,Batch,WareHouse
from item.serializers.adjustment_serializers import JoinAdjustmentAndAdjustItemSerializer
from salescustomer.serializers.Invoice_serializers import GSTReportsONLYInvoiceSerializer
from salescustomer.serializers.Creditnote_serializers import GSTReportONLYCnSerializer
from purchase.serializers.Bill_serializers import GSTReportsONLYBillSerializer
from purchase.serializers.Debitnote_serializers import GSTReportsONLYDebitnoteSerializer
from salescustomer.models.Creditnote_model import CreditNote
from salescustomer.models.Invoice_model import Invoice
from purchase.models.Bill_model import Bill
from purchase.models.Debitnote_model import DebitNote
from item.models.stock_model import ItemAvgTransaction

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        depth=1
        
        
        
class StockIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        exclude = ['branch_id','company_id']


class AdjStockSerializer(serializers.ModelSerializer):
    adj_serializer=JoinAdjustmentAndAdjustItemSerializer
    class Meta:
        model = Stock
        fields = '__all__' 
        
        
# may this serializers  Has probliming Becase both serilaizer same name but depth =1
class GodownSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = '__all__'

class GodownGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['label'] = instance.name
        representation['value'] = instance.wh_id
        return representation

class ItemAvgTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAvgTransaction
        exclude = ['item_id','company_id','branch_id']

class StockSerializerWithRefID(serializers.ModelSerializer):
    
    ref_id = serializers.SerializerMethodField()
    class Meta:
        model = Stock
        fields = '__all__'
        depth=2
        
    def get_ref_id(self, obj):
        if obj.ref_tblname == 'Invoice':
           return GSTReportsONLYInvoiceSerializer( Invoice.objects.get(invoice_id=obj.ref_id)).data
        if obj.ref_tblname == 'Bill':
           return GSTReportsONLYBillSerializer( Bill.objects.get(bill_id=obj.ref_id)).data
        if obj.ref_tblname == 'DebitNote':
           return GSTReportsONLYDebitnoteSerializer( DebitNote.objects.get(dn_id=obj.ref_id)).data
        if obj.ref_tblname == 'Credit Note':
           return GSTReportONLYCnSerializer( CreditNote.objects.get(cn_id=obj.ref_id)).data
       
       
            
       
        return obj.ref_id