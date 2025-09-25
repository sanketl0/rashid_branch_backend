from django.db import models
from company.models import Company, Branch,Company_Year
from item.models.item_model import Item
# from .models import *  # Invoice, SO, Estimate
from django.utils.timezone import now
import uuid

from salescustomer.BaseModel import BaseDateid,BaseTaxAmount, BaseTaxTotal

from .Vendor_model import Vendor
from .Bill_model import Bill
from .Paymentmade_model import PaymentMade

# class Multiple_Bill_Details(BaseDateid):
#     mul_bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor_paymentmade')
#     company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='company_paymentmade')
#     company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
#     bill_id = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, related_name='payments_made')
#     branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     pm_id = models.ForeignKey(PaymentMade, on_delete=models.SET_NULL, null=True, related_name='payments_made')
#     insert_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    
    
    
    
    
    
class Multiple_Bill_Details(BaseDateid):
    mul_bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    bill_id = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, related_name='payments_made')
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    pm_id = models.ForeignKey(PaymentMade, on_delete=models.SET_NULL, null=True, related_name='payments_made')
    insert_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)