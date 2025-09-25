
import uuid

from django.db import models
from django.utils.timezone import now

from company.models import Company, Branch,Company_Year
# from item.models import Item
from salescustomer.BaseModel import BaseTaxTotal,BaseDateid


EXT_TYPE = (
    ('TALLY','TALLY'),
)
class DC(BaseTaxTotal, BaseDateid):
    dc_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    invoice_id = models.ForeignKey("salescustomer.Invoice", on_delete=models.SET_NULL, null=True,
                                   related_name='invoice_dc')
    so_id = models.ForeignKey("salescustomer.SO", on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
    est_id = models.ForeignKey("salescustomer.Estimate", on_delete=models.SET_NULL, null=True)
    emp_id = models.ForeignKey("salescustomer.Employee", on_delete=models.SET_NULL, null=True)
    tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    is_converted = models.BooleanField(default=False)
    is_dc_generated = models.BooleanField(default=False)
    customer_note = models.CharField(max_length=200, blank=True, default='null', null=True)
    dc_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    dc_date = models.DateTimeField(default=now, null=True)
    dc_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    dc_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    dc_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    terms_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    so_delete = models.CharField(max_length=200, blank=True, default='null', null=True)
    emp_role = models.CharField(max_length=200, blank=True, default='null', null=True)
    subject = models.CharField(max_length=200, blank=True, default='null', null=True)
    item_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_quantity = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    shipping_tax_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    shipping_tax_rate = models.PositiveIntegerField(default=0, blank=True, null=True)
    entered_shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjustment = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    round_off = models.IntegerField(default=0, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    terms_condition = models.CharField(max_length=200, blank=True, default='null', null=True)
    attach_file = models.FileField(default='null', blank=True, null=True)
    convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_converted = models.BooleanField(default=False)
    TxnID = models.CharField(max_length=200, blank=True, default='null', null=True)
    ClassRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    CustomerMsgRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    CustomerRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    CustomerSalesTaxCodeRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    ItemSalesTaxRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    SalesRepRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    ShipMethodRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    TemplateRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    TermsRefListID = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    From_is_converted = models.BooleanField(default=False)
    To_convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    To_is_converted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    class Meta:
        verbose_name_plural = 'Delivery Challan'
        ordering=['-created_date']

    def __str__(self):
        if self.company_id:
            return self.company_id.company_name
        return "No Name"
