from django.db import models
from company.models import Company, Branch
import uuid
from salescustomer.BaseModel import BaseDateid



class StockTransfer(BaseDateid):
    st_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    trans_date = models.DateField(blank=True, null=True)
    transfer_serial = models.CharField(max_length=200,blank=True,null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        ordering = ['-created_date']


class StockTransferTransaction(BaseDateid):
    stt_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    stock_transfer = models.ForeignKey(StockTransfer, on_delete=models.SET_NULL, null=True,related_name='stock_transactions')
    primary_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True,related_name='primary_transactions')
    item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True,related_name='primary_items')
    sec_item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True,related_name='sec_items')
    secondary_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True,related_name='secondary_transactions')
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    batches = models.CharField(max_length=200, blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    sec_batches = models.CharField(max_length=200,default='[]')
    sec_mfg_date = models.DateField(blank=True, null=True)
    sec_expire_date = models.DateField(blank=True, null=True)