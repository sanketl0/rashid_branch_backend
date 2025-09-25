from django.db import models
from company.models import Company, Branch,Company_Year
from item.models.item_model import Item
# from .models import *  # Invoice, SO, Estimate
from django.utils.timezone import now
import uuid
 
from salescustomer.BaseModel import BaseDateid,BaseTaxAmount, BaseTaxTotal

from .Po_model import PO




class PoItem(BaseDateid,BaseTaxAmount,BaseTaxTotal):  # BaseTaxAmount
    poitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
    tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_rate = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    taxamount = models.CharField(max_length=200, blank=True, default='null', null=True)
    po_id = models.ForeignKey(PO, on_delete=models.SET_NULL, null=True, related_name='po_items')
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'purchase item'