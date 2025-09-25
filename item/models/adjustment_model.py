from django.db import models
from company.models import Company, Branch,Company_Year
# from salescustomercustomer.models import salescustomerCustomer
from django.utils.timezone import now
import uuid
from salescustomer.BaseModel import BaseDateid

EXT_TYPE = (
    ('TALLY','TALLY'),
)


class Adjustment(BaseDateid):
    adj_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    adj_type= models.CharField(max_length=200, default='null', blank=True, null=True)
    ref_no= models.CharField(max_length=200, default='null', blank=True, null=True)
    adj_date = models.DateField(blank=True, null=True)
    coa_id= models.ForeignKey("coa.COA", on_delete=models.SET_NULL, null=True)
    reason= models.CharField(max_length=200, default='null', blank=True, null=True)
    description= models.TextField(blank=True, null=True)
    ext_id = models.CharField(max_length=200, blank=True, null=True)
    ext_type = models.CharField(max_length=200, default='TALLY', choices=EXT_TYPE)
    attach_file = models.FileField(default='null', blank=True, null=True)
    status= models.CharField(max_length=200, default='null', blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    warehouse_id=models.CharField(max_length=200, default='null', blank=True, null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    adjusted_qty=models.IntegerField(default=0,null=True)
    changed_value= models.IntegerField(default=0,null=True)
    amount= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    rate= models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
    adjusted_value= models.IntegerField(default=0,null=True)
    current_value= models.IntegerField(default=0,null=True)
    created_by = models.CharField(max_length=200, blank=True, default='null', null=True)
    modified_by = models.CharField(max_length=200, blank=True, default='null', null=True)

    
    class Meta:
        verbose_name_plural = 'Adjustment'
        ordering =['-created_date']

    def __str__(self):
        if self.company_id:
            return self.company_id.company_name
