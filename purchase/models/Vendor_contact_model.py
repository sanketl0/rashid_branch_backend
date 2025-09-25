import imp
from django.db import models
from company.models import Company, Branch,Company_Year

# from .models import *  # Invoice, SO, Estimate
from django.utils.timezone import now
import uuid

from salescustomer.BaseModel import BaseDateid,BaseTaxAmount,BaseTaxTotal
from .Vendor_model import Vendor


class VendorContact(BaseDateid):
    contact_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='contact_person')
    contact_salutation = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_phone = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_mobile = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    contact_designation = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_department = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Vendor Contact'