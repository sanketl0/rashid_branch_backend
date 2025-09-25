# from rest_framework import serializers
# from .models import *#Vendor,ExpenseRecord,ExpenseMileage,ExpenseMileage,ExpenseBulk,ExpenseBulk,RecExpense,PO,Bills,PayMade,RecBills,VC
# from coa.models import COA

# #Vendor
# class VendorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = '__all__'

# #vendorshortbycompanyid
# class vendorshortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = ['vendor_id','vendor_name','vendor_display_name','company_id','company_name','vendor_mobile','vendor_email'] 

# #vendor serializer for by company id
# class VendorCompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = ['vendor_id','vendor_name','company_id','branch_id']

# #get vendor by company serializer
# class CompanySerializer(serializers.ModelSerializer):
#     contact_person=VendorSerializer(many=True)
#     class Meta:
#         model = Company
#         fields = ['company_id','company_name','contact_person']

# #getvendorbyname
# class vendornameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = ['vendor_name','vendor_id','company_name','company_id']

# #vendor with all contact
# class VendorContactSerializer(serializers.ModelSerializer):     
#     class Meta:   
#         model = VendorContact
#         fields= '__all__'        
#         #depth=1
# class allcontactofvendorSerializer(serializers.ModelSerializer): 
#     # if we only assign  VendorContactSerializer() then it will show all null values for contact_person object. so it need to be used "many=True"
#     contact_person=VendorContactSerializer(many=True)    
#     class Meta:
#         model= Vendor
#         fields= '__all__'        
#         #fields=['customer_id','customer_designation','company_id','branch_id','customer_invoices']

# # Bill       
# class BillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bill
#         fields = '__all__'

# #get bill by vendor. It will return only unpaid bills
# #get bill by vendor id
# class VendorBillSerializer(serializers.ModelSerializer):     
#     class Meta:   
#         model = Bill
#         fields= '__all__'  

# class BillbyVendorSerializer(serializers.ModelSerializer):     
#     vendor_bills=serializers.SerializerMethodField('getpayment_status')
#     def getpayment_status(self, vendor):
#         query=Bill.objects.filter(payment_status='unpaid', vendor_id=vendor)
#         serializer=VendorBillSerializer(instance=query, many=True)
#         return serializer.data
#     class Meta:
#         model= Vendor
#         #fields= '__all__'
#         fields=['vendor_id','company_id','branch_id','vendor_bills']

# #billshortbycompanyid
# class billshortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bill
#         fields = ['bill_id','vendor_id','bill_date','order_no','bill_serial','payment_status','bill_status','total','due_date','amount_due','company_id','branch_id'] 
#         depth=1

# #bill by vendor id
# class billbyvendorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bill
#         fields = ['bill_id','bill_serial','vendor_id','company_id','branch_id','total']   

# #Bill item serializer
# class BillItemSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = Bill_Item
#         fields = '__all__'
        
# #join Bill and BillItem
# class BillItemSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = Bill_Item        
#         fields = ['bill_id','billitem_id','vendor_id','coa_id','customer_id','item_name','item_id','amount','discount','quantity','rate','taxamount','tax_name','sgst_amount','cgst_amount','igst_amount']
#         depth=1

# class JoinBillAndBillItemSerializer(serializers.ModelSerializer):
#     bill_items = BillItemSerializer(many=True)
#     class Meta:
#         model = Bill
#         fields = '__all__'
#         depth=1

# #Bill journal transaction serializer
# class BillJTSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = BillJournalTransaction
#         fields = '__all__'

# #get bill journal transactions by bill id
# class COASerializer(serializers.ModelSerializer):
#     class Meta:
#         model = COA
#         fields = ['coa_id','account_type','chart_of_account']

# class BillJTSerializer(serializers.ModelSerializer):     
#     class Meta:
#         model = BillJournalTransaction
#         fields = '__all__'
#         depth=1

# class BilltransactionsSerializer(serializers.ModelSerializer):
#     bill_journal_trasaction = BillJTSerializer(many=True)    
#     class Meta:
#         model = Bill
#         fields = ['bill_id', 'bill_journal_trasaction']  

# #get bill by vendor. It will return only unpaid bills
# #get bill by vendor id
# class VendorBillSerializer(serializers.ModelSerializer):     
#     class Meta:   
#         model = Bill
#         fields= '__all__'  

# class BillbyVendorSerializer(serializers.ModelSerializer):     
#     vendor_bills=serializers.SerializerMethodField('getpayment_status')
#     def getpayment_status(self, vendor):
#         query=Bill.objects.filter(payment_status='unpaid', vendor_id=vendor)
#         serializer=VendorBillSerializer(instance=query, many=True)
#         return serializer.data
#     class Meta:
#         model= Vendor
#         #fields= '__all__'
#         fields=['vendor_id','company_id','branch_id','vendor_bills']

# #TDS
# class tdsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TDS
#         fields = '__all__'
        
# # Expense record
# class ExpenseRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExpenseRecord
#         fields = '__all__'
#         depth=1

# #ershortbycompanyid
# class ershortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExpenseRecord
#         fields = ['er_id', 'company_id', 'expense_date', 'coa_id', 'vendor_id', 'paid_through', 'customer_id', 'expense_serial','expense_status', 'amount']
#         depth = 1

# #expense journal transaction
# class ExpenseJTSerializer(serializers.ModelSerializer):  
#     class Meta:
#         model = ExpenseJournalTransaction
#         fields = '__all__'
#         depth=1

# #expense transaction serializer will show all fields from expense record model and expense transaction model
# class ExpenseTransactionSerializer(serializers.ModelSerializer):
#     expense_transactions = ExpenseJTSerializer(many=True)    
#     class Meta:
#         model = ExpenseRecord
#         fields = ['er_id', 'expense_transactions'] 


# # Payment made
# class PaymentmadeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentMade
#         fields= '__all__'	
#         depth=1		
		
# #paymentmadeshortbycompanyid
# class paymentmadeshortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentMade
#         fields=['pm_id','payment_ref_no','paid_through','amount_payable','bill_serial','balance_amount','vendor_id','company_id','bill_date','bill_amount','payment_date','payment_ref_no','payment_mode','amount_payable','amount_due','payment_serial']
#         depth=1
        
# #paymentmade journaltransaction
# class PaymentmadeJTSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentmadeJournalTransaction
#         fields="__all__"
#         depth=1	
		
# class PaymentmadeAllSerializer(serializers.ModelSerializer):    
#     paymentmade_transactions=PaymentmadeJTSerializer(many=True)
#     class Meta:
#         model = PaymentMade        
#         fields= ['pm_id','paymentmade_transactions']

# #Purchase Order
# class POSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PO
#         fields = '__all__'
#         depth=1

# #getpurchaseordershortbycompanyid    
# class purchaseordershortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PO
#         fields = ['po_id','total','expected_delivery_date','po_date','po_ref_no','po_serial','customer_id','po_status','vendor_id','company_id','branch_id']
#         depth=1
        
# #Po item serializer
# class PoItemSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = PoItem
#         fields = '__all__'
#         depth=1
        
# #join PO and PoItem
# class POItemSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = PoItem        
#         fields = ['po_id','poitem_id','item_name','item_id','amount','discount','quantity','rate','coa_id','customer_id','cgst_amount','sgst_amount','igst_amount','tax_name']
#         depth=1

# class JoinPoItemSerializer(serializers.ModelSerializer):
#     po_items = POItemSerializer(many=True)
#     class Meta:
#         model = PO
#         fields = '__all__'
#         depth=1

# # Debitnote Serializers	
# class DebitnoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=DebitNote
#         fields='__all__'
#         #depth=1

# #getdebitnoteshort      
# class ShortDebitNoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DebitNote
#         fields = ['dn_id','total','order_no','dn_date','dn_ref_no','dn_serial','vendor_id','dn_status','company_id','branch_id','balance_amount']
#         depth=1

# #Debit note item serializer
# class DnItemSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = DebitNote
#         fields = '__all__'        
        
# #join Debit Note and Item
# class DebitNoteItemSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = DebitItem        
#         fields = ['dn_id','coa_id','dnitem_id','item_name','item_id','amount','quantity','rate','tax_name','taxamount','cgst_amount','sgst_amount','igst_amount']
#         depth=1

# class JoinDebitNoteItemSerializer(serializers.ModelSerializer):
#     debit_note_items = DebitNoteItemSerializer(many=True)
#     class Meta:
#         model = DebitNote
#         fields = '__all__'
#         depth=1

# #Debit note journal transaction serializer
# class DebitnoteJTSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = DebitNoteTransaction
#         fields = '__all__'
#         depth=1

# class dntransactionsSerializer(serializers.ModelSerializer):
#     debitnote_transactions = DebitnoteJTSerializer(many=True)    
#     class Meta:
#         model = DebitNote
#         fields = ['dn_id', 'debitnote_transactions']  
#         depth=1
# class UpdatesDebitnoteItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DebitItem
#         fields = '__all__'
            
        
        
# class GETBillItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bill_Item
#         fields = '__all__'
    
# # #ExpenseMileage
# # class ExpenseMileageSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ExpenseMileage
# #         fields = '__all__'

# # #ExpenseBulk
# # class ExpenseBulkSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ExpenseBulk
# #         fields = '__all__'

# # #RecExpense
# # class RecExpenseSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = RecExpense
# #         fields = '__all__'

# # #PO
# # class POSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = PO
# #         fields = '__all__'

# # #Bills
# # class BillsSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Bills
# #         fields = '__all__'

# # #PayMade
# # class PayMadeSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = PayMade
# #         fields = '__all__'

# # #RecBills
# # class RecBillsSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = RecBills
# #         fields = '__all__'

# # #VC
# # class VCSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = VC
# #         fields = '__all__'




# #GST Reports Using Seralizer
# class GSTReportsBillItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bill_Item
#         fields = '__all__'
#         depth=2
        
# class GSTReportsDebitnoteItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DebitItem
#         fields = '__all__'
#         depth=2
        
        
# class GSTReportsONLYDebitnoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DebitNote
#         fields = '__all__'
#         depth=2
# class GSTReportsONLYBillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bill
#         fields = '__all__'
#         depth=2
        
        
        
# class UpdTExpenseRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExpenseRecord
#         fields = '__all__'

# class UpdtPOserializer(serializers.ModelSerializer):
#     class Meta:
#         model= PO
#         fields='__all__'

# class UpdtPOItemSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = PoItem        
#         fields = ['po_id','poitem_id','item_name','amount','discount','quantity','rate','coa_id','customer_id','cgst_amount','sgst_amount','igst_amount','tax_name']
       
      
# class UpdatePOSerializer(serializers.ModelSerializer):
  
#     class Meta:
#         model = PO
#         fields = '__all__'
        
        
        
# class UpdtPaymentmadeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentMade
#         fields= '__all__'	
        