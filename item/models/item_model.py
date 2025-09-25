from django.db import models
from company.models import Company, Branch,Company_Year
# from salescustomercustomer.models import salescustomerCustomer
from django.utils.timezone import now
import uuid
from salescustomer.BaseModel import BaseDateid
from purchase.models.Vendor_model import Vendor
import io
from salescustomer.models.Salescustomer_model import SalesCustomer
from coa.models import COA
from item.models.tax_name_model import TaxName
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from coa.models import Tax

EXT_TYPE = (
    ('TALLY','TALLY'),
)

class ItemGroup(BaseDateid):
    item_grp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200,blank=True,null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_groups')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)

    def __str__(self):
        return self.name

class ItemView(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200, default='null', blank=True, null=True)
    unit = models.CharField(max_length=200, default='null', blank=True, null=True)
    company_id =  models.UUIDField(blank=True, null=True,db_index=True)
    cost_price = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    item_category = models.CharField(max_length=200, blank=True, null=True)
    stock_quantity = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_view'

class Item(BaseDateid):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    item_grp_id = models.ForeignKey(ItemGroup, on_delete=models.SET_NULL, null=True, related_name='group_items')
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_items')
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    state_tax = models.ForeignKey('coa.Tax',on_delete=models.SET_NULL, null=True,blank=True,related_name='item_state_tax')
    central_tax = models.ForeignKey('coa.Tax',on_delete=models.SET_NULL, null=True,blank=True,related_name='item_central_tax')
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    est_id = models.ForeignKey(SalesCustomer, on_delete=models.SET_NULL, null=True, related_name='item_data')
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    coa_id = models.ForeignKey(COA, on_delete=models.SET_NULL, null=True)
    tax_id = models.ForeignKey(TaxName, on_delete=models.SET_NULL, null=True)
    ref_no = models.CharField(max_length=200, default='null', blank=True, null=True)
    item_category = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, default='null', blank=True, null=True)
    sku = models.CharField(max_length=200, default='null', blank=True, null=True)
    sac = models.CharField(max_length=200, default='null', blank=True, null=True)
    hsn_code = models.CharField(max_length=200, default='null', blank=True, null=True)
    unit = models.CharField(max_length=200, default='null', blank=True, null=True)
    alternate_unit = models.CharField(max_length=200, default='null', blank=True, null=True)
    unit_exchange_rate = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    category = models.CharField(max_length=200, default='null', blank=True, null=True)
    tax_preference = models.CharField(max_length=200, default='null', blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    sale_price = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    sales_account = models.CharField(max_length=200, default='null', blank=True, null=True)
    sale_description = models.TextField(blank=True, null=True)
    cost_price = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    purchase_account = models.CharField(max_length=200, default='null', blank=True, null=True)
    purchase_description = models.TextField(blank=True, null=True)
    inventory_account = models.CharField(max_length=200, default='null', blank=True, null=True)
    inter_rate = models.CharField(max_length=200, blank=True, null=True)
    intra_rate = models.CharField(max_length=200, blank=True, null=True)

    opening_stock = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    opening_stock_rate = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    reorder_point = models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    preferred_vendor = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    exemption_reason = models.TextField(blank=True, null=True)
    track_inventory= models.BooleanField(blank=True, null=True)
    full_inventory = models.BooleanField(default=False)
    total= models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True)
    qr_code = models.BinaryField(blank=True,null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    def __str__(self):
        return f"{self.name} "
    class Meta:
        # db_table = "item"
        verbose_name_plural = 'Item'
        ordering = ['-created_date']



@receiver(post_save,sender=Item)
def create_qrcode(sender,instance,created,**kwargs):
    if created:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(instance.item_id))
        qr.make(fit=True)
        image = qr.make_image(fill_color="black", back_color="white")
        with io.BytesIO() as byte_stream:
            image.save(byte_stream, format='PNG')  # You can change the format as needed
            image_bytes = byte_stream.getvalue()
            instance.qr_code = image_bytes
        instance.save()