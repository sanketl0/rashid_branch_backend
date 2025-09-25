import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
from coa.models import COA
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount,BaseTaxTotal
from .So_model import SO
EXT_TYPE = (
    ('TALLY','TALLY'),
)



class CreditNote(BaseTaxTotal, BaseDateid):
    cn_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True,
                                    related_name='customer_data')
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
    tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
    est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey("item.Item", on_delete=models.SET_NULL, null=True)
    pay_id = models.ForeignKey("salescustomer.PR", on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    reason = models.CharField(max_length=200, blank=True, default='null', null=True)
    subject = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=200, blank=True, null=True)
    received_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    received_date = models.DateTimeField(default=now, null=True)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    cn_date = models.DateTimeField(default=now, null=True)
    is_bank_transaction = models.BooleanField(default=False)
    party_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_party')
    sales_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_sales')
    coa_total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    igst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_igst')
    cgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_cgst')
    sgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_sgst')
    shipping_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_shipping')
    tcs_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_tcs')
    tds_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_tds')
    cess_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_cess')
    discount_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_cn_discount')
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_tax_name = models.CharField(max_length=50, blank=True, default='null', null=True)
    shipping_tax_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    tcs_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    invoice_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    customer_note = models.TextField(blank=True,  null=True)
    terms_condition = models.TextField(blank=True,  null=True)
    is_cn_converted = models.BooleanField(default=False)
    is_cn_generated = models.BooleanField(default=False)
    attach_file = models.FileField(default='null', blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, default='Open', null=True)
    cn_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    cn_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    cn_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_is_converted = models.BooleanField(default=False)
    is_converted = models.BooleanField(default=False)
    To_convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_is_converted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'Credit Note'
        ordering = ['-created_date']

    def __str__(self):
        return self.cn_serial