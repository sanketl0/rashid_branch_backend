from django.db import models
from company.models import Company, Branch,Company_Year
# from salescustomercustomer.models import salescustomerCustomer
from django.utils.timezone import now
import uuid
from salescustomer.BaseModel import BaseDateid

from item.models.adjustment_model import Adjustment





class AdjustmentItem(BaseDateid):
    adjitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    coa_id= models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
    adj_id= models.ForeignKey(Adjustment, on_delete=models.SET_NULL, null=True, related_name='adj_items')
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    warehouse_id=models.CharField(max_length=200, default='null', blank=True, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    adjusted_qty=models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    quantity =models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    stock_quantity=models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    batch_no = models.CharField(max_length=200, blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    changed_value= models.DecimalField(default=0,null=True,decimal_places=2, max_digits=15)
    amount= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjusted_value= models.DecimalField(default=0,null=True,decimal_places=2, max_digits=15)
    current_value= models.DecimalField(default=0,null=True,decimal_places=2, max_digits=15)
    item_id =models.CharField(max_length=200, default='null', blank=True, null=True)
    item_name =models.CharField(max_length=200, default='null', blank=True, null=True)