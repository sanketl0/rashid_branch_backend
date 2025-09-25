import uuid
from company.models import Company, Branch,Company_Year
from django.db import models
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount,BaseTaxTotal
from django.db.models.signals import post_save
from django.dispatch import receiver
from transaction.models import MasterTransaction
from coa.models import COA

class Charges(BaseTaxAmount,BaseDateid):
    chg_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    charge_name = models.CharField(max_length=200, blank=True, null=True)
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
    bill_id = models.ForeignKey("purchase.Bill", on_delete=models.SET_NULL, null=True)
    amt_qty = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate_per = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_charge = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)


    class Meta:
        ordering =['-created_date']

    def __str__(self):
        return self.charge_name



@receiver(post_save, sender=Charges)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    A signal handler that creates a Token when a new User is created.
    """
    if created:
        company_id = instance.company_id
        if instance.invoice_id:
            if instance.invoice_idpayment_status == "paid":
                account_receivable = COA.objects.get(company_id=company_id, account_name="Sales to Customer(Cash)")
            else:
                account_receivable = COA.objects.get(company_id=company_id, account_subhead="Account Receivables")
            TO_COA = COA.objects.get(company_id=company_id, account_name="Output Charges")
            MasterTransaction.objects.create(
                L1detail_id=instance.invoice_id.invoice_id,
                L1detailstbl_name='Invoice',
                main_module='Sales',
                module='Invoice',
                sub_module='Invoice',
                transc_deatils='Invoice',
                banking_module_type='Invoice',
                journal_module_type='Invoice',
                trans_date=instance.invoice_id.invoice_date,
                trans_status='Manually Added',
                debit=instance.total_charge,
                to_account=account_receivable.coa_id,
                to_acc_type=account_receivable.account_type,
                to_acc_head=account_receivable.account_head,
                to_acc_subhead=account_receivable.account_subhead,
                to_acc_name=account_receivable.account_name,
                credit=instance.total_charge,
                from_account=TO_COA.coa_id,
                from_acc_type=TO_COA.account_type,
                from_acc_head=TO_COA.account_head,
                from_acc_subhead=TO_COA.account_subhead,
                from_acc_name=TO_COA.account_name,
                company_id=company_id,
                customer_id=instance.invoice_id.customer_id)