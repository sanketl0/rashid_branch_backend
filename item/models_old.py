# from django.db import models
# from company.models import Company, Branch,Company_Year
# # from salescustomercustomer.models import salescustomerCustomer
# from django.utils.timezone import now
# import uuid
# from salescustomer.BaseModel import *

# from django.db.models import Sum

# # Create your models here.
# class Item(BaseDateid):
#     item_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_items')
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True, related_name='item_data')
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
#     tax_id = models.ForeignKey("item.TaxName", on_delete=models.SET_NULL, null=True)
#     ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
#     # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
#     item_category = models.CharField(max_length=50, blank=True, null=True)
#     name = models.CharField(max_length=50, default='null', blank=True, null=True)
#     sku = models.CharField(max_length=50, default='null', blank=True, null=True)
#     sac = models.CharField(max_length=50, default='null', blank=True, null=True)
#     hsn_code = models.CharField(max_length=50, default='null', blank=True, null=True)
#     unit = models.CharField(max_length=50, default='null', blank=True, null=True)
#     category = models.CharField(max_length=50, default='null', blank=True, null=True)
#     tax_preference = models.CharField(max_length=50, default='null', blank=True, null=True)
#     item_description = models.CharField(max_length=50, default='null', blank=True, null=True)
#     sale_price = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
#     sales_account = models.CharField(max_length=50, default='null', blank=True, null=True)
#     sale_description = models.TextField(max_length=50, default='null', blank=True, null=True)
#     cost_price = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
#     purchase_account = models.CharField(max_length=50, default='null', blank=True, null=True)
#     purchase_description = models.TextField(max_length=50, default='null', blank=True, null=True)
#     inventory_account = models.CharField(max_length=50, default='null', blank=True, null=True)
#     inter_rate = models.CharField(max_length=50, blank=True, null=True)
#     intra_rate = models.CharField(max_length=50, blank=True, null=True)
#     opening_stock = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
#     opening_stock_rate = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
#     reorder_point = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
#     preferred_vendor = models.CharField(max_length=50, blank=True, null=True)
#     date = models.DateField(blank=True, null=True)
#     exemption_reason = models.CharField(max_length=100, blank=True, null=True)
#     track_inventory= models.BooleanField(blank=True, null=True)
#     total= models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
#     class Meta:
#         # db_table = "item"
#         verbose_name_plural = 'Item'




# class ItemDetails(BaseDateid):
#     item_details_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     company_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     branch_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     tax_id = models.ForeignKey("item.TaxName", on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     is_estimate_generated = models.BooleanField(blank=False, null=True)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
#     est_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     est_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
#     is_so_generated = models.BooleanField(blank=False, null=True)
#     so_id = models.ForeignKey("salescustomer.SO", on_delete=models.SET_NULL, null=True)
#     so_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     so_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
#     is_dc_generated = models.BooleanField(blank=True, null=True)
#     dc_id = models.ForeignKey("salescustomer.DC", on_delete=models.SET_NULL, null=True)
#     dc_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     dc_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
#     is_invoice_generated = models.BooleanField(blank=False, null=True)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     invoice_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     invoice_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
#     is_ri_generated = models.BooleanField(blank=False, null=True)
#     is_enable = models.BooleanField(blank=False, null=True)
#     ri_id = models.ForeignKey("salescustomer.RI", on_delete=models.SET_NULL, null=True)
#     ri_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     ri_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
#     is_crn_generated = models.BooleanField(blank=False, null=True)
#     crn_id = models.ForeignKey("salescustomer.CreditNote", on_delete=models.SET_NULL, null=True)
#     crn_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     crn_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
#     # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
#     exemption_reason = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         verbose_name_plural = 'Item Details'

#     def __str__(self):
#         return self.company_name


# class TaxName(BaseDateid):
#     tax_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     type = models.CharField(max_length=50, blank=True, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, null=True)
#     # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
#     rate = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         verbose_name_plural = 'Tax Name'

#     def __str__(self):
#         return self.tax_name


# class TaxGroup(BaseDateid):
#     taxgroup_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     group_name = models.CharField(max_length=50, blank=True, null=True)
#     tax_id1 = models.CharField(max_length=50, blank=True, null=True)
#     tax_id2 = models.CharField(max_length=50, blank=True, null=True)

#     # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'Tax Group'

#     def __str__(self):
#         return self.group_name


# class TaxExemption(BaseDateid):
#     taxexemp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     exemption_reason = models.CharField(max_length=50, blank=True, null=True)
#     exemption_code = models.CharField(max_length=50, blank=True, null=True)
#     alias = models.CharField(max_length=50, blank=True, null=True)
#     type = models.CharField(max_length=50, blank=True, null=True)

#     # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'Tax Exemption'

#     def __str__(self):
#         return self.alias


# class InventoryAdjust(BaseDateid):
#     invadj_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     # customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
#     invadj_ref_no = models.CharField(max_length=50)
#     item_code1 = models.CharField(max_length=50, blank=True, null=True)
#     item_code2 = models.CharField(max_length=50, blank=True, null=True)
#     date = models.DateField(blank=True, null=True)
#     account = models.CharField(max_length=50, blank=True, null=True)
#     exemption_reason = models.CharField(max_length=100, blank=True, null=True)
#     branch_name = models.CharField(max_length=50, blank=True, null=True)
#     description = models.CharField(max_length=50, blank=True, null=True)
#     item_name = models.CharField(max_length=50, blank=True, null=True)
#     quantity_available = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     new_quantity_on_hand = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     quantity_adjusted = models.IntegerField(blank=True, null=True)
#     purchase_price = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     cost_price = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     current_value = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     changed_value = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjusted_value = models.IntegerField(blank=True, null=True)

#     class Meta:
#         verbose_name_plural = 'Inventory Adjustment'

#     def __str__(self):
#         return self.item_name
    



# #Stock Table Section
# class Stock(BaseDateid):
#     st_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     item_id =models.CharField(max_length=50, default='null', blank=True, null=True)
#     item_name =models.CharField(max_length=50, default='null', blank=True, null=True)
#     ref_id =models.CharField(max_length=50, default='null', blank=True, null=True)
#     ref_tblname =models.CharField(max_length=50, default='null', blank=True, null=True)
#     stock_in=models.IntegerField(default=0)
#     stock_out=models.IntegerField(default=0)
#     quantity=models.IntegerField(default=0)
#     module=models.CharField(max_length=50, default='null', blank=True, null=True)
#     formname=models.CharField(max_length=50, default='null', blank=True, null=True)
#     stage= models.CharField(max_length=50, default='null', blank=True, null=True)
#     date = models.DateField(blank=True, null=True)
#     warehouse_id=models.CharField(max_length=50, default='null', blank=True, null=True)
#     #stock_on_hand=models.IntegerField(default=0)
#     adjusted_qty=models.IntegerField(default=0)
#     changed_value= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjusted_value= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     current_value= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     class Meta:
#             verbose_name_plural = 'Stock'
    
# def getstock_on_hand(item_id):
#     sum_stok_in=Stock.objects.filter(item_id=item_id).aggregate(Sum('stock_in'))
#     print(type(sum_stok_in.values()))
#     print('Yeee Stokin is herer',sum_stok_in)
#     sum_stok_out=Stock.objects.filter(item_id=item_id).aggregate(Sum('stock_out')) 
#     stock_on_hand= sum_stok_in['stock_in__sum'] - sum_stok_out['stock_out__sum']
#     return stock_on_hand

# #Adjustment Table
# class Adjustment(BaseDateid):
#     adj_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     adj_type= models.CharField(max_length=50, default='null', blank=True, null=True)
#     ref_no= models.CharField(max_length=50, default='null', blank=True, null=True)
#     adj_date = models.DateField(blank=True, null=True)
#     coa_id= models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
#     reason= models.CharField(max_length=50, default='null', blank=True, null=True)
#     description= models.CharField(max_length=50, default='null', blank=True, null=True)
#     attach_file = models.FileField(default='null', blank=True, null=True)
#     status= models.CharField(max_length=50, default='null', blank=True, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     warehouse_id=models.CharField(max_length=50, default='null', blank=True, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     adjusted_qty=models.IntegerField(default=0,null=True)
#     changed_value= models.IntegerField(default=0,null=True)
#     amount= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjusted_value= models.IntegerField(default=0,null=True)
#     current_value= models.IntegerField(default=0,null=True)

    
#     class Meta:
#             verbose_name_plural = 'Adjustment'

#     def __str__(self):
#         return self.adj_id

# class AdjustmentItem(BaseDateid):
#     adjitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     coa_id= models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
#     adj_id= models.ForeignKey(Adjustment, on_delete=models.SET_NULL, null=True, related_name='adj_items')
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     warehouse_id=models.CharField(max_length=50, default='null', blank=True, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     adjusted_qty=models.IntegerField(default=0,null=True)
#     changed_value= models.IntegerField(default=0,null=True)
#     amount= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjusted_value= models.IntegerField(default=0,null=True)
#     current_value= models.IntegerField(default=0,null=True)
#     item_id =models.CharField(max_length=50, default='null', blank=True, null=True)
#     item_name =models.CharField(max_length=50, default='null', blank=True, null=True)