from django.db import models
from company.models import Company, Branch,Company_Year
# from salescustomercustomer.models import salescustomerCustomer
from django.utils.timezone import now
import uuid
from salescustomer.BaseModel import BaseDateid
from salescustomer.models.Salescustomer_model import SalesCustomer
from item.models.tax_name_model import TaxName
from item.models.item_model import Item
from salescustomer.models.Estimate_model import Estimate
from salescustomer.models.So_model import SO
from salescustomer.models.Invoice_model import Invoice
from salescustomer.models.Recurringinvoice_model import RI
from salescustomer.models.Dc_model import DC
from salescustomer.models.Creditnote_model import CreditNote
class ItemDetails(BaseDateid):
    item_details_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer_id = models.ForeignKey(SalesCustomer, on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    branch_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    tax_id = models.ForeignKey(TaxName, on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    is_estimate_generated = models.BooleanField(blank=False, null=True)
    est_id = models.ForeignKey(Estimate, on_delete=models.SET_NULL, null=True)
    est_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    est_ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    is_so_generated = models.BooleanField(blank=False, null=True)
    so_id = models.ForeignKey(SO, on_delete=models.SET_NULL, null=True)
    so_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    so_ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    is_dc_generated = models.BooleanField(blank=True, null=True)
    dc_id = models.ForeignKey(DC, on_delete=models.SET_NULL, null=True)
    dc_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    dc_ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    is_invoice_generated = models.BooleanField(blank=False, null=True)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    invoice_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    invoice_ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    is_ri_generated = models.BooleanField(blank=False, null=True)
    is_enable = models.BooleanField(blank=False, null=True)
    ri_id = models.ForeignKey(RI, on_delete=models.SET_NULL, null=True)
    ri_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    ri_ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    is_crn_generated = models.BooleanField(blank=False, null=True)
    crn_id = models.ForeignKey(CreditNote, on_delete=models.SET_NULL, null=True)
    crn_serial = models.CharField(max_length=200, default='null', blank=True, null=True)
    crn_ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    exemption_reason = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Item Details'

    def __str__(self):
        return self.company_name