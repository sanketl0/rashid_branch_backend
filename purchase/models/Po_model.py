from django.db import models
from company.models import Company, Branch,Company_Year

# from .models import *  # Invoice, SO, Estimate
from django.utils.timezone import now
import uuid

from salescustomer.BaseModel import BaseDateid, BaseTaxAmount, BaseTaxTotal
from .Vendor_model import Vendor
EXT_TYPE = (
    ('TALLY','TALLY'),
)
class PO(BaseDateid,BaseTaxTotal,BaseTaxAmount):  # BaseTaxTotal
    po_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    is_po_generated = models.BooleanField(default=False)
    po_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_po')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    po_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    po_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    po_date = models.DateField(blank=True, null=True)
    po_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    destination_place = models.CharField(max_length=50, blank=True, default='null', null=True)
    term_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    no_of_days = models.CharField(max_length=200, blank=True, default='null', null=True)
    shipment_preference = models.CharField(max_length=200, blank=True, default='null', null=True)
    discount_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    sub_total = models.CharField(max_length=200, blank=True, default='null', null=True)
    total = models.CharField(max_length=200, blank=True, default='null', null=True)
    entered_discount = models.CharField(max_length=200, blank=True, default='null', null=True)
    discount = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_note = models.CharField(max_length=200, blank=True, default='null', null=True)
    terms_condition = models.CharField(max_length=200, blank=True, default='null', null=True)
    tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
    tcs_amount = models.CharField(max_length=200, blank=True, default='null', null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
    attach_file = models.FileField(max_length=200, blank=True, default='null', null=True)
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
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    class Meta:
        verbose_name_plural = 'purchase order'

