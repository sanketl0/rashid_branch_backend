
import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid, BaseTaxTotal

EXT_TYPE = (
    ('TALLY','TALLY'),
)
class Estimate(BaseTaxTotal, BaseDateid):
    est_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
    emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
    so_id = models.ForeignKey("salescustomer.SO", on_delete=models.SET_NULL, null=True)
    tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    est_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    est_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    est_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    est_date = models.DateField(blank=True, null=True)
    is_estimate_generated = models.BooleanField(default=False)
    expiry_date = models.DateField(blank=True, null=True)
    project_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    subject = models.CharField(max_length=200, blank=True, default='null', null=True)
    total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
    shipping_tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tcs_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    round_off = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tax = models.CharField(max_length=200, blank=True, default='null', null=True)
    grand_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    customer_note = models.CharField(max_length=200, blank=True, default='null', null=True)
    terms_condition = models.CharField(max_length=200, blank=True, default='null', null=True)
    attach_file = models.FileField(default='null', blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_converted = models.BooleanField(default=False)
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
    class Meta:
        verbose_name_plural = 'estimate'

        ordering=['-created_date']

    def __str__(self):
        if self.company_id:
            return self.company_id.company_name
        return  "No Name"
