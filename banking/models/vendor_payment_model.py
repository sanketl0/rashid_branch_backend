from django.db import models
import uuid
from company.models import Company, Branch
from salescustomer.BaseModel import BaseDateid
from coa.models import COA
from company.models import Company_Year
from salescustomer.models.Salescustomer_model import SalesCustomer
from .banking_model import Banking






# Vendor Payment
class VendorPayment(BaseDateid):
    vp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    bank_id = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True)
    # is_bank_transaction = models.BooleanField(default=True)
    paid_through = models.CharField(max_length=200, blank=True, default='null', null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
    payment_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_mode = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount_payable = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    payment_date = models.DateField(blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True)
    bill_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    bill_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    payment_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount_excess = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    note = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_id = models.ForeignKey("purchase.Bill", on_delete=models.SET_NULL, null=True)
    attach_file = models.FileField(max_length=50, blank=True, default='null', null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'VendorPayment'

    def __str__(self):
        return str(self.vp_id)
