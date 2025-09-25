from django.db import models
from salescustomer.BaseModel import BaseDateid, BaseTaxAmount
import uuid
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
    doc_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.CharField(max_length=200, blank=True, null=True)
    branch_id = models.CharField(max_length=200, blank=True, null=True)
    filename = models.CharField(max_length=200, blank=True, null=True)
    content = models.BinaryField()
    error = models.BooleanField(default=False)
    error_message = models.TextField(blank=True,null=True)
    time_required = models.FloatField(default=0)
    resolution = models.CharField(max_length=10, default="0,0")
    pages_count = models.SmallIntegerField(default=0)
    created = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    document_type = models.CharField(max_length=20, blank=True, null=True, choices=DOC_TYPES)
    status = models.CharField(max_length=100, choices=STATUS, default='IDLE')
    result = models.JSONField(default=dict)

    class Meta:
        ordering =[ '-created_date' ]
    def __str__(self):
        return self.filename
