from banking.models.vendor_advanced_model import VendorAdvanced
from rest_framework import serializers
from purchase.models.Vendor_model import Vendor
from purchase.models.Tds_model import TDS
from coa.models import COA
from report.models import AccountBalance
class VendorAdvancedSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorAdvanced
        fields='__all__'
        depth=1



class VendorPaymentGETSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorAdvanced
        fields= "__all__"
    def to_representation(self,instance):
        ret = super().to_representation(instance)
        ret['vendor_name'] = None
        if instance.vendor_id:
            ret['vendor_name'] = Vendor.objects.get(vendor_id=instance.vendor_id.vendor_id).vendor_name
        ret['tds_name'] = None
        if instance.tds_id:
            ret['tds_name'] = TDS.objects.get(tds_id=instance.tds_id.tds_id).tax_name
        if instance.deposit_to:
            ret['deposit_to_name'] = AccountBalance.objects.get(coa_id=instance.deposit_to).account_name
            ret['balance'] = AccountBalance.objects.get(coa_id=instance.deposit_to).balance
        return ret

class UpdateVendorAdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorAdvanced
        fields='__all__'
        


class ForPaginationVendorAdvancedSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorAdvanced
        fields=['balance_amount', 'is_converted', 'paid_via', 'payment_serial', 'va_id', 'vendor_advance_date',
                'vendor_advance_ref_no', 'vendor_id', 'amount']
        depth = 1
