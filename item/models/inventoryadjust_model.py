from django.db import models
from company.models import Company, Branch,Company_Year
# from salescustomercustomer.models import salescustomerCustomer
from django.utils.timezone import now
import uuid
from salescustomer.BaseModel import BaseDateid

from item.models.item_model import Item

class InventoryAdjust(BaseDateid):
    invadj_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # customer_id = models.ForeignKey("salescustomer.SalesCustomer", on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    item_id = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    # user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    invadj_ref_no = models.CharField(max_length=200)
    item_code1 = models.CharField(max_length=200, blank=True, null=True)
    item_code2 = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    account = models.CharField(max_length=200, blank=True, null=True)
    exemption_reason = models.CharField(max_length=200, blank=True, null=True)
    branch_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    item_name = models.CharField(max_length=200, blank=True, null=True)
    quantity_available = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    new_quantity_on_hand = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    quantity_adjusted = models.IntegerField(blank=True, null=True)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    cost_price = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    current_value = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    changed_value = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjusted_value = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Inventory Adjustment'

    def __str__(self):
        return self.item_name
    

