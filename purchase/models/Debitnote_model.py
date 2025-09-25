from django.db import models
from company.models import Company, Branch,Company_Year
from item.models.item_model import Item# from .models import *  # Invoice, SO, Estimate
from django.utils.timezone import now
import uuid
from coa.models import COA
from salescustomer.BaseModel import BaseDateid,BaseTaxAmount,BaseTaxTotal

EXT_TYPE = (
    ('TALLY','TALLY'),
)




class DebitNote(BaseDateid,BaseTaxTotal,BaseTaxAmount):  # BaseTaxTotal):
    dn_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # customer_id=models.ForeignKey("sales.Customer", on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    # emp_id=models.ForeignKey("sales.Employee", on_delete=models.SET_NULL, null=True)
    vendor_id = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True, related_name="ven_debitnote")
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    bill_id = models.ForeignKey("purchase.Bill", on_delete=models.SET_NULL, null=True)
    source_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    supply_destination = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    order_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    dn_date = models.DateTimeField(default=now, null=True)
    batch = models.BooleanField(default=False)
    discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    entered_discount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_gst = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    terms_condition = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_dn_converted = models.BooleanField(default=False)
    is_dn_generated = models.BooleanField(default=False)
    dn_status = models.CharField(max_length=200, blank=True, default='null', null=True)
    dn_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    dn_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    convt_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    attach_file = models.FileField(max_length=200, blank=True, default='null', null=True)
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
    party_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_party')
    purchase_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_purchase')
    coa_total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total_charges = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    discount_type = models.CharField(max_length=200, blank=True, null=True)
    igst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_igst')
    cgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_cgst')
    sgst_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_sgst')
    shipping_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_shipping')
    tcs_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_tcs')
    tds_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_tds')
    cess_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_cess')
    discount_account = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True, related_name='coa_dn_discount')

    class Meta:
        verbose_name_plural = 'Debit Note'
        ordering=['-created_date']




class DebitNoteView(models.Model):
    dn_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    branch_id = models.CharField(max_length=200, blank=True, default='null', null=True)

    vendor_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    dn_date = models.DateField(blank=True, null=True)

    dn_serial = models.CharField(max_length=200, blank=True, default='null', null=True)
    dn_ref_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    order_no = models.CharField(max_length=200, blank=True, default='null', null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    balance_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    dn_status = models.CharField(max_length=200, blank=True, default='null', null=True)


    class Meta:
        managed = False
        db_table = 'debit_note_view'