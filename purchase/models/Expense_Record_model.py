from django.db import models
from company.models import Company, Branch,Company_Year

# from .models import *  # Invoice, SO, Estimate
from django.utils.timezone import now
import uuid

from salescustomer.BaseModel import BaseDateid,BaseTaxTotal,BaseTaxAmount
from .Vendor_model import Vendor

class ExpenseRecord(BaseTaxAmount,BaseDateid):
    er_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    bank_id = models.ForeignKey("banking.Banking", on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
    # po = models.ForeignKey("purchase.PO", on_delete=models.SET_NULL, null=True)
    expense_date = models.DateTimeField(default=now, null=True)
    expense_account = models.CharField(max_length=200, blank=True, default='null', null=True)
    expense_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    expense_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    expense_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    expense_status = models.CharField(max_length=200, default='null', blank=True, null=True)
    is_expense_generated = models.BooleanField(default=False)
    #  amount=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    paid_through = models.CharField(max_length=200, default='null', blank=True, null=True)
    notes = models.CharField(max_length=200, default='null', blank=True, null=True)
    gst_treatment = models.CharField(max_length=200, default='null', blank=True, null=True)
    vendor_gstin = models.CharField(max_length=200, default='null', blank=True, null=True)
    supply_place = models.CharField(max_length=200, default='null', blank=True, null=True)
    destination_place = models.CharField(max_length=200, default='null', blank=True, null=True)
    # reverse_charge=models.BooleanField(default=False)
    attach_file = models.FileField(default='null', blank=True, null=True)
    reporting_tag = models.CharField(max_length=200, default='null', blank=True, null=True)
    account = models.CharField(max_length=200, default='null', blank=True, null=True)
    sales_tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    total_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    item_details = models.CharField(max_length=200, default='null', blank=True, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    customer_details = models.CharField(max_length=200, default='null', blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    expense_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    status = models.CharField(max_length=200, default='null', blank=True, null=True)
    sac = models.CharField(max_length=200, default='null', blank=True, null=True)
    hsn_code = models.CharField(max_length=200, default='null', blank=True, null=True)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    is_converted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    
    class Meta:
        verbose_name_plural = 'Expense Record'
        ordering =['-created_date']
