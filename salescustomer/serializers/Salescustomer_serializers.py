
from rest_framework import serializers

from salescustomer.models.Salescustomer_model import SalesCustomer,CustomerTcs
from salescustomer.models.Invoice_model import Invoice
from .Invoice_serializers import CustomerInvoiceSerializer
from .Customerob_serializers import CustomerObSerializer
from .Pr_serializers import PRSerializer
from banking.models.customer_advance_model import CustomerAdvance
from banking.serializers.customer_advance_serializers import CustomerAdvSerializer
from .Creditnote_serializers import CreditNoteStatusSerializer,CreditNoteSerializer
from salescustomer.models.Creditnote_model import CreditNote

class NewSalesCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCustomer
        fields = [ 'customer_id','company_id','branch_id','customer_name','company_name','exemption_reason',
                  'company_number','opening_balance','customer_designation','customer_department',
    'customer_mobile','customer_display_name' ,'print_as_check_as', 'customer_contact',
    'customer_email','customer_type','salutation','contact_department','b_attention','bill_address_city',
    'customerTypeRefListId','bill_address_state','bill_contact_number','bill_address_country','term_name',
    'enable_portal' ,'company_display_name' ,'company_email' ,
   'website' , 'opening_balance' ,'currency',  'set_credit_limit' ,'gst_treatment' ,'gstin_number', 
    'tax_preference','cin_number' ,'trn_number' , 'vat_number' ,'pan_number' ,
    'bill_address1', 'bill_address2' ,'bill_address_state', 'bill_address_postal_code', 
    'bill_fax_number' ,'s_attention' ,'ship_address1' ,
    'ship_address2' ,'ship_address_city' ,'ship_address_state', 'ship_address_postal_code',
    'ship_address_country' ,'ship_contact_number','ship_fax_number', 'supply_place' ,'contact_salutation' ,
    'contact_name' ,'contact_phone','contact_mobile','contact_email','contact_designation' ,
    'remarks' ,'no_of_days' ,'is_verified','tcs_id','ext_id','ext_type'
    ]
class SalesCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCustomer
        fields = '__all__'
        
class SalesCustomerSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = SalesCustomer
        exclude = ['invoice_template']

class JoinCustomerSerializer(serializers.ModelSerializer):
    customer_balance = CustomerObSerializer(many=True)

    class Meta:
        model = SalesCustomer
        fields = '__all__'
        
class WholeCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerTcs
        fields = []
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = instance.customer_name
        representation['value'] = instance.customer_id
        representation['is_valid'] = instance.is_valid
        representation['tcs_id'] = instance.tcs_id
        obj = SalesCustomer.objects.get(customer_id=instance.customer_id)
        try:
            representation['coa_id'] = obj.coa_id.coa_id
            representation['coa_name'] = obj.coa_id.account_name
        except:
            representation['coa_id'] = None
            representation['coa_name'] = None
        return representation

class WholeCustomerJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerTcs
        fields = []
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = f"{instance.customer_name} ==> customers"
        representation['value'] = instance.customer_id
        representation['is_valid'] = instance.is_valid
        representation['tcs_id'] = instance.tcs_id
        return representation
class ShortCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCustomer
        fields = ['customer_name', 'company_name', 'customer_email', 'customer_contact', 'customer_id','customer_mobile','customer_type']
        ordered_tasks = SalesCustomer.objects.order_by('-customer_name')


class customernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCustomer
        fields = ['customer_name', 'customer_id', 'company_name', 'company_id', 'customer_mobile', 'customer_email',
                  'company_display_name']
        
        
class customershortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCustomer
        fields = ['customer_id', 'customer_name', 'customer_display_name']
        
        
class InvoicebyCustomerSerializer(serializers.ModelSerializer):
    # customer_invoices=CustomerInvoiceSerializer(many=True)
    customer_invoices = serializers.SerializerMethodField('getpayment_status')

    def getpayment_status(self, customer):
        query = Invoice.objects.filter(payment_status='unpaid', customer_id=customer)
        serializer = CustomerInvoiceSerializer(instance=query, many=True)
        return serializer.data

    class Meta:
        model = SalesCustomer
        # fields= '__all__'
        fields = ['customer_id', 'customer_designation', 'company_id', 'branch_id', 'customer_invoices']
        

        
class PRCustomerSerializer(serializers.ModelSerializer):
    customer_pr=PRSerializer(many=True)
    class Meta:
        model=SalesCustomer
        fields=['customer_pr']
        
        
        
class CustomerPaymentRefundSerializer(serializers.ModelSerializer):
    customer_ad=serializers.SerializerMethodField('getamount')
    def getamount(self, customer):
        query=CustomerAdvance.objects.filter(balance_amount__gt=0, customer_id=customer)
        serializer=CustomerAdvSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=SalesCustomer
        fields=['customer_ad']
        
        
# Get Cn_Status in Customer id
class CNStatusCustomerSerializer(serializers.ModelSerializer):
    cnsta_customer=CreditNoteStatusSerializer(many=True)
    class Meta:
        model=SalesCustomer
        fields=['cnsta_customer']
        

class GETCreditNoteCustomerSerializer(serializers.ModelSerializer):
    customer_cn=serializers.SerializerMethodField('getopen_status')
    def getopen_status(self, customer):
        query=CreditNote.objects.filter(status='Open', customer_id=customer)
        serializer=CreditNoteSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=SalesCustomer
        fields=['customer_cn']
        depth=1
        
        
class PaginationcustomershortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCustomer
        fields = ['customer_name', 'customer_email', 'customer_mobile', 'company_name', 'customer_type', 
                  'supply_place', 'customer_id', 'customer_display_name']