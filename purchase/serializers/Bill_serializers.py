from rest_framework import serializers
from purchase .models import Bill,BillView
from .Bill_Item_serializers import BillItemSerializer,BillItemSerializerGet
from transaction.models import CoaCharges
from transaction.serializers import CoaTransactionSerializer
class BillSerializer(serializers.ModelSerializer):
    total_quantity = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Bill
        exclude = ('attach_file',)

    def validate_total_quantity(self, value):
        return float(value)


class BillSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['bill_id','bill_status','payment_status','total','due_date','amount_due']  
        
class VendorBillSerializer(serializers.ModelSerializer):     
    class Meta:   
        model = Bill
        fields= '__all__'  
        
        
class billshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['bill_id','vendor_id','bill_date','order_no','bill_serial',
                  'payment_status','bill_status','total','due_date','amount_due','company_id','branch_id', 'charges']
        depth=1
        
        
class billbyvendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['bill_id','bill_serial','vendor_id','company_id','branch_id','total']  
        
        
class JoinBillAndBillItemSerializer(serializers.ModelSerializer):
    bill_items = BillItemSerializerGet(many=True)
    class Meta:
        model = Bill
        fields ='__all__'
        depth=1

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['pm_ids'] = [i.pm_id for i in instance.bill_paymentmade.all()]
        objs = CoaCharges.objects.filter(bill_id=instance, charges_type='DEFAULT')
        taxes = CoaCharges.objects.filter(bill_id=instance, charges_type='TAX')
        representation['co_charges'] = CoaTransactionSerializer(objs, many=True).data
        representation['total_taxes'] = CoaTransactionSerializer(taxes, many=True).data


        return representation
        
class VendorBillSerializer(serializers.ModelSerializer):     
    class Meta:   
        model = Bill
        fields= '__all__'
        
        
class GSTReportsONLYBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
        depth=2
        
        
class ForPaginationJoinBillAndBillItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillView
        fields = ['bill_date', 'bill_serial', 'bill_ref_no', 'payment_status', 'vendor_name',
                  'total', 'order_no',  'due_date', 'total', 'amount_due', 'bill_id']
