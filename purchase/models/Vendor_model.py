from django.db import models
from company.models import Company, Branch,Company_Year
from coa.models import COA
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from salescustomer.BaseModel import BaseDateid,BaseTaxTotal,BaseTaxAmount

EXT_TYPE = (
    ('TALLY','TALLY'),
)


class Vendor(BaseDateid):
    vendor_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_vendor')
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    tds_id = models.ForeignKey("purchase.TDS", on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    salutation = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_mobile = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_display_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    # print_as_check_as = models.BooleanField()
    vendor_contact = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_email = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_designation = models.CharField(max_length=200, blank=True, default='null', null=True)
    vendor_department = models.CharField(max_length=200, blank=True, default='null', null=True)
    # vendorTypeRefListId = models.CharField(max_length=50, blank=True, default='null', null=True)
    # vendorTypeReffullName = models.CharField(max_length=50, blank=True, default='null', null=True)    
    parent_vendor = models.CharField(max_length=200, blank=True, default='null', null=True)
    enable_portal = models.BooleanField(default=False)
    company_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_display_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    company_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    website = models.CharField(max_length=200, blank=True, default='null', null=True)
    opening_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, default='null', null=True)
    payment_terms = models.CharField(max_length=200, blank=True, default='null', null=True)
    term_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    no_of_days = models.IntegerField(default=0)
    set_credit_limit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    gst_treatment = models.CharField(max_length=200, blank=True, default='null', null=True)
    gstin_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_preference = models.CharField(max_length=200, blank=True, default='null', null=True)
    tds = models.CharField(max_length=200, blank=True, default='null', null=True)
    cin_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    trn_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    vat_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    pan_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    b_attention = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_address1 = models.TextField(blank=True, null=True)
    bill_address2 = models.TextField(blank=True, null=True)
    bill_address_city = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_address_state = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_address_postal_code = models.BigIntegerField(null=True, blank=True)
    bill_address_country = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_contact_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_fax_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    # BillingRateRefListID=models.CharField(max_length=50, blank=True, default='null', null=True)
    # BillingRateRefFullName=models.CharField(max_length=50, blank=True, default='null', null=True)
    s_attention = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_address1 = models.TextField(blank=True, null=True)
    ship_address2 = models.TextField(blank=True, null=True)
    ship_address_city = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_address_state = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_address_postal_code = models.BigIntegerField(null=True, blank=True)
    ship_address_country = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_contact_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_fax_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    source_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_prefrances = models.CharField(max_length=200, blank=True, default='null', null=True)
    exemption_reason = models.CharField(max_length=200, blank=True, default='null', null=True)
    remarks = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_verified=models.BooleanField(default=False)
    bill_template=models.FileField(default='null', blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'Vendor'
        ordering = ['-created_date']

    def __str__(self):
        return self.vendor_name

class VendorTds(models.Model):
    vendor_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    vendor_name =  models.CharField(max_length=200, blank=True, default='null', null=True)
    tds_id =  models.CharField(max_length=200, blank=True, default='null', null=True)
    company_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    branch_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    is_valid = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'vendor_tds'


@receiver(post_save, sender=Vendor)
def create_coa_post_save(sender, instance,created, **kwargs):
    if created:
        obj = COA.objects.create(
            account_head="Current Liabilities",
            account_subhead="Sundry Creditors",
            account_name=instance.vendor_name,
            account_type="Liabilities",
            isdefault=False,
            ext_id=instance.ext_id,
            ext_type=instance.ext_type,
            company_id=instance.company_id,
            branch_id=instance.branch_id
        )
        instance.coa_id = obj
        instance.save()
    else:
        coa = instance.coa_id
        coa.account_name = instance.vendor_name
        coa.save()