import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount,BaseTaxTotal
from item.models.stock_model import WareHouse




class CreditItem(BaseTaxAmount, BaseDateid):
    cnitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cn_id = models.ForeignKey("salescustomer.CreditNote", on_delete=models.SET_NULL, null=True,
                              related_name='credit_note_items')
    item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    selected_item_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    selected_tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
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
    godown_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    godown_id = models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True)
    batches = models.CharField(max_length=200,blank=True,null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)


    class Meta:
        verbose_name_plural = 'Credit Item'

