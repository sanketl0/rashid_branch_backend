import uuid

from django.db import models
from coa.models import COA

from company.models import Company, Branch,Company_Year

from django.db.models.signals import post_save
from django.dispatch import receiver
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount
EXT_TYPE = (
    ('TALLY','TALLY'),
)

class SalesCustomer(BaseDateid):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    tcs_id = models.ForeignKey("salescustomer.TCS", on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    salutation = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_mobile = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_display_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    print_as_check_as = models.BooleanField(default=False)
    customer_contact = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_email = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_designation = models.CharField(max_length=200, blank=True, default='null', null=True)
    customer_department = models.CharField(max_length=200, blank=True, default='null', null=True)
    exemption_reason = models.CharField(max_length=200, blank=True, default='null', null=True)
    customerRefListId = models.CharField(max_length=200, blank=True, default='null', null=True)
    customerTypeRefListId = models.CharField(max_length=200, blank=True, default='null', null=True)
    customerTypeReffullName = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_subcustomer = models.BooleanField(default=False)
    parent_customer = models.CharField(max_length=200, blank=True, default='null', null=True)
    enable_portal = models.BooleanField(default=True)
    company_display_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    company_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    website = models.CharField(max_length=200, blank=True, default='null', null=True)
    opening_balance = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, default='null', null=True)
    set_credit_limit = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    gst_treatment = models.CharField(max_length=200, blank=True, default='null', null=True)
    gstin_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_preference = models.CharField(max_length=200, blank=True, default='null', null=True)
    cin_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    trn_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    vat_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    pan_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    b_attention = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_address1 = models.TextField(blank=True,null=True)
    bill_address2 =  models.TextField(blank=True,null=True)
    bill_address_city = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_address_state = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_address_postal_code = models.BigIntegerField(null=True, blank=True)
    bill_address_country = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_contact_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    bill_fax_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    s_attention = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_address1 = models.TextField(blank=True,null=True)
    ship_address2 =models.TextField(blank=True,null=True)
    ship_address_city = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_address_state = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_address_postal_code = models.BigIntegerField(null=True, blank=True)
    ship_address_country = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_contact_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    ship_fax_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    supply_place = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_salutation = models.CharField(max_length=200, default='null', null=True, blank=True)
    contact_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_phone = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_mobile = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    contact_designation = models.CharField(max_length=200, blank=True, default='null', null=True)
    contact_department = models.CharField(max_length=200, blank=True, default='null', null=True)
    remarks = models.TextField(blank=True,null=True)
    term_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    no_of_days = models.IntegerField(blank=True, default=0, null=True)
    is_verified=models.BooleanField(default=False)
    invoice_template=models.FileField(default='null', blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'customer'
        ordering=['-created_date']

    def __str__(self):
        return self.customer_name

class CustomerTcs(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer_name =  models.CharField(max_length=200, blank=True, default='null', null=True)
    tcs_id =  models.CharField(max_length=50, blank=True, default='null', null=True)
    company_id = models.CharField(max_length=50, blank=True, default='null', null=True)
    branch_id = models.CharField(max_length=100, blank=True, default='null', null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    is_valid = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'customer_tcs'


@receiver(post_save, sender=SalesCustomer)
def create_coa_post_save(sender, instance,created, **kwargs):
    if created:
        obj = COA.objects.create(
            account_head="Current Assets",
            account_subhead="Sundry Debtors",
            account_name=instance.customer_name,
            account_type="Assets",
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
        coa.account_name = instance.customer_name
        coa.save()