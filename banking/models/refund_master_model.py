import imp
from django.db import models
import uuid
from company.models import Company, Branch
from salescustomer.BaseModel import BaseDateid
from company.models import Company_Year
from salescustomer.models.Salescustomer_model import SalesCustomer
from .banking_model import Banking
from coa.models import COA
from salescustomer.models.Creditnote_model import CreditNote


class RefundMaster(BaseDateid):
    rm_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_payment_date = models.DateField(blank=True, null=True)
    serial_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    payment_mode = models.CharField(max_length=200, blank=True, default='null', null=True)
    serial_ref = models.CharField(max_length=200, blank=True, default='null', null=True)
    serial_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount_ref = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    balance_amount_ref = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey(SalesCustomer, on_delete=models.SET_NULL, null=True)
    vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
    cn_id = models.ForeignKey(CreditNote, on_delete=models.SET_NULL, null=True)
    dn_id = models.ForeignKey("purchase.DebitNote", on_delete=models.SET_NULL, null=True)
    bank_id = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True)
    refund_date = models.DateTimeField(auto_now=True)
    is_bank_transaction = models.BooleanField(default=False)
    form_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    refund_balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    refund_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_cn_refund_generated = models.BooleanField(blank=False, null=True)
    is_dn_refund_generated = models.BooleanField(blank=False, null=True)
    is_cust_advance_refund_generated = models.BooleanField(blank=False, null=True)
    is_vend_advance_refund_generated = models.BooleanField(blank=False, null=True)
    refrence_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    transaction_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    attach_file = models.FileField(max_length=250, blank=True, default='null', null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    class Meta:
        verbose_name_plural = 'RefundMaster'

    def __str__(self):
        return "Refund Master: {}".format(self.rm_id)


