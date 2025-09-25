from salescustomer.BaseModel import BaseDateid
from django.db import models
import uuid
from company.models import Company,Company_Year,Branch


class TaxExemption(BaseDateid):
    taxexemp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    exemption_reason = models.CharField(max_length=200, blank=True, null=True)
    exemption_code = models.CharField(max_length=200, blank=True, null=True)
    alias = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)

    # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Tax Exemption'

    def __str__(self):
        return self.alias
