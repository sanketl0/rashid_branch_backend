import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid
class Employee(BaseDateid):
    emp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    emp_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    emp_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    emp_phone = models.CharField(max_length=200, blank=True, default='null', null=True)
    emp_mobile = models.CharField(max_length=200, blank=True, default='null', null=True)
    emp_role = models.CharField(max_length=200, blank=True, default='null', null=True)
    emp_address = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'Employee'

    def __str__(self):
        return self.emp_role