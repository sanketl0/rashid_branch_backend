from django.db import models
from salescustomer.BaseModel import BaseDateid
from salescustomer.models.Invoice_model import Invoice
from purchase.models.Paymentmade_model import PaymentMade
from salescustomer.models.Pr_model import PR
from purchase.models.Bill_model import Bill
from accounting.models import ManualJournal
import uuid
from company.models import Company, Branch
from registration.models import user
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bank(BaseDateid):
    bank_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name


def statement_path(instance, filename):
    return f'statements/{filename}'


class FileUpload(BaseDateid):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    bank_id = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True,related_name='statement_files')
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL,blank=True, null=True,related_name='company_files')
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL,blank=True, null=True)
    user_id = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    filename = models.CharField(max_length=200,blank=True,null=True)
    # file = models.FileField(upload_to=statement_path)
    parse = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    error_message = models.CharField(max_length=300,blank=True,null=True)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.filename if self.filename else "No Name"

class Transaction(BaseDateid):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file_id = models.ForeignKey(FileUpload, on_delete=models.SET_NULL,blank=True, null=True,related_name='transactions')
    date=models.DateField(blank=True,null=True)
    description = models.CharField(max_length=300,blank=True,null=True)
    reference = models.CharField(max_length=200,blank=True,null=True)
    credit = models.FloatField(default=0)
    debit = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return str(self.balance)

class TransactionDetail(BaseDateid):
    transaction_detail_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    transaction_id = models.ForeignKey(Transaction,null=True, on_delete=models.SET_NULL,related_name='transaction_details')
    amount = models.FloatField(default=0)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_id = models.ManyToManyField(Bill,blank=True,related_name='bill_transaction')
    invoice_id = models.ManyToManyField(Invoice,blank=True,related_name='invoice_transaction')
    purchase_id = models.ManyToManyField(PaymentMade,blank=True,related_name='purchase_transactions')
    voucher_id = models.ManyToManyField(ManualJournal,blank=True,related_name='voucher_transactions')
    payment_id = models.ManyToManyField(PR,blank=True,related_name='payment_transactions')

    class Meta:
        ordering = ['-created_date']

@receiver(post_save,sender=Transaction)
def create_balance(sender,instance,created,**kwargs):
    if created:
        if instance.credit:
            instance.balance = instance.credit
        if instance.debit:
            instance.balance = instance.debit
        instance.save()


@receiver(post_save,sender=TransactionDetail)
def update_balance(sender,instance,created,**kwargs):
    if created:
        if instance.transaction_id:

            instance.transaction_id.balance -= float(instance.amount)
            instance.transaction_id.balance = round(instance.transaction_id.balance,2)
            instance.transaction_id.save()

            print(instance.transaction_id.balance,instance.amount)
            if instance.transaction_id.balance <= 0:
                instance.transaction_id.paid = True
                instance.transaction_id.save()