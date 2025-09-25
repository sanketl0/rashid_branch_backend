from django.db import models
import uuid
from company.models import Company, Branch
from purchase.models import Tds_model
from salescustomer.BaseModel import BaseDateid,BaseTaxAmount
from coa.models import COA
from company.models import Company_Year
from salescustomer.models.Salescustomer_model import SalesCustomer
from .banking_model import Banking

from purchase.models.Tds_model import TDS


class VendorAdvanced(BaseDateid,BaseTaxAmount):
    va_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    is_vendor_advance_generated = models.BooleanField()
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    bank_id = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
    gst_treatment = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_gstin = models.CharField(max_length=200, blank=True, default='null', null=True)
    source_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    destination_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    vendor_advance_date = models.DateField(blank=True, null=True)
    vendor_advance_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    deposit_to = models.CharField(max_length=200, blank=True, default='null', null=True)
    paid_via = models.CharField(max_length=200, blank=True, default='null', null=True)
    description = models.TextField(blank=True,null=True)
    description_supply = models.TextField(blank=True,null=True)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    tax_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    reverse_charge = models.BooleanField(default=False)
    attach_file = models.FileField(max_length=250, blank=True, default='null', null=True)
    tds_id = models.ForeignKey(TDS, on_delete=models.SET_NULL, null=True)
    tds_amount= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    is_bank_transaction = models.BooleanField(default=False)
    is_converted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    tds_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_va_tds')
    party_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_va_party')
    igst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_va_igst')
    cgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_va_cgst')
    sgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_va_sgst')
    class Meta:
        verbose_name_plural = 'VendorAdvanced'
        ordering = ['-created_date']

    def __str__(self):
        return str(self.va_id)

