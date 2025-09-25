from django.db import models
from company.models import Company, Branch,Company_Year

# from .models import *  # Invoice, SO, Estimate
from django.utils.timezone import now
import uuid
 
from salescustomer.BaseModel import BaseDateid,BaseTaxAmount, BaseTaxTotal

EXT_TYPE = (
    ('TALLY','TALLY'),
)

class TDS(BaseDateid):
    tds_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    tds_section = models.CharField(max_length=200, blank=True, default='null', null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    tds_payable_account = models.CharField(max_length=200, blank=True, default='null', null=True)
    tds_receivable_account = models.CharField(max_length=200, blank=True, default='null', null=True)
    limit = models.PositiveIntegerField(default=0)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)

    class Meta:
        verbose_name_plural = 'TDS'

    def __str__(self):
        return self.tax_name