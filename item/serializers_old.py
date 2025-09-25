# import imp
# from rest_framework import serializers
# from rest_framework.response import Response

# from salescustomer.models.Invoice_model import Invoice
# from salescustomer.models.Creditnote_model import CreditNote
# # from purchase.models import  DebitNote,Bill
# from salescustomer.serializers import CreditNoteSerializer, InvoiceSerializer,GSTReportsInvoiceItemSerializer,GSTReportsCnItemSerializer,GSTReportsONLYInvoiceSerializer,GSTReportONLYCnSerializer
# from purchase.serializers.Bill_serializers import *
# from purchase.serializers.Debitnote_serializers import *
# from .models import Adjustment, Item, Company, Stock,AdjustmentItem

# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = '__all__'
#         depth=1

# #serializer for companywise item
# class ShortItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ['item_id','coa_id','name','item_description','opening_stock_rate','sales_account',
#         'opening_stock','unit','hsn_code','sac','exemption_reason','sale_price','cost_price']        

# #get item by company id
# class CompanySerializer(serializers.ModelSerializer): 
#     company_items=ShortItemSerializer(many=True) #Nested Serilizations
#     class Meta:
#         model = Company
#         fields = ['company_id','company_name','company_items']
        
        
        
        
# # Stock Serailzers
# class StockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stock
#         fields = '__all__'
#         depth=1
        
# #Adjustment

# class AdjustmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Adjustment
#         fields = '__all__'
#         depth=1
        
# class StockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stock
#         fields = '__all__'
      
        
        
# class AdjustmentItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdjustmentItem
#         fields = '__all__'
#         depth=1
        
        
# class JoinAdjustmentAndAdjustItemSerializer(serializers.ModelSerializer):
#     adj_items = AdjustmentItemSerializer(many=True)

#     class Meta:
#         model = Adjustment
#         fields = '__all__'
      
 
 
# class AdjStockSerializer(serializers.ModelSerializer):
#     adj_serializer=JoinAdjustmentAndAdjustItemSerializer
#     class Meta:
#         model = Stock
#         fields = '__all__'
        
        
# class StockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stock
#         fields = '__all__'
        

# class StockSerializerWithRefID(serializers.ModelSerializer):
    
#     ref_id = serializers.SerializerMethodField()
#     class Meta:
#         model = Stock
#         fields = '__all__'
#         depth=2
        
#     def get_ref_id(self, obj):
#         if obj.ref_tblname == 'Invoice':
#            return GSTReportsONLYInvoiceSerializer( Invoice.objects.get(invoice_id=obj.ref_id)).data
#         if obj.ref_tblname == 'Bill':
#            return GSTReportsONLYBillSerializer( Bill.objects.get(bill_id=obj.ref_id)).data
#         if obj.ref_tblname == 'DebitNote':
#            return GSTReportsONLYDebitnoteSerializer( DebitNote.objects.get(dn_id=obj.ref_id)).data
#         if obj.ref_tblname == 'Credit Note':
#                return GSTReportONLYCnSerializer( CreditNote.objects.get(cn_id=obj.ref_id)).data
       
       
            
       
#         return obj.ref_id