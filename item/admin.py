from django.contrib import admin
from item.models.item_model import Item,ItemGroup
from item.models.stock_model import Stock,Batch
from item.models.stock_transfer_model import StockTransfer
from item.models.tax_name_model import TaxName
from item.models.tax_group_model import TaxGroup
from item.models.adjustment_model import Adjustment
from item.models.manufacturing_journal import *
admin.site.register([Item,Stock,TaxName,TaxGroup,Batch,StockTransfer,ItemGroup,Adjustment,
                     ManufacturingJournal,ManufacturingJournalItem,ManufacturingByItem,StockJournal,Consumption,Production])
# # Register your models here.
# for m in (InventoryAdjust, Item, ItemDetails, TaxName, TaxGroup, TaxExemption):
#

