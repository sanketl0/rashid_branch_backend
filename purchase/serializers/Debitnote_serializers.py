import imp
from rest_framework import serializers
from transaction.models import CoaCharges
from transaction.serializers import CoaTransactionSerializer
from purchase.models.Debitnote_model import DebitNote,DebitNoteView
from .DebitItem_serializers import DebitNoteItemSerializerGet
class DebitnoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=DebitNote
        exclude = ['attach_file',]
        
        
class ShortDebitNoteSerializer(serializers.ModelSerializer):
    dn_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = DebitNote
        fields = ['dn_id','total','order_no','dn_date','dn_ref_no','dn_serial',
                  'vendor_id','dn_status','company_id','branch_id','balance_amount']
        depth=1
        

     
class DnItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = DebitNote
        fields = '__all__'  
        
class JoinDebitNoteItemSerializer(serializers.ModelSerializer):
    debit_note_items = DebitNoteItemSerializerGet(many=True)
    dn_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = DebitNote
        fields = '__all__'
        depth=1
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        objs = CoaCharges.objects.filter(dn_id=instance, charges_type='DEFAULT')
        taxes = CoaCharges.objects.filter(dn_id=instance, charges_type='TAX')
        representation['co_charges'] = CoaTransactionSerializer(objs, many=True).data
        representation['total_taxes'] = CoaTransactionSerializer(taxes, many=True).data
        print(representation['party_account'], ">>>>>>>>>>>>>>>>>>>")
        return representation
        
class GSTReportsONLYDebitnoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitNote
        fields = '__all__'
        depth=2
        
        
        

class DebitNoteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitNote
        fields= ['dn_status']
        
        
class DebitNoteVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=DebitNote
        fields= '__all__'
        
        

class FoRPaginationShortDebitNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DebitNoteView
        fields = ['dn_id','total','order_no','dn_date','dn_ref_no','dn_serial',
                  'vendor_name','dn_status','branch_id','balance_amount']
