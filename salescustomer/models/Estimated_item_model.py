import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount





class EstimatedItem(BaseTaxAmount, BaseDateid):
    estitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True,
                               related_name='estimate_items')
    item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
    tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    taxamount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
    vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name_plural = 'estimated item'
        ordering = ['-created_date']
    def __str__(self):
        if self.item_id:
            return self.item_id.name
        return "No Name"