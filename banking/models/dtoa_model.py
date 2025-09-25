from django.db import models
import uuid
from company.models import Company, Branch
from salescustomer.BaseModel import BaseDateid
from coa.models import COA
from company.models import Company_Year
from salescustomer.models.Salescustomer_model import SalesCustomer
from .banking_model import Banking
# Deposit To Other Account
class DTOA(BaseDateid):
    dtoa_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey(SalesCustomer, on_delete=models.SET_NULL, null=True)
    bank_id = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, blank=True, default='null', null=True)
    to_account = models.CharField(max_length=50, blank=True, default='null', null=True)
    paid_via = models.CharField(max_length=50, blank=True, default='null', null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    deposit_to_date = models.DateField(blank=True, null=True)
    deposit_to_ref_no = models.CharField(max_length=50, blank=True, default='null', null=True)
    description = models.CharField(max_length=50, blank=True, default='null', null=True)
    attach_file = models.FileField(null=True, default='null', max_length=250 )
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'DTOA'

    def __str__(self):
        return str(self.dtoa_id)


# Deposit To Other Account
