from django.db import models
import uuid
# Create your models here.
from rest_framework import serializers


class Dashboard(models.Model):

    month = models.PositiveIntegerField(default=0)
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profit_loss = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    purchase = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sales = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    pr = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    pm = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dashboard'


class DashboardTotal(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cash_bank = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_receivable = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_payable = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    invoice_count = models.PositiveIntegerField(default=0)
    bill_count = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'dashboard_total'

class StockValuationReport(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.UUIDField(blank=True, null=True)
    branch_id = models.UUIDField(blank=True, null=True)
    stk_in = models.IntegerField(default=0)
    stk_out = models.IntegerField(default=0)
    qty = models.IntegerField(default=0)
    last_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    valuation = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    batch_no = models.CharField(max_length=200,blank=True,null=True)
    created_date = models.DateField(blank=True, null=True)
    mfg_date = models.DateField(blank=True,null=True)
    expire_date = models.DateField(blank=True, null=True)
    item_name = models.CharField(max_length=200,blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'stock_report'


class StockReport(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cash_bank = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_receivable = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_payable = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    invoice_count = models.PositiveIntegerField(default=0)
    bill_count = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'dashboard_total'

class AccountReport(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account_name = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_type = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_head = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_subhead = models.CharField(max_length=100, blank=True, default='null', null=True)
    account = models.CharField(max_length=100, blank=True, default='null', null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_report_data_mat'

class AccountBalance(models.Model):

    coa_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_name = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_type = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_head = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_subhead = models.CharField(max_length=100, blank=True, default='null', null=True)
    balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, default='null', null=True)
    value = models.CharField(max_length=100, blank=True, default='null', null=True)
    created_date = models.DateTimeField(blank=True,null=True)
    isdefault = models.BooleanField(blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'account_balance'
        ordering = ['-created_date']


class PurchaseGst(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    branch_id = models.UUIDField(blank=True, null=True)
    date = models.DateField(blank=True,null=True)
    bill_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
    module = models.CharField(max_length=20, blank=True, default='null', null=True)
    vendor_name = models.CharField(max_length=100, blank=True, default='null', null=True)
    gstin_number = models.CharField(max_length=15, blank=True, default='null', null=True)
    tax_name = models.CharField(max_length=20, blank=True, default='null', null=True)
    i_tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    c_tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    s_tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase_gst'


class SalesGst(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    branch_id = models.UUIDField(blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    invoice_serial = models.CharField(max_length=50, blank=True, default='null', null=True)
    module = models.CharField(max_length=20, blank=True, default='null', null=True)
    customer_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    gstin_number = models.CharField(max_length=15, blank=True, default='null', null=True)
    tax_name = models.CharField(max_length=20, blank=True, default='null', null=True)
    i_tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    c_tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    s_tax = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_gst'


class GSTR3B(models.Model):
    ref_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField(blank=True,null=True)
    serial =  models.CharField(max_length=50, blank=True, default='null', null=True)
    supplier =  models.CharField(max_length=50, blank=True, default='null', null=True)
    module = models.CharField(max_length=50, blank=True, default='null', null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    igst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sgst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    cgst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    company_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    branch_id = models.UUIDField(blank=True, null=True)
    supplier_name = models.CharField(max_length=100, blank=True, default='null', null=True)
    class Meta:
        managed = False
        db_table = 'gstr_3b_report'

class CashBook(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    trans_date = models.DateField(blank=True,null=True)
    detail = models.CharField(max_length=50, blank=True, default='null', null=True)
    account = models.CharField(max_length=20, blank=True, default='null', null=True)
    debit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    branch_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cash_book'

class GSTR2A(models.Model):
    ref_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField(blank=True,null=True)
    serial =  models.CharField(max_length=50, blank=True, default='null', null=True)
    vendor_name =  models.CharField(max_length=50, blank=True, default='null', null=True)
    module = models.CharField(max_length=50, blank=True, default='null', null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    igst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sgst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    cgst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    branch_id = models.UUIDField(blank=True, null=True)
    company_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'gstr_2a_report'

class GSTR2B(models.Model):
    ref_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField(blank=True,null=True)
    serial =  models.CharField(max_length=50, blank=True, default='null', null=True)
    customer_name =  models.CharField(max_length=200, blank=True, default='null', null=True)
    module = models.CharField(max_length=50, blank=True, default='null', null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    igst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sgst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    cgst_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    branch_id = models.UUIDField(blank=True, null=True)
    company_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'gstr_2b_report'

class BankBook(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    trans_date = models.DateField(blank=True, null=True)
    detail = models.CharField(max_length=50, blank=True, default='null', null=True)
    account = models.CharField(max_length=20, blank=True, default='null', null=True)
    debit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    trans_status = models.CharField(max_length=20, blank=True, default='null', null=True)
    branch_id = models.UUIDField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'bank_book'