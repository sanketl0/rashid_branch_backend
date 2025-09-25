# from rest_framework import serializers

# from transaction.models import MasterTransaction
# from .models_old import SalesCustomer
# from coa.models import COA, OpeningBalance
# from item.models import Item
# from .models_old import *  # Estimate, SO, Invoice, DC, PR, RI, CreditNote
# from .models_old import Invoice


# # Customer
# class NewSalesCustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesCustomer
#         fields = [ 'customer_id','company_id','customer_name','company_name','exemption_reason',
#                   'company_number','opening_balance','customer_designation','customer_department',
#     'customer_mobile','customer_display_name' ,'print_as_check_as', 'customer_contact',
#     'customer_email','customer_type','salutation','contact_department','b_attention','bill_address_city',
#     'customerTypeRefListId','bill_address_state','bill_contact_number','bill_address_country','term_name',
#     'enable_portal' ,'company_display_name' ,'company_email' ,
#    'website' , 'opening_balance' ,'currency',  'set_credit_limit' ,'gst_treatment' ,'gstin_number', 
#     'tax_preference','cin_number' ,'trn_number' , 'vat_number' ,'pan_number' ,
#     'bill_address1', 'bill_address2' ,'bill_address_state', 'bill_address_postal_code', 
#     'bill_fax_number' ,'s_attention' ,'ship_address1' ,
#     'ship_address2' ,'ship_address_city' ,'ship_address_state', 'ship_address_postal_code',
#     'ship_address_country' ,'ship_contact_number','ship_fax_number', 'supply_place' ,'contact_salutation' ,
#     'contact_name' ,'contact_phone','contact_mobile','contact_email','contact_designation' ,
#     'remarks' ,'no_of_days' ,'is_verified'
#     ]


# ############################## file upload serializer ####################
# class SalesCustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesCustomer
#         fields = '__all__'

# # Customer and OB join
# # serializer to show selected field in customer API after join
# class CustomerObSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomerOB
#         # fields = ['credit','debit','available_balance','customer_id','company_id','ob_id']
#         fields = '__all__'


# # join Customer and OB
# class JoinCustomerSerializer(serializers.ModelSerializer):
#     customer_balance = CustomerObSerializer(many=True)

#     class Meta:
#         model = SalesCustomer
#         fields = '__all__'


# # getcustomershort
# class ShortCustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesCustomer
#         fields = ['customer_name', 'company_name', 'customer_email', 'customer_contact', 'customer_id']
#         ordered_tasks = SalesCustomer.objects.order_by('-customer_name')


# # getcustomerbyname
# class customernameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesCustomer
#         fields = ['customer_name', 'customer_id', 'company_name', 'company_id', 'customer_mobile', 'customer_email',
#                   'company_display_name']


# # customershortbycompanyid
# class customershortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesCustomer
#         fields = ['customer_id', 'customer_name', 'customer_email', 'customer_mobile', 'company_id', 'company_name']


# ###########################################################################
# # customershortbycompanyid
# # class CompanySerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Company
# #         fields = ['company_id','company_name']

# # class customershortbycompanySerializer(serializers.ModelSerializer):
# #     company_cust = CompanySerializer(many=True)
# #     class Meta:
# #         model = SalesCustomer
# #         fields = ['customer_id','customer_name','company_id','company_name']

# ############################################################################
# # Employee
# class employeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = '__all__'


# # TCS
# class tcsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TCS
#         fields = '__all__'


# # Payment Terms
# class PaymentTermSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentTerms
#         fields = '__all__'


# # Estimate
# class EstimateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Estimate
#         fields = '__all__'
#         depth=1


# # getestimateshort
# class ShortEstimateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Estimate
#         fields = ['est_date', 'est_ref_no', 'est_serial', 'customer_id', 'est_status', 'total', 'amount', 'tcs_amount',
#                   'est_id', 'company_id', 'branch_id']
#         depth = 1


# # Estimate and Item join
# class EstimateItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EstimatedItem
#         fields = '__all__'


# class JoinItemSerializer(serializers.ModelSerializer):
#     estimate_items = EstimateItemSerializer(many=True)

#     class Meta:
#         model = Estimate
#         fields = '__all__'
#         # fields = ['est_id','est_no','estimate_items']


# # Estimated item serializer
# class EstimatedItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EstimatedItem
#         fields = '__all__'
#         # depth = 1


# # join Estimate and EstimatedItem
# class EstItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EstimatedItem
#         fields = ['est_id', 'estitem_id', 'item_name','item_id','amount', 'quantity', 'rate', 'tax_name', 'taxamount',
#                   'igst_amount', 'cgst_amount', 'sgst_amount']


# class JoinEstimateItemSerializer(serializers.ModelSerializer):
#     estimate_items = EstItemSerializer(many=True)

#     class Meta:
#         model = Estimate
#         fields = '__all__'
#         depth = 1


# # Sales Order
# class SOSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SO
#         fields = '__all__'
#         depth=1


# # getsalesordershort
# class ShortSalesOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SO
#         fields = ['so_id', 'total', 'so_date', 'so_ref_no', 'so_serial', 'customer_id', 'so_status', 'company_id',
#                   'branch_id']
#         depth = 1


# # So item serializer
# class SoItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SoItem
#         fields = '__all__'


# # join SO and SoItem
# class SOItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SoItem
#         fields = ['so_id', 'soitem_id', 'item_name', 'amount', 'quantity', 'rate', 'tax_name', 'taxamount',
#                   'cgst_amount', 'sgst_amount', 'igst_amount','item_id']


# class JoinSoItemSerializer(serializers.ModelSerializer):
#     so_items = SOItemSerializer(many=True)

#     class Meta:
#         model = SO
#         fields = '__all__'
#         depth = 1


# # delivery Challan
# class DCSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DC
#         fields = '__all__'


# # getdcshort
# class ShortDeliveryChallanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DC
#         fields = ['dc_id', 'total', 'dc_date', 'dc_ref_no', 'dc_serial', 'customer_id', 'dc_status', 'company_id',
#                   'branch_id']
#         depth = 1


# # dcshortbycompanyid
# class dcshortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DC
#         fields = ['dc_id', 'total', 'dc_date', 'dc_ref_no', 'dc_serial', 'customer_id', 'dc_status', 'company_id',
#                   'branch_id']
#         depth = 1


# # Dc item serializer
# class DcItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DcItem
#         fields = '__all__'


# # #get dc by id serializer
# # class DcbyidSerializer(serializers.ModelSerializer):    
# #     class Meta:
# #         model = DC
# #         fields = ['dc_id','dc_type','','','dcitem_id','item_name','amount','quantity','rate']

# # join DC and DoItem
# class DCItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DcItem
#         fields = ['dc_id', 'dcitem_id', 'item_name', 'taxamount', 'amount', 'quantity', 'rate', 'tax_name',
#                   'cgst_amount', 'sgst_amount', 'igst_amount','item_id']


# class JoinDcItemSerializer(serializers.ModelSerializer):
#     dc_items = DCItemSerializer(many=True)

#     class Meta:
#         model = DC
#         fields = '__all__'
#         depth = 1


# # Credit Note
# class CreditNoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditNote
#         fields = '__all__'


# # getcreditnoteshort
# class ShortCreditNoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditNote
#         fields = ['cn_id', 'total', 'cn_date', 'cn_ref_no', 'cn_serial', 'customer_id', 'cn_status', 'company_id',
#                   'branch_id','balance_amount']
#         depth = 1


# # Credit note item serializer
# class CnItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditItem
#         fields = '__all__'


# # join Credit Note and Item
# class CreditNoteItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditItem
#         fields = ['cn_id', 'cnitem_id', 'item_name', 'amount', 'quantity', 'rate', 'tax_name', 'taxamount', 'coa_id',
#                   'cgst_amount', 'sgst_amount', 'igst_amount','item_id']
#         depth = 1


# class JoinCreditNoteItemSerializer(serializers.ModelSerializer):
#     credit_note_items = CreditNoteItemSerializer(many=True)

#     class Meta:
#         model = CreditNote
#         fields = '__all__'
#         depth = 1
# print("##################################",JoinCreditNoteItemSerializer)


# # Credit note journal transaction serializer
# class CreditnoteJTSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditNoteTransaction
#         fields = '__all__'
#         depth = 1


# class cntransactionsSerializer(serializers.ModelSerializer):
#     creditnotetransaction = CreditnoteJTSerializer(many=True)

#     class Meta:
#         model = CreditNote
#         fields = ['cn_id', 'creditnotetransaction']

#     # serializer for customer invoices


# # get invoice by customer id
# class CustomerInvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = '__all__'
#         # depth=1


# class InvoicebyCustomerSerializer(serializers.ModelSerializer):
#     # customer_invoices=CustomerInvoiceSerializer(many=True)
#     customer_invoices = serializers.SerializerMethodField('getpayment_status')

#     def getpayment_status(self, customer):
#         query = Invoice.objects.filter(payment_status='unpaid', customer_id=customer)
#         serializer = CustomerInvoiceSerializer(instance=query, many=True)
#         return serializer.data

#     class Meta:
#         model = SalesCustomer
#         # fields= '__all__'
#         fields = ['customer_id', 'customer_designation', 'company_id', 'branch_id', 'customer_invoices']


# # Invoice
# class InvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         exclude = ('attach_file', )
#         # depth=1
# class GST2AreportsInvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields='__all__'
#         depth=1


# # getinvoiceshort
# class ShortInvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = ['invoice_id', 'invoice_date', 'order_no', 'amount_due', 'due_date', 'invoice_serial', 'customer_id',
#                   'invoice_status', 'amount', 'total', 'company_id', 'branch_id']
#         depth = 1


# # invoiceshortbycompanyid
# class invoiceshortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = ['invoice_id', 'invoice_date', 'order_no', 'amount_due', 'due_date', 'invoice_serial', 'customer_id',
#                   'invoice_status', 'payment_status', 'amount', 'total', 'company_id', 'branch_id']
#         depth = 1


# # Invoice item serializer
# class InvoiceItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InvoiceItem
#         fields = '__all__'
#         depth=1


# # join Invoice and InvoiceItem
# class InvoiceItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InvoiceItem
#         fields = ['invoice_id', 'invoiceitem_id', 'item_name', 'amount', 'quantity', 'rate', 'tax', 'taxamount',
#                   'tax_name', 'sgst_amount', 'cgst_amount', 'igst_amount','item_id','coa_id']


# class JoinInvoiceAndInvoiceItemSerializer(serializers.ModelSerializer):
#     invoice_items = InvoiceItemSerializer(many=True)

#     class Meta:
#         model = Invoice
#         fields = '__all__'
#         depth = 1

# # Invoice item serializer
# class reports2AInvoiceItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InvoiceItem
#         fields = '__all__'
#         depth=1
        
        
# class InvoiceAndInvoiceItem2ASerializer(serializers.ModelSerializer):
#     invoice_items = reports2AInvoiceItemSerializer(many=True)

#     class Meta:
#         model = Invoice
#         fields = '__all__'
#         depth = 1        
        
        
        
# # # Invoice journal transaction serializer
# # class InvoiceJTSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = InvoiceJournalTransaction
# #         fields = '__all__'


# # get invoice journal transactions by invoice id
# class InvoiceJTSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InvoiceJournalTransaction
#         fields = '__all__'
#         depth = 1


# class InvoicetransactionsSerializer(serializers.ModelSerializer):
#     transactions = InvoiceJTSerializer(many=True)

#     class Meta:
#         model = Invoice
#         fields = ['invoice_id', 'transactions']

#     # Payment Mode


# class paymentmodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentMode
#         fields = '__all__'


# # PaymentReceived
# # get coa by account name
# class accountnameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = COA
#         fields = ['coa_id', 'account_name', 'account_type']
#         depth = 1


# class PRMSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PR
#         fields = '__all__'
#         depth = 2


# # getprshort
# class PrShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PR
#         fields = ['pr_id', 'payment_serial', 'amount_excess', 'payment_ref_no', 'invoice_serial', 'invoice_amount',
#                   'balance_amount', 'payment_date', 'payment_mode', 'amount_received', 'customer_id', 'company_id',
#                   'branch_id']
#         depth = 1

#     # prshortbycompanyid


# class prshortbycompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PR
#         fields = ['pr_id', 'payment_serial', 'amount_excess', 'payment_ref_no', 'invoice_serial', 'invoice_amount',
#                   'balance_amount', 'payment_date', 'payment_mode', 'amount_received', 'customer_id', 'company_id',
#                   'branch_id']
#         depth = 1

#     # payment journal transaction


# class PaymentJTSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentTransaction
#         fields = '__all__'
#         depth = 1


# # payment transaction serializer will show all fields from payment receive model and payment transaction model
# class PaymentTransactionSerializer(serializers.ModelSerializer):
#     payment_transactions = PaymentJTSerializer(many=True)

#     class Meta:
#         model = PR
#         fields = ['pr_id', 'payment_transactions']

#     # Recurring Invoice


# class RISerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RI
#         fields = '__all__'




# #GST Reports Using Serializer

# #GST Reports Invoice Serailizer


# class GSTReportsInvoiceItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InvoiceItem
#         fields = '__all__'
#         depth=3
        
# #GST Reports Usingf Credit Note Serializer
# class GSTReportsCnItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditItem
#         fields = '__all__'
#         depth=2
        
        
# class GSTReportsONLYInvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = '__all__'
#         depth=2
        
# class GSTReportONLYCnSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditNote
#         fields = '__all__'
#         depth=2
        
        
        
        
        
        
# class CreditNoteonlyserializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditNote
#         fields ='__all__'
        

# ###################################################### SERIALIZERS MADE BY VARSHA #################

# class SOUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=SO
#         fields='__all__'


# class UpdtJoinSoItemSerializer(serializers.ModelSerializer):
#     so_items = SOItemSerializer(many=True)

#     class Meta:
#         model = SO
#         fields = '__all__'


# class DCItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DcItem
#         fields = ['dc_id', 'dcitem_id', 'item_name', 'taxamount', 'amount', 'quantity', 'rate', 'tax_name',
#                   'cgst_amount', 'sgst_amount', 'igst_amount','item_id']


# class UpdtDcItemSerializer(serializers.ModelSerializer):
#     dc_items = DCItemSerializer(many=True)

#     class Meta:
#         model = DC
#         fields = '__all__'

# class EstimateSerializerUpdate(serializers.ModelSerializer):
#     class Meta:
#         model = Estimate
#         fields = '__all__'
# class EstimatedITEMSerializerUpdate(serializers.ModelSerializer):
#     class Meta:
#         model = EstimatedItem
#         fields = '__all__'


# class UpDtEstimateSerializer(serializers.ModelSerializer):
#     estimate_items = EstItemSerializer(many=True)
#     class Meta:
#         model = Estimate
#         fields = '__all__'



# ######################### SRIALIZERS MADE BY VARSHA ###############
# class updtPRMSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PR
#         fields = '__all__'
 
# ########################   

# class SalesOrderSerializerUpdate(serializers.ModelSerializer):
#     class Meta:
#         model = SO
#         fields = '__all__'
# class SOITEMSerializerUpdate(serializers.ModelSerializer):
#     class Meta:
#         model = SoItem
#         fields = '__all__'
 
# ######################################   

# class SalesOrderSerializerUpdate(serializers.ModelSerializer):
#     class Meta:
#         model = SO
#         fields = '__all__'
# class SOITEMSerializerUpdate(serializers.ModelSerializer):
#     class Meta:
#         model = SoItem
#         fields = '__all__'
 
 
# ##########################

# class DeliveryChalanSerializerUpdate(serializers.ModelSerializer):
#     class Meta:
#         model = DC
#         fields = '__all__'
# class DCITEMSerializerUpdate(serializers.ModelSerializer):
#     class Meta:
#         model = DcItem
#         fields = '__all__'       
