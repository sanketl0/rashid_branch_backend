import uuid
from django.db import models
from company.models import Company, Branch,Company_Year
from salescustomer .BaseModel import *
# Create your models here.
EXT_TYPE = (
    ('TALLY','TALLY'),
)
class ManualJournal(BaseDateid):
    mj_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    ext_id = models.CharField(max_length=100, blank=True, null=True)
    ext_type = models.CharField(max_length=100, default='TALLY',choices=EXT_TYPE)
    journal_date = models.DateField(blank=True, null=True)    
    journal_ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    journal_status = models.CharField(max_length=200, default='null', blank=True, null=True)
    journal_serial_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    journal_type = models.CharField(max_length=200, default='null', blank=True, null=True)
    is_journal_generated = models.BooleanField(default=False)    
    journal_amount=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sub_total=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    difference=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)     
    attach_file = models.FileField(default='null', blank=True, null=True)    

    class Meta:
        verbose_name_plural = 'ManualJournal'     

    def __str__(self):
        return str(self.mj_id)

class JournalTransaction(BaseDateid):
    jt_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    mj_id=models.ForeignKey("accounting.ManualJournal", on_delete=models.SET_NULL, null=True, related_name='journal_transactions')
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)  
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True) 
    customer_id=models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True) 
    date = models.DateField(blank=True, null=True)
    vendor_id=models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True) 
    coa_id=models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True, related_name='jt_coa') 
    transaction_type= models.CharField(max_length=200, default='Journal', null=True)
    account = models.CharField(max_length=200, default='null', blank=True, null=True)
    des = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=200, default='null', blank=True, null=True) #customer_id taken from UI
    debit=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    credit=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)       
   
    
    class Meta:
        verbose_name_plural = 'Journal Transaction'     
    def __str__(self):
        return self.des
        
class RecJournal(BaseDateid):
    rj_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    mj_id = models.ForeignKey(ManualJournal, on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)  
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)  
    profile_name = models.CharField(max_length=50, default='null', blank=True, null=True)
    repeat_every = models.CharField(max_length=50, default='null', blank=True, null=True)
    starts_on = models.DateField(blank=True, null=True)
    ends_on = models.DateField(blank=True, null=True)
    never_expires = models.CharField(max_length=50, default='null', blank=True, null=True)
    journal_no = models.CharField(max_length=50, default='null', blank=True, null=True)
    mj_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
    notes = models.CharField(max_length=100, default='null', blank=True, null=True)
    journal_type = models.CharField(max_length=100, default='null', blank=True, null=True)
    account = models.CharField(max_length=100, default='null', blank=True, null=True)
    des = models.CharField(max_length=100, default='null', blank=True, null=True)
    contact = models.CharField(max_length=15, default='null', blank=True, null=True)
    debit=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    credit=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sub_total=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    difference=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    mj_status = models.CharField(max_length=50, default='null', blank=True, null=True)
    mj_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
    
    
    class Meta:
        verbose_name_plural = 'RecJournal'     
    def __str__(self):
        return self.profile_name

class BulkUpdate(BaseDateid):
    bu_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)  
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    account = models.CharField(max_length=100, default='null', blank=True, null=True)    
    account_name = models.CharField(max_length=50, default='null', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    total_amount_range=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    expense_account = models.CharField(max_length=50, default='null', blank=True, null=True)
    bu_ref_no = models.CharField(max_length=50, default='null', blank=True, null=True)
    vendor_name = models.CharField(max_length=50, default='null', blank=True, null=True)
    paid_through = models.CharField(max_length=50, default='null', blank=True, null=True)
    customer_name = models.CharField(max_length=50, default='null', blank=True, null=True)
    amount=models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    bulk_update_status = models.CharField(max_length=50, default='null', blank=True, null=True)
    journal_no = models.CharField(max_length=50, default='null', blank=True, null=True)
    bu_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'BulkUpdate'     
    def __str__(self):
        return self.account_name

class Budget(BaseDateid):
    budget_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)  
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    fiscal_year = models.DateField(blank=True, null=True)
    income_acc = models.CharField(max_length=50, default='null', blank=True, null=True)
    expence_acc = models.CharField(max_length=50, default='null', blank=True, null=True)
    asset_acc = models.CharField(max_length=50, default='null', blank=True, null=True)
    liability_acc = models.CharField(max_length=50, default='null', blank=True, null=True)
    equity_acc = models.CharField(max_length=50, default='null', blank=True, null=True)
    name = models.CharField(max_length=50, default='null', blank=True, null=True)
    budget_period = models.CharField(max_length=50, default='null', blank=True, null=True)
    reporting_tag = models.CharField(max_length=50, default='null', blank=True, null=True)
    location = models.CharField(max_length=50, default='null', blank=True, null=True)    
    budget_serial = models.CharField(max_length=50, default='null', blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Budget'     
    def __str__(self):
        return self.name


