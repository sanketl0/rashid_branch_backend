# import uuid

# from django.db import models
# from django.utils.timezone import now

# from company.models import Company, Branch,Company_Year
# # from item.models import Item
# from .BaseModel import BaseDateid, BaseTaxAmount
# from .BaseModel import BaseTaxTotal

# # Base Tax Model GST Filed

# '''
# class BaseTaxTotal(models.Model):
#     cgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
#     sgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
#     igst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    
#     class Meta:
#         abstract=True

# class BaseTaxAmount(models.Model):
#     cgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
#     sgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
#     igst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
   
#     class Meta:
#         abstract=True
# '''


# # SalesCustomer
# class SalesCustomer(BaseDateid):
#     customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
#     salutation = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_mobile = models.CharField(max_length=15, blank=True, default='null', null=True)
#     company_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_display_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     print_as_check_as = models.BooleanField(default=False)
#     customer_contact = models.CharField(max_length=15, blank=True, default='null', null=True)
#     customer_email = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_designation = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_department = models.CharField(max_length=50, blank=True, default='null', null=True)
#     exemption_reason = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customerRefListId = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customerTypeRefListId = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customerTypeReffullName = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_subcustomer = models.BooleanField(default=False)
#     parent_customer = models.CharField(max_length=50, blank=True, default='null', null=True)
#     enable_portal = models.BooleanField(default=True)
#     company_display_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     company_email = models.EmailField(max_length=50, blank=True, default='null', null=True)
#     company_number = models.CharField(max_length=15, blank=True, default='null', null=True)
#     website = models.CharField(max_length=70, blank=True, default='null', null=True)
#     opening_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     currency = models.CharField(max_length=50, blank=True, default='null', null=True)
#     set_credit_limit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     gst_treatment = models.CharField(max_length=50, blank=True, default='null', null=True)
#     gstin_number = models.CharField(max_length=20, blank=True, default='null', null=True)
#     tax_preference = models.CharField(max_length=50, blank=True, default='null', null=True)
#     cin_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     trn_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vat_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     pan_number = models.CharField(max_length=20, blank=True, default='null', null=True)
#     b_attention = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address1 = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address2 = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address_city = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address_state = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address_postal_code = models.BigIntegerField(null=True, blank=True)
#     bill_address_country = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_contact_number = models.CharField(max_length=15, blank=True, default='null', null=True)
#     bill_fax_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     s_attention = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address1 = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address2 = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address_city = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address_state = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address_postal_code = models.BigIntegerField(null=True, blank=True)
#     ship_address_country = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_contact_number = models.CharField(max_length=15, blank=True, default='null', null=True)
#     ship_fax_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     contact_salutation = models.CharField(max_length=10, default='null', null=True, blank=True)
#     contact_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     contact_phone = models.CharField(max_length=15, blank=True, default='null', null=True)
#     contact_mobile = models.CharField(max_length=15, blank=True, default='null', null=True)
#     contact_email = models.EmailField(max_length=50, blank=True, default='null', null=True)
#     contact_designation = models.CharField(max_length=50, blank=True, default='null', null=True)
#     contact_department = models.CharField(max_length=50, blank=True, default='null', null=True)
#     remarks = models.CharField(max_length=100, blank=True, default='null', null=True)
#     term_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     no_of_days = models.IntegerField(blank=True, default=0, null=True)
#     is_verified=models.BooleanField(default=False)
#     invoice_template=models.FileField(default='null', blank=True, null=True)

#     class Meta:
#         verbose_name_plural = 'customer'

#     def __str__(self):
#         return self.customer_name


# class CustomerOB(BaseDateid):
#     ob_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True,
#                                     related_name='customer_balance')
#     opening_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     closing_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     available_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     debit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     migration_date = models.DateField(blank=True, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'Customer Opening Balance'

#     def __str__(self):
#         return 'opening_balanc'


# class Estimate(BaseTaxTotal, BaseDateid):
#     # class eststatus(models.Model):
#     #     STATUS=Choices(0, 'draft', _('draft')),
#     #     (1, 'submit', _('submit')),
#     #     (2, 'save', _('save'))
#     #     status = models.IntegerField(choices=STATUS, default=STATUS.draft)
#     est_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     so_id = models.ForeignKey("salescustomer.SO", on_delete=models.SET_NULL, null=True)
#     tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     est_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     est_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     est_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     est_date = models.DateField(blank=True, null=True)
#     is_estimate_generated = models.BooleanField(default=False)
#     expiry_date = models.DateField(blank=True, null=True)
#     project_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     subject = models.CharField(max_length=50, blank=True, default='null', null=True)
#     total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
#     shipping_tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tcs_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     round_off = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax = models.CharField(max_length=50, blank=True, default='null', null=True)
#     grand_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     attach_file = models.FileField(default='null', blank=True, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     convt_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_id = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_converted = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = 'estimate'

   


# class EstimatedItem(BaseTaxAmount, BaseDateid):
#     estitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True,
#                                related_name='estimate_items')
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     item_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     taxamount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'estimated item'

 


# class SO(BaseTaxTotal, BaseDateid):
#     so_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     customer_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     # so_no=models.CharField(max_length=50, blank=True, default='null', null=True)
#     so_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     so_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     so_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_so_generated = models.BooleanField(default=False)
#     so_date = models.DateField(blank=True, null=True)
#     expiry_date = models.DateField(blank=True, null=True)
#     expected_shipment_date = models.DateField(blank=True, null=True)
#     delivery_method = models.CharField(max_length=50, blank=True, default='null', null=True)
#     term_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     no_of_days = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     so_delete = models.CharField(max_length=50, blank=True, default='null', null=True)
#     # emp_role=models.CharField(max_length=50, blank=True, default='null', null=True)
#     project_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     subject = models.CharField(max_length=50, blank=True, default='null', null=True)
#     round_off = models.IntegerField(default=0, blank=True, null=True)
#     tax = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tcs = models.CharField(max_length=50, blank=True, default='null', null=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
#     shipping_tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     attach_file = models.FileField(default='null', blank=True, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     est_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_id = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_converted = models.BooleanField(default=False)
#     TxnID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ClassRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     CustomerMsgRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     CustomerRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     CustomerSalesTaxCodeRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ItemSalesTaxRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     SalesRepRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ShipMethodRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     TemplateRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     TermsRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Sales Order'

    


# class SoItem(BaseTaxAmount, BaseDateid):
#     soitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     so_id = models.ForeignKey("salescustomer.SO", on_delete=models.SET_NULL, null=True, related_name='so_items')
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     item_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     taxamount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'So Item'

 


# class Invoice(BaseDateid):
#     invoice_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True,
#                                     related_name='customer_invoices')
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     invoice_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     invoice_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     invoice_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     invoice_date = models.DateField(blank=True, null=True)
#     is_invoice_generated = models.BooleanField(default=False)
#     payment_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount_received = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     order_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     due_date = models.DateField(blank=True, null=True)
#     delivery_method = models.CharField(max_length=50, blank=True, default='null', null=True)
#     term_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     no_of_days = models.IntegerField(default=0, blank=True, null=True)
#     project_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     subject = models.CharField(max_length=50, blank=True, default='null', null=True)
#     total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     cgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     sgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     igst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
#     shipping_tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tcs_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     payment_mode = models.CharField(max_length=50, blank=True, default='null', null=True)
#     deposit_to = models.CharField(max_length=50, blank=True, default='null', null=True)
#     payment_received = models.BooleanField(default=False)
#     round_off = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax = models.CharField(max_length=50, blank=True, default='null', null=True)
#     grand_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     attach_file = models.FileField(default='null', blank=True, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     convt_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_id = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_converted = models.BooleanField(default=False)
#     TermsRefFullName = models.CharField(max_length=50, blank=True, default='null', null=True)
#     TermsRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         ordering = ('-due_date',)
#         verbose_name_plural = 'Invoice'
#         # ordering=('date')

#     def __str__(self):
#         return str(self.invoice_id)


# class InvoiceItem(BaseDateid):
#     invoiceitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True,
#                                    related_name='invoice_items')
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
#     item_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     taxamount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     cgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     sgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     igst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'invoice item'

#     def __str__(self):
#         return self.item_name


# class InvoiceJournalTransaction(BaseDateid):
#     invoicejt_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True,
#                                    related_name='transactions')
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     date = models.DateField(blank=True, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True, related_name='invoice_coa')
#     transaction_type = models.CharField(max_length=50, default='Invoice', null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
#     type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     debit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     credit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)

#     class Meta:
#         verbose_name_plural = 'invoice journal transaction'

#     def __str__(self):
#         return self.type


# class PaymentMode(BaseDateid):
#     payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     payment_mode = models.CharField(max_length=50, blank=True, default='null', null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'payment mode'

#     def __str__(self):
#         return self.payment_mode


# class DC(BaseTaxTotal, BaseDateid):
#     dc_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True,
#                                    related_name='invoice_dc')
#     so_id = models.ForeignKey("salescustomer.SO", on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     is_converted = models.BooleanField(default=False)
#     is_dc_generated = models.BooleanField(default=False)
#     customer_note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     dc_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     dc_date = models.DateTimeField(default=now, null=True)
#     dc_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     dc_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     dc_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     terms_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     so_delete = models.CharField(max_length=50, blank=True, default='null', null=True)
#     emp_role = models.CharField(max_length=50, blank=True, default='null', null=True)
#     subject = models.CharField(max_length=50, blank=True, default='null', null=True)
#     item_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     round_off = models.IntegerField(default=0, blank=True, null=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     attach_file = models.FileField(default='null', blank=True, null=True)
#     convt_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_id = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Delivery Challan'

#     def __str__(self):
#         return self.item_name


# class DcItem(BaseTaxAmount, BaseDateid):
#     dcitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     dc_id = models.ForeignKey("salescustomer.DC", on_delete=models.SET_NULL, null=True, related_name='dc_items')
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     item_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     taxamount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'Dc item'

#     def __str__(self):
#         return self.item_name


# class PR(BaseDateid):
#     pr_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
#     so_id = models.ForeignKey("salescustomer.SO", on_delete=models.SET_NULL, null=True)
#     dc_id = models.ForeignKey("salescustomer.DC", on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True,
#                                     related_name='customer_payment')
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
#     amount_received = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     bank_id = models.ForeignKey("banking.Banking", on_delete=models.SET_NULL, null=True)
#     form_type = models.CharField(max_length=50, blank=True, default='Payment Receive', null=True)
#     is_bank_transaction = models.BooleanField(default=False)
#     bank_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     payment_date = models.DateField(blank=True, null=True)
#     deposit_to = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_deducted = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tds_tax_account = models.CharField(max_length=50, blank=True, default='null', null=True)
#     date = models.DateField(blank=True, null=True)
#     invoice_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     # withholding_tax=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     # amount_refunded=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True) new table
#     amount_excess = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount_used_payment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     is_converted = models.BooleanField(default=False)
#     pay_generated = models.BooleanField(default=False)
#     payment_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     payment_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     invoice_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     invoice_date = models.DateField(blank=True, null=True)
#     pay_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     payment_mode = models.CharField(max_length=50, blank=True, default='null', null=True)
#     pay_method = models.CharField(max_length=50, blank=True, default='null', null=True)
#     payment_terms = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     notes = models.CharField(max_length=50, blank=True, default='null', null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     attach_file = models.FileField(max_length=250, blank=True, default='null', null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     PreferredPaymentMethodRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     PaymentMethodRefListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     PaymentMethodRefFullName = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ListID = models.CharField(max_length=50, blank=True, default='null', null=True)
#     EditSequence = models.CharField(max_length=50, blank=True, default='null', null=True)
#     Name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     IsActive = models.BooleanField(default=False)
#     CreditCardNumber = models.IntegerField(default=0)
#     CreditCardExpirationMonth = models.CharField(max_length=50, blank=True, default='null', null=True)
#     CreditCardExpirationYear = models.CharField(max_length=50, blank=True, default='null', null=True)
#     CreditCardNameOnCard = models.CharField(max_length=50, blank=True, default='null', null=True)
#     CreditCardAddress = models.CharField(max_length=50, blank=True, default='null', null=True)
#     CreditCardPostalCode = models.IntegerField(default=0)

#     class Meta:
#         verbose_name_plural = 'Payment Receive'

#     def __str__(self):
#         return str(self.pr_id)


# class PaymentTransaction(BaseDateid):
#     paymenttrans_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     pr_id = models.ForeignKey("salescustomer.PR", on_delete=models.SET_NULL, null=True,
#                               related_name='payment_transactions')
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     date = models.DateField(blank=True, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True, related_name='pr_coa')
#     bank_id = models.ForeignKey("banking.Banking", on_delete=models.SET_NULL, null=True)
#     form_type = models.CharField(max_length=50, blank=True, default='Payment Receive', null=True)
#     status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     transaction_type = models.CharField(max_length=50, default='Invoice Payment', null=True)
#     transaction_module = models.CharField(max_length=50, default='null', null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     debit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     credit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     type = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Payment Transaction'

#     def __str__(self):
#         return self.type


# class CreditNote(BaseTaxTotal, BaseDateid):
#     cn_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True,
#                                     related_name='customer_data')
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     pay_id = models.ForeignKey("salescustomer.PR", on_delete=models.SET_NULL, null=True)
#     customer_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_email = models.EmailField(max_length=50, blank=True, default='null', null=True)
#     reason = models.CharField(max_length=50, blank=True, default='null', null=True)
#     subject = models.CharField(max_length=50, blank=True, default='null', null=True)
#     received_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     received_date = models.DateTimeField(default=now, null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     cn_date = models.DateTimeField(default=now, null=True)
#     is_bank_transaction = models.BooleanField(default=False)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     shipping_tax_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tcs_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     invoice_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_cn_converted = models.BooleanField(default=False)
#     is_cn_generated = models.BooleanField(default=False)
#     attach_file = models.FileField(default='null', blank=True, null=True)
#     status = models.CharField(max_length=50, blank=True, default='Open', null=True)
#     cn_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     cn_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     cn_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_id = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Credit Note'

    

# class CreditItem(BaseTaxAmount, BaseDateid):
#     cnitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     cn_id = models.ForeignKey("salescustomer.CreditNote", on_delete=models.SET_NULL, null=True,
#                               related_name='credit_note_items')
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
#     item_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     selected_item_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     selected_tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     taxamount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'Credit Item'

    

# class CreditNoteTransaction(BaseDateid):
#     credittrans_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     cn_id = models.ForeignKey("salescustomer.CreditNote", on_delete=models.SET_NULL, null=True,
#                               related_name='creditnotetransaction')
#     pr_id = models.ForeignKey("salescustomer.PR", on_delete=models.SET_NULL, null=True)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     date = models.DateField(blank=True, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True, related_name='cn_coa')
#     transaction_type = models.CharField(max_length=50, default='Credit Note', null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     debit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     credit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     type = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Credit Journal Transaction'

#     def __str__(self):
#         return str(self.amount)


# class RI(BaseDateid):
#     ri_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
#     emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     customer_name = models.CharField(max_length=50)
#     so_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     invoice_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ri_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ri_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ri_generated = models.BooleanField()
#     profile_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     repeat_every = models.CharField(max_length=50, blank=True, default='null', null=True)
#     never_expire = models.BooleanField(default=False)
#     associated_project_hrs = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     order_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     start_date = models.DateField(blank=True, null=True)
#     end_date = models.DateField(blank=True, null=True)
#     payment_terms = models.CharField(max_length=50, blank=True, default='null', null=True)
#     emp_role = models.CharField(max_length=50, blank=True, default='null', null=True)
#     item_name = models.CharField(max_length=70)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     round_off = models.IntegerField(default=0)
#     tax = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tcs = models.CharField(max_length=50, blank=True, default='null', null=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     customer_note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     attach_file = models.FileField(default='please upload file')
#     customer_email = models.EmailField(max_length=50, blank=True, default='null', null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     ri_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_converted = models.BooleanField()
#     convt_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_id = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Recurring Invoice'

#     def __str__(self):
#         return self.customer_name


# class Employee(BaseDateid):
#     emp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     emp_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     emp_email = models.EmailField(max_length=50, blank=True, default='null', null=True)
#     emp_phone = models.CharField(max_length=15, blank=True, default='null', null=True)
#     emp_mobile = models.CharField(max_length=15, blank=True, default='null', null=True)
#     emp_role = models.CharField(max_length=50, blank=True, default='null', null=True)
#     emp_address = models.CharField(max_length=200, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Employee'

#     def __str__(self):
#         return self.emp_role


# class PaymentTerms(models.Model):
#     payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     term_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     no_of_days = models.IntegerField(blank=True, default=0, null=True)

#     class Meta:
#         verbose_name_plural = 'Payment Terms'

#     def __str__(self):
#         return self.term_name


# class TCS(models.Model):
#     tcs_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     nature_of_collection = models.CharField(max_length=50, blank=True, default='null', null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tcs_payable_account = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tcs_receivable_account = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'TCS'

#     def __str__(self):
#         return self.tax_name
