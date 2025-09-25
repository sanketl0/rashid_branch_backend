import uuid
from salescustomer.BaseModel import BaseDateid
from django.db import models
from company.models import Company, Branch,Company_Year
from purchase.models.Tds_model import TDS
from purchase.models.Vendor_model import Vendor
from salescustomer.models.Salescustomer_model import SalesCustomer
# Create your models here.

class Audit(BaseDateid):
    audit_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_audits')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey('registration.user', on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='user_logs')
    modified_by = models.ForeignKey('registration.user', on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='modified_user_logs')
    data = models.JSONField()
    module = models.CharField(max_length=200, blank=True, default='null', null=True)
    sub_module = models.CharField(max_length=200, blank=True, default='null', null=True)
    audit_created_date = models.DateField(blank=True,null=True)
    audit_modified_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-created_date']

