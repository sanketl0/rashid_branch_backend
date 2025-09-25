from django.db import models
import uuid
from company.models import Company, Branch
from salescustomer.BaseModel import BaseDateid
from coa.models import COA
from company.models import Company_Year
from salescustomer.models.Salescustomer_model import SalesCustomer
from .banking_model import Banking



class DFOA(BaseDateid):
    dfoa_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    bank_id = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_id = models.ForeignKey(SalesCustomer, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    deposit_from_date = models.DateField(blank=True, null=True)
    deposit_from_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
    from_account = models.CharField(max_length=200, blank=True, default='null', null=True)
    received_via = models.CharField(max_length=200, blank=True, default='null', null=True)
    description = models.TextField( blank=True, null=True)
    attach_file = models.FileField(max_length=250, blank=True, default='null', null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    class Meta:
        verbose_name_plural = 'DFOA'

    def __str__(self):
        return str(self.dfoa_id)