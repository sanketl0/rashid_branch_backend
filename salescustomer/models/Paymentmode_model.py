
import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount


class PaymentMode(BaseDateid):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    payment_mode = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'payment mode'

    def __str__(self):
        return self.payment_mode