from rest_framework import serializers

from salescustomer.models.Pr_model import PR,PrView
from coa.models import COA


class PRMSerializer(serializers.ModelSerializer):
    class Meta:
        model = PR
        fields = '__all__'
        depth = 2
    def to_representation(self,instance):
        representation = super().to_representation(instance)

        if instance.deposit_to:
            try:
                representation['deposit_to_name'] = COA.objects.get(coa_id=instance.deposit_to).account_name
            except:
                pass
            try:
                representation['party_account_name'] = instance.party_account.account_name
            except:
                pass

        return representation


class PrShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = PR
        fields = ['pr_id', 'payment_serial', 'amount_excess', 'payment_ref_no', 'invoice_serial', 'invoice_amount',
                  'balance_amount', 'payment_date', 'payment_mode', 'amount_received', 'customer_id', 'company_id',
                  'branch_id']
        depth = 1
        
        
        
class prshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PR
        fields = ['pr_id', 'payment_serial', 'amount_excess', 'payment_ref_no', 'invoice_serial', 'invoice_amount',
                  'balance_amount', 'payment_date', 'payment_mode', 'amount_received', 'customer_id', 'company_id',
                  'branch_id']
        depth = 1
        
        
        
        
class updtPRMSerializer(serializers.ModelSerializer):
    class Meta:
        model = PR
        fields = '__all__'
 
 
#Payment Recived Serializer
class PRSerializer(serializers.ModelSerializer):
    class Meta:
        model=PR
        fields=['invoice_id','payment_serial','amount_received','balance_amount','pr_id','amount_due','amount_excess','customer_id']
        depth=1
        

class GetPRshortbycompany_IDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrView
        fields = ['pr_id', 'payment_serial', 'amount_excess', 'payment_ref_no', 'invoice_serial', 'invoice_amount',
                  'balance_amount', 'payment_date', 'amount_received','payment_mode','customer_name'
                ]
