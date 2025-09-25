from django.db import models
import uuid
from company.models import Company, Branch
from salescustomer.BaseModel import BaseDateid
from coa.models import COA
from company.models import Company_Year
from salescustomer.models.Salescustomer_model import SalesCustomer
from .banking_model import Banking





# ExpenseRefund
class ExpenseRefund(BaseDateid):
    exp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    is_expense_refund_generated = models.BooleanField()
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    bank_id = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    expense_refund_date = models.DateField(blank=True, null=True)
    vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True)
    from_account = models.CharField(max_length=200, blank=True, default='null', null=True)
    expense_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    attach_file = models.FileField(null=True, default='null', max_length=250)
    sac = models.CharField(max_length=200, blank=True, default='null', null=True)
    gst_treatment = models.CharField(max_length=200, blank=True, default='null', null=True)
    source_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    destination_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    associated_expense = models.CharField(max_length=200, blank=True, default='null', null=True)
    hsn_code = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    expense_refund_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    description = models.TextField(blank=True, null=True)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    expense_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True, default=0.00)
    received_via = models.CharField(max_length=200, blank=True, default='null', null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    class Meta:
        verbose_name_plural = 'ExpenseRefund Model'

    def __str__(self):
        return str(self.exp_id)
