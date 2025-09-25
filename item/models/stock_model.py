
from django.db import models
from company.models import Company, Branch,Company_Year

import uuid
from salescustomer.BaseModel import BaseDateid
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from django.db.models import Sum,Q,Avg,F
from datetime import datetime
import traceback
EXT_TYPE = (
    ('TALLY','TALLY'),
)

FLOW = (
    ('INWARD','INWARD'),
    ('OUTWARD','OUTWARD'),
)


class WareHouse(BaseDateid):
    wh_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)

class Stock(BaseDateid):
    st_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    godown_name = models.CharField(max_length=200, default='null', blank=True, null=True)
    godown_id =models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True)
    purchase_stock = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    batch_no = models.CharField(max_length=200,blank=True, null=True)
    mfg_date = models.DateField(blank=True,null=True)
    expire_date = models.DateField(blank=True,null=True)
    item_id =models.CharField(max_length=200, default='null', blank=True, null=True)
    item_name =models.CharField(max_length=200, default='null', blank=True, null=True)
    ref_id =models.CharField(max_length=200, default='null', blank=True, null=True)
    ref_tblname =models.CharField(max_length=200, default='null', blank=True, null=True)
    stock_in= models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    stock_out= models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    quantity= models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    module=models.CharField(max_length=200, default='null', blank=True, null=True)
    formname=models.CharField(max_length=200, default='null', blank=True, null=True)
    stage= models.CharField(max_length=200, default='null', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    flow_type = models.CharField(max_length=200, blank=True, null=True,choices=FLOW)
    adjusted_qty= models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    changed_value= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjusted_value= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    current_value= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    module_date = models.DateTimeField(blank=True, null=True)
    closing_stock = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    closing_stock_value =  models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    closing_stock_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)


    class Meta:
        verbose_name_plural = 'Stock'
        ordering =['-created_date']

    def __str__(self):
        return str(self.quantity)



def getstock_on_hand(item_id):
    stocks = Batch.objects.filter(item_id=item_id)
    if stocks:
        stock_quantity  = sum(item.stock_quantity for item in stocks)
        return stock_quantity
    return 0


def get_inventory_value_rate(comp_id,item_id,batch_no,expire_date,mfg_date,target_quantity):

    stocks = Stock.objects.filter(Q(
        item_id=item_id,
        batch_no=batch_no,
        expire_date=expire_date,
        mfg_date=mfg_date,
        stock_in__gt=0,
        quantity__gt=0,
    )).order_by('date','created_date').iterator(chunk_size=10)
    rate = 0
    inventory_value = 0
    for stock in stocks:
        if target_quantity <= 0:
            break
        if stock.quantity >= target_quantity:
            inventory_value += target_quantity * float(stock.rate)
            stock.quantity = float(stock.quantity) -  target_quantity
            rate = float(stock.rate)
            stock.save()
            target_quantity = 0
        else:
            inventory_value += target_quantity * float(stock.rate)
            stock.quantity = float(stock.quantity) - target_quantity
            stock.quantity = 0
            stock.save()
    inventory_value = round(inventory_value,2)
    return inventory_value,rate


class Batch(models.Model):
    item_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    stock_quantity = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    batch_no = models.CharField(max_length=200,blank=True,null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    branch_id = models.CharField(max_length=200, blank=True, null=True)
    company_id = models.CharField(max_length=200, blank=True, null=True)
    godown_id = models.CharField(max_length=200, blank=True, null=True)
    godown_name = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'batch_view'

    def __str__(self):
        if self.company_id:
            return Company.objects.get(company_id=self.company_id).company_name

class ItemAvgTransaction(models.Model):
    item_id = models.CharField(primary_key=True,max_length=200, default=str(uuid.UUID))
    closing_stock = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    closing_stock_value = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    avg_weighted_cost_per_unit = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    batch_no = models.CharField(max_length=200,blank=True,null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    ref_id = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    module_date = models.DateTimeField(blank=True, null=True)
    branch_id = models.CharField(max_length=200, blank=True, null=True)
    company_id = models.CharField(max_length=200, blank=True, null=True)
    godown_id = models.CharField(max_length=200, blank=True, null=True)
    godown_name = models.CharField(max_length=200, blank=True, null=True)
    formname = models.CharField(max_length=200, blank=True, null=True)
    stock_in = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    stock_out = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avg_view'

class ItemTransaction(models.Model):
    item_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    sum_last_transactions = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    avg_weighted_cost_per_unit = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    batch_no = models.CharField(max_length=200,blank=True,null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    module_date = models.DateTimeField(blank=True, null=True)
    branch_id = models.CharField(max_length=200, blank=True, null=True)
    company_id = models.CharField(max_length=200, blank=True, null=True)
    godown_id = models.CharField(max_length=200, blank=True, null=True)
    godown_name = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'item_transaction'


# @receiver(post_delete, sender=Stock)
# def stock_deleted(sender, instance, **kwargs):
#     if instance.purchase_stock:
#         instance.purchase_stock.quantity = instance.quantity
#         instance.purchase_stock.save()
#     MasterTransaction.objects.filter(L1detail_id=instance.st_id).delete()
#     print("Transaction Of Stock Deleted")

# @receiver(post_save, sender=Stock)
# def stock_created(sender, instance,created, **kwargs):
    # with connection.cursor() as cursor:
    #     args = [instance.item_id,
    #             instance.batch_no, instance.expire_date,
    #             instance.mfg_date]
    #     cursor.execute(
    #         "CALL avg_procedure(%s, %s, %s, %s)",
    #         args
    #     )
    # print("procedure called")
    # objs = ItemTransaction.objects.filter(company_id='15d1f6e0-b5c6-4ccc-9842-e3a6e91d5f86')
    # for index,obj in enumerate(objs):
    #     with connection.cursor() as cursor:
    #         args = [obj.item_id,
    #                 obj.batch_no,obj.expire_date ,
    #                 obj.mfg_date]
    #         cursor.execute(
    #             "CALL avg_procedure(%s, %s, %s, %s)",
    #             args
    #         )
    #     print(f"Total done is {index+1}")
#     stocks = Stock.objects.filter(
#         Q(
#         item_id=instance.item_id,
#         batch_no=instance.batch_no,
#         expire_date=instance.expire_date,
#         mfg_date=instance.mfg_date
#         )
#         & Q(date__gte=instance.date)
#         & Q(created_date__gte=instance.created_date)
#     ).order_by('trans_date','created_date')
#     average_price = 0
#     item_obj = Item.objects.select_for_update().get(item_id=instance.item_id)
#     inventory_account = item_obj.inventory_account
#     closing_acc = COA.get_closing_account(instance.company_id)
#     inv_acc = COA.objects.get(company_id=instance.company_id, coa_id=inventory_account)
#     to_closing_acc = COA.get_closing_account(instance.company_id)
#     from_inventory_acc = COA.objects.get(company_id=instance.company_id, coa_id=inventory_account)
#     for index,stock in enumerate(stocks):
#         instance = stock
#         if index == 0 or stock.stock_in > 0 or stock.formname == 'Debit Note':
#             result = Stock.objects.filter(Q(
#                         item_id=instance.item_id,
#                         batch_no=instance.batch_no,
#                         expire_date=instance.expire_date,
#                         mfg_date=instance.mfg_date,
#                         date__lte=instance.date,
#                         created_date__lte=instance.created_date
#                         ) & (Q(stock_in__gt=0) | Q(formname='Debit Note'))
#                     ).aggregate(
#                         total_amount=Sum('amount'),
#                         total_quantity=Sum('quantity'))
#             average_price = result['total_amount'] / result['total_quantity'] if result['total_quantity'] else 0
#             average_price = float(round(average_price,2))
#
#         if instance.batch_no:
#             qty = Stock.objects.filter(Q(item_id=item_obj.item_id,
#                                           expire_date=instance.expire_date,
#                                           mfg_date=instance.mfg_date,
#                                           branch_id=instance.branch_id.branch_id,
#                                           batch_no=instance.batch_no,
#                                           date__lte=instance.date,
#                                           created_date__lte=instance.created_date
#                                          )
#                                        & Q ()
#
#                                        ).stock_quantity
#         else:
#             qty = Stock.objects.get(item_id=item_obj.item_id,
#                                     expire_date=instance.expire_date,
#                                     mfg_date=instance.mfg_date,
#                                     branch_id=instance.branch_id.branch_id,
#                                     batch_no__isnull=True).stock_quantity
#
#         amount = average_price * float(qty)
#
#     if created:
#         obj = MasterTransaction.objects.create(
#                         L1detail_id=stock.st_id,
#                         L1detailstbl_name="Stock",
#                         L2detail_id=stock.item_id,
#                         L2detailstbl_name='Item',
#                         main_module='Stock',
#                         module='Item',
#                         batch_no=stock.batch_no,
#                         expire_date=stock.expire_date,
#                         mfg_date=stock.mfg_date,
#                         company_id=stock.company_id,
#                         branch_id=stock.branch_id,
#                         to_account=TO_COA.coa_id,
#                         to_acc_type=TO_COA.account_type,
#                         to_acc_head=TO_COA.account_head,
#                         to_acc_subhead=TO_COA.account_subhead,
#                         to_acc_name=TO_COA.account_name,
#                         from_account=FROM_COA.coa_id,
#                         from_acc_type=FROM_COA.account_type,
#                         from_acc_head=FROM_COA.account_head,
#                         from_acc_subhead=FROM_COA.account_subhead,
#                         from_acc_name=FROM_COA.account_name,
#                     )
#         obj.debit = amount
#         obj.trans_date = stock.date
#         obj.credit = amount
#         obj.rate = stock.rate
#         obj.save()
#     else:
#         obj = MasterTransaction.objects.get(
#             L1detail_id=stock.st_id
#         )
#         obj.debit = amount
#         obj.trans_date = stock.date
#         obj.credit = amount
#         obj.rate = stock.rate
#         obj.save()
#
#
#     # if instance.quantity != 0:
#     #     with connection.cursor() as cursor:
#     #         args = [instance.item_id,instance.company_id.company_id,instance.branch_id.branch_id,
#     #                                            instance.batch_no,instance.expire_date ,
#     #                 instance.mfg_date ,instance.module,
#     #                                            instance.quantity]
#     #         cursor.execute(
#     #             "CALL fifo_procedure(%s, %s, %s, %s, %s, %s, %s, %s)",
#     #             args
#     #         )
#     #
#     #     print("fifo completed")
#     # return
#     # if instance.module not in ['Transfer'] and float(instance.quantity) != 0:
#     #     item_obj = Item.objects.select_for_update().get(item_id=instance.item_id)
#     #     inventory_account = item_obj.inventory_account
#     #     print(inventory_account,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     #
#     #     MasterTransaction.objects.select_for_update().filter(
#     #         L2detail_id=instance.item_id,
#     #         L2detailstbl_name='Item',
#     #         main_module='Stock',
#     #         company_id=instance.company_id,
#     #         branch_id=instance.branch_id,
#     #         batch_no=instance.batch_no,
#     #         expire_date=instance.expire_date,
#     #         mfg_date=instance.mfg_date
#     #     ).delete()
#     #
#     #     stock_entries  = Stock.objects.filter(Q(
#     #         item_id=instance.item_id,
#     #         batch_no=instance.batch_no,
#     #         expire_date=instance.expire_date,
#     #         mfg_date=instance.mfg_date,
#     #         stock_in__gt=0
#     #     )).order_by('date', 'created_date').iterator(chunk_size=10)
#     #     stock_outs = Stock.objects.filter(Q(
#     #         item_id=instance.item_id,
#     #         batch_no=instance.batch_no,
#     #         expire_date=instance.expire_date,
#     #         mfg_date=instance.mfg_date,
#     #         stock_out__gt=0,
#     #     ) & (Q(rate__gt=0) | Q(module='Transfer'))).order_by('date', 'created_date')
#     #     print(stock_outs)
#     #     stock_outs = stock_outs.iterator(chunk_size=10)
#     #     target_quantity = 0
#     #     # FIFO: Iterate over stock entries and apply usage
#     #     stock_out_completed = False
#     #     stock_out_obj = None
#     #     stock_out_list = []
#     #     credit_outs = []
#     #     result  = Stock.objects.filter(Q(
#     #         item_id=instance.item_id,
#     #         batch_no=instance.batch_no,
#     #         expire_date=instance.expire_date,
#     #         mfg_date=instance.mfg_date,
#     #         stock_in__gt=0
#     #     )).aggregate(
#     #         total_amount=Sum('amount'),
#     #         total_quantity=Sum('quantity'))
#     #     average_price = result['total_amount'] / result['total_quantity'] if result['total_quantity'] else 0
#     #     average_price = float(round(average_price,2))
#     #     FROM_COA = COA.get_closing_account(instance.company_id)
#     #     TO_COA = COA.objects.get(company_id=instance.company_id, coa_id=inventory_account)
#     #     STOCK_TO_COA = FROM_COA
#     #     STOCK_FROM_COA = TO_COA
#     #     for stock in stock_entries:
#     #         print(stock)
#     #         amount = 0
#     #         stock_id_out = None
#     #         stock_date_out = None
#     #
#     #         stock_in = float(stock.quantity)
#     #         if stock.rate > 0:
#     #             obj = MasterTransaction.objects.create(
#     #                 L1detail_id=stock.st_id,
#     #                 L1detailstbl_name="Stock",
#     #                 L2detail_id=stock.item_id,
#     #                 L2detailstbl_name='Item',
#     #                 main_module='Stock',
#     #                 module='Item',
#     #                 batch_no=stock.batch_no,
#     #                 expire_date=stock.expire_date,
#     #                 mfg_date=stock.mfg_date,
#     #                 company_id=stock.company_id,
#     #                 branch_id=stock.branch_id,
#     #                 to_account=TO_COA.coa_id,
#     #                 to_acc_type=TO_COA.account_type,
#     #                 to_acc_head=TO_COA.account_head,
#     #                 to_acc_subhead=TO_COA.account_subhead,
#     #                 to_acc_name=TO_COA.account_name,
#     #                 from_account=FROM_COA.coa_id,
#     #                 from_acc_type=FROM_COA.account_type,
#     #                 from_acc_head=FROM_COA.account_head,
#     #                 from_acc_subhead=FROM_COA.account_subhead,
#     #                 from_acc_name=FROM_COA.account_name,
#     #             )
#     #             obj.debit = stock.amount
#     #             obj.trans_date = stock.date
#     #             obj.credit = stock.amount
#     #             obj.rate = stock.rate
#     #             obj.save()
#     #
#     #         try:
#     #
#     #             while True and not stock_out_completed:
#     #                 if target_quantity == 0:
#     #                     stock_out_obj = next(stock_outs)
#     #                     target_quantity = float(abs(stock_out_obj.stock_out))
#     #
#     #                 stock_id_out = stock_out_obj.st_id
#     #                 stock_date_out = stock_out_obj.date
#     #                 if stock_out_obj.formname == 'Credit Note':
#     #                     if stock_out_list:
#     #                         temp = stock_out_list.pop()
#     #                         qty,rate = temp[0],temp[1]
#     #                         if qty >= target_quantity:
#     #                             amount = qty * rate
#     #                             target_quantity = 0
#     #                         else:
#     #                             amount = qty * rate
#     #                             target_quantity -= qty
#     #                         obj = MasterTransaction.objects.create(
#     #                             L1detail_id=stock_out_obj.st_id,
#     #                             L1detailstbl_name="Stock",
#     #                             L2detail_id=stock_out_obj.item_id,
#     #                             L2detailstbl_name='Item',
#     #                             main_module='Stock',
#     #                             module='Item',
#     #                             batch_no=stock_out_obj.batch_no,
#     #                             expire_date=stock_out_obj.expire_date,
#     #                             mfg_date=stock_out_obj.mfg_date,
#     #                             company_id=stock_out_obj.company_id,
#     #                             branch_id=stock_out_obj.branch_id,
#     #                             to_account=TO_COA.coa_id,
#     #                             to_acc_type=TO_COA.account_type,
#     #                             to_acc_head=TO_COA.account_head,
#     #                             to_acc_subhead=TO_COA.account_subhead,
#     #                             to_acc_name=TO_COA.account_name,
#     #                             from_account=FROM_COA.coa_id,
#     #                             from_acc_type=FROM_COA.account_type,
#     #                             from_acc_head=FROM_COA.account_head,
#     #                             from_acc_subhead=FROM_COA.account_subhead,
#     #                             from_acc_name=FROM_COA.account_name,
#     #                         )
#     #                         obj.debit = amount
#     #                         obj.trans_date = stock_out_obj.date
#     #                         obj.credit = amount
#     #                         obj.rate = rate
#     #                         obj.save()
#     #                     else:
#     #                         rate = average_price
#     #                         amount = target_quantity * rate
#     #                         credit_outs.append((target_quantity,average_price))
#     #                         target_quantity = 0
#     #                         obj = MasterTransaction.objects.create(
#     #                             L1detail_id=stock_out_obj.st_id,
#     #                             L1detailstbl_name="Stock",
#     #                             L2detail_id=stock_out_obj.item_id,
#     #                             L2detailstbl_name='Item',
#     #                             main_module='Stock',
#     #                             module='Item',
#     #                             batch_no=stock_out_obj.batch_no,
#     #                             expire_date=stock_out_obj.expire_date,
#     #                             mfg_date=stock_out_obj.mfg_date,
#     #                             company_id=stock_out_obj.company_id,
#     #                             branch_id=stock_out_obj.branch_id,
#     #                             to_account=TO_COA.coa_id,
#     #                             to_acc_type=TO_COA.account_type,
#     #                             to_acc_head=TO_COA.account_head,
#     #                             to_acc_subhead=TO_COA.account_subhead,
#     #                             to_acc_name=TO_COA.account_name,
#     #                             from_account=FROM_COA.coa_id,
#     #                             from_acc_type=FROM_COA.account_type,
#     #                             from_acc_head=FROM_COA.account_head,
#     #                             from_acc_subhead=FROM_COA.account_subhead,
#     #                             from_acc_name=FROM_COA.account_name,
#     #                         )
#     #                         obj.debit = amount
#     #                         obj.trans_date = stock_out_obj.date
#     #                         obj.credit = amount
#     #                         obj.rate = rate
#     #                         obj.save()
#     #                 elif credit_outs and stock_out_obj.formname != 'Debit Note':
#     #                     temp = credit_outs.pop()
#     #                     qty,rate = temp[0],temp[1]
#     #                     if qty >= target_quantity:
#     #                         amount = target_quantity * rate
#     #                         qty -= target_quantity
#     #                         credit_outs.append((qty,rate))
#     #                         target_quantity = 0
#     #                     else:
#     #                         amount = target_quantity * rate
#     #                         target_quantity -= qty
#     #                     if amount > 0:
#     #                         obj = MasterTransaction.objects.create(
#     #                             L1detail_id=stock_id_out,
#     #                             L1detailstbl_name="Stock",
#     #                             L2detail_id=instance.item_id,
#     #                             L2detailstbl_name='Item',
#     #                             main_module='Stock',
#     #                             module='Item',
#     #                             batch_no=instance.batch_no,
#     #                             expire_date=instance.expire_date,
#     #                             mfg_date=instance.mfg_date,
#     #                             company_id=instance.company_id,
#     #                             branch_id=instance.branch_id,
#     #                             to_account=STOCK_TO_COA.coa_id,
#     #                             to_acc_type=STOCK_TO_COA.account_type,
#     #                             to_acc_head=STOCK_TO_COA.account_head,
#     #                             to_acc_subhead=STOCK_TO_COA.account_subhead,
#     #                             to_acc_name=STOCK_TO_COA.account_name,
#     #                             from_account=STOCK_FROM_COA.coa_id,
#     #                             from_acc_type=STOCK_FROM_COA.account_type,
#     #                             from_acc_head=STOCK_FROM_COA.account_head,
#     #                             from_acc_subhead=STOCK_FROM_COA.account_subhead,
#     #                             from_acc_name=STOCK_FROM_COA.account_name,
#     #                         )
#     #                         obj.debit = amount
#     #                         obj.trans_date = stock_date_out
#     #                         obj.credit = amount
#     #                         obj.rate = stock.rate
#     #                         obj.save()
#     #
#     #                 elif stock_in >= target_quantity:
#     #                     if stock_out_obj.formname == 'Debit Note':
#     #                         rate = float(stock_out_obj.rate)
#     #
#     #                     else:
#     #                         rate = float(stock.rate)
#     #                         stock_out_list.append((target_quantity,rate))
#     #                     amount = target_quantity * rate
#     #
#     #                     stock_in -= target_quantity
#     #                     target_quantity = 0
#     #                     if amount > 0:
#     #
#     #                         obj = MasterTransaction.objects.create(
#     #                             L1detail_id=stock_id_out,
#     #                             L1detailstbl_name="Stock",
#     #                             L2detail_id=instance.item_id,
#     #                             L2detailstbl_name='Item',
#     #                             main_module='Stock',
#     #                             module='Item',
#     #                             batch_no=instance.batch_no,
#     #                             expire_date=instance.expire_date,
#     #                             mfg_date=instance.mfg_date,
#     #                             company_id=instance.company_id,
#     #                             branch_id=instance.branch_id,
#     #                             to_account=STOCK_TO_COA.coa_id,
#     #                             to_acc_type=STOCK_TO_COA.account_type,
#     #                             to_acc_head=STOCK_TO_COA.account_head,
#     #                             to_acc_subhead=STOCK_TO_COA.account_subhead,
#     #                             to_acc_name=STOCK_TO_COA.account_name,
#     #                             from_account=STOCK_FROM_COA.coa_id,
#     #                             from_acc_type=STOCK_FROM_COA.account_type,
#     #                             from_acc_head=STOCK_FROM_COA.account_head,
#     #                             from_acc_subhead=STOCK_FROM_COA.account_subhead,
#     #                             from_acc_name=STOCK_FROM_COA.account_name,
#     #                         )
#     #                         obj.debit = amount
#     #                         obj.trans_date = stock_date_out
#     #                         obj.credit = amount
#     #                         obj.rate = stock.rate
#     #                         obj.save()
#     #                 else:
#     #                     if stock_out_obj.formname == 'Debit Note':
#     #                         rate = float(stock_out_obj.rate)
#     #                     else:
#     #                         rate = float(stock.rate)
#     #                         stock_out_list.append((stock_in, rate))
#     #                     stk_qty = stock_in
#     #                     amount = stk_qty * rate
#     #                     target_quantity -= stk_qty
#     #                     if amount > 0:
#     #
#     #                         obj = MasterTransaction.objects.create(
#     #                             L1detail_id=stock_id_out,
#     #                             L1detailstbl_name="Stock",
#     #                             L2detail_id=instance.item_id,
#     #                             L2detailstbl_name='Item',
#     #                             main_module='Stock',
#     #                             module='Item',
#     #                             batch_no=instance.batch_no,
#     #                             expire_date=instance.expire_date,
#     #                             mfg_date=instance.mfg_date,
#     #                             company_id=instance.company_id,
#     #                             branch_id=instance.branch_id,
#     #                             to_account=STOCK_TO_COA.coa_id,
#     #                             to_acc_type=STOCK_TO_COA.account_type,
#     #                             to_acc_head=STOCK_TO_COA.account_head,
#     #                             to_acc_subhead=STOCK_TO_COA.account_subhead,
#     #                             to_acc_name=STOCK_TO_COA.account_name,
#     #                             from_account=STOCK_FROM_COA.coa_id,
#     #                             from_acc_type=STOCK_FROM_COA.account_type,
#     #                             from_acc_head=STOCK_FROM_COA.account_head,
#     #                             from_acc_subhead=STOCK_FROM_COA.account_subhead,
#     #                             from_acc_name=STOCK_FROM_COA.account_name,
#     #                         )
#     #                         obj.debit = amount
#     #                         obj.trans_date = stock_date_out
#     #                         obj.credit = amount
#     #                         obj.rate = stock.rate
#     #                         obj.save()
#     #                     break
#     #
#     #         except Exception as e:
#     #             traceback.print_exc()
#     #             print("Broke becoz no sale out present")
#     #             stock_out_completed = True
#     #             continue






