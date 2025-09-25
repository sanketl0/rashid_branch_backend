from rest_framework import serializers
from item.models.stock_model import Batch
from salescustomer.models.Invoice_item_model import InvoiceItem
from django.db.models import Q
        
        
# class InvoiceItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InvoiceItem
#         fields = '__all__'
#         depth=1

        
class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['invoice_id',
                  'cess_rate', 'cess_amount','godown_id','godown_name',
                  'invoiceitem_id', 'item_name', 'amount', 'quantity', 'rate', 'tax_rate','tax_type', 'taxamount','mfg_date','expire_date',
                  'tax_name', 'sgst_amount', 'cgst_amount', 'igst_amount','item_id','coa_id','discount','batches']

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['hsn_sac'] = instance.item_id.hsn_code
        btch = []
        try:
            btch = eval(instance.batches)
        except:
            pass

        representation['batches'] = btch
        representation['stock_quantity'] = 0
        # if representation['batches']:
        #     b_no = representation['batches'][0]
        #     branch_id = instance.invoice_id.branch_id.branch_id
        #     batch = Batch.objects.get(Q(item_id=instance.item_id.item_id,
        #                                 branch_id=branch_id,expire_date=instance.expire_date,
        #                                 mfg_date=instance.mfg_date,batch_no=b_no ))
        #     print(batch.stock_quantity)
        #     representation['stock_quantity'] = batch.stock_quantity
        representation['track_inventory'] = instance.item_id.track_inventory
        return representation
        
class reports2AInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        depth=1
        
        
        
class GSTReportsInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        depth=3