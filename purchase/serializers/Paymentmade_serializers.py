from rest_framework import serializers
from purchase.models.Paymentmade_model import PaymentMade
from coa.models import COA
from report.models import AccountBalance


class PaymentmadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMade
        fields= '__all__'	
        depth=1

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.deposit_to:
            try:
                representation['paid_through_name'] = AccountBalance.objects.get(coa_id=instance.paid_through).account_name
                representation['balance'] = AccountBalance.objects.get(
                    coa_id=instance.paid_through).balance
            except:
                pass

        return representation

class PaymentmadeSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = PaymentMade
        fields= '__all__'

class PaymentmadeSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = PaymentMade
        fields= '__all__'

        
        
class paymentmadeshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMade
        fields=['pm_id','payment_ref_no','paid_through','amount_excess','amount_payable','bill_serial','balance_amount','vendor_id','company_id','bill_date','bill_amount','payment_date','payment_ref_no','payment_mode','amount_payable','amount_due','payment_serial']
        depth=1

    def to_representation(self,instance):
        data = super().to_representation(instance)
        data['bill_date'] = instance.bill_date.date()
        data["paid_through"] = COA.objects.get(coa_id=instance.paid_through).account_name
        return data
        
class UpdtPaymentmadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMade
        fields= '__all__'	
        
        
        
class VendorPaymentMadeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaymentMade
        fields= ['pm_id','payment_serial','amount_payable','balance_amount','amount_due','amount_excess']
        
class ForPaginationpaymentmadeshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMade
        fields=['pm_id','payment_ref_no','paid_through','amount_payable','bill_serial','balance_amount',
                'vendor_id','bill_date','bill_amount','payment_date','payment_ref_no','payment_mode','amount_payable','amount_due','payment_serial',
                'is_converted', 'amount_excess']
        depth=1
