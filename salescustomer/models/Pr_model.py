
import uuid

from django.db import models
from coa.models import COA
from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount


EXT_TYPE = (
    ('TALLY','TALLY'),
)
class PR(BaseDateid):
    pr_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True,related_name='invoice_prs')
    coa_id = models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
    so_id = models.ForeignKey("salescustomer.SO", on_delete=models.SET_NULL, null=True)
    dc_id = models.ForeignKey("salescustomer.DC", on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True,
                                    related_name='customer_payment')
    est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    amount_received = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    bank_id = models.ForeignKey("banking.Banking", on_delete=models.SET_NULL, null=True)
    form_type = models.CharField(max_length=200, blank=True, default='Payment Receive', null=True)
    is_bank_transaction = models.BooleanField(default=False)
    bank_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    deposit_to = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_deducted = models.CharField(max_length=200, blank=True, default='null', null=True)
    tds_tax_account = models.CharField(max_length=200, blank=True, default='null', null=True)
    date = models.DateField(blank=True, null=True)
    invoice_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    party_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_pr_party')
    coa_total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    igst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_pr_igst')
    cgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_pr_cgst')
    sgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_pr_sgst')

    amount_excess = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_used_payment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    is_converted = models.BooleanField(default=False)
    pay_generated = models.BooleanField(default=False)
    payment_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_date = models.DateField(blank=True, null=True)
    pay_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_mode = models.CharField(max_length=200, blank=True, default='null', null=True)
    pay_method = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_terms = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_note = models.CharField(max_length=200, blank=True, default='null', null=True)
    notes = models.TextField(blank=True,null=True)
    terms_condition = models.CharField(max_length=200, blank=True, default='null', null=True)
    attach_file = models.FileField(max_length=200, blank=True, default='null', null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    PreferredPaymentMethodRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    PaymentMethodRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    PaymentMethodRefFullName = models.CharField(max_length=200, blank=True, default='null', null=True)
    ListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    EditSequence = models.CharField(max_length=200, blank=True, default='null', null=True)
    Name = models.CharField(max_length=200, blank=True, default='null', null=True)
    IsActive = models.BooleanField(default=False)
    CreditCardNumber = models.IntegerField(default=0)
    CreditCardExpirationMonth = models.CharField(max_length=200, blank=True, default='null', null=True)
    CreditCardExpirationYear = models.CharField(max_length=200, blank=True, default='null', null=True)
    CreditCardNameOnCard = models.CharField(max_length=200, blank=True, default='null', null=True)
    CreditCardAddress = models.CharField(max_length=200, blank=True, default='null', null=True)
    CreditCardPostalCode = models.IntegerField(default=0)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'Payment Receive'
        ordering =['-created_date']

    def __str__(self):
        if(self.company_id):
            return self.company_id.company_name
        return self.pr_id


class PrView(models.Model):
    pr_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    payment_date = models.DateField(blank=True, null=True)
    company_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    branch_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount_excess = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    payment_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_received = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    invoice_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    customer_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_mode = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        managed = False
        db_table = 'pr_view'