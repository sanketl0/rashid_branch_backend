from django.db import models
import uuid
class BaseTaxTotal(models.Model):
    cgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    sgst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    igst_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    
    class Meta:
        abstract=True

class BaseTaxAmount(models.Model):
    cgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    sgst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    igst_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
   
    class Meta:
        abstract=True


class BaseDateid(models.Model):
    created_id = models.CharField(max_length=50, blank=True, default='null', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_id = models.CharField(max_length=50, blank=True, default='null', null=True)
    modified_date =models.DateTimeField(auto_now=True, null=True)
    deleted_id = models.CharField(max_length=50, blank=True, default='null', null=True)
    deleted_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract=True





