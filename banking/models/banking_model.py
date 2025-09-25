
from django.db import models
import uuid
from company.models import Company, Branch
from salescustomer.BaseModel import BaseDateid
from coa.models import COA
from company.models import Company_Year
# Banking
class Banking(BaseDateid):
    bank_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account_code = models.CharField(max_length=200, blank=True, default='null', null=True)
    account_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    account_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    account_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    bank_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='bankcompany')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    ifsc_code = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'Banking '
        ordering = ['-created_date']
    def __str__(self):
        return str(self.bank_id)
