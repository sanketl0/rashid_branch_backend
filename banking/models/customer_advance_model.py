from django.db import models
import uuid
from company.models import Company, Branch
from salescustomer.BaseModel import BaseDateid,BaseTaxAmount
from coa.models import COA
from company.models import Company_Year
from salescustomer.models.Salescustomer_model import SalesCustomer
from .banking_model import Banking

class CustomerAdvance(BaseTaxAmount,BaseDateid):
    ca_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    is_customer_advance_generated = models.BooleanField()
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    bank_id = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_id = models.ForeignKey(SalesCustomer, on_delete=models.SET_NULL, null=True, related_name='customer_ad')
    gst_treatment = models.CharField(max_length=200, blank=True, default='null', null=True)
    gstin_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    amount_received = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    customer_advance_date = models.DateField(blank=True, null=True)
    customer_advance_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    received_via = models.CharField(max_length=200, blank=True, default='null', null=True)
    description = models.TextField(blank=True, null=True)
    description_supply = models.CharField(max_length=200, blank=True, default='null', null=True)
    bank_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    payment_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    attach_file = models.FileField(max_length=250, blank=True, default='null', null=True)
    is_bank_transaction = models.BooleanField(default=False)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'CustomerAdvanced'
        ordering =['-created_date']

    def __str__(self):
        return str(self.customer_id.customer_name)
