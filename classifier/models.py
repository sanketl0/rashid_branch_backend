from django.db import models
from salescustomer.BaseModel import BaseDateid
from company.models import Company
# Create your models here.

STATUS = (
    ('IDLE','IDLE'),
    ('PROCESSING','PROCESSING'),
    ('COMPLETED','COMPLETED')
)

DOC_TYPES = (
    ('INVOICE','INVOICE'),
    ('BILL','BILL'),

)


class Document(BaseDateid):
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL,blank=True, null=True,related_name='company_ocr_files')
    filename = models.CharField(max_length=200,blank=True,null=True)
    file = models.BinaryField()
    error = models.BooleanField(default=False)
    error_message = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=100, choices=STATUS, default='IDLE')
    document_type = models.CharField(max_length=20, blank=True, null=True, choices=DOC_TYPES)
    time_required = models.FloatField(default=0)
    resolution = models.CharField(max_length=10, default="0,0")