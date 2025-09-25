import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount
from salescustomer.BaseModel import BaseTaxTotal
from coa.models import COA


class VendorOB(BaseDateid):
    Vendorob_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    vendor_id = models.ForeignKey("purchase.vendor", on_delete=models.SET_NULL, null=True,
                                    related_name='vendor_balance')
    opening_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    closing_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    available_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    debit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    migration_date =  models.DateTimeField(default=now, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name_plural = 'Vendor Opening Balance'

    def __str__(self):
        return 'opening_balance'