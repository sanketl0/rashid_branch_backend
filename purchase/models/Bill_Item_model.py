from django.db import models
from company.models import Company, Branch,Company_Year
from item.models.item_model import Item
from item.models.stock_model import WareHouse
import uuid
from salescustomer.BaseModel import BaseTaxAmount, BaseTaxTotal
from salescustomer.BaseModel import BaseDateid
from .Bill_model import Bill

class Bill_Item(BaseTaxAmount,BaseTaxTotal,BaseDateid):
    billitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    bill_id = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, related_name='bill_items')
    item_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    quantity =  models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    godown_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    godown_id = models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True)
    batch_no = models.CharField(max_length=200, blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    tax_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    tax_rate = models.CharField(max_length=200, default='null', blank=True, null=True)
    tax_type = models.CharField(max_length=200, default='null', blank=True, null=True)
    account_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    taxamount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
    cess_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
    cess_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    # cgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    # sgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    # igst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)

    class Meta:
        verbose_name_plural = 'bill item'
        ordering = ['-created_date']

    def __str__(self):
        if self.bill_id:
            return self.bill_id.bill_serial
        return self.billitem_id

