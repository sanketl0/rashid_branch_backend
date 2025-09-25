import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager,GroupManager
from django.contrib.auth.models import PermissionsMixin
from company.models import Company,Branch
#from httplib2 import Response
from datetime import date,timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
#Create your models here.
#Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=255)
#    created_by=models.ForeignKey(user, on_delete=models.SET_NULL, null=True)      
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.name
    class Meta:
        verbose_name_plural = 'Role'     
    def __str__(self):
        return str(self.name)



#custom user
class MyUserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("email required")
        if not username:
            raise ValueError("username required")

        user=self.model(
            email=self.normalize_email(email),
            username=username)

        user.set_password(password)
        user.save(using=self.db)
        return user 

    def create_superuser(self,email,username,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,)
        
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self.db)
        return user
        
class user(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(verbose_name="full_name",max_length=2250)
    email=models.EmailField(verbose_name="email",max_length=22250,unique=True)
    username=models.CharField(max_length=2250,unique=True)
    mobile_no=models.CharField(max_length=2250,unique=True)
    is_activated = models.BooleanField(default=False)#registration field
    is_activate = models.BooleanField(default=False)#after registration email status field
    is_subscribed = models.BooleanField(default=False) 
    activation_code = models.CharField(max_length=2250, blank=True,  default='null', null=True)
    forgot_pass_code = models.CharField(max_length=2250, blank=True,  default='null', null=True)
    forgot_pass_time = models.DateTimeField(null=True)
    last_password_change = models.DateTimeField(null=True)
    forgot_password_is_active=models.BooleanField(default=False)# To deactivate link after forgot password done
    forgot_password_reset_secret_key = models.CharField(max_length=16, null=True)
    forgot_password_reset_secret_time = models.DateTimeField(null=True)
   # forgot_password_token = models.CharField(max_length=2250)
    is_on_trial = models.CharField(max_length=10, blank=True,  default='null', null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    trial_expiry_date = models.DateField(blank=True, null=True)
    dob=models.DateField(blank=True, null=True)
    company = models.CharField(max_length=250, blank=True, default='null', null=True)
    industry = models.CharField(max_length=250, blank=True, default='null', null=True)
    country = models.CharField(max_length=250, blank=True, default='null', null=True)
    role = models.CharField(max_length=200,default='admin')
    gender = models.CharField(max_length=250, blank=True, default='null', null=True)
    district = models.CharField(max_length=250, blank=True, default='null', null=True)
    username = models.CharField(max_length=250, blank=True, default='null', null=True)
    department = models.CharField(max_length=250, blank=True, default='null', null=True)
    designation = models.CharField(max_length=250, blank=True, default='null', null=True)
    image = models.ImageField(default='image', blank=True, null=True)
    provider=models.CharField(max_length=250, blank=True, default='null', null=True)
    address = models.CharField(max_length=100, blank=True, default='null', null=True)    
    pincode = models.BigIntegerField(blank=True, default=0, null=True)
    city = models.CharField(max_length=250, blank=True, default='null', null=True)
    state = models.CharField(max_length=250, blank=True, default='null', null=True)    
    created_id = models.CharField(max_length=250, blank=True, default='null', null=True)
    created_date = models.DateTimeField(auto_now_add=True)#add current time in minute to the database table
    modified_id = models.CharField(max_length=250, blank=True, default='null', null=True)
    modified_date = models.DateTimeField(auto_now=True)# it adds the time that is currently updated
    deleted_id = models.CharField(max_length=250, blank=True, default='null', null=True)
    deleted_date = models.DateTimeField(auto_now=True)
  #  role=models.CharField(max_length=250)
    
    country=models.CharField(max_length=250)
    password = models.CharField(max_length=250, blank=True,  default='null', null=True)
    sub_users = models.ManyToManyField('self',blank=True)
  #  permissions=models.ManyToManyField(Permission)
   # role=models.ForeignKey(Role,on_delete=models.CASCADE, null=True)
    date_joined=models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last_login", auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username',]

    objects=MyUserManager()


    def __str__ (self):
        return self.email


    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

PLAN_CHOICES = (
    ("MONTHLY", "MONTHLY"),
    ("3 MONTHS", "3 MONTHS"),
    ("6 MONTHS", "6 MONTHS"),
    ("YEARLY", "YEARLY")
)

PAYMENT_STATUS_CHOICES = (
    ("APPROVED", "APPROVED"),
    ("DECLINED", "DECLINED"),
    ("PENDING", "PENDING"),

)

class UserAccess(models.Model):
    user = models.ForeignKey(user,blank=True,null=True,on_delete=models.SET_NULL,related_name='user_access')
    item = models.BooleanField(default=True)
    inventory = models.BooleanField(default=True)
    full_inventory = models.BooleanField(default=False)
    company = models.BooleanField(default=True)
    customer = models.BooleanField(default=True)
    estimate = models.BooleanField(default=True)
    so = models.BooleanField(default=True)
    dc = models.BooleanField(default=True)
    invoice = models.BooleanField(default=True)
    pr = models.BooleanField(default=True)
    cn = models.BooleanField(default=True)
    vendor = models.BooleanField(default=True)
    expense = models.BooleanField(default=True)
    po = models.BooleanField(default=True)
    bill = models.BooleanField(default=True)
    pm = models.BooleanField(default=True)
    dn = models.BooleanField(default=True)
    journal = models.BooleanField(default=True)
    coa = models.BooleanField(default=True)
    reconcilation = models.BooleanField(default=True)
    bank = models.BooleanField(default=True)
    ocr = models.BooleanField(default=True)
    profit_loss = models.BooleanField(default=True)
    balance = models.BooleanField(default=True)
    invoice_report = models.BooleanField(default=True)
    pr_report = models.BooleanField(default=True)
    bill_report = models.BooleanField(default=True)
    pm_report = models.BooleanField(default=True)
    sales_gst_report = models.BooleanField(default=True)
    purchase_gst_report = models.BooleanField(default=True)
    gstr_3b_report = models.BooleanField(default=True)
    gstr_2b_report = models.BooleanField(default=True)
    gstr_2a_report = models.BooleanField(default=True)
    inventory_report = models.BooleanField(default=True)
    inventory_valuation_report = models.BooleanField(default=True)
    day_book = models.BooleanField(default=True)
    cash_book = models.BooleanField(default=True)
    bank_book = models.BooleanField(default=True)
    audit = models.BooleanField(default=False)
    tally = models.BooleanField(default=True)
    filing = models.BooleanField(default=False)
    branches = models.ManyToManyField(Branch,blank=True)


    def __str__(self):
        if self.user:
            return f"{self.user.username} => {self.user.role}"

class UserAccessDb(models.Model):
    user_id = models.CharField(max_length=200,primary_key=True,default=1)
    item = models.BooleanField(default=True)
    inventory = models.BooleanField(default=True)
    full_inventory = models.BooleanField(default=False)
    company = models.BooleanField(default=True)
    customer = models.BooleanField(default=True)
    estimate = models.BooleanField(default=True)
    so = models.BooleanField(default=True)
    dc = models.BooleanField(default=True)
    invoice = models.BooleanField(default=True)
    pr = models.BooleanField(default=True)
    cn = models.BooleanField(default=True)
    vendor = models.BooleanField(default=True)
    expense = models.BooleanField(default=True)
    po = models.BooleanField(default=True)
    bill = models.BooleanField(default=True)
    pm = models.BooleanField(default=True)
    dn = models.BooleanField(default=True)
    journal = models.BooleanField(default=True)
    coa = models.BooleanField(default=True)
    reconcilation = models.BooleanField(default=True)
    bank = models.BooleanField(default=True)
    ocr = models.BooleanField(default=True)
    profit_loss = models.BooleanField(default=True)
    balance = models.BooleanField(default=True)
    invoice_report = models.BooleanField(default=True)
    pr_report = models.BooleanField(default=True)
    bill_report = models.BooleanField(default=True)
    pm_report = models.BooleanField(default=True)
    sales_gst_report = models.BooleanField(default=True)
    purchase_gst_report = models.BooleanField(default=True)
    gstr_3b_report = models.BooleanField(default=True)
    gstr_2b_report = models.BooleanField(default=True)
    gstr_2a_report = models.BooleanField(default=True)
    # inventory_report = models.BooleanField(default=True)
    inventory_valuation_report = models.BooleanField(default=True)
    day_book = models.BooleanField(default=True)
    cash_book = models.BooleanField(default=True)
    bank_book = models.BooleanField(default=True)
    audit = models.BooleanField(default=False)
    tally = models.BooleanField(default=True)
    filing = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'user_access_view'


    def __str__(self):
        if self.user:
            return f"{self.user.username} => {self.user.role}"

class Plan(models.Model):
    name = models.CharField(max_length=50,default="Free Plan")
    user = models.ForeignKey(user,blank=True, null=True, on_delete=models.SET_NULL, related_name='user_custom_plan')
    validity = models.IntegerField(default=0)
    billing_cycle = models.CharField(max_length=200, blank=True, null=True, choices=PLAN_CHOICES)
    price = models.FloatField(default=0)
    no_of_branches = models.PositiveIntegerField(default=0)
    items = models.BooleanField(default=True)
    customers = models.PositiveIntegerField(default=25)
    estimates = models.PositiveIntegerField(default=0)
    sales_orders = models.PositiveIntegerField(default=0)
    delivery_challans = models.PositiveIntegerField(default=0)
    invoices = models.PositiveIntegerField(default=500)
    prs = models.PositiveIntegerField(default=500)
    credit_notes = models.PositiveIntegerField(default=0)
    vendors = models.PositiveIntegerField(default=10)
    expenses = models.PositiveIntegerField(default=0)
    purchase_orders = models.PositiveIntegerField(default=0)
    bills = models.PositiveIntegerField(default=250)
    pms = models.PositiveIntegerField(default=250)
    debit_notes = models.PositiveIntegerField(default=0)
    filing = models.PositiveIntegerField(default=1000)
    journals = models.PositiveIntegerField(default=0)
    coas = models.BooleanField(default=True)
    banks = models.PositiveIntegerField(default=1)
    statements = models.PositiveIntegerField(default=1)
    profit_loss = models.BooleanField(default=False)
    balance_sheet = models.BooleanField(default=False)
    audit = models.BooleanField(default=False)
    invoice_details = models.BooleanField(default=True)
    pr_details = models.BooleanField(default=True)
    bill_details = models.BooleanField(default=True)
    pm_details = models.BooleanField(default=True)
    sales_gst = models.BooleanField(default=False)
    purchase_gst = models.BooleanField(default=False)
    gstr_3b = models.BooleanField(default=False)
    gstr_2b = models.BooleanField(default=False)
    gstr_2a = models.BooleanField(default=False)
    inventory = models.BooleanField(default=True)
    full_inventory = models.BooleanField(default=False)
    inventory_valuation = models.BooleanField(default=True)
    day_book = models.BooleanField(default=False)
    cash_book = models.BooleanField(default=False)
    bank_book = models.BooleanField(default=False)
    webapp = models.BooleanField(default=False)
    scanner = models.PositiveIntegerField(default=10)
    backup = models.BooleanField(default=False)
    tally = models.BooleanField(default=False)

    user_roles = models.PositiveIntegerField(default=1)
    company_branches = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Feature(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True, default=uuid.uuid4)
    plan_id = models.PositiveIntegerField(default=0)
    customer_remaining = models.PositiveIntegerField(default=0)
    vendor_remaining = models.PositiveIntegerField(default=0)
    invoice_remaining = models.PositiveIntegerField(default=0)
    bill_remaining = models.PositiveIntegerField(default=0)
    bank_remaining = models.PositiveIntegerField(default=0)
    cn_remaining = models.PositiveIntegerField(default=0)
    dc_remaining = models.PositiveIntegerField(default=0)
    dn_remaining = models.PositiveIntegerField(default=0)
    doc_remaining = models.PositiveIntegerField(default=0)
    po_remaining = models.PositiveIntegerField(default=0)
    estimates_remaining = models.PositiveIntegerField(default=0)
    expense_remaining = models.PositiveIntegerField(default=0)
    journal_remaining = models.PositiveIntegerField(default=0)
    pm_remaining = models.PositiveIntegerField(default=0)
    pr_remaining = models.PositiveIntegerField(default=0)
    so_remaining = models.PositiveIntegerField(default=0)
    statement_remaining = models.PositiveIntegerField(default=0)
    user_remaining = models.PositiveIntegerField(default=0)
    items = models.BooleanField(default=False)
    coas = models.BooleanField(default=False)
    profit_loss = models.BooleanField(default=False)
    balance_sheet = models.BooleanField(default=False)
    audit = models.BooleanField(default=False)
    invoice_details = models.BooleanField(default=False)
    pr_details = models.BooleanField(default=False)
    bill_details = models.BooleanField(default=False)
    pm_details = models.BooleanField(default=False)
    sales_gst = models.BooleanField(default=False)
    purchase_gst = models.BooleanField(default=False)
    gstr_3b = models.BooleanField(default=False)
    gstr_2b = models.BooleanField(default=False)
    gstr_2a = models.BooleanField(default=False)
    inventory = models.BooleanField(default=False)
    full_inventory = models.BooleanField(default=False)
    inventory_valuation = models.BooleanField(default=False)
    day_book = models.BooleanField(default=False)
    cash_book = models.BooleanField(default=False)
    bank_book = models.BooleanField(default=False)
    webapp = models.BooleanField(default=False)
    backup = models.BooleanField(default=False)
    tally = models.BooleanField(default=False)
    branch_remaining = models.PositiveIntegerField(default=0)
    filing_remaining = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'feature'



class RequestCall(models.Model):
    user = models.ForeignKey(user,blank=True, null=True, on_delete=models.SET_NULL, related_name='user_requests')
    message = models.TextField(blank=True,null=True)
    responded = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,
                                        null=True)

    class Meta:
        ordering = ['-created_date']


class Subscribe(models.Model):
    created_date = models.DateTimeField(auto_now_add=True,
                                        null=True)
    modified_id = models.CharField(max_length=50, blank=True, default='null', null=True)
    modified_date = models.DateTimeField(auto_now_add=True, null=True)  #
    subscriber_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    plan = models.ForeignKey(Plan, blank=True, null=True, on_delete=models.SET_NULL, related_name='plan_subscribe')
    company_id = models.ManyToManyField('company.Company',blank=True,related_name='subscribe_companies')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    user_id = models.OneToOneField(user,blank=True,null=True,on_delete=models.SET_NULL,related_name='subscribe')

    class Meta:
        db_table = "subscribe"
        verbose_name_plural = 'subscribe'
        ordering = ['-created_date']

    def __str__(self):
        if self.user_id:
            return f"{self.user_id.username} {self.plan.name} valid till {self.end_date}"
        return "no user"

    def check_service_valid(self,service):
        pass

    def get_plan_subscribe(self):
        today_date = date.today()
        if self.start_date and self.end_date:
            if self.start_date <= today_date <= self.end_date:
                return True
        return False

class SubscriptionOrder(models.Model):
    user = models.ForeignKey(user,blank=True,null=True,on_delete=models.SET_NULL)
    subscribe = models.ForeignKey(Subscribe,blank=True,null=True,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True,
                                        null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    modified_id = models.CharField(max_length=50, blank=True, default='null', null=True)
    payment_id = models.CharField(max_length=200,blank=True,null=True)
    signature_id = models.CharField(max_length=200,blank=True,null=True)
    order_id = models.CharField(max_length=200, null=False, blank=False)
    status = models.CharField(max_length=200,default='PENDING',choices=PAYMENT_STATUS_CHOICES)
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    currency = models.CharField(max_length=4,default="inr")
    total_price = models.FloatField(default=0)
    plan = models.ForeignKey(Plan, blank=True, null=True, on_delete=models.SET_NULL, related_name='plan_subscribe_order')

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.plan.name
    def get_end_date(self,paid_date):
        days = self.plan.validity
        return paid_date + timedelta(days=days)

#Table for feedback
class Feedback(models.Model):
    feedback_id = models.UUIDField(primary_key=True, default = uuid.uuid4) 
    full_name = models.CharField(max_length=250, blank=True, default='null', null=True)
    mobile_no = models.CharField(max_length=15, blank=True, default='null', null=True)
    email = models.EmailField(max_length=250, blank=True, default='null', null=True)
    dev_comment = models.CharField(max_length=250, blank=True, default='null', null=True)
    username = models.CharField(max_length=250, blank=True, default='null', null=True)
    description = models.CharField(max_length=250, blank=True, default='null', null=True)    
    is_subscribed = models.BooleanField(default=False)    
    country = models.CharField(max_length=250, blank=True, default='null', null=True) 
    user_id = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)       
    created_id = models.CharField(max_length=250, blank=True, default='null', null=True)
    created_date = models.DateTimeField(auto_now_add=True)#add current time in minute to the database table
    modified_id = models.CharField(max_length=250, blank=True, default='null', null=True)
    modified_date = models.DateTimeField(auto_now=True)# it adds the time that is currently updated
    deleted_id = models.CharField(max_length=250, blank=True, default='null', null=True)
    deleted_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Feedback"
        verbose_name_plural = 'feedback'     
    def __str__(self):
        return self.username



class UserDetails(models.Model):
    device=models.TextField(default="",max_length=100)
    device_type=models.TextField(default="",max_length=100)
    browser=models.CharField(default="",max_length=100)
    browser_family=models.CharField(default="",max_length=100)
    browser_version=models.CharField(default="",max_length=100)
    os_type=models.CharField(default="",max_length=100)
    os_family=models.CharField(default="",max_length=100)
    os_version=models.CharField(default="",max_length=100)
    ip=models.TextField(default="",max_length=100)

    def __str__(self):
       return self.device_type

######API For saving user details###############

#################################
class Company_Users(models.Model):
    User = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)  
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
       return self.User



@receiver(post_save, sender=user)
def create_subscribe(sender, instance,created, **kwargs):
    if created and instance.role=='admin':
        plan = Plan.objects.get(name='Free Plan')
        start_date = date.today()
        end_date = start_date + timedelta(days=plan.validity)
        sub = Subscribe.objects.create(
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            user_id=instance

        )

@receiver(post_save, sender=user)
def create_access(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'admin':
            UserAccess.objects.create(
                user=instance
            )

@receiver(post_save, sender=Plan)
def update_access(sender, instance, created, **kwargs):
    pass
