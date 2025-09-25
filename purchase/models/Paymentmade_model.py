from django.db import models
from company.models import Company, Branch,Company_Year
from item.models.item_model import Item
# from .models import *  # Invoice, SO, Estimate
from django.utils.timezone import now
import uuid
from coa.models import COA
from salescustomer.BaseModel import BaseDateid,BaseTaxAmount, BaseTaxTotal

from .Vendor_model import Vendor
from .Bill_model import Bill
EXT_TYPE = (
    ('TALLY','TALLY'),
)
class PaymentMade(BaseDateid):
    pm_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor_paymentmade')
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_paymentmade')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    bill_id = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, related_name='bill_paymentmade')
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    bank_id = models.ForeignKey("banking.Banking", on_delete=models.SET_NULL, null=True)
    form_type = models.CharField(max_length=200, blank=True, default='Payment Made', null=True)
    is_bank_transaction = models.BooleanField(default=False)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    payment_mode = models.CharField(max_length=200, default='null', blank=True, null=True)
    # coa_id=models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True,related_name='coa_paymentmade')
    payment_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    amount_payable = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    bill_date = models.DateTimeField(default=now, null=True)
    bill_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_excess = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    paid_through = models.CharField(max_length=200, default='null', blank=True, null=True)
    amount_received = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amt_for_payment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amt_refunded = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    is_converted = models.BooleanField(default=False)
    pay_generated = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=200, default='null', blank=True, null=True)
    pm_method = models.CharField(max_length=200, default='null', blank=True, null=True)
    pm_terms = models.CharField(max_length=200, default='null', blank=True, null=True)
    terms_condition = models.CharField(max_length=200, default='null', blank=True, null=True)
    # refunded_on=models.DateTimeField(default=now)
  #  description_of_supply = models.CharField(max_length=150)
    refund = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
  #  source_os_supply = models.CharField(max_length=150)
    destination_of_supply = models.CharField(max_length=200, default='null', blank=True, null=True)
    reverse_charge = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    deposit_to = models.CharField(max_length=200, default='null', blank=True, null=True)
    amount_to_credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tds_to_credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_amount_to_credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    remaining_credits = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    attach_file = models.FileField(default='null', blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    party_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_pm_party')
    purchase_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_pm_purchase')
    coa_total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    # igst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_igst')
    # cgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cgst')
    # sgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sgst')
    # shipping_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_shipping')
    # tcs_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_tcs')
    # tds_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_tds')
    # cess_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cess')
    # discount_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_discount')

    class Meta:
        verbose_name_plural = 'Payment Made'
        ordering = ['-created_date']


    def __str__(self):
        if self.company_id:
            return self.company_id.company_name if self.company_id else "no company"
        return "no company"