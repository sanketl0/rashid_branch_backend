
import imp
from rest_framework import serializers
from coa.models import COA
from purchase.models.Vendor_model import Vendor,VendorTds
from purchase.models.Bill_model import Bill
from company.models import Company
from .Bill_serializers import VendorBillSerializer
from .Vendor_contact_serializers import VendorContactSerializer
from .Debitnote_serializers import DebitNoteStatusSerializer,DebitNoteStatusSerializer,DebitnoteSerializer,DebitNoteVendorSerializer
from purchase.models.Debitnote_model import DebitNote
from banking.models.vendor_advanced_model import VendorAdvanced
from banking.serializers.vendor_advanced_serializers import VendorPaymentGETSerializer
from purchase.serializers.Paymentmade_serializers import VendorPaymentMadeSerializer
#Vendor
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['bill_template']


class WholeVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorTds
        fields = []
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = instance.vendor_name
        representation['value'] = instance.vendor_id
        representation['is_valid'] = instance.is_valid
        representation['tds_id'] = instance.tds_id
        obj = Vendor.objects.get(vendor_id=instance.vendor_id)
        try:
            representation['coa_id'] = obj.coa_id.coa_id
            representation['coa_name'] = obj.coa_id.account_name
        except:
            representation['coa_id'] = None
            representation['coa_name'] = None
        return representation

class WholeVendorJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorTds
        fields = []
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = f"{instance.vendor_name} ==> vendors"
        representation['value'] = instance.vendor_id
        representation['is_valid'] = instance.is_valid
        representation['tds_id'] = instance.tds_id
        return representation



#vendorshortbycompanyid
class vendorshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_id','vendor_name','vendor_display_name']


#vendor serializer for by company id
class VendorCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_id','vendor_name','company_id','branch_id']

#get vendor by company serializer
class CompanySerializer(serializers.ModelSerializer):
    contact_person=VendorSerializer(many=True)
    class Meta:
        model = Company
        fields = ['company_id','company_name','contact_person']
        
        
class vendornameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_id','company_name','company_id']
        
        
class allcontactofvendorSerializer(serializers.ModelSerializer): 
    # if we only assign  VendorContactSerializer() then it will show all null values for contact_person object. so it need to be used "many=True"
    contact_person=VendorContactSerializer(many=True)    
    class Meta:
        model= Vendor
        fields= '__all__'  
        

class BillbyVendorSerializer(serializers.ModelSerializer):     
    vendor_bills=serializers.SerializerMethodField('getpayment_status')
    def getpayment_status(self, vendor):
        query=Bill.objects.filter(payment_status='unpaid', vendor_id=vendor)
        serializer=VendorBillSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model= Vendor
        #fields= '__all__'
        fields=['vendor_id','company_id','branch_id','vendor_bills']
        
        
        
class VendordDNSerializer(serializers.ModelSerializer):
    ven_debitnote=DebitNoteStatusSerializer(many=True, read_only=True)
    class Meta:
        model= Vendor
        fields= ('vendor_id', 'ven_debitnote')



class VendorDebitNoteRefSerializer(serializers.ModelSerializer):
    ven_debitnote=serializers.SerializerMethodField('getopen_status')
    def getopen_status(self, vendor):
        query=DebitNote.objects.filter(status='Open', vendor_id=vendor)
        serializer=DebitnoteSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=Vendor
        fields= ["ven_debitnote"]
        depth=1

# class VendorAdvancedSerializer(serializers.ModelSerializer):
#     class Meta:

        

class VendorpaymenttrefSerializer(serializers.ModelSerializer):
    vendor_py=serializers.SerializerMethodField('getamount')
    def getamount(self, vendor):
        query=VendorAdvanced.objects.filter(balance_amount__gt=0, vendor_id=vendor)
        serializer=VendorPaymentGETSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=Vendor
        fields= ['vendor_py']
        depth=1
        
        
class VendorExAmountSerializer(serializers.ModelSerializer):
    coa_vp=VendorPaymentMadeSerializer(many=True, read_only=True)
    class Meta:
        model=Vendor
        fields=['vendor_id','coa_vp']
        
class VendorDebitNoteRefSerializer(serializers.ModelSerializer):
    ven_debitnote=serializers.SerializerMethodField('getopen_status')
    def getopen_status(self, vendor):
        query=DebitNote.objects.filter(status='Open', vendor_id=vendor)
        serializer=DebitNoteVendorSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=Vendor
        fields= ["ven_debitnote"]
        depth=1

class ForPaginationvendorshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_email', 'vendor_mobile', 'company_name', 'vendor_type', 
                   'vendor_id', 'vendor_display_name']
