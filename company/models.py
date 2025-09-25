import uuid
from salescustomer.BaseModel import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from datetime import datetime

EXT_TYPE = (
    ('TALLY','TALLY'),
)
# Create your models here.
class Company(BaseDateid):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey('registration.user', on_delete=models.SET_NULL, blank=True, null=True,related_name='user_companies')
    trial_company = models.CharField(max_length=200, blank=True, default='null', null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY',choices=EXT_TYPE)
    company_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    alias_name = models.CharField(max_length=200, blank=True, default='null', null=True)
    address = models.CharField(max_length=200, blank=True, default='null', null=True)
    locality = models.CharField(max_length=200, blank=True, default='null', null=True)
    landmark = models.CharField(max_length=200, blank=True, default='null', null=True)
    pincode = models.BigIntegerField(blank=True, default=0, null=True)
    city = models.CharField(max_length=200, blank=True, default='null', null=True)
    state = models.CharField(max_length=200, blank=True, default='null', null=True)
    other = models.CharField(max_length=200, blank=True, default='null', null=True)
    is_primary = models.BooleanField(default=True, null=True)
    primary_phone_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    primary_mobile_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    primary_alternate_number = models.CharField(max_length=200, blank=True, default='null', null=True)

    primary_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    secondary_phone_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    secondary_mobile_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    secondary_alternate_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    secondary_email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    website = models.CharField(max_length=200, blank=True, default='null', null=True)
    books_start_date = models.DateField(blank=True, null=True)
    method = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_type = models.CharField(max_length=200, blank=True, default='null', null=True)
    pan_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    gstin = models.CharField(max_length=200, blank=True, default='null', null=True)
    cin = models.CharField(max_length=200, blank=True, default='null', null=True)
    other_registration_number = models.CharField(max_length=200, blank=True, default='null', null=True)
    password = models.CharField(max_length=200, blank=True, default='null', null=True)
    security_control = models.CharField(max_length=200, blank=True, default='null', null=True)
    audit_feature = models.CharField(max_length=200, blank=True, default='null', null=True)
    logo_image = models.ImageField(upload_to='logo/', height_field=None, width_field=None, max_length=None, blank=True,
                                   default='null', null=True)
    report_basis = models.CharField(max_length=200, blank=True, default='null', null=True)
    company_edit_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    tax_edit_id = models.CharField(max_length=200, blank=True, default='null', null=True)
    separate_payment_address = models.CharField(max_length=200, blank=True, default=False, null=True)
    address_receive_payment = models.TextField(default='null', null=True, blank=True, )
    is_new_company = models.BooleanField(default=False, null=True)
    is_copied_coa = models.BooleanField(default=False, null=True)
    financial_year=models.CharField(max_length=200, blank=True, default=False, null=True)
    invoice_sequence = models.BigIntegerField(default=1)
    country = models.CharField(max_length=200,default="India")
    currency_symbol = models.CharField(max_length=200,default="₹")
    currency = models.CharField(max_length=200 ,default="inr")
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    # latest = models.BooleanField(default=False)

    class Meta:
        db_table = "company"
        verbose_name_plural = 'company'
        ordering= ['-created_date']

    def __str__(self):
        if self.company_name:
            return f"{self.company_name} - {self.financial_year}"

    def get_logo_url(self):
        if self.logo_image:
            return self.logo_image.url

    def get_financial_year_start(self):
        # Get current year if no financial year is provided
        fy = self.financial_year
        if fy is None:
            year = datetime.now().year
            if datetime.now().month < 4:  # Assuming FY starts in April
                fy_start_year = year - 1
            else:
                fy_start_year = year
        else:
            fy_start_year, _ = map(int, fy.split('-'))

        # Financial year starts in April, so set the start date
        fy_start_date = datetime(fy_start_year, 4, 1)
        return fy_start_date

class Branch(BaseDateid):
    branch_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,related_name='company_branches')
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    main_branch = models.BooleanField(default=False)
    branch_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=200, blank=True, default='null', null=True)
    email = models.EmailField(max_length=200, blank=True, default='null', null=True)
    phone = models.CharField(max_length=200, blank=True, default='null', null=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    primary_contact = models.CharField(max_length=200, blank=True, default='null', null=True)
    state = models.CharField(max_length=200, blank=True, default='null', null=True)
    transaction_series = models.CharField(max_length=200, blank=True, default='null', null=True)
    website = models.CharField(max_length=200, blank=True, default='null', null=True)
    gstin = models.CharField(max_length=200, blank=True, default='null', null=True)

    class Meta:
        verbose_name_plural = 'branch'
        ordering = ['-created_date']

    # def __str__(self):
    #     return f"{self.company_name} => {self.branch_name}"


class FinancialYear(BaseDateid):
    fy_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    financial_start_date = models.DateField(blank=True, null=True)
    financial_end_date = models.DateField(blank=True, null=True)
    is_year_started = models.BooleanField(default=False, null=True)
    is_year_closed = models.BooleanField(default=False, null=True)
    Financial_year_close = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name_plural = 'Financial Year'




class Company_Year(BaseDateid):
    comp_yearid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

@receiver(post_save, sender=Branch)
def update_company_name(sender, instance, created, **kwargs):
    if created:
        instance.company_name = instance.company_id.company_name

@receiver(post_save, sender=Company)
def create_main_branch(sender, instance, created, **kwargs):
    if created and instance.is_new_company:
        print("creating new branch main")
        branch = Branch.objects.create(
            company_name=instance.company_name,
            company_id=instance,
            branch_name='Main Branch',
            main_branch=True,
            address=instance.address,
            city=instance.city,
            email=instance.primary_email,
            phone=instance.primary_phone_number,
            pincode=instance.pincode,
            primary_contact=instance.primary_mobile_number,
            state=instance.state,
            website=instance.website,
            gstin=instance.gstin
        )
        user = instance.user
        if user:
            access = user.user_access.all()[0]
            print("adding branch to access")
            access.branches.add(branch)



class Defaults(BaseDateid):
    def_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    exchange_rate = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    enable_cess = models.BooleanField(blank=False, null=True)
    enable_batch = models.BooleanField(blank=False, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='branch_default')
    company_id =  models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_default')


    class Meta:
        ordering = ['-created_date']