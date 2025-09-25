from rest_framework import serializers
from purchase.models.Bill_Item_model import Bill_Item
from item.models.stock_model import getstock_on_hand
from item.models.stock_model import Batch
from django.db.models import Q
class BillItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Bill_Item
        fields = '__all__'
        
        
class BillItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Bill_Item        
        fields = ['bill_id','billitem_id','vendor_id','customer_id',
                  'cess_rate','cess_amount',
                  'item_name','item_id','amount','discount','quantity','rate',
                  'taxamount','tax_name','sgst_amount','cgst_amount','igst_amount','coa_id']
        depth=1

class BillItemSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Bill_Item
        exclude = ['billitem_id','bill_id']

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        batches = eval(instance.batch_no)
        representation['batches'] = batches
        if representation['batches']:
            batch_no = batches[0]
        else:
            batch_no = None
        try:

            representation['stock_quantity'] = Batch.objects.get(Q(
                item_id=instance.item_id.item_id,
                batch_no=batch_no,
                expire_date=instance.expire_date,
                mfg_date=instance.mfg_date

            )).stock_quantity
            print(representation['stock_quantity'])
        except Exception as e:
            print(e)
            representation['stock_quantity'] = 0

        return representation
        
class GSTReportsBillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill_Item
        fields = '__all__'
        depth=2
        
        
class GETBillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill_Item
        fields = '__all__'