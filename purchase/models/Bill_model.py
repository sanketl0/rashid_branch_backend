from django.db import models
from company.models import Company, Branch,Company_Year
from item.models.item_model import Item
# from .models import *  # Invoice, SO, Estimate
from  coa.models import COA
import uuid

from salescustomer.BaseModel import BaseDateid,BaseTaxAmount,BaseTaxTotal

from .Vendor_model import Vendor
from .Tds_model import TDS

EXT_TYPE = (
    ('TALLY','TALLY'),
)

class Bill(BaseDateid,BaseTaxTotal,BaseTaxAmount):
    bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor_bills')
    batch = models.BooleanField(default=False)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY',choices=EXT_TYPE)
    is_bill_generate = models.BooleanField(default=False)
    bill_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='Company_bills')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    bill_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    order_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    discount_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_Type = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    # ayment_mode=models.CharField(max_length=50, blank=True, default='null', null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    cess_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    charges = models.ManyToManyField('transaction.ChargeTransaction', related_name='bill_charges_transaction', blank=True)
    total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
    tds_id = models.ForeignKey(TDS, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True,null=True)
    tcs_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tds_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    terms_condition = models.CharField(max_length=200, blank=True, default='null', null=True)
    term_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    no_of_days = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    packing_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    select_tax = models.CharField(max_length=200, blank=True, default='null', null=True)
    attach_file = models.FileField(max_length=250, blank=True, default='null', null=True)
    OpenAmount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    AmountIncludesVAT = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_converted = models.BooleanField(default=False)
    TermsRefFullName = models.CharField(max_length=200, blank=True, default='null', null=True)
    TermsRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_is_converted = models.BooleanField(default=False)
    To_convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_is_converted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    party_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_party')
    purchase_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_purchase')

    coa_total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    igst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True,related_name='coa_bill_igst')
    cgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_cgst')
    sgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_sgst')
    shipping_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_shipping')
    tcs_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_tcs')
    tds_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_tds')
    cess_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_cess')
    discount_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_bill_discount')

    class Meta:
        verbose_name_plural = 'Bills'
        ordering = ['-created_date']

    def __str__(self):
        return self.bill_serial


class BillView(models.Model):
    bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    vendor_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    bill_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    order_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    company_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    branch_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_status = models.CharField(max_length=200, blank=True, default='null', null=True)


    class Meta:
        managed = False
        db_table = 'bill_view'