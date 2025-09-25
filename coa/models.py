from django.db import models
from company.models import Company, Branch,Company_Year
from django.core.cache import cache
from salescustomer.BaseModel import *

from django.db.models.signals import post_save
from django.dispatch import receiver
EXT_TYPE = (
    ('TALLY','TALLY'),
)

TAX_TYPE = (
    ('GST','GST'),
)
# Create your models here.
class COA(BaseDateid):
    coa_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account_type = models.CharField(max_length=200, blank=True, null=True)
    account_head = models.CharField(max_length=200, blank=True, null=True)
    account_subhead = models.CharField(max_length=200, blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=100, blank=True, null=True)
    ext_type = models.CharField(max_length=50, default='TALLY', choices=EXT_TYPE)
    account_name = models.CharField(max_length=200, blank=True, null=True)
    account_code = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    add_to_watchlist_on_my_dashboard = models.BooleanField(blank=True, null=True)
    mark_this_is_sub_account = models.BooleanField(blank=True, null=True)
    is_child_allowed = models.BooleanField(blank=True, null=True)
    parent_account = models.CharField(max_length=200, blank=True, null=True)
    parent_id = models.CharField(max_length=200, blank=True, null=True, default='null')
    ListID = models.CharField(max_length=200, blank=True, null=True)
    EditSequence = models.CharField(max_length=200, blank=True, null=True)
    Name = models.CharField(max_length=200, blank=True, null=True)
    FullName = models.CharField(max_length=200, blank=True, null=True)
    IsActive = models.BooleanField(default=False, blank=True, null=True)
    ParentRefListID = models.CharField(max_length=200, blank=True, null=True)
    ParentRefFullName = models.CharField(max_length=200, blank=True, null=True)
    Sublevel = models.CharField(max_length=50, blank=True, null=True)
    SpecialAccountType = models.CharField(max_length=50, blank=True, null=True)
    IsTaxAccount = models.BooleanField(default=False, blank=True, null=True)
    AccountNumber = models.CharField(max_length=200, blank=True, null=True)
    BankNumber = models.CharField(max_length=200, blank=True, null=True)
    Balance = models.FloatField(default=0, blank=True, null=True)
    balance = models.FloatField(default=0, blank=True, null=True)
    open_balance = models.FloatField(default=0, blank=True, null=True)
    TotalBalance = models.FloatField(default=0, blank=True, null=True)
    OpenBalance = models.FloatField(default=0, blank=True, null=True)
    OpenBalanceDate = models.DateField(blank=True, null=True)
    SalesTaxCodeRefListID = models.CharField(max_length=200, blank=True, null=True)
    SalesTaxCodeRefFullName = models.CharField(max_length=200, blank=True, null=True)
    TaxCodeRefListID = models.CharField(max_length=200, blank=True, null=True)
    TaxCodeRefFullName = models.CharField(max_length=200, blank=True, null=True)
    TaxLineInfoRetTaxLineID = models.CharField(max_length=200, blank=True, null=True)
    TaxLineInfoRetTaxLineName = models.CharField(max_length=200, blank=True, null=True)
    CashFlowClassification = models.CharField(max_length=200, blank=True, null=True)
    CurrencyRefListID = models.CharField(max_length=200, blank=True, null=True)
    CurrencyRefFullName = models.CharField(max_length=200, blank=True, null=True)
    isdefault=models.BooleanField(default=False, blank=True, null=True)
    system = models.BooleanField(default=False)

    class Meta:
        db_table = "coa"
        verbose_name_plural = 'Chart Of Account'
        ordering = ['-created_date']

    def __str__(self):
        if self.account_name:
            return self.account_name
        return self.account_subhead

    @classmethod
    def get_account_paybles(cls, comp_id):
        account_payable = cls.objects.get(
            company_id=comp_id,
            system=True,
            account_subhead='Account Payables',isdefault=True)
        return account_payable
    @classmethod
    def get_inventory_assets(cls, comp_id):
        inven_assets = cls.objects.get(
            company_id=comp_id,

            account_subhead='Inventory Assets',isdefault=True)
    @classmethod
    def get_account_recievables(cls, comp_id):

        account_recievables = cls.objects.get(
            company_id=comp_id,
            system=True,
            account_subhead='Account Receivables',isdefault=True)
        return account_recievables

    @classmethod
    def get_income_adjustment(cls,cmp_id):
        income_account = cls.objects.get(
            company_id=cmp_id,account_subhead='Stock Adjustment',
            account_name='Income Adjustment',
            isdefault=True
        )
        return income_account

    @classmethod
    def get_opening_account(cls, cmp_id):
        opening_account = cls.objects.get(
            company_id=cmp_id, account_name='Opening Stock',
            system=True,
            isdefault=True
        )
        return opening_account

    @classmethod
    def get_closing_account(cls, cmp_id):
        closing_account = cls.objects.get(
            company_id=cmp_id, account_name='Closing Stock',
            system=True,
            isdefault=True
        )
        return closing_account

    @classmethod
    def get_input_igst_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Input IGST',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_output_igst_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Output IGST',
            system=True,
            isdefault=True
        )
        return account


    @classmethod
    def get_input_sgst_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Input SGST',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_output_sgst_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Output SGST',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_bank_fees_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Bank Fees and Charges',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_output_cgst_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Output CGST',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_input_cgst_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Input CGST',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_input_cess_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Input CESS',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_output_cess_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Output CESS',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_shipping_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='Shipping Charges',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_input_tcs_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='TCS Receivable',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_input_tcs_pay_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='TCS Payable',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_input_tds_account(cls, cmp_id):
        account = cls.objects.get(
            company_id=cmp_id, account_name='TDS Payable',
            system=True,
            isdefault=True
        )
        return account

    @classmethod
    def get_account(cls, coa_id):
        # result = cache.get(coa_id)
        # if result:
        #     return result
        result = cls.objects.get(
          coa_id=coa_id,
        )

        if result:
            cache.set(coa_id, result, 60 * 60 * 24)
        return result

    def get_account_name(self):
        try:
            return self.account_name
        except:
            return None
class AccountHead(BaseDateid):
    ah_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    account_type = models.CharField(max_length=50, blank=True, null=True)
    account_head = models.CharField(max_length=50, blank=True, null=True)
    account_subhead = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Account Head'

    def __str__(self):
        return self.account_type


class OpeningBalance(BaseDateid):
    ob_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='opbalance')
    available_balance = models.CharField(max_length=50, blank=True, null=True)
    opening_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    closing_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    credit = models.FloatField(blank=True, null=True)
    debit = models.FloatField(blank=True, null=True)
    migration_date = models.DateField(blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    notes = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Opening Balance'
        ordering =["-created_date"]

    def __str__(self):
        return str(self.coa_id.account_name)


class OpeningBalanceView(models.Model):
    coa_id = models.CharField(max_length=50,default=uuid.uuid4,primary_key=True)
    credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    debit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    company_id = models.CharField(max_length=50, blank=True, null=True)
    account_type = models.CharField(max_length=50, blank=True, null=True)
    account_head = models.CharField(max_length=50, blank=True, null=True)
    account_subhead = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'opening_balance_view'


class TransactionDetailCV(models.Model):
    L1detail_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    customer_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    vendor_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    company_id = models.CharField(max_length=100, primary_key=True)
    account = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_type = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_head = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_subhead = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_name = models.CharField(max_length=100, blank=True, default='null', null=True)
    trans_date = models.DateField(blank=True,null=True)
    trans_status = models.CharField(max_length=100, blank=True, default='null', null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_type = models.CharField(max_length=100, blank=True, default='null', null=True)

    class Meta:
        managed = False
        db_table = 'transaction_detail_cv'

class TransactionDetail(models.Model):
    L1detail_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    company_id = models.CharField(max_length=100, primary_key=True)
    account = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_type = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_head = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_subhead = models.CharField(max_length=100, blank=True, default='null', null=True)
    account_name = models.CharField(max_length=100, blank=True, default='null', null=True)
    trans_date = models.DateField(blank=True,null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    trans_status = models.CharField(max_length=100, blank=True, default='null', null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_type = models.CharField(max_length=100, blank=True, default='null', null=True)
    module =  models.CharField(max_length=100, blank=True, default='null', null=True)
    class Meta:
        managed = False
        db_table = 'transaction_detail'

# Create your models here.
class BaseCOA(BaseDateid):

    account_type = models.CharField(max_length=50, blank=True, null=True)
    account_head = models.CharField(max_length=50, blank=True, null=True)
    account_subhead = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)
    system = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'BaseCOA'

    def __str__(self):
        if self.account_name:
            return self.account_name
        return self.account_subhead


class Tax(BaseDateid):
    tax_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,blank=True,null=True, help_text="Name of the tax, e.g., VAT, GST")
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tax rate as a percentage, e.g., 5.00 for 5%")
    description = models.TextField(null=True, blank=True, help_text="Optional description for the tax")
    is_active = models.BooleanField(default=True, help_text="Indicates if this tax is active")
    coa_id = models.ForeignKey(COA,on_delete=models.SET_NULL, null=True,related_name='coa_taxes')
    coa_id_1 = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_1_taxes')
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True,related_name='company_taxes')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True,related_name='branch_taxes')
    system = models.BooleanField(default=False)
    account_type = models.CharField(max_length=255,default='Liabilities', help_text="account type")
    tax_type = models.CharField(max_length=200, blank=True, null=True,choices=TAX_TYPE)
    sub_section = models.CharField(max_length=200, blank=True, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)

    def __str__(self):
        return f"{self.name} - {self.rate}%"

#
# @receiver(post_save,sender=Tax)
# def create_or_update_coa(sender, instance,created,*args,**kwargs):
#     if created:
#         if instance.account_type == "Liabilities":
#             obj = COA.objects.create(
#                 account_name=instance.name,
#                 account_type=instance.account_type,
#                 account_head='Current Liabilities',
#                 account_subhead='Taxes'
#             )
#         else:
#             obj = COA.objects.create(
#                 account_name=instance.name,
#                 account_type=instance.account_type,
#                 account_head='Current Assets',
#                 account_subhead='Taxes'
#             )
#         instance.coa_id = obj
#         instance.save()
#     else:
#         instance.coa_id.account_name = instance.name
#         instance.coa_id.save()


@receiver(post_save, sender=BaseCOA)
def base_coa_post_save(sender, instance,created, **kwargs):
    if created:
        comp = Company.objects.all()
        print("Creating coa for company")
        basecoa = instance
        for company in comp:
            COA.objects.create(
                account_head=basecoa.account_head,
                account_subhead=basecoa.account_subhead,
                account_name=basecoa.account_name,
                account_type=basecoa.account_type,
                system=basecoa.system,
                isdefault=True,
                company_id_id=str(company.company_id)
            )

