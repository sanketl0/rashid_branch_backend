from audit.models import Audit
from rest_framework import serializers
from salescustomer.models import *
from purchase.models import *
from .models import *
from transaction .models import MasterTransaction


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields ='__all__'


class AuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audit
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        c_name = None
        m_name = None
        try:
            c_name = instance.created_by.name
        except Exception as e:
            print(e)

        try:
            m_name = instance.modified_by.name
        except:
            pass
        print(instance.created_by)
        ret['created_by'] = c_name
        ret['modified_by'] = m_name
        return ret


class AccountReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountReport
        exclude = ['trans_date']

class AccountReportTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountReport
        fields = ['account_type','total']

class PurchasegstSerializer(serializers.ModelSerializer):
        class Meta:
            model = PurchaseGst
            fields = '__all__'

        def to_representation(self, instance):
            ret = super().to_representation(instance)
            ret['total'] = round((instance.i_tax + instance.c_tax + instance.s_tax + instance.amount), 2)
            return ret

class SalesGstSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesGst
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['total'] = round((instance.i_tax + instance.c_tax + instance.s_tax + instance.amount),2)
        return ret
class GSTR2ASerializer(serializers.ModelSerializer):
    class Meta:
        model = GSTR2A
        fields = '__all__'

class GSTR2BSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSTR2B
        fields = '__all__'
class GSTR3BSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSTR3B
        fields = '__all__'


    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     name = None
    #     try:
    #         if instance.module == 'Bill' or instance.module == 'DebitNote':
    #             name = Vendor.objects.get(vendor_id=instance.supplier).vendor_name
    #         else:
    #             name = SalesCustomer.objects.get(customer_id=instance.supplier).customer_name
    #     except Exception as e:
    #         print(e)
    #     ret['supplier_name'] = name
    #     return ret

class CashBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBook
        fields = '__all__'

class BankBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankBook
        fields = '__all__'
class creditnoteshortbycompanyserializer(serializers.ModelSerializer):    
    class Meta:
        model = CreditNote
        fields = ['cn_id','cn_serial','customer_id', 'cn_status', 'cn_date', 'customer_note', 'total', 'balance_amount','company_id','branch_id']
        depth=1        

#prshortbycompanyid
class prshortbycompanyserializer(serializers.ModelSerializer):
    class Meta:
        model = PR
        fields = ['pr_id','payment_serial', 'notes', 'payment_ref_no','payment_mode','payment_date','customer_id','balance_amount','invoice_serial','notes','amount_received', 'amount_excess','pr_id','company_id','branch_id'] 
        depth=1 
        
#invoiceshortbycompanyid
class invoiceshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_id','invoice_status', 'invoice_date', 'due_date', 'invoice_serial', 'order_no', 'customer_id', 'total', 'amount_due','company_id','branch_id']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        customer_name = None
        if instance.customer_id:
            customer_name = instance.customer_id.customer_name
        ret['customer_id'] = customer_name
        return ret
#getsalesordershortbycompanyid      
class ShortSalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SO
        fields = ['so_id','so_status', 'so_date', 'expected_shipment_date', 'so_serial', 'customer_id', 'total','company_id','branch_id']
        depth=1
#Invoice Dc Serializer
class InvoiceDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields=['invoice_status']
        depth=1


#getdeliverychallandetailsbycompanyid
class dcshortbycompanySerializer(serializers.ModelSerializer):
    invoice_dc=InvoiceDCSerializer(many=True, read_only=True)
    class Meta:
        model = DC
        fields = ('dc_id','total','dc_serial', 'dc_date', 'dc_status', 'invoice_id', 'customer_id','company_id','branch_id','invoice_dc')
        depth=1

#getestimatedetailsbycompanyid      
class ShortEstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = ['est_id','company_id','branch_id','est_status', 'invoice_id','est_date', 'expiry_date', 'est_serial', 'est_ref_no', 'customer_id', 'total']
        depth=1

#getbilldetailsbycompanyid
class billshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['bill_id', 'bill_date', 'bill_serial',
                  'amount_due','vendor_id', 'bill_status', 'total', 'due_date']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        vendor_name = None
        if instance.vendor_id:
            vendor_name = instance.vendor_id.vendor_name
        ret['vendor_id'] = vendor_name
        return ret

#getdebitnotedetailsbycompanyid      
class debitnoteshortSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitNote
        fields = ['dn_id','dn_date','dn_serial','vendor_id','dn_status','balance_amount','total','company_id','branch_id']
        depth=1        

#paymentmadeshortbycompanyid
class paymadeshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMade
        fields=['pm_id','payment_serial','bill_serial','vendor_id','payment_date','payment_ref_no','payment_mode','paid_through','note', 'bill_amount','amount_excess','amount_payable']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        vendor_name = None
        if instance.vendor_id:
            vendor_name = instance.vendor_id.vendor_name
        ret['vendor_id'] = vendor_name
        return ret

#getpurchaseordershortbycompanyid    
class poshortbycompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PO
        fields = ['po_id','vendor_id','total','expected_delivery_date','po_date','po_serial','po_status']
        depth=1

#payable summary by company id
# class BillJTransSerializer(serializers.ModelSerializer):     
#     class Meta:
#         model = BillJournalTransaction
#         fields = ['transaction_type']
#         depth=1

# class payablesummaryshortbycompanySerializer(serializers.ModelSerializer):
#     bill_journal_trasaction = BillJTransSerializer(many=True)    
#     class Meta:
#         model = Bill
#         fields = ['bill_id','vendor_id', 'bill_date', 'bill_serial', 'bill_status', 'total', 'amount_due','customer_id','company_id', 'bill_journal_trasaction']  
#         depth=1

# Expense details
class ExpenseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseRecord
        fields = ['er_id', 'company_id','coa_id', 'expense_date', 'expense_account', 'expense_ref_no' ,'vendor_id', 'customer_id','expense_status', 'amount']
        depth = 1

class MasterTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=MasterTransaction
        fields=['L1detail_id','L1detailstbl_name','debit','credit','L2detail_id','L2detailstbl_name','main_module',
        'module','sub_module','transc_deatils','banking_module_type','journal_module_type','trans_date','trans_status','to_account','to_acc_name',
        'to_acc_type','to_acc_head','to_acc_subhead','from_account','from_acc_type','from_acc_head','from_acc_subhead','from_acc_name','customer_id','vendor_id','company_id']
        fields='__all__'
        depth=1

class MasterJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model=MasterTransaction
        fields='__all__'
        depth=1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.to_account:
            try:

                representation['balance'] =  AccountBalance.objects.get(
                    coa_id=instance.to_account).balance
            except:
                pass

        return representation
        
        
        
        
        
        
####################### serializers for excel report##################
class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model=SalesCustomer
        fields=['customer_name']

class invoiceExcelReportSerializer(serializers.ModelSerializer):
    customer_id=customerSerializer()
    class Meta:
        model = Invoice
        fields = ['invoice_status', 'invoice_date', 'due_date', 'invoice_serial',  'total', 'amount_due','customer_id']

        
        # def create(self, validated_data):
        #     tracks_data = validated_data.pop('customer_id')
        #     cs = SalesCustomer.objects.create(**validated_data)
        #     for track_data in tracks_data:
        #         SalesCustomer.objects.create(cs=cs, **track_data)
        #     return cs
         
class PrExlReportSerializer(serializers.ModelSerializer):
    customer_id=customerSerializer()
    class Meta:
        model = PR
        fields = [ 'payment_serial', 'amount_excess', 'payment_ref_no', 'invoice_serial', 'invoice_amount',
                  'balance_amount', 'payment_date', 'payment_mode', 'amount_received', 'customer_id', 
                  ]

    def to_representation(self,instance):
        ret = super().to_representation(instance)
        customer_name = None
        if instance.customer_id:
            customer_name = instance.customer_id.customer_name
        ret['customer_id'] = customer_name
        return ret
class ven_dorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=['vendor_name']      
class billExlReportSerializer(serializers.ModelSerializer):
    vendor_id=ven_dorSerializer()
    class Meta:
        model = Bill
        fields = [ 'bill_date', 'bill_serial', 'vendor_id', 'bill_status', 'total', 'due_date'] 
            
        
class PMExlReportSerializer(serializers.ModelSerializer):
    vendor_id=ven_dorSerializer()
    class Meta:
        model = PaymentMade
        fields=['bill_serial','vendor_id','payment_date','payment_mode', 'bill_amount','amount_excess','amount_payable']
                 
        
class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBalance
        fields = '__all__'
class StockValuationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockValuationReport
        fields = '__all__'

    # def to_representation(self,instance):


#Get Day Report


class DaybookreportSerializer(serializers.ModelSerializer):
    class Meta:
        model=MasterTransaction
        fields=['trans_date','from_acc_name','transc_deatils','journal_module_type','debit','credit',]   
        
        
class CashbookreportSerializer(serializers.ModelSerializer):
    class Meta:
        model=MasterTransaction
        fields=['trans_date','transc_deatils','debit','credit','from_acc_name']     
        
class BankbookreportSerializer(serializers.ModelSerializer):
    class Meta:
        model=MasterTransaction
        fields=['trans_date','from_acc_name','transc_deatils','banking_module_type','debit','credit',] 
        
    