# from django.db import models
# from company.models import Company, Branch,Company_Year
# from item.models import Item
# # from .models import *  # Invoice, SO, Estimate
# from django.utils.timezone import now
# import uuid
# from salescustomer.models_old import BaseTaxAmount, BaseTaxTotal
# from salescustomer.BaseModel import BaseDateid


# #  Create your models here.
# class Vendor(BaseDateid):
#     vendor_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_vendor')
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     # vendorRefListId = models.CharField(max_length=50, blank=True, default='null', null=True)
#     # VendorRefFullName= models.CharField(max_length=50, blank=True, default='null', null=True)
#     # VendorTaxIdent= models.CharField(max_length=50, blank=True, default='null', null=True)
#     salutation = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vendor_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vendor_mobile = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vendor_display_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     # print_as_check_as = models.BooleanField()
#     vendor_contact = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vendor_email = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vendor_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vendor_designation = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vendor_department = models.CharField(max_length=50, blank=True, default='null', null=True)
#     # vendorTypeRefListId = models.CharField(max_length=50, blank=True, default='null', null=True)
#     # vendorTypeReffullName = models.CharField(max_length=50, blank=True, default='null', null=True)    
#     parent_vendor = models.CharField(max_length=50, blank=True, default='null', null=True)
#     enable_portal = models.BooleanField(default=False)
#     company_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     company_display_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     company_email = models.EmailField(max_length=50, blank=True, default='null', null=True)
#     company_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     website = models.CharField(max_length=50, blank=True, default='null', null=True)
#     opening_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     currency = models.CharField(max_length=50, blank=True, default='null', null=True)
#     payment_terms = models.CharField(max_length=50, blank=True, default='null', null=True)
#     term_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     no_of_days = models.IntegerField(default=0)
#     set_credit_limit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     gst_treatment = models.CharField(max_length=50, blank=True, default='null', null=True)
#     gstin_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_preference = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tds = models.CharField(max_length=50, blank=True, default='null', null=True)
#     cin_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     trn_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vat_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     pan_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     b_attention = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address1 = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address2 = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address_city = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address_state = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_address_postal_code = models.BigIntegerField(null=True, blank=True)
#     bill_address_country = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_contact_number = models.CharField(max_length=15, blank=True, default='null', null=True)
#     bill_fax_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     # BillingRateRefListID=models.CharField(max_length=50, blank=True, default='null', null=True)
#     # BillingRateRefFullName=models.CharField(max_length=50, blank=True, default='null', null=True)
#     s_attention = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address1 = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address2 = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address_city = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address_state = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_address_postal_code = models.BigIntegerField(null=True, blank=True)
#     ship_address_country = models.CharField(max_length=50, blank=True, default='null', null=True)
#     ship_contact_number = models.CharField(max_length=15, blank=True, default='null', null=True)
#     ship_fax_number = models.CharField(max_length=50, blank=True, default='null', null=True)
#     source_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_prefrances = models.CharField(max_length=50, blank=True, default='null', null=True)
#     exemption_reason = models.CharField(max_length=50, blank=True, default='null', null=True)
#     remarks = models.CharField(max_length=100, blank=True, default='null', null=True)
#     is_verified=models.BooleanField(default=False)
#     bill_template=models.FileField(default='null', blank=True, null=True)

#     class Meta:
#         verbose_name_plural = 'Vendor'
#         # db_table = "Vendor"

#     def __str__(self):
#         return self.vendor_name


# class VendorContact(BaseDateid):
#     contact_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='contact_person')
#     contact_salutation = models.CharField(max_length=50, blank=True, default='null', null=True)
#     contact_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     contact_phone = models.CharField(max_length=30, blank=True, default='null', null=True)
#     contact_mobile = models.CharField(max_length=30, blank=True, default='null', null=True)
#     contact_email = models.EmailField(max_length=50, blank=True, default='null', null=True)
#     contact_designation = models.CharField(max_length=50, blank=True, default='null', null=True)
#     contact_department = models.CharField(max_length=50, blank=True, default='null', null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'Vendor Contact'
#         # db_table = "Vendor"

#     def __str__(self):
#         return str(self.vendor_id)


# class TDS(BaseDateid):
#     tds_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     tds_section = models.CharField(max_length=50, blank=True, default='null', null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tds_payable_account = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tds_receivable_account = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'TDS'

#     def __str__(self):
#         return self.tax_name


# class Bill(BaseDateid,BaseTaxTotal,BaseTaxAmount):
#     bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor_bills')
#     # customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     is_bill_generate = models.BooleanField(default=False)
#     bill_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     payment_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='Company_bills')
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     bill_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     order_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_date = models.DateField(blank=True, null=True)
#     due_date = models.DateField(blank=True, null=True)
#     discount_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_Type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     # ayment_mode=models.CharField(max_length=50, blank=True, default='null', null=True)
#     sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     # cgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     # sgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     # igst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
#     tds_id = models.ForeignKey(TDS, on_delete=models.SET_NULL, null=True)
#     notes = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tcs_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tds_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     discount_account = models.CharField(max_length=50, blank=True, default='null', null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     term_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     no_of_days = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     packing_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     select_tax = models.CharField(max_length=50, blank=True, default='null', null=True)
#     attach_file = models.FileField(max_length=250, blank=True, default='null', null=True)
#     OpenAmount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     AmountIncludesVAT = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_id = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_converted = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = 'Bills'

#     def __str__(self):
#         return str(self.vendor_id)


# class Bill_Item(BaseTaxAmount,BaseTaxTotal,BaseDateid):
#     billitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     bill_id = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, related_name='bill_items')
#     item_name = models.CharField(max_length=50, default='null', blank=True, null=True)
#     quantity =  models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
#     tax_name = models.CharField(max_length=50, default='null', blank=True, null=True)
#     tax_rate = models.CharField(max_length=50, default='null', blank=True, null=True)
#     tax_type = models.CharField(max_length=50, default='null', blank=True, null=True)
#     account_name = models.CharField(max_length=50, default='null', blank=True, null=True)
#     taxamount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)

#     # cgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     # sgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     # igst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)

#     class Meta:
#         verbose_name_plural = 'bill item'

#     def __str__(self):
#         return self.item_name


# class BillJournalTransaction(BaseDateid):
#     billjt_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     bill_id = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, related_name='bill_journal_trasaction')
#     item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True, related_name='bill_coa')
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
#     date = models.DateField(blank=True, null=True)
#     transaction_type = models.CharField(max_length=50, default='Bill', null=True)
#     type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     debit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     credit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)

#     class Meta:
#         verbose_name_plural = 'bill journal transaction'

#     def __str__(self):
#         return self.type


# class PaymentMade(BaseDateid):
#     pm_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor_paymentmade')
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_paymentmade')
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     bill_id = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, related_name='bill_paymentmade')
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     bank_id = models.ForeignKey("banking.Banking", on_delete=models.SET_NULL, null=True)
#     form_type = models.CharField(max_length=50, blank=True, default='Payment Made', null=True)
#     is_bank_transaction = models.BooleanField(default=False)
#     status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     payment_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
#     payment_mode = models.CharField(max_length=50, default='null', blank=True, null=True)
#     # coa_id=models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True,related_name='coa_paymentmade')
#     payment_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     amount_payable = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     payment_date = models.DateField(blank=True, null=True)
#     bill_date = models.DateTimeField(default=now, null=True)
#     bill_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount_excess = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     note = models.CharField(max_length=50, default='null', blank=True, null=True)
#     paid_through = models.CharField(max_length=50, default='null', blank=True, null=True)
#     amount_received = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amt_for_payment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amt_refunded = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     is_converted = models.BooleanField(default=False)
#     pay_generated = models.BooleanField(default=False)
#     payment_status = models.CharField(max_length=50, default='null', blank=True, null=True)
#     pm_method = models.CharField(max_length=50, default='null', blank=True, null=True)
#     pm_terms = models.CharField(max_length=50, default='null', blank=True, null=True)
#     terms_condition = models.CharField(max_length=50, default='null', blank=True, null=True)
#     # refunded_on=models.DateTimeField(default=now)
#   #  description_of_supply = models.CharField(max_length=150)
#     refund = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#   #  source_os_supply = models.CharField(max_length=150)
#     destination_of_supply = models.CharField(max_length=50, default='null', blank=True, null=True)
#     reverse_charge = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     deposit_to = models.CharField(max_length=50, default='null', blank=True, null=True)
#     amount_to_credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     tds_to_credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_amount_to_credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     remaining_credits = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     attach_file = models.FileField(default='null', blank=True, null=True)

#     class Meta:
#         verbose_name_plural = 'Payment Made'

#     def __str__(self):
#         return str(self.pm_id)


# class PaymentmadeJournalTransaction(BaseDateid):
#     paymentmadeJT_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     pm_id = models.ForeignKey(PaymentMade, on_delete=models.SET_NULL, null=True,
#                               related_name='paymentmade_transactions')
#     bill_id = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True, related_name='pm_coa')
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
#     date = models.DateField(blank=True, null=True)
#     bank_id = models.ForeignKey("banking.Banking", on_delete=models.SET_NULL, null=True)
#     form_type = models.CharField(max_length=50, blank=True, default='Payment Made', null=True)
#     status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     transaction_type = models.CharField(max_length=50, default='Payment Made', null=True)
#     transaction_module = models.CharField(max_length=50, default='null', null=True)
#     type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     debit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     credit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)

#     class Meta:
#         verbose_name_plural = 'paymentmade journal transaction'

#     def __str__(self):
#         return self.type


# class ExpenseRecord(BaseTaxAmount):
#     er_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     # item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     bank_id = models.ForeignKey("banking.Banking", on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
#     # po = models.ForeignKey("purchase.PO", on_delete=models.SET_NULL, null=True)
#     expense_date = models.DateTimeField(default=now, null=True)
#     expense_account = models.CharField(max_length=50, blank=True, default='null', null=True)
#     expense_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     expense_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     expense_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     invoice_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
#     expense_status = models.CharField(max_length=50, default='null', blank=True, null=True)
#     is_expense_generated = models.BooleanField(default=False)
#     #  amount=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     paid_through = models.CharField(max_length=50, default='null', blank=True, null=True)
#     notes = models.CharField(max_length=50, default='null', blank=True, null=True)
#     gst_treatment = models.CharField(max_length=50, default='null', blank=True, null=True)
#     vendor_gstin = models.CharField(max_length=50, default='null', blank=True, null=True)
#     supply_place = models.CharField(max_length=50, default='null', blank=True, null=True)
#     destination_place = models.CharField(max_length=50, default='null', blank=True, null=True)
#     # reverse_charge=models.BooleanField(default=False)
#     attach_file = models.FileField(default='null', blank=True, null=True)
#     reporting_tag = models.CharField(max_length=50, default='null', blank=True, null=True)
#     account = models.CharField(max_length=50, default='null', blank=True, null=True)
#     sales_tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     total_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     item_details = models.CharField(max_length=50, default='null', blank=True, null=True)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     customer_details = models.CharField(max_length=50, default='null', blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     expense_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     status = models.CharField(max_length=50, default='null', blank=True, null=True)
#     sac = models.CharField(max_length=50, default='null', blank=True, null=True)
#     hsn_code = models.CharField(max_length=50, default='null', blank=True, null=True)
#     tax_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     tax_percentage = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
#     class Meta:
#         verbose_name_plural = 'Expense Record'
#         # db_table = "RecordExpenses"

#     def __str__(self):
#         return str(self.vendor_id)


# class ExpenseJournalTransaction(BaseDateid):
#     expensejt_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     er_id = models.ForeignKey(ExpenseRecord, on_delete=models.SET_NULL, null=True, related_name='expense_transactions')
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True, related_name='er_coa')
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
#     transaction_type = models.CharField(max_length=50, default='Expence Payment', null=True)
#     date = models.DateField(blank=True, null=True)
#     type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     debit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     credit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)

#     class Meta:
#         verbose_name_plural = 'expense journal transaction'

#     def __str__(self):
#         return self.type


# # Purchase Order Model
# class PO(BaseDateid,BaseTaxTotal,BaseTaxAmount):  # BaseTaxTotal
#     po_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     is_po_generated = models.BooleanField(default=False)
#     po_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_po')
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     po_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     po_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     po_date = models.DateField(blank=True, null=True)
#     po_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     supply_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     destination_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     term_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     no_of_days = models.CharField(max_length=50, blank=True, default='null', null=True)
#     shipment_preference = models.CharField(max_length=50, blank=True, default='null', null=True)
#     discount_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     sub_total = models.CharField(max_length=50, blank=True, default='null', null=True)
#     total = models.CharField(max_length=50, blank=True, default='null', null=True)
#     entered_discount = models.CharField(max_length=50, blank=True, default='null', null=True)
#     discount = models.CharField(max_length=50, blank=True, default='null', null=True)
#     customer_note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
#     tcs_amount = models.CharField(max_length=50, blank=True, default='null', null=True)
#     expected_delivery_date = models.DateField(blank=True, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     attach_file = models.FileField(max_length=150, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'purchase order'

#     def __str__(self):
#         return str(self.po_id)


# # Model of Purchase item
# class PoItem(BaseDateid,BaseTaxAmount,BaseTaxTotal):  # BaseTaxAmount
#     poitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     item_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
#     tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_rate = models.CharField(max_length=50, blank=True, default='null', null=True)
#     tax_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     taxamount = models.CharField(max_length=50, blank=True, default='null', null=True)
#     po_id = models.ForeignKey(PO, on_delete=models.SET_NULL, null=True, related_name='po_items')
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'purchase item'

#     def __str__(self):
#         return str(self.po_id)


# class DebitNote(BaseDateid,BaseTaxTotal,BaseTaxAmount):  # BaseTaxTotal):
#     dn_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     # customer_id=models.ForeignKey("sales.Customer", on_delete=models.SET_NULL, null=True)
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     # emp_id=models.ForeignKey("sales.Employee", on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True, related_name="ven_debitnote")
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     bill_id = models.ForeignKey("purchase.Bill", on_delete=models.SET_NULL, null=True)
#     source_place = models.CharField(max_length=50, blank=True, default='null', null=True)
#     supply_destination = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     bill_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     order_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     dn_date = models.DateTimeField(default=now, null=True)
#     discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     terms_condition = models.CharField(max_length=50, blank=True, default='null', null=True)
#     note = models.CharField(max_length=50, blank=True, default='null', null=True)
#     status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     is_dn_converted = models.BooleanField(default=False)
#     is_dn_generated = models.BooleanField(default=False)
#     dn_status = models.CharField(max_length=50, blank=True, default='null', null=True)
#     dn_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     dn_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_type = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_id = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
#     convt_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
#     discount_account = models.CharField(max_length=50, blank=True, default='null', null=True)
#     attach_file = models.FileField(max_length=150, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Debit Note'

#     def __str__(self):
#         return str(self.dn_id)


# class DebitItem(BaseDateid,BaseTaxAmount,BaseTaxTotal):  # BaseTaxAmount
#     dnitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     dn_id = models.ForeignKey("purchase.DebitNote", on_delete=models.SET_NULL, null=True,
#                               related_name='debit_note_items')
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
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
#     vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name_plural = 'debit item'


# class DebitNoteTransaction(BaseDateid):
#     debittrans_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     dn_id = models.ForeignKey("purchase.DebitNote", on_delete=models.SET_NULL, null=True,
#                               related_name='debitnote_transactions')
#     pm_id = models.ForeignKey("purchase.PaymentMade", on_delete=models.SET_NULL, null=True)
#     invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
#     date = models.DateField(blank=True, null=True)
#     item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
#     coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True, related_name='dn_coa')
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     debit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     credit = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     transaction_type = models.CharField(max_length=50, default='Debit Note', null=True)
#     type = models.CharField(max_length=50, blank=True, default='null', null=True)

#     class Meta:
#         verbose_name_plural = 'Debit Journal Transaction'

#     def __str__(self):
#         return str(self.amount)
# # class ExpenseMileage(models.Model):
# #     mileage_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
# #     exp_id = models.ForeignKey(ExpenseRecord, on_delete=models.SET_NULL, null=True)
# #     item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
# #     invoice_id = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
# #     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
# #     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
# #     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)    
# #     #po_id = models.ForeignKey(PO, on_delete=models.SET_NULL, null=True)
# #     so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)    
# #     associate_employee= models.CharField(max_length=50)
# #     mileage_category= models.CharField(max_length=50)
# #     default_unit= models.CharField(max_length=50)
# #     start_date=models.DateTimeField(default=now)
# #     mileage_rate=models.DateTimeField(default=now)
# #     date=models.DateTimeField(default=now)    
# #     calculating_mileage_using=models.CharField(max_length=50)
# #     distance_amount=models.FloatField()
# #     paid_through= models.CharField(max_length=150)
# #     amount=models.FloatField()
# #     vendor_name= models.CharField(max_length=50)
# #     customer_name= models.CharField(max_length=50)
# #     notes= models.CharField(max_length=150)
# #     report_tag= models.CharField(max_length=50)
# #     invoice_no= models.CharField(max_length=50)
# #     attach_file= models.FileField()
# #     mileage_serial=models.CharField(max_length=100)
# #     created_id=models.CharField(max_length=50)
# #     created_date=models.DateTimeField(default=now)
# #     modified_id=models.CharField(max_length=50)
# #     modified_date=models.DateTimeField(auto_now=True)
# #     deleted_id=models.CharField(max_length=50)
# #     deleted_date=models.DateTimeField(default=now)
# #     class Meta:
# #         verbose_name_plural = 'Record Mileage' 
# #         db_table = "RecordMileage"    
# #     def __str__(self):
# #         return self.vendor_name

# # class ExpenseBulk(models.Model):
# #     bulk_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
# #     exp_id = models.ForeignKey(ExpenseRecord, on_delete=models.SET_NULL, null=True)
# #     item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
# #     invoice_id = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
# #     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
# #     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
# #     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)    
# #     #po_id = models.ForeignKey(PO, on_delete=models.SET_NULL, null=True)
# #     so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)    
# #     date=models.DateTimeField(default=now)
# #     expense_account= models.CharField(max_length=50)
# #     amount= models.CharField(max_length=50)
# #     paid_through= models.CharField(max_length=50)
# #     vendor= models.CharField(max_length=50)
# #     customer_name= models.CharField(max_length=50)
# #     project= models.CharField(max_length=50)
# #     billable= models.BooleanField(max_length=50)
# #     ref_no= models.CharField(max_length=50)
# #     bulk_serial=models.CharField(max_length=100)
# #     created_id=models.CharField(max_length=50)
# #     created_date=models.DateTimeField(default=now)
# #     modified_id=models.CharField(max_length=50)
# #     modified_date=models.DateTimeField(auto_now=True)
# #     deleted_id=models.CharField(max_length=50)
# #     deleted_date=models.DateTimeField(default=now)
# #     class Meta:
# #         verbose_name_plural = 'Bulk Expenses' 
# #         db_table = "BulkExpenses"    
# #     def __str__(self):
# #         return self.vendor_name

# # class RecExpense(models.Model):
# #     re_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
# #     exp_id = models.ForeignKey(ExpenseRecord, on_delete=models.SET_NULL, null=True)
# #     item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
# #     invoice_id = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
# #     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
# #     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
# #     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)    
# #     #po_id = models.ForeignKey(PO, on_delete=models.SET_NULL, null=True)
# #     so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)    
# #     start_date=models.DateTimeField(default=now)
# #     end_date=models.DateTimeField(default=now)
# #     expense_account= models.CharField(max_length=50)
# #     amount= models.CharField(max_length=50)
# #     paid_through= models.CharField(max_length=50)
# #     vendor_name= models.CharField(max_length=50)
# #     repeat_every=models.DateTimeField(default=now)
# #     never_expires=models.BooleanField()
# #     notes= models.CharField(max_length=150)
# #     customer_name= models.CharField(max_length=50)
# #     profile_name= models.CharField(max_length=50)    
# #     sub_total=models.FloatField()
# #     item_details= models.CharField(max_length=150)
# #     account=models.CharField(max_length=150)
# #     quantity=models.FloatField()
# #     rate=models.FloatField()
# #     discount=models.FloatField()
# #     amount=models.FloatField()
# #     tax=models.FloatField()
# #     sub_total=models.FloatField()
# #     memo= models.CharField(max_length=150)
# #     ref_no= models.CharField(max_length=50)
# #     re_serial=models.CharField(max_length=100)
# #     re_status=models.CharField(max_length=100)
# #     created_id=models.CharField(max_length=50)
# #     created_date=models.DateTimeField(default=now)
# #     modified_id=models.CharField(max_length=50)
# #     modified_date=models.DateTimeField(auto_now=True)
# #     deleted_id=models.CharField(max_length=50)
# #     deleted_date=models.DateTimeField(default=now)
# #     class Meta:
# #         verbose_name_plural = 'Recurring Expenses'
# #         db_table = "RecurringExpenses"     
# #     def __str__(self):
# #         return self.vendor_name

# # class PO(models.Model):
# #     po_id=models.UUIDField(primary_key=True, default = uuid.uuid4)        
# #     so_id=models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
# #     #bill_id = models.ForeignKey(Bills, on_delete=models.SET_NULL, null=True)
# #     vendor_name=models.CharField(max_length=50)
# #     vendor_id=models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
# #     est_id=models.ForeignKey(Estimate, on_delete=models.SET_NULL, null=True)
# #     supply_place=models.CharField(max_length=50)
# #     po_no=models.CharField(max_length=50)
# #     po_ref_no=models.CharField(max_length=50)
# #     po_serial=models.CharField(max_length=50)
# #     po_status=models.CharField(max_length=50)
# #     bill_status=models.CharField(max_length=50)
# #     po_date=models.DateTimeField(default=now)    
# #     expected_shipment_date=models.DateTimeField(default=now)
# #     delivery_to=models.CharField(max_length=50)
# #     delivery_method=models.CharField(max_length=50)
# #     payment_terms=models.CharField(max_length=50)    
# #     item_details=models.CharField(max_length=70)
# #     quantity=models.FloatField()    
# #     rate=models.FloatField()
# #     discount=models.FloatField()
# #     amount=models.FloatField()
# #     account=models.CharField(max_length=70)
# #     customer_details=models.CharField(max_length=70)
# #     sub_total=models.FloatField()
# #     total_quantity=models.FloatField()
# #     discount=models.FloatField()    
# #     adjustment=models.FloatField()
# #     round_off=models.IntegerField()
# #     tax=models.CharField(max_length=50)
# #     tcs=models.CharField(max_length=50)
# #     total=models.FloatField()
# #     customer_note=models.CharField(max_length=50)
# #     terms_condition=models.CharField(max_length=50)
# #     attach_file=models.FileField(default='please upload file')
# #     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
# #     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)    
# #     convt_type=models.CharField(max_length=50)
# #     convt_id=models.CharField(max_length=50)
# #     convt_serial=models.CharField(max_length=50)
# #     convt_ref_no=models.CharField(max_length=50)
# #     is_converted=models.BooleanField()
# #     TxnID=models.CharField(max_length=50)
# #     EditSequence=models.CharField(max_length=50)
# #     TxnNumber=models.CharField(max_length=50)
# #     TxnDate=models.DateTimeField(default=now)
# #     TxnDateMacro=models.DateTimeField(default=now)
# #     TermsRefListID=models.CharField(max_length=50)
# #     TermsRefFullName=models.CharField(max_length=50)
# #     ExpectedDate=models.DateTimeField(default=now)
# #     ShipMethodRefListID=models.CharField(max_length=50)
# #     ShipMethodRefFullName=models.CharField(max_length=50)
# #     FOB=models.CharField(max_length=50)
# #     VendorMsg=models.CharField(max_length=50)
# #     IsToBePrinted=models.CharField(max_length=50)
# #     IsToBeEmailed=models.CharField(max_length=50)      
# #     created_id=models.CharField(max_length=50)
# #     created_date=models.DateTimeField(default=now)
# #     modified_id=models.CharField(max_length=50)
# #     modified_date=models.DateTimeField(auto_now=True)
# #     deleted_id=models.CharField(max_length=50)
# #     deleted_date=models.DateTimeField(default=now)

# #     class Meta:
# #         verbose_name_plural = 'Purchase Order'
# #         db_table = "PurchaseOrder"     
# #     def __str__(self):
# #         return self.vendor_name

# # class Bills(models.Model):
# #     bill_id=models.UUIDField(primary_key=True, default = uuid.uuid4)        
# #     so_id=models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
# #     po_id = models.ForeignKey(PO, on_delete=models.SET_NULL, null=True)
# #     vendor_name=models.CharField(max_length=50)
# #     vendor_id=models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True) 
# #     supply_place=models.CharField(max_length=50)
# #     bill_no=models.CharField(max_length=50)
# #     bill_ref_no=models.CharField(max_length=50)
# #     bill_serial=models.CharField(max_length=50)
# #     bill_status=models.CharField(max_length=50)    
# #     bill_date=models.DateTimeField(default=now) 
# #     order_no=models.CharField(max_length=50)   
# #     due_date=models.DateTimeField(default=now)    
# #     payment_terms=models.CharField(max_length=50)    
# #     item_details=models.CharField(max_length=70)
# #     account=models.CharField(max_length=70)
# #     quantity=models.FloatField()    
# #     rate=models.FloatField()
# #     customer_details=models.CharField(max_length=70)
# #     customer_email=models.EmailField(max_length=254)  
# #     amount=models.FloatField() 
# #     discount=models.FloatField()   
# #     sub_total=models.FloatField()
# #     total_quantity=models.FloatField()
# #     shipping_charges=models.FloatField()   
# #     packing_charges=models.FloatField() 
# #     adjustment=models.FloatField()
# #     round_off=models.IntegerField()
# #     tds=models.CharField(max_length=50)
# #     tcs=models.CharField(max_length=50)
# #     select_tax=models.CharField(max_length=50)
# #     total=models.FloatField()
# #     customer_note=models.CharField(max_length=50)
# #     terms_condition=models.CharField(max_length=50)
# #     attach_file=models.FileField(default='please upload file')
# #     OpenAmount=models.FloatField()
# #     AmountIncludesVAT=models.CharField(max_length=50)
# #     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
# #     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)    
# #     convt_type=models.CharField(max_length=50, default='null')
# #     convt_id=models.CharField(max_length=50, default='null')
# #     convt_serial=models.CharField(max_length=50, default=0)
# #     convt_ref_no=models.CharField(max_length=50, default='null')
# #     is_converted=models.BooleanField()      
# #     created_id=models.CharField(max_length=50)
# #     created_date=models.DateTimeField(default=now)
# #     modified_id=models.CharField(max_length=50)
# #     modified_date=models.DateTimeField(auto_now=True)
# #     deleted_id=models.CharField(max_length=50)
# #     deleted_date=models.DateTimeField(default=now)

# #     class Meta:
# #         verbose_name_plural = 'Bills' 
# #         db_table = "Bills"    
# #     def __str__(self):
# #         return self.vendor_name

# # class PayMade(models.Model):
# #     pm_id=models.UUIDField(primary_key=True, default = uuid.uuid4)
# #     item_id=models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)    
# #     po_id=models.ForeignKey(PO, on_delete=models.SET_NULL, null=True) 
# #     bill_id=models.ForeignKey(Bills, on_delete=models.SET_NULL, null=True)             
# #     vendor_id=models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)    
# #     vendor_name=models.CharField(max_length=50)
# #     vendor_email = models.EmailField(max_length=50)    
# #     pm_no=models.CharField(max_length=50) 
# #     pm_ref_no=models.CharField(max_length=50)   
# #     amount=models.FloatField()    
# #     payment_date=models.DateTimeField(default=now)
# #     payment_through=models.CharField(max_length=50)
# #     bill_date=models.DateTimeField(default=now)
# #     bill_no=models.CharField(max_length=50)
# #     bill_amount=models.FloatField()
# #     amount_due=models.FloatField()
# #     payment=models.FloatField()
# #     total=models.FloatField()
# #     amount_received=models.FloatField()
# #     amt_for_payment=models.FloatField()
# #     amt_refunded=models.FloatField()
# #     amt_excess=models.FloatField()
# #     is_converted=models.BooleanField()
# #     pay_generated=models.BooleanField()
# #     pm_ref_no=models.CharField(max_length=50)
# #     pm_serial=models.CharField(max_length=50)
# #     pm_status=models.CharField(max_length=50) 
# #     pm_mode=models.CharField(max_length=50)
# #     pm_method=models.CharField(max_length=50)    
# #     pm_terms=models.CharField(max_length=50)    
# #     customer_note=models.CharField(max_length=50)
# #     terms_condition=models.CharField(max_length=50)    
# #     refunded_on=models.DateTimeField(default=now)
# #     description_of_supply=models.CharField(max_length=150)
# #     refund=models.FloatField()
# #     source_os_supply=models.CharField(max_length=150)
# #     destination_of_supply=models.CharField(max_length=50)
# #     reverse_charge=models.FloatField()
# #     deposit_to=models.CharField(max_length=50)
# #     bill_amount=models.FloatField()
# #     bill_balance=models.FloatField()
# #     amount_to_credit=models.FloatField()
# #     tds_to_credit=models.FloatField()
# #     total_amount_to_credit=models.FloatField()
# #     remaining_credits=models.FloatField()
# #     refund=models.FloatField()
# #     attach_file=models.FileField(default='please upload file')
# #     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
# #     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)    
# #     created_id=models.CharField(max_length=50)
# #     created_date=models.DateTimeField(default=now)
# #     modified_id=models.CharField(max_length=50)
# #     modified_date=models.DateTimeField(auto_now=True)
# #     deleted_id=models.CharField(max_length=50)
# #     deleted_date=models.DateTimeField(default=now)
# #     class Meta:
# #         verbose_name_plural = 'Payment Made' 
# #         db_table = "PaymentMade"

# #     def __str__(self):
# #         return self.vendor_name

# # class RecBills(models.Model):
# #     rb_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
# #     bill_id = models.ForeignKey(Bills, on_delete=models.SET_NULL, null=True)
# #     item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)    
# #     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
# #     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
# #     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)    
# #     po_id = models.ForeignKey(PO, on_delete=models.SET_NULL, null=True)    
# #     start_date=models.DateTimeField(default=now)
# #     end_date=models.DateTimeField(default=now)
# #     paid_through= models.CharField(max_length=50)
# #     vendor_name= models.CharField(max_length=50)
# #     repeat_every=models.DateTimeField(default=now)
# #     never_expires=models.BooleanField()
# #     pm_terms=models.CharField(max_length=50)
# #     notes= models.CharField(max_length=150)
# #     customer_name= models.CharField(max_length=50)
# #     profile_name= models.CharField(max_length=50)    
# #     item_details= models.CharField(max_length=150)
# #     account= models.CharField(max_length=150)
# #     quantity=models.FloatField()
# #     rate=models.FloatField()
# #     customer_details= models.CharField(max_length=150)
# #     discount=models.FloatField()
# #     amount=models.FloatField()
# #     total_amount=models.FloatField()
# #     tds=models.FloatField()
# #     sub_total=models.FloatField()
# #     total_quantity=models.FloatField()
# #     adjustment=models.FloatField()
# #     memo= models.CharField(max_length=150)
# #     ref_no= models.CharField(max_length=50)
# #     attach_file=models.FileField(default='please upload file')
# #     rb_serial=models.CharField(max_length=100)
# #     created_id=models.CharField(max_length=50)
# #     created_date=models.DateTimeField(default=now)
# #     modified_id=models.CharField(max_length=50)
# #     modified_date=models.DateTimeField(auto_now=True)
# #     deleted_id=models.CharField(max_length=50)
# #     deleted_date=models.DateTimeField(default=now)

# #     class Meta:
# #         verbose_name_plural = 'Recurring Bill'
# #         db_table = "RecurringBills"     
# #     def __str__(self):
# #         return self.vendor_name

# # class VC(models.Model):  
# #     vc_id=models.UUIDField(primary_key=True, default = uuid.uuid4)    
# #     po_id=models.ForeignKey(PO, on_delete=models.SET_NULL, null=True)    
# #     vendor_id=models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
# #     item_id=models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
# #     bill_id=models.ForeignKey(Bills, on_delete=models.SET_NULL, null=True)
# #     vendor_name=models.CharField(max_length=50)
# #     vendor_email = models.EmailField(max_length=50)
# #     order_no=models.CharField(max_length=50)        
# #     vc_no=models.CharField(max_length=50)      
# #     vc_date=models.DateTimeField(default=now)          
# #     item_details=models.CharField(max_length=70)
# #     account=models.CharField(max_length=50)
# #     quantity=models.FloatField()        
# #     rate=models.FloatField()
# #     customer_details=models.CharField(max_length=70)
# #     amount=models.FloatField()
# #     discount=models.FloatField()    
# #     sub_total=models.FloatField()
# #     total_quantity=models.FloatField()    
# #     adjustment=models.FloatField()
# #     total=models.FloatField()
# #     customer_note=models.CharField(max_length=50)
# #     terms_condition=models.CharField(max_length=50)        
# #     customer_email = models.CharField(max_length=50)
# #     attach_file=models.FileField(default='please upload file')
# #     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
# #     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
# #     vc_status=models.CharField(max_length=50)    
# #     vc_generated=models.BooleanField()    
# #     vc_serial=models.CharField(max_length=50)
# #     vc_ref_no=models.CharField(max_length=50)
# #     convt_type=models.CharField(max_length=50)
# #     convt_id=models.CharField(max_length=50)
# #     convt_serial=models.CharField(max_length=50)
# #     convt_ref_no=models.CharField(max_length=50) 
# #     TxnID=models.CharField(max_length=50)
# #     EditSequence=models.CharField(max_length=50)
# #     TxnNumber=models.CharField(max_length=50)
# #     VendorRefListID=models.CharField(max_length=50)
# #     VendorRefFullName=models.CharField(max_length=50)
# #     APAccountRefListID=models.CharField(max_length=50)
# #     APAccountRefFullName=models.CharField(max_length=50)    
# #     created_id=models.CharField(max_length=50)
# #     created_date=models.DateTimeField(default=now)
# #     modified_id=models.CharField(max_length=50)
# #     modified_date=models.DateTimeField(auto_now=True)
# #     deleted_id=models.CharField(max_length=50)
# #     deleted_date=models.DateTimeField(default=now)
# #     class Meta:
# #         verbose_name_plural = 'Vendor Credit'
# #         db_table = "VendorCredit"     
# #     def __str__(self):
# #         return self.customer_name
