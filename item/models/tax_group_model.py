from company.models import Company,Company_Year,Branch
from salescustomer.BaseModel import BaseDateid
from django.db import models
import uuid


class TaxGroup(BaseDateid):
    taxgroup_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
    group_name = models.CharField(max_length=200, blank=True, null=True)
    tax_id1 = models.CharField(max_length=200, blank=True, null=True)
    tax_id2 = models.CharField(max_length=200, blank=True, null=True)
