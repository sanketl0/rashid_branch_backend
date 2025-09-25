from rest_framework import serializers
from salescustomer.models.Invoice_model import Invoice
from .Invoice_item_serializers import InvoiceItemSerializer,reports2AInvoiceItemSerializer
from coa.models import COA
from transaction.models import CoaCharges
from transaction.serializers import CoaTransactionSerializer
class CustomerInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        
        
        
class InvoiceSerializer(serializers.ModelSerializer):
    total_quantity = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Invoice
        exclude = ('attach_file', )

    def validate_total_quantity(self, value):
        return float(value)
        
class GST2AreportsInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields='__all__'
        depth=1
        
        
class ShortInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_id', 'invoice_date', 'order_no', 'amount_due', 'due_date', 'invoice_serial', 'customer_id',
                  'invoice_status', 'amount', 'total', 'company_id', 'branch_id']
        depth = 1



class invoiceshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_id', 'invoice_date', 'order_no', 'amount_due', 'due_date', 'invoice_serial','customer_name',
                  'invoice_status', 'payment_status', 'amount', 'total','amount_due',
                 ]
    #
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     name = None
    #     if instance.customer_id:
    #         name = instance.customer_id.customer_name
    #
    #     representation['customer_name'] = name
    #     return representation
class JoinInvoiceAndInvoiceItemSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1

    def to_representation(self,instance):
        representation = super().to_representation(instance)

        representation['pr_ids'] = [i.pr_id for i in  instance.invoice_prs.all()]
        if instance.deposit_to:
            try:
                representation['deposit_to_name'] = COA.objects.get(coa_id=instance.deposit_to).account_name
            except:
                pass
        objs = CoaCharges.objects.filter(invoice_id=instance,charges_type='DEFAULT')
        taxes = CoaCharges.objects.filter(invoice_id=instance, charges_type='TAX')
        representation['co_charges'] = CoaTransactionSerializer(objs, many=True).data
        representation['total_taxes'] = CoaTransactionSerializer(taxes, many=True).data
        # print(representation['total_taxes'])
        return representation


class InvoiceAndInvoiceItem2ASerializer(serializers.ModelSerializer):
    invoice_items = reports2AInvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1        
        
class GSTReportsONLYInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        depth=2
        