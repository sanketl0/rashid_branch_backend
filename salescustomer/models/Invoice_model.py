import uuid

from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from coa.models import COA
from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount
from .So_model import SO

EXT_TYPE = (
    ('TALLY','TALLY'),
)

class Invoice(BaseDateid):
    invoice_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True,
                                    related_name='customer_invoices',blank=True)
    customer_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
    est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
    tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    invoice_date = models.DateField(blank=True, null=True)
    is_invoice_generated = models.BooleanField(default=False)
    retail_invoice = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_received = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    order_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    due_date = models.DateField(blank=True, null=True)
    delivery_method = models.CharField(max_length=200, blank=True, default='null', null=True)
    term_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    no_of_days = models.IntegerField(default=0, blank=True, null=True)
    project_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    subject = models.CharField(max_length=200, blank=True, default='null', null=True)
    total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount_type = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    cgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    sgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    igst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    cess_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    charges = models.ManyToManyField('transaction.ChargeTransaction',related_name='charges_transaction', blank=True)
    total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    party_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sales_party')
    sales_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sales')
    coa_total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    igst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True,related_name='coa_sales_igst')
    cgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sales_cgst')
    sgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sales_sgst')
    shipping_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_salesshipping')
    tcs_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sales_tcs')
    tds_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sales_tds')
    cess_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sales_cess')
    discount_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_sales_discount')

    shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
    shipping_tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tcs_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    payment_mode = models.CharField(max_length=200, blank=True, default='null', null=True)
    deposit_to = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_received = models.BooleanField(default=False)
    round_off = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tax = models.CharField(max_length=200, blank=True, default='null', null=True)
    grand_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    customer_note = models.TextField(blank=True, null=True)
    terms_condition =  models.TextField(blank=True, null=True)
    attach_file = models.FileField(default='null', blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_converted = models.BooleanField(default=False)
    TermsRefFullName = models.CharField(max_length=200, blank=True, default='null', null=True)
    TermsRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_is_converted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    class Meta:
        ordering = ('-created_date',)
        verbose_name_plural = 'Invoice'
        # ordering=('date')
    def __str__(self):
        return f"{self.invoice_serial} => {self.retail_invoice}"


# class InvoiceView(models.Model):
#     invoice_id = models.UUIDField(primary_key=True, default=uuid.uuid4)