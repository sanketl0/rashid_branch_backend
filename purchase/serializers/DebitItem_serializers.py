from rest_framework import serializers
from purchase.models.DebitItem_model import DebitItem
from item.models.stock_model import Batch
from django.db.models import Q
class DebitNoteItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = DebitItem        
        fields = ['dn_id','coa_id','dnitem_id','item_name','item_id','amount','quantity','rate','tax_name','taxamount','cgst_amount','sgst_amount','igst_amount']
        depth=1

class DebitNoteItemSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = DebitItem
        exclude = ['dnitem_id','dn_id']

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        batches = eval(instance.batch_no)
        print((instance.batch_no),">>>>>>>>>>>>>>>>>>>")
        representation['batches'] = batches

        # if representation['batches']:
        #     batch_no = batches[0]
        # else:
        #     batch_no = None
        # try:
        #     representation['stock_quantity'] = Batch.objects.get(Q(
        #         item_id=instance.item_id.item_id,
        #         batch_no=batch_no,
        #         expire_date=instance.expire_date,
        #         mfg_date=instance.mfg_date
        #
        #     )).stock_quantity
        # except:
        #     representation['stock_quantity'] = 0

        return representation

class UpdatesDebitnoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitItem
        fields = '__all__'
        
        

class GSTReportsDebitnoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitItem
        fields = '__all__'
        depth=2