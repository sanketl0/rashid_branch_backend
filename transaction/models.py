from django.db import models
import uuid
from django.db.models.signals import post_save,pre_save,pre_delete
from django.dispatch import receiver
from coa.models import COA
from salescustomer.models.Salescustomer_model import SalesCustomer
from salescustomer.models.Invoice_model import Invoice
from salescustomer.BaseModel import BaseDateid
from company.models import Company,Branch,Company_Year
#Commented By SK
# Master Transaction 
# All the Transaction Of Banking Sales And Purchase 
class MasterTransaction(BaseDateid):
    mast_id=models.UUIDField(primary_key=True, default = uuid.uuid4)
    L1detail_id=models.CharField(max_length=200, blank=True, default='null', null=True)
    L1detailstbl_name= models.CharField(max_length=200, blank=True, default='null', null=True)
    debit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True,default=0.00)
    credit =models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True,default=0.00)     
    L2detail_id= models.CharField(max_length=200, blank=True, default='null', null=True)
    L2detailstbl_name= models.CharField(max_length=200, blank=True, default='null', null=True)
    L3detail_id= models.CharField(max_length=200, blank=True, default='null', null=True)
    L3detailstbl_name= models.CharField(max_length=200, blank=True, default='null', null=True)
    main_module= models.CharField(max_length=200, blank=True, default='null', null=True)
    module= models.CharField(max_length=200, blank=True, default='null', null=True)
    sub_module= models.CharField(max_length=200, blank=True, default='null', null=True)
    transc_deatils= models.CharField(max_length=200, blank=True, default='null', null=True)
    banking_module_type= models.CharField(max_length=200, blank=True, default='null', null=True)
    journal_module_type= models.CharField(max_length=200, blank=True, default='null', null=True)
    trans_date=models.DateField(blank=True,null=True)
    trans_status= models.CharField(max_length=200, blank=True, default='null', null=True)
    to_account= models.CharField(max_length=200, blank=True, default='null', null=True)
    to_acc_type= models.CharField(max_length=200, blank=True, default='null', null=True)
    to_acc_head= models.CharField(max_length=200, blank=True, default='null', null=True)
    to_acc_subhead= models.CharField(max_length=200, blank=True, default='null', null=True)
    to_acc_name= models.CharField(max_length=200, blank=True, default='null', null=True)
    from_account= models.CharField(max_length=200, blank=True, default='null', null=True)
    from_acc_type= models.CharField(max_length=200, blank=True, default='null', null=True)
    from_acc_head= models.CharField(max_length=200, blank=True, default='null', null=True)
    from_acc_subhead= models.CharField(max_length=200, blank=True, default='null', null=True)
    from_acc_name= models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_id=models.ForeignKey(SalesCustomer, on_delete=models.SET_NULL, null=True)
    vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
    is_customer= models.CharField(max_length=200, blank=True, default='null', null=True)
    comp_yearid= models.CharField(max_length=200, blank=True, default='null', null=True)
    company_id=models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    branch_id=models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    attach_file = models.FileField(default='null', blank=True, null=True)
    batch_no = models.CharField(max_length=200, blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True,default=0.00)

    class Meta:
        verbose_name_plural = 'Master_Transaction'
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.from_acc_name}=>{self.to_acc_name} => {self.trans_date}'

    def updateBalance(self,new_debit,new_credit):
        pass
        # if self.L1detailstbl_name == "Invoice" or "Payment Made" or "PR" or "Bill":
        #     print(new_debit,self.debit,"update balance")
        #     account_from = COA.objects.get(coa_id=self.from_account)
        #     account_to = COA.objects.get(coa_id=self.to_account)
        #     if account_from.account_type in ["Assets", "Expenses"]:
        #         account_from.Balance = account_from.Balance  + round(float(self.debit), 2)  - round(float(new_debit), 2)
        #
        #     else:
        #         account_from.Balance = account_from.Balance - round(float(self.credit), 2) + round(float(new_credit), 2)
        #
        #     account_from.save()
        #
        #     if account_to.account_type in ["Assets", "Expenses"]:
        #         account_to.Balance = account_to.Balance - round(float(self.credit), 2) + round(float(new_debit), 2)
        #
        #     else:
        #         account_to.Balance = account_to.Balance + round(float(self.credit), 2) - round(float(new_credit), 2)
        #
        #     account_to.save()




rate_per_choices = [
    ('rate', 'rate'),
    ('percentage', 'percentage'),

]

amt_qty_choices = [
    ('total', 'total'),
    ('custom', 'custom'),

]
CHARGES_TYPE = [
    ('DEFAULT', 'DEFAULT'),
    ('TAX', 'TAX'),

]
class Charges(BaseDateid):
    chg_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    charge_name = models.CharField(max_length=200, blank=True, null=True)
    amt_qty = models.CharField(max_length=200, blank=True, null=True,choices=amt_qty_choices)
    rate_per = models.CharField(max_length=200, blank=True, null=True,choices=rate_per_choices)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    percentage = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    class Meta:
        ordering =['-created_date']

    def __str__(self):
        return self.charge_name

class ChargeTransaction(BaseDateid):
    chg_transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    chg_id = models.ForeignKey(Charges, on_delete=models.SET_NULL, null=True,related_name='charges_transaction')
    bill_id = models.ForeignKey("purchase.Bill", on_delete=models.SET_NULL, null=True,related_name='bill_charge_transactions')
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True,related_name='invoice_charge_transactions')

    total_amt = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amt = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        if self.invoice_id:
            return "Invoice"
        else:
            return "Bill"

class CoaCharges(BaseDateid):
    ch_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True,related_name='coa_charges')
    coa_name = models.CharField(max_length=200, blank=True, null=True)
    credit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    debit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    module = models.CharField(max_length=200, blank=True, null=True)
    bill_id = models.ForeignKey("purchase.Bill", on_delete=models.SET_NULL, null=True,
                                related_name='bill_coa_transactions')
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True,
                                   related_name='invoice_coa_transactions')
    dn_id = models.ForeignKey("purchase.DebitNote", on_delete=models.SET_NULL, null=True,
                                related_name='dn_coa_transactions')
    cn_id = models.ForeignKey("salescustomer.CreditNote", on_delete=models.SET_NULL, null=True,
                              related_name='cn_coa_transactions')
    charges_type = models.CharField(max_length=200, default='DEFAULT', choices=CHARGES_TYPE)
    name = models.CharField(max_length=200,blank=True,null=True)
