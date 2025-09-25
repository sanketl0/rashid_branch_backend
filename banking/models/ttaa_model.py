
from django.db import models
import uuid
from company.models import Company, Branch
from salescustomer.BaseModel import BaseDateid
from coa.models import COA
from company.models import Company_Year
from .banking_model import Banking
class TTAA(BaseDateid):
    ttaa_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    bank_id = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True)
    to_account = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    transfer_to_date = models.DateField(blank=True, null=True)
    transfer_to_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    description = models.TextField(blank=True,null=True)
    attach_file = models.FileField(default='null', blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'TTAA'
        ordering=['-created_date']

    def __uuid__(self):
        return self.ttaa_id


# Transfer to Another Account
