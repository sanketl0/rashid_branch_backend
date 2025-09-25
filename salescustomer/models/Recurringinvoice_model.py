import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount

from .So_model import SO



class RI(BaseDateid):
    ri_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
    est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
    emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=200)
    so_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    ri_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    ri_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    ri_generated = models.BooleanField()
    profile_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    repeat_every = models.CharField(max_length=200, blank=True, default='null', null=True)
    never_expire = models.BooleanField(default=False)
    associated_project_hrs = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    order_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    payment_terms = models.CharField(max_length=200, blank=True, default='null', null=True)
    emp_role = models.CharField(max_length=200, blank=True, default='null', null=True)
    item_name = models.CharField(max_length=200)
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    round_off = models.IntegerField(default=0)
    tax = models.CharField(max_length=200, blank=True, default='null', null=True)
    tcs = models.CharField(max_length=200, blank=True, default='null', null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    customer_note = models.CharField(max_length=200, blank=True, default='null', null=True)
    terms_condition = models.CharField(max_length=200, blank=True, default='null', null=True)
    attach_file = models.FileField(default='please upload file')
    customer_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ri_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_converted = models.BooleanField()
    convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'Recurring Invoice'

    def __str__(self):
        return self.customer_name
