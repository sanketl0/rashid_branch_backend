from rest_framework import serializers
from salescustomer.models.Creditnote_model import CreditNote
from .Credit_item_serializers import CreditNoteItemSerializerGet
from transaction.models import CoaCharges
from transaction.serializers import CoaTransactionSerializer
class CreditNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditNote
        exclude = ['attach_file', ]
        
class ShortCreditNoteSerializer(serializers.ModelSerializer):
    cn_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = CreditNote
        fields = ['cn_id', 'total', 'cn_date', 'cn_ref_no', 'customer_name', 'cn_status',
                  'is_converted','balance_amount','cn_serial']

       
     
        
        
class JoinCreditNoteItemSerializer(serializers.ModelSerializer):
    cn_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    credit_note_items = CreditNoteItemSerializerGet(many=True)

    class Meta:
        model = CreditNote
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        objs = CoaCharges.objects.filter(cn_id=instance, charges_type='DEFAULT')
        taxes = CoaCharges.objects.filter(cn_id=instance, charges_type='TAX')
        representation['co_charges'] = CoaTransactionSerializer(objs, many=True).data
        representation['total_taxes'] = CoaTransactionSerializer(taxes, many=True).data

        return representation





class GSTReportONLYCnSerializer(serializers.ModelSerializer):
    cn_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = CreditNote
        fields = '__all__'
        depth=2
        
        
        
class CreditNoteonlyserializer(serializers.ModelSerializer):
    cn_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = CreditNote
        fields ='__all__'
        
        
class CreditNoteStatusSerializer(serializers.ModelSerializer):
    cn_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model=CreditNote
        fields=['cn_status']