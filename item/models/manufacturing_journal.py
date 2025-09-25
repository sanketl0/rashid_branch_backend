from django.db import models
from company.models import Company, Branch,Company_Year
import uuid
from item.models.item_model import Item
from django.db.models.signals import post_save
from django.dispatch import receiver
from salescustomer.BaseModel import BaseDateid
from item.models.stock_model import WareHouse
EXT_TYPE = (
    ('TALLY','TALLY'),
)



class ManufacturingJournal(BaseDateid):
    mfg_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_mfg_journals')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    journal_date =  models.DateField(blank=True, null=True)
    batches = models.CharField(max_length=200, blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    mfg_serial_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    mfg_status =  models.CharField(max_length=200, blank=True, default='null', null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    total_cost =  models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_by_cost =  models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    effective_cost =  models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    effective_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_stock = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    godown_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    godown_id = models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ['-created_date']


class ManufacturingJournalItem(BaseDateid):
    mfg_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    mfg_id = models.ForeignKey(ManufacturingJournal, on_delete=models.SET_NULL, null=True,related_name='mfg_items')
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    batches = models.CharField(max_length=200, blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate =  models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    godown_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    godown_id = models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ['-created_date']

class ManufacturingByItem(BaseDateid):
    mfg_by_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    mfg_id = models.ForeignKey(ManufacturingJournal, on_delete=models.SET_NULL, null=True,related_name='mfg_by_items')
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    batches = models.CharField(max_length=200, blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate_percentage =  models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    godown_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    godown_id =models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ['-created_date']


class StockJournal(BaseDateid):
    sj_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    date = models.DateField(blank=True, null=True)
    serial_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    total_consumption = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    total_production = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    total_consumption_qty = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    total_production_qty = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)

    class Meta:
        ordering =['-created_date']


class Consumption(BaseDateid):
    cmp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sj_id = models.ForeignKey(StockJournal, on_delete=models.SET_NULL, null=True, related_name='consumption_items')
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    warehouse_id = models.CharField(max_length=200, default='null', blank=True, null=True)
    quantity = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    batches = models.CharField(max_length=200, blank=True, null=True)
    godown_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    godown_id =models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    class Meta:
        ordering =['-created_date']

class Production(BaseDateid):
    prd_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sj_id = models.ForeignKey(StockJournal, on_delete=models.SET_NULL, null=True, related_name='production_items')
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    warehouse_id = models.CharField(max_length=200, default='null', blank=True, null=True)
    quantity = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    batches = models.CharField(max_length=200, blank=True, null=True)
    godown_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    godown_id =models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    class Meta:
        ordering =['-created_date']





